# ADR 0001 — Generic Chat Succession entry and re-entry

- **Status** — Proposed for owner review
- **Source date** — 19 November 2026
- **Baseline reviewed by Astra** — `0bee12a1725fbb103d82c5d08365959b3bf8c173`, plugin `0.3.0`

## Context

The owner wants to invoke the same plugin and speak naturally. An approval whose scope is clear from the conversation should continue the authorized work with the existing worker. The Rowing trial verified that the controller could launch a desktop worker and honor a project-level hold. The controller stayed halted after approval, and the later checkpoint appeared on a different branch without a succession receipt. The evidence does not establish whether the chat that continued was the registered worker or another chat.

Astra reran 35 integration tests, 119 reference tests, the approval reproduction and 13 archived fixture validations. Six additional offline probes reproduced the entry gaps. Those results support the proposal. Installed post-approval succession on an ordinary project remains unverified.

## Proposed decision

Use the existing plugin as the entry point for both fresh work and continuation. Keep project decisions in the entry and worker models. Keep saved-chat identity, dispatch, receipt verification, deduplication, pause and recovery in the existing controller.

| Leaf | Astra's recommendation |
| --- | --- |
| L1 | Interpret the current request and project authority in context. Reuse one worker instruction builder. Carry approval only for the identified scope, and ask a focused question when the scope or executor is genuinely ambiguous. |
| L2 | Inspect existing runs first. Prefer a verified run ID, then the stable Project ID and normalized repo. Preserve existing identity, history and cap through branch changes and Project renames. Make a genuinely new job an explicit internal action. Reconcile uncertain startup and confirm one controller owns the run. |
| L3 | If the saved worker already has the owner input, resume observation. If it is verified idle at the relevant hold, deliver the scoped input exactly once through the existing same-chat Send path. Keep the input in a private immutable record and pass a short pointer. Preserve drafts, existing pending actions and uncertain-Send recovery. |
| L4 | Retain the three Git trailers. Let the completed saved worker supply an optional branch locator. Fetch that exact remote branch, verify the current run and worker receipt, and persist the effective checkpoint with the completion and next action in one state update. Keep the original branch as the entry branch. |
| L5 | Cover the proposed offline regression matrix, verify the installed launcher and plugin, and run two bounded live exercises on different project shapes. Demonstrate natural approval and an automatic successor, and demonstrate verified branch rotation without changing the run or resetting its count. |

The proposed gates cover evidence and contract review (G0), the offline implementation (G1), and installed bounded acceptance (G2). They apply to this proposal. The earlier Astra acceptance record retains its original scope.

## Consequences and open questions

- The owner can approve in ordinary language. The verified saved worker receives the scope at most once and keeps its existing chat budget.
- Approval delivery and branch rotation rely on positive evidence. A same-Project chat may be a different executor. A published branch has to carry a valid handoff before the controller can change routes.
- Recovery must handle an older saved state, an already-delivered approval, and a response that advances while an action is being prepared. Verify these against the actual Windows browser adapter.
- Rowing remains evidence for the design. Its seven committed whitespace diagnostics describe the published patch. The evidence does not identify the writer or establish concurrent edits.

## Source and review material

- [Astra's complete implementation plan, tables and acceptance matrix](../astra-succession/generic-entry-plan-20261119.md)
- The imported plan preserves Astra's wording. Two Markdown hard breaks in the header were converted to paragraph breaks to pass Git's whitespace check.
- [Astra's independent review evidence and reproducible probes](../../evidence/astra-generic-entry-20261119/Chat_Succession_Review_Evidence_2026-11-19.zip)
- [Original response](../../evidence/astra-generic-entry-20261119/response.md) and [API usage record](../../evidence/astra-generic-entry-20261119/usage.json)
- [Original Google Drive package](https://drive.google.com/file/d/1wM5OwZLzixb1OUI1RCLSFc1w9Xu2_b33/view). Package SHA-256 `f43b6796e22bda586c92c4dcaea3c1f9c57e2aaf4b3fc3440208ccfcfa675b93`.
