"""Route a scoped owner request to the one registered worker."""
from __future__ import annotations

import hashlib
import json
import os

from cli import exclusive_lock, load_config, read_pause_marker, release_pause_marker
from runner import inspect_state, owner_pause_reason, read_verified_owner_input
from succession.core import Config, Controller


def record_context(state_path, context):
    request_id = context["request_id"]
    path = state_path.with_name(f"owner-{request_id}.json")
    receipt = path.with_suffix(".sha256")
    if path.exists():
        body = path.read_bytes()
        if json.loads(body.decode("utf-8")) != context:
            raise ValueError("Owner request ID already has different content")
    else:
        body = json.dumps(context, ensure_ascii=False, sort_keys=True).encode("utf-8")
    digest = hashlib.sha256(body).hexdigest()
    if receipt.exists() and receipt.read_text(encoding="ascii").strip() != digest:
        raise ValueError("Owner request differs from its durable input receipt")
    # The run lock serializes both writes. An interrupted intake can finish
    # only when the explicit retry matches the existing content or receipt.
    for destination, data in ((path, body), (receipt, (digest + "\n").encode("ascii"))):
        if destination.exists():
            continue
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        with temporary.open("wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(destination)
    return request_id


def accepted_context(state_path, controller, incoming):
    for request_id, anchor in controller.state.owner_requests.items():
        same_id = request_id == incoming["request_id"]
        if not same_id and anchor != [incoming["worker_id"], incoming["response_id"]]:
            continue
        saved = state_path.with_name(f"owner-{request_id}.json")
        if read_verified_owner_input(saved) != {**incoming, "request_id": request_id}:
            raise ValueError("The same hold already has an owner decision with different content")
        return request_id
    return None


def resume_request(cfg_path, state_path, request, name, dependencies, start):
    cfg = load_config(cfg_path)
    context = request.get("owner_context")
    expected = Config(cfg["project"], cfg["repo"], cfg["branch"], cfg["max_unique_chats"])
    name_changed = cfg["project_name"] != name
    cfg["project_name"] = name
    browser, reader = dependencies(cfg, state_path)
    pause = state_path.with_suffix(".pause")
    event = "controller_resumed"
    with exclusive_lock(state_path):
        c = Controller.load(state_path)
        if c.config != expected:
            raise ValueError("Persisted controller configuration does not match run")
        result = {"run_id": cfg["run_id"], **inspect_state(state_path)}
        p = c.state.pending
        accepted = accepted_context(state_path, c, context) if context else None
        if accepted:
            event = ("owner_request_already_recorded" if context["request_id"] == accepted
                     else "owner_hold_already_handled")
            if p is None or p.owner_request_id != accepted:
                if c.state.halted or p is not None:
                    return {**result, "event": event}
            if (p is not None and p.phase == "prepared" and c.state.halted
                    and not request.get("release_pause")):
                return {**result, "event": "owner_request_prepared"}
            context = None
        if c.state.halted in ("programme_finished", "chat_cap"):
            raise ValueError("Finished or capped runs cannot resume")
        observed_pause = read_pause_marker(pause)
        if observed_pause is not None and request.get("release_pause") is not True:
            raise ValueError("The separate operator pause is still in effect")
        if p and p.phase in ("sending", "uncertain"):
            receipt = browser.reconcile_readonly()
            if (receipt.posted_message_observed is not True or receipt.submitted_text != p.message
                    or not receipt.chat_id or receipt.project != cfg["project"]):
                return {**result, "event": "send_requires_reconciliation"}
            c.confirm(p.action_id, receipt.chat_id, receipt.project)
            c.save(state_path)
            if c.state.pending:
                return {**result, "event": "send_requires_reconciliation"}
            if context and context["request_id"] != p.owner_request_id:
                return {**result, "event": "send_reconciled_retry_selection"}
            event = "controller_resumed"
        elif p and context:
            raise ValueError("The existing prepared action may conflict with the new owner scope")
        elif context:
            worker, anchor = context["worker_id"], context["response_id"]
            if (worker != c.state.current_chat_id or c.state.consumed_responses[-1:] != [[worker, anchor]]
                    or not c.state.halted):
                raise ValueError("The owner request no longer matches the observed worker and hold")
            disposition = browser.reentry_disposition(worker, anchor, release_pause=request.get("release_pause", False))
            if disposition == "idle":
                request_id = record_context(state_path, context)
                pointer = (f"Continue the approved work in GitHub repo {cfg['repo']}, "
                           f"branch {c.checkpoint_branch}."
                           + reader.instructions(cfg["run_id"], c.unique_count, request_id))
                c.continue_after_owner(request_id, anchor, pointer)
            else:
                # Observation showed the saved worker advanced, but did not
                # establish that this owner decision was delivered. Resume
                # observation only; do not claim an approval receipt or Send.
                event = "worker_advanced_owner_input_unverified"
                c.resume_after_owner()
        else:
            c.resume_after_owner()
        if request.get("release_pause") and not release_pause_marker(pause, observed_pause):
            c.pause(owner_pause_reason(state_path))
            c.save(state_path)
            return {"run_id": cfg["run_id"], **inspect_state(state_path), "event": "pause_preserved"}
        c.save(state_path)
        if name_changed:
            config_pending = cfg_path.with_suffix(".tmp")
            config_pending.write_text(json.dumps(cfg), encoding="utf-8")
            config_pending.replace(cfg_path)
        result = {"run_id": cfg["run_id"], **inspect_state(state_path)}
    pid = start(cfg_path, state_path)
    return {**result, "event": event, "controller_pid": pid}
