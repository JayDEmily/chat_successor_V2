# Unknown, negative and unverified findings

**Meaning of “not found”:** absence of evidence in the inspected sources and times, not proof that something cannot exist.

| ID | Status | What remains unknown or was not observed |
| --- | --- | --- |
| U01 | Not observed | Chat 2 did **not** receive a submitted reviewer instruction during trial 001. The launcher stopped before Send. No step-002 review result was found on the trial branch. |
| U02 | Not observed | Chat 3 was not launched or audited; therefore no three-chat or indefinite-chain result exists. |
| U03 | Not implemented/tested | No verified controller interprets `NEED_MORE_TIME`, `TASK_COMPLETE` and `ERROR` terminal markers and performs all three actions. |
| U04 | Not implemented/tested | No successful run to 30 distinct chats; 30 is a requested configurable bound, not a demonstrated capability. |
| U05 | Not directly captured | The exact composer Value **at the moment** of the failed Chat 2 launch. Later read-only inspection showed a placeholder and the launcher compared against empty string; likely causal, not strictly proven. |
| U06 | Not demonstrated | How many consecutive same-thread “Okay, continue working” continuations are reliable at context/resource limits. |
| U07 | Not demonstrated | How the selected worker will initiate successor browsing after emitting its final status; an external controller or accessible desktop tool must actually perform it. |
| U08 | Not established | Guaranteed persistence of the final status marker in every reply when a worker runs out of budget, disconnects, stops mid-turn or encounters a tool error. |
| U09 | Not established | Whether semantic classification without a terminal marker can be performed reliably enough to launch another chat without manual correction. |
| U10 | Not established | Long-run reliability across Chrome updates, project navigation/UIA changes or mixed browser profile sessions. |
| U11 | Not copied as secrets | Chrome credentials, cookies, account passwords and the private SQLite journal bytes. They are outside the requested evidence scope; the observed journal `blocked` status is documented. |
| U12 | Scope distinction | Earlier `Chat 1 → 2 → 3` packet validator and one-shot SQLite journal were built for a finite pilot, not for an unrestricted persistent runner. Their restrictions must not be inferred as the owner's desired general security model. |

## Observed historical failure

- The first live Chat 2 attempt used a new window and strict `Value != ''` editor check. It recorded `blocked` without posting anything, then persisted a held run.
- Afterward, a read-only UIA probe showed the editor's *placeholder* in its Value field. The apparent root cause is **false classification of placeholder text as a user draft**, but this inference needs confirmation in a fresh, separate test rather than retroactively altering the failed run.
- This failure does not imply the GitHub handover failed: Chat 1's R1 and A2 were committed and read back.

## Sandbox-source collection note

A full authenticated GitHub clone cannot be performed by ordinary network Git inside the isolated sandbox: `git ls-remote` from the sandbox failed with `Could not resolve host: github.com`. The Windows/Ubuntu machine could access the repository. The precise source import method and any material not imported must be stated in `docs/SOURCE_INVENTORY.md`; do not label a partial snapshot “full history” unless its original commit objects and refs are verified.
