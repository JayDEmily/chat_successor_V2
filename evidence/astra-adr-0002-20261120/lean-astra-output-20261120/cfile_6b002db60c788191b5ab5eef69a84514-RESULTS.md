# Fresh local results — 20 November 2026

## What ran

Selected source was reconstructed from the inline mirror and compared with its
supplied SHA-256 values. Nine executable/test source files matched exactly or
after the documented CRLF/LF transformation. The management document used for
the pointer patch also matched (10 files total). This does not verify the
original archive or Git commit objects. Exact paths and hashes are in
`results/source_subset.json`.

Environment: Python 3.13.5; Git 2.47.3; Linux. No PowerShell executable or
Windows UIAutomation assemblies were available.

| Check | Actual outcome |
|---|---|
| New focused integration tests, supplied baseline | 13 run: 11 pass, 2 fail, 0 errors/skips |
| Same new tests after the two tiny Python patches | 13 pass |
| Supplied existing controller tests, final targeted run | 36 pass, including the original 300-trace test |
| Final combined run | **49 pass, 0 failures/errors/skips** |
| Route-upgrade characterization | Same account/profile/root with a changed backend commit or plugin ID rejects the old saved binding; characterization only |
| New native transcript assertions | 27 authored; **NOT_RUN** |
| Full 114 integration / 119 reference suites | **NOT_RUN here**; supplied results remain historical |
| Chrome, iPhone, actual account routes, capacity, remote Git | **NOT_RUN** |

The 300 traces inside one original test are not counted as 300 additional tests.
Raw baseline failure: `results/new_regressions_before.log`.
Raw final run: `results/targeted_after.log`.
Machine-readable summary: `results/summary.json`.

## The two failures, and the precise candidate scope

1. `test_existing_pause_blocks_preparation_not_only_the_click`:
   a marker already existed, but `dispatch_prepared` called mocked `prepare`
   before returning HOLD. No click occurred. The CLI loop already has a
   pre-cycle pause check; this test targets the direct dispatch seam.
   `03_pause_before_prepare.patch` adds the early return and retains the later
   check for a pause racing during preparation.

2. `test_explicitly_unqualified_reader_holds_instead_of_polling_forever`:
   `UIA_VIRTUALIZED_UNQUALIFIED` produced WAIT rather than a saved hold.
   Without a configured deadline, repeating that unchanged observation has no
   exit in the supplied loop. `02_reader_hold.patch` maps this specific
   unsupported-reader indication to the existing observation-error/hold path.
   It does not infer completion, mint an identity, reload or resend.

**Seven added runtime lines total.** No new controller, package dependency,
state version, worker status, service or automatic recovery mechanism.

These are narrow, author-tested candidates—not independent acceptance of the
author's own fixes and not a production release. The current native F1 blocker
and positive actionable-reader gap remain unresolved.

## What the tests establish, and what they do not

The Python regressions exercise the actual reconstructed production modules,
not a new control-model implementation. They cover the simple loop, identical
same-chat continuations with distinct supplied event IDs, cap/finish ordering,
publication repair, lost acknowledgement, owner-input preservation, pause,
read-only status and supported versus explicitly unsupported observations.

One regression uses real Git with a local bare remote, two published commits
and an unpushed intermediate handoff. It checks the direct parent and exact
two-line result. Its origin-identity check is deliberately mocked for the
file-only remote. Browser effects and model work are simulated.

The native script reuses existing fixture functions by AST extraction and
adds opaque-group, changed-heading, unknown-pane/custom/list, exact-body,
literal-label and streaming assertions. It tests actual production turn
functions with synthetic trees/prose evidence. It has **not** been parsed or
executed by PowerShell here. The unknown non-group cases and the interrupted
edit's old diagnostic-string mismatch are static findings awaiting Windows
reproduction, not reported live failures.

No supplied HOLD was cleared. No state or artifact was fabricated for the
missing positive current-turn, automatic stale recovery, phone or capacity
cases.

## Reproduction and delivery validation

After applying the patches to the complete source checkout:

```sh
python3 -B -X utf8 -m unittest discover -s integration/tests -p test_a2_thin_loop.py -v
(cd astra/2026-11-17/unpacked/chat_succession_test_kit_20261117 &&
 python3 -B -X utf8 -m unittest discover -s tests -p test_controller.py -v)
```

Run the complete existing suites at the programme's behavior gates, rather
than substituting these 49 selected tests.

Patch application was checked on reconstructed LF and CRLF Git working copies.
The final combined patch was also applied to a fresh local review copy and
its selected tests rerun. Package integrity/extraction validation is recorded
separately in `results/delivery_validation.json`. Those are artifact checks,
not product acceptance gates.
