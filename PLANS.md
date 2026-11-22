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

Leaf 1 was completed before this governance checkpoint. G4 starts with a single fresh leaf 2 assignment against the current remote governance tip, not the old leaf 1 SHA. Each later leaf uses the exact newly published SHA. Read all three governing documents and the live README; require the exact preceding lines, complete SHA match and correct Project before an append. Publish exactly one README-only commit by normal non-force push or equivalent expected-parent conditional ref update. Verify the remote HEAD, commit parent, changed-path set and exact bytes. If already present, parent differs, or publication uncertain, stop and reconcile without repeating.

After verified publication, post the leaf receipt in the worker's saved Project chat (leaf, predecessor, published SHA, exact line, readback, completion time, next action). Inspect scheduled tasks without changing unrelated tasks. There must be no other active trial timer; if uncertain, stop. Leaf 4 ends with no successor. For leaves 2 and 3, create exactly one permitted one-shot successor task, targeting five minutes after verified completion. Confirm its returned enabled/schedule status; report it in the same worker chat and stop. Do not wait or keep a worker running for the timer. The successor timer acts only as launcher, gets its complete private assignment from the task, and must not itself write Git or schedule a successor.

## Frozen launcher procedure (G2/G3 demonstrated)

Use Remote Desktop Commander in the existing signed-in Chrome session and the designated tab. The private payload supplies the observed Project URL and current designated chat route/window; do not guess or scan for a globally unique sidebar button. Verify designated tab's current route, Project breadcrumb and no draft or active generation. Navigate through the exact Project breadcrumb to the verified Project landing page; verify the route and unique visible project-specific composer labelled New chat in Automatic Timer Trial V1. Treat the actual UI placeholder as empty only when it matches the verified label; do not overwrite a draft. Set the exact assigned text through UIA ValuePattern, read back, find the unique enabled Send within the composer's scope, and InvokePattern once. Verify new distinct saved conversation route in the named Project and the exact submitted text (plus acknowledgement for diagnostic gates). Follow the G3 one-shot launcher procedure recorded in the private trial chat, with only the assignment and verified starting route/window substituted; if it cannot be recovered or preconditions fail, stop rather than invent a different mechanism. Read process output by PID if still available; reconcile the visible browser on output loss or ambiguous return, without another Send. No sidebar lookup, new identity protocol or persistent controller.

Private launcher payload must include: repository, branch, assigned leaf, exact expected parent SHA, governing files, one-line append instruction, one-commit and readback requirement, permitted successor instruction, verified Project route and designated tab anchor. The new worker receives the assignment, not permission to modify this plan. Record task scheduled/start/finish timestamps, launcher outcome, verified destination/posted prompt, and fresh chat evidence privately.

## Acceptance, recovery and handoff

Independently check each leaf's parent, README-only change, exact ordered prefix, remote publication and distinct saved in-Project conversation; check actual task run times and that only one successor is created. After leaf 4 inspect active trial timers and all three successor chat receipts. A completed task status is not a substitute for evidence. A lost receipt, incorrect route, early/late execution or missing approval is recorded with the precise distinction between functional and timing success. Stop at the first failed mandatory condition. Do not reset, force-push, blindly retry, skip a leaf, change architecture or advance from a claimed result. Reconcile current state before any authorised restart.

## Progress, surprises, decisions and retrospective

PROGRESS.md is the linked checkpoint and evidence ledger for these four living sections. Read it with this plan. During G4, the immutable README-only history and saved private receipts carry intermediate state; reconcile PROGRESS.md at a governance checkpoint or final review without adding commits between leaf executions. The plan and all gates are sufficient to resume with the current Git state and explicit private assignment, not undocumented assumptions from a prior conversation.

## Sources and methodology

OpenAI [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans), [Iterating Development Workflows with Codex](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex), and [Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex) support self-contained plans, limited scope, evidence-based milestone validation and current progress/decisions. The three-file layout is a project-specific adaptation, not an OpenAI requirement or a supported guarantee of this UI-based succession experiment. Sources reviewed 22 November 2026.
