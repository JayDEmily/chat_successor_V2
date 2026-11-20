# ADR 0002 independent mock fixture allocation

**Decision:** All live acceptance uses isolated disposable ChatGPT Projects;
never use the active Rowing or SolidWorks Projects. Standing authority from
the owner to create and operate new mock Projects and repositories applies.

## Available GitHub assets

| Purpose | Repo | Notes |
| --- | --- | --- |
| Realistic source-size and worker handoff | `JayDEmily/rowing-clone-test` | Private repo created 20 Nov 2026; snapshot of `rowing2026` `main@5b04bd24` stored under `snapshot/`, test assignment at repo root. Published and verified `main@f2c28775532bc3f828af95edd6c61258f6313496`; snapshot tree `31e770b057f5c9ac8d610c0aed5ad2f24db1c144` equals the pinned source tree. |
| Two-worker normal completion | `JayDEmily/chat-succession-cat-dog-pair` | Existing disposable story fixture; use fresh branch and verified current Project |
| Cap with eligible third step | `JayDEmily/chat-succession-bird-pig` | Existing disposable story fixture; use fresh branch and verified current Project |
| Phone approval | `JayDEmily/chat-succession-trial-approval` | Existing approval seed branch `codex/g2-iphone-approval-shoco-20261120`; verify it remains clean before use |

### Proposed new ChatGPT Project names

- `Chat Succession ADR2 — Finish Test`
- `Chat Succession ADR2 — Cap Test`
- `Chat Succession ADR2 — Approval Test`

These are **proposed names, not claims that the Projects currently exist**.
They will be created in the verified intended account and their exact URLs
and IDs recorded privately. A test is not authorised merely by a matching
display name; positively verify the Project identity and account/profile.

## Explicit non-targets

Neither `JayDEmily/rowing2026` nor `JayDEmily/sw_v1`, nor Project A Test
or Project B Test, are targets for new acceptance Sends. Their existing
paused journals and markers must stay unchanged.

## Gate design

A2-G3: two separate mock Projects and repos/branches; one normal finish, one
STOP_CAP with work eligible; simultaneous observer overlap, pause/restart,
positive same-worker view recovery, and fault evidence. A2-G4: separate fresh
mock approval Project with the current Shoco private plugin. A2-G5:
similarly isolated mock cohorts with measured PC resources. Preserve exact
Astra case IDs and expected outcomes rather than claiming equivalent
results from historical projects.
