"""Astra controller execution boundary. No second state machine or retrying sender.

All browser effects are delegated to one adapter, after the reference model's
state is persisted. Tests inject an adapter; real operation uses Windows UIA.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
import json
import logging
import re
import sys
import time

_KIT = Path(__file__).resolve().parents[1] / "astra/2026-11-17/unpacked/chat_succession_test_kit_20261117"
if str(_KIT) not in sys.path:
    sys.path.insert(0, str(_KIT))

from succession.composer import ComposerObservation, ComposerState, classify_composer
from succession.core import Action, Config, Controller, Response, RepoView, Status, interpret
from repo_reader import GitHandoffReader, GitPublishedReader, GitStoryReader, PublishedStateError


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


class SendBlockedBeforeClick(RuntimeError):
    """The adapter positively established that it did not invoke Send."""


class PausedBeforeClick(SendBlockedBeforeClick):
    """The browser adapter observed owner pause before invoking Send."""


class WorkerAdvancedBeforeClick(RuntimeError):
    """The worker already advanced past the response that triggered Send."""


class Browser(Protocol):
    def observe(self, expected_chat_id: str) -> Response | None: ...
    def prepare(self, kind: str, current_chat_id: str) -> Destination: ...
    def send_once(self, target: Destination, message: str) -> Submitted: ...


def dispatch_prepared(controller: Controller, browser: Browser, state_path: Path) -> Action:
    """Serialized prepare -> persist sending -> one click -> read-back.

    After begin_send, only an explicit adapter receipt can establish no click.
    Other failures enter read-only reconciliation.
    """
    p = controller.state.pending
    if p is None:
        return Action.WAIT
    if p.phase != "prepared" or controller.state.halted:
        return Action.HOLD
    try:
        if p.owner_request_id and browser.reentry_disposition(p.source_chat_id, p.response_id) == "advanced":
            controller.state.pending = None
            controller.save(state_path)
            return Action.IGNORE
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

    if state_path.with_suffix(".pause").exists():
        controller.pause("Operator pause requested before Send")
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
    except SendBlockedBeforeClick as exc:
        controller.confirm_not_sent(p.action_id, str(exc))
        controller.pause(str(exc))
        controller.save(state_path)
        return Action.HOLD
    except WorkerAdvancedBeforeClick:
        controller.state.pending = None
        controller.save(state_path)
        return Action.IGNORE
    except Exception as exc:
        controller.uncertain(p.action_id, f"UI submission outcome uncertain: {exc}")
        controller.save(state_path)
        return Action.HOLD


def checkpoint_from_response(text: str, current: str) -> str:
    lines = [line for line in text.splitlines() if line.strip()]
    candidates = [line for line in lines if re.search(r"\bCHAT_HANDOFF_BRANCH\b", line, re.I)]
    if not candidates:
        return current
    match = re.fullmatch(r"CHAT_HANDOFF_BRANCH: ([A-Za-z0-9_./-]+)", candidates[0])
    if (not match or candidates != lines[-2:-1] or lines[-1] != "CHAT_STATUS: TASK_COMPLETE"):
        raise PublishedStateError("Malformed or conflicting handoff branch locator")
    return match[1]


def cycle(controller: Controller, browser: Browser,
          reader: GitPublishedReader | GitStoryReader | GitHandoffReader,
          run_id: str, state_path: Path, *, defer_dispatch: bool = False,
          response_deadline: float | None = None) -> Action:
    """One observation/dispatch cycle.

    The L06 one-shot preparation mode persists the reference controller's
    prepared action without opening a composer or sending; a normal later cycle
    dispatches that same pending action after the repo-only probe is rotated.
    """

    if controller.state.halted:
        return Action.HOLD
    if controller.state.pending:
        if controller.state.pending.phase != "prepared":
            return Action.HOLD
        if defer_dispatch:
            return Action(controller.state.pending.kind)
        return dispatch_prepared(controller, browser, state_path)

    response = None
    try:
        if response_deadline is None or time.monotonic() < response_deadline:
            response = browser.observe(controller.state.current_chat_id)
    except Exception as exc:
        controller.pause(f"Desktop response observation unavailable: {exc}")
        controller.save(state_path)
        return Action.HOLD
    if response_deadline is not None and time.monotonic() >= response_deadline:
        controller.pause("Configured response wait expired")
        controller.save(state_path)
        return Action.HOLD
    if response is None:
        return Action.WAIT
    repo: RepoView | None = None
    accepted_publication = None
    parsed = interpret(response.text, response.complete)
    if (response.role == "assistant" and parsed.status == Status.TASK_COMPLETE and
            response.project == controller.config.project and
            response.chat_id == controller.state.current_chat_id and
            isinstance(response.response_id, str) and response.response_id.strip() and
            [response.chat_id, response.response_id] not in controller.state.consumed_responses):
        logging.info("publication_check_start chat=%s", response.chat_id)
        try:
            if isinstance(reader, GitHandoffReader):
                branch = checkpoint_from_response(response.text, controller.checkpoint_branch)
                if "CHAT_HANDOFF_BRANCH" in response.text.upper() and response.handoff_locator_verified is False:
                    raise PublishedStateError("Browser did not verify the branch locator in the assistant's prose")
                publication = reader.read_checkpoint(run_id, branch)
                if (publication.view.last_chat_id != response.chat_id or
                        publication.view.repo != controller.config.repo or publication.view.branch != branch):
                    raise PublishedStateError("Published receipt is for a different worker or route")
                if branch != controller.config.branch:
                    controller.state.checkpoint_branch = branch
                else:
                    controller.state.checkpoint_branch = None
            else:
                publication = reader.read(run_id)
            if (isinstance(reader, GitStoryReader) and
                    publication.completed_turns != controller.unique_count):
                raise PublishedStateError("Published story turn does not match the current worker count")
            repo = publication.view
            accepted_publication = publication
            logging.info("publication_receipt_verified run=%s chat=%s response=%s ref=refs/heads/%s sha=%s result=IDENTITY_MATCH",
                         run_id, response.chat_id, response.response_id,
                         repo.branch, publication.commit)
        except (PublishedStateError, OSError, ValueError) as exc:
            # Hold without consuming: publication can be repaired and this
            # exact completed turn can then be processed once on resume.
            logging.warning("publication_receipt_rejected run=%s chat=%s response=%s result=HOLD reason=%s",
                            run_id, response.chat_id, response.response_id, exc)
            controller.pause(f"Published Git state unavailable: {exc}")
            controller.save(state_path)
            return Action.HOLD
        logging.info("publication_check_finished chat=%s", response.chat_id)
    decision = controller.consume(response, repo)
    if decision.action == Action.LAUNCH_SUCCESSOR and isinstance(reader, GitHandoffReader):
        controller.state.pending.message += reader.instructions(run_id, controller.unique_count + 1)
    controller.save(state_path)
    if accepted_publication is not None:
        logging.info("publication_receipt_adopted run=%s chat=%s response=%s ref=refs/heads/%s sha=%s decision=%s",
                     run_id, response.chat_id, response.response_id,
                     accepted_publication.view.branch, accepted_publication.commit,
                     decision.action.value)
    if decision.action in (Action.CONTINUE_CURRENT, Action.LAUNCH_SUCCESSOR):
        if defer_dispatch:
            return decision.action
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
    marker = state_path.with_suffix(".pause")
    paused = marker.is_file()
    cfg_path = state_path.with_name("config.json")
    account_key = None
    route_receipt = None
    if cfg_path.is_file():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            raise ValueError("Private run account configuration unreadable") from exc
        account_key = cfg.get("account_key")
        route_receipt = cfg.get("route_receipt")
    return {
        "project": c.config.project,
        "repo": c.config.repo,
        "branch": c.checkpoint_branch,
        "initial_branch": c.config.branch,
        "max_unique_chats": c.config.max_unique_chats,
        "current_chat_id": c.state.current_chat_id,
        "response_anchor": c.state.consumed_responses[-1] if c.state.consumed_responses else None,
        "unique_chat_count": c.unique_count,
        "last_status": c.state.last_status,
        "pending_action": None if c.state.pending is None else {
            "kind": c.state.pending.kind, "phase": c.state.pending.phase,
            "action_id": c.state.pending.action_id,
        },
        "halted": c.state.halted,
        "pause_requested": paused,
        "pause_acknowledged": (paused and isinstance(c.state.halted, str)
                               and c.state.halted.startswith("Operator pause requested")),
        "account_key": account_key,
        "route_receipt": route_receipt,
        "publication_commit": None,  # not persisted; never invent a live Git receipt
    }
