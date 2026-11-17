"""Task 2: durable launch reservation tests. All SQLite files are disposable."""
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from launcher.journal import (
    JournalError,
    get_launch,
    init_journal,
    record_launch_outcome,
    reserve_launch,
)


class LaunchJournalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db = Path(self.tmp.name) / "launches.sqlite3"
        self.sha = "a" * 40
        self.run = "succession-20261117-001"

    def create(self):
        init_journal(self.db)

    def reserve(self, step=2, sha=None):
        return reserve_launch(self.db, self.run, step, sha or self.sha)

    def test_no_implicit_initialisation(self):
        with self.assertRaises(JournalError):
            self.reserve()
        self.assertFalse(self.db.exists())

    def test_explicit_initialisation_and_readback(self):
        self.create()
        self.assertEqual(self.reserve().state, "reserved")
        row = get_launch(self.db, self.run, 2)
        self.assertEqual((row.state, row.assignment_sha), ("reserved", self.sha))

    def test_initialisation_not_repeatable(self):
        self.create()
        with self.assertRaises(JournalError):
            init_journal(self.db)

    def test_duplicate_reservation_held(self):
        self.create()
        self.assertEqual(self.reserve().state, "reserved")
        self.assertEqual(self.reserve().state, "held")
        self.assertEqual(get_launch(self.db, self.run, 2).state, "reserved")

    def test_different_sha_conflicts(self):
        self.create()
        self.reserve()
        with self.assertRaises(JournalError):
            self.reserve(sha="b" * 40)

    def test_distinct_steps_allowed(self):
        self.create()
        self.assertEqual(self.reserve(2).state, "reserved")
        self.assertEqual(self.reserve(3).state, "reserved")
        self.assertEqual(get_launch(self.db, self.run, 3).assignment_sha, self.sha)

    def test_terminal_fourth_step_refused(self):
        self.create()
        with self.assertRaises(JournalError):
            self.reserve(4)
        self.assertIsNone(get_launch(self.db, self.run, 4))

    def test_first_step_is_manual_not_successor(self):
        self.create()
        with self.assertRaises(JournalError):
            self.reserve(1)

    def test_invalid_identity_rejected(self):
        self.create()
        with self.assertRaises(JournalError):
            reserve_launch(self.db, "bad/id", 2, self.sha)
        with self.assertRaises(JournalError):
            reserve_launch(self.db, self.run, 2, "short")

    def test_missing_journal_after_reservation_holds(self):
        self.create()
        self.reserve()
        self.db.unlink()
        with self.assertRaises(JournalError):
            self.reserve()
        self.assertFalse(self.db.exists())

    def test_unreadable_journal_holds(self):
        self.db.write_text("corrupted", encoding="utf-8")
        with self.assertRaises(JournalError):
            self.reserve()

    def test_crash_after_reservation_holds(self):
        self.create()
        self.reserve()
        # Simulate next process after losing the delivery acknowledgement.
        self.assertEqual(self.reserve().state, "held")

    def test_posted_terminal_and_receipt(self):
        self.create()
        self.reserve()
        self.assertEqual(
            record_launch_outcome(self.db, self.run, 2, self.sha, "posted",
                                  {"message_observed": True, "saved_url": "local-only"}).state,
            "posted",
        )
        self.assertEqual(get_launch(self.db, self.run, 2).state, "posted")
        self.assertEqual(self.reserve().state, "held")
        with self.assertRaises(JournalError):
            record_launch_outcome(self.db, self.run, 2, self.sha, "posted", {})

    def test_unknown_effect_holds(self):
        self.create()
        self.reserve()
        result = record_launch_outcome(self.db, self.run, 2, self.sha,
                                       "effect_unknown", {"reason": "send timeout"})
        self.assertEqual(result.state, "effect_unknown")
        self.assertEqual(self.reserve().state, "held")
        with self.assertRaises(JournalError):
            record_launch_outcome(self.db, self.run, 2, self.sha, "posted", {})

    def test_blocked_before_send_holds(self):
        self.create()
        self.reserve()
        record_launch_outcome(self.db, self.run, 2, self.sha, "blocked",
                              {"reason": "occupied draft"})
        self.assertEqual(self.reserve().state, "held")

    def test_mark_requires_prior_reservation_and_matching_sha(self):
        self.create()
        with self.assertRaises(JournalError):
            record_launch_outcome(self.db, self.run, 2, self.sha, "posted", {})
        self.reserve()
        with self.assertRaises(JournalError):
            record_launch_outcome(self.db, self.run, 2, "b" * 40, "posted", {})
        with self.assertRaises(JournalError):
            record_launch_outcome(self.db, self.run, 2, self.sha, "reserved", {})

    def test_concurrent_reservations_only_one_wins(self):
        self.create()
        with ThreadPoolExecutor(max_workers=8) as executor:
            records = list(executor.map(lambda _: self.reserve(), range(8)))
        self.assertEqual([r.state for r in records].count("reserved"), 1)
        self.assertEqual([r.state for r in records].count("held"), 7)

    def test_cli_init_reserve_and_status(self):
        source = Path(__file__).resolve().parents[1] / "launcher" / "journal.py"
        for args, expected_status in [
            (["init", "--db", str(self.db)], "initialised"),
            (["reserve", "--db", str(self.db), "--run", self.run, "--step", "2",
              "--sha", self.sha], "reserved"),
            (["status", "--db", str(self.db), "--run", self.run, "--step", "2"],
             "reserved"),
        ]:
            completed = subprocess.run([sys.executable, str(source), *args],
                                       text=True, capture_output=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(json.loads(completed.stdout)["state"], expected_status)


if __name__ == "__main__":
    unittest.main()
