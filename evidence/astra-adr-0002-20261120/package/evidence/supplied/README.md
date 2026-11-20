# Chat Succession handoff for Astra

Prepared on 20 November 2026 after the owner paused the live desktop trials. Start with the [brief for Astra](ASTRA_BRIEF.md), then read the [pause checkpoint and findings](evidence/pause-2026-11-20/LIVE_PAUSE.md).

| Contents | Location |
| --- | --- |
| Chat Succession Git history, including the original work and every advertised branch at capture | `history/chat_successor.bundle` and `history/refs.tsv` |
| Ready-to-read source, plans, tests, and existing evidence pinned to `283e6c17bf3359c203a362fd6593563480eeea5f` | `source/` |
| Original Astra design, ADR, test kit, and prior live results | [ADR](source/docs/adr/0001-generic-entry-and-re-entry.md) · [Astra plan and gates](source/docs/astra-succession/README.md) · `source/astra/2026-11-17/` · `source/evidence/` |
| Separate disposable fixture histories | `history/fixtures/` contains the Cat/Dog pair, Bird/Pig, the four-turn My Cat and Dog story, iPhone approval, and branch-rotation repositories |
| Earlier 19 November handoff with its offline reproduction, timing evidence, and known errors | `evidence/historical/` |
| Local pause snapshots, selected controller events, and captured offline test output | `evidence/pause-2026-11-20/` |
| The exact plugin archive uploaded to Shoco | `release/chat-succession-0.4.3.zip` |
| File checksums and Git restoration verification | `SHA256SUMS.txt` and `history/VERIFICATION.md` |

The history is a full Git bundle. It includes the GitHub refs and reachable commits, and the four checked Ubuntu branch tips are present in that history. The live pause evidence uses stable worker labels for local journal excerpts. Git receipts in the committed history retain their original trailers.

## Restore the repository offline

From the extracted directory, run:

```sh
git clone --mirror history/chat_successor.bundle chat_successor-history.git
git -C chat_successor-history.git fsck --full
git clone --branch codex/chat-succession-finish chat_successor-history.git chat_successor-review
```

Each fixture bundle can be restored with `git clone --mirror` in the same way. The `source/` snapshot is available without Git. To read the earlier archive, extract it into its own directory and open its `START_HERE.md`.

## Reproduce the offline tests

From the extracted directory, use Python 3 and Git. Run the recovery check in Windows PowerShell.

```sh
(cd source && python3 -B -m unittest discover -s integration/tests)
(cd source/astra/2026-11-17/unpacked/chat_succession_test_kit_20261117 && python3 -B -X utf8 -m unittest discover -s tests)
```

```powershell
powershell -NoProfile -File source/integration/tests/test_worker_view_recovery.ps1
```

The pause checkpoint and fixture history are review inputs. Resume or run further live acceptance under the owner's direction.
