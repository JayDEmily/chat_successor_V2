# Verified findings and provenance — 17 November 2026

These are historical observations, **not** evidence that the lightweight 30-chat controller is implemented.

| ID | Evidence | Finding |
| --- | --- | --- |
| V01 | Remote Desktop Commander on Windows `DESKTOP-I188O30` with Ubuntu WSL | Desktop interaction and Ubuntu Git access were available to the experiment. |
| V02 | Ubuntu `git ls-remote --heads origin` for `JayDEmily/chat_successor` | The source repository had three remote heads: `main` at `26b33e8991119f9886b23f0c01651c3f49435706`; offline work at `f8c002690c0a1a9ff4f298bd9a8d68b21f5ba1f8`; stopped trial at `3b2c95b954eb90b1e6c9b82403dd1956c6f34b39`. |
| V03 | Windows UI Automation, Chrome, 17 November | The button named `New chat in Chat succession folder` was found and invoked, opening the right Project. This was tested without sending a message. |
| V04 | UIA browser navigation result | Project page: `https://chatgpt.com/g/g-p-6afbfc5e59248191a8c690296b24c8ef/project`. It **does not need to be empty**. |
| V05 | One-send UIA test and saved-chat readback | Chat 1 was sent in the correct Project. Saved chat: `https://chatgpt.com/g/g-p-6afbfc5e59248191a8c690296b24c8ef-chat-succession-folder/c/6afc0c31-e420-83ec-b8f0-457149e3c4d0`. The assistant began work. |
| V06 | Trial branch commit `846bd4ff12a558eefe5dbb6df65535d521d08ff9` | Chat 1 created a three-step trial run and first assignment (A1). |
| V07 | Trial branch commit `73eec3791fd5ae984db95bf7aeb9f8077ed6e18c` | Chat 1 committed its calculation: `17 * 23 + 19 = 410` (R1). |
| V08 | Trial branch commit `898cd68740b2b46d75da1b9e195fe9e01bb9a685` | Chat 1 committed a pinned reviewer assignment/handover for Chat 2 (A2). |
| V09 | Trial branch commit `3b2c95b954eb90b1e6c9b82403dd1956c6f34b39` and `evidence/succession-20261117-001/CHAT2_LAUNCH_BLOCKED.md` | Chat 2 launcher reserved step 2 but stopped before typing/Send with `Existing draft detected; preserve it`; local journal state `blocked`, run state `held`. No reviewer result or Chat 3 audit exists on that branch. |
| V10 | Windows read-only composer inspection after the stop | Composer UIA Value was `New chat in Chat succession folder` with trailing newline; original launcher compared `Value != ''`. This is evidence for a **probable false-positive placeholder check**, not a direct recording of the value during the failed attempt. |
| V11 | Ubuntu tests and Windows offline probes recorded in repository | Protocol and SQLite tests reached 37/37 passing; Windows PowerShell parse and offline SQLite smoke checks passed. These do not establish a working repeated live succession chain. |

## What the pilot actually proved

It proved the browser can navigate to the Project and post an instruction, and that one chat can do substantive work and commit a GitHub handover. It **did not** prove unattended Chat 1 → Chat 2 → Chat 3 delivery, nor semantic status routing, a 30-chat cap or ongoing self-succession.

## Source links

- [Committed trial stop record](https://github.com/JayDEmily/chat_successor/blob/3b2c95b954eb90b1e6c9b82403dd1956c6f34b39/evidence/succession-20261117-001/CHAT2_LAUNCH_BLOCKED.md)
- [Trial progress record](https://github.com/JayDEmily/chat_successor/blob/3b2c95b954eb90b1e6c9b82403dd1956c6f34b39/PROGRESS.md)
- [Original offline launcher checkpoint](https://github.com/JayDEmily/chat_successor/tree/f8c002690c0a1a9ff4f298bd9a8d68b21f5ba1f8)
