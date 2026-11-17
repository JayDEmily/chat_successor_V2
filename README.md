# chat_successor — Chat Succession

Explore continuing work through fresh ChatGPT conversations, with GitHub holding the durable instructions, results and next action.

`Chat 1 → GitHub → Chat 2 → GitHub → Chat 3 → …`

**Status:** Astra's continuing loop has an offline reference model and an implementation plan. Use the [Astra leaves and gates](docs/superpowers/plans/2026-11-18-astra-succession-execution.md) for the implementation handoff. Its live integration is pending.

The owner has created a blank ChatGPT Project called **Chat Succession** (the supplied screenshot displays “Chat succession folder”). Its browser URL and tool configuration have not yet been verified.

## Read in order

1. [Design and scope](docs/superpowers/specs/2026-11-17-chat-succession-design.md)
2. [Astra implementation leaves and gates](docs/superpowers/plans/2026-11-18-astra-succession-execution.md) or the [original exploration plan](docs/superpowers/plans/2026-11-17-chat-succession.md) for the earlier trial
3. [Progress](PROGRESS.md)
4. [Evidence and provenance](docs/PROVENANCE.md)
5. [Proposed Project instructions](docs/PROJECT_INSTRUCTIONS.md)

The original exploration proposed a fixed three-chat trial. Astra's continuing loop reuses the proven desktop method, routes on three worker statuses and sends a short repo/branch pointer. Each run has a configurable cap on distinct saved chats.

Returning to the original chat, discovering the original iPhone conversation and forwarding answer bodies are outside this exploration's requirements. The Second Chat OCR project continues separately.

The current handoff and evidence are recorded in [PROGRESS.md](PROGRESS.md).
