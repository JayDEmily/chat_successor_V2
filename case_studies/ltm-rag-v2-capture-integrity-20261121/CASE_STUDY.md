# Case study — repairing synthetic source fidelity through independent review

**Verbatim correction:** [VERBATIM_SUPPLEMENT.md](VERBATIM_SUPPLEMENT.md) now preserves the full original reviewer prompts, PowerShell command arguments, account routing, run files, reviewer Python scripts and the recoverable 245-record tool trace. Earlier redacted representations and exclusion statements below describe the first publication and are superseded. No authentication-token substitutions were required; 32 large outputs were already unavailable from the history source.

## 1. Executive abstract and the engineering decision

The engineering goal was deliberately narrow: harden the existing synthetic capture ledger so that source identities, exact text, authorship, index payloads, verification status, coverage and revocation snapshots could not silently diverge through plausible database corruption or an adversarially interleaved write.

At the start, the public V2 repository was a sanitised source snapshot with main at 0aa4b8042fc60991aa8a7d9d2278314b52efa24d. Its secret-free GitHub Actions baseline had passed 276 synthetic cases, but that was not evidence of exhaustive G2/G5/G9 fidelity. Passive genuine source capture was unproved. The surrounding architecture ADR remained proposed, with no accepted numbered implementation-leaf register. No real account ingestion, new provider, production service or live ChatGPT capture was part of this work.

The adopted execution pattern was bounded engineering followed by a **different ChatGPT reviewer**, with review evidence on GitHub, a revised candidate on RETURN_TO_WORKER, and a pull request only after a final PASS. This is a case in which the independent review substantially changed the engineering result: it found defects that the worker's own initially passing unit tests had not covered.

**Recorded final outcome:** the reviewed code was commit 8d27bd55d4abf0c5f864b60a33f24d666920a130. The third independent reviewer published PASS on that exact head, a separate hosted Ubuntu Actions run passed 285/285 reproducible cases on a generated PR merge ref, and PR #2 remained unmerged pending an owner decision. This is acceptance of the bounded synthetic repair by an independent reviewer and hosted CI, **not** acceptance of the broader memory architecture or approval to merge.

## 2. State, authority and evidence at entry

The active development repository was JayDEmily/LTM_RAG_V2 (public). Its baseline was a fresh root commit, 0aa4b804, containing 421 tracked Git paths; the original JayDEmily/LTM_RAG repository stayed a separate private archive. The worker used the Ubuntu working copy and Remote Desktop Commander to inspect the actual on-disk source. GitHub was the durable record. The installed browser-launch automation lived in another repository, JayDEmily/chat_successor (private), and was not a component of the V2 codebase.

Relevant policies: V2 root AGENTS.md, GUARDRAILS.md, vnext/AGENTS.md; the proposed complementary-memory ADR; G2 source identity/fidelity; G5 capture/coverage/index relationships; and G9 revocation suppression. Governance expressly distinguished worker tests, independent reviewer acceptance, hosted CI and final owner-authorised merge.

The source foundation was a synthetic-only SQLite ledger. Each ingested original had stable source/message/version identity, exact original text, role, a SHA256 content digest and an index-outbox payload digest. Indexing progressed through PENDING, IN_FLIGHT and SEARCHABLE, and source verification used a separately supplied synthetic comparison and reference. Coverage represented known OBSERVED positions, explicit GAP_UNKNOWN, and effective revocation visibility. Snapshot assembled originals, coverage, outbox, corrections and revocation totals for one source/conversation/branch.

The project had no authorised passive ChatGPT capture path. No change in this case study establishes one. The use of ordinary ChatGPT reviewer threads for engineering feedback is separate from an LTM-RAG source-capture feature or its exhausted historical native-trial quotas.

## 3. Incident chronology and review loop

| Stage | Source revision | Engineering and independent result |
| --- | --- | --- |
| Public baseline | 0aa4b804 | Existing synthetic ledger and 276-case hosted baseline; no independent boundary review of this prospective repair. |
| First worker repair | 65820f3 | Added guarded payload checks for reservation and acknowledgement; 278/278 CI-equivalent local synthetic cases. |
| Independent review 1 | Against 65820f3 | 278-case independent regression passed, but independent fault probe was 11/12: forged source version could still be indexed. RETURN_TO_WORKER, GitHub issue #1. |
| Second worker repair | d27acd1 | Added stable source/message/version identity checks in index, verification and snapshot paths; 282/282 local CI-equivalent cases. |
| Independent review 2 | Against d27acd1 | Existing fixes passed, but a 17-case independent fault suite found five failures: three false source-verification promotions, one mixed snapshot and one orphaned OBSERVED coverage state. RETURN_TO_WORKER, issue #1 comment 7061870012. |
| Third worker repair | 8d27bd5 | Strengthened SOURCE_VERIFIED certification, transactional snapshot consistency, coverage coherence. 285/285 local synthetic, 38/38 targeted, 31/31 review-tool cases, plus 30 forced WAL-interleaving repetitions. |
| Independent review 3 | Against exact 8d27bd5 | Independent 35/35 adversarial tests (12 WAL interleavings), red/green five failure controls 0/5 on parent and 5/5 on repaired head, 285/285 CI-equivalent, 31/31 review tools. PASS, issue #1 comment 7061961835. |
| Integration check | V2 PR #2 | GitHub Actions 44899629182 job 136832604143 passed on synthetic merge commit aa2fdf3, explicitly merging 8d27bd5 into baseline 0aa4b804. |
| Stopping condition | No merge | PR opened, mergeable and unmerged at the recorded checkpoint. Owner merge authorisation not inferred. |

Every implementation revision changed only three paths within V2: the ledger, its unit tests and vnext/PROGRESS.md. GitHub compared the whole candidate series against main as three commits ahead, none behind. The prior independent failure verdicts were preserved in issue #1 rather than overwritten by the final PASS.

## 4. First failure mechanism: index payload certified without checking the source

The first worker reproduced a structural inconsistency: a corrupted stored exact-text original could still be returned from reserve_index as an upload payload even though its recorded content_sha256 and outbox digest corresponded to different source data. A separate snapshot method rejected that corruption; the index transition was missing comparable validation.

The worker added a shared _checked_index_payload query joining index_outbox and originals, recomputing the current UTF-8 text digest and the upload payload digest constructed from local ID, author role and exact text. reserve_index no longer releases bytes from an inconsistent original, and acknowledge_index checks again before making a source SEARCHABLE. A failed reservation rolls back its provisional PENDING-to-IN_FLIGHT update; acknowledgement obtains a write transaction before testing tombstones and payload contents. Idempotent acknowledgements and concurrency remain separately exercised.

The initial tests covered direct mutation of exact_text, author_role, content_sha256 and index_outbox.payload_sha256. The first reviewer confirmed the behaviour but explicitly tested a different invariant: a directly modified version_id with unchanged local_id and source bytes. The new integrity function had not checked whether the record's identity columns still generated its stable local ID. The forged version was accepted for indexing. That was an inherited G2 defect, not evidence of a real-world adversary reaching the private SQLite database.

## 5. Second failure mechanism: identity columns disagreed with immutable local ID

The second worker introduced _check_source_identity, recomputing the stable local ID from stored source_id, message_id and version_id. It was invoked inside the shared index validation and in source verification and snapshot readback. New tests forged each of the three identity components before reservation and late acknowledgement and expected CaptureConflict without an unauthorised PENDING/IN_FLIGHT/SEARCHABLE change.

Test-first evidence was meaningful: eight new assertions failed on the preceding candidate, then targeted tests passed after the repair. The subsequent independent reviewer confirmed source-identity rejection and normal Unicode/index/concurrency cases.

However, the second reviewer did not stop at the announced defect. It examined every boundary that could release or certify an original and developed a second independent fault suite. That suite found five related failures outside the new identity-specific tests. All five were present on the earlier parent as well. This justified a third, mechanism-focused repair, rather than another patch for version_id alone.

## 6. Third failure mechanism A: false SOURCE_VERIFIED promotion

Before the final repair, verify_synthetic compared independently provided bytes to the **stored** content_sha256, then promoted source_status to SOURCE_VERIFIED. This was necessary but not sufficient. An attacker-or-test mutation of stored exact_text, author_role or index_outbox.payload_sha256, without changing content_sha256, left the comparison successful. The method could certify an internally corrupted source record. In contrast, snapshot would reject the same corruption.

A verified local reproduction individually changed exact_text or author_role after ingest and observed that verify_synthetic accepted the untouched original bytes and set SOURCE_VERIFIED. The independent review additionally reproduced an altered outbox mapping/digest.

The final repair invokes the shared canonical text/role/outbox validation **inside verification's write transaction** before promotion. A corrupt original or outbox raises CaptureConflict; verification_ref remains unset, source_status stays SOURCE_OBSERVED, and no false certification is released. The final reviewer checked text, role, original digest, outbox digest, missing outbox, verification provenance, genuine Unicode success and identity mutations.

This is a consistency check among independently persisted fields, not a signature-based guarantee against an actor that can rewrite the original and every corresponding digest and receipt.

## 7. Third failure mechanism B: mixed pre/post-revocation snapshot

Prior snapshot implementation issued separate SELECT statements for originals, coverage, outbox, tombstones and counts without establishing one consistent SQLite read snapshot. Under Write-Ahead Logging (WAL), the independent tester paused the read after the visible originals query, committed revoke on another SQLite connection, then resumed the remaining SELECTs.

The result could include the old original's text while later counts and tombstone-derived coverage referred to a newly committed revocation. The violation was temporal **inconsistency within one released view**, not a claim that WAL itself is faulty.

The final repair starts an explicit SQLite read transaction before the first source SELECT. In WAL mode the snapshot is fixed at that first consistent read; a concurrent writer can commit, but all subsequent queries within that snapshot see the same version. The resulting **pre-commit view** may complete after a concurrent revocation commits, while the next newly started snapshot sees the post-revocation state. This is snapshot consistency, not strict real-time suppression of an already-in-progress read after a revoke returns.

The worker's tightened deterministic test **requires** the writer to commit while the reader is paused, instead of merely sleeping or accepting a race that did not occur. Thirty local forced runs passed. The independent reviewer authored twelve more forced WAL runs and checked all of originals, outbox, coverage and revoked_count in both versions, with no deadlocks or timeouts.

## 8. Third failure mechanism C: orphaned OBSERVED coverage

Coverage is indexed by source, conversation, branch and position. After a synthetic database mutation changed the source_id in originals, a snapshot of the **old scope** selected no original rows. Identity checks inside the loop over visible originals never ran, yet coverage from the original scope still reported an OBSERVED source position.

The fix enforces coverage coherence against the existence of an original in the same source/conversation/branch/position, including tombstoned versions where appropriate. If an OBSERVED slot lacks any scoped original, snapshot fails closed instead of returning a contradictory record. It does **not** require a live visible original where a legitimate tombstone exists: when all versions at a position are revoked, coverage is reported REVOKED. One revoked version among several retains OBSERVED if another is visible. GAP_UNKNOWN remains distinct.

The final reviewer mutated source, conversation, branch and position identity, injected an orphan coverage row and confirmed that only contradictory OBSERVED slots failed. It also checked versioned positions, redacted predecessor links and correct revocation masking.

## 9. Why repeated independent review mattered

The old tests were accurate within their coverage but incomplete at the material release boundaries. At each step, a worker added tests for the immediately visible defect; the independent reviewer challenged adjacent invariants instead of echoing those fixtures.

Reviewers were instructed to inspect the exact GitHub head and parent, the repository requirements, and existing failure evidence, and to write fresh synthetic fault injections. Their reports gave exact SHAs, test counts, rollback observations, and source links. Two genuine RETURN_TO_WORKER verdicts remained recorded. The final reviewer controlled for false confidence by running the same five relevant fault checks on the old and repaired revisions. The five failed against the parent and passed at the new head.

That red/green differential is stronger than observing 285 green pre-existing tests alone. It proves the new repair changes the behaviour that the reviewer previously reproduced. It does not establish untested capabilities.

## 10. Why the reviewer automation is part of the incident

The successful test result did not imply the automated reviewer launcher was fully successful. Its exact installed source commit was 5c86ad6d735b4c0626c49aedfdb93aeb95e6199b. After authenticating the correct James Student Chrome profile and expanding the correct Project, the preflight passed. The first launcher invocation created a saved review conversation and posted the message, but its strict message-container readback failed to certify the posted turn. The private bootstrap intent survived; controller.json did not appear. The launcher safely held rather than resending.

For subsequent reviews the operator used new Chrome Project windows with **one intended Send each**. The scripts positively checked Project URL, empty Project-specific editor, lack of another active Send, exact typed text, and saved-chat URL; wrote local intents before clicking; invoked the UIA Send button only once; and confirmed exact posted text. This bypassed the failed controller path without treating the failure as success. The actual scripts were ephemeral tool commands, so the case preserves the installed executable automation source, the source-tree commit, launcher wrapper, message digests, saved-chat locators and a documented reconstruction of manual procedure—not a fabricated byte-identical saved UIA script.

See AUTOMATION.md for the control-plane failure and the distinction between launcher-assisted bootstrap and manual one-shot reviewer launches.

## 11. Hosted integration was a different gate

After the third independent PASS was published, PR #2 targeted the public V2 main at exactly 0aa4b804 and the reviewed head at exactly 8d27bd5. It contained three commits and three paths. GitHub Actions run 44899629182, job 136832604143, checked out ref pull/2/merge at aa2fdf3, whose log explicitly named the reviewed head and baseline.

The hosted Ubuntu runner set up Python 3.14, installed pinned mcp==2.3.0, validated governance links/proposed ADR/G1-G10, selected 25 baseline Python test modules and 13 Stage W fake-provider cases, and logged **Ran 285 tests ... OK**. Source-diff whitespace validation passed, and the workflow concluded SUCCESS. The full retrieved job log and metadata are under evidence/; the GitHub Actions URL is the authoritative online record.

These were genuine hosted results on a generated merge revision. They were not a hosted test of nine historical cases that require untracked private Stage T/W evidence, nor an inference that native source capture had been implemented.

## 12. Conclusions, limits, and reuse

This case establishes a bounded, reproducible pattern:

1. Identify a specific invariant and reproduction against source, not a generic risk.
2. Change the narrowest common release/certification mechanism.
3. Use tests that fail before and pass after the change.
4. Ask an independent tester to derive materially different faults.
5. Preserve genuine RETURN_TO_WORKER outcomes and the exact commit lineage.
6. Require actual hosted PR merge-ref CI after a new independent PASS.
7. Keep the final merge decision separate and explicit.

The most transferable insight is **test the places where evidence becomes authoritative**: index payload issuance, SEARCHABLE acknowledgement, SOURCE_VERIFIED promotion, scope coverage, and composite snapshots. Checking a digest somewhere else in the ledger is not equivalent to protecting every transition.

Cautions are scoped to what was actually observed. SQLite fault injection is not evidence of an external exploit; passing synthetic tests do not establish genuine owner history or native ChatGPT unprompted lookup. The architecture ADR remained proposed, the nine private-evidence tests remained NOT_RUN, and the original private LTM repository and public V2 main were unchanged.

**Recorded stopping point:** final review PASS, hosted Actions SUCCESS, V2 PR #2 open and unmerged. The case-study publication itself is archival and does not amend that status or grant merge authority.

### Subsequent archival recovery of the one-shot code

The local Remote Desktop Commander tool history still contained the later one-shot PowerShell command arguments. Copies with only the literal review messages redacted have been added to tools/ as *.ps1.txt. Their timestamp, message SHA256 and classification are documented in AUTOMATION.md. No archived redacted script was used to send a live message; the historical originals were transient tool-call arguments.
