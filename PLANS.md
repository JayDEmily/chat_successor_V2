# Automatic Timer Trial V1 — execution plan

## Purpose and outcome

Demonstrate autonomous succession between distinct saved ChatGPT conversations in the Project Automatic Timer Trial V1, with Git as durable state and a native one-shot scheduled task as trigger. Keep the test payload trivial: exactly four successive README-only leaf commits, no duplicate leaves, no extra leaf commits and no active trial timer after leaf 4. One initial human setup is permitted; subsequent handoffs must not depend on human intervention or a prior worker. Governance-only documentation commits are not leaf commits.

## Architecture and constraints

Use the native ChatGPT Project, ChatGPT worker, GitHub, native scheduled task, Remote Desktop Commander and Chrome Windows UI Automation. No other orchestration. Workers read the three governing files and live remote state. The timer only launches the next distinct chat. The successful route is the dedicated browser Project page opened via a verified Project breadcrumb/direct Project URL, not global sidebar discovery. Private route/identity evidence and assigned payload travel only in private chat/task context; never in Git. Do not rely on uploaded Project files in a scheduled task. A five-minute relative one-shot is the experimental target, conditional on permitted platform frequency, timing and authorisation. A chain must not be used to circumvent hourly recurrence or other limits. Exact fire time is measured, not guaranteed. If the platform rejects the delay or the sequence is not permitted, stop and report; no silent rescheduling or substitutes. Current official guidance: [scheduled tasks](https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt) and [Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt).

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

After verified publication, post the leaf receipt in the worker's saved Project chat (leaf, predecessor, published SHA, exact line, readback, completion time, next action). Inspect scheduled tasks without changing unrelated tasks. There must be no other active trial timer; if uncertain, stop. Leaf 4 ends with no successor. For leaves 2 and 3, call the Automations plugin directly to create exactly one permitted one-shot successor task, targeting five minutes after verified completion only when the whole sequence is permitted. The current plugin specifies a maximum task frequency of once per hour; do not chain separate tasks to achieve a prohibited higher frequency. If the required cadence is unsupported, stop at the last verified leaf. Changing the cadence requires owner authorisation. Confirm its returned enabled/schedule status; report it in the same worker chat and stop. Do not wait or keep a worker running for the timer. The successor timer acts only as launcher: read the repository plan using the short reference prompt below, create the next chat and stop. It must not itself write Git or schedule a successor.

## Frozen launcher procedure (G2/G3 demonstrated)

Use Remote Desktop Commander in the existing signed-in Chrome session and the designated tab. The private payload supplies the observed Project URL and current designated chat route/window; do not guess or scan for a globally unique sidebar button. Verify designated tab's current route, Project breadcrumb and no draft or active generation. Navigate through the exact Project breadcrumb to the verified Project landing page; verify the route and unique visible project-specific composer labelled New chat in Automatic Timer Trial V1. Treat the actual UI placeholder as empty only when it matches the verified label; do not overwrite a draft. Set the exact assigned text through UIA ValuePattern, read back, find the unique enabled Send within the composer's scope, and InvokePattern once. Verify new distinct saved conversation route in the named Project and the exact submitted text (plus acknowledgement for diagnostic gates). Use the self-contained launcher template below. Do not retrieve a previous chat, task definition or historical timer. Only substitute the verified private inputs and the exact assigned prompt. Read process output by PID if still available; reconcile the visible browser on output loss or ambiguous return, without another Send. No sidebar lookup, new identity protocol or persistent controller.

Private launcher payload includes only the repository, branch, assigned leaf, exact expected parent SHA, governing file references and verified private destination inputs. The repository defines the append, commit, readback and successor instructions. The new worker receives the assignment, not permission to modify this plan. Record task scheduled/start/finish timestamps, launcher outcome, verified destination/posted prompt, and fresh chat evidence privately.

## Self-contained launcher template

The timer is a reference, not a script. After verified leaf publication, the worker calls the Automations plugin's supported create action directly with this short plain-text assignment and a permitted one-shot schedule:

> Automatic Timer Trial V1. Read AGENTS.md, PLANS.md and PROGRESS.md in JayDEmily/chat_successor_V2, branch automatic-timer. Execute the approved launcher for leaf <NEXT_LEAF>, expected parent <PUBLISHED_SHA>. Private destination: <DEVICE>, <WINDOW_HANDLE>, <VERIFIED_START_CHAT_URL>, <VERIFIED_PROJECT_LANDING_URL>. Launch only.

No executable code, copied plan, historical task ID or previous task lookup belongs in the timer. The scheduled launcher reads the three files and README at the live tip, checks the expected parent and executes the procedure in this section. The fresh worker receives:

> Automatic Timer Trial V1. Execute leaf <NEXT_LEAF> only in JayDEmily/chat_successor_V2, branch automatic-timer, expected parent <PUBLISHED_SHA>. Read AGENTS.md, PLANS.md, PROGRESS.md and README.md and follow them. Private destination: <DEVICE>, <WINDOW_HANDLE>, <VERIFIED_PROJECT_LANDING_URL>.

The plan determines the append, commit, verification, successor and final stop rules. The worker obtains the current designated chat route by inspecting its own browser tab, not by looking up previous tasks. Substitute all placeholders with actual verified values privately; never publish private identifiers. Respect service limits and approval prompts; do not attempt to evade a safety warning.

Use Remote Desktop Commander start_process on the supplied authorised device to execute the following existing UIA procedure with the private inputs and exact next-worker prompt substituted. Escape single quotes inside substituted PowerShell string inputs by doubling them.

```powershell
$ErrorActionPreference='Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$w=[System.Windows.Automation.AutomationElement]::FromHandle([IntPtr]<WINDOW_HANDLE>)
$start='<VERIFIED_START_CHAT_URL>'
$project='<VERIFIED_PROJECT_LANDING_URL>'
$q='<EXACT_NEXT_WORKER_ASSIGNMENT>'
function Elements { @($w.FindAll([System.Windows.Automation.TreeScope]::Descendants,[System.Windows.Automation.Condition]::TrueCondition)) }
function Address {
    $a=@(Elements | Where-Object {$_.Current.Name -eq 'Address and search bar' -and $_.Current.ControlType.ProgrammaticName -eq 'ControlType.Edit'})
    if($a.Count -ne 1){throw 'Address ambiguous'}
    $a[0].GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value
}
function Normalise([string]$u) { ($u -replace '^https://','').TrimEnd('/') }
function Composer([string]$name) { @(Elements | Where-Object {$_.Current.Name -eq $name -and $_.Current.ControlType.ProgrammaticName -eq 'ControlType.Edit' -and !$_.Current.IsOffscreen}) }
if((Normalise (Address)) -ne (Normalise $start)){throw 'Starting route mismatch'}
$ed=@(Composer 'Ask ChatGPT')
if($ed.Count -ne 1){throw 'Composer ambiguous'}
$v=$ed[0].GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value
if(![string]::IsNullOrWhiteSpace($v) -and $v.Trim() -ne 'Ask ChatGPT'){throw 'Existing draft'}
if(@(Elements | Where-Object {$_.Current.ControlType.ProgrammaticName -eq 'ControlType.Button' -and $_.Current.Name -match '^Stop( generating)?$' -and !$_.Current.IsOffscreen}).Count -ne 0){throw 'Active generation'}
$h=@(Elements | Where-Object {$_.Current.Name -eq 'Automatic Timer Trial V1' -and $_.Current.ControlType.ProgrammaticName -eq 'ControlType.Hyperlink' -and !$_.Current.IsOffscreen})
if($h.Count -ne 1){throw 'Project breadcrumb ambiguous'}
$h[0].GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
$ed=@()
for($i=0;$i -lt 30;$i++){
    Start-Sleep -Milliseconds 300
    if((Normalise (Address)) -eq (Normalise $project)){
        $ed=@(Composer 'New chat in Automatic Timer Trial V1')
        if($ed.Count -eq 1){break}
    }
}
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

After Send, inspect the designated browser read-only. Verify a distinct saved conversation in the same Project and the exact posted assignment; do not wait for worker completion. On process-output loss, reconcile the browser without resending. No new mechanism and no historical dependency.

## Acceptance, recovery and handoff

Independently check each leaf's parent, README-only change, exact ordered prefix, remote publication and distinct saved in-Project conversation; check actual task run times and that only one successor is created. After leaf 4 inspect active trial timers and all three successor chat receipts. A completed task status is not a substitute for evidence. A lost receipt, incorrect route, early/late execution or missing approval is recorded with the precise distinction between functional and timing success. Stop at the first failed mandatory condition. Do not reset, force-push, blindly retry, skip a leaf, change architecture or advance from a claimed result. Reconcile current state before any authorised restart.

## Progress, surprises, decisions and retrospective

PROGRESS.md is the linked checkpoint and evidence ledger for these four living sections. Read it with this plan. During G4, the immutable README-only history and saved private receipts carry intermediate state; reconcile PROGRESS.md at a governance checkpoint or final review without adding commits between leaf executions. The plan and all gates are sufficient to resume with the current Git state and explicit private assignment, not undocumented assumptions from a prior conversation.

## Sources and methodology

OpenAI [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans), [Iterating Development Workflows with Codex](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex), and [Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex) support self-contained plans, limited scope, evidence-based milestone validation and current progress/decisions. The three-file layout is a project-specific adaptation, not an OpenAI requirement or a supported guarantee of this UI-based succession experiment. Sources reviewed 22 November 2026.
