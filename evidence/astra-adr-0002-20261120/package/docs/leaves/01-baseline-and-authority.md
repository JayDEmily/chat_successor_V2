# A2-L01 — Freeze baseline and authority

**Prerequisite:** supplied archive and an owner decision on ADR 0002. **Gate:** A2-G0. **Checks:** A2-E01–E03.

## Expected outcome

A reproducible baseline with clearly separated fresh offline results, historical live observations, source limitations and remaining acceptance. The owner approves or amends the bounded plan; neither paused ordinary-project run is implicitly resumed.

## Work

1. Record the archive SHA, source/candidate revisions and ZIP payload match from V01–V05. Carry forward 63 + 119 passing tests and 13 valid fixtures at their exact scope.
2. Read ADR 0001 and the current brief before older “next action” notes. Preserve the pause table and its absolute Sydney/UTC times. Retain the Rowing/SolidWorks journals and original uncertain approval/rotation attempts separately.
3. Identify both account routes, exact Project/repo/branch selection rules, worker caps and the authorized fixture branches. Owner-created Projects/repos are prerequisites, not automation to build in this leaf.
4. Record the three new characterization limitations P07–P09 as repair candidates, not as observed live failures.
5. Confirm which future trial writes, account switches, bounded fault injections and resource budgets the owner authorizes. A proposed plan is not that authorization.

## Exact checks and evidence

- **E01:** rerun the pinned reproducer into a new directory; require 295 manifest matches, 268 normalized source matches, release/source match and old suites without skips. Preserve raw command logs.
- **E02:** restore all six bundles sequentially; fsck/ref TSV match; validate all 13 fixture states; retain interrupted/assisted outcomes. Rejoin the 15 A/B/F published state slices to their supplied saved IDs, without claiming live replay.
- **E03:** record run/count/cap/branch/pending/pause fields from the supplied checkpoint and the separate post-pause receipt. Record owner ADR decision and the named next leaf. `b91b00f…` remains staged, not a phone pass.

## Hold / failure

Integrity or content mismatch: stop before running unverified code or modifying an installation; explain the exact path/hash. Missing authority: deliver the proposed plan and hold execution. Unavailable private journals/accounts: retain the supplied redacted baseline and mark live identity unverified. Do not invent a replacement run.

## Completion artifact

Baseline ledger, reproducible output, named owner decision, fixture allocation and open-gate list. Sources: S01–S09, S14–S16; V01–V07.
