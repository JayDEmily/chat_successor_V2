"""A2-L03 independent negative review of published 942474/6dac source.

Synthetic mock adapter only; never opens Chrome or calls Send.
"""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from launch_story import bootstrap
from runner import Destination, initialise
from succession.composer import ComposerObservation
from succession.core import Config, Response, RepoView
from windows_backend import WindowsUIA, BrowserObservationError


class A2L03IndependentNegativeTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.state = self.root / "controller.json"
        self.cfg = Config("g-p-test", "example/fixture", "main", 3)
        self.current = "source-chat"
        self.browser = WindowsUIA(self.cfg.project, "Synthetic", Path("adapter.ps1"), self.state)

    def pending(self, successor=False):
        c = initialise(self.state, self.cfg, self.current)
        response = Response(self.current, "uia-turn-1-aaaaaaaaaaaaaaaaaaaa",
                            "CHAT_STATUS: TASK_COMPLETE" if successor else "CHAT_STATUS: NEED_MORE_TIME",
                            project=self.cfg.project)
        repo = RepoView(self.cfg.repo, self.cfg.branch, self.current, False,
                        "Next fixture slice", True, True) if successor else None
        action = c.consume(response, repo)
        c.save(self.state)
        p = c.state.pending
        record = {"project": self.cfg.project, "handle": 223, "kind": p.kind,
                  "source": p.source_chat_id, "source_response": p.response_id,
                  "action_id": p.action_id,
                  "message_sha256": hashlib.sha256(p.message.encode()).hexdigest(),
                  "route_receipt": None}
        self.browser._atomic_target_write(record)
        return c, action, record

    def test_wrong_destination_project_and_worker_hold_before_browser(self):
        controller, action, record = self.pending()
        controller.begin_send(action.action_id)
        controller.save(self.state)
        self.browser._invoke = Mock(return_value={"project":self.cfg.project,
                                                    "posted_message_observed":True})
        for wrong in (
            Destination("g-p-other", self.current, ComposerObservation(editable_text=""), 223),
            Destination(self.cfg.project, "other-worker", ComposerObservation(editable_text=""), 223),
        ):
            with self.subTest(wrong=wrong):
                with self.assertRaisesRegex(BrowserObservationError, "Prepared destination"):
                    self.browser.send_once(wrong, action.message)
                self.browser._invoke.assert_not_called()

    def test_stale_target_receipt_cannot_supply_old_window_handle(self):
        controller, action, record = self.pending(successor=True)
        record["message_sha256"] = "0"*64
        self.browser._atomic_target_write(record)
        self.browser._invoke = Mock(return_value={
            "project": self.cfg.project, "current_chat_id": None,
            "private_window_handle": 224,
            "editable_text": "", "attachments_present": False
        })
        target = self.browser.prepare("LAUNCH_SUCCESSOR", self.current)
        self.assertEqual(target.private_window_handle, 224)
        self.assertNotIn("WindowHandle", self.browser._invoke.call_args.kwargs)
        updated = json.loads(self.browser.target_path.read_text())
        self.assertEqual(updated["action_id"], action.action_id)
        self.assertEqual(updated["message_sha256"],
                         hashlib.sha256(action.message.encode()).hexdigest())

    def test_bound_initial_intent_route_change_blocks_before_reconcile(self):
        cfg = {"project":self.cfg.project,"repo":self.cfg.repo,"branch":"main",
               "run_id":"a"*24,"max_unique_chats":3,"route_receipt":"a"*64}
        browser = Mock()
        browser.project = self.cfg.project
        browser.prepare.return_value = Destination(
            self.cfg.project, None, ComposerObservation(editable_text="", attachments_present=False), 114)
        browser._invoke.return_value = {}
        reader = Mock()
        reader.heads.return_value = {"main":"seed"}
        with self.assertRaisesRegex(RuntimeError, "Initial Send is held"):
            bootstrap(cfg, self.state, browser, reader)
        before = (self.root/"bootstrap-intent.json").read_bytes()
        browser._invoke.reset_mock()
        with self.assertRaisesRegex(RuntimeError, "changed run, route or message"):
            bootstrap({**cfg, "route_receipt":"b"*64}, self.state, browser, reader)
        browser._invoke.assert_not_called()
        self.assertEqual((self.root/"bootstrap-intent.json").read_bytes(), before)

    def test_initial_preclick_pause_keeps_original_intent_without_new_send(self):
        cfg = {"project":self.cfg.project,"repo":self.cfg.repo,"branch":"main",
               "run_id":"b"*24,"max_unique_chats":3}
        browser = Mock()
        browser.project = self.cfg.project
        browser.prepare.return_value = Destination(
            self.cfg.project, None, ComposerObservation(editable_text="", attachments_present=False), 115)
        browser._invoke.return_value = {"paused_before_click":True}
        reader = Mock()
        reader.heads.return_value = {"main":"seed"}
        with self.assertRaisesRegex(RuntimeError, "durable intent retained"):
            bootstrap(cfg, self.state, browser, reader)
        original = (self.root/"bootstrap-intent.json").read_bytes()
        with self.assertRaisesRegex(RuntimeError, "Initial Send is held"):
            bootstrap(cfg, self.state, browser, reader)
        self.assertEqual([call.args[0] for call in browser._invoke.call_args_list],
                         ["Send","Reconcile"])
        self.assertEqual((self.root/"bootstrap-intent.json").read_bytes(), original)
        self.assertFalse(self.state.exists())

    def test_bound_account_without_receipt_rejects_adapter_send(self):
        controller, action, record = self.pending()
        controller.begin_send(action.action_id)
        controller.save(self.state)
        self.state.with_name("config.json").write_text(
            json.dumps({"account_key":"shoco"}))
        self.browser._invoke = Mock()
        target = Destination(self.cfg.project, self.current, ComposerObservation(editable_text=""), 223)
        with self.assertRaisesRegex(BrowserObservationError, "Invalid private account route receipt"):
            self.browser.send_once(target, action.message)
        self.browser._invoke.assert_not_called()


if __name__ == "__main__":
    unittest.main()
