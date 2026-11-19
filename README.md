# Chat Succession

Chat Succession carries a GitHub-backed job through successive ChatGPT conversations in one Project. Each worker reads the current assignment from GitHub, publishes its work there, and leaves the next worker a short repo and branch pointer.

## My Cat and Dog iPhone trial

In the **My cat and dog** Project on your iPhone, choose the personal **Chat Succession** plugin and say:

> Start the My Cat and Dog story from the GitHub instructions.

The request chat starts the installed Windows launcher through Remote Desktop Commander. Chrome opens a fresh chat in the same Project. Once the exact first message and its saved chat ID are verified, that desktop chat becomes worker 1. Each worker publishes one new branch based on the preceding turn. The controller verifies the published line and the worker's Git commit trailer before starting a successor. After four turns the controller stops. [Story instructions](https://github.com/JayDEmily/my-cat-and-dog/blob/main/README.md)

## Start a GitHub workload from iPhone or desktop

Once the owner’s GitHub and Remote Desktop Commander access is connected, the intended setup is two steps per run.

1. Open or create a ChatGPT Project. Choose any name for a new Project.
2. In a chat in that Project, select the personal **Chat Succession** plugin and point it at the GitHub workload.

For example, you can say

> Continue this project using Chat Succession.

After the Project chat has identified a decision for you, select the same
plugin and respond naturally, for example “I approve.” The plugin uses the
conversation to carry that scoped decision to the saved run. If the current
worker already received it, the controller resumes watching that worker.

Include the repo and branch if they are unclear from the chat. The request chat uses Remote Desktop Commander to open authenticated desktop Chrome in the same Project. That fresh, saved chat is worker 1. Keep the Windows desktop session and its Ubuntu GitHub access available while the controller runs. If Chrome cannot find the Project by name in its sidebar, use its verified Project landing link.

## What the starter handles

- **Find the work.** Each worker reads the nominated repository's instructions, progress and current assignment. The worker applies that project's own rules for approval, branching, verification and publishing.
- **Connect the run.** The starter verifies the saved desktop chat in the chosen Project, then starts one Windows controller with private run state. It uses Ubuntu for the GitHub readback. An existing run retains its worker and chat cap if the Project name or checkpoint branch changes. A genuinely new job can reuse an earlier branch.
- **Work and hand off.** After authorized verification and publication, the worker puts the handoff receipt at the tip of the nominated branch. The controller verifies the receipt and sends a repo and branch pointer to the next worker. The next worker reasons from the project's current instructions and agreement with the owner.
- **Stop cleanly.** The controller honors the configured chat cap and owner pause. At the first setup, the existing defaults may be used when no job policy overrides them. A bounded starter cap of five is the template default, polling is every 20 seconds, and the optional response deadline is unset.

| Worker’s final status | Controller action |
| --- | --- |
| `CHAT_STATUS: NEED_MORE_TIME` | Continue useful work in the same saved chat. |
| `CHAT_STATUS: TASK_COMPLETE` | Verify the published result and current job state. Open one successor if work remains and the cap allows it. Stop if the job is complete or the cap is reached. |
| `CHAT_STATUS: ERROR` | Hold and surface the blocker. |

Use one status on its own final line. For `TASK_COMPLETE`, complete and verify the GitHub publication first. If a Send outcome is unclear, preserve the run state and reconcile it read-only before another attempt.

## The shared handoff receipt

The generic controller reads three Git commit trailers on the published checkpoint branch. The worker's prompt tells it where to obtain the run ID and its saved desktop chat ID.

```text
Chat-Succession-Run: <run ID>
Chat-ID: <saved desktop chat ID>
Chat-Succession-Next: <authorized next assignment or FINISHED>
```

Use the repository's normal publication route. For a different authorized checkpoint branch, place `CHAT_HANDOFF_BRANCH: work/example` immediately before `CHAT_STATUS: TASK_COMPLETE`. The controller advances to that branch only after verifying the receipt. If there is an owner hold, no authorized assignment, or no approved way to publish, the worker reports `CHAT_STATUS: ERROR` and the controller holds.

Astra is verified through G4. The My Cat and Dog iPhone trial finished four workers and three automatic handoffs. The generic launcher passed a desktop Chrome preflight and simulated handoffs against real Git commits. The first generic run on a live workload remains to be done.

- [Astra gates and leaves](docs/astra-succession/README.md)
- [Validation results and handoff](PROGRESS.md)
- [Controller operations](integration/README.md)
- [Personal plugin source](plugins/chat-succession/)
