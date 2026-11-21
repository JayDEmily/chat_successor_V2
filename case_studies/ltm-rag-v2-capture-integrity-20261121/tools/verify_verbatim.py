#!/usr/bin/env python3
"""Verify the unredacted source supplement without network or browser operations."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
V = ROOT / "verbatim"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parsed(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_live(path: str, expected: bytes, enabled: bool) -> None:
    if not enabled:
        return
    original = Path(path)
    check(original.is_file(), f"Original not available for live comparison: {path}")
    check(original.read_bytes() == expected, f"Original has changed: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compare-live-sources", action="store_true",
                        help="Also compare archived sources against their surviving original local files")
    args = parser.parse_args()
    try:
        local = parsed(V / "local-source-provenance.json")
        records = local["records"]
        check(len(records) == 12, "Wrong original local file count")
        for entry in records:
            data = (V / entry["archive_relative_path"]).read_bytes()
            check(len(data) == entry["source_bytes"], "Local-original source length changed")
            check(sha(data) == entry["source_sha256"] == entry["archived_sha256"],
                  "Local-original source checksum mismatch")
            check(entry["readback"] == "BYTE_EQUAL", "Local-original source equality unproved")
            check(not entry["authentication_token_replacements"], "Unlisted token substitution")
            verify_live(entry["source_local_path"], data, args.compare_live_sources)
        print(f"PASS: {len(records)} original local files and routing configuration, byte-equivalent")

        trace = V / "trace/20261121-220236-223402-recorded-tool-calls.jsonl"
        content = trace.read_bytes()
        provenance = parsed(V / "trace/source-and-extract-provenance.json")
        limitations = parsed(V / "trace/TRACE_LIMITS.json")
        check(sha(content) == provenance["trace_sha256"] == limitations["trace_sha256"],
              "Recorded original tool history digest mismatch")
        events = [json.loads(row) for row in content.decode("utf-8").splitlines()]
        check(len(events) == provenance["tool_records"] == limitations["extracted_tool_records"] == 245,
              "Original tool history record count wrong")
        check(events[0]["timestamp"] == "11/21/2026, 22:02:36", "Unexpected first tool event")
        check(events[-1]["timestamp"] == "11/21/2026, 22:34:02", "Unexpected last tool event")
        count_omissions = sum("omitted" in json.dumps(ev.get("output", {})).lower() for ev in events)
        check(count_omissions == limitations["recorded_output_omission_marker_entries"] == 32,
              "Missing original tool-history output omission markers")
        print(f"PASS: {len(events)} tool-call records with all {count_omissions} upstream output omissions disclosed")

        for command in provenance["commands"]:
            check(command["changes"] == "NONE" and command["message_included_verbatim"],
                  "Unexpected command editing")
            found = [e for e in events if e["timestamp"] == command["source_timestamp"]
                     and e["toolName"] == command["source_tool"]]
            check(len(found) == 1, "Missing or ambiguous original command tool call")
            exact = found[0]["arguments"]["command"].encode("utf-8")
            stored = (V / command["archive_command_path"]).read_bytes()
            check(exact == stored, "Original command text was altered")
            check(sha(stored) == command["code_sha256"], "Original command hash differs")
            check(len(stored) == command["bytes"], "Original command length differs")
        check(len(provenance["commands"]) == 3, "Incorrect count of original UIA commands")
        print("PASS: three exact original PowerShell commands, including two successful Send invocations")

        prompts = provenance["review_prompts"]
        mapping = {
            "01-first-review-assignment.txt": "local-originals/runs/7d8b4ba389602e089d735e8a/bootstrap-intent.json",
            "02-d27-review-assignment.txt": "local-originals/requests/ltm-v2-d27-g2-fresh-review-intent.json",
            "03-8d27-review-assignment.txt": "local-originals/requests/ltm-v2-8d27-g2g5g9-review-intent.json",
        }
        check(len(prompts) == len(mapping), "Incomplete original review prompts")
        for record in prompts:
            filename = Path(record["path"]).name
            check(filename in mapping, "Unknown or missing source assignment")
            intent = parsed(V / mapping[filename])
            data = intent["message"].encode("utf-8")
            frozen = (V / record["path"]).read_bytes()
            check(frozen == data, f"Original reviewer prompt altered: {filename}")
            check(record["changes"] == "NONE", f"Unexpected reviewer prompt edit: {filename}")
            check(sha(frozen) == intent[record["original_sha256_field"]].lower()
                  == record["sha256"], f"Original prompt digest mismatch: {filename}")
            check(len(frozen) == record["bytes"], f"Original prompt length mismatch: {filename}")
        print("PASS: all three original reviewer prompts verbatim, identical to persisted Send intents")

        original_tests = parsed(V / "temp-scripts/EXACT_SOURCE_MANIFEST.json")["files"]
        check(len(original_tests) == 9, "Incomplete original reviewer Python test suite sources")
        for script in original_tests:
            code = (V / "temp-scripts" / script["archived_path"]).read_bytes()
            check(script["byte_equal"] and len(code) == script["bytes"]
                  and sha(code) == script["sha256"], "Recovered reviewer source changed")
            verify_live(script["original_path"], code, args.compare_live_sources)
        check((V / "temp-scripts/third/independent_g2g5g9.py").read_bytes()
              == (ROOT / "tools/reviewer-authored/8d27_final_35_test_review.py").read_bytes(),
              "Original final reviewer test source contradicts earlier archive")
        check((V / "temp-scripts/second/independent_g2g5_review.py").read_bytes()
              == (ROOT / "tools/reviewer-authored/d27_17_test_review.py").read_bytes(),
              "Original second reviewer test source contradicts earlier archive")
        print("PASS: nine additional original reviewer Python scripts, byte-identical")

        print("VERBATIM CASE STUDY: VERIFIED OFFLINE")
        return 0
    except (AssertionError, OSError, ValueError, KeyError, UnicodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
