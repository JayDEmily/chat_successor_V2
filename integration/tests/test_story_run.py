from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from launch_story import bootstrap
from repo_reader import GitStoryReader, PublishedStateError, STORY_REPO, STORY_TURNS
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


class BootstrapTests(unittest.TestCase):
    def test_lost_initial_acknowledgement_reconciles_without_resending(self):
        with TemporaryDirectory() as temp:
            path = Path(temp) / "controller.json"
            cfg = {"project": PROJECT, "max_unique_chats": 4}
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
