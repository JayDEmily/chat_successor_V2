# Rowing continuation after owner approval

This is an ordinary-project transport example. The Rowing repository governs
what work is authorized. The snapshots here document the Chat Succession
behavior and the Git publication boundary.

| Sydney time, 19 November 2026 | Event | Evidence |
| --- | --- | --- |
| 15:05:49 | An existing Project chat launched one fresh saved desktop worker. The Windows controller began observing it on `work/bio2-golden-yaml-19-8plus-semantic-20261116`. | Windows timing log and saved state |
| 15:08:56 | The worker reported there was no authorized active assignment and ended with `CHAT_STATUS: ERROR`. The controller recorded `HOLD` and exited with one worker, no pending Send and no successor. | Saved and final Windows state, controller timing log, owner-supplied screenshots |
| By 15:28 | The owner gave approval in Rowing. The chat reported that it was continuing, had created a GY24 worktree based on the accepted parent, and recognized the old controller was halted. | Owner-supplied screenshots |
| 15:31:13 | A separate, read-only observation from desktop Chrome of the controller's exact saved worker still returned its first `ERROR` response, with no active Stop control. The controller was not running. | Live UIA readback and Windows process check |
| 15:43 | The Rowing chat reported a local checkpoint, concurrent edits in the worktree and staged whitespace diagnostics. It said it had left the staged work in place. This report does not identify who wrote the files. | Owner-supplied worker output |
| Around 16:17, before publication | Independent local Git readback found seven staged `new blank line at EOF` diagnostics in evidence logs. Git had no explicit `core.whitespace` value. The working-tree diff check passed. | `git-whitespace-before-publication.log` |
| 16:20:03 | GitHub returned the newly published GY24 branch at `ff2876dc3c3b0d739df1e5e08de0626233c7ffa9`. Both local whitespace checks passed. Local HEAD matched the published SHA. | `git-diagnostic-snapshot.json` |
| 16:21 | A parent-to-commit diff check returned the same seven whitespace diagnostics. The published commit has none of the three Chat Succession trailers. The original controller process was absent. | `published-checkpoint.json` and `controller-process-check.json` |

The available records cannot establish whether the chat that continued from
the iPhone was the identical saved worker with a stale desktop view or a
different chat. The original controller remained stopped and configured for
the older branch. Its Git access was through a separate bare reader, and its
log shows zero successor Sends and zero publication checks. The whitespace
problem came from staged file contents. The supplied evidence does not
identify the writer or prove the reported concurrency.

The new GY24 checkpoint demonstrates project work continued after approval.
The post-publication staged and unstaged checks covered uncommitted changes.
The committed patch still contains the seven blank lines.
There was no automatic Chat Succession handoff after approval.
The offline reproduction in `verification/reproduce_resume.py` exercises the
existing same-worker resume path and changed-branch behavior.

## User experience to review

The owner expects to tag the same plugin and say something natural such as
“I approve” when the previous chat context already establishes the scope.
The plugin should be able to resume a verified existing worker without
causing two workers to act on the same job. Project-specific approval,
branching and work rules belong to the project.
