# Protocol v1 — bounded three-chat experiment

**Scope:** one disposable Git branch, three *fresh* conversations in the existing Chat Succession Project, at most two worker-initiated successor launches. This directory describes a future experiment; no browser action is authorised by its presence.

## Identity, branches and packet schema

Run IDs match `[a-z0-9][a-z0-9-]{0,63}`; a run has exactly one branch `trial/<run-id>`. Before a launch, fetch that branch, check that the local and remote heads equal the exact 40-character assignment commit SHA, and evaluate `validate_packet(repo_dir, run_id, step, assignment_sha)`. On conflict, stop. Source file content may never choose or execute shell commands.

- `runs/<run-id>/run.json`: `schema_version: 1`, `run_id`, `branch`, `max_steps: 3`, `launch_mode: "worker"`, `project_config_ref: "local:..."`, and `stop_state` (`prepared`, `active`, `held` or `complete`). The `local:` reference points to private Windows setup outside Git; the actual Project URL is **not** committed.
- `steps/NNN/assignment.json`: `schema_version`, `run_id`, `step`, `role`, `task_id`, `predecessor_result_commit` (null for step 1), `terminal`, `allowed_paths`, `required_output_paths`. The child receives its containing commit SHA in the posted prompt, not a vague branch tip.
- `steps/NNN/result.json`: `schema_version`, `run_id`, `step`, `assignment_commit`, `status` (`completed`, `blocked`, `failed`), `changed_paths`, nonempty `checks`, and `unresolved_issues`. This file cannot cite its own future commit. The next handover refers to the separately published result commit.
- `steps/NNN/handover.json`: `schema_version`, `run_id`, `step`, `result_commit`, `next_step`, `next_assignment_path`, `terminal`. A nonterminal handover and the exact next assignment are published together in a subsequent Git commit. Step 3 instead publishes a terminal handover with no successor.

No credentials, Chrome URLs, conversation transcripts or unredacted account receipts belong in Git. The Windows launcher journal is private and must be explicitly initialised before a live run.

## Frozen toy work and path ownership

| Step | Expected role | Task ID | Required paths after result commit |
| --- | --- | --- | --- |
| 001 | worker | `toy-calculate` | `steps/001/toy.json`, `steps/001/result.json` |
| 002 | reviewer | `toy-independent-review` | `steps/002/review.json`, `steps/002/result.json` |
| 003 | auditor | `toy-terminal-audit` | `steps/003/summary.json`, `steps/003/result.json` |

All these paths are under `runs/<run-id>/`; no other result-commit paths are allowed. The validator checks the actual Git diff rather than trusting `changed_paths`. For this finite experiment, each result commit must be an immediate single-parent child of its assignment commit; each following assignment/handover commit must be an immediate single-parent child of the prior result commit. No parallel writers, repair loop, or fourth step.

**Step 1 instruction:** Compute `17 * 23 + 19` independently. Write UTF-8 `toy.json` with precisely `{"expression":"17 * 23 + 19","value":410}`. Record the calculation check and a `completed` result, commit and independently read back the result, then create the next assignment and handover in a distinct later commit. The successor launch is the final work action.

**Step 2 instruction:** Recompute the expression without treating step 1's claim as authority. Inspect the exact step 1 result commit and actual changed paths. Write `review.json` with `{"verdict":"ACCEPT","recomputed_value":410}` if and only if evidence and arithmetic agree; otherwise `verdict:"RETURN"` and terminate, without launching step 3. Publish the result, then the step 3 assignment and handover, separately. Launch only after readback and successful preflight.

**Step 3 instruction:** Independently verify both prior assignments, actual changes, result and handover lineage, and the accepted arithmetic. Write a `summary.json` with machine-readable `status`, `verified_steps`, `lineage_ok`, `arithmetic_ok` and `observations`; write `result.json`. Publish a terminal handover and finish. Never create or launch step 4. Task correctness and browser delivery still require independent evidence review.

## Immutable publication sequence

1. Create the new run branch and commit `run.json` and step 1 assignment; push/fetch/read back; pin commit **A1**.
2. In Chat 1 publish `toy.json` and `result.json` at **R1**, verify R1. In a later commit publish step 1 handover and step 2 assignment at **A2**, verify A2. Reserve launch key `(run_id, 2)`, then make at most one Send with immutable A2 in the prompt.
3. In Chat 2 publish `review.json` and `result.json` at **R2**, verify R2, then step 2 handover and step 3 assignment at **A3**, verify A3. Reserve key `(run_id, 3)` and make at most one Send of A3. A reviewer RETURN stops without A3.
4. In Chat 3 publish `summary.json` and `result.json` at **R3**, verify R3, then a separate terminal handover at **T3**. Mark the run complete; no fourth assignment, key or Send.

A successor's fixed prompt must give repository `JayDEmily/chat_successor`, exact run ID, step, role, **assignment SHA and path**, plus a clear instruction to read `AGENTS.md`, design/plan, pinned packet and run instructions. Do not quote a branch as the immutable source of assignment text.

## Validator and limits

In Ubuntu, with a prepared run and current `origin` branch fetched:

```python
from tools.validate_packet import validate_packet
result = validate_packet("/home/jds/chat_successor", "RUN_ID", 2, "A2_FULL_40_CHAR_SHA")
assert result.ok, result.errors
```

Tests: `python3 -m unittest discover -s tests -v`. The validator performs **no browser actions** and checks one incoming assignment and its immediate predecessor. The complete terminal chain, actual Chrome placement, launch reservations, original window retention and human-independent succession are only established by the later Task 2/3 evidence; an offline PASS is not a live result. `protocol/examples/` are non-executable illustrative templates, not admitted live run packets.
