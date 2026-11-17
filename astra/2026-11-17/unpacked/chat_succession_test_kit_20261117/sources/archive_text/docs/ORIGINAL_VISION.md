# Original user vision — authoritative design intent

**Recorded:** 17 November 2026, based on the owner's explicit instructions in this conversation. The user's concept below supersedes incidental complexity introduced by exploratory implementations. It is a **design objective**, not a claim of working automation.

## One-sentence objective

Enable an arbitrary long-running engineering job to **continue automatically from one fresh ChatGPT conversation to the next**, all inside one nominated ChatGPT Project, with **GitHub as the sole durable handover record**, until the task ends, needs intervention or reaches a configurable maximum number of unique conversations (for example, 30).

## Intended operating sequence

1. **Project prerequisite.** A nominated ChatGPT Project exists. Every worker conversation is started *inside that Project*, using its **New chat in [Project name]** control. The Project may contain existing conversations; it need not be empty. Merely seeing its sidebar link while another chat is active does not establish the destination. No requirement exists to return to the originating conversation.
2. **Worker begins.** The first chat receives the overall task and a GitHub repository/branch pointer. Each subsequent chat receives a *short* message of the form: **“Continue the work in GitHub repository `owner/repo`, branch `branch`; read the current instructions and state there.”** It should not need a long copied handover in the ChatGPT message.
3. **Worker does substantive work.** The chat reads the repository's standing instructions, current plan and progress, uses available tools, does as much useful work as it can, and records durable outcomes, unresolved issues and the next task in GitHub.
4. **Controller recognises the terminal state.** At the end of each assistant response, Project instructions require an unambiguous status marker (`NEED_MORE_TIME`, `TASK_COMPLETE` or `ERROR`). The controlling agent may semantically interpret responses when the marker is missing, but uncertain classification is not equivalent to confirmed success.
5. **`NEED_MORE_TIME` → same chat.** Tell the current conversation **“Okay, continue working.”** Do not create a new conversation or reset its active context.
6. **`TASK_COMPLETE` → next fresh chat.** The current conversation has finished the work it can perform, its GitHub state is recorded, and further work remains. The controller uses **New chat in the same nominated Project** and posts a short GitHub pointer. The new conversation independently reads GitHub to understand what to do next.
7. **`ERROR` → user intervention.** Stop automatic progression. Surface the error and relevant GitHub/current-chat context to the user so they can decide how to resolve it.
8. **Bounded number of unique chats.** The controller counts actual newly created conversation identities and prevents a new Chat 31 when the configured cap is 30. Same-chat continuation does not increase this count. The three-chat pilot was a *test boundary*, not the intended production limit.

The cycle continues as long as there is useful work and an allowed next chat. The controller, rather than a textual instruction alone, must perform the browser/new-chat/Send actions; a ChatGPT Project instruction by itself does not create new browser conversations.

## Deliberate simplicity

- **Only material routing/security condition:** the message must be sent to a new conversation *within the nominated Project*. This is the owner's requested security boundary; do not add unrelated account, other-project, empty-Project or source-check constraints.
- **GitHub is a working ledger, not a cryptographic challenge.** Do not demand a separate pre-launch hash/readback ceremony, a new signed packet for every turn or pinned immutable handover for each successor. The worker simply finds and follows the existing repo/branch instructions and current durable state.
- **Do not manufacture artificial gate approvals.** A finite max-chat counter, state marker handling and avoiding an accidental double Send are practical control flow, not a separate security regime.
- **Simple human experience.** The owner should not have to copy results, paste prompts, return to the initial chat, reconfigure Chrome for every step or supervise normal continuation.
- **Scope isolation.** The nominated repository and work assignment define the job; no inferred permission to edit unrelated projects. This is ordinary task scoping, not an extra succession security checkpoint.
- **One path.** Default to worker-completes → GitHub update → status → controller action; avoid building an unused parallel watcher/daemon in advance.

## Status marker semantics

`NEED_MORE_TIME`: the **current conversation** can still make useful progress; controller replies *in the same thread* with a short continuation prompt.

`TASK_COMPLETE`: the **current conversation's work slice** is complete and its progress/next-step is in GitHub; controller starts the next conversation if work remains and the cap permits. This does **not** automatically imply the entire engineering programme is finished.

`ERROR`: an actual blocker requiring the owner; controller stops and exposes the cause. No automatic next-chat creation.

The three states are the user's proposed core protocol. If the underlying programme itself finishes, its completion must be recorded in GitHub and the controller should stop rather than waste the remaining chat budget. That terminal-programme condition should be represented in the GitHub state; it is not an additional browser security check.

## What not to import from the earlier proof of concept

The previously built validator's fixed arithmetic task, three-step maximum, exact assignment SHA, detailed permitted-path lists, strict launch journal and pre-flight source-hash comparisons are **historical test mechanisms**. They may be retained as evidence but must not silently constrain the 30-chat design. The owner explicitly rejected unnecessary baby steps and over-verification.
