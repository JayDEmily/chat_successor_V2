# ADR 0002 — Account-bound, resumable runs on one Windows PC

- **Status:** Proposed for owner decision; no implementation or live acceptance is claimed by this document.
- **Date:** 20 November 2026.
- **Extends:** ADR 0001, without reopening its accepted separation of project reasoning from transport.
- **Reviewed baseline:** source `283e6c17bf3359c203a362fd6593563480eeea5f`; runtime/plugin candidate `2c29406b1c43904c5ead79064fe7856971e0aa2e`; plugin ZIP 0.4.3.
- **Evidence:** [independent review](../../evidence/EVIDENCE_REVIEW.md) and [source index](../../evidence/SOURCE_INDEX.md). `Sxx`/`Vxx` below refer to that index.
- **Execution plan:** [ten leaves](../IMPLEMENTATION_PLAN.md), [gates](../../acceptance/GATES.md).

## 1. Context

The owner creates each ChatGPT Project and GitHub repository before invocation. The repository already has its own work record, approval boundaries, verification obligations and publication route. The owner identifies the exact Project, repo and published branch when the conversation does not establish them. Chat Succession must not replace those rules with a story-specific plan or grant itself approval. [S01/S02]

James Student and Shoco are accounts of the same owner, both authorized for GitHub and PC access. Their private plugins and signed-in Chrome profiles are nevertheless distinct routes. The captured Shoco connector has a different LocalAppData; the wrapper selects Shoko Profile 11 and candidate code, while its other-account default retains another checkout. Those profile numbers are historical installation observations, not universal account identities. [S03/S04/S06]

Earlier fixtures support same-chat continuation, scoped approval, branch rotation, bounded terminal stops and two overlapping controllers. The paused Shoco pair supports one automatic Rowing successor and one displaced-view restoration, but not final completion of both runs or a successful automatic reload of a genuinely stale view. The fresh Shoco iPhone approval and >2 concurrency remain open. [S04–S09]

The problem is therefore **operable identity and recovery on a shared PC**, not a need to replace the proven three-status controller.

## 2. Decision in one sentence

Retain one existing controller per run and the established Windows/Chrome/WSL path; make its account route and action/view identity explicit, keep uncertainty and pause durable, and raise simultaneous run count only through measured, isolated acceptance.

### Keep, simplify and avoid

| Layer | Decision | Reason / boundary |
| --- | --- | --- |
| Private plugin in each account | **Keep** as contextual start/resume/inspect entry from phone or desktop | Same natural owner workflow; do not share a private plugin ID across accounts. [S02/S03] |
| Desktop Commander | **Keep** as the authorized bridge to the installed launcher and private owner-input files | No per-poll orchestration by the request chat; it reports the controller receipt and then gets out of the way. |
| Installed wrapper | **Simplify** to one explicit verified route selection per account, common request handling, and a readback of the chosen installation/backend/profile | Replace fragile ambient-path/fallback assumptions, not the bridge. Unknown or conflicting route holds. |
| Python reference controller + runner | **Keep**; extend small validation/status seams | No second state machine, scheduler service, fleet daemon or separate approval controller. [S10/S11] |
| Native Windows state | **Keep** private NTFS config, journal, locks, pause marker, bootstrap intent and owner-input records | Preserve the tested placement; do not move locks to WSL UNC or Git. [S13] |
| Chrome UIA adapter | **Keep** verified background-window observation, ValuePattern typing, document-bound Send and posted-turn readback | One selected tab in an accessible run window; no global keystroke/clipboard workflow or forced foreground dependency. [S12] |
| Successor navigation | **Prefer existing verified worker-window Project link**, with existing fresh-window fallback | Avoid unnecessary renderers. Only after source completion, exact action, empty composer and Project are verified. Do not reuse another active run's window. |
| View recovery | **Keep and qualify** the bounded same-saved-chat reopen / fresh-view comparison path | Never treat elapsed time, a missing tab, or a `waiting` probe as completed work. |
| Ubuntu/Git reader | **Keep** one bare readback per run, fresh fetch of the exact nominated branch and three trailers | GitHub remains the work record; local unpushed state does not authorize handoff. [S13] |
| Worker prompt | **Reuse one builder**, short repo/branch pointer plus stable private identity/owner-input lookup | Project reasoning stays with the worker. Do not turn source hashes or long transcripts into runtime handoff ceremonies. |
| Concurrency controls | **Keep** per-run ownership locks and the short Chrome-window discovery mutex; measure first | No hard-coded “two runs maximum.” No global lock held while a model thinks or Git fetches. |

An alternative browser automation stack, API rewrite, container farm, new front end, automatic account login or fleet scheduler is outside this increment. Reconsider one only if a specific acceptance case proves the existing mechanism cannot meet the requirement and the smallest targeted repair is insufficient.

## 3. Account, run and window identity

### 3.1 Explicit account route

At installation and account-switch/recovery verification, record one private route:

`account_key → private plugin/binding → launcher/install root → backend revision → verified signed-in Chrome profile`

The human-readable account name and the actual private identity check belong in private evidence, not in public Git. Profile directory names alone do not establish which account is signed in.

**Proposed delta:** save the expected `account_key` and verified Chrome profile path/route receipt in the existing private run configuration; validate them before starting, resuming or recovering a view. Pass the selected profile explicitly to the child controller from that saved route, not from whichever connector environment happens to make a later request. Confirm the selected account read-only at release, restart/account change and recovery enrollment. If the actual account cannot be established, hold. This need not add a new service or change the reference controller's workload semantics. [F01/F06 in the evidence review]

Use the same resolved native installation root for `Requests`, `Runs/<run-id>`, locks and the worker's private pointer. Keep the existing relative layout. A shared installed wrapper may select the two explicit route records; unrecognized environments must not fall through to another account. Separate physical roots are optional, not a new requirement.

### 3.2 Stable run ownership

- For new runs, namespace selection/creation by verified account, stable Project ID and normalized `owner/repo`; use a stable internal job ID for a genuinely new job.
- Keep at most one nonterminal run for that selected account/Project/repo combination, as the current launcher intends. Distinct authorized jobs use distinct Projects/repositories during capacity acceptance; a branch rename alone is not a new job.
- Explicit `run_id` selection must agree with the saved account, Project, repo and native run directory.
- Project display-name changes and verified effective-branch rotation retain the run ID, worker list, owner-input history, response history and cap.
- `max_unique_chats` is an immutable **per-run worker budget**. The request chat, an inspection window, a recovery view and same-chat continuation do not consume it.
- New job IDs are generated once by the entry implementation as exactly 24 lowercase alphanumerics and retained on retry; owner request IDs retain their 24–64-character contract. The owner should not need to invent or format them. [S10/V07]
- A legacy run without new binding fields is preserved in place. Positively verify its existing route and attach metadata under its lock, with owner confirmation if identity is ambiguous. Do not derive a new run ID, move its journal blindly, reset its count or bootstrap a replacement.

### 3.3 A handle is a locator, not identity

Each run owns its private controller state and a view/action record. For a dispatch/reconciliation, check the composite:

`account/profile + run + Project ID + source saved chat + triggering response + action ID + target window/document`

A successor additionally requires an observed fresh Project composer before Send and a distinct server-saved chat ID after Send. An existing worker requires the exact saved chat. Window handles and process/lifecycle metadata are supporting locators, revalidated after restart/recovery; they are not authority by themselves.

**Proposed delta:** record and verify `action_id` for **every** prepared target and reconciliation, not only the same-window successor path. Check it against the persisted pending action, exact message and route before invoking the adapter. P08 demonstrates why matching only handle/source/kind is insufficient as an identity contract. Invalid or legacy-unbound pending records hold for positive reconciliation; do not silently regenerate a target and retry.

Use one dedicated accessible worker window per active run, with its worker as the selected tab. Background operation is permitted. Enrollment must not claim a window already owned by another live run. Use the existing short acquisition mutex and private records for this check; do not create a second controller. Duplicate views of the same saved worker hold. A probe owns only the temporary view it created and closes only that view.

## 4. Controller, pause and recovery contract

### 4.1 Status protocol remains unchanged

| Completed worker response | Controller action |
| --- | --- |
| `CHAT_STATUS: NEED_MORE_TIME` | One “Okay, continue working.” in the same saved chat, including at the cap |
| `CHAT_STATUS: TASK_COMPLETE` | Verify current published receipt; `FINISHED` stops first, otherwise stop at cap, otherwise prepare one successor |
| `CHAT_STATUS: ERROR` | Hold automatic posting and surface the blocker; contextual owner input may later resume the same worker |

Only the full completed current assistant turn can trigger an action. Retain source-response deduplication, streaming waits, canonical parsing and ambiguity holds. Keep semantic classification disabled/shadow-only. A hold is controller state, not a fourth worker status. [S11/S12]

The fetched Git tip must carry exactly one nonempty `Chat-Succession-Run`, `Chat-ID`, and `Chat-Succession-Next` with matching run/current worker. `FINISHED` is the terminal value; an eligible next assignment is not completion. The optional preceding `CHAT_HANDOFF_BRANCH` is a locator: fetch and verify that branch before atomically adopting the effective checkpoint with response/action state. Preserve the original entry branch. A receipt's trailers are attribution metadata, not cryptographic proof of authorship or proof of substantive workload correctness. [S13]

### 4.2 Persistent pause

An owner pause is a durable marker associated with the selected run, independent of the observer process. Pause does not kill the worker or undo an already-submitted message.

1. Write the marker using the existing marker synchronization path; report **pause requested**, not “all work stopped.”
2. The loop and final adapter boundaries check it before typing and before Send. A prepared action and any draft remain intact.
3. Record **pause acknowledged** when the controller reaches its safe hold/exits; record an in-flight click/uncertain result separately.
4. A restart with the marker present must not launch, continue or create a successor. A later owner release clears only the exact pause generation observed; a newer pause wins.
5. Resume the same run, saved worker, cap and histories. Terminal `programme_finished`/`chat_cap` cannot be converted into a retry.
6. Reconcile a possibly submitted action read-only before considering any new action, even when the owner asks to resume.

A pause racing after the final pre-click check may encounter an already-in-flight Send. Do not claim cancellation or retry it. The acceptance trace must distinguish request time, final gate, click, acknowledgement and reconciliation. The guarantee is no new dispatch after acknowledged pause, with all pre-acknowledgement uncertainty preserved, not retroactive cancellation. [S11/S12]

**Proposed status delta:** report marker present/generation, requested versus acknowledged pause, pending kind/phase/action ID, current saved-worker link, count/cap, terminal reason, account route and last verified publication in one read-only summary. Until implemented, the operator must inspect the marker as well as `status`. [F03]

### 4.3 Recovery decision table

| Condition | Permitted behavior | Mandatory hold / no-go |
| --- | --- | --- |
| Registered worker view closed or behind another tab; no possibly sent action | Reopen the exact saved-worker URL under the bound account, verify Project/chat, then observe twice. Count and worker identity stay unchanged. | Missing/unverified saved ID, account mismatch, unavailable desktop or duplicate accessible views. Do not inspect/erase a hidden tab's draft by guessing. |
| View appears unchanged for 120 seconds | At most one fresh comparison per worker per 300 seconds in a running controller. Compare the same latest user-turn digest/count and a stable completed response. | A fresh view still streaming, a different user turn, changed source, draft/attachment, or uncertain composer is not reload permission. |
| Fresh comparison proves newer completion | Close owned duplicate probe; reverify original identity, response and empty composer; reload only that original; then require normal stable completed reads and Git verification. | `refreshed` alone is not a response or handoff receipt. If proof is missing, return `waiting` or hold; do not post. |
| `prepared` action after pause/restart | Reuse that same persisted action only after safe destination/empty-composer checks and owner release. | Typed draft is not permission to Send. Preserve it; use documented operator recovery only with positive no-click evidence. |
| `sending` or `uncertain` action | Read-only reconciliation against the exact original action/posted user turn/Project/saved destination. Adopt once if positively matched. | Do not fall into normal missing-view recovery and make a new successor. Lost target or absent UI evidence is not proof of no submission. |
| Positive proof no submission occurred | Authorized explicit rearm of the **same** action; record proof; recheck draft/destination and pause. | Timeout, missing sidebar entry or provisional local ID is not positive no-send evidence. |
| Bootstrap intent exists without a journal | Reconcile its original exact first message and destination; initialize worker 1 only from confirmed saved-chat evidence. | Never write a new initial intent/message as a shortcut. A timing log with missing journal holds for restoration. |
| Finished/capped run | Read-only inspection; separate explicit new job only if owner-authorized | No resume, count reset, branch trick or extra successor |

Timers are liveness controls, not authority. A controller restart resetting stale-probe timers is acceptable if documented and measured; it must not reset action/response identity or the worker count. Keep 20-second polling unless the owner-approved workload specifies otherwise. [S12/S13]

## 5. Phone start, scoped approval and publication

The request chat stays outside the desktop worker count. The private plugin inspects before choosing `start`, `resume` or explicit `new`.

A scoped owner decision has a stable immutable request ID, literal input, scope and project/proposal pointer; re-entry also names the saved worker and consumed hold-response anchor. An unambiguous “I approve” is enough for the owner; the plugin resolves the scope from context. If scope or executor is ambiguous, ask one focused question rather than broadcasting an approval. [S02/S03/S10]

- If that exact saved worker is positively idle at the relevant hold with an empty composer, deliver one short private-input pointer through the existing same-chat dispatch path.
- Replay of the same decision returns its existing receipt. A second ID for identical content at the same hold is deduplicated; conflicting content/authority holds.
- If the worker has advanced, do not inject the input again. Observe/reconcile the actual new turn. Merely seeing a later turn or Stop control must not be reported as proof that this particular approval was delivered.
- Keep any pending action/uncertain Send ahead of owner-input delivery.
- Verify the first worker's fetched Git receipt and authorized branch before opening a successor. The project, not the controller, determines whether the work and approval were legitimate.
- Test fresh Shoco iPhone start plus one scoped decision to that original worker; replay the logical request; prove one published approved edit, one successor and terminal stop. Earlier James Student success does not close this gate.

## 6. Exactly-once acceptance without an impossible delivery promise

The browser and local journal do not share a transaction. Therefore “exactly once” means the following observable acceptance invariants, not guaranteed eventual delivery through arbitrary failure:

1. One controller owns a run; one persisted action identifies the triggering response or scoped decision.
2. `sending` is durable before the possible click. Automatic code attempts the action once; uncertainty stops it.
3. A confirmed action maps to one exact posted user turn in the correct saved destination. A successor is counted once after positive saved-ID observation.
4. Duplicate response reads, callbacks, request retries and restart acknowledgements do not cause another Send or another count.
5. Successful fixture handoff has one expected published slice with matching run/worker attribution and parent, and no extra worker or duplicate edit.
6. If positive evidence is unavailable, the result is **held/unresolved**, not success and not a blind retry.

Retain failed/assisted traces. Receipt hashes in acceptance evidence are audit aids; do not add an owner hash-approval ceremony to normal operation.

## 7. Concurrency on the shared PC

`M_i = max_unique_chats for run i` and `N = simultaneous run instances` are independent. A five-worker run is not five concurrent controllers; two two-worker runs can produce four saved IDs without ever exceeding two concurrent instances.

Keep separate run state, locks, owner-input files, private target records and Ubuntu readers. During acceptance use distinct owner-created Project/repo pairs and isolated fresh fixture branches. Do not test capacity by letting separate runs concurrently edit the same branch.

| Shared contention point | Isolation / measurement |
| --- | --- |
| Chrome process/window creation | Retain `Local\ChatSuccession.OpenChromeWindow` only across launch and unique-window discovery; log wait/timeout/abandonment. |
| Chrome renderers, UIA tree and Windows desktop | Dedicated run window, no foreground typing/clipboard, exact route/document checks; sample windows, CPU, memory and UIA duration. |
| Temporary fresh-view probes | At most one per run at a time, verified ownership and cleanup; no mass-close of Chrome or another run's view. |
| Native filesystem/locks and connector requests | Unique request files, canonical root, per-run ownership; concurrent pause markers do not depend on the long-running run lock. |
| Ubuntu/Git/network | Per-run bare readers and isolated publication routes; time fetches, distinguish readback latency from worker publication latency. |
| Account sessions and connector routing | Explicit binding; no hot-switch of a running worker to another account. A changed/missing login holds that run. |

Start with two overlapping runs: one ordinary finish, one cap stop with an eligible next assignment. Pause/restart one while its peer demonstrably progresses. Include closed/displaced view, genuinely stale view, pre-click pause and uncertain Send.

Then qualify 3, 4, 6, 8, and further increments of two **as measurements allow**, without changing per-run caps to manufacture a result. The [capacity protocol](../../acceptance/CAPACITY.md) fixes proposed thresholds, repetitions and stop rules before execution. No numerical maximum is asserted now. If testing ends before saturation, report a lower bound, not a measured limit. No throughput conclusion may be borrowed from the five-chat serial trials.

## 8. Migration, release and rollback

1. Preserve both paused trial journals, original uncertain attempts and the uploaded 0.4.3 ZIP.
2. Use the exact baseline for characterization. Implement only the nominated leaf in an authorized future workspace.
3. Version/pin any changed candidate separately; do not overwrite the historical 0.4.3 artifact and call the new behavior “0.4.3 verified.”
4. Verify the account-specific private plugin, binding, wrapper target, native root, backend revision and selected signed-in profile. A release ZIP/source match is only one part of this.
5. Existing legacy state is migrated conservatively under lock only after route/action evidence is reconciled. Unknown or incompatible state stays held.
6. On failed acceptance, stop admissions and preserve current actions/evidence. Pause affected runs; if isolation itself is suspect, pause the affected shared session's runs. Do not kill workers, delete journals, blindly restore a wrapper while controllers run, or repeat a possibly sent message.
7. Rollback only to a known compatible pinned route after controllers are safely stopped and pending actions retained/reconciled. If state compatibility cannot be proven, keep the run held for owner review.

## 9. Consequences and acceptance

Benefits: the same owner workflow, reusable code, fewer ambient-path surprises, explicit pause status and a measurable capacity envelope. Costs: a small configuration/target-record extension, conservative legacy-state handling, additional private evidence and bounded owner-environment trials.

Remaining risks include UIA structure changes, unavailable/changed logins, draft preservation, unresolved lost browser evidence, model output format and shared-PC resource contention. None is solved by asserting more retries.

Acceptance is the ordered `A2-G0`–`A2-G6` sequence. Existing 182 offline tests pass now; the **proposed deltas and all new live gates remain unaccepted**. The owner's approval of this ADR is a decision to proceed with the leaves, not authorization for arbitrary workload edits or automatic resumption of the paused pair.

Finish with the [operator's four operations](../../operator/QUICKSTART.md): start, pause, resume and check.
