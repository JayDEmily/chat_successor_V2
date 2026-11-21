# Frozen engineering case study — LTM-RAG V2 capture integrity

**Event:** 21 November 2026, Melbourne (AEDT)
**Nature:** An archival engineering case study, not a new feature, review verdict or merge request.
**Source repository:** [JayDEmily/LTM_RAG_V2](https://github.com/JayDEmily/LTM_RAG_V2), **public**.
**Private case-study host:** [JayDEmily/chat_successor](https://github.com/JayDEmily/chat_successor), branch case-study/ltm-rag-v2-integrity-20261121.
**Reason for private hosting:** The actual Chat Succession automation source is private. Republishing it on a public V2 branch would cross an avoidable confidentiality boundary.

## Outcome at the end of the observed exercise

A bounded synthetic-only G2/G5/G9 integrity repair moved through three worker commits, two independent RETURN_TO_WORKER reviews, a third independent PASS, and a real successful GitHub Actions PR job. The last approved source revision was **8d27bd55d4abf0c5f864b60a33f24d666920a130**. V2 PR #2 was **open, mergeable and unmerged** at the recorded checkpoint; there was no owner-authorised merge.

The final independent reviewer authored 35 separate fault tests: **35 passed**, including **12 deterministic SQLite WAL revocation interleavings**. A five-case red/green comparison was **0/5 on the immediately preceding commit** and **5/5 on the reviewed head**. Independently and in hosted CI, the reproducible synthetic suite passed **285/285**. A separate Astra review-tool suite passed **31/31**. These results do not attest genuine ChatGPT source capture, personal source completeness, hosted provider readback, or production behaviour.

The case is notable for a **partly failed reviewer-launch automation that recovered safely without a duplicate Send**. The first reviewer was reached via the installed Chat Succession launcher but its strict structural UIA acknowledgement failed and no controller was registered. The following two fresh reviewers were instead launched by deliberate one-shot Windows Chrome UI automation, with durable Send intents and exact message readback. This was a hybrid human-directed/tool-operated workflow, **not a successful unattended Chat Succession controller handoff**.

## Navigation

- [CASE_STUDY.md](CASE_STUDY.md) — technical problem, failure mechanisms, remediation, full chronology, engineering lessons.
- [AUTOMATION.md](AUTOMATION.md) — precise installed reviewer-automation version, launcher path, manual recovery and the unresolved readback defect.
- [EVIDENCE.md](EVIDENCE.md) — source revisions, independent review comments, pull request, hosted CI log and interpretation of test counts.
- [REPRODUCIBILITY.md](REPRODUCIBILITY.md) — frozen source archives, command-line reproduction, hashes, limitations.
- [tools/verify_case_study.py](tools/verify_case_study.py) — read-only SHA and provenance validation; optionally replays the final independent 35-test suite in a temporary directory.
- [tools/reviewer-authored/](tools/reviewer-authored/) — **unmodified recovered reviewer-authored Python files** from the actual isolated Ubuntu test directories, with exact hashes in SHA256SUMS.
- [prompts/INDEX.json](prompts/INDEX.json) — SHA256/length, revision and saved-chat identity for each reviewer assignment. No account transcript text, account routing table, credentials or browser session material is committed.
- [artifacts/](artifacts/) — complete code snapshots of public V2 baseline and reviewed head, complete relevant private automation source/dependencies at the installed commit, intermediate Python source/test snapshots, and the three implementation diffs.
- [evidence/](evidence/) — preserved GitHub issue #1, PR #2, Actions job metadata, full hosted job log and compare metadata as recorded for this case.
- [SHA256SUMS](SHA256SUMS) — fixed byte digests of all case-study content (excluding the manifest itself). The final Git commit freezes both manifest and bytes.

## Exact durable references

| Role | Revision or record |
| --- | --- |
| V2 public baseline/main | 0aa4b8042fc60991aa8a7d9d2278314b52efa24d |
| First worker integrity candidate | 65820f3c36d59d5636cc03e260e1666e6ca5836e |
| Second candidate, after source-identity repair | d27acd1ab6d06031ffc773c855907cfd8362027a |
| Final independently reviewed candidate | 8d27bd55d4abf0c5f864b60a33f24d666920a130 |
| Installed private reviewer automation tree | 5c86ad6d735b4c0626c49aedfdb93aeb95e6199b |
| Hosted synthetic PR merge revision | aa2fdf3ad5371dcb086ba4f14f3256bbaa64b017 |
| Final independent PASS | [Issue #1 comment 7061961835](https://github.com/JayDEmily/LTM_RAG_V2/issues/1#issuecomment-7061961835) |
| Integration pull request | [V2 PR #2](https://github.com/JayDEmily/LTM_RAG_V2/pull/2) |
| Hosted CI | [run 44899629182](https://github.com/JayDEmily/LTM_RAG_V2/actions/runs/44899629182), job 136832604143 |

## Freeze and authority

This branch is based deliberately on the **installed automation commit** (not the private repository's subsequently advanced main branch). Its existing Git ancestry already contains the automation source at the version actually used. The archived source distribution and launcher checksum provide an inspectable secondary record. The V2 code and review artefacts are added **only to this separate private archival branch**; the V2 candidate branch, V2 main, V2 PR and existing private automation installation are not changed by the case-study publication.

A review PASS and a green CI job were prerequisites to considering integration, not authority to merge. The nine historical private-evidence-dependent Stage T/W checks are explicitly NOT_RUN. The passive/unprompted native ChatGPT source-capture route remains CAPTURE_ROUTE_NOT_ESTABLISHED and the complementary-memory ADR was still PROPOSED FOR OWNER REVIEW.

## Verification

On a local copy of the archived branch, from this directory:

    python3 tools/verify_case_study.py
    python3 tools/verify_case_study.py --replay-independent

The first checks every recorded SHA256 and the GitHub/CI evidence structure without network access. The second additionally runs the preserved independent 35-test final-head script against the archived V2 source in a temporary directory. No live Send, provider, inference, external network or personal-history operation is performed.

**Classification:** frozen reproduction and analysis of a specific historical engineering exercise; not a standing process change or an accepted architecture decision.

**Further provenance:** tools/uia_*.ps1.txt contains recovered original one-shot UIA PowerShell command arguments, with reviewer-message content redacted for account privacy. These are non-executable archival text records, not a new launcher or evidence of a successful registered controller.
