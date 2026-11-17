# Leaf 03 — Wrap the proven desktop method

**Entry:** Leaf 02. **Output:** `succession/adapters/desktop.py` and `tests/test_desktop_adapter.py`. Implement the [adapter seam](../../../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/docs/PROTOCOL_AND_ADAPTER.md) using a fake desktop driver in offline tests.

| Operation | Interface and observation |
| --- | --- |
| Observe | `observe_current_assistant() -> Response \| None` supplies full text, role, saved chat ID, active Project, stable turn ID and actual completion. Repeated polls use the same ID. Regeneration/editing of a consumed response holds for reconciliation. |
| Prepare | `prepare(pending: Pending, project: str) -> PreparedDestination` handles the same saved chat or prepares a fresh composer through the nominated Project. It observes active destination and a `ComposerObservation`. Allow text entry only at a verified empty editor, then verify exact payload readback. Preparation never clicks Send. |
| Submit | `send_once(destination: PreparedDestination) -> SendObservation` verifies the prepared target and exact text still match, then issues at most one click. A positive receipt includes the observed posted message, Project and saved ID, tied to the prepared action. |
| Reconcile | `reconcile(pending: Pending) -> SendObservation` inspects existing UI/history without writing. Represent `submitted`, `not_sent` with positive evidence, or `unknown`. Include the evidence or reason. |

1. Add driver tests for a Project visible only in the sidebar, wrong active composer, real text identical to a placeholder, attachment-only draft, unknown editable content, exact payload readback mismatch, stale target, a single click followed by timeout and a recovered receipt. Assert zero typing into wrong/occupied/unknown editors, zero Send on failed readback, and one click total on timeout. Exercise stable turn identity with streaming, repeated polls and completed replies.
2. Bind the owner's working navigation/Send primitives when available. The [historical launcher](https://github.com/JayDEmily/chat_successor/blob/3b2c95b954eb90b1e6c9b82403dd1956c6f34b39/launcher/launch.ps1) is a source reference for target/focus/readback, and its trial receipt documents the editor guard failure. Use independently observed actual editable content and attachments with `classify_composer`. UIA Value alone leaves the editor unknown. Keep the historical pinned packets, fixed three-chat budget and journal out of the new adapter. If the available launcher cannot isolate its UI primitives or retries internally, expose the required seams or record the blocker. Never launch it as an opaque second actor.
3. Derive actual browser selectors and editor observations during Leaf 05. Until then the driver tests use supplied observations. Record which observations still need binding in the owner environment.

**Leaf check:** Run `python -m unittest discover -s tests -p "test_desktop_adapter.py" -v`. The fake driver proves the adapter guards and reports the correct evidence at every boundary. Any new PowerShell wrapper must also parse cleanly on Windows. Commit and advance to Leaf 04.
