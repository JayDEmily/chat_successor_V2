# M03 — synthetic proof candidate and fresh-checkout verification

22 November 2026 AEDT. **WORKER_TESTED; INDEPENDENT REVIEW PENDING.** Exact candidate [80688e4620cbddb4b53317ee7dd48434a9c8dd6b](https://github.com/JayDEmily/chat_successor_V2/commit/80688e4620cbddb4b53317ee7dd48434a9c8dd6b); direct parent [9bf311a21a5e7d64b7f2be58b37ffd8294d78c7e](https://github.com/JayDEmily/chat_successor_V2/commit/9bf311a21a5e7d64b7f2be58b37ffd8294d78c7e) is the frozen M02 contract. Branch work/mcp-native-succession-20261122.

## Implementation scope

Two new files only: integration/mcp_native_poc.py (Git blob 066f6b2c2f0d344167032ac5680e6f60d875f788, 25,470 bytes) and integration/tests/test_mcp_native_poc.py (blob 38ee5f75bc97bfed901b59c6d5aa380ffd96d32a, 23,127 bytes). Existing reference Controller imports unchanged, sole decision engine. Two explicit local mock tool handlers register_worker and report_worker, strict body fields and separately injected scoped Auth; one-use challenge/prompt digests and independent injected Delivery/Quiet/Remote observations. Per-run serialized writer (POSIX flock plus in-instance RLock), checksummed atomically replaced snapshot containing core/evidence together, finite synthetic total action budget in addition to unique-chat cap, hold on uncertain restoration and write failure. Actual sender, native UI observation, real OAuth/tunnel/MCP server, external Git reader, production installation and owner re-entry are not implemented. The harness has no network/browser/service calls. Remote evidence is mock, not live Git readback. No new architecture replaces the existing core. A real authenticated context or independently established session-to-saved-chat mapping must not be inferred from these injected objects.

## Verification

Implemented in new isolated Ubuntu sparse checkout of exact parent; no original checkout or service touched. Local commit failed because this fresh WSL clone had no configured author identity; global Git configuration remained unchanged. Read exact staged source bytes through Desktop Commander and created GitHub blobs through the authenticated repository connector; both remote blob hashes matched staged Git index hashes. Created two-file commit with exact parent and branch update using expected-head lease. GitHub commit comparison confirms only these two additions. Independently cloned remote into a second disposable Ubuntu directory, detached at 80688e4620cbddb4b53317ee7dd48434a9c8dd6b, clean initial status, and checked both blob hashes. Fresh checkout Python 3.14.4:

| Check | Result |
| --- | --- |
| git diff --check parent HEAD | exit 0 |
| python3 -B integration/tests/test_mcp_native_poc.py | 21/21 PASS, exit 0 |
| python3 -B astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/run_offline.py --out new-temp-directory | 119/119 PASS, exit 0 |
| Supplemental worker-authored separate stress probe on fresh checkout | exit 0; 31 same-chat reservations and restart/reconciliations, distinct report anchors, count one, action budget hold |

Initial suite 16/16; expanded to 19/19 with actual abrupt child-process exit, failed ledger write and finite action budget probes; final 21/21 adds eight concurrent duplicate reports (one received, seven duplicates, one consumed action) and duplicate reservation preservation at the budget limit. Intermediate whitespace check flagged trailing blank lines; trimmed before commit and verified clean on fresh source. All frozen S01–S13 represented. Reference 119 tests include original controller, fixture and local Git model tests. No hosted CI, full legacy integration, or live acceptance claimed here; M06 retains full applicable regression requirements.

Supplemental stress probe (fresh synthetic data; run from candidate checkout with PYTHONPATH=integration or add integration to sys.path):

```python
from pathlib import Path
import tempfile
from mcp_native_poc import *
route = Route('stress-run','stress-principal','stress-account','stress-project',
              'example/stress','work/stress','0'*40,1,31)
a = Auth(route.principal,route.run_id,route.account_key,'stress-session','stress-subject')
cid = '33333333-3333-3333-3333-333333333333'
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp)/'run'
    p = Proof(path,route,clock=lambda:100.0)
    ids, anchors, prior = set(), set(), None
    for turn in range(31):
        d = p.reserve()
        assert d.action_id not in ids
        ids.add(d.action_id)
        q = None if prior is None else Quiet(route.run_id,prior,cid,True)
        t = Preflight(route.account_key,route.project_id,None if turn==0 else cid,True,True,q)
        assert p.begin_attempt(d,t)==Action.WAIT
        p.close()
        p = Proof(path,clock=lambda:100.0)
        assert p.active['phase']=='uncertain'
        try:
            p.begin_attempt(d,t)
        except Rejected:
            pass
        else:
            raise AssertionError('blind retry')
        p.register_worker(dict(schema_version=1,run_id=route.run_id,action_id=d.action_id,
                               challenge=d.challenge),a)
        assert p.admit_delivery(Delivery(route.run_id,d.action_id,route.account_key,
                route.project_id,cid,digest(d.prompt),a.principal,a.session,a.subject,True))==Action.WAIT
        assert p.count==1
        body=dict(schema_version=1,run_id=route.run_id,action_id=d.action_id,
                  status='NEED_MORE_TIME',publication_sha=None,publication_branch=None)
        assert p.report_worker(body,a)=='received'
        assert p.report_worker(body,a)=='duplicate'
        assert p.evaluate(Quiet(route.run_id,d.action_id,cid,True))==Action.CONTINUE_CURRENT
        anchor=tuple(p.core.state.consumed_responses[-1])
        assert anchor not in anchors
        anchors.add(anchor)
        assert p.evaluate(Quiet(route.run_id,d.action_id,cid,True))==Action.IGNORE
        prior=d.action_id
    try:
        p.reserve()
    except Rejected:
        assert p.data['hold']=='action_budget' and p.count==1
    else:
        raise AssertionError('action budget bypass')
    assert len(p.data['history'])==30 and len(ids)==len(anchors)==31
    p.close()
```

This separate stress trace uses graceful close with in-flight state; the actual abrupt process-exit cases are in the checked-in suite. Fresh-checkout readback, regression and worker-authored additional stress are direct verification, **not** a genuinely separate reviewer verdict. [Issue #2](https://github.com/JayDEmily/chat_successor_V2/issues/2) is the queued independent assignment, pinned to exact candidate; no reviewer conversation launched or acknowledgement yet. Do not mark independent acceptance or use the candidate live until the applicable gate is met.

## Remaining boundaries and next action

- Independently review exact candidate via issue #2; repair, re-pin and re-review if required. No automated dispatch of a reviewer chat is assumed available within M03 no-Send scope.
- M04 needs separately scoped owner authority for one dedicated private loopback MCP service, separate local fixture/audit store, tunnel and private plugin, scoped credentials/auth and bounded native calls. No LTM resources reused. Propose a maximum of eight native calls, up to two isolated saved chats and no automated successors, with exact case freeze and actual quota enforcement before any live invocation. Test registration/report, same-chat duplicate, distinct-session replay, reconnect and independent synthetic Git publication check. Use public synthetic IDs only; never publish native session/subject values or private route receipts. A live public Git worker-attribution alias/private saved-ID mapping must be resolved before actual live handover. M04 transport-only qualification cannot establish M05 native saved receipt or launch.
- Actual desktop account/Project and saved-chat mapping, genuine composer empty/no attachment proof, quiescence and native Send/readback remain open. No new tunnel, plugin, credential or native Send authorised by this evidence; no merge/deploy. Legacy L12, original implementation and LTM-RAG untouched.
