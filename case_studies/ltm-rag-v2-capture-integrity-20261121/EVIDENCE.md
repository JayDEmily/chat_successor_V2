# Evidence catalogue — commits, reviews, automation and hosted CI

This catalogue identifies **observed records**, **reported results**, **reproduced tests**, and **not-established capabilities** separately. The files under evidence/ are frozen copies of GitHub data at collection time, not a claim that a PR or external record will never subsequently change.

## A. Source-of-truth repository records

**Public V2 implementation:** https://github.com/JayDEmily/LTM_RAG_V2

| Commit | Description | Source for readback |
| --- | --- | --- |
| 0aa4b8042fc60991aa8a7d9d2278314b52efa24d | Public sanitised V2 root/base, main at case checkpoint | https://github.com/JayDEmily/LTM_RAG_V2/commit/0aa4b8042fc60991aa8a7d9d2278314b52efa24d |
| 65820f3c36d59d5636cc03e260e1666e6ca5836e | First integrity repair: reservation and acknowledgement text/role/outbox validation | https://github.com/JayDEmily/LTM_RAG_V2/commit/65820f3c36d59d5636cc03e260e1666e6ca5836e |
| d27acd1ab6d06031ffc773c855907cfd8362027a | Second repair: canonical source/message/version ID consistency | https://github.com/JayDEmily/LTM_RAG_V2/commit/d27acd1ab6d06031ffc773c855907cfd8362027a |
| 8d27bd55d4abf0c5f864b60a33f24d666920a130 | Final repair: verified source integrity, consistent revocation snapshots and scoped coverage | https://github.com/JayDEmily/LTM_RAG_V2/commit/8d27bd55d4abf0c5f864b60a33f24d666920a130 |

**Observed cumulative diff:** exactly three modified paths, three commits ahead of the V2 root and zero behind: vnext/ltm_vnext/capture_foundation_v.py; vnext/tests/test_capture_foundation_v.py; vnext/PROGRESS.md. The preserved artifact baseline-to-final-compare.json is a GitHub compare-result snapshot. The complete source archives and the three individual Git binary-safe patches allow the actual code to be inspected independently of a summary.

**Private reviewer-automation repository:** https://github.com/JayDEmily/chat_successor (requires authorised access). Installed source version at the time of this exercise: 5c86ad6d735b4c0626c49aedfdb93aeb95e6199b, not whatever revision currently happens to be main. All pre-existing source at that revision is retained by this case-study branch's ancestry; a focused source archive also appears under artifacts/.

## B. Independent reviewer evidence

**Initial independent review — RETURN_TO_WORKER**

https://github.com/JayDEmily/LTM_RAG_V2/issues/1

The reviewer confirmed 278 CI-equivalent synthetic checks on the initial candidate, but an independent 12-expectation fault probe passed only 11. Changing source version_id without updating immutable local_id did not prevent index reservation or snapshot acceptance. The issue is a report of a source-identity defect; it is not a claim that a real outside actor had access to SQLite.

**Second independent review — RETURN_TO_WORKER**

https://github.com/JayDEmily/LTM_RAG_V2/issues/1#issuecomment-7061870012

The reviewer independently reproduced 282/282 CI-equivalent cases and confirmed that source-id tampering was correctly rejected in the repaired identity path. Its separate 17-case fault suite was 12 passed, 5 failed: three falsely verified stored records after corruption of text/role/outbox mapping; one mixed pre/post-revocation snapshot under a committed WAL interleaving; and one orphaned OBSERVED coverage record when the original's source identity was changed. It checked the parent and classified the failures as pre-existing/uncovered, not introduced by the new identity logic.

**Final fresh independent review — PASS**

https://github.com/JayDEmily/LTM_RAG_V2/issues/1#issuecomment-7061961835

Reviewer, not implementing worker, inspected the exact GitHub head 8d27bd55d4abf0c5f864b60a33f24d666920a130 and its parent, requirements and original failure report; then ran an independently written 35-test fault suite: **35/35 PASS** with **12 forced SQLite WAL revocation interleavings**. It independently reran the secret-free 285/285 CI-equivalent selection and separate 31/31 review-tool tests. A direct differential check against the immediately preceding commit reproduced all five earlier defects (0/5 passed on parent) and then passed the same five on the repaired head (5/5).

This PASS is bounded to the synthetic source-fidelity and revocation/coverage repair. It is not a ChatGPT native capture pass, production certification, hosted model/provider readback, or merge approval.

**Worker follow-up and integration record**

- https://github.com/JayDEmily/LTM_RAG_V2/issues/1#issuecomment-7061774878 — second worker source-identity repair checkpoint.
- https://github.com/JayDEmily/LTM_RAG_V2/issues/1#issuecomment-7061891891 — final worker integrity repair and regressions.
- https://github.com/JayDEmily/LTM_RAG_V2/pull/2#issuecomment-7061974863 — hosted CI integration record, explicitly not merge permission.

The full issue body and its observed comments were captured into evidence/issue-1-full.json to preserve individual verdict text, context and comment IDs.

## C. Hosted GitHub Actions (integration, distinct from review)

**PR:** https://github.com/JayDEmily/LTM_RAG_V2/pull/2
**Workflow run:** https://github.com/JayDEmily/LTM_RAG_V2/actions/runs/44899629182
**Job ID:** 136832604143, name synthetic-unit
**Reported conclusion from GitHub jobs and run:** SUCCESS

The **actual hosted job log**, not a worker's local shell, proves:

- Checkout of GitHub-generated synthetic PR merge ref pull/2/merge at **aa2fdf3ad5371dcb086ba4f14f3256bbaa64b017**.
- Git checkout message explicitly identifies merge of exact reviewed head 8d27bd55... into public main/base 0aa4b804....
- Ubuntu hosted runner and Python 3.14.
- Installation of pinned **mcp==2.3.0** from vnext/requirements-mcp.txt.
- Passing validation of governing links, proposed ADR and original G1–G10 reference material.
- Exactly **25 base unittest modules** plus **13 Stage W synthetic fake-provider test selections**.
- Actual log line **Ran 285 tests ... OK**, with job and every named step marked SUCCESS.
- Source diff-whitespace check passed.

The full retrieved GitHub job log is evidence/ci-job-136832604143-full.log; a short filter from the same response is evidence/ci-job-136832604143-selected.log; the structured job/step statuses are evidence/actions-run-44899629182-jobs.json.

The job ran a **synthetic merge ref**, not only a feature-branch detached HEAD. This is appropriate PR integration evidence but not a claim the PR was merged into main.

## D. Worker and reviewer test counts are different categories

| Test evidence | Context | Exact result | Limit |
| --- | --- | --- | --- |
| First worker | 65820f3 | 278/278 local synthetic | Missed identity/version divergence |
| Independent reviewer 1 | 65820f3 | 278 regression passes; fault probe 11/12 | RETURN_TO_WORKER |
| Second worker | d27acd1 | 282/282 local synthetic | Missed five related source-release inconsistencies |
| Independent reviewer 2 | d27acd1 | 282/282 regressions; new fault suite 12/17 | RETURN_TO_WORKER |
| Final worker | 8d27bd5 | 285/285 CI-equivalent, 38/38 targeted, 31/31 separate review tools | Not an independent verdict |
| Final reviewer | 8d27bd5 | 35/35 self-authored adversarial; 12 forced WAL; 285/285 reproducible; 31/31 review tools | PASS on bounded repair |
| Red/green control | d27acd1 vs 8d27bd5 | 0/5 on parent, 5/5 on repaired head | Strong causal regression evidence |
| Hosted Ubuntu Actions | PR merge aa2fdf3 | 285/285 tests, SUCCESS | Historical private evidence excluded |

Nine private-evidence-dependent historical tests — eight Stage T and one Stage W preregistration — were **NOT_RUN**. Their omission was explicit, not a passed test. No owner-source dialogue completeness, native unprompted lookup, provider readback or production ingestion was proved.

## E. Preserved original reviewer-authored Python sources

The following are exact copies recovered from isolated reviewer test directories, **not** newly invented worker tests. Their SHA256 digests were independently checked during the archival copy.

| Case-study path in tools/reviewer-authored/ | Original SHA256 |
| --- | --- |
| 8d27_final_35_test_review.py | 182c031080671e3ef13b5cb7460d91206fb209244b036272548d834b43db899d |
| d27_parent_red_control.py | 269815205dc8037141c673712d9173502aeeb004a0e628034209af753855dccb |
| 8d27_ci_selection.py | b237bf82259e4ead80fc0d5caf2e6baa35907f9b7bc542297ebe118a631f53c0 |
| d27_17_test_review.py | 6796d253e21ed4fe5930ef1a005cdb0744bd1662b5a07492a9b6ad9400087bd7 |

The original final reviewer file was rerun unmodified in its original temporary test environment during case-study creation: **Ran 35 tests ... OK**. The case verifier additionally supports executing the same source against the archived V2 head, changing only a disposable runtime ROOT pointer.

## F. Reviewer dispatch and controller-failure evidence

The first reviewed candidate was sent through the installed launcher but its strict UIA readback failed to register controller state. The actual saved reviewer chat existed and later delivered its verdict. Subsequent candidate assignments used manual one-shot UIA with durable local Send intent followed by exact posted-message verification.

The launch inputs were examined locally; the archived prompts/ records store exact reviewer-assignment **SHA256 digests, character counts, commit pins, saved-chat URLs and observed state**, not account message bodies. The last two positive prompt-delivery states were POSTED_EXACT_MATCH. The first launcher remained unregistered and is never marked passed.

The automation source and installed wrapper are preserved under the private version boundary, documented in AUTOMATION.md. Private runtime account-route configurations, browser cookies, owner conversation transcripts and credentials are excluded from this case study.

## G. What was not established

- Final merge permission, a merge commit into V2 main, or an owner-accepted technical ADR.
- Automated, reliable LTM-specific Chat Succession controller handoff, even though manual one-shot reviewer dispatch succeeded.
- Live ChatGPT history capture, cross-chat unprompted source acquisition, source completeness, genuine user role attestation or real-time server-send timestamps.
- A proof against arbitrary coordinated rewriting of all database fields and hashes by a malicious actor with database access.
- Hosted provider search/readback, production release, paid Responses inference or native ChatGPT source-capture testing for this repair.

**Source hierarchy:** Exact Git objects, independent reviewer comments, hosted job checkout and test log, and local test execution evidence support the conclusions. The surrounding prose is interpretation and does not override any cited record.
