# A2-L07 independent review commission — virtualized-turn safety candidate

**Review source (immutable):** `e33ae7ad49e3510bf3021c552184cbb9d0e05758` on `JayDEmily/chat_successor`, branch `codex/chat-succession-finish`. **Parent:** `34c8b790492f0e07d016f869350cf65aa46001da`. The source has been published; a reviewer must independently read it from a fresh checkout. Later documentation commits are outside the candidate source.

**Authority and scope:** Accepted ADR 0002, ordered A2-L07 / A2-G3. This is a **source review**, not approval to install the candidate or initiate a controller, browser Send, iPhone approval, real Rowing or SolidWorks action, or production release. The older G2 installed candidate `5c86ad6` and existing pause markers must remain intact.

## Sources to inspect

- `AGENTS.md`, `PROGRESS.md`, `docs/adr/0002-account-bound-resumable-runs.md`, `evidence/astra-adr-0002-20261120/package/acceptance/GATES.md`, and `package/docs/leaves/07-two-run-acceptance.md`.
- Source diff against the parent in `integration/uia_adapter.ps1`. Check the legacy article branch, the new `Get-VirtualizedConversationTurns`, `Get-ConversationTurns`, `Read-ConversationContent`, `Read-CurrentTurn` and `Find-PostedMessage`.
- Native test changes in `integration/tests/test_a2_l03_ps_action_gate.ps1` and `integration/tests/test_a2_g3_ps_virtualized_turns.ps1`, plus the [candidate report and raw tests](../../../evidence/astra-adr-0002-20261120/implementation/G3_20261120/virtualized-reader-candidate/CANDIDATE_RESULT.md).

## Mandatory independent challenges

1. **No stale or duplicate advancement:** a virtualized view must never produce `ready=true`, a response ID, absolute turn count, latest-user anchor, posted-message acknowledgement or stale-reload entitlement merely because a terminal status string is visible. Challenge same-text older responses and re-rendered body digests.
2. **Boundaries:** inspect missing, duplicate and nested `You said:` / `ChatGPT said:` headings; changed body classes, orphaned groups, unknown trailing content, mixed article/new virtualized turns, multiple transcript regions and re-ordered rows. No earlier article must be accepted when newer content is unverified.
3. **Existing contract:** ordinary fully verified article-based readbacks must continue to support positive exact action/Send receipts, terminal prose, user-body completeness and streaming holds. Test `Read-CurrentTurn`, `Find-PostedMessage`, owner re-entry, safe stale observation and no-effect dispatch boundaries together.
4. **Repeatability:** verify the exact Git SHA and clean status; run native positive/negative tests from the pinned checkout, and check the preserved 114 integration/119 reference baseline. Inspect the redacted Windows read-only fixture proof without treating it as an independent run or a positive G3 gate.

Record a precise **OFFLINE ACCEPT** or **OFFLINE HOLD** for this narrow candidate with the actual source SHA, reproduced commands, failures and any corrective leaf. Even an offline accept **does not close A2-G3**: affirmative latest-turn attribution, live posted-user receipts, positive stale recovery and two concurrent disposable mock runs remain unverified. Never infer full acceptance from four native test exits. A candidate failing any safety assertion cannot be installed or used for Send.

The original owner-paused Rowing and SolidWorks runs must not be touched. Private owner text, browser transcripts and account credentials are not for GitHub.
