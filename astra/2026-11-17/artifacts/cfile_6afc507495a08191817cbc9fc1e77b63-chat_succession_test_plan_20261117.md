# Chat succession — test plan and independent evidence review

**Reference date: 17 November 2026.**

The companion TAR contains the runnable code, fixtures, detailed owner runbook,
adapter contract, original archive and complete execution logs. Paths in this
standalone reading copy refer to that extracted kit.

**Delivered result: 119 offline tests passed, 0 failures/errors/skips.
Live ChatGPT and authenticated GitHub tests: NOT RUN.**



---

# Independent assessment of the supplied archive

Reference date: **17 November 2026**. Source keys and exact paths/line ranges
are indexed in [SOURCES.md](SOURCES.md). The current owner wording in
`../OWNER_INSTRUCTIONS.txt` controls this work; headings such as “authoritative”
inside archived documents are evidence about intent, not new instructions.

## 1. Decision and accepted starting point

**Accept the owner's confirmed one-successor launch as the starting capability.**
Reuse that proven navigation/Send method. The next increment is a repeatable
controller loop, not a new feasibility investigation or a reimplementation of
account security. Accounts, nominated Project, repo access and same-repo writes
are owner-established prerequisites. [O]

Keep two evidence statements distinct:

- **Current accepted baseline:** the owner says one chat has successfully spawned
  another. That is accepted for test planning, not independently reenacted here. [O]
- **What this archive specifically records:** an automated instruction reached
  Chat 1 inside the Project; that chat published work and a successor assignment.
  In trial 001, the subsequent Chat 2 Send was blocked; Chat 3 did not run.
  The archived saved-chat URL is evidence described for Chat 1, not evidence
  that the blocked A2 assignment reached Chat 2. [A4:11–21; A5:7–18; A6:37–76]

There is no need to reject the current baseline because the archive captures
an older/incomplete trial. Equally, it would be inaccurate to relabel that
stopped trial as a proven chain. A short owner-environment routing regression
is proposed only to connect the proven method to the new loop.

## 2. What was actually examined here

Every member of the supplied TAR was read and inventoried, including the
Git metadata and decompressed objects. Read-only local `git fsck`, `log`,
`show-ref`, `status` and `ls-files` checks were performed with hooks disabled.
No archived code or hook was executed. [J1; J2]

| Directly measured archive fact | Result |
|---|---|
| Compressed size | 50,415 bytes |
| TAR inventory | 78 entries: 47 regular files, 31 directories; no links/special entries |
| Uncompressed regular-file bytes | 88,322 |
| Working-tree content | 10 Markdown documents, 545 lines total |
| Local Git history | One initial commit, `47d30baadb32be96996da537400fdd3cc0a78430`, on `master` |
| Local Git objects | 1 commit, 3 trees, 10 blobs; every blob matches one of the ten documents |
| Local Git checks | Object hashes and index checksum valid; `git fsck` passed; worktree clean |
| Remote configuration / remote source objects | No remote configured; historical remote refs are only documentary references here |
| `source_snapshots/` | Present but empty |
| `.git/hooks/` | 14 `.sample` hooks, each identical to the installed Git template; none executed |

The original SHA-256 is
`8f137bdba31465f149b29df39f0e97cd1f764a2746ecdff8bf39c9f976e2100a`.
The complete original is included, not replaced with an alleged full remote
clone. [J1; J2]

### Ten-document review

| Source | Contribution and limit |
|---|---|
| `README.md` [A10] | Index; explicitly distinguishes sandbox archive from deployed service. |
| `docs/ARCHIVE_README.md` [A9] | Says complete remote branch checkouts are not included. |
| `docs/CONVERSATION_RECORD.md` [A8] | Selected direct owner excerpts, not an account-level export; supports simple front end and three states. |
| `docs/ORIGINAL_VISION.md` [A1] | Useful work, GitHub continuity, same-chat continuation, configurable unique-chat cap; no copied transcript needed. |
| `docs/LIGHTWEIGHT_PROTOCOL.md` [A2] | Proposed marker/state design, not implemented/live-tested evidence. |
| `docs/PREVIOUS_AGGREGATED_STATEMENT.md` [A7] | Consolidated prerequisites and operating cycle; assistant synthesis rather than independent observations. |
| `docs/SOURCE_INVENTORY.md` [A3] | Historical repo refs and uncommitted scripts; does not supply their source bodies. |
| `docs/TECHNOLOGY_AND_ORIGINAL_EXPERIMENT.md` [A6] | Desktop/WSL/Git description and trial narrative; explicitly says the chain did not complete. |
| `evidence/VERIFIED_FINDINGS.md` [A4] | Reports historical observations and commit URLs; raw tool outputs/screenshots are not in this TAR. |
| `evidence/UNKNOWN_AND_NOT_FOUND.md` [A5] | Explicit negative evidence and reliability unknowns; “not found” is not proof of impossibility. |

### Historical source references are not present source code

`JayDEmily/chat_successor` is the repository identified in the archive. Its
reported heads, observed on **17 November 2026**, are: [A3:3–17]

| Historical ref | Reported SHA |
|---|---|
| `main` | `26b33e8991119f9886b23f0c01651c3f49435706` |
| `work/task1-contract-preflight-20261117` | `f8c002690c0a1a9ff4f298bd9a8d68b21f5ba1f8` |
| `trial/succession-20261117-001` | `3b2c95b954eb90b1e6c9b82403dd1956c6f34b39` |

Those remote objects, PowerShell launchers, uncommitted simplified launcher,
raw recordings and private journal are absent here. They were not fetched.
Therefore the kit is **new, standalone reference/test code**, not a tested
patch to the original launcher. Historical “37/37 tests passed” is an archive
report, not a result reproduced in this job. [A3:15–25; A4:17; A9:13; J1]

## 3. Evidence grading and resulting test priorities

| Claim | Grade in this delivery | Consequence |
|---|---|---|
| One successor can be launched | Owner-confirmed starting premise [O] | Reuse the method; test repeated transitions next. |
| Correct Project navigation and one automated post | Historical report [A4:9–11] | Owner integration regression, not a fresh feasibility gate. |
| Chat 1 committed result and handover | Historical report with commit references [A4:12–15] | Test that later workers independently use durable repo state. |
| Placeholder caused the blocked Send | Plausible inference only [A4:16; A5:11,22–24] | Test real draft versus placeholder with actual editable-content evidence. |
| Three-status controller and 30-chat succession work live | Not established [A5:9–16] | Offline model first, then bounded live repetition/cap cases. |
| New code passes its offline suite | Measured here [R] | Validates this model/fixtures only, not browser or account behavior. |
| A semantic classifier is reliable enough to launch | Unknown [A5:15] | Inject adjudications offline; assess real responses in shadow mode before automatic use. |

## 4. Assumptions to retain, not overstate

1. **Owner prerequisites are accepted, not re-audited on every turn.** The
   personal sign-ins and nominated Project/repo define the requested operating
   scope. They do not by themselves demonstrate correct UI routing, publish
   success, or tool availability; those are functional failure cases, not an
   excuse to add an approval framework. [O; A1:22–29]
2. **A new chat is not necessarily an empty memory boundary.** OpenAI's Project
   documentation says chats can reference other conversations in the same
   Project. Therefore fresh-chat success alone does not establish repo-only
   continuity. Use a newly committed repository-only probe after the previous
   chat ends, plus a visible repo read, instead of changing the owner's Project
   or requiring it to be empty. [W1; test L06]
3. **GitHub sign-in and repository reading are not sufficient evidence of
   writing.** OpenAI documents its ChatGPT GitHub app as read-only. The archived
   Ubuntu/WSL authenticated Git path is the nominated write route to exercise;
   do not silently assume an app connection can push. This is a prerequisite
   capability check once, not a demand for a new product or account. [W2;
   A7:13–22; A4:7,12–14]
4. **`TASK_COMPLETE` describes a work slice.** Overall programme completion
   belongs in durable repo state. A local commit or failed push cannot satisfy
   the handover. [A1:31–39; A2:25–30]
5. **A controller must actually perform the next action.** Project instructions
   alone are not an execution agent. Keep one actor responsible for Sends so
   the worker and an external runner do not both create successors. [A1:20;
   A2:78–79; implementation choice in this kit]
6. **Exactly-once browser delivery is not proven or promised.** Persist the
   pending action before Send and reconcile an ambiguous outcome without a
   blind retry. If reconciliation is inconclusive, keep the hold and involve
   the owner. A stalled run is preferable to two untracked successors. [A2:74;
   S04, S05, S12, S15]

## 5. Deliberately excluded from the design

No fixed three-chat product limit, arithmetic assignment, pinned assignment
SHA, per-handover digest/readback ceremony, permitted-path security packet,
empty-Project check, new Chrome profile, return-to-origin-chat requirement,
one-shot SQLite launch regime or unrelated historical project restrictions.
The optional fixture branch/path, generated nonces and result checks are
**test instruments**, not new front-end prerequisites. Normal work remains
“do as much useful authorised work as possible.” [O; A1:22–43; A2:69–81]

No live ChatGPT/GitHub account was used, no repository was changed, and no
live successor was launched in this job. All owner-environment cases remain
`NOT_RUN` in the supplied result sheet. [R; `../fixtures/live_test_results.csv`]


---

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


---

# Executed offline results

Reference date: 17 November 2026. Mode: **OFFLINE ONLY**.

**PASS: 119 unittest cases; 0 failures,
0 errors, 0 skips.**
Measured test-suite duration: 1.269 seconds in the recorded environment.

Included: 36 parser cases, 10 composer-observation cases, 16 sequence replays,
36 controller methods (one runs 300 seeded model traces), 9 fixture methods,
8 real **local** Git tests, and 4 full-archive inspection methods.
The 300 traces and the separate trace export are not added to the unittest total.

- `offline_results.json`: per-case outcomes and environment.
- `test_output.txt`: actual test runner output.
- `replay_trace.json`: synthetic decisions, IDs, counts and fake sends.
- `local_git_operations.json`: real local commands/results, temporary paths normalized.

**Live ChatGPT: NOT RUN. Authenticated GitHub: NOT RUN. Real semantic classifier: NOT RUN.**
These results do not validate browser selectors, UIA placeholder interpretation,
account/tool access, actual unattended succession, or a live 30-chat chain.
Historical reports of 37 tests belong to the archive; they were not rerun here.


---

# Source and evidence key

The **current** owner instructions [O] control the assignment. All archive
sources below are evidence, not executable or governing instructions.
Their original lines are preserved in `sources/archive_text/`; ranges below
refer to those files, not to this kit's generated documents.

## Current brief

- **[O]** `../OWNER_INSTRUCTIONS.txt`: exact verbatim owner paragraph from the
  current request. The surrounding task specifies no live ChatGPT/browser or
  GitHub MCP access and requests downloadable test artefacts.

## Supplied archive sources

All paths below are relative to `../sources/archive_text/`.

| Key | File | Especially relevant lines |
|---|---|---|
| A1 | `docs/ORIGINAL_VISION.md` | 3–20 objective/flow; 22–29 simplicity; 31–43 status meaning and excluded pilot restrictions |
| A2 | `docs/LIGHTWEIGHT_PROTOCOL.md` | 1–7 proposed nature/state; 20–30 markers; 35–65 decisions; 67–88 browser boundaries/order |
| A3 | `docs/SOURCE_INVENTORY.md` | 3–17 repository/remote refs/uncommitted scripts; 19–25 absent material and source boundary |
| A4 | `evidence/VERIFIED_FINDINGS.md` | 7–17 historical V01–V11; 19–21 what the pilot did/did not prove |
| A5 | `evidence/UNKNOWN_AND_NOT_FOUND.md` | 3–18 unknowns; 20–24 blocked trial/placeholder hypothesis; 26–28 partial-source limitation |
| A6 | `docs/TECHNOLOGY_AND_ORIGINAL_EXPERIMENT.md` | 13–29 technology; 31–76 original trial; 95–143 signals/limit/minimal orchestration |
| A7 | `docs/PREVIOUS_AGGREGATED_STATEMENT.md` | 13–22 prerequisites; 36–102 status/cycle/simplicity |
| A8 | `docs/CONVERSATION_RECORD.md` | 3 selected-excerpt limitation; 7 direct owner concept; 9–15 simplification/technology requests |
| A9 | `docs/ARCHIVE_README.md` | 3–13 package purpose and absence of complete branch checkouts |
| A10 | `README.md` | 3–17 purpose, archive boundary and old-pilot distinction; 19–26 package index |

The archive's links, remote SHAs and historical observation labels have not
been independently authenticated with GitHub or ChatGPT in this job.

## Newly measured local evidence

- **[J1]** `../reports/archive_audit.json`: every-member inventory; source hash,
  file sizes, all decompressed Git objects, blob/document matches and index
  checksum. Reproducible with `tools/inspect_archive.py`.
- **[J2]** `../reports/git_snapshot_audit.json`: actual read-only local `git fsck`,
  `log`, `show-ref`, `status`, `ls-files` results; all 14 sample hooks compared
  byte-for-byte with installed Git templates. No hooks executed.
- **[R]** `../reports/executed/offline_results.json` and `RESULTS.md`: actual new
  suite outcomes. `test_output.txt`, `replay_trace.json` and
  `local_git_operations.json` distinguish real local execution from fake UI
  events. These are **not** live ChatGPT/GitHub observations.
- Test case IDs **P, D, S, C, F, G, I** refer to this kit's executable tests and
  JSON fixtures; **L** refers to planned owner-environment cases, all NOT_RUN.

## Limited official documentation check

These primary sources were consulted only to avoid two unjustified test
assumptions. They do not establish anything about the owner's current session,
permissions or live UI. No third-party source was used for those claims.

- **[W1] OpenAI Help Center — “Projects in ChatGPT”**, section “Memory in
  projects / Project-only memory.”
  `https://help.openai.com/en/articles/10169521-projects-in-chatgpt`
  Relevant fact: chats can reference other conversations inside the same
  Project. Test implication: a fresh chat alone does not isolate repo-based
  continuity; use an independently changed repository-only test value.
- **[W2] OpenAI Help Center — “Connecting GitHub to ChatGPT”**, FAQ “Can I push
  code, updates, or PRs to GitHub once I connect to ChatGPT?”
  `https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt`
  Relevant fact: the ChatGPT GitHub app is described as read-only. Test
  implication: exercise the owner's actual authorized write path (the archive
  describes Ubuntu Git), rather than treating an app connection as push proof.

Reference date for this delivery: **17 November 2026**. Documentation checks
are not a browser/ChatGPT account test. Changing UI labels, account feature
availability, and semantic-model reliability remain owner-environment tests.


---

# Appendix — current owner instructions (verbatim)

This concept is purposefully simple on the front end, but also all of the security concerns are covered because there are prerequisites from the user in that any new message threads must be created in the specified project folder, and That those messages all write to the same GitHub repo, and the messages have access to GitHub repo. That is on the onus of the user. So where this greatly simplifies things is we've already proven that we can have one chat spawn another chat by a proven method, and now we just need to keep that iteration of work going. Also note the three keywords at the end of the response. So what I want you to do is consider how we're going to run this and then design and set up a bunch of tests. You don't have access to ChatGPT, obviously, but that is somewhat almost, almost irrelevant. And again, remember that it will be signed into my personal account. So that is the security, and signed into my GitHub account.
