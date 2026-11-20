# Ordered implementation leaves

**All implementation below is proposed, not performed in this delivery.** The current output is a review/ADR/acceptance package. Follow the [ADR](adr/0002-account-bound-resumable-runs.md) and preserve the [evidence boundary](../evidence/EVIDENCE_REVIEW.md).

Use one leaf at a time. Do not reopen historical Astra G0–G4, reset a paused run, or replace the established controller because a later acceptance check is still open. Source references resolve in the [source index](../evidence/SOURCE_INDEX.md).

| Order | Leaf | Prerequisite | Expected result | Gate |
| --- | --- | --- | --- | --- |
| 1 | [A2-L01 — Freeze baseline and authority](leaves/01-baseline-and-authority.md) | Archive and owner review | Agreed evidence ledger, preserved pause and bounded scope | A2-G0 |
| 2 | [A2-L02 — Bind account and installation route](leaves/02-account-and-route.md) | A2-G0 | Explicit per-account route; stable run identity; useful read-only status | Part of A2-G1 |
| 3 | [A2-L03 — Preserve pause and exact action identity](leaves/03-pause-and-action-identity.md) | L02 | Same durable action survives pause/restart/uncertainty; mismatched target cannot Send | Part of A2-G1 |
| 4 | [A2-L04 — Qualify saved-view recovery](leaves/04-view-recovery.md) | L03 | Closed/displaced and stale views handled without new worker or unsafe reload | Part of A2-G1 |
| 5 | [A2-L05 — Retain scoped approval and published handoff](leaves/05-approval-and-publication.md) | L02–L04 | Same-worker approval, correct receipt and branch/cap semantics | A2-G1 exit |
| 6 | [A2-L06 — Verify Windows release and both account routes](leaves/06-installation-and-accounts.md) | A2-G1; owner permits installation/preflight | Exact release/backend/profile/root verified, no-Send checks pass | A2-G2 |
| 7 | [A2-L07 — Two overlapping bounded runs and recovery faults](leaves/07-two-run-acceptance.md) | A2-G2; fresh authorized small fixtures | One finish, one eligible-work cap stop; independent pause/restart; positive stale recovery and no duplicate handoff | A2-G3 |
| 8 | [A2-L08 — Shoco iPhone start, approval and account round-trip](leaves/08-phone-and-reentry.md) | A2-G3; account-specific installed plugin | Request chat excluded; approval once to original worker; verified successor/finish; route isolation retained | A2-G4 |
| 9 | [A2-L09 — Measure practical concurrency](leaves/09-capacity.md) | A2-G4; frozen resource/latency budgets | Qualified measured envelope, or an explicit lower bound if no limit reached | A2-G5 |
| 10 | [A2-L10 — Close out without erasing open evidence](leaves/10-closeout.md) | A2-G0–G5 outcomes available | Owner-approved scoped release decision and four-operation runbook | A2-G6 |

## Required leaf record

Each implementation worker records: nominated leaf and authority, source/backend/plugin revision, changed files, exact tests/commands, raw outputs, fixture/run identities, observed results, unresolved holds, manual interventions, and next permitted action. Do not copy private owner-input bodies, account secrets or full unrelated transcripts into Git.

A check can be `PASS`, `FAIL`, `HOLD`, `NOT_RUN` or explicitly `ASSISTED`. A safe hold can pass a **negative safety test** but does not pass an unattended completion test. Missing positive stale evidence, account verification or capacity samples remains `NOT_RUN`, not “probably passed.”

The [case register](../acceptance/cases.csv) maps each exact check to its leaf/gate and required evidence. The [procedures](../acceptance/PROCEDURES.md) provide the actual fixture and fault sequences.

## Compatibility and release rule

The source ZIP and paused records stay immutable. Implementation changes require a new pinned candidate/release identity. Re-run the old suites and affected gates on that exact candidate. Earlier James Student or 0.4.1/0.4.2 passes do not close Shoco 0.4.3's missing cases. If the eventual tests run a newer patched candidate, state that plainly; do not backdate its result to 0.4.3.
