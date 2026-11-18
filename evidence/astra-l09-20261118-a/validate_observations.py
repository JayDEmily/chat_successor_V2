#!/usr/bin/env python3
"""Validate L09's published fixture and recorded owner-assisted live observations.

This validates file consistency; private live controller assertions come from
the recorded external-operator readbacks, not from an offline simulation.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
import subprocess
import sys

here = Path(__file__).resolve().parent
repo = here.parents[1]
fixture = repo / "succession-tests/astra-l09-20261118-a"
record = json.loads((here / "live_record.json").read_text(encoding="utf-8"))
recovery = json.loads((here / "operator_recovery_result.json").read_text(encoding="utf-8"))
run = json.loads((fixture / "RUN.json").read_text(encoding="utf-8"))
state = json.loads((fixture / "STATE.json").read_text(encoding="utf-8"))
results = json.loads((fixture / "RESULTS.json").read_text(encoding="utf-8"))

assert record["test_id"] == "L09" and record["outcome"] == "PASS"
assert record["scenario_type"] == "OWNER_ASSISTED_LIVE_FAULT_INJECTION"
assert record["run_id"] == run["run_id"] == state["run_id"] == recovery["run_id"]
assert state["completed_steps"] == len(run["steps"]) == len(results) == 2
assert state["programme_complete"] is True and state["next_task"] is None
assert state["last_chat_id"] == record["worker_chat_ids"][-1]
assert [r["chat_id"] for r in results] == record["worker_chat_ids"]
assert [r["step"] for r in results] == [1, 2]
assert [r["probe_nonce"] for r in results] == [s["probe_nonce"] for s in run["steps"]]
assert record["events"][-1]["action"] == "STOP_FINISHED"
assert record["events"][-1]["unique_chat_count"] == 2
assert record["events"][-1]["pending_action"] is None
assert record["events"][-1]["halted"] == "programme_finished"
assert record["events"][-2]["published_commit"] == "eedd2038278ff2371bd02d3571836c8a853b8b4e"
assert record["actual"]["unique_saved_chats"] == 2
assert record["actual"]["successor_launches"] == 1
assert record["actual"]["controller_continuations"] == 2
assert record["actual"]["owner_corrective_messages"] == 1
assert record["actual"]["duplicate_sends"] == 0
assert record["actual"]["fixture_valid"] is True
assert recovery["overall_l09"] == "PASS_ASSISTED"
assert recovery["terminal_fixture"]["controller_terminal_action"] == "STOP_FINISHED"
assert recovery["terminal_fixture"]["published_commit"] == record["events"][-2]["published_commit"]
assert recovery["terminal_fixture"]["controller_unique_chat_count"] == 2
assert record["acceptance"]["overall"] == "PASS_ASSISTED"
assert all(v is True for k, v in record["acceptance"].items() if k != "overall")

total_rows = sum(len(step["rows"]) for step in run["steps"])
total_value = sum(row["value"] for step in run["steps"] for row in step["rows"])
assert (total_rows, total_value) == (12, 149)
assert record["actual"]["result_rows"] == total_rows
assert record["actual"]["aggregate_value_total"] == total_value

with (repo / "evidence/live_test_results_20261118.csv").open(
        encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 15
assert [r["test_id"] for r in rows] == [f"L{i:02d}" for i in range(1, 16)]
assert all(r["outcome"] == "PASS" for r in rows[:9])
assert all(r["outcome"] == "NOT_RUN" for r in rows[9:])
l09 = rows[8]
assert l09["run_id"] == record["run_id"]
assert (l09["actual_unique_chats"], l09["actual_successor_launches"],
        l09["actual_continuations"], l09["work_verified"]) == ("2", "1", "2", "true")

result = subprocess.run([sys.executable, str(fixture / "fixture_tools.py"), "verify",
                         "--root", str(fixture)], check=True, text=True,
                        capture_output=True)
assert json.loads(result.stdout)["fixture_valid"] is True
print(json.dumps({
    "L09_record_valid": True,
    "outcome": "PASS_ASSISTED",
    "fixture_valid": True,
    "completed_steps": 2,
    "unique_chats": 2,
    "controller_continuations": 2,
    "terminal_stop_observed": True,
    "L01_to_L09": "PASS",
    "L10_to_L15": "NOT_RUN",
}, indent=2))
