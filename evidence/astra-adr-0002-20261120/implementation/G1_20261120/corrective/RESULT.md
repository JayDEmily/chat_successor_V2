# ADR 0002 A2-G1 corrective candidate

**Status — implementation verified offline, independent A2-G1 decision pending.** 20 November 2026 AEDT.

- Source candidate `66f4b94dc6fa94c708b42c11d2681da291dd9d99`, tree `5f78ffde112dfd6075f3d241e1bcf4e72363d3b2`, parent `6c860f971ae9a26e514e24444695e69644ccc249`.
- The [prior independent hold](../independent/REPORT.md) on `9a2fc38` records the failures that drove these corrections. The candidate is limited to the offline L02–L05 cases. A2-G2–G6 are NOT_RUN.
- The reference kit and plugin source match the previous candidate. The [G2 installation contract](../../../../../docs/astra-succession/adr-0002/ACCOUNT_ROUTE_INSTALL.md) records the private per-profile window ID and exact source pin. Real Chrome identity and document readback are G2 evidence.

## Corrections to the held cases

| Cases | Correction and regression |
| --- | --- |
| R01, R02, V05 | Compare the running backend HEAD and tracked source to the route before browser access. Validate distinct private plugin, profile path and native window AppUserModelID. Native window selection refuses an unverifiable profile. The synthetic launch and no-Send preflight both hold on the wrong SHA. A native helper test exercises wrong-profile rejection and a valid matching target. |
| R04 | Read the latest adopted Git SHA and exact ref from the private timing log by matching the run, effective branch and journaled response. The regression rejects an unconsumed log row. Status remains read-only. |
| S02 | Check worker, run, repo and ref before consuming or logging adoption for every supported reader. An actual local-Git story fixture publishes a wrong-worker receipt and leaves the response unconsumed. |
| S06 | Require saved-chat UUIDs at native URL parsing and Windows submission readback. A mocked provisional successor cannot clear uncertainty or increment count. |
| S09 | Bind bootstrap validation to the original action ID and check the prepared UIA document for both bootstrap and follow-up Sends. Native helper and bridge regressions change only a document or action ID and observe the hold. |
| V04 | Read the worker's journaled consumed responses for stale recovery. The native freshness comparison rejects an already-consumed ready response. It keeps the positive same-user comparison for an unconsumed response. |
| O05 | Read and validate the prepared owner input before browser preparation and compare it again before dispatch. Missing input preserves the same prepared action and count with zero mocked browser calls. |

## Verification

| Command and host | Result |
| --- | --- |
| `python -X utf8 -m unittest discover -s integration/tests -v` on Windows CPython 3.13.15 | [111/111](windows-integration.log) |
| `python3 -X utf8 -m unittest discover -s integration/tests -v` on Ubuntu CPython 3.14.4 | [111/111](ubuntu-integration.log) |
| `python -X utf8 run_offline.py --out <temp>` from the original kit on Windows | [119/119](windows-reference.log) |
| `python3 -X utf8 run_offline.py --out <temp>` from the original kit on Ubuntu | [119/119](ubuntu-reference.log) |
| Native PowerShell 5.1 `test_a2_l03_ps_action_gate.ps1` | [PASS](native-dispatch.log) |
| Native PowerShell 5.1 `test_a2_l04_ps_view_helpers.ps1`, including C# helper compilation | [PASS](native-view-profile.log) |
| Native PowerShell 5.1 `test_worker_view_recovery.ps1` | [PASS](native-legacy-view.log) |
| Windows Git backend check on the clean candidate | [Exact HEAD accepted and all-zero revision refused](windows-backend.log) |

The four Python suites exited zero with no failures, errors or skips. The native helpers exercised extracted functions and synthetic inputs. The suite logs abbreviate temporary result paths. The separate reviewer should use the [strict commission](../../../../../docs/astra-succession/adr-0002/G1_STRICT_REVIEW_COMMISSION.md) with the corrected source pin above and judge all 24 exact offline cases.
