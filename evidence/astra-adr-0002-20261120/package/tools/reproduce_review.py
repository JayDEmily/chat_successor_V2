#!/usr/bin/env python3
"""Reproduce this review's offline checks in fresh temporary directories.

Requires Python 3 and Git; no third-party dependencies. Executes only the supplied
offline unit suites and read-only fixture validators, plus the accompanying
characterization probes. Git transport is restricted to local files. Does not
install software, contact services, open Chrome, call MCP, or modify a repository
that existed before this command. Git bundle mirrors are processed one at a time.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tarfile
import tempfile
import time
import zipfile

BASELINE = "283e6c17bf3359c203a362fd6593563480eeea5f"
CANDIDATE = "2c29406b1c43904c5ead79064fe7856971e0aa2e"
KIT = "source/astra/2026-11-17/unpacked/chat_succession_test_kit_20261117"
SOURCE_ARCHIVE_SHA256 = "473876c6b0fffa1f55ef68ad9da62bda0e949295808f899d502edd68ab5f3945"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True,
                        help="New results directory; must not already exist")
    args = parser.parse_args()
    archive = args.archive.resolve()
    out = args.out.resolve()
    if out.exists():
        parser.error("--out must be a new directory (nothing will be overwritten)")
    if sha(archive.read_bytes()) != SOURCE_ARCHIVE_SHA256:
        parser.error("This reproducer is pinned to the supplied 20 November archive; SHA-256 differs")
    out.mkdir(parents=True)
    failures = []
    summary = {"scope": "offline-only", "reference_date": "2026-11-20",
               "archive_sha256": SOURCE_ARCHIVE_SHA256,
               "python": sys.version, "live_tests": "NOT_RUN",
               "powershell_execution": "NOT_RUN",
               "network_used": False, "mcp_used": False,
               "existing_repositories_modified": False}

    with tempfile.TemporaryDirectory(prefix="astra-review-") as temporary:
        temp = Path(temporary)
        root = temp / "input"
        root.mkdir()
        test_temp = temp / "test-tmp"
        test_temp.mkdir()
        env = os.environ.copy()
        env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1",
                    "TMPDIR": str(test_temp), "TEMP": str(test_temp), "TMP": str(test_temp),
                    "GIT_ALLOW_PROTOCOL": "file", "GIT_TERMINAL_PROMPT": "0",
                    "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
        def run(command, cwd=None, binary=False, check=True):
            cp = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                                text=not binary, timeout=180)
            if check and cp.returncode:
                raise RuntimeError(f"Command failed ({cp.returncode}): {command}\n{cp.stderr}")
            return cp
        def git(*command, **kw):
            return run(["git", *command], **kw)
        summary["git"] = git("--version").stdout.strip()

        with tarfile.open(archive, "r:gz") as tar:
            members = tar.getmembers()
            if len(members) > 500 or sum(m.size for m in members) > 64 * 1024 * 1024:
                raise ValueError("Archive exceeds this bounded review's member/size budget")
            top = {PurePosixPath(m.name).parts[0] for m in members}
            if len(top) != 1:
                raise ValueError("Expected exactly one top-level directory")
            prefix = next(iter(top))
            seen = set()
            inventory = []
            for member in members:
                p = PurePosixPath(member.name)
                if (p.is_absolute() or ".." in p.parts or member.name in seen
                    or not (member.isfile() or member.isdir())):
                    raise ValueError(f"Unsafe or duplicate member: {member.name}")
                seen.add(member.name)
                if not member.isfile():
                    continue
                rel = str(p.relative_to(prefix))
                data = tar.extractfile(member).read()
                dest = root / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
                inventory.append({"path": rel, "bytes": len(data), "sha256": sha(data)})
        write_json(out / "input-inventory.json", inventory)
        original_hashes = {item["path"]: item["sha256"] for item in inventory}
        checksums = []
        listed = set()
        for line in (root / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
            expected, rel = line.split("  ", 1)
            actual = sha((root / rel).read_bytes())
            listed.add(rel)
            checksums.append({"path": rel, "expected": expected, "actual": actual,
                              "matches": actual == expected})
        unlisted = sorted(set(original_hashes) - {"SHA256SUMS.txt"} - listed)
        integrity = {"files": len(inventory), "manifest_entries": len(checksums),
                     "mismatches": [row for row in checksums if not row["matches"]],
                     "unlisted": unlisted, "checks": checksums}
        write_json(out / "input-integrity.json", integrity)
        if integrity["mismatches"] or unlisted:
            raise ValueError("Input manifest verification failed")

        release = []
        zpath = root / "release/chat-succession-0.4.3.zip"
        with zipfile.ZipFile(zpath) as z:
            for entry in z.infolist():
                if entry.is_dir():
                    continue
                data = z.read(entry.filename)
                release.append({
                    "path": entry.filename, "sha256": sha(data),
                    "matches_source": data == (root / "source/plugins/chat-succession" / entry.filename).read_bytes()
                })
        write_json(out / "release-comparison.json",
                   {"zip_sha256": sha(zpath.read_bytes()), "files": release})
        if not all(row["matches_source"] for row in release):
            failures.append("release/source mismatch")

        suites = []
        for name, cwd, directory, expected in [
            ("integration", root / "source", "integration/tests", 63),
            ("reference", root / KIT, "tests", 119),
        ]:
            command = [sys.executable, "-B", "-X", "utf8", "-m", "unittest",
                       "discover", "-s", directory, "-v"]
            start = time.monotonic()
            cp = run(command, cwd=cwd, check=False)
            elapsed = time.monotonic() - start
            combined = cp.stdout + cp.stderr
            header = f"COMMAND: python3 -B -X utf8 -m unittest discover -s {directory} -v\n"
            header += f"CWD: INPUT/{cwd.relative_to(root)}\nRETURN CODE: {cp.returncode}\n\n"
            (out / f"{name}-tests.log").write_text(
                header + combined.replace(str(temp), "WORKSPACE"), encoding="utf-8")
            found = re.search(r"Ran (\d+) tests? in ([\d.]+)s", combined)
            count = int(found.group(1)) if found else None
            passed = cp.returncode == 0 and count == expected and "skipped=" not in combined
            suites.append({"suite": name, "returncode": cp.returncode, "tests": count,
                           "expected_tests": expected, "passed_without_skips": passed,
                           "elapsed_seconds": round(elapsed, 3)})
            if not passed:
                failures.append(f"{name} unit suite")
        write_json(out / "unit-tests.json", suites)

        fixture_validations = []
        for folder in sorted((root / "source/succession-tests").iterdir()):
            if not folder.is_dir():
                continue
            cp = run([sys.executable, "-B", str(folder / "fixture_tools.py"),
                      "verify", "--root", str(folder)], check=False)
            row = {"fixture": folder.name, "returncode": cp.returncode,
                   "result": json.loads(cp.stdout) if cp.returncode == 0 else None,
                   "stderr": cp.stderr}
            fixture_validations.append(row)
            if cp.returncode:
                failures.append(f"fixture {folder.name}")
        write_json(out / "fixture-validations.json", fixture_validations)

        probe_script = Path(__file__).resolve().with_name("review_probes.py")
        cp = run([sys.executable, "-B", str(probe_script), "--source", str(root / "source"),
                  "--json-out", str(out / "review-probes.json")], check=False)
        (out / "review-probes.log").write_text(cp.stdout + cp.stderr, encoding="utf-8")
        if cp.returncode:
            failures.append("baseline characterization probes")

        histories, details, history_logs = [], {}, []
        seeds = []
        seed_specs = {
            "chat-succession-cat-dog-pair": ("6d844f19f3a81752fe2c1bbb02caccb6f8a097f7", ["STORY.md"]),
            "chat-succession-bird-pig": ("5f43b42123c2ffdc3521285f866c31a60c2b3710", ["STORY.md"]),
            "chat-succession-trial-approval": ("b91b00fe75be2ca011eac1ad1cc0d668ffd8d8bf", ["NOTES.md"]),
            "chat-succession-trial-rotation": ("75e5d27480e5b0d01fd07d6a11efe05e52498697", ["CHECKLIST.md", "REVIEW.md"]),
        }
        bundles = [root / "history/chat_successor.bundle"]
        bundles += sorted((root / "history/fixtures").glob("*.bundle"))
        for bundle in bundles:
            # Sequential lifetime: never accumulate restored repositories.
            with tempfile.TemporaryDirectory(prefix="mirror-", dir=temp) as mirror_temp:
                mirror = Path(mirror_temp) / "repo.git"
                clone = git("clone", "--mirror", str(bundle), str(mirror))
                def mg(*command, **kw):
                    return git("-C", str(mirror), *command, **kw)
                verify = mg("bundle", "verify", str(bundle), check=False)
                fsck = mg("fsck", "--full", check=False)
                refout = mg("for-each-ref", "--format=%(objectname)\t%(refname)").stdout
                refs = dict(line.split("\t")[::-1] for line in refout.strip().splitlines())
                ref_file = (root / "history/refs.tsv" if bundle.name == "chat_successor.bundle"
                            else bundle.with_suffix(".refs.tsv"))
                expected_refs = dict(line.split("\t")[::-1] for line in
                                     ref_file.read_text(encoding="utf-8").strip().splitlines()[1:])
                count = int(mg("rev-list", "--all", "--count").stdout)
                rel = str(bundle.relative_to(root))
                row = {"bundle": rel, "bundle_verify_rc": verify.returncode,
                       "fsck_rc": fsck.returncode, "refs": len(refs), "commits": count,
                       "refs_match_supplied_tsv": refs == expected_refs,
                       "actual_refs": refs}
                history_logs.append(
                    f"### {rel}\nCLONE\n{clone.stdout}{clone.stderr}"
                    f"\nBUNDLE VERIFY rc={verify.returncode}\n{verify.stdout}{verify.stderr}"
                    f"\nFSCK rc={fsck.returncode}\n{fsck.stdout}{fsck.stderr}"
                    f"\nREFS\n{refout}\nCOMMITS={count}\n")
                if verify.returncode or fsck.returncode or refs != expected_refs:
                    failures.append(f"bundle {rel}")

                if bundle.name == "chat_successor.bundle":
                    byte_matches, newline_paths, mismatches, missing = [], [], [], []
                    for path in sorted((root / "source").rglob("*")):
                        if not path.is_file():
                            continue
                        rel_source = str(path.relative_to(root / "source"))
                        content = mg("show", f"{BASELINE}:{rel_source}", binary=True, check=False)
                        if content.returncode:
                            missing.append(rel_source)
                        elif content.stdout == path.read_bytes():
                            byte_matches.append(rel_source)
                        elif content.stdout.replace(b"\r\n", b"\n") == path.read_bytes().replace(b"\r\n", b"\n"):
                            newline_paths.append(rel_source)
                        else:
                            mismatches.append(rel_source)
                    runtime_delta = mg("diff", "--name-status", CANDIDATE, BASELINE, "--",
                                       "integration", "plugins",
                                       KIT.removeprefix("source/") + "/succession").stdout
                    comparison = {"baseline": BASELINE, "candidate": CANDIDATE,
                                  "byte_matches": len(byte_matches),
                                  "line_ending_only_matches": len(newline_paths),
                                  "line_ending_paths": newline_paths,
                                  "content_mismatches": mismatches, "missing_paths": missing,
                                  "runtime_delta_candidate_to_snapshot": runtime_delta}
                    row["source_comparison"] = comparison
                    if mismatches or missing or runtime_delta:
                        failures.append("pinned source comparison")
                    events = []
                    for run_id in ("astra-l13-20261118-a", "astra-l13-20261118-b", "astra-l13-20261119-f"):
                        record = json.loads((root / f"source/evidence/{run_id}/live_record.json").read_text())
                        for event in record["events"]:
                            commit = event["publication_commit"]
                            state = json.loads(mg("show", f"{commit}:succession-tests/{run_id}/STATE.json").stdout)
                            matches = (state["last_chat_id"] == event["saved_chat_id"]
                                       and state["completed_steps"] == event["slice"])
                            events.append({"run": run_id, "slice": event["slice"], "commit": commit,
                                           "state_last_chat_matches_record": state["last_chat_id"] == event["saved_chat_id"],
                                           "state_completed_steps": state["completed_steps"],
                                           "state_programme_complete": state["programme_complete"],
                                           "matches": matches})
                            if not matches:
                                failures.append(f"historic event {run_id}:{event['slice']}")
                    row["A_B_F_events"] = events
                else:
                    detail = {"refs": refs, "commits": [], "branch_files": {}}
                    for commit in mg("rev-list", "--all", "--reverse").stdout.splitlines():
                        detail["commits"].append({
                            "sha": commit,
                            "parents": mg("show", "-s", "--format=%P", commit).stdout.strip().split(),
                            "message": mg("show", "-s", "--format=%B", commit).stdout,
                            "changes": mg("diff-tree", "--root", "--no-commit-id", "--numstat", "-r", commit).stdout
                        })
                    for ref, commit in refs.items():
                        files = {}
                        for filename in mg("ls-tree", "-r", "--name-only", commit).stdout.splitlines():
                            if filename.endswith((".md", ".txt", ".json")):
                                files[filename] = mg("show", f"{commit}:{filename}").stdout
                        detail["branch_files"][ref] = {"commit": commit, "files": files}
                    details[bundle.stem] = detail
                    if bundle.stem in seed_specs:
                        seed_sha, forbidden = seed_specs[bundle.stem]
                        tree = mg("ls-tree", "-r", "--name-only", seed_sha).stdout.splitlines()
                        clean = not any(name in tree for name in forbidden)
                        seeds.append({"repository": bundle.stem, "seed": seed_sha,
                                      "tracked_paths": tree, "expected_absent": forbidden,
                                      "clean": clean})
                        if not clean:
                            failures.append(f"unclean seed {bundle.stem}")
                histories.append(row)
        write_json(out / "history-audit.json", histories)
        write_json(out / "fixture-history-details.json", details)
        write_json(out / "fixture-seeds.json", seeds)
        (out / "history-verification.log").write_text(
            "".join(history_logs).replace(str(temp), "WORKSPACE"), encoding="utf-8")

        # Corroborate the small fixture's terminal/partial artifacts independently.
        chains = []
        for name, detail in details.items():
            by_sha = {c["sha"]: c for c in detail["commits"]}
            for ref, branch in detail["branch_files"].items():
                tip = by_sha[branch["commit"]]
                lines = tip["message"].splitlines()
                trailers = {}
                for key in ("Chat-Succession-Run", "Chat-ID", "Chat-Succession-Next"):
                    values = [line.split(":", 1)[1].strip() for line in lines if line.startswith(key + ":")]
                    if values:
                        trailers[key] = values
                if not trailers:
                    if name == "chat-succession-trial-approval" and "shoco" in ref:
                        clean = "NOTES.md" not in branch["files"]
                        chains.append({"repo": name, "ref": ref, "tip": branch["commit"],
                                       "classification": "STAGED_NOT_RUN", "no_NOTES_file": clean})
                        if not clean:
                            failures.append("Shoco approval seed is not clean")
                    continue
                parent = by_sha.get(tip["parents"][0]) if len(tip["parents"]) == 1 else None
                run = trailers.get("Chat-Succession-Run", [None])[0]
                if name == "my-cat-and-dog":
                    turn = int(ref.split("story-")[1][:2])
                    story = branch["files"].get("STORY.md", "").splitlines()
                    valid = len(story) == turn and tip["changes"].strip() == "1\t0\tSTORY.md"
                    # Every branch must point directly to the preceding guide/turn.
                    previous_ref = ("refs/heads/main" if turn == 1 else
                                    f"refs/heads/codex/story-{turn-1:02d}-" + ("scruffy" if (turn-1) % 2 else "bluey"))
                    valid = valid and tip["parents"] == [detail["refs"][previous_ref]]
                    chains.append({"repo": name, "ref": ref, "tip": branch["commit"],
                                   "turn": turn, "chat_id": trailers.get("Chat-ID"),
                                   "one_line_only_and_expected_parent": valid})
                    if not valid:
                        failures.append(f"four-turn story {ref}")
                else:
                    # The generic two-worker chains share a run and have distinct worker IDs.
                    parent_run = re.search(r"^Chat-Succession-Run: (.+)$", parent["message"], re.M) if parent else None
                    parent_chat = re.search(r"^Chat-ID: (.+)$", parent["message"], re.M) if parent else None
                    second = bool(parent_run and parent_run.group(1).strip() == run)
                    row = {"repo": name, "ref": ref, "tip": branch["commit"],
                           "trailers": trailers, "two_receipt_chain": second,
                           "classification": "TWO_WORKERS_PUBLISHED" if second else "ONE_RECEIPT_ONLY"}
                    if second:
                        row["parent"] = parent["sha"]
                        row["distinct_chat_ids"] = bool(parent_chat and parent_chat.group(1).strip()
                                                       != trailers.get("Chat-ID", [None])[0])
                        row["tip_one_file_one_added_line"] = bool(re.fullmatch(r"1\t0\t[^\n]+\n?", tip["changes"]))
                        if not row["distinct_chat_ids"] or not row["tip_one_file_one_added_line"]:
                            failures.append(f"two-worker fixture {name}:{ref}")
                    chains.append(row)
        write_json(out / "fixture-chain-verification.json", chains)

        after = {str(p.relative_to(root)): sha(p.read_bytes())
                 for p in root.rglob("*") if p.is_file()}
        summary["input_unchanged_after_checks"] = after == original_hashes
        if after != original_hashes:
            failures.append("input changed during checks")
        summary.update({"manifest_entries_verified": len(checksums),
                        "source_files": 268, "bundles_checked": len(histories),
                        "unit_tests": suites, "fixture_validators": len(fixture_validations),
                        "characterization_probes": 9,
                        "characterization_limitations": ["P07", "P08", "P09"],
                        "failures": failures,
                        "overall_offline_status": "PASS" if not failures else "FAIL"})
        write_json(out / "summary.json", summary)
        print(json.dumps(summary, indent=2))
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
