"""Independent, ephemeral G2/G5/G9 adversarial review of exactly 8d27bd55.
No repository writes, providers, real data or external inference.
"""
import hashlib
import json
import sqlite3
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path("/tmp/ltm-independent-8d27-WTfufe/repo")
sys.path.insert(0, str(ROOT / "vnext"))
from ltm_vnext.capture_foundation_v import SyntheticCaptureLedger as Ledger, CaptureConflict, CaptureBoundaryError

class IndependentReview(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="fresh-review-")
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.sqlite"
        self.l = Ledger.initialise(self.path)

    def receipt(self, i=1, text="Exact ⛄ rôle\nαβ—line", role="user", version="v1", pos=None, msg=None):
        return dict(synthetic_only=True, source_id="synthetic-capture-review",
            conversation_id="review-fiction", branch_id="b-main",
            message_id=msg or f"independent-{i}", version_id=version,
            position=pos if pos is not None else i, author_role=role,
            source_locator=f"synthetic-capture://independent/{i}",
            capture_method="synthetic_ui_observation", exact_text=text,
            message_sent_at=None, observed_at=None)

    def snap(self):
        return self.l.snapshot("synthetic-capture-review","review-fiction","b-main")

    def one(self, i=1, **kw):
        r=self.receipt(i, **kw)
        self.assertEqual(self.l.ingest([r])["inserted"], 1)
        lid=self.l._validate(r)["local_id"]
        return r,lid

    def query(self, sql, args=()):
        with sqlite3.connect(self.path) as db:
            return db.execute(sql,args).fetchall()

    def corrupt(self, table, field, val, lid):
        with sqlite3.connect(self.path) as db:
            db.execute(f"UPDATE {table} SET {field}=? WHERE local_id=?", (val,lid))

    def status(self,lid):
        return self.query("SELECT source_status,verification_ref FROM originals WHERE local_id=?", (lid,))[0]

    def outbox(self,lid):
        return self.query("SELECT state,provider_file_id FROM index_outbox WHERE local_id=?", (lid,))[0]

    def exercise_verify_integrity(self, table, col, value):
        r,lid=self.one()
        self.corrupt(table,col,value,lid)
        with self.assertRaises(CaptureConflict):
            self.l.verify_synthetic(lid,r["exact_text"].encode(), "independent-readback")
        self.assertEqual(self.status(lid), ("SOURCE_OBSERVED",None))

    def test_exact_text_tamper_refused(self):
        self.exercise_verify_integrity("originals","exact_text","Other stored words")

    def test_role_tamper_refused(self):
        self.exercise_verify_integrity("originals","author_role","assistant")

    def test_outbox_digest_tamper_refused(self):
        self.exercise_verify_integrity("index_outbox","payload_sha256","b"*64)

    def test_original_digest_tamper_refused(self):
        self.exercise_verify_integrity("originals","content_sha256","f"*64)

    def test_outbox_deleted_prevents_verification(self):
        r,lid=self.one()
        with sqlite3.connect(self.path) as db:
            db.execute("DELETE FROM index_outbox WHERE local_id=?", (lid,))
        with self.assertRaises(CaptureConflict):
            self.l.verify_synthetic(lid, r["exact_text"].encode(), "independent")
        self.assertEqual(self.status(lid), ("SOURCE_OBSERVED",None))

    def test_bad_independent_bytes_do_not_promote(self):
        r,lid=self.one()
        with self.assertRaises(CaptureConflict):
            self.l.verify_synthetic(lid,b"NOT THE ORIGINAL", "independent")
        self.assertEqual(self.status(lid), ("SOURCE_OBSERVED",None))

    def test_successful_source_verification_exact_unicode(self):
        r,lid=self.one(text="A 🐙\nＡ\u200d🎓 e\u0301",role="assistant")
        self.l.verify_synthetic(lid,r["exact_text"].encode(),"independent-source-1")
        self.assertEqual(self.status(lid),("SOURCE_VERIFIED","independent-source-1"))
        self.assertEqual(self.snap()["originals"][0]["exact_text"],r["exact_text"])

    def test_verify_ref_conflict_does_not_rewrite(self):
        r,lid=self.one()
        self.l.verify_synthetic(lid,r["exact_text"].encode(),"ref-A")
        with self.assertRaises(CaptureConflict):
            self.l.verify_synthetic(lid,r["exact_text"].encode(),"ref-B")
        self.assertEqual(self.status(lid),("SOURCE_VERIFIED","ref-A"))

    def exercise_identity(self, field, changed, action):
        r,lid=self.one()
        ticket=self.l.reserve_index(lid) if action=="ack" else None
        self.corrupt("originals",field,changed,lid)
        with self.assertRaises(CaptureConflict):
            if action=="verify": self.l.verify_synthetic(lid,r["exact_text"].encode(),"ref")
            elif action=="reserve": self.l.reserve_index(lid)
            elif action=="ack": self.l.acknowledge_index(lid,ticket["payload_sha256"],"provider-1")
        if action=="verify": self.assertEqual(self.status(lid),("SOURCE_OBSERVED",None))
        else: self.assertEqual(self.outbox(lid),("IN_FLIGHT" if action=="ack" else "PENDING",None))

    def test_ingest_transaction_rolls_back_second_failure(self):
        valid=self.receipt(1)
        invalid=self.receipt(2)
        invalid["supersedes"]={"message_id":"not-found","version_id":"1"}
        with self.assertRaises(CaptureBoundaryError): self.l.ingest([valid,invalid])
        self.assertEqual(self.query("SELECT COUNT(*) FROM originals")[0][0],0)
        self.assertEqual(self.query("SELECT COUNT(*) FROM index_outbox")[0][0],0)
        self.assertEqual(self.query("SELECT COUNT(*) FROM coverage")[0][0],0)

    def test_replay_retains_original_local_id_and_time(self):
        r,lid=self.one()
        first=self.query("SELECT ingested_at_utc FROM originals WHERE local_id=?",(lid,))[0][0]
        self.assertEqual(self.l.ingest([r,r])["inserted"],0)
        self.assertEqual(self.query("SELECT ingested_at_utc FROM originals WHERE local_id=?",(lid,))[0][0],first)
        self.assertEqual(self.snap()["originals"][0]["local_id"],lid)

    def test_valid_index_reservation_and_ack_idempotent(self):
        _,lid=self.one()
        ticket=self.l.reserve_index(lid)
        self.assertEqual(hashlib.sha256(ticket["payload"]).hexdigest(),ticket["payload_sha256"])
        self.l.acknowledge_index(lid,ticket["payload_sha256"],"provider-1")
        self.l.acknowledge_index(lid,ticket["payload_sha256"],"provider-1")
        self.assertEqual(self.outbox(lid),("SEARCHABLE","provider-1"))

    def test_bad_ack_digest_preserves_inflight(self):
        _,lid=self.one()
        self.l.reserve_index(lid)
        with self.assertRaises(CaptureConflict):
            self.l.acknowledge_index(lid,"not-canonical","provider-1")
        self.assertEqual(self.outbox(lid),("IN_FLIGHT",None))

    def test_late_role_tamper_prevents_searchable(self):
        _,lid=self.one()
        ticket=self.l.reserve_index(lid)
        self.corrupt("originals","author_role","assistant",lid)
        with self.assertRaises(CaptureConflict):
            self.l.acknowledge_index(lid,ticket["payload_sha256"],"provider-1")
        self.assertEqual(self.outbox(lid),("IN_FLIGHT",None))

    def test_revoked_pending_never_verify_or_reserve(self):
        r,lid=self.one()
        self.l.revoke(lid,"fictional revoke")
        with self.assertRaises(CaptureBoundaryError):
            self.l.verify_synthetic(lid,r["exact_text"].encode(),"ref")
        with self.assertRaises(CaptureBoundaryError):
            self.l.reserve_index(lid)
        self.assertEqual(len(self.snap()["originals"]),0)
        self.assertEqual(self.snap()["coverage"][0]["state"],"REVOKED")

    def test_revoked_inflight_denies_late_ack(self):
        _,lid=self.one()
        ticket=self.l.reserve_index(lid)
        self.l.revoke(lid,"fictional revoke")
        with self.assertRaises(CaptureBoundaryError):
            self.l.acknowledge_index(lid,ticket["payload_sha256"],"provider-1")
        self.assertEqual(self.outbox(lid),("IN_FLIGHT",None))
        self.assertEqual(self.l.revocation_status(lid)["remote_cleanup"],"REQUIRED")

    def test_revocation_repeated_preserves_timestamp(self):
        _,lid=self.one()
        a=self.l.revoke(lid,"same")
        b=self.l.revoke(lid,"same")
        self.assertEqual(a,b)
        with self.assertRaises(CaptureConflict):
            self.l.revoke(lid,"different")

    def test_versioned_record_survives_other_version_revocation(self):
        r1,lid1=self.one(1,msg="editable")
        r2=self.receipt(1,msg="editable",version="v2",text="Edition 2")
        r2["supersedes"]={"message_id":"editable","version_id":"v1"}
        self.l.ingest([r2])
        self.l.revoke(lid1,"revoke earlier")
        snap=self.snap()
        self.assertEqual(len(snap["originals"]),1)
        self.assertEqual(snap["coverage"][0]["state"],"OBSERVED")
        self.assertTrue(snap["originals"][0]["predecessor_redacted"])
        self.l.revoke(self.l._validate(r2)["local_id"],"revoke current")
        self.assertEqual(self.snap()["coverage"][0]["state"],"REVOKED")

    def test_explicit_unknown_gap_is_not_orphan(self):
        self.l.mark_gap("synthetic-capture-review","review-fiction","b-main",3,"synthetic outage")
        self.assertEqual(self.snap()["coverage"][0]["state"],"GAP_UNKNOWN")
        self.assertEqual(len(self.snap()["originals"]),0)

    def test_manual_false_observed_slot_rejected(self):
        self.l.mark_gap("synthetic-capture-review","review-fiction","b-main",3,"synthetic outage")
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE coverage SET state='OBSERVED' WHERE position=3")
        with self.assertRaises(CaptureConflict): self.snap()

    def test_two_parallel_reservations_one_winner(self):
        _,lid=self.one()
        barrier=threading.Barrier(3)
        outcomes=[]
        def reserve():
            barrier.wait()
            try: outcomes.append(("ok",self.l.reserve_index(lid)))
            except BaseException as e: outcomes.append((type(e).__name__,str(e)))
        t1=threading.Thread(target=reserve);t2=threading.Thread(target=reserve)
        t1.start();t2.start();barrier.wait();t1.join(5);t2.join(5)
        self.assertFalse(t1.is_alive() or t2.is_alive())
        self.assertEqual(sorted(x[0] for x in outcomes),["CaptureBoundaryError","ok"])
        self.assertEqual(self.outbox(lid),("IN_FLIGHT",None))

    def test_remote_absence_requeues_with_evidence(self):
        _,lid=self.one()
        self.l.reserve_index(lid)
        self.l.remote_confirmed_absent(lid,"independent synthetic absence")
        self.assertEqual(self.outbox(lid),("PENDING",None))
        self.assertEqual(self.snap()["outbox"][0]["reconciliation_ref"],"independent synthetic absence")
        self.l.reserve_index(lid)

    def test_snapshot_wal_revocation_consistent_twelve_repetitions(self):
        for cycle in range(12):
            tmp=tempfile.TemporaryDirectory(prefix="wal-cold-")
            self.addCleanup(tmp.cleanup)
            path=Path(tmp.name)/"wal.sqlite"
            led=Ledger.initialise(path)
            rec=self.receipt(cycle+10)
            led.ingest([rec])
            local=led._validate(rec)["local_id"]
            with sqlite3.connect(path) as db: db.execute("PRAGMA journal_mode=WAL")
            gate=threading.Event();release=threading.Event();written=threading.Event()
            output={}; orig=Ledger._check_source_identity
            def check(row):
                gate.set()
                if not release.wait(5): raise AssertionError("read barrier timed out")
                return orig(row)
            def read():
                try: output["snapshot"]=led.snapshot("synthetic-capture-review","review-fiction","b-main")
                except BaseException as exc: output["read_err"]=repr(exc)
            def write():
                try: led.revoke(local,"concurrent revoke"); written.set()
                except BaseException as exc: output["write_err"]=repr(exc); written.set()
            with patch.object(Ledger,"_check_source_identity",staticmethod(check)):
                r=threading.Thread(target=read);r.start()
                self.assertTrue(gate.wait(3),f"reader barrier {cycle}")
                w=threading.Thread(target=write);w.start()
                try: self.assertTrue(written.wait(3),f"WAL write commit {cycle}")
                finally: release.set()
                r.join(5);w.join(5)
            self.assertFalse(r.is_alive() or w.is_alive(),f"thread incomplete {cycle}")
            self.assertNotIn("read_err",output)
            self.assertNotIn("write_err",output)
            old=output["snapshot"]
            self.assertEqual(len(old["originals"]),1)
            self.assertEqual(old["revoked_count"],0)
            self.assertEqual(old["coverage"][0]["state"],"OBSERVED")
            self.assertEqual(len(old["outbox"]),1)
            new=led.snapshot("synthetic-capture-review","review-fiction","b-main")
            self.assertEqual(new["originals"],[])
            self.assertEqual(new["outbox"],[])
            self.assertEqual(new["revoked_count"],1)
            self.assertEqual(new["coverage"][0]["state"],"REVOKED")

def add_generated():
    for field,value in (
        ("source_id","synthetic-capture-impostor"),
        ("message_id","substitute-id"),
        ("version_id","v999")):
        for action in ("verify","reserve","ack"):
            def fn(self, f=field, v=value, a=action):
                self.exercise_identity(f,v,a)
            setattr(IndependentReview,f"test_identity_{field}_{action}",fn)
    for field,value in (
        ("source_id","synthetic-capture-impostor"),
        ("conversation_id","impostor-conversation"),
        ("branch_id","other-branch"),
        ("position",999)):
        def fn(self,f=field,v=value):
            _,lid=self.one()
            self.corrupt("originals",f,v,lid)
            with self.assertRaises(CaptureConflict):
                self.snap()
        setattr(IndependentReview,f"test_orphan_coverage_after_{field}_change",fn)
add_generated()

if __name__=="__main__":
    unittest.main(verbosity=2)
