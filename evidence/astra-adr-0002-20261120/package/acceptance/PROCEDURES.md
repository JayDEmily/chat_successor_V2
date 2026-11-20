# Bounded acceptance procedures

**Planned work only; not executed by this review.** These procedures require the owner's authorized desktop/accounts and fresh disposable fixture scope. No command here grants permission to restart the paused ordinary workloads. Use the [case register](cases.csv) and [per-run evidence template](run_record.template.json).

## 1. Prepare small, auditable fixtures

Use the existing Cat/Dog and Bird/Pig designs or equivalently small projects. Each capacity instance has its own owner-created Project/repository and publication route. Repetitions may use fresh authorized branches after the preceding run is terminal; never force-reset an old completed/uncertain branch.

The bundled clean seeds were independently inspected in [fixture-seeds.json](../verification/fixture-seeds.json):

| Fixture | Seed in bundled history | Files absent at that seed | New-run settings |
| --- | --- | --- | --- |
| Cat/Dog | `6d844f19f3a81752fe2c1bbb02caccb6f8a097f7` | `STORY.md` | 2 work slices; cap **3**; ordinary early finish |
| Bird/Pig | `5f43b42123c2ffdc3521285f866c31a60c2b3710` | `STORY.md` | 2 published slices plus eligible review; cap **2** |
| Shoco approval | `b91b00fe75be2ca011eac1ad1cc0d668ffd8d8bf` | `NOTES.md` | 1 held/approved edit + successor verification; cap **2** |
| Branch rotation | `75e5d27480e5b0d01fd07d6a11efe05e52498697` | `CHECKLIST.md`, `REVIEW.md` | Entry branch read-only; two writes on authorized review branch; cap **2** |

These are captured seed objects, not assertions about today's remote refs. In the future authorized environment, read the remote and publish fresh fixture instructions before launch. Change all branch pointers to the allocated fresh branch; retain the original histories. Do not point a “fresh” run at final `STORY.md`/`NOTES.md` results and call that a new trial.

[Cat/Dog template](fixtures/CAT_DOG_FINISH.template.md), [Bird/Pig template](fixtures/BIRD_PIG_CAP.template.md), [approval template](fixtures/PHONE_APPROVAL.template.md) and [rotation template](fixtures/ROTATION.template.txt) are supplied for owner approval. Replace every placeholder and independently review the allowed path/branch before use. These templates are not deployed fixtures.

### Required artifact checks

For every two-worker story/approval chain:

1. Fetch the exact authorized remote branch. Read commits as objects, not an unpushed worktree.
2. Worker-one commit is directly on the published fixture instruction base, with exactly the one expected file and first line.
3. Worker-two commit directly parents worker one, changes only that file, adds exactly the expected second line and preserves the first.
4. Each receipt has one matching run trailer and the corresponding registered saved worker ID; the two IDs differ.
5. First `Next` is the expected second task. Final `Next` is exactly `FINISHED` for Cat/Dog/approval, but an eligible review for Bird/Pig. Bird/Pig has no review output yet.
6. Join the Git publication check to the controller's completed source response **before** the successor Send. The commit alone cannot prove automatic handoff or account identity.

For branch rotation, verify the first write descends from the published entry base, only authorized files change, the successor builds on that exact first write, and only the effective branch changes in the same run. Project rules still decide whether publication is permitted.

## 2. Evidence before any Send

Allocate a unique case/cohort ID and freeze:

- Exact account aliases and private installed plugin/binding, package SHA/backend revision, wrapper/native root/profile route.
- Stable Project IDs/verified URLs, repo, entry/effective branch, instruction-base commit, job/run ID and per-run cap.
- Windows/Chrome/Python/PC configuration, poll setting, response deadline and stale-probe timings.
- Which fault boundary and pause/release is deliberately authorized; a fault hook must be test-only.
- Expected files/lines/parents/trailers and stop reason.

Capture a read-only preflight and before-state: journal or known absence, bootstrap intent, target record, marker, active controller ownership, existing workers/windows/drafts. Do not overwrite another run's files.

For each action record UTC time plus monotonic elapsed time, run/account/Project/worker, action/response ID, phase, window/document/route, expected and observed message digest, posted-turn anchor, saved destination, Git commit/ref/next field, pause generation and outcome. Keep exact messages/identity joins in private evidence; public receipts can use consistent labels. Digests help auditing and do not change the runtime protocol.

Record timing at: response first known complete, normal stable response observed, Git readback start/end, prepare start/end, `sending` persisted, final pause gate, click, posted-message/saved-ID confirmation, terminal stop. For stale cases record original and fresh view fingerprints and probe close/reload times. Include all failures and operator interventions.

## 3. First two-run cohort: finish versus cap (A2-D01–D03)

1. Preflight both routes and fixture branch tips without Send. Start Cat/Dog and Bird/Pig through the installed launcher, in different Projects with distinct run directories/readers/windows. Keep caps 3 and 2 respectively. Record both initial saved-chat confirmations; count one in each.
2. Arrange genuinely overlapping active observers. Bird/Pig's two pre-authorized `NEED_MORE_TIME` responses give an opportunity for pause/restart while its peer progresses. Do not create a new worker for either continuation.
3. Pause Bird/Pig at a recorded safe point with worker one and no pending Send. Confirm marker, acknowledgement and observer exit. Attempt observer restart while marker remains: no Send, count/cap unchanged.
4. While Bird is paused/restarting, Cat/Dog must have an observed new poll and a real advancement (new completed response, publication check or successor confirmation). A static process list alone does not prove independence.
5. Release Bird's pause only at the owner's direction. Verify same saved worker, history and cap. Continue the recorded run, not a new job.
6. Require Cat/Dog's two verified publications, one successor and `STOP_FINISHED` at 2/3; Bird/Pig's two publications, one successor and `STOP_CAP` at 2/2, with third review explicitly eligible.
7. Repeat status/cycle inspection and restart checks for terminal states: no extra Send/worker. An attempted resume of a terminal run is refused; creating a genuinely new job requires separate authorization.
8. Compare owned-window count and untouched unrelated draft/window evidence before/after. Close only verified disposable test/probe windows after state/evidence are safe.

If one run finishes too soon for the planned overlap, the overlap case is not met. Repeat on fresh fixtures or use a pre-authorized continuation step; do not fabricate an interval from process start times that did not actually overlap.

## 4. Closed/displaced and genuinely stale views (A2-V01–V06)

Run closed and displaced cases in separate bounded repetitions.

**Closed:** no pending action, pause the run, record the saved ID and exact view, close only its worker view. Restart with pause still present (zero Send), then explicitly release. Verify automatic reopening of the same URL under the right account and stable observation. Count and cap remain unchanged.

**Displaced:** select another tab in the run's window without deleting the saved worker. Pause/restart/release as above. Opening a recovery view may bring Chrome forward, but it is the same chat and not a new worker. Do not erase the original hidden view or any draft. If duplicate accessible worker views emerge, hold.

**Positive stale:** establish, in actual Chrome, an old/Stop original and a fresh view of the exact same saved chat that shows a newer completed reply to the same latest user turn. Capture both states; let the automatic recovery path make its own comparison. Required trace:

1. Unchanged-progress age reaches the configured threshold; cooldown permits the probe.
2. Bound account, Project, chat and latest user-turn digest/count match.
3. Two stable fresh completions establish progress; original composer is empty/no attachment and original source has not changed.
4. Owned fresh probe closes before the original reload; recheck exact original URL/handle/turn and pause.
5. One original reload; subsequent normal stable observation consumes that completion once.
6. A fetched current-worker receipt is verified before any successor; no second worker count is attributed to the probe.

A read-only fresh probe that still streams is the **negative** case. A manual reload demonstrates an assisted recovery only. An injected Python/PowerShell snapshot is offline/helper evidence, not a positive live stale case. If actual stale/newer completion cannot be observed, leave V03 `NOT_RUN` and the gate open.

Test draft, exact-placeholder draft, attachment, ambiguous view, changed user turn, wrong account/Project and worker advancement during preparation as no-effect cases. Check owner pause again during the recovery path. Do not disturb unrelated tabs or remove user content.

## 5. Pending and uncertain Send boundaries (A2-S04–S09)

Run only in explicitly disposable test instances with private evidence. A test-only fault may stop execution at a known boundary; it must never turn into a normal retry policy.

| Boundary | Expected result and proof |
| --- | --- |
| Prepared, before typing | Pause/restart preserves exact action and marker; zero click/posted turn/count change. Release can dispatch only that still-unsent action after normal checks. |
| Typed but pre-click | Pause or destination change returns positive pre-click evidence. Preserve the exact draft. Automatic resume cannot assume a nonempty composer is safe. Use authorized recovery only after proving no click. |
| Durable `sending`, no click | Inject known pre-click fault. Restart holds. Positive no-click trace permits explicit same-action rearm; an absent browser message by itself does not. |
| Click, acknowledgement lost | One exact posted turn plus saved ID permits read-only adoption. No second click. Replaying acknowledgement does not increment count again. |
| Same-chat identical continuation text | An older identical message before the triggering assistant or after another assistant is rejected. Only the user turn after the exact anchor matches. |
| Provisional/local-only successor ID | No count increment or successful handoff. Retain uncertainty and reconcile without Send. |
| Original target missing after possible Send | Preserve action and seek read-only evidence; reopening the source is not proof that the successor was never sent. No automatic fresh composer. |
| Bootstrap intent but no journal | Repeat invocation reconciles the original first message/target; no second initial intent. Timing log with missing journal holds for restoration. |
| Old action ID / wrong route / changed document | No adapter invocation even if handle/source/kind happen to match. Preserve the pending action. |
| Pause race and terminal stop | Record ordering explicitly. New pause generation cannot be cleared by old resume. Terminal stop is immutable; no fresh Send after acknowledgement. |

After every fault, inspect both the test run and its unaffected peer. Each successful action must have exactly one observed posted message and one saved-destination adoption. A safe unresolved hold is a correct safety outcome, not a completed fixture.

## 6. Shoco phone start and scoped approval (A2-P01–P03 / O01–O05)

Use the fresh approval fixture and Shoco's **own** installed private plugin. Record the iPhone request channel separately from worker identity.

- Start with cap two; first desktop exact-message/saved-ID registration establishes count one. The phone chat is never counted.
- Before approval the worker declares the proposal/hold, has no authorized edit and ends `ERROR`. Record consumed hold response.
- Owner approves the single identified scope naturally in the request chat. Store one immutable context ID; send its pointer once to the registered idle worker.
- Check its exact posted user turn after the hold, then first published note and matching current-worker/run/next trailers. The successor may begin only after that readback.
- Second worker publishes only the verification line, and the controller records `STOP_FINISHED`, count two, no pending action.
- Replay the same logical request from another file; verify no extra post, edit or saved worker. Same-hold identical content under another ID deduplicates; conflicting content/anchor/scope holds.
- If the worker already received the input, observe without another input. Verify what was actually delivered; “advanced” alone is not a scoped approval receipt.
- Switch to the other account's private plugin route and back using read-only checks; verify its own account/profile/run, preserve pauses and reject a wrong-account run request. Do not sign an active worker into another account.

Keep literal approvals and full account evidence private. A copied older result on the 19 November James Student branch is not a Shoco replay.

## 7. Pass classification and cleanup

For a healthy cohort, require all planned artifacts, correct Project/account/branch continuity, no unplanned manual fixes, no duplicate/misrouted posts, correct immutable counts and no pending action at terminal stop. Planned pause/fault injections are disclosed test steps; unplanned format correction, reload, foregrounding or extra prompt is assistance and disqualifies unattended PASS.

Clean up only owned disposable views and temporary readers after their evidence/state is preserved. Do not delete a run journal, bootstrap intent, owner input, draft or uncertain target. A rollback or new attempt must not make an old possibly sent action disappear.

The [capacity protocol](CAPACITY.md) starts with this two-run design, not with a larger assumed capacity.
