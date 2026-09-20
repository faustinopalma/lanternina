"""What the content is made of: interests, what to avoid, the language, the note.

These are the fields the hub may put in a prompt, and the list is closed on purpose — a
body carrying something we do not store is refused rather than dropped, so it cannot look
as though it was saved.

The shape and the variety were two of these fields until 4 September 2026 and are gone; a
body that still sends them is refused by ``extra="forbid"``, which is the behaviour worth
having — an old browser is told rather than quietly steering with a field nobody reads.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict

from ..gate import CurrentAccount, DeviceKey
from ..preferences import DEFAULT_SHEETS, PreferencesStore, clean_preferences
from ..steering import SteeringConflict

router = APIRouter()


class NewPreferences(BaseModel):
    """What the content is made of. These are the fields the hub may put in a prompt.

    Unknown fields are refused rather than dropped: a body carrying a name would
    otherwise be accepted and quietly ignored, which reads as working.
    """

    model_config = ConfigDict(extra="forbid")

    interests: list[str] | None = None
    avoid: list[str] | None = None
    language: str
    # How many sheets one afternoon may put on the table. A ceiling, not a target.
    sheets: int = DEFAULT_SHEETS
    # What is true in this house at the moment. Saving it is what renews it; sending it
    # empty is what ends it early.
    note: str = ""


@router.get("/api/preferences")
def read_preferences(account: CurrentAccount, request: Request) -> Any:
    store: PreferencesStore = request.app.state.preferences
    return store.get(str(account.household_id)).to_public()


@router.post("/api/preferences")
def write_preferences(new: NewPreferences, account: CurrentAccount, request: Request) -> Any:
    """Record what the content is made of. It persists and returns: the hub reads it
    on its next run, and nothing here starts a generation."""
    store: PreferencesStore = request.app.state.preferences
    try:
        household = str(account.household_id)
        current = store.get(household)
        chosen = clean_preferences(
            household,
            interests=list(current.interests) if new.interests is None else new.interests,
            avoid=list(current.avoid) if new.avoid is None else new.avoid,
            language=new.language,
            sheets=new.sheets,
            note=new.note,
            updated_by=str(account.id),
        )
        guidance_store = request.app.state.steering
        guidance_store.get(household, current.language)
        if current.language != new.language:
            target = guidance_store.get(household, new.language)
            if not target.topics_consolidated:
                guidance_store.save(target, target.revision)
        if new.interests is not None or new.avoid is not None:
            guidance = guidance_store.get(household, new.language)
            guidance_store.save(guidance.edited(
                guidance.steering.instructions, guidance.steering.adaptive,
                topics=None if new.interests is None else "\n".join(chosen.interests),
                avoid=None if new.avoid is None else "\n".join(chosen.avoid),
            ), guidance.revision)
    except SteeringConflict as exc:
        raise HTTPException(status_code=409, detail="guidance_changed") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return store.set(chosen).to_public()


@router.get("/api/device/{household_id}/preferences")
def device_preferences(household_id: str, _: DeviceKey, request: Request) -> Any:
    """The settings the hub generates from, as the parent last left them. The hub adds
    the name locally; nothing that identifies a person has a field on this route."""
    store: PreferencesStore = request.app.state.preferences
    return store.get(household_id).to_public()
