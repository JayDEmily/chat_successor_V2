import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest

from tools.repo_fixture import (
    init_fixture, simulate_slice, verify_fixture, rotate_probe, expected_summary, read_json, put_json,
)


class FixtureTests(unittest.TestCase):
    def test_F01_independent_expected_aggregation(self):
        rows = [{"category": " A ", "value": 2}, {"category": "a", "value": -3},
                {"category": "B", "value": 7}]
        self.assertEqual(expected_summary(rows), {
            "a": {"count": 2, "total": -1}, "b": {"count": 1, "total": 7},
        })

    def test_F02_four_slices_programme_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_fixture(root)
            for n in range(1, 5):
                simulate_slice(root, f"c{n}")
                self.assertEqual(verify_fixture(root)["completed_steps"], n)
            state = read_json(root, "STATE.json")
            self.assertIs(state["programme_complete"], True)
            self.assertIsNone(state["next_task"])
            # A fresh worker can validate using only the files stored in its repo.
            cp = subprocess.run([sys.executable, "-B", str(root / "fixture_tools.py"),
                                 "verify", "--root", str(root)],
                                text=True, capture_output=True, timeout=30)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            with self.assertRaises(ValueError):
                simulate_slice(root, "c5")

    def test_F03_fresh_probe_not_disclosed_to_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_fixture(root)
            old = read_json(root, "RUN.json")["steps"][0]["probe_nonce"]
            receipt = rotate_probe(root)
            new = read_json(root, "RUN.json")["steps"][0]["probe_nonce"]
            self.assertNotEqual(old, new)
            self.assertFalse(receipt["nonce_disclosed"])
            result = simulate_slice(root, "c1")
            self.assertEqual(result["probe_nonce"], new)

    def test_F04_stale_nonce_fails_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_fixture(root)
            simulate_slice(root, "c1")
            results = read_json(root, "RESULTS.json")
            results[0]["probe_nonce"] = "stale"
            put_json(root, "RESULTS.json", results)
            with self.assertRaisesRegex(ValueError, "stale"):
                verify_fixture(root)

    def test_F05_duplicate_slice_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_fixture(root)
            simulate_slice(root, "c1")
            simulate_slice(root, "c2")
            results = read_json(root, "RESULTS.json")
            results[1]["step"] = 1
            put_json(root, "RESULTS.json", results)
            with self.assertRaises(ValueError):
                verify_fixture(root)

    def test_F06_nonempty_output_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "keep.txt").write_text("Owner data")
            with self.assertRaises(ValueError):
                init_fixture(root)
            self.assertEqual((root / "keep.txt").read_text(), "Owner data")

    def test_F07_thirty_one_slice_fixture_leaves_work_at_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_fixture(root, 31)
            for n in range(1, 31):
                simulate_slice(root, f"c{n}")
            self.assertFalse(read_json(root, "STATE.json")["programme_complete"])
            self.assertEqual(verify_fixture(root)["completed_steps"], 30)
            self.assertEqual(len(list(root.iterdir())), 5)  # bounded file count

    def test_F08_wrong_result_cannot_pass_on_status_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_fixture(root)
            simulate_slice(root, "c1")
            results = read_json(root, "RESULTS.json")
            results[0]["summary"]["alpha"]["total"] += 1
            put_json(root, "RESULTS.json", results)
            with self.assertRaisesRegex(ValueError, "substantive"):
                verify_fixture(root)

    def test_F09_wrong_completion_type_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_fixture(root)
            state = read_json(root, "STATE.json")
            state["programme_complete"] = "false"
            put_json(root, "STATE.json", state)
            with self.assertRaises(ValueError):
                verify_fixture(root)
