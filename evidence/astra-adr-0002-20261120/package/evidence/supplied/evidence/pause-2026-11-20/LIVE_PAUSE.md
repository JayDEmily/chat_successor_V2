# Live checkpoint and findings

On 20 November 2026 at 08:49:10 Sydney time, the owner requested a pause and handoff for a new Astra review. Both trial controllers acknowledged the pause and exited their observation loops. Their saved journals had no pending Send. The GitHub finish branch was `283e6c17bf3359c203a362fd6593563480eeea5f`. The controller and plugin source match candidate `2c29406b1c43904c5ead79064fe7856971e0aa2e`.

| Trial | Observed at pause | Verified publication |
| --- | --- | --- |
| Rowing in Project A Test | Run `b401f984a1927f6979067d07`, two distinct saved workers, cap two. The controller verified the first receipt, followed the isolated branch, and confirmed one automatic successor. The second worker was in progress. | One documentation-only receipt at `acbf989`. [Published commit](https://github.com/JayDEmily/rowing2026/commit/acbf989ffefed1771f9fd9d08261bdb9d2e4bce0) |
| SolidWorks in Project B Test | Run `271867d56ebd3443a4b40fa6`, one saved worker, cap two. The first receipt and completion reply were saved. The controller had not consumed the reply or confirmed a successor when paused. | One metadata-only Help-index receipt at `b6579ae`. [Published commit](https://github.com/JayDEmily/sw_v1/commit/b6579ae8dc308ad4912ede85530056d53566bc8a) |

Both published receipts matched the first saved worker and run in their Git trailers. GitHub comparisons found one commit ahead of each pinned checkpoint with exactly one added Markdown file. The original Rowing and SolidWorks refs still pointed to the pinned bases when checked after the pause.

The already-started Rowing successor published `1eadc9d` after the pause. GitHub shows one verification line added on top of `acbf989` and matching run and second-worker trailers with `FINISHED`. The controller stayed paused and did not record a terminal cycle for it. [Second Rowing receipt](https://github.com/JayDEmily/rowing2026/commit/1eadc9d8b5486aecf13b312a0d02737b3cf8a35f)

## Observed failures and recoveries

| Finding | Outcome and evidence |
| --- | --- |
| The earlier James Student private plugin was absent from the Shoco personal plugin list. Desktop Commander also gave Shoco a different `LocalAppData`. | The owner confirmed that both accounts have GitHub and PC access. Created and read back a private Shoco copy of 0.4.3 and routed its connector environment to the signed-in Shoko Chrome profile (`Profile 11`). The previous James Student flow uses its separate verified Chrome profile (`Profile 13`). The installed wrapper has a backup and retains its existing default command. [Private Shoco release](https://chatgpt.com/plugins/plugins_6aff6858ab788191a4a6b7c15a7216bc) |
| The staged Shoco wrapper initially pointed runs to an account-specific directory while the 0.4.3 worker prompt expected journals beside the native launcher. | Aligned the wrapper with the existing worker path before a live Send. The 0.4.3 backend and private plugin package remain the staged candidate. |
| Both first launch requests failed with `Invalid job_id`. | The launcher accepts exactly 24 lowercase alphanumeric characters. The oversized IDs failed validation before writing an initial Send intent. Corrected both inputs. |
| Rowing then failed at `Fresh Project composer not established` during overlap startup. | Verified the configured run had neither a Send intent nor a registered worker. Retried that same run once and confirmed its first saved worker. The exact cause of the first preparation timeout is unproven. |
| Moving the Rowing worker to an inactive Chrome tab hid the registered view. | Paused with one saved worker and no pending Send, then restarted the observer while SolidWorks kept running. Recovery reopened the same Rowing worker at 08:38:08 Sydney time and preserved the count. One later successor followed its verified receipt. |
| Chrome continued to show a Stop control during the SolidWorks first response. | Two live comparisons returned `waiting` when the fresh view lacked a newer completed response. Later the saved response showed the branch marker and `TASK_COMPLETE` while the original view still showed Stop. The owner paused before an automatic stale reload or second worker was confirmed. |
| The first SolidWorks Windows-to-WSL shell invocation lost the search query quoting and flags. | The worker corrected the read-only invocation and published only the verified one-result metadata. Its receipt states the limitation. |

## Earlier results to carry forward

- The original bounded Astra runs A, B, and F met the five-worker acceptance, with four automatic successors per run. Earlier assisted and held runs remain in the history. [Project progress](../../source/PROGRESS.md)
- The Cat/Dog and Bird/Pig examples verified parallel operation in distinct Projects. Prior Bird/Pig replay needed an operator-assisted reload of a stale view and then reached its cap of two. [Earlier live evidence](../../source/evidence/astra-generic-entry-20261119/live-acceptance.md)
- An earlier James Student iPhone launch completed the four-worker My Cat and Dog story. A separate iPhone approval delivered one scoped approval to worker one, launched one successor, and finished at two workers. [Earlier handoff](../historical/Chat-Succession-Astra-Handoff-2026-11-19.tar.gz) · [Approval result](https://github.com/JayDEmily/chat-succession-trial-approval/blob/1590c45af104e34cdcd5c2820e9ce30c9da35e80/NOTES.md)

Shoco's fresh iPhone approval fixture was staged at `b91b00f` on `codex/g2-iphone-approval-shoco-20261120`. No iPhone start or approval was performed on that branch. Completion and terminal checks for the paused desktop pair, a successful automatic stale reload, and a concurrency test above two remain open. [Fresh approval fixture](https://github.com/JayDEmily/chat-succession-trial-approval/blob/b91b00fe75be2ca011eac1ad1cc0d668ffd8d8bf/README.md)
