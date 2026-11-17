# Owner-environment runbook — all live cases NOT RUN here

This runbook is for the already authenticated personal environment described
by the owner: nominated ChatGPT Project, same GitHub repo and working branch,
authorized desktop control and the necessary tools. It does not request
credentials or require a separate browser profile. The archived stack is
Chrome on Windows with an authorized desktop controller and Ubuntu/WSL Git;
reuse the owner's working equivalent. [O; A6:13–29]

The missing integration is the **live adapter** described in
[PROTOCOL_AND_ADAPTER.md](PROTOCOL_AND_ADAPTER.md). The test kit has no live
Send command. Connect the proven launcher to that seam in the owner's
environment before marking an end-to-end test as automatic. Manually clicking
through a scenario can validate observations, but cannot prove unattended
controller operation.

## 1. One-time run setup

1. Nominate the Project and repo/branch once. The archive names **Chat
   succession folder**, Project ID `g-p-6afbfc5e59248191a8c690296b24c8ef`, and
   `JayDEmily/chat_successor`. Those are historical identifiers to match to the
   owner's nominated environment, not assumed currently accessible here.
   Existing chats in that Project are fine. [A4:9–11; A3:3–13]
2. Choose an owner-approved test branch and subdirectory **in that same repo**.
   Do not overwrite the existing job instructions or reuse a stopped run's
   pending state. A fresh test run is for unambiguous measurements, not an
   inherited one-shot security rule. No force push, history rewrite or journal
   reset is part of these procedures.
3. Add the concise Project instructions in `prompts/`, and one repo-level
   pointer to the active fixture instructions/state. Use the existing
   authenticated Git write path. If only a read-only app is available, the
   prerequisite of publishing work is not met; identify the real write tool
   once rather than inventing a successful push. [W2; A7:13–22]
4. Start the first worker inside the Project, capture its saved conversation
   ID, and initialize the single controller with it. Count=1, regardless of
   how many unrelated chats already exist.
5. Set the planned cap and, if wanted, an owner-selected silence/overall-time
   budget. These time budgets are adapter/run policy, not a limit on the number
   of `NEED_MORE_TIME` responses. Show pause and the current pending action in
   the simple controller output.
6. Create one evidence record per test/run from the supplied template. Record
   observed timestamps, not this package's reference date as a fake live time.
   Never export login cookies, tokens, passwords or unrelated conversations.

### Create a small fixture locally

These commands only generate files; nothing below logs into ChatGPT or
pushes to GitHub:

```sh
KIT=/path/to/chat_succession_test_kit_20261117
REPO=/path/to/your/nominated/chat_successor
RUN_ID=succession-test-20261117-a
FIXTURE="$REPO/succession-tests/$RUN_ID"

python3 "$KIT/tools/repo_fixture.py" init   --root "$FIXTURE" --steps 2 --run-id "$RUN_ID"
python3 "$KIT/tools/repo_fixture.py" verify --root "$FIXTURE"
```

The fixture contains five files: `INSTRUCTIONS.md`, `RUN.json`, `STATE.json`,
`RESULTS.json` and the self-contained `fixture_tools.py` validator/helper. Its task is to normalize small category-labelled records and
produce counts/totals, recording the repository-only probe value used.
It is a deliberately bounded workflow test, not the old arithmetic pilot.

The owner commits/pushes these files and the repo's single active-work pointer
using normal Git on the nominated branch. First confirm the seed is actually
available to workers; then start. Do not pass results, nonce values or the
previous conversation in successor messages. The fixture's `last_chat_id`
can be obtained through the authorized desktop address observation or the
adapter's observed-publish attribution; it must not be invented.

For deterministic **offline** demonstrations only, `simulate-slice` can
perform the fixture transformation. In a live work test, record whether the
worker authored the result or invoked that helper. Either can test file/tool
continuity, but a helper invocation is not proof of independent model reasoning.

## 2. First bounded cycle and all three branches

### L01 — integrate one successor, then finish

Use two fixture slices and cap=3 or higher. Observe the first worker read
current repo state, produce slice 1, validate it, commit and **push** it.
Its completed assistant response ends in `CHAT_STATUS: TASK_COMPLETE`.

Let the controller—not the owner—open the nominated Project's new-chat
composer and Send the ordinary short repo/branch pointer once. Record the
new saved ID and active Project. The successor must read the published state,
produce slice 2 and publish the overall completion flag. The controller stops.

**Pass:** 2 unique run IDs, 1 successor launch, 2 correct published results,
same Project/repo/branch, no pasted prior transcript, no further Send after
programme completion. Use ordinary commit links/IDs as evidence; do not add
a per-launch hash comparison. This integrates the accepted launch proof with
the new loop; it is not an attempt to re-prove the concept from zero.

### L02 — same-chat continuation

Use a fresh small fixture with work remaining. The repo's temporary test
instructions ask the first worker to perform input inspection, emit
`NEED_MORE_TIME`, do another useful preparation/check after continuation,
emit `NEED_MORE_TIME` again, then complete the slice on the next turn.
This forced segmentation is **only a protocol stimulus**.

**Pass:** “Okay, continue working.” appears twice in the same saved ID; the
unique count does not change; only the later published `TASK_COMPLETE`
can trigger one successor. Capture response/turn identities to show a
poll/repeated observation did not cause extra prompts.

### L03 — material error and owner recovery

In the test path only, nominate an intentionally unavailable required input
or inject an unrecoverable test-tool failure. Do not revoke the owner's
account or interfere with unrelated work.

**Pass:** the worker explains the blocker and emits `ERROR`; controller
posts nothing automatically. The owner restores the input/tool and resumes.
Preserve run IDs and already-consumed events. A new work turn may continue;
do not replay the old terminal response or reset the count.

### L04 — overall completion early

Use one slice, cap=30. Publish a correct final result with
`programme_complete=true` and no next task, followed by `TASK_COMPLETE`.

**Pass:** stops after that worker. This distinguishes “slice finished” from
“whole programme finished.” A contradictory state (finished plus next task)
belongs to L15 and must hold.

### L05 — small-cap boundary

Use cap=2 and **3** fixture slices so work remains at the boundary.
Before chat 2 finishes its slice, exercise one `NEED_MORE_TIME`.

**Pass:** continuation stays in chat 2; its next published `TASK_COMPLETE`
stops at the cap. No new-chat action or Send for chat 3. Existing older chats
in the Project are irrelevant to this run's count.

## 3. Repository continuity and useful work

### L06 — repo-only change after prior chat ends

At a chosen handover, pause dispatch **before Send**. After the predecessor's
final response, change the next input/probe only in the repo:

```sh
python3 "$KIT/tools/repo_fixture.py" rotate-probe --root "$FIXTURE"
```

Commit/push that change on the same branch without pasting its value into a
chat. Resume the prepared dispatch, sending only the usual pointer. Observe
the successor's actual repo/file/tool read and validate its new result.

**Pass:** correct new probe and task content appear in the result. A fresh
chat alone is insufficient evidence of repo use because Project chats can
reference other Project conversations. [W1] The probe is non-secret test
data; it is not an authentication token or a production handover requirement.
Also test a stale branch view: refresh the correct branch or hold, never
invent access or substitute an old transcript.

### L15 — correctness, stale state and corruption

On the test branch, deliberately alter a completed result or point next work
to missing data. In a separate adapter-state variant, present stale
last-worker attribution, a string instead of a completion boolean, or a
finished state that also has remaining work.

**Pass:** the workload validator/worker detects incorrect work and repairs
or reports the blocker; the controller holds contradictory/stale metadata.
A `TASK_COMPLETE` string is not independent evidence of useful work.
The reference controller only checks handover metadata; it does not replace
arbitrary engineering tests or know whether a fabricated observation is true.

### L11 — publication/access failure

Prefer a scoped one-shot failure injected into the test tool/adapter, or a
real non-fast-forward conflict confined to the test branch. A conflict the
worker can resolve itself may properly use `NEED_MORE_TIME`; an unresolved
material blocker uses `ERROR`. Do not intentionally damage the repo or alter
account-wide permissions.

**Pass:** local edits/commits are not counted as a published handover while
push failed; no successor is launched on unavailable repo state. Repair and
retest. Distinguish a tool-failure injection from a real GitHub permission or
network failure in the evidence record.

## 4. Browser and recovery regressions

### L07 — isolate the placeholder issue read-only first

Prepare separate known conditions in a disposable nominated-Project composer:
(a) genuinely empty with placeholder, (b) a deliberately typed real draft,
(c) a draft literally equal to the placeholder string, (d) attachment only.

Capture the rendered editor plus available UIA/editor observations and the
ground-truth preparation for each. Probe without Send or clearing text.
Do not reuse someone else's unsent draft as test data.

**Pass:** actual editable content distinguishes (a) from (b)–(d); ambiguous
observations hold. Never blanket-ignore text equal to the placeholder, and
never infer a real draft merely because UIA Value is nonempty. A new result
does not retroactively prove the exact Value during the old blocked attempt.
[A4:16; A5:11,22–24]

### L08 — destination and nonempty Project

With an unrelated composer active and the nominated Project only visible in
the sidebar, ask the adapter to prepare a successor, initially stopping
before Send. Confirm it actually uses the nominated Project's new-chat route.
Repeat with several existing chats in that Project.

**Pass:** no typing/Send to unrelated composer; correct active destination
confirmed; no “Project must be empty” rejection and no counting old chats.
Continue using the already-authenticated browser; a new tab is sufficient
where the proven method supports it. [A2:67–74]

### L09 — lost acknowledgement and process restart

Add test hooks at two points in the owner adapter:
1. after saved `sending` state but before click (definitely not submitted);
2. after click/Send but before observed chat ID is saved (possibly submitted).

Repeat (2) for `NEED_MORE_TIME`, where duplicate continuation is also harmful.
Restart with the saved state. Inspect the existing UI/message read-only.

**Pass:** unknown outcome never automatically retries. A visible submitted
message is adopted, with the actual new ID counted once (or the same ID for
continuation). Positive before-click evidence permits explicit rearming.
A missing entry in a stale sidebar does not. If unresolved, keep held and
record that result rather than manufacture a successful handover.

### L10 — incomplete/ambiguous status and semantic fallback

Test streaming/partial replies, status examples inside code, conflicting
markers and no marker. If asking the worker for a malformed response does
not produce one, inject the captured/synthetic response at the observation
seam; label it **adapter fault injection**, not natural model behaviour.

For semantic fallback, run a non-sending shadow set containing clear examples
of each of the three meanings plus ambiguous cases. Record the owner-reviewed
label, classifier label and reason, and false-completion count. Do not call
injected JSON verdicts a tested semantic model.

**Pass:** no streaming/example/ambiguous response causes a Send. Explicit
markers control when valid. Uncertain semantic decisions hold. Automatic
semantic fallback is optional until the chosen real classifier has evidence;
a conservative hold uses the same three worker statuses, not a new protocol.

### L12 — silence, session loss and owner pause

Induce a controlled delayed observation and a missing-tool/session condition
in the test adapter, or use a naturally observed occurrence. Set a suitable
owner silence deadline, not a guessed “response complete” delay.
Pause once while idle and once while an action is prepared.

**Pass:** no success inferred from silence, no blind resend, no automatic
account/login loop, no Send while paused. A click already in flight is
reconciled, not undone. Show reason, current ID, repo/branch, last status and
pending action so the owner can recover without copying entire histories.

## 5. Repetition and the real limit

### L13 — five chats, repeated

Run three separate five-chat fixtures, without manual handover or corrective
prompting during normal paths. Collect per-run start/end times, useful-result
validations, number of continuations, launches, interventions and failure modes.

**Pass:** each run reaches its planned finish with exactly five run IDs and
four successor launches; no duplicates or misroutes. If the workload finishes
earlier unexpectedly, classify that observation rather than claiming the
planned five-chat chain. Repeatability measured here is bounded, not a
general reliability guarantee.

### L14 — optional 30-chat run

Only when the owner wants the longer exercise, generate **31** slices and
set cap=30. The extra unperformed slice ensures stop-at-cap is distinguishable
from ordinary programme completion. Include `NEED_MORE_TIME` near the boundary.

**Pass:** initial worker + at most 29 successor launches = 30 observed IDs.
Same-thread continuation at chat 30 is allowed; a later `TASK_COMPLETE` with
work remaining produces no chat 31. A timeout/error holds the run and is
reported; it must not be hidden by resetting state or silently restarting a
new budget. Do not claim L14 PASS from the offline 30-ID simulation alone.

## 6. Evidence, recovery and cleanup

Use `fixtures/live_record.template.json` for detailed events and
`fixtures/live_test_results.csv` for a summary. For each case record:
actual run/test identity, scenario type (real or injected), Project/repo/branch,
saved chat IDs, whole completed assistant response and response identity,
interpretation basis, action, count before/after, publish outcome, normal
commit references, expected/observed result, and artifact paths.
Keep unsuccessful/held runs as evidence.

In a failure, stop automatic posting, preserve state and any draft, inspect
only the nominated context, resolve actual cause, then explicitly resume or
end the run. Do not “repair” evidence by deleting a pending action or changing
the count until an observed submission has been reconciled.

After a test, restore the normal repo work pointer/temporary test instructions
and stop the test controller. Preserve the test branch/artifacts for review;
do not automatically delete chats, reset unrelated work, or change account
settings. No extra approval is needed for each ordinary successor once the
owner has started the bounded run.
