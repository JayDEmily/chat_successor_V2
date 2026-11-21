"""Reviewer-authored, ephemeral fault-injection tests; no repository edits."""
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path
from ltm_vnext.capture_foundation_v import SyntheticCaptureLedger, CaptureBoundaryError, CaptureConflict

class IndependentG2G5(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="d27-g2g5-")
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "ledger.sqlite"
        self.ledger = SyntheticCaptureLedger.initialise(self.path)
        self.source = "synthetic-capture-independent"
        self.convo = "fictional"
        self.branch = "main"

    def make(self, n):
        receipt = dict(synthetic_only=True, source_id=self.source,
                       conversation_id=self.convo, branch_id=self.branch,
                       message_id=f"msg-{n}", version_id="v1",
                       position=n, author_role="user",
                       source_locator=f"synthetic-capture://independent/{n}",
                       capture_method="synthetic_ui_observation",
                       exact_text=f"Verbatim ‘record’, déjà vu — {n}\nsecond line",
                       message_sent_at=None, observed_at=None)
        self.ledger.ingest([receipt])
        with sqlite3.connect(self.path) as db:
            lid = db.execute("SELECT local_id FROM originals WHERE message_id=?", (receipt["message_id"],)).fetchone()[0]
        return lid, receipt

    def mutate(self, lid, column, value):
        assert column in ("source_id", "message_id", "version_id", "exact_text", "content_sha256", "author_role", "payload_sha256")
        table = "index_outbox" if column == "payload_sha256" else "originals"
        with sqlite3.connect(self.path) as db:
            db.execute(f"UPDATE {table} SET {column}=? WHERE local_id=?", (value,lid))

    def status(self, lid):
        with sqlite3.connect(self.path) as db:
            original = db.execute("SELECT source_status, verification_ref FROM originals WHERE local_id=?", (lid,)).fetchone()
            outbox = db.execute("SELECT state,provider_file_id FROM index_outbox WHERE local_id=?", (lid,)).fetchone()
        return original, outbox

    def snapshot(self, source=None):
        return self.ledger.snapshot(source or self.source, self.convo, self.branch)

    def test_valid_unicode_index_ack_and_snapshot(self):
        lid,r = self.make(1)
        ticket = self.ledger.reserve_index(lid)
        self.assertEqual(__import__("json").loads(ticket["payload"].decode("utf8"))["exact_text"],r["exact_text"])
        self.ledger.acknowledge_index(lid,ticket["payload_sha256"],"file-valid")
        self.ledger.acknowledge_index(lid,ticket["payload_sha256"],"file-valid")
        s = self.snapshot()
        self.assertEqual(s["originals"][0]["exact_text"],r["exact_text"])
        self.assertEqual(s["originals"][0]["author_role"],"user")
        self.assertEqual(s["outbox"][0]["state"],"SEARCHABLE")

    def test_source_message_version_reject_reservation_rollback(self):
        for n,key in enumerate(("source_id","message_id","version_id"),10):
            with self.subTest(key=key):
                lid,r=self.make(n)
                self.mutate(lid,key,"synthetic-capture-forged" if key=="source_id" else "forged")
                with self.assertRaises(CaptureConflict): self.ledger.reserve_index(lid)
                self.assertEqual(self.status(lid)[1],("PENDING",None))

    def test_source_message_version_reject_late_ack_rollback(self):
        for n,key in enumerate(("source_id","message_id","version_id"),20):
            with self.subTest(key=key):
                lid,r=self.make(n)
                ticket=self.ledger.reserve_index(lid)
                self.mutate(lid,key,"synthetic-capture-forged" if key=="source_id" else "forged")
                with self.assertRaises(CaptureConflict):
                    self.ledger.acknowledge_index(lid,ticket["payload_sha256"],"file-bad")
                self.assertEqual(self.status(lid)[1],("IN_FLIGHT",None))

    def test_source_message_version_snapshot_checks_visible_rows(self):
        for n,key in enumerate(("source_id","message_id","version_id"),30):
            with self.subTest(key=key):
                lid,r=self.make(n)
                target="synthetic-capture-forged" if key=="source_id" else "forged"
                self.mutate(lid,key,target)
                with self.assertRaises(CaptureConflict):
                    self.snapshot(target if key=="source_id" else None)
                self.mutate(lid,key,r[key])

    def test_source_message_version_verification_stays_observed(self):
        for n,key in enumerate(("source_id","message_id","version_id"),40):
            with self.subTest(key=key):
                lid,r=self.make(n)
                self.mutate(lid,key,"synthetic-capture-forged" if key=="source_id" else "forged")
                with self.assertRaises(CaptureConflict):
                    self.ledger.verify_synthetic(lid,r["exact_text"].encode("utf8"),"independent-readback")
                self.assertEqual(self.status(lid)[0][0],"SOURCE_OBSERVED")

    def test_corrected_identity_can_reserve(self):
        lid,r=self.make(50)
        self.mutate(lid,"version_id","forged")
        with self.assertRaises(CaptureConflict): self.ledger.reserve_index(lid)
        self.mutate(lid,"version_id",r["version_id"])
        self.assertEqual(self.ledger.reserve_index(lid)["local_id"],lid)

    def test_role_corruption_rejects_index_and_snapshot(self):
        lid,r=self.make(51)
        self.mutate(lid,"author_role","assistant")
        with self.assertRaises(CaptureConflict): self.ledger.reserve_index(lid)
        with self.assertRaises(CaptureConflict): self.snapshot()
        self.assertEqual(self.status(lid)[1],("PENDING",None))

    def test_text_corruption_rejects_index_and_snapshot(self):
        lid,r=self.make(52)
        self.mutate(lid,"exact_text","forged Unicode text")
        with self.assertRaises(CaptureConflict): self.ledger.reserve_index(lid)
        with self.assertRaises(CaptureConflict): self.snapshot()
        self.assertEqual(self.status(lid)[1],("PENDING",None))

    def test_digest_corruption_rejects_index_and_snapshot(self):
        lid,r=self.make(53)
        self.mutate(lid,"content_sha256","0"*64)
        with self.assertRaises(CaptureConflict): self.ledger.reserve_index(lid)
        with self.assertRaises(CaptureConflict): self.snapshot()

    def test_outbox_corruption_rejects_index_and_snapshot(self):
        lid,r=self.make(54)
        self.mutate(lid,"payload_sha256","0"*64)
        with self.assertRaises(CaptureConflict): self.ledger.reserve_index(lid)
        with self.assertRaises(CaptureConflict): self.snapshot()

    def test_verification_rejects_modified_original_text(self):
        lid,r=self.make(60)
        self.mutate(lid,"exact_text","forged Unicode text")
        with self.assertRaises(CaptureConflict):
            self.ledger.verify_synthetic(lid,r["exact_text"].encode("utf8"),"independent-readback")
        self.assertEqual(self.status(lid)[0][0],"SOURCE_OBSERVED")

    def test_verification_rejects_modified_role(self):
        lid,r=self.make(61)
        self.mutate(lid,"author_role","assistant")
        with self.assertRaises(CaptureConflict):
            self.ledger.verify_synthetic(lid,r["exact_text"].encode("utf8"),"independent-readback")
        self.assertEqual(self.status(lid)[0][0],"SOURCE_OBSERVED")

    def test_verification_rejects_corrupt_outbox_mapping(self):
        lid,r=self.make(62)
        self.mutate(lid,"payload_sha256","0"*64)
        with self.assertRaises(CaptureConflict):
            self.ledger.verify_synthetic(lid,r["exact_text"].encode("utf8"),"independent-readback")
        self.assertEqual(self.status(lid)[0][0],"SOURCE_OBSERVED")

    def test_concurrent_reservation_at_most_one_ticket(self):
        lid,r=self.make(70)
        barrier=threading.Barrier(3)
        outcomes=[]
        lock=threading.Lock()
        def worker():
            barrier.wait()
            try:
                self.ledger.reserve_index(lid)
                result="ticket"
            except CaptureBoundaryError:
                result="blocked"
            with lock: outcomes.append(result)
        threads=[threading.Thread(target=worker) for _ in range(2)]
        for t in threads: t.start()
        barrier.wait()
        for t in threads: t.join(timeout=5)
        self.assertFalse(any(t.is_alive() for t in threads))
        self.assertCountEqual(outcomes,["ticket","blocked"])
        self.assertEqual(self.status(lid)[1],("IN_FLIGHT",None))

    def test_revocation_blocks_late_ack_and_snapshot(self):
        lid,r=self.make(71)
        ticket=self.ledger.reserve_index(lid)
        self.ledger.revoke(lid,"synthetic reviewer test")
        with self.assertRaises(CaptureBoundaryError):
            self.ledger.acknowledge_index(lid,ticket["payload_sha256"],"file-late")
        self.assertEqual(self.snapshot()["originals"],[])
        self.assertEqual(self.status(lid)[1],("IN_FLIGHT",None))

    def test_original_scope_snapshot_fails_closed_on_re_scoped_row(self):
        lid,r=self.make(80)
        self.mutate(lid,"source_id","synthetic-capture-forged")
        s=self.snapshot(self.source)
        # No source record may silently disappear while its coverage still says OBSERVED.
        self.assertFalse(any(c["state"]=="OBSERVED" for c in s["coverage"])
                         and not s["originals"])

    def test_concurrent_revocation_snapshot_is_consistent(self):
        lid,r=self.make(90)
        original_open=self.ledger._open
        scanned=threading.Event()
        resume=threading.Event()
        class PausedConnection:
            def __init__(self, actual): self.actual=actual
            def __enter__(self): self.actual.__enter__(); return self
            def __exit__(self,*args): return self.actual.__exit__(*args)
            def __getattr__(self,k): return getattr(self.actual,k)
            def execute(self,query,*args):
                if "SELECT position,state,note FROM coverage" in query:
                    scanned.set()
                    assert resume.wait(timeout=5), "reviewer synchronization timeout"
                return self.actual.execute(query,*args)
        self.ledger._open=lambda:PausedConnection(original_open())
        result=[]
        def take_snapshot():
            try: result.append(("ok",self.snapshot()))
            except Exception as exc: result.append(("error",repr(exc)))
        reader=threading.Thread(target=take_snapshot)
        reader.start()
        self.assertTrue(scanned.wait(timeout=5), "snapshot never reached coverage query")
        self.ledger.revoke(lid,"concurrent reviewer revoke")
        resume.set()
        reader.join(timeout=5)
        self.assertFalse(reader.is_alive())
        self.assertEqual(result[0][0],"ok",result)
        s=result[0][1]
        self.assertNotIn(lid,[r["local_id"] for r in s["originals"]],
                         "Snapshot released a revoked original after tombstone commit")
        self.assertEqual(s["revoked_count"],1)

if __name__=="__main__":
    unittest.main(verbosity=2)
