"""Independent A2-G1 probes. Real local Git and stubbed browser only."""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock

parser = argparse.ArgumentParser()
parser.add_argument("candidate", type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.candidate / "integration"))

from owner_reentry import resume_request
from repo_reader import GitHandoffReader, GitPublishedReader, HANDOFF_WORKFLOW
from runner import Destination, cycle, initialise, inspect_state
from succession.composer import ComposerObservation
from succession.core import Config, Controller, Response

PROJECT = "g-p-abc123"
CHAT = "00000000-0000-0000-0000-000000000001"
TURN = "uia-turn-1-aaaaaaaaaaaaaaaaaaaa"
RUN = "b" * 24
BRANCH = "work/check"
REPO = "example/fixture"


def git(root, *args):
    return subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def publish(root, path, data):
    path.write_text(json.dumps(data), encoding="utf-8")
    git(root, "add", str(path))
    git(root, "commit", "-m", "Publish synthetic fixture")
    git(root, "push", "origin", f"HEAD:refs/heads/{BRANCH}")
    return git(root, "rev-parse", "HEAD")


def publication_retry(root):
    writer, mirror, remote = (root / name for name in ("writer", "mirror", "remote.git"))
    for path in (writer, mirror, remote):
        path.mkdir(parents=True)
    git(remote, "init", "--bare")
    git(writer, "init", "-b", BRANCH)
    git(writer, "config", "user.email", "review@example.invalid")
    git(writer, "config", "user.name", "Offline Fixture")
    git(writer, "remote", "add", "origin", str(remote))
    git(mirror, "init", "--bare")
    git(mirror, "remote", "add", "origin", str(remote))

    reader = GitPublishedReader(mirror, REPO, BRANCH, "succession-tests/check")
    # The disposable local remote preserves the real fetch/ref/object path.
    reader._verify_origin = Mock()
    state_file = writer / "succession-tests/check/STATE.json"
    state_file.parent.mkdir(parents=True)
    state = {"run_id": RUN, "last_chat_id": CHAT, "programme_complete": False, "next_task": "  "}
    first_sha = publish(writer, state_file, state)
    response = Response(chat_id=CHAT, response_id=TURN, text="CHAT_STATUS: TASK_COMPLETE",
                        project=PROJECT, complete=True)
    browser = Mock()
    browser.observe.return_value = response
    journal = root / "controller.json"
    controller = initialise(journal, Config(PROJECT, REPO, BRANCH, 3), CHAT)
    invalid = cycle(controller, browser, reader, RUN, journal)
    consumed = Controller.load(journal).state.consumed_responses
    valid_sha = publish(writer, state_file, {**state, "next_task": "Do the next slice"})
    controller = Controller.load(journal)
    controller.resume_after_owner()
    retry = cycle(controller, browser, reader, RUN, journal, defer_dispatch=True)
    return {"bad_commit": first_sha, "repair_commit": valid_sha,
            "invalid_result": invalid.value, "consumed_before_repair": consumed,
            "retry_same_response_result": retry.value,
            "prepare_calls": browser.prepare.call_count, "send_calls": browser.send_once.call_count}


def owner_input_after_restart(root):
    root.mkdir()
    config_path, journal = root / "config.json", root / "controller.json"
    config = Config(PROJECT, REPO, BRANCH, 3)
    config_path.write_text(json.dumps({
        "project": PROJECT, "repo": REPO, "branch": BRANCH, "max_unique_chats": 3,
        "run_id": RUN, "project_name": "Synthetic", "repo_dir_wsl": "/mock",
        "project_url": f"https://chatgpt.com/g/{PROJECT}/project",
        "workflow": HANDOFF_WORKFLOW,
    }), encoding="utf-8")
    controller = initialise(journal, config, CHAT)
    controller.consume(Response(chat_id=CHAT, response_id=TURN, text="CHAT_STATUS: ERROR",
                                project=PROJECT, complete=True))
    controller.save(journal)
    context = {"request_id": "c" * 24, "worker_id": CHAT, "response_id": TURN,
               "instruction": "Approve synthetic item one", "scope": "synthetic item one",
               "pointer": "approval fixture one"}
    browser = Mock()
    browser.reentry_disposition.return_value = "idle"
    browser.prepare.return_value = Destination(PROJECT, CHAT, ComposerObservation(
        editable_text="", attachments_present=False), 55, "document-proof")
    browser.send_once.side_effect = RuntimeError("End at the fake Send boundary")
    reader = GitHandoffReader(root, REPO, BRANCH)
    initial = resume_request(config_path, journal, {"owner_context": context},
                             "Synthetic", lambda *_: (browser, reader), Mock(return_value=42))
    saved = root / ("owner-" + context["request_id"] + ".json")
    saved.write_text(json.dumps({**context, "instruction": "Approve synthetic item two",
                                 "pointer": "approval fixture two", "scope": "synthetic item two"}),
                     encoding="utf-8")
    controller = Controller.load(journal)
    pending_before = controller.state.pending
    result = cycle(controller, browser, reader, RUN, journal)
    pending_after = Controller.load(journal).state.pending
    return {"entry_event": initial["event"], "dispatch_result": result.value,
            "pending_action_id_preserved": pending_before.action_id == pending_after.action_id,
            "phase_after": pending_after.phase, "prepare_calls": browser.prepare.call_count,
            "send_calls": browser.send_once.call_count}


def pause_generation(root):
    root.mkdir()
    journal = root / "controller.json"
    controller = initialise(journal, Config(PROJECT, REPO, BRANCH, 3), CHAT)
    marker = journal.with_suffix(".pause")
    marker.write_text("Operator pause first\n", encoding="utf-8")
    controller.pause("Operator pause requested")
    controller.save(journal)
    acknowledged_first = inspect_state(journal)["pause_acknowledged"]
    marker.write_text("Operator pause second\n", encoding="utf-8")
    return {"first_acknowledged": acknowledged_first,
            "fresh_generation_before_observer_acknowledged": inspect_state(journal)["pause_acknowledged"],
            "marker_preserved": marker.read_text(encoding="utf-8").strip() == "Operator pause second"}


with tempfile.TemporaryDirectory(prefix="a2-g1-offline-review-") as folder:
    root = Path(folder)
    print(json.dumps({"S02_blank_published_continuation": publication_retry(root / "publication"),
                      "O05_changed_owner_input_after_restart": owner_input_after_restart(root / "owner"),
                      "R04_new_pause_generation": pause_generation(root / "pause")}, indent=2))
