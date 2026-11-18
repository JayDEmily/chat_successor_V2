#!/usr/bin/env python3
"""Validate L15 recorded disposable fixture and synthetic metadata injections."""
from pathlib import Path
import csv,json,subprocess,sys
here=Path(__file__).resolve().parent
repo=here.parents[1]
obs=json.loads((here/"observations.json").read_text(encoding="utf-8"))
record=json.loads((here/"injection_record.json").read_text(encoding="utf-8"))
assert obs["test_id"] == record["test_id"] == "L15"
assert obs["run_id"] == record["run_id"] == "astra-l15-20261118-a"
assert obs["outcome"] == "PASS_SCOPED_INJECTION_ONLY"
assert record["outcome"] == "PASS"
assert obs["scenario_type"] == record["scenario_type"]
assert len(obs["fixture_cases"]) == 2
assert len(obs["metadata_cases"]) == 6
assert obs["cases_passed"] == 8 == record["results"]["cases_passed"]
assert all(c["result"] == "PASS" for c in obs["fixture_cases"]+obs["metadata_cases"])
assert all(c["baseline_valid"] and c["validator_rejected"] and c["restored_valid"]
           and not c["published_fixture_changed"] for c in obs["fixture_cases"])
assert all(c["rejected_action"] == "HOLD"
           and c["post_repair_action"] == "LAUNCH_SUCCESSOR"
           and c["post_repair_pending_phase"] == "prepared"
           and c["actual_browser_send_calls"] == 0
           and c["actual_successor_launches"] == 0
           for c in obs["metadata_cases"])
assert obs["published_workloads_edited"] is False
assert obs["real_worker_correctness_proven"] is False
assert obs["real_browser_sends"] == obs["real_successor_launches"] == 0

for run_id, steps in [("astra-l09-20261118-a",2),
                      ("astra-l13-20261118-a",0),
                      ("astra-l13-20261118-b",0),
                      ("astra-l13-20261118-c",0)]:
    root=repo/"succession-tests"/run_id
    proc=subprocess.run([sys.executable,str(root/"fixture_tools.py"),"verify",
                         "--root",str(root)],capture_output=True,text=True,check=True)
    verified=json.loads(proc.stdout)
    assert verified["fixture_valid"] is True
    assert verified["completed_steps"] == steps

with (repo/"evidence/live_test_results_20261118.csv").open(newline="",encoding="utf-8") as f:
    sheet=list(csv.DictReader(f))
assert len(sheet) == 15
assert all(s["outcome"] == "PASS" for s in sheet[:12])
assert sheet[12]["outcome"] == "BLOCKED"
assert sheet[13]["outcome"] == "NOT_RUN"
assert sheet[14]["outcome"] == "PASS" and sheet[14]["run_id"] == obs["run_id"]
assert "INJECTION" in sheet[14]["environment"]
assert (sheet[14]["actual_unique_chats"],sheet[14]["actual_successor_launches"],
        sheet[14]["actual_continuations"],sheet[14]["work_verified"]) == ("0","0","0","false")
print(json.dumps({"L15_records_valid":True,"cases_passed":8,"fixture_repaired":2,
                  "metadata_held":6,"browser_sends":0,
                  "published_L09_and_L13_fixtures_preserved":True,
                  "L13":"BLOCKED_PREBOOTSTRAP","L14":"NOT_RUN","L15":"PASS_INJECTION_SCOPE"},indent=2))
