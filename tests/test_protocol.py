"""Offline, side-effect-free Git packet validation tests (Task 1).

All Git mutations happen inside disposable temporary repositories. No chats are launched.
"""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.validate_packet import validate_packet


class PacketTests(unittest.TestCase):
    def git(self, *args):
        done = subprocess.run(
            ["git", *args], cwd=self.root, text=True, capture_output=True, check=False
        )
        if done.returncode:
            self.fail(f"git {args!r} failed: {done.stderr}")
        return done.stdout.strip()

    def write_json(self, path, payload):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-m", message)
        return self.git("rev-parse", "HEAD")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Packet Test")
        self.git("config", "user.email", "packet-test@example.invalid")
        self.run_id = "probe-001"
        self.base = "runs/probe-001"
        self.branch = "trial/probe-001"
        self.assign1 = {
            "schema_version": 1, "run_id": self.run_id, "step": 1,
            "role": "worker", "task_id": "toy-calculate",
            "predecessor_result_commit": None, "terminal": False,
            "allowed_paths": [f"{self.base}/steps/001/toy.json",
                              f"{self.base}/steps/001/result.json"],
            "required_output_paths": [f"{self.base}/steps/001/toy.json",
                                      f"{self.base}/steps/001/result.json"]
        }
        self.write_json(f"{self.base}/run.json", {
            "schema_version": 1, "run_id": self.run_id, "branch": self.branch,
            "max_steps": 3, "launch_mode": "worker", "project_config_ref": "local:project",
            "stop_state": "active"
        })
        self.write_json(f"{self.base}/steps/001/assignment.json", self.assign1)
        self.a1 = self.commit("create first assignment")
        self.git("switch", "-c", self.branch)
        self.write_json(f"{self.base}/steps/001/toy.json",
                        {"expression": "17 * 23 + 19", "value": 410})
        self.result1 = {
            "schema_version": 1, "run_id": self.run_id, "step": 1,
            "assignment_commit": self.a1, "status": "completed",
            "changed_paths": self.assign1["allowed_paths"],
            "checks": ["recomputed 17 * 23 + 19 = 410"], "unresolved_issues": []
        }
        self.write_json(f"{self.base}/steps/001/result.json", self.result1)
        self.r1 = self.commit("publish toy result")
        self.assign2 = {
            "schema_version": 1, "run_id": self.run_id, "step": 2,
            "role": "reviewer", "task_id": "toy-independent-review",
            "predecessor_result_commit": self.r1, "terminal": False,
            "allowed_paths": [f"{self.base}/steps/002/review.json",
                              f"{self.base}/steps/002/result.json"],
            "required_output_paths": [f"{self.base}/steps/002/review.json",
                                      f"{self.base}/steps/002/result.json"]
        }
        self.h1 = {
            "schema_version": 1, "run_id": self.run_id, "step": 1,
            "result_commit": self.r1, "next_step": 2,
            "next_assignment_path": f"{self.base}/steps/002/assignment.json",
            "terminal": False
        }
        self.write_json(f"{self.base}/steps/001/handover.json", self.h1)
        self.write_json(f"{self.base}/steps/002/assignment.json", self.assign2)
        self.a2 = self.commit("publish second assignment and handover")
        self.write_json(f"{self.base}/steps/002/review.json",
                        {"verdict": "ACCEPT", "recomputed_value": 410})
        self.result2 = {
            "schema_version": 1, "run_id": self.run_id, "step": 2,
            "assignment_commit": self.a2, "status": "completed",
            "changed_paths": self.assign2["allowed_paths"],
            "checks": ["independently checked arithmetic"], "unresolved_issues": []
        }
        self.write_json(f"{self.base}/steps/002/result.json", self.result2)
        self.r2 = self.commit("publish independent review")
        self.assign3 = {
            "schema_version": 1, "run_id": self.run_id, "step": 3,
            "role": "auditor", "task_id": "toy-terminal-audit",
            "predecessor_result_commit": self.r2, "terminal": True,
            "allowed_paths": [f"{self.base}/steps/003/summary.json",
                              f"{self.base}/steps/003/result.json"],
            "required_output_paths": [f"{self.base}/steps/003/summary.json",
                                      f"{self.base}/steps/003/result.json"]
        }
        self.h2 = {
            "schema_version": 1, "run_id": self.run_id, "step": 2,
            "result_commit": self.r2, "next_step": 3,
            "next_assignment_path": f"{self.base}/steps/003/assignment.json",
            "terminal": False
        }
        self.write_json(f"{self.base}/steps/002/handover.json", self.h2)
        self.write_json(f"{self.base}/steps/003/assignment.json", self.assign3)
        self.a3 = self.commit("publish terminal assignment and handover")

    def validate(self, step, sha):
        return validate_packet(self.root, self.run_id, step, sha)

    def change_assignment3(self, assignment_updates=None, handover_updates=None):
        self.git("reset", "--hard", self.r2)
        assignment = {**self.assign3, **(assignment_updates or {})}
        handover = {**self.h2, **(handover_updates or {})}
        self.write_json(f"{self.base}/steps/002/handover.json", handover)
        self.write_json(f"{self.base}/steps/003/assignment.json", assignment)
        return self.commit("test tampered third assignment")

    def change_result1(self, status="completed", declared_extra=False, actual_extra=False):
        self.git("reset", "--hard", self.a1)
        self.write_json(f"{self.base}/steps/001/toy.json",
                        {"expression": "17 * 23 + 19", "value": 410})
        result = {**self.result1, "status": status}
        if declared_extra:
            result["changed_paths"] = result["changed_paths"] + ["README.md"]
        self.write_json(f"{self.base}/steps/001/result.json", result)
        if actual_extra:
            (self.root / "UNAUTHORISED.txt").write_text("out of scope\n")
        bad_r1 = self.commit("test modified first result")
        assign2 = {**self.assign2, "predecessor_result_commit": bad_r1}
        handover = {**self.h1, "result_commit": bad_r1}
        self.write_json(f"{self.base}/steps/001/handover.json", handover)
        self.write_json(f"{self.base}/steps/002/assignment.json", assign2)
        return self.commit("test modified second assignment")

    def test_valid_first_step(self):
        self.git("reset", "--hard", self.a1)
        self.assertTrue(self.validate(1, self.a1).ok)

    def test_valid_second_step(self):
        self.git("reset", "--hard", self.a2)
        self.assertTrue(self.validate(2, self.a2).ok)

    def test_valid_terminal_step(self):
        self.assertTrue(self.validate(3, self.a3).ok)

    def test_wrong_run(self):
        sha = self.change_assignment3({"run_id": "wrong"})
        self.assertFalse(self.validate(3, sha).ok)

    def test_wrong_step(self):
        sha = self.change_assignment3({"step": 2})
        self.assertFalse(self.validate(3, sha).ok)

    def test_wrong_role(self):
        sha = self.change_assignment3({"role": "worker"})
        self.assertFalse(self.validate(3, sha).ok)

    def test_missing_predecessor(self):
        sha = self.change_assignment3({"predecessor_result_commit": None})
        self.assertFalse(self.validate(3, sha).ok)

    def test_blocked_predecessor(self):
        sha = self.change_result1(status="blocked")
        self.assertFalse(self.validate(2, sha).ok)

    def test_failed_predecessor(self):
        sha = self.change_result1(status="failed")
        self.assertFalse(self.validate(2, sha).ok)

    def test_declared_out_of_scope(self):
        sha = self.change_result1(declared_extra=True)
        self.assertFalse(self.validate(2, sha).ok)

    def test_actual_out_of_scope(self):
        sha = self.change_result1(actual_extra=True)
        self.assertFalse(self.validate(2, sha).ok)

    def test_stale_handover_result_commit(self):
        sha = self.change_assignment3(handover_updates={"result_commit": self.r1})
        self.assertFalse(self.validate(3, sha).ok)

    def test_conflicting_local_run_branch(self):
        self.git("commit", "--allow-empty", "-m", "simulate conflicting head")
        self.assertFalse(self.validate(3, self.a3).ok)

    def test_prepared_run_cannot_launch_second_chat(self):
        self.git("reset", "--hard", self.a1)
        self.write_json(f"{self.base}/run.json", {
            "schema_version": 1, "run_id": self.run_id, "branch": self.branch,
            "max_steps": 3, "launch_mode": "worker",
            "project_config_ref": "local:project", "stop_state": "prepared"
        })
        changed_a1 = self.commit("test set prepared run")
        self.write_json(f"{self.base}/steps/001/toy.json",
                        {"expression": "17 * 23 + 19", "value": 410})
        self.write_json(f"{self.base}/steps/001/result.json",
                        {**self.result1, "assignment_commit": changed_a1})
        new_r1 = self.commit("test prepared predecessor result")
        self.write_json(f"{self.base}/steps/001/handover.json",
                        {**self.h1, "result_commit": new_r1})
        self.write_json(f"{self.base}/steps/002/assignment.json",
                        {**self.assign2, "predecessor_result_commit": new_r1})
        new_a2 = self.commit("test prepared successor packet")
        self.assertFalse(self.validate(2, new_a2).ok)

    def test_next_assignment_commit_cannot_smuggle_other_files(self):
        self.git("reset", "--hard", self.r2)
        self.write_json(f"{self.base}/steps/002/handover.json", self.h2)
        self.write_json(f"{self.base}/steps/003/assignment.json", self.assign3)
        (self.root / "UNAUTHORISED.txt").write_text("unexpected file\n")
        bad_sha = self.commit("test out of scope handover commit")
        self.assertFalse(self.validate(3, bad_sha).ok)

    def test_validator_cli_readback(self):
        import sys
        source = Path(__file__).resolve().parents[1] / "tools" / "validate_packet.py"
        process = subprocess.run(
            [sys.executable, str(source), "--repo-dir", str(self.root),
             "--run-id", self.run_id, "--step", "3", "--assignment-sha", self.a3],
            capture_output=True, text=True,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertTrue(json.loads(process.stdout)["ok"])

    def test_no_fourth_step(self):
        self.assertFalse(self.validate(4, self.a3).ok)

    def test_predecessor_cannot_expand_allowed_paths(self):
        self.git("reset", "--hard", self.a1)
        expanded = {**self.assign1,
                    "allowed_paths": self.assign1["allowed_paths"] + ["UNAUTHORISED.txt"]}
        self.write_json(f"{self.base}/steps/001/assignment.json", expanded)
        modified_a1 = self.commit("test broadened assignment")
        self.write_json(f"{self.base}/steps/001/toy.json",
                        {"expression": "17 * 23 + 19", "value": 410})
        (self.root / "UNAUTHORISED.txt").write_text("not assigned by contract\n")
        result = {**self.result1, "assignment_commit": modified_a1,
                  "changed_paths": expanded["allowed_paths"]}
        self.write_json(f"{self.base}/steps/001/result.json", result)
        bad_r1 = self.commit("test widened result")
        self.write_json(f"{self.base}/steps/001/handover.json",
                        {**self.h1, "result_commit": bad_r1})
        self.write_json(f"{self.base}/steps/002/assignment.json",
                        {**self.assign2, "predecessor_result_commit": bad_r1})
        bad_a2 = self.commit("test widened handover")
        self.assertFalse(self.validate(2, bad_a2).ok)

    def test_returned_review_blocks_auditor(self):
        self.git("reset", "--hard", self.a2)
        self.write_json(f"{self.base}/steps/002/review.json",
                        {"verdict": "RETURN", "recomputed_value": 409})
        self.write_json(f"{self.base}/steps/002/result.json", self.result2)
        bad_r2 = self.commit("test reviewer return")
        assign3 = {**self.assign3, "predecessor_result_commit": bad_r2}
        handover2 = {**self.h2, "result_commit": bad_r2}
        self.write_json(f"{self.base}/steps/002/handover.json", handover2)
        self.write_json(f"{self.base}/steps/003/assignment.json", assign3)
        sha = self.commit("test third assignment after return")
        self.assertFalse(self.validate(3, sha).ok)


if __name__ == "__main__":
    unittest.main()
