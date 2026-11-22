# Automatic Timer Trial V1 — progress and evidence

Checkpoint: 22 November 2026, Melbourne (AEDT, UTC+11). This is the reviewed governance checkpoint, not the live leaf queue. The exact live branch tip and README/history take precedence for current leaf state.

## Progress

- [x] G0 functional baseline: correct Project context confirmed after owner moved setup chat; Git tip ce67154678795e7e1af5d73383c1c2f8df7f4732 (leaf 1), README exactly baseline plus first run, zero active tasks at pre-governance check.
- [x] G1 native task: scheduled 16:37:51, started 16:39:19.046, completed 16:39:24.696. Task readback returned AT-V1-G1-OK and disabled. Browser readback showed result in originating setup chat; no fresh chat from native invocation.
- [x] G2 launcher control: exact Project breadcrumb discovered in saved setup chat; opened target landing page. 16:42:09 Send invoked once; 16:42:16 readback showed distinct in-Project conversation, exact prompt and AT-V1-G2-OK.
- [x] G3 functional integration: task recorded completed; scheduled 16:47:55, started 16:43:40.318, completed 16:44:08.902. Desktop script start 16:43:58.225. Original report BLOCKED because PID output retrieval returned No session found; subsequent independent read-only browser inspection at 16:54:41 confirmed a third distinct saved in-Project chat, exact G3 prompt and AT-V1-G3-OK. Functional result PASS; timing conformance NOT established (start 254.682 seconds early, trigger provenance unknown). Do not claim a genuine five-minute delay was proved.
- [ ] G4 full sequence: leaf 2 complete at 520daff6528843341daf37f43f8a217474ba9d7b, parent 0c24b04532763d9dc3df05b56debf84b81a50302. Fresh Project worker independently observed; README-only change and exact three-line prefix verified. Worker reported completion 17:13:53 AEDT. Its successor lookup returned HTTP 404; no successor created. Current active task count zero. Leaves 3–4 pending. Historical lookup dependency removed by owner-authorised governance correction; resume only under a permitted cadence. The current plugin explicitly limits task frequency to once per hour; the requested five-minute autonomous chain is not established as permitted. Stop rather than circumvent or silently change the cadence.

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

- 22 November 2026 / owner: lock execution against scope creep; remove historical timer lookup dependency, embed the demonstrated launcher with private inputs in PLANS.md, retain leaf 2 and use direct Automations create only under permitted cadence. No extra architecture, gates or task creation in this governance correction.

- 22 November 2026 / owner: the timer carries a short repository reference and private assignment, not executable code. Corrected erroneous duplicate prose inside the launcher template; no mechanism or gate change. Owner reported a suspicious-activity prompt on prior automation; respect all platform approval and safety controls. No timer created in this correction.

- 22 November 2026 / owner: clarified the fundamental timing contract: completion-relative, non-recurring one-shot timer five minutes after each non-final leaf; retire the preceding trial task before creating its sole successor. No fixed periodic interval and no timer after leaf 4. Do not conflate individual one-shot acceptance with permission for the complete sequence. No architecture, gate or timing change; platform limits still apply. No task created by this clarification.

- 22 November 2026 / recovery: leaf 3 standalone one-shot scheduled 18:12:18, started 18:13:34.777, completed 18:13:53.423. Git and desktop access passed; launcher reported Starting route mismatch, no Send. At 18:28:38 independent inspection found the old tab at chatgpt.com/scheduled. No active timers or leaf 3 commit. Owner authorised removal of starting-page and persistent window-handle dependencies. Direct Project navigation opened a new window at 18:30:29; both short and full named landing routes still displayed Loading project during readback, with no named composer. Direct cold navigation has not yet passed; do not assert it has. The already demonstrated single-Send procedure is retained. No timing or approval rule changes.

## Outcomes & Retrospective

Four functional gate objectives verified (G0–G3); two leaves published. The remaining autonomous chain and completion-relative timing remain unproven. Native task records, remote desktop readbacks and exact Git evidence are required for final acceptance. At G4 close record all leaf SHAs, distinct chat placement evidence (private references only), timestamp comparisons, outstanding anomalies and zero active trial timers. Current README is unchanged by governance. Historical records in private trial chats are the source of operational observations, not public identifiers.
