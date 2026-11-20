# Cat and Dog — ordinary finish acceptance fixture

TEMPLATE ONLY. The owner must approve the bounded work, allocate an existing
Project/repository and fresh `<AUTHORIZED_BRANCH>`, replace this placeholder,
and publish these instructions before a run starts. Controller cap: **3**.
There are only two authorized slices; no work exists beyond them.

Read the run ID and your saved desktop chat ID through the controller's
private identity instructions. Wait for registration/count for your worker
number; never use the request-chat ID. Respect the project's publication rules.

1. Worker one: if `STORY.md` is absent, create it with exactly this one line:

   `Scruffy: Bluey, shall we take a walk after the rain?`

   Change only `STORY.md`. Publish one commit on `<AUTHORIZED_BRANCH>` and
   independently read the published result. Include exactly one of each trailer:
   `Chat-Succession-Run: <actual run ID>`, `Chat-ID: <your actual saved chat ID>`,
   `Chat-Succession-Next: Reply as Bluey and finish the story`.

2. Worker two: only if the published file is exactly that first line, append:

   `Bluey: Yes, Scruffy. I'll meet you by the porch.`

   Change only `STORY.md`; make one commit directly on worker one's published
   commit, publish and verify. Use your own current saved chat ID and the same
   run trailer; set `Chat-Succession-Next: FINISHED`.

Each worker performs only its own slice. If both lines already exist, reconcile
rather than duplicate them. Any unexpected contents, identity, authority or
publication failure is a blocker, not permission to improvise. Put commentary
and timestamps before the final plain line `CHAT_STATUS: TASK_COMPLETE` only
after verified publication; otherwise explain the blocker and end
`CHAT_STATUS: ERROR`. Only the controller launches successors.

Expected controller outcome: two saved workers, one successor, `STOP_FINISHED`
at count 2 / cap 3, no pending action.
