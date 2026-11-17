"""Astra controller execution boundary. No second state machine or retrying sender.

All browser effects are delegated to one adapter, after the reference model's
state is persisted. Tests inject an adapter; real operation uses Windows UIA.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
import json
import sys

_KIT = Path(__file__).resolve().parents[1] / "astra/2026-11-17/unpacked/chat_succession_test_kit_20261117"
if str(_KIT) not in sys.path:
    sys.path.insert(0, str(_KIT))

from succession.composer import ComposerObservation, ComposerState, classify_composer
from succession.core import Action, Config, Controller, Response, RepoView, Status, interpret
from repo_reader import GitPublishedReader, PublishedStateError


@dataclass(frozen=True)
class Destination:
    """Observed destination after preparing, never inferred from the sidebar."""
    project: str
    current_chat_id: str | None
    composer: ComposerObservation
    private_window_handle: int


@dataclass(frozen=True)
class Submitted:
    """Read-back evidence, not an assertion that Send was invoked."""
    project: str
    chat_id: str | None
    submitted_text: str | None
    posted_message_observed: bool


class Browser(Protocol):
    def observe(self, expected_chat_id: str) -> Response | None: ...
    def prepare(self, kind: str, current_chat_id: str) -> Destination: ...
    def send_once(self, target: Destination, message: str) -> Submitted: ...


def dispatch_prepared(controller: Controller, browser: Browser, state_path: Path) -> Action:
    """Serialized prepare -> persist sending -> one click -> read-back.

    An exception after begin_send is indistinguishable from lost acknowledgement,
    even if the adapter believes the click never happened. Never retry blindly.
    """
    p = controller.state.pending
    if p is None:
        return Action.WAIT
    if p.phase != "prepared" or controller.state.halted:
        return Action.HOLD
    try:
        target = browser.prepare(p.kind, p.source_chat_id)
        expected = controller.config.project
        if target.project != expected or target.private_window_handle <= 0:
            controller.pause("Destination Project/window not independently observed")
            controller.save(state_path)
            return Action.HOLD
        if p.kind == Action.CONTINUE_CURRENT.value:
            if target.current_chat_id != p.source_chat_id:
                controller.pause("Continuation destination is not the current saved chat")
                controller.save(state_path)
                return Action.HOLD
        else:
            if target.current_chat_id is not None:
                controller.pause("Successor target is not an observed fresh Project composer")
                controller.save(state_path)
                return Action.HOLD
        if classify_composer(target.composer) != ComposerState.EMPTY:
            controller.pause("Existing draft, attachment or ambiguous editor evidence")
            controller.save(state_path)
            return Action.HOLD
    except Exception as exc:
        controller.pause(f"Desktop prepare did not establish safe target: {exc}")
        controller.save(state_path)
        return Action.HOLD

    controller.begin_send(p.action_id)
    controller.save(state_path)  # durable before the first possible keystroke
    try:
        receipt = browser.send_once(target, p.message)
        if (not receipt.posted_message_observed or
                receipt.submitted_text != p.message or
                receipt.chat_id is None):
            raise RuntimeError("Exact posted message, saved ID and Project not all observed")
        decision = controller.confirm(p.action_id, receipt.chat_id,
                                      receipt.project, message_observed=True)
        controller.save(state_path)
        return decision.action
    except Exception as exc:
        controller.uncertain(p.action_id, f"UI submission outcome uncertain: {exc}")
        controller.save(state_path)
        return Action.HOLD


def cycle(controller: Controller, browser: Browser, reader: GitPublishedReader,
          run_id: str, state_path: Path) -> Action:
    """One observation/dispatch cycle. Duplicate observations are deduplicated."""
    if controller.state.halted:
        return Action.HOLD
    if controller.state.pending:
        if controller.state.pending.phase != "prepared":
            return Action.HOLD
        return dispatch_prepared(controller, browser, state_path)

    try:
        response = browser.observe(controller.state.current_chat_id)
    except Exception as exc:
        controller.pause(f"Desktop response observation unavailable: {exc}")
        controller.save(state_path)
        return Action.HOLD
    if response is None:
        return Action.WAIT
    repo: RepoView | None = None
    parsed = interpret(response.text, response.complete)
    if (response.role == "assistant" and parsed.status == Status.TASK_COMPLETE and
            response.project == controller.config.project and
            response.chat_id == controller.state.current_chat_id):
        try:
            repo = reader.read(run_id).view
        except (PublishedStateError, OSError, ValueError) as exc:
            # Preserve the completed response event for audit; controller holds
            # with an unavailable published state instead of fabricating a view.
            decision = controller.consume(response)
            controller.save(state_path)
            return decision.action
    decision = controller.consume(response, repo)
    controller.save(state_path)
    if decision.action in (Action.CONTINUE_CURRENT, Action.LAUNCH_SUCCESSOR):
        return dispatch_prepared(controller, browser, state_path)
    return decision.action


def initialise(state_path: Path, config: Config, observed_chat_id: str) -> Controller:
    """No implicit reset of an existing run or missing previous state."""
    if state_path.exists():
        raise FileExistsError("Existing state: load it; do not reset count")
    c = Controller(config, observed_chat_id)
    c.save(state_path)
    return c


def inspect_state(state_path: Path) -> dict:
    c = Controller.load(state_path)
    return {
        "project": c.config.project,
        "repo": c.config.repo,
        "branch": c.config.branch,
        "current_chat_id": c.state.current_chat_id,
        "unique_chat_count": c.unique_count,
        "last_status": c.state.last_status,
        "pending_action": None if c.state.pending is None else {
            "kind": c.state.pending.kind, "phase": c.state.pending.phase,
            "action_id": c.state.pending.action_id,
        },
        "halted": c.state.halted,
    }
