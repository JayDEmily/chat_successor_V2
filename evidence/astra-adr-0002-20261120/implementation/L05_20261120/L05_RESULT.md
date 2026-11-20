# A2-L05 — Scoped owner re-entry and published Git handoff

**Date:** 20 November 2026 AEDT. **Disposition:** L05 implementation OFFLINE CORROBORATED, not an independent final A2-G1 acceptance and not a live Windows/iPhone release. Parent: f20f1b14080c58f80a6e4e646d7ba5173d8791a9. No additional service, sender or publication protocol added.

## Changes to the existing controller

- integration/owner_reentry.py: when the observed original worker is already **advanced**, resume observation without another user input, but label the outcome worker_advanced_owner_input_unverified. An advanced conversation is not a receipt proving the proposed approval was delivered. Existing immutable owner context, one-hold deduplication and exact anchor checks remain.
- integration/runner.py: log the **actual fetched Git branch and commit SHA** after publication identity validation, separately log its adoption after the controller response/action state is durably saved, and record rejected publication checks as HOLD. Logs contain run/worker/response identifiers and SHA, **not private instruction bodies**. The reference controller journal schema remains unchanged, so the SHA is a private log diagnostic, **not** a persisted field in controller.json. A crash between the journal save and log could leave a diagnostic absent; that does not affect saved state or prove missing publication.
- Tests now use complete mocked published receipts including a commit SHA.

## Exact offline case-to-assertion evidence

| Case | Existing tests or new assertions | Disposition |
| --- | --- | --- |
| A2-S01 | test_streaming_never_dispatches; test_continuation_at_cap_does_not_create_new_chat; test_finished_programme_stops_without_composer; test_duplicate_completed_response_has_no_second_send | OFFLINE CORROBORATED |
| A2-S02 | test_generic_stale_run_and_published_hold_are_refused; test_generic_empty_duplicate_trailer_holds; test_git_timeout_is_a_publication_error; test_publication_outage_does_not_consume_turn_before_repair; test_invalid_unpublished_receipt_logs_hold_without_adoption | OFFLINE CORROBORATED |
| A2-S03 | test_published_checkpoint_rotates_once_and_survives_restart; test_locator_must_be_single_plain_line_before_explicit_completion | OFFLINE CORROBORATED |
| A2-O01 | test_preflight_checks_the_exact_branch_without_touching_existing_run; test_launch_branch_rename_and_explicit_new_job; test_lost_initial_acknowledgement_reconciles_without_resending | OFFLINE CORROBORATED |
| A2-O02 | test_idle_approval_persists_and_sends_once_without_counting_a_chat; test_matched_published_sha_logged_then_adopted_after_journal_save | OFFLINE CORROBORATED |
| A2-O03 | test_idle_approval_persists_and_sends_once_without_counting_a_chat (same/alternate IDs and conflict); test_repeated_prepared_owner_request_can_explicitly_release_pause | OFFLINE CORROBORATED |
| A2-O04 | test_advanced_worker_resumes_observation_without_delivery_claim; test_advanced_worker_not_misreported_as_owner_input_delivered; test_uncertain_owner_send_requires_positive_reconciliation | OFFLINE CORROBORATED |
| A2-O05 | test_keep_pause_and_hold_on_wrong_anchor_or_unreadable_browser; test_preflight_requires_verified_project_and_empty_composer; test_invalid_unpublished_receipt_logs_hold_without_adoption | OFFLINE CORROBORATED |

The mock suite covers branch publication through local temporary Git remotes and exact trailer validation; none of this asserts an actual browser post, real Shoco iPhone approval or completed external GitHub fixture.

## Actual executed checks

- [Raw 106-test integration log](integration_all.log): **106/106 PASS**, comprising 103 previously passing cases plus 3 targeted L05 regressions; no skips or unexpected failures.
- [Raw 119-test reference output](reference_119/test_output.txt): **119/119 PASS**, fresh execution of unchanged Astra reference kit.
- [Native Windows PowerShell action gate](powershell_action_gate.log) and [view-helper test](powershell_view_helper.log): PASS by AST-extracted helper checks, without invoking Chrome UIA modes.
- [Machine-readable summary](test_summary.json); Git diff check PASS.

## Remaining G1/G2 work

A2-G1 is not independently signed off merely because L02–L05 have passing offline suites. Independent end-to-end review must verify the exact candidate, R01–R04, S01–S09, V01–V06, O01–O05, old-run compatibility, and negative no-effects, before accepting the offline gate.

A2-G2–G6 are NOT_RUN. No private plugin/backend or installed launcher was changed; no live Chrome account, browser Send, iPhone approval, capacity test or paused Rowing/SolidWorks run was touched. Next: independent A2-G1 review from a fresh clone, repair any demonstrated defects, then proceed to scoped Windows account-route installation.
