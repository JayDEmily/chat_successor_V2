"""Windows entry point for one iPhone-launched My Cat and Dog run."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from cli import create_dependencies, exclusive_lock, load_config
from repo_reader import STORY_REPO
from runner import initialise, inspect_state
from succession.composer import ComposerState, classify_composer
from succession.core import Action, Config


def prepare_first(browser, reader):
    if set(reader.heads()) != {"main"}:
        raise RuntimeError("Story branches already exist. Preserve the published run.")
    target = browser.prepare(Action.LAUNCH_SUCCESSOR.value, None)
    composer = classify_composer(target.composer)
    if (target.project != browser.project or target.current_chat_id is not None
            or target.private_window_handle <= 0
            or composer != ComposerState.EMPTY):
        raise RuntimeError(f"Fresh empty story Project composer was not verified ({composer.value})")
    return target


def bootstrap(cfg: dict, state_path: Path, browser, reader) -> dict:
    """Persist intent once and use read-only reconciliation on uncertain retries."""
    intent_path = state_path.with_name("bootstrap-intent.json")
    pointer = (
        f"Continue the work in GitHub repo {STORY_REPO}, branch main. "
        "Read the current instructions, progress and next task there."
    )
    if intent_path.exists():
        intent = json.loads(intent_path.read_text(encoding="utf-8"))
        if intent["project"] != cfg["project"] or intent["message"] != pointer:
            raise RuntimeError("Existing initial Send intent belongs to a different run")
        receipt = browser._invoke("Reconcile", Kind=Action.LAUNCH_SUCCESSOR.value,
                                  WindowHandle=intent["handle"], Message=pointer)
    else:
        target = prepare_first(browser, reader)
        intent = {"handle": target.private_window_handle,
                  "project": target.project, "message": pointer}
        with intent_path.open("x", encoding="utf-8") as stream:
            json.dump(intent, stream)
            stream.flush()
            os.fsync(stream.fileno())
        receipt = browser._invoke("Send", Kind=Action.LAUNCH_SUCCESSOR.value,
                                  WindowHandle=intent["handle"], Message=pointer,
                                  PausePath=state_path.with_suffix(".pause").resolve())

    if (receipt.get("posted_message_observed") is not True
            or receipt.get("project") != cfg["project"]
            or receipt.get("submitted_text") != pointer
            or not receipt.get("chat_id")):
        raise RuntimeError("Initial Send is held until exact posted-message evidence identifies the saved chat")
    config = Config(cfg["project"], STORY_REPO, "main", cfg["max_unique_chats"])
    initialise(state_path, config, receipt["chat_id"])
    return inspect_state(state_path)


def start_controller(config_path: Path, state_path: Path) -> int:
    command = [sys.executable, "-B", "-X", "utf8", str(Path(__file__).with_name("cli.py")),
               "run", "--config", str(config_path), "--state", str(state_path)]
    with (state_path.with_name("controller-stdout.json").open("ab") as stdout,
          state_path.with_name("controller-timing.log").open("ab") as stderr):
        process = subprocess.Popen(
            command, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
        )
    time.sleep(0.5)
    if process.poll() is not None:
        raise RuntimeError("Windows controller exited at startup. Inspect its local timing log.")
    return process.pid


def launch(config_path: Path, state_path: Path, *, check_only: bool = False) -> dict:
    cfg = load_config(config_path)
    if cfg["repo"] != STORY_REPO:
        raise ValueError("This launcher is scoped to My Cat and Dog")
    browser, reader = create_dependencies(cfg, state_path)
    with exclusive_lock(state_path.with_name("bootstrap.json")):
        if check_only:
            if state_path.exists() or state_path.with_name("bootstrap-intent.json").exists():
                raise RuntimeError("The story already has a controller or a prior launch attempt")
            prepare_first(browser, reader)
            return {"event": "preflight_passed", "project": cfg["project"], "repo": STORY_REPO}

        if state_path.exists():
            summary = inspect_state(state_path)
            if summary["project"] != cfg["project"] or summary["repo"] != STORY_REPO:
                raise RuntimeError("The private controller state belongs to a different workload")
            if summary["halted"]:
                return {**summary, "event": "existing_run"}
            try:
                with exclusive_lock(state_path):
                    pass
            except OSError:
                return {**summary, "event": "controller_already_running"}
        else:
            summary = bootstrap(cfg, state_path, browser, reader)
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
