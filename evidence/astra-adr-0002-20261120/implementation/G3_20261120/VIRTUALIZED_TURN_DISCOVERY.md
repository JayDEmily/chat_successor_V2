# A2-G3 read-only virtualized-turn discovery — 20 November 2026

**Disposition:** A2-G3 remains `NOT_RUN`; this is diagnostic preparation for A2-L07, not a live success or a new controller run. **Installed source:** `5c86ad6d735b4c0626c49aedfdb93aeb95e6199b`, following the A2-G2 publication `85483c05c3dac06989eab98c41c935434f58ba6d`.

## Actual observed UI Automation structure

The completed, disposable Bird and Pig trial was read through the exact *James Student* Chrome profile and saved ChatGPT Project/chat using the current canonical installed Windows backend. The diagnostic selected exactly one verified Chrome window. It only enumerated accessibility roles, classes and structural counts; no navigation, typing, Send, worker launch, controller action or browser close was performed.

- **One** `thread-scroll-container` transcript region, **one** direct `transcriptContent-…` layout and **one** `relative shrink-0` wrapper.
- **Zero** accessibility `article` nodes under that transcript. The existing `Get-ConversationTurns` implementation requires articles to qualify role headings and turns.
- The wrapper had **14 direct children**. Position 1 was the application's `You said:` heading, directly followed by a user body group at position 2 (classes including `bg-user-message` and `text-user-message`). Position 7 was the application's `ChatGPT said:` heading, directly followed by a `Renderer-…` assistant group at position 8. Other direct children included buttons and a separator; they must not be treated as message boundaries or text.
- The assistant body exposed **42 accessibility text nodes**, including **one** text node matching an exact terminal status keyword. Text presence alone does not establish that it is final assistant prose, that the body is complete or that the visible assistant is the latest accountable turn.
- The completed fixture journal held four consumed responses across two saved chats, including **one** for the presently observed chat. A naive SHA-256 over all visible assistant-body text nodes did **not** match the short digest embedded in that saved response ID. That mismatch may reflect extraction differences between renderers; it is not evidence of altered Git or journal state.

## Safety interpretation and next eligible work

`Read-SavedWorkerIdentity` on `5c86ad6` successfully proves a stable saved-view identity. The established article-based `Read-CurrentTurn` / `Find-PostedMessage` path remains unable to verify this virtualized assistant's exact actionable turn and user anchor. Replacing article membership with raw heading/text matching would risk accepting stale, incomplete or quoted status text and would not on its own reconcile the persisted response identity.

**Next step within A2-L07:** qualify a bounded virtualized-turn reader against the observed direct heading/body structure, requiring complete latest-turn coverage, a stable response and user anchor compatible with the controller journal, and fail-closed behaviour for unverified trailing content, nested labels, duplicate headings, streaming, stale reloads and draft/posted-turn readback. Verify this *offline* with native negative/positive tests, then separately on the disposable completed view, followed by independent source-pinned review before any live Send or paired-run trial. Do not infer a positive V03 stale recovery from a preserved identity-only view.

This discovery does not close A2-D01–D03, S04–S09, V01–V06, owner iPhone approval, capacity or release. Preserve the original paused Rowing/SolidWorks runs and do not merge to `main`.

**Private diagnostic evidence on Windows:** `C:\Users\james\AppData\Local\Temp\chat_succession_g3_virtualized_tree_readonly.ps1`. It contains the exact disposable Project/chat locator, so the unredacted script remains local rather than published.
