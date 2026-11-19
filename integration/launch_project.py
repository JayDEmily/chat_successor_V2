"""Provision a private repo-neutral Windows run from an explicit phone request."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess

from cli import create_dependencies, exclusive_lock, load_config
from launch_story import launch, start_controller
from owner_reentry import owner_context, record_context, resume_request
from repo_reader import GitHandoffReader, HANDOFF_WORKFLOW, validate_github_repo
from runner import inspect_state
from windows_backend import WindowsUIA


PROJECT_URL = re.compile(r"https://chatgpt[.]com/g/(g-p-[0-9a-f]+)(?:-[A-Za-z0-9-]+)?/project/?")
RUN_ID = re.compile(r"[a-z0-9]{24}")
WSL = ("wsl.exe", "-d", "Ubuntu", "--exec")
GIT = (*WSL, "/usr/bin/git")


def read_request(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    required = {"repo", "project_name"}
    optional = {"branch", "project_url", "max_unique_chats", "operation", "run_id",
                "job_id", "owner_context", "release_pause"}
    if not isinstance(data, dict) or not required <= data.keys() <= required | optional:
        raise ValueError("Request needs the GitHub repository and Project name")
    validate_github_repo(data["repo"])
    operation = data.setdefault("operation", "start")
    if operation not in ("inspect", "start", "resume", "new"):
        raise ValueError("Unknown entry operation")
    if "branch" in data or operation in ("start", "new"):
        if not isinstance(data.get("branch"), str):
            raise ValueError("Use the published work branch")
        GitHandoffReader(Path("."), data["repo"], data["branch"])
    for key in ("run_id", "job_id"):
        if key in data and (not isinstance(data[key], str) or not RUN_ID.fullmatch(data[key])):
            raise ValueError(f"Invalid {key}")
    if operation == "new" and "job_id" not in data:
        raise ValueError("An explicit new job needs a stable job ID")
    if type(data.get("release_pause", False)) is not bool:
        raise ValueError("release_pause must be boolean")
    if "owner_context" in data:
        data["owner_context"] = owner_context(data["owner_context"], anchored=operation == "resume")
    name = data["project_name"]
    if (not isinstance(name, str) or not name.strip() or len(name) > 160
            or any(ord(c) < 32 for c in name)):
        raise ValueError("Use the exact displayed Project name")
    data["project_name"] = name.strip()
    cap = data.get("max_unique_chats", 5)
    if type(cap) is not int or cap < 1:
        raise ValueError("The chat cap must be a positive integer")
    if "project_url" in data:
        url = data["project_url"]
        if not isinstance(url, str) or not PROJECT_URL.fullmatch(url):
            raise ValueError("Use the verified ChatGPT Project landing URL")
        data["project_url"] = url.rstrip("/")
    return data


def wsl(*args: str) -> str:
    result = subprocess.run(
        [*WSL, *args], capture_output=True, text=True, encoding="utf-8", timeout=45, check=True,
    )
    return result.stdout.strip()


def provision_reader(repo: str, branch: str, run_id: str) -> str:
    home = PurePosixPath(wsl("/usr/bin/printenv", "HOME"))
    if not home.is_absolute():
        raise RuntimeError("The Ubuntu home directory was not resolved")
    path = str(home / ".local/share/chat-succession" / run_id / "repo.git")
    wsl("/usr/bin/mkdir", "-p", path)
    wsl("/usr/bin/git", "-C", path, "init", "--bare", "--quiet")
    wsl("/usr/bin/git", "-C", path, "config", "remote.origin.url", f"https://github.com/{repo}.git")
    reader = GitHandoffReader(Path(path), repo, branch, git_command=GIT)
    reader.published_tip(shallow=True)
    return path


def resolve_project(request: dict, state_path: Path) -> tuple[str, str, str]:
    if "project_url" in request:
        url = request["project_url"]
        match = PROJECT_URL.fullmatch(url)
        return match[1], request["project_name"], url
    browser = WindowsUIA("", request["project_name"], Path(__file__).with_name("uia_adapter.ps1"), state_path)
    resolved = browser._invoke("ResolveProject")
    url = resolved.get("project_url", "")
    match = PROJECT_URL.fullmatch(url)
    name = resolved.get("project_name")
    if (not match or resolved.get("project") != match[1] or not isinstance(name, str)
            or name.casefold() != request["project_name"].casefold()):
        raise RuntimeError("The desktop could not verify the exact Project landing page")
    return match[1], name, url


def matching_runs(runs, project, repo):
    matches = {}
    for path in sorted(runs.glob("*/config.json")):
        cfg = load_config(path)
        if cfg["project"] != project or cfg["repo"].casefold() != repo:
            continue
        if cfg["run_id"] != path.parent.name or cfg.get("workflow") != HANDOFF_WORKFLOW:
            raise RuntimeError("Saved run configuration is inconsistent")
        state = path.with_name("controller.json")
        stage = "registered" if state.exists() else (
            "initial_send_pending" if path.with_name("bootstrap-intent.json").exists() else "configured"
        )
        summary = inspect_state(state) if stage == "registered" else {
            "halted": "Initial Send requires reconciliation" if stage == "initial_send_pending" else None,
            "project": project, "repo": cfg["repo"], "branch": cfg["branch"],
            "initial_branch": cfg["branch"], "max_unique_chats": cfg["max_unique_chats"],
        }
        if any(summary[k] != cfg[v] for k, v in (("project", "project"), ("repo", "repo"),
                                               ("initial_branch", "branch"), ("max_unique_chats", "max_unique_chats"))):
            raise RuntimeError("Saved controller does not match its private configuration")
        matches[cfg["run_id"]] = (path, {**summary, "run_id": cfg["run_id"], "run_stage": stage})
    return matches


def launch_request(path: Path, base: Path, *, check_only: bool = False) -> dict:
    request = read_request(path)
    project, name, url = resolve_project(request, base / "controller.json")
    identity = project, request["repo"].casefold()
    key = hashlib.sha256(json.dumps(identity).encode()).hexdigest()[:24]
    operation = request["operation"]
    context = request.get("owner_context")
    terminal = ("programme_finished", "chat_cap")
    runs = base / "Runs"
    with exclusive_lock(base / "Locks" / f"{key}.json"):
        matches = matching_runs(runs, *identity)
        active = {ident: item for ident, item in matches.items() if item[1]["halted"] not in terminal}
        run_id = request.get("run_id")
        new_id = hashlib.sha256(f"{key}:{request['job_id']}".encode()).hexdigest()[:24] if operation == "new" else None
        if new_id in matches:
            return {**matches[new_id][1], "event": "existing_run"}
        if run_id is not None and run_id not in matches:
            raise RuntimeError("The nominated run does not match this Project and repository")
        candidates = active or matches
        if run_id is None and len(candidates) == 1:
            run_id = next(iter(candidates))
        if run_id is None and candidates:
            return {"event": "selection_required", "runs": [item[1] for item in candidates.values()]}
        if operation == "inspect":
            return {**matches[run_id][1], "event": "inspected"} if run_id else {"event": "no_run"}
        if operation == "resume" and run_id is None:
            raise RuntimeError("No existing run matches the approval")
        if operation == "new" and active:
            raise RuntimeError("An existing nonterminal run owns this Project and repository")
        if run_id and operation != "new":
            cfg_path, summary = matches[run_id]
            state_path = cfg_path.with_name("controller.json")
            if request.get("max_unique_chats", summary["max_unique_chats"]) != summary["max_unique_chats"]:
                raise RuntimeError("The existing run has a different chat cap")
            if state_path.exists() and operation == "resume" and not check_only:
                return resume_request(cfg_path, state_path, request, name, create_dependencies, start_controller)
            if state_path.exists() and not check_only:
                return {**summary, "event": "existing_run"}
            intent_path = cfg_path.with_name("bootstrap-intent.json")
            if context and intent_path.exists():
                intent = json.loads(intent_path.read_text(encoding="utf-8"))
                if f"/owner-{context['request_id']}.json." not in intent["message"]:
                    raise RuntimeError("Reconcile the existing initial Send before delivering new owner input")
        else:
            run_id = new_id or key
            branch = request["branch"]
            checkout = provision_reader(request["repo"], branch, run_id)
            cfg_path = runs / run_id / "config.json"
            cfg_path.parent.mkdir(parents=True, exist_ok=True)
            cfg = {"project": project, "project_name": name, "project_url": url,
                   "repo": request["repo"], "branch": branch, "repo_dir_wsl": checkout,
                   "run_id": run_id, "max_unique_chats": request.get("max_unique_chats", 5),
                   "workflow": HANDOFF_WORKFLOW}
            pending = cfg_path.with_suffix(".tmp")
            pending.write_text(json.dumps(cfg), encoding="utf-8")
            pending.replace(cfg_path)
        state_path = cfg_path.with_name("controller.json")
        if operation == "resume" and not state_path.with_name("bootstrap-intent.json").exists():
            raise RuntimeError("No initialized worker exists to resume")
        kwargs = {}
        if context and not check_only:
            kwargs["owner_request_id"] = record_context(state_path, context)
        result = launch(cfg_path, state_path, check_only=check_only, **kwargs)
        return {**result, "run_id": run_id}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    base = Path(os.environ["LOCALAPPDATA"]) / "ChatSuccession"
    try:
        print(json.dumps(launch_request(args.request, base, check_only=args.check)))
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps({"event": "launch_held", "reason": str(exc)}))
        raise SystemExit(1)
