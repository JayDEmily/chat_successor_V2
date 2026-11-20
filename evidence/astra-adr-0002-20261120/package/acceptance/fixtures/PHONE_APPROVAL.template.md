# Scoped iPhone approval — same saved worker

TEMPLATE ONLY. The owner must approve staging this fixture, select an existing
Project/repository and fresh `<AUTHORIZED_BRANCH>`, replace the placeholder and
publish these rules first. Controller cap: **2**. Staging is not the approval
of the held edit below.

The only proposed first edit is one line, `Pebble approved`, in `NOTES.md`.
It is deliberately on owner hold.

If `NOTES.md` is absent and no scoped owner approval for this proposal/run has
been received, make no edit, state the one proposal clearly and end with the
plain final line `CHAT_STATUS: ERROR`.

The owner can say “I approve” in the Project request chat. The controller routes
the scoped private-input pointer to the already saved first worker. Read that
input and the project's authority; do not infer approval merely from being in
the same Project.

After that verified scope is received, worker one creates `NOTES.md` containing
exactly `Pebble approved`. Change only that file; publish one commit to
`<AUTHORIZED_BRANCH>` and independently verify the remote. Use the actual run
and current registered saved Chat-ID trailers; set
`Chat-Succession-Next: Append verification line to NOTES.md`.

Worker two, finding exactly the single published first line, appends exactly
`Verified by the successor`. Change only `NOTES.md`, directly on the first
published edit; publish and verify. Use the same run ID and its own saved
Chat-ID, and set `Chat-Succession-Next: FINISHED`.

Each worker publishes only its slice. If both lines exist, reconcile; do not
repeat the edit. Put commentary and timestamps before the final plain
`CHAT_STATUS: TASK_COMPLETE` only after publication is verified. Unknown scope,
identity or publication is `CHAT_STATUS: ERROR`.

Only the controller sends. Expected outcome: the iPhone request chat is not a
worker; one scoped input to worker one; one successor; exactly two saved
workers; `STOP_FINISHED`; duplicate request replay produces no duplicate input,
edit or worker.
