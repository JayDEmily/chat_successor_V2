"""Windows UIA bridge for the existing Chrome navigation/Send method.

The PowerShell script performs no implicit retries. Its prepared window handle
is persisted locally for read-only reconciliation after a lost acknowledgement.
"""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import json
import logging
import os
import subprocess
import tempfile
import time

from runner import Browser, Destination, PausedBeforeClick, Submitted, WorkerAdvancedBeforeClick
from succession.composer import ComposerObservation
from succession.core import Controller, Response


log = logging.getLogger(__name__)


class BrowserObservationError(RuntimeError):
    pass


class WindowsUIA(Browser):
    def __init__(self, project: str, project_name: str, script: Path,
                 state_path: Path, *, powershell: str = "powershell.exe", project_url: str | None = None):
        self.project = project
        self.project_name = project_name
        self.project_url = project_url
        self.script = Path(script)
        self.state_path = Path(state_path)
        self.target_path = self.state_path.with_suffix(".uia-target.json")
        self.powershell = powershell

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
        log.info("uia_start mode=%s chat=%s", mode, chat)
        started = time.monotonic()
        result = subprocess.run(cmd, text=True, capture_output=True,
                                encoding="utf-8", errors="replace", timeout=90)
        log.info("uia_exit mode=%s chat=%s seconds=%.2f code=%d",
                 mode, chat, time.monotonic() - started, result.returncode)
        if result.returncode:
            raise BrowserObservationError(
                f"Windows UIA {mode} failed ({result.returncode}): "
                + result.stderr.strip()[-600:])
        try:
            payload = json.loads(result.stdout.strip())
        except json.JSONDecodeError as exc:
            raise BrowserObservationError(
                f"Windows UIA {mode} returned unparseable output") from exc
        if not isinstance(payload, dict):
            raise BrowserObservationError("Windows UIA output is not an object")
        if mode == "Observe":
            log.info("observation chat=%s ready=%s reason=%s",
                     chat, payload.get("ready"), payload.get("reason"))
        return payload

    def observe(self, expected_chat_id: str) -> Response | None:
        first = self._invoke("Observe", ChatId=expected_chat_id)
        if not first.get("ready"):
            return None
        # Check independent read-back of the exact completed turn at a later poll.
        time.sleep(1.2)
        second = self._invoke("Observe", ChatId=expected_chat_id)
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
        payload = self._invoke("Prepare", Kind=kind, ChatId=current_chat_id, ProjectUrl=self.project_url)
        if payload.get("project") != self.project:
            raise BrowserObservationError("Prepared wrong Project")
        if type(payload.get("private_window_handle")) is not int:
            raise BrowserObservationError("Prepared window handle absent")
        target = Destination(project=payload["project"],
                             current_chat_id=payload.get("current_chat_id"),
                             composer=ComposerObservation(
                                 editable_text=payload.get("editable_text"),
                                 uia_value=payload.get("uia_value"),
                                 attachments_present=payload.get("attachments_present", None)),
                             private_window_handle=payload["private_window_handle"])
        self._atomic_target_write({"kind": kind, "source": current_chat_id,
                                   "handle": target.private_window_handle})
        return target

    def reentry_disposition(self, chat_id: str, anchor: str) -> str:
        observed = self._invoke("ObserveReentry", ChatId=chat_id, OwnerAnchor=anchor)
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
            OwnerAnchor=p["response_id"] if p.get("owner_request_id") else None,
            L09Fault="after_click" if fault == "after_click" else None)
        if result.get("paused_before_click") is True:
            raise PausedBeforeClick("Operator pause requested before Send")
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
                              Message=p.message)
        return Submitted(project=result.get("project", ""),
                         chat_id=result.get("chat_id"),
                         submitted_text=result.get("submitted_text"),
                         posted_message_observed=result.get("posted_message_observed") is True)
