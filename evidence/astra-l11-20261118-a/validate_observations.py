#!/usr/bin/env python3
"""Validate L11 scoped failure-injection and disposable Git evidence."""
import csv
import json
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
repo = here.parents[1]
observed = json.loads((here / "observations.json").read_text(encoding="utf-8"))
record = json.loads((here / "injection_record.json").read_text(encoding="utf-8"))
assert observed["test_id"] == record["test_id"] == "L11"
assert observed["run_id"] == record["run_id"] == "astra-l11-20261118-a"
assert observed["outcome"] == "PASS_TEST_ONLY" and record["outcome"] == "PASS"
assert len(observed["scenarios"]) == 2 and observed["scenarios_passed"] == 2
outage, git_case = observed["scenarios"]
assert outage["result"] == git_case["result"] == "PASS"
assert outage["first_action"] == "HOLD"
assert outage["persisted_hold_survived_restart"] is True
assert outage["response_consumed_during_outage"] is False
assert outage["pending_during_outage"] is None
assert outage["after_repair_action"] == "LAUNCH_SUCCESSOR"
assert outage["pending_after_repair"] == "prepared"
assert outage["browser_send_calls"] == outage["browser_prepare_calls"] == 0
assert git_case["local_only_commit_sha"] != git_case["published_remote_commit_sha"]
assert git_case["published_remote_commit_sha"] == record["pinned_published_commit"]
assert git_case["local_state_programme_complete"] is False
assert git_case["published_state_programme_complete"] is True
assert git_case["reader_used_published_state"] is True
assert git_case["controller_action"] == "STOP_FINISHED"
assert git_case["browser_send_calls"] == git_case["browser_prepare_calls"] == 0
assert git_case["local_commit_pushed"] is False
assert git_case["real_successor_launched"] is False
assert observed["published_repository_modified_by_test"] is False
assert record["actual"]["real_browser_sends"] == 0
assert record["actual"]["real_successor_launches"] == 0
assert record["acceptance"]["overall"] == "PASS_TEST_ONLY"
worktrees = subprocess.run(["git", "-C", str(repo), "worktree", "list", "--porcelain"],
                          check=True, capture_output=True, text=True).stdout
assert "astra-l11-unpushed-" not in worktrees
with (repo / "evidence/live_test_results_20261118.csv").open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 15
assert all(row["outcome"] == "PASS" for row in rows[:11])
assert all(row["outcome"] == "NOT_RUN" for row in rows[11:])
row = rows[10]
assert row["run_id"] == observed["run_id"] and "INJECTION" in row["environment"]
assert (row["actual_unique_chats"], row["actual_successor_launches"],
        row["actual_continuations"]) == ("0", "0", "0")
print(json.dumps({"L11_valid": True, "scenarios_passed": 2,
                  "local_only_commit_not_published": True,
                  "injected_outage_held_and_repaired": True,
                  "browser_send_calls": 0,
                  "L01_to_L11": "PASS", "L12_to_L15": "NOT_RUN"}, indent=2))
