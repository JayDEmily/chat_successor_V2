# Chat succession: practical test kit

**Reference date: 17 November 2026 · Delivered mode: offline only**

Start from the owner's confirmed proof that one successor can be launched.
The question now is whether useful work can **keep iterating** correctly.
This kit accepts the owner's authenticated personal accounts, nominated
ChatGPT Project and same GitHub repository as prerequisites. It does not
add per-handover approvals or the old pilot's restrictions.

## Quick start — no accounts, network or browser needed

From this extracted directory, with Python 3.10+ and local Git available:

```sh
python3 run_offline.py
```

Results go to `reports/my_run/`. No dependency installation is needed.
The runner returns 0 for a full pass, 1 for failure, and 2 if tests are skipped
(e.g. local Git is absent). It uses temporary local repos, only Git's `file`
transport, and no production checkout. Temporary repos are cleaned per test.

**Delivered execution: 119 tests passed; 0 failed, 0 errored, 0 skipped.**
This includes 36 parser fixtures, 10 composer-observation fixtures, 16 replay
scenarios, 36 controller tests, 9 workload tests, 8 real local-Git tests, and
4 archive-inspection tests. One controller test also exercises 300 seeded
model traces; those are not counted as 300 additional tests.
See [`reports/executed/RESULTS.md`](reports/executed/RESULTS.md) and the
per-case JSON/logs alongside it.

**Live ChatGPT tests: NOT RUN. Authenticated GitHub tests: NOT RUN.**
There is no live browser adapter in this deliverable. The executable code is
a new reference model/test harness, not the missing historical launcher.

## What to read

1. [`docs/ASSESSMENT.md`](docs/ASSESSMENT.md): complete archive review, what is
   supported, the accepted launch baseline, and evidence limits.
2. [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md): ordered tests and acceptance criteria.
3. [`docs/OWNER_RUNBOOK.md`](docs/OWNER_RUNBOOK.md): owner-environment procedures.
4. [`docs/PROTOCOL_AND_ADAPTER.md`](docs/PROTOCOL_AND_ADAPTER.md): connect the
   existing proven launcher to the three-status loop, without a new front end.
5. [`OWNER_INSTRUCTIONS.txt`](OWNER_INSTRUCTIONS.txt): exact current owner wording.

## Simple operating shape

Nominate the Project, repo, branch and maximum once. Start one controller.
Normal operation is only:

| Final worker status | Controller action |
|---|---|
| `NEED_MORE_TIME` | Send “Okay, continue working.” to the same chat. |
| `TASK_COMPLETE` | If the whole job is finished, stop; if capped, stop; otherwise launch one fresh chat in the same Project with the short repo pointer. |
| `ERROR` | Stop automatic posting and show the blocker to the owner. |

Only actual observed conversation IDs count. The initial worker counts as one.
An unknown outcome, partial response or ambiguous interpretation is a
controller hold, **not** a fourth worker status.

## Workload and replay tools

```sh
# Fully local, four-slice repository fixture; refuses a nonempty destination.
python3 tools/repo_fixture.py init --root /tmp/succession-fixture --steps 4 --run-id demo

# MOCK worker changes local fixture files only; does not publish or call ChatGPT.
python3 tools/repo_fixture.py simulate-slice --root /tmp/succession-fixture --chat-id c1
python3 tools/repo_fixture.py verify --root /tmp/succession-fixture

# Synthetic event traces; not a browser recording.
python3 -m succession.replay fixtures/sequence_cases.json --out /tmp/succession-replay.json

# Reproduce every-member archive inspection without extracting/executing it.
python3 tools/inspect_archive.py sources/original_archive.tar.gz --out /tmp/archive-audit.json
```

Use a fresh directory name if the fixture already exists; no cleanup command
here deletes owner data. Owner live tests use a dedicated test path/branch in
**the same nominated repo**, not a different GitHub repository.

## Package boundary

- Original upload preserved byte-for-byte in `sources/original_archive.tar.gz`.
- Ten source documents reproduced verbatim under `sources/archive_text/`.
- Complete member inventory, Git-object audit and read-only Git checks in `reports/`.
- No credentials, account sessions, live browser recordings or GitHub changes.
- SHA-256 values in the delivery manifest are file-integrity evidence, not a
  proposed runtime handover/hash ceremony.
