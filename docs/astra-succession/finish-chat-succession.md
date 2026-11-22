# Earlier finish plan for Chat Succession

This page records the earlier 0.4.3 rollout plan. The historical sequence is recorded in the [Shoko Yumi execution plan](https://github.com/JayDEmily/chat_successor_V2/blob/820aa20c6643c0ed30177459a685a4a6ee56de79/docs/astra-succession/adr-0002/PROJECT_MANAGEMENT.md); for active MCP-native work see the root [PLANS.md](../../PLANS.md).

## Release goal

Publish the 0.4.3 candidate as a private plugin for the Shoco account so the owner can start or resume GitHub-backed work from a Project chat. The controller should recover the same saved worker when its Chrome view becomes stale or inaccessible, preserve the worker cap across restarts, and hand off only after verifying the worker’s published receipt.

Use revision `8345978` as the audit baseline. Reconcile Astra’s requirements against the controller and the evidence in `PROGRESS.md`. Carry forward the verified approval, branch rotation, and parallel-run results. Close the gaps in automatic Chrome recovery, isolated ordinary-project acceptance, and verification of the updated plugin. [Astra ADR](../adr/0001-generic-entry-and-re-entry.md) · [Takeover audit](../../PROGRESS.md#takeover-audit--20-november-2026)

## Controller and launcher

- Have the Windows wrapper pass its verified installation directory to the controller. Resolve that wrapper when Desktop Commander redirects `LocalAppData`, and write requests beside it. Use the verified existing James Chrome profile. Before the first Send, verify the Project, empty composer, and Ubuntu access to the nominated GitHub branch.
- If the saved worker’s view is missing, open a dedicated view of its verified Project and saved chat ID. If progress is unchanged for two minutes, compare with a fresh view of that exact chat. Keep one temporary window at a time and probe at most every five minutes per worker. Reload the original only after positive evidence of a newer completed response and verification of an empty composer. Chrome can briefly bring a new window forward. Normal observation and Send can work in the background.
- Keep recovery with the existing controller and preserve the run ID, worker, response history, and cap. A recovery view does not count as a worker. Preserve drafts and attachments. Hold on ambiguity, unavailable desktop, or an unverified composer and give the saved-chat link when known. A possibly submitted Send stays in read-only reconciliation until the exact posted message is verified.

## Acceptance and rollout

1. Run focused regressions for stale and missing views, duplicate views, drafts, anchor-specific receipt matching, pause and restart, uncertain Send, terminal cap, and branch rotation. Run the Windows PowerShell parser and preflight without sending. Use Windows Ubuntu for all GitHub writes.
2. Save the staged package in Shoco and read back the release, skill, and Desktop Commander binding. Route the verified Shoco Desktop Commander environment to the pinned Windows/Ubuntu candidate and its signed-in Shoko Chrome profile. Preserve the original launcher for rollback. Pass the native launcher directory so workers can use the same private run path as the controller. Verify the configured route without a Send.
3. Run two overlapping desktop trials through the Shoco launcher. Use disposable ChatGPT Projects verified in the Shoco profile. Carry forward the no-Send preflights for the actual Rowing and SolidWorks Projects and recheck the pinned repository branches from Shoco. Publish scoped trial receipts on disposable branches under the real repository rules.
   - **Rowing.** Read its current authority and verify one published checkpoint. Publish a short receipt on a separate review branch, then verify the successor follows the branch under the same run and cap. Keep this independent of the active Rowing gate.
   - **SolidWorks.** Run one documented read-only lookup against the 2021 Help index. Publish a short evidence note without source extracts or native CAD changes. Verify the successor checks it and records an eligible third review step. Confirm the controller stops at `STOP_CAP` after worker two.
   - Pause and restart one run. Displace its verified worker view and prove automatic recovery while its peer keeps running. Verify exact worker IDs, receipts, no duplicate Sends, and a cap of two for each run.
4. Run one fresh iPhone approval against the candidate. Use a clean disposable ref in the existing approval repository with a cap of two. Give the owner the verified Project link and instructions. On the iPhone in Shoco, select **Chat Succession**, start the fixture, and reply `I approve` in the request chat after the scoped hold appears. Verify one approval delivery to the original worker, one automatic successor, both published edits, and a terminal stop. Replay the recorded request to check for duplicate Send.

## Closeout

Mark the release ready after both desktop trials and the iPhone approval pass on the installed candidate. Record the version, backend commit, run IDs, GitHub receipts, stop reasons, and manual interventions in the existing progress notes. Preserve any pending Send for reconciliation before retrying or restoring the previous compatible release. Give the owner the verified private plugin link and the normal start and approval prompts.
