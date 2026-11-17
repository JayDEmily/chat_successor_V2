# Bounded trial 001 — Chat 1 to Chat 2 launch blocked

Date: 2026-11-17 (Australia/Melbourne). Experiment: `succession-20261117-001`.
Branch: `trial/succession-20261117-001`. Source checkpoint: `f8c002690c0a1a9ff4f298bd9a8d68b21f5ba1f8`.
Scope: `JayDEmily/chat_successor` only; existing checkout and other projects untouched.

## Immutable Git checkpoints

- A1 (run admitted and Chat 1 assignment): `846bd4ff12a558eefe5dbb6df65535d521d08ff9`.
- R1 (Chat 1 toy and result): `73eec3791fd5ae984db95bf7aeb9f8077ed6e18c`. The exact calculation is `17 * 23 + 19 = 410`, with `toy.json` and `result.json` the only R1 changed paths.
- A2 (Chat 1 handover and independent Chat 2 reviewer assignment): `898cd68740b2b46d75da1b9e195fe9e01bb9a685`.
- All three commits were pushed to GitHub; `git ls-remote`, fresh fetch/readback and `git diff --exit-code HEAD origin/trial/succession-20261117-001` checked the published heads at their respective checkpoints.
- Pinned A2 validator returned `{"ok":true,"errors":[]}`. The Ubuntu suite passed 37 tests.

## Live attempt and exact stopping reason

- Project destination was derived from the existing Chat Succession Project browser tab; only the private local Project configuration reference is stored in Git.
- Chrome profile configured as `Profile 13`, based on Chrome's local `last_used` profile metadata; this is not independent proof of the profile's signed-in account.
- Pinned launcher files were staged in a separate local Windows trial directory. SHA-256 of staged files matched source; PowerShell parser returned `PARSE_OK`; non-sending preflight returned `STATIC_PREFLIGHT_PASS` and `NO_SEND`.
- A new, initially empty private SQLite journal was explicitly initialised; key `(succession-20261117-001, 2)` was initially `absent`.
- One live `-ExecuteSend` invocation occurred with exact immutable assignment A2. The launcher reserved key 2 and opened a new Chrome window, but stopped at its editor-content guard. **Exact launcher error: `Launch blocked. No retry is permitted. Existing draft detected; preserve it`.**
- Post-attempt journal readback returned `{"state":"blocked"}`. The guard failed **before typing or Send**. There is no observed delivered Chat 2 user message. The existing composer text was not inspected, altered or disclosed.
- This is an observed launch blocker, not a proof that Project placement, saved conversation identity or future successor tool availability would have worked.

## Stop disposition

The run is held. Do not retry the same launch key, clear/recreate the journal, send the pinned prompt manually as a substitute, create step 3/4, or alter the preserved draft under this run. There is **no Chat 2 reviewer result, no Chat 3 audit, and no three-chat success claim**.

A later experiment requires separate owner authorisation and a fresh run; this record grants no restart.
