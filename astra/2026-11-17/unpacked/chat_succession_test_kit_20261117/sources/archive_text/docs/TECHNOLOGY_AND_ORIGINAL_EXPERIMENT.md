# Chat Succession — Original Vision, Technology and Operating Concept

## 1. Objective

Create a system that allows ChatGPT to perform continuous, autonomous work across successive, independent chat conversations.

Each conversation performs as much useful work as possible, saves its progress to GitHub and hands responsibility to a new conversation within the same nominated ChatGPT Project.

**GitHub provides persistent memory. ChatGPT conversations perform the work. Remote Desktop Commander provides computer access. Ubuntu provides the execution environment.**

The system should require minimal user intervention and minimal orchestration complexity.

## 2. Technology and user prerequisites

The user establishes the environment before the first conversation begins.

| Technology | Purpose |
|---|---|
| **ChatGPT account** | Provides authenticated access to ChatGPT and the user's Projects |
| **ChatGPT Project** | The nominated location for all conversations, such as *Chat succession folder* |
| **Remote Desktop Commander (RDC)** | Provides remote control of the user's Windows PC, including Chrome and desktop applications |
| **Google Chrome** | Hosts the authenticated ChatGPT interface and allows the creation of new Project conversations |
| **Windows 11** | Hosts Chrome, Remote Desktop Commander and WSL |
| **Ubuntu on WSL** | Provides the terminal, Git, Python and other development tools |
| **GitHub** | Stores project instructions, code, committed progress, decisions and the next work to perform |

The user signs into the required accounts, establishes the connections and nominates an existing GitHub repository and working branch.

GitHub already contains the instructions and project material. The individual chat conversations do not need to reconstruct the project from earlier conversation histories.

## 3. How the original three-chat experiment worked

The original experiment used the repository **JayDEmily/chat_successor** and the ChatGPT Project **Chat succession folder**.

It was designed to prove that one conversation could complete work, publish a GitHub handover and automatically launch another conversation in the same Project.

### Chat 1 — Initiation

The first conversation was created inside Chat succession folder using Chrome and Remote Desktop Commander.

It received instructions to access the GitHub repository, use Ubuntu WSL and Git, and perform a simple arithmetic task:

`17 × 23 + 19 = 410`

Chat 1 successfully completed the calculation and committed the result to GitHub.

It then created a GitHub assignment for Chat 2, identifying the work that the new conversation should perform.

### Chat 2 — Attempted succession

Chat 1 attempted to create Chat 2 through Windows PowerShell and Chrome UI Automation.

The launcher used Remote Desktop Commander and Windows to operate Chrome, locate the ChatGPT Project and prepare a new conversation.

However, its draft-detection check reported that the new composer already contained text.

The launcher stopped before sending the Chat 2 assignment.

Subsequent inspection found that the ChatGPT editor could expose its placeholder text through Windows UI Automation, even when no user-written draft was present.

This is a plausible explanation for the failure, although the exact editor value during the failed attempt was not recorded.

### Result

The experiment established that:

- A conversation could read its GitHub instructions, perform work and commit results using Ubuntu.
- Remote Desktop Commander could operate Chrome and navigate to the nominated ChatGPT Project.
- A new conversation could be created within that Project and receive an automated message.
- Chat 1 could prepare and publish a GitHub handover for a successor.

**It did not establish a successful automatic Chat 1 → Chat 2 → Chat 3 chain.** Chat 2 was blocked before receiving its assignment, and Chat 3 never ran.

The original implementation also introduced significant complexity: pinned assignment commits, validation routines, SQLite launch journals, draft checks and extensive verification.

The revised vision deliberately avoids making those mechanisms requirements for the continuing system.

## 4. Intended autonomous workflow

Once the prerequisites are established:

1. **Chat 1 starts** in the nominated ChatGPT Project and reads the GitHub repository and branch.
2. It uses Remote Desktop Commander, Ubuntu and GitHub to complete as much authorised work as possible.
3. It commits useful progress, outcomes and continuation instructions to GitHub.
4. It emits one of three execution signals.
5. The controller acts on that signal, either continuing the current chat, creating a successor or stopping for intervention.
6. A successor receives a short GitHub pointer and repeats the process.

The successor message needs only to identify where the work is:

> Continue working. Read GitHub repository JayDEmily/example, branch main, including its current instructions and progress.

The successor reads GitHub and takes responsibility for continuing the task.

## 5. The three execution signals

**NEED_MORE_TIME**

The current conversation can continue productive work.

The controller sends **"Continue working"** into that same conversation.

No new chat is created.

**TASK_COMPLETE**

The current conversation has finished its work interval and committed its progress to GitHub.

If the overall objective remains unfinished, the controller creates a new conversation inside the nominated ChatGPT Project and supplies the GitHub pointer.

**ERROR**

The conversation has encountered a problem it cannot resolve autonomously.

It records the error where possible, describes the blocker and stops for the user to intervene.

The controller may recognise these states through explicit keywords defined in the ChatGPT Project instructions, with semantic interpretation as a fallback.

## 6. Session limit and completion

The succession can continue for a configurable maximum, initially proposed as **30 unique chat conversations**.

A `NEED_MORE_TIME` response continues the existing conversation and does not count as a new session.

A `TASK_COMPLETE` handover creates one new conversation and increments the count.

The system stops when the overall objective is achieved, the session limit is reached, or an unresolved error requires user intervention.

## 7. Minimal orchestration requirements

The controller needs to know only:

- Which ChatGPT Project must contain the conversations.
- Which GitHub repository and branch contain the work.
- Which of the three execution signals was produced.
- Whether to continue, create a successor or stop.
- How many distinct conversations have been created.

**The nominated ChatGPT Project is the required routing boundary.**

There is no requirement for the Project to be empty, for handover messages to be hashed or repeatedly verified, or for each conversation to perform only a narrowly defined task.

Normal account permissions, GitHub access controls and platform controls remain applicable. Additional orchestration-level security machinery is not part of the requested design.

## 8. Intended end state

The user establishes the environment once and initiates the first conversation.

Thereafter, the system should work autonomously:

**ChatGPT Project → Worker Chat → Remote Desktop Commander / Ubuntu → GitHub commit → Execution signal → Continue or New Project Chat**

This continues until the overall task is finished, an error requires user intervention or the configured conversation limit is reached.

The fundamental design principle is:

**Each chat works for as long as it can, GitHub preserves the work, and the next chat picks up where the previous one stopped.**
