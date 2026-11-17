# Proposed executable trial — three fresh chats, worker-launch first

**Status:** prepared protocol proposal only; no run admitted, no browser Send. Owner selected the *worker-launch-first* approach for Task 1 on 17 November 2026. This does not authorise a live launch.

## Fixed experiment

- Proposed run ID: `succession-20261117-001` (reserve only when Task 3 is authorised and all prerequisites pass).
- Proposed run branch: `trial/succession-20261117-001` (not created by Task 1).
- Destination: existing Chat Succession ChatGPT Project. Resolve its actual URL, Chrome account/profile and private `local:chat-succession-project` mapping **outside Git**.
- Roles: Chat 1 `worker` → Chat 2 `reviewer` → Chat 3 `auditor`. Three distinct conversation IDs in that Project, two automatic handovers, zero required original-chat callbacks.
- Transport: remote Windows PowerShell UIA through Remote Desktop Commander, authenticated Chrome, **one** Send per reserved launch key. Worker-launch first. No watcher or extension for this run.
- Fixed work: step 1 compute `17 * 23 + 19 = 410`; step 2 independently recompute/ACCEPT or RETURN; step 3 independently audit the pinned lineage and publish terminal result. A RETURN, failure, blocked step or uncertain launch ends the run; no repairs or step 4.
- Operator: the owner inspects local/GitHub status if a launch is held; no automatic stall alert is claimed.
- GitHub is authoritative for work and pinned assignment contents. Local launch journal is authoritative for suppressing duplicate browser effects.

## Entry gates (before any ChatGPT Send)

1. Task 1 protocol committed/pushed/read back; verified private Project URL, Chrome profile, and fresh successor ChatGPT Project tool access. If the fresh tool check needs an assisted diagnostic chat, record it **outside the three-step run**; it does not count as an automatic handover.
2. Task 2 implements and tests a reusable launcher and SQLite journal. Verify explicit Windows Python executable and journal script location, initialise the private durable journal, and offline test duplicate/lost acknowledgement/unknown Send/terminal guards. PowerShell parsing and exact payload handling pass. The launcher never sends before reservation.
3. Separately authorise the bounded **live** run. Freeze source commit, run ID, branch, operator, Project mapping and maximum three steps. Create/push/fetch/read back assignment A1. Prevent competing workers on the same run branch.

## Exact child prompt shape

A launch prompt is templated only from validated local arguments, never from untrusted GitHub shell text:

```text
Chat Succession bounded run. Repository: JayDEmily/chat_successor.
Run: <EXACT_RUN_ID>. Step: <2_OR_3>. Role: <EXACT_ROLE>.
Read AGENTS.md, README.md, the linked design and plan, and
runs/<EXACT_RUN_ID>/run.json. Read your assigned JSON from
runs/<EXACT_RUN_ID>/steps/<NNN>/assignment.json
at immutable commit <FULL_40_CHARACTER_ASSIGNMENT_SHA>.
Follow only its bounded task, path restrictions, result contract and stop
conditions. Do not return to a previous chat. Do not create a fourth chat.
If tools, scope, lineage or delivery are uncertain, record BLOCKED and stop.
```

Step 1 can be started manually once after the run is admitted (record assisted entry), or launched under an explicitly revised admission instruction. It is not a successor launch. Step 2 and step 3 must be sent without the owner carrying prompts between chats to count as automatic handovers.

## Acceptance evidence

- Source-backed proof that Chat 1, 2 and 3 are distinct, saved conversations in the **correct Project**, with exact posted prompts and pinned A1/A2/A3 respectively.
- Verifiable Git result and handover commits R1/A2/R2/A3/R3/T3, actual changed paths inside assigned scope, and independent reviewer ACCEPT before step 3.
- Two journal launch keys reserved exactly once; no repeated ambiguous Send; no key, assignment or conversation for step 4.
- Independent review distinguishes task correctness, protocol/Git lineage, and observed UI transport. User intervention, unclear identity, timeout, blocked state or failed check is reported as such, not counted as unassisted success.

**Explicit stop:** do not execute Task 2 or Task 3 from this proposal alone. The current user authorisation covers only Task 1.
