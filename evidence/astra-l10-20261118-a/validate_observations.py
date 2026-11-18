#!/usr/bin/env python3
"""Verify L10 injected observation records, scope and cumulative sheet."""
from collections import Counter
import csv
import json
from pathlib import Path

here = Path(__file__).resolve().parent
repo = here.parents[1]
data = json.loads((here / "observations.json").read_text(encoding="utf-8"))
record = json.loads((here / "injection_record.json").read_text(encoding="utf-8"))
rows = data["cases"]
assert data["test_id"] == record["test_id"] == "L10"
assert data["run_id"] == record["run_id"] == "astra-l10-20261118-a"
assert data["outcome"] == "PASS_INJECTION_SCOPE" and record["outcome"] == "PASS"
assert data["scenario_type"] == record["scenario_type"] == "SYNTHETIC_ADAPTER_FAULT_INJECTION"
assert len(rows) == data["case_count"] == data["passed"] == record["cases_total"] == record["cases_passed"] == 21
assert len({r["case"] for r in rows}) == 21
counts = Counter(r["action"] for r in rows)
assert counts == {"WAIT": 3, "HOLD": 11, "CONTINUE_CURRENT": 4,
                  "LAUNCH_SUCCESSOR": 2, "STOP_FINISHED": 1}
assert counts == record["outcome_counts"]
assert all(r["result"] == "PASS" and r["source"] == "SYNTHETIC_ADAPTER_FAULT_INJECTION" for r in rows)
assert all(r["browser_prepare_calls"] == 0 and r["browser_send_calls"] == 0 for r in rows)
assert all(r["unique_chats"] == 1 and r["browser_observe_calls"] == 1 for r in rows)
assert data["real_browser_sends"] == 0 and record["actual"]["real_browser_send_calls"] == 0
assert data["ambiguous_response_false_task_complete"] == 0
assert record["actual"]["false_task_complete_from_ambiguous_cases"] == 0
assert not data["semantic_classifier_called"]
assert not data["automatic_semantic_fallback_enabled"]
assert data["semantic_shadow"] == "NOT_RUN_OPTIONAL_NO_CLASSIFIER"
assert record["actual"]["semantic_confusion_matrix"] is None
assert record["actual"]["classifier_false_TASK_COMPLETE"] is None
assert all(r["interpreted_status"] != "TASK_COMPLETE" for r in rows if r["basis"] == "ambiguous")
assert next(r for r in rows if r["case"] == "L09_style_inline_leaf")["action"] == "HOLD"
assert next(r for r in rows if r["case"] == "valid_after_code_example")["action"] == "CONTINUE_CURRENT"
assert next(r for r in rows if r["case"] == "valid_programme_finished")["action"] == "STOP_FINISHED"
with (repo / "evidence/live_test_results_20261118.csv").open(newline="", encoding="utf-8") as f:
    results = list(csv.DictReader(f))
assert len(results) == 15
assert all(r["outcome"] == "PASS" for r in results[:10])
assert all(r["outcome"] == "NOT_RUN" for r in results[10:])
l10 = results[9]
assert l10["run_id"] == data["run_id"] and "SYNTHETIC" in l10["environment"]
assert (l10["actual_unique_chats"], l10["actual_successor_launches"],
        l10["actual_continuations"], l10["work_verified"]) == ("0", "0", "0", "false")
print(json.dumps({"L10_valid": True, "injection_cases_passed": 21,
                  "action_counts": dict(counts), "real_browser_sends": 0,
                  "optional_classifier_shadow": "NOT_RUN",
                  "L01_to_L10": "PASS", "L11_to_L15": "NOT_RUN"}, indent=2))
