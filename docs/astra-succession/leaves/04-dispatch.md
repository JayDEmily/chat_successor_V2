# Leaf 04 — Connect dispatch, state and recovery

**Entry:** Leaves 01–03. **Output:** one controller loop with Astra's dispatch and recovery ordering.

1. Follow the [dispatch ordering](../../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/docs/PROTOCOL_AND_ADAPTER.md#dispatch-ordering-pseudocode-not-executable-browser-integration). Observe the turn, read repository state if needed, consume the response and save the decision. Prepare the destination; hold on an unresolved target or draft. Call `begin_send`, save `sending`, then Send once. Confirm a posted message in the observed saved chat or hold for reconciliation. Save the result.
2. Use Astra's single-writer state and recovery methods. On restart, reconcile an attempted Send read-only. Adopt observed delivery once, rearm explicitly only with positive evidence of no submission, and keep unresolved or lost state held. Preserve the existing chat count.
3. Expose the simple progress, pause/resume and error output from Astra's contract. Serialize owner stop with the next Send. An already in-flight click is reconciled by the same recovery procedure.

**G1 check:** Walk the wiring against Astra's adapter contract and use the existing S01–S16 replays and controller recovery cases for offline verification. For a reference rerun, use `python -X utf8 run_offline.py --out <temporary-report-dir>` from the kit root. Live ordering and recovery evidence come from L01, L09 and L12. Advance to Leaf 05.
