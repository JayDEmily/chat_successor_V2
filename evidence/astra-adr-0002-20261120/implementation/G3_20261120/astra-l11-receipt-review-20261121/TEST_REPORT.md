# Test/readback report

**Date:** November 21, 2026. **Scope:** supplied focused bundle and derivatives
of its synthetic fixtures only. No Windows desktop, authenticated Chrome,
private state, account access, remote repository change, or actual Send.

## Results actually obtained

| Check | Baseline | Candidate | Evidence |
| --- | ---: | ---: | --- |
| Python integration discovery | 118 passed | **126 passed** (8 added) | `evidence/*-integration.txt` |
| Added focused Python suite | — | **8 passed** | `evidence/candidate-focused-python.txt` |
| Included reference kit | 115 passed | **115 passed** | `evidence/*-reference.txt` |
| Real headless DOM, **mocked location/history** | 8 passed | **22 passed** | `evidence/*-dom.txt`, `candidate-dom-readbacks.json` |
| JS syntax (`node --check`) | — | Passed | `evidence/javascript-parse.txt` |
| Deliberately weakened DOM guards | — | Both negative controls failed as expected | `evidence/negative-controls.txt` |
| Unified patch / clean local reconstruction | — | Passed; candidate file hashes match | `evidence/patch-verification.txt` |
| Windows PowerShell/UIA | **Not run** | **Not run** | Six supplied suites plus one proposed suite; Windows required |

The focused snapshot contains 115 runnable reference cases here. The supplied
window report's historical 119-case claim refers to its own run; I did not
reproduce that count. The snapshot README explicitly excludes its historical
archive audit. Do not count the supplied reports' Windows passes as this review's.

Environment: Linux, Python 3.13.5, Chromium 144.0.7559.96, installed Playwright
and Node (exact versions/hashes in `evidence/input-manifest.json`). Temporary
fixtures and browser profiles were processed sequentially and cleaned up.

## What the new tests demonstrate

- **Positive:** exact saved continuation evidence can be confirmed once through
  the unchanged runner/CLI/controller boundary, with the recorded `SourceResponse`
  and action identity passed to the adapter.
- **Provisional/stale mismatch:** provisional rendered owners remain unqualified;
  an invalid provisional destination cannot be rescued by a positive receipt
  flag; stale route DOM and a previously qualified node rebound to another
  route are rejected. Repeated Chrome samples with the same timestamp do not
  consume a response or prepare a Send.
- **Plausible lost acknowledgement:** one **simulated** adapter Send fails.
  Three read-only unresolved receipts (missing predecessor, ambiguous markers,
  expired sample) leave journal and target bytes unchanged. Restart/cycle/
  dispatch remain held. A later exact receipt clears that same action with no
  second Send and no count inflation. These Python tests mock PowerShell's
  output; they do not independently execute its DOM/anchor gates.
- **Additional safety checks:** false receipt flags and inexact text cannot be
  overridden by diagnostic metadata; wrong saved chat/project retain pending;
  malformed JSON, a nonzero adapter exit, and a timeout never retry Reconcile
  at the Python transport layer; a generic module-path error is not an automatic
  no-click/rearm receipt.
- **DOM:** the supplied eight checks remain. Four identical or conflicting
  selection markers hold with count 4. Missing/ambiguous/non-prose predecessors
  do not export an anchor; restoring the exact preceding row does. A fixture-only
  scoped scroll restores the bottom/previous-row sample. Duplicate user keys
  still hold.
- **Native suite supplied, unexecuted:** exercises the actual AST-extracted
  Reconcile block and snapshot functions with synthetic UIA values and a
  disposable private target receipt. It checks positive evidence, transient
  recovery, 25-read/24-sleep exhaustion, immediate mismatch holds, changed route,
  and revalidation of a changed action record between polls.

The negative controls used temporary copies of the supplied reader:
removing the route-history guard failed the rebound-node case; removing the
selection-count guard failed the two four-marker cases and the ambiguous
predecessor case. The candidate source was not weakened.

## Readback sample summary

From `candidate-dom-readbacks.json` (all IDs/text synthetic):

- Saved route + provisional user: `unqualified / user_conversation_provisional`.
- User saved, reply still provisional: `unqualified / assistant_conversation_provisional`.
- Both owners corrected: `observed`, original turn/reply IDs retained.
- Four markers: `unqualified / assistant_selection_ambiguous`, `selectionCount=4`.
- Current turn exact, preceding row absent: `observed`, `previous=null`,
  `previousReason=turn_missing` — **not sufficient for a continuation receipt**.
- Restored prior row: the supplied first turn key and exact reply ID return.
- Offscreen: `offscreen / transcript_offscreen`; fixture-only scroll restores
  the same anchored sample.

## Execution limits

A normal Chromium command-line launch could not start its GPU helper here.
The disposable Playwright in-process renderer worked, but browser policy blocked
HTTP navigation, including the loopback entry point. No policy was removed.
The recorded run therefore used `--mock-route`: original reader code in a lexical
location double, fixture history double, and a controlled DOMContentLoaded event.
All page network requests were blocked; there were no page errors or requests
in the successful run. It is **not** an extension, real-navigation, timestamp-
delivery, Windows-provider, or live receipt acceptance test.

No PowerShell executable or Windows UIAutomation assemblies were available.
The proposed native loop has not been executed or natively parsed here.
Its runnable synthetic suite and all six existing suites must pass on Windows
before adoption. Exact Windows observation requirements and conservative recovery
rules are in `REVIEW.md`; the original controller and journal schema are unchanged.
