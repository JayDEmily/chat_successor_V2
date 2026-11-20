"""ADR 0002 L04 qualification: mocked saved-worker view recovery only."""
from pathlib import Path
import json
import sys
import tempfile
import unittest
from unittest.mock import Mock,patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from windows_backend import WindowsUIA,BrowserObservationError
from runner import initialise,inspect_state
from succession.core import Config

class SavedViewQualification(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.state=Path(temp.name)/"controller.json"
        self.chat="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        self.project="g-p-abcd12"
        self.url="https://chatgpt.com/g/g-p-abcd12-mock-project/project"
        self.cfg=Config(self.project,"example/fixture","work/test",2)
        initialise(self.state,self.cfg,self.chat)
        self.w=WindowsUIA(self.project,"Mock Project",Path(temp.name)/"adapter.ps1",
                          self.state,project_url=self.url)
        self.identity={"project":self.project,"chat_id":self.chat}
        self.partial={**self.identity,"view_status":"observed","window_handle":81,
                      "ready":False,"stop_control":True,
                      "response_id":"uia-turn-1-aaa00000000000000000",
                      "latest_user_digest":"user-turn-123","user_turn_count":1,
                      "user_after_assistant":False}
        self.ready={**self.partial,"ready":True,"stop_control":False,
                    "response_id":"uia-turn-2-bbb00000000000000000",
                    "role":"assistant","text":"CHAT_STATUS: TASK_COMPLETE",
                    "assistant_turn_count":1}
        self.before=self.state.read_bytes()

    def test_v01_missing_view_restores_exact_worker_without_count_change(self):
        self.w._invoke=Mock(side_effect=[
          {**self.identity,"view_status":"missing"},
          {**self.identity,"recovery_status":"restored"},
          self.ready,self.ready])
        with patch("windows_backend.time.sleep"):
            actual=self.w.observe(self.chat)
        self.assertEqual(actual.chat_id,self.chat)
        self.assertEqual([x.args[0] for x in self.w._invoke.call_args_list],
                         ["Observe","RecoverView","Observe","Observe"])
        recovery=self.w._invoke.call_args_list[1].kwargs
        self.assertEqual(recovery["ProjectUrl"],self.url)
        self.assertEqual(recovery["Recovery"],"missing")
        self.assertEqual(recovery["ChatId"],self.chat)
        self.assertEqual(self.state.read_bytes(),self.before)
        self.assertEqual(inspect_state(self.state)["unique_chat_count"],1)

    def test_v02_displaced_view_restores_same_chat_and_duplicate_holds(self):
        self.w._invoke=Mock(side_effect=[
          {**self.identity,"view_status":"missing"},
          {**self.identity,"recovery_status":"restored"},
          {**self.identity,"view_status":"ambiguous"}])
        with self.assertRaisesRegex(BrowserObservationError,"Multiple accessible"):
            self.w.observe(self.chat)
        self.assertEqual(self.w._invoke.call_count,3)
        self.assertEqual(self.state.read_bytes(),self.before)

    def test_v03_stale_original_then_newer_completed_read_is_consumable(self):
        self.w._invoke=Mock(side_effect=[
          self.partial,self.partial,
          {**self.identity,"recovery_status":"refreshed"},
          self.ready,self.ready])
        with patch("windows_backend.time.monotonic",side_effect=[0,120]), \
             patch("windows_backend.time.sleep"):
            self.assertIsNone(self.w.observe(self.chat))
            self.assertIsNone(self.w.observe(self.chat))
            observed=self.w.observe(self.chat)
        self.assertEqual(observed.response_id,self.ready["response_id"])
        self.assertEqual([x.args[0] for x in self.w._invoke.call_args_list],
                         ["Observe","Observe","RecoverView","Observe","Observe"])
        self.assertEqual(self.w._invoke.call_args_list[2].kwargs["SourceResponse"],
                         self.partial["response_id"])
        self.assertEqual(self.state.read_bytes(),self.before)

    def test_v04_uncompleted_fresh_probe_waits_without_send(self):
        self.w._invoke=Mock(side_effect=[
          self.partial,self.partial,{**self.identity,"recovery_status":"waiting"}])
        with patch("windows_backend.time.monotonic",side_effect=[0,120]):
            self.assertIsNone(self.w.observe(self.chat))
            self.assertIsNone(self.w.observe(self.chat))
        self.assertEqual(self.w._invoke.call_count,3)
        self.assertEqual(self.w._progress[0],self.chat)
        self.assertEqual(self.state.read_bytes(),self.before)

    def test_v05_wrong_project_holds_before_recovery_or_send(self):
        self.w._invoke=Mock(return_value={**self.partial,"project":"g-p-wrong"})
        with self.assertRaisesRegex(BrowserObservationError,"registered Project"):
            self.w.observe(self.chat)
        self.w._invoke.assert_called_once()
        self.assertEqual(self.state.read_bytes(),self.before)

    def test_v05_paused_recovery_holds_original_state(self):
        marker=self.state.with_suffix(".pause")
        marker.write_text("Operator pause 1")
        self.w._invoke=Mock(side_effect=[
          {**self.identity,"view_status":"missing"},
          {**self.identity,"recovery_status":"paused"}])
        with self.assertRaisesRegex(BrowserObservationError,"Operator pause"):
            self.w.observe(self.chat)
        self.assertTrue(marker.exists())
        self.assertEqual(self.state.read_bytes(),self.before)

    def test_v06_owner_worker_advanced_is_observation_not_send_receipt(self):
        self.w._invoke=Mock(return_value={**self.identity,"disposition":"advanced"})
        result=self.w.reentry_disposition(self.chat,"uia-turn-1-aaa00000000000000000")
        self.assertEqual(result,"advanced")
        self.w._invoke.assert_called_once_with("ObserveReentry",ChatId=self.chat,
                                 OwnerAnchor="uia-turn-1-aaa00000000000000000")
        self.assertEqual(self.state.read_bytes(),self.before)

if __name__=="__main__":
    unittest.main()
