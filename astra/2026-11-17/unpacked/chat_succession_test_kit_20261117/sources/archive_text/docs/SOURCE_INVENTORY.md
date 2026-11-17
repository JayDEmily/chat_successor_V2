# Source and capture inventory

## Authoritative remote repository

`https://github.com/JayDEmily/chat_successor`

Observed remote branch heads, 17 November 2026:

| Ref | Exact SHA | Purpose |
| --- | --- | --- |
| `main` | `26b33e8991119f9886b23f0c01651c3f49435706` | Project creation and baseline design/planning |
| `work/task1-contract-preflight-20261117` | `f8c002690c0a1a9ff4f298bd9a8d68b21f5ba1f8` | Protocol, tests and offline launcher/journal implementation |
| `trial/succession-20261117-001` | `3b2c95b954eb90b1e6c9b82403dd1956c6f34b39` | R1/A2 and Chat 2 blocked-launch evidence |

The Ubuntu repository also contained an **uncommitted** draft of a simpler Project-specific launcher, plus the two untracked PowerShell scripts `launcher/check_static_guards.ps1` and `launcher/inspect_project_readonly.ps1`. These local changes must be distinguished from published GitHub commits.

A project-specific Windows staging directory contained offline and live UIA probe scripts, including `send_chat1_once.ps1`, `nav_probe.ps1` and the blocked-launch-era launcher. The source archive may preserve these as **evidence**; they do not form a production installation or prove 30-chat operation.

## Material not in scope

No NVIDIA or Second Chat OCR source, private account credentials, Chrome cookies or the personal journal database are included. The latter's `blocked` state is captured by the GitHub trial evidence.

## Reproduction principle

Use the three exact refs above to inspect historical GitHub state. Do not merge the stopped trial into main, reset its held journal, replay an ambiguous Send or treat the 3-chat cap as an ongoing architectural requirement. The new architecture documents are a sandbox-only synthesis unless explicitly promoted by the owner.
