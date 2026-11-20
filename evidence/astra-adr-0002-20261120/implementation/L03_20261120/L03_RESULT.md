# A2-L03 — Exact action identity at the final Send boundary

**Disposition:** Code and mocked/native-parser checks PASS; live browser fault
acceptance still **NOT_RUN**. **Original development parent:** `3f9715e`; reconciled onto peer-reviewed `77ffd1b`.
**Scope:** Existing Windows UIA adapter and Python controller only; no new
sender, service, plugin or private installation changed.

## Change

- The existing `WindowsUIA.prepare` captures the complete current pending
  action: `action_id`, exact triggering `response_id`, source saved chat,
  project, native window handle, message SHA-256 and optional account route
  receipt. It refuses kind/source mismatches before replacing a target record.
- Before `send_once` enters the adapter it independently checks all these
  fields against the persisted `sending` action and target. The same exact
  check is required before read-only reconciliation of a `sending` or
  `uncertain` action. A legacy target without action identity holds rather
  than being silently rearmed.
- `uia_adapter.ps1` checks that exact persisted action in the original
  native PowerShell process both before typing and immediately before its
  one native UIA Send Invoke. This closes the static P08 gap where an older
  action ID could pass the earlier Python match. The installed adapter and
  its existing document-bound Send/posted-turn readback remain in place.
- Initial bootstrap continues to use its **separate durable bootstrap intent**.
  New intents carry a UUID action ID; the final native Send boundary checks
  that persisted intent, handle, Project and message. A historical intent
  missing the new action ID remains eligible for read-only reconciliation,
  not for a new Send.
- No uncertain action is automatically resent. Existing pause marker,
  generation-aware release, counted-once adoption, terminal stop, and
  initial intent semantics are retained.

## Actual checks

- [Post-peer-review 91/91 integration tests](integration_91_tests_after_l02_review.log), 63 original tests, 16 L02 tests, 3 independently discovered L02 negative regressions and 9 L03 tests: **PASS** after integration of `77ffd1b`.
- Earlier [88/88 integration tests](integration_88_tests.log), including the 63
  original case classes (updated to require the stronger target identity),
  16 L02 tests and 9 new L03 tests: **PASS**, no skips.
- [Native Windows PowerShell AST and gate tests](windows_ps_action_gate.log):
  script parsed and the exact action assertion accepted correct target and
  bootstrap records while rejecting stale action ID, wrong message digest
  and missing bootstrap action ID; **PASS**, no browser opened.
- The reusable [PowerShell test harness](../../../../integration/tests/test_a2_l03_ps_action_gate.ps1)
  uses parser/AST extraction, not execution of the UIA adapter's live modes.
- The unchanged [119-reference baseline](../L02_20261120/reference_119_offline_results.json)
  is carried forward at its exact scope. No assertion that this source
  candidate was installed or live-tested.
- `git diff --check` PASS, AST parsing of changed Python source PASS.

## L03 acceptance still open

S04–S09 have representative offline mock tests and the final adapter parser
check. Real crash/pause/draft/uncertain-window injections on isolated
owner-authorised mock fixtures remain for A2-G3, **not** active Rowing or
SolidWorks. UIA browser account/window verification and actual posted-turn
readback on the installed candidate are **NOT_RUN**.

**Next:** A2-L04 — qualify saved-worker missing/displaced and genuinely
stale-view recovery without sending or admitting a replacement worker.
