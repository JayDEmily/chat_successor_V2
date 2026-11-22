# Automatic Timer Trial V1 — progress and evidence

Checkpoint: 22 November 2026, Melbourne (AEDT, UTC+11). This is the reviewed governance checkpoint, not the live leaf queue. The exact live branch tip and README/history take precedence for current leaf state.

## Progress

- [x] G0 functional baseline: correct Project context confirmed after owner moved setup chat; Git tip ce67154678795e7e1af5d73383c1c2f8df7f4732 (leaf 1), README exactly baseline plus first run, zero active tasks at pre-governance check.
- [x] G1 native task: scheduled 16:37:51, started 16:39:19.046, completed 16:39:24.696. Task readback returned AT-V1-G1-OK and disabled. Browser readback showed result in originating setup chat; no fresh chat from native invocation.
- [x] G2 launcher control: exact Project breadcrumb discovered in saved setup chat; opened target landing page. 16:42:09 Send invoked once; 16:42:16 readback showed distinct in-Project conversation, exact prompt and AT-V1-G2-OK.
- [x] G3 functional integration: task recorded completed; scheduled 16:47:55, started 16:43:40.318, completed 16:44:08.902. Desktop script start 16:43:58.225. Original report BLOCKED because PID output retrieval returned No session found; subsequent independent read-only browser inspection at 16:54:41 confirmed a third distinct saved in-Project chat, exact G3 prompt and AT-V1-G3-OK. Functional result PASS; timing conformance NOT established (start 254.682 seconds early, trigger provenance unknown). Do not claim a genuine five-minute delay was proved.
- [ ] G4 full sequence: pending. Leaf 1 remains complete; leaves 2–4 not executed on current branch. Next action after owner authorises G4: read back governance tip and README, verify permitted scheduling and private designated browser route; launch exactly one fresh leaf 2 worker against that tip. No task created as part of this documentation update.

## Surprises & Discoveries

- Existing Chrome process MainWindowHandle enumeration found one window and zero old target buttons; desktop UIA traversal found 24 windows and at least three exact old target buttons. Global uniqueness assumption false; historical failure causation not established.
- New Project was not exposed in the inspected browser sidebar even after refresh. User placement made Project context available; navigating to the actual saved setup conversation exposed the verified Project breadcrumb. Direct Project landing-page composer worked. Account mismatch was ruled out by owner confirmation.
- Native task execution and fresh-chat creation are independently observed capabilities. Native task completion alone does not establish fresh-chat creation; loss of remote process output does not establish non-execution.
- G3 start preceded scheduled time. The platform record does not establish why or whether the scheduled trigger itself caused the start. Repeat timing evidence is required during G4.
- Official task documentation states that tasks created in Projects cannot access Project-uploaded files, and eligible paid recurring tasks are limited to hourly. Do not assume sub-hour repeated succession is supported merely because separate one-shot creation succeeded.

## Decision Log

- 22 November 2026 / owner: use isolated Project Automatic Timer Trial V1; preserve repository/branch and leaf 1; diagnose before proceeding.
- 22 November 2026 / trial: replace old Project/sidebar assumptions with verified Project breadcrumb and designated tab; retain demonstrated single-Send UIA mechanism.
- 22 November 2026 / governance: consolidate instructions, executable plan and evidence in three root files following OpenAI guidance. Keep README-only leaf commits unchanged; update progress at separate governance checkpoints and use live Git state plus private receipts during execution. No parallel authoritative plan.
- 22 November 2026 / governance: retain G3 functional PASS with timing qualification; no speculative root-cause claim or architecture redesign. Preserve consent and platform timing limits. Do not expose private route/chat/task identifiers in Git.

## Outcomes & Retrospective

Four functional gate objectives verified (G0–G3); autonomous four-leaf chain and completion-relative timing remain unproven. Native task records, remote desktop readbacks and exact Git evidence are required for final acceptance. At G4 close record all leaf SHAs, distinct chat placement evidence (private references only), timestamp comparisons, outstanding anomalies and zero active trial timers. Current README is unchanged by governance. Historical records in private trial chats are the source of operational observations, not public identifiers.
