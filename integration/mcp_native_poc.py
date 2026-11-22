"""M03 synthetic-only admission seam; no MCP listener, Git or desktop effects.

Trusted observations are test injections, not host attestations. The reference
Controller is the only decision engine. A durable reservation precedes every
simulated attempt. This proof runs on POSIX in an isolated private directory.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import wraps
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import secrets
import stat
import sys
import tempfile
import threading
import time
from typing import Callable

_KIT = Path(__file__).resolve().parents[1] / "astra/2026-11-17/unpacked/chat_succession_test_kit_20261117"
if str(_KIT) not in sys.path:
    sys.path.insert(0, str(_KIT))
from succession.core import Action, Config, Controller, RepoView, Response, Status


class Rejected(ValueError):
    """Invalid/untrusted input; not an instruction to retry or send."""


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False)


def strict_object(body, fields):
    if type(body) is not dict or set(body) != set(fields):
        raise Rejected("Unexpected or missing fields")
    if type(body["schema_version"]) is not int or body["schema_version"] != 1:
        raise Rejected("Unsupported schema")
    for field in ("run_id", "action_id"):
        if not token(body[field]):
            raise Rejected("Invalid request identity")


def token(value):
    return type(value) is str and 0 < len(value) <= 1024 and bool(
        re.fullmatch(r"[A-Za-z0-9_.:/@-]+", value))


def branch_name(value):
    """Conservative exact short Git branch grammar; never invoke Git on a request."""
    return (type(value) is str
            and bool(re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_./-]*", value))
            and value != "HEAD" and not value.startswith("refs/")
            and ".." not in value and not value.endswith(".")
            and all(c and not c.startswith(".") and not c.endswith(".lock")
                    for c in value.split("/")))


def valid_time(value):
    return type(value) in (int, float) and math.isfinite(value)


def sha(value):
    return type(value) is str and bool(re.fullmatch(r"(?:[a-f0-9]{40}|[a-f0-9]{64})", value))


def saved_id(value):
    return type(value) is str and bool(re.fullmatch(
        r"[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}", value))


def read_file(directory, name):
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError("Journal member is not a regular file")
        with os.fdopen(fd, "rb", closefd=False) as f:
            return f.read()
    finally:
        os.close(fd)


def identity(st):
    return (st.st_dev, st.st_ino)


def atomic_write(directory, name, data):
    """Publish immutable bytes, never replace an existing journal member.

    Both names are relative to the already locked directory descriptor, not
    a potentially replaced path. Hard link is atomic and fails if name exists.
    A partial intent/record pair is a recovery hold, never a prior-state reset.
    """
    staging = ".stage-" + secrets.token_hex(16)
    fd = os.open(staging, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                 0o600, dir_fd=directory)
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        os.link(staging, name, src_dir_fd=directory, dst_dir_fd=directory,
                follow_symlinks=False)
        os.fsync(directory)
    finally:
        os.unlink(staging, dir_fd=directory)
        os.fsync(directory)


def member_names(generation):
    return (f"intent-{generation:08d}.json",
            "ledger.json" if generation == 0 else f"ledger-{generation:08d}.json")


def journal_names(directory):
    # Staging files are not publication; a crash before the first link can
    # leave them behind. Never interpret them as committed snapshots.
    return {n for n in os.listdir(directory)
            if n.startswith("ledger") or n.startswith("intent")}


@dataclass(frozen=True)
class Route:
    run_id: str
    principal: str
    account_key: str
    project_id: str
    repo: str
    branch: str
    base_sha: str
    cap: int
    action_cap: int = 32  # finite total synthetic reservation budget
    response_timeout_seconds: int = 300  # finite per-attempt response policy

    def __post_init__(self):
        if not all(token(x) for x in (self.run_id, self.principal, self.account_key,
                                       self.project_id, self.repo, self.branch)):
            raise ValueError("Invalid synthetic route")
        if not re.fullmatch(r"[A-Za-z0-9-]+/[A-Za-z0-9_.-]+", self.repo):
            raise ValueError("Invalid repo")
        if not branch_name(self.branch):
            raise ValueError("Invalid branch")
        if (not sha(self.base_sha) or type(self.cap) is not int or self.cap < 1
                or type(self.action_cap) is not int or self.action_cap < 1):
            raise ValueError("Invalid base or cap")
        if (type(self.response_timeout_seconds) is not int
                or not 1 <= self.response_timeout_seconds <= 86400):
            raise ValueError("Invalid finite response timeout")


@dataclass(frozen=True)
class Auth:
    """Mock transport-generated context; never parsed from worker body."""
    principal: str
    run_id: str
    account_key: str
    session: str
    subject: str


@dataclass(frozen=True)
class Dispatch:
    action_id: str
    prompt: str
    challenge: str  # volatile controller-only, never persisted in this POC


@dataclass(frozen=True)
class Quiet:
    """Independent mock observation anchored to one reserved turn."""
    run_id: str
    action_id: str
    chat_id: str
    idle: bool | None


@dataclass(frozen=True)
class Preflight:
    """Independent mock target observation; never supplied by the worker."""
    account_key: str
    project_id: str
    target_chat: str | None
    empty: bool
    no_attachments: bool
    source_quiet: Quiet | None


@dataclass(frozen=True)
class Delivery:
    """Independent synthetic saved receipt AND session-to-chat evidence."""
    run_id: str
    action_id: str
    account_key: str
    project_id: str
    chat_id: str
    prompt_digest: str
    principal: str
    session: str
    subject: str
    observed: bool


@dataclass(frozen=True)
class Remote:
    """Injected independent remote read, including ancestry observation."""
    run_id: str
    commit: str
    view: RepoView
    verified_ancestor: str


def serialized(method):
    """Serialize all mutation through the single owning controller instance."""
    @wraps(method)
    def guarded(self, *args, **kwargs):
        if self._pid != os.getpid():
            raise RuntimeError("Inherited controller is not a writer")
        with self._mutex:
            return method(self, *args, **kwargs)
    return guarded


class Proof:
    """Single directory-inode writer over immutable atomic snapshot pairs.

    Private local POSIX directory; no hostile filesystem administrator or
    coordinated deletion/rollback of multiple independent journal members.
    No path replacement of existing evidence, no auto rearm or actual sender.
    """
    def __init__(self, path: Path, route: Route | None = None, *, clock=time.time):
        self.path = Path(path)
        self.clock = clock
        self.closed = False
        self.poisoned = False
        self.core = None
        self._directory = None
        self._marker = None
        self._owner = None
        self._pid = os.getpid()
        self._committed = {}  # exact immutable intent/record bytes
        self._generation = 0
        self._previous = None
        self._mutex = threading.RLock()
        creating = route is not None
        if creating:
            self.path.mkdir(mode=0o700, parents=False, exist_ok=False)
        try:
            self._directory = os.open(self.path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            # A removable marker is not a lock: lock the stable directory inode.
            fcntl.flock(self._directory, fcntl.LOCK_EX | fcntl.LOCK_NB)
            flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
            if creating:
                flags = os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
            self._marker = os.open("writer.lock", flags, 0o600, dir_fd=self._directory)
            if creating:
                # Persistent random witness prevents inode-number reuse from
                # making an empty replacement marker appear authentic.
                with os.fdopen(os.dup(self._marker), "wb") as marker:
                    marker.write(secrets.token_hex(32).encode("ascii"))
                    marker.flush()
                    os.fsync(marker.fileno())
                os.fsync(self._directory)
            witness = read_file(self._directory, "writer.lock")
            if not re.fullmatch(b"[0-9a-f]{64}", witness):
                raise ValueError("Invalid writer witness")
            self._owner = list(identity(os.fstat(self._directory))
                               + identity(os.fstat(self._marker))) + [
                                   hashlib.sha256(witness).hexdigest()]
            if creating:
                self.route = route
                self.data = {"version": 1, "route": asdict(route), "active": None,
                             "history": [], "bindings": {}, "prior_sha": route.base_sha,
                             "hold": None, "paused": False, "core": None}
                self._commit()
            else:
                self._restore()
        except BaseException:
            self.close()
            raise

    def __enter__(self):
        self._usable()
        return self

    def __exit__(self, *_):
        self.close()

    @serialized
    def close(self):
        self.closed = True
        if self._marker is not None:
            os.close(self._marker)
            self._marker = None
        if self._directory is not None:
            os.close(self._directory)
            self._directory = None

    def _verify_owner(self):
        if self.closed or self.poisoned or self._pid != os.getpid():
            raise RuntimeError("Ledger unavailable or inherited; reopen and reconcile")
        directory = self._directory
        if (identity(os.stat(self.path, follow_symlinks=False)) !=
                identity(os.fstat(directory))):
            raise ValueError("Run directory replaced")
        mark = os.stat("writer.lock", dir_fd=directory, follow_symlinks=False)
        if (not stat.S_ISREG(mark.st_mode)
                or identity(mark) != identity(os.fstat(self._marker))):
            raise ValueError("Writer marker missing or replaced")
        witness = read_file(directory, "writer.lock")
        if (list(identity(os.fstat(directory)) + identity(mark)) +
                [hashlib.sha256(witness).hexdigest()]) != self._owner:
            raise ValueError("Writer identity mismatch")

    def _verify_journal(self, expected):
        self._verify_owner()
        if journal_names(self._directory) != set(expected):
            raise ValueError("Journal inventory changed")
        for name, raw in expected.items():
            if read_file(self._directory, name) != raw:
                raise ValueError("Immutable journal member changed")
        self._verify_owner()

    def _usable(self):
        try:
            self._verify_journal(self._committed)
        except (OSError, ValueError) as exc:
            self.poisoned = True
            raise RuntimeError("Ledger unavailable or changed; reconcile without overwriting") from exc

    def _now(self):
        now = self.clock()
        if not valid_time(now):
            self.poisoned = True
            raise RuntimeError("Invalid clock; reconcile")
        return now

    def _response_expired(self, r):
        return (r is not None and not r["consumed"]
                and r["response_deadline"] is not None
                and self._now() >= r["response_deadline"])

    @property
    def active(self):
        return self.data["active"]

    @property
    def count(self):
        return 0 if self.core is None else self.core.unique_count

    @property
    def terminal(self):
        return self.core is not None and self.core.state.halted in (
            "programme_finished", "chat_cap")

    def _serialize_core(self):
        if self.core is None:
            return None
        return {"version": 2, "config": asdict(self.core.config), "state": asdict(self.core.state)}

    def _commit(self):
        self._usable()
        try:
            self.data["core"] = self._serialize_core()
            generation = self._generation
            intent_name, record_name = member_names(generation)
            envelope = canonical({
                "payload": self.data, "sha256": digest(canonical(self.data)),
                "generation": generation, "previous": self._previous,
                "owner": self._owner,
            }).encode("utf-8") + b"\n"
            record_digest = hashlib.sha256(envelope).hexdigest()
            intent = canonical({"generation": generation, "record_sha256": record_digest,
                                "previous": self._previous,
                                "owner": self._owner}).encode("utf-8") + b"\n"
            # Durable intent is a separate witness against deletion of the
            # newest record. Never overwrite, even on a competing publication.
            atomic_write(self._directory, intent_name, intent)
            expected = self._committed | {intent_name: intent}
            try:
                self._verify_journal(expected)
            except (OSError, ValueError) as exc:
                raise RuntimeError("Journal changed during intent publication") from exc
            atomic_write(self._directory, record_name, envelope)
            expected[record_name] = envelope
            # Faults during either publication preserve old evidence. A missing,
            # damaged or incomplete pair prevents any later restart/admission.
            try:
                self._verify_journal(expected)
            except (OSError, ValueError) as exc:
                raise RuntimeError("Journal changed during snapshot publication") from exc
            self._committed = expected
            self._generation += 1
            self._previous = record_digest
        except BaseException:
            self.poisoned = True
            raise

    def _restore(self):
        self._verify_owner()
        names = journal_names(self._directory)
        if "ledger.json" not in names:
            raise FileNotFoundError("Missing genesis ledger")
        if not names or len(names) % 2:
            raise ValueError("Incomplete journal pair")
        expected = {}
        previous = None
        d = None
        for generation in range(len(names) // 2):
            intent_name, record_name = member_names(generation)
            if intent_name not in names or record_name not in names:
                raise ValueError("Missing or unexpected journal generation")
            raw = read_file(self._directory, record_name)
            iraw = read_file(self._directory, intent_name)
            env = json.loads(raw)
            intent = json.loads(iraw)
            record_digest = hashlib.sha256(raw).hexdigest()
            if (type(env) is not dict or set(env) != {"payload", "sha256",
                                                    "generation", "previous", "owner"}
                    or type(env["generation"]) is not int or env["generation"] != generation
                    or env["previous"] != previous or env["owner"] != self._owner
                    or digest(canonical(env["payload"])) != env["sha256"]
                    or type(intent) is not dict or type(intent.get("generation")) is not int
                    or intent != {"generation": generation, "record_sha256": record_digest,
                                  "previous": previous, "owner": self._owner}):
                raise ValueError("Journal integrity or ownership failure")
            d = env["payload"]
            expected[intent_name], expected[record_name] = iraw, raw
            previous = record_digest
        self._verify_journal(expected)
        self._committed = expected
        self._generation = len(names) // 2
        self._previous = previous
        if (type(d) is not dict or set(d) != {"version", "route", "active", "history",
                      "bindings", "prior_sha", "hold", "paused", "core"}
                or type(d["version"]) is not int or d["version"] != 1
                or not sha(d["prior_sha"]) or type(d["paused"]) is not bool
                or type(d["history"]) is not list or type(d["bindings"]) is not dict):
            raise ValueError("Invalid ledger")
        # Old disposable proof ledgers without a deadline policy are not migrated.
        if "response_timeout_seconds" not in d["route"]:
            raise ValueError("Missing durable response policy")
        self.route = Route(**d["route"])
        self.data = d
        if d["core"] is not None:
            # Reuse original load validation; scratch file is not authoritative.
            with tempfile.TemporaryDirectory(dir=self.path) as temp:
                state = Path(temp) / "core.json"
                state.write_text(canonical(d["core"]), encoding="utf-8")
                self.core = Controller.load(state)
            if self.core.config != self._config():
                raise ValueError("Core route mismatch")
        if set(d["bindings"]) != (set(self.core.state.unique_chat_ids) if self.core else set()):
            raise ValueError("Saved binding/count mismatch")
        for cid, binding in d["bindings"].items():
            if (not saved_id(cid) or set(binding) != {"principal", "session", "subject"}
                    or binding["principal"] != self.route.principal
                    or not token(binding["session"]) or not token(binding["subject"])):
                raise ValueError("Invalid binding")
        if len({b["session"] for b in d["bindings"].values()}) != len(d["bindings"]):
            raise ValueError("Reused session")
        if len({b["subject"] for b in d["bindings"].values()}) > 1:
            raise ValueError("Subject changed")
        if len(d["history"]) + bool(self.active) > self.route.action_cap:
            raise ValueError("Reservation budget exceeded")
        seen = set()
        for r in d["history"] + ([self.active] if self.active else []):
            if (type(r) is not dict or r["action_id"] in seen
                    or r["phase"] not in {"prepared", "sending", "uncertain", "bound"}
                    or not sha(r["challenge_digest"]) or not sha(r["prompt_digest"])
                    or r["kind"] not in {"bootstrap", "CONTINUE_CURRENT", "LAUNCH_SUCCESSOR"}
                    or not valid_time(r.get("expiry"))
                    or "response_deadline" not in r
                    or (r["response_deadline"] is not None if r["phase"] == "prepared"
                        else not valid_time(r["response_deadline"]))):
                raise ValueError("Invalid reservation")
            seen.add(r["action_id"])
        if any(not r["consumed"] or r["phase"] != "bound" for r in d["history"]):
            raise ValueError("Invalid archived action")
        r = self.active
        if r:
            if r["phase"] == "bound":
                if (self.core is None or r["saved_chat"] != self.core.state.current_chat_id
                        or d["bindings"].get(r["saved_chat"]) != r["registration"]):
                    raise ValueError("Active receipt does not match core")
            elif r["kind"] == "bootstrap":
                if self.core is not None or r["ordinal"] != 1:
                    raise ValueError("Duplicate bootstrap")
            elif (self.core is None or self.core.state.pending is None
                  or self.core.state.pending.action_id != r["action_id"]
                  or self.core.state.pending.phase != r["phase"]):
                raise ValueError("Core pending reservation mismatch")
            if r["phase"] in ("sending", "uncertain"):
                # A crash at either boundary is indistinguishable from a Send.
                r["phase"] = "uncertain"
                if self.core:
                    self.core.uncertain(r["action_id"], "Restart: possibly submitted")
                if self.data["hold"] not in ("conflict", "response_deadline", "expired"):
                    self.data["hold"] = "uncertain"
                self._commit()
        elif self.core or d["history"]:
            raise ValueError("Missing active reservation")
        self._usable()

    def _config(self):
        route = self.route
        return Config(route.project_id, route.repo, route.branch, route.cap)

    def _hold(self, reason):
        if not self.terminal:
            if (self.data["hold"] != "conflict"
                    and (self.data["hold"] != "response_deadline" or reason == "conflict")):
                self.data["hold"] = reason
            self._commit()
        return Action.HOLD

    @serialized
    def pause(self):
        self._usable()
        if not self.terminal:
            self.data["paused"] = True
            self._commit()

    @serialized
    def resume(self):
        self._usable()
        if self._response_expired(self.active):
            self._hold("response_deadline")
        if (self.terminal or self.data["hold"] in ("conflict", "uncertain", "delivery", "expired",
                                                  "action_budget", "response_deadline")
                or (self.active and self.active["phase"] in ("sending", "uncertain"))):
            raise Rejected("Explicit positive reconciliation required")
        self.data["paused"] = False
        self.data["hold"] = None
        if self.core and self.core.state.halted:
            self.core.resume_after_owner()
        self._commit()

    @serialized
    def reserve(self, *, ttl=300) -> Dispatch:
        """Controller-only reservation. No body-selected kind, route or command."""
        self._usable()
        if (self.terminal or self.data["paused"] or self.data["hold"]
                or type(ttl) is not int or not 1 <= ttl <= 3600):
            raise Rejected("Reservation blocked")
        previous = self.active
        if previous is None:
            if self.core is not None:
                raise Rejected("Not a bootstrap")
            kind, action_id, ordinal, source, anchor = (
                "bootstrap", self.route.run_id + ":bootstrap", 1, None, None)
            message = "Begin the authorized synthetic fixture."
        else:
            if (not previous["consumed"] or self.core is None
                    or self.core.state.pending is None or self.core.state.pending.phase != "prepared"):
                raise Rejected("Existing reservation or no core action")
            p = self.core.state.pending
            kind, action_id, source, anchor = p.kind, p.action_id, p.source_chat_id, p.response_id
            ordinal = self.count + (kind == Action.LAUNCH_SUCCESSOR.value)
            message = p.message
            if ordinal > self.route.cap:
                raise Rejected("Cap exceeded")
        if len(self.data["history"]) + bool(previous) >= self.route.action_cap:
            self._hold("action_budget")
            raise Rejected("Finite reservation budget exhausted")
        challenge = secrets.token_urlsafe(32)
        prompt = (message + "\nSynthetic run: " + self.route.run_id + "\nAction: " + action_id
                  + "\nRegistration challenge: " + challenge)
        r = {"action_id": action_id, "kind": kind, "ordinal": ordinal, "source": source,
             "anchor": anchor, "challenge_digest": digest(challenge),
             "prompt_digest": digest(prompt), "expiry": self._now() + ttl, "phase": "prepared",
             "response_deadline": None, "registration": None, "saved_chat": None, "report": None, "consumed": False}
        if previous:
            self.data["history"].append(previous)
        self.data["active"] = r
        self._commit()
        return Dispatch(action_id, prompt, challenge)

    def _quiet(self, observation, action_id, cid):
        return (type(observation) is Quiet and observation.run_id == self.route.run_id
                and observation.action_id == action_id and observation.chat_id == cid
                and observation.idle is True)

    @serialized
    def begin_attempt(self, dispatch: Dispatch, target: Preflight):
        """Persist sending before any simulated effect. Does not perform Send."""
        self._usable()
        r = self.active
        if (not r or r["phase"] != "prepared" or self.data["paused"]
                or self.data["hold"] or self.terminal):
            raise Rejected("Cannot attempt or retry")
        if (dispatch.action_id != r["action_id"] or digest(dispatch.prompt) != r["prompt_digest"]
                or digest(dispatch.challenge) != r["challenge_digest"]):
            raise Rejected("Reservation mismatch")
        now = self._now()
        if now >= r["expiry"]:
            return self._hold("expired")
        desired = r["source"] if r["kind"] == Action.CONTINUE_CURRENT.value else None
        if (type(target) is not Preflight or target.account_key != self.route.account_key
                or target.project_id != self.route.project_id or target.target_chat != desired
                or target.empty is not True or target.no_attachments is not True
                or (r["source"] is not None and not self._quiet(
                    target.source_quiet, self.data["history"][-1]["action_id"], r["source"]))):
            return self._hold("preflight")
        if self.core is not None:
            self.core.begin_send(r["action_id"])
        r["phase"] = "sending"
        r["response_deadline"] = now + self.route.response_timeout_seconds
        self._commit()
        return Action.WAIT

    @serialized
    def uncertain(self):
        self._usable()
        r = self.active
        if not r or r["phase"] not in ("sending", "uncertain"):
            raise Rejected("No attempted reservation")
        r["phase"] = "uncertain"
        if self.core:
            self.core.uncertain(r["action_id"], "Possibly submitted")
        return self._hold("uncertain")

    def _request(self, body, fields, auth):
        self._usable()
        strict_object(body, fields)
        r = self.active
        if (not r or body["run_id"] != self.route.run_id or body["action_id"] != r["action_id"]):
            raise Rejected("Stale or wrong reservation")
        if (type(auth) is not Auth or auth.principal != self.route.principal
                or auth.run_id != self.route.run_id or auth.account_key != self.route.account_key
                or not token(auth.session) or not token(auth.subject)):
            raise Rejected("Missing or unscoped authenticated context")
        return r, {"principal": auth.principal, "session": auth.session, "subject": auth.subject}

    @serialized
    def register_worker(self, body, auth):
        r, binding = self._request(body, ("schema_version", "run_id", "action_id", "challenge"), auth)
        if (not token(body["challenge"]) or not secrets.compare_digest(
                digest(body["challenge"]), r["challenge_digest"])):
            raise Rejected("Invalid challenge")
        if r["registration"] is not None:
            if r["registration"] != binding:
                raise Rejected("Conflicting registration")
            return {"receipt": r["action_id"], "bound": r["phase"] == "bound"}
        if r["phase"] not in ("sending", "uncertain"):
            raise Rejected("No attempted reservation")
        if self._now() >= r["expiry"]:
            self._hold("expired")
            raise Rejected("Expired challenge")
        prior = self.data["bindings"]
        if r["kind"] == Action.CONTINUE_CURRENT.value:
            if prior.get(r["source"]) != binding:
                raise Rejected("Continuation session changed")
        else:
            if any(x["session"] == binding["session"] or x["subject"] != binding["subject"]
                   for x in prior.values()):
                raise Rejected("Successor session or subject mismatch")
        r["registration"] = binding
        self._commit()
        return {"receipt": r["action_id"], "bound": False}

    @serialized
    def admit_delivery(self, observation: Delivery):
        """Independent observation is required; callback alone never increments."""
        self._usable()
        r = self.active
        if not r or r["phase"] not in ("sending", "uncertain", "bound"):
            raise Rejected("No attempted reservation")
        if type(observation) is not Delivery or not r["registration"]:
            return self._hold("delivery")
        binding = {"principal": observation.principal, "session": observation.session,
                   "subject": observation.subject}
        if (observation.observed is not True or observation.run_id != self.route.run_id
                or observation.action_id != r["action_id"] or observation.account_key != self.route.account_key
                or observation.project_id != self.route.project_id or not saved_id(observation.chat_id)
                or observation.prompt_digest != r["prompt_digest"] or binding != r["registration"]):
            return self._hold("delivery")
        cid = observation.chat_id
        if r["phase"] == "bound":
            return Action.IGNORE if cid == r["saved_chat"] else self._hold("conflict")
        if self.data["hold"] == "conflict":
            return Action.HOLD
        if r["kind"] == Action.CONTINUE_CURRENT.value:
            if cid != r["source"] or self.data["bindings"].get(cid) != binding:
                return self._hold("delivery")
        elif cid in self.data["bindings"] or self.count >= self.route.cap:
            return self._hold("delivery")
        if self.core is None:
            self.core = Controller(self._config(), cid)
        else:
            result = self.core.confirm(r["action_id"], cid, self.route.project_id, message_observed=True)
            if result.action != Action.WAIT:
                return self._hold("delivery")
        self.data["bindings"][cid] = binding
        r["saved_chat"] = cid
        r["phase"] = "bound"
        # Positive late receipt can reconcile the known delivery/count, never
        # rearm an expired response window or erase an existing deadline hold.
        if self.data["hold"] == "response_deadline" or self._response_expired(r):
            self.data["hold"] = "response_deadline"
            self._commit()
            return Action.HOLD
        self.data["hold"] = None
        self._commit()
        return Action.WAIT

    @serialized
    def report_worker(self, body, auth):
        r, binding = self._request(body, ("schema_version", "run_id", "action_id", "status",
                                           "publication_sha", "publication_branch"), auth)
        if r["phase"] != "bound" or r["registration"] != binding:
            raise Rejected("Worker not independently bound")
        if type(body["status"]) is not str or body["status"] not in {s.value for s in Status}:
            raise Rejected("Invalid status")
        status, commit, branch = body["status"], body["publication_sha"], body["publication_branch"]
        if status == Status.TASK_COMPLETE.value:
            if not sha(commit) or not branch_name(branch) or branch != self.route.branch:
                raise Rejected("Unauthorized or malformed publication")
        elif commit is not None or branch is not None:
            raise Rejected("Unexpected publication")
        report = {"status": status, "sha": commit, "branch": branch}
        if r["report"] is not None:
            if r["report"] == report:
                return "duplicate"
            self._hold("conflict")
            return "conflict"
        if self.terminal or self.data["hold"] == "conflict":
            raise Rejected("Terminal or conflicting run")
        r["report"] = report
        if self.data["hold"] == "response_deadline" or self._response_expired(r):
            self._hold("response_deadline")
            return "hold"
        self._commit()
        return "received"

    def _publication_ok(self, evidence, report, cid):
        if type(evidence) is not Remote or type(evidence.view) is not RepoView:
            return False
        v = evidence.view
        prior = self.data["prior_sha"]
        return (evidence.run_id == self.route.run_id and evidence.commit == report["sha"]
                and evidence.commit != prior and evidence.verified_ancestor == prior
                and v.repo == self.route.repo and v.branch == self.route.branch
                and v.last_chat_id == cid and v.published is True and v.readable is True
                and type(v.programme_complete) is bool
                and ((v.programme_complete and v.next_task is None)
                     or (not v.programme_complete and type(v.next_task) is str
                         and bool(v.next_task.strip())
                         and v.next_task.strip().upper() != "HOLD"
                         and v.next_task.strip() != "FINISHED")))

    @serialized
    def evaluate(self, quiet: Quiet | None, read_remote: Callable | None = None):
        """Only this controller-side method can turn a report into a core event."""
        self._usable()
        r = self.active
        if self.terminal:
            return Action.HOLD
        if self._response_expired(r):
            return self._hold("response_deadline")
        if self.data["paused"] or self.data["hold"]:
            return Action.HOLD
        if not r or r["phase"] != "bound" or not r["report"]:
            return Action.WAIT
        if r["consumed"]:
            return Action.IGNORE
        cid, report = r["saved_chat"], r["report"]
        if not self._quiet(quiet, r["action_id"], cid):
            return Action.WAIT
        evidence = None
        if report["status"] == Status.TASK_COMPLETE.value:
            try:
                args = (self.route.repo, self.route.branch, self.data["prior_sha"])
                first = read_remote(*args)
                second = read_remote(*args)
            except Exception:
                return self._hold("publication")
            if (not self._publication_ok(first, report, cid)
                    or not self._publication_ok(second, report, cid) or first != second):
                return self._hold("publication")
            evidence = first
        if (self.data["paused"] or self.data["hold"] or self.active is not r
                or r["consumed"] or (evidence and self.data["prior_sha"] != args[2])):
            return Action.HOLD
        # Independent reads may have taken time or exposed persisted-state loss.
        self._usable()
        if self._response_expired(r):
            return self._hold("response_deadline")
        # Action-scoped synthetic report anchor, never a claimed host message ID.
        outcome = self.core.consume(Response(cid, "mcp-report:" + digest(r["action_id"]),
                                             "CHAT_STATUS: " + report["status"],
                                             complete=True, project=self.route.project_id),
                                    evidence.view if evidence else None)
        r["consumed"] = True
        if evidence:
            self.data["prior_sha"] = evidence.commit
        self._commit()
        return outcome.action
