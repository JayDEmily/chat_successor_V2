# Test design: from one proven launch to repeatable succession

**Scope:** the current owner's instructions, the nominated Project, and
`JayDEmily/chat_successor` (unless the owner expressly nominates a replacement).
All workers in a run use that same repo and working branch. The archive's
Project identity/name is prefilled as an example in `config.example.json`;
the working branch is intentionally left for the owner to nominate.
This is not a proposal for another service, watcher or approval system. [O; A1; A2]

**Execution distinction:** `O` means executable offline here; `L` means it
requires the owner's authenticated ChatGPT/desktop/Git environment.
A fake UI test is not a live ChatGPT test. A local bare Git repo is not GitHub.

## 1. Small operating contract

| Completed worker response | Expected action | Unique-chat count |
|---|---|---|
| `CHAT_STATUS: NEED_MORE_TIME` | Same thread: “Okay, continue working.” | Unchanged |
| `CHAT_STATUS: TASK_COMPLETE`, published handover, work remains | Create one successor inside nominated Project; send short repo/branch pointer | Add observed new ID once |
| `CHAT_STATUS: TASK_COMPLETE`, programme finished | Stop | Unchanged |
| `CHAT_STATUS: TASK_COMPLETE`, work remains, already at cap | Stop without another new-chat action | Unchanged |
| `CHAT_STATUS: ERROR` | Stop automatic posts; surface blocker and current context | Unchanged |
| Partial/missing/ambiguous reply, uncertain Send, unavailable state | Wait or hold; do not infer success | Unchanged until a real new ID is reconciled |

The initial worker counts as one. Existing unrelated chats in the Project
are neither forbidden nor added to this run's count. A pending launch is not
a counted chat. `WAIT`, `HOLD`, `STOP_FINISHED` and `STOP_CAP` are internal
controller outcomes, **not extra worker keywords**. [A1:11–18,31–39; A2:35–81]

Canonical markers are uppercase final nonblank lines. The model also accepts
an exact bare final keyword to accommodate the owner's simpler wording.
Quoted/fenced/code examples, user messages and tool output cannot act as
status signals. Missing-marker semantic interpretation is a separate,
reasoned adjudication seam, not substring matching or a claimed working NLP
classifier. Ambiguity always holds. [O; proposed clarification; P01–P36]

## 2. Practical sequence

### Stage A — delivered now: offline confidence, not live proof

Run `python3 run_offline.py`. The included execution passed **119/119 tests**
with no skips. Read the failure/skip distinctions in the runner before using
a partial local result as a pass. [R]

| Area / test IDs | Procedure and fixture | Pass oracle |
|---|---|---|
| Archive boundary I01–I04 | Inspect all TAR members, Git objects/index; reject special/path-traversal inputs | Exact uploaded archive accounted for; no hidden launcher checkout asserted |
| Parser P01–P36 | Replay exact/bare markers, whitespace, streaming, examples, duplicates, malformed/absent statuses and injected semantic verdicts | Only one unambiguous completed assistant status controls an action |
| Routing C01–C13, C29, C33 | Feed current/foreign assistant events, all three statuses and repo states | Correct branch of the three-state loop; no fabricated completion |
| Unique IDs C14–C22 | Simulate 1→30; 100 same-chat continuations; URL aliases and duplicate events | 30 actual synthetic IDs maximum; no 31st; repeats do not inflate count |
| Persistence/recovery C23–C28, C30–C31, C34–C36 | Persist prepared/sending state; restart; inject lost ack; preserve draft; repair only after explicit reconciliation | No blind retry or reset count; owner holds remain recoverable |
| Composer D01–D10 | Replay actual-text/Value/placeholder/attachment observations | Real text preserved, even if identical to placeholder; Value alone remains unknown |
| End-to-end replays S01–S16 | Golden event sequences through fake UI + JSON state | Per-event action, count, pending phase and fake-send totals match the fixture |
| Workload F01–F09 | Generated category/count/total task, repo-only probe, duplicate/stale/bad outputs, 31-slice fixture | Substantive result/state verified; test fixture does not overwrite owner files |
| Git transport G01–G08 | Real local bare repo, separate worker clones, commits/pushes; failed push/wrong branch/unavailable remote | Published state can be picked up cold; local-only or wrong-branch state cannot masquerade as a handover |
| Model robustness C32 | 300 seeded traces with varied caps and statuses, compared with a small independent oracle | No count inflation, cap breach or incorrect three-state action |

These cases test the **new model** and test workloads. G08 verifies incorrect
work is detectable by the workload validator; it does not claim the controller
can assess arbitrary job quality. D01–D10 test interpretation of supplied
observations, not how Chrome/UIA actually exposes an editor.

### Stage B — connect the existing proven method, owner environment

No new account setup is requested beyond the owner's prerequisites. Nominate
the branch, load the short Project instructions and connect the existing
launcher to the adapter seam. Capture results in `fixtures/live_test_results.csv`.
Use one small same-repo test path, not production job data. [O; owner runbook]

| ID | Procedure / stimulus | Required observation and pass condition |
|---|---|---|
| **L01** | Two-slice run with the proven Project-new-chat route; first worker publishes slice 1 and emits `TASK_COMPLETE` | Exactly one successor Send; new observed ID in same Project; same repo/branch; slice 2 read/produced from repo; final programme stop |
| **L02** | Ask test worker to emit `NEED_MORE_TIME` twice while doing useful fixture preparation, then finish slice | Two prompts in same ID; no fresh chat until later `TASK_COMPLETE`; count unchanged by continuations |
| **L03** | Introduce a test-only material blocker; worker emits `ERROR`; owner later repairs and resumes | Blocker visible; no automatic Send while held; next owner-approved work continues without resetting count/replaying the old response |
| **L04** | One-slice programme with cap well above 1 | Published `programme_complete=true` plus `TASK_COMPLETE` stops immediately, rather than consuming unused chat budget |
| **L05** | Cap=2, fixture has 3 slices; exercise a same-thread continuation at chat 2 | Two observed run IDs only; `NEED_MORE_TIME` still stays in chat 2; next slice completion with work remaining stops at cap |
| **L06** | After previous chat ends, update a repository-only nonce/next task; send only the ordinary short pointer | Successor visibly reads correct repo/branch and produces result using new value not supplied in the prompt; no copied transcript |
| **L07** | Read-only editor observations: empty/placeholder, real draft, draft literally equal to placeholder, attachment-only draft | True blank can proceed; actual draft/attachment remains untouched; ambiguous observation holds; no blanket `Value != ''` rule |
| **L08** | Start with a non-nominated composer active but nominated Project visible in sidebar; also test a nominated Project with many existing chats | No Send to wrong composer; correct Project control used; existing chats neither rejected nor counted in run |
| **L09** | Interrupt adapter after Send but before ack; restart it; repeat for same-chat continuation | Read-only reconciliation identifies actual submission; no duplicate Send; successor counted once, continuation count unchanged |
| **L10** | Streaming/truncated/missing/conflicting markers, plus clearly worded missing-marker replies in shadow mode | No early Send on streaming text; ambiguity holds; semantic labels and reasons recorded separately from deterministic parsing |
| **L11** | Inject a one-time publish failure or missing repo/tool capability within test adapter/workspace | Worker reports `ERROR` or controller holds; no local-only/failed publication treated as completed handover; repair is explicit |
| **L12** | Slow/no response, tool/session loss, owner pause | No inference of success; no blind retry/login loop/new chat; owner sees current chat, pending action, reason and elapsed wait |
| **L13** | Five-chat unattended chain; repeat on 3 separate small runs after L01–L12 | Useful valid results, exactly expected IDs/handovers, no manual prompt transfer and no unexplained duplicate/misroute |
| **L14** | Optional long-run test: cap=30 with 31 fixture slices, initial chat included | Exactly 29 successor launches at most; chat 30 may continue in-thread; `TASK_COMPLETE` with work remaining cannot create chat 31 |
| **L15** | Supply stale/incorrect fixture result or missing next-task state on test branch | Worker detects/repairs work or emits `ERROR`; stale/malformed programme state causes hold; independently validate useful work, not just happy status text |

Every L-case is **NOT RUN in this API job**. Some are deliberate adapter fault
injections in the owner's environment, not naturally occurring ChatGPT/GitHub
outages; label them accordingly. Exact steps and recovery are in
[OWNER_RUNBOOK.md](OWNER_RUNBOOK.md).

### Stage C — use on a real job

Promote only what the evidence establishes. After the bounded integration
works, use the same short pointer against the real repo instructions; remove
artificial one-slice-per-chat fixture constraints. The proposed 2→5→30
progression controls test cost and localizes faults, not a fixed product limit
or a set of per-chat approvals. The owner can combine/reorder live cases if
all observations remain covered. A 30-chat exercise is optional until its
account/time cost is acceptable; do not label the feature “live validated to
30” if only small-cap or offline tests were run.

## 3. Fault-recovery expectations

- **Response slow/incomplete:** observe without posting. An owner-selected
  silence deadline may hold the run; timeout is not `TASK_COMPLETE`. No fixed
  number of `NEED_MORE_TIME` turns is imposed by this design.
- **Send outcome unknown:** persist pending action, do not repost; inspect
  existing UI/message/history. If the message is found, adopt its real ID.
  If positive evidence proves it was not sent, explicitly rearm the action.
  Absence in a possibly stale sidebar alone is not proof of non-delivery.
- **Real worker `ERROR`:** stop, show explanation, preserve work and count.
  Owner repair/resume is separate from normal automatic continuation.
- **Unreadable/stale/contradictory repo state:** hold rather than use old chat
  memory. A normal current-branch read determines remaining work; no digest
  catalogue or immutable assignment pinning is introduced.
- **Lost/corrupt controller state:** do not silently start with count=1.
  Reconstruct from observed run IDs and pending UI evidence, or keep stopped.
- **Owner stop:** takes effect before the next Send. A click already in flight
  still needs reconciliation; it cannot be “unsent” by the bookkeeping file.

## 4. Acceptance and honest reporting

For each bounded run record:

- actual distinct run IDs (initial + successors), continuation count, expected
  versus observed launches, and any unknown/duplicate submissions;
- Project identity of the active destination, same repo/branch and current
  programme state, normal commit references as evidence (not launch pins);
- final assistant text, completed/streaming observation and stable response
  event identity; status interpretation basis and action;
- work-result validation, repo-only probe outcome, stops/recoveries;
- observed timing and owner interventions, with no cookies/tokens in evidence.

**Minimum integration acceptance:** no wrong-destination posts, no duplicates,
no cap breach, no auto-post after `ERROR`/finish/owner pause, and useful
published work survives each tested handover. Unknown outcomes must hold
correctly; they are not counted as successful handovers. A fault-injection
case can PASS by demonstrating the correct hold.

Report parser accuracy, live launch success and work correctness separately.
For semantic shadow cases, record a confusion table with particular attention
to false `TASK_COMPLETE`; zero such errors in the sample is an acceptance
target, not proof of general reliability. The delivered fallback has **zero
real classifier evaluations**. A bounded successful chain likewise provides
no guarantee of indefinite succession.

**Delivered measurement:** 119 offline unit/integration cases passed, 0
failures/errors/skips; all L-cases await the owner environment. [R]
