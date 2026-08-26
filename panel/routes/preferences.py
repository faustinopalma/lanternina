"""What the content is made of: interests, what to avoid, difficulty, language.

These are the fields the hub may put in a prompt, and the list is closed on purpose — a
body carrying something we do not store is refused rather than dropped, so it cannot look
as though it was saved.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from ..gate import CurrentAccount, DeviceKey
from ..preferences import PreferencesStore, clean_preferences

router = APIRouter()


class NewPreferences(BaseModel):
    """What the content is made of. These are the fields the hub may put in a prompt.

    Unknown fields are refused rather than dropped: a body carrying a name would
    otherwise be accepted and quietly ignored, which reads as working.
    """

    model_config = ConfigDict(extra="forbid")

    interests: list[str] = Field(default_factory=list)
    avoid: list[str] = Field(default_factory=list)
    difficulty: str
    variety: str
    maxWordsPerLine: int
    language: str


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
        chosen = clean_preferences(
            str(account.household_id),
            interests=new.interests,
            avoid=new.avoid,
            difficulty=new.difficulty,
            variety=new.variety,
            max_words_per_line=new.maxWordsPerLine,
            language=new.language,
            updated_by=str(account.id),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return store.set(chosen).to_public()


@router.get("/api/device/{household_id}/preferences")
def device_preferences(household_id: str, _: DeviceKey, request: Request) -> Any:
    """The settings the hub generates from, as the parent last left them. The hub adds
    the name locally; nothing that identifies a person has a field on this route."""
    store: PreferencesStore = request.app.state.preferences
    return store.get(household_id).to_public()
