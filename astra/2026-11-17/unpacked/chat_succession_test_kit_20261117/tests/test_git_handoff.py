"""REAL local Git, FAKE workers. The only allowed Git transport is local file.

Temporary repos are created sequentially and cleaned after every test.
These tests are not GitHub, credential, permission, browser or ChatGPT tests.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from succession.core import Action, Config, Controller, RepoView, Response
from succession.mock import FakeBrowser
from tools.repo_fixture import init_fixture, simulate_slice, verify_fixture, rotate_probe, read_json

BRANCH = "test/succession"
REPO = "JayDEmily/chat_successor"
GIT_OPERATIONS = []


@unittest.skipUnless(shutil.which("git"), "Git required for the local repository transport tests")
class LocalGitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="succession-local-git-")
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.remote = self.base / "remote.git"
        self.worker = self.base / "worker1"
        self.env = os.environ.copy()
        # Do not use user account credentials/config; prohibit all network protocols.
        self.env.update({
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull, "GIT_TERMINAL_PROMPT": "0",
            "GIT_ALLOW_PROTOCOL": "file",
        })
        for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_CONFIG_COUNT",
                    "GIT_CONFIG_PARAMETERS"):
            self.env.pop(key, None)
        self.git(self.base, "init", "--bare", "--template=", str(self.remote))
        self.git(self.base, "init", "--template=", "-b", BRANCH, str(self.worker))
        init_fixture(self.worker / "fixture", steps=3, run_id="local-git-test")
        self.commit(self.worker, "Seed bounded test workload")
        self.git(self.worker, "remote", "add", "origin", str(self.remote))
        self.git(self.worker, "push", "-u", "origin", BRANCH)
        self.git(self.base, "--git-dir", str(self.remote), "symbolic-ref", "HEAD", f"refs/heads/{BRANCH}")

    def git(self, cwd, *args, check=True):
        cp = subprocess.run(
            ["git", "-c", "core.hooksPath=" + os.devnull,
             "-c", "user.name=Offline Test", "-c", "user.email=offline@example.invalid",
             "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false",
             "-C", str(cwd), *args],
            text=True, capture_output=True, env=self.env, timeout=30,
        )
        norm = lambda text: text.replace(str(self.base), "<TEMP>")
        GIT_OPERATIONS.append({
            "test": self._testMethodName, "mode": "REAL_LOCAL_GIT_ONLY",
            "cwd": norm(str(cwd)), "args": [norm(str(arg)) for arg in args],
            "returncode": cp.returncode, "stdout": norm(cp.stdout), "stderr": norm(cp.stderr),
        })
        if check and cp.returncode:
            raise AssertionError(f"Local git {args} failed:\n{cp.stdout}\n{cp.stderr}")
        return cp

    def commit(self, worker, message):
        self.git(worker, "add", "fixture")
        return self.git(worker, "commit", "-m", message)

    def clone(self, name):
        target = self.base / name
        self.git(self.base, "clone", "--template=", "--branch", BRANCH,
                 str(self.remote), str(target))
        return target

    def remote_state(self):
        cp = self.git(self.base, "--git-dir", str(self.remote),
                      "show", f"refs/heads/{BRANCH}:fixture/STATE.json")
        return json.loads(cp.stdout)

    def view(self, state, published=True):
        return RepoView(REPO, BRANCH, state["last_chat_id"],
                        state["programme_complete"], state["next_task"],
                        published=published)

    def controller(self):
        return Controller(Config("project-nominated", REPO, BRANCH, 30), "c1")

    def response(self, c, rid="r1"):
        return Response(c.state.current_chat_id, rid, "Published work.\nCHAT_STATUS: TASK_COMPLETE",
                        project=c.config.project)

    def test_G01_push_then_fresh_worker_reads_durable_handoff(self):
        result = simulate_slice(self.worker / "fixture", "c1")
        self.commit(self.worker, "Publish first slice")
        self.git(self.worker, "push", "origin", BRANCH)
        fresh = self.clone("worker2")
        self.assertEqual(verify_fixture(fresh / "fixture")["completed_steps"], 1)
        self.assertEqual(read_json(fresh / "fixture", "RESULTS.json")[0], result)
        c = self.controller()
        d = c.consume(self.response(c), self.view(self.remote_state()))
        self.assertEqual(d.action, Action.LAUNCH_SUCCESSOR)
        self.assertNotIn(result["probe_nonce"], d.message)

    def test_G02_local_commit_without_push_is_not_a_handover(self):
        simulate_slice(self.worker / "fixture", "c1")
        self.commit(self.worker, "Local only")
        self.assertEqual(self.remote_state()["completed_steps"], 0)
        c = self.controller()
        view = self.view(read_json(self.worker / "fixture", "STATE.json"), published=False)
        self.assertEqual(c.consume(self.response(c), view).action, Action.HOLD)

    def test_G03_wrong_branch_publication_does_not_update_nominated_branch(self):
        self.git(self.worker, "switch", "-c", "test/other-branch")
        simulate_slice(self.worker / "fixture", "c1")
        self.commit(self.worker, "Wrong-branch fixture update")
        self.git(self.worker, "push", "origin", "test/other-branch")
        self.assertEqual(self.remote_state()["completed_steps"], 0)
        c = self.controller()
        self.assertEqual(c.consume(self.response(c), self.view(self.remote_state())).action, Action.HOLD)

    def test_G04_rejected_push_is_not_completion(self):
        competing = self.clone("competing")
        rotate_probe(competing / "fixture")
        self.commit(competing, "Other writer changed the next repository-only probe")
        self.git(competing, "push", "origin", BRANCH)
        simulate_slice(self.worker / "fixture", "c1")
        self.commit(self.worker, "Now-stale local worker")
        cp = self.git(self.worker, "push", "origin", BRANCH, check=False)
        self.assertNotEqual(cp.returncode, 0)
        self.assertEqual(self.remote_state()["completed_steps"], 0)
        c = self.controller()
        view = self.view(read_json(self.worker / "fixture", "STATE.json"), published=False)
        self.assertEqual(c.consume(self.response(c), view).action, Action.HOLD)

    def test_G05_repo_only_fresh_probe_observed_after_previous_worker_ends(self):
        simulate_slice(self.worker / "fixture", "c1")
        self.commit(self.worker, "First handover")
        self.git(self.worker, "push", "origin", BRANCH)
        # This local 'owner' change occurs after c1's work and is not in any prompt.
        rotate_probe(self.worker / "fixture")
        probe = read_json(self.worker / "fixture", "RUN.json")["steps"][1]["probe_nonce"]
        self.commit(self.worker, "Owner adds next probe")
        self.git(self.worker, "push", "origin", BRANCH)
        fresh = self.clone("worker2")
        result = simulate_slice(fresh / "fixture", "c2")
        self.assertEqual(result["probe_nonce"], probe)
        self.commit(fresh, "Second handover from fresh workspace")
        self.git(fresh, "push", "origin", BRANCH)
        self.assertEqual(self.remote_state()["completed_steps"], 2)

    def test_G06_three_mock_workers_continue_using_only_repository(self):
        c = self.controller()
        b = FakeBrowser(c.config.project)
        worker = self.worker
        for n in range(1, 4):
            if n > 1:
                worker = self.clone(f"worker{n}")
            simulate_slice(worker / "fixture", c.state.current_chat_id)
            self.commit(worker, f"Mock worker slice {n}")
            self.git(worker, "push", "origin", BRANCH)
            d = c.consume(self.response(c, f"r{n}"), self.view(self.remote_state()))
            if n < 3:
                self.assertEqual(d.action, Action.LAUNCH_SUCCESSOR)
                b.perform(c)
            else:
                self.assertEqual(d.action, Action.STOP_FINISHED)
        self.assertEqual((c.unique_count, b.opens), (3, 2))

    def test_G07_remote_unavailable_does_not_trigger_next_chat(self):
        cp = self.git(self.worker, "fetch", str(self.base / "not-a-repo"), check=False)
        self.assertNotEqual(cp.returncode, 0)
        c = self.controller()
        self.assertEqual(c.consume(self.response(c), None).action, Action.HOLD)
        self.assertIsNone(c.state.pending)

    def test_G08_corrupt_published_fixture_is_not_useful_progress(self):
        simulate_slice(self.worker / "fixture", "c1")
        path = self.worker / "fixture" / "RESULTS.json"
        data = json.loads(path.read_text())
        data[0]["summary"]["alpha"]["total"] += 100
        path.write_text(json.dumps(data))
        self.commit(self.worker, "Deliberately incorrect test-only work")
        self.git(self.worker, "push", "origin", BRANCH)
        fresh = self.clone("worker2")
        with self.assertRaises(ValueError):
            verify_fixture(fresh / "fixture")
