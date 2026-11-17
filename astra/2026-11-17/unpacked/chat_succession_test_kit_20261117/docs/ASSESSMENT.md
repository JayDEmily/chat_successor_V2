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
