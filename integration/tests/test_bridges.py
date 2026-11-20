"""New Git published-view and Windows bridge unit tests; no network or Send."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from repo_reader import GitPublishedReader, PublishedStateError
from runner import Destination, SendBlockedBeforeClick, initialise
from windows_backend import WindowsUIA, BrowserObservationError
from succession.core import Config, Controller, Response
from succession.composer import ComposerObservation


class RepoReaderTests(unittest.TestCase):
    def reader(self):
        return GitPublishedReader(Path("/tmp/checkout"),
                                  "JayDEmily/chat_successor", "trial/l01",
                                  "succession-tests/l01")

    def test_exact_remote_commit_not_working_tree(self):
        r = self.reader()
        transcript = []
        state = {"run_id": "l01", "programme_complete": False,
                 "next_task": "slice 2", "last_chat_id": "chat-first"}
        def git(*args):
            transcript.append(args)
            if args[:2] == ("remote", "get-url"):
                return "https://github.com/JayDEmily/chat_successor.git"
            if args[0] == "fetch":
                return ""
            if args[0] == "rev-parse":
                return "a" * 40
            if args[0] == "show":
                return json.dumps(state)
            raise AssertionError(args)
        r._git = git
        o = r.read("l01")
        self.assertTrue(o.view.published)
        self.assertEqual(o.view.last_chat_id, "chat-first")
        self.assertEqual(o.commit, "a" * 40)
        self.assertIn(("show", f"{'a'*40}:succession-tests/l01/STATE.json"), transcript)
        self.assertTrue(any(row[0] == "fetch" for row in transcript))
        self.assertFalse(any(row[0] == "status" for row in transcript))

    def test_reject_mismatched_run_and_stale_attribution(self):
        r = self.reader()
        r._git = lambda *a: {
            "remote": "https://github.com/JayDEmily/chat_successor.git",
            "fetch": "", "rev-parse": "b"*40,
            "show": json.dumps({"run_id": "other", "programme_complete": False,
                                "next_task": "x", "last_chat_id": "chat-first"}),
        }[a[0]]
        with self.assertRaises(PublishedStateError):
            r.read("l01")

    def test_reject_nonboolean_completion(self):
        r = self.reader()
        r._git = lambda *a: {
            "remote": "https://github.com/JayDEmily/chat_successor.git",
            "fetch": "", "rev-parse": "b"*40,
            "show": json.dumps({"run_id": "l01", "programme_complete": "false",
                                "next_task": "x", "last_chat_id": "chat-first"}),
        }[a[0]]
        with self.assertRaises(PublishedStateError):
            r.read("l01")

    def test_scoped_path_and_ref(self):
        with self.assertRaises(ValueError):
            GitPublishedReader(Path("/tmp"), "JayDEmily/chat_successor",
                               "../main", "succession-tests/l01")
        with self.assertRaises(ValueError):
            GitPublishedReader(Path("/tmp"), "JayDEmily/chat_successor",
                               "trial/l01", "../private/STATE.json")


class WindowsBridgeTests(unittest.TestCase):
    def test_malformed_observation_recovers_on_one_retry(self):
        bridge = WindowsUIA("g-p-TEST", "Project", Path("adapter.ps1"), Path("controller.json"))
        malformed = Mock(returncode=0, stdout="{")
        recovered = Mock(returncode=0, stdout='{"ready": false}')
        with patch("windows_backend.subprocess.run", side_effect=[malformed, recovered]) as run:
            with self.assertLogs("windows_backend", level="WARNING"):
                self.assertEqual(bridge._invoke("Observe", ChatId="chat-first"), {"ready": False})
            self.assertEqual(run.call_count, 2)

    def test_persistent_malformed_observation_holds_and_send_never_retries(self):
        bridge = WindowsUIA("g-p-TEST", "Project", Path("adapter.ps1"), Path("controller.json"))
        malformed = Mock(returncode=0, stdout="{")
        with patch("windows_backend.subprocess.run", return_value=malformed) as run:
            with self.assertLogs("windows_backend", level="WARNING"):
                with self.assertRaisesRegex(BrowserObservationError, "Observe returned unparseable"):
                    bridge._invoke("Observe", ChatId="chat-first")
            self.assertEqual(run.call_count, 2)
            run.reset_mock()
            with self.assertRaisesRegex(BrowserObservationError, "Send returned unparseable"):
                bridge._invoke("Send")
            self.assertEqual(run.call_count, 1)

    def test_reuse_only_the_same_actions_prepared_successor_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "controller.json"
            w = WindowsUIA("g-p-TEST", "Project", Path(tmp) / "uia_adapter.ps1", state)
            w._invoke = Mock(return_value={"project": "g-p-TEST", "current_chat_id": None,
                                          "private_window_handle": 34, "editable_text": "",
                                          "attachments_present": False})
            pending = {"kind": "LAUNCH_SUCCESSOR", "source_chat_id": "chat-first", "phase": "prepared",
                       "response_id": "turn-one", "action_id": "action-one",
                       "message": "Next worker instruction"}
            state.write_text(json.dumps({"state": {"pending": pending}}))
            w._atomic_target_write({"kind": "LAUNCH_SUCCESSOR", "source": "chat-first", "handle": 12,
                                    "action_id": "action-one"})
            w.prepare("LAUNCH_SUCCESSOR", "chat-first")
            self.assertEqual(w._invoke.call_args.kwargs["WindowHandle"], 12)
            self.assertEqual(w._invoke.call_args.kwargs["SourceResponse"], "turn-one")
            pending["action_id"] = "action-two"
            state.write_text(json.dumps({"state": {"pending": pending}}))
            w.prepare("LAUNCH_SUCCESSOR", "chat-first")
            self.assertNotIn("WindowHandle", w._invoke.call_args.kwargs)
            # A different triggering worker or action kind is a hard hold,
            # not an opportunity to prepare another window.
            with self.assertRaisesRegex(BrowserObservationError, "persisted action identity"):
                w.prepare("LAUNCH_SUCCESSOR", "chat-second")
            w._invoke.return_value["current_chat_id"] = "chat-second"
            with self.assertRaisesRegex(BrowserObservationError, "persisted action identity"):
                w.prepare("CONTINUE_CURRENT", "chat-second")

    def test_send_only_after_disk_recorded_sending(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "controller.json"
            cfg = Config("g-p-TEST", "JayDEmily/chat_successor", "trial/l01", 3)
            c = initialise(state, cfg, "chat-first")
            w = WindowsUIA(cfg.project, "Chat succession folder",
                           Path(tmp) / "uia_adapter.ps1", state)
            response = Response("chat-first", "turn1", "CHAT_STATUS: NEED_MORE_TIME",
                                project=cfg.project)
            d = c.consume(response)
            c.save(state)
            t = Destination(cfg.project, "chat-first", ComposerObservation(editable_text=""), 1234)
            w._atomic_target_write({"kind": "CONTINUE_CURRENT",
                                    "source": "chat-first", "handle": 1234,
                                    "project": cfg.project, "action_id": d.action_id,
                                    "source_response": "turn1",
                                    "message_sha256": hashlib.sha256(d.message.encode()).hexdigest(),
                                    "route_receipt": None})
            w._invoke = Mock(return_value={"project": cfg.project, "chat_id": "chat-first",
                                           "submitted_text": d.message,
                                           "posted_message_observed": True})
            with self.assertRaises(BrowserObservationError):
                w.send_once(t, d.message)
            self.assertEqual(w._invoke.call_count, 0)
            c.begin_send(d.action_id)
            c.save(state)
            receipt = w.send_once(t, d.message)
            self.assertTrue(receipt.posted_message_observed)
            self.assertEqual(w._invoke.call_count, 1)
            self.assertEqual(w._invoke.call_args.kwargs["SourceResponse"], "turn1")
            w._invoke.return_value = {"destination_changed_before_click": True}
            with self.assertRaises(SendBlockedBeforeClick):
                w.send_once(t, d.message)
            w.reconcile_readonly()
            self.assertEqual(w._invoke.call_args.kwargs["SourceResponse"], "turn1")


if __name__ == "__main__":
    unittest.main()
