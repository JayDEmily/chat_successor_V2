# A2-L02 — Bind account and installation route

**Prerequisite:** A2-G0. **Gate:** part of A2-G1. **Checks:** A2-R01–R04. **Touch only:** existing wrapper/discovery contract, `launch_project.py`, `cli.py`, dependency construction and focused tests.

## Expected outcome

A start, resume or recovery has one explicit account → plugin → native installation → backend → signed-in Chrome-profile route. A changed connector LocalAppData, display name or branch cannot silently create a different worker or route to the other account.

## Smallest implementation

- Preserve the canonical native installation root and current `Requests` / `Runs/<run-id>` layout. Make wrapper and worker lookup resolve that same root. Keep the old wrapper for compatible rollback.
- Extend the private config with a non-secret account key and verified profile/route receipt; choose the child's profile from that binding. Unknown connector environment or conflicting launcher discovery holds rather than using a permissive default.
- Namespace new run selection/creation by account plus stable Project ID and normalized repo. Keep one nonterminal owner per combination and stable new-job request IDs. Do not recalculate legacy run IDs.
- Add conservative legacy binding: positively verify existing account/Project/profile/root under lock, preserve every state/history/cap field, or hold for owner confirmation.
- Expose a read-only status including chosen route, worker/count/cap, entry/effective branch, pending action, pause requested/acknowledged, terminal reason and last publication evidence. Inspection must not mutate journals or release pause.
- Generate valid 24-character job IDs internally once. Keep the existing 24–64-character owner-input ID contract.

## Exact checks and evidence

| Case | Check |
| --- | --- |
| R01 | Correct Shoco and James route records independently resolve the intended private plugin, root, backend and explicit profile; worker/controller read the same run path. Store non-secret route readback. |
| R02 | Unknown account, wrong profile, unverified login, duplicate wrapper or conflicting route: zero bootstrap intent, zero typed text, zero Send. Preserve all existing journals. |
| R03 | Project rename, repo-case normalization, verified checkpoint rotation and repeated request retain run/count/cap. A genuinely new stable job ID after a terminal run creates only one new run; duplicate new request returns it. Invalid 32-character job ID fails before effects. |
| R04 | Legacy paused/configured/registered/uncertain/terminal states either bind explicitly without semantic changes or hold. No replacement bootstrap. Status distinguishes a marker just written from controller acknowledgement, addressing P09. |

P07 must become a positive regression for the new documented fields, not be removed to hide the characterization. Re-run existing request/owner/story tests and both old suites; log actual counts.

## Hold / failure

Any identity mismatch blocks that run before browser effects. A held account does not authorize fallback to its sibling or wiping shared state. Do not migrate a pending action by guessing its route. Capture the exact mismatch and return to this leaf; no live acceptance until the offline contract passes.

Sources: S03/S10/S11/S12; F01/F03/F06/F07 and V07.
