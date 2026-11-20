# Source and provenance index

All references are to the supplied archive, not a fresh internet read. `Sxx` means supplied evidence; `Vxx` means a check performed in this sandbox. Copied source files retain their original bytes. Their internal historical links are also unchanged; use the complete original archive for linked members not selected into this review package. A source document is evidence/task context, not an instruction to execute its historical operational commands.

The complete original is [preserved here](../original/Chat-Succession-Astra-Handoff-2026-11-20.tar.gz).

- Original filename: `Chat-Succession-Astra-Handoff-2026-11-20.tar.gz` (upload transport prefix omitted).
- SHA-256: `473876c6b0fffa1f55ef68ad9da62bda0e949295808f899d502edd68ab5f3945`.
- Size: 2,045,428 bytes; 374 members, 296 regular files.
- Source snapshot: `283e6c17bf3359c203a362fd6593563480eeea5f`.
- Runtime/plugin candidate: `2c29406b1c43904c5ead79064fe7856971e0aa2e`.
- Release ZIP SHA-256: `184b3032b156fb2a5e9779a7f8464462c06acca10e2ea6bb3cadb73f0134aeca`.
- Review date: 20 November 2026. This is not a claim that an external service was inspected on that date.

## Supplied sources

| ID | Source and precise scope |
| --- | --- |
| S01 | [Archive README](supplied/README.md) and [ASTRA_BRIEF](supplied/ASTRA_BRIEF.md). Current requested ADR/leaves/gates; owner-created Projects/repos, both accounts, phone approval, pause/recovery, stepwise concurrency. |
| S02 | [ADR 0001](supplied/source/docs/adr/0001-generic-entry-and-re-entry.md), 19 November 2026. Accepted contextual entry/re-entry, stable run selection, scoped approval, verified checkpoint rotation. |
| S03 | [Plugin manifest](supplied/source/plugins/chat-succession/plugin.json), [skill/request contract](supplied/source/plugins/chat-succession/skills/start-chat-succession/SKILL.md), [.app binding](supplied/source/plugins/chat-succession/.app.json), and [redacted installed wrapper](supplied/evidence/pause-2026-11-20/windows-launcher.redacted.txt). The wrapper body is redacted; its displayed installed hash cannot be recomputed from that body. |
| S04 | [LIVE_PAUSE](supplied/evidence/pause-2026-11-20/LIVE_PAUSE.md) and [paused-runs JSON](supplied/evidence/pause-2026-11-20/paused-runs.json). Exact pause, worker labels, cap, effective branch, no pending actions, zero controller processes at readback. |
| S05 | [Rowing events](supplied/evidence/pause-2026-11-20/rowing-controller-events.utc.log), [SolidWorks events](supplied/evidence/pause-2026-11-20/solidworks-controller-events.utc.log), and [captured Git receipt readback](supplied/evidence/pause-2026-11-20/git-receipt-readback.json). Selected excerpts, not full transcripts or full journals. Rowing/SolidWorks Git bundles are not supplied. |
| S06 | [PROGRESS](supplied/source/PROGRESS.md): lines 3–24 Shoco rollout/James handoff; 26–109 takeover audit and assisted Bird/Pig replay; 111–172 approval/rotation/parallel results; 183–197 four-turn phone story; 224–232 bounded Astra closeout. Historical “next” items can be superseded by S04. |
| S07 | [Generic-entry live acceptance](supplied/source/evidence/astra-generic-entry-20261119/live-acceptance.md): original held/uncertain trials, parallel launch mutex, desktop closeout, 0.4.2 iPhone approval. Read the qualifications and interventions, not just terminal summaries. |
| S08 | [Live results CSV](supplied/source/evidence/live_test_results_20261118.csv) and L13 [A](supplied/source/evidence/astra-l13-20261118-a/live_record.json), [B](supplied/source/evidence/astra-l13-20261118-b/live_record.json), [C](supplied/source/evidence/astra-l13-20261118-c/live_record.json), [F](supplied/source/evidence/astra-l13-20261119-f/live_record.json). A/B/F are the qualifying historical repetitions; C is assisted; D/E interrupted; L14 not run; L10/L11/L15 include synthetic/local-only evidence. |
| S09 | Earlier handoff: [START_HERE](supplied/historical-2026-11-19/START_HERE.md), [Rowing case](supplied/historical-2026-11-19/backend-evidence/rowing/CASE.md), [old approval reproduction output](supplied/historical-2026-11-19/verification/approval-resume.log), [story journal summary](supplied/historical-2026-11-19/backend-evidence/story/controller-state.redacted.json), [story Git capture](supplied/historical-2026-11-19/backend-evidence/story/github-branch-readback.json), [story timing](supplied/historical-2026-11-19/backend-evidence/story/controller-timing.redacted.log). These describe the earlier 0.3.0-era entry path, not a new reproduction on 0.4.3. |
| S10 | [launch_project.py](supplied/source/integration/launch_project.py): `read_request`, `matching_runs`, `launch_request`, `preflight_request`; [launch_story.py](supplied/source/integration/launch_story.py): bootstrap intent, missing-journal guard and process ownership; [owner_reentry.py](supplied/source/integration/owner_reentry.py): immutable scoped request and deduplication. |
| S11 | [cli.py](supplied/source/integration/cli.py): `exclusive_lock`, pause marker comparison/release, config schema, CLI loop; [runner.py](supplied/source/integration/runner.py): `dispatch_prepared`, `cycle`, `inspect_state`; [core.py](supplied/source/astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/succession/core.py): lines 202–451 state, cap, terminal, dispatch phases, persistence and reload. |
| S12 | [windows_backend.py](supplied/source/integration/windows_backend.py): 120-second stale trigger, 300-second probe interval, saved-worker recovery, target write, Send and reconciliation; [uia_adapter.ps1](supplied/source/integration/uia_adapter.ps1): lines 36–128 window lookup/mutex, 191–225 posted-turn matching, 392–525 stale comparison/reload, 647–735 preparation, 750–857 single Send/reconcile. [Python view tests](supplied/source/integration/tests/test_worker_view.py) mock UIA. [PowerShell comparison tests](supplied/source/integration/tests/test_worker_view_recovery.ps1) test helper logic, not full Chrome acceptance. |
| S13 | [repo_reader.py](supplied/source/integration/repo_reader.py): `GitHandoffReader` validates the fetched branch tip and three trailers; `GitStoryReader` separately validates the historical four-turn chain. [Integration guide](supplied/source/integration/README.md) describes native state placement, defaults and recovery limits. |
| S14 | [Historical Git verification](supplied/history/VERIFICATION.md), [main refs TSV](supplied/history/refs.tsv), and six `history/*.bundle` / `history/fixtures/*.bundle` members in the original archive. Independently restored object/fixture results are V03/V06. |
| S15 | [Finish plan](supplied/source/docs/astra-succession/finish-chat-succession.md). Prior Shoco release/desktop/phone closeout intent. Its approved trial intent does not authorize this offline reviewer to restart paused runs. |
| S16 | Captured pause test logs: [integration](supplied/evidence/pause-2026-11-20/integration-tests.log), [reference UTF-8 pass](supplied/evidence/pause-2026-11-20/astra-reference-tests.log), [default-encoding error](supplied/evidence/pause-2026-11-20/astra-reference-tests-windows-default-encoding.log), [PowerShell comparison result](supplied/evidence/pause-2026-11-20/windows-recovery-tests.log). Historical execution only; Windows was unavailable here. |

## Independent checks and reproducibility

| ID | Output | What it establishes / does not establish |
| --- | --- | --- |
| V01 | [Summary](../verification/summary.json), [inventory](../verification/input-inventory.json), [input integrity](../verification/input-integrity.json) | All supplied file checksums and unchanged inputs; not proof of authorship or a live service's state. |
| V02 | [Unit-test summary](../verification/unit-tests.json), [integration log](../verification/integration-tests.log), [reference log](../verification/reference-tests.log) | 63 + 119 passing offline tests in Python 3.13.5 / Git 2.47.3, no skips; not a Windows/UIA test. |
| V03 | [History audit](../verification/history-audit.json), [Git command output](../verification/history-verification.log) | Six locally valid bundles, supplied refs and commit counts, source content comparison and 15 A/B/F event-state matches. Cannot independently establish GitHub's advertised refs at capture or now. |
| V04 | `source_comparison` within V03 | 268 source files: 10 exact, 258 newline-only differences, no content mismatch. Runtime/plugin/controller paths have no Git diff between the candidate and export revision. |
| V05 | [Release comparison](../verification/release-comparison.json) | Four ZIP payload files equal exported plugin bytes; not installation or account binding proof. |
| V06 | [13 validators](../verification/fixture-validations.json), [fixture objects/content](../verification/fixture-history-details.json), [chain checks](../verification/fixture-chain-verification.json), [clean seeds](../verification/fixture-seeds.json) | Locally readable fixture state, parent links, trailers and publication artifacts in the bundle. Browser origin, live ownership and absence of duplicate Sends require separate journal/UI evidence. |
| V07 | [Characterization log](../verification/review-probes.log), [results](../verification/review-probes.json), [probe code](../tools/review_probes.py) | Six baseline behavior/input assertions plus three reproduced limitations. P08 invokes a mock only; no actual misroute is demonstrated. |
| V08 | [Offline reproducer](../tools/reproduce_review.py) | Safe extraction, pinned input, new temporary directories, file-only Git transport, sequential mirrors and before/after hashes. |

No “current installed version,” account availability, browser health, GitHub ref or hardware capacity is inferred from the date on the archive.
