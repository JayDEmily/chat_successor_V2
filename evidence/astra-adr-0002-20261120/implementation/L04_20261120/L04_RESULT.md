# A2-L04 — Saved-worker view recovery qualification

**Disposition:** Offline Python and native PowerShell helper tests PASS.
**No application code changes were justified by these checks.**
Live Chrome missing/displaced/stale acceptance remains **NOT_RUN**.
**Source base:** `6dac237` (L03).

## Existing recovery mechanism retained

The current adapter checks exact saved chat and Project, preserves the same
worker and cap, compares a fresh view of a stale response, requires the same
latest user-turn anchor, requires two stable fresh reads, closes its own probe,
revalidates original view and empty composer, and only then invokes the
original window's reload. An observed `refreshed` outcome is an invocation,
not proof that the response was then consumed. It requires the normal next
poll, stable response and Git publication check. Timeouts remain 120s/300s
as Astra recommended.

## New offline evidence

- [98 integration tests](integration_98_tests.log): **PASS**, comprising
  91 post-L03 cases and 7 new V01–V06 qualification cases.
- [Native Windows PowerShell helper tests](windows_ps_view_helpers.log):
  **PASS**, positive same-user fresh completion; rejection of streaming,
  changed user digest/count, changed response during stable-double-read;
  persistent pause marker recognised. Pure AST-extracted helper tests, no
  UIA Chrome interaction or Send.
- [Reusable PS test harness](../../../../integration/tests/test_a2_l04_ps_view_helpers.ps1).
- No failing tested requirement established a need to rewrite the existing
  recovery code. No source rewrite, global Chrome restart, window closure,
  custom timeout adjustment or extra automation was introduced.

## Open live acceptance

V01 (closed same-chat), V02 (displaced/tab), V03 (positive genuinely stale
Chrome response), V04 (negative streaming/changed user), V05 (draft/duplicate/
wrong-account/attachment) and V06 (advanced worker) **must still be observed
in the installed account-specific Chrome environment on isolated disposable
Chat Succession Projects and repositories**. These offline mock passes do
not satisfy G2/G3; particularly V03 remains an important positive live gap.

**Next:** A2-L05 — scoped approval and publication regression matrix,
then independent A2-G1 offline review of L02–L05.
