"""Offline regression model for the historical placeholder/draft ambiguity.

A real adapter must demonstrate that editable_text is *actual editable content*,
not the UIA Value merely renamed. Unknown observations remain unknown.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ComposerState(str, Enum):
    EMPTY = "EMPTY"
    DRAFT = "DRAFT"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ComposerObservation:
    editable_text: Optional[str] = None
    uia_value: Optional[str] = None
    placeholder: Optional[str] = None
    placeholder_visible: Optional[bool] = None
    attachments_present: Optional[bool] = False


def classify_composer(obs: ComposerObservation) -> ComposerState:
    if obs.attachments_present is True:
        return ComposerState.DRAFT
    if obs.attachments_present is None:
        return ComposerState.UNKNOWN
    if obs.editable_text is not None:
        # Do not trim real text, even if it equals a known placeholder.
        return ComposerState.EMPTY if obs.editable_text == "" else ComposerState.DRAFT
    # Value equality alone never proves empty. This evidence was missing in the
    # failed historical attempt. A live text/placeholder probe must resolve it.
    return ComposerState.UNKNOWN
