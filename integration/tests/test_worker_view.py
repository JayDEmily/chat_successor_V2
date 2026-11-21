from pathlib import Path
import json
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runner import cycle, initialise
from succession.core import Action, Config, Controller
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
                        "response_id": "uia-turn-1-63adfe00000000000000",
                        "latest_user_digest": "63adef00000000000000"}
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

    def test_chrome_read_requires_two_live_matching_samples(self):
        first = {**self.ready, "method": "CHROME_DOM", "chrome_read_at": 1000}
        self.adapter.side_effect = [first, first, first, {**first, "chrome_read_at": 2000}]
        with patch("windows_backend.time.sleep"):
            self.assertIsNone(self.bridge.observe(self.chat))
            self.assertEqual(self.bridge.observe(self.chat).response_id, first["response_id"])

    def test_saved_reply_identity_holds_reader_changes_and_regeneration(self):
        chrome_turn = "chrome-turn-11111111-1111-1111-1111-111111111111-22222222-2222-2222-2222-222222222222"
        regenerated = "chrome-turn-11111111-1111-1111-1111-111111111111-33333333-3333-3333-3333-333333333333"
        legacy_turn = self.ready["response_id"]
        for consumed, current in ((legacy_turn, chrome_turn), (chrome_turn, legacy_turn),
                                  (chrome_turn, regenerated)):
            with self.subTest(consumed=consumed, current=current):
                state = {"state": {"consumed_responses": [[self.chat, consumed]]}}
                self.bridge.state_path.write_text(json.dumps(state), encoding="utf-8")
                self.adapter.side_effect = [{**self.ready, "response_id": current}]
                with self.assertRaises(BrowserObservationError) as hold:
                    self.bridge.observe(self.chat)
                self.assertIn(self.worker_url, str(hold.exception))
                self.assertEqual(json.loads(self.bridge.state_path.read_text()), state)

    def test_unqualified_view_waits_for_streaming_then_saves_hold(self):
        state = self.bridge.state_path
        controller = initialise(state, Config(self.project, "example/fixture", "work/test", 2), self.chat)
        reader = Mock()
        observation = {**self.identity, "ready": False, "stop_control": True,
                       "method": "UIA_VIRTUALIZED_UNQUALIFIED"}
        self.adapter.return_value = observation
        before = state.read_bytes()
        self.assertEqual(cycle(controller, self.bridge, reader, "test", state), Action.WAIT)
        self.assertEqual(state.read_bytes(), before)
        self.adapter.assert_called_once_with("Observe", ChatId=self.chat)

        self.adapter.reset_mock()
        self.adapter.return_value = {**observation, "stop_control": False}
        self.assertEqual(cycle(controller, self.bridge, reader, "test", state), Action.HOLD)
        saved = Controller.load(state)
        self.assertIn("unqualified", saved.state.halted)
        self.assertIn(self.worker_url, saved.state.halted)
        self.assertIsNone(saved.state.pending)
        self.assertEqual(saved.state.consumed_responses, [])
        self.assertEqual(saved.unique_count, 1)
        self.assertEqual(cycle(saved, self.bridge, reader, "test", state), Action.HOLD)
        self.adapter.assert_called_once_with("Observe", ChatId=self.chat)
        reader.read.assert_not_called()

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

    def test_stall_timer_resets_on_progress_then_holds_without_a_probe(self):
        state = self.bridge.state_path
        controller = initialise(state, Config(self.project, "example/fixture", "work/test", 2), self.chat)
        reader = Mock()
        later = {**self.partial, "response_id": "uia-turn-2-79adfe00000000000000"}
        observations = iter([self.partial, self.partial] + [later] * 3)

        def read(mode, **_kwargs):
            if mode == "Observe":
                return next(observations)
            return {**self.identity, "recovery_status": "waiting"}

        self.adapter.side_effect = read
        with patch("windows_backend.time.monotonic", side_effect=[0, 119, 120, 239, 240]):
            for _ in range(4):
                self.assertEqual(cycle(controller, self.bridge, reader, "test", state), Action.WAIT)
            self.assertEqual(cycle(controller, self.bridge, reader, "test", state), Action.HOLD)
        saved = Controller.load(state)
        self.assertIn("stalled", saved.state.halted)
        self.assertIn(self.worker_url, saved.state.halted)
        self.assertIsNone(saved.state.pending)
        self.assertEqual(saved.state.consumed_responses, [])
        self.assertEqual(saved.unique_count, 1)
        self.assertEqual([call.args[0] for call in self.adapter.call_args_list], ["Observe"] * 5)
        reader.read.assert_not_called()

    def test_reopened_view_without_turn_anchors_cannot_arm_the_stall_timer(self):
        unqualified = {**self.identity, "view_status": "observed", "window_handle": 45,
                       "ready": False}
        self.adapter.side_effect = [self.missing, self.restored, unqualified,
                                    unqualified, unqualified]
        with patch("windows_backend.time.monotonic") as clock:
            for _ in range(3):
                self.assertIsNone(self.bridge.observe(self.chat))
            clock.assert_not_called()
        self.assertEqual([call.args[0] for call in self.adapter.call_args_list],
                         ["Observe", "RecoverView", "Observe", "Observe", "Observe"])
        self.assertIsNone(self.bridge._progress)

    def test_consumed_chrome_reply_holds_without_a_probe_or_state_change(self):
        response_id = "chrome-turn-11111111-1111-1111-1111-111111111111-22222222-2222-2222-2222-222222222222"
        turn = {**self.ready, "method": "CHROME_DOM", "response_id": response_id}
        del turn["latest_user_digest"]
        state = {"state": {"consumed_responses": [[self.chat, response_id]]}}
        self.bridge.state_path.write_text(json.dumps(state), encoding="utf-8")
        self.adapter.side_effect = [{**turn, "chrome_read_at": timestamp} for timestamp in (1000, 2000, 3000, 4000)]
        with patch("windows_backend.time.monotonic", side_effect=[0, 120]), patch("windows_backend.time.sleep"):
            self.assertEqual(self.bridge.observe(self.chat).response_id, response_id)
            with self.assertRaisesRegex(BrowserObservationError, "stalled") as hold:
                self.bridge.observe(self.chat)
        self.assertIn(self.worker_url, str(hold.exception))
        self.assertEqual([call.args[0] for call in self.adapter.call_args_list], ["Observe"] * 3)
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
