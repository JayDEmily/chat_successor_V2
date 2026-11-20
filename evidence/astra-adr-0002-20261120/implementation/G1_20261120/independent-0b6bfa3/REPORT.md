# ADR 0002 independent A2-G1 review of 0b6bfa3

**Verdict — A2-G1 OFFLINE ACCEPT.** 20 November 2026 AEDT. All 24 published offline cases pass at the source pin below. A2-G2 is eligible for its installed Windows and account-route checks under the standing authority. A2-G2–G6 remain `NOT_RUN`.

Reviewer — Codex independent reviewer `g1_reviewer`. [Operative ADR](../../../../../docs/adr/0002-account-bound-resumable-runs.md) · [Exact cases](../../../package/acceptance/cases.csv) · [Acceptance gates](../../../package/acceptance/GATES.md) · [Previous hold](../independent-c605c5f/REPORT.md) · [Corrective evidence](../corrective-0b6bfa3/RESULT.md)

## Pinned source and verification

- Source `0b6bfa3e935e713fe2f36afd8da79c2befab9a42`, tree `668194fff116591bb88958276994f32025f24caf`, direct parent `0ac9fe6a0ee7575894dad0eaf8a30997a811fcd2`. Fresh Windows and Ubuntu GitHub clones matched those IDs, had empty status and passed `git fsck --full`. Intake tip `c747e92ccb9cf3d65c045876fd4649f2e2353ef4` has the tested integration, plugin and reference kit source.
- Ubuntu `sha256sum --check --strict MANIFEST.sha256` verified 94 of 94 package entries. The original archive matched SHA-256 `8fcb94cd24b954c6f31b37a636fcb346dac1d48c1e7b647713fae664ff6a15c2`. [Manifest output](ubuntu-manifest.log)
- Windows used CPython 3.13.15 and native Windows PowerShell 5.1.26100.9818. Ubuntu over WSL used CPython 3.14.4. All four Python runs exited zero with zero failures, errors or skips. Integration logs list the actual 113 test names on each host.

| Host and exact command | Result | Time and evidence |
| --- | --- | --- |
| Windows `python -X utf8 -m unittest discover -s integration/tests -v` | 113/113 | 28.156 s [log](windows-integration.log) |
| Ubuntu `python3 -X utf8 -m unittest discover -s integration/tests -v` | 113/113 | 1.924 s [log](ubuntu-integration.log) |
| Windows `python -X utf8 run_offline.py --out <temp>`, reference kit cwd | 119/119 | 13.968 s [log](windows-reference.log) |
| Ubuntu `python3 -X utf8 run_offline.py --out <temp>`, reference kit cwd | 119/119 | 1.332 s [log](ubuntu-reference.log) |
| `powershell.exe -NoProfile -File integration/tests/test_a2_l03_ps_action_gate.ps1` | PASS, exit 0 | 3.742 s wall [log](native-action.log) |
| `powershell.exe -NoProfile -File integration/tests/test_a2_l04_ps_view_helpers.ps1` | PASS, exit 0 | 3.174 s wall [log](native-view.log) |
| `powershell.exe -NoProfile -File integration/tests/test_worker_view_recovery.ps1` | PASS, exit 0 | 2.398 s wall [log](native-legacy-view.log) |
| Windows Git-backed Python verification of exact and all-zero revision | Exact accepted and wrong revision held, exit 0 | [readback](windows-backend.log) |

Both independent local-Git and journal probes also exited zero, with `python -X utf8 review-probes.py <pinned checkout>` and `python3 -X utf8 review-probes.py <pinned checkout>`. The repaired publication remains eligible on its original unconsumed response. A changed owner input preserves the prepared action with zero mock dispatch. A fresh pause generation stays unacknowledged and retains its marker. The reference logs abbreviate temporary paths. [Python probe](review-probes.py), [Windows results](windows-review-probes.json), [Ubuntu results](ubuntu-review-probes.json)

## Independent transcript retest

`powershell.exe -NoProfile -File article-completeness-review.ps1 -Candidate <pinned checkout>` exited zero on native Windows. The probe loads the production functions and supplies synthetic accessibility descendants, parents and prose evidence.

- The previously reproduced trailing article with an unverifiable role now blocks anchored and unanchored acknowledgement. It holds an earlier assistant status when the transcript is idle.
- Duplicate same-role headings with distinct runtime IDs, conflicting role headings and multiple transcript regions all fail closed. Verified streaming and an incomplete streaming transcript both wait.
- Exact whole-body readbacks with and without an anchor and a genuinely final prose status pass. All five previous literal labels stay inside the body. The longer user messages are rejected and the earlier status in each longer assistant message stays unready.

These probes resolve S01, S05, S06 and O04 from the last hold. [Native probe source](article-completeness-review.ps1), [raw native outcomes](article-completeness-review.json)

## Exact A2-G1 dispositions

| Case | Decision | Evidence |
| --- | --- | --- |
| A2-R01 | OFFLINE_PASS | Exact backend and root, distinct route/config and child-profile selection verified at offline boundaries. |
| A2-R02 | OFFLINE_PASS | Invalid and duplicate route, wrong backend/root and wrong native window profile all hold. |
| A2-R03 | OFFLINE_PASS | Project rename and case-normalized repo reuse, validated job IDs, repeat identity and checkpoint rotation retain cap. |
| A2-R04 | OFFLINE_PASS | Current generation acknowledgement, legacy holds and read-only publication diagnostics match durable evidence. |
| A2-S01 | OFFLINE_PASS | Transcript requires one verified role per article. Literal text, non-prose and streaming cases stay unready. Reference parser and cap and finish controls pass. |
| A2-S02 | OFFLINE_PASS | Invalid attribution and malformed or unpublished receipts hold before consuming. A repaired local-Git receipt reuses the same response. |
| A2-S03 | OFFLINE_PASS | Verified locator and exact fetched ref precede rotation with original branch, run and cap retained. |
| A2-S04 | OFFLINE_PASS | Prepared action and count survive modeled pause stages. Native gate checks before typing and before Invoke. |
| A2-S05 | OFFLINE_PASS | Exact same-chat anchor and whole latest posted body pass. Older, longer and unverified-trailing-turn evidence hold. |
| A2-S06 | OFFLINE_PASS | Provisional ID, missing or duplicate receipt and unverified later article hold. Exact saved successor readback is counted once in the mock. |
| A2-S07 | OFFLINE_PASS | Original bootstrap intent and read-only reconciliation survive lost acknowledgement and pre-click pause. Missing journal with earlier activity holds. |
| A2-S08 | OFFLINE_PASS | Newer pause generation resists release. Finished and capped journals retain reason and count. |
| A2-S09 | OFFLINE_PASS | Native target/action checks hold on wrong message, source, account route, prepared window or document and substituted bootstrap ID. |
| A2-V01 | OFFLINE_PASS | Mock recovers the exact saved worker and Project without changing count. |
| A2-V02 | OFFLINE_PASS | Mock displaced view restoration retains the saved chat and holds on duplicate accessible views. |
| A2-V03 | OFFLINE_PASS | Stable, newer, unconsumed completion for the same user turn qualifies in the native helper. Mock returns to normal observation. |
| A2-V04 | OFFLINE_PASS | Consumed, streaming and changed-user or changed-count inputs hold. Threshold and cooldown tests pass. |
| A2-V05 | OFFLINE_PASS | Wrong Project/profile, ambiguous target and unverified composer hold at native-helper or mock boundaries. |
| A2-V06 | OFFLINE_PASS | Advanced worker observation suppresses additional input and the native gate preserves the draft before click. |
| A2-O01 | OFFLINE_PASS | Inspection, explicit new, configured reuse and first intent uncertainty retain registered worker and cap. |
| A2-O02 | OFFLINE_PASS | Correct held scope and empty composer queue one action to the same saved worker before publication-gated handoff. |
| A2-O03 | OFFLINE_PASS | Same and equivalent request replays deduplicate only on verified owner input. Conflicting scope holds. |
| A2-O04 | OFFLINE_PASS | Advanced observation remains distinct from delivery. Reconciliation requires exact anchored whole-user-body evidence with verified article coverage. |
| A2-O05 | OFFLINE_PASS | Changed, absent or wrongly anchored private owner input preserves the prepared action and blocks dispatch. |

**Totals — 24 OFFLINE_PASS.** The installed Windows G2 checks must verify actual account/profile pairing, Chrome accessibility structure and no-Send preflight on this pin. The later paired-run, Shoco phone, capacity and closeout checks retain their own gates.

Successful Git processing fetches and checks the full SHA/ref, verifies publication trailers or fixture attribution and binds it to the current run, worker and response. The saved journal records the consumed response, effective ref and resulting action together. Read-only status correlates the later private SHA/ref adoption diagnostic with that anchored journal. The Project's procedure determines work quality and authority.
