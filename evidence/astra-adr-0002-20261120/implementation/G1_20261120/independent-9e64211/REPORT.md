# ADR 0002 independent A2-G1 review of 9e64211

**Verdict — A2-G1 OFFLINE HOLD.** 20 November 2026 AEDT. All five failures reproduced on the previous pin now pass their independent probes. One remaining fault at the same native text boundary holds four published cases.

Reviewer — Codex independent reviewer `g1_reviewer`, separate from the corrective author. [Operative ADR](../../../../../docs/adr/0002-account-bound-resumable-runs.md) · [Exact cases](../../../package/acceptance/cases.csv) · [L02–L05 work plan](../../../package/docs/IMPLEMENTATION_PLAN.md) · [Prior review](../independent-66f4b94/REPORT.md) · [Corrective evidence](../corrective-9e64211/RESULT.md)

## Pinned source and independent runs

- Source `9e6421112286f7e993d7e91a3e63fbfea0a0c206`, tree `4f29a26ac119bb8485d951c80d13fe358d9d22e2`, direct parent `2491fcc68a64d8c6de62e63d62424de8e0c86cfd`. Fresh GitHub clones on Windows and Ubuntu matched those IDs, showed empty status and passed `git fsck --full`. Published intake tip `09ce6b50fccb0bc6ddd14845caac2914a2283631` has the tested integration, reference kit and plugin source.
- Ubuntu verified all 94 package entries with `sha256sum --check --strict MANIFEST.sha256`. The original archive SHA-256 matched `8fcb94cd24b954c6f31b37a636fcb346dac1d48c1e7b647713fae664ff6a15c2`. [Manifest readback](ubuntu-manifest.log)
- Windows used CPython 3.13.15 and native Windows PowerShell 5.1.26100.9818. Ubuntu over WSL used CPython 3.14.4. The four Python suites had zero failures, errors or skips.

| Environment and command | Result | Time and evidence |
| --- | --- | --- |
| Windows `python -X utf8 -m unittest discover -s integration/tests -v` | 113/113, exit 0 | 28.375 s [log](windows-integration.log) |
| Windows `python -X utf8 run_offline.py --out <temp>` from reference kit root | 119/119, exit 0 | 14.313 s [log](windows-reference.log) |
| Ubuntu `python3 -X utf8 -m unittest discover -s integration/tests -v` | 113/113, exit 0 | 2.003 s [log](ubuntu-integration.log) |
| Ubuntu `python3 -X utf8 run_offline.py --out <temp>` from reference kit root | 119/119, exit 0 | 1.517 s [log](ubuntu-reference.log) |
| `powershell.exe -NoProfile -File integration/tests/test_a2_l03_ps_action_gate.ps1` | PASS, exit 0 | 3.414 s wall [log](native-action.log) |
| `powershell.exe -NoProfile -File integration/tests/test_a2_l04_ps_view_helpers.ps1` | PASS, exit 0 | 3.365 s wall [log](native-view.log) |
| `powershell.exe -NoProfile -File integration/tests/test_worker_view_recovery.ps1` | PASS, exit 0 | 2.564 s wall [log](native-legacy-view.log) |
| Native Git checkout verification with correct and all-zero commit IDs | Correct pin accepted and wrong pin held, exit 0 | [readback](windows-backend.log) |

The independent Python probe runs with `python -X utf8 review-probes.py <pinned checkout>` or `python3 -X utf8 review-probes.py <pinned checkout>`. Its pause fixture now writes an acknowledgement through the candidate's generation-aware function. Both hosts reproduce the expected findings below. Git fixture commits are synthetic. Reference output paths were abbreviated. [Python source](review-probes.py), [Windows output](windows-review-probes.json), [Ubuntu output](ubuntu-review-probes.json)

Both independent native probes run in Windows PowerShell 5.1 using `powershell.exe -NoProfile -File <probe> -Candidate <pinned checkout>`. They extract functions from the pinned script and supply synthetic UIA nodes. They exit zero after recording outcomes. [Prior probe](native-review-probes.ps1), [prior probe output](native-review-probes.json), [text-boundary probe](posted-boundary-probe.ps1), [text-boundary output](posted-boundary-probe.json)

## Retest of the five previous findings

| Cases | Independent result |
| --- | --- |
| R04 | Acknowledgement matches the first observed marker. A second generation shows requested without acknowledgement and retains exact marker bytes. |
| S01 | Non-prose `NEED_MORE_TIME` and `TASK_COMPLETE` both stay unready. The native suite also checks `ERROR` and the positive prose controls. |
| S02 | A blank published continuation holds with empty consumed history. After publishing the repair on the same local-Git ref, the original response yields `LAUNCH_SUCCESSOR` with dispatch deferred. Prepare and Send counters stay zero. |
| S05, S06, O04 | The exact anchored turn is acknowledged. The previously accepted ordinary longer body is rejected in both anchored and unanchored modes. |
| O05 | A substituted owner file under the same IDs fails the durable receipt check after reload. The original action stays prepared and both Prepare and Send counters stay zero. The Windows native action suite also holds a changed file against the saved receipt. |

## Remaining hold

**S01, S05, S06 and O04 share one false text boundary.** `Read-AssistantContent` treats a `Text` node with the literal name `Ask ChatGPT` as a boundary regardless of its position in the message. The same extraction drives final-status eligibility and full posted-body verification.

- User readback used a valid triggering assistant anchor. The fake UIA user body contained three nodes, `Okay, continue working.`, `Ask ChatGPT` and `Discuss the sample only`. Native extraction returned only the first node. `Find-PostedMessage` returned true both with and without the exact anchor. The same harness accepted the exact-body control and rejected a normal longer body without the delimiter.
- Assistant status used a prose-qualified `NEED_MORE_TIME` node followed by literal `Ask ChatGPT` and `The line above was an example`, both within the synthetic assistant body. The scan dropped the remaining body and reported `ready=true`. It had already passed the new prose check on the earlier status.

The fault is at the offline helper boundary. Use structural evidence to distinguish page controls and turn headers from text belonging to the message, or hold when a boundary is ambiguous. Then verify exact posted acknowledgement and final-status behavior with both positive and negative controls. [Pinned extraction code](../../../../../integration/uia_adapter.ps1), [synthetic reproduction](posted-boundary-probe.ps1), [observed values](posted-boundary-probe.json)

## Exact offline dispositions

| Case | Decision | Basis |
| --- | --- | --- |
| A2-R01 | OFFLINE_PASS | Positive exact backend and root checks, distinct route/config and native profile matching mocks. |
| A2-R02 | OFFLINE_PASS | Invalid/duplicate route, wrong backend/root and wrong-profile window negatives hold at the offline boundaries. |
| A2-R03 | OFFLINE_PASS | Stable named Project and case-normalized repo identity, new-job idempotence, exact request ID validation and checkpoint rotation. |
| A2-R04 | OFFLINE_PASS | Journal and publication diagnostic matching, legacy holds and independent marker-generation retest. |
| A2-S01 | HOLD | Non-prose rejection repaired. An in-body delimiter still hides trailing text and marks a non-final status ready. |
| A2-S02 | OFFLINE_PASS | Wrong worker/run/ref and trailer faults hold. Independent real local-Git repair permits reusing the unconsumed response. |
| A2-S03 | OFFLINE_PASS | Verified exact branch locator and receipt preserve entry branch and cap, and malformed locator holds. |
| A2-S04 | OFFLINE_PASS | Durable action and pause checks cover mocked before-prepare/after-prepare/pre-click outcomes with preserved count and draft policy. |
| A2-S05 | HOLD | Exact-anchor and ordinary longer-body tests pass. Delimiter truncation still acknowledges a different same-chat user body. |
| A2-S06 | HOLD | Provisional-ID and lost/duplicate acknowledgement tests pass. The delimiter truncation also returns positive in successor readback. |
| A2-S07 | OFFLINE_PASS | Exact durable initial intent and repeat-launch readback, preserved pre-click record and missing-journal hold. |
| A2-S08 | OFFLINE_PASS | Newer pause generation resists concurrent release, and terminal stops remain immutable. |
| A2-S09 | OFFLINE_PASS | Native action/response/message/route/handle/document checks and substituted bootstrap ID negatives pass. |
| A2-V01 | OFFLINE_PASS | Mock recovery re-observes the exact saved worker with stable account/Project/chat inputs and unchanged count. |
| A2-V02 | OFFLINE_PASS | Mock displaced view reuses the saved worker and rejects multiple accessible views. |
| A2-V03 | OFFLINE_PASS | Native helpers recognize a stable newer completion for the same user turn. Mock recovery returns to normal response consumption. |
| A2-V04 | OFFLINE_PASS | Native consumed, changed-user, changed-count and streaming controls hold. Probe interval and cooldown tests pass. |
| A2-V05 | OFFLINE_PASS | Wrong-project, wrong-profile, ambiguous target and unverified composer controls hold at the mock or helper boundary. |
| A2-V06 | OFFLINE_PASS | Mock advanced worker and native pre-click checks avoid new input and preserve typed draft policy. |
| A2-O01 | OFFLINE_PASS | Inspect, configured reuse, explicit-new selection and initial uncertainty preserve original registration and count. |
| A2-O02 | OFFLINE_PASS | One normally accepted scoped action queues to the same worker before publication-gated handoff. |
| A2-O03 | OFFLINE_PASS | Verified saved input deduplicates same/equivalent ID replay. Conflicting content holds. |
| A2-O04 | HOLD | Advanced observation remains distinct. False exact-input evidence can still reconcile an uncertain owner action through the shared native helper. |
| A2-O05 | OFFLINE_PASS | Independent replaced owner input, existing missing input, mismatched request and wrong anchor negatives preserve the held action. |

**Totals — 20 OFFLINE_PASS and 4 HOLD.** All 24 exact offline cases are listed. A2-G2–G6 remain `NOT_RUN`. Correct the reproduced native boundary and re-review the resulting source pin before installation. Actual Chrome accessibility structure, installed account pairing, desktop/phone sends and cap and capacity trials belong to the later published gates.

A valid local-Git handoff still checks fetched SHA/ref/trailers, matches the run and worker to the response, and persists response, branch and next action together. Read-only status matches the post-adoption diagnostic SHA/ref against persisted run/ref/response. Project rules govern work quality and authority.
