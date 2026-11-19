# Chat Succession

Chat Succession carries a GitHub-backed job through successive ChatGPT conversations in one Project. Each worker reads the current assignment from GitHub, publishes its work there, and leaves the next worker a short repo and branch pointer.

## My Cat and Dog iPhone trial

In the **My cat and dog** Project on your iPhone, choose the personal **Chat Succession** plugin and say:

> Start the My Cat and Dog story from the GitHub instructions.

The request chat starts the installed Windows launcher through Remote Desktop Commander. Chrome opens a fresh chat in the same Project. Once the exact first message and its saved chat ID are verified, that desktop chat becomes worker 1. Each worker publishes one new branch based on the preceding turn. The controller verifies the published line and the worker's Git commit trailer before starting a successor. After four turns the controller stops. [Story instructions](https://github.com/JayDEmily/my-cat-and-dog/blob/main/README.md)

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

Astra’s bounded Windows Chrome and GitHub integration is verified through G4. The controller accepts Astra test fixtures and the bounded My Cat and Dog branch chain. The personal plugin supplies the startup instructions and uses the owner’s existing tools.

**Stage C is still to be commissioned for ordinary workloads.** Each new workload needs a compatible repository reader. It must map the job’s published progress to the last worker, whether the overall job is complete, and the next assignment. The starter reports an unsupported workload before starting its controller.

- [Astra gates and leaves](docs/astra-succession/README.md)
- [Validation results and handoff](PROGRESS.md)
- [Controller operations](integration/README.md)
- [Personal plugin source](plugins/chat-succession/)
