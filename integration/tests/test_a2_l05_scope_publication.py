"""A2-L05 targeted scope, approval and Git-publication diagnostic regressions.

No Chrome, network, phone, remote Git changes or real Send.
"""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from owner_reentry import resume_request
from repo_reader import PublishedObservation, PublishedStateError
from runner import Destination, Submitted, initialise, cycle, inspect_state
from succession.composer import ComposerObservation
from succession.core import Config, Controller, RepoView, Response, Action


PROJECT = "g-p-abc123"
REPO = "example-org/fixture"
BRANCH = "work/fixture"
CHAT = "00000000-0000-0000-0000-000000000001"
RESPONSE = "uia-turn-1-aaaaaaaaaaaaaaaaaaaa"
RUN_ID = "c"*24
PUBLISHED_SHA = "a"*40


class L05ScopeAndPublicationTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root=Path(t.name)
        self.state=self.root/"controller.json"
        self.cfg=Config(PROJECT,REPO,BRANCH,3)
        self.c=initialise(self.state,self.cfg,CHAT)

    def test_advanced_worker_not_misreported_as_owner_input_delivered(self):
        response=Response(CHAT,RESPONSE,"CHAT_STATUS: ERROR",project=PROJECT)
        self.c.consume(response)
        self.c.save(self.state)
        context={"request_id":"d"*24,"instruction":"Approve the single mock step",
                 "scope":"One mock fixture line","pointer":"FIXTURE.md",
                 "worker_id":CHAT,"response_id":RESPONSE}
        cfg_path=self.root/"config.json"
        cfg_path.write_text(json.dumps({
            "project":PROJECT,"project_name":"Mock",
            "project_url":"https://chatgpt.com/g/g-p-abc123/project",
            "repo":REPO,"branch":BRANCH,"run_id":RUN_ID,"max_unique_chats":3,
            "repo_dir_wsl":"/tmp/fixture","workflow":"git-handoff"}))
        browser=Mock()
        browser.reentry_disposition.return_value="advanced"
        reader=Mock()
        start=Mock(return_value=21)
        result=resume_request(cfg_path,self.state,{"owner_context":context},
                              "Mock",lambda *_:(browser,reader),start)
        self.assertEqual(result["event"],"worker_advanced_owner_input_unverified")
        self.assertEqual(Controller.load(self.state).unique_count,1)
        self.assertEqual(Controller.load(self.state).state.owner_requests,{})
        self.assertFalse((self.root/f"owner-{context['request_id']}.json").exists())
        browser.send_once.assert_not_called()
        reader.instructions.assert_not_called()
        start.assert_called_once()

    def test_matched_published_sha_logged_then_adopted_after_journal_save(self):
        response=Response(CHAT,RESPONSE,"CHAT_STATUS: TASK_COMPLETE",project=PROJECT)
        publication=PublishedObservation(
            RepoView(REPO,BRANCH,CHAT,False,"Continue mock fixture",True,True),
            PUBLISHED_SHA,RUN_ID,"")
        reader=Mock()
        reader.read.return_value=publication
        browser=Mock()
        browser.observe.return_value=response
        browser.prepare.return_value=Destination(
            PROJECT,None,ComposerObservation(editable_text="",attachments_present=False),123)
        browser.send_once.return_value=Submitted(
            PROJECT,"00000000-0000-0000-0000-000000000002",
            "Continue the work in GitHub repo example-org/fixture, branch work/fixture. Read the current instructions, progress and next task there.",True)
        # Use defer_dispatch so no message/body needs to be simulated.
        with self.assertLogs(level="INFO") as captured:
            result=cycle(self.c,browser,reader,RUN_ID,self.state,defer_dispatch=True)
        self.assertEqual(result,Action.LAUNCH_SUCCESSOR)
        joined="\n".join(captured.output)
        self.assertIn("publication_receipt_verified",joined)
        self.assertIn("publication_receipt_adopted",joined)
        self.assertIn("sha="+PUBLISHED_SHA,joined)
        self.assertIn("ref=refs/heads/"+BRANCH,joined)
        self.assertIn("result=IDENTITY_MATCH",joined)
        self.assertIn("decision=LAUNCH_SUCCESSOR",joined)
        persisted=Controller.load(self.state)
        self.assertEqual(persisted.state.consumed_responses,[[CHAT,RESPONSE]])
        self.assertIsNotNone(persisted.state.pending)
        browser.send_once.assert_not_called()
        self.state.with_name("config.json").write_text(json.dumps({"run_id": RUN_ID}))
        timing = self.state.with_name("controller-timing.log")
        timing.write_text("\n".join(row.removeprefix("INFO:root:") for row in captured.output)
                          + "\n2026-11-20T04:00:00Z publication_receipt_adopted "
                            f"run={RUN_ID} chat={CHAT} response=unknown ref=refs/heads/{BRANCH} "
                            f"sha={'b' * 40} decision=LAUNCH_SUCCESSOR\n",
                          encoding="utf-8")
        before = self.state.read_bytes()
        summary = inspect_state(self.state)
        self.assertEqual(summary["publication_commit"], PUBLISHED_SHA)
        self.assertEqual(summary["publication_ref"], f"refs/heads/{BRANCH}")
        self.assertEqual(self.state.read_bytes(), before)

    def test_invalid_unpublished_receipt_logs_hold_without_adoption(self):
        browser=Mock()
        browser.observe.return_value=Response(
            CHAT,RESPONSE,"CHAT_STATUS: TASK_COMPLETE",project=PROJECT)
        reader=Mock()
        reader.read.side_effect=PublishedStateError("Missing exact remote trailer")
        with self.assertLogs(level="WARNING") as captured:
            result=cycle(self.c,browser,reader,RUN_ID,self.state)
        self.assertEqual(result,Action.HOLD)
        self.assertIn("publication_receipt_rejected","\n".join(captured.output))
        saved=Controller.load(self.state)
        self.assertEqual(saved.state.consumed_responses,[])
        self.assertEqual(saved.checkpoint_branch,BRANCH)
        self.assertIsNone(saved.state.pending)
        browser.prepare.assert_not_called()
        browser.send_once.assert_not_called()


if __name__=="__main__":
    unittest.main()
