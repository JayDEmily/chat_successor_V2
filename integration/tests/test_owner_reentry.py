import json
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cli
from launch_project import launch_request, matching_runs
from owner_reentry import resume_request
from repo_reader import GitHandoffReader, PublishedStateError
from runner import Destination, Submitted, checkpoint_from_response, cycle, initialise
from succession.composer import ComposerObservation
from succession.core import Action, Config, Controller, Response


PROJECT = "g-p-abc123"
REPO = "example-org/work"
BRANCH = "work/entry"
CHAT = "00000000-0000-0000-0000-000000000001"
HOLD = "uia-turn-1-hold"
REQUEST_ID = "a" * 24
URL = "https://chatgpt.com/g/g-p-abc123/project"


class ReentryTests(unittest.TestCase):
    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.base = Path(folder.name)
        self.cfg = self.base / "config.json"
        self.state = self.base / "controller.json"
        self.cfg.write_text(json.dumps({"project": PROJECT, "project_name": "Project", "repo": REPO,
                                       "branch": BRANCH, "repo_dir_wsl": "/tmp/reader", "run_id": "c" * 24,
                                       "max_unique_chats": 5, "project_url": URL, "workflow": "git-handoff"}))
        controller = initialise(self.state, Config(PROJECT, REPO, BRANCH, 5), CHAT)
        controller.consume(Response(CHAT, HOLD, "CHAT_STATUS: ERROR", project=PROJECT))
        controller.save(self.state)
        self.context = {"instruction": "Yes, approve Zoë's proposal.", "scope": "Review",
                        "pointer": "plan.md", "worker_id": CHAT, "response_id": HOLD,
                        "request_id": REQUEST_ID}
        self.browser = Mock()
        self.browser.reentry_disposition.return_value = "idle"
        self.browser.prepare.return_value = Destination(
            PROJECT, CHAT, ComposerObservation(editable_text="", attachments_present=False), 17)
        self.reader = GitHandoffReader(self.base, REPO, BRANCH)
        self.start = Mock(return_value=42)

    def resume(self, **request):
        return resume_request(self.cfg, self.state, request, "Renamed",
                              lambda *_: (self.browser, self.reader), self.start)

    def test_idle_approval_persists_and_sends_once_without_counting_a_chat(self):
        self.assertEqual(self.resume(owner_context=self.context)["event"], "controller_resumed")
        request_file = self.state.with_name(f"owner-{REQUEST_ID}.json")
        self.assertEqual(json.loads(request_file.read_text(encoding="utf-8")), self.context)
        restored = Controller.load(self.state)
        self.assertEqual(restored.state.last_status, "ERROR")
        self.assertEqual(restored.state.consumed_responses, [[CHAT, HOLD]])
        pointer = restored.state.pending.message
        self.assertTrue(pointer.isascii())
        self.browser.send_once.return_value = Submitted(PROJECT, CHAT, pointer, True)
        self.assertEqual(cycle(restored, self.browser, self.reader, "c" * 24, self.state), Action.WAIT)
        self.assertEqual(self.resume(owner_context=self.context)["event"], "owner_request_already_recorded")
        self.assertEqual(self.resume(owner_context={**self.context, "request_id": "b" * 24})["event"],
                         "owner_hold_already_handled")
        with self.assertRaisesRegex(ValueError, "different content"):
            self.resume(owner_context={**self.context, "scope": "Changed"})
        self.assertEqual(Controller.load(self.state).unique_count, 1)
        self.browser.send_once.assert_called_once()

    def test_advanced_worker_resumes_observation_without_delivery_claim(self):
        self.browser.reentry_disposition.return_value = "advanced"
        self.assertEqual(self.resume(owner_context=self.context)["event"],
                         "worker_advanced_owner_input_unverified")
        self.assertIsNone(Controller.load(self.state).state.pending)
        self.browser.send_once.assert_not_called()

    def test_repeated_prepared_owner_request_can_explicitly_release_pause(self):
        self.resume(owner_context=self.context)
        c = Controller.load(self.state)
        action = c.state.pending.action_id
        c.pause("Operator pause")
        c.save(self.state)
        pause = self.state.with_suffix(".pause")
        pause.touch()
        self.assertEqual(self.resume(owner_context=self.context)["event"], "owner_request_prepared")
        self.assertEqual(self.resume(owner_context=self.context, release_pause=True)["event"],
                         "owner_request_already_recorded")
        self.assertFalse(pause.exists())
        self.assertEqual(Controller.load(self.state).state.pending.action_id, action)

    def test_new_pause_during_scoped_release_is_preserved(self):
        pause = self.state.with_suffix(".pause")
        pause.write_text("original pause", encoding="utf-8")

        def request_pause(*_args, **_kwargs):
            pause.write_text("later pause", encoding="utf-8")
            return "idle"

        self.browser.reentry_disposition.side_effect = request_pause
        outcome = self.resume(owner_context=self.context, release_pause=True)
        self.assertEqual(outcome["event"], "pause_preserved")
        self.assertEqual(pause.read_text(encoding="utf-8"), "later pause")
        controller = Controller.load(self.state)
        self.assertEqual(controller.state.pending.phase, "prepared")
        self.assertTrue(controller.state.halted)
        self.start.assert_not_called()
        self.browser.send_once.assert_not_called()

    def test_worker_advances_after_preparation(self):
        self.resume(owner_context=self.context)
        self.browser.reentry_disposition.return_value = "advanced"
        restored = Controller.load(self.state)
        self.assertEqual(cycle(restored, self.browser, self.reader, "c" * 24, self.state), Action.IGNORE)
        self.assertIsNone(Controller.load(self.state).state.pending)
        self.browser.prepare.assert_not_called()

    def test_uncertain_owner_send_requires_positive_reconciliation(self):
        self.resume(owner_context=self.context)
        controller = Controller.load(self.state)
        pending = controller.state.pending
        controller.begin_send(pending.action_id)
        controller.save(self.state)
        self.browser.reconcile_readonly.return_value = Submitted(PROJECT, CHAT, None, False)
        self.assertEqual(self.resume(owner_context=self.context)["event"], "send_requires_reconciliation")
        self.browser.reconcile_readonly.return_value = Submitted(PROJECT, CHAT, pending.message, True)
        self.assertEqual(self.resume(owner_context=self.context)["event"], "controller_resumed")
        self.assertIsNone(Controller.load(self.state).state.pending)
        self.browser.send_once.assert_not_called()

    def test_keep_pause_and_hold_on_wrong_anchor_or_unreadable_browser(self):
        pause = self.state.with_suffix(".pause")
        pause.touch()
        with self.assertRaisesRegex(ValueError, "operator pause"):
            self.resume(owner_context=self.context)
        with self.assertRaisesRegex(ValueError, "does not|no longer"):
            self.resume(owner_context={**self.context, "response_id": "unexpected"}, release_pause=True)
        self.browser.reentry_disposition.side_effect = RuntimeError("Draft present")
        with self.assertRaisesRegex(RuntimeError, "Draft present"):
            self.resume(owner_context=self.context, release_pause=True)
        self.assertTrue(pause.exists())
        self.start.assert_not_called()

    def test_inspection_maintains_legacy_version_until_mutation(self):
        raw = json.loads(self.state.read_text())
        raw["version"] = 1
        raw["state"].pop("checkpoint_branch")
        raw["state"].pop("owner_requests")
        self.state.write_text(json.dumps(raw))
        self.assertEqual(Controller.load(self.state).checkpoint_branch, BRANCH)
        self.assertEqual(json.loads(self.state.read_text())["version"], 1)
        self.resume(owner_context=self.context)
        self.assertEqual(json.loads(self.state.read_text())["version"], 2)

    def test_missing_registered_journal_is_not_an_initial_send(self):
        runs = self.base / "Runs"
        run = runs / ("c" * 24)
        run.mkdir(parents=True)
        (run / "config.json").write_bytes(self.cfg.read_bytes())
        (run / "bootstrap-intent.json").touch()
        self.assertEqual(matching_runs(runs, PROJECT, REPO)["c" * 24][1]["run_stage"],
                         "initial_send_pending")
        (run / "controller-timing.log").touch()
        with self.assertRaisesRegex(RuntimeError, "journal is missing"):
            matching_runs(runs, PROJECT, REPO)

    def test_terminal_run_survives_pause_and_cycle(self):
        run = self.base / ("c" * 24)
        run.mkdir()
        cfg = run / "config.json"
        state = run / "controller.json"
        cfg.write_bytes(self.cfg.read_bytes())
        pause = state.with_suffix(".pause")
        for reason in ("programme_finished", "chat_cap"):
            with self.subTest(reason=reason):
                controller = Controller.load(self.state)
                controller.state.halted = reason
                controller.save(state)
                before = state.read_bytes()
                args = ["--config", str(cfg), "--state", str(state)]
                with patch.object(sys, "argv", ["cli.py", "pause", *args]), redirect_stdout(StringIO()):
                    cli.main()
                self.assertTrue(pause.exists())
                with patch.object(sys, "argv", ["cli.py", "cycle", *args]), redirect_stdout(StringIO()):
                    cli.main()
                self.assertEqual(state.read_bytes(), before)
                pause.unlink()

    def test_launch_branch_rename_and_explicit_new_job(self):
        path = self.base / "request.json"
        args = {"repo": REPO, "branch": BRANCH, "project_name": "Project", "project_url": URL}
        path.write_text(json.dumps(args))
        with patch("launch_project.provision_reader", return_value="/tmp/reader") as provision, patch(
            "launch_project.launch", return_value={"event": "preflight"}
        ) as launch:
            first = launch_request(path, self.base)
            run = self.base / "Runs" / first["run_id"] / "controller.json"
            path.write_text(json.dumps({**args, "operation": "inspect"}))
            self.assertEqual(launch_request(path, self.base)["run_stage"], "configured")
            intent = run.with_name("bootstrap-intent.json")
            intent.touch()
            self.assertEqual(launch_request(path, self.base)["run_stage"], "initial_send_pending")
            intent.unlink()
            c = initialise(run, Config(PROJECT, REPO, BRANCH, 5), CHAT)
            self.assertEqual(launch_request(path, self.base)["run_stage"], "registered")
            moved = {**args, "branch": "work/other", "project_name": "Renamed"}
            path.write_text(json.dumps(moved))
            self.assertEqual(launch_request(path, self.base)["run_id"], first["run_id"])
            self.assertEqual(launch.call_count, 1)
            request = {**args, "operation": "new", "job_id": "d" * 24}
            path.write_text(json.dumps(request))
            with self.assertRaisesRegex(RuntimeError, "nonterminal"):
                launch_request(path, self.base)
            c.state.halted = "programme_finished"
            c.save(run)
            second = launch_request(path, self.base)
            self.assertNotEqual(second["run_id"], first["run_id"])
            self.assertEqual(launch_request(path, self.base)["event"], "existing_run")
            self.assertEqual(provision.call_count, 2)

    def test_locator_must_be_single_plain_line_before_explicit_completion(self):
        for invalid in ("> CHAT_HANDOFF_BRANCH: foo", "CHAT_HANDOFF_BRANCH: branch..name extra",
                        "CHAT_HANDOFF_BRANCH: foo\nCHAT_HANDOFF_BRANCH: bar",
                        "```\nCHAT_HANDOFF_BRANCH: foo\n```"):
            with self.subTest(invalid=invalid), self.assertRaises(PublishedStateError):
                checkpoint_from_response(invalid + "\nCHAT_STATUS: TASK_COMPLETE", BRANCH)
