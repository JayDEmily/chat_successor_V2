# Chat Succession — Astra ADR 0002 review package

**20 November 2026 · Offline review and proposed implementation plan · Not a deployment**

## Recommendation

Keep the existing Windows/Python controller, Chrome UI Automation adapter, Desktop Commander entry point and Ubuntu/Git publication route. Make the account/profile route explicit, strengthen existing action identity checks, preserve durable pause and reconciliation, and qualify capacity by measurement rather than imposing a two-run architecture.

The proposed ADR is **not owner-approved or implemented by this delivery**. The supplied Shoco 0.4.3 release is a baseline, not a fully accepted release. No live run was resumed.

## Read in this order

1. [Evidence review and exact pause disposition](evidence/EVIDENCE_REVIEW.md).
2. [ADR 0002 — Account-bound, resumable runs on one Windows PC](docs/adr/0002-account-bound-resumable-runs.md).
3. [Ordered implementation leaves](docs/IMPLEMENTATION_PLAN.md).
4. [Acceptance gates](acceptance/GATES.md), [executable test procedures](acceptance/PROCEDURES.md), and [capacity qualification](acceptance/CAPACITY.md).
5. [Start / pause / resume / check operator procedure](operator/QUICKSTART.md).

The new identifiers `A2-Lxx`, `A2-Gx` and `A2-...` deliberately do not overwrite the earlier Astra gates or live-case IDs.

## What was independently checked

| Check | Result in this sandbox |
| --- | --- |
| Input manifest | All **295** listed files match; no unlisted regular files except the manifest itself |
| Existing offline suites | **63 integration + 119 reference tests passed**, no failures/errors/skips |
| Archived workload validators | **13/13 valid**; validity does not mean an interrupted run finished |
| Additional baseline characterization | **9/9 assertions passed**; three explicitly reproduce limitations, not fixes |
| Git bundles | All **six** restore into fresh mirrors and pass `git fsck --full`; refs match the supplied TSVs |
| Pinned source | All **268** exported files match Git content: 10 byte-for-byte, 258 after CRLF/LF normalization |
| Release ZIP | Its four files match the exported plugin source byte-for-byte |
| Source preservation | Input hashes unchanged after all checks |

See [machine-readable results](verification/summary.json) and [source/provenance index](evidence/SOURCE_INDEX.md). Historical live evidence is distinguished from fresh offline checks throughout.

**Not run here:** Windows PowerShell, Chrome/UIA, Desktop Commander, either account's installed private plugin, iPhone, authenticated GitHub, or capacity trials. No MCP calls, network calls, browser Sends, pushes, installs, or changes to an existing repository were made.

## Package contents

- `docs/`: proposed ADR, dependency order, and ten implementable leaves.
- `acceptance/`: gates, detailed procedures, case register, evidence template and capacity worksheet. Planned live cases remain `NOT_RUN`.
- `operator/`: concise owner workflow plus exact existing CLI operations for an authorized operator.
- `evidence/`: findings, citations, and selected supplied files copied without alteration.
- `verification/`: actual offline output, Git-object readback, checksums and characterization results.
- `tools/`: reproducible offline review; no production launcher.
- `original/Chat-Succession-Astra-Handoff-2026-11-20.tar.gz`: the complete original upload, preserved byte-for-byte.
- `MANIFEST.sha256`: output integrity manifest, excluding itself.

## Reproduce safely

From this package directory, using Python 3 and local Git:

```sh
python3 -B tools/reproduce_review.py \
  --archive original/Chat-Succession-Astra-Handoff-2026-11-20.tar.gz \
  --out /tmp/astra-review-results-new
```

The output path must not already exist. The tool verifies the pinned input hash, extracts into a new temporary directory, prohibits non-file Git transport, runs the offline checks, restores one bundle at a time, and cleans up its temporary repositories. It does not edit the supplied snapshot. It executes reviewed test code from the supplied archive; it is not a general-purpose runner for arbitrary archives.

`tools/review_probes.py` is a **baseline characterization** tool. In particular P07–P09 demonstrate missing account/profile config binding, an unchecked target `action_id` at the mocked Send boundary, and omission of the pause marker from `inspect_state`. A green characterization is not a safety acceptance pass. The leaves specify the future regression assertions.

This package contains the owner's original evidence, including saved-chat identifiers already present in that evidence. Keep it in the owner's private review workflow.
