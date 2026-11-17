# Astra integration seam — implementation branch only

The reference controller and its three statuses remain in
`astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/succession/`.
This directory is the minimal connection to the existing Windows 11/Chrome
UI Automation method and Git/WSL publication route, **not another controller**.

- `runner.py` calls Astra's `Controller.consume`, persists state before Send,
  and delegates observation/prepare/one Send/reconciliation.
- `repo_reader.py` reads the nominated, freshly fetched remote-branch
  `succession-tests/<run-id>/STATE.json`, never local-only state.
- `windows_backend.py` calls `uia_adapter.ps1` for Chrome observations and
  the existing Project-specific navigation/Send mechanism.
- `cli.py` exposes run status and pause/resume/reconcile, using the same
  controller state file. It does not launch additional controllers.
- `tests/` covers these connections with simulated browser/Git observations.

**Current validation:** the reference 119 offline tests and 16 separate
local integration tests pass. A controlled, unsent live editor probe
distinguished the placeholder from an identical real draft. The live
Project-new-chat preparation then stopped because the sidebar button
remained offscreen after the existing UIA ScrollIntoView action.
No live ChatGPT Send, genuine successor, or end-to-end Git worker
handover has passed. Live scenarios remain NOT_RUN.

Do not invoke `Send` against the authenticated environment before
the Leaf 03 desktop observation/navigation boundary is confirmed.
Continue from the original `docs/astra-succession/leaves/` plan.
