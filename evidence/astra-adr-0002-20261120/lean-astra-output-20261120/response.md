I’ll separate the essential reliability checks from the accumulated process overhead, then produce a smaller execution plan with tightly scoped leaves and runnable regressions where the supplied source allows. I’ll keep the published candidate, unreviewed edit and reported installed backend distinct.
The central issue is not account separation. The supplied record shows repeated repairs around one browser-reading boundary, while the newer reader deliberately produces no actionable result for virtualized views. That can be a safe stop, but it is not working succession.

I’m restructuring the plan around proving that boundary first, then testing the simple loop. Capacity testing and advanced recovery will remain explicit, separate claims—not prerequisites that obscure whether basic succession works.
The local checks reproduced two smaller problems: an explicitly unqualified reader remains in `WAIT`, and direct dispatch can prepare the browser before noticing an existing pause. I’ve included separate, seven-line-total candidate patches for those behaviors.

The targeted suite now passes 49 tests. I’ve also written native regressions for the mixed-transcript defect, but I cannot run PowerShell/UIA here. The handoff therefore keeps that blocker open and makes it the first task.
**Your concern is justified: the programme needs less process overhead, not another layer of infrastructure.** But some checks protect against demonstrated faults—especially falsely acknowledging a Send—and should stay.

I’ve produced a leaner execution amendment to ADR 0002, rather than proposing a replacement controller.

### Deliverables

- **[Read the revised programme, leaves and gates](sandbox:/mnt/data/chat_succession_lean_20261120/PROGRAM.md)**
- **[Download the handoff package](sandbox:/mnt/data/chat_succession_lean_20261120.tar.gz)** — programme, tests, small candidate patches and execution logs.
- **[Download the unified diff](sandbox:/mnt/data/chat_succession_lean_20261120.patch)** — applicable to a review checkout without replacing omitted archive members.
- **[Read the actual test results](sandbox:/mnt/data/chat_succession_lean_20261120/RESULTS.md)**

### My assessment

The immediate problem is concentrated at the **browser observation and acknowledgement boundary**. The supplied independent review reports an older message being accepted despite newer, unclassified content. Separately, the virtualized reader deliberately produces no actionable response. That is containment—not working succession.

Another important simplification: require a stable identity for the **current input/response**, not an absolute census of the entire conversation. UIA runtime IDs can be reused, and virtualized items may be absent from the accessibility tree; neither supplies durable message identity by itself. ([learn.microsoft.com](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getruntimeid))

### What the revised programme changes

**Three release gates:**

1. **The browser boundary is safe and usable**, including positive current-turn and posted-message evidence.
2. **One run does useful work**, finishes or stops at its cap, and survives pause and uncertain acknowledgements.
3. **The intended owner workflow works**, including overlapping runs, phone approval and separate account routes.

These are divided into **23 individually assignable small leaves**. Each identifies its input, permitted changes, completion check and next action.

The programme also:
- Keeps the existing controller, three statuses, account separation and repository handoff.
- Removes repeated historical archive audits and large reports from ordinary leaf work.
- Uses focused tests per change and independent review at meaningful gates.
- Separates capacity and automatic stale recovery from the initial limited release. **Untested automatic reload must actually be disabled before that narrower release—not merely described as unsupported.**
- Preserves the original paused workloads and all unresolved submissions.

### Work completed here

**49 targeted offline tests passed:** 36 existing controller tests and 13 focused integration regressions, including a real file-only Git test.

Two new regressions initially failed. Separate candidate patches—**seven added runtime lines total**—address:
- Explicitly unqualified observation remaining in `WAIT` instead of reporting a durable hold.
- Direct dispatch preparing the browser before noticing an already-present pause.

I also supplied **27 native transcript assertions**, but PowerShell/UIA was unavailable here, so those remain **NOT_RUN**. The full historical 114/119 suites were not rerun.

**This does not clear the native reader blocker or constitute a release.** The next assignment is deliberately narrow: run the native regression against the published reader and preserved interrupted edit, then repair that specific boundary. No new scheduler, framework or broad hardening exercise.