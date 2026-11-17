# Leaf 02 — Read published programme state

**Entry:** Leaf 01. **Output:** a `RepoView` from the ordinary published programme state on the nominated repo and branch.

1. Map the current repo and branch, actual last-worker attribution, programme completion, next task and observed publish/read outcome into `RepoView` as defined in [Astra's adapter contract](../../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/docs/PROTOCOL_AND_ADAPTER.md). Use the fixture's `STATE.json` or the real job's existing progress and next-task record.
2. Use the owner's existing authenticated write route. For an eligible `TASK_COMPLETE`, read the current state once. A failed push, unavailable state, stale attribution or contradictory completion state holds progression. Leave usefulness and correctness to the job's ordinary checks or Astra's fixture validator.

**Leaf check:** Reuse Astra's G01–G08 local Git and F01–F09 fixture evidence, plus C08–C12 for controller decisions. The live write route, cold pickup and failure outcomes are covered by L01, L06, L11 and L15. Advance to Leaf 03.
