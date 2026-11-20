# A2-L10 — Close out without erasing open evidence

**Prerequisite:** A2-G0–G5 results, including any holds or lower-bound capacity result. **Gate:** A2-G6. **Checks:** A2-Q01–Q02.

## Expected outcome

An owner-approved, accurately scoped release decision; a usable start/pause/resume/check procedure; and preserved disposition for every historical paused/uncertain run.

## Work

- Produce a release matrix by account, exact plugin/package/backend/wrapper/profile binding, installation root, Windows/Chrome versions, and qualifying test cohort. Clearly distinguish unchanged Shoco 0.4.3 from any patched successor release.
- Attach every case result and link raw evidence. Separate parser/interpretation, browser transport, Git publication and useful fixture work. Retain `ASSISTED`, `HOLD`, `FAIL` and `NOT_RUN`; do not collapse them into PASS.
- State the measured simultaneous-run envelope and fixed per-run caps used. If no practical ceiling was reached, publish only the tested lower bound and leave the ceiling objective open.
- Walk the owner through the [four-operation procedure](../../operator/QUICKSTART.md) on an authorized disposable run. Confirm terminal runs cannot resume and a genuine new job is explicit.
- Record each original run's disposition: remains paused/held by owner choice, or separately authorized reconciliation with evidence. Do not merge later successful fixture results into older uncertain attempts.
- Supply a compatible rollback route, known limitations, the last passing candidate and exact next unclosed case. No automatic merge or new workload approval follows from transport acceptance.

## Exact checks / evidence

**Q01:** independent readback of release/account matrix, gate register, no duplicate actions, counts, Git artifacts and the operator start/pause/restart/resume/check walkthrough. Owner acknowledges the release scope and operating envelope.

**Q02:** original Rowing and SolidWorks remain untouched unless the owner explicitly releases them. If released, reconcile the exact saved journals and any changed remote tips before action. Rowing needs a verified second-worker `FINISHED` response/receipt and a terminal cycle, not just the post-pause Git commit. SolidWorks needs its first completion/branch receipt consumed, at most one successor, then a verified second receipt with eligible third work and `STOP_CAP`. Keep earlier provisional-ID attempts separately held until their own read-only reconciliation. If no release is authorized, record “preserved paused/ordinary-project closeout still open,” not “complete.”

## Hold / failure

No release-wide “ready” claim while a required new gate is open. A documented limited fixture/account envelope may be accepted by the owner as a narrower result, but cannot be described as full ordinary-project, stale-recovery or capacity acceptance. Preserve state and report the first unresolved case with its owner-directed next step.

Sources: S04/S05/S07/S15 and the independent evidence review.
