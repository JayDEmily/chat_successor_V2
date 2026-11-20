"""Windows UIA bridge for observation, view recovery and a single Send."""
from __future__ import annotations

from pathlib import Path
import json
import logging
import os
import re
import subprocess
import tempfile
import time

from runner import (
    Browser, Destination, PausedBeforeClick, SendBlockedBeforeClick, Submitted,
    WorkerAdvancedBeforeClick,
)
from succession.composer import ComposerObservation
from succession.core import Controller, Response


log = logging.getLogger(__name__)

STALE_VIEW_SECONDS = 120
VIEW_PROBE_INTERVAL_SECONDS = 300


def saved_chat_url(project: str, project_url: str | None, chat_id: str) -> str | None:
    if not isinstance(project_url, str) or not isinstance(chat_id, str):
        return None
    landing = re.fullmatch(
        r"(https://chatgpt[.]com/g/(g-p-[a-f0-9]+)(?:-[A-Za-z0-9-]+)?)/project/?",
        project_url,
    )
    if (landing is None or landing[2] != project
            or not re.fullmatch(r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}", chat_id)):
        return None
    return f"{landing[1]}/c/{chat_id}"


class BrowserObservationError(RuntimeError):
    pass


class WindowsUIA(Browser):
    def __init__(self, project: str, project_name: str, script: Path,
                 state_path: Path, *, powershell: str = "powershell.exe",
                 project_url: str | None = None, profile_path: str | None = None):
        self.project = project
        self.project_name = project_name
        self.project_url = project_url
        self.profile_path = profile_path
        self.script = Path(script)
        self.state_path = Path(state_path)
        self.target_path = self.state_path.with_suffix(".uia-target.json")
        self.powershell = powershell
        self._progress = None
        self._progress_since = 0.0
        self._last_view_probe: dict[str, float] = {}

    def _invoke(self, mode: str, **arguments) -> dict:
        cmd = [self.powershell, "-STA", "-NoProfile",
               "-NonInteractive", "-ExecutionPolicy", "Bypass",
               "-File", str(self.script), "-Mode", mode,
               "-ProjectId", self.project, "-ProjectName", self.project_name]
        for name, value in arguments.items():
            if type(value) is bool:
                # PowerShell switch parameters are flags, not "-Flag True".
                if value:
                    cmd.append(f"-{name}")
            elif value is not None:
                cmd.extend([f"-{name}", str(value)])
        chat = arguments.get("ChatId", "-")
        for attempt in range(2):
            log.info("uia_start mode=%s chat=%s", mode, chat)
            started = time.monotonic()
            environment = None
            if self.profile_path is not None:
                environment = os.environ.copy()
                environment["CHAT_SUCCESSION_CHROME_PROFILE_PATH"] = self.profile_path
            result = subprocess.run(cmd, text=True, capture_output=True,
                                    encoding="utf-8", errors="replace", timeout=90,
                                    **({"env": environment} if environment is not None else {}))
            log.info("uia_exit mode=%s chat=%s seconds=%.2f code=%d",
                     mode, chat, time.monotonic() - started, result.returncode)
            if result.returncode:
                raise BrowserObservationError(
                    f"Windows UIA {mode} failed ({result.returncode}): "
                    + result.stderr.strip()[-600:])
            try:
                payload = json.loads(result.stdout.strip())
            except json.JSONDecodeError as exc:
                if mode != "Observe" or attempt:
                    raise BrowserObservationError(
                        f"Windows UIA {mode} returned unparseable output") from exc
                log.warning("uia_observation_retry chat=%s position=%d error=%s",
                            chat, exc.pos, exc.msg)
            else:
                break
        if not isinstance(payload, dict):
            raise BrowserObservationError("Windows UIA output is not an object")
        if mode == "Observe":
            log.info("observation chat=%s ready=%s reason=%s",
                     chat, payload.get("ready"), payload.get("reason"))
        return payload

    def _worker_error(self, chat_id: str, reason: str) -> BrowserObservationError:
        url = saved_chat_url(self.project, self.project_url, chat_id)
        return BrowserObservationError(f"{reason} Saved chat: {url}" if url else reason)

    def _worker_view(self, mode: str, chat_id: str, **arguments) -> dict:
        try:
            payload = self._invoke(mode, ChatId=chat_id, **arguments)
        except (OSError, subprocess.SubprocessError, BrowserObservationError) as exc:
            raise self._worker_error(chat_id, str(exc)) from exc
        status = payload.get("view_status", "observed")
        if mode in ("Observe", "ObserveReentry", "RecoverView") or status != "observed":
            if payload.get("project") != self.project or payload.get("chat_id") != chat_id:
                raise self._worker_error(chat_id, "Chrome did not verify the registered Project and worker.")
        if status == "ambiguous":
            raise self._worker_error(chat_id, "Multiple accessible Chrome views show the same saved worker.")
        if status not in ("observed", "missing"):
            raise self._worker_error(chat_id, "Chrome view status was not verified.")
        return payload

    def _recover_view(self, chat_id: str, recovery: str, *, release_pause=False, **arguments) -> str:
        if recovery == "missing" and not saved_chat_url(self.project, self.project_url, chat_id):
            raise self._worker_error(chat_id, "Chrome could not reopen the worker without a verified Project and saved chat ID.")
        pause_path = None if release_pause else self.state_path.with_suffix(".pause").resolve()
        payload = self._worker_view("RecoverView", chat_id, Recovery=recovery,
                                    ProjectUrl=self.project_url, PausePath=pause_path, **arguments)
        status = payload.get("recovery_status")
        if status == "paused":
            raise self._worker_error(chat_id, "Operator pause requested before Chrome view recovery.")
        allowed = ("restored",) if recovery == "missing" else ("refreshed", "waiting")
        if status not in allowed:
            raise self._worker_error(chat_id, "Chrome could not verify recovery of the saved worker view.")
        log.info("worker_view_recovery chat=%s outcome=%s", chat_id, status)
        return status

    def _read_or_restore_worker(self, mode: str, chat_id: str, *, release_pause=False, **arguments) -> dict:
        payload = self._worker_view(mode, chat_id, **arguments)
        if payload.get("view_status") == "missing":
            self._recover_view(chat_id, "missing", release_pause=release_pause)
            payload = self._worker_view(mode, chat_id, **arguments)
            if payload.get("view_status") == "missing":
                raise self._worker_error(chat_id, "The saved worker view disappeared after recovery.")
        return payload

    def _response_was_consumed(self, chat_id: str, response_id: str | None) -> bool:
        if not response_id or not self.state_path.exists():
            return False
        state = json.loads(self.state_path.read_text(encoding="utf-8"))["state"]
        return [chat_id, response_id] in state.get("consumed_responses", ())

    def _probe_stale_view(self, chat_id: str, turn: dict) -> bool:
        handle = turn.get("window_handle")
        if type(handle) is not int or handle <= 0:
            return False
        fingerprint = (chat_id, handle, turn.get("response_id"), turn.get("ready"),
                       turn.get("stop_control"), turn.get("user_after_assistant"),
                       turn.get("user_turn_count"), turn.get("latest_user_digest"))
        now = time.monotonic()
        if fingerprint != self._progress:
            self._progress, self._progress_since = fingerprint, now
            return False
        if (now - self._progress_since < STALE_VIEW_SECONDS
                or now - self._last_view_probe.get(chat_id, -float("inf")) < VIEW_PROBE_INTERVAL_SECONDS):
            return False
        self._last_view_probe[chat_id] = now
        status = self._recover_view(chat_id, "stale", WindowHandle=handle,
                                    SourceResponse=turn.get("response_id"))
        if status == "refreshed":
            self._progress = None
        return True

    def observe(self, expected_chat_id: str) -> Response | None:
        first = self._read_or_restore_worker("Observe", expected_chat_id)
        ready = first.get("ready") is True
        if not ready or self._response_was_consumed(expected_chat_id, first.get("response_id")):
            if self._probe_stale_view(expected_chat_id, first) or not ready:
                return None
        else:
            self._progress = None
        # Check independent read-back of the exact completed turn at a later poll.
        time.sleep(1.2)
        second = self._worker_view("Observe", expected_chat_id)
        if not second.get("ready") or second != first:
            log.info("response_readback_changed chat=%s", expected_chat_id)
            return None
        if (second.get("project") != self.project or
                second.get("chat_id") != expected_chat_id or
                not second.get("response_id") or
                not isinstance(second.get("text"), str)):
            raise BrowserObservationError("Assistant identity/Project not established")
        return Response(chat_id=second["chat_id"], response_id=second["response_id"],
                        text=second["text"], complete=True,
                        role=second["role"], project=second["project"],
                        handoff_locator_verified=second.get("handoff_locator_verified") is True)

    def prepare(self, kind: str, current_chat_id: str | None) -> Destination:
        navigation = {}
        if kind == "LAUNCH_SUCCESSOR" and current_chat_id is not None and self.state_path.exists():
            state = json.loads(self.state_path.read_text(encoding="utf-8"))["state"]
            pending = state.get("pending")
            if (pending and pending["kind"] == kind and pending["source_chat_id"] == current_chat_id
                    and pending["phase"] == "prepared"):
                navigation = {
                    "SourceResponse": pending["response_id"], "PrepareAction": pending["action_id"],
                    "PrepareTargetPath": self.target_path.resolve(),
                }
                if self.target_path.exists():
                    previous = json.loads(self.target_path.read_text(encoding="utf-8"))
                    if (previous.get("kind") == kind and previous.get("source") == current_chat_id
                            and previous.get("action_id") == pending["action_id"]
                            and type(previous.get("handle")) is int and previous["handle"] > 0):
                        navigation["WindowHandle"] = previous["handle"]
        arguments = {"Kind": kind, "ProjectUrl": self.project_url, **navigation}
        if kind == "CONTINUE_CURRENT" and current_chat_id:
            payload = self._read_or_restore_worker("Prepare", current_chat_id, **arguments)
        else:
            payload = self._invoke("Prepare", ChatId=current_chat_id, **arguments)
        if payload.get("project") != self.project:
            raise BrowserObservationError("Prepared wrong Project")
        handle = payload.get("private_window_handle")
        if type(handle) is not int or handle <= 0:
            raise BrowserObservationError("Prepared window handle absent")
        expected_chat = current_chat_id if kind == "CONTINUE_CURRENT" else None
        if payload.get("current_chat_id") != expected_chat:
            raise BrowserObservationError("Prepared composer does not belong to the nominated destination")
        target = Destination(project=payload["project"],
                             current_chat_id=payload.get("current_chat_id"),
                             composer=ComposerObservation(
                                 editable_text=payload.get("editable_text"),
                                 uia_value=payload.get("uia_value"),
                                 attachments_present=payload.get("attachments_present", None)),
                             private_window_handle=handle)
        record = {"kind": kind, "source": current_chat_id, "handle": target.private_window_handle}
        if navigation:
            record["action_id"] = navigation["PrepareAction"]
        self._atomic_target_write(record)
        return target

    def reentry_disposition(self, chat_id: str, anchor: str, *, release_pause=False) -> str:
        observed = self._read_or_restore_worker("ObserveReentry", chat_id, release_pause=release_pause,
                                               OwnerAnchor=anchor)
        if observed.get("project") != self.project or observed.get("chat_id") != chat_id:
            raise BrowserObservationError("Re-entry did not identify the saved worker")
        disposition = observed.get("disposition")
        if disposition not in ("idle", "advanced"):
            raise BrowserObservationError("Re-entry could not establish the current worker's turn")
        return disposition

    def _atomic_target_write(self, record: dict):
        self.target_path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp = tempfile.mkstemp(dir=self.target_path.parent, prefix="uia-")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(record, f, sort_keys=True)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp, self.target_path)
        finally:
            if os.path.exists(temp):
                os.unlink(temp)

    def send_once(self, target: Destination, message: str) -> Submitted:
        # Explicitly validate persisted controller state BEFORE calling Send.
        # Controller.load intentionally holds a persisted 'sending' state as
        # a *restart* precaution. The same-process sender must validate the
        # on-disk phase without asking Controller.load to reconcile it.
        raw = json.loads(self.state_path.read_text(encoding="utf-8"))
        state = raw.get("state", {})
        p = state.get("pending")
        if (not isinstance(p, dict) or p.get("phase") != "sending" or
                p.get("message") != message or state.get("halted")):
            raise BrowserObservationError("No matching persisted sending phase")
        record = json.loads(self.target_path.read_text(encoding="utf-8"))
        if (record.get("handle") != target.private_window_handle or
                record.get("kind") != p["kind"] or
                record.get("source") != p["source_chat_id"]):
            raise BrowserObservationError("Prepared window identity mismatch")
        # L09 test-only fault points. Set this only for a bounded test CLI
        # process; normal controller runs have no injection.
        fault = os.environ.get("ASTRA_L09_FAULT", "")
        if fault not in ("", "before_click", "after_click"):
            raise BrowserObservationError("Unknown L09 fault point")
        if fault == "before_click":
            raise BrowserObservationError(
                "L09 injected after durable sending but before UIA Send; no click")
        result = self._invoke(
            "Send", Kind=p["kind"], ChatId=p["source_chat_id"],
            WindowHandle=target.private_window_handle, Message=message,
            PausePath=self.state_path.with_suffix(".pause").resolve(),
            SourceResponse=p["response_id"] if p["kind"] == "CONTINUE_CURRENT" else None,
            L09Fault="after_click" if fault == "after_click" else None)
        if result.get("paused_before_click") is True:
            raise PausedBeforeClick("Operator pause requested before Send")
        if result.get("destination_changed_before_click") is True:
            raise SendBlockedBeforeClick("Chrome destination changed before Send. Preserve any draft.")
        if result.get("worker_advanced_before_click") is True:
            raise WorkerAdvancedBeforeClick()
        return Submitted(project=result.get("project", ""),
                         chat_id=result.get("chat_id"),
                         submitted_text=result.get("submitted_text"),
                         posted_message_observed=result.get("posted_message_observed") is True)

    def reconcile_readonly(self) -> Submitted:
        saved = Controller.load(self.state_path)
        p = saved.state.pending
        if p is None or p.phase not in ("sending", "uncertain"):
            raise BrowserObservationError("No possibly sent action to reconcile")
        record = json.loads(self.target_path.read_text(encoding="utf-8"))
        if record.get("source") != p.source_chat_id or record.get("kind") != p.kind:
            raise BrowserObservationError("Saved target is for a different action")
        result = self._invoke("Reconcile", WindowHandle=record["handle"],
                              Kind=p.kind, ChatId=p.source_chat_id,
                              SourceResponse=p.response_id if p.kind == "CONTINUE_CURRENT" else None,
                              Message=p.message)
        return Submitted(project=result.get("project", ""),
                         chat_id=result.get("chat_id"),
                         submitted_text=result.get("submitted_text"),
                         posted_message_observed=result.get("posted_message_observed") is True)
