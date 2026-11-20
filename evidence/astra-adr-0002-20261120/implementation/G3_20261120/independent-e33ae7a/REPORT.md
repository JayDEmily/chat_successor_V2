# A2-G3 / A2-L07 independent exact-source adversarial review — OFFLINE HOLD

**Review date:** 20 November 2026 (Australia/Melbourne)  
**Repository:** JayDEmily/chat_successor  
**Reviewed immutable source SHA:** e33ae7ad49e3510bf3021c552184cbb9d0e05758  
**Verified parent:** 34c8b790492f0e07d016f869350cf65aa46001da  
**Implementation ref at assignment:** codex/chat-succession-finish  
**Later project checkpoint (context only):** beacfae4790c2ec4f390e90ad0bd214fe6a1ef05  
**Independent review publication branch:** review/a2-g3-independent-e33ae7a-20261120  
**Verdict:** **OFFLINE HOLD — HIGH-severity unresolved latest-turn/Send-receipt safety defect.**

## Scope, authority and isolation

Read the pinned AGENTS.md, repository README and progress, accepted ADR 0002, A2-G3 acceptance gates, original L07 two-run acceptance leaf and G3_VIRTUALIZED_REVIEW_COMMISSION.md. Reviewed the e33ae7a source and test changes against parent 34c8b79 independently; prior implementation claims were not relied on for the verdict.

Remote Desktop Commander identity: authenticated shokopa66@gmail.com; one online device DESKTOP-I188O30 (b8195d8a-f2fd-4c65-8c44-975f2a1f7cdd); executing Windows identity DESKTOP-I188O30\james. Windows PowerShell 5.1.26100.9818; Git for Windows 2.55.0; CPython Windows 3.13.15; Ubuntu/WSL Python 3.14.4 and Git 2.53.0. Work was confined to a newly cloned, detached source at:

C:\Users\james\AppData\Local\Temp\a2g3-independent-ikXafDfS\repo

Sibling review scripts and logs are outside the repository checkout, in the temporary parent directory. The implementation worker's working tree was not used. No installed controller restart, ChatGPT browser Send, successor worker, live run-journal access or pause-marker change took place.

Fresh independent checkout command, executed via Ubuntu/WSL:

~~~bash
d=$(mktemp -d /mnt/c/Users/james/AppData/Local/Temp/a2g3-independent-XXXXXXXX)
git clone -q --filter=blob:none --no-checkout https://github.com/JayDEmily/chat_successor.git "$d/repo"
cd "$d/repo"
git checkout --detach -q e33ae7ad49e3510bf3021c552184cbb9d0e05758
git rev-parse HEAD
git rev-parse HEAD^
git status --porcelain
git fsck --full
~~~

Observed HEAD and parent match the two specified full SHAs. Initial and post-test working trees were clean, git diff --exit-code and git fsck --full succeeded. The only changed source file in the candidate is integration/uia_adapter.ps1 (+106/-11), alongside integration/tests/test_a2_l03_ps_action_gate.ps1 (+15) and new integration/tests/test_a2_g3_ps_virtualized_turns.ps1 (+116), and published evidence/documentation.

## Independent tests: actual commands and results

From the detached checkout (not the installed backend):

| Environment / command | Result | Local evidence |
| --- | --- | --- |
| Windows: C:\Program Files\Python313\python.exe -B -m unittest discover -s integration/tests -v | **PASS, 114/114**, zero reported skips; 29.636 s | ../logs/windows-integration.log |
| Ubuntu: python3 -B -m unittest discover -s integration/tests -v | **PASS, 114/114**, zero reported skips; 1.516 s | ../logs/ubuntu-integration.log |
| Windows, with PYTHONUTF8=1 and cwd astra/2026-11-17/unpacked/chat_succession_test_kit_20261117: C:\Program Files\Python313\python.exe -B -m unittest discover -s tests -v | **PASS, 119/119**; 14.369 s | ../logs/windows-reference-utf8.log |
| Ubuntu, cwd at same reference kit: python3 -B -m unittest discover -s tests -v | **PASS, 119/119**; 0.957 s | ../logs/ubuntu-reference.log |
| Native Windows: powershell.exe -NoProfile -ExecutionPolicy Bypass -File integration/tests/test_a2_l03_ps_action_gate.ps1 | **PASS, exit 0** | ../logs/test_a2_l03_ps_action_gate.ps1.log |
| Native Windows: same command for integration/tests/test_a2_l04_ps_view_helpers.ps1 | **PASS, exit 0** | ../logs/test_a2_l04_ps_view_helpers.ps1.log |
| Native Windows: same command for integration/tests/test_worker_view_recovery.ps1 | **PASS, exit 0** | ../logs/test_worker_view_recovery.ps1.log |
| Native Windows: same command for integration/tests/test_a2_g3_ps_virtualized_turns.ps1 | **PASS, exit 0** | ../logs/test_a2_g3_ps_virtualized_turns.ps1.log |
| Native Windows: independent review/REPRO.ps1 using pinned source and fixture helpers | **Reproduces all unsafe assertions**, exit 0 | ../logs/repro-portable.log |

An initial Windows Python integration invocation was interrupted by the outer PowerShell ErrorActionPreference=Stop interpreting unittest -v stderr as a terminating NativeCommandError; its controlled rerun completed 114/114. The first Windows reference run (without PYTHONUTF8) executed 58 tests but failed to import test_tables with UnicodeDecodeError from the host's default cp1252 encoding. Setting PYTHONUTF8=1 and rerunning the unchanged suite yielded 119/119. These are execution/environment limitations, not silent passes or source-code fixes. The failed first reference output remains ../logs/windows-reference.log.

Representative SHA-256 values of review-local logs (full raw tests retained outside the checkout on the connected machine):

- windows-integration.log: 6d73894c7bb7a666dece61eb3f2737bf0a602d758ebb93a1ccfcb79f1bb36902
- ubuntu-integration.log: 94b8cd8d1080cb0981f6e12188c25b76efc21f03745ba95e41a1a301e948f473
- windows-reference-utf8.log: 8288d30dba7d2479200b3606117779c53e27eb4dca87e021b99d9cbb437759db
- ubuntu-reference.log: 42acdda0c96cbba9848c595bfb6685d550db7ea7ff769cc33f581f9ac1876005
- adversarial.log: 350b475fc4438140ccdba90126d276ac826c0cef3c93a629a44c4c335a74b4ce

## F1 — HIGH: opaque newer transcript sibling does not invalidate older article (reproduced)

**Applicable requirement:** The G3 review commission expressly requires testing an older valid article-based assistant completion with a newer, unclassified transcript sibling. A2-G3, S01/S05/S06 and V03 require positive latest-response and posted-message attribution; an unknown newer element cannot be presumed non-message. Invalid or ambiguous observation must not qualify a Send acknowledgement or stale-reload predicate.

**Exact deficient implementation:**

- integration/uia_adapter.ps1:337–363, especially 347–362: when any article exists, Get-ConversationTurns scans non-article descendants only for a heading with a recognised application label **and** sr-only class, or for a body group with Renderer-* / bg-user-message. An opaque group with unrecognised class, or a changed-class heading, is ignored. The older verified articles are still returned as the full apparent conversation.
- integration/uia_adapter.ps1:395–410: Find-PostedMessage consequently accepts an older exact user article as the latest posted turn and can return true.
- integration/uia_adapter.ps1:520–567: Read-CurrentTurn consequently issues ready=true with the older assistant response ID and latest user digest. Its virtualized fail-closed logic only activates when Get-ConversationTurns actually returns virtualized=true.

**Independent reproduction:** The source-pinned native [REPRO.ps1](REPRO.ps1) dot-sources the existing native action fixture helpers and adds **synthetic** newer transcript siblings after verified older articles. It invokes the actual functions extracted from the pinned production source. Run on Windows from a checkout containing this review folder:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File evidence/astra-adr-0002-20261120/implementation/G3_20261120/independent-e33ae7a/REPRO.ps1
~~~

Reproduced output:

~~~text
PASS: Windows PowerShell action, structurally bounded full turns, prose status and owner receipt checks.
REPRO_STALE_STATUS_READY=TRUE; CHANGED_HEADING=False; RESPONSE_REUSED=TRUE; USER_ANCHOR_REUSED=TRUE
REPRO_STALE_STATUS_READY=TRUE; CHANGED_HEADING=True; RESPONSE_REUSED=TRUE; USER_ANCHOR_REUSED=TRUE
REPRO_FALSE_POSTED_ACK=TRUE; NEWER_OPAQUE_SIBLING_IGNORED=TRUE
~~~

- **F1a:** an unclassified group after a valid assistant article leaves the older completion actionable, with its prior response ID and latest-user digest unchanged.
- **F1b:** the result persists if that newer row has a ChatGPT said: heading whose accessibility class changed from sr-only to a different class.
- **F1c:** the same unclassified newer sibling leaves Find-PostedMessage returning true for an older article-based exact user turn after the specified assistant anchor.

These tests establish a **permitted input shape and unsafe decision**, not that the present production Chrome UI necessarily renders that precise unknown class in every session. Safety explicitly requires fail-closed behaviour when message identity cannot be verified. The worker's existing tests cover recognised-class mixed rows but do not cover this unclassified sibling.

**Required correction:** In mixed article/non-article layouts, verify *complete* transcript sibling membership and ordering within a known message/controls hierarchy. Unknown or changed-accessibility children that could be turns must invalidate all actionable article completion, user-anchor and posted-message predicates unless they can positively be excluded as non-message chrome. Add F1a/F1b/F1c to native source-pinned tests. Re-review a new immutable implementation commit. Do not merely add another renderer class guess or silently accept unknown groups.

## Other independently checked safety dimensions

- **Pure virtualized structure:** new native suite exercises direct paired user/assistant headings, duplicated/missing/nested headings, changed user/assistant body classes, orphaned renderer, multiple transcript regions/layouts, streaming Stop control and rejected virtualized posted-message receipts. All assertions pass on this source. Pure virtualized Read-CurrentTurn remains non-actionable: ready=false, method=UIA_VIRTUALIZED_UNQUALIFIED, response_id=null, no absolute counts or latest_user_digest. This is a narrow safety positive, not an affirmative latest-turn qualification.
- **Article path and action boundaries:** native action and view suites pass exact anchored user body, literal role-like text inside body, prose-only terminal status, no-status/streaming holds, wrong/duplicated article role heading, owner scope substitution and account/action receipt guards. The independent F1 probe shows a separate mixed-layout failure despite these passes.
- **Durable absolute identity:** Read-ConversationContent produces an application-local value of the form uia-turn-[visible ordinal]-[20 hex characters of visible text SHA-256]. Article GetRuntimeId and heading GetRuntimeId in Get-ConversationRole identify accessibility elements, not server-issued persistent ChatGPT message IDs. The G3 metadata investigation published after the candidate reports empty AutomationId/ItemType/ItemStatus/HelpText and no exposed absolute position on the four checked virtualized nodes. This earlier observation was reviewed as evidence **but not rerun on the live browser**. Thus no source-qualified durable absolute identity is established for virtualized turns; one must not infer one from UIA runtime IDs, visible text hashes or visible row counts. This is a separate unfulfilled positive gate, not an independent claim that all ChatGPT APIs lack message IDs.

## Verdict, limitations, next authorised action

**OFFLINE HOLD** on exact source e33ae7ad49e3510bf3021c552184cbb9d0e05758 due to F1a–F1c, a single high-severity root defect with stale-response, anchor and false-acknowledgement consequences. Baseline test passes do not override a reproduced unsafe case.

This is an offline synthetic UIA review. No live Windows Chrome message was posted; no live user/assistant transcript, browser interaction or private journal was read for this review. Previously recorded virtualized UIA node metadata and saved-view readback are provenance from the implementation work, not independently repeated observations. The commissioned **source review is decided HOLD**; A2-G3 live D01–D03, positive V03 stale reload, S05/S06 posted-turn confirmation and concurrent two-run acceptance remain **NOT_RUN**. A2-G4–G6 remain open. An OFFLINE ACCEPT, even if later achieved, would not close those tests.

**Next permitted action:** implementation owner correct the mixed transcript boundary on the implementation branch and publish a *new* pinned candidate; then commission independent rerun of this proof, preserved 114/119 suites on both hosts and all native suites. Only after affirmative latest-turn/posted-message identity and the separate authorised live gate can deployment/Send be considered. Keep installed Windows backend at its recorded 5c86ad6 pin; do not resume Rowing or SolidWorks, touch their pause markers or amend private run journals. This review only adds this report and a synthetic reproducer to its own independent branch, with no source edits or merge.
