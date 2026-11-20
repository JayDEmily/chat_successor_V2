"""Astra controller execution boundary. No second state machine or retrying sender.

All browser effects are delegated to one adapter, after the reference model's
state is persisted. Tests inject an adapter; real operation uses Windows UIA.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
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
from succession.core import Action, Config, Controller, Pending, Response, RepoView, Status, interpret
from repo_reader import GitHandoffReader, GitPublishedReader, GitStoryReader, PublishedStateError


@dataclass(frozen=True)
class Destination:
    """Observed destination after preparing, never inferred from the sidebar."""
    project: str
    current_chat_id: str | None
    composer: ComposerObservation
    private_window_handle: int
    private_document_id: str | None = None


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


def owner_context(data, *, anchored):
    fields = {"request_id", "instruction", "scope", "pointer"}
    if anchored:
        fields |= {"worker_id", "response_id"}
    if (not isinstance(data, dict) or set(data) != fields
            or any(not isinstance(value, str) or not value.strip() or len(value) > 4000
                   for value in data.values())
            or not re.fullmatch(r"[a-z0-9]{24,64}", data["request_id"])):
        raise ValueError("Owner context needs a stable ID, instruction, scope and project pointer")
    return data


def read_verified_owner_input(path: Path) -> dict:
    try:
        body = path.read_bytes()
        expected = path.with_suffix(".sha256").read_text(encoding="ascii").strip()
        if hashlib.sha256(body).hexdigest() != expected:
            raise ValueError("Private owner input differs from its durable receipt")
        return json.loads(body.decode("utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError("The saved private owner input or its receipt is unavailable or changed") from exc


def read_pending_owner_context(controller: Controller, pending: Pending, state_path: Path) -> dict:
    request_id = pending.owner_request_id
    if not isinstance(request_id, str) or not re.fullmatch(r"[a-z0-9]{24,64}", request_id):
        raise ValueError("Invalid saved owner request ID")
    path = state_path.with_name(f"owner-{request_id}.json")
    context = owner_context(read_verified_owner_input(path), anchored=True)
    anchor = [pending.source_chat_id, pending.response_id]
    if (context["request_id"] != request_id or [context["worker_id"], context["response_id"]] != anchor
            or controller.state.owner_requests.get(request_id) != anchor):
        raise ValueError("The saved private owner input does not match the pending worker and response")
    return context


def pause_marker_digest(state_path: Path) -> str | None:
    try:
        return hashlib.sha256(state_path.with_suffix(".pause").read_bytes()).hexdigest()
    except FileNotFoundError:
        return None


def owner_pause_reason(state_path: Path, reason: str = "Operator pause requested") -> str:
    digest = pause_marker_digest(state_path)
    return f"{reason} [pause-marker={digest}]" if digest else reason


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
        context = None
        if p.owner_request_id:
            context = read_pending_owner_context(controller, p, state_path)
            if browser.reentry_disposition(p.source_chat_id, p.response_id) == "advanced":
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
        if context is not None and read_pending_owner_context(controller, p, state_path) != context:
            raise ValueError("The saved private owner input changed during preparation")
    except Exception as exc:
        controller.pause(f"Desktop prepare did not establish safe target: {exc}")
        controller.save(state_path)
        return Action.HOLD

    if state_path.with_suffix(".pause").exists():
        controller.pause(owner_pause_reason(state_path, "Operator pause requested before Send"))
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
        reason = owner_pause_reason(state_path, str(exc)) if isinstance(exc, PausedBeforeClick) else str(exc)
        controller.pause(reason)
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
            branch = controller.checkpoint_branch
            if isinstance(reader, GitHandoffReader):
                branch = checkpoint_from_response(response.text, branch)
                if "CHAT_HANDOFF_BRANCH" in response.text.upper() and response.handoff_locator_verified is False:
                    raise PublishedStateError("Browser did not verify the branch locator in the assistant's prose")
                publication = reader.read_checkpoint(run_id, branch)
            else:
                publication = reader.read(run_id)
            if (publication.run_id != run_id or publication.view.last_chat_id != response.chat_id
                    or publication.view.repo != controller.config.repo or publication.view.branch != branch):
                raise PublishedStateError("Published receipt is for a different run, worker or route")
            if (publication.view.published is not True or publication.view.readable is not True
                    or not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", publication.commit or "")):
                raise PublishedStateError("Published receipt lacks a verified commit")
            if (isinstance(reader, GitStoryReader) and
                    publication.completed_turns != controller.unique_count):
                raise PublishedStateError("Published story turn does not match the current worker count")
            repo = publication.view
            controller.state.checkpoint_branch = branch if branch != controller.config.branch else None
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
    if accepted_publication is not None and decision.action in (
            Action.LAUNCH_SUCCESSOR, Action.STOP_FINISHED, Action.STOP_CAP):
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


_ADOPTED_PUBLICATION = re.compile(
    r"^(?:\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z )?"
    r"publication_receipt_adopted run=(\S+) chat=(\S+) response=(\S+) "
    r"ref=(refs/heads/\S+) sha=([0-9a-f]{40}|[0-9a-f]{64}) "
    r"decision=(?:LAUNCH_SUCCESSOR|STOP_FINISHED|STOP_CAP)\s*$"
)


def last_publication(state_path: Path, controller: Controller, run_id: str | None) -> tuple[str | None, str | None]:
    if not run_id:
        return None, None
    consumed = {tuple(anchor) for anchor in controller.state.consumed_responses}
    ref = f"refs/heads/{controller.checkpoint_branch}"
    commit = None
    try:
        with state_path.with_name("controller-timing.log").open(encoding="utf-8", errors="replace") as log:
            for line in log:
                match = _ADOPTED_PUBLICATION.search(line)
                if match and match[1] == run_id and match[4] == ref and (match[2], match[3]) in consumed:
                    commit = match[5]
    except OSError:
        return None, None
    return (commit, ref) if commit else (None, None)


def inspect_state(state_path: Path) -> dict:
    c = Controller.load(state_path)
    marker_digest = pause_marker_digest(state_path)
    halted = c.state.halted
    pause_acknowledged = False
    if isinstance(halted, str) and halted.startswith("Operator pause requested"):
        reason, separator, recorded = halted.rpartition(" [pause-marker=")
        if separator and re.fullmatch(r"[a-f0-9]{64}\]", recorded):
            halted = reason
            pause_acknowledged = marker_digest is not None and recorded == f"{marker_digest}]"
    cfg_path = state_path.with_name("config.json")
    cfg = {}
    if cfg_path.is_file():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            if not isinstance(cfg, dict):
                raise ValueError("Private run config must be an object")
        except (ValueError, OSError) as exc:
            raise ValueError("Private run account configuration unreadable") from exc
    publication_commit, publication_ref = last_publication(state_path, c, cfg.get("run_id"))
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
        "halted": halted,
        "pause_requested": marker_digest is not None,
        "pause_acknowledged": pause_acknowledged,
        "account_key": cfg.get("account_key"),
        "route_receipt": cfg.get("route_receipt"),
        "publication_commit": publication_commit,
        "publication_ref": publication_ref,
    }
