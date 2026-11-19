---
name: start-chat-succession
description: Use when the owner invokes Chat Succession from iPhone or desktop to launch a bounded GitHub workload in their existing ChatGPT Project.
---

# Start Chat Succession

## My Cat and Dog from iPhone

When the owner asks to start the story in **My cat and dog** using the published `JayDEmily/my-cat-and-dog` guide, use this installed one-shot launcher. The request chat is the launcher. A new desktop chat in that Project will be worker 1. The launch uses no saved ID from the request chat.

Use connected Remote Desktop Commander on the authorized Windows PC. Start this PowerShell command once:

```powershell
& (Join-Path $env:LOCALAPPDATA 'ChatSuccession\MyCatAndDog\start.cmd')
```

If Desktop Commander returns a process ID before the receipt, read that process's output. The launcher confirms the first posted message and obtains the new saved chat ID before it starts the controller. A repeated request can report an existing run. Preserve an uncertain launch for read-only reconciliation and report its actual outcome. Leave all story writing to the desktop workers. The controller watches the four published turn branches and stops after Bluey's last line.

## Launch another GitHub workload

The invocation chat is a launcher. The fresh desktop chat becomes worker 1. Use the exact Project name from the owner's context. The phone conversation ID is unnecessary.

### Resolve the launch target

Resolve the exact owner-approved GitHub repository and branch from the chat context and repository. Use the nominated assignment or the published current assignment on the default branch when it is clear. Ask the owner only if the launch target remains ambiguous. The first desktop worker reads the repository's instructions, verifies what work the project currently authorizes, and reports any hold it finds.

### Send the private launch request

Use Remote Desktop Commander on the authorized Windows PC. Run this PowerShell expression to allocate a private request path:

```powershell
Join-Path $env:LOCALAPPDATA ('ChatSuccession/Requests/' + [guid]::NewGuid().ToString('N') + '.json')
```

Use Remote Desktop Commander's file write tool to save JSON at that exact returned path. Substitute the confirmed values for this run:

```json
{"repo":"OWNER/REPO","branch":"work/current","project_name":"Exact Project name"}
```

Optional fields are `max_unique_chats` (default five, or use the owner’s cap) and `project_url` when a verified ChatGPT Project landing link is available. With a name alone, the desktop looks for a saved chat in the exact Project's sidebar list. If the list is unavailable, use the verified landing link. Report any unresolved or ambiguous Project.

Start this PowerShell command once, substituting the actual absolute file path from the earlier command. Escape any apostrophe in the Windows path by doubling it inside the literal:

```powershell
& (Join-Path $env:LOCALAPPDATA 'ChatSuccession/start-project.cmd') --request 'ABSOLUTE_REQUEST_PATH'
```

Read the same process's output if it returns a PID ahead of the result. Report the actual verified desktop worker receipt or specific hold. Keep credentials, config and logs private on Windows. Repeat requests for the same target report or resume the existing run. For a subsequent run after that one ends, use a new checkpoint branch authorized by the project. Preserve any uncertain initial Send for read-only reconciliation.

### What each desktop worker publishes

The worker reads the nominated repo's own authority, chooses its authorized work and runs its normal verification. Its published work branch needs a tip commit with three trailers. `Chat-Succession-Run` identifies the private run, `Chat-ID` is the worker's saved ID from verified Windows state, and `Chat-Succession-Next` names the authorized next assignment or says `FINISHED`. This receipt belongs on the nominated branch using the repository's authorized write route.

Use the final `CHAT_STATUS: TASK_COMPLETE` line only after verifying publication. Use `CHAT_STATUS: NEED_MORE_TIME` for same-chat continuation and `CHAT_STATUS: ERROR` for an unresolved requirement, authorization hold, or unsuitable publication route. Only the single Windows controller sends automatic continuations and successors.

For the maintained startup guide and verified Astra scope, see [the Chat Succession repository](https://github.com/JayDEmily/chat_successor).
