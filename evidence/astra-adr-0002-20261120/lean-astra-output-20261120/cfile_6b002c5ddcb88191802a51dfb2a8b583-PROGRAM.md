# Chat Succession — lean ADR 0002 execution programme

**20 November 2026 · Recommended execution amendment, not a release**

## Decision

Keep the existing controller and account separation. Stop adding general
infrastructure. Finish the one missing browser contract, demonstrate useful
succession, then qualify extra capabilities separately.

The product remains:

1. A worker reads the nominated repository and does useful authorized work.
2. `NEED_MORE_TIME` continues that saved chat.
3. `TASK_COMPLETE` checks the published handoff, then finishes, stops at cap,
   or starts one successor with the repository pointer.
4. `ERROR`, owner pause, or an unresolved submission stops automatic posting.

**23 small core leaves; three release gates; one current work queue.**
L10 is split into four individually assignable cards. Leaves are developer tasks,
not approvals imposed on every worker handoff.
A normal worker is not restricted to a one-line fixture or one tiny task.

This proposal changes the *order and initial release scope* of ADR 0002.
Adoption allows a limited release before automatic stale reload and maximum-PC
capacity qualification. It does not mark the original A2-G3–G6 gates passed.
If that narrower scope is not adopted, the original full-release conditions
remain open. The current request authorizes this review and these local
deliverables; it is not a command to operate the owner's accounts.

## 1. Independent assessment: what is actually blocking progress

### Evidence boundary

The input is the inline `CHAT_SUCCESSION_ASTRA_INPUT.md`, not a mounted Git
checkout. Its reported published HEAD is `beacfae4790c2ec4f390e90ad0bd214fe6a1ef05`.
Its separate review at `568ed35a775b143bd5a2894bce9333ae014e4ade`
holds source `e33ae7ad49e3510bf3021c552184cbb9d0e05758`.
The supplied `integration/uia_adapter.ps1` already contains an uncommitted edit.
The reported installed backend is **another revision**, `5c86ad6…`.
None is interchangeable. No live installation was inspected here. [S1]

| Finding | Assessment and consequence |
|---|---|
| Earlier chains, approvals and overlap worked in bounded trials. | Retain that evidence and the implementation. Do not restart feasibility work or rerun six historical bundles for every leaf. It is not acceptance of this changed reader. [S2] |
| The independent review reproduces an older article being accepted despite a newer opaque sibling, including a false posted-message acknowledgement. | A real safety defect at a synthetic native boundary, not just paperwork. Repair it before live dispatch. The supplied report is evidence; its Windows reproduction was **not** rerun here. [S1] |
| The interrupted edit checks only non-article `group`, `heading` and `text` kinds. | It addresses the reported group example, but does not establish complete coverage of other unknown kinds. The old native test also expects “unverified virtualized row”, while the edit throws “unverified non-article row”. Both require attention; neither is a reason to delete the safety assertion. Static findings, not new native execution. [S3] |
| Pure virtualized reads intentionally have no response ID or actionable result. | That is containment, not working succession. The Python path can keep returning `WAIT` with no response deadline. One new test reproduces this distinction; a three-line candidate reports a durable hold instead. [S4, fresh results] |
| Pause is checked after preparation as well as at the click boundary. | Direct `dispatch_prepared` can still call preparation with a marker already present. The CLI loop normally checks first. This is **not** evidence of a post-pause Send; the four-line candidate avoids unnecessary preparation as well. [S4, fresh results] |
| Backend version and plugin identity participate in saved route equality. | A controlled local probe changes only deployment metadata and the same account/profile/root no longer matches its run. This is deliberate conservatism but also upgrade friction. Do not solve it by resetting a run or removing account binding. [S5] |
| The programme has several overlapping plans, gate matrices and repeated audits. | Keep the historical evidence, but maintain only this queue and a short result entry in the existing progress record. Test a changed behavior, not the number of reports produced. [S2, S6] |

**The key distinction:** most of the needed reliability behavior already exists.
The immediate blocker is trustworthy current-turn/posted-message observation.
Removing pause, exact destination, draft or no-resend checks would not solve it.

### Stable identity does not require a global transcript census

The required fact is: **this is the current complete assistant response to this
run's confirmed current input**, and it has not already been consumed.

A server-provided stable message ID is one possible implementation. A persisted
local turn identity tied to positively observed input/response progression is
another; the original adapter contract already permits it. Neither visible
ordinal, text digest, two identical stale reads, nor UIA runtime ID alone proves
the fact. Do not require an absolute ordinal for every message in the account.
Do not simply remove the current ordinal and retain the digest. [S7]

Microsoft documents that UIA runtime IDs can be reused and that virtualized
items may be absent from the accessibility tree. These are reasons to test
coverage, not proof that a particular alternative ChatGPT interface will work.
The four supplied node probes establish limits of that inspected view only.
[MS1, MS2, S8]

Leaf L05 must establish a usable observable before L06/L07 implement it.
If the existing interface cannot supply one, stop that investigation and
return the exact missing fact for a focused read-adapter decision. Do not
produce successive “safe but cannot do work” releases or invent more CSS guesses.

## 2. Keep, remove from the critical path, and do not build

| Keep at the boundary where it matters | Simplify or defer |
|---|---|
| One controller/Send owner per run; existing native lock and short window-acquisition mutex. | No new supervisor, scheduler, second sender, queue service or gate engine. |
| Saved account/profile/root, Project, current worker and immutable cap. | Setup/restart/changed-route verification is not a per-turn account audit. Keep release identification separate from task reasoning. |
| Actual editable-content/attachment checks; exact document-bound typing and Send. | No blanket placeholder-text exemption; no automatic draft clearing. These are functional protections, not removable ceremony. |
| Persist action and `sending` before the one possible click; reconcile uncertainty read-only. | No timeout-based resend, “try another worker”, new-job recovery shortcut, or guaranteed-exactly-once marketing. |
| Full current assistant turn, explicit statuses and response deduplication. | No semantic completion classifier, whole-transcript reconstruction project, or per-poll invented IDs. |
| One fresh exact-ref publication check on an eligible completion; existing three trailers. | No signed handoff packets, repeated owner hash approvals, universal project file schema, or controller assessment of engineering quality. |
| Scoped owner input and its existing immutable receipt. | No new approval engine; an unambiguous ordinary approval remains sufficient. |
| Correct hold and a useful saved-chat link when observation fails. | Automatic stale reload is a later capability. For the limited release, remove its automatic invocation in L09; merely disclaiming it while leaving it active is insufficient. |
| Existing tests and a targeted independent review at gates. | Focused tests per leaf; complete suites at a behavior gate. No fresh clone/fsck/archive restoration/24-case re-audit for every small edit or documentation commit. |

No gate registry, database, extra runtime manifest or per-leaf evidence directory
is required. Retain existing private journals, bootstrap intents, target records
and pause files. Do not consolidate these files during a bug repair.

## 3. Release gates

These identifiers are new **execution checkpoints**, not replacements for
historical evidence labels.

### LEAN-G1 — The browser boundary is both safe and usable

**After L01–L08. No new worker Send is permitted by an offline green suite alone.**

Require all of:

- F1 regression fails on the old source for the intended reason and passes on
  the corrected candidate, with positive full-article controls still passing.
- A real, read-only disposable saved-chat observation proves the current
  complete assistant body and its causal identity. Repeated reads, scrolling,
  reopen/reload and identical successive messages do not invent a new event.
- Exact known posted-user readback succeeds; an older identical message, a
  fragment, wrong anchor, unknown trailing row or provisional saved ID fails.
- Current candidate passes the complete existing Python suites and relevant
  native PowerShell suites on Windows. Record actual counts and skips.
  The supplied 114/119 results are historical, not a required magic total.
- One independent reviewer checks the changed observation/receipt path,
  preserved state compatibility and the actual positive evidence.

**Failure:** keep candidate off live dispatch. Negative-only success does not
close this gate. Do not open a fresh worker just to discover that its initial
Send cannot be acknowledged.

### LEAN-G2 — One run performs useful work and survives interruption

**After L09–L15 (including L10a–L10d), on a pinned installed candidate and named account route.**

Require normal finish at 2/3, eligible-work cap stop at 2/2, same-chat
continuation at cap, durable pause/restart, and positive once-only adoption
after lost acknowledgements for continuation and successor. Verify the useful
published file, parent chain, run/worker trailers and final journal, not merely
a status string. Ordinary bootstrap must use its existing durable intent;
offline bootstrap crash/missing-journal regressions must also pass.

No unexpected manual correction in a healthy run. Planned pause/fault injection
is recorded separately and is not disguised as a naturally occurring failure.
No automatic stale reload may remain reachable in this limited configuration.

**Failure:** preserve the original action, draft and run; repair the earliest
failed boundary. A safe unresolved fault passes only its safety assertion,
not the positive adoption/completed-work requirement.

### LEAN-G3 — The intended owner workflow works

**After L16–L20.**

Require two genuinely overlapping isolated runs, peer progress while one is
paused/restarted, same-worker displaced-view recovery, fresh Shoco phone start,
one scoped approval to its saved worker, publication before one successor,
terminal finish and replay without another input. Verify both separate account
routes and the start/pause/resume/check walkthrough.

Record **one** release line: exact backend and plugin per account, qualified
capabilities/concurrency, known limits, compatible rollback and next open item.
Independent review covers the affected final candidate, not another full
history reconstruction.

**Exit:** owner-accepted limited operating scope only. The recommended initial
scope is the measured two-run workflow, not a hard-coded two-run architecture.
More concurrency, automatic stale reload and ordinary-project completion
remain separate claims. Neither Rowing nor SolidWorks is released by this gate.

## 4. Execution rules for the 6.0 implementer

- Receive **one** leaf ID, a base revision, and its stated input. Read the small
  contract above, that card, its named functions and tests—not every archived plan.
- Change one behavior. Prefer one production function/branch plus one test.
  If the named scope cannot contain the repair, return the dependency; do not
  invent a framework or silently broaden the card.
- An already-passing unchanged behavior needs evidence, not a rewrite.
- Keep work on the selected implementation branch. Publish coherent checkpoints;
  a tiny leaf does not require its own release archive or independent commission.
- Routine in-scope work uses the recorded standing implementation grant.
  Escalate only a real scope/architecture/authority gap, not every ordinary step.
- Result record, in the existing progress log, is five lines:

```text
Leaf / base → candidate:
Changed files and observable behavior:
Command → exit / counts / evidence path:
Remaining blocker or limitation:
Next leaf:
```

Do not turn this five-line record into a new schema or validator.

### L01 — Install the regression, not a new parser

**Input:** supplied published source and preserved uncommitted diff. **Touch:**
`integration/tests/test_a2_transcript_boundary.ps1` only.
Use the supplied new test. On Windows compare the clean published reader and a
separate copy with the interrupted edit. Retain the original diff unchanged.
**Done:** positive controls work and each negative's actual result is recorded.
An unsafe baseline must exit nonzero. Do not use the historical reproducer's
“unsafe behavior reproduced” exit zero as a safety pass. **Next:** L02.

### L02 — Close the mixed-transcript hole

**Input:** L01 failures. **Touch:** `Get-ConversationTurns` and its focused tests.
Classify the transcript's known row/layout/control structure with unknown
possible-message siblings rejected, including non-group kinds. Do not enlarge
a renderer-name blacklist. Keep literal role labels inside bodies.
Fix the old test's diagnostic wording without weakening its behavioral check.
**Done:** native regression positives and negatives pass together. This is
containment, not qualification of virtualized responses. **Next:** L03.

### L03 — Make unsupported observation visible

**Input:** L02. **Touch:** `WindowsUIA.observe` and the new Python regression.
Review/apply `02_reader_hold.patch`: explicit
`UIA_VIRTUALIZED_UNQUALIFIED` becomes a saved hold through the existing runner,
not unlimited normal waiting. Ordinary streaming remains waiting.
**Done:** the focused unqualified-reader test passes with no publication,
preparation, reload or Send; state/count preserved. **Next:** L04.

### L04 — Respect pause before preparing

**Input:** L03. **Touch:** `dispatch_prepared` and its focused regression.
Review/apply `03_pause_before_prepare.patch`. Keep the later pause checks:
a pause may arrive while preparation is running.
**Done:** existing-marker case makes zero browser calls; late-marker case
makes zero Send calls; pending action and marker survive. **Next:** L05.

### L05 — Establish the missing observable, read-only

**Input:** L02 containment; authorized completed disposable saved chat.
**Touch:** no runtime code.
Use the existing diagnostic method once to capture the latest message boundary,
complete body, completion signal, ordering and any available durable identity.
Use a history containing repeated text; verify what is absent as well as present.
**Done:** a short evidence-backed choice of one reader/anchor method for L06–L08,
or the precise unavailable fact. If unavailable, stop here for a senior design
decision on this read seam; do not launch, install a new stack, or add more
non-actionable parser variants. Private transcripts stay private.

### L06 — Return one qualified current assistant event

**Input:** L05's positively demonstrated method, not an assumed selector.
**Touch:** the existing native current-turn reader and, only if necessary,
its Python mapping; no replacement controller.
Return the full body and a stable causal event key. Use an observed persistent
ID, or the specifically designed persisted local anchor from L05. No bare
digest/visible-count inference. Keep unsupported shapes non-actionable.
**Done:** current completed positive and stale/partial/quoted/duplicate
negatives pass. A required state-format change must be explicitly specified
and compatibility-tested, not improvised by the implementation worker. **Next:** L07.

### L07 — Use that same boundary for acknowledgement

**Input:** L06. **Touch:** `Find-PostedMessage` and its callers/tests.
Require the full exact user body in the correct destination and, for same-chat
input, immediately after the triggering assistant anchor. Do not accept a
matching fragment or earlier identical message. Preserve the original
bootstrap/target action and saved-ID checks.
**Done:** known true post succeeds; F1, longer-body, wrong-anchor and provisional
ID cases do not acknowledge. No browser Send in this leaf. **Next:** L08.

### L08 — Check cold-read identity and compatibility

**Input:** L06–L07. **Touch:** tests and a short gate result only.
Replay unchanged reads, viewport prefix disappearance, reopen, reload,
same-text successive replies, edit/regeneration and an old pending action.
After restart, use positive evidence or hold; never assign new IDs to old text
or rewrite old consumed history to fit the new extractor.
Run full affected suites and the read-only Windows positives. Obtain the
single LEAN-G1 review. **Done:** G1 passes, or stop at the exact failure.

### L09 — Remove autonomous reload from the initial scope

**Input:** G1 and adoption of the limited-release scope.
**Touch:** scheduled stale path in `windows_backend.py` and implicit advanced
re-entry reload in `uia_adapter.ps1`, with focused tests.
Keep the existing progress timer, but at its stall boundary report a hold/link
instead of opening a probe or reloading. Advanced owner re-entry reports
observation-only, never delivered approval or implicit reload. Closed/missing
view recovery remains separate. No new capability framework or second monitor.
**Done:** stalled/advanced cases make zero reload/probe calls; drafts and pending
actions survive. Adjust only tests of this explicitly changed feature policy;
retain dormant recovery comparisons for R01/R02. **Next:** L10.

### L10a — Stage one exact installation

**Input:** G1 and L09; installation within the existing scoped grant.
**Touch:** the selected installation only.
Stage/read back the candidate backend and wrapper; preserve the compatible
previous installation. Inspect affected run ownership first. Do not migrate
old journals, alter a pending action's route, or replace a backend underneath
a running controller.
**Done:** actual source/entry path identified; old runs retained. **Next:** L10b.

### L10b — Check one account route without Send

**Input:** L10a and the nominated signed-in account.
**Touch:** no-Send installed entry calls only.
Confirm that account's plugin/profile/root, then run the existing `--check`
against the nominated Project and exact published fixture branch.
**Done:** expected Project/ref, genuinely empty composer and no run-state
mutation. Repeat separately for the other account; never infer symmetry.
**Next:** L10c.

### L10c — Restore one closed saved view

**Input:** L10b; completed disposable saved chat, no possibly-sent action.
**Touch:** only its owned view.
Close/reopen through the existing recovery path; verify saved account/Project/
chat, stable observation and unchanged journal/count. Closing that owned test
view is a declared test step, not permission to close unrelated Chrome windows.
**Done:** same worker restored, no new prompt or worker. **Next:** L10d.

### L10d — Preserve one unsafe view

**Input:** L10b; one nominated disposable no-Send condition.
**Touch:** that condition only.
Run this card separately for wrong profile, duplicate accessible view, a real
draft (including placeholder-identical text), and an attachment. Use existing
helpers; do not make another diagnostic framework.
**Done:** no typing/Send/reload, exact original content/views retained and only
owned probes cleaned up. Do not sign the owner out to manufacture a test;
unavailable live conditions remain `NOT_RUN`, not a claimed full R02/V05 pass.
**Next:** L11 after the required selected-route checks.

### L11 — Finish two useful slices

**Input:** L10a–L10d; fresh Cat/Dog branch and isolated Project, cap three.
**Touch:** that fixture only.
Run the ordinary launcher. Require two exact story lines, direct commit chain,
two distinct saved workers, exactly one successor, `STOP_FINISHED` at 2/3 and
no pending action. Verify receipt before successor, not after the fact.
**Done:** unattended positive, or record failure/assistance. **Next:** L12.

### L12 — Stop with work still eligible

**Input:** L11; fresh Bird/Pig branch and Project, cap two.
**Touch:** that fixture only.
Retain its repeated first-worker continuations; stage one `NEED_MORE_TIME`
in worker two before its final slice to exercise continuation at cap.
Require two story lines, eligible review still absent, one successor,
`STOP_CAP` at 2/2. Terminal restart/resume cannot create worker three.
**Done:** no cap change, duplicate input or corrective prompt. **Next:** L13.

### L13 — Pause and restart the same run

**Input:** L10a–L12; disposable nonterminal fixture.
**Touch:** that run only, through existing pause/resume operations.
Request pause before a prepared action dispatches, observe acknowledgement,
restart with marker still present (no Send), then explicitly release that
generation. Reuse the same worker/cap/action. Preserve a pre-click typed draft;
release must not auto-send it. A new pause must defeat an old release.
**Done:** ordered request/gate/ack trace; no new dispatch after acknowledgement.
A click already in flight is retained for reconciliation. **Next:** L14.

### L14 — Lose one continuation acknowledgement

**Input:** G1 and a disposable prepared continuation.
**Touch:** existing test-only fault hook; no new recovery service.
Inject the existing after-click failure once. Restart, observe the exact posted
user turn after its anchor and adopt without another click.
**Done:** original action resolved once, saved worker/count unchanged; an older
identical continuation cannot satisfy it. If evidence is lost, remain held.
Do not create a replacement fixture to erase the uncertain action. **Next:** L15.

### L15 — Lose one successor acknowledgement

**Input:** L14; disposable published completion below cap.
**Touch:** existing fault hook and that run only.
Inject after one successor click; restart and reconcile its exact initial
message, Project and distinct saved ID. Replay the acknowledgement.
**Done:** one counted successor and no second click. Missing target or local-only
ID preserves uncertainty and creates no new composer. Complete LEAN-G2 review;
do not claim arbitrary crash-proof delivery. **Next:** L16.

### L16 — Demonstrate independent overlap

**Input:** G2; fresh finish/cap fixtures in distinct Projects/repos.
**Touch:** two disposable runs only.
Observe both controllers concurrently for two normal poll intervals. Pause/
restart one while its peer both polls and makes useful progress. Displace the
paused worker's selected view, then explicitly release and recover the same
saved worker without disturbing a hidden draft. Duplicate accessible views hold.
**Done:** each expected terminal artifact/stop, unchanged caps, disjoint action/
worker mapping and no unrelated window/draft changes. **Next:** L17.

### L17 — Start from Shoco's iPhone request chat

**Input:** G2; Shoco L10a–L10d receipts; fresh approval fixture, cap two.
**Touch:** that phone request and its desktop fixture only.
Invoke the existing private plugin. Register the first desktop saved worker;
the phone conversation counts zero. Observe the intended `ERROR` approval hold
and verify `NOTES.md` absent.
**Done:** one registered worker, one clear proposal, no authorized edit yet.
Do not substitute the older James Student phone result. **Next:** L18.

### L18 — Deliver one approval, then replay it

**Input:** L17 and the owner's approval for that specific proposal.
**Touch:** the same saved run only.
Deliver one anchored private-input pointer. Verify the first published note
before one successor. Require the second verification line and
`STOP_FINISHED` at 2/2. Replay the same logical approval from another request
file; equivalent same-hold input deduplicates and conflicting scope holds.
**Done:** one approval post, one successor, no repeated edit/input. If the worker
advanced independently, report that separately from approval delivery.
**Next:** L19.

### L19 — Switch entry routes, not active worker logins

**Input:** both accounts' L10a–L10d receipts.
**Touch:** read-only installed entry calls only.
Use James → Shoco → James (or inverse), inspect the respective saved runs,
and try one deliberately mismatched run/account selection with zero effects.
**Done:** each route returns its own profile/root/run; no fallback, count reset
or pause release. Do not sign an active worker into another account.
**Next:** L20.

### L20 — Close narrowly and stop developing

**Input:** G1–G3 evidence on the final candidate.
**Touch:** existing quickstart/progress and release metadata only.
Walk start, pause, resume and check using the qualified fixture. Record tested
capabilities and versions, rollback compatibility and remaining limits in one
short release entry. Keep the original Rowing/SolidWorks journals, markers and
uncertain attempts unchanged.
**Done:** independent closeout and owner-accepted scope; no automatic merge,
ordinary-project resume, additional gates, or speculative cleanup sprint.

## 5. Later leaf types — only when that capability is wanted

| Leaf | Small assignment and exit |
|---|---|
| R01 — Capture genuine staleness | On a disposable run, obtain an old original and a fresh newer completed response to the **same confirmed input**. Capture stable identities and an empty original composer. No automatic reload yet. If this condition is absent, `NOT_RUN`, not assisted PASS. |
| R02 — Restore one automatic recovery path | After R01, qualify the existing owned-probe close → original recheck → one reload → normal consumption/publication path. Test changed input, streaming, consumed response, draft, attachment, pause and duplicates. Remove overlapping implicit re-entry reload behavior. Enable only this reviewed path on a new pinned candidate after native/live success. |
| C01 — Measure one capacity cohort | After G3, reuse the existing capacity protocol, not a new scheduler. One bounded cohort per task. Preserve the 2→3→4→6→8→+2 series, three cohorts/level and last-good confirmation for the original ceiling claim. Freeze budget/thresholds first; count observing runs separately from saved workers. Stop admissions at the first failure. Budget exhaustion proves only a tested lower bound. |
| U01 — Separate upgrade metadata from run identity | Only when an upgrade is actually required. In the existing route module distinguish account/profile/root identity from the reviewed backend deployment pin. Use the existing per-run lock and explicit compatible migration; preserve histories/caps/pauses. Old target/bootstrap receipts are not silently rewritten, and possibly-sent actions reconcile under their original binding. Test all legacy/prepared/uncertain/terminal states before removing any version-equality check. No registry or broad bypass. |
| U02 — Shorten the one worker instruction builder | Only after stable end-to-end behavior. Keep repo/branch, run/worker/private lookup and three-trailer/status essentials. Move repeated general guidance to existing standing instructions where actually available to every fresh worker. Keep ASCII/owner-context compatibility. Do not remove identity lookup before providing its replacement, or turn fixture slice sizes into product limits. |

R01/R02 and C01 are **deferred initial-release dependencies**, not deleted
requirements. U01/U02 are targeted simplification opportunities, not extra
mandatory release gates. Any runtime change reruns affected boundary tests.

## 6. Old-to-new coverage, without losing requirements

| Original ADR 0002 scope | Disposition in this programme |
|---|---|
| A2-E01–E03 / G0 | Carry historical baseline/standing scope; identify current source and dirty diff once. Do not relabel old tests as fresh. |
| R01–R04, W01–W03 | Preserve existing binding/status tests; L10a–L10d/L19 verify actual selected routes. Legacy migration, if needed, is U01—not a run reset. |
| S01–S03 | L02/L05–L08 current-turn proof; existing parser/Git/branch-rotation regressions; L11/L12 useful publication. Do not rewrite the core. |
| S04–S09 | L04/L13–L15 plus existing bootstrap, action-mismatch and terminal tests. Full original live fault matrix is not claimed merely by these representatives; unexecuted variants remain open. |
| V01/V02/V05/V06 | L10c/L10d/L13/L16 and the exact observer/approval tests. Recovery of a view alone never qualifies a response or receipt. |
| V03/V04 | Negative no-unsafe-reload tests retained; automatic positive stale qualification R01/R02. Limited release cannot advertise this feature, and L09 must disable automatic invocation. |
| O01–O05, P01–P03 | L17–L19 and existing owner-input/entry tests. Correct scope remains project reasoning, not a new backend classifier. |
| D01–D03 | L16, with supporting L11–L15 evidence on the same candidate. One test may supply several observations; no duplication for its own sake. |
| C01–C03 / G5 | Capacity lane C01; original ceiling objective open until actually measured or explicitly narrowed. |
| Q01/Q02 / G6 | L20 limited release. Original paused workloads remain paused; their substantive closeout remains open. |

A backend change invalidates affected path evidence, not every historical result.
A docs-only change does not require repeating a live chain. Carry-forward must
name the unchanged component and originating candidate. Positive safety-critical
reader evidence cannot be borrowed from a different extractor.

## 7. Delivered tests, status and commands

**Fresh local execution:** 36 supplied controller tests passed. Thirteen new
integration regressions initially had 11 passes and two failures; after the
two small Python candidates all 13 passed. That is **49 passing tests** in the
final targeted run, with no skips. The new suite includes real file-only Git,
temporary journals and mocked browser calls. One existing controller test
contains 300 seeded traces; those are not 300 extra tests.

The supplied baseline modules were reconstructed and matched to the inline
hashes, allowing CRLF/LF equivalence where reported. Full integration/reference
suites, native PowerShell, Chrome, iPhone and capacity were **not run** here.
Twenty-seven native assertions are supplied for Windows; their result is
**NOT_RUN**. These deliverables do not clear F1 or qualify virtualized actionability.

Apply the additive plan/test patch to a review workspace, then review/apply
each tiny candidate as its named leaf. The patches do not touch the interrupted
PowerShell edit, installed routes or journals. See `START_HERE.md` in the
delivery for exact patch commands and preservation notes.

```sh
python3 -B -X utf8 -m unittest discover -s integration/tests -p test_a2_thin_loop.py -v
```

```powershell
powershell.exe -NoProfile -File integration/tests/test_a2_transcript_boundary.ps1
```

At LEAN-G1/G2 use the normal full-suite commands from the existing repository,
plus the relevant native tests. Missing required environment is `NOT_RUN`, not
a skipped success. For a case, report `PASS`, `FAIL`, `HOLD`, `ASSISTED` or
`NOT_RUN`, with offline/live scope stated separately. Never count a safety hold
as useful completed work.

**Next task: L01 on Windows, not another architecture or capacity exercise.**
L03/L04 already have locally tested candidate patches; review them as small
changes, but do not mistake them for the native reader repair.

## Sources

All S references are to the supplied inline mirror, not new GitHub fetches.

- **S1:** source files 0268–0274, especially `manifest.json`,
  `independent_review_e33ae7a/REPORT.md`, `REPRO.ps1`,
  `git_status.txt`, and `uncommitted_uia_adapter.patch`.
- **S2:** 0142 `docs/adr/0002-account-bound-resumable-runs.md`;
  0171 `PROGRESS.md`, bounded results and later G3 sections;
  0179 independent `0b6bfa3` offline acceptance;
  0185–0187 G2 preflight/recovery scope. These are historical reports.
- **S3:** 0066 `integration/uia_adapter.ps1::Get-ConversationTurns`;
  0054 `test_a2_l03_ps_action_gate.ps1`, final mixed-layout assertion;
  0274 interrupted diff. This supplied PowerShell body is **not** clean e33ae7a.
- **S4:** 0068 `WindowsUIA.observe/_probe_stale_view`;
  0048 `runner.dispatch_prepared/cycle`; 0043 CLI loop/deadline.
- **S5:** 0042 `account_routes.require_route/verify_saved_binding/verify_backend`.
- **S6:** 0002/0006/0013 original gates/cases/leaves; 0148 management summary;
  0241–0244 original simplicity statements. Archived plans are context.
- **S7:** 0223 `docs/PROTOCOL_AND_ADAPTER.md`, browser identity paragraph;
  0251 `succession/core.py`, `Response`, `consume`, `begin_send`, `confirm`, `load`.
- **S8:** 0188–0190 virtualized discovery/metadata findings; 0212 node readback.
- **S9:** 0047 `GitHandoffReader`; 0046 owner re-entry; 0001 capacity procedure.
- **Fresh results:** delivery `results/` logs, source-subset provenance and
  route-coupling characterization; these are this review's local checks only.
- **MS1:** Microsoft, *IUIAutomationElement::GetRuntimeId*, remarks:
  `https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getruntimeid`
- **MS2:** Microsoft, *Working with Virtualized Items*:
  `https://learn.microsoft.com/en-us/windows/desktop/WinAuto/uiauto-workingwithvirtualizeditems`

Only general UIA semantics were checked in external primary documentation;
that does not inspect the owner's actual browser or establish an alternative
message-reading capability.
