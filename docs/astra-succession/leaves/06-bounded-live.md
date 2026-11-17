# Leaf 06 — Prove bounded live routing and recovery

**Entry:** G2. **Output:** the bounded case outcomes in Astra's results sheet. Follow the [owner runbook](../../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/docs/OWNER_RUNBOOK.md), starting with L01. Label adapter fault injections, manual observations and real live outcomes by scenario type. Use Astra's option to combine or reorder cases when their observations are covered.

| Case | Stimulus | Pass condition |
| --- | --- | --- |
| L01 | Two fixture slices, cap ≥3. Publish slice 1 and emit `TASK_COMPLETE`. | One automatic successor in the correct Project, two saved IDs and two validated results on the same branch. Slice 2 publishes programme completion and dispatch stops. |
| L02 | First worker emits `NEED_MORE_TIME` twice during useful preparation, then completes the slice. | Two exact continuation messages in the same saved ID. Neither changes the count. The subsequent published completion permits one successor. |
| L03 | Supply an isolated material blocker and then repair it. | `ERROR` surfaces the blocker with zero automatic posts. Explicit resume after repair preserves count and consumes a new event. |
| L04 | One slice, cap 30, publish completed programme with no next task. | Stop after the first worker with no new chat. |
| L05 | Three slices, cap 2. Continue once in chat 2 before completing its slice. | Same-chat continuation is allowed at cap. Exactly two IDs, slice 3 remains, and no chat-3 creation or Send. |
| L06 | Hold a prepared handover, end the prior chat's work, then run `python tools/repo_fixture.py rotate-probe --root <fixture>` from the kit and push the new value. Resume with the ordinary pointer. | Successor visibly reads the right branch and uses the new repo-only probe in the independently verified result. A stale branch view refreshes or holds. |
| L07 | Observe the empty-with-placeholder, real draft, draft equal to the placeholder and attachment-only composers read-only. | Actual editable content distinguishes empty from drafts, drafts stay intact, ambiguity holds. |
| L08 | Start with another composer active and the nominated Project visible in the sidebar. Initially stop before Send. Exercise the nominated Project with existing chats. | Correct active Project route, no typed or sent message in the wrong composer, no unrelated chat counted. |
| L09 | Interrupt after saving `sending` before click, and after click before acknowledgement. Repeat lost ack for same-chat continuation. Restart and inspect read-only. | Positive delivery is adopted once. Positive before-click evidence permits explicit rearm. Unresolved outcomes stay held. Neither a timeout nor missing sidebar item triggers a retry. |
| L10 | Observe/inject streaming or truncated replies, missing and conflicting markers and code examples. Run the non-sending semantic shadow set if a classifier is being evaluated. | No early or ambiguous Send. A valid marker controls routing. Record shadow labels, reasons, confusion counts and false `TASK_COMPLETE` separately. A classifier without live evidence stays disabled. |
| L11 | Inject test-only publish/tool failure or a disposable branch conflict. | Local-only work or failed publication cannot dispatch a successor. Repair and retest. |
| L12 | Delay observation, lose a test session/tool, pause while idle and while prepared. | No automatic login or Send while held. Show current chat, reason, last status, pending action and elapsed wait if known. Reconcile any click already in flight. |
| L15 | Corrupt fixture output or next input, and separately inject stale attribution, non-boolean or contradictory programme state. | The fixture validator or worker detects bad work and repairs it or reports the blocker. The controller holds invalid metadata without sending. |

Use Astra's fixture validator and observe normal commits/publication for useful work. Record whether a worker authored the result or used the fixture helper. Record assisted handovers as assisted evidence.

**G3 check:** Record L01–L12 before L13 and record L15 in the live results sheet. Apply Astra's acceptance criteria for routing, published work, and holds. Record any skipped L10 classifier shadow portion as untested and keep automatic fallback disabled.
