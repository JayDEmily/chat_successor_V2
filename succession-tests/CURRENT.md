# Active Astra L01 live fixture

This is the disposable **L01 two-slice owner-environment test** in
JayDEmily/chat_successor on branch trial/astra-l01-20261118.
It is separate from the implementation programme and the older three-chat trial.

Fixture path: succession-tests/astra-l01-20261118

**Worker assignment:** On entry, read AGENTS.md and the fixture's
INSTRUCTIONS.md, RUN.json, STATE.json and RESULTS.json from this branch.
Work only the next uncompleted fixture slice. Use the available approved
Windows/Ubuntu Git route to commit, push and verify the new published branch
HEAD. Validate using fixture_tools.py verify --root . inside the fixture.
Do not use simulate-slice as evidence of model-authored work.

Record **your observed saved ChatGPT conversation ID** in the appended
RESULTS.json row and STATE.json last_chat_id. Obtain it from the active
nominated Project conversation URL, not from guesswork or earlier chats.
If you cannot observe your own identity or publish, explain the precise
blocker and end CHAT_STATUS: ERROR. Do not fabricate a result or completion.

After one useful published fixture slice, end exactly
CHAT_STATUS: TASK_COMPLETE. The controller alone launches a successor.
The second worker independently reads this same branch and performs slice 2.
Do not paste the predecessor conversation to the successor.

Case expectation: cap 3, two valid published results, two distinct saved
chat IDs, exactly one controller-launched successor, final
programme_complete=true and next_task=null; controller stops.
L01 remains NOT_RUN until independently observed. Other cases remain
unaffected.
