# Operator quickstart — start, pause, resume, check

**This is a proposed handoff procedure, not a statement that the new release gates passed.** Keep the paused Rowing/SolidWorks runs unchanged until the owner explicitly directs otherwise. Use only the verified installed runtime, not the copied evidence source in this package.

## Once per account

Verify that account's private Chat Succession plugin, Desktop Commander binding, installed wrapper/backend, native state root and signed-in Chrome profile. James Student and Shoco need separate verified routes even though they have the same owner. Do not assume historical Profile 13 / Profile 11 still identify the correct signed-in accounts.

The owner creates the Project and GitHub repo and supplies existing work/publication rules. Keep the Windows session and Ubuntu Git access available. The run's worker must be the selected tab in its own accessible Chrome window; the window may be in the background. Do not open duplicate views or type in a controller-owned composer during dispatch.

## The four operations

| Operation | Owner's simple request | What must be checked / reported |
| --- | --- | --- |
| **Start** | In the exact Project on phone or desktop, choose that account's plugin: “Start Chat Succession for this Project, repo OWNER/REPO, branch BRANCH, with a cap of 2.” | Inspect existing runs first. Verify account, Project, published branch and empty composer. A genuinely new job is explicit. Report run ID, first saved desktop worker, count/cap and route. The request chat does not count. |
| **Pause** | “Pause this run.” Identify the run if more than one is relevant. | The operator writes the existing durable pause marker and waits for acknowledgement. Report requested versus acknowledged, current worker/count, pending action and any in-flight uncertainty. Pausing does not cancel work already running in ChatGPT. |
| **Resume** | “Resume the same run.” If separately paused: “Release my pause and resume the same run.” | Inspect first; reconcile any possibly submitted action before resuming. Preserve saved worker, histories, branch checkpoint and cap. Explicitly release only the observed pause generation. Never bootstrap a replacement. |
| **Check** | “Show this run's status.” | Read-only: account/Project/repo, entry/effective branch, current saved-worker link, count/cap, marker/acknowledgement, pending phase/action, terminal/hold reason and last verified Git receipt. Status is not permission to send. |

For one clear proposal, “I approve” in the Project request chat is sufficient owner wording. The plugin carries only that scoped decision once to the already saved worker. If scope or executor is unclear, clarify it. A terminal capped/finished run cannot resume: a separately authorized new job is different, not a cap reset.

## Existing 0.4.3 operator commands

The current generic launcher has `inspect`, `start`, `resume`, `new` — **no JSON `pause` operation**. The pause request above maps to the existing CLI `pause`. A2-L02 proposes a richer summary; until then inspect the pause marker separately from `status`.

An authorized Windows operator resolves these values from the installed route, not by guessing:

```powershell
$Python = 'VERIFIED_ABSOLUTE_WINDOWS_PYTHON_EXE'
$Backend = 'VERIFIED_BACKEND_CHECKOUT_ROOT'
$Install = 'VERIFIED_NATIVE_INSTALL_ROOT'
$RunId = 'VERIFIED_24_CHARACTER_RUN_ID'
$Run = Join-Path $Install ('Runs\' + $RunId)
$State = Join-Path $Run 'controller.json'
$Config = Join-Path $Run 'config.json'
$Cli = Join-Path $Backend 'integration\cli.py'
```

### Check and pause

```powershell
& $Python -B -X utf8 $Cli status --state $State
Test-Path -LiteralPath ([IO.Path]::ChangeExtension($State, '.pause'))

& $Python -B -X utf8 $Cli pause --state $State
& $Python -B -X utf8 $Cli status --state $State
Test-Path -LiteralPath ([IO.Path]::ChangeExtension($State, '.pause'))
```

`pause_requested` is not acknowledgement. Wait for the original controller's safe hold/exit (or an already-terminal run), inspect its pending action and ownership/process evidence, and retain the marker across restart. Do not delete the journal or kill/relaunch Chrome as a substitute.

### Reconcile before a possible retry

For an existing journal with `sending` / `uncertain`:

```powershell
& $Python -B -X utf8 $Cli reconcile --config $Config --state $State
```

This inspects the browser without sending. It may update local bookkeeping after a positive exact posted-message/saved-ID match. It does not itself release a pause. `unresolved_no_resend`, a missing target, local-only ID or ambiguous evidence means **hold**, not repeat Send.

An initial bootstrap intent without a journal is reconciled through the original launcher request, not this controller command. Reuse the selected run/intent; do not choose `new`.

### Resume through the existing launcher

After explicit owner direction and required reconciliation, write a new private request beside the verified installation using the existing plugin contract. Retain the selected run, omit cap changes, and use `release_pause: true` only for an explicit release:

```json
{
  "operation": "resume",
  "repo": "OWNER/REPO",
  "project_name": "EXACT_PROJECT_NAME",
  "project_url": "VERIFIED_PROJECT_LANDING_URL",
  "run_id": "VERIFIED_24_CHARACTER_RUN_ID",
  "release_pause": true
}
```

The strings above are placeholders, not a valid ready-to-run request. Set the actual verified values, save to a unique private request file and invoke the installed wrapper once:

```powershell
& (Join-Path $Install 'start-project.cmd') --request $RequestPath
```

Use observer-only resume (no new owner context) when the input is already delivered. A genuine scoped approval uses the immutable `owner_context` contract and current worker/hold response from inspection. Do not manufacture a new decision ID to defeat deduplication.

`cli.py resume` alone clears a permitted hold but does not start an observer; using the launcher avoids forgetting the existing run step. Do not start a second controller if ownership is unresolved.

### Preflight for a new run

The installed wrapper's `--check` requires the exact published `branch` in the request:

```powershell
& (Join-Path $Install 'start-project.cmd') --request $RequestPath --check
```

This verifies Git/Project/composer without Send and must leave durable run state unchanged. A successful preflight is not a completed launch, publication or acceptance trial.

## If a run holds

- **Draft/attachment/duplicate view:** preserve it; inspect with the owner. Never clear user content automatically.
- **Closed/displaced saved view, no uncertain action:** same-chat recovery may restore it; counts do not change. If identity is unresolved, hold.
- **Stale rendering:** require a genuinely newer completed response in the same-chat fresh comparison before safe reload. A streaming fresh view means wait.
- **Pending/uncertain Send:** reconcile the original action first. Lost readback is not proof that nothing was sent.
- **Wrong account/Project/repo/branch:** no fallback, no replacement worker. Correct the verified route under the owner.
- **Cap or job finished:** do not resume or increase the saved cap. Explain the terminal result and seek a separately authorized new job if necessary.
- **Resource saturation:** stop new admissions and follow the measured last-good operating level. Do not globally close other runs' windows.

The simplest normal path remains: **select the right account's plugin, identify the work, and let one saved run carry it. Pause is sticky; resume preserves it; checking never sends.**
