"""Independent A2-L02 negative regressions against published 3f9715e.

Offline fixtures only. No GitHub, Windows browser, account switch or Send.
"""
from pathlib import Path
import json
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from account_routes import require_route
from runner import inspect_state, initialise
from succession.core import Config, Controller


class A2L02StrictReviewTests(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.install = Path(temp.name)
        (self.install / "account-routing-required").write_bytes(b"")
        self.route_file = self.install / "account_routes.json"

    def entry(self, profile):
        return {"install_root": str(self.install), "profile_path": profile,
                "chrome_app_id": "Chrome.Test",
                "plugin_id": "plugins_12345678",
                "backend_commit": "a" * 40}

    def test_duplicate_account_json_key_holds_instead_of_last_wins(self):
        first = json.dumps(self.entry("C:\\Chrome\\Profile11"))
        second = json.dumps({**self.entry("C:\\Chrome\\Profile13"),
                             "plugin_id": "plugins_abcdefgh"})
        self.route_file.write_text(
            '{"schema":1,"accounts":{"shoco":' + first + ',"shoco":' + second + '}}')
        with self.assertRaisesRegex(ValueError, "malformed"):
            require_route(self.install, "shoco")

    def test_shared_chrome_profile_across_accounts_holds(self):
        self.route_file.write_text(json.dumps({"schema": 1, "accounts": {
            "shoco": self.entry("C:\\Users\\james\\Chrome\\Profile11"),
            "james-student": self.entry("c:/users/james/Chrome/Profile11"),
        }}))
        with self.assertRaisesRegex(ValueError, "share one Chrome profile"):
            require_route(self.install, "shoco")
        with self.assertRaisesRegex(ValueError, "share one Chrome profile"):
            require_route(self.install, "james-student")

    def test_marker_after_pre_send_gate_is_acknowledged_read_only(self):
        state = self.install / "controller.json"
        c = initialise(state, Config("g-p-test", "example-org/test", "main", 2),
                       "00000000-0000-0000-0000-000000000001")
        c.pause("Operator pause requested before Send")
        c.save(state)
        marker = state.with_suffix(".pause")
        marker.write_text("Owner pause gate 1")
        before = state.read_bytes()
        info = inspect_state(state)
        self.assertEqual(info["halted"], "Operator pause requested before Send")
        self.assertTrue(info["pause_requested"])
        self.assertTrue(info["pause_acknowledged"])
        self.assertEqual(state.read_bytes(), before)
        self.assertEqual(marker.read_text(), "Owner pause gate 1")

    def test_shared_window_profile_identity_holds_even_with_different_paths(self):
        self.route_file.write_text(json.dumps({"schema": 1, "accounts": {
            "shoco": self.entry("C:\\Chrome\\Profile11"),
            "james-student": {**self.entry("C:\\Chrome\\Profile13"), "plugin_id": "plugins_abcdefgh"},
        }}))
        with self.assertRaisesRegex(ValueError, "share a Chrome window identity"):
            require_route(self.install, "shoco")


if __name__ == "__main__":
    unittest.main()
