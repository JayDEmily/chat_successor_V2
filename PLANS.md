# Automatic Timer — four runs

Start with README.md containing exactly "This is a README.md file." and a newline.

| Leaf | Append one line |
| --- | --- |
| 1 | This is the first run. |
| 2 | This is the second run. |
| 3 | This is the third run. |
| 4 | This is the fourth run. |

The setup chat may perform leaf 1. For every later leaf, execute only in a genuinely fresh saved ChatGPT conversation in the same ChatGPT Project ("Chat succession project"), not the preceding chat. If the timer invocation is not itself such a conversation, use only an available supported or previously demonstrated one-shot launch mechanism to create exactly one fresh chat in the verified Project, giving it a pointer to this repository, branch, exact expected predecessor commit and leaf. Do not run the leaf in the timer's original conversation instead. If tooling or Project identity cannot be verified, report BLOCKED and stop; do not simulate a pass or request a manual launch.

Read the remote tip and README. Confirm the assigned leaf's preceding lines match exactly and the expected predecessor SHA matches the tip. Append only the one prescribed line, commit only README.md, publish by normal non-force Git push or an equivalent compare-and-update GitHub operation, and read back the exact remote tip and text. Do not advance another leaf in the same chat. If the line is already present or publication is uncertain, stop and reconcile rather than append again.

After verified publication, inspect all scheduled tasks. The owner has explicitly authorised deleting existing tasks for this experiment. Delete them where the supported task interface permits; otherwise pause every enabled task and disclose that deletion is unavailable. Do not delete chats. If leaf 4 is complete, stop without creating another timer. Otherwise create exactly one one-shot timer, not a recurring task, instructing it to create a new chat in the same Project and pass the next leaf, exact published SHA, repository and branch. Respect the platform's supported scheduling intervals and consent requirements (use an hour between subsequent scheduled invocations). No other timer or continuing worker. Stop on an uncertain timer creation, unsupported launch, or missing permission; do not retry blindly. Report the actual outcome, including new chat identity if observable, and the commit. Do not place private chat or account identifiers in the public repository.

Success: four successive single-line README commits on this isolated branch, with the three successor executions independently observed in distinct saved conversations in the intended Project; zero extra leaf commits or timers after leaf 4. Git history alone proves the file changes, not fresh-chat creation.
