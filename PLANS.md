# Automatic Timer Trial V1 — execution plan

## Purpose and outcome

Demonstrate autonomous succession between distinct saved ChatGPT conversations in the Project Automatic Timer Trial V1, with Git as durable state and a native one-shot scheduled task as trigger. Keep the test payload trivial: exactly four successive README-only leaf commits, no duplicate leaves, no extra leaf commits and no active trial timer after leaf 4. One initial human setup is permitted; subsequent handoffs must not depend on human intervention or a prior worker. Governance-only documentation commits are not leaf commits.

## Architecture and constraints

Use the native ChatGPT Project, ChatGPT worker, GitHub, native scheduled task, Remote Desktop Commander and Chrome Windows UI Automation. No other orchestration. Workers read the three governing files and live remote state. The timer only launches the next distinct chat. The required destination is the dedicated browser Project landing page, opened directly by its verified private URL in a newly opened window. The earlier breadcrumb-based path was demonstrated but depended on the previous page; direct cold navigation requires successful named composer readback before sending. Private route/identity evidence and assigned payload travel only in private chat/task context; never in Git. Do not rely on uploaded Project files in a scheduled task. The owner requires completion-relative single-shot scheduling: exactly one non-recurring successor task five minutes after verified completion of each non-final leaf, not a fixed five-minute recurrence. Retire only the preceding trial timer before creating its successor. Individual one-shot acceptance has been observed; permission for the complete sequence remains unestablished. This distinction does not override platform frequency limits or approval requirements, and successive tasks must not be used to circumvent them. Exact fire time is measured, not guaranteed. If the platform rejects the delay or the sequence is not permitted, stop and report; no silent rescheduling or substitutes. Current official guidance: [scheduled tasks](https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt) and [Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt).

## Gates (in order)

- G0 — baseline: user places the setup chat in the named Project; verify remote tip, README prefix and no active trial timers.
- G1 — native trigger: one harmless one-shot sends exact AT-V1-G1-OK. Record scheduled/actual times and result; no tools, Git or new chat. This proves invocation, not fresh-chat routing.
- G2 — manual launcher control: open the verified Project page in the designated Chrome tab, submit the exact harmless G2 prompt once; independently verify a new distinct saved in-Project chat and AT-V1-G2-OK.
- G3 — integration: one scheduled invocation runs the demonstrated G2 launcher for G3. Independently verify the distinct saved Project chat, exact prompt and AT-V1-G3-OK. Record actual start and scheduled time separately. If the process output is lost after a possible Send, inspect the browser read-only; never resend. Functional creation and schedule-time conformance are separate evidence.
- G4 — full trial: continuation of the existing leaf 1 checkpoint through leaf 4 using the verified launcher; no restart. Requires G0–G3 functional evidence and owner authorisation to start the sequence; record any timing qualification. A schedule that runs early does not prove a genuine completion-relative delayed handoff. Do not certify timing or full autonomous delayed succession without evidence for each handoff.

## Leaf sequence

Initial README contains exactly one newline-terminated line: This is a README.md file.

| Leaf | Append exactly one newline-terminated line |
| --- | --- |
| 1 | This is the first run. |
| 2 | This is the second run. |
| 3 | This is the third run. |
| 4 | This is the fourth run. |

Leaves 1 and 2 are complete. Resume at leaf 3 against the live governance tip, after an authorised and permitted successor launch. Never repeat either completed leaf. Each subsequent assignment uses the exact current predecessor SHA. Read all three governing documents and the live README; require the exact preceding lines, complete SHA match and correct Project before an append. Publish exactly one README-only commit by normal non-force push or equivalent expected-parent conditional ref update. Verify the remote HEAD, commit parent, changed-path set and exact bytes. If already present, parent differs, or publication uncertain, stop and reconcile without repeating.

After verified publication, post the leaf receipt in the worker's saved Project chat (leaf, predecessor, published SHA, exact line, readback, completion time, next action). Inspect scheduled tasks without changing unrelated tasks. Retire only the preceding trial timer: delete it if the supported interface permits; otherwise its completed, disabled state is sufficient to prevent further execution. There must be no other active trial timer; if uncertain, stop. Leaf 4 ends with no successor. For each non-final leaf, call the Automations plugin directly to request exactly one permitted one-shot successor task, targeting five minutes after verified completion with no recurrence rule. The five-minute delay is a dependency-relative target, not a periodic interval. The plugin's maximum-frequency restriction must still be respected; do not chain tasks to circumvent it. If the sequence is unsupported, stop at the last verified leaf. Changing the five-minute target requires owner authorisation. Confirm its returned enabled/schedule status; report it in the same worker chat and stop. Do not wait or keep a worker running for the timer. The successor timer acts only as launcher: read the repository plan using the short reference prompt below, create the next chat and stop. It must not itself write Git or schedule a successor.

## Approved Project launcher

The sole destination is the named Project Automatic Timer Trial V1, resolved using its verified private landing URL. No previous conversation, starting page or persistent window handle is required. Use Remote Desktop Commander and the existing signed-in Chrome profile. Open the exact Project landing URL directly in a new Chrome window (ordinary browser navigation via `chrome.exe --new-window <VERIFIED_PROJECT_LANDING_URL>`). Do not navigate or close existing windows. Record the existing top-level Chrome window handles before opening, then identify the single newly opened window by the exact Project landing route. The window handle is discovered during this invocation only; never pass it to a successor. Accept a canonical redirect only if its Project ID and exact named Project composer match the supplied destination. If necessary allow the page to load; do not submit to a loading screen, ambiguous destination, nonempty draft or login/approval screen. If the composer does not establish within a bounded 60-second observation, stop and report. Do not bypass any approval or safety prompt.

## Reference-only handoff

The timer is a reference, not a script. After verified leaf publication, the worker calls the Automations plugin's supported create action directly with a permitted one-shot schedule and this short plain-text assignment:

> Automatic Timer Trial V1. Read AGENTS.md, PLANS.md and PROGRESS.md in JayDEmily/chat_successor_V2, branch automatic-timer. Create a new conversation in Automatic Timer Trial V1 for leaf <NEXT_LEAF>, expected parent <PUBLISHED_SHA>, using the approved Project launcher. Private destination: <DEVICE>, <VERIFIED_PROJECT_LANDING_URL>. Launch only.

No executable code, copied plan, historical task ID, prior conversation URL or window handle belongs in the timer. The scheduled launcher reads the three files and README, checks expected parent, and runs the approved procedure. The new worker receives:

> Automatic Timer Trial V1. Execute leaf <NEXT_LEAF> only in JayDEmily/chat_successor_V2, branch automatic-timer, expected parent <PUBLISHED_SHA>. Read AGENTS.md, PLANS.md, PROGRESS.md and README.md and follow them. Private destination: <DEVICE>, <VERIFIED_PROJECT_LANDING_URL>.

The plan defines the append, commit, evidence and successor rules. Substitute private values only within the handoff. Respect service limits and approval requirements.

After the Project has loaded in the newly opened window, use the existing single-Send procedure below. Substitute the observed new window handle, exact observed verified Project landing URL and exact short worker assignment. Escape single quotes in substituted strings by doubling them.

```powershell
$ErrorActionPreference='Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$w=[System.Windows.Automation.AutomationElement]::FromHandle([IntPtr]<OBSERVED_NEW_WINDOW_HANDLE>)
$project='<VERIFIED_PROJECT_LANDING_URL>'
$q='<EXACT_NEXT_WORKER_ASSIGNMENT>'
function Elements { @($w.FindAll([System.Windows.Automation.TreeScope]::Descendants,[System.Windows.Automation.Condition]::TrueCondition)) }
function Normalise([string]$u) { ($u -replace '^https://','').TrimEnd('/') }
$a=@(Elements | Where-Object {$_.Current.Name -eq 'Address and search bar' -and $_.Current.ControlType.ProgrammaticName -eq 'ControlType.Edit'})
if($a.Count -ne 1){throw 'Address ambiguous'}
$url=$a[0].GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value
if((Normalise $url) -ne (Normalise $project)){throw 'Project route mismatch'}
$ed=@(Elements | Where-Object {$_.Current.Name -eq 'New chat in Automatic Timer Trial V1' -and $_.Current.ControlType.ProgrammaticName -eq 'ControlType.Edit' -and !$_.Current.IsOffscreen})
if($ed.Count -ne 1){throw 'Project composer not established'}
$vp=$ed[0].GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
$v=$vp.Current.Value
if(![string]::IsNullOrWhiteSpace($v) -and $v.Trim() -ne 'New chat in Automatic Timer Trial V1'){throw 'Project draft present'}
$ed[0].SetFocus()
$vp.SetValue($q)
Start-Sleep -Milliseconds 300
if($vp.Current.Value.Trim() -ne $q.Trim()){throw 'Prompt readback mismatch'}
$walker=[System.Windows.Automation.TreeWalker]::ControlViewWalker
$p=$walker.GetParent($ed[0]);$buttons=@()
for($i=0;$i -lt 4 -and $p;$i++){
    $buttons=@($p.FindAll([System.Windows.Automation.TreeScope]::Descendants,[System.Windows.Automation.Condition]::TrueCondition)|Where-Object {$_.Current.ControlType.ProgrammaticName -eq 'ControlType.Button' -and $_.Current.Name -match '^Send( prompt| message)?$' -and $_.Current.IsEnabled -and !$_.Current.IsOffscreen})
    if($buttons.Count -gt 0){break}
    $p=$walker.GetParent($p)
}
if($buttons.Count -ne 1 -or $vp.Current.Value.Trim() -ne $q.Trim()){throw 'Send or prompt uncertain; no submission'}
Write-Output 'SEND_INTENT_ONCE'
$buttons[0].GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
Write-Output 'SEND_INVOKED_ONCE'
```

After Send, verify a distinct saved conversation route in the same Project and the exact posted assignment. On lost process output reconcile browser read-only without resending. Record time, launch result and private saved conversation evidence. Do not wait for worker completion. 

## Acceptance, recovery and handoff

Independently check each leaf's parent, README-only change, exact ordered prefix, remote publication and distinct saved in-Project conversation; check actual task run times and that only one successor is created. After leaf 4 inspect active trial timers and all three successor chat receipts. A completed task status is not a substitute for evidence. A lost receipt, incorrect route, early/late execution or missing approval is recorded with the precise distinction between functional and timing success. Stop at the first failed mandatory condition. Do not reset, force-push, blindly retry, skip a leaf, change architecture or advance from a claimed result. Reconcile current state before any authorised restart.

## Progress, surprises, decisions and retrospective

PROGRESS.md is the linked checkpoint and evidence ledger for these four living sections. Read it with this plan. During G4, the immutable README-only history and saved private receipts carry intermediate state; reconcile PROGRESS.md at a governance checkpoint or final review without adding commits between leaf executions. The plan and all gates are sufficient to resume with the current Git state and explicit private assignment, not undocumented assumptions from a prior conversation.

## Sources and methodology

OpenAI [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans), [Iterating Development Workflows with Codex](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex), and [Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex) support self-contained plans, limited scope, evidence-based milestone validation and current progress/decisions. The three-file layout is a project-specific adaptation, not an OpenAI requirement or a supported guarantee of this UI-based succession experiment. Sources reviewed 22 November 2026.
