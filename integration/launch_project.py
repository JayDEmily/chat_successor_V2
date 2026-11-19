"""Provision a private repo-neutral Windows run from an explicit phone request."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess

from cli import exclusive_lock, load_config
from launch_story import launch
from repo_reader import GitHandoffReader, HANDOFF_WORKFLOW, validate_github_repo
from windows_backend import WindowsUIA


PROJECT_URL = re.compile(r"https://chatgpt[.]com/g/(g-p-[0-9a-f]+)(?:-[A-Za-z0-9-]+)?/project/?")
WSL = ("wsl.exe", "-d", "Ubuntu", "--exec")
GIT = (*WSL, "/usr/bin/git")


def read_request(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    required = {"repo", "branch", "project_name"}
    if not isinstance(data, dict) or not required <= data.keys() <= required | {"project_url", "max_unique_chats"}:
        raise ValueError("Request needs the GitHub repository, work branch and Project name")
    validate_github_repo(data["repo"])
    if not isinstance(data["branch"], str):
        raise ValueError("Use the published work branch")
    GitHandoffReader(Path("."), data["repo"], data["branch"])
    name = data["project_name"]
    if (not isinstance(name, str) or not name.strip() or len(name) > 160
            or any(ord(c) < 32 for c in name)):
        raise ValueError("Use the exact displayed Project name")
    data["project_name"] = name.strip()
    cap = data.get("max_unique_chats", 5)
    if type(cap) is not int or cap < 1:
        raise ValueError("The chat cap must be a positive integer")
    data["max_unique_chats"] = cap
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


def launch_request(path: Path, base: Path, *, check_only: bool = False) -> dict:
    request = read_request(path)
    key = (request["repo"].casefold(), request["branch"], request["project_name"].casefold())
    run_id = hashlib.sha256(json.dumps(key).encode()).hexdigest()[:24]
    folder = base / "Runs" / run_id
    state_path = folder / "controller.json"
    config_path = folder / "config.json"
    with exclusive_lock(folder / "provision.json"):
        if config_path.exists():
            cfg = load_config(config_path)
            if (cfg["repo"].casefold() != key[0] or cfg["branch"] != key[1]
                    or cfg["project_name"].casefold() != key[2]
                    or cfg["run_id"] != run_id
                    or cfg["max_unique_chats"] != request["max_unique_chats"]
                    or request.get("project_url", cfg["project_url"]) != cfg["project_url"]):
                raise RuntimeError("The existing run has a different Project URL or chat cap")
        else:
            checkout = provision_reader(request["repo"], request["branch"], run_id)
            project, name, url = resolve_project(request, state_path)
            cfg = {
                "project": project, "project_name": name, "project_url": url,
                "repo": request["repo"], "branch": request["branch"], "repo_dir_wsl": checkout,
                "run_id": run_id, "max_unique_chats": request["max_unique_chats"],
                "workflow": HANDOFF_WORKFLOW,
            }
            pending = config_path.with_suffix(".tmp")
            pending.write_text(json.dumps(cfg), encoding="utf-8")
            pending.replace(config_path)
        return launch(config_path, state_path, check_only=check_only)


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
