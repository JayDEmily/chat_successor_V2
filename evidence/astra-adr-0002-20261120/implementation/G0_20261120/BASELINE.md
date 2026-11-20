# A2-G0 verified baseline and owner authority

**Date:** 20 November 2026 (Melbourne, AEDT). **Disposition:** A2-G0 PASS for archived evidence and scoped owner grant. Live release gates remain NOT_RUN.

## Source and new independent reproduction

- Exact received Astra archive `8fcb94cd24b954c6f31b37a636fcb346dac1d48c1e7b647713fae664ff6a15c2` (2,286,051 bytes), kept verbatim under the intake.
- Exact original input `473876c6b0fffa1f55ef68ad9da62bda0e949295808f899d502edd68ab5f3945`.
- Reviewed source `283e6c17bf3359c203a362fd6593563480eeea5f`; 0.4.3 candidate `2c29406b1c43904c5ead79064fe7856971e0aa2e`; separately published Astra intake base `b3daeda63643b9ad8d8860fb5cc99a3e4ef400c7`.
- Fresh independent Ubuntu execution of unchanged `package/tools/reproduce_review.py` with original archive and a new output directory; [raw output](reproduction/summary.json) and all companion raw logs/JSON retained.
- Runtime **CPython 3.14.4 / Git 2.53.0**, distinct from Astra's earlier recorded 3.13.5 environment. Python 3.13 executable not installed in this Ubuntu; no claim of an additional 3.13 rerun.
- Fresh result **PASS**: 295/295 input manifest hashes, 268 source files reconciled, six Git bundle histories/refs/fsck, 13 fixture validators, all 15 A/B/F event joins, 63 integration and 119 reference tests without skips, nine baseline probes with P07–P09 still demonstrating missing features. Input bytes unchanged. No live Windows/browser/iPhone tests in this reproducer.

## E03: real pause readback, no writes

Read-only local inspection of `C:\Users\james\AppData\Local\ChatSuccession\Runs` at approximately 13:41:55 AEDT on 20 November verified:
- Rowing run `b401f984a1927f6979067d07`, Project A Test: count 2/cap 2, `halted=Operator pause requested`, `controller.pause` present, no pending action recorded.
- SolidWorks run `271867d56ebd3443a4b40fa6`, Project B Test: count 1/cap 2, same halt and pause marker, no pending action.
- Both configs have the legacy nine fields, with no account/profile binding: `project`, `project_name`, `project_url`, `repo`, `branch`, `repo_dir_wsl`, `run_id`, `max_unique_chats`, `workflow`. State schema: `config`, `state`, `version`.
- Read-only inspection is a point-in-time local snapshot, not proof that every Chrome chat is idle now or that a completed worker receipt was consumed. Original controller/run files, marker and branches were not changed.

## Authority, isolation and fixture plan

The owner expressly delegated execution of Astra's ordered leaves, including implementation and appropriate testing, without renewed routine approval. The [operative decision](../../../../docs/adr/0002-account-bound-resumable-runs.md) records this scope and preserves ordinary-project pauses and safety holds.

For future G3/G4 tests, first verify that the existing Cat/Dog, Bird/Pig and approval test repos/Projects are still separate and available in the correct signed-in account, then use fresh fixture branches. Do not assume a historical saved run is eligible to reuse or create a different ChatGPT Project without verifying its exact identity. Do not introduce new GitHub repos until the existing fixtures prove insufficient.

## Gate outcomes

- **A2-E01:** PASS — fresh input integrity, normalized source, release and offline-suite comparisons.
- **A2-E02:** PASS — six bundled Git histories and 13 fixture states, including partial/assisted cases retained at historical scope.
- **A2-E03:** PASS — owner scoped adoption, exact live pause-marker readback and named next leaf `A2-L02`; no paused-run release.

**Next:** Implement A2-L02 explicit account route and status contract, with R01–R04 offline tests, and preserve all legacy runs. No release or browser Send is authorised merely by closing G0.
