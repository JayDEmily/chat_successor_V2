# Chat Succession V2 — MCP-native execution plan

**Status:** Owner-selected architectural direction; feasibility not yet demonstrated. **Branch:** `work/mcp-native-succession-20261122` in public `JayDEmily/chat_successor_V2`. **Branch baseline:** `820aa20c6643c0ed30177459a685a4a6ee56de79` (public `codex/chat-succession-finish`). The old Chrome source-refresh PR remains isolated and unmerged. No live installation, tunnel, worker or message was changed by this governance checkpoint.

## Purpose and outcome

Carry a bounded GitHub-backed assignment through fresh, identifiable ChatGPT conversations in one verified Project, with a single durable controller, independently checked Git publications, safe same-chat continuation and owner approval, pause/restart and no duplicate successor dispatch. Replace browser-extension-dependent observation with explicit MCP worker registration and completion reporting. Investigate native desktop UI Automation for the narrow launch/control boundary, not as a second orchestrator. Preserve the useful existing controller and handoff contract until evidence supports a different design.

[AGENTS.md](AGENTS.md) controls execution and authority; [ADR 0003](docs/adr/0003-mcp-native-succession.md) defines the architectural decision. [PROGRESS.md](PROGRESS.md) is the current execution ledger. The prior [Shoko execution plan at the public baseline](https://github.com/JayDEmily/chat_successor_V2/blob/820aa20c6643c0ed30177459a685a4a6ee56de79/docs/astra-succession/adr-0002/PROJECT_MANAGEMENT.md) is preserved in Git, not an active work queue on this branch.

## Milestones and acceptance order

| Leaf | Work and acceptance | State |
| --- | --- | --- |
| M00 | Establish governance, scope, source pin and historical conflict resolution. Verify public branch and document links; no runtime changes. | Governance checkpoint |
| M01 | Read-only feasibility: inspect existing tunnel/MCP pattern, current official OpenAI docs and native desktop accessibility; identify available tools, account/Project binding and supported launch/readback interfaces. Document what is observed versus proposed, including no viable interface if found. No new service or Send in this leaf. | Discovery complete; native qualification pending |
| M02 | Define the minimum worker registration/completion contract and threat model. Decide whether stable host session correlation, per-launch one-use challenge, scoped authentication and independent remote Git readback meet identity and replay requirements. Distinguish a completion tool call from proof of quiescence. Freeze small positive/negative test set, data schema, authority and abort predicates before implementation. | Contract frozen; offline only |
| M03 | Implement isolated synthetic-only MCP/controller proof of concept after M02. Exercise registration, wrong identity/route, stale/duplicate/conflicting callbacks, missing or mismatched Git publication, restart, pause, cap, crash/uncertain dispatch. Use mocks/local transport first; no real credentials or existing LTM services. | PASS — independently accepted at `0640138`, offline synthetic scope |
| M04 | Qualify separately scoped connected-plugin/tunnel transport with fresh disposable records and a finite native-call quota. Verify actual ChatGPT registration and completion tool calls, same/different session correlation, reconnect/replay, failure handling, server-side audit and independent Git verification. Do not interpret metadata alone as account ownership, original user text, native message identity or finality. Resource creation/live calls require actual applicable authority. | Authority granted; M03 accepted; M04 preflight active |
| M05 | Qualify extension-free native launch/control in an isolated Project: exact account/Project, empty composer, one approved submission, positive new-worker registration and independent saved-conversation receipt; wrong target/draft/attachment and lost-acknowledgement holds. Start with no-Send checks, then a separately scoped bounded trial. Stop if identity or uncertainty cannot be resolved; do not fall back to a Chrome extension. | Pending |
| M06 | Integrate qualified transport and launch; run full applicable local regressions and hosted PR checks, then independent source-pinned review. Repeat bounded Cat/Dog finish and Bird/Pig cap plus same-chat continuation on the new candidate; demonstrate useful publication, exact action/worker counts and terminal state. Pause/restart and one continuation/one successor lost-acknowledgement case. | Pending |
| M07 | Qualify iPhone initiation and proposal-specific approval/replay, then two independent same-account runs in distinct Projects, with pause/restart, isolation and verified terminal outcomes. Freeze release scope, backend/plugin pins and rollback. Independent closeout before any merge/deployment decision. | Pending |

Each milestone is independently verifiable. Derive exact commands, candidate pins, fixture quotas and success/failure observations as its concrete design is established; do not invent tests for a component that does not exist. Use focused regression on changed paths, then the applicable complete suites and CI at M06. Do not equate offline tests with native acceptance. If the new direction cannot satisfy account/Project binding, positive delivery or safe continuation, report the blocker and return to an owner decision rather than weakening requirements.

## Progress

The old plan's L11 was assisted; L12 remained incomplete. Public PR #1's four hosted jobs passed on `915fa802a1522e9a48eb57558b11db6e9be69c6e` only (offline legacy candidate). That is not acceptance of MCP-native operation. No old gate is automatically inherited as passed for the new adapter. Preserve test/evidence for unchanged controller contracts and requalify affected boundaries. Do not resume or migrate the held legacy L12 action.

Current leaf, tested evidence and next executable step are recorded in [PROGRESS.md](PROGRESS.md).

## Surprises & discoveries

- Earlier MV3 extension attempts repeatedly encountered action-admission, worker lifecycle, script injection and restart/installation problems. The later read-only DOM extension removed orchestration responsibilities but still suffered stale observations. The owner elected to move away from the extension.
- LTM-RAG V2 demonstrates private outbound MCP transport and observed same-chat/different-chat session correlation, not authentication of exact user text, owner consent or autonomous successor creation. Its services remain untouched.
- A completion report can reduce transcript polling, but it does not prove that the host has stopped generating or that a successor prompt was posted. M02/M05 must resolve these separate predicates.

## Decision log

- 2026-11-22: Owner selected MCP registration/completion direction and a separate public development branch. Native desktop launch is an investigation, not a proven platform capability. No extension development or inherited live-run migration.
- 2026-11-22: Adopt root `PLANS.md` in place of `docs/astra-succession/adr-0002/PROJECT_MANAGEMENT.md`; authorise only the scoped work described by the active assignment and compatible standing rules. Historical original remains at the pinned baseline.

## Outcomes & retrospective

M01 read-only discovery completed; see [M01 feasibility](docs/mcp-native/M01-feasibility.md). Official private tunnel path and native accessibility controls are credible, but exact account/Project route, saved-chat receipt, authenticated worker binding and finality remain unqualified. [M02 contract and frozen synthetic tests](docs/mcp-native/M02-contract.md) complete; [M03 candidate and test evidence](docs/mcp-native/M03-results.md) published; worker-tested only, separate independent reviewer acknowledged at issue #2; see [dispatch evidence](docs/mcp-native/M03-review-dispatch.md). M04 scoped owner authority granted; see [preflight specification](docs/mcp-native/M04-preflight.md). [Independent M03 PASS](https://github.com/JayDEmily/chat_successor_V2/issues/2#issuecomment-7072268126) verified at `064013839ad71f97aa4bfddb770497340ab28f46`; 36/36 candidate, 119/119 reference and 62/62 independently derived cases. M04 preflight active. No live qualification is claimed.

This living roadmap adapts OpenAI's [ExecPlans Cookbook](https://developers.openai.com/cookbook/articles/codex_exec_plans) and [workflow guidance](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex). These are optional conventions, not platform-mandated gates.
