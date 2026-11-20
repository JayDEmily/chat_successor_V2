# Independent read-only saved-view recovery review

**Verdict — OFFLINE ACCEPT for the read-only recovery repair.** 20 November 2026 AEDT. Source `5c86ad6d735b4c0626c49aedfdb93aeb95e6199b`, tree `483f3e7b3366e81ae0acc3f1873406907eb53501`, parent `e6868fd78d65ddc8d13cfaa8ee0ddcb7966e3300`. Reviewer — Codex independent reviewer `g1_reviewer`.

Fresh GitHub clones on Windows and Ubuntu matched the commit, tree and parent, started clean and passed `git fsck --full`. On Windows CPython 3.13.15, all 114 integration tests passed in 29.048 s and all 119 reference tests passed in 14.620 s. On Ubuntu CPython 3.14.4, the same suites passed in 2.044 s and 1.340 s. All exited zero with zero skips. Native Windows PowerShell 5.1.26100.9818 passed the action/full-turn helper, view/profile helper and legacy recovery comparison scripts.

## Independent negative checks

A separate native PowerShell fixture extracted the pinned recovery and strict-turn functions. Synthetic windows supplied handles, profiles, URLs and accessibility structure. Test doubles recorded owned-window open and close operations.

- A complete virtualized view restored after two stable identity reads. Its identity contained only the address, document ID and user heading ID. The owned restored window was retained.
- Incorrect profile, missing heading/body pair, continuously changing document ID and changed address held. The failed opened probes closed once.
- A duplicate appearing at final validation and a pause arriving before the recovery result each held and closed only the owned probe. A pre-existing duplicate appeared before acquisition and neither existing window was closed.
- With an exact expected user message and an assistant completion marker inside virtualized groups, the strict observer produced no ready status, response ID or user anchor. Anchored and unanchored posted-message checks returned false. The anchorless idle owner check returned unknown. The existing Stop path can indicate observer-only advancement and supplies no delivery proof or new input.
- Direct stale recovery stopped before opening a window on this virtualized fixture. The Python integration test confirmed that anchorless observation cannot arm the stale timer. The delta leaves the strict stale comparison, Send receipt and owner-anchor paths separate from the identity-only helper.

This review supports the limited W03/V01 read-only code repair. Installed checks still need actual saved-view stability and unchanged journal evidence on the candidate. Stale reload, actionable turn qualification, live Send and approval receipt remain separate gate evidence. [Published recovery criteria](../../../package/acceptance/GATES.md) · [Original G2 preflight](../PREFLIGHT.md)
