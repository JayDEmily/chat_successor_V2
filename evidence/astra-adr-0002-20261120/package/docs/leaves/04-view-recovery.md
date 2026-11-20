# A2-L04 — Qualify saved-view recovery

**Prerequisite:** L03. **Gate:** part of A2-G1; actual Chrome evidence in A2-G2/G3. **Checks:** A2-V01–V06. **Touch only:** `windows_backend.py`, existing PowerShell helper/adapter paths and focused tests.

## Expected outcome

A missing view can reopen the same registered saved worker without a new worker count. A genuinely stale original reloads only after positive fresh completion evidence. A still-streaming fresh view simply waits. A pending/uncertain Send is never confused with ordinary view loss.

## Work

Retain the current 120-second unchanged-view threshold and 300-second per-worker probe interval unless a measured, approved reason changes them. Preserve the bounded fresh-view comparison, exact latest-user anchor, owned-probe cleanup, original-view revalidation and empty-composer protection.

Add only the route/action identity checks from L02/L03 and diagnostics needed to distinguish restored, waiting, reload-invoked, fresh completion consumed, and held. A single accessible selected tab per run remains the operating constraint; foreground focus is not required.

## Exact checks

- **V01 — closed:** without a pending Send, close the registered worker's view. Reopen exact account/Project/chat; verify stable readback; no new saved ID or posted prompt.
- **V02 — displaced:** move the saved worker behind another tab, pause/restart and release. Restore an accessible view of the same chat, preserve the hidden view/draft, count/history/cap and peer run. If old and recovered views later both become accessible, hold ambiguity rather than choose.
- **V03 — positive stale:** original remains old/Stop while a fresh same-chat view has a newer completed response to the **same user turn**. Two stable fresh comparisons, empty unchanged original, close owned probe, one reload, then normal stable observation/Git readback. Capture both fingerprints and timestamps. `refreshed` alone is not PASS.
- **V04 — negative stale:** fresh also streaming, same completed response already consumed, latest user changed, or source advances during probing. No unjustified reload, no Send; enforce timing/cooldown and document restart timer reset.
- **V05 — unsafe view:** duplicate accessible targets, draft matching the placeholder, ordinary draft, attachment, unknown composer, wrong account/Project, missing desktop/login. Hold; no clearing/typing/reload of unverified content. Owned temporary probes close; unrelated windows remain untouched.
- **V06 — worker advances during preparation:** preserve any typed draft, avoid duplicate owner input/continuation, and reconcile the current turn without treating “advanced” as authorization proof.

## Evidence and limits

Run Python view/dispatch tests and PowerShell helper comparisons on Windows. The supplied PowerShell log only reports comparison tests; it is not a live stale recovery receipt. Record actual account, window handle/lifecycle, saved ID, response/user anchors, probe ownership, counts before/after and any manual action. Actual positive stale behavior remains a required live test; if it cannot be reproduced, mark it `NOT_RUN`.

## Hold / failure

Do not tune timeouts into blind reloads. Do not restart Chrome globally, close other runs, clear a draft or send a corrective message to hide a failed case. Keep the saved-worker link and reason. Any possibly sent action returns to L03 reconciliation, not this leaf's missing-view path.

Sources: S04–S07/S12/S13; F05/F06.
