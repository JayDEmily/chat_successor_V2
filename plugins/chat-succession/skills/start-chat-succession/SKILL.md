---
name: start-chat-succession
description: Use when the owner invokes Chat Succession from iPhone or desktop to start or continue GitHub-backed work in a ChatGPT Project.
---

# Start Chat Succession

## Enter or re-enter from iPhone or desktop

Interpret the owner's current instruction using the conversation and the project's published work record. Invoking the plugin may mean starting, resuming or inspecting existing work. Discovery, planning, review and implementation are all possible assignments. Preserve explicit holds and independent review requirements. Carry an unambiguous approval only for its identified scope. Ask one focused question when the authority, target, or active executor remains ambiguous.

Use the exact Project name and GitHub repository. The phone conversation ID is unnecessary for a new job. Claim the current chat as the registered worker only when its saved identity is positively verified. If the invocation is elsewhere, route the instruction to the registered worker and leave execution to that worker. Account for other active executors and reconcile work published outside the run before proceeding.

### Resolve the launch target

Resolve the exact owner-approved GitHub repository from the conversation and repository. Inspect the saved run before choosing an operation. The worker applies the repository's rules for approval, work, verification, and publication.

### Send the private launch request

Use Remote Desktop Commander on the authorized Windows PC. Run this PowerShell expression to allocate a private request path:

```powershell
Join-Path $env:LOCALAPPDATA ('ChatSuccession/Requests/' + [guid]::NewGuid().ToString('N') + '.json')
```

Use Remote Desktop Commander's file write tool to save JSON at that exact returned path. Substitute the confirmed values for this run:

```json
{"operation":"inspect","repo":"OWNER/REPO","project_name":"Exact Project name"}
```

Use `project_url` when a verified ChatGPT Project landing link is available. Otherwise the desktop looks for the exact Project's sidebar list. Report unresolved or ambiguous identity. For starts, set the published entry `branch` and optionally `max_unique_chats` (default five).

Start this PowerShell command once, substituting the actual absolute file path from the earlier command. Escape any apostrophe in the Windows path by doubling it inside the literal:

```powershell
& (Join-Path $env:LOCALAPPDATA 'ChatSuccession/start-project.cmd') --request 'ABSOLUTE_REQUEST_PATH'
```

Read the same process output if it returns a PID first. Once you have the inspection result, choose the applicable operation and write a new private request.

| Operation | When to use it |
| --- | --- |
| `start` | No run exists, or inspection reports `run_stage: configured` after a known pre-Send hold. Supply `branch` and reuse the existing run ID when present. |
| `resume` | Use the selected `run_id` for a registered worker after the owner directs continuation. If inspection reports `initial_send_pending`, use resume without new context to reconcile the original Send. |
| `new` | A genuinely new authorized job after the prior run finished or reached its cap. Supply `branch`, a stable 24-character lowercase alphanumeric `job_id`, and the prior `run_id` when needed to select it. |

When the owner's current instruction is relevant and absent from the published work record, include `owner_context` with string fields `request_id` (24–64 lowercase alphanumeric characters), `instruction` (the actual current owner input), `scope`, and `pointer` (the project or proposal reference). For resume, add `worker_id` and `response_id` from the inspection's `response_anchor`. Reuse the same logical ID when retrying. Use observer-only resume for a positively identified worker that already received the input. When delivery is unclear, the launcher verifies the saved worker's turn before considering a Send. Set `release_pause` only when the owner explicitly releases a separate operator pause.

Use the controller receipt to report the outcome. Preserve uncertain sends and drafts. Keep credentials and private request data on Windows. A different branch or Project display name alone has no effect on which worker owns the run.

### What each desktop worker publishes

The worker follows the canonical handoff instructions it receives from the controller. It reads the project's actual authority, respects approvals and review roles, and verifies and publishes the scoped work through the project's normal route. Use any private owner-input pointer for this turn and record necessary authority in the project's own durable record. The receipt on the published branch uses `Chat-Succession-Run`, `Chat-ID`, and `Chat-Succession-Next`. On a different authorized branch, place `CHAT_HANDOFF_BRANCH: branch-name` immediately before the completion status.

Use the final `CHAT_STATUS: TASK_COMPLETE` line only after verifying publication. Use `CHAT_STATUS: NEED_MORE_TIME` for same-chat continuation and `CHAT_STATUS: ERROR` for an unresolved requirement, authorization hold, or unsuitable publication route. Only the single Windows controller sends automatic continuations and successors.

## Existing My Cat and Dog trial

When explicitly asked to use the original four-turn fixture for `JayDEmily/my-cat-and-dog`, run its existing Windows command through Remote Desktop Commander and read back that process's result.

```powershell
& (Join-Path $env:LOCALAPPDATA 'ChatSuccession\MyCatAndDog\start.cmd')
```

For the maintained startup guide and verified Astra scope, see [the Chat Succession repository](https://github.com/JayDEmily/chat_successor).
