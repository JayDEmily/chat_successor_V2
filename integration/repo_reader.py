"""Read *published* succession fixture state from the nominated remote branch.

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


class PublishedStateError(RuntimeError):
    pass


@dataclass(frozen=True)
class PublishedObservation:
    view: RepoView
    commit: str
    run_id: str
    fixture_path: str


class GitPublishedReader:
    def __init__(self, repo_dir: Path, repo_name: str, branch: str,
                 fixture_path: str, *, git_command: tuple[str, ...] = ("git",)):
        self.repo_dir = Path(repo_dir)
        self.repo_name = repo_name
        self.branch = branch
        self.fixture_path = fixture_path.rstrip("/")
        self.git_command = git_command
        if (not _SAFE_REF.fullmatch(branch) or branch.endswith("/") or
                branch.startswith("refs/") or branch.endswith(".") or
                branch.endswith("-") or "@{" in branch):
            raise ValueError("Unsafe branch name")
        if (not _SAFE_PATH.fullmatch(self.fixture_path) or
                not self.fixture_path.startswith("succession-tests/")):
            raise ValueError("Fixture path must be a scoped succession-tests subdirectory")

    def _git(self, *args: str) -> str:
        result = subprocess.run(
            [*self.git_command, "-C", str(self.repo_dir), *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=45, check=False,
        )
        if result.returncode != 0:
            raise PublishedStateError(f"Git {args[0]} failed ({result.returncode}): {result.stderr.strip()[:400]}")
        return result.stdout.strip()

    def read(self, expected_run_id: str) -> PublishedObservation:
        # Verify that this local checkout really targets the nominated repository.
        remote_url = self._git("remote", "get-url", "origin")
        valid_https = f"github.com/{self.repo_name}.git"
        valid_ssh = f"github.com:{self.repo_name}.git"
        if not (remote_url.rstrip("/").endswith(valid_https) or
                remote_url.rstrip("/").endswith(valid_https[:-4]) or
                remote_url.rstrip("/").endswith(valid_ssh)):
            raise PublishedStateError("origin does not match nominated repository")
        ref = f"refs/remotes/origin/{self.branch}"
        self._git("fetch", "--no-tags", "origin",
                  f"+refs/heads/{self.branch}:{ref}")
        sha = self._git("rev-parse", "--verify", f"{ref}^{{commit}}")
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
