# ADR 0002 A2-G2 Windows preflight checkpoint

**A2-G2 HOLD. Both staged no-Send preflights passed.** 20 November 2026 AEDT. Source candidate `0b6bfa3e935e713fe2f36afd8da79c2befab9a42` passed all 24 offline cases. [Independent A2-G1 acceptance](../G1_20261120/independent-0b6bfa3/REPORT.md)

## Shoco

- Opened an ordinary Chrome window in the existing Shoco profile. Chrome reported Profile 11, version 158.0.8127.37 and Windows window identity `Chrome.UserData.Profile11`. The same signed-in browser displayed Chat Succession as its owned cloud plugin. Plugin Creator confirmed private release 0.4.3, the `start-chat-succession` skill and Remote Desktop Commander binding. This identifies the current plugin package. The candidate is a new backend revision.
- Created the isolated **Chat Succession ADR2 — Finish Test** Project in Shoco, with no saved chats. The exact Project URL and scoped route are in the private Windows staging request. The Project window was left open.
- Windows Git refused to verify the backend from a WSL UNC checkout because its ownership could not be established. A fresh Windows NTFS clone at the exact accepted commit passed the normal backend verifier. Ubuntu Git retained its existing role for published repo readback. Git trust settings were preserved.
- Ran the accepted native candidate through `launch_project.py --check` with the staged Shoco route, verified Project and disposable approval fixture. Exit 0, `preflight_passed`. The probe verified a fresh empty composer and published ref `codex/g2-iphone-approval-shoco-20261120` at `b91b00fe75be2ca011eac1ad1cc0d668ffd8d8bf`. The Project still showed no saved chats. [Disposable fixture](https://github.com/JayDEmily/chat-succession-trial-approval/tree/codex/g2-iphone-approval-shoco-20261120)
- Repeated the known no-Send check with deterministic file snapshots. The positive Shoco check exited 0 and a James Student key against the Shoco-only test route held with exit 1 and `Unknown account route; refusing implicit fallback`. Exact staged file hashes and the installed wrapper, route-marker and recorded paused-run state matched before and after. Only the three staged input files were present. The first successful check lacked a reliable file comparison, which the repeated run supplied.

## James Student

- The owner opened a signed-in Chrome window and created the empty `test_folder_2` Project. Its native window reported `Chrome.UserData.Profile13`. The verified Chrome profile directory existed. The same browser showed its own private Chat Succession 0.4.2 and the connected Remote Desktop Commander app. The exact Project URL, profile path and plugin ID are in the private two-account stage.
- On that NTFS stage, the Windows launcher at the accepted source pin invoked Ubuntu Git to verify `codex/g2-iphone-approval-shoco-20261120` at `b91b00fe75be2ca011eac1ad1cc0d668ffd8d8bf`. The James Student run exited 0 and returned `preflight_passed` at 17:10:56 AEDT. An unknown key exited 1 before browser work. All four staged files and 186 canonical entries matched before and after. The canonical comparison included the wrapper, runs, requests and locks, plus the two absent routing files. [Disposable fixture](https://github.com/JayDEmily/chat-succession-trial-approval/tree/codex/g2-iphone-approval-shoco-20261120)
- A plugin card populated its stock prompt and mention without submitting a message. The draft persisted when the agent switched to Chat mode at the owner's direction. The James Student check held with exit 1 and `Chrome did not verify an empty composer without attachments`. Shoco passed the other check on the same stage. After confirming the draft contained only the stock text and mention, the agent removed both. The Project showed an empty composer, Chat mode selected and no chats.
- The verified Chat-mode rerun returned `preflight_passed` at 17:19:35 AEDT in 10.829 seconds. The exact project and published ref matched. The staged and canonical hash snapshots matched again. Zero messages were posted throughout these checks. The private Windows stage retains the receipts and the local screenshot.

## Installed route boundary

- The canonical Windows launcher exists with SHA-256 `a52548403b71a9d1ce029adbae0aaf6a9fda2734c8bc062a079f292992096900`. It still uses the existing legacy account selector. The actual installation has no ADR 0002 route document or routing marker. A staged candidate pointed at that root with an explicit account key held immediately, ahead of any browser action.
- The available Remote Desktop Commander connection found one canonical launcher with the same SHA-256 and could see the native `Runs` root. Its process used native Windows LocalAppData. The old wrapper sends that environment through its default route. The two signed-in ChatGPT plugin invocations still need separate connector-to-wrapper readbacks before a selector can be installed.
- Plugin Creator returned `Plugin not found` for the exact James Student private plugin ID shown in its own browser. Version 0.4.2 and its connected app are visible there. The release's installed skill and binding bytes still need readback from James Student. The owner-opened window resolved the earlier Chrome launch and tab-access failures.

| Case | Disposition |
| --- | --- |
| A2-W01 and live portions of R01/R02 | **HOLD**. Both staged exact-profile positives and the unknown-key negative passed. Installed private release and account selection evidence is incomplete. |
| Live draft portion of A2-V05 | Stock draft held before typing or Send. The stage and canonical snapshots matched. The remaining installed unsafe-view cases are open. |
| A2-W02 | **NOT_RUN**. Installed concurrent window/mutex acceptance awaits W01. |
| A2-W03 | **NOT_RUN** for installed acceptance. Native helper tests already passed at G1. Installed UTF-8 observation and saved-chat reopen await the verified account route. |
| A2-G3–G6 | **NOT_RUN**. |

Next action is to read the installed James Student release from that account's Plugin Creator connection and verify the existing launcher selector through each account's own Remote Desktop Commander connection. Those receipts determine the pinned installation and W01 rerun.
