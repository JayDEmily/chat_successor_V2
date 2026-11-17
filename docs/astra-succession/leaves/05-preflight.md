# Leaf 05 — Set up the owner environment

**Entry:** G1 and an assigned owner-environment run. **Output:** the live adapter connected to the nominated environment and Astra's first test fixture ready. Follow [the owner runbook](../../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/docs/OWNER_RUNBOOK.md#1-one-time-run-setup).

1. Use the Project, repo, working branch and cap nominated once by the owner, along with the existing authenticated desktop and Git write route. Connect the live observations and proven navigation/Send method from Leaf 03.
2. For L01, seed a dedicated fixture path on the nominated same-repo test branch. From the kit directory run `python tools/repo_fixture.py init --root <fixture> --steps 2 --run-id <run-id>` then `python tools/repo_fixture.py verify --root <fixture>`. Publish the fixture and current-work pointer using normal Git and confirm workers can read the seed.
3. Use Astra's [Project instructions](../../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/prompts/project_instructions.txt) and [short successor pointer](../../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/prompts/successor_message.txt). For L01 use cap 3 or higher. Initialize the one controller with the observed saved initial worker and count of one. Use the runbook's optional time budget if selected.

**G2 check:** The runbook's one-time setup is complete and the worker can read the published fixture. The next action is L01. Capture L07 and L08 as part of the live cases.
