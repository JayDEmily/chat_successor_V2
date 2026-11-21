from independent_g2g5_review import IndependentG2G5
from ltm_vnext.capture_foundation_v import CaptureConflict
for n,field,value in [(101,"exact_text","injected replacement"),(102,"author_role","assistant"),(103,"payload_sha256","0"*64)]:
    probe=IndependentG2G5("test_valid_unicode_index_ack_and_snapshot")
    probe.setUp()
    lid,original=probe.make(n)
    probe.mutate(lid,field,value)
    outcome="succeeded"
    try:
        probe.ledger.verify_synthetic(lid,original["exact_text"].encode("utf8"),"independent-source-check")
    except CaptureConflict:
        outcome="rejected"
    orig,outbox=probe.status(lid)
    snapshot_outcome="returned"
    try:
        probe.snapshot()
    except CaptureConflict:
        snapshot_outcome="rejected"
    print(f"{field}: verify={outcome}; source_status={orig[0]}; verification_ref={orig[1]}; snapshot={snapshot_outcome}; outbox={outbox}")
    probe.doCleanups()
