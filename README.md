# Chat Succession

Chat Succession carries a GitHub-backed job through successive ChatGPT conversations in one Project. Each worker reads the current assignment from GitHub, publishes its work there, and leaves the next worker a short repo and branch pointer.

## Start from a browser Project

Once the owner’s GitHub and Remote Desktop Commander access is connected, the intended setup is two steps per run.

1. Create a ChatGPT Project in your browser. Choose any name.
2. Open its first chat, select the personal **Chat Succession** plugin, and point it at the GitHub workload.

Paste this into that first chat:

> Start Chat Succession for `OWNER/REPO`. Use the current published assignment in that repository.

Include a branch or a link to the specific assignment if the repo has several active workloads. If the published assignment is clear on the default branch, the repo alone is enough. That first conversation is worker 1.

## What the starter handles

- **Find the work.** Use the owner-approved GitHub repo and branch. Read the repo’s instructions and current assignment, then identify where it publishes progress, what comes next, and when the overall job is complete.
- **Connect the run.** Use the existing authenticated Chrome session and the actual saved Project chat ID. Use Ubuntu for Git operations and Remote Desktop Commander where access to Ubuntu or Windows is needed. Start one Windows controller with private run state. The shared controller stays in its own checkout.
- **Work and hand off.** Worker 1 does the assigned work, runs the repo’s ordinary checks, publishes to the nominated branch, and verifies the published result. Every successor receives the short repo and branch pointer and reads the current assignment from GitHub. The controller owns all automatic continuation and successor sends.
- **Stop cleanly.** The controller honors the configured chat cap and owner pause. At the first setup, the existing defaults may be used when no job policy overrides them. A bounded starter cap of five is the template default, polling is every 20 seconds, and the optional response deadline is unset.

| Worker’s final status | Controller action |
| --- | --- |
| `CHAT_STATUS: NEED_MORE_TIME` | Continue useful work in the same saved chat. |
| `CHAT_STATUS: TASK_COMPLETE` | Verify the published result and current job state. Open one successor if work remains and the cap allows it. Stop if the job is complete or the cap is reached. |
| `CHAT_STATUS: ERROR` | Hold and surface the blocker. |

Use one status on its own final line. For `TASK_COMPLETE`, complete and verify the GitHub publication first. If a Send outcome is unclear, preserve the run state and reconcile it read-only before another attempt.

## What works today

Astra’s bounded Windows Chrome and GitHub integration is verified through G4. The current controller accepts the Chat Succession test repository and reads test-fixture state from `succession-tests/<run-id>/STATE.json`. The personal plugin supplies the reusable startup instructions and uses the owner’s existing tools.

**Stage C is still to be commissioned.** A different GitHub repo or an ordinary job needs a compatible repository reader. It must map the job’s existing published progress to the last worker, whether the overall job is complete, and the next assignment. Until that connection is available and verified, the starter reports the specific setup gap before starting an automatic handoff. The eventual real-job trial uses the job’s own workload and checks.

- [Astra gates and leaves](docs/astra-succession/README.md)
- [Validation results and handoff](PROGRESS.md)
- [Controller operations](integration/README.md)
- [Personal plugin source](plugins/chat-succession/)
