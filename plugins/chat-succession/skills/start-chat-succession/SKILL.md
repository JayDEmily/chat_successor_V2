---
name: start-chat-succession
description: Use when the owner invokes Chat Succession in the first saved chat of a browser Project and supplies a GitHub repository or workload for a bounded succession run.
---

# Start Chat Succession

The owner creates a browser ChatGPT Project with a name of their choice, starts its first chat, and points this plugin to the GitHub workload. Treat this saved chat as worker 1. Handle routine setup through the existing tools.

## Establish the workload and browser context

1. Resolve the exact owner-approved GitHub repository and branch. Use the nominated assignment or the published current assignment on the default branch when it is clear. Ask about the workload only if the repository leaves it ambiguous.
2. Read the repository's current instructions, applicable plan, verification commands and work boundaries. Treat the repository as the durable authority for progress, completion and the next task.
3. Positively observe the existing authenticated Chrome Project and this saved chat's identity. Obtain the actual Project ID and displayed name from the owner’s browser. Use Remote Desktop Commander when needed to reach the Windows desktop or owner-authorized Ubuntu environment. Use existing authenticated GitHub access and Ubuntu Git for repo operations. Preserve authentication, existing drafts and unrelated sessions.

## Start one controller when the workload is supported

Keep the controller checkout separate from the workload checkout. Verify that the installed controller accepts the nominated repo and branch and can read the job's published progress, last worker identity, completion flag and next task. The tested Astra controller in `JayDEmily/chat_successor` is presently scoped to its own fixture repository and fixture state layout. When the target job needs the Stage C reader, identify the missing mapping before starting a controller or claiming automatic succession is ready.

If the context and published-state reader are supported, read the installed controller's integration README and CLI usage. On the tested Windows entry point the setup sequence is `init --config <private-json> --state <private-state> --initial-chat-id <observed-id>`, followed by `run --config <private-json> --state <private-state>`. Use the Windows Python runtime for the controller. Create a fresh run identity and private Windows configuration and state, unless inspection shows a matching controller is already running. Initialize against this saved worker, confirm count one and no pending action, then start one controller and verify that it is observing this chat. Prefer the owner's job policy. With no other cap, start with five distinct saved chats. Use the existing 20-second polling default and leave the response deadline unset unless configured.

Keep controller state in a private native Windows location. Log locally through the controller. Keep credentials, local paths and raw account transcripts out of the GitHub work record.

## Worker and successor contract

- Deliver the published assignment using the repository's normal checks. Commit and push through the authorized write route. Verify the publication from GitHub. Record actual work, the worker attribution and the next assignment or overall completion.
- End a verified published handoff with exactly one final line `CHAT_STATUS: TASK_COMPLETE`. Use `CHAT_STATUS: NEED_MORE_TIME` when another turn in this same saved chat is needed. Use `CHAT_STATUS: ERROR` and explain a blocker.
- The controller is the sole automatic sender. It uses the ordinary short repo and branch pointer for each successor. Successors read GitHub and continue that run. Only an explicit fresh owner start can initialize a new run.
- Keep pause, chat cap and terminal completion in force. For uncertain submissions, preserve the prepared or in-flight action and reconcile read-only. If a required tool, Project identity or published-state reader is missing, report the exact blocker and the last verified state before carrying out succession. Continue as a standalone worker only when the owner separately requests it.

For the maintained startup guide and verified Astra scope, see [the Chat Succession repository](https://github.com/JayDEmily/chat_successor).
