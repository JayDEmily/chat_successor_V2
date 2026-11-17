# Leaf 01 — Adopt the offline controller

**Entry:** G0. **Output:** Astra's reference controller available to the continuing loop.

1. Reuse `Config`, `Response`, `Controller` and the existing parser in Astra's [reference package](../../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/succession/). Configure the nominated Project, repo, working branch and maximum distinct saved chats. Initialize the model with the observed first worker.
2. Preserve Astra's three statuses, exact continuation text, short successor pointer, event deduplication, count and stop behavior. Use the existing controller's prepare, save/load and recovery methods when wiring the adapter in Leaf 04.

**Leaf check:** Use Astra's existing P01–P36 and C01–C36 results for parser, routing, count and controller persistence. The [recorded offline pass](../README.md#evidence-available-at-entry) covers the unchanged reference model. Advance to Leaf 02.
