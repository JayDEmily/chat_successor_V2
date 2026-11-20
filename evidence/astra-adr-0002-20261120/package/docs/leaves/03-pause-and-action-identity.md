# A2-L03 — Preserve pause and exact action identity

**Prerequisite:** L02. **Gate:** part of A2-G1. **Checks:** A2-S04–S09. **Touch only:** existing dispatch, private target records, bootstrap/reconciliation and pause seams.

## Expected outcome

One persisted action is attempted at most once automatically, is adopted at most once, and remains recoverable across pause/restart. An old target record cannot be reused just because handle/source/kind match. Pause is persistent and visible, not merely a killed observer process.

## Smallest implementation

- Carry the matching action ID and route through all target writes and Send/reconcile checks, including same-chat continuation. Match exact source response, message and destination; keep core `prepared → sending → confirmed/uncertain`.
- Preserve bootstrap's separate durable initial intent. Bind its route/request identity without introducing another automatic sender.
- Retain final pause checks before typing/click, atomic state writes and generation-aware pause release. Report in-flight uncertainty separately from pause acknowledgement.
- Never clear an uncertain action through ordinary resume. Adoption is read-only; explicit rearm requires positive no-submission evidence and retains the action ID.
- Legacy target/action records missing new binding data hold for positive reconciliation; no silent reset. Never overwrite terminal cap/finish with a resumable error.

## Exact fault matrix

| Case | Injection and expected observation |
| --- | --- |
| S04 | Pause at prepared state, after composer preparation and after typing but before click; restart with marker present. Zero click; same action/count/cap; typed draft untouched. Release does not bypass draft checks. |
| S05 | Same-chat click succeeds but acknowledgement is lost. Restart and reconcile exact posted user turn after the triggering assistant response. Earlier identical “Okay, continue working.” or a post after another response is rejected; one adoption, no extra Send. |
| S06 | Successor click may have occurred; test local-only ID, unknown receipt, missing target view and duplicate acknowledgement. Count remains unchanged until one verified saved successor; unresolved cases hold without another composer/Send. |
| S07 | Crash around initial intent/first Send/worker registration; repeat launch. Exact original intent reconciles, or holds. Prior timing log with missing controller journal never causes fresh bootstrap. |
| S08 | Pause survives observer restart, repeated pause generations race with resume, and finished/capped runs receive pause/resume requests. Newest pause wins; terminal state/count remain unchanged. |
| S09 | Mismatch target action ID, source, route, message, handle/document or destination. No adapter Send invocation. Reverse P08's current acceptance-of-stale-ID characterization into this regression. |

Offline mock evidence is required for every branch. Live fault cases later run only on authorized disposable fixtures and preserve their evidence. Log the action ID, phase transitions, pause request/gate/click/ack times, before/after counts, exact posted-turn anchor and reconcile result; do not log private instruction bodies publicly.

## Hold / failure

Unknown outcome is not positive no-send evidence. Preserve journal/intent/target/draft and stop automatic posting. Do not “recover” by changing a branch, creating a new job or directly invoking the adapter's Send. Failed isolation/duplicate evidence blocks the release; fix the earliest invariant failure before further live trials.

Sources: S10–S12; V07 P01–P05/P08/P09.
