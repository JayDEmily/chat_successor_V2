# M04 — offline rehearsal and live preflight hold

22 November 2026 AEDT. M03 independently accepted on `064013839ad71f97aa4bfddb770497340ab28f46` ([PASS](https://github.com/JayDEmily/chat_successor_V2/issues/2#issuecomment-7072268126)). Rehearsal source `50339ed980b69de533a67d9a492e2dca6133524e`, parent `6d582a669443c8ff61aaa3f346a427aedbbda318`; only added `integration/tests/test_m04_offline_preflight.py`, Git blob `43cf4a7da044a0855177c764cfbb9ab943fcc509` matched local staged bytes. The accepted M03 controller, its tests and unchanged reference kit are preserved. This is a worker-executed offline rehearsal, not independent M04 acceptance or a live transport candidate.

## Evidence

Isolated WSL Ubuntu checkout and fresh detached verification checkout `/tmp/chat-successor-v2-m04-verify-50339ed`. PyJWT 2.10.1, cryptography 46.0.5, SQLite 3.46.1 were already available in the inspected Python environment; no package installation. Default environment did not expose MCP SDK, uvicorn, starlette, httpx or tunnel-client on PATH (not a whole-machine absence claim). Temporary loopback ephemeral bind succeeded and socket closed. No listener left running; port not reserved.

- `python3 -B integration/tests/test_m04_offline_preflight.py`: 8/8 test methods, exit 0 on fresh exact source checkout.
- `python3 -B integration/tests/test_mcp_native_poc.py`: 36/36 exit 0.
- `python3 -B astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/run_offline.py --out <fresh temp directory>`: 119/119 exit 0.
- `git diff --check HEAD^ HEAD`: exit 0; Git diff from accepted M03 across reference/adaptor and prior tests empty; clean worktree. First remote process output was no longer available after the MCP execution session expired; regression results separately rerun and read back with explicit exit codes.

## Rehearsal fixture

Two disposable offline run ledgers, A and B, a single local SQLite invocation budget, generated in-memory RSA keys and dummy issuer/audience/principal, separately supplied mock host metadata mapped to private keyed digests. Scope `succession:trial`. A valid signed test token is verified with PyJWT against pinned issuer, audience, local public key, required temporal claims, subject and exact scope. Real OAuth discovery, browser login, consent, token exchange, deployment, issuer JWKS rotation/revocation and actual ChatGPT metadata are NOT established.

| Planned slot | Executed offline outcome |
| --- | --- |
| N01 | provisional registration A; count unchanged |
| N02 | exact duplicate registration A, same receipt |
| N03 | after synthetic delivery, NEED_MORE_TIME report A received |
| N04 | duplicate report A |
| N05 | B presents A registration, rejected |
| N06 | independent B reservation registered, distinct session digest, same subject digest |
| N07 | after synthetic delivery B, ERROR carrying publication fields rejected before recording immutable report |
| N08 | reopen local quota and both proof stores (reconnect simulation only); valid TASK_COMPLETE report B received against exact independently read local bare Git fixture SHA |

The N07 incompatible status choice is deliberate: an accepted but wrong valid SHA would occupy the immutable report slot and cannot be silently replaced at N08. A valid local commit has exact run, synthetic saved-chat alias, terminal trailer, payload and base ancestry checked from the bare remote. This is local Git only, not actual GitHub publication. No evaluation, core pending successor, real worker adoption, transport invocation or Send occurs; synthetic fixture count is not a native worker count. All eight steps reserve a durable SQL row before handler validation; separate completion row, ninth blocked, unknown outcome holds after actual child process exit or injected exception. Tests include wrong-key/issuer/audience/subject/scope, missing/expired/not-yet-valid tokens, missing claims/metadata, schema/body identity injection, same-session and different-subject denial, competing budget connection and missing-store refusal. Raw mock metadata and bearer token excluded from tested journal records. The SQL budget is rehearsal-only: ordinary local transaction durability, not M03's immutable filesystem fault model, production audit or live quota qualification. Do not promote it unreviewed.

## Live blocker and next scope decision

Current official [OpenAI authentication](https://developers.openai.com/plugins/build/auth), [tool-server guidance](https://developers.openai.com/plugins/build/mcp-server), [secure MCP tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) and [metadata reference](https://developers.openai.com/plugins/reference) verified 22 November 2026. Tunnel client authentication and anonymised host session/subject correlation do not authenticate the human. OAuth requires an independently validated end-user credential; the tunnel can forward protected-resource discovery but does not automatically make the authorization server publicly reachable. No previously verified Chat Succession-specific reachable OAuth issuer/account/client or exact Platform organisation/workspace role route was established from relevant available records. This is a missing concrete prerequisite, not a denial of the owner's existing M04 resource grant. The available Platform key setup flow is not an end-user OAuth provider or evidence of resource-restricted tunnel permissions. Do not use another project's credentials, anonymous tools, or a dummy/token-bearing prompt as authentication.

Recommended next step: an established identity provider with an isolated Chat Succession-only OAuth API/client, fixed audience and scope, one authorised test user, short token lifetime, PKCE S256, compatible CIMD/pre-registered client and exact redirect URI, publicly reachable discovery/JWKS/token endpoints and resource-indicator support. Auth0 is a concrete candidate ([official MCP availability](https://auth0.com/blog/auth0-auth-for-mcp-servers-generally-available/), [client registration](https://auth0.com/blog/scaling-ai-agent-identity-cimd-application-profiles/)); no compatibility claim for this particular tunnel/account until discovery and real flow are verified. Use a separate tenant if required to avoid altering shared tenant settings; no signup/spend/tenant-wide changes or new provider provisioning under the current grant alone. Owner must nominate an authorised existing isolated provider or expressly extend scope to a new isolated provider configuration and complete required platform login/consent. Confirm target Platform organisation/ChatGPT account and least-privilege tunnel role through supported setup before creating credentials, plugin or tunnel. Once resolved, pin the actual transport candidate, freeze native test manifest, independently review security and budget boundaries, then run only N01–N08 with explicit fixture consent and teardown.

**M04 live: BLOCKED / NOT_RUN (0/8 native handler invocations).** No live service, tunnel, plugin, OAuth provider, credential or remote synthetic fixture branch created. No changes to original implementation, LTM-RAG, shared services or global settings. No M05 qualification.
