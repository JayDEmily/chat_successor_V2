# ADR 0002 independent A2-G1 review of c605c5f

**Verdict — A2-G1 OFFLINE HOLD.** 20 November 2026 AEDT. The structured transcript parser fixes all five literal-label truncations. A newer conversation article with an unverifiable role can still disappear from the parsed sequence, leaving an older turn actionable.

Reviewer — Codex independent reviewer `g1_reviewer`. [Operative ADR](../../../../../docs/adr/0002-account-bound-resumable-runs.md) · [Exact cases](../../../package/acceptance/cases.csv) · [L02–L05 plan](../../../package/docs/IMPLEMENTATION_PLAN.md) · [Previous hold](../independent-9e64211/REPORT.md) · [Corrective evidence](../corrective-c605c5f/RESULT.md)

## Independent verification

- Source `c605c5fafe4d3cfefe4173f04a53ebf0d1943d59`, tree `7bbf56bf60cf0006782dd6fef300a8d9b0217071`, direct parent `c8a3020d9c3e8bca763be31f81720fe6cfc6a6c2`. Fresh Windows and Ubuntu GitHub clones matched the pin, were clean and passed `git fsck --full`. The published evidence-only tip `da58477c47a715938550271eab5490f3b7d6f75a` has the same integration, plugin and reference kit source.
- Ubuntu `sha256sum --check --strict MANIFEST.sha256` verified 94 of 94 package entries. The archived return matched SHA-256 `8fcb94cd24b954c6f31b37a636fcb346dac1d48c1e7b647713fae664ff6a15c2`. [Manifest output](ubuntu-manifest.log)
- Windows used CPython 3.13.15 and native Windows PowerShell 5.1.26100.9818. Ubuntu under WSL used CPython 3.14.4. All Python runs exited zero with zero failures, errors or skips.

| Command and host | Result | Time and raw output |
| --- | --- | --- |
| Windows `python -X utf8 -m unittest discover -s integration/tests -v` | 113/113 | 27.825 s [integration log](windows-integration.log) |
| Ubuntu `python3 -X utf8 -m unittest discover -s integration/tests -v` | 113/113 | 1.869 s [integration log](ubuntu-integration.log) |
| Windows `python -X utf8 run_offline.py --out <temp>` from kit root | 119/119 | 13.974 s [reference log](windows-reference.log) |
| Ubuntu `python3 -X utf8 run_offline.py --out <temp>` from kit root | 119/119 | 1.332 s [reference log](ubuntu-reference.log) |
| Windows `powershell.exe -NoProfile -File integration/tests/test_a2_l03_ps_action_gate.ps1` | PASS, exit 0 | 3.737 s wall [action log](native-action.log) |
| Windows `powershell.exe -NoProfile -File integration/tests/test_a2_l04_ps_view_helpers.ps1` | PASS, exit 0 | 3.317 s wall [view log](native-view.log) |
| Windows `powershell.exe -NoProfile -File integration/tests/test_worker_view_recovery.ps1` | PASS, exit 0 | 2.544 s wall [legacy view log](native-legacy-view.log) |
| Windows Python backend check using local Git | Correct commit accepted, all-zero commit held, exit 0 | [backend log](windows-backend.log) |

The previous local-Git and private-journal probes reran on both hosts using `python -X utf8 review-probes.py <pinned checkout>` and `python3 -X utf8 review-probes.py <pinned checkout>`, both exit 0. The blank-continuation receipt leaves the response unconsumed and a repaired receipt can proceed. Owner input substitution preserves the prepared action with zero mock dispatch calls. A newly written pause generation remains unacknowledged. Reference output paths were abbreviated. [Python source](review-probes.py), [Windows outcomes](windows-review-probes.json), [Ubuntu outcomes](ubuntu-review-probes.json)

## Native retest and remaining hold

Independent probe command `powershell.exe -NoProfile -File article-boundary-review.ps1 -Candidate <pinned checkout>`, exit 0. It loads the production turn functions and supplies a recursive synthetic accessibility tree. Parent access, descendants and prose recognition use isolated stubs. No adapter mode contacts a browser.

The probe accepts a full exact posted body in anchored and unanchored modes and a genuinely final prose status. All five former delimiters inside longer user bodies are rejected as acknowledgement evidence. All five inside assistant bodies retain the text past the label, leaving the earlier status unready.

One negative still yields positive receipts. Append a newer sibling `article` under the same thread region with a `You said:` heading whose structure lacks the required `sr-only` class and a different user body. The role cannot be verified. `Get-ConversationTurns` silently omits the article, so `Find-PostedMessage` acknowledges the older exact body in anchored and unanchored modes. With the newer unverified article immediately after a verified assistant status, `Read-CurrentTurn` reports that earlier status as ready. This is a directly observed failure to hold when the latest turn cannot be established. Require verified role coverage for the selected conversation articles before acknowledging a post or acting on the latest status. [Pinned source](../../../../../integration/uia_adapter.ps1), [independent probe](article-boundary-review.ps1), [raw results](article-boundary-review.json)

## Exact A2-G1 dispositions

| Case | Decision | Basis |
| --- | --- | --- |
| A2-R01 | OFFLINE_PASS | Exact backend and root accepted, child account binding and profile descriptor verified in tests. |
| A2-R02 | OFFLINE_PASS | Invalid and duplicate route, wrong backend/root and wrong-profile native helper negatives hold. |
| A2-R03 | OFFLINE_PASS | Named Project and case-normalized repo reuse, exact job IDs, repeat stability and branch rotation preserve identity and cap. |
| A2-R04 | OFFLINE_PASS | New marker remains unacknowledged until observed. Legacy status and publication evidence correlate with durable records. |
| A2-S01 | HOLD | In-body labels and non-prose final text now hold. Newer unverified article leaves the previous status ready. |
| A2-S02 | OFFLINE_PASS | Wrong attribution and unpublished or malformed receipts hold. Local Git repair reuses the same unconsumed response. |
| A2-S03 | OFFLINE_PASS | Exact locator and fetched ref and worker receipt precede persisted rotation. Invalid locator holds. |
| A2-S04 | OFFLINE_PASS | Mock pause before dispatch keeps the original prepared action and count. Native action harness checks pre-click controls. |
| A2-S05 | HOLD | Exact positive, wrong anchor and longer-body controls behave correctly. An older body is accepted ahead of a newer unverified article. |
| A2-S06 | HOLD | Provisional IDs and duplicate or lost ACK safeguards pass. Unanchored readback still acknowledges the older user article. |
| A2-S07 | OFFLINE_PASS | Original bootstrap intent survives loss and pre-click hold. Missing journal with prior activity holds. |
| A2-S08 | OFFLINE_PASS | Newer pause generation resists release and terminal states preserve reason and count. |
| A2-S09 | OFFLINE_PASS | Exact receipt and document gate holds on mismatched target, action, message, source, route or bootstrap ID. |
| A2-V01 | OFFLINE_PASS | Exact saved view is restored with unchanged worker identity and count in mocked recovery. |
| A2-V02 | OFFLINE_PASS | Displaced view restoration holds on duplicate accessible matches and retains the saved chat. |
| A2-V03 | OFFLINE_PASS | Stable, newer, same-user unconsumed completion qualifies in the native helper. Mock resumes normal observation. |
| A2-V04 | OFFLINE_PASS | Consumed, changed-user, changed-count and streaming states hold. Threshold and cooldown tests pass. |
| A2-V05 | OFFLINE_PASS | Wrong session profile and Project, unverified composer and ambiguous target hold in native helper or mock. |
| A2-V06 | OFFLINE_PASS | Advanced worker evidence suppresses further input and preserves the draft in the mocked action path. |
| A2-O01 | OFFLINE_PASS | Inspect, configured reuse, explicit-new selection and uncertain first attempt preserve journal and registration. |
| A2-O02 | OFFLINE_PASS | Correct scope and empty composer queue one same-chat input. Handoff requires its published Git receipt. |
| A2-O03 | OFFLINE_PASS | Same or equivalent request ID deduplicates on verified input. Conflicting scope holds. |
| A2-O04 | HOLD | Advanced observation remains distinct. The unverified-article case permits false exact-input evidence during reconciliation. |
| A2-O05 | OFFLINE_PASS | Missing, replaced or wrongly anchored owner context preserves the prepared action and blocks dispatch. |

**Totals — 20 OFFLINE_PASS and 4 HOLD.** A2-G2 is ineligible on this pin. A2-G2–G6 remain `NOT_RUN`. Fix the shared latest-turn verification and obtain an independent decision on the resulting source pin. The installed profile, actual accessibility structure, real Send, phone and capacity checks retain their published later gates.

Valid Git processing verifies full fetched SHA/ref and run/worker attribution to the current response. The saved journal records the response, effective ref and next action at adoption. Read-only status correlates the subsequent private SHA/ref diagnostic with that journaled response. Project rules determine work quality and authority.
