# ADR 0002 A2-G1 — Fresh receiver / coverage preflight

**Status: PRECHECK PASS, FORMAL INDEPENDENT ACCEPTANCE PENDING.** Date: 20 November 2026 AEDT. The exact published review candidate was commit **9a2fc382049a548adfefb5ed26a202c715988ca2**, direct parent **f20f1b14080c58f80a6e4e646d7ba5173d8791a9**.

This report comes from a **new, clean Ubuntu clone and new test execution**, but was prepared by the same developer/project-management assistant. It is **not** a separate independently designated model/tester decision. The formal G1 requirement stays OPEN until a separate reviewer checks this evidence and the actual source.

## Checks directly reproduced

- New clone exact commit and clean working tree before test execution; full Git fsck --full --no-reflogs PASS.
- [106 integration tests](integration_106.log): 106/106 PASS, no skipped/failing cases.
- [119 Astra baseline reference tests](reference_119/test_output.txt): 119/119 PASS, exact original reference kit, no skipped/failing cases.
- [Native Windows PowerShell action identity test](windows_ps_action_gate.log) and [native view helper test](windows_ps_view_helper.log): PASS; AST-extracted function tests only, **not** live Chrome or UIA mode execution.
- [A2-G1 case-to-test reconciliation](CASE_MATRIX.csv): 24 distinct A2-R/S/V/O case IDs were joined against 49 named test assertions verified to exist in the published source (some tests cover multiple cases). Coverage means targeted offline tests exist and execute, **not** that each full live predicate is proven.
- [Machine-readable summary](AUDIT_SUMMARY.json).

## Where these checks stop

A2-G1 formal independent review must still inspect exactly this code plus the L02–L05 evidence, including immutable no-click target checks, same-chat exact-anchor reconcile, current versus advanced owner receipt, durable bootstrap intent and native route preflight. A mock pass is not a real profile/login/account verification, actual Windows Send, stale Chrome positive recovery or phone approval.

A2-R01/R02 and V05 require real account/profile/native-root verification at **A2-G2**. Live S04–S09, V01–V06 and the two-worker overlapping fixture require **A2-G3**; O01–O05 require actual phone/worker trace at **A2-G4**. No held production Rowing/SolidWorks run was resumed.

## Strict disposition

- Offline precheck and runnable named-case inventory: PASS.
- **A2-G1 release decision: PENDING_SEPARATE_REVIEW**.
- Windows installation or new Send: NOT authorised on this precheck alone.
- A2-G2–G6: NOT_RUN.
