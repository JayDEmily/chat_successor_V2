# ADR 0002 acceptance gates

These gates are **new**, not the earlier Astra G0–G5 or ADR 0001 G0–G2. See [case register](cases.csv), [procedures](PROCEDURES.md), [capacity protocol](CAPACITY.md) and [evidence template](run_record.template.json).

## Current disposition

Only the offline baseline audit has been performed here. A2-G0 still needs the owner's ADR decision; A2-G1's **proposed changes** are not implemented; A2-G2–G6 have not been executed. The 182 passing old tests do not close a proposed implementation gate. All required new live acceptance remains `NOT_RUN`.

## A2-G0 — Evidence and authority

- **Prerequisite:** supplied archive; current brief and ADR 0001 read; paused records preserved.
- **Expected outcome:** owner adopts/amends ADR 0002 and authorizes only the nominated bounded leaves/trials.
- **Exact checks:** A2-E01 manifest/source/release; E02 six bundles and fixture validity; E03 exact paused pair, unknowns and scoped owner decision.
- **Evidence:** V01–V07, source index, baseline/authority record and named next leaf.
- **Hold/fail:** integrity mismatch or absent owner authority stops implementation/live work. Retain evidence; no new bootstrap.
- **Exit:** owner decision plus verified baseline, not a general workload approval.

## A2-G1 — Minimal offline implementation

- **Prerequisite:** A2-G0; L02–L05 implemented in an authorized future workspace.
- **Expected outcome:** explicit route, durable pause/action identity, conservative recovery and scoped re-entry retain the existing controller contract.
- **Exact checks:** A2-R01–R04, S01–S09, V01–V06 at mocked/helper boundaries, O01–O05. Reverse P07–P09 limitations into desired regression assertions. Old 63 + 119 tests still pass with no skips; publish actual additional test names/counts. Test legacy paused, configured, prepared, uncertain and terminal states.
- **Evidence:** source diff/revision, raw unit outputs, per-case assertions, local-Git receipt checks, no-effects assertions for every invalid identity/scope/action.
- **Hold/fail:** no installation or live attempt while an offline invariant fails. A mocked positive stale result is not live acceptance.
- **Exit:** new candidate pinned and compatible-state handling documented.

## A2-G2 — Installed Windows and account route

- **Prerequisite:** A2-G1; owner permits installation/account checks; usable signed-in desktop and authorized Git route.
- **Expected outcome:** each private plugin selects its verified account/profile/root/backend; preflight makes no Send.
- **Exact checks:** A2-W01–W03, live R01/R02; PowerShell syntax/helper tests and UTF-8 output; wrong-account/draft/duplicate-window no-Send holds; exact branch ref and fresh composer; native state path; short window mutex; state/intent/marker unchanged by preflight.
- **Evidence:** actual installed hashes and account-specific route receipts, Windows/Chrome versions, PowerShell logs, exact ref SHA, before/after journals and owned-window cleanup.
- **Hold/fail:** unresolved account/profile, login, path, branch, composer or state compatibility blocks G3. Preserve original release and pending actions; no permissive default.
- **Exit:** the precise installed candidate/account combination is known. A ZIP comparison alone is insufficient.

## A2-G3 — Two-run isolation, recovery and bounded stops

- **Prerequisite:** A2-G2; two owner-created Project/repo fixtures, fresh published branches, fixed caps.
- **Expected outcome:** normal finish and cap-with-work-remains; one paused/restarted while peer progresses; correct same-worker recovery; exactly-once observed handoffs or explicit no-resend holds.
- **Exact checks:** A2-D01–D03; real V01/V02/V03/V04/V05/V06; live authorized S04/S05/S06/S07/S08/S09 where a browser boundary is involved. Cat/Dog count 2/cap 3 `STOP_FINISHED`; Bird/Pig count 2/cap 2 `STOP_CAP`, next review eligible and absent. Positive stale test must show newer completed response, owned-probe close, safe reload, normal consumption and publication check.
- **Evidence:** run/worker/action/route mapping, actual overlapping intervals, peer progress while paused, click/readback trace, both Git chains, final journals/markers, draft/window preservation and all interventions.
- **Hold/fail:** positive stale cannot be reproduced → NOT_RUN; manual reload/format correction → ASSISTED, not unattended PASS. Expected negative fault hold passes only its safety case. Unexpected duplicate/misroute/cap violation stops progression.
- **Exit:** all positive and safety cases satisfied on the target candidate, with planned fault interventions labelled separately.

## A2-G4 — Shoco iPhone and account-switch acceptance

- **Prerequisite:** A2-G3; fresh approval fixture and Shoco private plugin verified.
- **Expected outcome:** phone request chat excluded; one approval delivered to original desktop worker; receipt verified before one successor; terminal finish; safe account round-trip.
- **Exact checks:** A2-P01–P03 and live O01–O05: first desktop count one; no approval edit before scoped input; one anchored input; exact two-line `NOTES.md` chain; count two; repeat request no duplicate; wrong route/scope holds; already-advanced input is not falsely reported as delivered.
- **Evidence:** request-channel/account record, owner-input receipt, turn anchor, both Git receipts, Send timeline, final stop and repeated invocation results.
- **Hold/fail:** earlier James Student result is not substitution. Any pending/uncertain action must reconcile first; wrong/unclear account or approval scope makes no Send.
- **Exit:** actual Shoco installed candidate passes. A later patched release must be named, not labelled an unchanged 0.4.3 pass.

## A2-G5 — Measured capacity

- **Prerequisite:** A2-G4; frozen [thresholds](capacity_thresholds.proposed.json), workload and candidate; owner-approved resource/time budget.
- **Expected outcome:** practical concurrency envelope for this exact PC/configuration, independent of worker caps.
- **Exact checks:** A2-C01–C03, N=2 → 3 → 4 → 6 → 8 → further +2 steps; three bounded cohorts per level; real all-run overlap; per-run publication/terminal invariants; proposed latency/resource criteria; first failing level diagnosed; last-good level reconfirmed.
- **Evidence:** completed [worksheet](capacity.csv), full timing/resource samples and sample counts, metrics by account/profile, failure reason and last-good confirmation.
- **Hold/fail:** any safety failure stops all further admission in the affected shared session. Saturation stops scaling without deleting/retrying state. If budget ends before a limit, report only a tested lower bound and keep the ceiling-finding objective open.
- **Exit:** measured limit and selected operating level, or an explicitly narrower owner-accepted bounded result that does not claim full G5 closure.

## A2-G6 — Scoped release and operator handoff

- **Prerequisite:** accurate A2-G0–G5 dispositions; L10 independent closeout and owner review.
- **Expected outcome:** release decision limited to what actually passed; simple start/pause/resume/check; no erased old holds.
- **Exact checks:** A2-Q01 four-operation walkthrough and release matrix; Q02 preserved/owner-directed disposition of Rowing, SolidWorks and old uncertain attempts; rollback/state compatibility documented.
- **Evidence:** signed-off gate register, account/revision matrix, original-run disposition, known limits and exact next action.
- **Hold/fail:** do not call all gates closed when a required case is NOT_RUN or only assisted. Ordinary-project closeout remains open if those runs stay paused. Any limited release must say so.
- **Exit:** owner approves the stated scope. It does not authorize unrelated workloads or automatic merge.

## Result vocabulary

- `PASS`: required observable result and evidence exist for this exact case/revision.
- `FAIL`: wrong result, invariant violation, threshold failure or unexpected intervention.
- `HOLD`: unresolved identity, authority or possible submission; no automatic continuation.
- `ASSISTED`: achieved only with extra operator recovery/correction; preserve and repeat the unattended case.
- `NOT_RUN`: required environment/condition/sample absent; no inference from another account/revision.
- `OFFLINE_CORROBORATED`: supports the baseline only, not live acceptance.

Never average a misroute away or count a safety hold as useful completed work.
