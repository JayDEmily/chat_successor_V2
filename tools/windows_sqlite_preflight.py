"""Offline Windows Python/SQLite reservation capability probe.

TASK 1 ONLY: NOT the Task 2 launch journal. Tests a temporary reservation,
persistent readback and unique-key refusal. No browser or GitHub side effects.
"""
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path


def main():
    with tempfile.TemporaryDirectory(prefix="chat_succession_probe_") as tmp:
        db = Path(tmp) / "journal_probe.sqlite3"
        with closing(sqlite3.connect(db)) as connection:
            connection.execute(
                "CREATE TABLE launch (run_id TEXT, next_step INTEGER, "
                "assignment_sha TEXT NOT NULL, PRIMARY KEY (run_id, next_step))"
            )
            connection.execute(
                "INSERT INTO launch VALUES (?, ?, ?)",
                ("offline-probe", 2, "a" * 40),
            )
            connection.commit()
        with closing(sqlite3.connect(db)) as connection:
            row = connection.execute(
                "SELECT assignment_sha FROM launch WHERE run_id = ? AND next_step = ?",
                ("offline-probe", 2),
            ).fetchone()
            assert row == ("a" * 40,), "durable reservation readback mismatch"
            try:
                connection.execute(
                    "INSERT INTO launch VALUES (?, ?, ?)",
                    ("offline-probe", 2, "b" * 40),
                )
            except sqlite3.IntegrityError:
                connection.rollback()
            else:
                raise AssertionError("duplicate key was not rejected")
        print("PASS: Windows Python SQLite reserve/readback and duplicate-key refusal")
        print("NOTE: Task 2 journal and browser Send are NOT tested")


if __name__ == "__main__":
    main()
