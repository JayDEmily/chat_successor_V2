"""Read *published* succession state from the nominated remote branch.

This adapter never treats the working tree, an unpushed commit or a worker's
claim as publication. It reads the fetched remote-tracking commit object.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
import subprocess
import sys

_KIT = Path(__file__).resolve().parents[1] / "astra/2026-11-17/unpacked/chat_succession_test_kit_20261117"
if str(_KIT) not in sys.path:
    sys.path.insert(0, str(_KIT))
from succession.core import RepoView

_SAFE_REF = re.compile(r"^(?![-./])(?!.*(?:\\.\\.|//|\\.lock(?:/|$)))[A-Za-z0-9_./-]+$")
_SAFE_PATH = re.compile(r"^(?![/\\\\])(?!.*(?:\\.\\.|//|\\\\))[A-Za-z0-9_./-]+$")


STORY_REPO = "JayDEmily/my-cat-and-dog"
STORY_TURNS = (
    ("codex/story-01-scruffy", "Scruffy"),
    ("codex/story-02-bluey", "Bluey"),
    ("codex/story-03-scruffy", "Scruffy"),
    ("codex/story-04-bluey", "Bluey"),
)
_SAVED_CHAT = re.compile(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}")
HANDOFF_WORKFLOW = "git-handoff"
_GITHUB_REPO = re.compile(r"[A-Za-z0-9-]+/[A-Za-z0-9_.-]+")


def validate_github_repo(repo: str):
    if (not isinstance(repo, str) or not _GITHUB_REPO.fullmatch(repo)
            or ".." in repo or repo.split("/")[1] in (".", "-", ".git")):
        raise ValueError("Use an exact GitHub owner/repository")


class PublishedStateError(RuntimeError):
    pass


@dataclass(frozen=True)
class PublishedObservation:
    view: RepoView
    commit: str
    run_id: str
    fixture_path: str
    completed_turns: int | None = None


class PublishedGit:
    def __init__(self, repo_dir: Path, repo_name: str, branch: str,
                 *, git_command: tuple[str, ...] = ("git",)):
        self.repo_dir = Path(repo_dir)
        self.repo_name = repo_name
        self.branch = branch
        self.git_command = git_command
        if (not _SAFE_REF.fullmatch(branch) or branch.endswith("/") or
                branch.startswith("refs/") or branch.endswith(".") or
                branch.endswith("-") or "@{" in branch):
            raise ValueError("Unsafe branch name")

    def _git(self, *args: str) -> str:
        try:
            result = subprocess.run(
                [*self.git_command, "-C", self.repo_dir.as_posix(), *args],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=45, check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise PublishedStateError(f"Git {args[0]} did not finish within {exc.timeout:g} seconds") from exc
        if result.returncode != 0:
            raise PublishedStateError(f"Git {args[0]} failed ({result.returncode}): {result.stderr.strip()[:400]}")
        return result.stdout.strip()

    def _verify_origin(self):
        # Verify that this local checkout really targets the nominated repository.
        remote_url = self._git("remote", "get-url", "origin")
        expected = (
            f"https://github.com/{self.repo_name}",
            f"ssh://git@github.com/{self.repo_name}",
            f"git@github.com:{self.repo_name}",
        )
        if remote_url.rstrip("/").removesuffix(".git").lower() not in {x.lower() for x in expected}:
            raise PublishedStateError("origin does not match nominated repository")

    def published_tip(self, *, shallow: bool = False) -> str:
        self._verify_origin()
        ref = f"refs/remotes/origin/{self.branch}"
        depth = ["--depth=1", "--filter=blob:none"] if shallow else []
        self._git("fetch", "--no-tags", *depth, "origin", f"+refs/heads/{self.branch}:{ref}")
        return self._git("rev-parse", "--verify", f"{ref}^{{commit}}")


class GitPublishedReader(PublishedGit):
    def __init__(self, repo_dir: Path, repo_name: str, branch: str,
                 fixture_path: str, *, git_command: tuple[str, ...] = ("git",)):
        super().__init__(repo_dir, repo_name, branch, git_command=git_command)
        self.fixture_path = fixture_path.rstrip("/")
        if (not _SAFE_PATH.fullmatch(self.fixture_path) or
                not self.fixture_path.startswith("succession-tests/")):
            raise ValueError("Fixture path must be a scoped succession-tests subdirectory")

    def read(self, expected_run_id: str) -> PublishedObservation:
        sha = self.published_tip()
        raw = self._git("show", f"{sha}:{self.fixture_path}/STATE.json")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise PublishedStateError("Published STATE.json is invalid JSON") from exc
        if type(data) is not dict or data.get("run_id") != expected_run_id:
            raise PublishedStateError("Published fixture run_id mismatch")
        if type(data.get("programme_complete")) is not bool:
            raise PublishedStateError("Published completion flag is not boolean")
        if data.get("programme_complete") and data.get("next_task"):
            raise PublishedStateError("Completed programme contradicts next task")
        if not data.get("programme_complete") and not isinstance(data.get("next_task"), str):
            raise PublishedStateError("Published next task is missing or invalid")
        last = data.get("last_chat_id")
        if not isinstance(last, str) or not last.strip():
            raise PublishedStateError("Published worker attribution missing")
        view = RepoView(repo=self.repo_name, branch=self.branch,
                        last_chat_id=last,
                        programme_complete=data["programme_complete"],
                        next_task=data.get("next_task"),
                        published=True, readable=True)
        return PublishedObservation(view, sha, expected_run_id, self.fixture_path)


class GitHandoffReader(PublishedGit):
    """Read routing metadata from the published tip without interpreting the workload."""

    def instructions(self, run_id: str, worker_number: int, owner_request_id: str | None = None) -> str:
        owner = (
            f" Read the scoped owner input for this turn through Remote Desktop Commander from "
            f"Runs/{run_id}/owner-{owner_request_id}.json. "
            "Apply that scope and record any required approval through the normal project process."
            if owner_request_id else ""
        )
        return (
            f" Chat Succession run {run_id}, worker {worker_number}. "
            "Read the published project rules and work record. "
            "Do the authorized discovery, planning, review or implementation. "
            "Reconcile published progress and respect explicit holds. "
            "Use Remote Desktop Commander to locate the Windows ChatSuccession folder containing the unique "
            "start-project.cmd. Check the connector LocalAppData and the native AppData/Local under the "
            "current Windows SID profile from Win32_UserProfile. "
            f"Read your current_chat_id from Runs/{run_id}/controller.json in that installation."
            + owner + " "
            "If there is a prior handoff for this run, read Chat-Succession-Next on the published tip. "
            "Wait until unique_chat_ids contains your expected worker count before using the ID. "
            "Before TASK_COMPLETE publish a final commit using the authorized project branch with trailers "
            f"Chat-Succession-Run: {run_id}, Chat-ID: your saved chat ID, and "
            "Chat-Succession-Next: the authorized next task or FINISHED. "
            "End a verified handoff with CHAT_STATUS: TASK_COMPLETE. When handing off on a different "
            "branch, put CHAT_HANDOFF_BRANCH: followed by its exact name on the preceding line. "
            "For more time in this chat use CHAT_STATUS: NEED_MORE_TIME. "
            "If the assignment is unclear, held, requires approval, or cannot be published "
            "under the project rules, report the blocker and end with CHAT_STATUS: ERROR. "
            "Put commentary and timestamps before the status. The status is the final plain line. "
            "The controller owns successor launches."
        )

    def read_checkpoint(self, expected_run_id: str, branch: str) -> PublishedObservation:
        if branch == self.branch:
            return self.read(expected_run_id)
        return GitHandoffReader(self.repo_dir, self.repo_name, branch,
                                git_command=self.git_command).read(expected_run_id)

    def read(self, expected_run_id: str) -> PublishedObservation:
        sha = self.published_tip(shallow=True)

        def trailer(key: str) -> str:
            lines = self._git("show", "-s", f"--format=%(trailers:key={key})", sha).splitlines()
            if len(lines) != 1:
                raise PublishedStateError(f"Published tip needs one {key} trailer")
            name, _, value = lines[0].partition(":")
            if name.casefold() != key.casefold() or not value.strip():
                raise PublishedStateError(f"Published tip needs a nonempty {key} trailer")
            return value.strip()

        if trailer("Chat-Succession-Run") != expected_run_id:
            raise PublishedStateError("Published handoff belongs to a different run")
        chat_id = trailer("Chat-ID")
        if not _SAVED_CHAT.fullmatch(chat_id):
            raise PublishedStateError("Published handoff needs a saved Chat-ID")
        next_task = trailer("Chat-Succession-Next")
        if next_task.upper() == "HOLD":
            raise PublishedStateError("Published handoff is on hold")
        done = next_task == "FINISHED"
        view = RepoView(repo=self.repo_name, branch=self.branch, last_chat_id=chat_id,
                        programme_complete=done, next_task=None if done else next_task,
                        published=True, readable=True)
        return PublishedObservation(view, sha, expected_run_id, "")


class GitStoryReader(PublishedGit):
    """Read one bounded story through its published branch chain."""

    def __init__(self, repo_dir: Path, *, git_command: tuple[str, ...] = ("git",)):
        super().__init__(repo_dir, STORY_REPO, "main", git_command=git_command)

    def heads(self) -> dict[str, str]:
        self._verify_origin()
        names = ["main", *(branch for branch, _ in STORY_TURNS)]
        refs = [f"refs/heads/{name}" for name in names]
        lines = self._git("ls-remote", "--refs", "origin", *refs).splitlines()
        heads = {}
        for line in lines:
            sha, ref = line.split("\t")
            heads[ref.removeprefix("refs/heads/")] = sha
        if "main" not in heads:
            raise PublishedStateError("Published story guide on main is missing")
        return heads

    def read(self, expected_run_id: str) -> PublishedObservation:
        heads = self.heads()
        turns = [(branch, speaker) for branch, speaker in STORY_TURNS if branch in heads]
        if not turns or tuple(turns) != STORY_TURNS[:len(turns)]:
            raise PublishedStateError("Published story branches must start at turn 1 without gaps")
        refs = {name: f"refs/remotes/origin/{name}" for name in heads}
        self._git("fetch", "--atomic", "--no-tags", "origin",
                  *(f"+refs/heads/{name}:{ref}" for name, ref in refs.items()))
        for name, ref in refs.items():
            if self._git("rev-parse", "--verify", f"{ref}^{{commit}}") != heads[name]:
                raise PublishedStateError(f"Published branch {name} changed during observation")

        parent = heads["main"]
        previous_lines = []
        chat_ids = []
        for branch, speaker in turns:
            commit = heads[branch]
            if self._git("rev-list", "--parents", "-n", "1", commit).split() != [commit, parent]:
                raise PublishedStateError(f"{branch} must add one commit to the previous turn")
            if self._git("diff-tree", "--no-commit-id", "--name-only", "-r", commit) != "STORY.md":
                raise PublishedStateError(f"{branch} must change only STORY.md")
            lines = self._git("show", f"{commit}:STORY.md").splitlines()
            prefix = f"{speaker}: "
            if (len(lines) != len(previous_lines) + 1 or lines[:-1] != previous_lines
                    or not lines[-1].startswith(prefix) or not lines[-1][len(prefix):].strip()):
                raise PublishedStateError(f"{branch} must append one line spoken by {speaker}")
            chat_id = self._git("show", "-s", "--format=%(trailers:key=Chat-ID,valueonly)", commit)
            if not _SAVED_CHAT.fullmatch(chat_id) or chat_id in chat_ids:
                raise PublishedStateError(f"{branch} needs one distinct saved Chat-ID trailer")
            chat_ids.append(chat_id)
            parent, previous_lines = commit, lines

        count = len(turns)
        done = count == len(STORY_TURNS)
        view = RepoView(repo=self.repo_name, branch=self.branch, last_chat_id=chat_ids[-1],
                        programme_complete=done, next_task=None if done else STORY_TURNS[count][0],
                        published=True, readable=True)
        return PublishedObservation(view, parent, expected_run_id, "STORY.md", completed_turns=count)
