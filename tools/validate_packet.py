"""Read-only validation of a pinned, finite Chat Succession toy assignment.

This validator does not execute task instructions, access Chrome, send messages,
reserve launches or mutate Git. The caller must fetch the run branch immediately
before validation. A successful check is not evidence of browser delivery.
"""
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
_SHA = re.compile(r"^[0-9a-f]{40}$")
_ROLES = {1: "worker", 2: "reviewer", 3: "auditor"}
_TASKS = {1: "toy-calculate", 2: "toy-independent-review", 3: "toy-terminal-audit"}
_OUTPUTS = {1: "toy.json", 2: "review.json", 3: "summary.json"}


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: tuple[str, ...]
    assignment_sha: str


class PacketError(ValueError):
    pass


def _git(root: Path, *args: str) -> str:
    p = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, check=False
    )
    if p.returncode:
        raise PacketError(f"git {' '.join(args[:2])} rejected: {p.stderr.strip()}")
    return p.stdout.strip()


def _read_json(root: Path, sha: str, path: str) -> dict:
    raw = _git(root, "show", f"{sha}:{path}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise PacketError(f"invalid JSON at {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise PacketError(f"object required at {path}")
    return data


def _one_parent(root: Path, child: str, expected_parent: str, label: str) -> None:
    parents = _git(root, "rev-list", "--parents", "-n", "1", child).split()
    if len(parents) != 2 or parents[1] != expected_parent:
        raise PacketError(f"{label}: commit must have exactly the expected parent")


def _file_changes(root: Path, sha: str) -> set[str]:
    output = _git(root, "diff-tree", "--no-commit-id", "--name-only", "-r", sha)
    return set(output.splitlines()) if output else set()


def _require_ident(data: dict, run_id: str, step: int, where: str) -> None:
    if data.get("schema_version") != 1 or data.get("run_id") != run_id:
        raise PacketError(f"{where}: wrong schema or run ID")
    if data.get("step") != step:
        raise PacketError(f"{where}: wrong step")


def validate_packet(
    repo_dir: str | Path, run_id: str, step: int, assignment_sha: str
) -> ValidationResult:
    """Inspect immutable Git objects and serial lineage; never trigger a launch."""
    try:
        root = Path(repo_dir)
        if not _ID.fullmatch(run_id):
            raise PacketError("invalid run ID")
        if step not in _ROLES:
            raise PacketError("step outside fixed 1..3 budget")
        if not isinstance(assignment_sha, str) or not _SHA.fullmatch(assignment_sha):
            raise PacketError("assignment SHA must be full lowercase commit SHA")

        base = f"runs/{run_id}"
        run = _read_json(root, assignment_sha, f"{base}/run.json")
        if run.get("schema_version") != 1 or run.get("run_id") != run_id:
            raise PacketError("run contract mismatch")
        branch = f"trial/{run_id}"
        if run.get("branch") != branch or run.get("max_steps") != 3:
            raise PacketError("run branch or budget mismatch")
        if run.get("launch_mode") != "worker":
            raise PacketError("not the selected worker-launch approach")
        if run.get("stop_state") not in ("prepared", "active"):
            raise PacketError("run is held, stopped or complete")
        if step > 1 and run.get("stop_state") != "active":
            raise PacketError("successor launch requires an admitted active run")
        if not isinstance(run.get("project_config_ref"), str) or not run["project_config_ref"].startswith("local:"):
            raise PacketError("missing private Project config reference")

        head = _git(root, "rev-parse", "--verify", f"refs/heads/{branch}")
        if head != assignment_sha:
            raise PacketError("conflicting local run branch head")
        remote = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=root, capture_output=True, text=True, check=False
        )
        if remote.returncode == 0 and remote.stdout.strip():
            # Caller must fetch immediately before invoking this offline validator.
            remote_head = _git(root, "rev-parse", "--verify",
                               f"refs/remotes/origin/{branch}")
            if remote_head != assignment_sha:
                raise PacketError("conflicting or unfetched origin run branch head")

        assignment_path = f"{base}/steps/{step:03d}/assignment.json"
        assignment = _read_json(root, assignment_sha, assignment_path)
        _require_ident(assignment, run_id, step, "assignment")
        if assignment.get("role") != _ROLES[step]:
            raise PacketError("wrong role for fixed toy step")
        if assignment.get("task_id") != _TASKS[step]:
            raise PacketError("wrong task ID")
        if assignment.get("terminal") is not (step == 3):
            raise PacketError("terminal flag contradicts step budget")

        required = {
            f"{base}/steps/{step:03d}/{_OUTPUTS[step]}",
            f"{base}/steps/{step:03d}/result.json",
        }
        if (
            not isinstance(assignment.get("allowed_paths"), list)
            or set(assignment["allowed_paths"]) != required
            or len(assignment["allowed_paths"]) != len(required)
            or not isinstance(assignment.get("required_output_paths"), list)
            or set(assignment["required_output_paths"]) != required
            or len(assignment["required_output_paths"]) != len(required)
        ):
            raise PacketError("assigned output/scope paths do not match fixed toy contract")

        prev_sha = assignment.get("predecessor_result_commit")
        if step == 1:
            if prev_sha is not None:
                raise PacketError("first step must have no predecessor")
            return ValidationResult(True, (), assignment_sha)

        if not isinstance(prev_sha, str) or not _SHA.fullmatch(prev_sha):
            raise PacketError("missing or invalid predecessor result commit")
        prev_step = step - 1
        prev_base = f"{base}/steps/{prev_step:03d}"
        previous = _read_json(root, prev_sha, f"{prev_base}/result.json")
        _require_ident(previous, run_id, prev_step, "predecessor result")
        if previous.get("status") != "completed":
            raise PacketError("predecessor is blocked, failed or unfinished")
        if not isinstance(previous.get("checks"), list) or not previous["checks"]:
            raise PacketError("predecessor has no recorded checks")
        if previous.get("unresolved_issues") != []:
            raise PacketError("predecessor has unresolved issues")

        prev_assignment_sha = previous.get("assignment_commit")
        if not isinstance(prev_assignment_sha, str) or not _SHA.fullmatch(prev_assignment_sha):
            raise PacketError("predecessor missing pinned assignment commit")
        _one_parent(root, prev_sha, prev_assignment_sha, "predecessor result")
        _one_parent(root, assignment_sha, prev_sha, "next assignment")
        prev_assignment = _read_json(root, prev_assignment_sha,
                                     f"{prev_base}/assignment.json")
        _require_ident(prev_assignment, run_id, prev_step, "previous assignment")
        if prev_assignment.get("role") != _ROLES[prev_step]:
            raise PacketError("wrong predecessor role")
        if prev_assignment.get("task_id") != _TASKS[prev_step]:
            raise PacketError("wrong predecessor task")
        prev_allowed = prev_assignment.get("allowed_paths")
        prev_required = prev_assignment.get("required_output_paths")
        expected_previous = {
            f"{prev_base}/{_OUTPUTS[prev_step]}",
            f"{prev_base}/result.json",
        }
        actual_changes = _file_changes(root, prev_sha)
        if (
            not isinstance(prev_allowed, list)
            or not isinstance(prev_required, list)
            or set(prev_allowed) != expected_previous
            or len(prev_allowed) != len(expected_previous)
            or set(prev_required) != expected_previous
            or len(prev_required) != len(expected_previous)
            or not isinstance(previous.get("changed_paths"), list)
            or len(set(previous["changed_paths"])) != len(previous["changed_paths"])
            or set(previous["changed_paths"]) != actual_changes
            or not actual_changes.issubset(set(prev_allowed))
            or not set(prev_required).issubset(actual_changes)
        ):
            raise PacketError("predecessor result changed paths violate assigned scope")

        expected_assignment_changes = {
            f"{prev_base}/handover.json", assignment_path
        }
        if _file_changes(root, assignment_sha) != expected_assignment_changes:
            raise PacketError("next-assignment commit changes files outside handover and assignment")
        handover = _read_json(root, assignment_sha, f"{prev_base}/handover.json")
        _require_ident(handover, run_id, prev_step, "handover")
        if (
            handover.get("result_commit") != prev_sha
            or handover.get("next_step") != step
            or handover.get("next_assignment_path") != assignment_path
            or handover.get("terminal") is not False
        ):
            raise PacketError("handover does not bind the exact predecessor and assignment")

        if prev_step == 2:
            review = _read_json(root, prev_sha, f"{prev_base}/review.json")
            if review.get("verdict") != "ACCEPT" or review.get("recomputed_value") != 410:
                raise PacketError("independent reviewer did not ACCEPT the toy value")

        return ValidationResult(True, (), assignment_sha)
    except (PacketError, OSError, TypeError, ValueError) as exc:
        return ValidationResult(False, (str(exc),), assignment_sha)

if __name__ == "__main__":
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(description="Validate a pinned Chat Succession assignment")
    parser.add_argument("--repo-dir", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--step", required=True, type=int)
    parser.add_argument("--assignment-sha", required=True)
    args = parser.parse_args()
    outcome = validate_packet(
        args.repo_dir, args.run_id, args.step, args.assignment_sha
    )
    print(json.dumps({"ok": outcome.ok, "errors": outcome.errors,
                      "assignment_sha": outcome.assignment_sha}))
    sys.exit(0 if outcome.ok else 4)
