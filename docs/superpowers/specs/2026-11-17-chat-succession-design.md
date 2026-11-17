# Chat Succession — exploration design

Date: 17 November 2026. Status: proposed technical design, published for owner review. Repository bootstrap/planning authorised; implementation not started.

## Intent

The owner wants work to continue through Chat 1, Chat 2, Chat 3 and onward. GitHub carries the assignment, evidence and next instruction between them. No chat needs to return to its predecessor. A user-created ChatGPT Project is a prerequisite and provides a known destination for fresh conversations.

The owner has created the blank Chat Succession Project. The screenshot shows “Chat succession folder”; the actual Project URL, signed-in Windows account/profile and available tools remain to be verified during setup. No Project configuration was changed for this planning publication.

## Goals and success

- Create genuinely fresh conversations inside that existing Project.
- Give each one a short, exact instruction pointing to an immutable GitHub assignment.
- Let each worker retrieve context independently, do only its assigned work and commit a result plus the proposed next assignment.
- Demonstrate three successive chats and two automatic handovers, ending after chat 3 with a GitHub completion record. The user may start chat 1 manually; that assistance is recorded. No copying prompts or intervening between chats 1–3 in a positive run.
- Separate transport success, task correctness and independent review.
- Make failures and stalled work inspectable in GitHub/local status, without needing to notify the original chat. The first trial relies on operator inspection; it provides no automatic stall detection or alert.

## Non-goals

Original-parent discovery, return-to-parent messaging, answer forwarding, arbitrary restart recovery, an official ChatGPT conversation API, an extension rewrite, open-ended autonomous execution and NVIDIA product operations. Existing Second Chat OCR work continues independently.

## Approaches to evaluate

1. **Worker launches its successor.** Each chat publishes its handover, then invokes the Windows launcher. Closest to the observed NVIDIA method and fewest new runtime components. A worker can stop between commit and launch; each worker also needs the launch tool.
2. **GitHub watcher launches successors.** Workers only publish ready handovers. One local process notices them, records an attempt and opens the next chat. This separates task execution from launch scheduling, but introduces a small persistent process and GitHub polling/authentication.
3. **Manual successor launch.** Useful as an explicitly assisted diagnostic baseline. It cannot satisfy the automatic-handover goal.

**Agent recommendation, not an owner-selected implementation:** start with a reusable Windows UIA launcher and a finite worker-launched chain. After observing it, evaluate the watcher against the actual commit-to-launch gap. Do not build both orchestration systems in advance. The existing OCR architecture is neither imported nor superseded by this proposal.

## Durable records

Use one isolated branch per experimental run, identified by a run ID. Record its fixed three-step budget and exact first assignment before launching. Only the current assigned step may produce its result and proposed successor packet on that run branch; serialise updates using the expected branch head. A conflicting update stops advancement.

Proposed layout:

```text
runs/<run-id>/run.json
runs/<run-id>/steps/001/assignment.json
runs/<run-id>/steps/001/result.json
runs/<run-id>/steps/001/handover.json
runs/<run-id>/steps/002/assignment.json
```

Each assignment contains schema version, run/step IDs, expected role, task, allowed paths/operations, predecessor result commit (null for step 1), required output paths and whether it is terminal. It points to any larger brief in the same pinned commit. A result names its exact assignment commit, outcome (`completed`, `blocked` or `failed`), changed paths, checks and unresolved issues.

A handover names the existing result commit and next assignment path/step, or marks the run complete. Publish results first, then a handover referencing that existing commit. The next assignment and handover may share a later commit; the launcher resolves that commit and passes its exact SHA to the successor. A file never claims to contain its own eventual commit hash.

The child prompt identifies repository, run, step, immutable assignment SHA/path and role. “Look at GitHub” describes the concept; ambiguous “latest work” discovery is not the targeting protocol.

## Launch boundary

Reuse the demonstrated path: Remote Desktop Commander → Windows PowerShell → UIAutomationClient/Win32 → existing authenticated Chrome → known Project. Reinspect the live target, preserve occupied drafts, type with exact readback, submit once and verify the posted user message and resulting conversation identity. The new chat must differ from prior chats. A blank window alone does not establish a saved conversation.

One small local launch journal has a unique key `(run_id, next_step)` and stores an immutable assignment commit plus attempt state before any possible browser effect. A different assignment SHA for the same run/step is a conflict, never a new launch. Initialise the journal explicitly before admitting a run; missing or unreadable state after admission holds the run and must not create a fresh empty journal. An uncertain effect holds that launch key for inspection; automatic retry is forbidden. This journal covers browser actions; GitHub remains authoritative for work instructions/results. Local storage cannot atomically commit a ChatGPT Send.

Conversation URLs may be captured as diagnostic receipts. They are not parent bindings and are not needed for the next task's context. Keep account-specific receipts local; commit a redacted evidence summary.

## Completion and progression

For succession, readiness is a valid committed result and handover, not a heuristic about whether ChatGPT's UI has stopped generating. Publish the handover only after work and checks finish and the relevant commit is verified. Launching a successor is the predecessor's final workflow action; it must perform no further task mutations afterwards.

This is a procedural boundary initially. A handover can be incorrect or premature, and a chat may still be displaying a reply after publication. Claims of process quiescence require evidence; a GitHub record alone does not prove it. Restrict each step to its assigned paths and use an independent review step for the toy output.

A watcher, if selected later, validates the run/branch, assignment/result lineage, permitted next step, remaining budget and prior launch journal before acting. Failed/blocked results, invalid records and terminal steps do not trigger successors. It never uses arbitrary repository text as a shell command.

## Bounded first experiment

Chat 1 writes a deterministic toy result. Chat 2 independently verifies it and records accept/return. Chat 3 verifies the two predecessors and writes a final summary, with no fourth assignment or launch. All changes stay in this repository's disposable run branch. A return or failure ends the run rather than creating a repair loop.

No parent message or original iPhone URL is supplied to the launcher. Demonstrate continuity from pinned GitHub context alone. The first experiment does not certify sustained reliability.

## Open decisions and assumptions

- Owner review chooses worker-launch first or watcher-first; recommendation above remains a proposal.
- Capture the actual Project URL privately; verify Remote Desktop Commander and Git read/write tools are available in each fresh chat. Project membership alone does not prove tool availability.
- Use private repository visibility and Windows UIA initially (agent defaults). Revisit only for an observed obstacle.
- Initial maximum is three chats, serial execution, one run, one browser submission attempt per step; no automatic recovery. The live run needs a specific bounded execution assignment.
- Preflight also verifies the exact Windows Python executable and journal invocation path with an offline reserve/readback check. Normal operation assumes an awake Windows PC, authenticated Chrome and working tool connection. A stalled run has a named operator and a reported held state; no automatic rescue is promised.

## Stop and acceptance

Stop on ambiguous target, occupied draft, payload mismatch, uncertain Send, conflicting GitHub head, missing tools, failed work, step-budget exhaustion or owner stop. Record the first missing boundary. Existing work is preserved.

Accept only the observed scope: exact assignments received by three distinct Project conversations, correct result lineage, two verified automatic handovers, terminal completion and no fourth launch. Independent evidence review decides whether the next experiment is justified.
