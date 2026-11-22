# Progress

## Active branch — MCP-native governance (22 November 2026)

- Owner selected extension-free MCP registration/completion direction and isolated public branch. Active authority: [AGENTS.md](AGENTS.md), [ADR 0003](docs/adr/0003-mcp-native-succession.md), [PLANS.md](PLANS.md). Governance-only checkpoint; no runtime, live tests or installation changes. See [governance review](docs/governance-review-20261122.md).
- **M01 discovery completed:** [feasibility / direct observations](docs/mcp-native/M01-feasibility.md). Private tunnel/reference pattern reviewed and native Windows UIA New chat/Projects/Edit patterns observed. Exact account/Project identity and saved route not established; no Send, resource creation or legacy migration.
- **M02 contract frozen:** [identity, threat model, durable admission, evidence gates and S01–S13 synthetic cases](docs/mcp-native/M02-contract.md). Reuse existing reference Controller; no direct callback dispatch, no fabricated native message identity. No live qualification claimed.
- **M03 worker-tested candidate:** `80688e4620cbddb4b53317ee7dd48434a9c8dd6b`; [fresh-checkout evidence](docs/mcp-native/M03-results.md). Exactly two new source/test files, 21/21 synthetic tests and 119/119 original reference tests passed, plus 31-turn stress trace. No native qualification.
- **Next: independent M03 review** [issue #2](https://github.com/JayDEmily/chat_successor_V2/issues/2), exact source pin. Reviewer not yet acknowledged; worker must not self-approve. M04 held pending separate scoped live-resource/native-call authority and required review; no new services, credentials, plugin, tunnel or Sends.
- Public legacy PR #1 passed four hosted offline jobs on `915fa802a1522e9a48eb57558b11db6e9be69c6e`; it remains unmerged. Existing held L12 action and other projects are untouched.

## Historical ledger (legacy branch; not active assignments)

The [Shoko Yumi execution plan](https://github.com/JayDEmily/chat_successor_V2/blob/820aa20c6643c0ed30177459a685a4a6ee56de79/docs/astra-succession/adr-0002/PROJECT_MANAGEMENT.md) defines the scope and acceptance order. L11 Cat/Dog finished with assisted read-only receipt recovery; L12 Bird/Pig is next.

## Lean ADR 0002 L11 — assisted Cat/Dog completion verified (21 November 2026)

- The installed Shoko backend was repinned to \`36b17092aa5fef09b5ac3747c03e5661be23559c\` with matching route/config rollback. The [existing independent owner re-entry review](evidence/astra-adr-0002-20261120/implementation/G3_20261120/LEAN_L11_REENTRY_REVIEW.md) is now published. The previously registered worker remained the same; no new fixture run was created.
- The original Cat/Dog run \`ae039421dbcc3f45bb4ae1f2\` published [opening commit \`e3d2aa4\`](https://github.com/JayDEmily/chat-succession-cat-dog-pair/commit/e3d2aa48cb991bbe340b5477c66f9025994dbf67), then one verified successor published [completion \`66b80b5\`](https://github.com/JayDEmily/chat-succession-cat-dog-pair/commit/66b80b5c3292338bd941f842158fffdcbf7b8cf9) on \`codex/lean-shoko-cat-dog-20261121\`. GitHub commit trailers match the run and distinct workers; remote branch readback matches \`66b80b5\`.
- Native controller evidence at \`2026-11-21T10:32:37Z\` verified the final publication and recorded \`STOP_FINISHED\`. Its saved state records two unique workers of cap three, \`halted=programme_finished\` and no pending action. Earlier receipts required scoped manual scroll/refresh and read-only reconciliation. This passes the **assisted** Cat/Dog end-to-end result only; unattended provisional-to-saved convergence remains unverified. Do not repeat those Sends.
- **Next: L12 Bird/Pig** under the published LEAN-G2 plan: a separate disposable run, cap two, with eligible work still remaining at \`STOP_CAP\`, followed by same-chat continuation. Preserve current installed-run identity and previously paused Rowing/SolidWorks runs. Astra's diagnostic proposal remains unadopted pending native verification.

## Astra L11 external receipt review received (21 November 2026)

- Received Astra's original offline review for L11. The [verbatim REVIEW.md](evidence/astra-adr-0002-20261120/implementation/G3_20261120/astra-l11-receipt-review-20261121/REVIEW.md), [test report](evidence/astra-adr-0002-20261120/implementation/G3_20261120/astra-l11-receipt-review-20261121/TEST_REPORT.md), proposed patch, and [complete original tarball](evidence/astra-adr-0002-20261120/implementation/G3_20261120/astra-l11-receipt-review-20261121/astra-l11-receipt-review.tar.gz) are recorded alongside existing L11 evidence. Tarball SHA-256: `4dd69cd3fe1fb6a09683ccaff2f79f45c305c9d24c3bf2ad44bda81d7d2fde28`; the archive's 78 per-file checks passed at intake.
- Astra reports 126 synthetic Python integration tests and 22 headless DOM tests passing on its candidate; Windows PowerShell/UIA and live acceptance were not run by Astra. This is external advice, **not accepted implementation or a gate pass**. No proposed patch or runtime change was applied. The existing L11 hold and project acceptance requirements remain in force.

## Lean ADR 0002 L11 — Worker-window sizing and saved-ID regression (21 November 2026)

- Candidate `23c66570a4bfd3c08158cf5c771b40e354c535d1` uses Windows `WindowPattern` to maximize newly opened worker windows after verifying their Project and profile. On initial candidate `808257175b235967964ad48a31fed843521623c9`, independent review found a window provider could resize and then throw, leaving preparation with the pre-resize address. The correction rereads the destination on the next ordinary poll after every resize attempt. [Microsoft window-state documentation](https://learn.microsoft.com/en-us/dotnet/api/system.windows.automation.windowpattern.setwindowvisualstate)
- The new preparation and missing-view recovery regressions failed on the previous adapter and passed on the candidate. All 118 Windows integration cases, 119 reference cases, six native PowerShell suites and eight headless Chrome checks passed. The saved-ID regression held while either rendered ID was provisional on a saved URL, then accepted the same exact post once both matched. The native receipt check held an unqualified reader sample on the saved URL.
- Independent review accepted `23c6657` offline after reproducing and verifying the resize-failure correction. The report records the inherited window acquisition and cleanup limits. [Independent review](evidence/astra-adr-0002-20261120/implementation/G3_20261120/LEAN_L11_WINDOW_REVIEW.md)
- Both candidates passed live `Prepare -Preflight` in Shoko Chrome. Each temporary window reported `Normal` before sizing and `Maximized` at composer lookup, showed an empty composer, and closed. The original run, launcher and route files matched byte-for-byte. These were direct candidate checks. The installed route still points at `9f6c13a`.
- The spontaneous transition on a fresh live Send remains unverified. The original Cat/Dog worker still reports `ERROR` at 1/3 with an empty pending slot. The next L11 action is the owner's recovery decision for that registered worker.

## Lean ADR 0002 L11 — Original Cat/Dog Send reconciled, worker held (21 November 2026)

- Read-only inspection verified the one posted user message in the original saved Shoko chat. Its full 1,659-character body matched the preserved intent’s SHA-256 digest. Reloading the saved view restored its app-rendered conversation ID. The existing reader then included the ellipsis and “Show more” or the “Show less” label in the posted text.
- The scoped Chrome reader correction extracts the complete prompt in both display states and holds when the controls or text differ from the verified layout. Six headless Chrome checks passed, including a completed first post, an anchored continuation and a provisional-ID hold. The 118 Windows integration cases, 119 reference cases and six native PowerShell suites passed. The integration rerun removed an inherited Git override from the test process after ten disposable repository setups failed. [Reader correction](https://github.com/JayDEmily/chat_successor/commit/6df0b93a19264dd195a08d5872a27e22a86beb49)
- The existing Shoko extension loaded that script with the same Project scope and a private copy of the previous script for rollback. The installed `9f6c13a2f0300bdcc7e9f783bfb6bf293c58bbf9` backend verified the exact receipt and read the completed reply twice. Its normal bootstrap reconciliation registered the original saved chat as worker 1/3. The original intent stayed byte-identical.
- The worker had already reported `CHAT_STATUS: ERROR` because its controller journal was unavailable during its reply. The controller recorded `HOLD` after two `Observe` calls, with an empty pending-action slot. Reconciliation made zero Sends and opened zero successors. The Cat/Dog fixture remains at its empty-story seed `4c7a2fd5a4e70704d3a38adefbcad5ae6d3dc37a`. [Fixture tip](https://github.com/JayDEmily/chat-succession-cat-dog-pair/tree/4c7a2fd5a4e70704d3a38adefbcad5ae6d3dc37a)
- **Next:** surface the worker’s error for an owner decision on recovering the registered worker. L11’s two story commits, one successor and `STOP_FINISHED` at 2/3 remain pending.

## Lean ADR 0002 L11 — Cat/Dog initial Send held (21 November 2026)

- The installed Shoko wrapper at `9f6c13a2f0300bdcc7e9f783bfb6bf293c58bbf9` verified a fresh run slot and attempted one initial Send to the Cat/Dog fixture, with cap three. It retained its original intent when the exact posted-message receipt timed out.
- The existing read-only reconciliation verified a saved chat in the exact Shoko Project. The Chrome reader first reported the saved view offscreen. One scoped scroll to the bottom produced an unqualified read and the exact receipt still held. The original intent matched byte-for-byte and the controller journal remained absent. No repeat Send or controller start occurred.
- The published fixture remains at its empty-story seed `4c7a2fd5a4e70704d3a38adefbcad5ae6d3dc37a`. Useful story commits, successor and terminal finish are pending. On resume, inspect the original saved view for the unqualified receipt and use the existing reconciliation path when the exact evidence is available.

## Lean ADR 0002 L10d — Shoko no-Send safeguards (21 November 2026)

- Installed Shoko pin `9f6c13a2f0300bdcc7e9f783bfb6bf293c58bbf9` held on the synthetic wrong-profile identity, duplicate saved views, an ordinary draft and a draft equal to the live placeholder. Both drafts stayed exact through the installed checks. Only the diagnostic duplicate and the verified test drafts were removed. All 145 run and lock files matched.
- Live attachment setup is `NOT_RUN`. The existing browser connector rejected local file selection, leaving the owned composer blank. The installed attachment guard passed its regression and the unchanged native detector has prior [attachment-only live evidence](evidence/astra-l07-20261118-a/attempt4.json). No full V05 pass is claimed.
- Next is L11, launch the published Cat/Dog fixture once through the installed Shoko wrapper with cap three.

## Lean ADR 0002 L10c — Installed Shoko saved view restored (21 November 2026)

- On installed Shoko pin `9f6c13a2f0300bdcc7e9f783bfb6bf293c58bbf9`, one guarded close removed only the owned disposable window. Observe reported the saved view missing. The ordinary installed recovery reopened it in one Shoko window. The complete reply, both causal IDs and saved identity matched the pre-close observations.
- All 145 run and lock files, including both original pause markers, matched before and after. The other Chrome windows survived. The recovery performed no Send and created no journal.
- Next is L10d, the selected-route no-Send unsafe-view checks.

## Lean ADR 0002 L10b — Installed Shoko preflight passed (21 November 2026)

- The installed Shoko wrapper at `2c2c5f7` held on an empty composer. Native readback showed the same verified placeholder tree with a duplicate label clipped at 15 characters. The earlier empty view clipped it at 52. The reviewed `9f6c13a2f0300bdcc7e9f783bfb6bf293c58bbf9` candidate accepts an exact ellipsized prefix while retaining the existing tree, draft and attachment gates. All 118 Windows integration tests and six native PowerShell suites passed.
- The Shoko wrapper now selects `9f6c13a`. Its previous route and wrapper were retained under `pre-lean-9f6c13a`. The original rollback remains available.
- The authenticated Shoko connector ran the installed `--check` and returned `preflight_passed` at the exact Project and Cat/Dog fixture tip `4c7a2fd5a4e70704d3a38adefbcad5ae6d3dc37a`. The fresh branch starts from the empty story seed and names its own publication ref. All 145 native run and lock files matched before and after. [Cat/Dog fixture](https://github.com/JayDEmily/chat-succession-cat-dog-pair/tree/4c7a2fd5a4e70704d3a38adefbcad5ae6d3dc37a)
- Next is L10c, restore the completed disposable saved view through the installed reader.

## Lean ADR 0002 L10a — Shoko installation pinned (21 November 2026)

- The canonical Shoko launcher and route now select the clean published backend `2c2c5f7c06f64b54441de19cfb6cd176bca1c576`. Its installed entry and backend binding were verified on Windows. The James Student launcher line and route still select `5c86ad6d735b4c0626c49aedfdb93aeb95e6199b`.
- There were no active native controllers. All run files matched before and after staging, including the original pause markers and legacy pending state. The versioned rollback pair `start-project.pre-lean-2c2c5f7.cmd` and `account_routes.pre-lean-2c2c5f7.json` match the previous installation byte-for-byte. The previous backend checkout remains available.
- Next is L10b, verify the installed Shoko route and exact Cat/Dog fixture ref with `--check` before any worker starts.

## Lean ADR 0002 L09 — Automatic stale recovery disabled (21 November 2026)

- Candidate `2c2c5f7c06f64b54441de19cfb6cd176bca1c576` holds after 120 seconds of unchanged verified progress and includes the saved-chat link. Automatic observation opens a window only for missing-view recovery. Verified owner re-entry advancement returns observation-only and leaves the original draft intact. An explicit re-entry still verifies a fresh view before treating a worker as idle.
- The old code failed the stall and completed-advancement regressions. All 118 Windows integration cases, 119 reference cases, and six native PowerShell suites passed after the change. The independent reviewer accepted the identical runtime files at `abae7d9`. Source inspection also identified an inherited window-ownership race if a manual window opens in the same profile during the launcher’s acquisition. The L09 checks made no live browser action.
- Next is L10a, stage the pinned Shoko installation with a compatible rollback.

## Shoko Yumi iPhone no-Send preflight — 21 November 2026

- The phone's Cat/Dog request used `JayDEmily/chat-succession-cat-dog-pair@main` with a cap of three in the Shoko Yumi Qualification Project. The installed launcher returned `launch_held` at composer verification. The clean installed checkout and Shoko route both identify `5c86ad6d735b4c0626c49aedfdb93aeb95e6199b`. The preflight performed no Send.
- A read-only check found an empty editor with no attachment or enabled Send. Chrome exposed the full placeholder and a second copy ending in an ellipsis through both Windows accessibility text patterns. The installed adapter rejected that value as unknown.
- The independently reviewed candidate `dfbb6a144b04ed52a57ac54ec26027ae59cc0a6a` accepts that exact value only with the known empty-placeholder tree. The original empty value passes. Drafts and other placeholder shapes still hold. The Windows suites passed 118 integration and 119 reference cases, plus all six native PowerShell suites.
- The development checkout replayed only the preflight of the saved phone request. It returned `preflight_passed` and verified the published Cat/Dog ref at `61c609a3391b1adbb0bb462beab71e4cff39a21c`. There were zero matching runs before and after. The installed launcher still uses `5c86ad6`.
- Shoko Chrome registered the exact staged read-only reader, version 1.0.0, after one owner-approved native Select Folder action. The staged script matches the independently reviewed source.
- The installed phone launch remains at its preflight checkpoint. Rerun the installed preflight on the later desktop candidate before the first Cat/Dog worker.

## Lean ADR 0002 L08 — LEAN-G1 passed (21 November 2026)

- **Base:** `e63c315`.
- **Implementation:** an existing saved worker holds if the readback identity changes between native and Chrome readers, or if Chrome replaces the reply to an already-consumed input. A pending action stays held if its anchor belongs to the other reader. Journal format and contents are preserved.
- **Focused offline evidence:** eighteen Windows Chrome-readback assertions and eleven Python worker-view tests passed. The new reader-change and regeneration assertions reproduced the missing holds before the repair.
- **Review follow-up:** the initial candidate `1f13363` needed stronger route and transcript binding. The repair requires the app-rendered conversation ID and verified assistant prose, holds unknown trailing rows, and checks saved source and reader identity at re-entry, successor preparation, and receipt readback. Twenty-five Windows assertions and twelve headless Chrome checks passed on the repair.
- **Successor follow-up:** source and destination stay in separate ordinary Chrome windows so a paused preparation can be resumed with source proof. The native Send path verifies the source again after typed readback. The twenty-five native readback assertions still pass.
- **Offline acceptance:** the independent reviewer confirmed the final successor fixes at `2348046`. The full Windows run passed 118 integration and 119 reference cases. [Independent review](evidence/astra-adr-0002-20261120/implementation/G3_20261120/LEAN_L06_L08_REVIEW.md)
- With the reader installed, the existing missing-view recovery restored the exact disposable saved chat from the verified Shoko Project link and chat ID in a separate window, preserving the original Shoko window. The Computer Use active-URL guard interrupted a diagnostic tab selection. The qualification used the controller’s existing saved-view recovery.
- The independently reviewed `dfbb6a1` integration source passed 13 live comparisons. Native Observe returned the full current reply and distinct current/prior identities for two identical user messages. Exact posted-text readback accepted the latest message after its verified preceding reply and rejected the latest-reply anchor, a wrong anchor, a fragment, and a provisional ID. Two fresh samples through `WindowsUIA.observe` agreed.
- Native observation and receipt held when scrolled away from the latest turn. Returning to the bottom, one explicit reload in the owned test window, and fresh adapter processes preserved the full reply and both causal identities. The independent reviewer accepted LEAN-G1 on the `dfbb6a1` integration tree. [Live review](evidence/astra-adr-0002-20261120/implementation/G3_20261120/LEAN_L06_L08_REVIEW.md)
- **iPhone entry observation:** the owner supplied screenshots from the Shoko Yumi Qualification Project showing a successful Remote Desktop Commander lookup and `no_run`. The Windows request was independently found as `inspect` for `JayDEmily/chat_successor`, with no registered run for the Project. The Shoko launcher still selects `5c86ad6`. This establishes a read-only phone invocation. Live Cat/Dog uses its separate fixture repository and fresh branch after qualification.
- Next is L09, removing automatic stale probes and reloads while retaining missing-view recovery and the stall hold.

## Lean ADR 0002 L07 — Exact Chrome posted-message receipt (21 November 2026)

- **Base:** `e42d67d`.
- **Implementation:** the existing Send and reconcile paths read the exact posted user body in the saved destination. A continuation must directly follow the verified triggering reply. The snapshot carries just that preceding reply’s identity.
- **Offline evidence:** sixteen Windows Chrome-reader assertions, seven headless Chrome checks, the 28-case transcript regression, and three existing native guard suites passed. Earlier identical text, a wrong anchor, fragments, and a temporary chat URL stay unacknowledged.
- **Limit:** offline code and receipt tests. Live Windows readback and independent gate approval are pending.
- **Next:** L08 cold-read and prior-state compatibility before the desktop trial.

## Lean ADR 0002 L06 — Chrome turn reader (21 November 2026)

- **Base:** `3a1cf0d`. The owner approved a read-only DOM path before the Shoko Yumi desktop chain.
- **Implementation:** a Project-scoped Chrome content script exposes the current rendered user and assistant identities and reply through one read-only accessibility field. Windows checks the exact Project, saved chat, sample age, and two fresh matching observations.
- **Offline evidence:** ten Windows readback assertions, ten Python worker-view tests, and six headless Chrome assertions passed. Test cases cover identical replies with different IDs, duplicate turn keys, unknown trailing rows, code-block text, partial renders, and offscreen reads.
- **Limit:** packaged candidate and offline checks. The installed reader and live fixture qualification remain pending.
- **Next:** verify the reader in Shoko Yumi, then qualify exact posted-message readback (L07).

## Lean ADR 0002 L05 — Shoko Yumi read-only qualification (21 November 2026)

- **Source and fixture:** `7fc7a7a4f4ac2103625c6394a82de997634c9cbb`. Created the dedicated **Chat Succession — Shoko Yumi Qualification** Project and posted two owner-authorized identical manual prompts to one saved fixture chat. The controller stayed idle.
- **Observed:** the fresh Chrome page grouped each exact user body with its exact completed assistant reply. Two distinct `data-turn-key` values, message IDs and order remained stable after reload once the bodies finished rendering. The existing `Observe` found the exact saved chat but returned `UIA_VIRTUALIZED_UNQUALIFIED` with no response ID, user anchor, or body. The older disposable chat produced the same native hold.
- **Windows checks:** 116/116 integration, 119/119 reference, five native PowerShell suites including 28/28 transcript assertions. The integration rerun removed an inherited counted Git override for that test process after missing Git config values broke disposable repository setup. An earlier attempt also saw one temporary-file replacement denial. [Independent offline review](evidence/astra-adr-0002-20261120/implementation/G3_20261120/LEAN_L02_L04_REVIEW.md).
- **Limit:** positive DOM feasibility on the fresh fixture. The standalone Windows controller still has no access to those DOM fields, so its current-turn and posted-message paths are unqualified. LEAN-G1 and worker dispatch remain held. Account transcripts and locators remain private.
- **Follow-up:** on the fresh fixture, eight UI Automation heading and body nodes exposed a framework identifier and no turn identity or ordering property. The DevTools endpoint file predates the active Shoko Chrome process and has no listening socket. Shoko Yumi and James Student use separate profile identities under the same Chrome user-data root. [Chrome connection and permission documentation](https://developer.chrome.com/docs/devtools/agents/get-started/configuration/)
- **Next:** decide on one read-only DOM connection scoped to the nominated Shoko Yumi tab before L06–L07. Keep the existing UI Automation Send path.

## Lean ADR 0002 L04 — Pause before preparation (21 November 2026)

- **Base and candidate:** `7258fff` to runner blob `5a5252b70ab961a6b6d95a11f86874e71590f399`.
- **Behavior:** direct dispatch acknowledges an existing pause before browser preparation or owner re-entry. The later pause checks still protect the click boundary.
- **Windows `test_runner.py`:** before the fix 15/16, with one unexpected prepare call. After the fix 16/16, exit 0. An existing marker caused zero browser calls. A marker written during prepare blocked Send. The pending action, count, and marker survived.
- **Limit:** mock dispatch and temporary saved state. No live Send or installation evidence.
- **Next:** L05, read-only Shoko Yumi observation of the current input and response.

## Lean ADR 0002 L03 — Durable unsupported-reader hold (21 November 2026)

- **Base and candidate:** `1eafce8` to Windows backend blob `b351141db970d18176cb463748e99c1a3ec00fd1`.
- **Behavior:** an explicit `UIA_VIRTUALIZED_UNQUALIFIED` observation holds the saved run with its chat link once streaming stops. A verified Stop control still waits. The test reuses `test_worker_view.py`.
- **Windows `test_worker_view.py`:** before the fix 8/9, with the new case returning `WAIT` after streaming stopped. After the fix 9/9, exit 0. The hold preserved the count and consumed history with no publication, preparation, reload, or Send.
- **Limit:** mocked bridge observations. The hold does not qualify a virtualized response.
- **Next:** L04, check the pause marker before browser preparation.

## Lean ADR 0002 L02 — Mixed transcript containment (21 November 2026)

- **Base and candidate:** `a46b492` to adapter blob `82778debdb69bd2738e4dc3626137ac3e5d3b1c1`.
- **Behavior:** `Get-ConversationTurns` accepts article content and its layout ancestry. Unknown siblings hold regardless of control type. The old native diagnostic assertion now checks the deliberate error, and a layout pane enclosing verified articles stays valid.
- **Windows PowerShell 5.1:** transcript regression 28/28, action gate PASS, virtualized turns PASS. All three exited 0.
- **Limit:** this contains false receipts in the synthetic article path. Current-turn identity on virtualized Chrome remains unqualified.
- **Next:** L03, surface explicit unqualified observation as a durable hold.

## Lean ADR 0002 L01 — Windows regression baseline (21 November 2026)

- **Base and candidate:** published `beacfae4790c2ec4f390e90ad0bd214fe6a1ef05` and a byte-identical copy of the interrupted adapter, SHA-256 `dfed13f20650162de74500eb4806dc884ea3effef868dbccc4c3b02193e9b769`.
- **Behavior:** added Astra's native regression with an actual older identical continuation. Adopted the [Shoko Yumi execution scope](https://github.com/JayDEmily/chat_successor_V2/blob/820aa20c6643c0ed30177459a685a4a6ee56de79/docs/astra-succession/adr-0002/PROJECT_MANAGEMENT.md).
- **Windows PowerShell 5.1:** `test_a2_transcript_boundary.ps1 -RepoRoot <snapshot>` exited 1 on the published reader (12/27 pass) and the interrupted copy (18/27 pass). All controls passed. The published reader failed status/user-anchor, anchored acknowledgement, and unanchored acknowledgement for each of five shapes. The interrupted copy passed the opaque group and changed-heading cases and failed all three assertions for each of pane, custom, and list. Raw outputs and the interrupted patch are saved privately.
- **Limit:** synthetic observations only. The working adapter still matches the interrupted snapshot at this checkpoint. LEAN-G1 remains open.
- **Next:** L02, close the mixed-transcript gap in `Get-ConversationTurns`.

## ADR 0002 A2-G3 native UIA metadata follow-up — 20 November 2026

A [source-pinned, read-only Windows metadata probe](evidence/astra-adr-0002-20261120/implementation/G3_20261120/virtualized-reader-candidate/NODE_METADATA_FINDINGS.md) checked the four verified virtualized user/assistant heading/body nodes. All exposed empty AutomationId, ItemType, ItemStatus and HelpText, and no absolute turn-position property was listed. Their runtime IDs are UIA element-instance identities, not verified persistent response or user-turn IDs. The [redacted raw output](evidence/astra-adr-0002-20261120/implementation/G3_20261120/virtualized-reader-candidate/node-metadata-readback.json) contains no conversation body. **No new actionability was established.**

The `e33ae7a` fail-closed source, independent review commission and existing G3 NOT_RUN hold stand. The next legitimate work requires a separately verifiable full-turn/ordinal source rather than constructing a receipt from visible virtualized text.

## ADR 0002 A2-L07 published exact-SHA candidate and review commission — 20 November 2026

The fail-closed virtualized-turn reader and raw test evidence are now published at **`e33ae7ad49e3510bf3021c552184cbb9d0e05758`**, with an exact [source and evidence report](evidence/astra-adr-0002-20261120/implementation/G3_20261120/virtualized-reader-candidate/CANDIDATE_RESULT.md). A fresh clean GitHub clone matched the SHA, passed `git fsck --full`, 114/114 Windows integration tests and both targeted native action/virtualized suites. The implementing worker's fresh-clone tests do **not** substitute for the separate reviewer. The [independent exact-source commission](docs/astra-succession/adr-0002/G3_VIRTUALIZED_REVIEW_COMMISSION.md) is prepared.

**Status:** separate source review pending; A2-G3 live D01–D03, positive stale response V03 and later gates remain NOT_RUN. The installed Windows backend stays at `5c86ad6`. The virtualized reader deliberately yields no Send receipt or actionable response, and the original Rowing/SolidWorks pauses are retained. The next review must challenge the immutable `e33ae7a` source and either record OFFLINE ACCEPT for the narrow safety change or identify corrective work, then independently qualify positive absolute turn attribution before any live worker dispatch.

## ADR 0002 A2-L07 fail-closed virtualized-turn reader candidate — 20 November 2026

A bounded [source and native-test candidate](evidence/astra-adr-0002-20261120/implementation/G3_20261120/virtualized-reader-candidate/CANDIDATE_RESULT.md) now recognises the verified virtualized user/assistant heading/body structure without treating visible terminal text as an authenticated latest-turn receipt. Mixed article/virtualized layouts, missing or duplicate headings, changed body classes, nested labels, streaming and posted-message acknowledgements hold safely. **No response ID, absolute count, owner input anchor, stale reload or Send receipt is issued by this fallback.** The existing article-based path is preserved.

Both hosts passed 114/114 integration tests and 119/119 reference tests. Four native Windows PowerShell suites passed, including the new negative matrix. A real read-only check of an already-finished disposable James Student chat produced two matching unqualified observations, no actionable receipt, and unchanged protected state. The canonical installed backend remains `5c86ad6`, and both original Rowing/SolidWorks pause markers remain present.

**Disposition:** source candidate verified locally; *separate independent review pending*. A2-G3 D01–D03, positive stale V03 and live Send remain NOT_RUN, as do G4–G6. Do not install or start new workers on the basis of this read-only candidate. Next action is to commission exact-SHA independent review and qualify an absolute latest-turn anchor before a live test.

## ADR 0002 A2-G3 read-only virtualized-turn discovery — 20 November 2026

[A2-G3 native accessibility evidence](evidence/astra-adr-0002-20261120/implementation/G3_20261120/VIRTUALIZED_TURN_DISCOVERY.md) was collected on the installed `5c86ad6` backend and an already-completed disposable Bird and Pig chat. The exact account, Project and one saved view were verified without any navigation or Send. Chrome exposed zero conversation article nodes, one user/assistant heading-and-body pair, and one terminal-status text node. A naive visible-body text digest did not match the previous saved response receipt, so this is discovery only: an actionable assistant status and verified user anchor are **not** established.

**A2-G3 remains NOT_RUN; no new paired controller/worker was launched.** The next leaf action is a bounded, fail-closed virtualized-turn readback repair with native negative tests and independent acceptance before live D01–D03/V03/S05–S06 actions. Do not equate the G2 identity-only recovery pass with a G3 message/receipt pass.

## ADR 0002 A2-G2 source-pinned Windows read-only recovery follow-up — 20 November 2026

**A2-G2 PASS for installed Windows account routing, no-Send preflight and read-only saved-view recovery on `5c86ad6d735b4c0626c49aedfdb93aeb95e6199b`.** The prior W01 and W02 observations and the new W03 read-only recovery are reconciled in [the exact-candidate receipt](evidence/astra-adr-0002-20261120/implementation/G2_20261120/RECOVERY_RECONCILIATION_5C86AD6.md). The separate [independent OFFLINE ACCEPT](evidence/astra-adr-0002-20261120/implementation/G2_20261120/recovery-review-5c86ad6/REPORT.md) covered 114 integration and 119 reference tests per host, three native PowerShell suites and fail-closed virtualized-view negatives. W02's two-window/mutex live evidence was carried forward from the unchanged code path on the preceding installed candidate; it was not freshly repeated on `5c86ad6`.

Codex published and installed the exact source revision and recorded no-Send installed checks for both accounts. A real Windows cold-open restored the completed disposable saved chat on the exact candidate in a temporary root, then a fresh **installed** verification on the canonical root reused that same already-open saved chat with two stable read-only observations. Protected files were unchanged, both original project pause markers remained present, and no controller or Send action was performed. In particular, the latest assistant turn still cannot be qualified as actionable in Chrome's virtualized UI; identity-only recovery must not be used as a completion, stale-response, approval or Send receipt.

**Next:** A2-L07 / A2-G3 starts with safe read-only qualification of virtualized latest-turn boundaries using a disposable fixture. Independent negative checks are required before live advancement; real positive stale reload and paired-run criteria remain NOT_RUN. G4–G6 are NOT_RUN. Keep Rowing/SolidWorks paused and `main` unchanged.

## ADR 0002 A2-G2 installed Windows routes and recovery hold — 20 November 2026

A2-G1 remains independently accepted for `0b6bfa3`. Both separate Remote Desktop Commander accounts read the same `codex/chat-succession-finish` tip at `8f33cc5`. The installed Windows launcher now uses the two verified `USERPROFILE` selectors. **Both installed no-Send preflights and the concurrent-window/mutex checks passed.** The installed [A2-G2 evidence](evidence/astra-adr-0002-20261120/implementation/G2_20261120/PREFLIGHT.md) records the pin, rollback hash, both route receipts, exact fixture SHA `b91b00f`, and matching before/after state.

**A2-G2 is HOLD.** Windows PowerShell checks passed, but saved-chat recovery timed out on the completed approval fixture. A manual view verified the saved chat and profile. The current Chat renderer exposes virtualized groups without the article boundaries required by the native adapter. Wrong-profile and duplicate-view checks held as expected. A2-G3–G6 are NOT_RUN. The next action is to qualify a reliable latest-turn boundary and rerun read-only recovery on the exact candidate.

## ADR 0002 A2-G1 independent acceptance — 20 November 2026

**A2-G1 OFFLINE ACCEPT** on `0b6bfa3e935e713fe2f36afd8da79c2befab9a42`. The [independent report, 24-case matrix and raw evidence](evidence/astra-adr-0002-20261120/implementation/G1_20261120/independent-0b6bfa3/REPORT.md) confirm all 24 offline cases, 113 integration and 119 reference tests on both hosts, and three native Windows PowerShell passes. The trailing unverified article now blocks older acknowledgement and status. Exact complete and streaming controls pass.

**Next eligible work** is A2-L06 / A2-G2 installed Windows account and no-Send verification on this pin. A2-G2–G6 are NOT_RUN.

## ADR 0002 A2-G1 complete transcript verification — 20 November 2026

Source `0b6bfa3e935e713fe2f36afd8da79c2befab9a42` holds on any unverified top-level article so a newer unidentified turn cannot expose an older Send receipt or assistant status. [Corrective evidence](evidence/astra-adr-0002-20261120/implementation/G1_20261120/corrective-0b6bfa3/RESULT.md) records 113/113 integration on both hosts and three native Windows PowerShell passes.

**Next eligible work** is independent A2-G1 review of the source pin. A2-G2–G6 are NOT_RUN.

## ADR 0002 A2-G1 independent review of c605c5f — 20 November 2026

**A2-G1 OFFLINE HOLD** on `c605c5fafe4d3cfefe4173f04a53ebf0d1943d59`. [Independent review, exact case matrix and raw repro](evidence/astra-adr-0002-20261120/implementation/G1_20261120/independent-c605c5f/REPORT.md). Both hosts pass 113 integration and 119 reference tests, and the three native suites pass. All five in-body labels are now preserved. A newer article without a verified role can still be omitted while an older status or posted body is accepted, holding S01, S05, S06 and O04.

**Next eligible work** is correcting this shared latest-turn boundary and independently re-reviewing the next pin. A2-G2–G6 are NOT_RUN.

## ADR 0002 A2-G1 conversation readback correction — 20 November 2026

Candidate `c605c5fafe4d3cfefe4173f04a53ebf0d1943d59` corrects the shared accessibility text-boundary fault found below. [Corrective evidence](evidence/astra-adr-0002-20261120/implementation/G1_20261120/corrective-c605c5f/RESULT.md) records 113/113 integration on Windows and Ubuntu and three native Windows PowerShell passes. The native test covers all five former literal delimiters, whole anchored acknowledgement, and genuine final prose status.

**Next eligible work** is a separate A2-G1 decision for the new source pin. A2-G2–G6 are NOT_RUN.

## ADR 0002 A2-G1 independent review of 9e64211 — 20 November 2026

**A2-G1 OFFLINE HOLD** on `9e6421112286f7e993d7e91a3e63fbfea0a0c206`. The [independent review, 24-case matrix and raw repro](evidence/astra-adr-0002-20261120/implementation/G1_20261120/independent-9e64211/REPORT.md) verify 113 integration and 119 reference passes on both hosts and all three native helper suites. The five earlier findings pass their independent repros. An in-body UIA text delimiter can truncate the assistant or posted user turn, holding S01, S05, S06 and O04.

**Next eligible work** is targeted correction of that native text boundary and independent re-review at the new pin. A2-G2–G6 are NOT_RUN.

## ADR 0002 A2-G1 second corrective candidate — 20 November 2026

Candidate `9e6421112286f7e993d7e91a3e63fbfea0a0c206` addresses the five findings from the separate review below. [Corrective evidence](evidence/astra-adr-0002-20261120/implementation/G1_20261120/corrective-9e64211/RESULT.md) records 113 integration and 119 reference passes on Windows and Ubuntu plus three native PowerShell passes. The checks cover exact pause acknowledgement, prose status, repaired publication, whole posted-turn receipts and durable owner scope.

**Next eligible work** is the separate A2-G1 re-review of this pin. A2-G2–G6 are NOT_RUN.

## ADR 0002 A2-G1 independent re-review — 20 November 2026

**A2-G1 OFFLINE HOLD** on corrective candidate `66f4b94dc6fa94c708b42c11d2681da291dd9d99`. The [independent 24-case review and raw evidence](evidence/astra-adr-0002-20261120/implementation/G1_20261120/independent-66f4b94/REPORT.md) reproduce 111 integration and 119 reference passes on each of Windows and Ubuntu and three native PowerShell passes. New local-Git, journal and native helper probes hold seven cases involving pause acknowledgement, actionable non-prose status, publication repair, exact posted-turn acknowledgement and replaced owner scope.

**Next eligible work** is targeted repair of these findings and independent re-review of the resulting source pin. A2-G2–G6 are NOT_RUN.

## ADR 0002 A2-G1 corrective candidate — 20 November 2026

Corrected L02–L05 at `66f4b94dc6fa94c708b42c11d2681da291dd9d99` against the independent hold below. [Source-pinned corrections and raw checks](evidence/astra-adr-0002-20261120/implementation/G1_20261120/corrective/RESULT.md) record 111 integration and 119 reference passes with zero skips on both Windows and Ubuntu, plus three native Windows PowerShell helper tests. The account, browser, publication and owner-input regressions cover the nine held cases.

**Next eligible work** is independent A2-G1 review of the corrected candidate. The candidate is pending review. A2-G2–G6 are NOT_RUN.

## ADR 0002 A2-G1 independent review — 20 November 2026

**A2-G1 OFFLINE HOLD** on candidate `9a2fc382049a548adfefb5ed26a202c715988ca2`. The separate review reproduced 106 integration and 119 reference passes on each of Windows CPython 3.13.15 and Ubuntu CPython 3.14.4, plus all three native PowerShell helper tests. The [independent review, 24-case matrix and raw evidence](evidence/astra-adr-0002-20261120/implementation/G1_20261120/independent/REPORT.md) record 15 offline passes and 9 holds. The negative probes reproduce unverified routing, a mismatched bootstrap action, provisional successor adoption, stale-view and publication gaps, and dispatch with absent private owner context.

**Next eligible work** is targeted correction in L02–L05 and separate A2-G1 review of the new pinned candidate. A2-G2–G6 are NOT_RUN. The paused Shoco workloads retain their recorded holds.

## ADR 0002 G1 fresh receiver precheck — 20 November 2026

Clean clone of 9a2fc382 verified [24-case G1 receiver matrix](evidence/astra-adr-0002-20261120/implementation/G1_20261120/RECEIVER_AUDIT.md), 106 integration + 119 reference, and native PowerShell action/view helper tests PASS. [A strictly independent separate-review commission](docs/astra-succession/adr-0002/G1_STRICT_REVIEW_COMMISSION.md) is ready; A2-G1 remains PENDING separate reviewer. A2-G2–G6 NOT_RUN; no installed changes or active project restarts.


## ADR 0002 L05 scoped approval and publication — 20 November 2026

[L05 implementation and test matrix](evidence/astra-adr-0002-20261120/implementation/L05_20261120/L05_RESULT.md): distinguish worker advancement from verified owner approval delivery, and log the exact published Git SHA/ref before and after adoption. **106/106 integration + 119/119 reference PASS**, plus two Windows PowerShell helper tests; no installed, browser or iPhone tests. L02–L05 offline implementation is ready for separate **A2-G1 independent review**, not yet released. Active Rowing and SolidWorks runs remain paused.


## ADR 0002 L03 safety repair on post-L04 baseline — 20 November 2026

An independently reproduced [L03 negative review](evidence/astra-adr-0002-20261120/implementation/L03_20261120/review_20261120/NEGATIVE_REVIEW.md) corrected wrong-destination adapter entry, changed account-route bootstrap adoption and lost initial intent on pre-click pause. Full post-repair offline checks: 103 integration and 119 reference PASS, native Windows PowerShell action-check PASS. No desktop install or live Send. G1 remains in progress with L05 pending; G2–G6 remain NOT_RUN.


## ADR 0002 L04 offline saved-view qualification — 20 November 2026

Existing Chrome recovery logic retained after [7 positive/negative mocked
view cases and native Windows PowerShell helper checks](evidence/astra-adr-0002-20261120/implementation/L04_20261120/L04_RESULT.md):
98/98 total integration PASS. No existing recovery-code deficiency demonstrated.
Real positive automatic stale recovery and account-specific installed tests
remain NOT_RUN. Next A2-L05; G1 remains open.

## ADR 0002 L03 offline action-identity candidate — 20 November 2026

The final Windows UIA adapter now verifies the same persisted action ID,
response, source, project, window, message digest and route receipt before
Send; read-only uncertain reconciliation also refuses a stale target.
New bootstrap intents carry their own UUID identity. [L03 evidence](evidence/astra-adr-0002-20261120/implementation/L03_20261120/L03_RESULT.md):
91/91 integration tests after integrating independently reviewed L02 fixes (retained prior 88/88 result), and native Windows PowerShell AST plus positive/negative
action-record checks PASS. No browser Send or installation; L03 live faults
remain NOT_RUN. Next A2-L04, while G1 remains open.
## ADR 0002 L02 — independent negative review and targeted repair (20 November 2026)

The published `3f9715e` account-route implementation passed its 79 integration tests, but a fresh independent review reproduced three untested edge cases: duplicate JSON route keys resolved by last-write-wins, two account records accepted with the same Chrome profile, and a pre-Send operator pause not shown as acknowledged. [Exact probes, repairs and 82+119 fresh tests](evidence/astra-adr-0002-20261120/implementation/L02_20261120/review_20261120/NEGATIVE_REVIEW.md). Corrections are deliberately limited to private route ambiguity and pause-status readback; no installed Windows candidate was changed. A2-L02 remains offline only, and A2-G1/G2 are not accepted.


## ADR 0002 L02 offline account-routing candidate — 20 November 2026

Added explicit account/native installation/private profile binding to the
existing controller (new `integration/account_routes.py` and small changes
to the launcher/CLI/Windows UIA/status). The opt-in native marker is deliberately
**not installed**. [Implementation and raw results](evidence/astra-adr-0002-20261120/implementation/L02_20261120/L02_RESULT.md):
79/79 integration tests (63 baseline + 16 new) and 119/119 unchanged reference
tests pass on Ubuntu, with mocked wrong-route no-Send holds and preserved
legacy pause handling. No real account/plugin installation or browser Send.
Next leaf is A2-L03; A2-G1 remains open.

## ADR 0002 mock-fixture isolation — 20 November 2026

The owner expressly replaced Rowing and SolidWorks as live-test workloads with disposable mocks. A private `JayDEmily/rowing-clone-test` repository has been created with a prepared pinned `main@5b04bd24` source snapshot under `snapshot/`; published remote `main@f2c28775532bc3f828af95edd6c61258f6313496` with exact source-tree equality and GitHub API readback, READY for fresh isolated fixture branches. Existing Cat/Dog, Bird/Pig and approval fixtures provide the complementary finish, cap and phone cases. [Mock fixture register](docs/astra-succession/adr-0002/MOCK_FIXTURES.md). Real Rowing/SolidWorks remain paused.

## ADR 0002 programme — 20 November 2026

Owner accepted the bounded ten-leaf implementation with standing authority (no repeat routine approvals). [Operative ADR](docs/adr/0002-account-bound-resumable-runs.md) · [Management and gates](https://github.com/JayDEmily/chat_successor_V2/blob/820aa20c6643c0ed30177459a685a4a6ee56de79/docs/astra-succession/adr-0002/PROJECT_MANAGEMENT.md) · [G0 baseline](evidence/astra-adr-0002-20261120/implementation/G0_20261120/BASELINE.md). A2-G0 PASS via fresh Ubuntu 295/295 manifest, 63+119 suites, six Git histories and 13 fixtures. The paused Rowing and SolidWorks runs remain untouched. Next eligible leaf: A2-L02.

## Astra ADR 0002 review intake — 20 November 2026

The complete 13:09 AEDT Astra response has been preserved verbatim on this branch: [intake and checksums](evidence/astra-adr-0002-20261120/INTAKE.md), [proposed ADR](evidence/astra-adr-0002-20261120/package/docs/adr/0002-account-bound-resumable-runs.md), [implementation plan](evidence/astra-adr-0002-20261120/package/docs/IMPLEMENTATION_PLAN.md) and [acceptance gates](evidence/astra-adr-0002-20261120/package/acceptance/GATES.md).

Disposition is **review received; proposed ADR pending owner decision**. This intake adds only documentation, evidence and the unmodified source archive. It does not change controller/plugin source, current trial state, an installed release or live acceptance. All 94 package-manifest entries were verified locally before commit.


## Shoco rollout — 20 November 2026

Resumed at `30f5757` on `codex/chat-succession-finish`. At the owner's direction, the rollout now targets the Shoco account. [Finish plan](docs/astra-succession/finish-chat-succession.md)

- **Private release saved.** Chat Succession 0.4.3 was created in Shoco from the staged package at `2c29406`. Readback confirmed the private personal release, the `start-chat-succession` skill, and its Remote Desktop Commander binding. [Chat Succession](https://chatgpt.com/plugins/plugins_6aff6858ab788191a4a6b7c15a7216bc)
- **Windows route verified.** The installed launcher routes the verified Shoco Desktop Commander environment to Ubuntu candidate `2c29406` and Chrome's signed-in Shoko profile (`Profile 11`). It passes the native installation directory used by the 0.4.3 worker instructions. The previous command remains the default for other environments. The original Windows wrapper is backed up beside the launcher as `start-project.pre-shoco-0.4.3.cmd`.
- **Validation.** All 63 Python integration tests and the Windows PowerShell recovery comparisons passed. The Desktop Commander launcher verified an empty Project A Test composer without a Send. Repeat no-Send tests in Shoko verified the pinned Rowing `993741f` and SolidWorks `bb258b6` checkpoints using the existing disposable Project A Test and Project B Test, respectively.
- **Overlapping desktop runs.** The launch requests first held before any Send because the job IDs exceeded 24 characters. With valid IDs, SolidWorks run `271867d56ebd3443a4b40fa6` registered at 08:34:59 Sydney time. Rowing run `b401f984a1927f6979067d07` registered at 08:36:31 after its initial composer preparation timed out before Send. The retry reused the configured run. Both caps are two.
- **Live view recovery.** Paused Rowing with one saved worker and no pending Send, moved the same chat to an inactive tab, and resumed its observer at 08:37:54. The controller restored that exact worker at 08:38:08 and kept the count at one while SolidWorks continued to poll. The first live SolidWorks stale-view comparison saw a still-streaming fresh view and returned `waiting`. The automatic stale-view reload still needs a trial with a newer completed response.
- **Phone fixture staged.** `codex/g2-iphone-approval-shoco-20261120` was published with its instructions pinned to the new branch. Its base predates the first approval edit. [Fixture `b91b00f`](https://github.com/JayDEmily/chat-succession-trial-approval/blob/b91b00fe75be2ca011eac1ad1cc0d668ffd8d8bf/README.md)
- **Next.** Verify the overlapping Rowing and SolidWorks desktop trials with a cap of two and observe live worker-view recovery. Run the fresh Shoco iPhone approval from Project A Test after the desktop trials. The prior account's trial evidence is recorded below.

## James Student release handoff

Resume in `JayDEmily/chat_successor` on `codex/chat-succession-finish`. The audit baseline is `8345978`. The previous iPhone approval, overlapping desktop runs, and two-worker cap are verified below. [Approved finish plan](docs/astra-succession/finish-chat-succession.md) · [Astra ADR](docs/adr/0001-generic-entry-and-re-entry.md)

- **Candidate 0.4.3.** Source commit `2c29406b1c43904c5ead79064fe7856971e0aa2e` includes recovery of an already saved Chrome view, a bounded stale-view probe, wrapper discovery when the connector redirects LocalAppData, and a no-Send project and Git preflight. Recovery reuses the saved chat ID and leaves the worker count intact. A draft, attachment, ambiguous view, or possibly submitted Send can require operator review. The stale probe waits two minutes and is limited to once per five minutes per worker in a running controller. A controller restart begins fresh observation. All 63 Python integration tests and `git diff --check` passed.
- **Windows setup.** The installed wrapper was verified at `C:\Users\james\AppData\Local\ChatSuccession\start-project.cmd`, sourcing `/home/jds/chat_successor_usage_template_20261119` in Ubuntu. The tested candidate is in a detached Ubuntu worktree at `/home/jds/chat_successor_finish_2c29406`. Use Desktop Commander and those Ubuntu Git credentials for publication. The candidate wrapper passes `--install-root "%~dp0."` before the request arguments and sets `CHAT_SUCCESSION_CHROME_PROFILE_PATH` to the verified James Chrome profile, `C:\Users\james\AppData\Local\Google\Chrome\User Data\Profile 13`. This was verified with a temporary wrapper. Keep the existing wrapper available for rollback.
- **Windows results.** Parsing and the saved-view comparison tests passed in Windows PowerShell. Running the plugin's launcher discovery command returned the exact installed wrapper. No-Send preflight passed for the actual Rowing and SolidWorks Projects, including each fresh empty composer and the exact branch tip listed below. Preflight created no durable state. A separate live recovery probe reopened the closed saved worker `6afee7d1-a62c-83ec-9624-023f3c6ca5a7` from completed iPhone run `8f8bb228a19625f450959aaa`. Two stable ready reads matched the same chat and new window. The controller journal hash matched before and after. The new test window closed. A live automatic reload of a genuinely stale view remains to be tested during the candidate trials. A worker still has to be the selected tab in an accessible Chrome window. Opening a recovery window can briefly bring Chrome forward.
- **Private release and trials.** The plugin list available to this conversation showed no Chat Succession entry. Resolve the original James Student private plugin link or backend ID, verify its installed revision, and update that same plugin. The tested candidate is staged separately from the installed wrapper. Once the candidate is installed, run the two overlapping desktop trials and then the fresh iPhone approval on a clean ref in `JayDEmily/chat-succession-trial-approval`. Use a cap of two. The earlier iPhone branch `codex/g2-iphone-approval-20261119` is a completed baseline fixture.

Windows preflight verified `JayDEmily/rowing2026` on `work/bio2-golden-yaml-24-integrated-workstation-20261119` at `993741f947aba6e622cf97d233c4f85836671d13`, and `JayDEmily/sw_v1` on `work/sw2021-full-source-library-20261119` at `bb258b66d311f3a5a8c2d5eea83310d41dfdce6a`. The proposed isolated receipt refs are `work/chat-succession-audit-rowing-20261119` and `work/chat-succession-audit-sw2021-20261119`. Preserve both existing project runs and recheck the scoped authority at each pinned checkpoint before staging trial work.

## Takeover audit — 20 November 2026

The Windows launcher used the Ubuntu checkout of `codex/chat-succession-template`. Its starting
revision matched `179a4b9`. Followed the actual path from the plugin request
through Project and run selection, Windows observation and Send, GitHub
receipt verification, and the next saved worker. The current implementation
resolves runs by stable Project and repository and retains the configured cap
across an authorized checkpoint branch change. [ADR 0001](docs/adr/0001-generic-entry-and-re-entry.md)

- **Requested iPhone trial.** The selected branch already held both expected
  commits. The Windows journal independently confirmed run `8f8bb228a19625f450959aaa`,
  a cap of two, two distinct saved workers, one scoped approval delivery to the
  original worker, one automatic successor and `STOP_FINISHED` with no pending
  action. The Git commit trailers matched the journal. The completed fixture
  was reconciled. [Published notes](https://github.com/JayDEmily/chat-succession-trial-approval/blob/1590c45af104e34cdcd5c2820e9ce30c9da35e80/NOTES.md)
- **Previous concurrency.** Both Windows journals confirmed the 3m09s overlap
  of Cat/Dog and Bird/Pig, one automatic successor per run and two saved workers
  per terminal run. The original approval and its Cat/Dog companion also
  overlapped for 94 seconds before the approval hold. The companion needed a
  format-only response correction. Bird/Pig had its own GitHub repository.
  [Prior evidence](evidence/astra-generic-entry-20261119/live-acceptance.md)
- **Controller corrections.** `6f3a255` binds the Send button to the verified
  editor's document, checks the active address and draft before invoking it,
  and requires a same-chat posted turn after the exact triggering assistant
  response. An operator pause preserves terminal `chat_cap` and
  `programme_finished`. A prior timing log with a missing controller journal
  now holds for recovery before any bootstrap. A worker prompt places
  commentary and timestamps above the standalone status line. Independent
  review and 50 integration tests passed. Windows PowerShell parsing and
  receipt probes accepted the exact new post and rejected the older identical
  post and a post after another assistant turn.
- **Windows and Chrome.** Both first live attempts held before Send. The
  connected tool had a different LocalAppData path and one fresh Chrome
  window showed sign-in. A no-Send probe using the verified existing signed-in
  profile found the exact Project, an empty composer, and its UI Automation
  document. `07c8a64` adds a launcher-process profile override, inherited by
  the controller. Used that setting and the verified existing run directory
  for the desktop replays. The fixture route updates and this audit entry were
  published from Ubuntu.

- **Parallel desktop replays.** On 20 November Melbourne time, Cat/Dog
  registered at 00:13:58 and Bird/Pig at 00:14:25, each in its own Project
  with a cap of two. Cat/Dog confirmed its automatic successor at 00:19:07
  and reached `STOP_FINISHED` at 00:23:59. Both published story commits
  matched its two saved worker IDs. [Cat/Dog branch result](https://github.com/JayDEmily/chat-succession-cat-dog-pair/blob/3105b8d6af3bc4c37ecbd79c127e14d0312b375e/STORY.md)
- **Bird/Pig pause and continuation.** Paused the observer and resumed the
  same worker with its count still one at 00:16:40. It overlapped with the
  Cat/Dog controller for another 7m19s. The two identical `NEED_MORE_TIME`
  continuations were separately confirmed in the same saved chat at 00:16:53
  and 00:17:49. The first worker published only the expected opening line.
  [Opening commit](https://github.com/JayDEmily/chat-succession-bird-pig/commit/8c2bf709570ab3ce6333d5ae7afda9cf45b8b387)
- **Stale view recovery.** After the Bird/Pig publication, the original view
  continued to show a partial answer and a Stop control. A separate read-only
  view of the same saved chat showed a complete response and no Stop control.
  With the observer paused, closed the temporary view, reloaded the original
  view after verifying its composer was empty, and resumed the saved run. The controller
  confirmed the one automatic successor at 00:31:19. This replay required
  operator-assisted view recovery. At 00:35:27 it reached `STOP_CAP`, with
  two distinct saved workers and no pending action. The verified second
  story commit leaves the third review task eligible. [Bird/Pig branch result](https://github.com/JayDEmily/chat-succession-bird-pig/blob/e940ee5381f32bdb8fa5a85a12a174aeb5a8c2a4/STORY.md)

The Send method supports a background Chrome window. The target still has to
be the selected tab in exactly one accessible Chrome window. Closing the
registered chat, leaving it behind another tab, or opening duplicate views
can still hold observer recovery. A read-only probe of a closed historical
worker returned zero eligible targets. A Project with no saved sidebar chat needs
its verified landing URL. The owner supplies an existing Project and an
authorized GitHub publication route for each workload.

The original Rowing hold was consistent with the published project authority.
The later scoped release and work branch are real. That checkpoint lacks the
succession trailers needed for a controller handoff. The Windows journal still
shows one worker, the original branch, and no publication check or successor.
The checkpoint's ownership note
documents the seven preserved raw-stdout blank lines and the separate scoped
whitespace checks. The sources do not establish which ChatGPT conversation
received the original instruction or confirm concurrent writers. [Rowing checkpoint](https://github.com/JayDEmily/rowing2026/commit/ff2876dc3c3b0d739df1e5e08de0626233c7ffa9)

The SolidWorks request resolved `JayDEmily/sw_v1` and its actual working branch.
The run directory has configuration and no initial Send intent, controller
journal or timing log. GitHub has project commits without succession trailers.
There is no saved evidence identifying the precise pre-registration failure.
An ordinary-project replay remains outstanding for both cases. Each workload
keeps its own native-tool, approval, artifact and publication rules. [SolidWorks project checkpoint](https://github.com/JayDEmily/sw_v1/commit/bb258b66d311f3a5a8c2d5eea83310d41dfdce6a)

## iPhone approval and Cat and Dog overlap — 19 November 2026

The owner launched a disposable approval run from the iPhone with Chat
Succession 0.4.2. It overlapped with Cat and Dog on Windows for 94 seconds
before the approval hold. Both made one automatic handoff and reached
`STOP_FINISHED` with two saved workers. Cat and Dog needed one format-only
follow-up after publication. The iPhone approval was delivered once to the
original worker. [Live evidence](evidence/astra-generic-entry-20261119/live-acceptance.md#iphone-approval-and-cat-and-dog-overlap)

## Desktop approval and branch-rotation closeout — 19 November 2026

The bounded desktop replays delivered one scoped approval to the original
worker and handed off once on a verified rotated branch. Each run stopped at
two saved workers. The identical approval request returned an existing
receipt. The replay uncovered two Windows adapter faults, both fixed and
reviewed. [Replay evidence](evidence/astra-generic-entry-20261119/live-acceptance.md#desktop-closeout-replays)

The personal plugin's 0.4.2 source points to the maintained usage guide. The
iPhone approval result is recorded above. The owner's Stage C workload remains
open.

## Concurrent Chrome window startup — 19 November 2026

Two near-simultaneous Project lookups reproduced an ambiguous Chrome window
error. The adapter now lets one run at a time open and identify its new window.
Both live lookups passed when repeated one millisecond apart. Their temporary
windows closed. [Trial evidence](evidence/astra-generic-entry-20261119/live-acceptance.md#concurrent-window-startup-follow-up)

## Hidden Project lookup and overlapping story runs — 19 November 2026

The Windows launcher resolved the Cat and Dog Project by name with the Projects
section collapsed. Cat and Dog and Bird and Pig then ran concurrently in one
Chrome profile. Each verified one successor and reached `STOP_FINISHED` with
two saved workers. The console peaked at three Chrome windows and returned to
one after cleanup. [Trial evidence](evidence/astra-generic-entry-20261119/live-acceptance.md#hidden-project-lookup-and-overlapping-story-runs)

## Bird and Pig clean Chrome trial — 19 November 2026

The installed plugin started a disposable two-worker run after a complete
Chrome shutdown and restart. Both workers published verified Git receipts,
and the controller launched the second worker automatically. One malformed
browser read briefly held the run. A no-Send observation cycle verified
`STOP_FINISHED` with two saved workers. The controller now retries a malformed
read once. [Trial evidence](evidence/astra-generic-entry-20261119/live-acceptance.md#bird-and-pig-clean-chrome-trial)

## Astra generic entry implementation — 19 November 2026

The working branch implements L1–L4 from ADR 0001. Entry resolves an existing
run by verified Project and repository. Scoped approval uses the existing
sender only when the saved worker is at the nominated hold. The effective
checkpoint advances only after a published current-worker receipt.

The 45 integration tests, 119 Astra reference tests, PowerShell parser, and
installed no-run inspection passed. Independent OpenAI Exec Plans review
identified recovery and browser identity issues that were addressed before
publication. The private plugin is installed at 0.4.1. [Live L5
evidence](evidence/astra-generic-entry-20261119/live-acceptance.md) verifies
same-worker approval delivery and checkpoint rotation on two disposable
projects. The original fresh-window failure was reproduced and the
same-window successor path prepared both live composers successfully.
Both original clicks produced local-only conversation IDs and remain
unconfirmed. The desktop closeout above records the results of the new runs.

## Astra generic entry and re-entry proposal — 19 November 2026

[ADR 0001](docs/adr/0001-generic-entry-and-re-entry.md) records Astra's
proposed decision. The [complete plan](docs/astra-succession/generic-entry-plan-20261119.md)
and [review evidence](evidence/astra-generic-entry-20261119/) preserve the
five leaves, three gates, and offline reproduction for owner review. Astra
reran 154 tests and six additional probes on the supplied baseline.
Implementation and installed post-approval acceptance remain open.

## My Cat and Dog mobile-launch trial

The personal startup workflow now opens one fresh desktop worker through the
installed Windows launcher. The iPhone request chat stays outside the count.
Remote Desktop Commander preflight verified the authenticated Project and an
empty composer without posting. The first preflight held on a draft and left
it intact. A later preflight passed.

The four-turn story guide is published at `94eee8b6162520fc0f75f355bdac6e778310c50b`.
The owner's live iPhone launch started its Windows controller at 14:26:32
Sydney time on 19 November. The timing log records three confirmed successor
sends and `STOP_FINISHED` at 14:36:20. The saved controller has four distinct
chat IDs and no pending action. Each ID matches its Git commit trailer, and
each turn's published commit descends directly from the preceding turn.
[The completed story](https://github.com/JayDEmily/my-cat-and-dog/blob/9b0180354fc1a6e127c9982dd44fb4b17f5716a9/STORY.md)
contains four dialogue lines.

## Repo-neutral launcher and handoff

The generic launcher accepts the nominated GitHub repo, branch and ChatGPT
Project. Workers reason from their own repository's instructions and use three
Git trailers to publish a common handoff receipt. On Windows, Chrome found
the trial Project by name, and Remote Desktop Commander ran the installed
Windows launcher successfully in no-Send mode against its GitHub branch.
Real-Git tests with simulated browser handoffs cover successor launch,
terminal stop, stale receipts and holds. Independent review cleared the
changes after 35 integration tests and 119 Astra reference tests passed.
A live generic workload is the next acceptance step.

## Chat Succession startup template — 19 November 2026

The tested Astra baseline is published on `main` at `cffdb253aa24c52cbfec59b08112742f18f7352e`. This separate working branch contains the owner quickstart and the personal plugin source for the two-step browser startup. The shared controller stays separate from the workload repository.

An ordinary workload still needs a live Stage C run under its own authority. This branch has no active test assignment.

## Chrome composer focus dependency removed — 19 November 2026

The L12 test's first attempt exposed a remaining Windows foreground failure in the composer clipboard read. The existing Windows adapter now observes Chrome's empty-placeholder structure through UI Automation. The same read runs at Prepare and before typing. Exact-placeholder drafts, attachments and ambiguous composer states still hold the action.

[Live background-composer evidence](evidence/astra-l07-20261119-background-composer/live_record.json) records an empty composer inspected while another Chrome window remained foreground, preservation of both ordinary and exact-placeholder drafts, and one verified disposable Send whose target was in the background at dispatch. The ordinary Project and saved chat checks, owner pause and single-Send receipt still apply. The completed Astra gate records and earlier run fixtures remain intact. This branch has no active test assignment.

## Astra bounded integration closeout — 19 November 2026

**G0–G4 closed for the bounded test plan.** Runs A, B and F satisfy L13, with 15 distinct saved Project chats, 12 automatic successors and 15 independently validated published slices. Each controller reached `STOP_FINISHED` with no pending action. A/B ran on the earlier adapter. F repeated the five-chat chain on the polling and focus update. Run C remains assisted. Runs D and E remain preserved at 1/5 and 3/5.

- **Response interpretation:** The unchanged reference parser retains its recorded offline results. In Run F the Windows adapter read back all five completed `TASK_COMPLETE` markers and routed each against current GitHub state. Semantic classification remains disabled and its shadow test was skipped.
- **Live handoff:** [Run A](evidence/astra-l13-20261118-a/live_record.json), [Run B](evidence/astra-l13-20261118-b/live_record.json) and [Run F](evidence/astra-l13-20261119-f/live_record.json) each recorded four automatic successors and a terminal stop. Run F finished at 12:10:12 Sydney time after 36 minutes 41 seconds, with individual handoffs of 28–44 seconds from verified completion to confirmed Send. The passing runs record zero corrective prompts, manual handovers, duplicate posts or misroutes.
- **Published work:** The five ordered slice commits for each passing run matched the saved controller identities and final fixture. The original fixture validator passed each run. Run F’s final publication receipt is `ab6aede1c367768f46799087fdc931b8fb950830`.
- **Owner-pause regression:** `1610597ade9ef238698c22546b94916bf1e87f68` checks pause after Chrome preparation and at the pre-click boundary. All 25 integration tests passed. The [live L12 receipt](evidence/astra-l12-owner-pause-20261119/live_record.json) verifies a pause during successful Chrome preparation with a preserved action and zero successor posts. The first attempt held on Chrome focus. The passing retry reused the same worker and positively unsent action. The disposable test branch is retired at `9ae63a41e4f306705174f92c84077c1a59d9f642`.
- **Handoff:** [Live results](evidence/live_test_results_20261118.csv) are current. G5 / L14 stays `NOT_RUN`. The Run F controller and the L12 test controller have stopped. This branch has no active test assignment. Use the normal repo and working-branch pointer for the next owner-assigned job. A real job still needs its published progress and next-task record connected to the fixture-scoped repository reader.

## L13 Run F fifth saved worker — terminal slice 5 of 5, 19 November 2026

- **Scope:** Single final Run F fixture slice from remote `4f9f761b7adf7f4c49b794770fc6c5f5adca653b` in distinct saved Project chat `6afe4a7f-d920-83ec-8b4e-06b9426a1eae`. Existing controller PID 6684 showed five distinct saved IDs, four consumed `TASK_COMPLETE` replies and no pending action/halt; matching read-only Chrome UIA confirmed Project and this chat. No worker-side controller or browser Send.
- **Result:** probe `fixture-964f687612d858eb`: alpha 2/-11, beta 2/16, gamma 2/19; six rows and combined total 24. Added only step 5; `STATE.json` is 5/5 with `programme_complete=true` and `next_task=null`. Earlier Run F and Run E results retained.
- **Validated publication:** the unchanged fixture validator returned `fixture_valid=true`, `completed_steps=5`, `total_steps=5`; both working and staged `git diff --check` were clean, and the staged diff contained exactly four files (Run F RESULTS/STATE, worker evidence and PROGRESS). Fixture/evidence commit `d26e4f621bafaeac5c5903a99d8fbf6e19a29632` was pushed; `git ls-remote` matched exactly. Independent GitHub readback pinned to that commit confirmed five ordered results and distinct chat IDs, final 5/5 terminal state, evidence and PROGRESS; Run E remained 3/5. Evidence: `evidence/astra-l13-20261119-f/run_f_worker_slice5.md`.
- **Next action:** the pre-existing single external Run F controller consumes this final `TASK_COMPLETE` and should terminally stop with `STOP_FINISHED`, no sixth chat. A separate terminal readback and three-run G4 assessment are still required; this worker does not assert terminal observation.


## L13 Run F fourth saved worker — slice 4 of 5, 19 November 2026

- **Scope and provenance:** Run F `astra-l13-20261119-f`, fourth distinct saved Project worker `6afe4875-e7b8-83ec-bc8b-6a14169b58e5`. Read-only UIA matched this chat and correct Project. The already-running controller had four distinct IDs, three consumed completed turns, no pending action/halt; this worker did not operate its controller or Send.
- **One slice only:** from remote source `da00f4b1c223fee647c705d4f582b6f34407f9cc`, normalised six fourth-probe rows into alpha 2/23, beta 2/25, gamma 2/24; 72 total. One result was appended; state is 4/5, `programme_complete=false`, next slice 5. Prior Run F steps and independent Run E untouched.
- **Validation and evidence:** unchanged fixture validator returned `fixture_valid=true`, `completed_steps=4`, `total_steps=5`; Git whitespace check passed and both JSON files parsed. See `evidence/astra-l13-20261119-f/run_f_worker_slice4.md`. The follow-up publication receipt records the exact remote SHA and GitHub readback.
- **Publication readback:** substantive fixture/evidence commit `94ef1ea977cbb37e644566dbe75596536543bd0b` was pushed; `git ls-remote` matched exactly. Independent GitHub fetch pinned to that SHA confirmed four Run F results, fourth chat ID and totals, 4/5 state, evidence file and PROGRESS.md. Run E state was independently read back unchanged at 3/5.
- **Next action:** the sole existing Run F controller consumes the final published `TASK_COMPLETE` and launches precisely one distinct saved successor for slice 5. G4 and Run F terminal assessment remain open until fifth worker, four actual handovers and terminal `STOP_FINISHED`.

## L13 Run F third saved worker — slice 3 of 5, 19 November 2026

- **Assignment and observed ID:** Run F `astra-l13-20261119-f`, third distinct saved Project worker `6afe468d-80f8-83ec-9058-1b8aba066115`. Read-only Windows Chrome UIA matched this exact chat ID, the nominated Project ID and this worker's in-progress assistant content. The pre-existing external controller (Windows PID 6684) recorded three distinct IDs, two consumed `TASK_COMPLETE` turns, no pending action and no halt; this worker neither operated nor duplicated it.
- **One slice only:** from published source `99b7577e85a9b04c7dd14a62bb4078ff1ba8352b`, aggregated the unchanged Run F probe `fixture-34f40d483630871b`: alpha 2/22, beta 2/5, gamma 2/6, six rows and total value 33. Appended the third result; updated state to 3/5, `programme_complete=false`, next slice 4. All prior results and Run E remained unchanged.
- **Verified publication:** substantive fixture and evidence commit `e88ad13f11f2b6a3ae96a95b95b7107fb69f0ff6` was pushed to the nominated branch, and `git ls-remote` returned this exact SHA. The original fixture validator returned `fixture_valid=true`, `completed_steps=3`, `total_steps=5`; staged `git diff --check` was clean. Independent GitHub pinned readback at `e88ad13` confirmed the three Run F results, state and `evidence/astra-l13-20261119-f/run_f_worker_slice3.md`. Run E state was also read back unchanged at 3/5.
- **Next action:** the existing single external Run F controller consumes this worker's final `TASK_COMPLETE`, then launches exactly one distinct saved successor for **slice 4 of 5**. Do not manually launch, Send, resume or operate another controller. G4 repeatability remains open pending all five validated Run F slices, four handovers and terminal observation.

## L13 Run F second saved worker — slice 2 of 5, 19 November 2026

- **Run and provenance:** `astra-l13-20261119-f` only; observed controller-recorded saved chat ID `6afe44f5-18cc-83ec-9c3c-0d19a51dcecb`, distinct from worker 1. Existing controller PID 6684 continues; this worker did not Send or start a controller. Starting published revision `e441598385e46d1c2809873732b8edb450a5227b`.
- **Computed result:** alpha 2/-6, beta 2/38, gamma 2/45; six rows and value total 77 from the unchanged second Run F probe. One appended result and updated state to 2/5, `programme_complete=false` and next slice 3; Run E and other tests unchanged.
- **Publication verified:** fixture and worker-evidence commit `9ed4e2c0ae3cbf2222473b10e2294c5b63f5adfb` was pushed, with matching `git ls-remote`. Independent pinned GitHub readback confirmed Run F `RESULTS.json` (two entries), `STATE.json` (2/5), this worker's evidence and `PROGRESS.md`. The unchanged fixture validator returned `fixture_valid=true`, 2/5; staged `git diff --check` passed after removing a trailing blank line in the new evidence.
- **Next action:** the **single existing external Run F controller** consumes this worker's final `TASK_COMPLETE` and launches exactly one saved successor for slice 3. Do not manually post or operate a second controller. G4 verdict remains open.

## L13 Run F first saved worker — slice 1 of 5, 19 November 2026

- **New independent five-chat run:** `astra-l13-20261119-f` was seeded from branch revision `743d35b0d233145e66df1c24073aaf307ec4a677`, with five distinct test inputs and initial fixture validation `fixture_valid=true`, 0/5. Setup publication `2f47a37e5f67c3ad88098213c2c4499fe7e7f156` was independently read back from GitHub. Existing Run E remains 3/5 and was not reset, resumed or modified.
- **Current worker and active controller:** saved Chat Succession Project ID `6afe4226-e4c8-83ec-b279-4716d52d1e56` positively observed via read-only Windows Chrome UIA. A separate fresh private Run F controller state was initialised with this chat, one distinct ID, cap five and no pending action/halt. The existing controller CLI was launched on Windows as PID 6684, polling every 20 seconds with no response deadline. Its initial logged UIA observation of this chat returned `WAIT` during the streaming response; no Send was attempted by this worker.
- **Substantive one-slice publication:** from first Run F probe, independently aggregated alpha 2/25, beta 2/16 and gamma 2/34; six rows, total value 75. Updated only Run F `RESULTS.json` and `STATE.json` to 1/5, `programme_complete=false`, next slice 2. Unchanged fixture validator returned valid 1/5 and staged whitespace check passed. Fixture/evidence commit `3c9fd2faa21be1dcba649abec0dd3432bef66444` was pushed, matching `git ls-remote`; independent pinned GitHub readback confirmed result, state and worker evidence.
- **Next action:** this first worker ends with one canonical completion marker only after publication. The already-running single external controller consumes that completed turn, verifies the remote result, and launches one distinct successor for slice 2. Complete all remaining slices and terminal stop before assessing Run F or G4. No manual successor is authorised from this worker.

## Controller polling, monitoring and composer focus — 19 November 2026

- The owner requested a 20-second default poll, an optional response deadline in the existing private JSON, a monitor output fix and a bounded focus check for the composer. Each confirmed Send starts a fresh response budget. Expiry saves a hold, and the existing dispatch and reconciliation paths still own Send.
- The CLI emits one final JSON result on stdout. UTC diagnostics on stderr record observation reasons, UI Automation and publication checks, and confirmed submissions. The private Run E launcher now uses the config and appends stderr to its local timing log. The optional deadline is unset in that launcher configuration pending an owner choice.
- Run E evidence places the delay before slice 2. Worker footers show 08:50, 10:41 and 10:47 Sydney time. The monitor restarted at 08:58:37 and recorded its parse failure at 10:48:38. The first handover lacks a timestamped observation trace, so the cause of the gap remains open. The Run E controller is still held at 3/5 with the next action prepared.
- Verification covered the existing integration suite, simulated polling, deadline and stdout behavior on Windows, and PowerShell parsing and simulated focus guards. Live Chrome focus and G4 repeatability remain open. Preserve the existing held run as evidence for future live verification.

## L13 Run E third saved worker — slice 3 of 5, 19 November 2026

- **Observed saved Chat Succession worker:** `6afe37c3-efcc-83ec-8644-1f418f439259`, from connected-browser read-only tab inventory in the nominated Project. Page content and completed-turn status were not established by that read-only inventory.
- **Published work:** source revision `dba5d1f130ea7d3b6bce178809a34ac840cf5621`; processed **only step 3** of Run E, using probe `fixture-f09529af81dda9da`. Alpha 2/29, beta 2/38, gamma 2/23; six rows and total 90. Previous Run E steps and earlier runs preserved. Updated fixture state to 3/5 with `programme_complete=false` and next slice 4.
- **Validation and verified GitHub publication:** original fixture validator `fixture_valid=true`, `completed_steps=3`, `total_steps=5`; staged Git diff whitespace check passed. Fixture commit `68188a6957bf1804e3f1b94cb764688205242d99` was pushed; `git ls-remote` matched its full SHA. Independent GitHub pinned readback confirmed `STATE.json`, `RESULTS.json`, `PROGRESS.md` and `evidence/astra-l13-20261119-e/run_e_worker_slice3.md`. The final verification note is this separate progress-only evidence update.
- **Next action:** the sole external controller verifies the completed worker status and published GitHub state, then launches exactly one new saved worker for slice 4. Do not operate or duplicate the controller from this worker. G4 remains open.

## L13 Run E second saved worker — slice 2 of 5, 19 November 2026

- **Saved Project worker ID:** `6afe362d-5088-83ec-8b45-afc15aba6b1d`, observed in the read-only connected-browser tab inventory and matching the one existing controller's current-chat state. Two distinct saved chat IDs were present; this worker did not operate the controller.
- **Completed next fixture slice:** from source branch HEAD `35db97a5f6b205768baa0cece0144592921215f8`, processed Run E step 2 only, probe `fixture-b4a02517e1ff83ab`. Alpha 2/40, beta 2/18, gamma 2/15; six records, overall 73. Published state now has 2/5, `programme_complete=false`, next slice 3.
- **Publication and checks:** fixture commit `d7f5a39a1653c06d4f661107cf84d6d3f0db3bd9` was pushed to the nominated branch; `git ls-remote` matched the full SHA. The unchanged fixture validator returned `fixture_valid=true`, `completed_steps=2`, `total_steps=5`; staged `git diff --check` passed. Independent pinned GitHub readback confirmed `STATE.json`, `RESULTS.json`, `PROGRESS.md` and `evidence/astra-l13-20261119-e/run_e_worker_slice2.md`. The previous observer timeout remains recorded and G4 is open.
- **Next action:** the sole external Run E controller consumes this worker's finished status, verifies remote state and launches one distinct worker for slice 3. Do not Send or start a second controller from this worker.

## L13 Run E monitoring timeout and read-only recovery — 19 November 2026

- The first Run E worker published validated slice 1/5. The Windows observer wrapper, a local serial caller of the existing controller, then hit its own 740-second timeout before the worker produced a completed final assistant status. This was an observation interruption, **not** a successful handover or a browser Send.
- The existing private controller still held exactly one saved chat, no consumed responses, no pending action and no halt. The operator corrected the wrapper polling/time limit and restarted observation against **the same persisted state**; no second controller, duplicate Send, manual chat continuation or successor was initiated.
- Evidence: `evidence/astra-l13-20261119-e/controller_observer_timeout.json`; Run E is **IN_PROGRESS**, but does not independently prove an uninterrupted repetition because the observation wrapper was restarted. G4 remains open.
- **Next action:** allow the original Run E controller to observe the first worker's final response and, if valid, complete the five-chat fixture without further interference. Preserve the monitor interruption in the final report; schedule a genuinely uninterrupted replacement repetition if needed for G4.

## L13 Run E first saved worker — slice 1 of 5, 19 November 2026

- **Current active assignment:** Run E (`astra-l13-20261119-e`) only. This first worker observed its actual saved Chat Succession Project conversation ID `6afe1bba-a8b0-83ec-b393-3017ea056dd2` using read-only authenticated Chrome UI Automation. The separate pre-existing Windows controller was observed with cap-five Run E state, one distinct saved chat, no pending action and no halt. This worker did not operate the controller.
- **Completed work:** Starting from GitHub branch `dc8c86efdc41c809d9c026838e4201e2b8ddeaaf`, processed exactly Run E slice 1: alpha count 2 / total 34, beta 2 / 31, gamma 2 / 11; six records, total 76. The published `STATE.json` has `completed_steps=1/5`, `programme_complete=false` and next task slice 2. Earlier Runs A–D were not modified.
- **Published fixture and evidence:** commit `52be4619d4587611e9f8c853a84dd8a700e2c002` pushed to `work/astra-succession-implementation-20261118`. The remote branch hash matched, and independent pinned GitHub readback confirmed `RESULTS.json`, `STATE.json`, and `evidence/astra-l13-20261119-e/run_e_worker_slice1.md`.
- **Checks:** unchanged fixture validator returned `fixture_valid=true`, `completed_steps=1`, `total_steps=5`; staged Git whitespace check passed. The isolated checkout initially lacked a Git author identity, so the first commit attempt failed before committing; the already-published branch author identity was reused for the successful single fixture commit without changing global Git configuration.
- **Next action:** the sole external controller consumes this worker's completed final status, independently verifies the published fixture and launches exactly one new saved Run E worker for slice 2. It must complete four automatic successors and five valid remote-published slices without intervention before Run E can support closing G4. This worker performed no Send, continuation, successor launch or second slice.

## L13 fresh uninterrupted repeat — Run E staged, 19 November 2026

- **Owner decision:** restart one complete unattended five-chat L13 repetition after the PC was switched off overnight. Keep historical Runs A/B (unattended PASS), C (assisted), and D (1/5 published) intact; do not reset or replay any prior state.
- **New independent run:** `astra-l13-20261119-e` in `succession-tests/astra-l13-20261119-e/`; fixture validator passed at 0/5. See `evidence/astra-l13-20261119-e/setup.json`.
- **Active assignment:** Run E only. Each distinct worker publishes exactly one slice with observed saved ID. The existing single external controller handles successor launches.
- **Next action:** Bootstrap the first worker in the existing authenticated Project; observe the saved chat ID and initialise **one fresh private Run E** cap-five controller; verify four automatic successors, five remote-published slices and `STOP_FINISHED` without intervention. Preserve all prior evidence.

## L13 Run D first saved worker — slice 1 of 5, 18 November 2026

- **Observed saved worker ID:** `6afd746b-6a30-83ec-a408-6a7408771beb` in the nominated Chat Succession Project, from read-only Chrome UI Automation address observation. This is chat identity evidence, not controller transport or completed-turn observation.
- **Source and work:** starting at branch commit `f058654e974b441d48f7eea6a9a444b217b999dd`, computed only Run D step 1: alpha 2/-7, beta 2/31, gamma 2/5, six rows/29 total. Used the live Run D repository probe and left Runs A/B/C unchanged.
- **Published fixture and evidence:** `succession-tests/astra-l13-20261118-d/` updated to one result, `completed_steps=1/5`, `programme_complete=false`, next task slice 2. See `evidence/astra-l13-20261118-d/run_d_worker_slice1.md`. Worker publication commit `002ad1a694eadf6786acae7fc7667a8f2f21c744` was pushed, and independent GitHub branch readback verified the exact state, result and evidence files at that revision; unchanged fixture validator returned valid 1/5 and staged Git whitespace check passed.
- **Next action:** the sole external controller independently verifies this worker's published slice and final status, then launches exactly one new saved Project worker for Run D slice 2. No worker-side controller action or successor launch. G4 remains open.

## L13 / G4 — Run D selected for the unattended repeat

**Active ChatGPT worker assignment is Run D only.** Read `succession-tests/astra-l13-20261118-d/INSTRUCTIONS.md`, then process and publish exactly one next slice from that fixture. Verify the publication and end with one canonical final status line. The external controller is the only actor that launches successors.

- Run D is an independent replacement for the assisted Run C. A and B already passed. Original Run C remains recorded as assisted. The new fixture verified at 0/5 with five distinct inputs and repository-only probes separate from the earlier runs.
- The operator bootstraps one chat in the nominated Project and starts one fresh controller with cap five. For G4, Run D must deliver five validated published slices, five distinct saved chats, four automatic successors, no material intervention, and `STOP_FINISHED`. Log any hold promptly.

## L13 closeout — two unattended passes and one assisted completion

**L13 did not meet its unattended acceptance criterion.** All three staged runs finished. Runs A and B passed unattended. Run C required a controller resume before its fifth saved chat. There is no active test worker assignment.

- Across the three runs, 15 distinct saved Project chats published 15 validated slices. The existing controller made all 12 successor launches. There were zero corrective prompts, same-chat continuations, manual successor launches, duplicate Sends or misroutes observed.
- In Run C, the fourth worker published its slice and finished. The controller held with the fifth-chat action still prepared after Windows UI Automation could not focus the new Project composer. The failed preparation reached no Send. The operator foregrounded the empty Project window and used the controller's existing resume operation. That controller sent the original pending pointer once and the fifth worker published its slice.
- All three private controller states reached `STOP_FINISHED` with no pending action. Run C's final remote state at `20f8ebc6869d` had `programme_complete=true` and `next_task=null`. The existing fixture validator passed against every pinned GitHub slice publication. Per-run evidence is linked from `evidence/astra-l13-20261118/setup.json`.
- G4 remains open pending a fresh unattended repetition. L01–L12 are recorded as PASS, L14 is optional and NOT_RUN, and L15 is recorded as PASS within its controlled-injection scope.

## L13 Run C fifth saved worker — terminal slice 5 of 5, 18 November 2026

- **Saved worker identity:** `6afd6fea-c214-83ec-b0ee-7781196b5a06` from connected browser read-only tab inventory under the nominated Chat Succession Project; saved-chat identity only, not completed-turn observation or controller transport.
- **Work:** Run C step 5 only from source branch revision `ee2c999d973225305220a15b7dccaa6b7b65ce5a`. Step-5 nonce `fixture-3fa244adf517a775`; alpha 2/34, beta 2/8, gamma 2/19, overall six rows/61. Five distinct saved chat IDs have five results. `STATE.json` is terminal with `completed_steps=5/5`, `programme_complete=true`, `next_task=null`.
- **Evidence:** `evidence/astra-l13-20261118-c/run_c_worker_slice5.md` and fixture; original validation, Git whitespace, remote push and pinned readback are checked separately. Runs A/B and earlier Run C slices unchanged.
- **Next action:** the sole existing external controller consumes this worker's final status, verifies terminal publication, observes `STOP_FINISHED` with no sixth chat, and writes Run C live transport evidence and three-run G4 assessment. This worker has not run the controller, sent messages, or concluded L13 PASS.

## L13 Run C fourth saved worker — slice 4 of 5, 18 November 2026

- **Saved worker identity:** `6afd6a75-8b94-83ec-ba02-94aeab6a1d92`, independently observed from the authorised read-only Chrome UI Automation window/address inventory in the nominated Chat Succession Project. This establishes saved conversation identity, not controller transport or completed-turn observation.
- **Useful work:** processed precisely Run C step 4 from the published `RUN.json` at starting branch commit `01f3ab753ab467b0d7cb5cd8ad68e0007683247a`. Step-4 nonce `fixture-c0855ac9e599e358`; alpha 2/21, beta 2/46, gamma 2/35, combined six rows/102. `RESULTS.json` has four distinct worker results; `STATE.json` now records 4/5, `programme_complete=false`, and next task slice 5.
- **Evidence:** `evidence/astra-l13-20261118-c/run_c_worker_slice4.md` and the fixture. Run C's previous three results and Runs A/B are unchanged. Git validation, push and remote readback are separate verification steps; no three-run L13 verdict is inferred from this worker.
- **Next action:** the existing external controller alone consumes this worker's canonical completion marker, independently verifies the fixture publication and launches the fifth distinct Run C saved Project worker for slice 5 only. This worker has not run the controller, posted a message, launched a successor or modified its private state.

## L13 Run C third saved worker ? slice 3 of 5, 18 November 2026

- **Saved worker identity:** `6afd68e9-b2d8-83ec-b803-36ccda13c6d9`, observed from the browser's read-only tab inventory in the nominated Chat Succession Project. This proves saved chat and Project identity, not controller completed-turn or successor transport.
- **Work:** one next Run C slice only (step 3); alpha 2/29, beta 2/38, gamma 2/23, combined six rows/90. Source run probe `fixture-f09529af81dda9da`. Completed steps now 3/5, programme incomplete, next slice 4.
- **Evidence:** `evidence/astra-l13-20261118-c/run_c_worker_slice3.md` and published fixture state/results. Git publication/readback and fixture validation are checked as separate operations; no three-run L13 verdict follows from one worker.
- **Next action:** the sole existing external controller consumes this worker's one canonical completion marker, verifies the published fixture, and launches the fourth distinct saved Run C worker for slice 4 only. Do not run the controller, send messages, launch a successor or touch its private state from this worker. Runs A/B remain untouched.

## L13 Run C second saved worker — slice 2 of 5, 18 November 2026

- **Saved worker identity:** `6afd6699-9f68-83ec-8fd8-06fbf9b37f4f`, observed in the authorised read-only browser tab inventory under the nominated Chat Succession Project. This establishes saved chat identity only, not controller transport or a completed response event.
- **Published fixture:** source `18db7d7666741c5dae271463684a2ffbab2f410a`; fixture commit `b3bf6333cd1f031cdb42582b38c13f195cb600da` pushed to `work/astra-succession-implementation-20261118`. Independent pinned GitHub readback confirmed exact Run C STATE.json, RESULTS.json and `evidence/astra-l13-20261118-c/run_c_worker_slice2.md`. The original validator passed: `fixture_valid=true, completed_steps=2, total_steps=5`; Git whitespace checks clean.
- **Work completed:** Run C slice 2 only, six rows: alpha 2/40, beta 2/18, gamma 2/15, combined total 73. Two distinct saved worker IDs have two published results; `completed_steps=2/5`, `programme_complete=false`, next task slice 3. Run C slice 1 and completed Runs A/B were not altered.
- **Next action:** the sole existing external controller consumes this worker's final completion marker, verifies remote fixture status and launches the third distinct saved Run C worker. No worker-side continuation, controller action or successor launch. Run C and G4 remain pending; no three-run PASS is claimed.

## L13 Run C first saved worker — slice 1 of 5, 18 November 2026

- **Saved worker identity:** `6afd651b-db04-83ec-a386-4d709438d383`, from the read-only browser tab inventory, matched to the nominated Chat Succession Project. This does not establish completed-turn or controller transport.
- **Work:** from source remote revision `d433fd337cf3e4d2ece3b8db1381cd1a3e770780`, processed only Run C slice 1. Six rows: alpha 2/34, beta 2/31, gamma 2/11; combined total 76. Run C is now `completed_steps=1/5`, `programme_complete=false`, next task slice 2. Runs A and B unchanged.
- **Publication and verification:** `9752a6502b44bfb2e59beec29613ed937744a302`, pushed to the nominated branch; remote `git ls-remote` matched. Existing fixture validator returned `fixture_valid=true, completed_steps=1, total_steps=5`; staged `git diff --check` was clean. Independent pinned GitHub readback confirmed `STATE.json`, `RESULTS.json`, `PROGRESS.md` and `evidence/astra-l13-20261118-c/run_c_worker_slice1.md` with the expected worker ID, probe and category totals.
- **Next action:** the sole external controller consumes this worker's final status, verifies the remote fixture and launches the second distinct saved Run C worker. No worker-side controller action or successor launch. Run C and G4 remain pending.

## L13 Run B verified — 2/3 live repetitions complete

**Active ChatGPT worker assignment is Run C only.** Read `succession-tests/astra-l13-20261118-c/INSTRUCTIONS.md`, then process and publish exactly one next slice from that fixture. Read the current branch, finish with one canonical final status line, and leave all controller actions to the external operator.

- Run B reached five distinct saved Project chats with four automatic successor launches. There were zero same-chat continuations, corrective prompts, manual successors, duplicate Sends, misroutes or controller holds observed.
- The existing fixture validator passed against each of five pinned GitHub publications. The final remote state at `ad664d099d52` had `programme_complete=true` and `next_task=null`. The controller returned `STOP_FINISHED` with no pending action. See `evidence/astra-l13-20261118-b/live_record.json`.
- The operator will bootstrap Run C once and use a new private cap-five controller state. The finished run and its evidence remain available for inspection.

## L13 Run B fifth saved worker — terminal slice 5 of 5, 18 November 2026

- **Actual saved worker:** `6afd6318-d2c4-83ec-9fc5-99657da67de1`, observed in the connected browser's read-only tab inventory under the nominated Chat Succession Project. This is saved-chat identity evidence only; no completed-turn or external-controller transport observation is claimed.
- **Published terminal fixture:** `a855bfac062ba1eb27e3872f6fad03f1aa31c12d`, committed and pushed on `work/astra-succession-implementation-20261118` from `855016bb98e3688f76ce9a04a6e2064624eb7b9f`. Remote `git ls-remote` matched, and independent pinned GitHub readback verified the exact Run B `STATE.json`, `RESULTS.json` and `evidence/astra-l13-20261118-b/run_b_worker_slice5.md`.
- **Useful work:** normalised the six Run B step-5 rows only: alpha count 2/total 34; beta 2/8; gamma 2/19; combined total 61. All five distinct worker IDs now have five published results. Run B `completed_steps=5/5`, `programme_complete=true`, `next_task=null`; prior Run B results and Runs A/C unchanged.
- **Validation:** original fixture validator returned `fixture_valid=true, completed_steps=5, total_steps=5`; Git whitespace check clean. This proves the terminal worker fixture publication, **not** external Run B `STOP_FINISHED` or three-run L13 PASS.
- **Next action:** the **existing external controller alone** consumes this worker's single final completion marker, verifies this published terminal programme and observes `STOP_FINISHED` with exactly five saved IDs and four automatic successors. Record actual Run B transport and terminal evidence. Then follow the nominated plan for the independent Run C repetition; no worker-side controller operation, successor launch, continuation or other run modification occurred.

## L13 Run B fourth saved worker — slice 4 of 5, 18 November 2026

- **Actual saved worker:** `6afd6197-7d70-83ec-b2b4-ae597adbae69`, verified by read-only Chrome UI Automation of the current saved Chat Succession Project conversation address. This proves the worker's saved-chat/Project identity, not completed-turn observation or controller transport.
- **Published fixture checkpoint:** `5bb570fb325211d366b12c42d85bb7308af6e2c0`, committed and pushed on `work/astra-succession-implementation-20261118` from source `2f2efeeef6554cfff3d7f5338c31cb9a121dd084`. Remote `git ls-remote` matched, and independent pinned GitHub readback verified `STATE.json`, `RESULTS.json` and `evidence/astra-l13-20261118-b/run_b_worker_slice4.md` including the worker ID and step-4 probe.
- **Useful work:** normalised only six Run B step-4 rows: alpha count 2/total 21; beta 2/46; gamma 2/35; combined total 102. Four distinct saved workers have four published results. `completed_steps=4/5`, `programme_complete=false`, next task slice 5. Earlier results and Runs A/C unchanged.
- **Validation:** the original fixture tool returned `fixture_valid=true, completed_steps=4, total_steps=5`; Git whitespace checks clean; staged three-file commit and push succeeded. This is not Run B or three-run L13 PASS.
- **Next action:** the **existing external controller alone** consumes this worker's single final completion marker, verifies the published handover and launches the fifth distinct saved Run B worker for exactly slice 5. No worker-side controller operation, continuation, successor or additional slice was performed. Run B transport evidence and terminal programme state remain to be observed.

## L13 Run B third saved worker — slice 3 of 5, 18 November 2026

- **Actual saved worker:** `6afd5ff2-8f6c-83ec-b143-c7e715fdbb2b`, observed in the connected browser tab inventory at the nominated Chat Succession Project conversation URL (last opened 19:20 Melbourne). This proves saved Project/chat identity, not response completion or controller transport.
- **Verified fixture publication:** `a9c2efc0d825d28798e201d2ecd710e236017b4c`, committed and pushed from the independent clean worker checkout based on `edf856205e853a114c9504e5488701aeb308dfe0`. Remote Git HEAD matched the commit; independent pinned GitHub readback verified `STATE.json`, `RESULTS.json` and `evidence/astra-l13-20261118-b/run_b_worker_slice3.md`, including saved worker ID and the step-3 probe.
- **Useful work:** processed only RUN.json step 3 (six rows): alpha count 2/total 29, beta 2/38, gamma 2/23, combined total 90. Three distinct workers have published three results. `completed_steps=3/5`; `programme_complete=false`; next task is slice 4. Previous results and Runs A/C unchanged.
- **Validation:** original fixture validator reported `fixture_valid=true, completed_steps=3, total_steps=5`; Git whitespace check clean, commit/push successful, remote pinned files matched. This is not Run B or three-run L13 PASS.
- **Next action:** the **existing external controller alone** consumes this worker's single canonical final completion marker, verifies handover and launches the fourth distinct saved Run B worker for exactly slice 4. No worker-side controller action, successor, same-chat continuation or additional slice was performed. Controller transport and terminal Run B evidence remain to be observed.

## L13 Run B second saved worker — slice 2 of 5, 18 November 2026

- **Actual saved worker:** `6afd5e97-dc08-83ec-9725-1d5ce61b3183`, observed by read-only connected browser tab inventory at the exact nominated Chat Succession Project conversation URL. This observation establishes the saved chat and Project identity, not response completion or controller transport.
- **Published fixture checkpoint:** `39a65a626b872ab882b3802578bbfee18aa7e182`, pushed on `work/astra-succession-implementation-20261118` from starting revision `e3c7d166cc42b91fdd7e089c01836be814df5297`. Independent pinned GitHub readback confirmed `STATE.json`, `RESULTS.json`, and `evidence/astra-l13-20261118-b/run_b_worker_slice2.md` with matching worker ID and step 2 probe.
- **Useful work:** normalised six step-2 rows: alpha count 2/total 40, beta 2/18, gamma 2/15, combined total 73. Only Run B slice 2 was processed; completed steps now `2/5`, next task slice 3, `programme_complete=false`. Run A and Run C were not modified.
- **Checks:** original fixture validator returned `fixture_valid=true, completed_steps=2, total_steps=5`; unstaged and staged Git whitespace checks passed. Git push returned success and remote pinned contents matched. This is a worker publication, not Run B or three-run L13 PASS.
- **Next action:** only the existing external controller consumes this worker's final completion marker, verifies this published handover and launches the third distinct saved Run B worker for exactly slice 3. This worker must not send, launch or operate the controller. External-controller launch and terminal evidence remain unobserved here.

## L13 Run B first saved worker — slice 1 of 5, 18 November 2026

- **Actual saved worker:** `6afd5cc9-f314-83ec-a31d-7b08037957d3`, independently identified in the nominated Chat Succession Project through the connected browser tab inventory and existing Windows UIA read-only Observe mode. The adapter reported streaming at observation; it was not a completed-turn test.
- **Published checkpoint:** `be235c810f983a60cbab71623956cec2dfef4f4c`, pushed to `work/astra-succession-implementation-20261118` and independently read back on GitHub at that pinned commit for `STATE.json`, `RESULTS.json` and `evidence/astra-l13-20261118-b/run_b_worker_slice1.md`. Input revision was `5cb3db77b9ab3d75f5c487f75471b0443e4fc735`.
- **Useful work:** only Run B slice 1 was processed: six rows, alpha 2/34, beta 2/31, gamma 2/11, combined total 76. Updated Run B state to `completed_steps=1/5`, `programme_complete=false`, next task slice 2; Runs A and C remain untouched.
- **Checks:** original fixture validator returned `fixture_valid=true, completed_steps=1, total_steps=5`; staged whitespace check passed; pinned GitHub contents matched the worker ID, probe and totals. This is one worker checkpoint, **not** Run B or full L13 repeatability PASS.
- **Next action:** only the existing external controller consumes this worker's final completion marker, verifies the published handover and launches the second distinct saved Run B worker for exactly slice 2. This worker must not launch a successor, continue the same chat or process another slice.

## L13 Run A verified — 1/3 live repetitions complete

**Active ChatGPT worker assignment is Run B only.** Read `succession-tests/astra-l13-20261118-b/INSTRUCTIONS.md`, then process and publish exactly one next slice from that fixture. Read the current branch, finish with one canonical final status line, and leave all controller actions to the external operator.

- Run A reached five distinct saved Project chats with four automatic successor launches. There were zero same-chat continuations, corrective prompts, manual successors, duplicate Sends, misroutes or controller holds observed.
- The existing fixture validator passed against each of five pinned GitHub publications. The final remote state at `73b495e960a6` had `programme_complete=true` and `next_task=null`. The controller returned `STOP_FINISHED` with no pending action. See `evidence/astra-l13-20261118-a/live_record.json`.
- The operator will bootstrap Run B once and use a new private cap-five controller state. The finished run and its evidence remain available for inspection.

## L13 Run A fifth saved worker — slice 5 of 5, 18 November 2026

- **Actual saved worker:** `6afd58e7-3934-83ec-ae7c-fd24df740e51`. The existing external controller's persisted read-only Run A state listed this as current and recorded five distinct saved chat IDs. Independent invocation of the existing Windows Chrome UIA adapter in Observe mode positively matched the same saved conversation and nominated Chat Succession Project. The worker did not invoke Send, control the successor loop or modify its private state.
- **Published fixture commit:** `eb3dad69c2092c0c699e5d6552e6494c5812c2f4`, pushed to `work/astra-succession-implementation-20261118`. GitHub remote readback confirms five result entries, the fifth chat ID, `completed_steps=5/5`, `programme_complete=true` and `next_task=null`. Starting source revision was `ceb258ad9c5e5aa33124063f6d28ed3c76064ad3`.
- **Useful work:** independently processed only RUN.json slice 5: alpha count 2/total 34, beta 2/8, gamma 2/19; combined six rows and total 61. Earlier four fixture entries and Runs B/C were unchanged.
- **Checks:** existing fixture validator returned `fixture_valid=true, completed_steps=5, total_steps=5`; staged Git diff whitespace check passed. Evidence: `evidence/astra-l13-20261118-a/run_a_worker_slice5.md`.
- **Next action:** **only the existing external controller** consumes this worker's one canonical final completion marker, verifies the published terminal programme and records `STOP_FINISHED` with exactly five saved worker IDs and four automatic successors. The full Run A transport verdict is pending this observation. Then independently repeat L13 with Runs B and C; do not treat one five-chat fixture as the three-run L13 PASS. The worker must not launch or operate a successor.

## L13 Run A fourth saved worker — slice 4 of 5, 18 November 2026

- **Actual saved worker:** `6afd572e-73d8-83ec-9bf7-ba08380a6861`, matched by the existing external controller's persisted fourth-chat ID and independently confirmed via the existing read-only Windows UIA observation of the nominated Project conversation. The fourth saved chat was launched by the controller, not this worker.
- **Published fixture commit:** `eaec57557c9fc1d3a352828dbb416c72b70da43e`, successfully pushed and independently read back by pinned GitHub ref for STATE.json, RESULTS.json and `evidence/astra-l13-20261118-a/run_a_worker_slice4.md`. Initial working revision was `8bda40da46271d424e8c3035e89ac58da17f8520`.
- **Useful work:** processed only RUN.json slice 4, normalising six rows: alpha count 2/total 21, beta 2/46, gamma 2/35; combined count 6 and total 102. The new result records this worker's actual saved ID and the current step-4 probe. State is `completed_steps=4/5`, `programme_complete=false`, next task slice 5. Earlier results and Runs B/C were unchanged.
- **Checks:** fixture validator returned `fixture_valid=true, completed_steps=4, total_steps=5`; unstaged and staged Git diff checks passed. Pinned remote STATE.json and RESULTS.json were verified independently after the successful push. First commit attempt failed before committing because the new isolated checkout lacked local author identity; the worker reused the verified identity from the earlier worker checkout and successfully committed/pushed without changing global Git configuration.
- **Next action:** only the **existing external controller** may consume this worker's one canonical final completion marker, verify published programme state and launch the fifth distinct Run A saved worker for slice 5. Do not launch a successor from this worker. Run A's five-chat verdict remains pending; Runs B/C remain staged and untouched.

## L13 Run A third saved worker — slice 3 of 5, 18 November 2026

- **Actual saved worker:** `6afd5556-f9c0-83ec-975d-363ed733db3b`, independently matched by the running external controller's persisted saved-chat state and a read-only Chrome UIA target observation in the nominated Project. The third chat was launched by the existing controller, not by the worker.
- **Published fixture commit:** `3af7c82fc2140634efeb6e78ddfa5dd2b850d2ab`, pushed to the nominated branch and independently read back by pinned GitHub ref (RUN A STATE.json, RESULTS.json, evidence). Starting source was `5f91f52cdd671d715725e3a73abfdb92eed6e3f9`.
- **Useful work:** processed only six rows in step 3: alpha 2/29, beta 2/38, gamma 2/23; combined count 6 and total 90. RESULTS.json records the current real saved worker ID and step-3 RUN.json probe; state is `completed_steps=3/5`, `programme_complete=false`, next task slice 4.
- **Checks:** existing fixture validator returned `fixture_valid=true, completed_steps=3, total_steps=5`; `git diff --check` and staged-diff check passed before commit. Remote pinned STATE.json and RESULTS.json matched the calculated values and saved ID. Evidence: `evidence/astra-l13-20261118-a/run_a_worker_slice3.md`.
- **Next action:** only the **existing external controller** may consume this worker's one final canonical completion marker, verify the published programme state and launch the fourth distinct Run A saved worker for slice 4. This worker must not launch a successor. Run A's five-chat verdict remains pending; Runs B/C are staged and untouched.

## L13 Run A second saved worker — slice 2 of 5, 18 November 2026

- **Actual saved worker:** `6afd5379-92c4-83ec-8297-d60011fd0c2e`, independently confirmed by read-only Chrome UIA in the nominated Project. The existing controller had launched this second saved chat; the worker did not send, launch, reset or modify the controller.
- **Published fixture commit:** `9982cd25e087ac569b0e5cdf9ebba5ef6de19e6e`, pushed from the dedicated worker checkout; GitHub ref and pinned remote RESULTS.json, STATE.json and worker evidence were read back successfully. The source revision was `3b93d64423ce5e5f0fdd8de359343d196b57fc4a`.
- **Useful work:** calculated only slice 2 from current RUN.json. Six normalised rows: alpha 2/40, beta 2/18, gamma 2/15; total 73. RESULTS.json records this actual worker and step-2 repo probe; state is `completed_steps=2/5`, `programme_complete=false`, and the next task is slice 3.
- **Validation:** existing fixture tool returned `fixture_valid=true, completed_steps=2, total_steps=5`. `git diff --check` and cached-diff check passed; remote pinned readback agreed with the computed totals and observed ID. Evidence: `evidence/astra-l13-20261118-a/run_a_worker_slice2.md`.
- **Next action:** the **sole existing external controller** observes this second worker's one unambiguous final completion marker, verifies current published programme state and launches the third distinct Run A saved worker for slice 3. The worker must not launch a successor. Run A's five-chat repeatability verdict remains pending; Runs B/C remain staged and untouched.


## L13 Run A first saved worker ? slice 1 of 5, 18 November 2026

- **Run A worker identity:** browser UI Automation read-only address of the authenticated Chat Succession Project conversation showed saved ID `6afd5272-342c-83ec-b108-134d391b3577`. This is the first observed Run A worker, not a simulated conversation.
- **Published-work candidate:** independently calculated only the first six fixture rows, yielding alpha count 2/total 34, beta 2/31, gamma 2/11. Updated only Run A RESULTS.json and STATE.json, leaving `completed_steps=1/5`, `programme_complete=false` and the next task at slice 2. Existing fixture validator returned `fixture_valid=true` and `git diff --check` passed locally.
- **Control boundary:** no same-chat continuation, browser Send, successor launch, private controller state change or Run B/C mutation was performed by this worker. This worker publication alone does not constitute an L13 five-chat result.
- **Next action:** after verifying the remote publication and consuming this worker's unambiguous final status, the **sole external controller** uses its Run A cap-5 state to launch the next distinct saved worker for slice 2. Verify real saved IDs and remote state at every step; stop after five published slices and four successors. Runs B/C remain staged.
- **Evidence:** `evidence/astra-l13-20261118-a/run_a_worker_slice1.md`.

## L13 pre-bootstrap recovery — Run A selected, 18 November 2026

- The fresh authenticated Chrome Project window inherited the existing one-line draft. The operator verified a private local backup against the live editor and cleared only the fresh composer. Both original Project windows retained the exact draft at readback. The fresh Project composer had no attachments and no enabled Send button. See `evidence/astra-l13-20261118/bootstrap_recovery.json` for the observation.
- **Active worker assignment: Run A** at `succession-tests/astra-l13-20261118-a/INSTRUCTIONS.md`. Each saved worker completes and publishes one next slice on its first turn. It uses the canonical final status line after validating remote publication. The external controller alone handles successors. Runs B and C stay staged until selected.
- This checkpoint clears the pre-bootstrap hold. Three fixtures independently validated at 0/5. No Run A worker or controller had started at this checkpoint. The operator now bootstraps one initial saved worker and starts the existing controller with cap 5.

## L13 pre-bootstrap HOLD — existing private Project draft, 18 November 2026

- **L13 BLOCKED BEFORE START, not a five-chat reliability verdict.** Three independent five-slice fixtures remain valid at 0/5, and their seed checkpoint is published at commit 95122d34eaaee9cd445405a25ff3a35581cbd0e6. No L13 saved worker or private controller has been created.
- **Observed Project condition:** two authenticated nominated-Project new-chat windows both presented an existing **nonempty unsent draft**, with a non-placeholder editable UIA Value and enabled Send. Its contents are private and not exported. The ordinary New chat control was attempted from an existing completed Project test conversation, but no independently empty nominated-Project composer appeared. This is a real browser-state blocker, not a focus gate, fixture failure, or test result.
- **Preservation:** no draft was typed over, cleared, selected for Send, or copied into GitHub; no initial worker message, successor, controller or fixture slice was executed. Evidence: evidence/astra-l13-20261118/prebootstrap_hold.json.
- **Next action:** once that draft is preserved or sent through normal account use, or an independently empty nominated-Project composer is available, bootstrap the Run A initial worker exactly once. Observe its saved conversation ID and initialise the pre-existing CLI in a fresh private state with five-chat cap. Then let only that controller launch four successors following verified publication. Runs B/C remain staged. L01–L12 PASS and L14–L15 NOT_RUN.

## L15 corruption and stale metadata — PASS (scoped injection), 18 November 2026

- **L15 PASS within its bounded test scope (8/8).** Two real fixture-validator runs on **disposable local copies** rejected (a) a tampered completed L09 result total and (b) a missing next-input `RUN.json` in staged L13 data. Both passed after restoring the original bytes. Nothing corrupt was pushed to GitHub or written into the staged live fixtures.
- **Six controller metadata injections:** stale last-worker attribution, string completion flag, finished-with-next-work contradiction, unfinished-without-next-task, unpublished handover and absent handover each produced **HOLD** from the imported reference controller. A separately injected valid published state with an explicit resume and fresh response produced a **prepared** successor action only, not a Send. No controller invoked a browser or launched a real successor.
- **Evidence boundary:** `evidence/astra-l15-20261118-a/run_corruption.py`, `observations.json` and `injection_record.json`. These are local copied-fixture and synthetic metadata tests, **not** live worker encounters or claims that a terminal marker verifies arbitrary engineering results. L15's outcome is labelled accordingly; no real ChatGPT worker was asked to repair corrupted remote input.
- **Next active leaf remains L13 Run A**, held before first worker because the nominated Project composer contains a genuine unsent private draft. Runs A/B/C remain 0/5; L14 is optional and NOT_RUN. No L09 terminal controller state was changed.

## L13 fixture setup — Run A staged (18 November 2026)

- **L13 NOT_RUN until live evidence exists.** Three separate five-slice repository-only fixtures have been seeded and independently validated at 0/5: `succession-tests/astra-l13-20261118-a`, `-b` and `-c`. The fixtures are bounded independent workloads; their preparation is **not** live five-chat evidence. See `evidence/astra-l13-20261118/setup.json`.
- **Next selected assignment after the pre-bootstrap hold: Run A** — `succession-tests/astra-l13-20261118-a/INSTRUCTIONS.md`. Each saved ChatGPT worker completes **exactly one next incomplete slice on its first turn**, validates and publishes RESULTS.json/STATE.json, verifies its remote commit, and ends with exactly one final completion status marker. The worker never runs the controller, sends messages, starts a successor, or works on B/C. Avoid stray standalone status words in the narrative: the controller must observe exactly one unambiguous final marker.
- **External controller:** bootstrap the initial worker in the authenticated Chat Succession Project, observe its real saved chat ID, initialise one **fresh private Run A controller** with distinct-chat cap **5**, and use its existing single Send actor. Require remote publication before each of the four automatic successor launches. After slice 5 publishes `programme_complete=true` and `next_task=null`, verify exactly five observed saved IDs, four successor launches, no duplicates/misroutes, then `STOP_FINISHED`.
- **Subsequent independent repeats:** after Run A finishes and its evidence is published, select Run B and then Run C with their own fresh controller states and fixture paths. Do not share run counters or reset any previously completed controller. The L13 result is PASS **only after all three five-chat live runs finish without manual corrective prompting during normal paths**. Record start/end times, actual validations, continuations, launches, interventions, and failures for each. A hold or unexpected early finish is recorded, not hidden.
- **Continuity:** L01–L12 PASS on the published branch; L13–L15 NOT_RUN. Preserve the finished L09 controller and separate L10–L12 synthetic evidence. Do not start a parallel successor outside the controller.

## L12 silence, tool loss and owner pause — PASS (synthetic injection), 18 November 2026

- **L12 PASS within controlled test-injection scope (6/6).** The existing reference controller and integration runner received delayed/absent response observations, a simulated missing UIA session, an injected preparation failure, an explicit owner pause while idle and an explicit owner pause with an already prepared action. All remained WAIT or HOLD as applicable; no Send occurred while held. Each persisted state survived restart and was inspectable through the established `inspect_state` fields.
- **In-flight action:** a pending `sending` action was deliberately marked uncertain in a temporary state and remained held across restart. Only an explicitly labelled **synthetic positive read-only receipt** allowed its adoption; no blind retry or new chat was performed. The controlled delay duration was measured in the evidence, but **no production owner silence deadline** was established or inferred from that short duration.
- **Evidence and limits:** `evidence/astra-l12-20261118-a/run_pause.py`, `observations.json` and `injection_record.json`. Six injected scenarios passed; zero real browser Sends, login attempts or ChatGPT session interruptions. L01–L12 PASS are separately classified by actual evidence type; L13–L15 remain NOT_RUN.
- **Next leaf: L13** — three independent five-chat *live* repetitions without manual correction during normal paths, against the existing Project. Preserve the finished L09 private state and avoid treating L12's injected holds as natural browser outages.

The earlier RDC publication blocker is retained in evidence/astra-l12-20261118-a/PUBLICATION_BLOCKER.md and resolved by this subsequently verified publication. Previous L01–L11 outcomes and L13–L15 statuses are unchanged.

## L11 publication failure regression — PASS (test-only), 18 November 2026

- **L11 PASS within its published test-failure scope.** A one-shot injected `PublishedStateError` in the existing runner's repository reader caused a `HOLD` before any Send or consumption of the completed worker response. The hold survived restart, with unique chat count unchanged. After an explicit owner-resume and simulated restored published read, the same response produced only a **prepared** successor action; browser dispatch remained disabled.
- **Actual local Git verification:** a *disposable detached worktree* created an unpushed local-only commit `1116fe71c2f77c4022a90cfb06ca557091ebabb4` changing the L09 fixture's completion flag. The existing `GitPublishedReader` fetched and read actual nominated remote commit `fd49e4df47029008264083dc989ab196af6b5d6e`, whose terminal fixture was unchanged. The reference controller correctly returned `STOP_FINISHED` rather than launching a successor based on the local-only change. The temporary worktree was removed and the disposable commit was **never pushed**.
- **Evidence boundary:** the outage was a *synthetic adapter injection*, not a real GitHub permission/network outage. The local-only Git commit was a real disposable local test, not published work. Both scenarios recorded **zero browser Send, zero real successor launches**, no account permission changes and no production controller operation. Evidence: `evidence/astra-l11-20261118-a/run_failure.py`, `observations.json`, `injection_record.json`. L01–L11 PASS now recorded with scenario types; L12–L15 remain NOT_RUN.
- **Next leaf: L12** — controlled delayed response/session-tool loss, and owner pause while idle and while prepared; no auto-login or Send while held.

## L10 status and streaming regression — PASS (synthetic observation injection), 18 November 2026

- **L10 PASS within the runbook's permitted injection scope:** 21/21 test-only Response observations were supplied to the existing imported Astra controller through `integration/runner.py` using ephemeral state, **not** to a new ChatGPT conversation. Cases covered incomplete/streaming and absent observations, missing/truncated/malformed/nonterminal statuses, repeated/conflicting markers, examples inside fenced/indented/quoted text and the observed L09-style ambiguous status pattern.
- **Actual results:** streaming or unavailable observations WAIT; ambiguous/malformed/code-example-only cases HOLD; valid final explicit or bare marker determines the prepared `CONTINUE_CURRENT`/`LAUNCH_SUCCESSOR` or terminal `STOP_FINISHED` route. The runner's dispatch was deliberately deferred for positives. **Zero browser prepare/Send calls, zero false `TASK_COMPLETE` from ambiguous cases, zero new chats or controller launches.** See `evidence/astra-l10-20261118-a/observations.json`, `run_injection.py`, `injection_record.json`.
- **Evidence boundary:** every case is labelled `SYNTHETIC_ADAPTER_FAULT_INJECTION`; this is **not** proof that 21 live ChatGPT responses naturally exhibited these behaviours. No real semantic classifier was used, the optional shadow/confusion matrix is **NOT_RUN**, and automatic semantic fallback remains disabled. L09's previous live streaming observations are contextual, not new L10 evidence.
- **Continuity:** cumulative results sheet records L01–L10 PASS with L10's synthetic scope identified; L11–L15 remain NOT_RUN. **Next leaf: L11**, controlled test-only publication/tool failure or disposable branch conflict; validate that unpublished work cannot cause a successor Send.

## L09 final live verdict — PASS (owner-assisted), 18 November 2026

- **All three L09 fault boundaries verified live:** durable `sending` then positive **before-click no-Send/rearm**; **after-click successor acknowledgement loss**, adopted once from the actual new saved Project ID; and **after-click same-chat continuation acknowledgement loss**, adopted once without a new chat. Unknown outcomes held until read-only reconciliation; no blind retry, duplicate Send or parallel controller.
- **Explicit owner intervention:** the successor's first status was ambiguous and the existing controller correctly held. One recorded corrective owner/operator message to the *same* successor (under the existing private controller lock) produced a fresh exact one-line `CHAT_STATUS: NEED_MORE_TIME`; the same private controller then resumed and completed the planned after-click continuation. This was assisted recovery, **not** unattended repeatability.
- **Remote work and terminal check:** first worker published slice 1 at `20200223d4a384aa00cd10ed33b20e557dea4bae`; second worker published slice 2 at `eedd2038278ff2371bd02d3571836c8a853b8b4e`. Independent verification of that pinned remote fixture yielded `fixture_valid=true`, `completed_steps=2/2`, `programme_complete=true`, `next_task=null`. The external controller consumed the successor's final `TASK_COMPLETE` and returned **`STOP_FINISHED`** with `unique_chat_count=2`, `pending_action=null`, `halted=programme_finished`. Exactly one successor launch and two controller continuations; no third saved chat.
- **Evidence:** `evidence/astra-l09-20261118-a/live_record.json` and `operator_recovery_result.json`, with prior fault/hold records preserved. The cumulative live sheet records L09 PASS and L01–L08 remain unchanged. Private controller state remains outside GitHub.
- **Next leaf: L10** — streaming/truncated, missing/conflicting status and code-example cases under Leaf 06. Preserve the finished L09 state; label any synthetic observation injections explicitly and do not infer automatic semantic fallback.

## L09 successor fixture slice 2 — worker publication, 18 November 2026

- **Worker output:** the same saved successor `6afd3221-f970-83ec-9889-1d09b1762a5f` has received the exact continuation after the externally controlled after-click recovery. It processed only the second `astra-l09-20261118-a` fixture slice from published RUN.json, independently aggregating alpha 2/40, beta 2/18, gamma 2/15 (six rows, total 73). Appended RESULTS.json and made STATE.json terminal with `completed_steps=2/2`, `programme_complete=true`, `next_task=null`. See `evidence/astra-l09-20261118-a/successor_worker_slice2.md`.
- **Separate external controller evidence:** existing private controller recorded an injected after-click same-chat `CONTINUE_CURRENT` as uncertain; subsequent read-only reconciliation returned `WAIT`, with the same saved ID, unique-chat count 2, no pending Send and no hold. Worker did not invoke a Send or launch a successor. That controller's final terminal STOP_FINISHED readback and L09 PASS adjudication remain separate operator tasks, not worker claims.
- **Next action:** the sole external controller consumes this worker's final unambiguous TASK_COMPLETE response, independently validates the newly published remote terminal fixture, verifies STOP_FINISHED with exactly two saved chats and no third launch, then records full L09 verdict and next L10 work.

## L09 live test held — ambiguous successor first-turn status, 18 November 2026

- **L09 BLOCKED, not PASS.** Its first-worker continuation and positive-no-click recovery were observed, and the successor after-click acknowledgement-loss case was observed and reconciled once. The first worker published slice 1/2 at `20200223d4a384aa00cd10ed33b20e557dea4bae`. The sole external controller adopted successor saved chat `6afd3221-f970-83ec-9889-1d09b1762a5f` once, unique-chat count **2**, pending null, no duplicate launch. L01–L08 remain PASS and the live fixture remains 1/2.
- **Specific current blocker:** the successor's first completed assistant response `uia-turn-1-775697475c9fbc793a56` ended with the canonical `CHAT_STATUS: NEED_MORE_TIME` marker but the UIA-flattened response also contained an earlier standalone `NEED_MORE_TIME` Text leaf in its narrative. The unchanged reference controller correctly held with `halted="Repeated, conflicting or nonterminal status"`; it consumed the ambiguous event, left pending null and did **not** send the planned same-chat continuation. Do not claim a new continuation or work slice, bypass the status parser, or launch a replacement successor. Evidence: `evidence/astra-l09-20261118-a/successor_first_turn_ambiguity.json`.
- **Required recovery within the same L09 run:** obtain a **new**, unambiguous assistant response in that **same saved successor chat** containing only one canonical final status marker and no standalone status keywords earlier in the message. An authorised owner/operator corrective message is needed because the existing controller is deliberately held and cannot initiate another continuation. Then resume the **same private controller** and process the new response; inject the prescribed after-click fault on one same-chat continuation, reconcile it read-only, allow slice 2 publication and verify terminal STOP_FINISHED. No second controller, no blind retry and no state reset.
- **Evidence boundary:** the standalone earlier status token is established in the UIA accessibility text; whether it appeared as an independent visual paragraph is not independently authenticated. The controller's conservative hold is supported. The L09 cumulative result is BLOCKED; the after-click same-chat variant is NOT_EXECUTED and L10–L15 remain NOT_RUN.

## L09 after-click successor adopted; successor first-turn inspection pending — 18 November 2026

- **L09 IN_PROGRESS, not PASS.** The first L09 worker at saved chat `6afd2e8f-606c-83ec-a47b-4d6783bd711c` published fixture slice 1/2 at commit `20200223d4a384aa00cd10ed33b20e557dea4bae`. Independent pinned remote worktree verification: `fixture_valid=true`, `completed_steps=1/2`, `programme_complete=false`; slice 2 is unmodified.
- **Live after-click successor fault verified.** The first controlled attempt held before typing (no Send); read-only reconciliation found no posted message and explicit positive no-Send evidence rearmed the exact pending action. A minimal change to the same UIA adapter now writes directly to the target editor's ValuePattern, avoiding the irrelevant Windows foreground. On the second single controlled attempt, `ASTRA_L09_FAULT=after_click` actually invoked Send once and deliberately lost acknowledgement. The controller persisted `uncertain`; read-only reconciliation adopted the exact posted standard short pointer in new saved nominated-Project chat `6afd3221-f970-83ec-9889-1d09b1762a5f` **once**. Unique-chat count is now **2**, pending null; no duplicate successor Send. Evidence: `evidence/astra-l09-20261118-a/after_click_successor_observation.json`.
- **Immediate next task — for successor worker, not controller:** the new saved chat's **first response** must follow `succession-tests/astra-l09-20261118-a/INSTRUCTIONS.md`: inspect published RUN/STATE/RESULTS, perform **no fixture edit or controller operation**, and finish with exactly one `CHAT_STATUS: NEED_MORE_TIME`. The external operator/controller alone handles continuation and successor routing. Do not repeat the already completed L09 first-worker/reconciliation operations. A premature `TASK_COMPLETE` without independently published fixture work is not an authorised successful handover.
- **Then:** use the existing single private L09 controller to inject after-click lost acknowledgement on one `CONTINUE_CURRENT` for the new chat; reconcile the exact posted message read-only, preserving two unique chat IDs. Only after that continuation should the second worker complete/publish slice 2, followed by terminal STOP_FINISHED. L01–L08 PASS unchanged and L09 cumulative row remains NOT_RUN until all required live cases are independently verified.

## L09 first live before-click case — observed and repaired, 18 November 2026

- **L09 overall IN_PROGRESS, not PASS.** Initial L09 first worker was bootstrapped in the nominated existing Chat Succession Project at actual saved conversation `6afd2e8f-606c-83ec-a47b-4d6783bd711c`, returned completed final `NEED_MORE_TIME` (response `uia-turn-1-743656fa12f7da2e6a01`) and left the two-slice test fixture untouched at 0/2. Fresh private Windows L09 controller initialised with unique count 1.
- Controlled `ASTRA_L09_FAULT=before_click` produced persisted `sending` then `uncertain` with detail that **UIA Send was never called**. On restart the original read-only reconciliation **incorrectly marked the standard continuation as posted**, although it existed only as a quotation in the assistant's reply. Root cause in `Find-PostedMessage`: it accepted exact text from assistant turns. **That first reconciliation result is invalid and is not evidence of a Send.**
- Corrected the existing UIA readback routine to accept matching text only within user-turn boundaries. In the actual saved conversation a no-send readback now returns `posted_message_observed=false` for `Okay, continue working.`, while the known original submitted user message returns `true`. Following explicit before-click no-invocation evidence, the same single private controller's misconfirmed pending action was repaired to `prepared CONTINUE_CURRENT` without Send; backup and state hashes recorded in `evidence/astra-l09-20261118-a/before_click_observation.json`. The unique chat count remains 1, no other Project was changed.
- **Next action:** validate and publish this readback correction, then dispatch the prepared continuation **once** using the existing L09 controller with no fault variable. Verify same saved chat and no duplicate, allow first worker to publish fixture slice 1, then proceed to the two published after-click fault/reconciliation variants. L01–L08 PASS unchanged; L09 cumulative row remains NOT_RUN until all required live cases are verified.

## L09 live fixture staged — 18 November 2026

- **L09 LIVE NOT_RUN; staged only.** Fresh independent test-only fixture `succession-tests/astra-l09-20261118-a` seeded with the unchanged imported Astra repo_fixture.py for exactly two work slices and validated at `completed_steps=0/2`. No worker wrote results, no controller state was initialised, no messages sent and no successor launched.
- The fixture's INSTRUCTIONS.md establishes the prescribed L09 sequence: first worker first emits NEED_MORE_TIME; operator exercises persisted-sending before-click injection, positive no-Send/rearm and one same-chat continuation; worker then publishes slice 1; existing controller injects after-click lost acknowledgement on one successor launch and reconciles the actual new saved ID; successor emits NEED_MORE_TIME, then controller injects after-click on continuation and adopts exact same-chat message once; successor publishes slice 2, then STOP_FINISHED. Each fault applies to one controlled CLI process and no parallel controller exists.
- **Next action:** verify fixture seed on remote branch, bootstrap first L09 worker in the existing authenticated Chat Succession Project with the short L09 fixture assignment, positively observe its saved conversation ID, and initialise a **fresh private** L09 state with cap 3. Do not recycle or reset any earlier controller. Wait for completed NEED_MORE_TIME before applying a before-click injection. If an initial Send outcome is uncertain, reconcile read-only rather than retrying.

## L09 scoped uncertain-Send hooks — offline preparation, 18 November 2026

- **L09 LIVE NOT_RUN.** Added only two fault points to the existing single Windows UIA Send path: environment variable ASTRA_L09_FAULT=before_click raises after persisted sending but before any UIA Send call; after_click sends once and raises immediately after Enter but before acknowledgement. Normal operation with the variable unset is unchanged. The controller/state machine, statuses and unique-chat counting were not modified.
- **Checks:** 22/22 integration tests passed, including four focused before-click/after-click/successor/same-chat recovery seam tests; unchanged Astra offline suite 119/119 passed; PowerShell UIA adapter parsed with zero errors. These are offline fault injections and parser checks, **not live L09 evidence**. No ChatGPT Send or successor was launched.
- **Evidence:** evidence/astra-l09-20261118-a/setup.md; modified integration/windows_backend.py and integration/uia_adapter.ps1 plus integration/tests/test_l09_faults.py. Cumulative L09 result remains NOT_RUN; L01–L08 PASS untouched.
- **Next action:** create a fresh scoped L09 fixture and private controller state, then conduct the three live cases under the **existing one controller**: positive before-click no-submission/rearm; after-click successor lost ack/restart/read-only adoption; after-click same-chat continuation lost ack/restart/read-only adoption. Preserve unknown outcomes and never automatically resend.

## L08 live active Project routing — PASS, 18 November 2026

- **L08 PASS (preparation-only, no Send).** Began with an ordinary authenticated ChatGPT composer active outside the nominated Project; Chat Succession was visible in the sidebar. Recorded the unrelated editor's UIA Value SHA-256 and length without exporting its content. The unchanged existing adapter's Prepare LAUNCH_SUCCESSOR opened the correct Chat Succession Project URL in a distinct Chrome window (saved chat ID null), independently read an empty editable buffer and found no attachment. No message was typed or sent.
- **Non-interference and nonempty Project:** the original unrelated composer retained exactly the same UIA Value SHA-256 and length and remained unsaved. Navigation worked with existing saved chats in the Project. Fourteen sidebar chat-action controls were visible, but are not represented as Project-only saved IDs. Separately published **L06** live-controller evidence shows two run IDs counted despite other Project chats already being present; the earlier counting observation is reused under Astra's combined-case option. L08 did not operate a new controller or increment a run count.
- **Evidence and limits:** evidence/astra-l08-20261118-a/live_record.json and validate_observations.py; supporting count evidence evidence/astra-l06-20261118-a/live_record.json. PASS covers correct destination preparation and nonempty Project behaviour; no post-Send delivery is claimed. L01-L07 PASS preserved and L09-L15 NOT_RUN.
- **Publication note:** Remote Desktop Commander timed out after creating local-only L08 commit 2f29e38. This remote L08 publication uses the existing connected GitHub Git API instead. The separate Ubuntu L08 working copy must be refreshed/reconciled before its next Git push; do not treat the local-only commit as the remote publication.
- **Next action:** Leaf 06 L09 — controlled uncertain Send and restart reconciliation using the existing single controller and scoped test hooks, without blind retries or new launch architecture.

## L07 final live composer regression — PASS, 18 November 2026

- L07 PASS: all four composer states observed. Previously verified empty, real draft and placeholder-identical draft preserved. In the existing authenticated Chat Succession Project, an unsaved composer displayed placeholder and disabled Send. Native Windows Open picker selected a harmless 65-byte text file; the accessible filename and Remove filename control established a real attachment. Independent clipboard/selection read returned actual editable text empty while UIA Value remained the placeholder. Send became enabled due to the attachment.
- No message Send, saved chat, succession-controller action, or existing draft deletion. The test attachment remains unsent. Target Chrome PrintWindow screenshot is cropped to the attachment chip and editor without unrelated desktop content. Evidence: evidence/astra-l07-20261118-a/attempt4.json, l07_attachment_only_printwindow.png, live_record.json. Earlier failed attempts remain in attempt2.json and attempt3.json.
- Validation: validate_observations.py verifies four classifications and all four screenshot hashes. Cumulative evidence/live_test_results_20261118.csv records L07 PASS; L01-L06 remain PASS and L08-L15 remain NOT_RUN. This is a live composer test, not an unattended controller handover.
- Next action: Leaf 06 L08, active Project routing with a different composer active and existing chats in the nominated Project. Prepare the correct destination without Send; verify no wrong-composer typing/Send or unrelated chat counting. Use existing authenticated browser, no new foreground-focus workstream.

## L07 bounded retry — desktop focus/window contention, 18 November 2026

- Continued from the verified remote L07 checkpoint `355b263226f31c2bf9a51578742f25b6bf1b5ab7`. Read README, AGENTS, PROGRESS and Astra's Leaf 06/runbook. Reused the authorised Remote Desktop Commander and Ubuntu; no controller or successor run.
- The previously verified L06 test composer window had navigated to another Project by the time it was re-inspected; the destination check stopped before interaction. A new Chrome window was opened at the **existing saved** L06 second-worker URL, but actual editable content was nonempty, so no attempt was made to clear/replace it. Another pre-existing L06 test-chat window lost foreground focus twice before a clipboard/editor read completed. Nothing was attached or sent, and unrelated Project details were omitted from the public evidence.
- **L07 remains BLOCKED, 3/4 composer states observed.** This retry adds evidence of window/draft/focus instability, **not** a verified attachment-only draft or an attachment-handling defect. L01–L06 PASS and L08–L15 NOT_RUN remain unchanged. See `evidence/astra-l07-20261118-a/attempt3.json`.
- **Next action (scope corrected):** complete the L07 attachment-only composer test using the existing authenticated Chrome session and nominated Chat Succession Project, in an ordinary window or tab. Use a harmless test attachment; independently observe actual editable text empty and positive attachment presence without sending or clearing drafts. Focus-dependent UIA is one possible inspection technique, not an L07 acceptance criterion or a separate engineering workstream. If the attachment-only state cannot be verified, record the specific observation limitation and keep L07 BLOCKED. Do not add browser-isolation or focus-management architecture. Proceed to L08 only after L07 is resolved or the owner changes the sequence.

## L07 follow-up — existing test-chat attachment probe, 18 November 2026

- Continued L07 using the existing nominated Project and authenticated Windows Chrome session, with no owner action needed. The existing completed L06 test chat `6afd0f07-e17c-83ec-ae22-a257184d7db4` had independently verified empty editable text, UIA Value `"Ask ChatGPT\\n"` and no detected attachments. This resolves the first attempt's lack of an empty composer, without clearing the separate unsent drafts.
- The nominated browser's `Add files and more` menu was positively expanded (UIA ExpandCollapse Collapsed → Expanded); the actual `Add photos & files — Upload from computer` action was identified. A cropped menu screenshot is retained, excluding conversations. The Invoke action did not produce a positively observed file chooser/attachment and the foreground switched to another Chrome window. A generated harmless-image clipboard paste also left actual editable text empty but produced no visible attachment. A later combined menu-click check could not find the upload item, so no unverified selection was attempted.
- **L07 remains BLOCKED (3/4 live conditions verified).** An accessible empty test composer and the upload-menu path are now confirmed, but **attachment-only has not been observed**. No chats launched, no messages sent, no controller operation and no existing draft or attachment deleted. This is an observation limitation, not an established application defect. Evidence: `evidence/astra-l07-20261118-a/attempt2.json` and `attachment_menu_cropped.png`. L01–L06 are unchanged.
- **Next action:** complete actual attachment selection in the existing authenticated Project test composer; independently observe editable text empty and a file preview/remove control. Only then update the L07 outcome. Do not proceed to L08 as a substitute for unverified L07 acceptance.

## L07 live browser composer regression — 18 November 2026

- **L07 outcome: BLOCKED, not PASS.** Three of four required states were independently inspected in the existing authenticated Chat Succession Project through the existing Windows Chrome UIA adapter plus a test-only selection/clipboard probe. No controller, successor, saved chat or Send was invoked. Existing drafts and attachments were neither cleared nor submitted.
- **Verified live:** (a) empty composer: actual editable buffer `""` while UIA Value was `"New chat in Chat succession folder\n"`; (b) genuine unsent draft: actual editable content and UIA Value both `"L07 unsent test draft keep intact"`; (c) real unsent draft equal to placeholder: actual editable content and UIA Value both `"New chat in Chat succession folder"`. Each has a cropped rendered-editor screenshot, SHA-256 and live output in `evidence/astra-l07-20261118-a/live_record.json`. The adapter must not infer emptiness or draft status from UIA Value alone.
- **Unobserved fourth state:** attachment-only was not prepared. Two newly opened `/project` windows unexpectedly presented inherited unsent text from earlier disposable test composers, first the genuine draft and then the placeholder-identical draft. Their independent editable reads were nonempty. There was no safe verified-empty new composer for attaching a harmless file without overwriting a draft; both were preserved. Additional read-only probes aborted on foreground changes, without Send.
- **Acceptance:** live empty-versus-draft and placeholder-identical discrimination demonstrated; attachment-only detection **NOT VERIFIED**, so L07's four-state acceptance criterion is not met. This is a bounded observation blocker, not proof of an attachment-handling defect. The offline D05 attachment model remains a separate reference result.
- **Evidence and method:** `evidence/astra-l07-20261118-a/` contains `live_record.json`, three cropped screenshots, test-only PowerShell probe and `validate_observations.py`. The separate clean L07 Ubuntu clone started at remote `601d922f7c153db76c2b8d080bd353d9bdbfe5b1`; the older dirty repository checkout was untouched. L01–L06 remain recorded PASS without resets.
- **Next action:** obtain an independently empty, disposable nominated-Project composer without erasing or reusing an existing draft; attach a harmless test file without text and record rendered editor, actual editable content, attachment presence and ambiguity-hold behaviour. Revalidate and update L07, then proceed to L08. Do not mark L07 PASS based on the three completed cases.

## L06 live repository-only handover verdict - 18 November 2026

- L06 verdict: PASS. Original first worker 6afd0a50-bb5c-83ec-8769-aad757de38c9 published slice 1 at b56f9fe5684828ad07005655b669da2705014aac; live Chrome UIA observed completed marked turn uia-turn-1-ab855a5d43e4a16a7064. The fresh single L06 reference controller began with one observed saved chat (cap 3).
- Controller --prepare-only persisted one unsent LAUNCH_SUCCESSOR action after first worker. Only then Astra's unchanged rotate-probe changed the NEXT uncompleted slice's probe (not rows or earlier slice). Operator published the repo-only rotation in 7b2eca1305a5bfe92734cc8a56155b9e55f1721d and verified remote Git before any successor Send; no probe was pasted to chat.
- The same existing controller dispatched the ordinary repo/branch pointer once and positively observed distinct saved successor 6afd0f07-e17c-83ec-ae22-a257184d7db4. The successor emitted NEED_MORE_TIME (uia-turn-1-b6b5d3e4293f5a3937d4); the controller sent an exact same-chat continuation without adding a chat.
- The second worker published terminal slice 2 at 06429f2c78e5fb55e8bfa43e8d0a3abfdfe29d8b with actual current post-rotation probe. Independent fresh Git clone pinned to exact remote SHA validated fixture_valid=true, completed_steps=2, total_steps=2, both saved IDs and both matching probes; programme_complete=true and next_task=null. A separate deliberately stale local Git checkout successfully refreshed the current remote branch using the existing RepoView reader (supporting Git test, not a naturally stale ChatGPT response).
- Terminal controller consumed uia-turn-2-45c7d04bc273c7e09bd6 and returned action STOP_FINISHED; persisted halted=programme_finished, pending=null, last_status=TASK_COMPLETE, unique_chat_count=2, with no third Send. The process exited.
- Evidence: evidence/astra-l06-20261118-a/operator_sequence.json, evidence/astra-l06-20261118-a/live_record.json and cumulative evidence/live_test_results_20261118.csv. Assisted initial bootstrap and limited stale-view scope recorded explicitly; L01-L05 preserved.
- Next action: Leaf 06 L07 read-only editor/composer regression: independently observe empty placeholder, real draft, real draft equal to placeholder and attachment-only states in nominated Project; distinguish editable content from UIA placeholder without Send or clearing drafts. Record actual observations in new L07 evidence, then proceed L08 as authorised. Do not modify unrelated projects or launch a new succession controller for L07.

## L06 second saved Project worker — terminal slice 2, 18 November 2026

- Second saved Project chat `6afd0f07-e17c-83ec-ae22-a257184d7db4` positively observed in live Chrome UIA while its current assistant response was produced. The external reference controller had already delivered the ordinary short successor pointer and its same-chat continuation. Worker made no Send or controller call.
- Starting remote commit `7b2eca1305a5bfe92734cc8a56155b9e55f1721d` contains the separately rotated step-2 probe `281e408db06ee9ba01d562299f75b794`. Fresh cloned working copy on the nominated branch was used; no stale L05 state or prior-chat nonce.
- Worker computed step 2 directly: alpha 2/40, beta 2/18, gamma 2/15, six rows and combined total 73; appended the result with current probe/chat ID. STATE.json terminal 2/2, programme_complete=true, next_task=null; first-worker slice 1 intact.
- Evidence: `evidence/astra-l06-20261118-a/second_worker_slice2.md`. This worker's publication is not itself an L06 PASS; the live controller/operator still must validate the pinned remote result, consume the final response, record STOP_FINISHED and update the live results sheet.
- Next action (external controller/operator only): observe the terminal worker reply, verify exactly two observed saved chats and zero extra Sends, independently pin/validate publication, and record L06 verdict. Then proceed to L07 according to Astra's Leaf 06. Do not launch an independent successor.

## L06 first live fixture worker — slice 1, 18 November 2026

- First saved Chat Succession Project conversation confirmed via existing Chrome UIA URL and matching displayed user assignment: `6afd0a50-bb5c-83ec-8769-aad757de38c9`. Starting nominated branch HEAD `353373b206eae8131c63431b2fec69a5a2edad77`.
- Original unrotated fixture step 1 normalised and aggregated directly from RUN.json: alpha 2/34, beta 2/31, gamma 2/11; six rows, total 76. Worker updated RESULTS.json and STATE.json to completed_steps=1/2, programme_complete=false, next_task=slice 2.
- Evidence: `evidence/astra-l06-20261118-a/first_worker_slice1.md`. Fixture validator and remote publication are independently checked during this worker handover; no simulation, controller action, successor launch, slice 2 or probe rotation by this worker.
- Next action (external controller/operator only): consume the clean terminal first-worker event with a fresh L06 controller, persist its prepared unsent action, rotate/publish only the next probe as a separate Git commit, then dispatch its existing pending action to the second saved Project worker. Do not claim L06 PASS until that real two-worker sequence and STOP_FINISHED are verified.

## L06 repository-only continuity setup - 18 November 2026

- New two-slice test-only fixture succession-tests/astra-l06-20261118-a seeded with unchanged Astra repo_fixture.py; initial validation 0/2. No worker has processed this fixture and no L06 controller or successor has been started. The next-slice probe is intentionally not rotated yet.
- The L06 handover is staged: first worker publishes slice 1; one existing-controller CLI cycle in --prepare-only mode stores the prepared unsent action; operator rotates/publishes only the next probe via Astra rotate-probe; a normal cycle then sends the ordinary branch pointer; successor publishes slice 2 and controller must stop on programme completion.
- Focused integration change: an optional deferral of dispatch using the same Astra Controller and persistent pending action, never a second launcher. New simulated test verifies no Send in the preparation phase, restart persistence, and exactly one subsequent dispatch.
- Evidence: evidence/astra-l06-20261118-a/setup.md. L06 remains NOT_RUN until the actual two-worker transport, changed probe and terminal observation. L01-L05 evidence and stopped controllers preserved.
- Next action: commit/push this L06 setup and implementation, verify remotely, then bootstrap first L06 saved Project worker with observed ID before initialising a fresh L06 controller. Do not create an independent successor or use L05 state.

## L05 live cap-two controller verdict - 18 November 2026

- L05 verdict: PASS. Existing reference controller, assisted first saved chat 6afcf6b8-65a0-83ec-9e23-6bf655cf8004, one automatic successor 6afcf7a9-93a8-83ec-aa5f-435905e0c1ae, cap 2.
- First worker completed and published at d1398b1ff25e2c221ecc1b21e56621f280f02107; controller consumed uia-turn-1-4be4e32fa1e885da2024 and confirmed distinct successor. Chat 2 first emitted NEED_MORE_TIME (uia-turn-1-39b7ac67377778332681), then received exact same-chat continuation while unique-chat count stayed 2.
- Final worker turn uia-turn-2-bbcc38a3c3a0c5b0aa1a consumed after publication c411dc7bd74d608c05837a6155b6f3c2984cc4bb. Fresh pinned remote clone independently verified fixture_valid=true, completed_steps=2, total_steps=3, both chat IDs and probes. Slice 3 outstanding, programme_complete=false.
- Controller terminal: action STOP_CAP; persisted halted=chat_cap, pending=null, last_status=TASK_COMPLETE, exactly two saved chats, no chat-3 Send. Controller process exited normally.
- Evidence: evidence/astra-l05-20261118-a/live_record.json and cumulative evidence/live_test_results_20261118.csv. Assisted initial bootstrap and no separate full UIA message-enumeration are recorded limitations. L01-L04 untouched.
- Next action: Leaf 06 L06: seed a fresh two-slice fixture, stage first-worker completion and a prepared unsent handover, rotate the next-slice probe only in GitHub, then use the existing controller to send ordinary pointer. Independently check successor uses current probe and correct branch and validate completed slice 2. Do not reuse L05 state.

## L05 second live fixture worker - slice 2, 18 November 2026

- Starting remote HEAD d1398b1ff25e2c221ecc1b21e56621f280f02107. Resumed as saved Project chat 6afcf7a9-93a8-83ec-aa5f-435905e0c1ae; existing controller recorded two distinct chats, cap 2, and consumed chat 2's first NEED_MORE_TIME response before same-chat continuation.
- From current RUN.json slice 2: alpha 2/40, beta 2/18, gamma 2/15, six rows, total 73. Appended a worker-attributed result and advanced fixture to 2/3; programme_complete remains false; slice 3 is the next task.
- Evidence: evidence/astra-l05-20261118-a/second_worker_slice2.md. No worker-initiated successor Send. The external controller still must observe this worker's final marked response and verify STOP_CAP with no third chat. Not an L05 verdict.

## L05 first live fixture worker ? slice 1, 18 November 2026

- Worker processed only slice 1 of 3 for Astra L05 from remote HEAD a33f37bf9602e6a28fb1a10e0ea7402874c9b8c0 on the nominated implementation branch.
- Existing controller private state recorded saved chat 6afcf6b8-65a0-83ec-9e23-6bf655cf8004, cap 2, one saved chat and no pending action. Worker made no successor Send.
- Computation directly from RUN.json: alpha 2/34, beta 2/31, gamma 2/11; six rows, total 76. Result and state set completed_steps 1, programme_complete false and next_task for slice 2. Slice 3 remains outstanding.
- Worker evidence: evidence/astra-l05-20261118-a/first_worker_slice1.md. The external controller must independently verify publication and complete the staged second-worker continuation and cap-stop observations. This is not an L05 verdict.


## L05 two-chat cap setup — 18 November 2026 (in progress)

- **Case:** Astra Leaf 06 L05, fresh test-only `succession-tests/astra-l05-20261118-a` with **three slices** and controller cap **two saved chats**. Seeded using the unchanged Astra fixture tool; validated initially at 0/3. The fixture's `INSTRUCTIONS.md` stages worker 1 publication of slice 1; successor worker 2's `NEED_MORE_TIME` followed by a controller same-chat continuation at cap; worker 2's publication of slice 2 while leaving slice 3 outstanding.
- **Pass boundary:** exactly two observed saved Project chats; one automatic successor, exactly one `Okay, continue working.` in chat 2 without changing count; published results validated at 2/3, `programme_complete=false`; controller terminal **`STOP_CAP`** with no attempted chat 3. L05 remains NOT_RUN until actual live observations. L01–L04 are finished and preserved.
- **Next action:** publish seed, start initial worker in nominated Project as assisted bootstrap, initialise fresh private controller cap 2 using its actual saved chat ID, then run the existing controller. Do not install another launcher, fork an extra controller or alter unrelated projects.

## L04 live early-completion result — 18 November 2026 (current)

- **L04 verdict: PASS.** Test `astra-l04-20261118-a`, cap **30**, first and only saved Chat Succession worker `6afcf52d-bed4-83ec-ad68-98479eb0caf9`, assisted bootstrap. Worker committed/pushed the one-slice fixture terminal result in remote `9476d451fb12896317765529972583c1b6081f51`.
- Independent Git archive of exact remote revision: `fixture_valid=true`, `completed_steps=1`, `total_steps=1`, `last_chat_id` matching worker, `programme_complete=true`, `next_task=null`. The browser observer saw a single clean final `CHAT_STATUS: TASK_COMPLETE` with completed turn identity `uia-turn-1-aac2393264a2cdf2d134`.
- **Controller:** observed `action=STOP_FINISHED`; persisted `halted=programme_finished`, `pending=null`, `unique_chat_count=1`, `last_status=TASK_COMPLETE`. Exactly **zero successor Sends** despite cap 30. No effect on prior L01–L03 states.
- **Evidence:** `evidence/astra-l04-20261118-a/live_record.json`, `first_worker_slice1.md`, fixture files, and cumulative `evidence/live_test_results_20261118.csv`. L01–L04 PASS with their recorded intervention caveats; L05–L15 NOT_RUN and L14 excluded by owner.
- **Next action:** Leaf 06 **L05**, a fresh **three-slice** fixture with **cap 2**. First worker publishes slice 1 and controller automatically launches worker 2. Worker 2 emits one `NEED_MORE_TIME`; controller sends exact same-chat continuation despite cap. Worker 2 then publishes slice 2, leaving slice 3 undone, and controller must emit `STOP_CAP` without creating chat 3. No new controller architecture or extra browser isolation.

## L04 initial live worker ? terminal fixture slice, 18 November 2026

- **Assigned run:** `astra-l04-20261118-a` on `work/astra-succession-implementation-20261118`, starting remote HEAD `1777b14c980de47697c16edd002f21bc0e879d3c`. Only the one authorised slice was processed.
- **Worker provenance:** L04 controller private state recorded first saved chat `6afcf52d-bed4-83ec-ad68-98479eb0caf9` with configured cap 30, one unique saved chat, and no pending action before fixture publication. The worker did not launch a successor.
- **Computed result:** alpha 2/34, beta 2/31, gamma 2/11 (count/integer total); six rows, combined total 76. Updated RESULTS.json and STATE.json to `completed_steps=1`, `programme_complete=true`, `next_task=null`, with matching worker attribution. See [worker evidence](evidence/astra-l04-20261118-a/first_worker_slice1.md).
- **Boundary:** This published terminal fixture is worker evidence, not a live L04 verdict. The external controller must independently consume this worker's clean terminal marker, validate remote state and record STOP_FINISHED with one saved chat and zero successor Send. Preserve completed L01?L03.

## L04 early-completion setup — 18 November 2026 (in progress)

- **Case:** Leaf 06 L04, one-slice fixture `astra-l04-20261118-a` in the nominated repo/branch. The initial worker should read the fixture, compute and publish slice 1 of 1, verify `programme_complete=true` and `next_task=null`, and finish with one canonical final `CHAT_STATUS: TASK_COMPLETE`.
- **Controller:** fresh private state; planned cap **30 distinct saved chats**. Observe initial saved chat as count 1, current published worker identity and final marked response. **Pass only if `STOP_FINISHED` occurs with one saved chat and zero successor Send.**
- **Boundary:** L01–L03 are already completed and recorded, not reset. L04 untested until live result. No independent successor launcher or new browser automation mechanism.

## L03 live ERROR/recovery result — 18 November 2026 (current)

- **L03 verdict: PASS with explicit operator interventions.** Case `astra-l03-20261118-a` used only initial saved chat `6afcf279-ed74-83ec-b39b-dacaf73af948` and the same Astra reference controller. The worker observed deliberately missing `RECOVERY_INPUT.json`, returned final `CHAT_STATUS: ERROR` (`uia-turn-1-674db1c40e5e6095ceba`), and the controller returned `HOLD` with `last_status=ERROR`, `pending=null`, `unique_chat_count=1`, zero automatic posts.
- **Repair and resume:** operator published matching `RECOVERY_INPUT.json` at `cbd95946d80a4ea93385a6a812dfcab125b30928`; explicitly resumed existing controller; assisted recovery prompt posted/read back in the same saved chat. Worker published validated one-slice terminal fixture in remote commit `99fae2147d2bd5bbdcd3bd95227741cb2f19adbc`. Independent Git archive validation: `fixture_valid=true`, `completed_steps=1`, `total_steps=1`, `programme_complete=true`, `next_task=null`, and published worker attribution unchanged.
- **Additional terminal-marker hold:** the first recovered assistant turn's UIA-flattened text contained an inline bare `TASK_COMPLETE` fragment as well as the final canonical marker. Astra's unchanged strict parser held this ambiguous response; no Send followed. Operator explicitly resumed the same controller and posted/read back a request for one clean final marker. The new response `uia-turn-2-d4e15be845b76613ca0f` was consumed, and controller produced **`STOP_FINISHED`** with `halted=programme_finished`, `pending=null`, `unique_chat_count=1`, prior consumed identities retained, and **zero successor launches**.
- **Evidence:** `evidence/astra-l03-20261118-a/live_record.json`, worker's `worker_recovery.md`, fixture and cumulative `evidence/live_test_results_20261118.csv`. The repeated-marker observation may inform L10 but **does not count as an L10 PASS**. No parser or new architecture was introduced; L01–L03 PASS and L04–L15 NOT_RUN (L14 outside scope).
- **Next action:** Leaf 06 **L04** — use a fresh one-slice fixture and cap 30, publish programme completion in the first saved worker, and verify `STOP_FINISHED` with **no successor Send**. Use new private controller state; do not modify completed L01–L03.

## L03 recovered first worker — 18 November 2026

- **Recovery input:** operator published `RECOVERY_INPUT.json` at `cbd95946d80a4ea93385a6a812dfcab125b30928` with the correct run ID and `repair_authorised=true`. Initial missing-input `ERROR` was preserved.
- **Same saved worker:** `6afcf279-ed74-83ec-b39b-dacaf73af948` confirmed by read-only controller state, with one unique chat and the earlier `ERROR` consumed. No successor launch by this worker.
- **Fixture result:** six rows, alpha 2/34; beta 2/31; gamma 2/11; total 76. `RESULTS.json` and `STATE.json` terminal 1/1, `programme_complete=true`, `next_task=null`. Validator returned `fixture_valid=true, completed_steps=1, total_steps=1` and `git diff --check` was clean. See [worker evidence](evidence/astra-l03-20261118-a/worker_recovery.md).
- **Next action:** external controller independently observes and consumes this worker's new `TASK_COMPLETE` event, verifies same-chat continuation and preserved count/history, and records the L03 verdict. This worker publication alone does **not** claim L03 PASS. L04–L15 remain untested.

## L03 controlled ERROR/recovery setup — 18 November 2026 (in progress)

- **Case:** Leaf 06 L03 on `work/astra-succession-implementation-20261118`. Test-only run `astra-l03-20261118-a` seeds one normal Astra fixture slice. Its `INSTRUCTIONS.md` requires a `RECOVERY_INPUT.json` file deliberately absent at seed, so first worker must report a concrete `ERROR` and not modify results.
- **Planned recovery:** observe controller HOLD with zero automatic posts, publish only the missing test input, explicitly resume the *same saved controller and chat*, send an assisted operator recovery instruction, and verify that a new completed event is consumed without resetting history/count. First worker then completes 1/1 and controller terminates with no successor. All observations are to be recorded, not assumed.
- **Preservation:** L01 and L02 are finished and not reused/reset; original imported Astra artefacts unchanged. No unrelated project or additional browser automation layer. L03 not yet PASSED; L04–L15 not run.

## L02 live integration result — 18 November 2026 (current)

- **L02 verdict: PASS.** Run `astra-l02-20261118-a` with configured cap 3 used one assisted initial worker and one automatic successor. The external reference controller alone sent both exact same-chat continuations and the one successor pointer. No new UI automation or isolation layer.
- **Two continuations, same saved chat:** first worker `6afcef76-26b0-83ec-82e2-0de6db78a838` produced two completed, distinct `NEED_MORE_TIME` turns; controller persisted both consumed identities and posted exactly `Okay, continue working.` twice. Read-only Chrome UIA message history confirmed exactly two actual user messages of that text (one extra matching assistant explanation was not a Send). Unique-chat count remained 1 and there was no pending Send after either.
- **Published first worker handover:** after the second continuation, worker committed/pushed slice 1 of 2 at remote HEAD `f08da56d9a7f1437723bf49bb011fda49a64dba3`, with validator `fixture_valid=true` and published `last_chat_id` matching first worker. Controller consumed its third, marked `TASK_COMPLETE` and automatically posted the ordinary pointer once, observing a distinct successor `6afcf107-76f0-83ec-9367-eee546d55837`.
- **Published terminal result:** successor committed/pushed slice 2 at remote HEAD `83a82f3112ad90503887058b32d1895ea8beef77`; independent verification by Git archive of this exact commit returned `fixture_valid=true`, `completed_steps=2`, `total_steps=2`, `programme_complete=true`, `next_task=null`, and `last_chat_id` equal to the successor.
- **Controller terminal:** observed `action=STOP_FINISHED` and persisted `halted=programme_finished`, `pending=null`, exactly two saved chat IDs, last status `TASK_COMPLETE`. Zero additional successor sends. L01 terminal state remains untouched.
- **Evidence:** `evidence/astra-l02-20261118-a/live_record.json`, the two worker evidence Markdown files, fixture data, and cumulative `evidence/live_test_results_20261118.csv`. Imported Astra deliverables unchanged. L01 and L02 PASS; **L03–L15 NOT_RUN**; L14 remains outside owner scope.
- **Next action:** Leaf 06, case **L03**: fresh test-only controlled blocker and same-run repair. Confirm completed `ERROR` produces HOLD with zero automatic posts, then explicit recovery preserving count and event history. Continue using the same Astra controller/Windows UIA/WSL Git method on the nominated branch, without duplicate launchers or extra ceremony.

## L02 second live fixture worker — terminal slice 2, 18 November 2026

- **Run:** `astra-l02-20261118-a`; second saved Chat Succession worker ID `6afcf107-76f0-83ec-9367-eee546d55837`, independently recorded by the existing controller state, distinct from first worker `6afcef76-26b0-83ec-82e2-0de6db78a838`.
- **Published-branch starting point:** `f08da56d9a7f1437723bf49bb011fda49a64dba3`. The first result existed and fixture validated at 1/2.
- **Slice 2:** six rows normalised and aggregated directly from RUN.json: alpha 2/40, beta 2/18, gamma 2/15; combined value 73. RESULTS.json and STATE.json updated; `completed_steps=2`, `programme_complete=true`, `next_task=null`.
- **Worker verification:** `fixture_tools.py verify` returned `fixture_valid=true, completed_steps=2, total_steps=2`; `git diff --check` clean. See [worker evidence](evidence/astra-l02-20261118-a/second_worker_slice2.md). No worker-side successor Send.
- **Next action:** the single external controller observes this worker's final marked turn, confirms terminal STOP_FINISHED and no third chat, verifies two exact prior same-chat continuation posts, and records the L02 outcome in live evidence/results. This worker's publication alone is **not** an L02 PASS; L03 remains the next separate case.

## L02 first live fixture worker — slice 1 prepared and committed, 18 November 2026

- **Run and authority:** `astra-l02-20261118-a` on `work/astra-succession-implementation-20261118`, first worker's prescribed third turn only. Two earlier in-chat replies ended `NEED_MORE_TIME` before this fixture publication. External controller's two same-chat postings still require independent observation before L02 can pass.
- **Saved worker ID:** `6afcef76-26b0-83ec-82e2-0de6db78a838`, observed in the exact Chat Succession Chrome window URL via Windows UIA; its title was `Inspect L02 Inputs`. The worker did not start a new conversation or Send a browser message.
- **Starting remote revision:** `78a961da068d01ffcc699ca67aed8f811caad8d8`. Slice 1 result, state and [worker observations](evidence/astra-l02-20261118-a/first_worker_slice1.md) committed at `22e6c56b592ed5c2e379affec5a3fc52cc5b8b5a`. No simulated worker was used.
- **Result:** alpha 2/34, beta 2/31, gamma 2/11 (count/total); overall six rows and value total 76. The published fixture's `completed_steps=1`, `programme_complete=false`, `next_task=Process fixture slice 2 of 2; read RUN.json and verify RESULTS.json.`. Validator returned `fixture_valid=true, completed_steps=1, total_steps=2`; `git diff --check` clean.
- **Next action:** external controller consumes the final first-worker `TASK_COMPLETE`, confirms both same-saved-ID continuations and distinct-chat count 1, reads the published branch and handles any single successor. A later distinct worker finishes slice 2. L02 remains pending until live controller evidence and terminal observation; L03–L15 unchanged.

## L02 live preparation — 18 November 2026

- **Current task:** Leaf 06, case L02 only. New run `astra-l02-20261118-a` is a two-slice test-only workload on `work/astra-succession-implementation-20261118`. The first worker's three turns are staged in this run's `INSTRUCTIONS.md`: initial `NEED_MORE_TIME`, continuation `NEED_MORE_TIME`, then commit/push slice 1 and `TASK_COMPLETE`. Later worker finishes slice 2 normally.
- **Acceptance:** two exact controller-sent `Okay, continue working.` messages in the *same* saved first worker; distinct-chat count remains 1 across both; published slice 1 allows one automatic successor; slice 2 publishes programme completion and controller stops. Fresh private controller state; L01 terminal state preserved unchanged.
- **Gate/evidence:** fixture seeded with Astra's unchanged `repo_fixture.py` and validated as 0/2 before publication. L02 is not yet passed; L03–L15 remain NOT_RUN. Record live observations in a new evidence file, not as offline simulation. No extra browser isolation or new controller framework.

## L01 live integration result — 18 November 2026 (current)

- **L01 verdict: PASS against the prescribed L01 acceptance criteria**, with assisted first-chat setup and explicit recovery of two *pre-Send* UIA entry failures (not unattended-repeatability evidence).
- Test run `astra-l01-20261118-a`, cap 3. First saved Chat Succession worker `6afce427-98c4-83ec-b3e7-a05c19f0806f` published slice 1 at `a375250b60e31c44836f5452a3fd64f7be54bf76`. The original Astra controller then automatically posted the plain GitHub repo/branch pointer **once** and positively observed successor `6afced4f-870c-83ec-8370-fbe7e296b386` in the nominated Project. No chat 3 was launched.
- The second worker published slice 2 and terminal `programme_complete=true`, `next_task=null` in remote commit `d6302c55097188cd8a23c89641e862e715d0eab7`. Independent validation from an archive of that exact remote Git object: `fixture_valid=true`, `completed_steps=2`, `total_steps=2`; two distinct matching worker IDs and correct category aggregates.
- **Observed terminal controller outcome:** `action=STOP_FINISHED`, saved `halted=programme_finished`, `unique_chat_count=2`, `pending=null`, `last_status=TASK_COMPLETE`. It consumed the second worker's completed status and made **no further Send**.
- **Local adapter corrections:** Windows-to-WSL repo path preserved via `Path.as_posix()`; a failed Git observation now holds *without consuming* a valid turn; native writable Chrome UIA `ValuePattern.SetValue` successfully entered the complete 173-character pointer after unreliable simulated keystrokes/paste. All 17 simulated integration tests passed; Windows PowerShell parsed with zero syntax errors. Earlier failing Send attempts stopped *before Enter* and were explicitly re-armed through reference `confirm_not_sent` with their disposable drafts cleared. No new browser-instance verification machinery was introduced.
- **Live evidence:** `evidence/astra-l01-20261118-a/live_record.json` and `live_test_results.csv`; L02–L15 remain `NOT_RUN`. The imported Astra source deliverables are unchanged; the earlier three-chat trial is unrelated.
- **Next action:** continue Leaf 06 with a **fresh L02 fixture and controller state**, preserving terminal L01. L02 must prove two same-chat `NEED_MORE_TIME` continuations, then a handover. Before claiming repeatable event deduplication, investigate the observed UIA assistant-count component changing across viewport scroll for the same second-worker content; do not add a new orchestration system. G4/L13 remains pending.

## L01 second live fixture worker — 18 November 2026

- **Assigned scope:** resumed the published `astra-l01-20261118-a` fixture on `work/astra-succession-implementation-20261118`; processed slice 2 of 2 only. The external controller remains the sole successor launcher.
- **Provenance:** existing controller state recorded second saved Chat Succession ID `6afced4f-870c-83ec-8370-fbe7e296b386`, distinct from first worker `6afce427-98c4-83ec-b3e7-a05c19f0806f`. No additional successor was launched by this worker.
- **Worker result:** trimmed/lowercased slice-2 categories: alpha count=2 total=40; beta count=2 total=18; gamma count=2 total=15. Appended a second `RESULTS.json` result with the published RUN.json probe and observed successor ID; updated `STATE.json` to `completed_steps=2`, `programme_complete=true`, `next_task=null`.
- **Verification:** `python3 succession-tests/astra-l01-20261118-a/fixture_tools.py verify --root succession-tests/astra-l01-20261118-a` reported `fixture_valid=true`, `completed_steps=2`, `total_steps=2`; `git diff --check` clean. Fixture commit `8041f08323f0865c69afda29be9196138959dfb1`.
- **Boundary:** this is published-worker evidence, not yet a full L01 PASS. The single live controller still needs to consume this worker's completed, status-marked turn, read the published terminal repo state and observe that no additional successor is launched.
- **Next action:** complete the above read-only terminal controller observation and record L01's actual outcome; then follow Leaf 06 for the remaining bounded cases. Preserve one controller and the existing worker chats.

## Astra implementation Worker — 18 November 2026 (work in progress)

- **Owner scope correction:** no drift or new orchestration system. Use Astra's existing reference controller, the nominated implementation leaves, and the already demonstrated Windows/Chrome method. Keep only necessary integration code; disposable investigative scripts have been deleted. Do not expand scope by importing assumptions or architecture from other projects.

- **Source verified:** remote evidence/astra-source-import-20261118 at f2f0a3de9f6ed55f2315c8389eeddd4486b34209; implementation work isolated on work/astra-succession-implementation-20261118. Existing unrelated WSL checkout with uncommitted work left untouched.
- **G0:** imported Astra reference suite rerun in Ubuntu, 119/119 PASS, zero skips/failures/errors. This is offline model evidence only.
- **G1 / Leaves 01–04:** new integration/ code imports Astra's unchanged Config/Controller/Response/RepoView/parser/composer and connects a scoped published-branch RepoView reader, Windows UIA/Chrome observation/prepare/Send/reconcile seam, persistent pre-Send dispatch and recovery, and single-writer CLI. New tests 16/16 PASS locally, simulated/mock; also 11/11 checked on Windows Python 3.13 before expanding the suite. Browser Send is not yet claimed live-tested.
- **Desktop diagnostics:** read-only Chrome UIA verified an actual Project page and saved Project chat, distinct URL identity, UIA assistant fragments and a Project-specific composer. UIA Value and TextPattern both included placeholder text. A controlled L07 subprobe found empty editor (selection/copy leaves clipboard sentinel unchanged), and a genuine draft literally equal to the placeholder (copy returns actual text); test draft was cleared and placeholder restored on reinspection. Clipboard restored. This covers only part of L07 and is **not** an L07 PASS.
- **Navigation regression:** UIA ScrollIntoView did not expose the Project-specific sidebar button in a new Chrome window. Reused the *already observed* exact Project /project URL in a new Chrome window; verified correct fresh editor, actual editable content empty, zero attachments and no saved chat ID. No message sent.
- **Gate status:** G1 local wiring implemented and locally checked; G2 in progress. G3 L01–L12 and L15 still NOT_RUN as complete live cases; G4 L13 not eligible. G5 L14 excluded by assignment. No autonomous successor, useful live fixture publication or Send yet.
- **L01 fixture setup:** generated and locally verified `succession-tests/astra-l01-20261118-a` on `work/astra-succession-implementation-20261118`. This is the active two-slice **test-only** workload; its `INSTRUCTIONS.md`, `RUN.json`, `STATE.json` and `RESULTS.json` are the worker's next task. Do not use `simulate-slice` as evidence of live worker work. Cap for L01: 3 distinct saved chats.
- **Next action:** Verify the published fixture from the remote branch, then initialise the controller only after observing a fresh first worker ID in the nominated Project. Validate the completed-turn and Send readback seam before treating L01 as live. Keep the six Astra deliverables unchanged; preserve uncertain outcomes.

## L01 first live fixture worker - 18 November 2026

- **Assigned scope:** fixture slice 1 only, on `work/astra-succession-implementation-20261118`, initial remote revision `96fc3927b70fe765f545b21937e076e9225f062b`. Existing working copies and controller remain untouched.
- **Worker provenance:** Chat Succession browser tab titled `Complete Fixture Slice 1`; saved conversation URL ID `6afce427-98c4-83ec-b3e7-a05c19f0806f` observed in permitted tab metadata. Page-content observation was not available and is not claimed.
- **Result:** category trimming/lowercasing gives alpha count=2 total=34, beta count=2 total=31, gamma count=2 total=11. Updated `RESULTS.json` and `STATE.json`; no mock slice executed.
- **Next action:** Process fixture slice 2 of 2 from fresh published repository state. `programme_complete=false`; the external controller alone handles any successor launch.

## L01 live controller checkpoint — 18 November 2026

- L01 uses the nominated Project and `work/astra-succession-implementation-20261118`; the first worker was **assisted bootstrap**, not a controller-created successor. Its posted initial assignment and saved chat ID `6afce427-98c4-83ec-b3e7-a05c19f0806f` were observed through existing Windows Chrome UIA.
- First worker published fixture slice 1 in remote commit `a375250b60e31c44836f5452a3fd64f7be54bf76`. Independently ran the unchanged fixture validator on a Git archive of this exact remote revision: `fixture_valid=true`, `completed_steps=1`, `total_steps=2`. The published fixture `last_chat_id` agrees with the observed initial worker ID; slice 2 remains.
- The single L01 controller is saved privately at `C:\Users\james\AppData\Local\chat_successor_astra_l01_20261118\state.json` (not tracked). Its observed status on resuming: **one saved chat; no pending action; no terminal status; no successor Send**.
- **First incomplete boundary:** repeated UIA Observe reads returned `ready=false`, `stop_control=true`, only an early partial assistant reply, and no final status marker. Publishing slice 1 does **not** substitute for observing a completed assistant turn. The reference controller appropriately returned `WAIT` and did not launch a successor. Do not mark L01 PASS or reset/re-send the initial assignment.
- The owner explicitly rejected extra window-isolation or identity-checking ceremony. Continue with the existing Chrome/UIA mechanism and its already specified Astra adapter rules; do not add machinery to protect the other project.
- **Next action:** use the existing live observer to consume a completed, marked first-worker turn; if one appears, let the *single* controller read the current published fixture and decide whether to launch the ordinary short successor pointer once. If UIA remains stuck in an incomplete view, investigate that Leaf 03 observation boundary directly, without a second orchestration system. Preserve the first chat and fixture result.

## Astra execution handoff — 18 November 2026

- Source branch `evidence/astra-source-import-20261118`, import commit `44c0d5948318e305c42fb0ac4f463e77f90531bc`. The [execution plan](docs/astra-succession/README.md) organizes Astra's existing cases and integration work into seven leaves with gates G0–G5.
- G0 reference baseline: Astra recorded 119/119 offline passes. The [independent Ubuntu rerun](https://github.com/JayDEmily/chat_successor/blob/14478119c9b4cc9288bb66b846975bd71b43d06c/AGENTS.md#local-checks) also recorded 119/119. A fresh run on Windows Python 3.13 using `python -X utf8 run_offline.py --out <temporary-report-dir>` from the kit root passed 119/119 with zero skips, failures or errors. Without UTF-8 mode the default Windows-1252 decoder failed loading the parser fixture.
- G1–G5 await execution. Astra live cases L01–L15 remain `NOT_RUN`. The [older trial](https://github.com/JayDEmily/chat_successor/blob/3b2c95b954eb90b1e6c9b82403dd1956c6f34b39/evidence/succession-20261117-001/CHAT2_LAUNCH_BLOCKED.md) is separate historical evidence and remains held.
- An independent review checked the revised handoff against Astra's source and confirmed that the leaves use the existing offline suite and all 15 live cases.
- Next action for the implementation chat is [Leaf 01 — Adopt the offline controller](docs/astra-succession/leaves/01-controller.md) on the assigned implementation branch.

## Original exploration handoff — 17 November 2026

- Repository: owner-created private `JayDEmily/chat_successor`; original initial commit retained. Planning publication prepared; remote verification is reported after pushing.
- User-created ChatGPT Project: confirmed by owner statement and screenshot; exact URL/profile/tools not yet checked.
- Design: proposed, owner review pending. Worker-launch first is an agent recommendation.
- Implementation: NOT STARTED.
- Live experiments: NOT RUN; zero chats launched by this repository.
- Existing Second Chat OCR work: separate; no changes authorised by this exploration.

| Task | Status | Next action |
| --- | --- | --- |
| 1: contract and prerequisites | NOT STARTED | Owner reviews design; choose launch approach, verify actual Project/tool setup |
| 2: bounded launcher | NOT STARTED | Follow accepted Task 1 contract |
| 3: three-chat chain | NOT RUN | Requires bounded trial assignment and verified launcher |
| 4: orchestration assessment | NOT STARTED | Evaluate actual observations |

Future workers append the exact source/evidence commits, check commands/outcomes, interventions and first missing boundary. Preserve failed attempts. Do not mark an experiment successful merely because a chat says it finished.

## Planning verification

A separate read-only builder check identified launch-key uniqueness, journal-loss behaviour, operator-inspected stall status and Windows Python preflight as material gaps. All four corrections are incorporated. Local Markdown links and documentation-only scope were checked before publication. No product tests or live chat launches occurred.

A concurrently created empty `JayDEmily/chat-succession` repository is unused; no files are published there.
