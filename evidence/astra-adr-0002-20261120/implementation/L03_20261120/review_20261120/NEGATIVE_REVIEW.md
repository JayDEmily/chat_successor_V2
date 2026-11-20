# ADR 0002 L03 — independent negative review and safety repair

**Reviewed parent:** `9424740882e01f3c8beb04b4a65caafe512a4b85` (already included the L04 offline case additions). **Scope:** desktop-state mocks and native Windows PowerShell function-only tests; **no live browser Send, installation, account switching, paused production run or Git merge**.

## Independently reproduced original failure modes

The exact same 5-key test was run against an untouched fresh clone at the pinned parent and the amended checkout. Raw before/after records are [unpatched](unpatched_pinned_probe.json) and [repaired](repaired_candidate_probe.json).

| Predicate | Unpatched observation | Repaired observation |
| --- | --- | --- |
| Wrong Project/worker destination entered adapter Send | **YES** (unsafe boundary) | **NO** — hold before adapter |
| Initial bootstrap intent included route receipt | **NO** | **YES** |
| Initial bootstrap intent included run identity | **NO** | **YES** |
| Changed account route triggered read-only Reconcile against old initial intent | **YES** (wrong-route attempt) | **NO** — hold before browser |
| Confirmed pre-click pause preserved original bootstrap intent | **NO** (deleted) | **YES** — immutable intent retained |

These outcomes are reproduced on synthetic mocked states, not evidence of actual misrouted messages. They are narrower, code-specific failures against the [operative L03 requirements](../../../package/docs/leaves/03-pause-and-action-identity.md).

## Targeted corrections

1. `integration/windows_backend.py`: check the prepared destination's Project and current-chat identity before invoking Send; stop using an old successor window handle unless **all** current target identity fields match, including action, response, message digest, Project and route; re-read the pending action after UIA preparation; reject missing bound account-route receipts. Pass both route receipt and pending response ID into native click/reconcile.
2. `integration/launch_story.py`: persist initial intent with exact run ID, account-route receipt and message hash, validate them on restart before Reconcile, and **retain** the intent when the pre-click adapter reports a definite pause/destination change. Retrying a private request file is read-only reconciliation, not an automatic second Send. An historic unbound bootstrap intent remains eligible only for read-only reconciliation, never a new Send through the amended PowerShell boundary.
3. `integration/uia_adapter.ps1`: before typing/click and during Reconcile, verify exact route and triggering-response identity in the persisted action record. Before a new initial Send verify the request/run ID, route and message SHA-256 in its durable bootstrap intent.
4. Updated historical tests to construct valid identity-bearing receipts and to assert the **intent-preserving** pre-click pause behaviour. No previous passing test was disabled or removed.

## Evidence and status

- [103 integration test cases](integration_103_tests.log): **PASS**, comprising 98 previously published L02–L04 cases plus five new negative regressions, no failures or skips.
- [119 unchanged Astra reference tests](reference_119/test_output.txt): **PASS**, fresh execution on the amended checkout.
- [Native Windows PowerShell gate log](native_windows_powershell_action_gate.log): AST parse and action-check function exercised; one positive ordinary action, four negative target identities, one positive bootstrap, two negative bootstrap checks. The actual adapter modes and Chrome UI were **not** invoked.
- [Machine-readable summary](verification_summary.json) and raw [before](unpatched_pinned_probe.json)/[after](repaired_candidate_probe.json) comparison. `git diff --check` PASS.

**Disposition:** Targeted L03 safety defects repaired and offline verified on a post-L04 candidate. **Not** an independent final acceptance of our own amended code, and **not** A2-G1/G2 closure. The missing/displaced/stale positive live Chrome acceptance and S04–S09 live fault matrix remain for authorised disposable fixture runs after the account install gate.

No Rowing or SolidWorks project state or workers were changed.
