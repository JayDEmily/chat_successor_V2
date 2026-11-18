"""L09 scoped fault-hook checks only; these do not constitute live ChatGPT Sends."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch
import os
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runner import Destination, initialise
from succession.composer import ComposerObservation
from succession.core import Action, Config, Controller, RepoView, Response
from windows_backend import BrowserObservationError, WindowsUIA


class L09AdapterFaultTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "controller.json"
        self.cfg = Config("g-p-L09TEST", "JayDEmily/chat_successor",
                          "work/astra-succession-implementation-20261118", 3)
        self.c = initialise(self.path, self.cfg, "chat-first")
        self.w = WindowsUIA(self.cfg.project, "Chat succession folder",
                            Path(self.tmp.name) / "uia_adapter.ps1", self.path)

    def stage_sending(self, kind):
        if kind == Action.CONTINUE_CURRENT:
            response = Response("chat-first", "turn-1", "CHAT_STATUS: NEED_MORE_TIME",
                                project=self.cfg.project)
            decision = self.c.consume(response)
            chat_id = "chat-first"
        else:
            response = Response("chat-first", "turn-1", "CHAT_STATUS: TASK_COMPLETE",
                                project=self.cfg.project)
            repo_view = RepoView(self.cfg.repo, self.cfg.branch, "chat-first",
                                 False, "Next fixture slice", True, True)
            decision = self.c.consume(response, repo_view)
            chat_id = None
        self.assertEqual(decision.action, kind)
        self.c.save(self.path)
        self.c.begin_send(decision.action_id)
        self.c.save(self.path)
        self.w._atomic_target_write({"kind": kind.value,
                                     "source": "chat-first", "handle": 1234})
        target = Destination(self.cfg.project, chat_id,
                             ComposerObservation(editable_text=""),
                             private_window_handle=1234)
        return decision, target

    def test_before_click_has_durable_sending_and_never_invokes_UIA_send(self):
        decision, target = self.stage_sending(Action.CONTINUE_CURRENT)
        self.w._invoke = Mock()
        with patch.dict(os.environ, {"ASTRA_L09_FAULT": "before_click"}):
            with self.assertRaisesRegex(BrowserObservationError, "no click"):
                self.w.send_once(target, decision.message)
        self.w._invoke.assert_not_called()
        self.c.uncertain(decision.action_id, "Injected before-click, no UIA Send invoked")
        self.c.save(self.path)
        restarted = Controller.load(self.path)
        self.assertEqual(restarted.state.pending.phase, "uncertain")
        self.assertEqual(restarted.unique_count, 1)
        restarted.confirm_not_sent(decision.action_id,
                                   "Adapter before-click hook proved _invoke Send never ran")
        restarted.save(self.path)
        rearmed = Controller.load(self.path)
        self.assertEqual(rearmed.state.pending.phase, "prepared")
        self.assertIsNone(rearmed.state.halted)
        self.assertEqual(rearmed.unique_count, 1)

    def check_lost_ack_after_click(self, kind, observed_chat):
        decision, target = self.stage_sending(kind)
        self.w._invoke = Mock(side_effect=BrowserObservationError(
            "Injected after click before acknowledgement"))
        with patch.dict(os.environ, {"ASTRA_L09_FAULT": "after_click"}):
            with self.assertRaisesRegex(BrowserObservationError, "after click"):
                self.w.send_once(target, decision.message)
        self.assertEqual(self.w._invoke.call_count, 1)
        arguments = self.w._invoke.call_args
        self.assertEqual(arguments.args, ("Send",))
        self.assertEqual(arguments.kwargs["L09Fault"], "after_click")
        self.c.uncertain(decision.action_id, "L09 after-click acknowledgement lost")
        self.c.save(self.path)
        restarted = Controller.load(self.path)
        self.assertEqual(restarted.state.pending.phase, "uncertain")
        self.assertEqual(restarted.unique_count, 1)
        # Reconcile uses existing read-only browser seam after restart.
        self.w._invoke = Mock(return_value={
            "project": self.cfg.project, "chat_id": observed_chat,
            "submitted_text": decision.message, "posted_message_observed": True})
        receipt = self.w.reconcile_readonly()
        self.assertTrue(receipt.posted_message_observed)
        self.assertEqual(receipt.submitted_text, decision.message)
        self.assertEqual(self.w._invoke.call_args.args, ("Reconcile",))
        confirmed = restarted.confirm(decision.action_id, receipt.chat_id,
                                      receipt.project, message_observed=True)
        self.assertEqual(confirmed.action, Action.WAIT)
        restarted.save(self.path)
        saved = Controller.load(self.path)
        expected_count = 1 if kind == Action.CONTINUE_CURRENT else 2
        self.assertEqual(saved.unique_count, expected_count)
        self.assertIsNone(saved.state.pending)
        self.assertEqual(saved.confirm(decision.action_id, receipt.chat_id,
                                       receipt.project).action, Action.IGNORE)
        self.assertEqual(saved.unique_count, expected_count)

    def test_after_click_lost_ack_reconciles_successor_once(self):
        self.check_lost_ack_after_click(Action.LAUNCH_SUCCESSOR, "chat-next")

    def test_after_click_lost_ack_reconciles_same_chat_once(self):
        self.check_lost_ack_after_click(Action.CONTINUE_CURRENT, "chat-first")

    def test_unknown_fault_name_does_not_enter_UIA(self):
        decision, target = self.stage_sending(Action.CONTINUE_CURRENT)
        self.w._invoke = Mock()
        with patch.dict(os.environ, {"ASTRA_L09_FAULT": "invalid"}):
            with self.assertRaisesRegex(BrowserObservationError, "Unknown L09"):
                self.w.send_once(target, decision.message)
        self.w._invoke.assert_not_called()


if __name__ == "__main__":
    unittest.main()
