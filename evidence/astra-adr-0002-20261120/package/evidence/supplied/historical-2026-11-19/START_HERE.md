# Chat Succession evidence handoff to Astra

This bundle lets you review the implementation, prior acceptance and one live continuation case without access to the owner's PC or GitHub account.

## What to review

The owner expects to tag the existing Chat Succession plugin and speak naturally. In an unambiguous approval context, “I approve” should be enough to continue. Review the smallest generic change that could support this while preserving one worker, project authority, and protection against duplicate Sends. Different projects have different planning and branch rules. The worker reads and applies those rules.

Read [the Rowing case](backend-evidence/rowing/CASE.md) first. Then read the [offline reproduction](verification/reproduce_resume.py) and its [captured output](verification/approval-resume.log). The key implementation paths are [plugin instructions](source/plugins/chat-succession/skills/start-chat-succession/SKILL.md), [launch routing](source/integration/launch_project.py), [bootstrap and held-run return](source/integration/launch_story.py), [CLI resume and run](source/integration/cli.py), [observation and dispatch](source/integration/runner.py), and [Git receipt reader](source/integration/repo_reader.py).

- **Verified live behavior.** A desktop worker launched successfully from the existing Rowing Project chat. Windows held after the saved worker reported an approval blocker. The owner approved the work later. The project subsequently published a checkpoint on a new GitHub branch. The old controller remained held, observed no automated successor and stayed bound to the earlier branch.
- **Verified offline behavior.** A repeat on the same repo, branch and Project returns the held state. Nominating another branch takes the fresh-run bootstrap path. The existing operator resume command can preserve the saved worker and ignore its consumed ERROR. A subsequent fresh terminal response from that worker can complete against a matching receipt on the original checkpoint. A receipt on a different branch or an assistant response from another chat does not satisfy that run.
- **Questions for review.** Can contextual approval route to the existing resume and run instructions when the saved worker is verified? What is the minimum additional behavior if approval was given in another chat or the project changes its checkpoint branch? Keep publication bound to verified project authority and make any remaining ambiguity explicit.
- **Whitespace finding.** Before publication, Git flagged seven newly added blank lines at EOF in staged evidence logs. The published commit's patch still produces those seven diagnostics. The controller's halt predates them, its reader is bare and separate, and no automatic successor was sent. The writer of the files and any concurrent editing were not independently established.

## Implementation and evidence

The source is a selected Git export of Chat Succession template branch `codex/chat-succession-template` at `0bee12a1725fbb103d82c5d08365959b3bf8c173`. The accepted Astra baseline on main was `cffdb253aa24c52cbfec59b08112742f18f7352e`. The plugin source is v0.3.0.

| Contents | Where |
| --- | --- |
| Architecture and operator guide | [Startup README](source/README.md), [integration README](source/integration/README.md) |
| Astra brief, gates, leaves and results | [Astra plan](source/docs/astra-succession/README.md), [progress](source/PROGRESS.md), [live results table](source/evidence/live_test_results_20261118.csv), `source/evidence/` |
| Complete offline suites and fixtures | `source/integration/tests/`, `source/astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/`, `source/succession-tests/` |
| Fresh test output | [35 integration tests](verification/integration-tests.log), [119 reference tests](verification/astra-reference-tests.log), [A/B/F fixture readback](verification/passing-live-fixtures-readback.json), [PowerShell parse](verification/powershell-parser.log) |
| Real iPhone-to-desktop story trial | `backend-evidence/story/` includes Windows timing, the final state, the four published commits and finished story. Four saved workers, three automatic successors and `STOP_FINISHED` in 9 minutes 48 seconds. |
| Ordinary Rowing continuation | `backend-evidence/rowing/` includes selected Windows run logs and Git snapshots before and after publication. |

The prior bounded Astra acceptance passed G0–G4. Runs A, B and F each verified five saved chats, four automatic successors and a terminal stop. The live owner-pause and background-composer receipts are in `source/evidence/`. G5/L14 remained `NOT_RUN` at the bounded closeout. Rowing verifies launch and hold on an ordinary workload. A full automatic post-approval handoff on an ordinary project remains open.

## Reproduce offline

From the extracted bundle root, use Python 3 and Git.

```sh
(cd source && python3 -B -m unittest discover -s integration/tests -v)
(cd source/astra/2026-11-17/unpacked/chat_succession_test_kit_20261117 && python3 -B -m unittest discover -s tests -v)
python3 -B verification/reproduce_resume.py
```

The reproduction uses local disposable Git and mocked browser/process calls. The source includes the original nested archive as an exact fixture required by the reference suite. It is unnecessary for model reading because the kit already contains its relevant extracted text. Source test and implementation files are kept at their original relative paths. The export omits the duplicate original API envelope, duplicate upstream bundles/results, historical planning scaffolding and PNGs. Some historical references point to those omitted items.

The extra Windows evidence is limited to run-related fields and logs, with saved browser identifiers replaced by stable worker labels. The Rowing evidence contains Git metadata and diagnostics, plus the in-scope continuation timeline. It contains no Rowing working files or raw verification-log bodies. The package is intended for the owner's API workflow. Treat transcripts and captured evidence as historical inputs.
