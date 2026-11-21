# Reviewer automation — exact version, live operation and failure

**Verbatim correction:** [VERBATIM_SUPPLEMENT.md](VERBATIM_SUPPLEMENT.md) now preserves the full original reviewer prompts, PowerShell command arguments, account routing, run files, reviewer Python scripts and the recoverable 245-record tool trace. Earlier redacted representations and exclusion statements below describe the first publication and are superseded. No authentication-token substitutions were required; 32 large outputs were already unavailable from the history source.

## 1. What automation actually ran

The installed Chat Succession automation used by the initial LTM-RAG V2 reviewer bootstrap was in the **private** GitHub repository JayDEmily/chat_successor, at the detached installed checkout:

    5c86ad6d735b4c0626c49aedfdb93aeb95e6199b

Git described this revision as “fix: verify loaded saved chats in virtualized Chrome views” (20 November 2026). Its parent was e6868fd78d65ddc8d13cfaa8ee0ddcb7966e3300. The private repository's main had subsequently moved beyond this installation; **5c86ad6 is the observed runtime**, not a claim that it was the latest upstream release.

The actual Windows entry point was an installed wrapper, start-project.cmd, outside the tracked Git tree. The wrapper routed the authenticated Windows profile into Python 3.13, with UTF-8 mode, and the installed integration/launch_project.py at the above revision. The complete wrapper bytes are preserved at artifacts/automation/installed-start-project.cmd. Its observed SHA256 was:

    3869731a405807b2833e5670f9a883b328bc0a6ca5d651fa386c2f63e60b93fb

The case-study branch **starts at that exact private Git source commit** and retains its full tracked source through Git ancestry. For portable inspection, artifacts/chat-successor-automation-source-5c86ad6.tar.gz also captures the relevant tracked automation code, imported Astra sources/fixtures, plugins and docs, excluding unrelated historical evidence directories and untracked runtime credentials.

Core implementation files at the installed version, with original SHA256:

| File in the original automation tree | SHA256 |
| --- | --- |
| integration/launch_story.py | f4a00a41fd513032856b75e123e37428fc1d3ccc5d2f3d4ea0f9a144ae940725 |
| integration/runner.py | 172356c301614bb51b7d7cbf1f9dfa474ef09440224b59080baf889b5c6c7c0f |
| integration/uia_adapter.ps1 | 412ddf7f3f29dc947b6da6fbf7b9a10ae19bf0012e4d17cd13f39ad0c5194580 |
| integration/repo_reader.py | 55b13d001b4d1a98b3981546004c82fc4effbadc6fde61ad9038f08c1bf9e07 |

The integrated execution path also involved integration/launch_project.py, cli.py, windows_backend.py, account_routes.py, owner_reentry.py and tests; all are in the pinned automation archive. Their exact Git blobs and inherited repository history are preferable to a source reconstruction. This archival branch does **not** install, update, reconfigure or restart those programmes.

## 2. Intended launch and controller behaviour

The requested reviewer assignment was deliberately finite: one new independent tester in the nominated ChatGPT Project, against an exact public V2 GitHub head, with a GitHub issue verdict. The controller's intended workflow was:

1. Resolve the designated local account route and signed-in browser profile, project name, Git repository, branch and owner scope.
2. Run the existing preflight without Send; verify repo/Project/browser requirements and a fresh destination.
3. Persist a bootstrap intent before a UIA Send, with the exact message identity.
4. Invoke Send once, then positively observe the posted exact message in a saved chat with the expected Project URL and distinct chat ID.
5. Only after positive readback establish controller identity/state and manage the bounded single-chat run. On any uncertain outcome, **hold**, do not blindly repeat a Send.

The owner did not authorise synthetic LTM-RAG native conversation capture or extra model inference as part of the engineering review. Ordinary Project reviewer requests and responses were a separate task from the LTM memory source-ingestion experiment.

## 3. Actual initial launch

The correct authenticated Project became visible after expanding the saved-chat Project list. The preflight returned success with the public repo and reviewed source head. The first start request was issued through the installed start-project.cmd with a one-chat cap.

A saved reviewer conversation was created and the reviewer assignment visibly appeared. Its exact first-source message could later be matched as a UIA Text element, and the assistant had begun responding. However, the launcher's stricter message-structure check failed to positively classify that posted content using its expected structural elements; the window had visible text but the expected article/container semantics were absent or not exposed to that validator. The initial bootstrap intent persisted. The run did **not** produce a controller.json with current_chat_id/unique_chat_ids, and the strict acknowledgement path returned a held/error state.

This is a specific **transport/readback failure**, not proof that the reviewer conversation was never created. It also is not an initial-controller PASS. The safe action was to reconcile the existing saved URL/posted text and **not send the message again**. A resume/preflight did not retroactively manufacture the missing controller record. The first independent reviewer continued the actual engineering review independently and published its RETURN_TO_WORKER result in GitHub issue #1.

No configuration change to repair the installed controller, nor any new controller service, was introduced during this case.

## 4. Two later fresh reviewer chats: manual UIA recovery

For candidate d27acd1 and final candidate 8d27bd5 the workflow used a **manually orchestrated, one-shot UIA Send**, with Remote Desktop Commander executing Windows PowerShell in the existing signed-in Chrome profile.

The pre-send checks were:

- Open a separate Chrome window at the exact known Project landing URL; never infer account identity from a transient login route.
- Confirm a unique Project-specific new-chat editor, the expected Project URL, an actual empty editable value (apart from placeholder), no active Stop and no enabled pre-existing Send.
- Construct an exact, commit-pinned independent-review assignment.
- Compute SHA256 over the UTF-8 prompt; persist a local intent record before the click.
- Fill the editor with UIAutomation.ValuePattern.SetValue and read its value back character-for-character.
- Identify exactly one enabled Send button within that composer document, check the URL again, and set the intent to an uncertain/sending state **before** invoking Send.
- Invoke that specific UIA Send **once**. Observe the saved conversation URL and one exact message-text match. Mark POSTED_EXACT_MATCH only on a positive readback; otherwise hold rather than repeat.

A pre-Send attempt used a static SHA256.HashData method not available in the installed Windows PowerShell/.NET runtime. It failed **before** any Send; the corrected code used SHA256.Create().ComputeHash. A separate fresh-window observation initially saw no loaded editor, then succeeded after waiting for the UI to render; again, no Send occurred until the preconditions were satisfied.

Both later Send receipts reached POSTED_EXACT_MATCH and match their original recorded prompt SHA256. The local raw intent files remain in the private installation, outside Git. The case-study prompts/INDEX.json and individual JSON records preserve **hashes, lengths, reviewed commits, UI-readback state and saved-chat locators**, but exclude the account conversation text itself.

Important distinction: those manual PowerShell scripts were issued as transient Remote Desktop Commander tool commands and were **not persisted as versioned .ps1 source files at the time of execution**. The case preserves the exact installed Chat Succession code and exact reviewer-written Python tests. It does **not** falsely describe a later script reconstruction as byte-identical historical automation source.

## 5. Three reviewer assignments and attribution

| Assignment | Pinned head | Launch evidence and reviewer output |
| --- | --- | --- |
| Initial launcher bootstrap | 65820f3c36d59d5636cc03e260e1666e6ca5836e | Saved reviewer chat 6b017bb8-4dec-83ec-af20-c757c6cdb15f. Launcher controller unregistered; independent RETURN_TO_WORKER on issue #1. |
| Direct one-shot independent review | d27acd1ab6d06031ffc773c855907cfd8362027a | Saved chat 6b017de0-8380-83ec-ba6b-e451c3d907fe, positive exact text readback. RETURN_TO_WORKER on issue #1 comment 7061870012. |
| Direct one-shot final reviewer | 8d27bd55d4abf0c5f864b60a33f24d666920a130 | Saved chat 6b018018-3188-83ec-b0dd-99b282e32dd5, positive exact text readback. Independent PASS on issue #1 comment 7061961835. |

The saved chats were separate fresh ChatGPT threads. The GitHub issue comments, not the current worker's description, are the durable independent review verdicts. No later reviewer inherited a successful Chat Succession controller for this case. The initial automation hold and the successful manual UIA sends are both part of the frozen record.

## 6. Preserved runnable reviewer test code

Unlike the transient browser Send code, the isolated third reviewer left executable Python files in its Ubuntu temporary review directory. They were recovered and copied **byte-for-byte**, without modifications, into tools/reviewer-authored/:

- 8d27_final_35_test_review.py — standalone reviewer-authored G2/G5/G9 tests: 35/35 on reviewed head.
- d27_parent_red_control.py — corresponding independent parent differential control (five documented red cases).
- 8d27_ci_selection.py — the reviewer's CI-equivalent module selection.
- d27_17_test_review.py — the preceding independent review's fault-injection script.

The original files' SHA256 values, checked against the copies, appear in SHA256SUMS and EVIDENCE.md. The standalone test imports the reviewed ledger through a temporary-path ROOT variable. tools/verify_case_study.py rewrites **only a temporary execution copy** of that path to point at the extracted archived source; the preserved original never changes.

These files and their GitHub review comments are distinct evidence from the worker-authored tests in the V2 source tree. The third reviewer also reran the configured CI-equivalent suite independently and compared old and new behaviour with fresh SQLite databases.

## 7. Automation failure classification and sensible follow-up

**Observed defect:** the launcher's exact-post verification was too dependent on a particular Chrome UIA message-container hierarchy; visible, exact text and saved-chat identity alone were not accepted by that path. Its fail-closed behaviour was correct: it did not send a duplicate. Its inability to register the controller was a real automation failure.

**No fix in this case:** repair of the Chat Succession launcher's UIA structural readback would be a separate, independently tested change in its own private repository, not an incidental rewrite of V2 or this frozen case study. No controller success or general automatic reviewer-handoff capability is inferred from the manual one-shot recovery.

**Boundary retained:** account_routes.json, passwords, cookies, local browser state, owner chat history, raw account transcripts and controller secrets were not copied to this GitHub branch. The retained launcher wrapper contains only the original programme routes and paths; the branch is private because even executable automation implementation detail is not intended for the public V2 repository.

The case therefore records a **successful review-and-CI engineering loop with a partial/failed reviewer controller launch**, not an unattended reviewer automation success story.

## 8. Recovered original manual UIA command arguments

After the initial narrative was written, the Remote Desktop Commander local tool history was inspected. It retained the original Windows PowerShell argument strings at **22:17:29**, **22:17:52** and **22:27:18 AEDT** on 21 November 2026. These represent the pre-Send SHA API failure, the successful d27 one-Send command and the successful 8d27 one-Send command, respectively.

They are preserved under tools/ as *.ps1.txt, in the original source order and with original control logic, **except for redaction of the exact reviewer-message literal**. Each file records the corresponding original message SHA256. The records are archival and must not be executed; they were not saved as script files at the time of the actual sends, and the redacted copies were never executed. This is stronger source provenance than a later reconstruction, but it is not a claim to have an unredacted, byte-identical Git copy of each command.

These records do not change the outcome: the first Chat Succession controller failed its exact-post acknowledgement and was not registered. Both later reviewer chats were sent once via manually invoked UIA, and the saved messages were positively matched. No account transcript was committed to Git.


## Installed Windows checkout bytes versus canonical Git blobs

One byte-level distinction was found during archival verification. The installed Chat Succession checkout used Windows CRLF line endings, while git archive at 5c86ad6 emits the canonical LF blobs. The **source logic is identical after CRLF-to-LF normalisation**, but SHA256 of each file differs. The canonical Git source remains in artifacts/chat-successor-automation-source-5c86ad6.tar.gz; the exact five **runtime byte streams** (four central implementation files plus start-project.cmd) are separately captured in artifacts/automation/installed-windows-runtime-bytes-5c86ad6.tar.gz.

The checksum verifier checks **both**: Git canonical hashes against the source-tree archive, and the original as-executed Windows file hashes against the runtime byte archive. The case-study-specific .gitattributes disables Git line-ending conversion for all frozen assets on subsequent checkouts. This prevents an otherwise silent failure of archive replay integrity.
