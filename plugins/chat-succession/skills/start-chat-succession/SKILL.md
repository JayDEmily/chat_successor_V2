---
name: start-chat-succession
description: Use when the owner invokes Chat Succession to start a bounded GitHub workload in a ChatGPT Project, including the My Cat and Dog iPhone launch.
---

# Start Chat Succession

## My Cat and Dog from iPhone

When the owner asks to start the story in **My cat and dog** using the published `JayDEmily/my-cat-and-dog` guide, use this installed one-shot launcher. The request chat is the launcher. A new desktop chat in that Project will be worker 1. The launch uses no saved ID from the request chat.

Use connected Remote Desktop Commander on the authorized Windows PC. Start this PowerShell command once:

```powershell
& (Join-Path $env:LOCALAPPDATA 'ChatSuccession\MyCatAndDog\start.cmd')
```

If Desktop Commander returns a process ID before the receipt, read that process's output. The launcher confirms the first posted message and obtains the new saved chat ID before it starts the controller. A repeated request can report an existing run. Preserve an uncertain launch for read-only reconciliation and report its actual outcome. Leave all story writing to the desktop workers. The controller watches the four published turn branches and stops after Bluey's last line.

## Other workloads

For a supported workload with a verified desktop chat, treat that saved chat as worker 1. The owner points the plugin to the GitHub workload from the intended Project. Handle routine setup through the existing tools.

## Establish the workload and browser context

1. Resolve the exact owner-approved GitHub repository and branch. Use the nominated assignment or the published current assignment on the default branch when it is clear. Ask about the workload only if the repository leaves it ambiguous.
2. Read the repository's current instructions, applicable plan, verification commands and work boundaries. Treat the repository as the durable authority for progress, completion and the next task.
3. Positively observe the existing authenticated Chrome Project and this saved chat's identity. Obtain the actual Project ID and displayed name from the owner’s browser. Use Remote Desktop Commander when needed to reach the Windows desktop or owner-authorized Ubuntu environment. Use existing authenticated GitHub access and Ubuntu Git for repo operations. Preserve authentication, existing drafts and unrelated sessions.

## Start one controller when the workload is supported

Keep the controller checkout separate from the workload checkout. Verify that the installed controller accepts the nominated repo and branch and can read the job's published progress, last worker identity, completion flag and next task. The Astra fixture entry point uses `JayDEmily/chat_successor` and its published fixture state. When the target job needs the Stage C reader, identify the missing mapping before starting a controller or claiming automatic succession is ready.

If the context and published-state reader are supported, read the installed controller's integration README and CLI usage. On the tested Windows entry point the setup sequence is `init --config <private-json> --state <private-state> --initial-chat-id <observed-id>`, followed by `run --config <private-json> --state <private-state>`. Use the Windows Python runtime for the controller. Create a fresh run identity and private Windows configuration and state, unless inspection shows a matching controller is already running. Initialize against this saved worker, confirm count one and no pending action, then start one controller and verify that it is observing this chat. Prefer the owner's job policy. With no other cap, start with five distinct saved chats. Use the existing 20-second polling default and leave the response deadline unset unless configured.

Keep controller state in a private native Windows location. Log locally through the controller. Keep credentials, local paths and raw account transcripts out of the GitHub work record.

## Worker and successor contract

- Deliver the published assignment using the repository's normal checks. Commit and push through the authorized write route. Verify the publication from GitHub. Record actual work, the worker attribution and the next assignment or overall completion.
- End a verified published handoff with exactly one final line `CHAT_STATUS: TASK_COMPLETE`. Use `CHAT_STATUS: NEED_MORE_TIME` when another turn in this same saved chat is needed. Use `CHAT_STATUS: ERROR` and explain a blocker.
- The controller is the sole automatic sender. It uses the ordinary short repo and branch pointer for each successor. Successors read GitHub and continue that run. Only an explicit fresh owner start can initialize a new run.
- Keep pause, chat cap and terminal completion in force. For uncertain submissions, preserve the prepared or in-flight action and reconcile read-only. If a required tool, Project identity or published-state reader is missing, report the exact blocker and the last verified state before carrying out succession. Continue as a standalone worker only when the owner separately requests it.

For the maintained startup guide and verified Astra scope, see [the Chat Succession repository](https://github.com/JayDEmily/chat_successor).
