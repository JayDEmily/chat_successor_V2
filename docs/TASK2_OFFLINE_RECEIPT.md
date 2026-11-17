# Task 2 — offline launcher and journal verification

**Date:** 17 November 2026, Melbourne. **Machine:** remote `DESKTOP-I188O30`. **Git operations:** Ubuntu WSL, user `jds`, working copy `/home/jds/chat_successor`. **Browser Sends:** zero.

## Observed test sequence

1. Wrote `tests/test_launch_journal.py` with 18 checks before implementation. Initial `python3 -m unittest discover -s tests -v` failed as expected with `ModuleNotFoundError: No module named 'launcher'`, then after implementing `launcher/journal.py`, all 34 existing + new tests passed.
2. Added the validator CLI and a command-line fixture. Separately introduced the next-assignment out-of-scope negative fixture: it initially **failed to reject** an unexpected file added to the handover/assignment commit. Fixed by requiring the assignment commit's actual Git paths to equal the handover and assignment paths exactly. The next run passed.
3. Added active-run precondition for a successor and a prepared-run rejection fixture. Final `python3 -m unittest discover -s tests -q`: **37 tests, 0 failures** (~1.2 s). All fixtures use disposable Git repositories and SQLite files.
4. On Windows, `powershell.exe -File \\wsl.localhost\Ubuntu\...\check_parse.ps1` was **blocked by existing `RemoteSigned` policy**, not a parser error. `Get-ExecutionPolicy -List` showed CurrentUser and LocalMachine `RemoteSigned`; no execution policy was changed. Copied `launch.ps1`, `check_parse.ps1` and `journal.py` into a separate user-local staging directory. Parser output: **`PARSE_OK: launch.ps1`**.
5. On Windows, exact `C:\Program Files\Python313\python.exe` (Python 3.13.15) ran the staged `windows_offline_smoke.py`; output: **`WINDOWS_JOURNAL_SMOKE_PASS: init/readback/duplicate/conflict/unknown/loss`**, with all database state in a disposable file. This test exercises actual Windows Python/SQLite, not a live Send.
6. The staged PowerShell launcher without `-ExecuteSend`, with a synthetic `chatgpt.com/g/g-p-offline-demo/project` URL and `Default` profile, printed **`STATIC_PREFLIGHT_PASS`** and **`NO_SEND`**. An intentionally wrong `example.org` domain was rejected before any Git, browser or journal operations.
7. A read-only targeted query of existing Chrome History files found **no entries matching Chat Succession**. This does **not** show the Project is absent; it only leaves the target URL and signed-in profile unresolved. No browser tabs or drafts were modified. The browser-tab connector was unavailable from the current iPhone-originated conversation.

## Verified offline boundaries

- Journal `init` is explicit and one-time. `reserve` fails closed on missing/corrupt file; unique `(run_id,next_step)`; mismatch SHA conflicts; concurrent reservations give one winner; every duplicate is held; there is no automatic reset.
- Outcome transitions only from `reserved` to `posted`, `effect_unknown` or `blocked`. A crash, uncertain effect or lost acknowledgement retains an inspectable held key. Steps 1 and 4 cannot reserve.
- Packet preflight checks exact local and fetched remote branch SHA, permitted role/task, prior Git lineage, real changed-path scope, reviewer ACCEPT and the fixed three-step budget. An unadmitted `prepared` run cannot launch steps 2/3.
- Windows static parsing and Python journal integration are positive evidence. The Windows UIA **browser effect path is source code only**, not yet tested.

## Unverified and stop

**First missing live boundary:** exact existing Chat Succession Project URL and Chrome profile/account, plus tool availability in a genuinely fresh Project chat. No child chat was created to check those prerequisites, per the owner's original restriction.

**Additional Task 2 live boundaries:** target editor identity, occupied-draft guard under actual Chrome, typed prompt exact readback, single Send, posted message, saved distinct Project conversation and receipt persistence after a browser effect. They require a separate live trial and cannot be claimed from static parsing or SQLite tests.

**Task 3 remains NOT RUN.** No accepted run branch, assignment A1, live launch reservation or Chrome submission was made. NVIDIA, Second Chat OCR and its installed runtime were untouched. No main merge.
