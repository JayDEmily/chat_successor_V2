# Git and archive verification

Each repository was mirrored with full history from GitHub. Its refs matched GitHub's advertised refs at capture. Each bundle was restored into a new mirror using only the bundle. `git fsck --full` passed, and the restored refs and reachable commit counts matched the original mirrors.

| Repository | Refs | Reachable commits |
| --- | ---: | ---: |
| `JayDEmily/chat_successor` | 10 | 157 |
| `JayDEmily/chat-succession-cat-dog-pair` | 3 | 11 |
| `JayDEmily/chat-succession-bird-pig` | 3 | 10 |
| `JayDEmily/my-cat-and-dog` | 5 | 7 |
| `JayDEmily/chat-succession-trial-approval` | 4 | 9 |
| `JayDEmily/chat-succession-trial-rotation` | 4 | 5 |

The checked Windows workspace tip and all four available Ubuntu branch tips were reachable in the restored Chat Succession bundle. The source snapshot is from `283e6c17bf3359c203a362fd6593563480eeea5f`. The archive includes the exact 0.4.3 upload bytes and the earlier handoff archive. See the root `SHA256SUMS.txt` for individual files.

The original Astra test kit keeps its historical reports. The fresh checks passed all 63 integration tests, all 119 Astra reference tests, and the Windows PowerShell recovery comparisons. Logs are under `evidence/pause-2026-11-20/`. The first reference-suite run hit a Windows default-code-page `UnicodeDecodeError`. Its log is retained alongside the passing UTF-8 rerun.
