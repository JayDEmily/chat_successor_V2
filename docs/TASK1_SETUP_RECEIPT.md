# Task 1 — prerequisite and offline setup receipt

**Date:** 17 November 2026 (Melbourne). **Execution:** Remote Desktop Commander on the user's Windows computer, Git and tests through Ubuntu WSL. **Scope:** this repository only. **Live ChatGPT Sends:** zero.

## Verified on this device

| Boundary | Observation | Evidence / limit |
| --- | --- | --- |
| Remote device | `DESKTOP-I188O30` online; Desktop Commander v0.3.3 | `list_devices` returned online and target device ID; tool execution receipts were returned |
| Ubuntu | WSL 2 default `Ubuntu`; current Linux user `jds` | `wsl.exe --status` and `wsl.exe -d Ubuntu -- bash -lc ...`; system is Linux |
| Linux Git | `git version 2.53.0`; private repo accessible over HTTPS through existing Git configuration | `git ls-remote https://github.com/JayDEmily/chat_successor.git HEAD` returned `26b33e8991119f9886b23f0c01651c3f49435706`; no credential contents inspected |
| Local working copy | `/home/jds/chat_successor`, cloned from main `26b33e8991119f9886b23f0c01651c3f49435706` | `git clone`, `git status --short --branch` showed clean `main...origin/main` before new branch |
| Isolated Task 1 branch | `work/task1-contract-preflight-20261117` | `git switch -c`; all planned Task 1 writes confined to this branch |
| Ubuntu Python | `/usr/bin/python3`, Python 3.14.4 | CLI output; `python3 -m unittest discover -s tests -v` initially failed with missing module as expected, then passed all 16 tests |
| Windows Python | `C:\Program Files\Python313\python.exe`, Python 3.13.15 | `Get-Command python` followed by explicit executable invocation; Windows `py` launcher was absent and was **not** relied upon |
| Windows-to-WSL invocation | Windows Python executes `\\wsl.localhost\Ubuntu\home\jds\chat_successor\tools\windows_sqlite_preflight.py` | Offline SQLite reservation/readback and duplicate key refusal: PASS on second run; no chat actions |
| Chrome | Chrome process with main-window title `Review NVIDIA Revision Commission - Google Chrome` | Read-only process title check. **Does not** confirm Chat Succession Project URL, signed-in account, Chrome tab placement or authentication |

The initial Windows SQLite probe reported correct insertion/readback but failed on temporary-file cleanup because a SQLite connection remained open. The probe was corrected to close connections explicitly and rerun successfully without a traceback. The failed probe's isolated temporary directory was removed. This was **not** a production journal test.

## Not verified — first missing live setup boundary

1. **Exact Chat Succession Project browser URL and Windows Chrome account/profile.** Owner has confirmed the Project exists and is the intended target, but this preflight has no verified URL or target profile. The visible Chrome window is occupied by unrelated work; it was not navigated, focused, or modified.
2. **Git read/write and Remote Desktop Commander in a truly fresh successor chat inside that Project.** These tools are available in this current project conversation; availability in future separate chats is not established by Project membership. This cannot be demonstrated without a fresh-chat setup/trial, which the current assignment explicitly excludes.
3. **Production launcher and journal.** Neither exists. The offline SQLite probe only establishes Windows interpreter/SQLite/UNC invocation capability; Task 2 must implement unique launch keys, missing-journal holds, explicit journal initialisation, browser guards and the actual `launcher/launch.ps1` invocation contract.
4. **Conversation delivery and chain success.** No Send, browser navigation, tool installation, successor chat, fourth chat or long-running watcher was created by Task 1.

**Task 1 status:** packet/test engineering verified; prerequisite setup is **open**, with the exact Project URL/profile and fresh successor tool checks as unverified live-setup boundaries. The live experiment must not be admitted until these are resolved and Task 2 is implemented and checked. No inference of a working three-chat chain is justified.

## What was actually tested

- Test command: `wsl.exe -d Ubuntu -- bash -lc 'cd /home/jds/chat_successor && python3 -m unittest discover -s tests -v'`
- Failing-first: import error on `tools.validate_packet` before code existed.
- Passing run: 16 tests, 0 failures in ~0.7s, covering valid steps 1/2/3, wrong run/step/role, missing/blocked/failed predecessor, declared and actual scope violations, attempted expansion of predecessor permissions, stale handover, branch head conflict, reviewer RETURN and step 4 rejection.
- Windows offline interpreter probe: `& 'C:\Program Files\Python313\python.exe' '\\wsl.localhost\Ubuntu\home\jds\chat_successor\tools\windows_sqlite_preflight.py'`. Second run returned `PASS` and terminated without error.
- These tests use disposable repositories and a disposable Windows SQLite file. They are not Task 2 launch-journal tests or Task 3 chat tests.

All device-specific session values remain outside the run packet. No account credentials, signed-in Chrome URL or conversation body was placed in the repository.
