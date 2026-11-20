# ADR 0002 — published L02 independent negative review and targeted repair

**Reviewed pinned Worker candidate:** `3f9715e2b34755c0bc2bbf2c0b23dd3d2dfa6c8c` (the published A2-L02 offline checkpoint).
**Scope:** Offline source, separate fresh Git clone, mocked/synthetic run state; no real account switch, browser Send, installed Windows changes, Chrome draft or production project work.

## Reproduced contract gaps in the original 79-test candidate

1. The private `account_routes.json` parser accepted duplicate `shoco` keys and silently used the last occurrence. This defeats the no-ambiguous-route objective.
2. The same Chrome profile path was accepted for both `shoco` and `james-student`. A single profile cannot constitute verified independent account routes.
3. A persisted operator pause at the final pre-Send boundary has `halted="Operator pause requested before Send"` and an existing marker, but the read-only status reported `pause_acknowledged=false`. It had only recognised the exact shorter pause text.

Raw observed original probe booleans are retained in [verification_summary.json](verification_summary.json). They demonstrate contract inconsistencies at synthetic/mock boundaries, **not observed live cross-account sends**.

## Minimal in-scope repairs

- `integration/account_routes.py`: reject duplicate JSON keys and sibling accounts sharing a case-/separator-equivalent Windows Chrome profile.
- `integration/runner.py`: recognise the controller's explicit `Operator pause requested…` pre-Send halt as acknowledgement when the durable marker is present.
- `integration/tests/test_a2_l02_independent_negatives.py`: three focused negative regressions, including a read-only journal/draft-preservation check.

## Reproduced post-fix tests

- [82 integration tests](integration_82_tests.log): PASS; 79 original plus three new regressions, no failures/skips.
- [119 reference tests](reference_119/test_output.txt): PASS; fresh execution, original offline reference kit.
- `git diff --check`: PASS.
- No deployment, plugin update, Windows UIA live test or G1/G2 signoff. These are targeted fixes generated after independent discovery, **not an independent final acceptance of the amended candidate**.

**Disposition:** Repair candidate ready for subsequent independent gate validation. A2-L02 remains offline only; A2-G1/G2 not closed. Keep existing paused Rowing/SolidWorks runs untouched. Continue the ordered L03 leaf only after this checkpoint is published and its source/parent checked.
