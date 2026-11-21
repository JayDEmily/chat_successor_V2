# Verbatim evidence supplement — correction to the initial case study

**Purpose:** Additive correction to the original frozen case study. The original commit remains in Git history; this supplement preserves source material that was wrongly omitted or redacted.

## Preservation rule

Freeze every recoverable reviewer prompt, script, instruction, configuration file, command, tool observation and test result verbatim. Only live authentication token **values** may be replaced with a clearly identified SHA-256 digest. Preserve the rest of the original source unaltered.

**Result for these sources:** No recognised authentication bearer tokens were found in the recovered originals, so no token substitution was necessary. Original on-disk files were copied byte-for-byte. Where a tool history entry contained a command argument or a Send message, that exact string was extracted into a separate UTF-8 file. The new verbatim files supersede the redacted representations in the first case-study commit; those earlier redacted files remain only as a record of the mistake and subsequent correction.

## 1. Original reviewer assignments

All three complete, original reviewer assignment messages are now present as original UTF-8 strings, with no omitted text:

- **verbatim/prompts/01-first-review-assignment.txt** — first Chat Succession bootstrap; reviewed 65820f3.
- **verbatim/prompts/02-d27-review-assignment.txt** — independent d27acd1 review.
- **verbatim/prompts/03-8d27-review-assignment.txt** — final independent review on 8d27bd5.

For each, the archived content's SHA-256 matches the exact original message digest from the corresponding local intent. Original complete intent JSON files are also preserved under **verbatim/local-originals**.

## 2. Actual unredacted PowerShell Send commands

These are the literal command arguments issued through Remote Desktop Commander, recovered from the local tool history and saved unmodified as inert .ps1.txt records:

| Time, Melbourne 21 Nov 2026 | Original command |
| --- | --- |
| 22:17:29 — failed before Send (unsupported SHA-256 static API) | verbatim/commands/01-pre-send-failed-sha256-api.original-arguments.ps1.txt |
| 22:17:52 — successful second-review one-shot Send | verbatim/commands/02-d27-successful-send.original-arguments.ps1.txt |
| 22:27:18 — successful final-review one-shot Send | verbatim/commands/03-8d27-successful-send.original-arguments.ps1.txt |

The commands are **not** later reconstructions, and their literal reviewer message bodies are included. Do not run these archived commands: doing so could send new reviewer messages. Source timestamps and individual SHA-256 values are in **verbatim/trace/source-and-extract-provenance.json**.

## 3. Original installation routing and run evidence

**Twelve local files**, copied byte-for-byte, are preserved under **verbatim/local-originals/**:

- The complete installed account-routing JSON, not a redacted description.
- All five surviving LTM-V2 review request JSON files.
- All six surviving original run files, including original config, owner scope, bootstrap intent, window target, lock and SHA evidence.

**verbatim/local-source-provenance.json** records original absolute paths, exact SHA-256, file lengths and readback equality. The original run had no controller.json; no controller identity has been manufactured.

The original installed Chat Succession program source at commit 5c86ad6 and the Windows runtime-byte archives were already preserved in the first case-study commit.

## 4. Recoverable execution history

**verbatim/trace/20261121-220236-223402-recorded-tool-calls.jsonl** stores **245 chronological Remote Desktop Commander tool records** covering 22:02:36–22:34:02 AEDT on 21 November 2026, preserving every returned tool name, timestamp, argument field and recorded output string. The outer export format is JSONL; the original field values remain unedited.

This is the **complete recoverable history supplied for that time window**, not a claim to possess unrecorded events. The source retained a rolling window and had **already replaced 32 large tool outputs with omission markers**. Those omission markers are preserved as received. The missing original output bytes are not recoverable from that source and have not been invented. The window may also contain concurrent tooling from other threads; it has not been altered to make the sequence appear more streamlined. See **verbatim/trace/TRACE_LIMITS.json**.

## 5. Reviewer-authored Python code

Nine additional byte-identical original test scripts are now under **verbatim/temp-scripts**:

- **first/** — three original initial-review fault, CI-selection and base-control scripts.
- **second/** — original independent 17-case source, CI runner and readback checker.
- **third/** — original independent 35-case review, parent red control and CI runner.

**verbatim/temp-scripts/EXACT_SOURCE_MANIFEST.json** lists the original on-disk paths and exact byte digests. They supplement the already-preserved worker's full V2 code at all four commit points.

## 6. Token treatment

The user permitted hashing authentication tokens, **not** removing non-secret engineering source, reviewer prompts, account-routing details or unsuccessful test evidence. Known credential patterns (OpenAI API keys, GitHub access tokens, bearer tokens and JWT-like material) were checked before exporting the recovered local files and tool trace. Zero qualifying authentication token strings were detected in the newly copied sources; consequently **zero fields were altered**.

If a live credential is found in a later source, only its value may be replaced with a SHA-256-labelled placeholder, with the exact substitution documented. This rule does not change any existing original source in this supplement.

## 7. Verification and authority boundary

The original forensic material is checkable offline:

    python3 tools/verify_case_study.py --replay-independent
    python3 tools/verify_verbatim.py

The first checks the archived V2 code, hosted CI evidence and independent 35-test replay. The second checks all verbatim sources, prompt-to-intent equality, command-to-history equality and source provenance; neither makes an external request or performs a browser Send.

The original case-study commit remains reachable. This is an additive archival correction, **not** a change to V2 source, the Chat Succession launcher, accepted requirements, hosted CI or merge authority.

**Unavoidable gaps are labelled as gaps, never redactions:** 32 output bodies already elided by the upstream history tool, events outside its available time window, and any full live browser session recording that was not created at the time.
