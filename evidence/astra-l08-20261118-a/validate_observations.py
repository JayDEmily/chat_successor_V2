#!/usr/bin/env python3
"""Validate recorded L08 preparation-only observations and prior live L06 count evidence."""
import csv
import json
from pathlib import Path
here=Path(__file__).resolve().parent
repo=here.parents[1]
record=json.loads((here/"live_record.json").read_text(encoding="utf-8"))
prior=json.loads((repo/"evidence/astra-l06-20261118-a/live_record.json").read_text(encoding="utf-8"))
assert record["test_id"]=="L08" and record["outcome"]=="PASS"
assert record["controller_used_in_L08"] is False
assert record["unique_chats_created"]==0 and record["successor_launch_count"]==0
assert record["wrong_destination_count"]==0 and record["observed_run_chat_ids"]==[]
before,prepared,after,combined=record["events"]
assert before["foreground_is_nominated_project"] is False
assert before["nominated_project_visible_in_sidebar"] is True
assert before["editor_name"]=="Ask ChatGPT"
assert before["editor_value_length"]==after["editor_value_length"]==12
assert before["editor_value_sha256"]==after["editor_value_sha256"]
assert after["unchanged"] is True and after["unsaved_chat"] is True
assert prepared["operation"]=="Prepare LAUNCH_SUCCESSOR"
assert prepared["project"]==record["project_identity"]
assert "/g/"+record["project_identity"] in prepared["observed_url"]
assert prepared["observed_url"].endswith("/project")
assert prepared["current_chat_id"] is None
assert prepared["editable_text"]=="" and prepared["attachments_present"] is False
assert prepared["no_typed_message"] and prepared["no_sent_message"]
assert after["prepared_project_chat_is_unsaved"] is True
assert after["visible_sidebar_chat_action_controls"]>=1
assert prior["test_id"]=="L06" and prior["outcome"]=="PASS"
assert prior["project_identity"]==record["project_identity"]
assert prior["actual"]["distinct_saved_chats"]==2
assert len(prior["observed_run_chat_ids"])==2
assert combined["L06_live_run_chat_ids"]==prior["observed_run_chat_ids"]
assert combined["L06_run_unique_count"]==2
assert combined["L08_new_saved_chat_count"]==0
with (repo/"evidence/live_test_results_20261118.csv").open(newline="",encoding="utf-8") as f:
 rows=list(csv.DictReader(f))
l08=next(r for r in rows if r["test_id"]=="L08")
assert l08["outcome"]=="PASS" and l08["run_id"]==record["run_id"]
assert all(r["outcome"]=="PASS" for r in rows[:8])
assert all(r["outcome"]=="NOT_RUN" for r in rows[8:])
print(json.dumps({"L08_record_valid":True,"correct_preparation":True,"other_composer_unchanged":True,"no_send":True,"L06_count_reused":2},indent=2))
