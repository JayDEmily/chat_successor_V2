# A2-L05 — Retain scoped approval and published handoff

**Prerequisite:** L02–L04. **Gate:** A2-G1 exit. **Checks:** A2-S01–S03, A2-O01–O05.

## Expected outcome

Natural owner input reaches the one saved worker only for the identified scope; publication, not a chat's assertion, controls handoff. The core three-status/count/branch behavior remains unchanged.

## Work

Reuse `owner_reentry` and the one worker-instruction builder. Keep immutable private owner context, logical request deduplication, worker/hold-response anchoring and exact posted-turn verification. Clearly distinguish “controller delivered this approval” from “worker advanced; observer resumed.” If the latter does not establish the input's authority, inspect the actual conversation/project record or ask a focused question; do not invent an approval receipt.

Retain current-worker/run Git trailers and authorized branch locator handling. Persist checkpoint adoption, consumed response and next action together. Add publication SHA/ref and comparison outcome to private acceptance diagnostics without adding another publication protocol.

## Exact checks

| Case | Required outcome |
| --- | --- |
| S01 | Completed current assistant only; quoted/tool/user/streaming/conflicting statuses cannot dispatch. `NEED_MORE_TIME` continues same chat at cap. Verified `FINISHED` stops even when count equals cap; eligible work at cap produces `STOP_CAP`. |
| S02 | Wrong run/chat/repo, missing/duplicate trailers, unpublished local changes, missing branch/fetch error or explicit hold: no successor. Preserve the unconsumed response for a valid repaired receipt; no branch adoption on failure. |
| S03 | Current saved worker's authorized branch marker and fetched receipt rotate effective checkpoint once, preserving entry branch, run/count/cap through restart. Bad/ambiguous marker holds. |
| O01 | Inspect precedes start/new/resume. Known pre-Send configured failure can reuse its run; uncertain first Send cannot. Request chat never counts. |
| O02 | Held worker + correct scope/anchor + empty composer: one same-chat input, count unchanged; first receipt verified before successor. |
| O03 | Replay same ID from a different request file, identical decision under another ID for the same hold, and conflicting content/scope: deduplicate identical; reject conflict; no second edit/Send. |
| O04 | Input already delivered or worker has advanced: no repeat input. Positive exact input evidence supports delivery; unrelated advancement supports only observation/reconciliation, not a fabricated approval receipt. |
| O05 | Stale/wrong worker anchor, multiple possible scopes, independent review requirement, unauthorized branch/write route or unverified private context: hold/clarify; worker follows project rules. |

## Evidence

Run both old suites plus new tests; retain case-to-assertion mapping and raw logs. Use small local Git fixtures to verify changed file, exact lines, parent and three trailers. Do not claim a generic trailer parser validates engineering work in Rowing/SolidWorks. Existing 182 tests are a baseline; report the actual expanded total rather than invent a target count.

## Hold / failure

Preserve owner inputs and pending actions. Never create a new worker to bypass an approval boundary, increase a cap to make a test complete, or accept a locally staged commit as publication. An uncertain existing action takes priority over a new owner decision.

Sources: S02/S03/S10/S11/S13; S07/V06 for earlier approval/rotation artifacts.
