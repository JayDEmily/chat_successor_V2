#!/usr/bin/env python3
"""Explicit L09 successor rearm after positive pre-typing/no-Send evidence."""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

repo = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo / "integration"))
from cli import exclusive_lock, load_config
from succession.core import Controller
from windows_backend import WindowsUIA

SOURCE = "6afd2e8f-606c-83ec-a47b-4d6783bd711c"
ACTION_ID = SOURCE + ":uia-turn-2-ef188239d7b0fd3a39bc:LAUNCH_SUCCESSOR"
MESSAGE = (
    "Continue the work in GitHub repo JayDEmily/chat_successor, "
    "branch work/astra-succession-implementation-20261118. "
    "Read the current instructions, progress and next task there."
)
DETAIL = "Incorrect foreground before typing"

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--state", type=Path, required=True)
    p.add_argument("--config", type=Path, required=True)
    args = p.parse_args()
    cfg = load_config(args.config)
    assert cfg["run_id"] == "astra-l09-20261118-a"
    browser = WindowsUIA(
        cfg["project"], cfg["project_name"],
        repo / "integration/uia_adapter.ps1", args.state)
    with exclusive_lock(args.state):
        c = Controller.load(args.state)
        pending = c.state.pending
        assert pending is not None
        assert pending.action_id == ACTION_ID
        assert pending.kind == "LAUNCH_SUCCESSOR"
        assert pending.source_chat_id == SOURCE
        assert pending.message == MESSAGE
        assert pending.phase == "uncertain"
        assert DETAIL in pending.detail
        assert c.unique_count == 1 and c.state.current_chat_id == SOURCE
        assert c.state.last_status == "TASK_COMPLETE"
        target = json.loads(browser.target_path.read_text(encoding="utf-8"))
        assert target["kind"] == pending.kind and target["source"] == SOURCE
        receipt = browser.reconcile_readonly()
        assert not receipt.posted_message_observed
        assert receipt.submitted_text is None
        backup = args.state.with_name(args.state.name + ".l09_successor_preclick.bak")
        if backup.exists():
            raise FileExistsError("Refusing second rearm for this fault")
        shutil.copy2(args.state, backup)
        before = hashlib.sha256(backup.read_bytes()).hexdigest()
        c.confirm_not_sent(
            ACTION_ID,
            "Exact L09 UIA error occurred before target editor ValuePattern "
            "write and before the sole Send Invoke; read-only posted user "
            "message check was false.")
        c.save(args.state)
        saved = Controller.load(args.state)
        assert saved.state.pending is not None
        assert saved.state.pending.phase == "prepared"
        assert saved.state.pending.action_id == ACTION_ID
        assert saved.unique_count == 1
        print(json.dumps({
            "result": "EXPLICIT_NO_SEND_REARM_SUCCESSOR",
            "pending_phase": saved.state.pending.phase,
            "pending_kind": saved.state.pending.kind,
            "unique_chat_count": saved.unique_count,
            "backup_sha256": before,
            "rearmed_state_sha256": hashlib.sha256(args.state.read_bytes()).hexdigest(),
            "send_performed": False,
        }, indent=2))

if __name__ == "__main__":
    main()
