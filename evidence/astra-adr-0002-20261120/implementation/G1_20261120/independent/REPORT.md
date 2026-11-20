# ADR 0002 independent A2-G1 review

**Verdict — A2-G1 OFFLINE HOLD.** 20 November 2026 AEDT. The published candidate passes the existing suites and Windows helper tests. Independent probes found offline launch, recovery and approval failures that block installation.

Reviewer — Codex desktop continuation, separate from the worker who authored L02–L05 and ran the receiver precheck. Reviewed against the [operative ADR](../../../../../docs/adr/0002-account-bound-resumable-runs.md), [exact case register](../../../package/acceptance/cases.csv), [Astra leaves](../../../package/docs/leaves/) and the [published review commission](../../../../../docs/astra-succession/adr-0002/G1_STRICT_REVIEW_COMMISSION.md).

## Candidate and execution

- Candidate [9a2fc382049a548adfefb5ed26a202c715988ca2](https://github.com/JayDEmily/chat_successor/commit/9a2fc382049a548adfefb5ed26a202c715988ca2). Tree `f6fcf2942e08ba73bbf32c9c70d74db2a02d5b4f`. Direct parent `f20f1b14080c58f80a6e4e646d7ba5173d8791a9`.
- Fresh GitHub clones on Windows and Ubuntu were checked out at that commit. Git object identities matched, both working trees were clean and both passed `git fsck --full`. The intake branch tip `abe27afd310d3a1da03f68a7feb89c1097919d23` has the same integration, plugin and reference-kit source as the candidate. The reference kit also matches baseline `283e6c1`.
- Ubuntu verified all 94 package manifest entries and original archive SHA-256 `8fcb94cd24b954c6f31b37a636fcb346dac1d48c1e7b647713fae664ff6a15c2`. [Manifest readback](ubuntu-manifest.log).
- Both Python versions ran the complete suites with zero failures, errors or skips. Windows used CPython 3.13.15 and native Windows PowerShell 5.1.26100.9818. Ubuntu under WSL used CPython 3.14.4. The Python and PowerShell results exercise source, local Git and mocks. The installed account route and real browser lifecycle are later gates.

| Environment and command | Result | Duration and evidence |
| --- | --- | --- |
| Windows `python -X utf8 -m unittest discover -s integration/tests -v` | 106/106, exit 0 | 22.893 s [output](windows-integration.log) |
| Windows `python -X utf8 run_offline.py --out <temp>` from the original kit | 119/119, exit 0 | 13.752 s [output](windows-reference.log) |
| Ubuntu `python3 -X utf8 -m unittest discover -s integration/tests -v` | 106/106, exit 0 | 0.896 s [output](ubuntu-integration.log) |
| Ubuntu `python3 -X utf8 run_offline.py --out <temp>` from the original kit | 119/119, exit 0 | 0.687 s [output](ubuntu-reference.log) |
| Native `powershell.exe -NoProfile -File integration/tests/test_a2_l03_ps_action_gate.ps1` | PASS, exit 0 | 2.158 s [output](windows-powershell-action.log) |
| Native `powershell.exe -NoProfile -File integration/tests/test_a2_l04_ps_view_helpers.ps1` | PASS, exit 0 | 2.089 s [output](windows-powershell-view.log) |
| Native `powershell.exe -NoProfile -File integration/tests/test_worker_view_recovery.ps1` | PASS, exit 0 | 1.744 s [output](windows-powershell-legacy-view.log) |
| `python -X utf8 probes.py <candidate checkout>` | Reproduced, exit 0 on both hosts | Windows 4.403 s [results](windows-probes.json), Ubuntu 0.689 s [results](ubuntu-probes.json) |
| `powershell.exe -NoProfile -File native-probes.ps1 -Candidate <candidate checkout>` | Reproduced, exit 0 | 2.157 s [results](native-probes.json) |

The [Python probes](probes.py) use temporary state and run actual Git operations against disposable local remotes. The [PowerShell probes](native-probes.ps1) extract selected candidate functions and use synthetic windows and turns. Probe exit 0 means the measurements completed. The recorded values are the gate evidence. The suite logs abbreviate the temporary result paths.

## Reproduced findings

1. **R01, R02 and V05 — the declared backend and existing window profile are unverified.** A private route naming the all-zero backend SHA yielded `preflight_passed`, wrote one fixture bootstrap intent and reached the stub's Send boundary. A separate native probe selected an existing synthetic window from a different profile when its project, saved chat URL and handle matched. `Open-ChromeWindow` uses the selected profile for new windows. `Find-TargetWindows` selects existing windows by handle and URL. Verify the backend pairing and target profile at the existing boundaries. [Account route](../../../../../integration/account_routes.py), [native target lookup](../../../../../integration/uia_adapter.ps1).
2. **R04 — status omits the last verified publication.** The generic local-Git repair produced the exact SHA and ref in the verification and adoption logs. `inspect_state` returned `publication_commit: null` even though the saved response, checkpoint and pending action were present. L05 permits the SHA to live in private diagnostics, which can supply the read-only status evidence. [Status and publication code](../../../../../integration/runner.py).
3. **S02 — a wrong-worker receipt consumes the response on the supported story path.** Against a real local bare remote, the original story reader fetched a valid published step attributed to a different saved chat. The controller held Send, consumed the source response and logged `IDENTITY_MATCH` and `publication_receipt_adopted`. The generic reader rejected the wrong worker before consumption and accepted the repaired receipt for the same response. Apply that attribution check across the supported readers. [Publication path](../../../../../integration/runner.py).
4. **S06 — the saved-ID boundary accepts a provisional slug.** The native URL function extracted `local-chatgpt` from a synthetic Project `/c/local-chatgpt` URL on the expected host. An exact-message reconciliation with that ID passed through `WindowsUIA.reconcile_readonly`. The controller cleared uncertainty and counted worker two. The saved-view and Git receipt validators already require a saved-chat UUID. This was an injected adapter receipt. The older live preview incidents retain their recorded outcomes. [Native URL and reconciliation](../../../../../integration/uia_adapter.ps1), [Python reconciliation](../../../../../integration/windows_backend.py).
5. **S09 — a different bootstrap action ID passes the native gate.** A valid initial receipt passed. Changing only its action ID to another valid 32-character ID passed again. The bootstrap branch checks syntax and receives the expected run ID. It has no expected action ID to compare. Carry the exact bootstrap action ID into the existing gate. [Bootstrap](../../../../../integration/launch_story.py), [native receipt check](../../../../../integration/uia_adapter.ps1).
6. **V04 — an already consumed completion qualifies for stale reload.** With a spinning original, the native comparison accepted a fresh ready view carrying the same response ID the fixture had already consumed. The changed-user negative control failed as expected. Python has the journal's consumed responses and sends the original view anchor to the probe. The native completion check has no consumed-response context. Require unconsumed completion evidence before reload. [Observer](../../../../../integration/windows_backend.py), [native stale comparison](../../../../../integration/uia_adapter.ps1).
7. **O05 — dispatch continues after the private owner input disappears.** The probe saved a correctly anchored owner action, then removed its synthetic owner-input file before dispatch. The pointer entered the mocked same-chat Send once. Verify the saved input at dispatch and preserve the pending action if the file is unavailable. [Owner input handling](../../../../../integration/owner_reentry.py), [dispatch](../../../../../integration/runner.py).

## Exact case decisions

`OFFLINE_PASS` covers the mocked, helper or local-Git predicates for this candidate. All installed and live predicates in A2-G2–G6 are `NOT_RUN`.

| Case | Decision | Basis |
| --- | --- | --- |
| A2-R01 | HOLD | Finding 1. Config fields and child environment are exercised. The wrong declared backend reached preparation and simulated Send. |
| A2-R02 | HOLD | Unknown keys, duplicate JSON and shared profile paths hold in the suite. Finding 1 shows the unchecked backend and existing window profile. |
| A2-R03 | OFFLINE_PASS | Account namespacing, stable new-job retry, display rename, repo-case and branch reuse tests. Independent 32-character ID negative stopped before project resolution. |
| A2-R04 | HOLD | Unbound or changed legacy routes hold, and marker/ack readback passed. Finding 2 shows missing publication evidence in status. |
| A2-S01 | OFFLINE_PASS | Reference parser and C04/C12/C15/C17 plus integration streaming, continuation-at-cap, finish and duplicate-response tests. |
| A2-S02 | HOLD | Generic hold, retry, trailer and fetch-failure paths pass. Finding 3 violates the receipt and consumption invariant on the story reader. |
| A2-S03 | OFFLINE_PASS | Temporary Git rotation rejected a wrong-worker tip, adopted the corrected tip once, and retained the entry branch, count and cap. Malformed or conflicting locator tests held. |
| A2-S04 | OFFLINE_PASS | Mock pause during prepare and adapter pre-click pause retain the action and count. The native code checks the marker before typing and Invoke and leaves a typed draft in place. |
| A2-S05 | OFFLINE_PASS | Lost-ack and exact-action tests passed. Native readback rejected an older identical input and accepted the exact input after the triggering response. |
| A2-S06 | HOLD | Lost-ack and duplicate-ack tests passed. Finding 4 advances count and clears uncertainty on the synthetic provisional ID. |
| A2-S07 | OFFLINE_PASS | Lost initial acknowledgement reconciles with the first intent, pre-click pause retains it, and a missing journal with a timing log holds. S09 separately checks exact bootstrap action-ID matching. |
| A2-S08 | OFFLINE_PASS | Latest pause marker survives a scoped release race, paused restart makes no Send, and terminal pause/resume tests preserve terminal reason and count. |
| A2-S09 | HOLD | Ordinary target identity and stale-receipt negatives passed. Finding 5 shows the bootstrap substitution. |
| A2-V01 | OFFLINE_PASS | Exact saved-worker URL, recovery and two stable reads pass at the mock boundary with count and journal preserved. |
| A2-V02 | OFFLINE_PASS | Mock displaced-view restoration keeps the same worker and subsequent duplicate accessible views hold. Actual tab and peer behaviour belongs to G3. |
| A2-V03 | OFFLINE_PASS | Native newer-completion and stable-double-read helpers passed. The mocked refreshed view then returned the new response via normal observation. Actual stale reload and subsequent publication are G3. |
| A2-V04 | HOLD | Streaming, changed user and timing controls passed. Finding 6 leaves the consumed response eligible for reload. |
| A2-V05 | HOLD | Missing and duplicate view, wrong Project, draft and ambiguity checks are corroborated. Finding 1 reproduces selection of the wrong-profile window in the native lookup. |
| A2-V06 | OFFLINE_PASS | Mock worker advancement suppresses duplicate dispatch. Native pre-click advancement returns before Invoke and preserves the composer. |
| A2-O01 | OFFLINE_PASS | Inspection, known-unsent config reuse, explicit new-job and uncertain initial reconciliation tested. Bootstrap counts the observed saved desktop worker. |
| A2-O02 | OFFLINE_PASS | Matching hold and input queue one same-chat pointer with unchanged count. Subsequent handoff requires the published worker receipt. |
| A2-O03 | OFFLINE_PASS | Same ID and equivalent alternate ID for one hold deduplicate. Changing the scope under the same ID holds. |
| A2-O04 | OFFLINE_PASS | Exact posted-turn reconciliation is required for an uncertain input. Advanced observation has a distinct unverified result and sends nothing. |
| A2-O05 | HOLD | Stale anchor and unreadable-browser holds passed. Finding 7 reaches the Send seam after private input becomes unavailable. |

**Total** — 15 OFFLINE_PASS and 9 HOLD. Return the findings to L02–L05 for targeted correction and review a newly pinned candidate at A2-G1. A2-G2/L06 remains blocked by the published offline gate.

Git verification establishes the fetched object, exact ref, worker and run evidence, and the response anchored in saved state. For the valid generic case the verification and adoption logs carry the exact SHA. The saved controller journal contains the consumed response and checkpoint/action state and has no SHA field. The project's own process governs approval and work quality.
