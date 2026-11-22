# M04 — authorised scope and preflight specification

**Status:** owner resource authority granted on 22 November 2026 AEDT; execution remains conditional on independent M03 review (issue #2). This is preparation, not native qualification.

## Authority

Following publication of M03, the owner explicitly replied, "Okay, I give you authority, continue." This accepts the preceding recommendation: one isolated MCP service, one dedicated private tunnel and private plugin, separately scoped credentials, at most eight native tool calls across at most two disposable chats, following successful independent M03 review. No routine further owner approval for this specific scope. No authority to bypass platform consent or the review gate, launch unattended successors, alter the original implementation, use the Chrome extension, change LTM-RAG, merge/deploy, or provision additional infrastructure outside the approved scope.

## Preflight stop conditions

1. Require separate source-pinned M03 PASS on the finally accepted candidate; if RETURN_TO_WORKER, repair and re-review. Issue #2 was open with no comments when checked. No independent reviewer-dispatch operation is exposed to this chat's tools. Historical browser-based dispatch is not an authorised fallback for this milestone. Do not mistake the worker's fresh-checkout tests for independent review.
2. Confirm intended account/Platform organisation and supported permissions without publishing identifiers. Select a fresh private loopback endpoint, private working directory and separate audit ledger; confirm no listener collision before start. Require a resource-specific runtime credential with only needed tunnel permissions; never read, expose or reuse other service credentials. No changes to existing services, profiles or environment/global configuration. Use documented tunnel setup and private custom MCP plugin creation only. If permission or consent is unavailable, record the exact blocker.
3. Establish a supported end-user authentication route before enabling state-mutating registration/report calls. OpenAI's [authentication guide](https://developers.openai.com/plugins/build/auth) describes OAuth 2.1 with PKCE and per-request token signature, issuer, audience, expiry and scope validation. Its [tunnel guide](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) explains that the tunnel does not automatically expose an OAuth authorization server. A private tunnel authenticates transport, not the human. Do not substitute a hardcoded principal, model-supplied account, anonymous subject or one-time challenge for authenticated context. No new public auth host/provider is implicit in this grant; if no separately scoped reachable supported auth route exists, hold the authenticated trial. Do not implement an ad hoc auth server for convenience.
4. [Plugin reference](https://developers.openai.com/plugins/reference) documents openai/session and openai/subject metadata. Use opaque, private keyed digests for comparisons and never publish raw values. Absence, collision or contradictory values fail the relevant predicate. Discovery and metadata do not establish native saved-chat identity.
5. Enable only two narrowly defined synthetic tool handlers after authorisation. Both mutate a synthetic ledger, advertise appropriate write annotations and never expose a native sender, arbitrary command execution, external URLs or Git writes. Stage the fixed synthetic Git publication as a separate explicitly scoped repository branch object (no new repository or live worker access needed); read exact remote Git commit and verify the authorised synthetic alias, run and expected payload independently. Keep M03-delivery and quiescence inputs unqualified for live operation: the M04 harness may test downstream handler behaviour with labelled synthetic evidence, but cannot adopt an actual worker, advance a real controller or claim native delivery. M05 must qualify actual identity/receipt and quiet state.

## Proposed native envelope (fixed upper limit, conditional on preflight)

Two disposable, manually initiated chats A and B; each tool call is an explicit synthetic instruction. No automatic sends/continuations, no access to real transcripts or ordinary projects. Do not use current development conversation as a fixture. Before first native invocation freeze exact fixture inputs, unique run/action identifiers, schema, request order and expected per-call result in a private record, with public redacted manifest and hash. Limit any necessary user action to the bounded fixture and platform consent. Tests run sequentially; do not automatically repeat a call whose outcome is unknown.

| Call | Chat | Operation | Expected isolated observation |
| --- | --- | --- | --- |
| N01 | A | register approved synthetic reservation | authenticated principal/scope plus metadata; durable provisional registration only |
| N02 | A | exact duplicate registration | same receipt, no extra registration |
| N03 | A | report against that reservation after explicitly labelled synthetic delivery | one accepted synthetic report; no native action |
| N04 | A | identical report retry | duplicate response, no second consumption or effect |
| N05 | B | try A's registration challenge | reject cross-session conflict, unchanged ledger |
| N06 | B | register B's independent disposable reservation | distinct session and consistent authenticated subject; provisional only |
| N07 | B | report wrong synthetic publication SHA or incompatible status | reject/hold according to exact frozen case; no consumption |
| N08 | B | after bounded reconnection and positively reconciled repair of synthetic input, report independently verified synthetic publication | accepted only if exact authorised state; same chat/session correlation, no action |

No more than eight handler invocations, including rejected and duplicate calls. Persist and reserve count before processing (atomic and restart-resistant), not only on success. Reject any additional attempt without mutation other than denial auditing; stop at unknown outcome or unexpected count and retain evidence. Do not claim a clean eight-call run after extra attempts. Track discovery separately from invocations. Test missing/invalid/expired auth, metadata absence, schema rejection, quota exhaustion and replay offline before native calls; never spend extra native calls on retries. A transport disconnect does not authorise resending a possibly processed call. A reconnect test may pause and restart only the newly dedicated client within scope; no shared services.

## Acceptance and teardown

For each cell record actual handler invocation order, redacted auth decision, private correlation check, receipt classification, quota count, independently read synthetic Git SHA and unchanged no-dispatch state. Report verified transport/identity facts vs mock delivery and Git fixture; preserve failed tests and missing evidence. Verify separate resource and plugin status, then stop the dedicated test listener/client and securely disable or revoke only disposable credentials and test access as applicable; preserve private redacted audit and Git records. Do not touch original installations. Native result remains NOT_RUN until actual calls observed. All setup and trial code/tests must be source-pinned and available for review under AGENTS.md. M05 remains separate.

Reviewed current official documentation on 22 November 2026. No service, credential, user account or plugin has been modified by this preflight specification.
