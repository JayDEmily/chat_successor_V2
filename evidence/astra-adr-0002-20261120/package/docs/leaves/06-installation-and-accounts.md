# A2-L06 — Verify Windows release and both account routes

**Prerequisite:** A2-G1 and explicit owner permission for installation/account checks. **Gate:** A2-G2. **Checks:** A2-W01–W03, live no-Send portions of R01/R02/V01/V05.

## Expected outcome

An exact installed candidate is bound to each intended account, the native state path and the correct signed-in Chrome profile. No-Send preflight proves the selected Project and published branch, not complete end-to-end acceptance.

## Ordered checks

1. Record candidate source/backend revision, package bytes, actual private plugin identity/version/skill/connector binding and actual wrapper hash/body. The supplied redacted wrapper cannot validate its displayed hash; capture the installed file privately.
2. Verify Shoco/“Shoko” and James Student mappings separately. Historical Profile 11 and Profile 13 are clues to recheck, not defaults to assume. Unknown account/launcher/profile must hold. Do not silently update the other account's private plugin.
3. Verify wrapper → backend → `--install-root` → request/config/journal/owner-input location. Read the same root as a worker would. Confirm native NTFS lock placement and one-controller ownership.
4. Run the PowerShell parser, `test_worker_view_recovery.ps1`, UTF-8 observation/receipt comparisons, and a read-only saved-chat reopen. Record that these helper tests do not establish a newer-completed-response stale reload.
5. Run exact Project/repo/branch `--check`: remote ref readback, fresh empty composer, correct account/Project, no attachments; owned temporary window closes. Snapshot state/intents/counts/markers before and after: unchanged, no posted prompt.
6. Near-simultaneous two-window lookup/preflight requests verify unique-window assignment, session mutex wait/release and cleanup. Test abandoned-mutex handling in an isolated diagnostic process. No lock is held across model work.
7. Switch account entry routes and return. Each selects its own profile/backend/root/run; a wrong-route request is rejected with zero effects. Existing paused journals and terminal runs remain preserved.

## Evidence

Private release/route receipt with hashes and non-secret account aliases, no-Send process output, Windows/Python/Chrome versions, PowerShell logs, before/after state hashes, window lifecycle record, Git ref SHA and mutex timings. Store any account-identifying screenshots privately and redact public copies.

The baseline ZIP SHA is in the source index. If L02–L05 changed source, this gate must identify a **new candidate**; do not call it an unchanged Shoco 0.4.3 pass. Record the earlier James route independently if it remains a different compatible version.

## Hold / failure

Any sign-in screen, unknown account, ambiguous root/window, draft, incompatible state or wrong branch blocks live Sends. Preserve old installation/state and diagnostics. Do not clear a draft, change credentials, globally close Chrome or try the sibling account as a workaround. Roll back only after controllers are safely stopped and state compatibility is established.

Sources: S03/S04/S06/S12/S13/S16; V05 is package comparison only.
