# Leaf 01 — Adopt the offline controller

**Entry:** G0. **Output:** importable `succession` package and baseline contract tests.

1. Copy `__init__.py`, `core.py` and `composer.py` from the [imported reference package](../../../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/succession/) into the root `succession/` runtime package. Keep the API and defaults from the [adapter contract](../../../../astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/docs/PROTOCOL_AND_ADAPTER.md). Keep the imported snapshot intact.
2. Exercise the runtime package with Astra's parser/composer tables, controller tests and golden replays. Reuse the existing assertions and fixture data, and point replay and fake browser support at the runtime package. Keep fake/replay code under `tests/` and use explicit UTF-8 when reading JSON fixtures. Ensure the tests import the root runtime package. Use `tests/test_tables.py` and `tests/test_controller.py` for these checks.
3. Verify prepared/sending/uncertain transitions, atomic save/load and the recovery API. Confirm that a repeat or URL alias cannot inflate the count, the initial worker counts, `NEED_MORE_TIME` at cap stays in-thread, completed work at cap stops after validating publication, and finishing the programme stops at any count. Simulated 1→30 exercises the boundary. Keep the three worker statuses and the existing exact continuation and successor messages.

**Leaf check:** From the repo root run `python -m unittest discover -s tests -p "test_tables.py" -v` and `python -m unittest discover -s tests -p "test_controller.py" -v`. All 98 reference cases in these groups pass (36 parser, 10 composer, 16 replay and 36 controller), plus any integration regressions added. Commit and advance to Leaf 02.
