import sys,sqlite3,tempfile
from pathlib import Path
src=Path(sys.argv[1]);sys.path.insert(0,str(src/"vnext"))
from ltm_vnext.capture_foundation_v import SyntheticCaptureLedger,CaptureConflict
from ltm_vnext.archive import _local_id
with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp)/"ledger.sqlite"; ledger=SyntheticCaptureLedger.initialise(path)
    data=dict(synthetic_only=True,source_id="synthetic-capture-review",conversation_id="fictional",branch_id="main",message_id="m1",version_id="v1",position=1,author_role="user",source_locator="synthetic-capture://fictional/m1",capture_method="synthetic_ui_observation",exact_text="Fictional initial version",message_sent_at=None,observed_at=None)
    ledger.ingest([data])
    original=_local_id(data["source_id"],"m1","v1")
    with sqlite3.connect(path) as db: db.execute("UPDATE originals SET version_id='forged-v99'")
    modified=_local_id(data["source_id"],"m1","forged-v99")
    try:
        ticket=ledger.reserve_index(original); verdict="ACCEPTED_FORGED_VERSION"
    except CaptureConflict:
        verdict="REJECTED_FORGED_VERSION"
    snap=ledger.snapshot("synthetic-capture-review","fictional","main")
    print(src.name,"original_id="+original,"recomputed_forged_id="+modified,"original_still_used="+str(original==snap["originals"][0]["local_id"]),"shown_version="+snap["originals"][0]["version_id"],"reservation="+verdict)
