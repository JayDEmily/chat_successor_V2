#!/usr/bin/env python3
"""L15 disposable fixture corruption and reference-controller metadata holds.

No live Chrome interaction, successor dispatch, or published fixture mutations.
Synthetic cases do not replace a real worker's substantive validation.
"""
from __future__ import annotations
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

here=Path(__file__).resolve().parent
repo=here.parents[1]
sys.path.insert(0,str(repo/"astra/2026-11-17/unpacked/chat_succession_test_kit_20261117"))
from succession.core import Action, Config, Controller, RepoView, Response

COMPLETE=repo/"succession-tests/astra-l09-20261118-a"
FRESH=repo/"succession-tests/astra-l13-20261118-a"
CFG=Config("g-p-L15-INJECTION","JayDEmily/chat_successor",
           "work/astra-succession-implementation-20261118",3)
CHAT="l15-source-worker"

def verify(path:Path)->tuple[bool,str]:
    result=subprocess.run(
        [sys.executable,str(path/"fixture_tools.py"),"verify","--root",str(path)],
        capture_output=True,text=True,timeout=20)
    return result.returncode==0,(result.stdout if result.returncode==0 else result.stderr).strip()

def fixture_cases()->list[dict]:
    outcomes=[]
    with tempfile.TemporaryDirectory(prefix="astra-l15-complete-") as t:
        dest=Path(t)/"fixture"
        shutil.copytree(COMPLETE,dest)
        ok,detail=verify(dest)
        assert ok and json.loads(detail)["completed_steps"]==2
        results_path=dest/"RESULTS.json"
        original=results_path.read_bytes()
        data=json.loads(original)
        key=next(iter(data[0]["summary"]))
        data[0]["summary"][key]["total"]+=1
        results_path.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
        valid,reason=verify(dest)
        assert not valid and "Incorrect substantive slice result" in reason, reason
        results_path.write_bytes(original)
        restored,check=verify(dest)
        assert restored and results_path.read_bytes()==original
        outcomes.append({
            "case":"corrupt_completed_result_total",
            "source":"DISPOSABLE_LOCAL_COPY_OF_PUBLISHED_COMPLETED_L09_FIXTURE",
            "baseline_valid":True,"corruption_detected_by":"REAL_FIXTURE_VALIDATOR",
            "validator_rejected":True,"diagnostic":"Incorrect substantive slice result",
            "repaired_by":"Restored original bytes",
            "restored_valid":True,
            "published_fixture_changed":False,"browser_send_calls":0,"result":"PASS"})

    with tempfile.TemporaryDirectory(prefix="astra-l15-next-") as t:
        dest=Path(t)/"fixture"
        shutil.copytree(FRESH,dest)
        ok,detail=verify(dest)
        assert ok and json.loads(detail)["completed_steps"]==0
        next_file=dest/"RUN.json"
        original=next_file.read_bytes()
        next_file.unlink()
        valid,reason=verify(dest)
        assert not valid and ("RUN.json" in reason or "No such file" in reason), reason
        next_file.write_bytes(original)
        restored,check=verify(dest)
        assert restored and next_file.read_bytes()==original
        outcomes.append({
            "case":"missing_next_work_input_RUN_json",
            "source":"DISPOSABLE_LOCAL_COPY_OF_PUBLISHED_SEEDED_L13_FIXTURE",
            "baseline_valid":True,
            "corruption_detected_by":"REAL_FIXTURE_VALIDATOR",
            "validator_rejected":True,
            "diagnostic_contains":"RUN.json",
            "repaired_by":"Restored original bytes",
            "restored_valid":True,
            "published_fixture_changed":False,
            "browser_send_calls":0,"result":"PASS"})
    return outcomes

def controller_cases()->list[dict]:
    valid=RepoView(CFG.repo,CFG.branch,CHAT,False,"Next work slice",
                   published=True,readable=True)
    variants=[
        ("stale_last_worker_attribution",
         RepoView(CFG.repo,CFG.branch,"different-worker",False,"Next work slice"),"stale"),
        ("non_boolean_completion_flag",
         RepoView(CFG.repo,CFG.branch,CHAT,"true","Next work slice"),"boolean"),
        ("finished_and_next_task_contradiction",
         RepoView(CFG.repo,CFG.branch,CHAT,True,"Next work slice"),"finished"),
        ("unfinished_without_next_task",
         RepoView(CFG.repo,CFG.branch,CHAT,False,None),"next task"),
        ("unpublished_handover",
         RepoView(CFG.repo,CFG.branch,CHAT,False,"Next work slice",
                  published=False),"publication"),
        ("missing_repository_handover",None,"publication")
    ]
    observations=[]
    for name,bad,needle in variants:
        c=Controller(CFG,CHAT)
        first=Response(CHAT,"synthetic-event-1","CHAT_STATUS: TASK_COMPLETE",
                       project=CFG.project,role="assistant")
        blocked=c.consume(first,bad)
        assert blocked.action==Action.HOLD,name
        assert needle in blocked.reason.lower(),(name,blocked.reason)
        assert c.unique_count==1 and c.state.pending is None,name
        assert c.state.halted is not None
        c.resume_after_owner()
        second=Response(CHAT,"synthetic-event-2","CHAT_STATUS: TASK_COMPLETE",
                        project=CFG.project,role="assistant")
        prepared=c.consume(second,valid)
        assert prepared.action==Action.LAUNCH_SUCCESSOR,name
        assert c.state.pending is not None and c.state.pending.phase=="prepared"
        assert c.unique_count==1
        observations.append({
            "case":name,
            "source":"SYNTHETIC_REPOVIEW_REFERENCE_CONTROLLER",
            "rejected_action":blocked.action.value,
            "hold_reason":blocked.reason,
            "positive_repair":"Explicit owner resume and new response event with valid published RepoView",
            "post_repair_action":prepared.action.value,
            "post_repair_pending_phase":"prepared",
            "actual_browser_send_calls":0,
            "actual_successor_launches":0,
            "unique_chat_count":1,
            "result":"PASS"})
    return observations

def main():
    fixtures=fixture_cases()
    metadata=controller_cases()
    data={
      "test_id":"L15","run_id":"astra-l15-20261118-a",
      "scenario_type":"DISPOSABLE_FIXTURE_CORRUPTION_AND_SYNTHETIC_METADATA_INJECTION",
      "reference_fixture_validators_used":True,
      "real_worker_correctness_proven":False,
      "real_browser_sends":0,
      "real_successor_launches":0,
      "published_workloads_edited":False,
      "fixture_cases":fixtures,
      "metadata_cases":metadata,
      "cases_passed":len(fixtures)+len(metadata),
      "outcome":"PASS_SCOPED_INJECTION_ONLY",
      "limitations":[
        "Fixture corruption occurred only in automatically deleted disposable local copies; no actual bad commit was pushed.",
        "Invalid RepoView observations were injected; no live ChatGPT worker or browser Send was operated.",
        "A terminal marker is not treated as evidence of substantive fixture accuracy; the separate validator rejected corrupt results."
      ]
    }
    (here/"observations.json").write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"cases_passed":data["cases_passed"],
                      "fixture_corruption_detected":2,
                      "invalid_metadata_held":6,
                      "browser_sends":0,"real_successors":0},indent=2))

if __name__=="__main__":
    main()
