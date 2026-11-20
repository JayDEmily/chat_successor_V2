#!/usr/bin/env python3
"""Offline characterization of the supplied 0.4.3 baseline, not live acceptance.

No network/browser/process launcher is invoked. All writes are to new temporary
directories. P07-P09 deliberately demonstrate baseline limitations; a passing
assertion for those probes does NOT mean the desired safety improvement exists.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, required=True, help="Extracted source/ directory")
parser.add_argument("--json-out", type=Path)
args = parser.parse_args()
source = args.source.resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(source / "integration"))

from cli import load_config
from launch_project import read_request
from runner import Destination, dispatch_prepared, inspect_state
from succession.composer import ComposerObservation
from succession.core import Action, Config, Controller, RepoView, Response
from windows_backend import WindowsUIA

PROJECT = "g-p-abcdef"
REPO = "ExampleOwner/fixture"
CHAT1 = "11111111-1111-4111-8111-111111111111"
CHAT2 = "22222222-2222-4222-8222-222222222222"

DESCRIPTIONS = {
    "P01": ("INVARIANT_CHECK", "Cap stop with an eligible next assignment survives reload and refuses resume."),
    "P02": ("INVARIANT_CHECK", "FINISHED takes precedence over cap when the published programme is complete."),
    "P03": ("INVARIANT_CHECK", "NEED_MORE_TIME at the cap continues the same chat; repeated response is ignored."),
    "P04": ("INVARIANT_CHECK", "A durable pause marker blocks dispatch after preparation; pending action/count survive reload."),
    "P05": ("INVARIANT_CHECK", "Restart with a possibly sent action holds; positive adoption counts once and does not Send."),
    "P06": ("INPUT_CONTRACT", "New job IDs accept 24 lowercase alphanumerics and reject a 32-character ID."),
    "P07": ("LIMITATION_REPRODUCED", "The baseline config schema rejects proposed account/profile binding fields."),
    "P08": ("LIMITATION_REPRODUCED", "With browser invocation mocked, send_once accepts a target record with a different action_id when handle/source/kind match."),
    "P09": ("LIMITATION_REPRODUCED", "inspect_state alone does not expose a pause marker before controller acknowledgement."),
}

def response(text="CHAT_STATUS: TASK_COMPLETE", chat=CHAT1, anchor="r1"):
    return Response(chat, anchor, text, project=PROJECT)

def view(chat=CHAT1, finished=False):
    return RepoView(REPO, "main", chat, finished, None if finished else "One eligible next assignment")

def controller(cap=2):
    return Controller(Config(PROJECT, REPO, "main", cap), CHAT1)

class BaselineProbes(unittest.TestCase):
    def test_P01_cap_stop_survives_restart(self):
        c = controller()
        d = c.consume(response(), view())
        self.assertEqual(d.action, Action.LAUNCH_SUCCESSOR)
        c.begin_send(d.action_id)
        c.confirm(d.action_id, CHAT2, PROJECT)
        d2 = c.consume(response(chat=CHAT2, anchor="r2"), view(CHAT2))
        self.assertEqual(d2.action, Action.STOP_CAP)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "controller.json"
            c.save(path)
            restored = Controller.load(path)
            self.assertEqual(restored.unique_count, 2)
            self.assertIsNone(restored.state.pending)
            with self.assertRaises(ValueError):
                restored.resume_after_owner()

    def test_P02_finish_before_cap(self):
        c = controller(cap=1)
        self.assertEqual(c.consume(response(), view(finished=True)).action, Action.STOP_FINISHED)
        self.assertEqual(c.unique_count, 1)

    def test_P03_continue_at_cap_and_deduplicate(self):
        c = controller(cap=1)
        r = response("CHAT_STATUS: NEED_MORE_TIME")
        d = c.consume(r)
        self.assertEqual(d.action, Action.CONTINUE_CURRENT)
        c.begin_send(d.action_id)
        c.confirm(d.action_id, CHAT1, PROJECT)
        self.assertEqual(c.unique_count, 1)
        self.assertEqual(c.consume(r).action, Action.IGNORE)
        self.assertIsNone(c.state.pending)

    def test_P04_pause_after_prepare_survives_restart(self):
        c = controller()
        c.consume(response("CHAT_STATUS: NEED_MORE_TIME"))
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "controller.json"
            c.save(path)
            marker = path.with_suffix(".pause")
            marker.write_text("unique-owner-pause-token", encoding="utf-8")
            browser = Mock()
            browser.prepare.return_value = Destination(
                PROJECT, CHAT1, ComposerObservation("", "", False), 17
            )
            self.assertEqual(dispatch_prepared(c, browser, path), Action.HOLD)
            browser.send_once.assert_not_called()
            restored = Controller.load(path)
            self.assertTrue(marker.exists())
            self.assertEqual(restored.unique_count, 1)
            self.assertEqual(restored.config.max_unique_chats, 2)
            self.assertEqual(restored.state.pending.phase, "prepared")

    def test_P05_uncertain_action_is_not_retried(self):
        c = controller()
        d = c.consume(response(), view())
        c.begin_send(d.action_id)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "controller.json"
            c.save(path)
            restored = Controller.load(path)
            browser = Mock()
            self.assertEqual(dispatch_prepared(restored, browser, path), Action.HOLD)
            browser.prepare.assert_not_called()
            browser.send_once.assert_not_called()
            self.assertEqual(restored.confirm(d.action_id, CHAT2, "g-p-wrong").action, Action.HOLD)
            self.assertEqual(restored.unique_count, 1)
            self.assertEqual(restored.confirm(d.action_id, CHAT2, PROJECT).action, Action.WAIT)
            self.assertEqual(restored.unique_count, 2)
            self.assertEqual(restored.confirm(d.action_id, CHAT2, PROJECT).action, Action.IGNORE)
            self.assertEqual(restored.unique_count, 2)

    def test_P06_job_id_contract(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "request.json"
            request = {"operation": "new", "repo": REPO, "branch": "main",
                       "project_name": "Disposable fixture", "job_id": "a" * 24}
            path.write_text(json.dumps(request), encoding="utf-8")
            self.assertEqual(read_request(path)["job_id"], "a" * 24)
            request["job_id"] = "a" * 32
            path.write_text(json.dumps(request), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Invalid job_id"):
                read_request(path)

    def test_P07_characterize_absent_account_binding_schema(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "config.json"
            cfg = {"project": PROJECT, "project_name": "Fixture", "repo": REPO,
                   "branch": "main", "run_id": "a" * 24, "max_unique_chats": 2,
                   "repo_dir_wsl": "/unused/local/readback.git", "workflow": "git-handoff",
                   "project_url": f"https://chatgpt.com/g/{PROJECT}/project"}
            path.write_text(json.dumps(cfg), encoding="utf-8")
            load_config(path)
            cfg["account_key"] = "account-a"
            cfg["chrome_profile_path"] = "not-a-real-profile"
            path.write_text(json.dumps(cfg), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "documented fields"):
                load_config(path)

    def test_P08_characterize_unchecked_target_action_id(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "controller.json"
            c = controller()
            d = c.consume(response("CHAT_STATUS: NEED_MORE_TIME"))
            c.begin_send(d.action_id)
            c.save(path)
            bridge = WindowsUIA(PROJECT, "Fixture", Path("unused.ps1"), path)
            bridge._atomic_target_write({
                "kind": "CONTINUE_CURRENT", "source": CHAT1, "handle": 17,
                "action_id": "an-older-different-action"
            })
            bridge._invoke = Mock(return_value={
                "project": PROJECT, "chat_id": CHAT1,
                "submitted_text": c.state.pending.message,
                "posted_message_observed": True,
            })
            target = Destination(PROJECT, CHAT1, ComposerObservation("", "", False), 17)
            observed = bridge.send_once(target, c.state.pending.message)
            self.assertTrue(observed.posted_message_observed)
            bridge._invoke.assert_called_once()
            self.assertEqual(bridge._invoke.call_args.args[0], "Send")

    def test_P09_characterize_pause_status_omission(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "controller.json"
            controller().save(path)
            original = path.read_bytes()
            path.with_suffix(".pause").write_text("pause-requested", encoding="utf-8")
            summary = inspect_state(path)
            self.assertIsNone(summary["halted"])
            self.assertNotIn("pause_marker", summary)
            self.assertEqual(path.read_bytes(), original)

class Result(unittest.TextTestResult):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.rows = []
    def addSuccess(self, test):
        super().addSuccess(test)
        ident = test._testMethodName.split("_")[1]
        classification, description = DESCRIPTIONS[ident]
        self.rows.append({"probe_id": ident, "classification": classification,
                          "assertion_result": "PASS", "description": description})

result = unittest.TextTestRunner(verbosity=2, resultclass=Result).run(
    unittest.defaultTestLoader.loadTestsFromTestCase(BaselineProbes)
)
summary = {"mode": "OFFLINE_CHARACTERIZATION_ONLY", "tests_run": result.testsRun,
           "failures": len(result.failures), "errors": len(result.errors),
           "skipped": len(result.skipped), "probes": result.rows,
           "browser_calls_real": 0, "network_calls": 0,
           "warning": "P07-P09 PASS means a baseline limitation was reproduced, not that it is fixed."}
if args.json_out:
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
else:
    print(json.dumps(summary, indent=2))
raise SystemExit(0 if result.wasSuccessful() else 1)
