# Chat Succession Exploration Plan

> For agentic workers: after owner review of the proposed design, use superpowers:executing-plans to carry out the assigned task. Do not start implementation from this planning publication alone.

**Goal:** test whether fresh ChatGPT conversations can continue a finite workflow through GitHub without returning to an original chat.

**Architecture:** a known, user-created ChatGPT Project supplies the destination. Immutable GitHub packets supply context; a small Windows UIA launcher supplies transport. Compare worker launch with a watcher after the first bounded proof.

**Tech stack:** Git/GitHub, existing Windows Chrome and Remote Desktop Commander; PowerShell UIA for the first launcher; local standard-library SQLite if a durable launch journal is implemented. No new extension assumed.

**Spec:** [exploration design](../specs/2026-11-17-chat-succession-design.md).

## Global constraints

- Planning publication only; no live launch or installation performed here.
- Existing user-created Chat Succession Project; actual URL privately verified during setup.
- GitHub holds durable instructions/results; no original-parent discovery or return notice.
- One isolated run branch, serial steps, maximum three fresh chats and two automatic handovers.
- One submission attempt per launch key; uncertain effects hold for inspection.
- No changes to NVIDIA, Second Chat OCR or the original Second Chat installation.
- Exact pinned assignment and allowed paths; no implicit production work or merge.

## Review focus

1. Wrong Project or unavailable successor tools: preflight must stop before a run (Task 1).
2. Duplicate launch after a lost acknowledgement: durable reservation blocks repetition (Task 2).
3. Premature, stale or conflicting handover: pinned lineage and path checks stop progression (Tasks 1–3).
4. Completed UI reply mistaken for successful task: GitHub result and independent review remain separate (Task 3).
5. Terminal step accidentally launches a fourth chat: fixed budget enforced and observed (Tasks 2–3).

## File responsibilities

Existing planning files describe intent, tasks, provenance and progress. Proposed implementation paths below do not exist yet:

- `protocol/README.md`, `protocol/examples/`: packet fields and literal three-step toy assignments.
- `tools/validate_packet.py`: validate run, result and next-assignment lineage without browser effects.
- `launcher/launch.ps1`: exact Project targeting, input/readback, one Send, delivery receipt.
- `launcher/journal.py`: launch-key reservation and status only.
- `tests/test_protocol.py`, `tests/test_launch_journal.py`: meaningful offline negative cases.
- `runs/<run-id>/`: actual task packets/results; redacted evidence summaries in `evidence/<run-id>/`.
- `docs/EXPERIMENT_REPORT.md`: observed results and recommendation on orchestration.

### Task 1 — freeze the first experiment and verify prerequisites

Produces: packet contract/examples, setup receipt and a specific executable trial proposal. No chat Send.

- [ ] Review the design with the owner and select worker-launch or watcher-first. If watcher-first is selected, revise Task 2 before implementation; do not silently add a daemon.
- [ ] Record the actual Project browser URL/profile privately; verify Project identity and available Git read/write/remote tools in a normal fresh-chat setup. Any assisted setup is recorded and not counted as an automatic handover. Verify an explicitly configured Windows Python executable and journal invocation path with an offline reserve/readback check.
- [ ] Define `run.json` (run ID, branch, maximum_steps=3, Project configuration reference, stop state) and assignments/results/handovers with the fields in the spec. Add exact toy task and reviewer instructions; no ambiguous “latest” lookup.
- [ ] Implement `validate_packet(repo_dir, run_id, step, assignment_sha) -> validation result` in `tools/validate_packet.py`. Read Git objects at exact SHAs; reject wrong run/step/role, missing predecessor, out-of-scope changed paths, blocked/failed predecessor, conflicting run branch and a successor after step 3.
- [ ] First add failing tests for each rejection plus one valid chain; run `python -m unittest discover -s tests -v`, implement the validator, then rerun. Commit and independently read back the exact remote files/SHA.
- [ ] Update PROGRESS.md with prerequisites, chosen launch approach and any unresolved tool availability. No implementation completion inferred from a setup screenshot.

### Task 2 — reusable bounded launch mechanism

Depends: Task 1 and the selected technical design. Produces: launcher, durable launch journal and offline evidence. Actual browser draft/Send checks require the separately scoped trial assignment.

- [ ] Specify `reserve_launch(run_id, step, assignment_sha) -> reserved|held` and `record_launch_outcome(key, state, receipt)` in `launcher/journal.py`. States: reserved, posted, effect_unknown, blocked. The unique key is `(run_id, step)`; store assignment_sha as immutable data and reject a different SHA for an existing step. An existing reservation never grants a second attempt; no automatic reset. Initialise explicitly before run admission; missing/unreadable journal after admission holds rather than creates a new store.
- [ ] Add tests for duplicate/concurrent reservation, crash after reservation, lost acknowledgement, terminal step, mismatched assignment and journal loss. Run them failing, implement the minimal SQLite journal, then run `python -m unittest discover -s tests -v`.
- [ ] Implement `launcher/launch.ps1` accepting a configured Project URL, run/step/assignment identity and exact prompt. Validate the packet and reserve before opening a window; inspect fresh UIA elements, focus, preserve drafts, type/read back exactly, submit once and verify delivery. Reacquire elements after typing; encode SendKeys characters correctly or reject unsupported payloads before any input.
- [ ] Record outcome to the journal. If a tool timeout or post-Send readback fails, mark unknown/retain reservation; inspect without another Send. Treat UI-post observation and fresh-load persistence as separate evidence fields.
- [ ] Verify PowerShell parsing and offline guards. During the bounded live trial, prove exact draft readback, one posted prompt, Project placement and a new conversation identity. Do not label offline tests as live validation.
- [ ] Commit source before live use; record exact source hash, invocation and redacted outcome. Leave existing installed scripts unchanged.

### Task 3 — run one three-chat succession experiment

Depends: Tasks 1–2, verified tools/Project and explicit bounded trial assignment. Produces: one isolated run branch and observed evidence.

- [ ] Freeze the run ID, first assignment SHA, exact toy outputs, Project destination, launcher revision, one-run/three-chat budget and operator before launch. Record whether the user starts chat 1 manually.
- [ ] Chat 1 reads the pinned task, writes the toy result, commits/pushes/verifies it, then publishes the next assignment/handover referencing that existing result commit. As its final workflow action, invoke one successor launch.
- [ ] Chat 2 independently reads its exact assignment and predecessor result. Verify correctness and scope; commit accept/return. Only accept permits publication and launch of the third assignment; return/blocked/failed ends the run.
- [ ] Chat 3 independently verifies predecessor lineage and writes the terminal summary. Publish terminal handover with no successor. Confirm no launch reservation or conversation was created for step 4.
- [ ] Capture redacted receipts proving three distinct conversations in the Project, exact posted instructions and immutable assignment/result lineage. No original-parent URL or return message is used. Record any manual rescue as failure of the unassisted claim.
- [ ] Independently fetch all result commits and compare changes with each assignment's allowed paths. Task correctness, launcher delivery and chain completion receive separate verdicts. Update PROGRESS.md with actual outcomes, including failed attempts.

### Task 4 — assess interruptions and choose ongoing orchestration

Depends: Task 3's report, even if the experiment fails. Produces: a grounded recommendation, not automatic expansion.

- [ ] In offline fixtures, exercise commit-before-launch interruption, duplicate worker invocation, stale handover and unknown Send. Verify retained state prevents automatic duplicate effects. Do not induce additional live Sends under the original run budget.
- [ ] Compare worker-launch and watcher based on observed failure points, launch-tool availability and handover latency. Initial worker-launch trials have operator-inspected status only; automatic stall detection/alerting would require a later monitor or watcher. A GitHub-ready record replaces UI-finality inference only for scheduling; it does not prove an old process has ceased all activity.
- [ ] Write `docs/EXPERIMENT_REPORT.md`: evidence links, actual limits, manual interventions, failures, proposed next experiment and recommendation. Identify any need for a small watcher rather than presuming one.
- [ ] Review the report independently before accepting any reliability claim. A longer chain, watcher implementation, restart recovery or continuous service is a subsequent scoped assignment.

## Current execution boundary

Repository creation and planning are complete only when their remote commit is verified. Tasks 1–4 remain NOT STARTED. The owner reviews the concrete design/plan before implementation; this repository does not alter the running OCR project or initiate a live chain.
