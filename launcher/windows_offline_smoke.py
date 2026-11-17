"""Windows-local offline integration test for journal.py.

Runs on explicit Windows Python. Creates only a disposable database; never
opens Chrome, publishes Git data, or calls a ChatGPT API.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    journal = Path(__file__).with_name("journal.py")
    if not journal.is_file():
        raise RuntimeError("journal.py missing beside Windows smoke test")
    with tempfile.TemporaryDirectory(prefix="chat_succession_journal_test_") as d:
        db = str(Path(d) / "journal.sqlite3")
        run = "offline-windows-test"
        sha = "a" * 40

        def invoke(*args, expect=0):
            proc = subprocess.run(
                [sys.executable, str(journal), *args],
                capture_output=True, text=True,
            )
            if proc.returncode != expect:
                raise AssertionError(
                    f"journal returned {proc.returncode} (expected {expect}): "
                    f"{proc.stdout} {proc.stderr}"
                )
            return json.loads(proc.stdout)["state"]

        assert invoke("init", "--db", db) == "initialised"
        common = ("--db", db, "--run", run, "--step", "2")
        assert invoke("reserve", *common, "--sha", sha) == "reserved"
        assert invoke("status", *common) == "reserved"
        assert invoke("reserve", *common, "--sha", sha, expect=4) == "held"
        assert invoke("reserve", *common, "--sha", "b" * 40, expect=4) == "held"
        assert invoke("mark", *common, "--sha", sha, "--state",
                      "effect_unknown", "--receipt-json", "{}") == "effect_unknown"
        assert invoke("reserve", *common, "--sha", sha, expect=4) == "held"
        Path(db).unlink()
        assert invoke("reserve", *common, "--sha", sha, expect=4) == "held"
        assert not Path(db).exists(), "missing journal was silently recreated"

    print("WINDOWS_JOURNAL_SMOKE_PASS: init/readback/duplicate/conflict/unknown/loss")
    print("NO_SEND: all database work used a temporary local file")


if __name__ == "__main__":
    main()
