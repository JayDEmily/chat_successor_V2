# A2-L07 virtualized-turn structural reader — candidate and source-review handoff

**Date:** 20 November 2026 AEDT. **Base:** `34c8b790492f0e07d016f869350cf65aa46001da`; authorised branch `codex/chat-succession-finish`. This candidate has not been installed. The canonical Windows installation remains pinned to `5c86ad6d735b4c0626c49aedfdb93aeb95e6199b`.

## Defined source change

- `integration/uia_adapter.ps1` adds a fallback that inspects virtualized conversation rows only when no `article` nodes are exposed. It requires exactly one transcript/layout/message wrapper and adjacent, correctly typed application role headings with direct body groups. Orphaned, duplicate, nested, mixed or unverified headings/body groups fail closed. The existing verified-article reader is retained.
- The new fallback deliberately refuses **all actionable response IDs, absolute turn counts, owner anchors, Send acknowledgements and stale-response reload predicates**. It may report a stable saved-view identity and `user_turn_seen`, but `ready=false` and `method=UIA_VIRTUALIZED_UNQUALIFIED`. A terminal status string inside a visible body does not change this.
- `Find-PostedMessage` always rejects a virtualized view as posted-turn evidence; mixed article and virtualized headings also reject an older article-based completion.
- `integration/tests/test_a2_g3_ps_virtualized_turns.ps1` adds direct-heading/body positive structure and negative ambiguous, changed-class, nested-heading, orphaned-body, streaming, and false Send-receipt assertions. The original `test_a2_l03_ps_action_gate.ps1` now includes a mixed-layout negative case.

## Fresh recorded checks

| Check | Result | Raw record |
| --- | --- | --- |
| Windows Python 3.13.15 integration | **114/114 PASS**, 0 skipped | [windows-integration.log](windows-integration.log) |
| Ubuntu Python integration (WSL) | **114/114 PASS**, 0 skipped | [ubuntu-integration.log](ubuntu-integration.log) |
| Windows Astra reference suite | **119/119 PASS** | [windows-reference.log](windows-reference.log) |
| Ubuntu Astra reference suite | **119/119 PASS** | [ubuntu-reference.log](ubuntu-reference.log) |
| Native PowerShell action, view, legacy recovery and new virtualized suite | **4/4 PASS** | [action](native-action.log), [view](native-view.log), [legacy](native-legacy-recovery.log), [virtualized](native-virtualized.log) |
| Existing completed disposable saved chat (James Student profile) | **PASS**, two stable reads, non-actionable; no Send, navigation or protected-file change | [redacted real readback](real-readonly-acceptance.json) |

## Published exact-source readback

The candidate source was published as `e33ae7ad49e3510bf3021c552184cbb9d0e05758` and read back from GitHub. A **separate clean shallow GitHub clone** in the Windows temporary workspace matched this SHA, had empty status, and completed `git fsck --full` successfully. The implementing worker separately reproduced **114/114 Windows integration PASS**, native action PASS and native virtualized-turn PASS on that exact Git tree. See [fresh-clone integration](fresh-clone-integration.log), [native action](fresh-clone-native-action.log), [native virtualized](fresh-clone-native-virtualized.log) and [fsck output](fresh-clone-fsck.log). This is source-pin replication by the implementing worker, not the separately required independent reviewer acceptance.

The [exact-SHA independent review commission](../../../../../docs/astra-succession/adr-0002/G3_VIRTUALIZED_REVIEW_COMMISSION.md) identifies the mandatory challenge cases. Installation and live work remain held.

## Safety and acceptance disposition

**A2-G3 stays NOT_RUN.** This is a fail-closed code candidate, not a successful unattended positive turn, live stale reload, paired-run D01–D03, owner approval or release. A complete absolute latest-turn identity still cannot be proved solely by Chrome's virtualized accessibility body groups. The earlier evidence of a visible terminal text node and a response-digest mismatch remains unresolved.

**Next required:** a *separate independent source-pinned review* of this candidate, including mixed layout/older status, user/assistant text truncation, nested role labels, streaming and absent absolute-ordinal cases. Only after independent acceptance should work continue on a positively attributable latest-turn identity. A new version must pass the normal exact-revision installed/release checks before live Send. Original Rowing and SolidWorks holds remain intact. No update to `main` or existing controller installation is authorised by this candidate alone.
