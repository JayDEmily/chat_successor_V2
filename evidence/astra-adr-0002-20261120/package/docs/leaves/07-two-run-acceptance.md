# A2-L07 — Two overlapping bounded runs and recovery faults

**Prerequisite:** A2-G2; owner-created disposable Projects/repos and fresh authorized fixture branches. **Gate:** A2-G3. **Checks:** A2-D01–D03, live S04–S09 and V01–V06.

## Expected outcome

Two isolated runs overlap on the same PC. Cat/Dog finishes its two slices with cap **three**; Bird/Pig reaches cap **two** with a third review assignment still eligible. One run is paused/restarted while the other makes observable progress. Their caps never change.

## Procedure

Follow the [detailed procedures](../../acceptance/PROCEDURES.md), not the completed historical branches.

1. Stage new instructions from clean seeds in the bundled histories, update their exact branch pointers, and publish before launch. Do not reset/force-push old receipts. Freeze authority and expected edits/parents/trailers.
2. Start two separate runs/Projects and record overlapping active intervals. Align one pair of launch requests closely enough to exercise window acquisition, with separate immutable request records.
3. Pause Bird/Pig while it still has one worker and no pending Send. Verify durable marker and acknowledgement; restart the observer with marker still present and require zero Send. Meanwhile Cat/Dog must show a new poll plus useful advancement/publication/handoff, not merely a process ID.
4. Close or displace Bird's view in separate bounded repetitions. Explicitly release pause and recover the same saved chat/count/cap. Exercise the other missing-view form in another repetition rather than conflating closed and inactive-tab evidence.
5. Capture an actual stale-original/fresh-completed comparison and automatic reload. If no such condition occurs, V03 remains `NOT_RUN`; `waiting` or manual reload cannot close it.
6. On separate authorized disposable runs, exercise prepared/pre-click pause, uncertain continuation/successor/bootstrap and action/route mismatch. Fault injections must not touch the two ordinary paused workloads. One positive posted-turn adoption, never automatic retry.
7. Verify each first fetched receipt before its successor; each final artifact and stop reason; repeated polls/restarts cannot produce worker three in the capped run. Record independent publication, transport and interpretation outcomes.

## Exact final checks / evidence

- Cat/Dog: two distinct saved workers, one successor, two exact story lines, correct parent chain/trailers, `STOP_FINISHED`, no pending action; count 2 < cap 3.
- Bird/Pig: two distinct saved workers, one successor, two story lines, next trailer “Review the two published lines,” absent review output, `STOP_CAP`, no pending action; count/cap 2/2.
- Phone/request/inspection/probe views count zero. All IDs/account/Project/run/branch/action mappings are disjoint as intended.
- Pause/recovery preserves worker, cap and consumed history; peer work progresses; owned probes close and unrelated windows/drafts are unchanged.
- Click/posted-turn/receipt mapping establishes exactly one handoff for each confirmed action. Unresolved attempts remain held.
- Record raw UTC event traces, original/fresh view fingerprints, per-run journals/markers, Git SHAs/diffs, active intervals, Windows resources and every operator action.

## Hold / failure

An expected negative case passes only its no-effect safety assertion. Unexpected hold, corrective prompt, manual reload or assisted Send fails the unattended positive case; preserve it and repeat later on an explicitly fresh fixture after a targeted repair. Duplicate/misroute/cap breach stops progression to phone/scale gates and requires owner review.

Sources: earlier S06/S07 are a baseline, not completion of this leaf.
