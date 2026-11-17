# Lightweight Chat Succession protocol — proposed

This is a **design contract for future implementation**, not the implementation or a claim that it has passed a 30-chat trial.

## Minimal state

One local controller maintains: nominated Project identity/control, repository URL, branch, number of unique created chat IDs, configured maximum (e.g. 30), current chat ID and last interpreted status. The repository holds work instructions, progress and the next task. No independent digest catalogue, immutable packet chain or repeated Git SHA validation is required.

## Worker-side Project instructions (draft)

```text
You are a worker in this nominated ChatGPT Project. GitHub carries the durable
instructions, progress, results and next task. On entry, read the nominated
repository and branch, especially its AGENTS.md / README / current plan and
progress file, as applicable. Continue the authorised job and do as much
substantive work as possible. Commit useful progress and clear next steps to
GitHub before handing over. Do not depend on the prior conversation's memory
or send results back to the first chat.

At the end of each response, place exactly one status on the final line:
CHAT_STATUS: NEED_MORE_TIME
CHAT_STATUS: TASK_COMPLETE
CHAT_STATUS: ERROR

Use NEED_MORE_TIME if further useful work can continue in this same chat.
Use TASK_COMPLETE when this chat's work is finished, GitHub records the result,
and the next chat can pick up the remaining job.
Use ERROR for a material blocker; explain the error and needed user decision
above the final status line. Never use TASK_COMPLETE as a substitute for a
failed or uncommitted handover. Do not request unrelated approvals.
```

The actual final line contains **one** of the three alternatives, not all three.

## Controller behaviour

```text
Project: Chat succession folder
Repo:    JayDEmily/chat_successor (example, not a universal job repo)
Branch:  <nominated-working-branch>
Max:     30 unique chat IDs (configurable)

On current assistant response:
    if explicit final-line CHAT_STATUS exists:
        classify from it
    else:
        semantically classify NEED_MORE_TIME / TASK_COMPLETE / ERROR
        if genuinely uncertain: stop and show the ambiguity to the owner

    NEED_MORE_TIME:
        send "Okay, continue working." to the same chat
        do not increment unique-chat count

    TASK_COMPLETE:
        if GitHub says the overall programme is finished: stop
        elif number of unique chats >= max: stop at cap
        else:
            activate "New chat in Chat succession folder"
            send "Continue the work in GitHub repo <repo>, branch <branch>.
                  Read the current instructions, progress and next task there."
            count the newly observed unique conversation ID once

    ERROR:
        stop automatic posting; present the error to the owner
```

## What the browser needs to do

- Use an existing authenticated Chrome session; opening a new tab is enough. No need for an additional browser profile or a new window.
- Open ChatGPT and activate **New chat in Chat succession folder**. The presence of the Project in the sidebar is not sufficient proof that the *active composer* belongs to it.
- Type the short GitHub pointer and Send once. Observe the resulting new conversation to count it. Do not type into unrelated chats.
- Do not check that the Project contains zero other chats. It may contain arbitrarily many.

A minimal record of the attempted Send/created conversation ID is useful to avoid accidental duplicate launches following a timeout. That is ordinary reliability bookkeeping, **not** a new security/approval protocol.

## Operating boundaries

- This workflow requires a controller that can act on the browser and read the relevant status. Project instructions alone cannot spawn ChatGPT conversations.
- If a worker loses access to a necessary tool or genuinely cannot proceed, it should emit `ERROR` with a reason. Absence of a response, latency or tool timeout cannot automatically be interpreted as a successful handover.
- The hard cap applies to **distinct chats**, not the number of `NEED_MORE_TIME` messages. At 30 chats, the next `TASK_COMPLETE` does not open a 31st.
- For a later project run, the controller needs the exact nominated Project and repo/branch. No automated check against other repo source, no heavy handover hashing and no strict three-chat arithmetic contract are universal prerequisites.

## Recommended implementation order

1. Keep the proven Project navigation route and simplify the existing launcher to use a **new tab** and the Project's New chat control.
2. Implement **one** terminal marker parser with semantic fallback and the three branches above.
3. Implement the configurable `max_unique_chats=30` counter and record each created chat ID once.
4. Run a bounded end-to-end test before enabling longer continuous operation, recording evidence without importing the old pilot's irrelevant per-commit gates.
