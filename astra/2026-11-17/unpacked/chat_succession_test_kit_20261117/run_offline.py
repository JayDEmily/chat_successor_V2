#!/usr/bin/env python3
"""One-command offline test run. No installations or remote/browser operations."""
from __future__ import annotations
import argparse
import io
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
from succession.replay import replay_case


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append({"test": test.id(), "outcome": "PASS"})

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.records.append({"test": test.id(), "outcome": "FAIL",
                             "detail": self._exc_info_to_string(err, test)})

    def addError(self, test, err):
        super().addError(test, err)
        self.records.append({"test": test.id(), "outcome": "ERROR",
                             "detail": self._exc_info_to_string(err, test)})

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.records.append({"test": test.id(), "outcome": "SKIP", "reason": reason})

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err:
            self.records.append({"test": subtest.id(), "outcome": "SUBTEST_FAIL",
                                 "detail": self._exc_info_to_string(err, test)})


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, default=ROOT / "reports/my_run")
    args = p.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    start = time.monotonic()
    result = unittest.TextTestRunner(stream=stream, verbosity=2,
                                    resultclass=RecordingResult).run(suite)
    duration = time.monotonic() - start
    output = stream.getvalue()
    (out / "test_output.txt").write_text(output, encoding="utf-8")
    trace = []
    replay_error = None
    if result.wasSuccessful():
        try:
            cases = json.loads((ROOT / "fixtures/sequence_cases.json").read_text())
            trace = [replay_case(case) for case in cases]
        except Exception as exc:
            replay_error = repr(exc)
    (out / "replay_trace.json").write_text(json.dumps(trace, indent=2) + "\n", encoding="utf-8")
    git_log = []
    for name, module in list(sys.modules.items()):
        if name.endswith("test_git_handoff"):
            git_log = getattr(module, "GIT_OPERATIONS", [])
    (out / "local_git_operations.json").write_text(json.dumps({
        "mode": "REAL_LOCAL_GIT_ONLY", "network_protocols_allowed": ["file"],
        "operations": git_log,
    }, indent=2) + "\n", encoding="utf-8")
    outcome = ("FAIL" if not result.wasSuccessful() or replay_error else
               "PARTIAL_SKIPPED" if result.skipped else "PASS")
    git_version = None
    if shutil.which("git"):
        git_version = subprocess.run(["git", "--version"], text=True, capture_output=True).stdout.strip()
    counts = {
        "tests_run": result.testsRun, "failures": len(result.failures),
        "errors": len(result.errors), "skips": len(result.skipped),
        "parser_fixtures": 36, "composer_fixtures": 10, "sequence_fixtures": 16,
        "controller_methods": 36, "fixture_methods": 9, "local_git_methods": 8,
        "archive_inspection_methods": 4,
        "seeded_model_runs_inside_one_controller_test": 300,
    }
    report = {
        "report_reference_date": "2026-11-17",
        "mode": "OFFLINE_ONLY", "outcome": outcome, "counts": counts,
        "elapsed_seconds": round(duration, 3),
        "environment": {"python": platform.python_version(), "git": git_version,
                        "platform": platform.platform()},
        "records": result.records,
        "replay_error": replay_error,
        "live_ChatGPT_tests_performed": 0, "live_GitHub_tests_performed": 0,
        "semantic_model_tests_performed": 0,
        "limitations": [
            "This tests a new reference model, not the absent historical launcher source.",
            "Browser, UIA, ChatGPT and authenticated GitHub behavior were not exercised.",
            "Semantic verdicts are injected fixtures, not verified classifier performance.",
            "Local Git repositories are stand-ins, with only file transport permitted.",
            "No guarantee of exactly-once browser delivery or long-run reliability is claimed.",
        ],
    }
    (out / "offline_results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary = f"""# Executed offline results

Reference date: 17 November 2026. Mode: **OFFLINE ONLY**.

**{outcome}: {result.testsRun} unittest cases; {len(result.failures)} failures,
{len(result.errors)} errors, {len(result.skipped)} skips.**
Measured test-suite duration: {duration:.3f} seconds in the recorded environment.

Included: 36 parser cases, 10 composer-observation cases, 16 sequence replays,
36 controller methods (one runs 300 seeded model traces), 9 fixture methods,
8 real **local** Git tests, and 4 full-archive inspection methods.
The 300 traces and the separate trace export are not added to the unittest total.

- `offline_results.json`: per-case outcomes and environment.
- `test_output.txt`: actual test runner output.
- `replay_trace.json`: synthetic decisions, IDs, counts and fake sends.
- `local_git_operations.json`: real local commands/results, temporary paths normalized.

**Live ChatGPT: NOT RUN. Authenticated GitHub: NOT RUN. Real semantic classifier: NOT RUN.**
These results do not validate browser selectors, UIA placeholder interpretation,
account/tool access, actual unattended succession, or a live 30-chat chain.
Historical reports of 37 tests belong to the archive; they were not rerun here.
"""
    (out / "RESULTS.md").write_text(summary, encoding="utf-8")
    print(output, end="")
    print(f"Report: {out / 'offline_results.json'}")
    return 1 if outcome == "FAIL" else 2 if outcome == "PARTIAL_SKIPPED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
