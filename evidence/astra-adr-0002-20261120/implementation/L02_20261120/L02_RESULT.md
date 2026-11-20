# A2-L02 candidate: account and installation routing

**Scope:** Offline implementation only, no Windows installation or live
Send. **Parent baseline:** `2434584` after G0 acceptance and owner-requested
mock fixture isolation. **Next:** A2-L03 (durable pause/action identity).

## Implementation

- New `integration/account_routes.py` rejects missing, conflicting,
  malformed or unknown route entries once installation opts in via a private
  marker; private route record binds non-secret account key, native root,
  Chrome profile, plugin ID and backend commit.
- New bound run selection keys include account+Project ID+normalized repo;
  same account preserves the Project/branch run and immutable chat cap.
- Before any browser effect, the installed launcher selects an account-specific
  route; bound controller dependencies independently validate the saved
  profile/root/receipt. CLI bypass of an unbound legacy run is held.
- New explicitly requested job without a caller-supplied job ID derives a
  24-character stable ID from the private request file, avoiding owner ID entry.
  A repeated same-file request reuses the same new run.
- UIA invocations receive the explicit bound Chrome profile via their private
  environment, overriding ambient connector settings. Existing opt-out
  installations retain legacy behaviour until G2 migration is verified.
- Read-only status distinguishes pause marker requested and actual pause
  acknowledgement; route binding and pending action ID are visible, without
  pretending to know an unpersisted Git receipt commit.

## Actual offline results

- [79 integration tests](integration_79_tests.log) **PASS**, 63 existing
  and 16 new L02; no skips.
- [Reference 119 test suite](reference_119_offline_results.json) **PASS**;
  unchanged source kit and separate fresh execution.
- AST parse for all changed Python source and `git diff --check` **PASS**.
- No installed Windows route, real signed-in account, PowerShell/live Chrome,
  iPhone approval, fresh G3 runs, or capacity test was executed.

## Outstanding exact cases

R01–R04 have positive mocked routes and negative side-effect checks, **not
live acceptance**. G2 still must verify the actual two private plugins,
native launcher/root, signed-in profiles and backend binding. The original
Rowing/SolidWorks runs remain paused and unmodified. All G1 L03–L05 tests
remain pending.

[Private route activation procedure](../../../../docs/astra-succession/adr-0002/ACCOUNT_ROUTE_INSTALL.md).
