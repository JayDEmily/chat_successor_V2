#!/usr/bin/env python3
"""Offline, read-only verification of a frozen engineering case study.

Default mode hashes archived files, checks the provenance and inspects GitHub
evidence already frozen to disk. --replay-independent extracts only the public
V2 source into a temporary directory and runs the recovered synthetic SQLite
review suite. It does NOT send messages, contact APIs or operate live systems.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parent.parent
FINAL_HEAD = "8d27bd55d4abf0c5f864b60a33f24d666920a130"
PARENT = "d27acd1ab6d06031ffc773c855907cfd8362027a"
BASE = "0aa4b8042fc60991aa8a7d9d2278314b52efa24d"
MERGE = "aa2fdf3ad5371dcb086ba4f14f3256bbaa64b017"
ORIGINAL_REVIEW_SCRIPT_SHA = "182c031080671e3ef13b5cb7460d91206fb209244b036272548d834b43db899d"
INSTALLED_WRAPPER_SHA = "3869731a405807b2833e5670f9a883b328bc0a6ca5d651fa386c2f63e60b93fb"


class CaseStudyError(Exception):
    pass


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise CaseStudyError(reason)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def checksum_manifest() -> None:
    manifest = ROOT / "SHA256SUMS"
    require(manifest.is_file(), "Missing frozen SHA256SUMS")
    expected: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        require("  " in line, "Malformed SHA256SUMS entry")
        sha, relative = line.split("  ", 1)
        require(re.fullmatch(r"[0-9a-f]{64}", sha) is not None, "Invalid manifest digest")
        candidate = (ROOT / relative).resolve()
        require(candidate.is_relative_to(ROOT.resolve()), "Manifest path escapes archive root")
        require(candidate.is_file(), f"Missing case-study file: {relative}")
        require(relative not in expected, f"Duplicate manifest path: {relative}")
        require(digest(candidate) == sha, f"SHA256 mismatch: {relative}")
        expected[relative] = sha

    actual = {
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*")
        if p.is_file() and p.name != "SHA256SUMS"
    }
    require(set(expected) == actual, f"Unlisted or stale files: {sorted(actual ^ set(expected))}")
    require(len(expected) >= 26, "Unexpectedly incomplete case-study manifest")
    print(f"PASS: {len(expected)} exact SHA256 file entries, no omitted files")


def archive_members(filename: str, prefix: str, minimum: int) -> tuple[tarfile.TarFile, dict]:
    path = ROOT / "artifacts" / filename
    obj = tarfile.open(path, mode="r:gz")
    entries = {m.name: m for m in obj.getmembers()}
    require(len(entries) >= minimum, f"Incomplete source archive {filename}: {len(entries)} entries")
    for name, member in entries.items():
        path_parts = Path(name).parts
        require(not Path(name).is_absolute(), f"Absolute archive path: {name}")
        require(".." not in path_parts, f"Archive traversal path: {name}")
        require(name == prefix.rstrip("/") or name.startswith(prefix), f"Wrong archive prefix: {name}")
        require(member.isfile() or member.isdir(), f"Unexpected special tar member: {name}")
    return obj, entries


def tar_bytes(tf: tarfile.TarFile, entries: dict, relative: str) -> bytes:
    require(relative in entries, f"Missing archived source: {relative}")
    stream = tf.extractfile(entries[relative])
    require(stream is not None, f"Non-file source: {relative}")
    with stream:
        return stream.read()


def check_code_archives() -> None:
    base, base_entries = archive_members(
        "ltm-rag-v2-baseline-0aa4b80.tar.gz", "ltm-rag-v2-baseline/", 400
    )
    final, final_entries = archive_members(
        "ltm-rag-v2-reviewed-8d27bd5.tar.gz", "ltm-rag-v2-reviewed/", 400
    )
    automation, automation_entries = archive_members(
        "chat-successor-automation-source-5c86ad6.tar.gz", "chat-successor-installed-5c86/", 120
    )
    try:
        for label, tf, entries, prefix in [
            ("baseline", base, base_entries, "ltm-rag-v2-baseline/"),
            ("final-pass", final, final_entries, "ltm-rag-v2-reviewed/"),
        ]:
            for relative, stem in [
                ("vnext/ltm_vnext/capture_foundation_v.py", "capture_foundation_v.py"),
                ("vnext/tests/test_capture_foundation_v.py", "test_capture_foundation_v.py"),
            ]:
                expected = (ROOT / "artifacts" / "snapshots" / label / stem).read_bytes()
                actual = tar_bytes(tf, entries, prefix + relative)
                require(actual == expected, f"Snapshot/tree disagreement: {label}/{stem}")
        for rel, expected in [
            ("integration/launch_story.py", "5399ae30a66a9e750438a008305f9490d15ed660c26fdd220e287a62ce6376e2"),
            ("integration/runner.py", "bc9c631c24cb137e3c91a569170c987383086a10e71d1233dce22f03d613bc8f"),
            ("integration/uia_adapter.ps1", "9de21cdaed2889028a0c64b537fd91e67124c18d892ec00b17425b4a42155c10"),
            ("integration/repo_reader.py", "3b455753f5dbfcfd20c8b1effe7a93ccc067ff89bdecf18d34505c2cea72fab8"),
        ]:
            b = tar_bytes(automation, automation_entries, "chat-successor-installed-5c86/" + rel)
            require(hashlib.sha256(b).hexdigest() == expected, f"Wrong installed automation source: {rel}")
    finally:
        base.close()
        final.close()
        automation.close()

    # Git archives contain canonical LF bytes. The executed Windows working
    # tree was an autocrlf checkout, so preserve and verify the actual CRLF
    # runtime bytes separately rather than treating their hashes as Git blobs.
    runtime_archive = ROOT / "artifacts" / "automation" / "installed-windows-runtime-bytes-5c86ad6.tar.gz"
    with tarfile.open(runtime_archive, "r:gz") as runtime:
        for relative, expected_sha in [
            ("integration/launch_story.py", "f4a00a41fd513032856b75e123e37428fc1d3ccc5d2f3d4ea0f9a144ae940725"),
            ("integration/runner.py", "172356c301614bb51b7d7cbf1f9dfa474ef09440224b59080baf889b5c6c7c0f"),
            ("integration/uia_adapter.ps1", "412ddf7f3f29dc947b6da6fbf7b9a10ae19bf0012e4d17cd13f39ad0c5194580"),
            ("integration/repo_reader.py", "55b13d001b4d1a98b3981546004c82fc4effbadc6fde61ad9038f08c1bf9e07b"),
            ("installed-start-project.cmd", INSTALLED_WRAPPER_SHA),
        ]:
            member = runtime.extractfile("installed-windows-runtime/" + relative)
            require(member is not None, f"Missing real installed runtime bytes: {relative}")
            with member:
                actual_bytes = member.read()
            require(hashlib.sha256(actual_bytes).hexdigest() == expected_sha,
                    f"Installed Windows runtime bytes changed: {relative}")

    wrapper = ROOT / "artifacts" / "automation" / "installed-start-project.cmd"
    require(digest(wrapper) == INSTALLED_WRAPPER_SHA, "Installed launcher wrapper mismatch")
    require(digest(ROOT / "tools" / "reviewer-authored" / "8d27_final_35_test_review.py")
            == ORIGINAL_REVIEW_SCRIPT_SHA, "Recovered reviewer fault suite mismatch")
    print("PASS: public baseline/final archives, frozen source snapshots, installed private automation and wrapper")


def check_review_and_ci_evidence() -> None:
    issue = load("evidence/issue-1-full.json")
    comments = {c["id"]: c.get("body", "") for c in issue["comments"]}
    require(7061870012 in comments and "RETURN_TO_WORKER" in comments[7061870012],
            "Missing second independent failure record")
    require(7061961835 in comments, "Missing final independent PASS record")
    passed = comments[7061961835]
    for required in ("PASS", FINAL_HEAD, "35/35", "285/285"):
        require(required in passed, f"Independent reviewer record missing {required}")

    pr = load("evidence/pr-2-final-state.json")["pr"]
    require(pr["head_sha"] == FINAL_HEAD, "PR changed head")
    require(pr["base_sha"] == BASE, "PR changed base")
    require(pr["number"] == 2 and pr["state"] == "open" and not pr["merged"],
            "Frozen PR state inconsistent with checkpoint")

    status = load("evidence/actions-workflow-44899629182-status.json")
    runs = [r for r in status["runs"] if r.get("id") == 44899629182]
    require(len(runs) == 1 and runs[0]["status"] == "completed"
            and runs[0]["conclusion"] == "success", "Hosted workflow did not finish successfully")
    jobs = load("evidence/actions-run-44899629182-jobs.json")["jobs"]
    checked = [job for job in jobs if job.get("id") == 136832604143]
    require(len(checked) == 1 and checked[0]["conclusion"] == "success", "Hosted CI job not successful")
    require(all(step.get("conclusion") == "success" for step in checked[0]["steps"]),
            "Not all hosted job steps succeeded")
    log = (ROOT / "evidence" / "ci-job-136832604143-full.log").read_text(
        encoding="utf-8", errors="replace"
    )
    for required in (
        f"HEAD is now at {MERGE[:7]}",
        "Merge 8d27bd55d4abf0c5f864b60a33f24d666920a130 into 0aa4b8042fc60991aa8a7d9d2278314b52efa24d",
        "Base modules: 25", "Additional Stage W tests: 13", "Ran 285 tests", "Governance links",
    ):
        require(required in log, f"Frozen hosted log does not substantiate {required}")

    prompts = load("prompts/INDEX.json")["assignments"]
    require(len(prompts) == 3, "Expected exactly three reviewer assignments")
    for entry in prompts:
        require(re.fullmatch(r"[0-9a-f]{64}", entry["message_sha256_utf8"]) is not None,
                "Missing exact reviewer prompt hash")
    for f in (ROOT / "prompts").glob("0*.json"):
        record = json.loads(f.read_text(encoding="utf-8"))
        require("exact_reviewer_prompt" not in record and "message" not in record,
                "Account message text must not be in the frozen Git archive")
    require(not (ROOT / "account_routes.json").exists(), "Account routes must never be archived")
    print("PASS: independent review verdicts, PR, hosted merge-ref CI, prompt hashes and privacy boundary")


def replay_independent() -> None:
    script = (ROOT / "tools" / "reviewer-authored" / "8d27_final_35_test_review.py")
    original = script.read_text(encoding="utf-8")
    marker = 'ROOT = Path("/tmp/ltm-independent-8d27-WTfufe/repo")'
    require(original.count(marker) == 1, "Unexpected reviewer-authored script ROOT expression")
    with tempfile.TemporaryDirectory(prefix="ltm-v2-frozen-case-review-") as tmp:
        tmpdir = Path(tmp)
        with tarfile.open(ROOT / "artifacts" / "ltm-rag-v2-reviewed-8d27bd5.tar.gz", "r:gz") as tf:
            tf.extractall(path=tmpdir, filter="data")
        extracted = tmpdir / "ltm-rag-v2-reviewed"
        temp_script = tmpdir / "reviewer_exact_source_retargeted_copy.py"
        temp_script.write_text(
            original.replace(marker, f"ROOT = Path({str(extracted)!r})"),
            encoding="utf-8",
        )
        env = dict(os.environ)
        env["PYTHONWARNINGS"] = "ignore::ResourceWarning"
        run = subprocess.run(
            [sys.executable, str(temp_script), "-q"],
            capture_output=True, text=True, timeout=45, env=env,
            check=False,
        )
        summary = run.stdout + "\n" + run.stderr
        require(run.returncode == 0 and "Ran 35 tests" in summary
                and re.search(r"^OK$", summary, re.MULTILINE) is not None,
                f"Independent synthetic replay failed: {summary[-1500:]}")
    print("PASS: original reviewer-authored 35/35 synthetic fault suite replayed on frozen final V2 code")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay-independent", action="store_true",
                        help="Run original 35-case synthetic reviewer suite against extracted source")
    args = parser.parse_args()
    try:
        checksum_manifest()
        check_code_archives()
        check_review_and_ci_evidence()
        if args.replay_independent:
            replay_independent()
    except (CaseStudyError, OSError, ValueError, tarfile.TarError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("CASE STUDY: VERIFIED OFFLINE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
