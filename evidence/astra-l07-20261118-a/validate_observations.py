#!/usr/bin/env python3
"""Validate L07 *recorded* observations. This is not a substitute for live UIA evidence."""
from __future__ import annotations
import csv
import hashlib
import json
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
repo = here.parents[1]
kit = repo / "astra/2026-11-17/unpacked/chat_succession_test_kit_20261117"
sys.path.insert(0, str(kit))
from succession.composer import ComposerObservation, ComposerState, classify_composer

record = json.loads((here / "live_record.json").read_text(encoding="utf-8"))
assert record["test_id"] == "L07"
assert record["outcome"] == "BLOCKED" and record["acceptance_met"] is False
assert record["save_or_send_operations"] == 0
assert len(record["observations"]) == 4
expect = ["EMPTY", "DRAFT", "DRAFT", "UNKNOWN"]
for obs, wanted in zip(record["observations"], expect):
    if obs["status"] == "OBSERVED":
        snapshot = ComposerObservation(
            editable_text=obs["actual_editable_text"],
            uia_value=obs["uia_value"],
            attachments_present=obs["attachments_present"],
        )
        screenshot = here / obs["rendered_editor"]
        assert screenshot.is_file(), screenshot
        actual_hash = hashlib.sha256(screenshot.read_bytes()).hexdigest()
        assert actual_hash == obs["screenshot_sha256"], screenshot
    else:
        assert obs["state"] == "attachment_only"
        assert obs["actual_editable_text"] is None
        snapshot = ComposerObservation(
            editable_text=None, uia_value=None, attachments_present=None
        )
    actual_state = classify_composer(snapshot)
    assert actual_state == ComposerState(wanted), (obs["state"], actual_state)
    assert obs["classification"] == wanted, (obs["state"], obs["classification"])
sheet = repo / "evidence/live_test_results_20261118.csv"
with sheet.open(newline="", encoding="utf-8") as handle:
    entries = list(csv.DictReader(handle))
row = next(r for r in entries if r["test_id"] == "L07")
assert row["outcome"] == "BLOCKED", row["outcome"]
assert row["run_id"] == record["run_id"]
assert all(r["outcome"] == "PASS" for r in entries[:6])
assert all(r["outcome"] == "NOT_RUN" for r in entries[7:])
print(json.dumps({
    "record_valid": True,
    "directly_observed": 3,
    "required": 4,
    "attachment_only_live_observed": False,
    "outcome": "BLOCKED",
    "screenshots_sha256_verified": 3,
    "prior_L01_through_L06_preserved": True,
    "later_L08_through_L15_unchanged": True
}, indent=2))
