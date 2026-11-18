#!/usr/bin/env python3
"""Validate L12 actual local synthetic fault-injection evidence and results ledger."""
from pathlib import Path
import csv
import json

base=Path(__file__).resolve().parent
repo=base.parents[1]
observed=json.loads((base/"observations.json").read_text(encoding="utf-8"))
record=json.loads((base/"injection_record.json").read_text(encoding="utf-8"))
assert observed["test_id"] == record["test_id"] == "L12"
assert observed["run_id"] == record["run_id"] == "astra-l12-20261118-a"
assert observed["outcome"] == "PASS_TEST_INJECTION_SCOPE"
assert record["outcome"] == "PASS"
assert observed["scenario_type"] == record["scenario_type"] == "SYNTHETIC_DELAY_TOOL_LOSS_AND_PAUSE_INJECTION"
cases=observed["cases"]
assert len(cases) == observed["cases_passed"] == record["cases_passed"] == 6
assert observed["cases_failed"] == 0
assert [c["case"] for c in cases] == record["case_names"]
assert len({c["case"] for c in cases}) == 6
for case in cases:
    assert case["source"] == "TEST_ONLY_ADAPTER_AND_STATE_INJECTION"
    assert case["result"] == "PASS" and case["browser_send_calls"] == 0
    assert case["automatic_login_calls"] == 0 and case["real_chat_created"] is False
    s=case["observed_state"]
    assert s["project"] == "g-p-L12-INJECTION"
    assert s["current_chat_id"] == "l12-injected-chat"
    assert s["unique_chat_count"] == 1
assert cases[0]["initial_actions"] == ["WAIT","WAIT"]
assert cases[0]["measured_elapsed_wait_ms"] >= 120
assert cases[0]["no_premature_completion"] is True
assert cases[0]["production_owner_silence_deadline"] == "NOT_CONFIGURED_BY_THIS_TEST"
assert cases[1]["first_action"] == "HOLD" and cases[1]["held_across_restart"] is True
assert cases[1]["no_automatic_login"] is True
assert cases[2]["held_state"]["pending_action"] is None
assert cases[2]["held_state"]["halted"] == "Owner pause while idle"
assert cases[3]["held_state"]["pending_action"]["phase"] == "prepared"
assert cases[3]["held_state"]["halted"] == "Owner pause while prepared"
assert cases[4]["previous_hold"]["pending_action"]["phase"] == "uncertain"
assert cases[4]["receipt_source"] == "SYNTHETIC_POSITIVE_READ_ONLY"
assert cases[4]["after_receipt_action"] == "WAIT"
assert cases[5]["first_action"] == "HOLD" and cases[5]["retained_pending"] == "prepared"
assert observed["real_browser_sends"] == observed["real_browser_login_attempts"] == observed["real_successor_launches"] == 0
assert record["actual"]["real_browser_send_calls"] == record["actual"]["real_login_attempts"] == 0
assert record["actual"]["production_owner_silence_deadline_established"] is False
assert record["acceptance"]["outcome"] == "PASS_TEST_ONLY"
with (repo/"evidence/live_test_results_20261118.csv").open(newline="",encoding="utf-8") as f:
    rows=list(csv.DictReader(f))
assert [r["test_id"] for r in rows]==[f"L{i:02d}" for i in range(1,16)]
assert all(r["outcome"]=="PASS" for r in rows[:12])
assert all(r["outcome"]=="NOT_RUN" for r in rows[12:])
row=rows[11]
assert row["run_id"] == observed["run_id"]
assert "SYNTHETIC" in row["environment"]
assert row["evidence_path"] == "evidence/astra-l12-20261118-a/injection_record.json"
assert (row["actual_unique_chats"],row["actual_successor_launches"],row["actual_continuations"],row["work_verified"]) == ("0","0","0","false")
print(json.dumps({"record_valid":True,"cases_passed":6,"browser_send_calls":0,"login_calls":0,"production_deadline_verified":False,"L01_to_L12":"PASS","L13_to_L15":"NOT_RUN"},indent=2))
