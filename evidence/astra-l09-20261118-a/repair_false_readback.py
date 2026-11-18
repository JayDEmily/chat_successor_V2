#!/usr/bin/env python3
"""One-shot L09 private-state repair after demonstrated false-positive readback.

Use only when before_click injected fault has positive no-UIA-Send evidence and
the quoted expected continuation was incorrectly adopted. Never generic retry.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

repo = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo / "integration"))
from cli import exclusive_lock
from succession.core import Controller, Pending

SOURCE = "6afd2e8f-606c-83ec-a47b-4d6783bd711c"
RESPONSE = "uia-turn-1-743656fa12f7da2e6a01"
KIND = "CONTINUE_CURRENT"
ACTION = f"{SOURCE}:{RESPONSE}:{KIND}"
MESSAGE = "Okay, continue working."
REASON = ("L09 before_click injection positively prevented UIA Send; "
          "role-scoped live Reconcile found no posted continuation; "
          "original quoted assistant text caused false-positive adoption.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", type=Path, required=True)
    args = ap.parse_args()
    state_path = args.state
    with exclusive_lock(state_path):
        c = Controller.load(state_path)
        assert c.state.current_chat_id == SOURCE
        assert c.state.unique_chat_ids == [SOURCE]
        assert c.state.last_status == "NEED_MORE_TIME"
        assert c.state.halted is None and c.state.pending is None
        assert [SOURCE, RESPONSE] in c.state.consumed_responses
        original = state_path.read_bytes()
        backup = state_path.with_name(state_path.name + ".l09_false_positive.backup")
        if backup.exists():
            raise FileExistsError("Refusing repeated repair")
        shutil.copy2(state_path, backup)
        assert backup.read_bytes() == original
        c.state.pending = Pending(ACTION, KIND, SOURCE, RESPONSE, MESSAGE,
                                  phase="uncertain",
                                  detail="Original before-click action misconfirmed by role-blind readback")
        c.state.halted = "L09 false-positive readback repair"
        c.confirm_not_sent(ACTION, REASON)
        c.save(state_path)
        check = Controller.load(state_path)
        assert check.state.pending is not None
        assert check.state.pending.action_id == ACTION
        assert check.state.pending.phase == "prepared"
        assert check.state.pending.message == MESSAGE
        assert check.state.halted is None
        assert check.unique_count == 1
        assert check.state.consumed_responses == c.state.consumed_responses
        print(json.dumps({
            "repair": "L09_SINGLE_BOUNDED_TEST_STATE",
            "backup_sha256": hashlib.sha256(original).hexdigest(),
            "repaired_state_sha256": hashlib.sha256(state_path.read_bytes()).hexdigest(),
            "positive_no_send_reason": REASON,
            "pending_kind": KIND,
            "pending_phase": check.state.pending.phase,
            "unique_chat_count": check.unique_count,
            "continuation_sent_by_repair": False,
        }, indent=2))

if __name__ == "__main__":
    main()
