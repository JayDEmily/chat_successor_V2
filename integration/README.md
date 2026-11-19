# Chat Succession integration

## Repo-neutral launcher

`launch_project.py --request PATH` takes a private Windows JSON request with
`repo`, `project_name` and an `operation` of `inspect`, `start`, `resume`,
or `new`. Supply `branch` for starts. `max_unique_chats` defaults to five.
`project_url` is optional when a verified ChatGPT Project landing URL is
available. With a name alone, desktop Chrome looks for a saved chat in the
exact Project's sidebar list. Use the verified Project landing link if Chrome
cannot find that list. Inspection selects using the verified Project ID and
normalized repo, or a matching explicit `run_id`. A genuine new job requires
a stable `job_id`. An optional `owner_context` follows the [plugin request
contract](../plugins/chat-succession/skills/start-chat-succession/SKILL.md).
Adding `--check` verifies the GitHub branch and the browser composer without
posting a message or starting a controller.

The launcher keeps controller files in `%LOCALAPPDATA%\ChatSuccession\Runs`
and makes an Ubuntu bare readback repository for each run. `GitHandoffReader`
fetches the nominated branch tip and checks the run ID, saved chat ID and
next-assignment Git trailers described in the [startup guide](../README.md).
Each worker reads and applies its repository's own instructions before it
works or publishes.

## Existing story and Astra modes

The My Cat and Dog trial uses `launch_story.py` from the authorized Windows
desktop. Its private config points at the verified Project landing page and an
Ubuntu checkout of `JayDEmily/my-cat-and-dog`. The installed launcher accepts
`--check` to verify a fresh composer and remote setup without a Send. A normal
launch persists the first Send intent and verifies the new saved chat before
initializing worker 1. A later request uses the existing state or reconciles an
uncertain first Send read-only.

The story reader verifies each published branch in order. It checks the parent,
the single added dialogue line, and the saved worker ID in the commit trailer.
The ordinary controller still sends the short pointer to `main`, where the
next worker discovers its turn. Four published turns end the trial.

The reference controller and its three statuses remain in
`astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/succession/`.
This directory is the minimal connection to the existing Windows 11/Chrome
UI Automation method and Git/WSL publication route, **not another controller**.

- `runner.py` calls Astra's `Controller.consume`, persists state before Send,
  and delegates observation/prepare/one Send/reconciliation.
- `repo_reader.py` reads the nominated, freshly fetched remote branch. Astra
  uses `succession-tests/<run-id>/STATE.json` on that branch.
- `windows_backend.py` calls `uia_adapter.ps1` for Chrome observations and
  the existing Project-specific navigation/Send mechanism.
- `cli.py` exposes run status and pause/resume/reconcile, using the same
  controller state file. It does not launch additional controllers.
- `tests/` covers these connections with simulated browser/Git observations.

See [project progress](../PROGRESS.md) for live Astra and story results.

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

When a successor is due, the adapter can follow the verified Project link
from the saved, completed worker in its current Chrome window. It checks the
completed response and empty source composer first. It records the window
against the pending action before navigating and verifies the fresh Project
composer before Send. If the link is unavailable, the existing Chrome
new-window path remains available. A local-only conversation ID cannot
confirm a Send.

The composer check reads Chrome's accessibility tree without selecting text
or using the clipboard. It requires ProseMirror's empty-placeholder paragraph
and its trailing break, in addition to the expected UIA value. A draft with
the same words as the placeholder still blocks Send. Unknown composer
structure or attachment evidence holds the action.

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
