# ADR 0002 independent A2-G1 review of 66f4b94

**Verdict — A2-G1 OFFLINE HOLD.** 20 November 2026 AEDT. The candidate closes the original wrong-backend, destination, provisional-ID and missing-input probes. New fault probes reproduce failures in seven of the 24 exact offline cases. Installation and live gates remain ineligible on this pin.

Reviewer — Codex independent reviewer `g1_reviewer`, separate from the corrective author and precheck. Reviewed the [operative ADR](../../../../../docs/adr/0002-account-bound-resumable-runs.md), [Astra case register](../../../package/acceptance/cases.csv), [L02–L05 acceptance](../../../package/docs/IMPLEMENTATION_PLAN.md), [prior independent hold](../independent/REPORT.md), and [correction evidence](../corrective/RESULT.md).

## Pinned source and independent execution

- Source `66f4b94dc6fa94c708b42c11d2681da291dd9d99`, tree `5f78ffde112dfd6075f3d241e1bcf4e72363d3b2`, direct parent `6c860f971ae9a26e514e24444695e69644ccc249`. Fresh Windows and Ubuntu GitHub clones matched those IDs with empty status and `git fsck --full` exit 0. The branch intake tip `04ffeded885c32884cb6088788c46e7316feec1d` has the same integration, reference kit and plugin tree as the tested source.
- Ubuntu ran `sha256sum --check --strict MANIFEST.sha256` successfully for all 94 package entries. The separate original return archive matched digest `8fcb94cd24b954c6f31b37a636fcb346dac1d48c1e7b647713fae664ff6a15c2`. [Manifest readback](ubuntu-manifest.log)
- Windows used CPython 3.13.15 and native Windows PowerShell 5.1.26100.9818. Ubuntu under WSL used CPython 3.14.4. Both Python suites had zero failures, errors or skips on each host.

| Host and exact command | Result | Execution time and evidence |
| --- | --- | --- |
| Windows `python -X utf8 -m unittest discover -s integration/tests -v` | 111/111, exit 0 | 25.309 s [log](windows-integration.log) |
| Windows `python -X utf8 run_offline.py --out <temporary directory>`, reference kit cwd | 119/119, exit 0 | 13.874 s [log](windows-reference.log) |
| Ubuntu `python3 -X utf8 -m unittest discover -s integration/tests -v` | 111/111, exit 0 | 1.682 s [log](ubuntu-integration.log) |
| Ubuntu `python3 -X utf8 run_offline.py --out <temporary directory>`, reference kit cwd | 119/119, exit 0 | 1.532 s [log](ubuntu-reference.log) |
| `powershell.exe -NoProfile -File integration/tests/test_a2_l03_ps_action_gate.ps1` | PASS, exit 0 | 2.927 s wall [log](native-action.log) |
| `powershell.exe -NoProfile -File integration/tests/test_a2_l04_ps_view_helpers.ps1` | PASS, exit 0 | 3.398 s wall [log](native-view.log) |
| `powershell.exe -NoProfile -File integration/tests/test_worker_view_recovery.ps1` | PASS, exit 0 | 2.759 s wall [log](native-legacy-view.log) |
| Windows `verify_backend` called with exact HEAD and with all-zero SHA | Expected acceptance and hold, exit 0 | [Git readback](windows-backend.log) |

Reference logs abbreviate paths to private temporary outputs. The independently authored [Python fault probe](review-probes.py) runs as `python -X utf8 <probe> <pinned checkout>` on Windows or `python3 -X utf8 <probe> <pinned checkout>` on Ubuntu. The [native fault probe](native-review-probes.ps1) runs as `powershell.exe -NoProfile -File <probe> -Candidate <pinned checkout>`. The probe exits show that the measurements completed. They use local bare Git remotes, temporary journals, a fake browser adapter, and native PowerShell functions on a synthetic UIA text tree. [Windows results](windows-review-probes.json), [Ubuntu results](ubuntu-review-probes.json), [native results](native-review-probes.json)

## Reproduced holds

1. **R04 — a fresh pause marker is reported as acknowledged.** After a synthetic run acknowledges its first pause, replace the marker with a second generation while retaining the journal. Inspection still reports `pause_acknowledged=true` ahead of any observer check for that generation. It derives acknowledgement from marker presence and the previous halt reason. The marker bytes are preserved. This is a status error. The separate release-race protection still honors a newer marker. [Inspection code](../../../../../integration/runner.py), [Windows and Ubuntu probe](review-probes.py)
2. **S01 — a final non-prose UIA leaf becomes actionable.** A stubbed accessibility tree ends in a `CHAT_STATUS: NEED_MORE_TIME` text leaf classified as non-prose. `Read-CurrentTurn` marks it ready and includes it as the final response line. A non-prose `CHAT_STATUS: TASK_COMPLETE` also becomes ready even when the hierarchy qualification is false. The flag is applied only to branch locators. Classify the final status leaf at the existing native boundary for every status. [Native extraction and observer](../../../../../integration/uia_adapter.ps1), [native probe](native-review-probes.ps1)
3. **S02 — a malformed published continuation consumes the response before repair.** On a disposable bare Git remote, publish a fixture `STATE.json` with the exact run and worker, `programme_complete=false` and whitespace-only `next_task`. The fixture reader accepts it and `cycle` returns `HOLD` after journaling the response as consumed. Publish a corrected next task and re-offer the same completed turn. It returns `IGNORE`, preventing recovery from the repaired receipt. Both runs made zero browser Prepare or Send calls. Validate the fixture's continuation before response consumption. [Fixture reader](../../../../../integration/repo_reader.py), [receipt processing](../../../../../integration/runner.py), [Git-backed probe](review-probes.py)
4. **S05, S06 and O04 — a fragment is accepted as the exact posted turn.** The native acknowledgement helper accepts an exact-body positive and also accepts a longer synthetic user turn containing an extra text node and the expected continuation as a second node. It accepts that fragment with the correct triggering assistant anchor and with the unanchored successor mode. The acknowledgement boundary returns the expected string as the observed submission, so matching a fragment can clear uncertainty for a different body, including an owner pointer. Verify the complete user-turn body at the existing readback boundary. [Readback helper and result construction](../../../../../integration/uia_adapter.ps1), [native probe](native-review-probes.ps1)
5. **O05 — a substituted owner scope survives a restart and reaches dispatch.** Prepare a scoped owner request, replace its synthetic input file with a different instruction, scope and pointer under the same request, saved-worker and response IDs, and reload the journal. The candidate accepts the new file as its comparison baseline, then reaches fake Prepare and Send once each. The probe deliberately loses the fake acknowledgement and the original action becomes uncertain. Persist a binding to the authorized input at preparation and verify it on restart. [Private owner entry](../../../../../integration/owner_reentry.py), [dispatch checks](../../../../../integration/runner.py), [replacement probe](review-probes.py)

## Exact A2-G1 decisions

Each PASS covers the named offline predicate through source, tests, or the recorded helper boundary. Installed and live A2-G2–G6 are all `NOT_RUN`.

| Case | Disposition | Independent basis |
| --- | --- | --- |
| A2-R01 | OFFLINE_PASS | Actual Git accepted the exact HEAD and refused the wrong backend. Route, child config and exact native root tests passed. The C# window property reader compiled and holder/target matching used synthetic windows. |
| A2-R02 | OFFLINE_PASS | Missing and unknown keys, duplicated records/profile/window identity, and wrong backend/root hold before a synthetic launch. Native helper rejected a matching URL and HWND with a different profile. |
| A2-R03 | OFFLINE_PASS | Mock project rename, account-namespaced identity and repeat/new-job tests passed. Ref rotation keeps source identity and cap. Invalid request ID length is rejected before resolution. |
| A2-R04 | HOLD | Last publication diagnostics match durable run/ref/response, and legacy ambiguity holds. Finding 1 shows that a new marker inherits the previous acknowledgement in status. |
| A2-S01 | HOLD | Reference parser, stream, cap, finish and repeat cases passed. Finding 2 bypasses quote/tool separation when the accessibility tree presents an unadorned text leaf. |
| A2-S02 | HOLD | Wrong worker now holds prior to consumption for both story and generic Git reader paths. Finding 3 leaves a real fixture receipt unrecoverable on the same completed turn. |
| A2-S03 | OFFLINE_PASS | Local-Git checkpoint rotation requires the response locator and correct-worker receipt, rejects a malformed locator, and preserves entry branch, run/count and cap. |
| A2-S04 | OFFLINE_PASS | Durable prepared action survives paused prepare and adapter pre-click receipts in the suite. Native Send checks the marker before typing and Invoke. Journal/draft recovery is exercised further at G3. |
| A2-S05 | HOLD | Wrong response ID and uncertain action holds passed, and exact body after anchor acknowledged. Finding 4 accepts a different complete user turn containing an exact fragment. |
| A2-S06 | HOLD | Provisional ID and lost/duplicate acknowledgement controls passed. Finding 4 also applies to unanchored successor readback and weakens exact posted-prompt proof. |
| A2-S07 | OFFLINE_PASS | Immutable initial intent survives the pre-click hold, repeat reads reconcile without new Send, and a prior timing log without a journal holds. |
| A2-S08 | OFFLINE_PASS | Mock release race preserved newest pause bytes and stable terminal stops. The generation acknowledgement display issue is in R04. |
| A2-S09 | OFFLINE_PASS | Bridge and native gate compare the exact action, response, route, handle, message and document. Substituted bootstrap ID and changed document held in Windows PowerShell. |
| A2-V01 | OFFLINE_PASS | Mock restore checks the exact saved Project/chat URL and stable reads without incrementing worker count. Account-specific installed restore remains G2/G3. |
| A2-V02 | OFFLINE_PASS | Mock missing/displaced restoration and duplicate-accessible view hold passed. Actual hidden tab and peer progress are G3. |
| A2-V03 | OFFLINE_PASS | Stable positive same-user unconsumed completion passed native comparison. Mock recovery then uses normal response observation. Real reload/receipt timeline remains G3. |
| A2-V04 | OFFLINE_PASS | Changed user/count, streaming, consumed fresh reply and timer checks passed. Native stale call passes the persisted journal path for consumed history. |
| A2-V05 | OFFLINE_PASS | Wrong-project, duplicate/unverified view and preserved draft controls passed in mocks. Wrong window profile rejected by native lookup. Real login and installed profile remain G2. |
| A2-V06 | OFFLINE_PASS | Mock advanced worker emits no further input. Native late advancement precedes Invoke and preserves typed draft. |
| A2-O01 | OFFLINE_PASS | Mock inspect/status, configured reuse, explicit new and initial uncertainty cases preserve the registered worker count and first intent. |
| A2-O02 | OFFLINE_PASS | Correct anchor and empty composer queue one scoped input. Subsequent handoff requires a published receipt. Exact-content fault during readback is under O04. |
| A2-O03 | OFFLINE_PASS | Same ID and equivalent alternate ID for one hold deduplicate. Conflicting supplied scope holds in normal request replay. |
| A2-O04 | HOLD | Advanced observation is reported separately from delivered scope with no extra send. Finding 4 means an inexact observed turn can still act as delivery evidence after uncertainty. |
| A2-O05 | HOLD | The missing-file and wrong-worker checks now hold. Finding 5 accepts substituted anchored content after restart and advances to the fake Send seam. |

**Totals — 17 OFFLINE_PASS and 7 HOLD.** The exact 24 rows above match the published case register. Correct the recorded boundary failures and pin the next corrective candidate for an independent rerun before A2-G2.

Git verification checks fetched SHA/ref and current run/worker attribution before generic branch adoption. On valid consumption, the saved journal records the response, effective branch and resulting action together. SHA/ref are logged after that save and surfaced by read-only status when they match the journal. Work quality and scope remain governed by the project. Story validation separately checks the chain and chapter attribution. The fixture reader gap in finding 3 concerns adoption eligibility.
