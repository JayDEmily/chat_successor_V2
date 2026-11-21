# Reproducibility, code package and frozen integrity checks

**Verbatim correction:** [VERBATIM_SUPPLEMENT.md](VERBATIM_SUPPLEMENT.md) now preserves the full original reviewer prompts, PowerShell command arguments, account routing, run files, reviewer Python scripts and the recoverable 245-record tool trace. Earlier redacted representations and exclusion statements below describe the first publication and are superseded. No authentication-token substitutions were required; 32 large outputs were already unavailable from the history source.

## 1. Obtain the case study

The case-study branch is in the **private** automation repository so that the actual Chat Succession source used for the first reviewer launch is not disclosed in the public LTM-RAG V2 repository.

    git clone --branch case-study/ltm-rag-v2-integrity-20261121 \
      https://github.com/JayDEmily/chat_successor.git
    cd chat_successor/case_studies/ltm-rag-v2-capture-integrity-20261121

Use access authorised for the private repository. Do not treat this as a command to log into the owner’s ChatGPT account or start reviewer automation.

This case-study branch was intentionally based on **5c86ad6d735b4c0626c49aedfdb93aeb95e6199b**, the installed automation source, even though the remote automation main had progressed beyond it. The final branch Git commit contains the new archival documentation and packages; the ancestor commit retains the runtime source itself.

## 2. Verify the frozen files without executing the application

    python3 tools/verify_case_study.py

The verifier:

- Validates every path and SHA256 recorded in SHA256SUMS and checks there are no unlisted case-study files.
- Checks the archive prefixes and the presence of the V2 canonical implementation/test files.
- Confirms that the saved final snapshot Python files exactly match corresponding members of the final source tarball; checks the baseline snapshot in the same manner.
- Inspects saved evidence for the exact GitHub issue, reviewed head, PR state, hosted job result, merge test SHA and the logged 285 tests.
- Checks preserved reviewer script hashes and metadata-only reviewer prompt records.
- Performs no network requests, provider calls, live sends, reconfiguration, imports or deployment.

The frozen Git commit protects the checksum manifest itself. The manifest deliberately omits its own digest to avoid a self-referential checksum. A file that is not listed is a verification failure.

## 3. Run the final independent synthetic adversarial suite

    python3 tools/verify_case_study.py --replay-independent

This option first verifies the archive, then:

1. Creates a disposable temporary directory.
2. Extracts the exact reviewed V2 source archive under that directory.
3. Copies the **unchanged archived reviewer-authored script** into the temporary directory.
4. Changes only the temporary copy's hard-coded reviewer checkout ROOT to the freshly extracted V2 tree.
5. Executes the 35-test unittest script in a separate Python process, using only fictional SQLite fixtures.
6. Requires an exit code of 0 and the observed “Ran 35 tests” / “OK” markers.
7. Discards the temporary copies afterwards.

The unmodified recovered script itself is under tools/reviewer-authored/8d27_final_35_test_review.py. Its digest is 182c031080671e3ef13b5cb7460d91206fb209244b036272548d834b43db899d. The original script was independently rerun before this case study was committed, with **35/35 PASS**.

A different full CI-equivalent run requires the V2 project's pinned MCP dependency and Python version matching the workflow. The workflow itself is in the V2 code archive under .github/workflows/vnext-synthetic.yml. The actual hosted result already exists in evidence/; no extra provider or native trial is needed to inspect it.

## 4. Reconstruct the commit sequence

The complete reviewed public V2 source code at the final head is in:

    artifacts/ltm-rag-v2-reviewed-8d27bd5.tar.gz

The complete original public V2 baseline source is in:

    artifacts/ltm-rag-v2-baseline-0aa4b80.tar.gz

Each includes the tracked 421-path public V2 source tree at its respective commit, including the ledger, tests, governance, requirements and GitHub Actions workflow.

The exact three commit transitions are separately preserved as full binary-safe diffs:

    artifacts/patches/01-baseline-to-65820f3.patch
    artifacts/patches/02-65820f3-to-d27acd1.patch
    artifacts/patches/03-d27acd1-to-8d27bd5.patch

There is also an mbox-form three-commit patch series under artifacts/patches/all-3-commits-format-patch.mbox.

The folder artifacts/snapshots/ contains the exact ledger implementation and unit test source at all four material stages: baseline, first-review, second-review and final-pass. These are read directly from Git objects at their respective full SHAs rather than regenerated from narrative pseudocode.

To inspect source archives without modifying files:

    tar -tzf artifacts/ltm-rag-v2-reviewed-8d27bd5.tar.gz | head
    tar -tzf artifacts/chat-successor-automation-source-5c86ad6.tar.gz | head

The private reviewer-automation source archive captures the **relevant source/dependencies** (integration, Astra reference kit, plugins and documentation) at the exact installed commit. Its source files are additionally present in this branch's inherited private Git tree. It excludes untracked runtime account routes and unrelated tracked evidence folders from the duplicative archive.

## 5. Inspect the actual independent reviewer test code

Under tools/reviewer-authored/:

- 8d27_final_35_test_review.py: exact independent final fault suite, recovered from the temporary reviewer worktree.
- d27_parent_red_control.py: exact differential parent control.
- 8d27_ci_selection.py: independent workflow-equivalent selection helper.
- d27_17_test_review.py: the preceding independent review fault suite, which originally identified five failures.

The recovered parent control contains an ephemeral absolute ROOT pointing at the reviewer's former temporary parent checkout. To execute it independently, use a **disposable copy** with ROOT changed to an extracted parent tree, not an in-place edit of the frozen script. Expected red tests on the parent are failures by design; do not call them a green test suite. The published third-review comment records the five original failures reproduced on parent and their green counterpart after the repair.

The case verifier's optional replay exercises the final-head suite only; it does not quietly reinterpret expected failing red controls as a passing full suite.

## 6. Review UIA launch code without sending messages

The **actual installed** first-launch executable code is retained by Git commit 5c86ad6 and the source archive, including integration/launch_project.py, integration/launch_story.py, integration/runner.py, integration/uia_adapter.ps1 and related source/tests.

The Windows-installed start-project.cmd wrapper is captured byte-for-byte under artifacts/automation/installed-start-project.cmd. Its original checksum is documented in AUTOMATION.md.

The successful later one-shot Windows Chrome UIA PowerShell invocations were originally transient tool commands. Their argument strings were recovered from the local Remote Desktop Commander tool history and included as **archival .ps1.txt records**, except that actual reviewer-assignment text was removed and replaced with SHA256-labelled placeholders. Those redacted representations were **not themselves executed** and should not be run. Their relative names are:

    tools/uia_attempt_presend_sha256_api_failure.ps1.txt
    tools/uia_actual_d27_one_send_redacted.ps1.txt
    tools/uia_actual_8d27_one_send_redacted.ps1.txt

The first documents a pre-Send failure using an unsupported Windows SHA256 static API. The later two document the actual successful one-shot UIA send/readback code path. The original account-specific Send intent files are not uploaded into Git; their hash/length, commit and positive readback state are recorded in prompts/ and AUTOMATION.md.

No account message transcripts, browser cookies, account_routes.json, API keys, session tokens, or personal conversation history were added for this case study. All reproduction steps above are offline and read-only, except creation/removal of local temporary files.

## 7. Evidence freshness and closure

The frozen evidence shows that, after the independent final PASS:

- V2 PR #2 existed, was mergeable, and remained open/unmerged at the observed checkpoint.
- GitHub Actions run 44899629182, job 136832604143, passed against synthetic PR merge aa2fdf3ad5371dcb086ba4f14f3256bbaa64b017.
- The hosted log reported 285/285 tests, plus successful governance and whitespace checks.
- The original private LTM archive was not changed by this repair; public V2 main remained 0aa4b804 at this checkpoint.
- The native passive capture route, nine private-evidence-dependent tests, a production service and the owner merge decision remained out of scope.

These are **historical statements**. To determine any later PR/merge status, query GitHub live. Do not silently reinterpret a past CI success as permanent approval of a changed branch or new merge ref.

## 8. Success criterion for this archival task

The case study is complete when the private case-study branch has a pushed Git commit; its reported HEAD can be read back from GitHub; its local source/worktree is clean; its SHA256 manifest checks; the preserved reviewer 35-case script executes against the extracted reviewed code; and its contents document both successful engineering review and the initially failed automation accurately.

This archival task does **not** merge PR #2 or amend public V2 main.


## Installed Windows checkout bytes versus canonical Git blobs

One byte-level distinction was found during archival verification. The installed Chat Succession checkout used Windows CRLF line endings, while git archive at 5c86ad6 emits the canonical LF blobs. The **source logic is identical after CRLF-to-LF normalisation**, but SHA256 of each file differs. The canonical Git source remains in artifacts/chat-successor-automation-source-5c86ad6.tar.gz; the exact five **runtime byte streams** (four central implementation files plus start-project.cmd) are separately captured in artifacts/automation/installed-windows-runtime-bytes-5c86ad6.tar.gz.

The checksum verifier checks **both**: Git canonical hashes against the source-tree archive, and the original as-executed Windows file hashes against the runtime byte archive. The case-study-specific .gitattributes disables Git line-ending conversion for all frozen assets on subsequent checkouts. This prevents an otherwise silent failure of archive replay integrity.
