# Stepwise same-PC capacity qualification

**Status: proposed / NOT_RUN. No practical maximum is known.** Earlier evidence establishes only bounded two-run overlap, not a capacity ceiling. Source: ASTRA_BRIEF, S07 and the [evidence review](../evidence/EVIDENCE_REVIEW.md).

## Objective and independent variables

Measure how many **simultaneous run instances** the existing PC can sustain without violating routing, Send, pause, publication or terminal invariants. Let:

- `N_open`: nonterminal runs retaining state/resources.
- `N_observing`: concurrently active controller processes actually observing/dispatching.
- `workers_i`: distinct saved desktop workers already registered for run i.
- `M_i`: immutable per-run cap — three for the two-slice finish fixture, two for the cap-with-review fixture.

A paused run can remain open with zero observing process. A recovery window is not another worker; four saved workers across two runs is not N=4. Record all four quantities rather than conflating them.

Use separate owner-created Project/repo pairs and native run directories/readers. At one stage all runs use the same pinned candidate, workload class and polling policy. Changing a version, profile arrangement or threshold starts a new measurement series.

## Stage order and bounded repetitions

1. Capture idle PC configuration and resource samples; do not globally shut down the owner's Chrome or change unrelated applications.
2. **N=2 first:** Cat/Dog finish plus Bird/Pig cap, including one pause/restart while its peer progresses. This is the functional isolation prerequisite, not a stress extrapolation.
3. Increase to **N=3, 4, 6, 8**, then **+2** per level while criteria pass. N=2 is not a permanent architecture limit.
4. Run **three fresh bounded cohorts per level**. Fixed per-run caps keep every run finite. Use a mixed finish/cap workload; at least one of each per cohort.
5. Require N simultaneous observing controllers for at least **two normal polling intervals (40 seconds at 20-second polling)** in each cohort, plus at least one confirmed successor per run. Record actual intervals. If short fixtures do not overlap long enough, stage an additional pre-authorized same-chat continuation before launching the cohort; do not manually pad a completed result.
6. Exercise tightly grouped launch requests in one cohort (requested start spread ≤1 second, actual starts recorded) and pause/restart one run while peers progress in another. Initial launch serialization is expected; measure wait rather than invent simultaneous Sends.
7. Do not commence the next level until all current cohorts have terminal/held dispositions, no unresolved unsafe action and reviewed evidence. Required positive cases cannot be replaced with assisted runs.
8. At the first failing level, stop admissions, preserve state, identify the measured limiter and reconfirm the last passing level with one additional fresh cohort. Select an operating level with measured headroom; do not call it a universal limit.

No automatic unbounded chain is introduced: every job retains its finite cap; the human/operator test budget bounds the number of cohorts. If that budget expires before a limiting level, report **“tested through N; practical ceiling not measured”**, retain the evidence and leave that part of A2-G5 open.

## Freeze thresholds before the first cohort

The supplied [threshold JSON](capacity_thresholds.proposed.json) is a proposed starting budget, **not measured performance or an already accepted SLO**. The owner can amend it before a series starts. Do not loosen it retrospectively to pass a slow level.

| Dimension | Proposed criterion |
| --- | --- |
| Safety | Zero duplicate/misrouted Sends, wrong-account input, cap breach, lost pause, unauthorized branch/work or overwritten draft in every cohort |
| Completion reliability | 100% of healthy fixture runs reach their expected terminal state without unplanned intervention or unresolved Send; deliberately injected negative safety cases are assessed separately |
| Handoff latency | `L = saved-successor confirmation − stable completed source response observed`, excluding only a logged deliberate owner-pause interval. Per-stage nearest-rank p95 ≤ `max(90 seconds, 2 × N=2 p95)` and individual max ≤180 seconds |
| Pause acknowledgement | Marker durable promptly; acknowledgement within 120 seconds of accepted pause request. Zero new dispatch after acknowledgement; any pre-ack in-flight action explicitly preserved/reconciled |
| Last stable fresh proof to source-ready after reload | ≤180 seconds for the positive stale case; continued streaming before positive proof is a different metric, not a completed-response delay |
| Resource headroom | Available physical RAM must not stay below `max(2 GiB, 10% of installed RAM)` for ≥30 seconds; system committed memory must not stay above 90% of commit limit for ≥30 seconds; whole-PC CPU p95 ≤85% during cohort overlap |
| Lock/command reliability | No unexpected Chrome-mutex timeout, UIA operation timeout or Git timeout; record wait distributions against current configured bounds (window mutex 30 s, UIA subprocess 90 s, Git command 45 s) |
| Window lifecycle | Steady owned worker windows ≤N_open; ≤one additional owned probe per run; no orphaned owned probe after a case and no changes to unrelated windows/drafts |
| Fair progress | Every unpaused healthy run completes its bounded work; no run starves behind shared window operations. Report maximum consecutive observation gap per run |

These thresholds are conservative proposed admission criteria, not a claim that low memory caused the archived failures. If N=2 cannot meet an agreed threshold, investigate that baseline first; a passing integrity test cannot excuse it.

## Instrumentation and formulas

Sample resources every **5 seconds**, from just before launch until all cohort runs stop and owned probes close. Record:

- Physical total/available RAM, committed/commit-limit, total CPU normalized to the PC, Chrome processes/working set, Python controller and WSL resource use if available.
- Number of owner-existing windows, run windows and probes; count aliases/ownership separately.
- Per-run observer start/stop/pause intervals, poll delay, UIA Observe/Prepare/Send/Recover durations, session mutex wait, Git fetch/readback times and timeout/hold counts.
- Model/worker time from confirmed input to observed completed reply; Git publication-to-observation lag; independently observed fresh-completion-to-original-view lag; stable response-to-saved-successor latency. Do not conflate these.
- Account/profile arrangement, foreground activity, network problems, power/sleep/session conditions and manual intervention.

For `n` latency observations sorted as `x`, nearest-rank `p95 = x[ceil(0.95*n)-1]`. Publish n, min, median, p95 and max; when n<20 the p95 is a coarse upper order statistic, often the maximum, not a reliability estimate. Three cohorts give at least `3N` healthy successor observations at a level. Publish raw values; do not assert statistical guarantees from that small sample.

A failed/held action has no confirmed-successor latency and **must not be silently omitted**. Count it in reliability/failure totals; label its latency censored/unresolved. Exclude intentional pauses only with their exact start/end in the raw record. Do not exclude rendering delays or unplanned operator corrections to improve the metric.

## Stop, isolate and report

- On ambiguous routing, duplicate Send, lost action or wrong-account input: stop new admissions and request pause for affected shared-session runs. Preserve all in-flight evidence and reconcile read-only; do not force-kill browsers or repeat messages.
- On latency/resource saturation without safety violation: stop increasing N, let safe in-flight bounded work finish or pause under owner direction, and preserve all results.
- A simple safe hold is preferable to a duplicate, but repeated/unexpected holds still mean the capacity level failed.
- Diagnose the first limiting dimension with the resource/timing trace. Targeted polling jitter or a shorter shared-operation scope is considered only if those measurements justify it; any implementation change restarts affected qualification.
- Report last passing N, first failing N, candidate/PC/profile configuration, exact failure, all interventions, confirmation cohort and chosen operating level. If no failure was observed, report a lower bound only.

The [capacity worksheet](capacity.csv) is intentionally empty of measurements. Filling it with invented estimates would not satisfy this brief.
