from pathlib import Path
import json
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from launch_story import bootstrap
from launch_project import launch_request
from repo_reader import GitHandoffReader, GitStoryReader, PublishedStateError, STORY_REPO, STORY_TURNS
from runner import Destination, Submitted, cycle, initialise
from succession.composer import ComposerObservation
from succession.core import Action, Config, Response


PROJECT = "g-p-story-test"
CHATS = [f"00000000-0000-0000-0000-{step:012}" for step in range(1, 5)]


def git(path, *args):
    return subprocess.check_output(
        ["git", "-C", str(path), *args], text=True, stderr=subprocess.PIPE,
    ).strip()


class StoryTests(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        git(self.root, "init", "--bare", "--initial-branch=main", "remote.git")
        self.remote = self.root / "remote.git"
        git(self.root, "clone", str(self.remote), "writer")
        self.writer = self.root / "writer"
        git(self.writer, "config", "user.name", "Story Test")
        git(self.writer, "config", "user.email", "story-test@example.invalid")
        (self.writer / "README.md").write_text("Story instructions\n")
        git(self.writer, "add", "README.md")
        git(self.writer, "commit", "-m", "Seed")
        git(self.writer, "push", "origin", "main")
        git(self.root, "clone", str(self.remote), "reader")
        self.reader = GitStoryReader(self.root / "reader")
        self.reader._verify_origin = Mock()  # Disposable remote; all fetches use real Git.

    def publish(self, step, *, chat_id=None):
        branch, speaker = STORY_TURNS[step]
        git(self.writer, "switch", "-c", branch)
        with (self.writer / "STORY.md").open("a") as story:
            story.write(f"{speaker}: A short line for turn {step + 1}.\n")
        git(self.writer, "add", "STORY.md")
        git(self.writer, "commit", "-m", "Publish one turn",
            "-m", f"Chat-ID: {chat_id or CHATS[step]}")
        git(self.writer, "push", "origin", branch)

    def test_four_published_branches_launch_three_successors_then_stop(self):
        path = self.root / "controller.json"
        controller = initialise(path, Config(PROJECT, STORY_REPO, "main", 4), CHATS[0])
        browser = Mock()
        browser.prepare.return_value = Destination(
            PROJECT, None, ComposerObservation(editable_text="", attachments_present=False), 10)
        for step, chat_id in enumerate(CHATS):
            self.publish(step)
            browser.observe.return_value = Response(
                chat_id, f"turn-{step}", "CHAT_STATUS: TASK_COMPLETE", project=PROJECT)
            if step < 3:
                expected_pointer = (
                    f"Continue the work in GitHub repo {STORY_REPO}, branch main. "
                    "Read the current instructions, progress and next task there."
                )
                browser.send_once.return_value = Submitted(PROJECT, CHATS[step + 1], expected_pointer, True)
            result = cycle(controller, browser, self.reader, "story", path)
            self.assertEqual(result, Action.WAIT if step < 3 else Action.STOP_FINISHED)
        self.assertEqual(browser.send_once.call_count, 3)
        self.assertEqual(controller.state.unique_chat_ids, CHATS)
        self.assertIsNone(controller.state.pending)

    def test_gap_holds(self):
        self.publish(1)
        with self.assertRaisesRegex(PublishedStateError, "without gaps"):
            self.reader.read("story")

    def test_duplicate_worker_holds(self):
        self.publish(0)
        self.publish(1, chat_id=CHATS[0])
        with self.assertRaisesRegex(PublishedStateError, "distinct saved Chat-ID"):
            self.reader.read("story")

    def publish_handoff(self, chat_id, next_task, run="demo", branch="main"):
        with (self.writer / "NOTES.md").open("a") as notes:
            notes.write("Work verified by the worker.\n")
        git(self.writer, "add", "NOTES.md")
        git(self.writer, "commit", "-m", "Publish ordinary work",
            "-m", f"Chat-Succession-Run: {run}\nChat-ID: {chat_id}\nChat-Succession-Next: {next_task}")
        git(self.writer, "push", "origin", branch)

    def test_generic_handoff_uses_only_trailers_and_project_reader(self):
        repo = "example-org/ordinary-project"
        reader = GitHandoffReader(self.root / "reader", repo, "main")
        reader._verify_origin = Mock()
        path = self.root / "controller.json"
        controller = initialise(path, Config(PROJECT, repo, "main", 3), CHATS[0])
        browser = Mock()
        browser.prepare.return_value = Destination(
            PROJECT, None, ComposerObservation(editable_text="", attachments_present=False), 10)
        expected = (
            f"Continue the work in GitHub repo {repo}, branch main. "
            "Read the current instructions, progress and next task there."
        ) + reader.instructions("demo", 2)
        browser.send_once.return_value = Submitted(PROJECT, CHATS[1], expected, True)
        self.publish_handoff(CHATS[0], "Read the next authorized item")
        browser.observe.return_value = Response(CHATS[0], "a", "CHAT_STATUS: TASK_COMPLETE", project=PROJECT)
        self.assertEqual(cycle(controller, browser, reader, "demo", path), Action.WAIT)
        self.assertEqual(browser.send_once.call_args.args[1], expected)
        self.publish_handoff(CHATS[1], "FINISHED")
        browser.observe.return_value = Response(CHATS[1], "b", "CHAT_STATUS: TASK_COMPLETE", project=PROJECT)
        self.assertEqual(cycle(controller, browser, reader, "demo", path), Action.STOP_FINISHED)
        self.assertEqual(browser.send_once.call_count, 1)

    def test_generic_stale_run_and_published_hold_are_refused(self):
        reader = GitHandoffReader(self.root / "reader", "example-org/ordinary-project", "main")
        reader._verify_origin = Mock()
        self.publish_handoff(CHATS[0], "HOLD", run="old")
        with self.assertRaisesRegex(PublishedStateError, "different run"):
            reader.read("demo")
        with self.assertRaisesRegex(PublishedStateError, "on hold"):
            reader.read("old")

    def test_generic_empty_duplicate_trailer_holds(self):
        reader = GitHandoffReader(self.root / "reader", "example-org/ordinary-project", "main")
        reader._verify_origin = Mock()
        self.publish_handoff(CHATS[0], "\nChat-Succession-Next: FINISHED")
        with self.assertRaisesRegex(PublishedStateError, "one Chat-Succession-Next trailer"):
            reader.read("demo")

    def test_git_timeout_is_a_publication_error(self):
        reader = GitHandoffReader(self.root / "reader", "example-org/ordinary-project", "main")
        reader._verify_origin = Mock()
        with patch("repo_reader.subprocess.run", side_effect=subprocess.TimeoutExpired("git", 45)):
            with self.assertRaisesRegex(PublishedStateError, "Git fetch did not finish"):
                reader.read("demo")

    def test_published_checkpoint_rotates_once_and_survives_restart(self):
        repo = "example-org/ordinary-project"
        reader = GitHandoffReader(self.root / "reader", repo, "main")
        branch = "work/next"
        git(self.writer, "switch", "-c", branch)
        self.publish_handoff(CHATS[1], "Next task", branch=branch)
        path = self.root / "controller.json"
        controller = initialise(path, Config(PROJECT, repo, "main", 3), CHATS[0])
        browser = Mock()
        browser.observe.return_value = Response(
            CHATS[0], "a", "CHAT_HANDOFF_BRANCH: work/next\nCHAT_STATUS: TASK_COMPLETE", project=PROJECT)
        with patch("repo_reader.GitHandoffReader._verify_origin"):
            self.assertEqual(cycle(controller, browser, reader, "demo", path), Action.HOLD)
            self.assertEqual(controller.checkpoint_branch, "main")
            self.assertEqual(controller.state.consumed_responses, [])
            self.publish_handoff(CHATS[0], "Next task", branch=branch)
            controller.resume_after_owner()
            self.assertEqual(cycle(controller, browser, reader, "demo", path, defer_dispatch=True),
                             Action.LAUNCH_SUCCESSOR)
        from succession.core import Controller
        restored = Controller.load(path)
        self.assertEqual(restored.config.branch, "main")
        self.assertEqual(restored.checkpoint_branch, branch)
        self.assertEqual(restored.unique_count, 1)
        self.assertIn(f"branch {branch}.", restored.state.pending.message)
        browser.send_once.assert_not_called()


class BootstrapTests(unittest.TestCase):
    def test_generic_request_reuses_the_same_private_configuration(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            request = folder / "request.json"
            request.write_text(json.dumps({
                "repo": "example-org/ordinary-project", "branch": "work/active",
                "project_name": "Ordinary Project",
            }))
            with (patch("launch_project.provision_reader", return_value="/tmp/repo") as git_setup,
                  patch("launch_project.resolve_project",
                        return_value=("g-p-abc123","Ordinary Project",
                                      "https://chatgpt.com/g/g-p-abc123/project")) as resolver,
                  patch("launch_project.launch", return_value={"event": "controller_started"}) as start):
                launch_request(request, folder)
                launch_request(request, folder)
            git_setup.assert_called_once()
            self.assertEqual(resolver.call_count, 2)
            self.assertEqual(start.call_args_list[0].args, start.call_args_list[1].args)
            self.assertEqual(start.call_args_list[0].kwargs, start.call_args_list[1].kwargs)

    def test_lost_initial_acknowledgement_reconciles_without_resending(self):
        with TemporaryDirectory() as temp:
            path = Path(temp) / "controller.json"
            cfg = {"project": PROJECT, "max_unique_chats": 4, "repo": STORY_REPO, "branch": "main"}
            reader, browser = Mock(), Mock()
            reader.heads.return_value = {"main": "seed"}
            browser.project = PROJECT
            browser.prepare.return_value = Destination(
                PROJECT, None, ComposerObservation(editable_text="", attachments_present=False), 10)
            browser._invoke.return_value = {}
            with self.assertRaisesRegex(RuntimeError, "Initial Send is held"):
                bootstrap(cfg, path, browser, reader)
            pointer = browser._invoke.call_args.kwargs["Message"]
            browser._invoke.return_value = {
                "posted_message_observed": True, "project": PROJECT,
                "chat_id": CHATS[0], "submitted_text": pointer,
            }
            result = bootstrap(cfg, path, browser, reader)
            self.assertEqual([call.args[0] for call in browser._invoke.call_args_list], ["Send", "Reconcile"])
            self.assertEqual(result["current_chat_id"], CHATS[0])
            self.assertEqual(result["unique_chat_count"], 1)

    def test_verified_initial_pause_does_not_require_reconciliation(self):
        with TemporaryDirectory() as temp:
            path = Path(temp) / "controller.json"
            cfg = {"project": PROJECT, "max_unique_chats": 4, "repo": STORY_REPO, "branch": "main"}
            reader, browser = Mock(), Mock()
            reader.heads.return_value = {"main": "seed"}
            browser.project = PROJECT
            browser.prepare.return_value = Destination(
                PROJECT, None, ComposerObservation(editable_text="", attachments_present=False), 10)
            browser._invoke.return_value = {"paused_before_click": True}
            with self.assertRaisesRegex(RuntimeError, "Owner paused before the initial Send"):
                bootstrap(cfg, path, browser, reader)
            self.assertFalse(path.with_name("bootstrap-intent.json").exists())
            pointer = browser._invoke.call_args.kwargs["Message"]
            path.with_suffix(".pause").touch()
            with self.assertRaisesRegex(RuntimeError, "Owner paused before the initial Send"):
                bootstrap(cfg, path, browser, reader)
            self.assertEqual(browser.prepare.call_count, 1)
            path.with_suffix(".pause").unlink()
            browser._invoke.return_value = {
                "posted_message_observed": True, "project": PROJECT,
                "chat_id": CHATS[0], "submitted_text": pointer,
            }
            result = bootstrap(cfg, path, browser, reader)
            self.assertEqual([call.args[0] for call in browser._invoke.call_args_list], ["Send", "Send"])
            self.assertEqual(result["current_chat_id"], CHATS[0])
