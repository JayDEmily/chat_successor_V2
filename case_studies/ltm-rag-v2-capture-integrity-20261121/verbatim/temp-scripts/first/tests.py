from __future__ import annotations
import hashlib, json, sqlite3, sys, tempfile, threading, concurrent.futures
from pathlib import Path
sys.path.insert(0, "/tmp/ltmragv2_review_fresh_7d8b/vnext")
from ltm_vnext.capture_foundation_v import SyntheticCaptureLedger, CaptureBoundaryError, CaptureConflict

def receipt(n):
    return dict(synthetic_only=True, source_id="synthetic-capture-review", conversation_id="fictional-review", branch_id="main", message_id=f"ind-{n}", version_id="1", position=n, author_role="user", source_locator=f"synthetic-capture://review/{n}", capture_method="synthetic_ui_observation", exact_text=f"Private-ish fictional ✓\nquote — {n}", message_sent_at=None, observed_at=None)
def make(n=1):
    temp=tempfile.TemporaryDirectory(prefix="review-database-")
    path=Path(temp.name)/"ledger.sqlite"
    ledger=SyntheticCaptureLedger.initialise(path)
    ledger.ingest([receipt(n)])
    with sqlite3.connect(path) as db:
        local_id=db.execute("SELECT local_id FROM originals").fetchone()[0]
    return temp,path,ledger,local_id
def db_row(path):
    with sqlite3.connect(path) as db:
        return db.execute("SELECT state, provider_file_id FROM index_outbox").fetchone()
def mutate(path, table, field, value):
    with sqlite3.connect(path) as db:
        db.execute(f"UPDATE {table} SET {field}=?",(value,))
def expect_conflict(f, expected, message):
    try:
        f()
    except CaptureConflict as error:
        assert expected not in str(error), f"LEAK: {error!s}"
        return
    raise AssertionError(message)

results=[]
def run(label, function):
    try:
        function()
        results.append((label,"PASS"))
    except Exception as e:
        results.append((label,"FAIL:"+type(e).__name__+":"+str(e)))

def initial_unicode():
    t,p,l,i=make()
    try:
        ticket=l.reserve_index(i)
        payload=json.loads(ticket["payload"])
        assert payload["exact_text"]==receipt(1)["exact_text"]
        assert payload["author_role"]=="user"
        assert hashlib.sha256(ticket["payload"]).hexdigest()==ticket["payload_sha256"]
        l.acknowledge_index(i,ticket["payload_sha256"],"provider-reviewed")
        l.acknowledge_index(i,ticket["payload_sha256"],"provider-reviewed")
        assert db_row(p)==("SEARCHABLE","provider-reviewed")
    finally:t.cleanup()
run("independent_unicode_and_idempotence",initial_unicode)

for field,table,value in (("exact_text","originals","invented altered source"),("author_role","originals","assistant"),("content_sha256","originals","f"*64),("payload_sha256","index_outbox","c"*64)):
    def reservation(field=field,table=table,value=value):
        t,p,l,i=make()
        try:
            mutate(p,table,field,value)
            expect_conflict(lambda:l.reserve_index(i),receipt(1)["exact_text"],"corrupted reserve accepted")
            assert db_row(p)==("PENDING",None)
            with sqlite3.connect(p) as db:
                assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
        finally:t.cleanup()
    run("reserve_reject_"+field,reservation)
    def acknowledgment(field=field,table=table,value=value):
        t,p,l,i=make()
        try:
            ticket=l.reserve_index(i)
            mutate(p,table,field,value)
            expect_conflict(lambda:l.acknowledge_index(i,ticket["payload_sha256"],"provider-reviewed"),receipt(1)["exact_text"],"corrupted ack accepted")
            assert db_row(p)==("IN_FLIGHT",None)
        finally:t.cleanup()
    run("ack_reject_"+field,acknowledgment)

def concurrent_reservations():
    t,p,l,i=make()
    try:
        gate=threading.Barrier(3)
        def attempt():
            gate.wait()
            try:
                return "ticket",l.reserve_index(i)
            except CaptureBoundaryError:
                return "denied",None
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            a=pool.submit(attempt);b=pool.submit(attempt);gate.wait()
            replies=[a.result(timeout=8),b.result(timeout=8)]
        assert sorted(x[0] for x in replies)==["denied","ticket"],replies
        assert db_row(p)==("IN_FLIGHT",None)
    finally:t.cleanup()
run("concurrent_reservation_exactly_one",concurrent_reservations)

def revocation_blocks_ack():
    t,p,l,i=make()
    try:
        ticket=l.reserve_index(i)
        l.revoke(i,"synthetic review revocation")
        try:l.acknowledge_index(i,ticket["payload_sha256"],"provider-reviewed")
        except CaptureBoundaryError:pass
        else:raise AssertionError("revoked record acknowledged")
        assert db_row(p)==("IN_FLIGHT",None)
        assert not l.snapshot("synthetic-capture-review","fictional-review","main")["originals"]
    finally:t.cleanup()
run("revoke_before_ack_denied",revocation_blocks_ack)

def changed_version_should_fail():
    t,p,l,i=make()
    try:
        mutate(p,"originals","version_id","forged-revision")
        try:
            ticket=l.reserve_index(i)
        except CaptureConflict:
            return
        raise AssertionError("G2: forged version_id accepted as reservable original; bytes="+str(len(ticket["payload"])))
    finally:t.cleanup()
run("G2_version_identity_mutation_rejected",changed_version_should_fail)

for name,outcome in results:print(name+","+outcome)
print("TOTAL="+str(len(results))+",PASS="+str(sum(r=="PASS" for _,r in results))+",FAIL="+str(sum(r!="PASS" for _,r in results)))
if any(r!="PASS" for _,r in results):sys.exit(2)
