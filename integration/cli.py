"""Windows entry point for the Astra loop.

Usage: python cli.py init --config PRIVATE.json --state PRIVATE/controller.json --initial-chat-id OBSERVED_ID
       python cli.py cycle --config PRIVATE.json --state PRIVATE/controller.json
       python cli.py run --config PRIVATE.json --state PRIVATE/controller.json
       python cli.py status --state PRIVATE/controller.json

Private config/state remain OUTSIDE Git. One controller process owns Send.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import argparse
import json
import os
import sys
import time

from runner import cycle, initialise, inspect_state
from repo_reader import GitPublishedReader
from windows_backend import WindowsUIA
from succession.core import Action, Config, Controller


@contextmanager
def exclusive_lock(state_path: Path):
    """Non-blocking lock held across observe, prepare, state and Send."""
    path = state_path.with_suffix(".lock")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as f:
        f.seek(0)
        f.write(b"X")
        f.flush()
        f.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            f.seek(0)
            if os.name == "nt":
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def load_config(path: Path) -> dict:
    cfg = json.loads(path.read_text(encoding="utf-8"))
    fields = {"project", "repo", "branch", "max_unique_chats",
              "run_id", "fixture_path", "project_name", "repo_dir_wsl"}
    if not isinstance(cfg, dict) or set(cfg) != fields:
        raise ValueError("Private run config requires exactly the documented fields")
    if cfg["repo"] != "JayDEmily/chat_successor":
        raise ValueError("This implementation is scoped to chat_successor")
    if not cfg["run_id"] or not cfg["project_name"]:
        raise ValueError("Run identity and Project name are required")
    Config(**{key: cfg[key] for key in
             ("project", "repo", "branch", "max_unique_chats")})
    return cfg


def create_dependencies(cfg: dict, state_path: Path):
    browser = WindowsUIA(
        cfg["project"], cfg["project_name"],
        Path(__file__).resolve().with_name("uia_adapter.ps1"), state_path)
    reader = GitPublishedReader(
        Path(cfg["repo_dir_wsl"]), cfg["repo"], cfg["branch"],
        cfg["fixture_path"],
        git_command=("wsl.exe", "-d", "Ubuntu", "--exec", "/usr/bin/git"))
    return browser, reader


def output(label: str, state_path: Path, *, action: str | None = None):
    data = inspect_state(state_path)
    data["event"] = label
    if action is not None:
        data["action"] = action
    print(json.dumps(data, indent=2), flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=["init", "cycle", "run", "status",
                                         "pause", "resume", "reconcile"])
    ap.add_argument("--state", required=True, type=Path)
    ap.add_argument("--config", type=Path)
    ap.add_argument("--initial-chat-id")
    ap.add_argument("--poll-seconds", type=float, default=5)
    ap.add_argument("--max-polls", type=int, default=0)
    args = ap.parse_args()
    path = args.state
    if args.command == "status":
        output("status", path)
        return
    if args.command == "pause":
        path.with_suffix(".pause").write_text("Operator pause\n", encoding="utf-8")
        output("pause_requested", path)
        return
    if args.config is None:
        ap.error("--config required for this command")
    cfg = load_config(args.config)
    config = Config(cfg["project"], cfg["repo"], cfg["branch"],
                    cfg["max_unique_chats"])
    if args.command == "init":
        if not args.initial_chat_id:
            ap.error("--initial-chat-id is required and must be observed")
        with exclusive_lock(path):
            initialise(path, config, args.initial_chat_id)
            output("initialised", path)
        return
    browser, reader = create_dependencies(cfg, path)
    if args.command == "reconcile":
        with exclusive_lock(path):
            c = Controller.load(path)
            receipt = browser.reconcile_readonly()
            p = c.state.pending
            if (receipt.posted_message_observed and
                    receipt.submitted_text == p.message and receipt.chat_id):
                decision = c.confirm(p.action_id, receipt.chat_id, receipt.project)
                c.save(path)
                output("reconciled", path, action=decision.action.value)
            else:
                output("unresolved_no_resend", path)
        return
    if args.command == "resume":
        with exclusive_lock(path):
            c = Controller.load(path)
            c.resume_after_owner()
            c.save(path)
            path.with_suffix(".pause").unlink(missing_ok=True)
            output("resumed", path)
        return

    with exclusive_lock(path):
        c = Controller.load(path)
        if c.config != config:
            raise ValueError("Persisted controller configuration does not match run")
        polls = 0
        while True:
            if path.with_suffix(".pause").exists():
                c.pause("Operator pause requested")
                c.save(path)
                output("paused", path)
                return
            act = cycle(c, browser, reader, cfg["run_id"], path)
            output("cycle", path, action=act.value)
            if args.command == "cycle" or act not in (Action.WAIT, Action.IGNORE):
                return
            polls += 1
            if args.max_polls and polls >= args.max_polls:
                return
            time.sleep(args.poll_seconds)


if __name__ == "__main__":
    main()
