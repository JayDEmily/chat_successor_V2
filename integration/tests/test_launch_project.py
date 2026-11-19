from contextlib import redirect_stdout
from io import StringIO
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from launch_project import launch_request, main
from repo_reader import GitHandoffReader


PROJECT = "g-p-abc123"
PROJECT_URL = f"https://chatgpt.com/g/{PROJECT}/project"
REPO = "example-org/ordinary-project"
BRANCH = "work/active"
REF = f"refs/heads/{BRANCH}"
PUBLISHED_COMMIT = "a" * 40


class LauncherTests(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.installation = self.root / "Windows profile" / "ChatSuccession"
        self.request = self.root / "request.json"
        self.request.write_text(json.dumps({
            "repo": REPO, "branch": BRANCH, "project_name": "Ordinary Project",
            "project_url": PROJECT_URL,
        }), encoding="utf-8")
        self.empty_composer = {
            "project": PROJECT, "observed_url": PROJECT_URL, "current_chat_id": None,
            "private_window_handle": 10, "editable_text": "", "attachments_present": False,
        }

    def test_preflight_checks_the_exact_branch_without_touching_existing_run(self):
        run = self.installation / "Runs" / ("b" * 24)
        run.mkdir(parents=True)
        config = run / "config.json"
        config.write_text("historical config left as found", encoding="utf-8")
        before = set(self.installation.rglob("*"))
        with (patch("launch_project.wsl", return_value=f"{PUBLISHED_COMMIT}\t{REF}") as git,
              patch("launch_project.WindowsUIA") as browser,
              patch("launch_project.provision_reader") as provision,
              patch("launch_project.launch") as launch):
            browser.return_value._invoke.return_value = self.empty_composer
            result = launch_request(self.request, self.installation, check_only=True)
        self.assertEqual(result, {"event": "preflight_passed", "project": PROJECT, "repo": REPO,
                                  "branch": BRANCH, "published_commit": PUBLISHED_COMMIT})
        git.assert_called_once_with("/usr/bin/git", "ls-remote", "--exit-code", "--heads",
                                    f"https://github.com/{REPO}.git", REF)
        browser.return_value._invoke.assert_called_once_with(
            "Prepare", Kind="LAUNCH_SUCCESSOR", ProjectUrl=PROJECT_URL, Preflight=True)
        provision.assert_not_called()
        launch.assert_not_called()
        self.assertEqual(set(self.installation.rglob("*")), before)
        self.assertEqual(config.read_text(encoding="utf-8"), "historical config left as found")

    def test_preflight_rejects_a_different_or_ambiguous_published_ref(self):
        results = (f"{PUBLISHED_COMMIT}\trefs/heads/work/other",
                   f"{PUBLISHED_COMMIT}\t{REF}\n{PUBLISHED_COMMIT}\t{REF}")
        for result in results:
            with (self.subTest(result=result), patch("launch_project.wsl", return_value=result),
                  patch("launch_project.WindowsUIA") as browser):
                with self.assertRaisesRegex(RuntimeError, "exact published work branch"):
                    launch_request(self.request, self.installation, check_only=True)
                browser.assert_not_called()
        self.assertFalse(self.installation.exists())

    def test_preflight_requires_verified_project_and_empty_composer(self):
        invalid = (
            ("observed_url", "https://chatgpt.com/g/g-p-def456/project"),
            ("current_chat_id", "another-saved-chat"),
            ("editable_text", "existing draft"),
            ("attachments_present", True),
        )
        for field, value in invalid:
            with (self.subTest(field=field),
                  patch("launch_project.wsl", return_value=f"{PUBLISHED_COMMIT}\t{REF}"),
                  patch("launch_project.WindowsUIA") as browser):
                browser.return_value._invoke.return_value = {**self.empty_composer, field: value}
                with self.assertRaisesRegex(RuntimeError, "Chrome did not verify"):
                    launch_request(self.request, self.installation, check_only=True)
                browser.return_value._invoke.assert_called_once()
        self.assertFalse(self.installation.exists())

    def test_cli_passes_the_explicit_installation_or_preserves_legacy_default(self):
        connector_root = self.root / "Connector LocalAppData"
        arguments = ["launch_project.py", "--request", str(self.request), "--check"]
        for additional, expected in (
            (["--install-root", str(self.installation)], self.installation.resolve()),
            ([], connector_root / "ChatSuccession"),
        ):
            with (self.subTest(additional=additional),
                  patch.dict(os.environ, LOCALAPPDATA=str(connector_root)),
                  patch.object(sys, "argv", arguments + additional),
                  patch("launch_project.launch_request", return_value={}) as launch,
                  redirect_stdout(StringIO())):
                main()
                launch.assert_called_once_with(self.request, expected, check_only=True)

    def test_worker_instructions_keep_private_paths_relative_and_sendable(self):
        run_id, request_id = "b" * 24, "c" * 24
        instructions = GitHandoffReader(self.root, REPO, BRANCH).instructions(run_id, 1, request_id)
        self.assertIn("unique start-project.cmd", instructions)
        self.assertIn(f"Runs/{run_id}/controller.json", instructions)
        self.assertIn(f"Runs/{run_id}/owner-{request_id}.json.", instructions)
        self.assertRegex(instructions, r"^[A-Za-z0-9 .,/_:-]+$")
