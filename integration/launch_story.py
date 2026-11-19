"""Shared Windows bootstrap and entry point for the My Cat and Dog trial."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from uuid import uuid4

from cli import create_dependencies, exclusive_lock, load_config
from repo_reader import GitHandoffReader, HANDOFF_WORKFLOW, STORY_REPO
from runner import initialise, inspect_state
from succession.composer import ComposerState, classify_composer
from succession.core import Action, Config


def prepare_first(browser, reader):
    if isinstance(reader, GitHandoffReader):
        reader.published_tip(shallow=True)
    elif set(reader.heads()) != {"main"}:
        raise RuntimeError("Story branches already exist. Preserve the published run.")
    target = browser.prepare(Action.LAUNCH_SUCCESSOR.value, None)
    composer = classify_composer(target.composer)
    if (target.project != browser.project or target.current_chat_id is not None
            or target.private_window_handle <= 0
            or composer != ComposerState.EMPTY):
        raise RuntimeError(f"Fresh empty Project composer was not verified ({composer.value})")
    return target


def bootstrap(cfg: dict, state_path: Path, browser, reader, *, owner_request_id=None) -> dict:
    """Persist intent once and use read-only reconciliation on uncertain retries."""
    intent_path = state_path.with_name("bootstrap-intent.json")
    pause_path = state_path.with_suffix(".pause").resolve()
    pointer = (
        f"Continue the work in GitHub repo {cfg['repo']}, branch {cfg['branch']}. "
        "Read the current instructions, progress and next task there."
    )
    if isinstance(reader, GitHandoffReader):
        pointer += reader.instructions(cfg["run_id"], 1, owner_request_id)
    if intent_path.exists():
        intent = json.loads(intent_path.read_text(encoding="utf-8"))
        if intent["project"] != cfg["project"]:
            raise RuntimeError("Existing initial Send intent belongs to a different run")
        pointer = intent["message"]
        receipt = browser._invoke("Reconcile", Kind=Action.LAUNCH_SUCCESSOR.value,
                                  WindowHandle=intent["handle"], Message=pointer)
    else:
        if pause_path.exists():
            raise RuntimeError("Owner paused before the initial Send")
        target = prepare_first(browser, reader)
        intent = {"handle": target.private_window_handle,
                  "project": target.project, "message": pointer}
        with intent_path.open("x", encoding="utf-8") as stream:
            json.dump(intent, stream)
            stream.flush()
            os.fsync(stream.fileno())
        receipt = browser._invoke("Send", Kind=Action.LAUNCH_SUCCESSOR.value,
                                  WindowHandle=intent["handle"], Message=pointer,
                                  PausePath=pause_path)
        if receipt == {"paused_before_click": True}:
            intent_path.unlink()
            raise RuntimeError("Owner paused before the initial Send")

    if (receipt.get("posted_message_observed") is not True
            or receipt.get("project") != cfg["project"]
            or receipt.get("submitted_text") != pointer
            or not receipt.get("chat_id")):
        raise RuntimeError("Initial Send is held until exact posted-message evidence identifies the saved chat")
    config = Config(cfg["project"], cfg["repo"], cfg["branch"], cfg["max_unique_chats"])
    initialise(state_path, config, receipt["chat_id"])
    return inspect_state(state_path)


def start_controller(config_path: Path, state_path: Path) -> int:
    ready_file = state_path.with_name(f"startup-{uuid4().hex}.ready")
    command = [sys.executable, "-B", "-X", "utf8", str(Path(__file__).with_name("cli.py")),
               "run", "--config", str(config_path), "--state", str(state_path),
               "--ready-file", str(ready_file)]
    with (state_path.with_name("controller-stdout.json").open("ab") as stdout,
          state_path.with_name("controller-timing.log").open("ab") as stderr):
        process = subprocess.Popen(
            command, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
        )
    try:
        for _ in range(80):
            if ready_file.exists() and ready_file.read_text(encoding="ascii") == str(process.pid):
                return process.pid
            if process.poll() is not None:
                break
            time.sleep(0.1)
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=5)
        raise RuntimeError("Controller lock ownership was not confirmed. Inspect the existing run before retrying.")
    finally:
        ready_file.unlink(missing_ok=True)


def launch(config_path: Path, state_path: Path, *, check_only: bool = False, owner_request_id=None) -> dict:
    cfg = load_config(config_path)
    if cfg["repo"] != STORY_REPO and cfg.get("workflow") != HANDOFF_WORKFLOW:
        raise ValueError("This launcher needs a supported desktop handoff")
    browser, reader = create_dependencies(cfg, state_path)
    with exclusive_lock(state_path.with_name("bootstrap.json")):
        if check_only:
            if state_path.exists() or state_path.with_name("bootstrap-intent.json").exists():
                raise RuntimeError("The run already has a controller or a prior launch attempt")
            prepare_first(browser, reader)
            return {"event": "preflight_passed", "project": cfg["project"], "repo": cfg["repo"]}

        if state_path.exists():
            summary = inspect_state(state_path)
            if (summary["project"] != cfg["project"] or summary["repo"] != cfg["repo"]
                    or summary["initial_branch"] != cfg["branch"]
                    or summary["max_unique_chats"] != cfg["max_unique_chats"]):
                raise RuntimeError("The private controller state belongs to a different workload")
            if summary["halted"]:
                return {**summary, "event": "existing_run"}
            try:
                with exclusive_lock(state_path):
                    pass
            except OSError:
                return {**summary, "event": "controller_already_running"}
        else:
            kwargs = {"owner_request_id": owner_request_id} if owner_request_id else {}
            summary = bootstrap(cfg, state_path, browser, reader, **kwargs)
        pid = start_controller(config_path, state_path)
        return {**summary, "event": "controller_started", "controller_pid": pid}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        result = launch(args.config.resolve(), args.state.resolve(), check_only=args.check)
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps({"event": "launch_held", "reason": str(exc)}))
        raise SystemExit(1)
    print(json.dumps(result))
