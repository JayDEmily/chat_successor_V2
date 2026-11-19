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

**Validation to date (18 November):** reference 119/119 offline and
16/16 new simulated integration tests passed independently. Chrome UIA
placeholder/draft, exact Project URL navigation, and initial authenticated
message Send were exercised on Windows. The **first** L01 test worker is an
assisted bootstrap. The controller has not yet demonstrated an autonomous
successor or completed L01; L02-L15 remain unproven.

**Windows state placement:** Use a private native NTFS file path for the
controller state and its lock (for example under the user's LocalAppData).
Windows `msvcrt.locking` on a `\\wsl.localhost` UNC path returned
`OSError: [Errno 22] Invalid argument` in the live preflight. Keep the
private config and the fixture repository wherever appropriate; do not
put controller state into the Git branch or reset an existing run.

In the existing private JSON config, `"poll_seconds": 20` sets the delay
between response checks and defaults to 20 when omitted.
`"response_wait_minutes": 40` gives the controller 40 minutes to observe
each completed response. The time starts when `run` begins and starts again
after each confirmed Send, including same-chat continuations. Omit the
setting or use `null` for an unlimited wait. Expiry holds the saved controller
before it consumes a late response or prepares a new Send. An observation
already in progress can finish before the hold is recorded. An already
prepared action follows the existing dispatch and recovery rules.
Remove any old `--poll-seconds 5` from launchers to use the config value.

`run` writes one final JSON result to stdout. Redirect stderr to a private log
to retain UTC timestamps for UI Automation calls, observation outcomes,
publication checks and confirmed submissions. The adapter logs the
observation reason without response text.

Only the clipboard check requests foreground focus. It briefly waits for the
known Chrome window and checks editor focus before keyboard input. If Windows
denies the request or focus changes during the probe, the adapter holds.

The PowerShell `-AlreadyTyped` recovery switch is reserved for a manually
verified, **not previously sent** exact test draft. It is not called by
the automatic backend, which requires a genuinely empty composer. A
short UIA rendering delay caused an exact immediate readback failure,
so bounded polling of the exact draft is now used before any Send.

A browser Send is only valid after the reference controller has written
the matching `sending` phase (except the separately recorded *initial*
bootstrap). Never retry a possibly submitted message. Read the unchanged
original `docs/astra-succession/leaves/` for the test gates.

The controller checks the existing owner pause marker after composer preparation.
The Windows adapter checks it again before typing and immediately before invoking
Send. An explicit pre-click pause preserves the prepared action, including any
draft already typed. Missing or ambiguous receipts still require reconciliation.

**L06 prepared-handover test seam:** CLI cycle --prepare-only observes the
completed current worker, validates published handover state, and saves the
reference controller's prepared action without touching the composer or sending.
After the operator rotates the next-slice probe and publishes it, a normal CLI
cycle dispatches that exact persisted action once. Repeating prepare-only on the
prepared action makes no Send. This is a one-shot L06 test facility, not another
controller or a general automatic pause scheduler.
