"""Synthetic-only source receipts, coverage and crash-safe indexing ledger.

Implements Astra's proposed local foundation without a passive ChatGPT capture
adapter or real-history permissions. No network, model or plugin entrypoints.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from contextlib import closing

from .archive import _local_id, _normalise_sent_at


class CaptureBoundaryError(ValueError):
    """Invalid or out-of-scope source receipt."""


class CaptureConflict(CaptureBoundaryError):
    """A stable original identity has conflicting content or provenance."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _payload(local_id: str, role: str, exact_text: str) -> bytes:
    return json.dumps(
        {"local_id": local_id, "author_role": role, "exact_text": exact_text},
        sort_keys=True, ensure_ascii=False, separators=(",", ":"),
    ).encode("utf-8")


class SyntheticCaptureLedger:
    """Isolated source receipt ledger; NEVER authorises original personal history.

    The input is an *observed* synthetic receipt, not a verified native message.
    A second independent source comparison may promote the synthetic receipt to
    SOURCE_VERIFIED, without changing original text or time. An index worker must
    first reserve a pending item, then reconcile uncertain remote uploads before
    retrying. No method here uploads a file or sends a ChatGPT message.
    """

    FIELDS = ("local_id", "source_id", "conversation_id", "branch_id",
              "message_id", "version_id", "position", "author_role",
              "source_locator", "capture_method", "message_sent_at_source",
              "message_sent_at_utc", "observed_at_utc", "exact_text",
              "content_sha256", "supersedes_local_id")

    def __init__(self, path: str | Path):
        self.path = Path(path)
        if not self.path.is_file():
            raise FileNotFoundError("Capture ledger has not been initialised")

    @classmethod
    def initialise(cls, path: str | Path) -> "SyntheticCaptureLedger":
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with sqlite3.connect(path) as db:
            db.execute("PRAGMA foreign_keys=ON")
            db.executescript("""
                CREATE TABLE IF NOT EXISTS originals (
                    local_id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    conversation_id TEXT NOT NULL,
                    branch_id TEXT NOT NULL,
                    message_id TEXT NOT NULL,
                    version_id TEXT NOT NULL,
                    position INTEGER NOT NULL,
                    author_role TEXT NOT NULL CHECK(author_role IN ('user','assistant')),
                    source_locator TEXT NOT NULL,
                    capture_method TEXT NOT NULL,
                    message_sent_at_source TEXT,
                    message_sent_at_utc TEXT,
                    observed_at_utc TEXT,
                    exact_text TEXT NOT NULL,
                    content_sha256 TEXT NOT NULL,
                    supersedes_local_id TEXT,
                    ingested_at_utc TEXT NOT NULL,
                    source_status TEXT NOT NULL DEFAULT 'SOURCE_OBSERVED',
                    verification_ref TEXT,
                    UNIQUE(source_id, message_id, version_id)
                );
                CREATE TABLE IF NOT EXISTS index_outbox (
                    local_id TEXT PRIMARY KEY REFERENCES originals(local_id),
                    payload_sha256 TEXT NOT NULL,
                    state TEXT NOT NULL CHECK(state IN
                        ('PENDING','IN_FLIGHT','SEARCHABLE')),
                    provider_file_id TEXT UNIQUE,
                    reconciliation_ref TEXT
                );
                CREATE TABLE IF NOT EXISTS coverage (
                    source_id TEXT NOT NULL,
                    conversation_id TEXT NOT NULL,
                    branch_id TEXT NOT NULL,
                    position INTEGER NOT NULL,
                    state TEXT NOT NULL CHECK(state IN ('GAP_UNKNOWN','OBSERVED')),
                    note TEXT,
                    PRIMARY KEY(source_id,conversation_id,branch_id,position)
                );
                CREATE TABLE IF NOT EXISTS tombstones (
                    local_id TEXT PRIMARY KEY REFERENCES originals(local_id),
                    revoked_at_utc TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    remote_cleanup TEXT NOT NULL CHECK(remote_cleanup IN
                        ('NOT_REQUIRED','REQUIRED','EVIDENCE_LOGGED')),
                    remote_file_id TEXT,
                    remote_identity_ref TEXT,
                    remote_delete_ref TEXT
                );
                CREATE TABLE IF NOT EXISTS reconstructions (
                    note_id TEXT PRIMARY KEY,
                    exact_text TEXT NOT NULL,
                    content_sha256 TEXT NOT NULL,
                    created_at_utc TEXT NOT NULL,
                    fidelity TEXT NOT NULL CHECK(fidelity='MODEL_RECONSTRUCTION')
                );
            """)
        path.chmod(0o600)
        return cls(path)

    def _open(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        return db

    @classmethod
    def _validate(cls, receipt: dict) -> dict:
        if type(receipt) is not dict or receipt.get("synthetic_only") is not True:
            raise CaptureBoundaryError("Synthetic scope marker required")
        text = receipt.get("exact_text")
        if type(text) is not str or not text:
            raise CaptureBoundaryError("Non-empty original Unicode text required")
        for key in ("source_id", "conversation_id", "branch_id", "message_id",
                    "version_id", "source_locator"):
            if type(receipt.get(key)) is not str or not receipt[key]:
                raise CaptureBoundaryError("Missing source identity: " + key)
        if (not receipt["source_id"].startswith("synthetic-capture-")
            or not receipt["source_locator"].startswith("synthetic-capture://")
            or receipt.get("capture_method") != "synthetic_ui_observation"):
            raise CaptureBoundaryError("Real/unlabelled original-source capture denied")
        if receipt.get("author_role") not in ("user", "assistant"):
            raise CaptureBoundaryError("Only synthetic user and assistant roles allowed")
        pos = receipt.get("position")
        if type(pos) is not int or pos < 1:
            raise CaptureBoundaryError("Invalid branch-local position")
        if receipt.get("fidelity") not in (None, "SOURCE_OBSERVED"):
            raise CaptureBoundaryError("Verification cannot be claimed by a receipt")
        original, sent_utc = _normalise_sent_at(receipt.get("message_sent_at"))
        observed, observed_utc = _normalise_sent_at(receipt.get("observed_at"))
        correction = receipt.get("supersedes")
        target = None
        if correction is not None:
            if (type(correction) is not dict or
                any(type(correction.get(k)) is not str or not correction[k]
                    for k in ("message_id", "version_id"))):
                raise CaptureBoundaryError("Invalid correction identity")
            target = _local_id(receipt["source_id"], correction["message_id"],
                               correction["version_id"])
        local_id = _local_id(receipt["source_id"], receipt["message_id"],
                             receipt["version_id"])
        if local_id == target:
            raise CaptureBoundaryError("Source cannot supersede itself")
        return {
            "local_id": local_id,
            "source_id": receipt["source_id"],
            "conversation_id": receipt["conversation_id"],
            "branch_id": receipt["branch_id"],
            "message_id": receipt["message_id"],
            "version_id": receipt["version_id"],
            "position": pos,
            "author_role": receipt["author_role"],
            "source_locator": receipt["source_locator"],
            "capture_method": receipt["capture_method"],
            "message_sent_at_source": original,
            "message_sent_at_utc": sent_utc,
            "observed_at_utc": observed_utc,
            "exact_text": text,
            "content_sha256": _digest(text.encode("utf-8")),
            "supersedes_local_id": target,
        }

    def ingest(self, receipts: list[dict]) -> dict[str, int]:
        """Atomic batch: replay does not update originals or first ingestion time."""
        if type(receipts) is not list or not receipts:
            raise CaptureBoundaryError("Nonempty batch required")
        prepared = [self._validate(x) for x in receipts]
        inserted = 0
        with closing(self._open()) as db, db:
            for row in prepared:
                existing = db.execute("SELECT * FROM originals WHERE local_id=?",
                                      (row["local_id"],)).fetchone()
                if existing:
                    if any(existing[k] != row[k] for k in self.FIELDS):
                        raise CaptureConflict("Stable original identity changed")
                    continue
                occupied = db.execute(
                    """SELECT message_id FROM originals WHERE source_id=?
                       AND conversation_id=? AND branch_id=? AND position=? LIMIT 1""",
                    (row["source_id"], row["conversation_id"], row["branch_id"],
                     row["position"]),
                ).fetchone()
                if occupied and occupied["message_id"] != row["message_id"]:
                    raise CaptureConflict("Branch position already belongs to another message")
                if row["supersedes_local_id"]:
                    if db.execute("SELECT 1 FROM tombstones WHERE local_id=?",
                                  (row["supersedes_local_id"],)).fetchone():
                        raise CaptureBoundaryError("Correction target has been revoked")
                    prior = db.execute(
                        """SELECT source_id, conversation_id, branch_id, position
                           FROM originals WHERE local_id=?""",
                        (row["supersedes_local_id"],),
                    ).fetchone()
                    if (not prior or
                        any(prior[k] != row[k] for k in
                            ("source_id", "conversation_id", "branch_id")) or
                        prior["position"] > row["position"]):
                        raise CaptureBoundaryError("Correction target missing or cross-scope")
                values = {**row, "ingested_at_utc": _utc_now()}
                keys = (*self.FIELDS, "ingested_at_utc")
                db.execute(
                    f"INSERT INTO originals ({','.join(keys)}) VALUES ({','.join('?' for _ in keys)})",
                    tuple(values[k] for k in keys),
                )
                db.execute(
                    "INSERT INTO index_outbox(local_id,payload_sha256,state) VALUES (?,?,'PENDING')",
                    (row["local_id"], _digest(_payload(row["local_id"],
                                                      row["author_role"], row["exact_text"]))),
                )
                db.execute(
                    """INSERT INTO coverage(source_id,conversation_id,branch_id,
                       position,state,note) VALUES (?,?,?,?,'OBSERVED',NULL)
                       ON CONFLICT(source_id,conversation_id,branch_id,position)
                       DO UPDATE SET state='OBSERVED',note=NULL""",
                    (row["source_id"], row["conversation_id"], row["branch_id"],
                     row["position"]),
                )
                inserted += 1
        return {"inserted": inserted, "submitted": len(receipts)}

    def mark_gap(self, source: str, conversation: str, branch: str,
                 position: int, reason: str) -> None:
        """Explicit missing slot, never an inference from a high-water mark."""
        if (not all(type(x) is str and x for x in (source, conversation, branch, reason))
            or not source.startswith("synthetic-capture-")
            or type(position) is not int or position < 1):
            raise CaptureBoundaryError("Invalid synthetic gap report")
        with closing(self._open()) as db, db:
            row = db.execute(
                """SELECT state,note FROM coverage WHERE source_id=? AND
                   conversation_id=? AND branch_id=? AND position=?""",
                (source, conversation, branch, position),
            ).fetchone()
            if row:
                if row["state"] == "OBSERVED":
                    raise CaptureConflict("An observed source is not an unknown gap")
                if row["note"] != reason:
                    raise CaptureConflict("Changed gap declaration requires new evidence")
                return
            db.execute(
                "INSERT INTO coverage VALUES (?,?,?,?,'GAP_UNKNOWN',?)",
                (source, conversation, branch, position, reason),
            )

    def verify_synthetic(self, local_id: str, independent_bytes: bytes,
                         independent_source_ref: str) -> None:
        """Synthetic source reconciliation only; cannot attest a real account."""
        if (type(independent_bytes) is not bytes or
            type(independent_source_ref) is not str or not independent_source_ref):
            raise CaptureBoundaryError("Independent synthetic source evidence required")
        with closing(self._open()) as db, db:
            db.execute("BEGIN IMMEDIATE")
            if db.execute("SELECT 1 FROM tombstones WHERE local_id=?",
                          (local_id,)).fetchone():
                raise CaptureBoundaryError("Revoked source cannot be verified")
            row = db.execute("SELECT * FROM originals WHERE local_id=?",
                             (local_id,)).fetchone()
            if row is None or _digest(independent_bytes) != row["content_sha256"]:
                raise CaptureConflict("Independent source bytes do not match observed original")
            self._checked_index_payload(db, local_id)
            if row["verification_ref"] not in (None, independent_source_ref):
                raise CaptureConflict("Verification provenance changed")
            db.execute(
                """UPDATE originals SET source_status='SOURCE_VERIFIED',
                   verification_ref=? WHERE local_id=?""",
                (independent_source_ref, local_id),
            )

    @staticmethod
    def _check_source_identity(record) -> None:
        """Stored source/message/version must still identify the original row."""
        if _local_id(record["source_id"], record["message_id"],
                     record["version_id"]) != record["local_id"]:
            raise CaptureConflict("Stored source identity no longer matches canonical local ID")

    @staticmethod
    def _checked_index_payload(db: sqlite3.Connection, local_id: str):
        """Fail closed on canonical or outbox corruption before index transitions."""
        row = db.execute(
            """SELECT o.*,r.source_id,r.message_id,r.version_id,
                      r.author_role,r.exact_text,r.content_sha256
               FROM index_outbox o JOIN originals r USING(local_id)
               WHERE o.local_id=?""", (local_id,),
        ).fetchone()
        if row is None:
            raise CaptureConflict("Index original or outbox is missing")
        SyntheticCaptureLedger._check_source_identity(row)
        if _digest(row["exact_text"].encode("utf-8")) != row["content_sha256"]:
            raise CaptureConflict("Stored canonical original has changed")
        payload = _payload(row["local_id"], row["author_role"], row["exact_text"])
        if _digest(payload) != row["payload_sha256"]:
            raise CaptureConflict("Index outbox payload no longer matches original")
        return row, payload

    def reserve_index(self, local_id: str) -> dict:
        """Reserve BEFORE provider call; an interrupted reservation is uncertain."""
        with closing(self._open()) as db, db:
            cursor = db.execute(
                """UPDATE index_outbox SET state='IN_FLIGHT'
                   WHERE local_id=? AND state='PENDING'
                   AND NOT EXISTS(SELECT 1 FROM tombstones
                                  WHERE tombstones.local_id=index_outbox.local_id)""",
                (local_id,),
            )
            if cursor.rowcount != 1:
                raise CaptureBoundaryError("Not pending; remote reconciliation required")
            row, payload = self._checked_index_payload(db, local_id)
            return {"local_id": row["local_id"], "payload_sha256": row["payload_sha256"],
                    "payload": payload}

    def acknowledge_index(self, local_id: str, payload_sha256: str,
                          provider_file_id: str) -> None:
        if type(provider_file_id) is not str or not provider_file_id:
            raise CaptureBoundaryError("Provider identity is required")
        with closing(self._open()) as db, db:
            db.execute("BEGIN IMMEDIATE")
            if db.execute("SELECT 1 FROM tombstones WHERE local_id=?",
                          (local_id,)).fetchone():
                raise CaptureBoundaryError("Revoked source cannot become searchable")
            row, _ = self._checked_index_payload(db, local_id)
            if row["payload_sha256"] != payload_sha256:
                raise CaptureConflict("Index acknowledgement does not match source payload")
            if row["state"] == "SEARCHABLE":
                if row["provider_file_id"] != provider_file_id:
                    raise CaptureConflict("Indexed file identity changed")
                return
            if row["state"] != "IN_FLIGHT":
                raise CaptureBoundaryError("Cannot acknowledge an unreserved item")
            db.execute(
                "UPDATE index_outbox SET state='SEARCHABLE',provider_file_id=? WHERE local_id=?",
                (provider_file_id, local_id),
            )

    def remote_confirmed_absent(self, local_id: str, proof_ref: str) -> None:
        """Only an explicit provider check may requeue an uncertain upload."""
        if type(proof_ref) is not str or not proof_ref:
            raise CaptureBoundaryError("Provider absence proof required")
        with closing(self._open()) as db, db:
            changed = db.execute(
                """UPDATE index_outbox SET state='PENDING',reconciliation_ref=?
                   WHERE local_id=? AND state='IN_FLIGHT'
                   AND provider_file_id IS NULL
                   AND NOT EXISTS(SELECT 1 FROM tombstones
                                  WHERE tombstones.local_id=index_outbox.local_id)""",
                (proof_ref, local_id),
            ).rowcount
            if changed != 1:
                raise CaptureBoundaryError("No uncertain upload to reconcile")

    def revoke(self, local_id: str, reason: str) -> dict:
        """Durably suppress a synthetic original before any remote cleanup.

        Not a provider deletion, backup deletion, or genuine owner revocation
        workflow. An in-flight upload stays cleanup-required even if its remote
        identity is not yet known.
        """
        if (type(local_id) is not str or not local_id or
            type(reason) is not str or not reason.strip()):
            raise CaptureBoundaryError("Source identity and revocation reason required")
        with closing(self._open()) as db, db:
            existing = db.execute("SELECT * FROM tombstones WHERE local_id=?",
                                  (local_id,)).fetchone()
            if existing:
                if existing["reason"] != reason:
                    raise CaptureConflict("Revocation reason is immutable")
                return dict(existing)
            outbox = db.execute("SELECT * FROM index_outbox WHERE local_id=?",
                                (local_id,)).fetchone()
            if outbox is None:
                raise CaptureBoundaryError("Unknown original identity")
            state = ("NOT_REQUIRED" if outbox["state"] == "PENDING"
                     and not outbox["provider_file_id"] else "REQUIRED")
            db.execute(
                """INSERT INTO tombstones(local_id,revoked_at_utc,reason,
                   remote_cleanup,remote_file_id) VALUES (?,?,?,?,?)""",
                (local_id, _utc_now(), reason, state, outbox["provider_file_id"]),
            )
            return dict(db.execute("SELECT * FROM tombstones WHERE local_id=?",
                                   (local_id,)).fetchone())

    def record_revoked_remote_identity(self, local_id: str,
                                       provider_file_id: str,
                                       evidence_ref: str) -> None:
        """Log a supplied remote identity receipt; no provider call occurs."""
        if any(type(x) is not str or not x for x in
               (local_id, provider_file_id, evidence_ref)):
            raise CaptureBoundaryError("Remote identity and evidence required")
        with closing(self._open()) as db, db:
            entry = db.execute("SELECT * FROM tombstones WHERE local_id=?",
                               (local_id,)).fetchone()
            if entry is None:
                raise CaptureBoundaryError("Source is not revoked")
            if entry["remote_cleanup"] == "EVIDENCE_LOGGED":
                raise CaptureConflict("Previously logged delete receipt cannot be rewritten")
            if entry["remote_file_id"] not in (None, provider_file_id):
                raise CaptureConflict("Conflicting remote file identity")
            db.execute(
                """UPDATE tombstones SET remote_cleanup='REQUIRED',
                   remote_file_id=?,remote_identity_ref=?
                   WHERE local_id=?""",
                (provider_file_id, evidence_ref, local_id),
            )

    def record_remote_delete_evidence(self, local_id: str,
                                          provider_file_id: str,
                                          evidence_ref: str) -> None:
        """Log unverified deletion evidence; DOES NOT confirm provider cleanup."""
        if any(type(x) is not str or not x for x in
               (local_id, provider_file_id, evidence_ref)):
            raise CaptureBoundaryError("Remote delete evidence required")
        with closing(self._open()) as db, db:
            entry = db.execute("SELECT * FROM tombstones WHERE local_id=?",
                               (local_id,)).fetchone()
            if entry is None or entry["remote_cleanup"] == "NOT_REQUIRED":
                raise CaptureBoundaryError("No cleanup-required tombstone exists")
            if entry["remote_file_id"] != provider_file_id:
                raise CaptureConflict("Remote deletion cannot be matched to the original")
            if entry["remote_cleanup"] == "EVIDENCE_LOGGED":
                if entry["remote_delete_ref"] != evidence_ref:
                    raise CaptureConflict("Remote deletion evidence changed")
                return
            db.execute(
                """UPDATE tombstones SET remote_cleanup='EVIDENCE_LOGGED',
                   remote_delete_ref=? WHERE local_id=?""",
                (evidence_ref, local_id),
            )

    def revocation_status(self, local_id: str) -> dict | None:
        """Owner-side synthetic diagnostic. Not part of model source release."""
        with closing(self._open()) as db:
            row = db.execute("SELECT * FROM tombstones WHERE local_id=?",
                             (local_id,)).fetchone()
            return dict(row) if row else None

    def reconstruct(self, note_id: str, text: str) -> None:
        """Derived note is never an original and never enters the index outbox."""
        if (type(note_id) is not str or not note_id or
            type(text) is not str or not text):
            raise CaptureBoundaryError("Invalid reconstructed note")
        with closing(self._open()) as db, db:
            row = db.execute("SELECT content_sha256 FROM reconstructions WHERE note_id=?",
                             (note_id,)).fetchone()
            digest = _digest(text.encode("utf-8"))
            if row and row["content_sha256"] != digest:
                raise CaptureConflict("Reconstruction identity changed")
            if not row:
                db.execute(
                    "INSERT INTO reconstructions VALUES (?,?,?,?,'MODEL_RECONSTRUCTION')",
                    (note_id, text, digest, _utc_now()),
                )

    def snapshot(self, source: str, conversation: str, branch: str) -> dict:
        with closing(self._open()) as db, db:
            # Multiple SELECTs must observe one committed source/revocation
            # state; otherwise this view can mix pre/post-revocation records.
            db.execute("BEGIN")
            rows = [dict(r) for r in db.execute(
                """SELECT * FROM originals WHERE source_id=? AND conversation_id=?
                   AND branch_id=? AND NOT EXISTS(
                       SELECT 1 FROM tombstones t WHERE t.local_id=originals.local_id)
                   ORDER BY position,ingested_at_utc""",
                (source, conversation, branch),
            )]
            for record in rows:
                self._check_source_identity(record)
                if _digest(record["exact_text"].encode("utf-8")) != record["content_sha256"]:
                    raise CaptureConflict("Stored canonical original has changed")
            coverage = [dict(r) for r in db.execute(
                """SELECT position,state,note FROM coverage
                   WHERE source_id=? AND conversation_id=? AND branch_id=?
                   ORDER BY position""",
                (source, conversation, branch),
            )]
            # An OBSERVED slot cannot be claimed without an original at the
            # same source/conversation/branch/position, even when that original
            # is tombstoned. An identity mutation may otherwise hide the
            # corrupted row from the scoped read without hiding its coverage.
            positions = {r["position"] for r in db.execute(
                """SELECT position FROM originals WHERE source_id=?
                   AND conversation_id=? AND branch_id=?""",
                (source, conversation, branch),
            )}
            for slot in coverage:
                if slot["state"] == "OBSERVED" and slot["position"] not in positions:
                    raise CaptureConflict("Observed coverage has no scoped original")
            # The original position may have multiple edited versions. Mask
            # coverage only when *all* versions at that position are revoked.
            visible_positions = {r["position"] for r in rows}
            revoked_positions = {
                r["position"] for r in db.execute(
                    """SELECT r.position FROM originals r
                       JOIN tombstones t USING(local_id)
                       WHERE r.source_id=? AND r.conversation_id=?
                       AND r.branch_id=?""",
                    (source, conversation, branch))
            }
            for slot in coverage:
                if (slot["position"] in revoked_positions
                    and slot["position"] not in visible_positions):
                    slot.update(state="REVOKED", note=None)
            outbox = [dict(r) for r in db.execute(
                """SELECT o.local_id,o.state,o.payload_sha256,o.provider_file_id,o.reconciliation_ref
                   FROM index_outbox o JOIN originals r USING(local_id)
                   WHERE r.source_id=? AND r.conversation_id=? AND r.branch_id=?
                   AND NOT EXISTS(SELECT 1 FROM tombstones t
                                  WHERE t.local_id=r.local_id)
                   ORDER BY r.position""",
                (source, conversation, branch),
            )]
            indexed = {record["local_id"]: record for record in rows}
            for entry in outbox:
                original = indexed[entry["local_id"]]
                if _digest(_payload(original["local_id"], original["author_role"],
                                   original["exact_text"])) != entry["payload_sha256"]:
                    raise CaptureConflict("Index outbox payload no longer matches original")
            # A released correction must not expose a revoked predecessor's
            # canonical ID, nor keep a correction-graph edge to that predecessor.
            visible_ids = set(indexed)
            for row in rows:
                if (row["supersedes_local_id"] is not None and
                    row["supersedes_local_id"] not in visible_ids):
                    row["supersedes_local_id"] = None
                    row["predecessor_redacted"] = True
            corrections = {r["local_id"]: [p["local_id"] for p in rows
                           if p["supersedes_local_id"] == r["local_id"]] for r in rows}
            totals = db.execute(
                """SELECT COUNT(*) AS revoked,
                   COALESCE(SUM(t.remote_cleanup!='NOT_REQUIRED'),0) AS cleanup_pending
                   FROM tombstones t JOIN originals r USING(local_id)
                   WHERE r.source_id=? AND r.conversation_id=? AND r.branch_id=?""",
                (source, conversation, branch),
            ).fetchone()
            return {"synthetic_only": True, "capture_complete": False,
                    "originals": rows, "coverage": coverage, "outbox": outbox,
                    "corrected_by": corrections,
                    "revoked_count": totals["revoked"],
                    "remote_cleanup_pending_count": totals["cleanup_pending"]}
