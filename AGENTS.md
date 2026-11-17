# AGENTS.md — Chat Succession

**Scope:** `JayDEmily/chat_successor` only. **Reviewed:** 18 November 2026 (AEDT).
This file is a short operating map for repository-aware workers, not an executable launcher, an owner approval, or a replacement for an active task plan.

## Mission and source of truth

- Build and test succession of fresh ChatGPT conversations: Chat 1 → GitHub → Chat 2 → GitHub → Chat 3 → … . Each worker makes useful progress using the **same nominated GitHub repository and working branch**. No return to a predecessor or copying its transcript is needed.
- GitHub holds durable instructions, evidence, completed work and the next task. Chat history and Project memory are useful context, **not authoritative proof** of the current task or publication.
- Separate **historical evidence**, **new reference-model results**, **implemented integration** and **observed live behaviour**. Never claim a simulated browser, local Git transport or offline test proves a live ChatGPT handover.
- The earlier fixed three-chat experiment is a **held historical trial**, not the product's permanent limit. Do not restart its held Send or reinterpret its constraints as general programme rules. A new run needs its own bounded assignment and observed state.

## On entry: read, identify, then act

1. Read the current owner's request and the actual nominated repository, branch, run and stopping condition. Do not infer authority from merely being in a ChatGPT Project.
2. Read this file, `README.md`, `PROGRESS.md`, the applicable design/plan, and any instructions in the active run or assigned subtree. Check the real remote branch head and working-tree status before edits.
3. For the original three-chat exploration, consult `docs/superpowers/specs/2026-11-17-chat-succession-design.md`, `docs/superpowers/plans/2026-11-17-chat-succession.md` and the trial evidence on its own branch. Respect its existing held state.
4. For the **proposed continuing-loop design**, consult Astra's separately imported package at `JayDEmily/sequential-chat-nov2026`, commit `aec894b0376190c4fa1f32c2e5154fb0a10b3955`, especially `astra/2026-11-17/artifacts/*chat_succession_test_plan_20261117.md` and the TAR's `docs/PROTOCOL_AND_ADAPTER.md` and `docs/OWNER_RUNBOOK.md`. These are test specifications, not a live-installed adapter.
5. Choose the **current assigned plan** rather than stitching incompatible legacy instructions together. If a requirement conflicts, state the exact conflicting sources and follow the owner's latest in-scope direction. A review/plan assignment does not authorise implementation or a live Send.

## Established environment and tool boundaries

- Intended destination is the owner's existing ChatGPT Project **Chat succession folder**. Verify the actual active Project and saved conversation identity at each live launch; sidebar visibility or an open blank tab alone is insufficient.
- Normal engineering path: **Remote Desktop Commander → Windows 11/Chrome** for authorised browser interaction; **WSL2 Ubuntu → Git/GitHub** for local engineering, testing and publication. Use the authenticated capabilities that are actually available; a connected app or account does not guarantee that a future worker has those tools.
- The standard ChatGPT GitHub integration is documented as read-only; other authorised Git/Codex/connector actions can differ. Check the actual write route and **verify a remote push** before calling a handover published.
- ChatGPT Projects support project instructions, files and contextual memory; they do **not** by themselves start a successor or guarantee independent repo-only context. A normal ChatGPT worker must be explicitly told to read this `AGENTS.md` and the current repo plan. Codex can discover `AGENTS.md` as repo guidance.
- Never move, edit or inspect unrelated NVIDIA, `second-chat-thread` or `second_chat_ocr` work as part of this repository's tasks. Preserve existing browser drafts, authentication and unrelated sessions.

## Proposed continuing-loop protocol (requires live integration)

A completed worker turn emits **one** clear final status line:

- `CHAT_STATUS: NEED_MORE_TIME` — useful assigned work continues in the **same conversation**; controller sends “Okay, continue working.”
- `CHAT_STATUS: TASK_COMPLETE` — the assigned slice is complete. Confirm current **published** repository state: if the **whole programme** is finished, stop; if work remains and the configured unique-chat limit permits, create **one** successor in the nominated Project with a short repo/branch pointer.
- `CHAT_STATUS: ERROR` — an unresolved material blocker; stop automatic posting and record the actual cause and recovery boundary.

A missing, streaming or conflicting status is **unresolved**, not implicit completion. The run-specific maximum counts the initial worker and only *observed distinct saved conversation IDs*. Repeated same-chat continuations do not consume a new chat. The optional 30-chat Astra exercise is a test ceiling, **not** an unchangeable production maximum.

Only **one controller/launcher** is responsible for browser Sends in a given run. Workers publish work and report status; do not have the worker and controller independently create successors. Astra's synchronous reference controller, mock UI and offline fixtures are **not** a live Chrome adapter.

## Work, handover and failure handling

- Follow the actual assignment and permitted paths. Do as much useful authorised work as possible; validate changes, commit, push, read back the remote result and update `PROGRESS.md` (or the run's nominated ledger) with evidence and the next action. Do not write only a success marker.
- Keep normal evidence: branch, commit SHA, test command/result, actual observed destination/IDs, published versus local-only state, outstanding work and first blocker. Report tests and claims at their actual evidence level. Do not invent IDs, successful Sends, remote commits or tool access.
- Before a browser Send, persist its pending state; target the *active* correct Project composer, inspect actual editable draft/attachments, preserve occupied content, and verify typed text where possible. A placeholder-like UIA Value alone cannot prove a draft exists.
- After a Send with ambiguous delivery, **reconcile read-only**; do not blindly repost, clear a draft, reset the run counter or discard pending state. A positive observed submission counts once. An unresolved outcome stays held.
- No automatic merge, force-push, branch deletion, third-party account changes or materially wider work unless included in the current authorised assignment. Routine in-scope commits/tests and ordinary serial handovers do not need fresh per-step owner approval.
- For a complex implementation, maintain a bounded written execution plan and its checkpoints. For a review, inspect and report without editing implementation. Stop when the authorised programme finishes, its configured cap is reached, or a genuine unresolved blocker remains.

## Local checks

- On the legacy implementation branch (where `tests/` exists): `python3 -m unittest discover -s tests -q`.
- In an extracted Astra test kit: `python3 run_offline.py`. Its reported **119/119 offline passes** were independently reproduced on Ubuntu on 18 November 2026; all Astra live cases L01–L15 remained **NOT RUN** at that check.
- An offline pass is not a successful live launch. Begin live validation at Astra **L01** only in a separately authorised execution run, then test same-chat continuation/error and repeatability.

## Official OpenAI references (verify again when behaviour matters)

- [Codex and short AGENTS.md repository maps](https://openai.com/index/harness-engineering/) — keep instructions brief; link to living plans and evidence.
- [Codex prompting and AGENTS.md discovery](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide) — Codex behaviour; does not imply ChatGPT Project chats auto-load repository files.
- [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt) — project instructions, connected apps and project memory/context.
- [Connecting GitHub to ChatGPT](https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt) — standard integration's read-only scope and availability boundaries.
- [Managing app permissions](https://help.openai.com/en/articles/20001495-managing-app-permissions-in-chatgpt) — action rights depend on the actual connected account and settings.
- [OpenAI developer documentation MCP](https://developers.openai.com/learn/docs-mcp) — use it when installed/available for current OpenAI API, Codex or ChatGPT technical claims; otherwise consult official OpenAI documentation directly.

**These OpenAI references explain platform behaviour, not proof of the user's live account, browser adapter or a successfully executed chat chain.**
