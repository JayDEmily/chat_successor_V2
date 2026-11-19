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
import logging
import os
import sys
import time

from runner import cycle, initialise, inspect_state
from repo_reader import (
    GitHandoffReader, GitPublishedReader, GitStoryReader, HANDOFF_WORKFLOW, STORY_REPO, STORY_TURNS,
    validate_github_repo,
)
from windows_backend import WindowsUIA
from succession.core import Action, Config, Controller


DEFAULT_POLL_SECONDS = 20


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
              "run_id", "project_name", "repo_dir_wsl"}
    optional = {"poll_seconds", "response_wait_minutes", "fixture_path", "project_url", "workflow"}
    if not isinstance(cfg, dict) or not fields <= cfg.keys() <= fields | optional:
        raise ValueError("Private run config requires the documented fields")
    poll_seconds = cfg.get("poll_seconds", DEFAULT_POLL_SECONDS)
    if type(poll_seconds) not in (int, float) or not 0 < poll_seconds < float("inf"):
        raise ValueError("poll_seconds must be a positive finite number")
    wait_minutes = cfg.get("response_wait_minutes")
    if wait_minutes is not None and (
            type(wait_minutes) not in (int, float) or not 0 < wait_minutes < float("inf") / 60):
        raise ValueError("response_wait_minutes must be a positive number or null")
    if cfg.get("workflow") == HANDOFF_WORKFLOW:
        validate_github_repo(cfg["repo"])
        if not cfg.get("project_url") or "fixture_path" in cfg:
            raise ValueError("A generic handoff needs a verified Project URL")
    elif "workflow" in cfg:
        raise ValueError("Unknown workload kind")
    elif cfg["repo"] == STORY_REPO:
        if (cfg["branch"] != "main" or cfg["max_unique_chats"] != len(STORY_TURNS)
                or not cfg.get("project_url") or "fixture_path" in cfg):
            raise ValueError("The four-turn story needs main and its verified Project URL")
    elif cfg["repo"] != "JayDEmily/chat_successor" or not cfg.get("fixture_path"):
        raise ValueError("The controller requires a supported workload and published-state reader")
    if not cfg["run_id"] or not cfg["project_name"]:
        raise ValueError("Run identity and Project name are required")
    Config(**{key: cfg[key] for key in
             ("project", "repo", "branch", "max_unique_chats")})
    return cfg


def create_dependencies(cfg: dict, state_path: Path):
    browser = WindowsUIA(
        cfg["project"], cfg["project_name"],
        Path(__file__).resolve().with_name("uia_adapter.ps1"), state_path,
        project_url=cfg.get("project_url"))
    checkout = Path(cfg["repo_dir_wsl"])
    git_command = ("wsl.exe", "-d", "Ubuntu", "--exec", "/usr/bin/git")
    if cfg.get("workflow") == HANDOFF_WORKFLOW:
        reader = GitHandoffReader(checkout, cfg["repo"], cfg["branch"], git_command=git_command)
    elif cfg["repo"] == STORY_REPO:
        reader = GitStoryReader(checkout, git_command=git_command)
    else:
        reader = GitPublishedReader(checkout, cfg["repo"], cfg["branch"], cfg["fixture_path"],
                                    git_command=git_command)
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
    ap.add_argument("--poll-seconds", type=float,
                    help="Override the private config poll interval for this invocation")
    ap.add_argument("--max-polls", type=int, default=0)
    ap.add_argument("--prepare-only", action="store_true",
                    help="L06: persist the observed prepared handover without Send (cycle only)")
    ap.add_argument("--ready-file", type=Path, help=argparse.SUPPRESS)
    args = ap.parse_args()
    if args.prepare_only and args.command != "cycle":
        ap.error("--prepare-only is valid only with cycle")
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
    if cfg.get("workflow") == HANDOFF_WORKFLOW and (
            path.parent.name != cfg["run_id"] or path.parent.resolve() != args.config.parent.resolve()):
        raise ValueError("Private controller state and config must belong to the same run")
    if args.poll_seconds is not None and not 0 < args.poll_seconds < float("inf"):
        ap.error("--poll-seconds must be a positive finite number")
    poll_seconds = cfg.get("poll_seconds", DEFAULT_POLL_SECONDS)
    if args.poll_seconds is not None:
        poll_seconds = args.poll_seconds
    wait_minutes = cfg.get("response_wait_minutes") if args.command == "run" else None
    if args.command == "run":
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%dT%H:%M:%SZ")
        formatter.converter = time.gmtime
        handler.setFormatter(formatter)
        logging.basicConfig(level=logging.INFO, handlers=[handler])
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
            if c.config != config:
                raise ValueError("Persisted controller configuration does not match run")
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
            if c.config != config:
                raise ValueError("Persisted controller configuration does not match run")
            c.resume_after_owner()
            c.save(path)
            path.with_suffix(".pause").unlink(missing_ok=True)
            output("resumed", path)
        return

    with exclusive_lock(path):
        c = Controller.load(path)
        if c.config != config:
            raise ValueError("Persisted controller configuration does not match run")
        if args.ready_file is not None:
            with args.ready_file.open("x", encoding="ascii") as ready:
                ready.write(str(os.getpid()))
        wait_seconds = None if wait_minutes is None else wait_minutes * 60
        deadline = None if wait_seconds is None else time.monotonic() + wait_seconds
        logging.info("run_started chat=%s poll_seconds=%s response_wait_minutes=%s",
                     c.state.current_chat_id, poll_seconds, wait_minutes)
        polls = 0
        while True:
            if (c.state.halted not in ("programme_finished", "chat_cap")
                    and path.with_suffix(".pause").exists()):
                c.pause("Operator pause requested")
                c.save(path)
                output("paused", path)
                return
            pending = c.state.pending
            consumed = len(c.state.consumed_responses)
            act = cycle(c, browser, reader, cfg["run_id"], path,
                        defer_dispatch=args.prepare_only, response_deadline=deadline)
            # WAIT after a prepared or newly consumed action means Send was confirmed.
            if act == Action.WAIT and (pending is not None or len(c.state.consumed_responses) > consumed):
                logging.info("submission_confirmed chat=%s", c.state.current_chat_id)
                if wait_seconds is not None:
                    deadline = time.monotonic() + wait_seconds
            logging.info("cycle_result action=%s chat=%s", act.value, c.state.current_chat_id)
            polls += 1
            if (args.command == "cycle" or act not in (Action.WAIT, Action.IGNORE)
                    or (args.max_polls and polls >= args.max_polls)):
                output("cycle", path, action=act.value)
                return
            delay = poll_seconds
            if deadline is not None:
                delay = min(delay, max(0, deadline - time.monotonic()))
            time.sleep(delay)


if __name__ == "__main__":
    main()
