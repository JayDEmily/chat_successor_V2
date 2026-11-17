# Leaf 06 — Prove bounded live routing and recovery

**Entry:** G2 and the assigned bounded live run. **Output:** per-case receipts and a filled copy of Astra's live results sheet. Follow [the owner runbook](../../../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/docs/OWNER_RUNBOOK.md), starting with L01. Use fresh run records for variants and preserve unresolved attempts. Label adapter fault injections, manual observations and real live outcomes by scenario type.

| Case | Stimulus | Pass condition |
| --- | --- | --- |
| L01 | Two fixture slices, cap ≥3. Publish slice 1 and emit `TASK_COMPLETE`. | One automatic successor in the correct Project, two saved IDs and two validated results on the same branch. Slice 2 publishes programme completion and dispatch stops. |
| L02 | First worker emits `NEED_MORE_TIME` twice during useful preparation, then completes the slice. | Two exact continuation messages in the same saved ID. Neither changes the count. The subsequent published completion permits one successor. |
| L03 | Supply an isolated material blocker and then repair it. | `ERROR` surfaces the blocker with zero automatic posts. Explicit resume after repair preserves count and consumes a new event. |
| L04 | One slice, cap 30, publish completed programme with no next task. | Stop after the first worker with no new chat. |
| L05 | Three slices, cap 2. Continue once in chat 2 before completing its slice. | Same-chat continuation is allowed at cap. Exactly two IDs, slice 3 remains, and no chat-3 creation or Send. |
| L06 | Hold a prepared handover, end the prior chat's work, then run `python tools/repo_fixture.py rotate-probe --root <fixture>` from the kit and push the new value. Resume with the ordinary pointer. | Successor visibly reads the right branch and uses the new repo-only probe in the independently verified result. A stale branch view refreshes or holds. |
| L07 / L08 | Use the read-only observations from Leaf 05. | Correct editor classification, preserved drafts, correct active Project route, no unrelated chat counted. |
| L09 | Interrupt after saving `sending` before click, and after click before acknowledgement. Repeat lost ack for same-chat continuation. Restart and inspect read-only. | Positive delivery is adopted once. Positive before-click evidence permits explicit rearm. Unresolved outcomes stay held. Neither a timeout nor missing sidebar item triggers a retry. |
| L10 | Observe/inject streaming, missing and conflicting markers and code examples. Run the non-sending semantic shadow set if a classifier is being evaluated. | No early or ambiguous Send. A valid marker controls routing. Record shadow labels, reasons, confusion counts and false `TASK_COMPLETE` separately. A classifier without live evidence stays disabled. |
| L11 | Inject test-only publish/tool failure or a disposable branch conflict. | Local-only work or failed publication cannot dispatch a successor. Repair and retest with real remote readback. |
| L12 | Delay observation, lose a test session/tool, pause while idle and while prepared. | No automatic login or Send while held. Show current chat, reason, last status, pending action and elapsed wait if known. Reconcile any click already in flight. |
| L15 | Corrupt fixture output or next input, and separately inject stale attribution, non-boolean or contradictory programme state. | The fixture validator or worker detects bad work and repairs it or reports the blocker. The controller holds invalid metadata without sending. |

From the kit directory run `python tools/repo_fixture.py verify --root <fixture>` after each claimed useful slice. Independently read its result from the nominated remote branch. Record whether a worker authored the result or used the fixture helper. Record any assisted handover as assisted evidence.

**G3 check:** Archive reports and redacted receipts for L01–L12 and L15. For the bounded live claim, require correct Project, useful published work, unique counts, and zero wrong-destination posts, duplicates or prohibited sends. A deliberate failure case passes when it produces the expected hold and recovery. Preserve the first missing boundary for run failures. If L10's semantic shadow portion was skipped, record it as untested and keep automatic fallback disabled. Advance to L13 when the deterministic L10 acceptance and the other bounded cases are evidenced.
