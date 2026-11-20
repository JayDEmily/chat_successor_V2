# ADR 0002 — Project execution and acceptance

**Execution branch:** `codex/chat-succession-finish`; keep `main` unchanged. **Baseline source:** `283e6c17bf3359c203a362fd6593563480eeea5f`; runtime/plugin candidate `2c29406b1c43904c5ead79064fe7856971e0aa2e` (0.4.3); Astra intake `b3daeda63643b9ad8d8860fb5cc99a3e4ef400c7`.

The owner has accepted the [bounded ADR 0002 implementation](../../adr/0002-account-bound-resumable-runs.md) with a standing grant on 20 November 2026. [The original ten leaves](../../../evidence/astra-adr-0002-20261120/package/docs/IMPLEMENTATION_PLAN.md) and [A2 acceptance gates](../../../evidence/astra-adr-0002-20261120/package/acceptance/GATES.md) remain the operative procedure, not this status summary.

| Gate | Current disposition | Evidence and next action |
| --- | --- | --- |
| A2-G0 / L01 | **PASS — offline evidence and scoped authority** | [Fresh baseline](../../../evidence/astra-adr-0002-20261120/implementation/G0_20261120/BASELINE.md); continue A2-L02 |
| A2-G1 / L02–L05 | **NOT_RUN** | Implement minimal code deltas; exact R/S/V/O regression matrix and previous suites |
| A2-G2 / L06 | **NOT_RUN** | Windows installation/account route verification after G1 |
| A2-G3 / L07 | **NOT_RUN** | Two independent bounded live fixtures, proven stale recovery |
| A2-G4 / L08 | **NOT_RUN** | Actual Shoco iPhone approval and account re-entry |
| A2-G5 / L09 | **NOT_RUN** | Measured resource/concurrency capacity; budget/thresholds frozen before test |
| A2-G6 / L10 | **NOT_RUN** | Independent closeout, release matrix and verified start/pause/resume/check |

## Management commitments

Keep a single approved development branch rather than one branch per leaf. Commit exact leaf evidence and source as distinct reviewable checkpoints. Apply independent review at appropriate gates. Capture candidate SHA, test runs, raw outputs, observed Windows readbacks, run/fixture IDs, pending actions and real limitations. Do not substitute a model's claim or offline proxy for actual Windows acceptance. Confirm all remote pushes and final Git readbacks.

**Pre-existing pause holds:** Shoco Project A Test / Rowing run `b401f984a1927f6979067d07`, two workers of cap two; Project B Test / SolidWorks `271867d56ebd3443a4b40fa6`, one worker of cap two. Both remain owner-paused; this ADR grant does not automatically release them. Their journals are private and must not be copied into Git.

**Candidate 0.4.3 is not an ADR 0002 pass.** Every future implementation creates a new pinned candidate identity, and every Windows/iPhone result must be matched to the exact installed candidate and account.
