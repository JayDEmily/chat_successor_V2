#!/usr/bin/env python3
"""One-shot owner corrective message in held L09 successor, using existing Send adapter.

This is an explicit owner/operator recovery, not a worker continuation,
controller retry, new browser/project or new succession controller.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

repo = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo / "integration"))
from cli import exclusive_lock, load_config
from succession.core import Controller
from succession.composer import classify_composer, ComposerState
from windows_backend import WindowsUIA

CHAT = "6afd3221-f970-83ec-9889-1d09b1762a5f"
PROJECT = "g-p-6afbfc5e59248191a8c690296b24c8ef"
TEXT = ("L09 status correction only. Do not process slice 2. "
        "Reply with exactly one line: CHAT_STATUS: NEED_MORE_TIME")


def write_atomic(path: Path, obj: dict) -> None:
    blob = json.dumps(obj, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    fd, temp = tempfile.mkstemp(prefix="owner-correction-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(blob)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--state", required=True, type=Path)
    args = parser.parse_args()
    if os.environ.get("ASTRA_L09_FAULT"):
        raise RuntimeError("Fault injection must be disabled")
    cfg = load_config(args.config)
    assert cfg["run_id"] == "astra-l09-20261118-a"
    assert cfg["project"] == PROJECT
    proof_path = args.state.with_name("l09_owner_corrective_intent.json")
    browser = WindowsUIA(PROJECT, cfg["project_name"],
                         repo / "integration/uia_adapter.ps1", args.state)
    with exclusive_lock(args.state):
        if proof_path.exists():
            raise FileExistsError("Corrective message already attempted; inspect evidence, do not resend")
        controller = Controller.load(args.state)
        assert controller.state.current_chat_id == CHAT
        assert controller.state.halted == "Repeated, conflicting or nonterminal status"
        assert controller.state.pending is None
        assert controller.state.last_status == "TASK_COMPLETE"
        assert controller.unique_count == 2
        assert len(controller.state.consumed_responses) == 3
        destination = browser.prepare("CONTINUE_CURRENT", CHAT)
        assert destination.project == PROJECT and destination.current_chat_id == CHAT
        assert classify_composer(destination.composer) == ComposerState.EMPTY
        posted = browser._invoke("Reconcile", Kind="CONTINUE_CURRENT",
                                 ChatId=CHAT,
                                 WindowHandle=destination.private_window_handle,
                                 Message=TEXT)
        assert posted.get("project") == PROJECT and posted.get("chat_id") == CHAT
        if posted.get("posted_message_observed"):
            raise RuntimeError("Exact corrective user message already posted")
        base = {
            "run_id": "astra-l09-20261118-a",
            "kind": "OWNER_OPERATOR_STATUS_CORRECTION",
            "chat_id": CHAT,
            "message": TEXT,
            "message_sha256": hashlib.sha256(TEXT.encode()).hexdigest(),
            "project": PROJECT,
            "window_handle": destination.private_window_handle,
            "unique_chat_count_before": controller.unique_count,
            "started_utc": datetime.now(timezone.utc).isoformat(),
            "phase": "sending_or_uncertain",
            "controller_state_modified": False,
        }
        write_atomic(proof_path, base)  # durable intent before sole Send
        try:
            receipt = browser._invoke("Send", Kind="CONTINUE_CURRENT", ChatId=CHAT,
                                      WindowHandle=destination.private_window_handle,
                                      Message=TEXT)
            if not (receipt.get("posted_message_observed") is True
                    and receipt.get("submitted_text") == TEXT
                    and receipt.get("project") == PROJECT
                    and receipt.get("chat_id") == CHAT):
                raise RuntimeError("Exact user-turn posted message not confirmed")
            base.update(phase="confirmed", confirmed_utc=datetime.now(timezone.utc).isoformat(),
                        posted_message_observed=True,
                        unique_chat_count_after=Controller.load(args.state).unique_count)
            write_atomic(proof_path, base)
            print(json.dumps({"outcome": "ONE_CORRECTIVE_USER_MESSAGE_CONFIRMED",
                              "chat_id": CHAT, "unique_chat_count": 2,
                              "controller_halt_preserved": True,
                              "intent_path": str(proof_path),
                              "message_sha256": base["message_sha256"]}, indent=2))
            return 0
        except Exception as error:
            base.update(phase="uncertain_hold_no_retry",
                        error=str(error),
                        observed_utc=datetime.now(timezone.utc).isoformat())
            write_atomic(proof_path, base)
            print(json.dumps({"outcome": "UNCERTAIN_NO_RETRY", "detail": str(error),
                              "intent_path": str(proof_path)}, indent=2))
            return 2


if __name__ == "__main__":
    raise SystemExit(main())
