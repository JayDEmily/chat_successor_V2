#!/usr/bin/env python3
"""Check recorded L07 observations and fixture classification. Not a substitute for live UI evidence."""
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
attempt4 = json.loads((here / "attempt4.json").read_text(encoding="utf-8"))
assert record["test_id"] == "L07" and record["outcome"] == "PASS"
assert record["acceptance_met"] is True and record["save_or_send_operations"] == 0
assert record["saved_chat_ids_created"] == [] and record["controller_or_launcher_used"] is False
assert len(record["observations"]) == 4
expected = ["EMPTY", "DRAFT", "DRAFT", "DRAFT"]
for observed, wanted in zip(record["observations"], expected):
    assert observed["status"] == "OBSERVED", observed["state"]
    assert observed["classification"] == wanted, observed["state"]
    snapshot = ComposerObservation(
        editable_text=observed["actual_editable_text"],
        uia_value=observed["uia_value"],
        attachments_present=observed["attachments_present"],
    )
    assert classify_composer(snapshot) == ComposerState(wanted), observed["state"]
    screenshot = here / observed["rendered_editor"]
    assert screenshot.is_file(), screenshot
    digest = hashlib.sha256(screenshot.read_bytes()).hexdigest()
    assert digest == observed["screenshot_sha256"], screenshot
attachment = record["observations"][3]
assert attachment["state"] == "attachment_only"
assert attachment["actual_editable_text"] == "" and attachment["attachments_present"] is True
assert attachment["uia_value"] == "New chat in Chat succession folder\n"
assert attachment["attachment_bytes"] == 65
file_name = attachment["attachment_filename"]
assert {"name": "Remove " + file_name, "control_type": "Button"} in attachment["positive_accessibility_controls"]
assert attempt4["after"]["attachment_present"] is True
assert attempt4["after"]["actual_editable_text"] == ""
assert attempt4["after"]["screenshot_sha256"] == attachment["screenshot_sha256"]
assert attempt4["messages_sent"] == 0 and attempt4["saved_chats_created"] == 0
sheet = repo / "evidence/live_test_results_20261118.csv"
with sheet.open(newline="", encoding="utf-8") as handle:
    entries = list(csv.DictReader(handle))
row = next(r for r in entries if r["test_id"] == "L07")
assert row["outcome"] == "PASS", row["outcome"]
assert row["run_id"] == record["run_id"]
assert all(r["outcome"] == "PASS" for r in entries[:6])
assert all(r["outcome"] == "NOT_RUN" for r in entries[7:])
print(json.dumps({
    "record_valid": True,
    "directly_observed": 4,
    "required": 4,
    "attachment_only_live_observed": True,
    "outcome": "PASS",
    "screenshots_sha256_verified": 4,
    "prior_L01_through_L06_preserved": True,
    "later_L08_through_L15_unchanged": True
}, indent=2))
