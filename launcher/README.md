# Bounded launcher — Task 2 offline implementation

**Status:** source and offline checks only. No actual browser Send has been run or authorised. This is NOT proof that a live successor will appear in Chat Succession.

Source:
- `launch.ps1`: Windows UI Automation from the configured Chrome profile to an exact Project URL. **Default execution is non-sending static preflight**; browser use requires explicit `-ExecuteSend`.
- `journal.py`: standard-library SQLite local journal, explicit `init`, immutable launch key `(run_id, next_step)`, no retry/reset operation.
- `windows_offline_smoke.py`: cross-process Windows temporary-journal test.
- `check_parse.ps1`: PowerShell syntax parser; does not execute the launcher.
- `tools/validate_packet.py`: exact, read-only Ubuntu Git packet check; invoked before a launch reservation.

## Current offline checks

Ubuntu:

```bash
cd /home/jds/chat_successor
python3 -m unittest discover -s tests -v
```

Windows (tested with Python 3.13.15 at `C:\Program Files\Python313\python.exe`): copy the four launcher files from Ubuntu into a **local Windows staging directory**, then run `check_parse.ps1` and `windows_offline_smoke.py`. Do not run the launcher from `\wsl.localhost` under the existing `RemoteSigned` Windows execution policy; the remote path is not a locally trusted script path. No Windows execution policy was changed. Test receipts are in `docs/TASK2_OFFLINE_RECEIPT.md`.

## Admission prerequisites for a real trial

Before using `-ExecuteSend`, verify the **real** Project URL and Chrome profile/account, verify Git/remote tools in a separate fresh Project chat, admit exactly one fixed three-chat run, create and push its `trial/<run-id>` branch and pinned active run/assignment, and initialise a private local Windows journal **once**. Never store the local database or Chrome conversation URLs in Git. Require an explicitly scoped live execution authorisation; the presence of launch source code is not authorisation.

The launcher fetches the run branch, validates exact remote/local SHA, role, predecessor, statuses, changed paths and 3-step budget before a journal reservation. A reservation is durable before opening Chrome; every later attempt for the same `(run_id, next_step)` is held, even after an uncertain Send, crash, timeout or lost acknowledgement. Missing/corrupt journal holds (does not self-initialise). Only steps 2/3 can reserve.

For a deliberately admitted live run, provide the launcher with the actual Project URL, exact accessible Project name, verified Chrome profile directory, local journal path, run ID, step and 40-character pinned SHA. Chrome is given a new window; only a **new unique** matching Project window and empty editor can receive a single SendKeys-safe prompt. The code must read the typed value back exactly and observe one enabled Send button. After one Enter, positive observation needs both posted message and a distinct saved URL inside the Project. Anything less remains blocked/unknown with no automatic retry. **This entire browser path is untested.**

The first Chat 1 may be manually started only under the separate Task 3 admission; two automatic handovers (1→2, 2→3) are the trial goal. There is no watcher, no fourth launch and no return to the original chat.

## Tool/security boundary

The current installed Windows Chrome session belongs to other work and has not been manipulated. The offline staging directory is `%LOCALAPPDATA%\ChatSuccession\Task2Offline`, containing tested source copies. The one-off read-only Project history inspection helper was deleted after use. Neither source copies nor temporary tests constitute a production installation; do not initialise the actual trial journal until admission. The history check produced no target URL/profile result; that remains a blocker.
