"""Strict offline SQLite launch journal for a fixed three-chat experiment.

The journal is local-only. It is never initialised during reservation and there
is deliberately no retry/reset operation. A reserved key is held even if the
caller crashes before receiving a confirmation. Never store it in Git.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
_SHA = re.compile(r"^[0-9a-f]{40}$")
_STATES = frozenset({"reserved", "posted", "effect_unknown", "blocked"})
_FINAL = frozenset({"posted", "effect_unknown", "blocked"})


class JournalError(ValueError):
    """Journal missing, corrupted, duplicate, conflicted or unsafe."""


@dataclass(frozen=True)
class LaunchStatus:
    state: str
    assignment_sha: str | None = None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _valid_key(run_id: str, next_step: int, sha: str | None = None) -> None:
    if not isinstance(run_id, str) or not _ID.fullmatch(run_id):
        raise JournalError("invalid run ID")
    if type(next_step) is not int or next_step not in (2, 3):
        raise JournalError("only successor steps 2 and 3 may be reserved")
    if sha is not None and (not isinstance(sha, str) or not _SHA.fullmatch(sha)):
        raise JournalError("assignment SHA must be full lowercase Git SHA")


def _connection(db: Path) -> sqlite3.Connection:
    # Explicit rw means a missing database is never silently recreated.
    if not db.is_file():
        raise JournalError("journal is missing; hold launch for operator inspection")
    try:
        conn = sqlite3.connect(db.resolve().as_uri() + "?mode=rw",
                               uri=True, timeout=5)
        conn.execute("PRAGMA busy_timeout=5000")
        conn.execute("PRAGMA synchronous=FULL")
        if conn.execute("PRAGMA quick_check").fetchone() != ("ok",):
            raise JournalError("journal integrity check failed")
        if conn.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone() != ("1",):
            raise JournalError("journal schema not initialised")
        conn.execute("SELECT run_id FROM launches LIMIT 1").fetchall()
        return conn
    except (sqlite3.Error, JournalError) as exc:
        if "conn" in locals():
            conn.close()
        raise JournalError(f"journal unreadable or invalid; hold launch: {exc}") from exc


def init_journal(db_path: str | Path) -> LaunchStatus:
    """Explicitly create an empty durable journal once; never overwrite an old one."""
    db = Path(db_path).expanduser()
    if not db.parent.is_dir():
        raise JournalError("journal directory does not exist")
    try:
        fd = os.open(db, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(fd)
    except FileExistsError as exc:
        raise JournalError("journal already exists; refusing to initialise again") from exc
    except OSError as exc:
        raise JournalError(f"cannot create journal: {exc}") from exc
    try:
        with closing(sqlite3.connect(db, timeout=5)) as conn:
            conn.execute("PRAGMA synchronous=FULL")
            with conn:
                conn.execute("CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
                conn.execute("INSERT INTO metadata VALUES ('schema_version', '1')")
                conn.execute(
                    "CREATE TABLE launches ("
                    "run_id TEXT NOT NULL, next_step INTEGER NOT NULL, "
                    "assignment_sha TEXT NOT NULL, state TEXT NOT NULL, "
                    "receipt_json TEXT, created_utc TEXT NOT NULL, "
                    "updated_utc TEXT NOT NULL, "
                    "PRIMARY KEY (run_id, next_step))"
                )
        with closing(_connection(db)):
            pass
        return LaunchStatus("initialised")
    except (sqlite3.Error, JournalError) as exc:
        # Deliberately leave any partially created DB present and held.
        raise JournalError(f"journal initialisation incomplete; operator inspection required: {exc}") from exc


def get_launch(db_path: str | Path, run_id: str, next_step: int) -> LaunchStatus | None:
    """Read-only status, with no private receipt contents returned."""
    with closing(_connection(Path(db_path))) as conn:
        row = conn.execute(
            "SELECT state, assignment_sha FROM launches WHERE run_id=? AND next_step=?",
            (run_id, next_step),
        ).fetchone()
        if row is None:
            return None
        if row[0] not in _STATES or not _SHA.fullmatch(row[1]):
            raise JournalError("invalid stored launch record")
        return LaunchStatus(*row)


def reserve_launch(
    db_path: str | Path, run_id: str, next_step: int, assignment_sha: str
) -> LaunchStatus:
    """Return reserved ONLY for first, atomic insert; later calls return held."""
    _valid_key(run_id, next_step, assignment_sha)
    with closing(_connection(Path(db_path))) as conn:
        try:
            with conn:
                conn.execute("BEGIN IMMEDIATE")
                row = conn.execute(
                    "SELECT state, assignment_sha FROM launches "
                    "WHERE run_id=? AND next_step=?",
                    (run_id, next_step),
                ).fetchone()
                if row is not None:
                    if row[1] != assignment_sha:
                        raise JournalError("launch key exists with different assignment SHA")
                    if row[0] not in _STATES:
                        raise JournalError("invalid previously stored launch state")
                    return LaunchStatus("held", assignment_sha)
                now = _now()
                conn.execute(
                    "INSERT INTO launches VALUES (?,?,?,?,?,?,?)",
                    (run_id, next_step, assignment_sha, "reserved", None, now, now),
                )
            return LaunchStatus("reserved", assignment_sha)
        except sqlite3.Error as exc:
            raise JournalError(f"reservation write failed, do not retry: {exc}") from exc


def record_launch_outcome(
    db_path: str | Path, run_id: str, next_step: int, assignment_sha: str,
    state: str, receipt: dict
) -> LaunchStatus:
    """Write one terminal observation; never alter existing final or unknown states."""
    _valid_key(run_id, next_step, assignment_sha)
    if state not in _FINAL:
        raise JournalError("invalid outcome state")
    if not isinstance(receipt, dict):
        raise JournalError("receipt must be a JSON object")
    payload = json.dumps(receipt, sort_keys=True, separators=(",", ":"))
    with closing(_connection(Path(db_path))) as conn:
        try:
            with conn:
                conn.execute("BEGIN IMMEDIATE")
                row = conn.execute(
                    "SELECT state, assignment_sha FROM launches "
                    "WHERE run_id=? AND next_step=?",
                    (run_id, next_step),
                ).fetchone()
                if row is None:
                    raise JournalError("cannot mark a launch that has not been reserved")
                if row[1] != assignment_sha:
                    raise JournalError("assignment changed after reservation")
                if row[0] != "reserved":
                    raise JournalError("launch record already final or held; no replacement")
                conn.execute(
                    "UPDATE launches SET state=?, receipt_json=?, updated_utc=? "
                    "WHERE run_id=? AND next_step=? AND state='reserved'",
                    (state, payload, _now(), run_id, next_step),
                )
            return LaunchStatus(state, assignment_sha)
        except sqlite3.Error as exc:
            raise JournalError(f"outcome write failed; reservation held: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Local-only, no-retry launch reservation journal")
    operations = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "reserve", "mark", "status"):
        operation = operations.add_parser(name)
        operation.add_argument("--db", required=True)
        if name != "init":
            operation.add_argument("--run", required=True)
            operation.add_argument("--step", type=int, required=True)
        if name in ("reserve", "mark"):
            operation.add_argument("--sha", required=True)
        if name == "mark":
            operation.add_argument("--state", required=True, choices=sorted(_FINAL))
            operation.add_argument("--receipt-json", default="{}")
            operation.add_argument("--receipt-file", default=None)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = init_journal(args.db)
        elif args.command == "reserve":
            result = reserve_launch(args.db, args.run, args.step, args.sha)
        elif args.command == "mark":
            if args.receipt_file:
                receipt_text = Path(args.receipt_file).read_text(encoding="utf-8")
            else:
                receipt_text = args.receipt_json
            result = record_launch_outcome(
                args.db, args.run, args.step, args.sha,
                args.state, json.loads(receipt_text),
            )
        else:
            result = get_launch(args.db, args.run, args.step)
            if result is None:
                print(json.dumps({"state": "absent"}))
                return 0
        print(json.dumps({"state": result.state}))
        return 4 if result.state == "held" else 0
    except (JournalError, json.JSONDecodeError) as exc:
        print(json.dumps({"state": "held", "error": str(exc)}))
        return 4


if __name__ == "__main__":
    sys.exit(main())
