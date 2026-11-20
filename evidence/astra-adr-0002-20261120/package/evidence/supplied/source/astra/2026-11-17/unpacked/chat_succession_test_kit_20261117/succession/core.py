"""Small, offline succession control model. No browser, GitHub, or model calls.

Only three worker statuses exist. HOLD/WAIT/STOP are controller actions, not
additional worker statuses. A single serialized adapter owns one Controller.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
import json
import os
import re
import tempfile


class Status(str, Enum):
    NEED_MORE_TIME = "NEED_MORE_TIME"
    TASK_COMPLETE = "TASK_COMPLETE"
    ERROR = "ERROR"


class Action(str, Enum):
    WAIT = "WAIT"
    IGNORE = "IGNORE"
    HOLD = "HOLD"
    CONTINUE_CURRENT = "CONTINUE_CURRENT"
    LAUNCH_SUCCESSOR = "LAUNCH_SUCCESSOR"
    STOP_FINISHED = "STOP_FINISHED"
    STOP_CAP = "STOP_CAP"


@dataclass(frozen=True)
class Interpretation:
    status: Optional[Status]
    basis: str
    reason: str


@dataclass(frozen=True)
class SemanticVerdict:
    """An injected adjudication, NOT an implemented semantic classifier."""
    status: Status
    unambiguous: bool
    reason: str


def interpret(text: str, complete: bool = True,
              semantic: Optional[SemanticVerdict] = None) -> Interpretation:
    """Parse an entire *assistant* message, never a page/tool transcript.

    Canonical final nonblank line: CHAT_STATUS: <UPPERCASE_STATUS>.
    A bare uppercase final keyword is supported for the owner's short form.
    Code fences and quoted lines cannot supply a terminal status.
    An absent marker may use an injected, reasoned, unambiguous adjudication;
    malformed or conflicting explicit markers may not be overridden by it.
    """
    if complete is not True:
        return Interpretation(None, "incomplete", "Assistant response is still streaming")
    lines = text.splitlines()
    nonblank = [i for i, line in enumerate(lines) if line.strip()]
    if not nonblank:
        return Interpretation(None, "ambiguous", "No assistant response")
    last = nonblank[-1]
    fence_char = None
    fence_len = 0
    candidates = []
    marker_like = []
    for i, line in enumerate(lines):
        # Four-space indented code must not become an actionable marker.
        if line.startswith("    ") or line.startswith("\t"):
            continue
        stripped = line.strip()
        if stripped.startswith(">"):
            continue
        f = re.match(r"^(`{3,}|~{3,})(.*)$", stripped)
        if f:
            token, tail = f.groups()
            if fence_char is None:
                fence_char, fence_len = token[0], len(token)
            elif token[0] == fence_char and len(token) >= fence_len and not tail.strip():
                fence_char = None
            continue
        if fence_char is not None:
            continue
        match = re.fullmatch(r"(?:CHAT_STATUS: )?(NEED_MORE_TIME|TASK_COMPLETE|ERROR)", stripped)
        if match:
            candidates.append((i, Status(match.group(1)),
                               "explicit" if stripped.startswith("CHAT_STATUS:") else "bare"))
        elif (re.match(r"^CHAT_STATUS\b", stripped, flags=re.I) or
              re.fullmatch(r"(NEED_MORE_TIME|TASK_COMPLETE|ERROR)[.!:]?", stripped, flags=re.I)):
            marker_like.append(i)
    if marker_like:
        return Interpretation(None, "ambiguous", "Malformed explicit status")
    if len(candidates) == 1 and candidates[0][0] == last and fence_char is None:
        _, status, basis = candidates[0]
        return Interpretation(status, basis, "One final-line status")
    if candidates:
        return Interpretation(None, "ambiguous", "Repeated, conflicting or nonterminal status")
    # An unclosed code block is a truncated/ambiguous message, not semantic success.
    if fence_char is not None:
        return Interpretation(None, "ambiguous", "Unclosed code fence")
    if (semantic is not None and semantic.unambiguous is True
            and isinstance(semantic.reason, str) and semantic.reason.strip()):
        if isinstance(semantic.status, Status):
            return Interpretation(semantic.status, "semantic", semantic.reason)
    return Interpretation(None, "ambiguous", "No unambiguous terminal status")


def conversation_id(value: str) -> str:
    """Normalize alternate /c/ URL views of the same observed conversation."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("An observed conversation identity is required")
    value = value.strip()
    if "://" in value:
        path = urlparse(value).path
        match = re.search(r"(?:^|/)c/([^/]+)(?:/|$)", path)
        if not match:
            raise ValueError("URL does not identify a saved conversation")
        value = match.group(1)
    if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
        raise ValueError("Malformed conversation identity")
    return value


@dataclass(frozen=True)
class Config:
    project: str
    repo: str
    branch: str
    max_unique_chats: int = 30

    def __post_init__(self):
        for value in (self.project, self.repo, self.branch):
            if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
                raise ValueError("Project/repo/branch must be nonempty single-line values")
        if type(self.max_unique_chats) is not int or self.max_unique_chats < 1:
            raise ValueError("max_unique_chats must be a positive integer")


@dataclass(frozen=True)
class RepoView:
    """Ordinary current branch state observed by an adapter.

    This is an observation seam, NOT a cryptographic or live-verified receipt.
    A local commit without publication must not be mapped to published=True.
    """
    repo: str
    branch: str
    last_chat_id: str
    programme_complete: bool
    next_task: Optional[str]
    published: bool = True
    readable: bool = True


@dataclass(frozen=True)
class Response:
    chat_id: str
    response_id: str
    text: str
    complete: bool = True
    role: str = "assistant"
    project: Optional[str] = None
    handoff_locator_verified: Optional[bool] = None


@dataclass
class Pending:
    action_id: str
    kind: str
    source_chat_id: str
    response_id: str
    message: str
    phase: str = "prepared"  # prepared -> sending -> observed, or uncertain
    detail: str = ""
    owner_request_id: Optional[str] = None


@dataclass
class State:
    current_chat_id: str
    unique_chat_ids: list[str]
    consumed_responses: list[list[str]] = field(default_factory=list)
    last_status: Optional[str] = None
    pending: Optional[Pending] = None
    halted: Optional[str] = None
    checkpoint_branch: Optional[str] = None
    owner_requests: dict[str, list[str]] = field(default_factory=dict)


@dataclass(frozen=True)
class Decision:
    action: Action
    reason: str
    action_id: Optional[str] = None
    message: Optional[str] = None


class Controller:
    """A single-writer reference state machine, not a deployed browser service."""

    def __init__(self, config: Config, initial_chat_id: str):
        self.config = config
        cid = conversation_id(initial_chat_id)
        self.state = State(current_chat_id=cid, unique_chat_ids=[cid])

    @property
    def unique_count(self) -> int:
        return len(self.state.unique_chat_ids)

    @property
    def checkpoint_branch(self) -> str:
        return self.state.checkpoint_branch or self.config.branch

    def continue_after_owner(self, request_id: str, anchor: str, message: str) -> None:
        """Queue one explicit owner instruction without inventing an assistant turn."""
        cid = self.state.current_chat_id
        if request_id in self.state.owner_requests or [cid, anchor] in self.state.owner_requests.values():
            raise ValueError("The owner action for this hold already exists")
        if (not self.state.halted or self.state.pending is not None
                or self.state.halted in ("programme_finished", "chat_cap")
                or self.state.consumed_responses[-1:] != [[cid, anchor]]):
            raise ValueError("The saved worker is no longer at the nominated hold")
        self.state.owner_requests[request_id] = [cid, anchor]
        self.state.pending = Pending(f"{cid}:owner:{request_id}", Action.CONTINUE_CURRENT.value,
                                     cid, anchor, message, owner_request_id=request_id)
        self.state.halted = None

    def _hold(self, reason: str) -> Decision:
        self.state.halted = reason
        return Decision(Action.HOLD, reason)

    def consume(self, response: Response, repo: Optional[RepoView] = None,
                semantic: Optional[SemanticVerdict] = None) -> Decision:
        """Plan at most one action; caller saves state before any side effect."""
        if self.state.halted:
            return Decision(Action.HOLD, self.state.halted)
        if response.role != "assistant":
            return Decision(Action.IGNORE, "Only assistant responses can control the run")
        try:
            cid = conversation_id(response.chat_id)
        except ValueError:
            return self._hold("Missing or malformed source conversation identity")
        if cid != self.state.current_chat_id:
            return Decision(Action.IGNORE, "Response belongs to a different conversation")
        if response.project != self.config.project:
            return self._hold("Active response Project differs or is unknown")
        if not isinstance(response.response_id, str) or not response.response_id.strip():
            return self._hold("A stable response event identity is needed for deduplication")
        key = [cid, response.response_id]
        if key in self.state.consumed_responses:
            return Decision(Action.IGNORE, "Response event already consumed")
        if self.state.pending is not None:
            return Decision(Action.WAIT, "Resolve the in-flight send before another response")
        result = interpret(response.text, response.complete, semantic)
        if result.basis == "incomplete":
            return Decision(Action.WAIT, result.reason)
        self.state.consumed_responses.append(key)
        if result.status is None:
            return self._hold(result.reason)
        self.state.last_status = result.status.value
        if result.status == Status.ERROR:
            return self._hold("Worker reported ERROR; show its explanation to the owner")
        if result.status == Status.NEED_MORE_TIME:
            return self._prepare(Action.CONTINUE_CURRENT, response, "Okay, continue working.")
        # TASK_COMPLETE requires durable work, even when already at the cap.
        if (repo is None or repo.readable is not True or repo.published is not True):
            return self._hold("Handover publication or programme state is unavailable")
        if repo.repo != self.config.repo or repo.branch != self.checkpoint_branch:
            return self._hold("Repo observation is for a different nominated target")
        try:
            handoff_id = conversation_id(repo.last_chat_id)
        except ValueError:
            return self._hold("Handover has no valid source chat identity")
        if handoff_id != self.state.current_chat_id:
            return self._hold("Repo state is stale or belongs to a different worker")
        if type(repo.programme_complete) is not bool:
            return self._hold("programme_complete must be a real boolean")
        if repo.programme_complete:
            if repo.next_task is not None and str(repo.next_task).strip():
                return self._hold("Repo state says finished but also supplies remaining work")
            self.state.halted = "programme_finished"
            return Decision(Action.STOP_FINISHED, "GitHub programme state is finished")
        if not isinstance(repo.next_task, str) or not repo.next_task.strip():
            return self._hold("Unfinished programme lacks a next task")
        if self.unique_count >= self.config.max_unique_chats:
            self.state.halted = "chat_cap"
            return Decision(Action.STOP_CAP, "Configured distinct-chat cap reached")
        message = (
            f"Continue the work in GitHub repo {self.config.repo}, branch {self.checkpoint_branch}. "
            "Read the current instructions, progress and next task there."
        )
        return self._prepare(Action.LAUNCH_SUCCESSOR, response, message)

    def _prepare(self, kind: Action, response: Response, message: str) -> Decision:
        action_id = f"{self.state.current_chat_id}:{response.response_id}:{kind.value}"
        self.state.pending = Pending(action_id, kind.value, self.state.current_chat_id,
                                     response.response_id, message)
        return Decision(kind, "Ready for one serialized adapter action", action_id, message)

    def begin_send(self, action_id: str) -> None:
        """Call then save *before* invoking the UI Send action."""
        pending = self._pending(action_id)
        if self.state.halted:
            raise ValueError("Controller is halted")
        if pending.phase != "prepared":
            raise ValueError("This send was already attempted; reconcile, do not retry")
        pending.phase = "sending"

    def uncertain(self, action_id: str, detail: str = "Send result unknown") -> None:
        pending = self._pending(action_id)
        pending.phase = "uncertain"
        pending.detail = detail
        self.state.halted = detail

    def confirm(self, action_id: str, observed_chat_id: str, observed_project: str,
                message_observed: bool = True) -> Decision:
        """Adopt a *read-back observation*; this method never sends anything.

        Also used after restart. If no sent message can be established, leave the
        pending action intact. Duplicate acknowledgements have no side effect.
        """
        if self.state.pending is None:
            return Decision(Action.IGNORE, "No pending action; duplicate acknowledgement")
        pending = self._pending(action_id)
        if pending.phase not in ("sending", "uncertain"):
            return self._hold("No Send attempt was recorded; reconcile unexpected UI change")
        if message_observed is not True:
            return self._hold("No read-back evidence of the submitted message")
        if observed_project != self.config.project:
            return self._hold("Submitted message is not observed in the nominated Project")
        try:
            cid = conversation_id(observed_chat_id)
        except ValueError:
            return self._hold("Submitted message has no saved conversation identity")
        if pending.kind == Action.CONTINUE_CURRENT.value:
            if cid != pending.source_chat_id:
                return self._hold("Continuation was observed in a different chat")
        else:
            if cid in self.state.unique_chat_ids:
                return self._hold("Successor is not a new observed conversation")
            if self.unique_count >= self.config.max_unique_chats:
                return self._hold("Unexpected observation would exceed the chat cap")
            self.state.unique_chat_ids.append(cid)
            self.state.current_chat_id = cid
        self.state.pending = None
        self.state.halted = None
        return Decision(Action.WAIT, "Submitted message observed; wait for its assistant response")

    def confirm_not_sent(self, action_id: str, reason: str) -> None:
        """Explicit owner/adapter reconciliation, not an automatic timeout retry.

        Requires positive evidence that no submission occurred. An absent new
        chat in a possibly stale sidebar is NOT such evidence. Rearms same action.
        """
        pending = self._pending(action_id)
        if pending.phase not in ("sending", "uncertain") or not reason.strip():
            raise ValueError("A reasoned not-sent reconciliation is required")
        pending.phase = "prepared"
        pending.detail = reason
        self.state.halted = None

    def pause(self, reason: str = "Owner pause") -> Decision:
        return self._hold(reason)

    def resume_after_owner(self) -> None:
        """Clear a nonterminal hold; only a never-attempted prepared send may remain."""
        if self.state.pending is not None and self.state.pending.phase != "prepared":
            raise ValueError("Reconcile the pending Send before resuming")
        if self.state.halted in ("programme_finished", "chat_cap"):
            raise ValueError("A finished/capped run is not an error retry")
        self.state.halted = None

    def _pending(self, action_id: str) -> Pending:
        pending = self.state.pending
        if pending is None or pending.action_id != action_id:
            raise ValueError("Unknown action identity")
        return pending

    def save(self, path: Path) -> None:
        """Atomic local bookkeeping, not a launch approval or handover hash."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"version": 2, "config": asdict(self.config), "state": asdict(self.state)}
        handle, temp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as out:
                json.dump(payload, out, indent=2)
                out.write("\n")
                out.flush()
                os.fsync(out.fileno())
            os.replace(temp, path)
            # Best effort directory durability on systems which support it.
            if os.name == "posix":
                fd = os.open(path.parent, os.O_RDONLY)
                try:
                    os.fsync(fd)
                finally:
                    os.close(fd)
        finally:
            if os.path.exists(temp):
                os.unlink(temp)

    @classmethod
    def load(cls, path: Path) -> "Controller":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if payload.get("version") not in (1, 2):
            raise ValueError("Unsupported state version; do not start with a reset count")
        config = Config(**payload["config"])
        raw = payload["state"]
        raw["pending"] = Pending(**raw["pending"]) if raw.get("pending") is not None else None
        state = State(**raw)
        ids = state.unique_chat_ids
        if (not ids or len(ids) != len(set(ids)) or
                any(conversation_id(x) != x for x in ids) or
                state.current_chat_id not in ids or
                len(ids) > config.max_unique_chats):
            raise ValueError("Invalid persisted conversation count or identity")
        if state.last_status is not None:
            Status(state.last_status)
        if any(not isinstance(k, list) or len(k) != 2 or k[0] not in ids
               or not isinstance(k[1], str) or not k[1] for k in state.consumed_responses):
            raise ValueError("Invalid consumed response history")
        if len({tuple(k) for k in state.consumed_responses}) != len(state.consumed_responses):
            raise ValueError("Duplicate consumed response history")
        if (not isinstance(state.owner_requests, dict)
                or any(not re.fullmatch(r"[a-z0-9]{24,64}", key) or value not in state.consumed_responses
                       for key, value in state.owner_requests.items())
                or len({tuple(value) for value in state.owner_requests.values()}) != len(state.owner_requests)):
            raise ValueError("Invalid owner action history")
        if state.checkpoint_branch is not None:
            Config(config.project, config.repo, state.checkpoint_branch, config.max_unique_chats)
        p = state.pending
        if p is not None:
            if (p.kind not in (Action.LAUNCH_SUCCESSOR.value, Action.CONTINUE_CURRENT.value)
                    or p.phase not in ("prepared", "sending", "uncertain")
                    or p.source_chat_id != state.current_chat_id
                    or [p.source_chat_id, p.response_id] not in state.consumed_responses
                    or (p.owner_request_id is not None and
                        (p.kind != Action.CONTINUE_CURRENT.value
                         or p.action_id != f"{p.source_chat_id}:owner:{p.owner_request_id}"
                         or state.owner_requests.get(p.owner_request_id) != [p.source_chat_id, p.response_id]))):
                raise ValueError("Invalid pending action")
            if p.phase in ("sending", "uncertain"):
                state.halted = "Restart with a possibly submitted message: reconcile without sending"
        obj = cls(config, state.current_chat_id)
        obj.state = state
        return obj
