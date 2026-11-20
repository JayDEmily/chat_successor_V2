# ADR 0002 — Project execution and acceptance

**Execution branch:** `codex/chat-succession-finish`; keep `main` unchanged. **Baseline source:** `283e6c17bf3359c203a362fd6593563480eeea5f`; runtime/plugin candidate `2c29406b1c43904c5ead79064fe7856971e0aa2e` (0.4.3); Astra intake `b3daeda63643b9ad8d8860fb5cc99a3e4ef400c7`.

The owner has accepted the [bounded ADR 0002 implementation](../../adr/0002-account-bound-resumable-runs.md) with a standing grant on 20 November 2026. [The original ten leaves](../../../evidence/astra-adr-0002-20261120/package/docs/IMPLEMENTATION_PLAN.md) and [A2 acceptance gates](../../../evidence/astra-adr-0002-20261120/package/acceptance/GATES.md) remain the operative procedure, not this status summary.

| Gate | Current disposition | Evidence and next action |
| --- | --- | --- |
| A2-G0 / L01 | **PASS — offline evidence and scoped authority** | [Fresh baseline](../../../evidence/astra-adr-0002-20261120/implementation/G0_20261120/BASELINE.md); continue A2-L02 |
| A2-G1 / L02–L05 | **IN PROGRESS — L02 and L03 offline candidates PASS; L04–L05 NOT_RUN** | [L02](../../../evidence/astra-adr-0002-20261120/implementation/L02_20261120/L02_RESULT.md) and [L03](../../../evidence/astra-adr-0002-20261120/implementation/L03_20261120/L03_RESULT.md): 91/91 integration after independent L02 negative fixes, native PowerShell mock and 119/119 unchanged reference; continue L04 before G1 exit |
| A2-G2 / L06 | **NOT_RUN** | Windows installation/account route verification after G1 |
| A2-G3 / L07 | **NOT_RUN** | Two independent disposable mock Projects/repos, proven stale recovery |
| A2-G4 / L08 | **NOT_RUN** | Actual Shoco iPhone approval and account re-entry |
| A2-G5 / L09 | **NOT_RUN** | Measured resource/concurrency capacity; budget/thresholds frozen before test |
| A2-G6 / L10 | **NOT_RUN** | Independent closeout, release matrix and verified start/pause/resume/check |

## L02 negative-review follow-up

[Three negative contract gaps and targeted correction](../../../evidence/astra-adr-0002-20261120/implementation/L02_20261120/review_20261120/NEGATIVE_REVIEW.md) were reproduced after the original 79-test candidate. Post-repair offline suites: 82 integration and 119 reference PASS; independent final acceptance and installation remain open. No change to A2-G1 or A2-G2 NOT_RUN dispositions.

## Management commitments

Keep a single approved development branch rather than one branch per leaf. Commit exact leaf evidence and source as distinct reviewable checkpoints. Apply independent review at appropriate gates. Capture candidate SHA, test runs, raw outputs, observed Windows readbacks, run/fixture IDs, pending actions and real limitations. Do not substitute a model's claim or offline proxy for actual Windows acceptance. Confirm all remote pushes and final Git readbacks.

**Pre-existing pause holds:** Shoco Project A Test / Rowing run `b401f984a1927f6979067d07`, two workers of cap two; Project B Test / SolidWorks `271867d56ebd3443a4b40fa6`, one worker of cap two. Both remain owner-paused; this ADR grant does not automatically release them. Their journals are private and must not be copied into Git.

**Candidate 0.4.3 is not an ADR 0002 pass.** Every future implementation creates a new pinned candidate identity, and every Windows/iPhone result must be matched to the exact installed candidate and account.

## Owner-authorised mock isolation — 20 November

The owner instructed that ADR 0002 live acceptance must NOT use the real
`rowing2026` or `sw_v1` repositories/ongoing Projects. This replaces
Astra's illustrative Rowing/SolidWorks G3 trial targets without weakening
its acceptance predicates.

- Use isolated ChatGPT mock Projects and disposable GitHub repository branches
  for A2-G3/G4. Existing Cat/Dog, Bird/Pig and approval fixtures remain eligible,
  after checking present controller state and fixture isolation.
- Dedicated private `JayDEmily/rowing-clone-test` was created from an exact
  tracked-tree snapshot of `rowing2026` main at
  `5b04bd24c8308759dd70e3274fe259439c696e48`, under `snapshot/`,
  with an independent mock-worker assignment at the root. It is a
  realistic-sized fixture, not an active Rowing derivative. Remote snapshot is READY: published `main@f2c28775532bc3f828af95edd6c61258f6313496`, with exact Git tree equality `31e770b057f5c9ac8d610c0aed5ad2f24db1c144`; GitHub API readback verified the private fixture provenance and root agent instructions.
- Do not share one repository branch between concurrently active test runs.
  Each trial requires a fresh fixture branch and specific signed-in ChatGPT
  Project that is not associated with a live engineering workload.
- Both original Shoco Rowing and SolidWorks runs remain paused, unchanged.
  Closeout Q02 records their held status, but no automatic restart is
  authorised for them.
- Fresh projects may be created as needed for the agreed mock scope. Keep names
  explicit and stable, and verify the signed-in account and Project ID before
  any new controller Send.
