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

G1 offline implementation passed. In the first attempt at G2 both holds were
before Send. A snapshot showed approximately 0.6 GiB of free physical memory,
but it did not establish the cause of the failed Chrome navigation.

## Successor composer follow-up

- Cleanup closed several old Chrome windows and raised available RAM. The
  default fresh-window retry still failed. The new window had the exact
  Project URL in the address bar, but remained untitled with no accessibility
  document or composer. A reload of a disposable no-document window did not
  fix it.
- A no-Send probe followed the verified Project link in the completed rotation
  worker's existing window and verified the exact Project, no saved chat ID,
  an empty composer and no attachments. The reviewed adapter now checks the
  triggering saved response and records the window against the same pending
  action before following that link. It reuses only a verified fresh composer.
- The approval trial's existing pending action prepared successfully at
  07:31:18 UTC. One Send attempt ended in an uncertain hold at 07:32:09 UTC.
  The final reviewed path prepared the rotation trial at 07:36:59 UTC and
  its one Send attempt ended in an uncertain hold at 07:38:06 UTC.
- Read-only inspection matched both prepared windows, Project IDs and
  successor prompts. Chrome showed provisional `local-chatgpt` addresses
  in both. Neither showed a server-saved worker ID. Both controller counts
  remain one and the two previously published Git checkpoint tips still
  match. No uncertain attempt was repeated.
- Independent review approved the adapter change. The 46 integration tests,
  119 reference tests, PowerShell syntax and Windows atomic target replacement
  passed. G2 remains open pending read-only reconciliation and terminal work.

## Bird and Pig clean Chrome trial

- A complete Chrome shutdown on Windows raised available physical memory from
  about 1.4 to 6.3 GiB. The James profile reopened with one blank tab. The
  desktop kickoff used plugin 0.4.1 and the verified landing link for the new
  Bird and Pig Trial Project. Run `9c9a07c8f8eb7c2ac7b34adb` used `main` with a
  cap of two saved workers.
- The controller registered Bird (`6afed064-9f0c-83ec-bff0-36d3321ec3fe`).
  GitHub verified the [first story commit](https://github.com/JayDEmily/chat-succession-bird-pig/commit/eeba425d61918e17f7c8ab7ff9e9561e1d6943bb)
  with the matching worker and run trailers. At 10:34:22 UTC the controller
  confirmed its successor Send to Pig (`6afed0a8-1420-83ec-b7dc-9215bda97834`).
- Pig published the [final story commit](https://github.com/JayDEmily/chat-succession-bird-pig/commit/b7d083d88874f2c410d1901819fbb7c17ba4fdb9)
  with matching trailers and `Chat-Succession-Next: FINISHED`. At 10:35:06 UTC
  the controller held after one malformed browser observation. Two subsequent
  read-only observations found the completed response. A manual `resume` and
  one `cycle --prepare-only` on the same run recorded `STOP_FINISHED`, two
  saved workers and no pending action.
- The bridge now retries once after a JSON parse error in read-only `Observe`.
  The exact cause of the original malformed output is unknown. A Windows
  probe injected the bad first read and recovered through two fresh reads of
  Pig's saved response. The 48 integration tests and 119 reference tests
  passed. Independent OpenAI Exec Plans review approved the code change.

## Hidden Project lookup and overlapping story runs

- The installed launcher received a name-only `inspect` request for **My cat
  and dog**. The existing lookup succeeded when the Project was below the
  fold. It failed when the Projects section was collapsed and the Project row
  was absent. Windows UI Automation exposed the exact Projects button as
  collapsed. The adapter now expands that button in its temporary lookup
  window. The same request then resolved `g-p-6afe677ff69c81919764c224a992a7ec`
  and the lookup window closed.
- After that check, the installed Windows launcher opened the two story runs
  from their verified Project links. It staggered startup by 23 seconds. Both
  controllers were active together for 3 minutes and 9 seconds. They used
  separate run journals and Ubuntu Git readers and confirmed four distinct
  saved workers across the two Projects.

| Story | Run ID | Controller start (UTC) | Confirmed successor (UTC) | `STOP_FINISHED` (UTC) | Published story |
| --- | --- | --- | --- | --- | --- |
| Cat and Dog | `665ea3264e8d8c70d63adead` | 10:53:14 | 10:55:10 | 10:56:46 | [Cat and Dog](https://github.com/JayDEmily/chat-succession-cat-dog-pair/blob/61c609a3391b1adbb0bb462beab71e4cff39a21c/STORY.md) |
| Bird and Pig | `3a1bc9fa7d591d0030d5389d` | 10:53:37 | 10:59:11 | 11:01:08 | [Bird and Pig](https://github.com/JayDEmily/chat-succession-bird-pig/blob/5c3da4ee0d3edea355f229d8f73e7d15c4f3b95a/STORY.md) |

- GitHub readback verified both lines, the parent of each final commit, and
  each commit's run and saved-worker trailers. Both final trailers said
  `FINISHED`. Both journals recorded one confirmed successor, exactly two
  saved workers, and no pending action at terminal stop.
- Bird's opening line was published at 10:54:47 UTC. Windows still reported a
  Stop control at 10:58:28 UTC and first confirmed the marker at 10:58:50 UTC.
  A read-only Chrome inspection saw the final marker before the controller
  acted. The observed publish-to-handoff gap was 4 minutes and 24 seconds.
- The desktop started with one Chrome window and peaked at three. Both
  successors reused their respective worker windows. Closing the two finished
  test workers returned the console to one Chrome window. The 48 integration
  tests, 119 reference tests, PowerShell parser and independent OpenAI Exec
  Plans source review passed.

### Concurrent window startup follow-up

- Two installed name-only `inspect` requests started at 11:07:41.573 and
  11:07:41.574 UTC. Bird and Pig resolved its Project. My Cat and Dog held
  with `Ambiguous new Chrome windows`. The probe's remaining temporary window
  was closed.
- The adapter now uses a Windows session mutex while it opens Chrome and
  identifies the new window. A waiting process acquired an abandoned test
  mutex and released it successfully.
- The same requests started at 11:09:46.355 and 11:09:46.356 UTC with the fix.
  Both returned `inspected` with their expected Project IDs. Both lookup
  windows closed, returning the console to one Chrome window. PowerShell
  parsing and all 48 integration and 119 reference tests passed. Independent
  OpenAI Exec Plans review verified the lock scope and release paths.
