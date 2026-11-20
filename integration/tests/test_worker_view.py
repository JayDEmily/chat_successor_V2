from pathlib import Path
import json
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from windows_backend import BrowserObservationError, WindowsUIA


class WorkerViewTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.chat = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        self.project = "g-p-abcd12"
        self.url = "https://chatgpt.com/g/g-p-abcd12-exact-project/project"
        self.worker_url = f"https://chatgpt.com/g/g-p-abcd12-exact-project/c/{self.chat}"
        state = Path(folder.name) / "controller.json"
        self.bridge = WindowsUIA(self.project, "Exact Project", Path("adapter.ps1"), state,
                                 project_url=self.url)
        self.adapter = Mock()
        self.bridge._invoke = self.adapter
        self.identity = {"project": self.project, "chat_id": self.chat}
        self.missing = {**self.identity, "view_status": "missing"}
        self.restored = {**self.identity, "recovery_status": "restored"}
        self.partial = {**self.identity, "view_status": "observed", "window_handle": 45,
                        "ready": False, "stop_control": True,
                        "response_id": "uia-turn-1-63adfe00000000000000"}
        self.ready = {**self.partial, "ready": True, "stop_control": False,
                      "role": "assistant", "text": "CHAT_STATUS: TASK_COMPLETE"}

    def test_reopen_missing_worker_and_read_twice_before_returning_response(self):
        self.adapter.side_effect = [self.missing, self.restored, self.ready, self.ready]
        with patch("windows_backend.time.sleep"):
            response = self.bridge.observe(self.chat)
        self.assertEqual(response.chat_id, self.chat)
        self.assertEqual([call.args[0] for call in self.adapter.call_args_list],
                         ["Observe", "RecoverView", "Observe", "Observe"])
        reopen = self.adapter.call_args_list[1].kwargs
        self.assertEqual(reopen["ProjectUrl"], self.url)
        self.assertEqual(reopen["Recovery"], "missing")
        self.assertEqual(reopen["PausePath"], self.bridge.state_path.with_suffix(".pause"))
        self.assertFalse(self.bridge.target_path.exists())

    def test_ambiguous_and_unverified_views_hold_with_saved_link(self):
        for snapshot in ({**self.identity, "view_status": "ambiguous"},
                         {**self.partial, "chat_id": "unexpected"}):
            with self.subTest(snapshot=snapshot):
                self.adapter.reset_mock()
                self.adapter.return_value = snapshot
                with self.assertRaises(BrowserObservationError) as hold:
                    self.bridge.observe(self.chat)
                self.assertIn(self.worker_url, str(hold.exception))
                self.adapter.assert_called_once_with("Observe", ChatId=self.chat)

    def test_missing_recovery_requires_verified_landing_and_single_attempt(self):
        self.bridge.project_url = "https://chatgpt.com/g/g-p-ffff/project"
        self.adapter.return_value = self.missing
        with self.assertRaisesRegex(BrowserObservationError, "verified Project"):
            self.bridge.observe(self.chat)
        self.adapter.assert_called_once()
        self.bridge.project_url = self.url
        self.adapter.reset_mock()
        self.adapter.side_effect = [self.missing, self.restored, self.missing]
        with self.assertRaisesRegex(BrowserObservationError, "disappeared after recovery"):
            self.bridge.observe(self.chat)
        self.assertEqual(self.adapter.call_count, 3)

    def test_stale_detection_resets_on_progress_and_probes_at_agreed_interval(self):
        later = {**self.partial, "response_id": "uia-turn-2-79adfe00000000000000"}
        observations = iter([self.partial, self.partial] + [later] * 5)

        def read(mode, **_kwargs):
            if mode == "Observe":
                return next(observations)
            return {**self.identity, "recovery_status": "waiting"}

        self.adapter.side_effect = read
        with patch("windows_backend.time.monotonic", side_effect=[0, 119, 120, 239, 240, 539, 540]):
            for _ in range(7):
                self.assertIsNone(self.bridge.observe(self.chat))
        probes = [call for call in self.adapter.call_args_list if call.args == ("RecoverView",)]
        self.assertEqual(len(probes), 2)
        for probe in probes:
            self.assertEqual(probe.kwargs["Recovery"], "stale")
            self.assertEqual(probe.kwargs["WindowHandle"], 45)
            self.assertEqual(probe.kwargs["SourceResponse"], later["response_id"])

    def test_consumed_completed_view_can_be_stale_without_replaying_response(self):
        state = {"state": {"consumed_responses": [[self.chat, self.ready["response_id"]]]}}
        self.bridge.state_path.write_text(json.dumps(state), encoding="utf-8")
        refreshed = {**self.identity, "recovery_status": "refreshed"}
        self.adapter.side_effect = [self.ready, self.ready, self.ready, refreshed]
        with patch("windows_backend.time.monotonic", side_effect=[0, 120]), patch("windows_backend.time.sleep"):
            self.assertEqual(self.bridge.observe(self.chat).response_id, self.ready["response_id"])
            self.assertIsNone(self.bridge.observe(self.chat))
        self.assertEqual(self.adapter.call_args.args, ("RecoverView",))
        self.assertEqual(json.loads(self.bridge.state_path.read_text()), state)

    def test_prepared_continuation_and_explicit_resume_restore_exact_worker(self):
        prepared = {"project": self.project, "current_chat_id": self.chat,
                    "private_window_handle": 45, "document_id": "42.45",
                    "editable_text": "", "attachments_present": False}
        self.adapter.side_effect = [self.missing, self.restored, prepared,
                                    self.missing, self.restored, {**self.identity, "disposition": "idle"}]
        self.assertEqual(self.bridge.prepare("CONTINUE_CURRENT", self.chat).current_chat_id, self.chat)
        self.assertEqual(self.bridge.reentry_disposition(self.chat, "hold", release_pause=True), "idle")
        self.assertEqual([call.args[0] for call in self.adapter.call_args_list],
                         ["Prepare", "RecoverView", "Prepare", "ObserveReentry", "RecoverView", "ObserveReentry"])
        self.assertIsNone(self.adapter.call_args_list[4].kwargs["PausePath"])

    def test_unverified_prepared_composer_does_not_replace_target_receipt(self):
        self.bridge.target_path.write_text('{"handle": 32}', encoding="utf-8")
        for chat_id, handle in (("different", 45), (self.chat, 0)):
            with self.subTest(chat_id=chat_id, handle=handle):
                self.adapter.return_value = {"project": self.project, "current_chat_id": chat_id,
                                             "private_window_handle": handle}
                with self.assertRaises(BrowserObservationError):
                    self.bridge.prepare("CONTINUE_CURRENT", self.chat)
                self.assertEqual(json.loads(self.bridge.target_path.read_text()), {"handle": 32})
