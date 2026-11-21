# Earlier Astra chat succession execution plan

This page records the earlier bounded trial. For current work, use the [Shoko Yumi execution plan](adr-0002/PROJECT_MANAGEMENT.md) and the current leaf in [PROGRESS.md](../../PROGRESS.md). The [19 November implementation plan](generic-entry-plan-20261119.md) and [ADR 0001](../adr/0001-generic-entry-and-re-entry.md) document the earlier generic-entry increment.

The earlier bounded trial followed the [source plan](../../astra/2026-11-17/artifacts/cfile_6afc507495a08191817cbc9fc1e77b63-chat_succession_test_plan_20261117.md), [adapter contract](../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/docs/PROTOCOL_AND_ADAPTER.md) and [owner runbook](../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/docs/OWNER_RUNBOOK.md) imported at `44c0d5948318e305c42fb0ac4f463e77f90531bc`. The [three-chat exploration](../superpowers/plans/2026-11-17-chat-succession.md) documents that trial.

## Earlier bounded trial setup

1. Read [AGENTS.md](../../AGENTS.md), [PROGRESS.md](../../PROGRESS.md) and the leaf for the assigned work.
2. Carry forward G0 and start Leaf 01. Use the existing offline suite and live procedures. Leaf checks reference Astra's cases. A recorded reference pass already establishes that case's reference-model result. Record what was actually observed through the live adapter using Astra's live procedures.
3. Commit the work and record the result, evidence or first blocker and next action in [PROGRESS.md](../../PROGRESS.md). Follow the runbook's setup for the nominated same-repo live test branch and path.

## Operating contract

- Configure the existing Project, nominated repo and working branch, and a positive maximum of distinct saved chats once per run. Use a single controller/Send actor. The observed initial saved chat counts as one. Count a successor only once, after positive observation of its submitted message, correct Project and distinct saved ID.
- Read the full, completed, current assistant turn and deduplicate its stable identity within the saved chat. Accept one canonical final `CHAT_STATUS: …` or exact bare final keyword per Astra's parser. Ignore user/tool output and examples inside quotes or code. Wait for streaming. Hold ambiguous or conflicting responses. Keep semantic interpretation in shadow mode unless separately supported by real classifier evidence.
- `NEED_MORE_TIME` sends “Okay, continue working.” to the same saved chat, including at the cap. `TASK_COMPLETE` requires current published programme state attributable to this worker. Stop if the programme is complete or the unique-chat cap is reached. Otherwise use one new composer in the nominated Project and the ordinary repo/branch pointer. `ERROR` holds automatic posting and shows the blocker.
- Check the active destination and independently observed editable content and attachments. Preserve drafts. Persist the pending action and then `sending` before the click. Confirm a specific posted message and saved destination. An uncertain outcome or state loss holds. Reconcile read-only, with explicit rearm only after positive no-submission evidence. Resume preserves history, count and terminal stops.
- Use the owner's existing authenticated environment and documented write route. Repository state conveys progress, next task and programme completion. The short pointer carries repo/branch and asks the successor to read current instructions there. Test fixtures and source revision references serve verification. The continuing loop uses a configurable cap and one local state file with one writer.

## Evidence available at entry

| Evidence | Result and scope |
| --- | --- |
| [Astra execution report](../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/reports/executed/RESULTS.md) and [per-case JSON](../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/reports/executed/offline_results.json) | 119 passed, zero failures, errors or skips. P01–P36 parser, D01–D10 composer observations, S01–S16 synthetic replays, C01–C36 controller (C32 includes 300 seeded traces), F01–F09 workload, G01–G08 real local Git, I01–I04 archive checks. G01–G08 are Astra test IDs, distinct from the gates below. |
| [Independent Ubuntu rerun, 18 November](https://github.com/JayDEmily/chat_successor/blob/14478119c9b4cc9288bb66b846975bd71b43d06c/AGENTS.md#local-checks) | 119/119 offline. Carry forward the recorded passes for the unchanged kit. |
| Windows planning check | The same kit passed 119/119 offline on Python 3.13 using `python -X utf8 run_offline.py --out <temporary-report-dir>` from the kit root. UTF-8 mode avoids the default Windows-1252 decoding error in the imported parser table. |
| Owner-confirmed one-successor capability and [historical trial receipt](https://github.com/JayDEmily/chat_successor/blob/3b2c95b954eb90b1e6c9b82403dd1956c6f34b39/evidence/succession-20261117-001/CHAT2_LAUNCH_BLOCKED.md) | Reuse the proven navigation/Send method. The older trial's attempted Chat 2 launch stopped before typing or Send. Its 37 historical tests and saved Chat 1 evidence belong to that trial. Preserve the held run. |
| [Imported results sheet](../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/fixtures/live_test_results.csv) | L01–L15 start at `NOT_RUN`. Browser and authenticated GitHub outcomes for this controller, and real classifier evidence, remain open. |

## Leaves and gates

| Gate | Leaves | Pass criterion and next step |
| --- | --- | --- |
| **G0 — Reference baseline** | Read the evidence above | Prior reference passes identified at their source revisions and scope. Begin Leaf 01. |
| **G1 — Offline implementation** | [01 Controller](leaves/01-controller.md) → [02 Repository](leaves/02-repository.md) → [03 Desktop](leaves/03-desktop.md) → [04 Dispatch and recovery](leaves/04-dispatch.md) | The reference controller and Astra's adapter contract are wired for the run. Carry forward Stage A, using the existing cases for offline verification. |
| **G2 — Owner-environment setup** | [05 Setup](leaves/05-preflight.md) | Complete the runbook's one-time setup. The first live cycle is L01. |
| **G3 — Bounded live integration** | [06 Live routing and recovery](leaves/06-bounded-live.md) | Record outcomes for L01–L12 before L13, as Astra specifies. Record L15's correctness and stale-state outcome in the results sheet. Follow Astra's option to combine or reorder live cases when their observations are covered. Semantic shadow applies when evaluating a classifier. |
| **G4 — Five-chat repeatability** | [07 Repeat, assess and hand over](leaves/07-repeat-and-report.md) | L13 passes in three independent five-chat runs. Record useful work, correct Project and repo continuity, exactly four successors per run, no duplicates/misroutes and no manual transfers. |
| **G5 — Optional live cap of 30** | [07 Repeat, assess and hand over](leaves/07-repeat-and-report.md) | Run L14 only if selected for the longer exercise. Pass requires 30 observed saved IDs, at most 29 successors and the 31st slice still outstanding. Keep `NOT_RUN` when skipped and scope conclusions accordingly. |

Use Astra's [live evidence template](../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/fixtures/live_record.template.json), [results sheet](../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/fixtures/live_test_results.csv) and [runbook](../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/docs/OWNER_RUNBOOK.md) for observations, evidence and cleanup. Report response interpretation, live transport and useful published work separately.
