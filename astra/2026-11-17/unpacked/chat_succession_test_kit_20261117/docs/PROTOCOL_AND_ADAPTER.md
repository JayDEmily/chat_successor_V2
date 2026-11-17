# Minimal protocol and the live adapter seam

## Keep the front end small

The owner selects **Project, repository, working branch, maximum unique chats**
and starts a single run in an already authenticated environment. Thereafter
the front end needs only progress and pause/resume/error display. Normal
continuations and handovers require no new owner approvals. The existing
proven Project navigation/Send method remains the browser mechanism. [O; A2]

`config.example.json` contains four fields used by `succession.core.Config`.
The historical Project ID corresponds to “Chat succession folder” in [A4:9–11];
the branch placeholder must be replaced by the owner's chosen working branch.
No archived trial branch or source SHA is automatically selected.

The model's initial conversation ID is the **observed current worker**, not
a generic “New chat” URL. Existing Project chats outside this run are ignored.

## Worker and repository contract

Use `prompts/project_instructions.txt`. The launch message is
`prompts/successor_message.txt`, with only repo and branch filled in. Put any
fixture path or real job plan in the repo's standing instructions, not in a
large per-chat packet.

Repository state needs to convey: current progress, next task, and whether
the overall programme is complete. In this test workload, `STATE.json` also
has `last_chat_id` for attribution, plus result/probe files. A real existing
`PROGRESS.md`/plan is fine: the adapter maps its ordinary observations to:

```python
RepoView(
    repo="JayDEmily/chat_successor",
    branch="the-owner-selected-branch",
    last_chat_id=current_observed_chat_id,
    programme_complete=False,
    next_task="Current remaining work",
    published=True,
    readable=True,
)
```

`published=True` means the adapter observed successful publication/current
remote-branch state, not merely the assistant saying “committed.” Attribution
can come from the worker's progress record or the observed publish event.
Do not assign today's chat ID to an old repo record merely to satisfy the
model. Read the current state once for ordinary handover/completion logic;
there is no independent hash or repeated immutable-SHA ceremony.
The reference controller cannot verify a fabricated `RepoView`.

The test workload validator checks the result contents. Arbitrary production
job correctness remains the job's normal tests/review responsibility, not a
new succession security gate.

## Browser/desktop adapter: deliberately NOT supplied as working code

The archive does not contain the historical launcher source. The browser
adapter must be connected in the owner's environment; this kit neither
guesses today's selectors nor claims browser execution. Its required seam is:

| Adapter operation | Contract / observable evidence |
|---|---|
| Observe current assistant turn | Entire assistant message, stable turn/event identity, current saved chat ID, active Project, completed versus still streaming |
| Read programme/handover state | Current nominated repo/branch state and ordinary publish outcome, not prior-chat memory |
| Prepare continuation | Same saved conversation ID, nominated Project; preserve real unsent owner text |
| Prepare successor | Existing authenticated Chrome; optionally new tab; invoke nominated Project's new-chat control; confirm active composer destination, not just sidebar visibility |
| Send once | One serialized click/action after the model records `sending`; no hidden launcher retry |
| Observe submitted message | Read-back source/destination chat ID and Project, with the actual submitted message visible |
| Reconcile | Read-only inspection after timeout/restart; report observed delivery, positive not-sent evidence, or unresolved uncertainty |

An available browser response ID can be used as the event identity; otherwise
the adapter needs a persisted monotonically assigned turn identity tied to its
observation of that completed assistant turn. It must not generate a new ID
for every poll, mistake a tool output for an assistant turn, or infer completion
just because marker text has appeared while streaming. Regeneration/editing
of an already-consumed answer requires explicit reconciliation rather than
blindly treating it as another completion.

Keep **one actor** responsible for launching: either the owner-connected
controller uses the proven desktop method, or an existing driver performs it
on the controller's instruction. The worker must not also launch independently.

## Dispatch ordering (pseudocode; not executable browser integration)

```text
response = adapter.observe_current_assistant()
decision = controller.consume(response, adapter.current_repo_view_if_needed())
controller.save(state_path)

if decision is CONTINUE_CURRENT or LAUNCH_SUCCESSOR:
    adapter.prepare_correct_destination_without_sending()
    # If destination/draft is unresolved, pause and save; do not Send.
    controller.begin_send(decision.action_id)
    controller.save(state_path)             # BEFORE UI side effect
    observation = adapter.send_once_and_observe(decision.message)
    # No automatic retry inside this operation.
    if observation positively establishes delivery:
        controller.confirm(action_id, observation.chat_id, observation.project)
    else:
        controller.uncertain(action_id, observation.reason)
    controller.save(state_path)
```

Do not invoke `adapter.current_repo_view_if_needed()` on a streaming turn or
for every token; it is needed for a completed `TASK_COMPLETE` handover.
The reference code is synchronous. A real adapter must serialize callbacks
and owner stop requests around the pre-Send check.

`FakeBrowser.perform` implements this order only with synthetic side effects.
It has injected before-click, after-click and after-observation failures.
`Controller.load` preserves IDs, consumed responses and in-flight action.
A persisted `sending`/`uncertain` action restarts on hold, not by replaying Send.

The state file is small ordinary reliability bookkeeping, not the old SQLite
approval/one-shot protocol. It uses atomic replacement and a single writer;
simultaneous independent controllers are not supported. It is not a
distributed exactly-once-delivery mechanism.

## Status interpretation policy

- Canonical `CHAT_STATUS: ...`, or exact bare final keyword, wins when it is
  the single valid final marker outside quoted/fenced/indented code.
- Ignore tool/user messages; a marker example inside a repository file must
  never control the loop.
- Reject conflicting/repeated/malformed/nonfinal explicit markers.
- Without an explicit marker, `SemanticVerdict` can be provided with one of
  the same three statuses, `unambiguous=True`, and a reason. The kit does **not**
  implement a model classifier; its JSON verdicts are labelled test doubles.
- Absent reliable adjudication, hold. Before enabling automatic live semantic
  fallback, run L10 shadow assessment. A manual unambiguous adjudication is
  compatible with the seam but is not evidence of autonomous interpretation.
- Silence, truncation or a dropped connection never implies success. Adapter
  timeouts call `pause`/`uncertain`; there is no autonomous timer service here.

## The placeholder regression, without repeating the old mistake

`classify_composer` is intentionally small. An independently observed empty
editable buffer can be EMPTY even when UIA Value contains a placeholder.
Actual text or attachments are DRAFT, including text literally identical to
the placeholder. Value equality alone is UNKNOWN.

A live adapter must show how it gets **actual editable content**. Merely
renaming UIA `Value` to `editable_text` would reproduce the unresolved bug.
If the owner's tools cannot distinguish these cases reliably, preserve the
composer and hold; do not silently clear a real draft. [A4:16; A5:11,22–24]

## Recovery API

- `confirm(...)`: read-only adoption of positively observed submitted message;
  a duplicate ack does not create another ID.
- `confirm_not_sent(...)`: explicit reasoned reconciliation; allows another
  attempt only when there is positive evidence no submission occurred.
- `resume_after_owner()`: clears a nonterminal hold, preserving count/history;
  cannot bypass a possibly submitted action or a finished/capped run. A
  prepared-but-never-attempted action may resume after destination repair.
- No “resume” method sends a message itself. After a worker `ERROR`, owner
  repair followed by a new response event is used; old consumed events remain
  deduplicated.
