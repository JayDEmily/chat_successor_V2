# ADR 0002 second corrective candidate

**Status — offline implementation checks passed. Independent A2-G1 decision pending.** 20 November 2026 AEDT.

Source `9e6421112286f7e993d7e91a3e63fbfea0a0c206`, tree `4f29a26ac119bb8485d951c80d13fe358d9d22e2`, direct parent `2491fcc68a64d8c6de62e63d62424de8e0c86cfd`. This addresses all five findings in the [independent review of 66f4b94](../independent-66f4b94/REPORT.md). A2-G2–G6 are NOT_RUN.

| Cases | Corrected behavior |
| --- | --- |
| R04 | Persist acknowledgement of the marker digest that the controller observed. Inspection reports a fresh generation as requested until acknowledged and preserves terminal state. |
| S01 | Require a verified prose leaf for every final status. The native harness exercises prose and non-prose forms of all three statuses. |
| S02 | Reject a blank continuation in published fixture state before consuming the assistant response. A local-Git regression publishes the bad receipt, then proves the original response can adopt the repaired receipt. |
| S05, S06, O04 | Compare the latest complete posted user turn and, for same-chat input, the exact preceding assistant anchor. An expected substring in a longer synthetic turn cannot acknowledge either same-chat or successor Send. |
| O05 | Save a private SHA-256 receipt with owner input. Dispatch compares the received file against it after restart and again at the native boundary. Synthetic input substitution under the same request ID preserves the prepared action and prevents dispatch. |

| Check | Evidence |
| --- | --- |
| Windows 3.13.15 integration, 113/113 | [Raw output](windows-integration.log) |
| Ubuntu 3.14.4 integration, 113/113 | [Raw output](ubuntu-integration.log) |
| Windows original reference kit, 119/119 | [Raw output](windows-reference.log) |
| Ubuntu original reference kit, 119/119 | [Raw output](ubuntu-reference.log) |
| Native Windows PowerShell action, turn body, prose and owner receipts | [PASS](native-dispatch.log) |
| Native Windows PowerShell view and profile helpers | [PASS](native-view-profile.log) |
| Native Windows PowerShell legacy view comparisons | [PASS](native-legacy-view.log) |

The suites use `python -X utf8 -m unittest discover -s integration/tests -v` and `python -X utf8 run_offline.py --out <temp>` from the reference kit root, with `python3` on Ubuntu. All four exited zero with no failures, errors or skips. Temporary output paths are abbreviated. The reference kit and plugin source match the previous pin. The reviewer should apply the [strict commission](../../../../../docs/astra-succession/adr-0002/G1_STRICT_REVIEW_COMMISSION.md) to this source pin.
