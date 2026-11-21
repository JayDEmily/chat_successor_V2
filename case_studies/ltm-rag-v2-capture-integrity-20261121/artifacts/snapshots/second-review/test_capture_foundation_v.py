"""Offline synthetic-only acceptance for Astra capture foundation CF01-CF12."""
from __future__ import annotations

import hashlib
import sqlite3
import tempfile
import unittest
from pathlib import Path

from ltm_vnext.capture_foundation_v import (
    SyntheticCaptureLedger, CaptureBoundaryError, CaptureConflict,
)


class CaptureFoundationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="astra-capture-v-")
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "source.sqlite"
        self.ledger = SyntheticCaptureLedger.initialise(self.path)

    def receipt(self, n=1, *, message=None, position=None, branch="main", version="1",
                text=None, role="user", supersedes=None, sent=None):
        result = {
            "synthetic_only": True,
            "source_id": "synthetic-capture-cf",
            "conversation_id": "fictional-recovery",
            "branch_id": branch,
            "message_id": message or f"cf-{n:02d}",
            "version_id": version,
            "position": position or n,
            "author_role": role,
            "source_locator": f"synthetic-capture://fictional/{branch}/{n}",
            "capture_method": "synthetic_ui_observation",
            "exact_text": text if text is not None else f"Synthetic diary note {n}.",
            "message_sent_at": sent,
            "observed_at": None,
        }
        if supersedes is not None:
            result["supersedes"] = supersedes
        return result

    def snap(self, branch="main"):
        return self.ledger.snapshot("synthetic-capture-cf", "fictional-recovery", branch)

    def test_cf01_original_unicode_and_unknown_send_time(self):
        source = self.receipt(text="Original \u2018quote\u2019, line one.\nLine two \u2014 unchanged.")
        self.assertEqual(self.ledger.ingest([source]), {"inserted": 1, "submitted": 1})
        record = self.snap()["originals"][0]
        self.assertEqual(record["exact_text"], source["exact_text"])
        self.assertIsNone(record["message_sent_at_utc"])
        self.assertIsNotNone(record["ingested_at_utc"])
        self.assertEqual(record["author_role"], "user")
        self.assertEqual(record["content_sha256"],
                         hashlib.sha256(source["exact_text"].encode("utf-8")).hexdigest())

    def test_cf01_private_local_database_mode(self):
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)

    def test_cf09_corrupt_outbox_payload_never_accepted(self):
        self.ledger.ingest([self.receipt()])
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE index_outbox SET payload_sha256='mismatch'")
        with self.assertRaises(CaptureConflict):
            self.snap()

    def test_cf01_distinct_send_and_observed_timestamps(self):
        source = self.receipt(sent="2026-11-20T23:58:00+11:00")
        source["observed_at"] = "2026-11-20T13:00:00Z"
        self.ledger.ingest([source])
        row = self.snap()["originals"][0]
        self.assertEqual(row["message_sent_at_source"], source["message_sent_at"])
        self.assertEqual(row["message_sent_at_utc"], "2026-11-20T12:58:00.000000Z")
        self.assertEqual(row["observed_at_utc"], "2026-11-20T13:00:00.000000Z")
        self.assertNotEqual(row["message_sent_at_utc"], row["ingested_at_utc"])

    def test_cf02_atomic_batch_failure_no_partial_outbox_or_coverage(self):
        bad = self.receipt(2)
        bad["source_id"] = "real-history"
        with self.assertRaises(CaptureBoundaryError):
            self.ledger.ingest([self.receipt(1), bad])
        self.assertEqual(self.snap()["originals"], [])
        self.assertEqual(self.snap()["outbox"], [])
        self.assertEqual(self.snap()["coverage"], [])

    def test_cf02_atomic_correction_failure(self):
        first = self.receipt(1)
        second = self.receipt(2, supersedes={"message_id": "absent", "version_id": "1"})
        with self.assertRaises(CaptureBoundaryError):
            self.ledger.ingest([first, second])
        self.assertEqual(self.snap()["originals"], [])

    def test_cf03_idempotence_and_original_ingestion_time(self):
        source = self.receipt()
        self.ledger.ingest([source])
        before = self.snap()
        self.assertEqual(self.ledger.ingest([source, source])["inserted"], 0)
        self.assertEqual(self.snap()["originals"], before["originals"])
        self.assertEqual(self.snap()["outbox"], before["outbox"])
        changed = {**source, "exact_text": "tampered"}
        with self.assertRaises(CaptureConflict):
            self.ledger.ingest([changed])
        changed_role = {**source, "author_role": "assistant"}
        with self.assertRaises(CaptureConflict):
            self.ledger.ingest([changed_role])

    def test_cf04_same_text_distinct_identities_and_position_collision(self):
        first = self.receipt(1, text="yes")
        second = self.receipt(2, text="yes")
        self.assertEqual(self.ledger.ingest([first, second])["inserted"], 2)
        ids = [r["local_id"] for r in self.snap()["originals"]]
        self.assertEqual(len(set(ids)), 2)
        with self.assertRaises(CaptureConflict):
            self.ledger.ingest([self.receipt(3, position=1)])

    def test_cf05_correction_preserves_prior_and_rejects_cross_branch(self):
        first = self.receipt(1, text="Initial arrangement")
        correction = self.receipt(2, text="Corrected arrangement",
                                  supersedes={"message_id": first["message_id"],
                                              "version_id": "1"})
        self.ledger.ingest([first, correction])
        snapshot = self.snap()
        self.assertEqual(len(snapshot["originals"]), 2)
        self.assertEqual(snapshot["originals"][0]["exact_text"], "Initial arrangement")
        self.assertEqual(snapshot["originals"][1]["supersedes_local_id"],
                         snapshot["originals"][0]["local_id"])
        self.assertEqual(snapshot["corrected_by"][snapshot["originals"][0]["local_id"]],
                         [snapshot["originals"][1]["local_id"]])
        wrong = self.receipt(3, branch="other",
                             supersedes={"message_id": first["message_id"],
                                         "version_id": "1"})
        with self.assertRaises(CaptureBoundaryError):
            self.ledger.ingest([wrong])

    def test_cf06_branches_and_edited_message_version(self):
        old = self.receipt(1, message="editable", text="Old wording")
        edit = self.receipt(1, message="editable", version="2", text="Edited wording",
                            supersedes={"message_id": "editable", "version_id": "1"})
        alternative = self.receipt(1, branch="alternate", message="same-place",
                                   text="Unaccepted alternative")
        self.assertEqual(self.ledger.ingest([old, edit, alternative])["inserted"], 3)
        main = self.snap()["originals"]
        self.assertEqual({x["version_id"] for x in main}, {"1", "2"})
        self.assertEqual([x["branch_id"] for x in self.snap("alternate")["originals"]],
                         ["alternate"])

    def test_cf07_declared_gap_and_later_source_backfill(self):
        self.ledger.ingest([self.receipt(1)])
        self.ledger.mark_gap("synthetic-capture-cf", "fictional-recovery", "main", 2,
                             "host was offline")
        state = self.snap()
        self.assertFalse(state["capture_complete"])
        self.assertEqual(state["coverage"][1]["state"], "GAP_UNKNOWN")
        self.ledger.ingest([self.receipt(2)])
        state = self.snap()
        self.assertEqual(state["coverage"][1]["state"], "OBSERVED")
        self.assertFalse(state["capture_complete"])
        with self.assertRaises(CaptureConflict):
            self.ledger.mark_gap("synthetic-capture-cf", "fictional-recovery", "main",
                                 2, "fabricated loss")

    def test_cf08_uncertain_upload_requires_remote_reconciliation(self):
        self.ledger.ingest([self.receipt()])
        local_id = self.snap()["originals"][0]["local_id"]
        ticket = self.ledger.reserve_index(local_id)
        self.assertEqual(hashlib.sha256(ticket["payload"]).hexdigest(),
                         ticket["payload_sha256"])
        reopened = SyntheticCaptureLedger(self.path)
        with self.assertRaises(CaptureBoundaryError):
            reopened.reserve_index(local_id)
        with self.assertRaises(CaptureConflict):
            reopened.acknowledge_index(local_id, "wrong", "file-001")
        reopened.acknowledge_index(local_id, ticket["payload_sha256"], "file-001")
        reopened.acknowledge_index(local_id, ticket["payload_sha256"], "file-001")
        self.assertEqual(self.snap()["outbox"][0]["state"], "SEARCHABLE")
        with self.assertRaises(CaptureConflict):
            reopened.acknowledge_index(local_id, ticket["payload_sha256"], "file-002")

    def test_cf08_confirmed_remote_absence_allows_retry(self):
        self.ledger.ingest([self.receipt()])
        local_id = self.snap()["originals"][0]["local_id"]
        self.ledger.reserve_index(local_id)
        with self.assertRaises(CaptureBoundaryError):
            self.ledger.remote_confirmed_absent(local_id, "")
        self.ledger.remote_confirmed_absent(local_id, "synthetic-provider-listing-v1")
        self.assertEqual(self.snap()["outbox"][0]["state"], "PENDING")
        self.ledger.reserve_index(local_id)

    def test_cf09_observed_not_self_verified_and_reconstruction_separate(self):
        source = self.receipt(text="Wholly fictional original")
        source["fidelity"] = "SOURCE_VERIFIED"
        with self.assertRaises(CaptureBoundaryError):
            self.ledger.ingest([source])
        source["fidelity"] = "SOURCE_OBSERVED"
        self.ledger.ingest([source])
        local_id = self.snap()["originals"][0]["local_id"]
        with self.assertRaises(CaptureConflict):
            self.ledger.verify_synthetic(local_id, b"wrong", "source-2")
        self.ledger.verify_synthetic(local_id, source["exact_text"].encode("utf-8"),
                                     "independent-fictional-ui-readback")
        self.assertEqual(self.snap()["originals"][0]["source_status"], "SOURCE_VERIFIED")
        self.ledger.reconstruct("best-effort", "I remember something like a diary.")
        with sqlite3.connect(self.path) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM reconstructions").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM originals").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM index_outbox").fetchone()[0], 1)

    def test_cf08_requeue_proof_is_persisted(self):
        self.ledger.ingest([self.receipt()])
        local_id = self.snap()["originals"][0]["local_id"]
        self.ledger.reserve_index(local_id)
        self.ledger.remote_confirmed_absent(local_id, "synthetic-negative-provider-readback")
        self.assertEqual(self.snap()["outbox"][0]["reconciliation_ref"],
                         "synthetic-negative-provider-readback")

    def test_cf09_corrupt_original_never_released(self):
        self.ledger.ingest([self.receipt()])
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE originals SET exact_text='corrupted'")
        with self.assertRaises(CaptureConflict):
            self.snap()

    def test_index_reservation_refuses_corrupted_source_or_outbox_atomically(self):
        # The direct index writer must reject damage without requiring a
        # separate snapshot() call to detect it.
        for n, (table, field, value) in enumerate((
            ("originals", "exact_text", "altered source text"),
            ("originals", "author_role", "assistant"),
            ("originals", "content_sha256", "0" * 64),
            ("index_outbox", "payload_sha256", "0" * 64),
        ), start=30):
            with self.subTest(field=field):
                self.ledger.ingest([self.receipt(n)])
                with sqlite3.connect(self.path) as db:
                    local_id = db.execute(
                        "SELECT local_id FROM originals WHERE message_id=?",
                        (f"cf-{n:02d}",),
                    ).fetchone()[0]
                with sqlite3.connect(self.path) as db:
                    db.execute(f"UPDATE {table} SET {field}=? WHERE local_id=?",
                               (value, local_id))
                with self.assertRaises(CaptureConflict):
                    self.ledger.reserve_index(local_id)
                with sqlite3.connect(self.path) as db:
                    state, provider_id = db.execute(
                        "SELECT state,provider_file_id FROM index_outbox WHERE local_id=?",
                        (local_id,),
                    ).fetchone()
                self.assertEqual((state, provider_id), ("PENDING", None))

    def test_index_acknowledgement_refuses_late_source_corruption(self):
        # A valid ticket cannot make a subsequently damaged original searchable.
        for n, (table, field, value) in enumerate((
            ("originals", "exact_text", "altered after reservation"),
            ("originals", "author_role", "assistant"),
            ("originals", "content_sha256", "0" * 64),
            ("index_outbox", "payload_sha256", "0" * 64),
        ), start=40):
            with self.subTest(field=field):
                self.ledger.ingest([self.receipt(n)])
                with sqlite3.connect(self.path) as db:
                    local_id = db.execute(
                        "SELECT local_id FROM originals WHERE message_id=?",
                        (f"cf-{n:02d}",),
                    ).fetchone()[0]
                ticket = self.ledger.reserve_index(local_id)
                with sqlite3.connect(self.path) as db:
                    db.execute(f"UPDATE {table} SET {field}=? WHERE local_id=?",
                               (value, local_id))
                with self.assertRaises(CaptureConflict):
                    self.ledger.acknowledge_index(
                        local_id, ticket["payload_sha256"], f"file-{n}",
                    )
                with sqlite3.connect(self.path) as db:
                    state, provider_id = db.execute(
                        "SELECT state,provider_file_id FROM index_outbox WHERE local_id=?",
                        (local_id,),
                    ).fetchone()
                self.assertEqual((state, provider_id), ("IN_FLIGHT", None))

    def test_g2_corrupt_identity_rejected_before_reservation(self):
        # Original local_id is determined by source/message/version, and must
        # agree with the still-stored identity at the upload boundary.
        for n, (field, forged) in enumerate((
            ("source_id", "synthetic-capture-other"),
            ("message_id", "forged-message"),
            ("version_id", "forged-v99"),
        ), start=60):
            with self.subTest(identity=field):
                self.ledger.ingest([self.receipt(n)])
                with sqlite3.connect(self.path) as db:
                    local_id = db.execute(
                        "SELECT local_id FROM originals WHERE message_id=?",
                        (f"cf-{n:02d}",),
                    ).fetchone()[0]
                    db.execute(f"UPDATE originals SET {field}=? WHERE local_id=?",
                               (forged, local_id))
                with self.assertRaises(CaptureConflict):
                    self.ledger.reserve_index(local_id)
                with sqlite3.connect(self.path) as db:
                    state, provider = db.execute(
                        "SELECT state,provider_file_id FROM index_outbox WHERE local_id=?",
                        (local_id,),
                    ).fetchone()
                self.assertEqual((state, provider), ("PENDING", None))

    def test_g2_late_corrupt_identity_rejected_before_acknowledgement(self):
        for n, (field, forged) in enumerate((
            ("source_id", "synthetic-capture-other-late"),
            ("message_id", "forged-late-message"),
            ("version_id", "forged-late-v99"),
        ), start=70):
            with self.subTest(identity=field):
                self.ledger.ingest([self.receipt(n)])
                with sqlite3.connect(self.path) as db:
                    local_id = db.execute(
                        "SELECT local_id FROM originals WHERE message_id=?",
                        (f"cf-{n:02d}",),
                    ).fetchone()[0]
                ticket = self.ledger.reserve_index(local_id)
                with sqlite3.connect(self.path) as db:
                    db.execute(f"UPDATE originals SET {field}=? WHERE local_id=?",
                               (forged, local_id))
                with self.assertRaises(CaptureConflict):
                    self.ledger.acknowledge_index(
                        local_id, ticket["payload_sha256"], f"file-{n}",
                    )
                with sqlite3.connect(self.path) as db:
                    state, provider = db.execute(
                        "SELECT state,provider_file_id FROM index_outbox WHERE local_id=?",
                        (local_id,),
                    ).fetchone()
                self.assertEqual((state, provider), ("IN_FLIGHT", None))

    def test_g2_snapshot_rejects_corrupted_source_version(self):
        self.ledger.ingest([self.receipt(80, version="v1")])
        local_id = self.snap()["originals"][0]["local_id"]
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE originals SET version_id='forged-v99' WHERE local_id=?",
                       (local_id,))
        with self.assertRaises(CaptureConflict):
            self.snap()

    def test_g2_verification_refuses_corrupt_source_version(self):
        original = self.receipt(81, version="v1", text="Fictional immutable text")
        self.ledger.ingest([original])
        local_id = self.snap()["originals"][0]["local_id"]
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE originals SET version_id='forged-v99' WHERE local_id=?",
                       (local_id,))
        with self.assertRaises(CaptureConflict):
            self.ledger.verify_synthetic(local_id, original["exact_text"].encode("utf-8"),
                                         "independent-synthetic-readback")
        with sqlite3.connect(self.path) as db:
            status = db.execute(
                "SELECT source_status FROM originals WHERE local_id=?", (local_id,),
            ).fetchone()[0]
        self.assertEqual(status, "SOURCE_OBSERVED")

    def test_cf10_non_synthetic_rejection(self):
        for change in ({"synthetic_only": False},
                       {"source_id": "conversation-real"},
                       {"capture_method": "chatgpt_plugin"},
                       {"source_locator": "https://chatgpt.com/c/00000000-0000-0000-0000-000000000000"},
                       {"author_role": "tool"}):
            with self.subTest(change=change):
                with self.assertRaises(CaptureBoundaryError):
                    self.ledger.ingest([{**self.receipt(), **change}])
        self.assertEqual(self.snap()["originals"], [])

    def test_cf11_twelve_turn_offline_recovery_simulation(self):
        # Four exchanges captured before outage (8 messages), four exchanges
        # not received locally while offline (8 explicit gaps), then four more.
        def exchange(turn):
            user_position = turn * 2 - 1
            return [
                self.receipt(user_position, message=f"u-{turn}", position=user_position,
                             text=f"Fictional turn {turn} user"),
                self.receipt(user_position + 1, message=f"a-{turn}",
                             position=user_position + 1, role="assistant",
                             text=f"Fictional turn {turn} assistant"),
            ]
        online = [p for turn in range(1, 5) for p in exchange(turn)]
        missed = [p for turn in range(5, 9) for p in exchange(turn)]
        after = [p for turn in range(9, 13) for p in exchange(turn)]
        self.ledger.ingest(online)
        for position in range(9, 17):
            self.ledger.mark_gap("synthetic-capture-cf", "fictional-recovery", "main",
                                 position, "synthetic host-off period")
        self.ledger = SyntheticCaptureLedger(self.path)
        self.ledger.ingest(after)
        before = self.snap()
        self.assertEqual(len(before["originals"]), 16)
        self.assertEqual(sum(x["state"] == "GAP_UNKNOWN" for x in before["coverage"]), 8)
        self.assertFalse(before["capture_complete"])
        self.ledger.ingest(missed)
        self.ledger = SyntheticCaptureLedger(self.path)
        self.assertEqual(self.ledger.ingest(online + missed + after)["inserted"], 0)
        after_snapshot = self.snap()
        self.assertEqual(len(after_snapshot["originals"]), 24)
        self.assertEqual(len(after_snapshot["outbox"]), 24)
        self.assertEqual(len(after_snapshot["coverage"]), 24)
        self.assertFalse(any(x["state"] == "GAP_UNKNOWN" for x in after_snapshot["coverage"]))
        self.assertFalse(after_snapshot["capture_complete"])
        self.assertEqual([x["position"] for x in after_snapshot["originals"]],
                         list(range(1, 25)))
        self.assertTrue(all(x["state"] == "PENDING" for x in after_snapshot["outbox"]))


if __name__ == "__main__":
    unittest.main()
