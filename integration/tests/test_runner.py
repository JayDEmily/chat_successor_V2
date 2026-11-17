"""Local simulated integration checks; none are live ChatGPT evidence."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runner import (
    Destination, Submitted, cycle, dispatch_prepared, initialise, inspect_state,
)
from succession.composer import ComposerObservation
from succession.core import Action, Config, Controller, Response, RepoView


CFG = Config(project="g-p-TEST", repo="JayDEmily/chat_successor",
             branch="trial/test-run", max_unique_chats=2)


class SyntheticBrowser:
    def __init__(self, *, draft="", project=None, failure=None):
        self.draft = draft
        self.project = project or CFG.project
        self.failure = failure
        self.calls = []
        self.response = None

    def observe(self, expected_chat_id):
        self.calls.append("observe")
        return self.response

    def prepare(self, kind, current_chat_id):
        self.calls.append("prepare")
        if self.failure == "prepare":
            raise RuntimeError("Injected target failure")
        return Destination(self.project,
                           current_chat_id if kind == Action.CONTINUE_CURRENT.value else None,
                           ComposerObservation(editable_text=self.draft),
                           private_window_handle=100)

    def send_once(self, target, message):
        self.calls.append("send")
        if self.failure == "after_send":
            raise RuntimeError("Injected lost acknowledgement")
        return Submitted(self.project,
                         "chat-next" if target.current_chat_id is None else target.current_chat_id,
                         message, True)


class Reader:
    def __init__(self, *, programme_complete=False, publication=True):
        self.calls = 0
        self.programme_complete = programme_complete
        self.publication = publication

    def read(self, expected_run):
        self.calls += 1
        if not self.publication:
            raise RuntimeError("Injected remote fetch outage")
        class O: pass
        o = O()
        o.view = RepoView(CFG.repo, CFG.branch, "chat-first",
                          self.programme_complete,
                          None if self.programme_complete else "Next fixture slice")
        return o


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "state.json"
        self.controller = initialise(self.path, CFG, "chat-first")

    def tearDown(self):
        self.tmp.cleanup()

    def response(self, text="CHAT_STATUS: TASK_COMPLETE", response_id="turn1", complete=True):
        return Response("chat-first", response_id, text,
                        complete=complete, project=CFG.project)

    def test_first_run_is_counted_and_never_overwritten(self):
        self.assertEqual(inspect_state(self.path)["unique_chat_count"], 1)
        with self.assertRaises(FileExistsError):
            initialise(self.path, CFG, "another")

    def test_published_task_complete_launches_once(self):
        b = SyntheticBrowser()
        b.response = self.response()
        r = Reader()
        self.assertEqual(cycle(self.controller, b, r, "test", self.path), Action.WAIT)
        self.assertEqual(self.controller.unique_count, 2)
        self.assertEqual(self.controller.state.current_chat_id, "chat-next")
        self.assertEqual(b.calls, ["observe", "prepare", "send"])
        self.assertEqual(r.calls, 1)
        self.assertEqual(Controller.load(self.path).unique_count, 2)

    def test_continuation_at_cap_does_not_create_new_chat(self):
        self.controller.config = Config(CFG.project, CFG.repo, CFG.branch, 1)
        b = SyntheticBrowser()
        b.response = self.response("CHAT_STATUS: NEED_MORE_TIME")
        self.assertEqual(cycle(self.controller, b, Reader(), "test", self.path), Action.WAIT)
        self.assertEqual(self.controller.unique_count, 1)
        self.assertEqual(b.calls.count("send"), 1)

    def test_draft_is_preserved_and_no_send(self):
        b = SyntheticBrowser(draft="New chat in Chat succession folder")
        b.response = self.response()
        self.assertEqual(cycle(self.controller, b, Reader(), "test", self.path), Action.HOLD)
        self.assertEqual(b.calls.count("send"), 0)
        self.assertEqual(self.controller.state.pending.phase, "prepared")
        self.assertIsNotNone(self.controller.state.halted)

    def test_value_only_never_proves_empty(self):
        class ValueOnlyBrowser(SyntheticBrowser):
            def prepare(self, kind, current_chat_id):
                self.calls.append("prepare")
                return Destination(CFG.project, None,
                                   ComposerObservation(uia_value="New chat",
                                                       placeholder="New chat"),
                                   100)
        b = ValueOnlyBrowser()
        b.response = self.response()
        self.assertEqual(cycle(self.controller, b, Reader(), "test", self.path), Action.HOLD)
        self.assertEqual(b.calls.count("send"), 0)

    def test_wrong_project_no_send(self):
        b = SyntheticBrowser(project="other-project")
        b.response = self.response()
        self.assertEqual(cycle(self.controller, b, Reader(), "test", self.path), Action.HOLD)
        self.assertNotIn("send", b.calls)

    def test_lost_ack_persists_uncertain_and_restart_hold(self):
        b = SyntheticBrowser(failure="after_send")
        b.response = self.response()
        self.assertEqual(cycle(self.controller, b, Reader(), "test", self.path), Action.HOLD)
        self.assertEqual(b.calls.count("send"), 1)
        restarted = Controller.load(self.path)
        self.assertEqual(restarted.state.pending.phase, "uncertain")
        self.assertIsNotNone(restarted.state.halted)
        self.assertEqual(cycle(restarted, b, Reader(), "test", self.path), Action.HOLD)
        self.assertEqual(b.calls.count("send"), 1)

    def test_preparation_failures_do_not_begin_send(self):
        b = SyntheticBrowser(failure="prepare")
        b.response = self.response()
        self.assertEqual(cycle(self.controller, b, Reader(), "test", self.path), Action.HOLD)
        self.assertEqual(self.controller.state.pending.phase, "prepared")

    def test_streaming_never_dispatches(self):
        b = SyntheticBrowser()
        b.response = self.response(complete=False)
        self.assertEqual(cycle(self.controller, b, Reader(), "test", self.path), Action.WAIT)
        self.assertEqual(b.calls, ["observe"])

    def test_finished_programme_stops_without_composer(self):
        b = SyntheticBrowser()
        b.response = self.response()
        self.assertEqual(cycle(self.controller, b, Reader(programme_complete=True),
                               "test", self.path), Action.STOP_FINISHED)
        self.assertEqual(b.calls, ["observe"])

    def test_duplicate_completed_response_has_no_second_send(self):
        b = SyntheticBrowser()
        b.response = self.response()
        self.assertEqual(cycle(self.controller, b, Reader(), "test", self.path), Action.WAIT)
        b.response = Response("chat-next", "turn1", "CHAT_STATUS: NEED_MORE_TIME",
                              project=CFG.project)
        self.assertEqual(cycle(self.controller, b, Reader(), "test", self.path), Action.WAIT)
        self.assertEqual(self.controller.unique_count, 2)


if __name__ == "__main__":
    unittest.main()
