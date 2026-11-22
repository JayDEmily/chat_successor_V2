"""Frozen M02 S01-S13, synthetic only. No network, desktop or credentials."""
from dataclasses import replace
from pathlib import Path
import json
import os
import sys
import subprocess
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mcp_native_poc import (Action, Auth, Delivery, Preflight, Proof, Quiet,
                            Rejected, Remote, RepoView, Route, branch_name, digest)


C1 = "11111111-1111-1111-1111-111111111111"
C2 = "22222222-2222-2222-2222-222222222222"
BASE, SHA1, SHA2 = "0" * 40, "1" * 40, "2" * 40
ROUTE = Route("synthetic-run", "synthetic-principal", "synthetic-account",
              "synthetic-project", "example/synthetic", "work/fixture", BASE, 2)
AUTH = Auth(ROUTE.principal, ROUTE.run_id, ROUTE.account_key, "session-1", "subject")
AUTH2 = replace(AUTH, session="session-2")


class Contract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "run"
        self.now = 100.0
        self.proof = None
        self.addCleanup(self.close)

    def close(self):
        if self.proof:
            self.proof.close()

    def open(self, cap=2, action_cap=32, response_timeout_seconds=300):
        self.proof = Proof(self.path, replace(ROUTE, cap=cap, action_cap=action_cap,
                                              response_timeout_seconds=response_timeout_seconds), clock=lambda: self.now)
        return self.proof

    def reopen(self):
        self.close()
        self.proof = Proof(self.path, clock=lambda: self.now)
        return self.proof

    def reg(self, dispatch, **kwargs):
        return dict(schema_version=1, run_id=ROUTE.run_id, action_id=dispatch.action_id,
                    challenge=dispatch.challenge) | kwargs

    def report(self, dispatch, status="TASK_COMPLETE", commit=SHA1, **kwargs):
        return dict(schema_version=1, run_id=ROUTE.run_id, action_id=dispatch.action_id,
                    status=status, publication_sha=commit,
                    publication_branch=ROUTE.branch if commit else None) | kwargs

    def target(self, target=None, quiet=None, **kwargs):
        return replace(Preflight(ROUTE.account_key, ROUTE.project_id, target,
                                 True, True, quiet), **kwargs)

    def receipt(self, dispatch, auth=AUTH, cid=C1, **kwargs):
        return replace(Delivery(ROUTE.run_id, dispatch.action_id, ROUTE.account_key,
                                ROUTE.project_id, cid, digest(dispatch.prompt),
                                auth.principal, auth.session, auth.subject, True), **kwargs)

    def quiet(self, dispatch, cid=C1, idle=True):
        return Quiet(ROUTE.run_id, dispatch.action_id, cid, idle)

    def remote(self, cid=C1, commit=SHA1, ancestor=BASE, complete=True, **kwargs):
        view = replace(RepoView(ROUTE.repo, ROUTE.branch, cid, complete,
                               None if complete else "Next synthetic step"), **kwargs)
        return Remote(ROUTE.run_id, commit, view, ancestor)

    def read(self, evidence):
        def reader(repo, branch, ancestor):
            self.assertEqual(repo, ROUTE.repo)
            self.assertEqual(branch, ROUTE.branch)
            self.assertEqual(ancestor, self.proof.data["prior_sha"])
            return evidence
        return reader

    def bootstrap(self, cap=2, bind=True, action_cap=32, response_timeout_seconds=300):
        p = self.open(cap, action_cap, response_timeout_seconds)
        d = p.reserve()
        self.assertEqual(p.count, 0)
        self.assertEqual(p.begin_attempt(d, self.target()), Action.WAIT)
        self.assertEqual(p.register_worker(self.reg(d), AUTH)["bound"], False)
        self.assertEqual(p.count, 0)
        if bind:
            self.assertEqual(p.admit_delivery(self.receipt(d)), Action.WAIT)
            self.assertEqual(p.count, 1)
        return p, d

    def accept_report(self, p, d, status="TASK_COMPLETE", complete=True, cid=C1,
                      commit=SHA1, ancestor=BASE, auth=AUTH):
        self.assertEqual(p.report_worker(self.report(d, status, commit), auth), "received")
        return p.evaluate(self.quiet(d, cid), self.read(
            self.remote(cid, commit, ancestor, complete)) if commit else None)

    def test_S01_bootstrap_finish(self):
        p, d = self.bootstrap()
        self.assertEqual(self.accept_report(p, d), Action.STOP_FINISHED)
        self.assertEqual(p.core.state.halted, "programme_finished")
        self.assertEqual(p.count, 1)
        self.assertIsNone(p.core.state.pending)
        self.assertEqual(p.data["prior_sha"], SHA1)
        self.assertNotIn(d.challenge, (self.path / "ledger.json").read_text())

    def test_S02_same_chat_continuation(self):
        p, d = self.bootstrap()
        self.assertEqual(self.accept_report(p, d, "NEED_MORE_TIME", commit=None),
                         Action.CONTINUE_CURRENT)
        next_d = p.reserve()
        self.assertNotEqual(d.challenge, next_d.challenge)
        self.assertNotEqual(d.action_id, next_d.action_id)
        self.assertEqual(p.begin_attempt(next_d, self.target(C1, self.quiet(d))), Action.WAIT)
        p.register_worker(self.reg(next_d), AUTH)
        self.assertEqual(p.admit_delivery(self.receipt(next_d)), Action.WAIT)
        self.assertEqual(p.count, 1)
        self.assertEqual(p.core.state.current_chat_id, C1)
        self.assertEqual(self.accept_report(p, next_d), Action.STOP_FINISHED)

    def test_S03_successor(self):
        p, d = self.bootstrap()
        self.assertEqual(self.accept_report(p, d, complete=False), Action.LAUNCH_SUCCESSOR)
        next_d = p.reserve()
        self.assertEqual(p.begin_attempt(next_d, self.target(None, self.quiet(d))), Action.WAIT)
        p.register_worker(self.reg(next_d), AUTH2)
        self.assertEqual(p.count, 1)
        self.assertEqual(p.admit_delivery(self.receipt(next_d, AUTH2, C2)), Action.WAIT)
        self.assertEqual(p.count, 2)
        self.assertEqual(p.core.state.current_chat_id, C2)
        self.assertEqual(self.accept_report(p, next_d, cid=C2, commit=SHA2,
                                            ancestor=SHA1, auth=AUTH2), Action.STOP_FINISHED)

    def test_S04_invalid_auth_and_request(self):
        p = self.open()
        d = p.reserve()
        with self.assertRaises(Rejected):
            p.register_worker(self.reg(d), AUTH)
        p.begin_attempt(d, self.target())
        for body, auth in [
            (self.reg(d), replace(AUTH, principal="other")),
            (self.reg(d), replace(AUTH, account_key="other")),
            (self.reg(d), replace(AUTH, run_id="other")),
            (self.reg(d), replace(AUTH, session="")),
            (self.reg(d), replace(AUTH, subject="")),
            (self.reg(d, challenge="wrong"), AUTH),
            (self.reg(d, run_id="wrong"), AUTH),
            (self.reg(d, action_id="wrong"), AUTH),
            (self.reg(d, principal=AUTH.principal), AUTH),
            (self.reg(d, schema_version=True), AUTH),
        ]:
            with self.subTest(body_keys=list(body), auth=auth):
                with self.assertRaises(Rejected):
                    p.register_worker(body, auth)
        self.assertIsNone(p.active["registration"])
        self.now = 500
        with self.assertRaises(Rejected):
            p.register_worker(self.reg(d), AUTH)
        self.assertEqual(p.data["hold"], "expired")
        self.assertEqual(p.count, 0)

    def test_S05_preflight_and_receipt_mismatch(self):
        p = self.open()
        d = p.reserve()
        for target in [self.target(account_key="wrong"), self.target(project_id="wrong"),
                       self.target(empty=False), self.target(no_attachments=False),
                       self.target(target=C1)]:
            self.assertEqual(p.begin_attempt(d, target), Action.HOLD)
            self.assertEqual(p.active["phase"], "prepared")
            p.resume()
        p.begin_attempt(d, self.target())
        p.register_worker(self.reg(d), AUTH)
        for receipt in [self.receipt(d, account_key="wrong"), self.receipt(d, project_id="wrong"),
                        self.receipt(d, chat_id=""), self.receipt(d, prompt_digest=SHA1),
                        self.receipt(d, session="other"), self.receipt(d, subject="other"),
                        self.receipt(d, observed=False)]:
            self.assertEqual(p.admit_delivery(receipt), Action.HOLD)
            self.assertEqual(p.count, 0)
        self.assertEqual(p.admit_delivery(self.receipt(d)), Action.WAIT)
        self.assertEqual(self.accept_report(p, d, complete=False), Action.LAUNCH_SUCCESSOR)
        n = p.reserve()
        self.assertEqual(p.begin_attempt(n, self.target(None, self.quiet(d, idle=False))), Action.HOLD)
        p.resume()
        p.begin_attempt(n, self.target(None, self.quiet(d)))
        for bad in [AUTH, replace(AUTH2, subject="other")]:
            with self.assertRaises(Rejected):
                p.register_worker(self.reg(n), bad)
        p.register_worker(self.reg(n), AUTH2)
        self.assertEqual(p.admit_delivery(self.receipt(n, AUTH2, C1)), Action.HOLD)
        self.assertEqual(p.count, 1)
        self.assertEqual(p.admit_delivery(self.receipt(n, AUTH2, C2)), Action.WAIT)
        self.assertEqual(p.count, 2)

    def test_S05_continuation_wrong_chat_session(self):
        p, d = self.bootstrap()
        self.assertEqual(self.accept_report(p, d, "NEED_MORE_TIME", commit=None),
                         Action.CONTINUE_CURRENT)
        n = p.reserve()
        p.begin_attempt(n, self.target(C1, self.quiet(d)))
        with self.assertRaises(Rejected):
            p.register_worker(self.reg(n), AUTH2)
        p.register_worker(self.reg(n), AUTH)
        self.assertEqual(p.admit_delivery(self.receipt(n, AUTH, C2)), Action.HOLD)
        self.assertEqual(p.count, 1)

    def test_S06_duplicates_conflicts_stale(self):
        p, d = self.bootstrap(bind=False)
        with self.assertRaises(Rejected):
            p.report_worker(self.report(d), AUTH)
        self.assertEqual(p.register_worker(self.reg(d), AUTH)["receipt"], d.action_id)
        with self.assertRaises(Rejected):
            p.register_worker(self.reg(d), AUTH2)
        p.admit_delivery(self.receipt(d))
        self.assertEqual(p.register_worker(self.reg(d), AUTH)["bound"], True)
        self.assertEqual(p.admit_delivery(self.receipt(d)), Action.IGNORE)
        for bad in [AUTH2, replace(AUTH, subject="wrong"), replace(AUTH, principal="wrong")]:
            with self.assertRaises(Rejected):
                p.report_worker(self.report(d), bad)
        self.assertEqual(p.report_worker(self.report(d, "NEED_MORE_TIME", None), AUTH), "received")
        self.assertEqual(p.report_worker(self.report(d, "NEED_MORE_TIME", None), AUTH), "duplicate")
        self.assertEqual(p.evaluate(self.quiet(d)), Action.CONTINUE_CURRENT)
        self.assertEqual(p.evaluate(self.quiet(d)), Action.IGNORE)
        self.assertEqual(len(p.core.state.consumed_responses), 1)
        n = p.reserve()
        with self.assertRaises(Rejected):
            p.report_worker(self.report(d), AUTH)
        with self.assertRaises(Rejected):
            p.register_worker(self.reg(d), AUTH)
        p.begin_attempt(n, self.target(C1, self.quiet(d)))
        p.register_worker(self.reg(n), AUTH)
        p.admit_delivery(self.receipt(n))
        self.assertEqual(p.report_worker(self.report(n), AUTH), "received")
        self.assertEqual(p.report_worker(self.report(n, commit=SHA2), AUTH), "conflict")
        self.assertEqual(p.evaluate(self.quiet(n), self.read(self.remote())), Action.HOLD)
        self.assertEqual(len(p.core.state.consumed_responses), 1)
        with self.assertRaises(Rejected):
            p.resume()

    def test_S07_remote_negative_matrix(self):
        p, d = self.bootstrap()
        for body in [self.report(d, commit=None),
                     self.report(d, publication_branch="wrong"),
                     self.report(d, publication_branch="work/.hidden"),
                     self.report(d, publication_branch="work/component.lock/next"),
                     self.report(d, publication_branch=["work/fixture"]),
                     self.report(d, commit="bad"),
                     self.report(d, status="NEED_MORE_TIME"),
                     self.report(d, status="bad"),
                     self.report(d, schema_version=True),
                     self.report(d, chat_id=C1)]:
            with self.assertRaises(Rejected):
                p.report_worker(body, AUTH)
        p.report_worker(self.report(d), AUTH)
        entries = [
            None, self.remote(published=False), self.remote(readable=False),
            self.remote(commit=SHA2), self.remote(ancestor=SHA2),
            replace(self.remote(), run_id="wrong"), self.remote(repo="other/repo"),
            self.remote(branch="other"), self.remote(cid=C2),
            self.remote(next_task="contradictory"), self.remote(complete=False, next_task=None),
            self.remote(complete=False, next_task="HOLD"), self.remote(programme_complete=1),
            self.remote(complete=False, next_task="FINISHED"),
            self.remote(complete=False, next_task=" HOLD "),
            self.remote(complete=False, next_task=" FINISHED "),
        ]
        for evidence in entries:
            self.assertEqual(p.evaluate(self.quiet(d), self.read(evidence)), Action.HOLD)
            self.assertFalse(p.active["consumed"])
            self.assertIsNone(p.core.state.pending)
            self.assertEqual(p.data["prior_sha"], BASE)
            p.resume()
        # Branch moves between independent reads.
        reads = iter([self.remote(), self.remote(commit=SHA2)])
        self.assertEqual(p.evaluate(self.quiet(d), lambda *_: next(reads)), Action.HOLD)
        self.assertFalse(p.active["consumed"])
        p.resume()
        self.assertEqual(p.evaluate(self.quiet(d), self.read(self.remote())), Action.STOP_FINISHED)

    def test_S07_replayed_old_publication(self):
        p, d = self.bootstrap()
        self.assertEqual(self.accept_report(p, d, complete=False), Action.LAUNCH_SUCCESSOR)
        n = p.reserve()
        p.begin_attempt(n, self.target(None, self.quiet(d)))
        p.register_worker(self.reg(n), AUTH2)
        p.admit_delivery(self.receipt(n, AUTH2, C2))
        p.report_worker(self.report(n), AUTH2)  # repeats old commit
        self.assertEqual(p.evaluate(self.quiet(n, C2),
                                    self.read(self.remote(C2, SHA1, SHA1))), Action.HOLD)
        self.assertFalse(p.active["consumed"])

    def test_S08_quiescence(self):
        p, d = self.bootstrap()
        p.report_worker(self.report(d), AUTH)
        for quiet in [None, self.quiet(d, idle=False), self.quiet(d, idle=None),
                      self.quiet(d, C2), replace(self.quiet(d), action_id="wrong")]:
            self.assertEqual(p.evaluate(quiet, self.read(self.remote())), Action.WAIT)
            self.assertFalse(p.active["consumed"])
            self.assertIsNone(p.core.state.pending)
        self.assertEqual(p.evaluate(self.quiet(d), self.read(self.remote())), Action.STOP_FINISHED)

    def test_S09_pause_and_error(self):
        p, d = self.bootstrap()
        p.pause()
        p.report_worker(self.report(d, "ERROR", None), AUTH)
        self.assertEqual(p.evaluate(self.quiet(d)), Action.HOLD)
        self.assertFalse(p.active["consumed"])
        p.resume()
        self.assertEqual(p.evaluate(self.quiet(d)), Action.HOLD)
        self.assertTrue(p.active["consumed"])
        self.assertIn("ERROR", p.core.state.halted)
        self.assertIsNone(p.core.state.pending)

    def test_S09_pause_during_read(self):
        p, d = self.bootstrap()
        p.report_worker(self.report(d), AUTH)
        def pause_reader(*_):
            p.pause()
            return self.remote()
        self.assertEqual(p.evaluate(self.quiet(d), pause_reader), Action.HOLD)
        self.assertFalse(p.active["consumed"])
        p.resume()
        self.assertEqual(p.evaluate(self.quiet(d), self.read(self.remote())), Action.STOP_FINISHED)
        p.pause()
        self.assertEqual(p.core.state.halted, "programme_finished")
        with self.assertRaises(Rejected):
            p.resume()

    def test_S10_cap(self):
        p, d = self.bootstrap(cap=1)
        self.assertEqual(self.accept_report(p, d, complete=False), Action.STOP_CAP)
        with self.assertRaises(Rejected):
            p.reserve()
        self.assertEqual(p.count, 1)
        self.assertIsNone(p.core.state.pending)

    def test_S11_restart_and_exact_retry(self):
        p, d = self.bootstrap(bind=False)
        p = self.reopen()
        self.assertEqual(p.active["phase"], "uncertain")
        self.assertEqual(p.register_worker(self.reg(d), AUTH)["bound"], False)
        p.admit_delivery(self.receipt(d))
        p.report_worker(self.report(d, "NEED_MORE_TIME", None), AUTH)
        p = self.reopen()
        self.assertEqual(p.report_worker(self.report(d, "NEED_MORE_TIME", None), AUTH), "duplicate")
        self.assertEqual(p.evaluate(self.quiet(d)), Action.CONTINUE_CURRENT)
        n = p.reserve()
        p = self.reopen()
        self.assertEqual(p.active["action_id"], n.action_id)
        self.assertEqual(p.active["phase"], "prepared")
        self.assertEqual(p.count, 1)
        with self.assertRaises(Rejected):
            p.reserve()
        p.begin_attempt(n, self.target(C1, self.quiet(d)))
        p.register_worker(self.reg(n), AUTH)
        p.admit_delivery(self.receipt(n))
        self.assertEqual(p.count, 1)
        self.assertEqual(len(p.data["history"]), 1)

    def test_S12_lost_acknowledgement(self):
        p, d = self.bootstrap()
        self.assertEqual(self.accept_report(p, d, complete=False), Action.LAUNCH_SUCCESSOR)
        n = p.reserve()
        p.begin_attempt(n, self.target(None, self.quiet(d)))
        p = self.reopen()
        self.assertEqual(p.active["phase"], "uncertain")
        self.assertEqual(p.count, 1)
        with self.assertRaises(Rejected):
            p.begin_attempt(n, self.target(None, self.quiet(d)))
        with self.assertRaises(Rejected):
            p.resume()
        p.pause()
        p.register_worker(self.reg(n), AUTH2)
        p = self.reopen()
        self.assertEqual(p.admit_delivery(self.receipt(n, AUTH2, C2)), Action.WAIT)
        self.assertEqual(p.count, 2)
        self.assertTrue(p.data["paused"])
        self.assertEqual(p.admit_delivery(self.receipt(n, AUTH2, C2)), Action.IGNORE)
        self.assertEqual(p.count, 2)
        p.resume()
        self.assertEqual(self.accept_report(p, n, commit=SHA2, ancestor=SHA1,
                                            cid=C2, auth=AUTH2), Action.STOP_FINISHED)

    def test_S02_finite_action_budget(self):
        p, d = self.bootstrap(action_cap=2)
        self.assertEqual(self.accept_report(p, d, "NEED_MORE_TIME", commit=None),
                         Action.CONTINUE_CURRENT)
        n = p.reserve()
        p.begin_attempt(n, self.target(C1, self.quiet(d)))
        p.register_worker(self.reg(n), AUTH)
        p.admit_delivery(self.receipt(n))
        self.assertEqual(self.accept_report(p, n, "NEED_MORE_TIME", commit=None),
                         Action.CONTINUE_CURRENT)
        with self.assertRaises(Rejected):
            p.reserve()
        self.assertEqual(p.data["hold"], "action_budget")
        self.assertEqual(p.count, 1)
        with self.assertRaises(Rejected):
            p.resume()

    def test_S12_abrupt_process_exit(self):
        for after_callback in (False, True):
            with self.subTest(after_callback=after_callback):
                path = Path(self.temp.name) / ("crash-" + str(after_callback))
                with Proof(path, ROUTE, clock=lambda: self.now) as p:
                    d = p.reserve()
                child = os.fork()
                if child == 0:
                    try:
                        p = Proof(path, clock=lambda: self.now)
                        p.begin_attempt(d, self.target())
                        if after_callback:
                            p.register_worker(self.reg(d), AUTH)
                        os._exit(0)  # intentionally no finally/close/flush beyond durable writes
                    except BaseException:
                        os._exit(1)
                _, status = os.waitpid(child, 0)
                self.assertEqual(os.waitstatus_to_exitcode(status), 0)
                with Proof(path, clock=lambda: self.now) as p:
                    self.assertEqual(p.active["phase"], "uncertain")
                    self.assertEqual(p.count, 0)
                    self.assertEqual(p.active["registration"] is not None, after_callback)
                    with self.assertRaises(Rejected):
                        p.begin_attempt(d, self.target())
                    p.register_worker(self.reg(d), AUTH)
                    self.assertEqual(p.admit_delivery(self.receipt(d)), Action.WAIT)
                    self.assertEqual(p.count, 1)
                    self.assertEqual(p.admit_delivery(self.receipt(d)), Action.IGNORE)

    def test_S06_concurrent_duplicate_callbacks(self):
        p, d = self.bootstrap()
        body = self.report(d, "NEED_MORE_TIME", None)
        barrier = threading.Barrier(8)
        def invoke(_):
            barrier.wait(timeout=3)
            return p.report_worker(body, AUTH)
        with ThreadPoolExecutor(max_workers=8) as pool:
            outcomes = list(pool.map(invoke, range(8)))
        self.assertEqual(outcomes.count("received"), 1)
        self.assertEqual(outcomes.count("duplicate"), 7)
        self.assertEqual(p.evaluate(self.quiet(d)), Action.CONTINUE_CURRENT)
        self.assertEqual(p.evaluate(self.quiet(d)), Action.IGNORE)
        self.assertEqual(len(p.core.state.consumed_responses), 1)

    def test_S02_duplicate_reserve_preserves_existing_action_at_budget(self):
        p = self.open(action_cap=1)
        d = p.reserve()
        with self.assertRaises(Rejected):
            p.reserve()
        self.assertIsNone(p.data["hold"])
        self.assertEqual(p.begin_attempt(d, self.target()), Action.WAIT)

    def test_S13_write_failure_poisoning(self):
        p = self.open()
        d = p.reserve()
        with patch("mcp_native_poc.atomic_write", side_effect=OSError("synthetic failure")):
            with self.assertRaises(OSError):
                p.begin_attempt(d, self.target())
        with self.assertRaises(RuntimeError):
            p.begin_attempt(d, self.target())
        p = self.reopen()
        self.assertEqual(p.active["phase"], "prepared")
        self.assertEqual(p.count, 0)
        p.begin_attempt(d, self.target())
        self.assertEqual(p.active["phase"], "sending")

    def test_S13_corrupt_missing_locked_ledger(self):
        p, d = self.bootstrap()
        path = self.path / "ledger.json"
        with self.assertRaises(BlockingIOError):
            Proof(self.path)
        self.close()
        saved = path.read_text()
        env = json.loads(saved)
        env["payload"]["prior_sha"] = SHA2
        path.write_text(json.dumps(env))
        with self.assertRaises(ValueError):
            Proof(self.path)
        path.unlink()
        with self.assertRaises(FileNotFoundError):
            Proof(self.path)
        with self.assertRaises(FileExistsError):
            Proof(self.path, ROUTE)
        path.write_text(saved)
        p = self.reopen()
        self.assertEqual(p.count, 1)
        with self.assertRaises(Rejected):
            p.report_worker(self.report(d, schema_version="1"), AUTH)



    def test_S13_open_writer_integrity(self):
        # Each supported operation must refuse live loss/corruption or valid
        # but different bytes. A new path or altered envelope is not a reset.
        for damage in ("missing", "corrupt", "different", "lock"):
            for stage in ("attempt", "register", "delivery", "report", "evaluate",
                          "pause", "resume", "reserve", "reader"):
                with self.subTest(damage=damage, stage=stage):
                    path = Path(self.temp.name) / f"{damage}-{stage}"
                    with Proof(path, ROUTE, clock=lambda: self.now) as p:
                        d = p.reserve()
                        if stage != "attempt":
                            p.begin_attempt(d, self.target())
                        if stage not in ("attempt", "register"):
                            p.register_worker(self.reg(d), AUTH)
                        if stage not in ("attempt", "register", "delivery"):
                            p.admit_delivery(self.receipt(d))
                        if stage in ("evaluate", "reader"):
                            p.report_worker(self.report(d), AUTH)
                        ledger = path / "ledger.json"
                        original = ledger.read_bytes()
                        def break_state():
                            if damage == "missing":
                                ledger.unlink()
                            elif damage == "corrupt":
                                ledger.write_bytes(b"broken")
                            elif damage == "different":
                                # Checksummed, semantically plausible different state.
                                env = json.loads(original)
                                env["payload"]["paused"] = not env["payload"]["paused"]
                                from mcp_native_poc import canonical
                                env["sha256"] = digest(canonical(env["payload"]))
                                ledger.write_text(canonical(env))
                            else:
                                (path / "writer.lock").unlink()
                        def reader(*_):
                            if ledger.exists() and ledger.read_bytes() == original and (path / "writer.lock").exists():
                                break_state()
                            return self.remote()
                        calls = {
                            "attempt": lambda: p.begin_attempt(d, self.target()),
                            "register": lambda: p.register_worker(self.reg(d), AUTH),
                            "delivery": lambda: p.admit_delivery(self.receipt(d)),
                            "report": lambda: p.report_worker(self.report(d), AUTH),
                            "evaluate": lambda: p.evaluate(self.quiet(d), lambda *_: self.remote()),
                            "pause": p.pause, "resume": p.resume, "reserve": p.reserve,
                            "reader": lambda: p.evaluate(self.quiet(d), reader),
                        }
                        if stage != "reader":
                            break_state()
                        with self.assertRaises(RuntimeError):
                            calls[stage]()
                        self.assertTrue(p.poisoned)
                        self.assertFalse(p.active["consumed"])
                        if damage == "missing":
                            self.assertFalse(ledger.exists())
                        elif damage == "corrupt":
                            self.assertEqual(ledger.read_bytes(), b"broken")
                        elif damage == "different":
                            self.assertNotEqual(ledger.read_bytes(), original)
                            self.assertEqual(json.loads(ledger.read_bytes())["payload"]["paused"], True)
                        else:
                            self.assertEqual(ledger.read_bytes(), original)
                            self.assertFalse((path / "writer.lock").exists())
                        with self.assertRaises(RuntimeError):
                            p.evaluate(self.quiet(d))
        # Restore is a separate recovery operation; a poisoned writer never
        # becomes usable just because someone puts the bytes back.

    def test_deadline_no_report_late_report_restart(self):
        p, d = self.bootstrap(response_timeout_seconds=10)
        self.assertEqual(p.active["response_deadline"], 110.0)
        self.now = 109.999
        self.assertEqual(p.evaluate(None), Action.WAIT)
        p = self.reopen()
        self.assertEqual(p.active["response_deadline"], 110.0)
        self.now = 110
        self.assertEqual(p.evaluate(None), Action.HOLD)
        self.assertEqual(p.data["hold"], "response_deadline")
        body = self.report(d, "NEED_MORE_TIME", None)
        # A recorded expiry remains held even if the wall clock is adjusted.
        self.now = 109
        self.assertEqual(p.report_worker(body, AUTH), "hold")
        self.assertEqual(p.report_worker(body, AUTH), "duplicate")
        self.assertFalse(p.active["consumed"])
        self.assertIsNone(p.core.state.pending)
        p = self.reopen()
        self.assertEqual(p.evaluate(self.quiet(d)), Action.HOLD)
        with self.assertRaises(Rejected):
            p.resume()
        with self.assertRaises(Rejected):
            p.reserve()

    def test_deadline_late_report_first(self):
        p, d = self.bootstrap(response_timeout_seconds=10)
        self.now = 1000100
        self.assertEqual(p.report_worker(self.report(d, "NEED_MORE_TIME", None), AUTH), "hold")
        self.assertEqual(p.evaluate(self.quiet(d)), Action.HOLD)
        self.assertEqual(p.data["hold"], "response_deadline")
        self.assertFalse(p.active["consumed"])

    def test_deadline_waiting_quiescence_and_reader(self):
        for during_read in (False, True):
            with self.subTest(during_read=during_read):
                self.path = Path(self.temp.name) / f"deadline-{during_read}"
                self.now = 100
                p, d = self.bootstrap(response_timeout_seconds=10)
                p.report_worker(self.report(d), AUTH)
                self.assertEqual(p.evaluate(self.quiet(d, idle=False)), Action.WAIT)
                def reader(*_):
                    self.now = 110
                    return self.remote()
                if not during_read:
                    self.now = 110
                    reader = self.read(self.remote())
                self.assertEqual(p.evaluate(self.quiet(d), reader), Action.HOLD)
                self.assertFalse(p.active["consumed"])
                self.assertEqual(p.data["prior_sha"], BASE)
                self.assertIsNone(p.core.state.pending)
                self.close()

    def test_deadline_late_delivery_and_crash(self):
        p, d = self.bootstrap(bind=False, response_timeout_seconds=10)
        self.now = 110
        self.assertEqual(p.evaluate(None), Action.HOLD)
        p = self.reopen()
        self.assertEqual(p.active["phase"], "uncertain")
        self.assertEqual(p.active["response_deadline"], 110)
        self.assertEqual(p.admit_delivery(self.receipt(d)), Action.HOLD)
        self.assertEqual(p.count, 1)
        self.assertEqual(p.data["hold"], "response_deadline")
        self.assertEqual(p.evaluate(self.quiet(d)), Action.HOLD)
        with self.assertRaises(Rejected):
            p.resume()

    def test_deadline_new_attempt_has_new_window(self):
        p, d = self.bootstrap(response_timeout_seconds=10)
        self.now = 109
        self.assertEqual(self.accept_report(p, d, "NEED_MORE_TIME", commit=None),
                         Action.CONTINUE_CURRENT)
        self.now = 120
        n = p.reserve()
        self.assertIsNone(p.active["response_deadline"])
        self.assertEqual(p.begin_attempt(n, self.target(C1, self.quiet(d))), Action.WAIT)
        self.assertEqual(p.active["response_deadline"], 130)
        self.assertEqual(p.data["history"][0]["response_deadline"], 110)
        p.register_worker(self.reg(n), AUTH)
        p.admit_delivery(self.receipt(n))
        self.now = 129
        self.assertEqual(self.accept_report(p, n), Action.STOP_FINISHED)

    def test_strict_branch_and_policy(self):
        bad = ["work/.hidden", "work/component.lock/next", "HEAD",
               "work/.lock", "work//next", "work/next.lock", "work/next.",
               "work/../next", "work/foo bar", "work/@{oops", "work/foo~bar", "-branch"]
        for branch in bad:
            with self.subTest(branch=branch):
                self.assertNotEqual(subprocess.run(["git", "check-ref-format", "--branch", branch],
                                                   capture_output=True).returncode, 0)
                self.assertFalse(branch_name(branch))
                with self.assertRaises(ValueError):
                    replace(ROUTE, branch=branch)
        for branch in ("main", "work/fixture-20261122", "release/v1.2", "work/-child"):
            self.assertEqual(subprocess.run(["git", "check-ref-format", "--branch", branch],
                                            capture_output=True).returncode, 0)
            self.assertTrue(branch_name(branch))
        for value in (0, -1, True, 86401, 1.5, "10", None):
            with self.assertRaises(ValueError):
                replace(ROUTE, response_timeout_seconds=value)


if __name__ == "__main__":
    unittest.main(verbosity=2)
