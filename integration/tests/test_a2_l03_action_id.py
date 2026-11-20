"""L03 action-ID and exact source/target safety checks; mock browser only."""
from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest
from unittest.mock import Mock

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from windows_backend import WindowsUIA,BrowserObservationError
from runner import Destination,initialise
from succession.composer import ComposerObservation
from succession.core import Action, Config,Controller,Response,RepoView

WORKER = "00000000-0000-0000-0000-000000000001"
DOCUMENT = "42.222"

class L03ActionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.state=Path(self.tmp.name)/"controller.json"
        self.cfg=Config("g-p-TEST","example/fixture","work/test",2)
        self.c=initialise(self.state,self.cfg,WORKER)
        self.w=WindowsUIA(self.cfg.project,"Fixture",Path(self.tmp.name)/"adapter.ps1",self.state)
        self.response=Response(WORKER,"uia-turn-1-aaa00000000000000000",
                               "CHAT_STATUS: NEED_MORE_TIME",project=self.cfg.project)

    def stage(self,kind=Action.CONTINUE_CURRENT, uncertain=False):
        if kind==Action.CONTINUE_CURRENT:
            decision=self.c.consume(self.response)
            chat=WORKER
        else:
            resp=Response(WORKER,self.response.response_id,
                          "CHAT_STATUS: TASK_COMPLETE",project=self.cfg.project)
            pub=RepoView(self.cfg.repo,self.cfg.branch,WORKER,
                         False,"Next mock slice",True,True)
            decision=self.c.consume(resp,pub)
            chat=None
        self.c.save(self.state)
        pending=self.c.state.pending
        target=Destination(self.cfg.project,chat,ComposerObservation(editable_text=""),222,DOCUMENT)
        record={"kind":pending.kind,"source":pending.source_chat_id,"handle":222,"document_id":DOCUMENT,
                "project":self.cfg.project,"source_response":pending.response_id,
                "action_id":pending.action_id,
                "message_sha256":hashlib.sha256(pending.message.encode()).hexdigest(),
                "route_receipt":None}
        self.w._atomic_target_write(record)
        self.c.begin_send(decision.action_id)
        if uncertain:self.c.uncertain(decision.action_id,"Test lost ack")
        self.c.save(self.state)
        return decision,target,record

    def test_s09_stale_action_id_never_enters_browser(self):
        d,t,record=self.stage()
        record["action_id"]="stale-action-id"
        self.w._atomic_target_write(record)
        self.w._invoke=Mock()
        with self.assertRaisesRegex(BrowserObservationError,"identity mismatch"):
            self.w.send_once(t,d.message)
        self.w._invoke.assert_not_called()

    def test_s09_wrong_message_digest_never_enters_browser(self):
        d,t,record=self.stage()
        record["message_sha256"]="0"*64
        self.w._atomic_target_write(record)
        self.w._invoke=Mock()
        with self.assertRaisesRegex(BrowserObservationError,"identity mismatch"):
            self.w.send_once(t,d.message)
        self.w._invoke.assert_not_called()

    def test_s09_wrong_response_anchor_never_enters_browser(self):
        d,t,record=self.stage()
        record["source_response"]="wrong-trigger-response"
        self.w._atomic_target_write(record)
        self.w._invoke=Mock()
        with self.assertRaisesRegex(BrowserObservationError,"identity mismatch"):
            self.w.send_once(t,d.message)
        self.w._invoke.assert_not_called()

    def test_s09_wrong_project_and_handle_block(self):
        decision,target,record=self.stage()
        for changed,value in (("project","g-p-other"),("handle",333),("document_id","42.333"),
                              ("kind","LAUNCH_SUCCESSOR")):
            with self.subTest(changed=changed):
                self.w._atomic_target_write({**record,changed:value})
                self.w._invoke=Mock()
                with self.assertRaisesRegex(BrowserObservationError,"identity mismatch"):
                    self.w.send_once(target,decision.message)
                self.w._invoke.assert_not_called()

    def test_s09_bound_route_receipt_not_substitutable(self):
        d,t,record=self.stage()
        self.w.route_receipt = "a" * 64
        self.w.profile_path = r"C:\Mock Chrome\Profile 1"
        self.w.chrome_app_id = "Chrome.Mock"
        cfg={"account_key": "shoco", "route_receipt": self.w.route_receipt,
             "chrome_profile_path": self.w.profile_path, "chrome_app_id": self.w.chrome_app_id}
        self.state.with_name("config.json").write_text(json.dumps(cfg))
        self.w._invoke=Mock()
        with self.assertRaisesRegex(BrowserObservationError,"identity mismatch"):
            self.w.send_once(t,d.message)
        self.w._invoke.assert_not_called()

    def test_s05_uncertain_reconcile_rejects_old_target_action(self):
        d,t,record=self.stage(uncertain=True)
        record["action_id"]="wrong-old-action"
        self.w._atomic_target_write(record)
        self.w._invoke=Mock()
        with self.assertRaisesRegex(BrowserObservationError,"identity mismatch"):
            self.w.reconcile_readonly()
        self.w._invoke.assert_not_called()
        self.assertEqual(Controller.load(self.state).state.pending.phase,"uncertain")

    def test_s05_uncertain_reconcile_exact_action_and_anchor_once(self):
        d,t,record=self.stage(uncertain=True)
        self.w._invoke=Mock(return_value={
          "project":self.cfg.project,"chat_id":WORKER,
          "submitted_text":d.message,"posted_message_observed":True})
        receipt=self.w.reconcile_readonly()
        self.assertTrue(receipt.posted_message_observed)
        kw=self.w._invoke.call_args.kwargs
        self.assertEqual(kw["PrepareAction"],d.action_id)
        self.assertEqual(kw["PrepareTargetPath"],self.w.target_path.resolve())
        restarted=Controller.load(self.state)
        confirmed=restarted.confirm(d.action_id,receipt.chat_id,receipt.project,message_observed=True)
        restarted.save(self.state)
        self.assertEqual(restarted.unique_count,1)
        self.assertEqual(restarted.confirm(d.action_id,receipt.chat_id,receipt.project).action,Action.IGNORE)

    def test_s09_send_carries_original_action_id_to_ps_boundary(self):
        d,t,record=self.stage()
        self.w._invoke=Mock(return_value={
          "project":self.cfg.project,"chat_id":WORKER,
          "submitted_text":d.message,"posted_message_observed":True})
        receipt=self.w.send_once(t,d.message)
        self.assertTrue(receipt.posted_message_observed)
        kw=self.w._invoke.call_args.kwargs
        self.assertEqual(kw["PrepareAction"],d.action_id)
        self.assertEqual(kw["PrepareTargetPath"],self.w.target_path.resolve())
        self.assertEqual(kw["SourceResponse"],self.response.response_id)
        self.assertEqual(kw["DocumentId"], DOCUMENT)

    def test_s09_prepare_records_action_id_for_continuation(self):
        d=self.c.consume(self.response)
        self.c.save(self.state)
        self.w._invoke=Mock(return_value={
          "project":self.cfg.project,"current_chat_id":WORKER,
          "private_window_handle":222,"document_id":DOCUMENT,
          "editable_text":"","attachments_present":False})
        target=self.w.prepare("CONTINUE_CURRENT",WORKER)
        self.assertEqual(target.private_window_handle,222)
        record=json.loads(self.w.target_path.read_text())
        self.assertEqual(record["action_id"],d.action_id)
        self.assertEqual(record["source_response"],self.response.response_id)
        self.assertEqual(record["project"],self.cfg.project)
        self.assertEqual(record["document_id"], DOCUMENT)
        self.assertEqual(record["message_sha256"],hashlib.sha256(d.message.encode()).hexdigest())

if __name__=="__main__":
    unittest.main()
