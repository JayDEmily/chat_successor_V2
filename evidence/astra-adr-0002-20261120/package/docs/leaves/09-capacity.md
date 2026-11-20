# A2-L09 — Measure practical concurrency

**Prerequisite:** A2-G4; owner-approved per-stage time/resource budget and unchanged candidate/configuration. **Gate:** A2-G5. **Checks:** A2-C01–C03.

## Expected outcome

A measured operating envelope for this PC, account/profile arrangement, Chrome build and candidate — not a fixed two-run product limit or an invented maximum.

## Work and exact checks

Follow [CAPACITY.md](../../acceptance/CAPACITY.md).

1. Record PC/Windows/Chrome/Python/backend/profile configuration and idle resources. Freeze the transport and resource thresholds **before** measuring. Keep the ordinary 20-second poll setting and per-run caps (finish fixture three, cap fixture two).
2. Measure N=2 using the successful pair as the starting design, including one pause/restart while its peer progresses. Count actual overlapping controller intervals separately from open nonterminal runs and saved workers.
3. Increase N to 3, 4, 6, 8, then by two while criteria pass and the owner-approved budget permits. Each stage uses three fresh bounded cohorts; require all runs to overlap for two polling intervals and an observed handoff per run. If too short, use a pre-authorized continuation slice, never manual padding disguised as success.
4. Log per-run identity/action/publication outcomes, clocked transport and observer delays, resource samples and temporary-window cleanup. Separate model work, source rendering lag, Git latency, mutex wait, UIA time and handoff latency.
5. Any duplicate/misroute/approval leak/cap breach is a hard stop. An unresolved handoff, unfair starvation, resource or latency threshold failure also stops admissions and further scaling, while preserving/reconciling current work.
6. Confirm the highest passing level with another bounded cohort after the first failing level. Publish both levels and the limiting evidence. If the budget ends before a failure, report “tested through N, ceiling not measured”; do not invent a limit or pass the full ceiling-finding objective.

## Evidence

Completed [capacity worksheet](../../acceptance/capacity.csv), frozen threshold file, raw per-action events, per-run evidence records, resource time series, sample counts and percentile method, interventions/failures and last-good recovery. Use aliases in shared reports; retain complete private mapping for independent readback.

## Hold / failure

Stop new cohort admissions; do not raise per-run caps, increase deadlines silently, disable checks, globally kill Chrome, or introduce a scheduler to make the chart look better. Identify the measured bottleneck and choose only the smallest justified fix. Any changed candidate/settings creates a new series and requalifies the affected earlier gates.

Source: S01 requires stepwise capacity; S07 supplies only a two-run historical baseline. No capacity result is delivered by this offline review.
