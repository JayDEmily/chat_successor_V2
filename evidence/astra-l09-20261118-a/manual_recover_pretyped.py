#!/usr/bin/env python3
"""L09 one-shot, positive-no-click, pretyped continuation recovery.

This is a bounded operator action using the SAME private controller/state,
its existing exclusive lock, and the existing WindowsUIA Send adapter.
It is not a generic retry mechanism and must not run twice.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

repo = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo / "integration"))
from cli import exclusive_lock, load_config
from succession.core import Action, Controller
from windows_backend import WindowsUIA

SOURCE = "6afd2e8f-606c-83ec-a47b-4d6783bd711c"
ACTION_ID = (
    SOURCE + ":uia-turn-1-743656fa12f7da2e6a01:CONTINUE_CURRENT"
)
EXPECTED = "Okay, continue working."
FAILURE = "Foreground changed before Send"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    if os.environ.get("ASTRA_L09_FAULT"):
        raise RuntimeError("Fault injection must be disabled for this recovery")
    cfg = load_config(args.config)
    assert cfg["run_id"] == "astra-l09-20261118-a"
    browser = WindowsUIA(
        cfg["project"], cfg["project_name"],
        repo / "integration/uia_adapter.ps1", args.state,
    )
    with exclusive_lock(args.state):
        c = Controller.load(args.state)
        assert c.state.current_chat_id == SOURCE
        assert c.state.unique_chat_ids == [SOURCE]
        assert c.state.last_status == "NEED_MORE_TIME"
        p = c.state.pending
        assert p is not None
        assert p.action_id == ACTION_ID
        assert p.kind == Action.CONTINUE_CURRENT.value
        assert p.source_chat_id == SOURCE
        assert p.message == EXPECTED
        assert p.phase == "uncertain"
        assert FAILURE in p.detail, "Expected exact positive pre-click exception"
        saved_target = json.loads(browser.target_path.read_text(encoding="utf-8"))
        assert saved_target["kind"] == p.kind
        assert saved_target["source"] == SOURCE
        handle = saved_target["handle"]
        assert type(handle) is int and handle > 0
        observed = browser.reconcile_readonly()
        assert observed.project == cfg["project"]
        assert observed.chat_id == SOURCE
        assert not observed.posted_message_observed, (
            "Existing posted continuation found: never Send again")
        assert observed.submitted_text is None
        backup = args.state.with_name(args.state.name + ".l09_manual_recovery.bak")
        if backup.exists():
            raise FileExistsError("One-shot manual recovery already attempted")
        shutil.copy2(args.state, backup)
        backup_hash = hashlib.sha256(backup.read_bytes()).hexdigest()

        # The adapter's failure was at a source line before its Send Invoke,
        # and live readback found no continuation. This is positive no-click
        # evidence, rather than relying on an absent/stale sidebar entry.
        c.confirm_not_sent(
            ACTION_ID, "Observed adapter threw Foreground changed before Send "
            "before invoking any Send control; read-only user-turn "
            "reconciliation is false. Exact test draft remains unsent.")
        c.begin_send(ACTION_ID)
        c.save(args.state)  # durable before the only possible UI Send
        try:
            result = browser._invoke(
                "Send",
                Kind=p.kind,
                ChatId=SOURCE,
                WindowHandle=handle,
                Message=EXPECTED,
                AlreadyTyped=True,
            )
            if not (
                result.get("posted_message_observed") is True
                and result.get("submitted_text") == EXPECTED
                and result.get("project") == cfg["project"]
                and result.get("chat_id") == SOURCE
            ):
                raise RuntimeError("Exact posted continuation and chat identity not observed")
            decision = c.confirm(ACTION_ID, SOURCE, cfg["project"],
                                 message_observed=True)
            if decision.action != Action.WAIT:
                raise RuntimeError("Controller did not adopt observed continuation")
            c.save(args.state)
            again = Controller.load(args.state)
            assert again.state.pending is None
            assert again.unique_count == 1
            print(json.dumps({
                "outcome": "CONFIRMED_SINGLE_SAME_CHAT_CONTINUATION",
                "source_chat_id": SOURCE,
                "unique_chat_count": again.unique_count,
                "posted_message_observed": True,
                "pending": None,
                "backup_sha256": backup_hash,
                "new_state_sha256": hashlib.sha256(args.state.read_bytes()).hexdigest(),
            }, indent=2))
            return 0
        except Exception as exc:
            # No automatic retry. A failure after persisted sending must
            # remain uncertain until independent reconciliation.
            if c.state.pending is not None:
                c.uncertain(ACTION_ID, "Manual L09 AlreadyTyped Send outcome unknown: " + str(exc))
                c.save(args.state)
            print(json.dumps({
                "outcome": "HOLD_UNCERTAIN_NO_RETRY",
                "detail": str(exc),
                "backup_sha256": backup_hash,
                "unique_chat_count": c.unique_count,
            }, indent=2))
            return 2

if __name__ == "__main__":
    raise SystemExit(main())
