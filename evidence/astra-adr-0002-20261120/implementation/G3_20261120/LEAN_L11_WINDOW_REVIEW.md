# L11 independent review of worker window sizing

**Offline accept** for `23c66570a4bfd3c08158cf5c771b40e354c535d1` on `codex/chat-succession-finish`. I reviewed the original candidate `808257175b235967964ad48a31fed843521623c9` against `5457384bfa457269253827916d30cc7a38c20be6` and independently checked the follow-up.

## Window routing and provider failures

- The adapter requests maximization only for a newly acquired window on the nominated Project landing page during Prepare or for the exact saved chat during missing-view recovery. The resize uses the acquired handle and the existing profile check. Reused Prepare windows, existing saved views, and comparison windows for owner re-entry and stale recovery bypass the new resize call.
- The first candidate could return a pre-resize URL if the window provider changed geometry, the active route changed and the provider then threw. I reproduced that sequence with synthetic UI Automation. The correction polls again after every resize attempt, reads the Prepare route and composer again, and runs the existing stable identity reads for recovery. In temporary copies the new regression failed on `8082571` and passed on `23c6657`.
- Synthetic checks held a wrong Project, wrong profile or different saved chat before maximization. Missing-view recovery restored a matching saved worker after a resize failure, held when a failed resize changed the route, and skipped resize when the existing saved view was available. The adapter skipped modal, already maximized and non-maximizable windows. Preflight and newly opened recovery still use their existing `WindowPattern` requirement for closing a temporary window.

## Receipt boundary and reruns

- All six Windows PowerShell suites, 118 Windows integration cases, and 119 reference cases passed on the follow-up. An initial integration run hit ten disposable Git setup errors. Removing inherited `GIT_CONFIG_*` overrides from the test process resolved the setup failure.
- The eight headless Chrome reader assertions passed on the follow-up. The reader withheld an exact post on a saved URL while either rendered conversation ID was provisional, then reported the same turn and reply after both IDs matched. Six additional in-memory headless assertions passed at `8082571`, using the same reader and fixture sources as the follow-up. They challenged wrong saved IDs, stale and rebound DOM after a route change, and qualification of fresh matching DOM. The native receipt test separately rejected provisional URLs and unqualified samples before accepting the exact post when the rendered IDs qualified.

## Live limits

The existing handle-acquisition rule can still mistake a manually opened same-profile window on the same route for the launcher’s window if it appears during acquisition. This review used synthetic UI Automation and a disposable headless Chrome profile on loopback. It performed zero Sends, touched no authenticated views or installed routes, and generated no live maximization or recovery evidence. L11 still requires an owner decision on the held Cat/Dog worker and separate end-to-end acceptance. [L11 progress](../../../../PROGRESS.md)
