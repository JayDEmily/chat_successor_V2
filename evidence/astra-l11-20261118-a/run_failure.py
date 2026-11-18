#!/usr/bin/env python3
"""L11 scoped publication-failure injection and unpushed-commit readback.

No ChatGPT browser, live controller, account permissions, remote branch changes,
or successor Send. A disposable detached Git worktree is removed afterwards.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

here = Path(__file__).resolve().parent
repo = here.parents[1]
sys.path.insert(0, str(repo / "integration"))
from runner import cycle, initialise
from repo_reader import GitPublishedReader, PublishedStateError
from succession.core import Action, Config, Controller, Response, RepoView

REPO_NAME = "JayDEmily/chat_successor"
BRANCH = "work/astra-succession-implementation-20261118"
L09_FIXTURE = "succession-tests/astra-l09-20261118-a"
L09_RUN = "astra-l09-20261118-a"
L09_CHAT = "6afd3221-f970-83ec-9889-1d09b1762a5f"

def git(directory: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(directory), *args],
                            text=True, capture_output=True, timeout=45)
    if result.returncode:
        raise RuntimeError(f"git {args[0]} failed: {result.stderr[:350]}")
    return result.stdout.strip()

class Browser:
    def __init__(self, response: Response):
        self.response = response
        self.calls: list[str] = []
    def observe(self, chat_id: str):
        assert chat_id == self.response.chat_id
        self.calls.append("observe")
        return self.response
    def prepare(self, *args):
        self.calls.append("prepare")
        raise AssertionError("L11 non-sending test cannot prepare")
    def send_once(self, *args):
        self.calls.append("send")
        raise AssertionError("L11 non-sending test cannot Send")

class InjectedOutage:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.fail = True
        self.calls = 0
    def read(self, run_id: str):
        self.calls += 1
        if self.fail:
            raise PublishedStateError("L11 one-shot injected GitHub fetch outage")
        class Observed: pass
        observed = Observed()
        observed.view = RepoView(self.cfg.repo, self.cfg.branch,
                                 "l11-test-first", False,
                                 "Known published next slice",
                                 published=True, readable=True)
        return observed

def publication_failure_then_repair() -> dict:
    cfg = Config("g-p-L11-INJECT", REPO_NAME, BRANCH, 3)
    response = Response("l11-test-first", "l11-turn1",
                        "Published results.\nCHAT_STATUS: TASK_COMPLETE",
                        role="assistant", project=cfg.project)
    browser = Browser(response)
    reader = InjectedOutage(cfg)
    with tempfile.TemporaryDirectory(prefix="astra-l11-tool-outage-") as folder:
        path = Path(folder) / "state.json"
        c = initialise(path, cfg, response.chat_id)
        action = cycle(c, browser, reader, "astra-l11-failure-a", path)
        assert action == Action.HOLD
        assert reader.calls == 1
        assert browser.calls == ["observe"]
        assert c.state.pending is None
        assert c.state.consumed_responses == []
        assert c.unique_count == 1
        assert "Published Git state unavailable" in c.state.halted
        restarted = Controller.load(path)
        held = cycle(restarted, browser, reader, "astra-l11-failure-a", path)
        assert held == Action.HOLD and browser.calls == ["observe"]
        assert reader.calls == 1
        reader.fail = False
        restarted.resume_after_owner()
        restarted.save(path)
        repaired = cycle(restarted, browser, reader, "astra-l11-failure-a",
                         path, defer_dispatch=True)
        assert repaired == Action.LAUNCH_SUCCESSOR
        assert restarted.state.pending is not None
        assert restarted.state.pending.phase == "prepared"
        assert restarted.unique_count == 1
        assert browser.calls == ["observe", "observe"]
        assert "send" not in browser.calls and "prepare" not in browser.calls
        assert reader.calls == 2
        return {
            "scenario": "ONE_SHOT_TEST_ADAPTER_PUBLICATION_OUTAGE",
            "outage_injected": True,
            "first_action": action.value,
            "persisted_hold_survived_restart": True,
            "response_consumed_during_outage": False,
            "pending_during_outage": None,
            "unique_chat_count_during_outage": 1,
            "repair": "Owner resume with simulated restored published repository read",
            "after_repair_action": repaired.value,
            "pending_after_repair": restarted.state.pending.phase,
            "browser_send_calls": 0,
            "browser_prepare_calls": 0,
            "real_successor_launched": False,
            "source": "SYNTHETIC_ADAPTER_FAULT_INJECTION",
            "result": "PASS",
        }

def local_only_commit_not_remote(expected_head: str) -> dict:
    actual_head = git(repo, "ls-remote", "origin", f"refs/heads/{BRANCH}").split()[0]
    if actual_head != expected_head:
        raise RuntimeError(f"Remote branch changed unexpectedly: {actual_head}")
    cfg = Config("g-p-L11-GIT-TEST", REPO_NAME, BRANCH, 3)
    with tempfile.TemporaryDirectory(prefix="astra-l11-unpushed-") as folder:
        root = Path(folder)
        checkout = root / "worktree"
        try:
            git(repo, "worktree", "add", "--detach", str(checkout), expected_head)
            path = checkout / L09_FIXTURE / "STATE.json"
            original = json.loads(path.read_text(encoding="utf-8"))
            assert original["run_id"] == L09_RUN
            assert original["programme_complete"] is True
            assert original["next_task"] is None
            assert original["last_chat_id"] == L09_CHAT
            local = dict(original)
            local["programme_complete"] = False
            local["next_task"] = "LOCAL ONLY - intentionally never pushed"
            path.write_text(json.dumps(local, indent=2) + "\n", encoding="utf-8")
            git(checkout, "add", str(path.relative_to(checkout)))
            git(checkout, "-c", "user.name=Astra-L11-Disposable",
                "-c", "user.email=astra-l11@example.invalid",
                "commit", "-m", "L11 disposable local-only fixture edit")
            local_sha = git(checkout, "rev-parse", "HEAD")
            assert local_sha != expected_head
            remote = GitPublishedReader(checkout, REPO_NAME, BRANCH, L09_FIXTURE)
            actual = remote.read(L09_RUN)
            assert actual.commit == expected_head
            assert actual.view.programme_complete is True
            assert actual.view.next_task is None
            assert actual.view.last_chat_id == L09_CHAT
            assert json.loads(path.read_text())["programme_complete"] is False
            response = Response(L09_CHAT, "l11-test-terminal",
                                "CHAT_STATUS: TASK_COMPLETE",
                                role="assistant", project=cfg.project)
            browser = Browser(response)
            with tempfile.TemporaryDirectory(prefix="astra-l11-ref-") as state_folder:
                state = Path(state_folder) / "controller.json"
                c = initialise(state, cfg, L09_CHAT)
                action = cycle(c, browser, remote, L09_RUN, state)
                assert action == Action.STOP_FINISHED
                assert c.unique_count == 1
                assert "send" not in browser.calls and "prepare" not in browser.calls
            return {
                "scenario": "REAL_LOCAL_GIT_COMMIT_UNPUSHED_VS_REMOTE_PUBLISHED_STATE",
                "source": "DISPOSABLE_LOCAL_GIT_WORKTREE_PLUS_REAL_GIT_FETCH",
                "local_only_commit_sha": local_sha,
                "published_remote_commit_sha": actual.commit,
                "local_state_programme_complete": False,
                "published_state_programme_complete": True,
                "reader_used_published_state": True,
                "controller_action": action.value,
                "browser_send_calls": 0,
                "browser_prepare_calls": 0,
                "real_successor_launched": False,
                "local_commit_pushed": False,
                "result": "PASS",
            }
        finally:
            if checkout.exists():
                git(repo, "worktree", "remove", "--force", str(checkout))

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    args = parser.parse_args()
    first = publication_failure_then_repair()
    second = local_only_commit_not_remote(args.expected_head)
    result = {
        "test_id": "L11",
        "run_id": "astra-l11-20261118-a",
        "scenario_type": "MIXED_TEST_ADAPTER_FAILURE_AND_DISPOSABLE_LOCAL_GIT",
        "real_chatgpt_sends": 0,
        "real_successors": 0,
        "real_GitHub_permission_changes": 0,
        "published_repository_modified_by_test": False,
        "scenarios": [first, second],
        "scenarios_passed": 2,
        "outcome": "PASS_TEST_ONLY",
    }
    out = here / "observations.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"scenarios_passed": 2, "browser_send_calls": 0,
                      "pinned_remote_sha": second["published_remote_commit_sha"],
                      "local_only_sha": second["local_only_commit_sha"],
                      "worktree_removed": True}, indent=2))

if __name__ == "__main__":
    main()
