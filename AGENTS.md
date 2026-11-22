# Automatic Timer Trial V1 — operating instructions

## Authority and scope

Owner-authorised isolated experiment, 22 November 2026. Repository: JayDEmily/chat_successor_V2; branch: automatic-timer; ChatGPT Project: Automatic Timer Trial V1. Work nowhere else.

Every worker and launcher must explicitly read AGENTS.md, PLANS.md and PROGRESS.md at the live remote tip before acting (ChatGPT is not Codex and automatic AGENTS.md loading is not assumed). Use PLANS.md as the sole execution plan and PROGRESS.md as the checkpoint/evidence ledger. Read actual remote README.md and tip; do not reconstruct state from chat history or memory. A private handoff supplies exact assignment, predecessor SHA and verified Project route; it cannot expand authority.

## Execution discipline

- Execute only the assigned current gate or leaf, in order. Do not proceed beyond a failed or unverified mandatory precondition. Within authorised scope, resolve routine issues without asking for approval; stop for scope changes or unsupported actions.
- A worker performs exactly one leaf: append its prescribed README line, publish one non-force README-only commit, independently read back the remote tip and text, then arrange only its permitted successor. No return to or dependence on the prior worker. A launcher creates a fresh Project chat and submits its assignment once; never performs a Git leaf.
- Retain the demonstrated ordinary browser UI route, native scheduled task and Git publication mechanism. Do not invent parallel plans, new architecture, additional identity/authentication layers, services, controllers, databases or alternate launch routes. Do not change other branches, projects, chats, services or unrelated tasks.
- Only the owner may authorise changes to the governing plan or experimental variables. A governance session may edit these three documents under explicit owner authority; execution workers must not edit them. Record actual gate evidence and decisions in PROGRESS.md at governance checkpoints. During the README-only sequence, remote README/history and saved worker receipts are live evidence; PROGRESS.md is the last reviewed checkpoint, not a second mutable queue.
- Never retry an uncertain Send or publication. Reconcile via read-only evidence first. Report exact failed action, error, known state and next permissible check. A scheduler's completed status, a tool receipt, or Git history alone is insufficient evidence of successful fresh-chat delivery.
- Keep account identifiers, private Project/chat URLs, device identifiers and task identifiers out of repository content. Do not bypass scheduling, approval or platform restrictions. Preserve drafts and ongoing work.

## Fundamental scheduling semantics

This is completion-relative single-shot scheduling, not periodic scheduling. After verified completion of a non-final leaf, retire only the preceding trial timer (delete it if supported; an already disabled completed timer is retired for execution purposes), then request exactly one new non-recurring timer for five minutes after completion. No recurrence rule, fixed wall-clock cadence, simultaneous successor timers or timer after the final leaf. Do not reinterpret the five-minute delay as a recurring five-minute interval, or silently substitute an hourly delay. Individual one-shot acceptance is observed; permission for the complete autonomous sequence is not established merely by that observation. Respect actual platform frequency limits and approval requirements; do not use successive one-shot tasks to circumvent them. If unsupported, stop with the exact reason.

## Anti-drift lock

Before acting, identify the assigned leaf and its one next permitted action from PLANS.md. Execute that action using the frozen mechanism. Do not add a prerequisite, dependency, tool, architectural component or gate unless the existing plan requires it or the owner approves a specific change. Handoffs contain a short repository reference, leaf number, exact predecessor SHA and private destination inputs only. All implementation code and execution procedures reside in PLANS.md; never duplicate them in timers or require a previous chat or historical timer lookup. Respect platform restrictions and approval prompts. Verify the actual result, not gratuitous intermediate state. On failure isolate only that component, preserve completed work and stop where the existing plan requires. Do not interpret instruction adherence as authority to bypass platform limits.

## Methodology

Adapted from OpenAI's [AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md) and [execution plan guidance](https://developers.openai.com/cookbook/articles/codex_exec_plans). These are repository conventions for this experiment, not a guarantee of automatic instruction enforcement in ChatGPT. The current owner-approved scope governs any generic skill or example.
