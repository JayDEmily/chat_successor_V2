# ADR 0002 A2-G2 Windows preflight checkpoint

**A2-G2 HOLD — Shoco staged preflight passed.** 20 November 2026 AEDT. Source candidate `0b6bfa3e935e713fe2f36afd8da79c2befab9a42` passed all 24 offline cases. [Independent A2-G1 acceptance](../G1_20261120/independent-0b6bfa3/REPORT.md)

## Verified in Windows

- Opened an ordinary Chrome window in the existing Shoco profile. Chrome reported Profile 11, version 158.0.8127.37 and Windows window identity `Chrome.UserData.Profile11`. The same signed-in browser displayed Chat Succession as its owned cloud plugin. Plugin Creator confirmed private release 0.4.3, the `start-chat-succession` skill and Remote Desktop Commander binding. This identifies the current plugin package. The candidate is a new backend revision.
- Created the isolated **Chat Succession ADR2 — Finish Test** Project in Shoco, with no saved chats. The exact Project URL and scoped route are in the private Windows staging request. The Project window was left open.
- Windows Git refused to verify the backend from a WSL UNC checkout because its ownership could not be established. A fresh Windows NTFS clone at the exact accepted commit passed the normal backend verifier. Ubuntu Git retained its existing role for published repo readback. Git trust settings were preserved.
- Ran the accepted native candidate through `launch_project.py --check` with the staged Shoco route, verified Project and disposable approval fixture. Exit 0, `preflight_passed`. The probe verified a fresh empty composer and published ref `codex/g2-iphone-approval-shoco-20261120` at `b91b00fe75be2ca011eac1ad1cc0d668ffd8d8bf`. The Project still showed no saved chats. [Disposable fixture](https://github.com/JayDEmily/chat-succession-trial-approval/tree/codex/g2-iphone-approval-shoco-20261120)
- Repeated the known no-Send check with deterministic file snapshots. The positive Shoco check exited 0 and a James Student key against the Shoco-only test route held with exit 1 and `Unknown account route; refusing implicit fallback`. Exact staged file hashes and the installed wrapper, route-marker and recorded paused-run state matched before and after. Only the three staged input files were present. The first successful check lacked a reliable file comparison, which the repeated run supplied.

## Installed route boundary

- The canonical Windows launcher exists with SHA-256 `a52548403b71a9d1ce029adbae0aaf6a9fda2734c8bc062a079f292992096900`. It still uses the existing legacy account selector. The actual installation has no ADR 0002 route document or routing marker. A staged candidate pointed at that root with an explicit account key held immediately, ahead of any browser action.
- The available Remote Desktop Commander connection saw the same launcher hash. Its environment did not match the installed wrapper's Shoco selector. The owned Shoco plugin and the staged route are verified separately. The end-to-end plugin-to-wrapper selection is still open.
- Automatic approval review rejected the attempted new Chrome window for the historical James Student profile with `blocked by policy`. Read-only inspection through the existing James browser connection identified the Plugins tab, but the browser connection timed out on page readback. Profile 13's native window identity alone does not establish the signed-in James Student account or its private plugin.

| Case | Disposition |
| --- | --- |
| A2-W01 and live portions of R01/R02 | **HOLD**. Shoco stage passes exact-profile no-Send positive and wrong-key negative. Both installed private account routes and connector selection remain unverified. |
| A2-W02 | **NOT_RUN**. Installed concurrent window/mutex acceptance awaits W01. |
| A2-W03 | **NOT_RUN** for installed acceptance. Native helper tests already passed at G1. Installed UTF-8 observation and saved-chat reopen await the verified account route. |
| A2-G3–G6 | **NOT_RUN**. |

Next action is to inspect the private Chat Succession plugin from a dedicated signed-in James Student window, verify the plugin-to-launcher account selector in each real connector context, then complete W01 on a pinned installed candidate. The original paused workloads remain held.
