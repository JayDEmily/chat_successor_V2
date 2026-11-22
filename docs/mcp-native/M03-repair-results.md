# M03 repair — worker evidence, independent re-review required

22 November 2026 AEDT. Rejected candidate `80688e4620cbddb4b53317ee7dd48434a9c8dd6b`; direct repair parent `f160f6d2a1ee0cae4ba7626e79c24add8475fd4a` (management/evidence documentation, same rejected implementation); repair candidate `f03628139783c519342187e63bb6f8e80256fb84`; unchanged frozen M02 contract `9bf311a21a5e7d64b7f2be58b37ffd8294d78c7e`. Independent verdicts: [first](https://github.com/JayDEmily/chat_successor_V2/issues/2#issuecomment-7071887759), [second](https://github.com/JayDEmily/chat_successor_V2/issues/2#issuecomment-7072047353). Both independently reproduced four blocking defects. Historical results preserved, neither overridden nor self-approved.

## Changes against frozen M02
- S13: compare exact last verified durable envelope before every supported mutation, pre-effect commit and immediately after atomic write; check held writer-lock inode matches path. Any loss/change/unavailability poisons the open writer and raises without recreating/replacing the damaged state. Separate restart validates the checksum/schema; no hostile filesystem-writer guarantee. Check again after injected remote reads, before core consumption.
- S07: reject contradictory nonterminal FINISHED (including whitespace-padded FINISHED) and HOLD after trimming; require terminal next_task=None, preserve independent tip/provenance/ancestry gates.
- Bounded response: immutable Route.response_timeout_seconds (integer 1–86400, synthetic default 300) persisted with run. Set per attempted action at durable sending transition, not registration or receipt; persist absolute injected-clock deadline; hold at >= deadline, including no report, late report, lack of quiet or clock expiry during independent remote reads. A valid late report is immutable forensic evidence with "hold" return, not a received/actionable completion. Duplicate remains idempotent. A late exact delivery can reconcile count but cannot clear expiry. Restart preserves deadline and deadline hold; ordinary resume cannot rearm it. New actions only get a new window following safely consumed prior action. Synthetic wall-clock policy assumes a trustworthy elapsed-time source before first observed expiry; production clock policy is not qualified. Older disposable ledgers lacking the new policy are refused rather than migrated/reset.
- Strict refs: conservative existing short-branch character grammar plus reject HEAD, dot-leading components, .lock components, empty components, trailing dot, ref namespace and other invalid syntax. Apply at Route and TASK_COMPLETE schema admission; no request-derived shell/Git execution.

## Worker-tested evidence
Isolated Ubuntu clone /tmp/chat-successor-v2-m03-repair-f160f6d, then independently fetched byte-exact published candidate into /tmp/chat-successor-v2-m03-verify-f036281; exact HEAD and direct parent confirmed. Source Git blob 1054b78a615be5a15ad472b157f442d9229b894b; tests blob 1322c0b13dfca59179f03c1f57f4ba3a3949776b. Both matched staged local blobs. Only integration/mcp_native_poc.py and integration/tests/test_mcp_native_poc.py changed in candidate.

Fresh-checkout commands:
- python3 -B integration/tests/test_mcp_native_poc.py — 28/28, exit 0 (21 baseline plus seven additional test methods, including 36 loss/change/lock x operation subcases, deadline, malformed ref and timeout-policy tests; expanded terminal/ref negative matrix).
- python3 -B astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/run_offline.py --out /tmp/chat-successor-m03-repair-reference-fresh — 119/119, exit 0.
- git diff --check HEAD^ HEAD — exit 0; git status --porcelain empty.

Reviewer artifact regression (worker-executed, before final small clock-rollback hold-return refinement; originals unmodified, all four SHA256 matched original issue comments). Path-only temporary copies in /tmp/chat-successor-m03-repair-reviewer-regression:
- adversarial.py: passing identities, race, publication, flow, budget, recovery, contradiction and deadline groups. Three old diagnostic groups marked FAIL because the intended fail-closed RuntimeError/ValueError occurs before their former diagnostic output. No false claim of clean execution.
- recovery_review.py: both crash/reconciliation cases PASS; exit 1 due to previously uncaught intended RuntimeError on missing ledger before attempt.
- independent.py: all observations PASS except "late report accepted?" (old script expects exception instead of contract-allowed "hold" receipt). Separate "deadline hold" check PASS, both malformed refs PASS. New worker test checks late report is durably recorded, returns hold, remains unconsumed and cannot prepare/dispatch/rearm; recorded hold survives clock rollback.
- restart.py: all five observations PASS, exit 0.
These are regression observations, not a fresh independent verdict; reviewers must independently derive tests using the intended hold semantics, including preservation of damaged evidence, re-entrant read/expiry cases and restart.

## Disposition
M03 repair candidate worker-tested, not accepted. Fresh independent reviewer required; M04 resource grant unchanged, gate remains closed. Do not deploy, create live resources, launch native successors or touch original implementation or LTM-RAG. No further reviewer was launched by this repair operation. No credentials published.
