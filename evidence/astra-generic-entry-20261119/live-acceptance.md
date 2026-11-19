# Astra generic entry live acceptance

19 November 2026. Disposable repositories and Projects were selected by the owner for L5. The installed private plugin was verified at 0.4.1. The Windows wrapper points to the tested working checkout. The offline suites passed 45 integration tests and 119 reference tests. Both releases received independent OpenAI Exec Plans review before publication.

## Trial A — Natural owner approval

- Repository `JayDEmily/chat-succession-trial-approval`, seed `main`, cap two. Run `493f1052a969ff495c41afae`, registered worker 1 `6afe9cba-0704-83ec-9468-fb09cb209902`.
- At 06:57:02 UTC it held on the declared approval boundary with one saved worker. The invocation carried the owner's literal `I approve` scoped to the one proposed edit. The original worker resumed at 07:03:50 UTC. The Windows log records one same-chat owner Send with positive readback at 07:04:30 UTC. The run count remained one and no replacement worker was created.
- GitHub readback pinned `main` at `10e5aac1a2a11842aa72ccd4a1dd28cd3151a976`, with the current worker/run trailers, `Chat-Succession-Next: Append verification line to NOTES.md`, and the exact first line `Pebble approved`. The controller verified the publication at 07:07:11 UTC.
- The automatic successor remained `prepared`. Chrome failed to establish a fresh Project composer at 07:07:43 UTC, before Send. After removing disposable empty Chrome windows, one assisted retry of the same prepared action reproduced the failure at 07:12:24 UTC. One same-chat owner Send and zero successor Sends were recorded. A live repeated owner invocation and terminal stop were not run.

## Trial B — Authorized branch rotation

- Repository `JayDEmily/chat-succession-trial-rotation`, seed `main`, cap two. Run `2c4bd1cb353aa66f94590f28`, registered worker 1 `6afe9e15-c5d0-83ec-908f-157463a3a5f5`. A different work record, `MISSION.txt`, defines the pre-authorized planning and review.
- Initial bootstrap held on a browser draft. The verified disposable draft was cleared, and a plugin retry registered the first worker. The worker published a bicycle-bell checklist at `793d5361e3c37b8da88a192d31da40aedf418faa` on `work/checklist`. GitHub readback confirmed its exact run/worker trailers and `Chat-Succession-Next: Review the checklist and record the result`.
- The first observer held because the plain branch locator was rendered in a Chrome accessibility structure different from the original matcher. The independently reviewed 0.4.1 matcher verified the same saved response in a no-Send readback. A plugin request resumed observation after the fix. At 07:08:36 UTC Git verification succeeded. The effective checkpoint became `work/checklist` and the pending successor was prepared with that branch, leaving the seed branch, run, and count intact.
- Chrome failed before the successor Send at 07:09:07 UTC. One worker, zero successor Sends, and a preserved `prepared` action. A separate no-Send prepare reproduced the composer failure.

## Verdict

G1 offline implementation passed. G2 installed bounded acceptance remains open. The two trial checkpoints are valid and their pending successors are ready to retry once Chrome can establish a verified fresh composer. Both holds were before Send. A snapshot showed approximately 0.6 GiB of free physical memory, but the cause of the failed Chrome navigation was not established. Assisted recovery steps are recorded above.
