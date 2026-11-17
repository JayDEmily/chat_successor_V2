"""Explicitly fake UI side effects; no network/browser dependencies."""
from dataclasses import dataclass
from .core import Action, Controller
from .composer import ComposerObservation, ComposerState, classify_composer


@dataclass(frozen=True)
class ObservedSend:
    chat_id: str
    project: str
    message_observed: bool = True


class FakeBrowser:
    def __init__(self, project: str, current_chat_id: str = "c1"):
        self.project = project
        self.current_chat_id = current_chat_id
        self.sends = []
        self.opens = 0
        self.next_id = 2

    def perform(self, controller: Controller, state_path=None, *,
                actual_project=None, editable_text="", fault=None):
        """Simulate ready -> save -> send -> observation, with injected failures.

        fault='before_click': known, definitive not-sent; left for explicit repair.
        fault='after_click': side effect occurs, acknowledgement lost.
        fault='after_observation': acknowledgement exists but is not saved/applied.
        """
        pending = controller.state.pending
        if pending is None:
            raise ValueError("No planned action")
        actual_project = self.project if actual_project is None else actual_project
        if actual_project != controller.config.project:
            controller.pause("Composer not in nominated Project")
            if state_path is not None:
                controller.save(state_path)
            return None
        if classify_composer(ComposerObservation(editable_text=editable_text)) != ComposerState.EMPTY:
            controller.pause("Preserve an existing or ambiguous draft")
            if state_path is not None:
                controller.save(state_path)
            return None
        controller.begin_send(pending.action_id)
        if state_path is not None:
            controller.save(state_path)
        if fault == "before_click":
            controller.uncertain(pending.action_id, "Injected failure before click; no click occurred")
            if state_path is not None:
                controller.save(state_path)
            return None
        if pending.kind == Action.LAUNCH_SUCCESSOR.value:
            self.opens += 1
            cid = f"c{self.next_id}"
            self.next_id += 1
            self.current_chat_id = cid
        else:
            cid = pending.source_chat_id
        receipt = ObservedSend(cid, actual_project)
        self.sends.append({
            "action_id": pending.action_id, "chat_id": cid,
            "project": actual_project, "message": pending.message,
            "kind": pending.kind,
        })
        if fault == "after_click":
            controller.uncertain(pending.action_id, "Injected lost acknowledgement after click")
            if state_path is not None:
                controller.save(state_path)
            return None
        if fault == "after_observation":
            return receipt
        controller.confirm(pending.action_id, cid, actual_project)
        if state_path is not None:
            controller.save(state_path)
        return receipt
