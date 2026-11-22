# ADR 0003 — MCP-native Chat Succession direction

- **Decision date:** 22 November 2026.
- **Status:** Owner-selected direction for investigation and bounded engineering; no production acceptance.
- **Scope:** Public `JayDEmily/chat_successor_V2`, branch `work/mcp-native-succession-20261122`. Other branches/installations and projects remain unchanged.
- **Supersession:** On this branch only, replaces ADR 0002's Chrome-dependent implementation direction and its active execution sequence; retains ADR 0001/0002's compatible functional and safety requirements. [PLANS.md](../../PLANS.md) is the active plan.

## Decision and rationale

Move away from the Google Chrome extension. Investigate a dedicated MCP service, reached through an isolated private outbound tunnel, with explicit worker registration and completion reports; independent Git publication verification and durable single-controller action state. Investigate the native ChatGPT desktop application and a minimal Windows UI Automation launcher for creating and controlling fresh workers. Reuse existing Python/controller contracts where applicable; do not choose an EXE language or rebuild the core without evidence.

Earlier Chrome-owned extension work encountered intermittent action admission, service-worker lifecycle and document injection problems. The later read-only reader helped qualify rendered identity but encountered stale sample/lifecycle dependency. The [public offline PR](https://github.com/JayDEmily/chat_successor_V2/pull/1) is retained as evidence, not the new architecture baseline.

LTM-RAG V2 supplies a reference pattern: [native tunnel verification](https://github.com/JayDEmily/LTM_RAG_V2/blob/0aa4b8042fc60991aa8a7d9d2278314b52efa24d/vnext/TRIAL_G_CONNECTION_VERIFICATION_20261119.md), [post-restart plugin smoke](https://github.com/JayDEmily/LTM_RAG_V2/blob/0aa4b8042fc60991aa8a7d9d2278314b52efa24d/vnext/POST_RESTART_CONNECTED_PLUGIN_SMOKE_20261118.md), and [Stage K native metadata evidence](https://github.com/JayDEmily/LTM_RAG_V2/blob/0aa4b8042fc60991aa8a7d9d2278314b52efa24d/vnext/MCP_METADATA_K_NATIVE_RESULTS_20261120.md). Those results are not proof of Chat Succession launch, worker authority, source-message identity or owner consent. Reuse the pattern, never its services or credentials.

## Authority and unresolved design

Preserve bounded worker caps, positive verified routing and delivery, same-chat continuation, scoped approval, pause/recovery, independent Git verification, no blind retry, exactly one dispatch authority, and independent review. Treat client metadata as correlation, not authentication or original-turn attestation. Tool call, accepted work completion, independently verified publication, quiescence, and actual successor delivery are distinct.

MCP calls may be unavailable, omitted, repeated or premature. Native desktop launch/control, stable worker binding, session-to-saved-chat mapping, authentication, replay resistance and safe completion semantics require testing. MCP Events are optional, not assumed necessary or able to create a conversation. No unsupported internal ChatGPT APIs or Chrome-extension fallback. If feasibility fails, hold and report rather than silently lower acceptance.

Authorises the selected direction and ordinary scoped engineering under [AGENTS.md](../../AGENTS.md) and [PLANS.md](../../PLANS.md); does not release old run holds, install a plugin, create credentials/resources, submit an unapproved message, or approve a deployment. The precise protocol and live-test boundary must be established in the plan before use.
