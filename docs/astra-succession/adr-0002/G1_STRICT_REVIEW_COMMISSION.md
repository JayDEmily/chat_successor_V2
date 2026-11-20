# Strict independent A2-G1 case reviewer commission

Act as a separate independent ADR 0002 offline G1 reviewer, **not** the worker who authored L02–L05 or its G1 receiver precheck.

## Immutable candidate and authority

- Private GitHub repository: JayDEmily/chat_successor.
- Review **only** candidate commit **9a2fc382049a548adfefb5ed26a202c715988ca2**, direct parent **f20f1b14080c58f80a6e4e646d7ba5173d8791a9**, working branch codex/chat-succession-finish.
- Compare against exact Astra source: evidence/astra-adr-0002-20261120/package/ docs/leaves/{02,03,04,05} and acceptance/cases.csv, plus accepted docs/adr/0002-account-bound-resumable-runs.md.
- Read full L02/L03 negative-repair reports, L04 view qualification, L05_RESULT and G1_20261120/RECEIVER_AUDIT.md.
- User standing authorisation covers offline source analysis and independent tests. **Do not** touch live Rowing or SolidWorks, private browser sessions, account credentials, project folders, installed wrappers/plugin, launcher state, paused journals, or main. This is strictly OFFLINE/NO SEND.

## Required fresh verification

1. Clone from GitHub into a new local directory; verify commit, direct parent, tree, clean status, Git fsck and exact source/evidence file readback. Do not trust an unpushed checkout, a prior reviewer claim or test summary alone.
2. Independently execute all Python integration tests and all original reference tests, **no skipped tests**; on an actual Windows PowerShell environment run parser/function-only action and view test scripts. Report actual test count, runtime and command/exit status.
3. Audit all **24 exact A2-G1 cases** (A2-R01–R04; S01–S09; V01–V06; O01–O05) against the literal acceptance/cases.csv, the code and targeted negative evidence; make a per-case OFFLINE_PASS / HOLD / NOT_RUN decision. Treat later live predicates separately.
4. Specifically attempt to falsify exact account→plugin→native root→backend→Chrome-profile routing, duplicate/unknown route rejection, legacy pause and cap preservation, exact action/route/response/message/handle check at the native click gate, no duplicate uncertain Send, bootstrap resume/draft safety, missing/stale view replay, scope/hold deduplication, and no fabricated approval delivery.
5. Trace publication validation from fetched remote SHA/ref, worker/run trailers and response anchor through journal save/adoption. Distinguish documented private diagnostics from persistently saved Git SHA and do not infer work quality from trailers.
6. Reconcile source compatibility with Python 3.13 installed and CPython 3.14 Ubuntu mock; do not equate passing a 3.14 run with Windows 3.13 binary compatibility. Verify PowerShell parse and no-effect check on actual Windows.
7. Record first observed defects with exact negative reproduction; no silent test weakening. If no defect is found, independently justify the narrow offline verdict and explicit G2 live requirements.

## Deliverable and exit

Return a single independent G1 report with exact candidate SHA, tree and parent, case matrix, run commands/outputs, findings and an unambiguous **A2-G1 OFFLINE ACCEPT / HOLD** verdict, preserving live G2–G6 as NOT_RUN. Record independent review identity and verify publication in a branch that does not overwrite simultaneous worker work. No product source modifications, merge, new controller Send or installation under this reviewer commission.
