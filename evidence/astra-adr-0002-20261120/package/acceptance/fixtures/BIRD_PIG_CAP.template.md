# Bird and Pig — eligible work at the worker cap

TEMPLATE ONLY. The owner must approve this bounded trial, allocate an existing
Project/repository and fresh `<AUTHORIZED_BRANCH>`, replace the placeholder,
and publish these instructions first. Controller cap: **2**, unchanged on resume.

Use the controller's run ID and your registered saved desktop chat ID. The phone
or request chat and any recovery views do not count as workers.

## Worker one

If `STORY.md` is absent, state the intended opening without editing and end with
the plain final line `CHAT_STATUS: NEED_MORE_TIME`.

After the first controller “Okay, continue working.”, verify the published
branch/instructions, still without editing, then end
`CHAT_STATUS: NEED_MORE_TIME` again.

After the second such controller message, create only `STORY.md` with:

`Bird: Pig, what should we take on our picnic?`

Make one commit on `<AUTHORIZED_BRANCH>` and verify its remote publication.
Use your actual run/Chat-ID trailers and
`Chat-Succession-Next: Reply as Pig and complete the two-line story`.
End with `CHAT_STATUS: TASK_COMPLETE` as the final plain line.

## Worker two

Only when the published file contains exactly that opening, append:

`Pig: Apples, and a spare one for the ducks.`

Change only `STORY.md`, directly on worker one's published commit, publish and
verify. Use your own saved Chat-ID and the same run ID. Set
`Chat-Succession-Next: Review the two published lines`.
End with `CHAT_STATUS: TASK_COMPLETE`.

## Eligible review beyond this run

A third worker could review the two lines and write `REVIEW.md` if a separately
authorized run were later started. Neither worker in this cap-two run performs
that task. Keep it eligible in the work record; do not claim `FINISHED`.

Unexpected file content, identity, authority or publication failure means
`CHAT_STATUS: ERROR`. Only the controller sends continuations and successors.
Do not add corrective prompts or extra edits to conceal a test failure.

Expected result: two workers, two same-chat continuations in worker one, one
successor, `STOP_CAP` at 2/2, no pending action; `REVIEW.md` absent and the review
still eligible.
