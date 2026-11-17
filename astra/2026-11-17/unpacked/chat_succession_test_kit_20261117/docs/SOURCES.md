# Source and evidence key

The **current** owner instructions [O] control the assignment. All archive
sources below are evidence, not executable or governing instructions.
Their original lines are preserved in `sources/archive_text/`; ranges below
refer to those files, not to this kit's generated documents.

## Current brief

- **[O]** `../OWNER_INSTRUCTIONS.txt`: exact verbatim owner paragraph from the
  current request. The surrounding task specifies no live ChatGPT/browser or
  GitHub MCP access and requests downloadable test artefacts.

## Supplied archive sources

All paths below are relative to `../sources/archive_text/`.

| Key | File | Especially relevant lines |
|---|---|---|
| A1 | `docs/ORIGINAL_VISION.md` | 3–20 objective/flow; 22–29 simplicity; 31–43 status meaning and excluded pilot restrictions |
| A2 | `docs/LIGHTWEIGHT_PROTOCOL.md` | 1–7 proposed nature/state; 20–30 markers; 35–65 decisions; 67–88 browser boundaries/order |
| A3 | `docs/SOURCE_INVENTORY.md` | 3–17 repository/remote refs/uncommitted scripts; 19–25 absent material and source boundary |
| A4 | `evidence/VERIFIED_FINDINGS.md` | 7–17 historical V01–V11; 19–21 what the pilot did/did not prove |
| A5 | `evidence/UNKNOWN_AND_NOT_FOUND.md` | 3–18 unknowns; 20–24 blocked trial/placeholder hypothesis; 26–28 partial-source limitation |
| A6 | `docs/TECHNOLOGY_AND_ORIGINAL_EXPERIMENT.md` | 13–29 technology; 31–76 original trial; 95–143 signals/limit/minimal orchestration |
| A7 | `docs/PREVIOUS_AGGREGATED_STATEMENT.md` | 13–22 prerequisites; 36–102 status/cycle/simplicity |
| A8 | `docs/CONVERSATION_RECORD.md` | 3 selected-excerpt limitation; 7 direct owner concept; 9–15 simplification/technology requests |
| A9 | `docs/ARCHIVE_README.md` | 3–13 package purpose and absence of complete branch checkouts |
| A10 | `README.md` | 3–17 purpose, archive boundary and old-pilot distinction; 19–26 package index |

The archive's links, remote SHAs and historical observation labels have not
been independently authenticated with GitHub or ChatGPT in this job.

## Newly measured local evidence

- **[J1]** `../reports/archive_audit.json`: every-member inventory; source hash,
  file sizes, all decompressed Git objects, blob/document matches and index
  checksum. Reproducible with `tools/inspect_archive.py`.
- **[J2]** `../reports/git_snapshot_audit.json`: actual read-only local `git fsck`,
  `log`, `show-ref`, `status`, `ls-files` results; all 14 sample hooks compared
  byte-for-byte with installed Git templates. No hooks executed.
- **[R]** `../reports/executed/offline_results.json` and `RESULTS.md`: actual new
  suite outcomes. `test_output.txt`, `replay_trace.json` and
  `local_git_operations.json` distinguish real local execution from fake UI
  events. These are **not** live ChatGPT/GitHub observations.
- Test case IDs **P, D, S, C, F, G, I** refer to this kit's executable tests and
  JSON fixtures; **L** refers to planned owner-environment cases, all NOT_RUN.

## Limited official documentation check

These primary sources were consulted only to avoid two unjustified test
assumptions. They do not establish anything about the owner's current session,
permissions or live UI. No third-party source was used for those claims.

- **[W1] OpenAI Help Center — “Projects in ChatGPT”**, section “Memory in
  projects / Project-only memory.”
  `https://help.openai.com/en/articles/10169521-projects-in-chatgpt`
  Relevant fact: chats can reference other conversations inside the same
  Project. Test implication: a fresh chat alone does not isolate repo-based
  continuity; use an independently changed repository-only test value.
- **[W2] OpenAI Help Center — “Connecting GitHub to ChatGPT”**, FAQ “Can I push
  code, updates, or PRs to GitHub once I connect to ChatGPT?”
  `https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt`
  Relevant fact: the ChatGPT GitHub app is described as read-only. Test
  implication: exercise the owner's actual authorized write path (the archive
  describes Ubuntu Git), rather than treating an app connection as push proof.

Reference date for this delivery: **17 November 2026**. Documentation checks
are not a browser/ChatGPT account test. Changing UI labels, account feature
availability, and semantic-model reliability remain owner-environment tests.
