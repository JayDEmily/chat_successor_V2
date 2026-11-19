# Chat Succession — generic entry and re-entry implementation plan

**Date:** 19 November 2026

**Audience:** the model implementing the next increment

**Status:** evidence reviewed and baseline reproduced; changes below are **not implemented or live-verified**.

**Suggested repository home:** `docs/astra-succession/generic-entry-plan-20261119.md`. Point the current assignment here without rewriting the historical G0–G4 results.

## 1. Decision

Make the existing plugin a **state-aware entry point into Chat Succession**, rather than an unconditional fresh-worker launcher.

The model should work out what the nominated project currently authorizes—discovery, planning, review, implementation, recovery, further work, or nothing—and enter the existing succession methodology at that point. These are examples for reasoning, **not a new lifecycle enum or project-state engine**.

Keep the present division of responsibilities:

- **Entry model:** understand the owner's current request in context; resolve the project, workload and any approval scope; locate the existing run.
- **Worker model:** read the project's own authority and current durable work; perform the authorized activity, use its normal verification/publication route, and publish the next handoff.
- **Existing controller:** own automatic Sends, saved-chat identity, count, deduplication, pause/recovery and receipt checks. It must not become a project planner or approval classifier.

The necessary code changes are narrow: locate a run independently of its changing branch; deliver an owner-directed continuation through the existing sender when necessary; and let a verified handoff move to an authorized publication branch. Better instructions connect those mechanisms.

**Do not ship only an “I approve → clear halted” patch.** That neither wakes an idle worker nor repairs a changed publication route. Equally, do not build a generic workflow platform.

### The intended owner experience

In the relevant Project, the owner selects the same plugin and speaks naturally:

> Continue this project using Chat Succession.

Or, after an unambiguous proposal:

> I approve.

The owner should not need to name an internal resume operation, locate a Windows state file, copy a handover, create a special branch, or repeat an approval already given. Ask one focused question only where the target, scope, active executor or required project authority really remains ambiguous.

**The implementation gates below are engineering acceptance checks, not new runtime approval ceremonies.**

---

## 2. Independent assessment

### What the evidence establishes

| Finding | Consequence |
|---|---|
| The supplied baseline's **35 integration tests and 119 reference tests pass again** in this review. The supplied approval reproduction also passes. Six additional baseline probes reproduce the entry/resume gaps. These are offline results, not Windows/iPhone reruns. [E1] | Preserve the working transport; add the missing cases rather than restarting the feasibility investigation. |
| The story evidence records four saved workers, three automatic successors and `STOP_FINISHED` on **19 November 2026**. A/B/F establish the earlier bounded five-chat acceptance. L14 remains `NOT_RUN`; several other cases were controlled injections or assisted recoveries. [E2] | These successes are real evidence for their stated scope, not proof of generic post-approval continuation. |
| The Rowing controller held at **15:08:56 Sydney time, 19 November 2026**, after `ERROR`. It retained one worker, no pending Send, zero successors and zero publication checks. [E3] | The initial hold is consistent with the protocol. The supplied Rowing authority files are absent, so this review cannot independently decide whether that worker interpreted the assignment correctly. |
| A later approval/work continuation is reported, but the supplied records do **not establish whether that conversation was the saved worker or another chat**. The old controller stayed stopped; its later desktop read still showed the old response. [E3] | Do not diagnose a proven cross-chat mix-up, a proven synchronization defect, or a proven second writer. Resolve identity on re-entry. |
| Repeating the same launch returns `existing_run` when halted. CLI `resume` clears a hold but sends nothing; the consumed old `ERROR` remains ignored. The old L03 live recovery explicitly included an operator-posted recovery message. [E4, E5] | A working observer-resume primitive exists. A complete contextual owner-continuation path does not. |
| The launch key hashes **repo + branch + Project display name**. Another branch selects a fresh run, even when the old run is nonterminal. A changed display name can do the same despite an unchanged Project URL. [E4, E1] | Branch/display-name changes must not implicitly create another executor or reset the chat budget. |
| The generic reader requires the three receipt trailers at the nominated branch tip. The new Rowing checkpoint was on another branch and had **none** of those trailers. [E6, E7] | Resuming the old observer alone could not make that checkpoint a valid handoff. Neither a branch name nor published work alone is a completion receipt. |
| Seven staged EOF-blank-line diagnostics preceded publication; the committed patch retained all seven. Clean staged/unstaged checks after committing did not test that committed patch. The old controller had already stopped and used a separate bare reader. [E3, E7, W1] | Do not attribute the file contents to the controller or claim concurrency was proved. The writer remains unknown. Do not add a whitespace-cleaning controller or weaken project checks. |

### Why the passing checks missed the objective

The supplied tests establish specific routing, state-machine and publication behavior. They do not establish that a natural owner decision in an arbitrary project is carried to the right worker, with its scope intact, followed by resumed automatic succession. Some generic tests explicitly assume a fixed branch. The diagnostic reproduction deliberately demonstrates the old changed-branch bootstrap behavior. [E1, E4–E6]

**Instructions are the first fix; the small transport changes make those instructions executable.** The plugin currently describes the invocation as a launcher, does not carry an owner-context field, and tells the owner to nominate a different branch for a subsequent run. Its “report or resume” wording exceeds what the held-run path actually does. [E4]

---

## 3. Boundaries to preserve

1. One registered current worker and one controller Send owner per selected workload/run. Do not silently adopt the invocation chat or the newest visible chat.
2. Keep the three worker statuses: `NEED_MORE_TIME`, `TASK_COMPLETE`, `ERROR`. Keep explicit final-line parsing. Natural-language understanding belongs in the entry/worker instructions, not an automatic semantic-completion classifier.
3. Preserve observed chat IDs, count, consumed responses, pending actions and terminal stops. An owner continuation does not consume another chat.
4. Preserve the existing `prepared → sending → confirmed/uncertain` path, draft/attachment checks, owner pause and read-only reconciliation. Never retry a possibly submitted message.
5. GitHub remains the durable **work and successor-handoff** record. Private Windows state remains transport bookkeeping. A small private owner-input bridge is not an alternative work ledger.
6. Project rules decide approvals, branches, independent review, allowed writes and useful-work verification. Receipt metadata is transport attribution, not proof of semantic correctness or independent review.
7. Do not require every repository to have `STATE.json`, `RUN.json`, `AGENTS.md`, leaves/gates, or any particular progress filename. Read what actually governs that project.
8. No new daemon, second sender, scheduler, global workspace cleanup, project-specific reader, universal approval schema, forced Git rewrite, or automatic adoption of an external writer. Do not reopen the completed historical gates or require a 30-chat trial.

**Supported boundary:** this remains a GitHub-backed workflow with an authorized way to publish a handoff. A project with no permitted publication route may legitimately hold. “Generic” means its existing rules are respected, not bypassed.

---

## 4. Leaves and gates

Use repository-relative implementation paths below; the supplied archive prefixes them with `source/`. `KIT` below means:

```text
astra/2026-11-17/unpacked/chat_succession_test_kit_20261117
```

| Gate | Leaves | Exit |
|---|---|---|
| **G0 — Evidence and contract** | Read sections 1–3 and the cited source functions | Baseline understood; working branch/installed version identified; no speculative Rowing diagnosis. The sandbox review satisfies the supplied-source baseline, not deployment verification. |
| **G1 — Generic entry implemented offline** | L1 → L2 → L3 → L4 | Existing 35/119 suites pass, new regressions pass, old-state migration/restart tests pass, and prompt cases show no project-specific assumptions. |
| **G2 — Installed bounded acceptance** | L5 | Two different project situations exercise actual entry/re-entry and useful published work, including an automatic post-approval successor and authorized branch rotation. Report any unrun capability explicitly. |

Implement the leaves in order. Commit coherent changes and record actual results plus the next action in the existing `PROGRESS.md`. Do not request a fresh owner approval between leaves unless the repository already requires it.

### L1 — Make entry and worker instructions genuinely re-entrant

**Primary files**

- `plugins/chat-succession/skills/start-chat-succession/SKILL.md`
- `integration/repo_reader.py::GitHandoffReader.instructions`
- `README.md`, `integration/README.md`, and the current-assignment pointer in `docs/astra-succession/README.md`
- Plugin description/default prompts in `plugin.json` and `agents/openai.yaml`

**Implement**

Put generic entry first. Keep the story shortcut as a backwards-compatible example, not the conceptual template for all projects. Edit this contract first, but do not deploy a skill that advertises the new operations until their backend is implemented.

Teach the invocation model to resolve the current owner intent from the conversation plus published project authority. Inspect the existing run before deciding to bootstrap. Carry a concise, explicit scope when the owner's latest decision is not yet in the repository. Do not make another conversational executor start implementing while a registered worker owns the job.

Use this substance in the skill, adapted to its actual commands:

> Enter or re-enter Chat Succession for the owner's current GitHub-backed work. Do not assume that invoking this skill means a new run, implementation work, or a new approval requirement. Read the relevant project context and inspect the saved run. Resolve the owner's intent and scope using the conversation and the project's published instructions. An unambiguous “I approve” is an instruction about that identified scope; it is not approval of every future task.
>
> Reuse the verified current worker when a run exists. If this conversation is positively identified as that worker, continue in the worker role and resume observation without sending another instruction to yourself. Otherwise act as the request router: pass any needed owner decision to the registered worker through the controller, and do not perform the project work here. Never infer worker identity merely from membership in the same Project.
>
> For a new run, launch one fresh saved worker in the nominated Project. For an existing run, reconcile or resume it using the saved state. A different branch is not a request for another worker. Ask only for genuinely unresolved scope, authority or identity.

Use one canonical worker instruction builder for bootstrap, successors and owner re-entry. Its project-facing substance should be:

> Read the nominated repository's current instructions and work record, following their pointers to the applicable assignment. Determine the activity currently authorized. Continue useful work already in progress; perform planning, discovery or review when that is the authorized task; do not implement merely because the plugin was invoked. Respect completed work and explicit holds.
>
> Apply the owner's scoped instruction when it is available, and record a newly supplied decision in the project's normal durable record when its rules require it. Do not invent extra approvals or waive existing independent-review requirements. Use the project's branch and publication conventions; the incoming branch is the entry point, not a command to overwrite it.
>
> Before handing off, publish verified work, current progress and the authorized next step. Use the existing receipt and one final status. If useful work can continue in this chat, use NEED_MORE_TIME. If this slice is published and ready for handoff, use TASK_COMPLETE. If a real decision, tool or publication blocker prevents progress, explain the smallest required resolution and use ERROR. Only the controller launches successors.

Add the concrete run/worker identity and receipt details through the existing builder, rather than duplicating long variants in the skill.

**State examples, not additional workflow states**

| Situation discovered by the model | Expected behavior |
|---|---|
| Instructions authorize discovery but no implementation task exists yet | Do that discovery; do not invent a missing-assignment blocker solely because a familiar file is absent. |
| A proposal genuinely requires owner approval | Explain the specific proposal/decision and hold; do not manufacture authorization. |
| That exact proposal is already approved in the current request | Apply/carry the scoped decision; do not ask again just because the worker is fresh. |
| A task is awaiting independent review | Perform or hand off the authorized review role; do not self-award independent acceptance. |
| Work has already been published outside the run | Reconcile actual published progress before doing more; do not redo the old assignment. |
| The authorized programme is finished | Preserve/record terminal completion rather than finding speculative work. |
| Two proposals could be meant by “I approve” | Ask which one; make no work-changing Send. |

**Leaf check:** revised instructions cover these cases without Rowing/story names, hard-coded project files, keyword-based approval detection, or a new lifecycle schema. Keep these as small behavior checks; do not build an evaluation platform.

---

### L2 — Find and select the existing run before choosing start/resume

**Primary files**

- `integration/launch_project.py`
- `integration/launch_story.py` shared bootstrap/launch functions
- `integration/cli.py`, `integration/runner.py::inspect_state`
- Focused new tests in `integration/tests/test_entry.py`

**Implement**

1. Expose a read-only inspection operation through the **same installed launcher**. It should report the selected run ID, verified Project identity, current worker, current checkpoint branch, count/cap, hold/terminal reason, pending phase and relevant response/action identity. It must not prepare a composer or Send.
2. Prefer an explicit run ID from an existing receipt. Otherwise find candidate saved runs using **verified Project ID + normalized repo**, not branch or display name. Reuse the existing private `Runs` folders; no database is needed.
3. Retain existing run IDs and folders. A display-name change or work-branch change must not move/reset a run. If several plausible runs exist, return their short receipts and ask which one; never choose the newest by timestamp.
4. Treat `bootstrap-intent.json` without a finished initialization as an unresolved existing launch, not as “no run”. Reconcile it read-only. Unreadable or corrupt saved state is not evidence that a fresh run is safe.
5. Add explicit internal operations, for example `inspect`, `start`, `resume`, `new`. They are tool request fields, **not phrases the owner must learn**:
   - `start`: create only when there is no matching run/uncertain launch; otherwise report the existing run.
   - `resume`: operate on the resolved existing run; use L3.
   - `new`: a genuinely new, owner-authorized bounded job after the prior selected run ended; allocate a new run ID. The same branch may be reused.
   - A finished/capped run never becomes a resume retry. Changing the branch never implies `new`.
6. Keep a short selection/provision critical section, keyed independently of branch, using the existing lock primitive. Recheck candidates inside it. Preserve the per-run controller lock across observation and Send. Duplicate/concurrent entry requests must converge on the same selected run.
7. Do not claim the controller is ready merely because a child PID exists. Serialize startup and acknowledge ownership of the existing run lock; a repeated or uncertain start returns/reconciles the existing attempt rather than spawning another sender.
8. Compare the selected private config with the persisted controller before **any** resume mutation, not only before `run`. Validate Project/repo/run binding and unchanged cap. The existing CLI resume path currently omits the configuration comparison. [E1, E5]

Default to one active succession job for that Project/repo selection. If legacy histories or genuinely separate jobs make that selection ambiguous, expose the ambiguity; this increment is not a parallel-job manager. Do not disturb other historical runs.

**Leaf check:** duplicate requests, branch changes and Project renames cannot create another executor; a terminal run remains terminal; an explicitly new authorized job can reuse its old branch without erasing history.

---

### L3 — Resume both the methodology and, when needed, the worker

**Primary files**

- `integration/cli.py`, `integration/launch_project.py`, shared launcher
- `integration/runner.py`
- `integration/windows_backend.py` and narrowly scoped UIA observation changes
- `KIT/succession/core.py` for a small additive owner-action entry
- `integration/tests/test_owner_reentry.py`

#### A. Carry the owner decision without making the request chat another worker

Extend the private request with a small optional owner-context record:

- the owner's actual current instruction;
- the resolved scope and the relevant project/proposal pointer;
- the selected run/current-worker and observed hold/response anchor;
- a stable logical request ID.

The model supplies semantic scope; the backend does not parse “approve”, “yes”, or project task names. Historical quoted approvals are not current owner instructions.

Persist the accepted owner context as an immutable private request file associated with that run. A retry of the same logical request uses the same record. Reusing an ID with changed content must not silently overwrite it.

**Use a short safe pointer in the browser message**, telling the saved worker to read that request through its existing Remote Desktop Commander access and then re-enter the canonical worker instructions. This avoids expanding the UIA Send character whitelist just to transport arbitrary text. The present adapter only accepts a restricted ASCII message alphabet; a direct natural-language injection would otherwise fail on apostrophes, Unicode or line breaks. [E8]

This is a one-time owner-input bridge, not copied answer bodies or a new successor handoff format. Before a later handoff, relevant authorization/progress belongs in the project's normal GitHub record. Successors must not need the original request conversation or a chain of private approval files.

Apply the same bridge to a **fresh launch** when a scope/approval exists only in the invoking conversation. A repo/branch pointer alone must not discard the owner's current instruction.

#### B. Distinguish observer resume from owner-directed continuation

Read the exact saved worker and the persisted action first.

| Observed situation | Action |
|---|---|
| Saved worker already received the owner input and is processing it, or has a fresh response | Resume observation only; no duplicate input and no new worker. |
| Verified saved worker is idle at the relevant consumed hold, and has not received this scoped owner instruction | Queue exactly one owner-directed **same-chat** continuation through the existing controller. |
| An ordinary unattempted pending action already exists and the owner only releases its hold | Preserve and dispatch that original action once. Do not append a second recovery prompt. |
| Pending phase is `sending`/`uncertain`, or initial bootstrap Send is uncertain | Read-only reconciliation first. Approval cannot authorize a blind resend. |
| Prepared action conflicts with the newly requested scope | Preserve it and explain the conflict; do not silently replace its message. |
| Terminal finish/cap, wrong Project/worker, unreadable or conflicting identity | No resume/new Send. Return the actual condition. |
| Another conversation is actively doing the same work | Do not wake a second executor or adopt that conversation. Resolve which existing executor owns the work and reconcile published progress first. |

A scoped task approval does not automatically release a separate owner pause. Clear that pause only when the current request/context actually releases it.

The current `observe()` returns `None` for several situations. **`None` is not proof of an idle worker or that approval was never delivered.** For re-entry only, expose the observation information needed to distinguish generation, the latest posted user turn and the held assistant response at the saved identity. Reuse existing UIA/posted-message checks; do not scan all chats or add a second watcher.

For a possible phone/desktop stale view, establish a fresh read of the **same saved chat**, preserving drafts. Two reads of the same stale page are not proof of absence. If freshness or ownership cannot be established without disturbing a draft, hold with that precise reason. No universal exactly-once promise is required.

The invocation chat need not supply a phone conversation ID just to start a new run. But claiming that it is already the current worker requires positive identity evidence. “Same Project” or access to the Windows `current_chat_id` value alone is not that evidence. Project context can include other chats; it is not a transport identity receipt. [E8, W2]

#### C. Add one explicit owner-action method; reuse the existing sender

Add a controller entry such as `continue_after_owner(request_id, anchor, message)`. Its name may differ, but its behavior must not:

- It accepts only an explicitly selected nonterminal run and a still-valid current-worker/hold anchor.
- It does not delete consumed response IDs, reset count, change the prior ERROR, or invent an assistant `NEED_MORE_TIME` response.
- It prepares the existing `CONTINUE_CURRENT` action, with an **owner-event origin**, and dispatches through `dispatch_prepared`/`send_once`.
- It persists acceptance/action state before any possible Send.
- It durably remembers handled owner requests after confirmation, so a later retry cannot send them again.
- It leaves terminal stops, existing conflicting actions and uncertain Sends intact.

Minimal persistence: add owner-event bookkeeping and a pending-origin discriminator. Old pending actions default to assistant origin. `Controller.load` currently requires each pending action to refer to a consumed assistant response; extend that validation for owner-origin actions rather than inserting fake assistant history.

Use a versioned, backwards-readable state upgrade. Load version 1 with defaults, preserving every existing identity/history/pending field; write the new version atomically only under the existing lock when a real mutation is needed. Unknown/corrupt state holds. Inspection alone does not migrate or reset it.

**Idempotency is more than allocating a new UUID per invocation.** Bind an approval continuation to the selected worker and the specific hold/action it resolves. A repeated approval for that same anchor, even through another temporary request file, must report the pending/handled action rather than enqueue another one. A genuinely later hold may accept a new decision. A changed scope is a new decision, not an implicit overwrite.

Immediately before dispatch, recheck that the worker/hold has not advanced and that no intervening user message or active generation makes the proposed continuation stale. If it has advanced, observe/reconcile instead of posting into the new state. Keep all existing draft, pause and uncertain-Send protections.

For a verified same-worker response already in progress, the wrapper may use the existing `resume_after_owner` plus `run` without any new Send. For an idle blocked worker, do not stop at that pair: the persisted owner continuation is what actually creates the next turn.

**Leaf check:** one scoped approval delivered elsewhere reaches the registered worker once, preserves the old ERROR and count, produces a fresh response and permits ordinary succession. A direct approval already delivered to that worker adds zero recovery Sends. Crash/restart/lost acknowledgement never causes an automatic retry.

---

### L4 — Let the published checkpoint branch change without changing the run

**Primary files**

- `integration/repo_reader.py::GitHandoffReader`
- `integration/runner.py::cycle` and `inspect_state`
- `integration/cli.py::create_dependencies`
- Shared launcher configuration comparisons
- `KIT/succession/core.py`, narrowly for the effective branch and validated transition
- `integration/tests/test_handoff_routes.py`

**Chosen design: retain the three trailers; add one optional branch locator.**

Do not force work or receipt writes onto an old/protected branch. Do not add a mandatory “transport branch” to every repository.

The worker uses its project's authorized route. At a successful handoff on a branch different from the incoming checkpoint, its completed assistant response includes:

```text
CHAT_HANDOFF_BRANCH: work/authorized-next
CHAT_STATUS: TASK_COMPLETE
```

The existing three trailers remain on that branch's published tip:

```text
Chat-Succession-Run: <unchanged run ID>
Chat-ID: <actual saved current worker ID>
Chat-Succession-Next: <authorized next task or FINISHED>
```

A missing locator means “use the current checkpoint branch”, preserving existing runs. The locator is a lookup hint, **not a fourth worker status or authorization grant**. It is parsed only from the exact current worker's complete assistant response with a valid terminal completion marker. Reject malformed/duplicate/conflicting locators; quoted/code/tool/user text cannot supply one. For this small extension, require the locator on its own line immediately before the final status.

**Implement this acceptance order**

1. Reject/ignore wrong-source, streaming, consumed or otherwise ineligible responses before any route mutation.
2. Resolve the candidate branch from the optional locator or the existing effective checkpoint.
3. Fetch that exact branch from the nominated repository using the existing bare reader. Read the receipt from the fetched commit object, not the worktree or a claimed SHA.
4. Validate exactly one of each existing trailer, matching run and **current saved worker**, and a valid next/finished state. Do not scan branches for “the latest matching receipt”.
5. Only after all checks succeed, accept the effective checkpoint branch and consume the completion. Persist the branch, consumed response and next pending action/terminal stop together before Send.
6. Build the successor pointer and future reader from that accepted branch.

The worker must establish the branch's legitimacy from project rules/owner scope and record its work/authority in the existing project record. The controller verifies source identity and publication, not the meaning of every project's rules. Do not describe those metadata checks as an independent approval audit.

**One authoritative mutable branch field**

Keep the initial config branch as the seed/entry branch for compatibility. Store the **effective checkpoint branch as `state.checkpoint_branch`**, defaulting to the seed for version-1 states. Expose `initial_branch` separately from the effective `branch` in status. Use the effective branch consistently for receipt reads and successor prompts.

Do not update `config.json` and `controller.json` independently to perform a rebind; that creates a crash window and config mismatch. Update the launcher and CLI comparisons accordingly: immutable config identity still matches, while the state owns the current checkpoint. The run ID, folder, worker IDs, history and cap do not change.

The existing bootstrap-intent message remains immutable during an uncertain initial Send. Do not regenerate it from a newly supplied branch/context and then Send again.

**Failure and recovery**

- Missing/unpublished branch, wrong run/worker, missing trailers, duplicate trailers or invalid route: hold; no new chat, no branch update.
- A repairable publication failure should not consume the completion prematurely. Validate the current-worker attribution before calling the consuming core path; a repaired receipt can then be re-read on explicit resume.
- An owner request may point the current worker to newer project authority/work. It must not directly rebind the controller to an unverified receipt.
- A valid same-worker completion plus receipt may advance the route without another owner approval if the project's existing rules authorize it.
- Published work made outside the run, such as the supplied Rowing checkpoint, remains useful work but is not retroactively a valid succession receipt. The saved worker may inspect it, reconcile progress, and publish a new legitimate handoff/verification commit **if permitted**. Do not rewrite history, forge another chat's attribution, or label someone else's unfinished work complete.
- Leave the specialized story reader's four-turn rules and the fixture reader's fixed-target behavior unchanged.

**Leaf check:** both fixed-branch and rotating-branch projects use the same generic reader/controller path; a cold restart retains the new checkpoint and count; a receipt from another chat never completes this run.

---

### L5 — Verify, deploy the actual entry path, and close narrowly

#### Offline regression matrix

Add these cases to the existing test framework. Use disposable local Git and mocked browser/process calls; clean each fixture before the next. Include restart/fault points, not just in-memory happy paths.

| ID | Case | Required result |
|---|---|---|
| R01 | Ready work on a fixed branch | Existing bootstrap → publication → successor/stop still works. |
| R02 | Held run; contextual approval in request chat | One same-chat owner continuation; old ERROR/history/count preserved; fresh completion enables normal successor. |
| R03 | Approval already delivered to saved worker | Observer-only resume; zero duplicate recovery Sends. |
| R04 | Repeat/concurrent approvals, including different temporary request paths | One logical owner action for the same hold; unchanged-content retry reports existing result; changed payload cannot overwrite it. |
| R05 | Lost owner-continuation acknowledgement/restart | Persisted uncertain action; read-only reconciliation; no blind resend/count increment. |
| R06 | Draft, attachment, explicit pause, busy/stale/unknown view | Preserve content/state; do not infer an empty/idle/undelivered condition. |
| R07 | Existing prepared or possibly sent action | Original action preserved; conflicting request does not replace it; uncertain phase blocks resume. |
| R08 | Same Project/repo, new branch or renamed Project | Resolve original run; no bootstrap or cap reset. Two plausible runs ask for selection. |
| R09 | Finished/capped run and genuinely new job | Resume refused; explicit new job may reuse branch with new run ID and intact old history. |
| R10 | Authorized checkpoint rotates on ordinary completion | Same run and current worker; verified candidate branch becomes successor pointer, including after cold restart. |
| R11 | Missing, local-only, wrong-worker/run, duplicate or malformed receipt/locator | No successor or route mutation; repairable completion remains available for explicit repair/resume. |
| R12 | Another chat publishes a plausible checkpoint or supplies status | No silent adoption; reconcile useful work through the registered worker under project authority. |
| R13 | Legacy version-1 state, terminal state, uncertain bootstrap and wrong config | Safe migration/preservation; wrong config cannot clear a hold; uncertain bootstrap never reboots from scratch. |
| R14 | Fresh invocation carries approved scope not yet in GitHub, with Unicode/apostrophes | Private context arrives intact; ASCII-safe pointer uses existing sender; next successor needs only repository work context. |
| R15 | Existing parser, composer, pause, cap, story and fixture cases | Preserve current acceptance; do not relax assertions to conceal regressions. |

Also exercise L1's reasoning cases against the actual revised skill with small, differently structured repository examples. A mock which supplies the correct decision does **not** prove the model will make it. Label instruction reviews, model trials and deterministic tests separately.

Run from the repository root:

```sh
python3 -B -m unittest discover -s integration/tests -v
(cd astra/2026-11-17/unpacked/chat_succession_test_kit_20261117 \
  && python3 -B -m unittest discover -s tests -v)
```

The supplied `verification/reproduce_resume.py` and this review's `review_probes.py` deliberately assert some **old deficient behavior**. Preserve their baseline logs. Do not require those diagnostic assertions to keep passing after the fix; convert their scenarios into corrected R02/R08/R13 expectations.

If UIA observation code changed, perform the existing PowerShell parse and relevant no-Send observation checks on Windows. This review did not run PowerShell.

#### Install what was tested

Update the existing private launcher installation and the personal plugin skill/metadata. Increment the plugin version consistently, for example from the supplied `0.3.0` to `0.4.0`.

The archive does not include the installed `.cmd` wrapper bodies. Inspect the actual wrapper to locate the executable modules; do not invent an install layout or overwrite private run files. Deploy the compatible core if it changed, not just the skill text.

Before the live trials, read back the installed version/entry behavior and inspect the selected run through the actual Remote Desktop Commander path. An edited source checkout alone is not deployment evidence. Preserve old private states and do not attempt to roll new-version state backward by deleting fields; pause and use a compatible build if recovery is needed.

#### Two bounded live situations, not another large test programme

Use owner-nominated small workloads and their existing project rules. No automatic action against the archived Rowing worktree is authorized by this plan.

**Trial A — existing hold and natural approval**

- Start with one verified saved worker at a legitimate project approval hold.
- From the iPhone request chat, invoke the installed plugin with an unambiguous “I approve” in its established scope.
- Verify the same run/worker resumes. Observe either one routed owner input or zero if it was already delivered—not an untracked manual recovery prompt.
- Have the worker publish useful work and a valid handoff; observe at least one automatic successor reading the durable project record and completing its authorized next slice.
- Repeat the invocation once to demonstrate no duplicate Send/worker. End within a small cap.

**Trial B — a different project shape/state with branch rotation**

- Use a project with different instruction/progress filenames and a materially different starting situation, such as authorized planning/review rather than ready implementation.
- Let the worker find and follow that project's rules without adding succession-specific planning scaffolding.
- Where a real project approval is required, give it naturally and verify re-entry. Do not ask for approval merely to satisfy this test.
- Exercise an authorized work/checkpoint branch change, then an automatic successor using the new checkpoint without a new run or count reset.
- Reach a legitimate stop/hold and accurately report it. Include a terminal no-more-work check without creating another chat.

These trials may combine observations from the matrix. Do not require a 30-chat chain or deliberately corrupt live project files. If direct-to-worker approval is not exercised in Trial A, add a small bounded observation of that case or leave its live status explicitly `NOT_RUN`.

**G2 passes only with evidence**, not a narrative “the skill should work”:

- Installed version and exact selected run/Project/current-worker identity.
- Before/after count, held/consumed event, owner-request disposition and pending-action phase.
- Actual posted-message observations, automatic successor counts and duplicate count.
- Published branch/commit receipts and project-appropriate useful-work verification.
- Whether manual controller commands, state edits, copied prompts or corrective model instructions were needed.

Ordinary owner approval is part of the product interaction, not a hidden test intervention. Manual operator resume or message repair is an intervention: record it and do not call that path unassisted post-approval acceptance.

**Final implementation handoff:** publish the change summary, changed files/commit, tests and scoped live results, remaining limitations, and one short usage example. Keep failed/interrupted evidence. Do not claim universal success for all repositories.

---

## 5. Explicit answers to the review brief

- **Can contextual approval use the existing resume/run path?** Yes, when the exact saved worker is established and has already received the input or has a fresh response. If it is still idle at the consumed ERROR, resume/run alone is insufficient: use the persisted owner-directed same-chat action.
- **What if approval occurred in another chat?** Treat that chat as the intent router, not a replacement worker. Carry the scoped decision to the registered worker once; first resolve any evidence that another executor is already acting. Never infer identity from Project membership.
- **What if the checkpoint branch changes?** Keep the run and count. Have the registered worker nominate its authorized published handoff branch, verify the receipt there, and atomically advance the effective checkpoint. A changed branch without a valid receipt is not success.
- **Should the Rowing hold be removed or ERROR interpreted as success?** No. The archive does not supply enough project authority to judge the original assignment decision. Fix re-entry, scope transfer and publication routing; do not bypass legitimate project holds.
- **Should succession repair the whitespace/concurrent edits?** No. The diagnostic evidence supports the whitespace finding, not attribution of the writer. Apply normal project verification to the appropriate staged/committed changes; no generic sanitation or concurrency-repair subsystem.

## 6. Source and verification index

Archive-relative paths below identify the material reviewed. Historical “authoritative” headings inside the archive were treated as evidence of design intent, not instructions governing this review.

- **[E1] Independent sandbox verification.** Companion `Chat_Succession_Review_Evidence_2026-11-19.zip`: `review_summary.json`, `input_manifest.json`, `integration-tests-rerun.log`, `reference-tests-rerun.log`, `approval-resume-rerun.log`, `review_probes.py`, `review-probes.log`, `archived-fixtures-readback.json`, `REVIEW_RESULTS.md`. All 13 supplied workload snapshots also passed their read-only fixture validator; this is not a new live/remote verification. All original extracted files remained unchanged.
- **[E2] Bounded successes and limits.** `backend-evidence/story/controller-state.redacted.json`, `controller-final.redacted.json`, `controller-timing.redacted.log`, `github-branch-readback.json`; `source/evidence/live_test_results_20261118.csv`; `source/PROGRESS.md` sections “My Cat and Dog mobile-launch trial” and “Astra bounded integration closeout”.
- **[E3] Rowing timeline and scope.** `backend-evidence/rowing/CASE.md`; its controller state/final/timing/process files. Screenshot-derived statements are case-author reports: the screenshots and complete Rowing worktree are not supplied.
- **[E4] Entry mismatch.** `source/plugins/chat-succession/skills/start-chat-succession/SKILL.md`; `source/integration/launch_project.py::read_request, launch_request` (especially lines 85–115); `source/integration/launch_story.py::bootstrap, launch` (especially lines 100–118); supplied `verification/reproduce_resume.py`.
- **[E5] Resume semantics and assisted precedent.** `source/integration/cli.py` lines 178–191; `source/integration/runner.py::cycle`; `source/astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/succession/core.py::consume, resume_after_owner, load`; `source/evidence/astra-l03-20261118-a/live_record.json`.
- **[E6] Publication contract.** `source/integration/repo_reader.py::GitHandoffReader.instructions, read`; `source/integration/runner.py::cycle`; same reference `core.py::consume`.
- **[E7] Whitespace and missing receipts.** `backend-evidence/rowing/git-whitespace-before-publication.log`, `git-diagnostic-snapshot.json`, `published-checkpoint.json`. The last file records commit `ff2876dc3c3b0d739df1e5e08de0626233c7ffa9` and absent trailers.
- **[E8] Browser/identity constraints.** `source/integration/windows_backend.py::observe, send_once, reconcile_readonly`; `source/integration/uia_adapter.ps1`, Observe section starting line 241 and Send whitelist at line 356.
- **[E9] Lightweight intent retained.** `source/astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/sources/archive_text/docs/ORIGINAL_VISION.md` and `LIGHTWEIGHT_PROTOCOL.md`; current `source/docs/astra-succession/README.md`. The new leaves do not import the old fixtures as universal project requirements.
- **[W1] Git primary documentation**, consulted 19 November 2026: `https://git-scm.com/docs/git-diff`. Default diff, cached diff and commit-to-commit diff examine different changes; `--check` checks the selected diff. This supports the diagnostic distinction, not attribution of the Rowing writer.
- **[W2] OpenAI primary documentation**, consulted 19 November 2026: “Projects in ChatGPT”, `https://help.openai.com/en/articles/10169521-projects-in-chatgpt`. Shared project context is documented; the requirement to verify saved-worker identity is this plan's transport conclusion, not a claim that the documentation verifies this installation.

**Input provenance:** 267 regular archive members; 1,269,903 uncompressed file bytes. The selected export reports template commit `0bee12a1725fbb103d82c5d08365959b3bf8c173` and plugin `0.3.0`; no live repository head or installed version was independently queried. Input archive SHA-256:

```text
3b76acba923c1e7d00718ff82799a5d20785df6a530a162eb4d908a0d62e1c08
```

**Bottom line:** enter the methodology according to the project's actual state, retain one known executor, and carry owner intent and verified publication across interruptions. Do not special-case Rowing, and do not replace model reasoning with more ceremony.
