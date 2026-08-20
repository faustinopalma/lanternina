"""The subjects the pictures may be about, approved once by the parent.

The parent approves the theme, not each image. That is what makes a picture a day possible
without somebody signing off four sentences before breakfast.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from ..gate import CurrentAccount, DeviceKey
from ..themes import ThemeStore, clean_label, make_theme

router = APIRouter()


class NewTheme(BaseModel):
    label: str


@router.get("/api/themes")
def list_themes(account: CurrentAccount, request: Request) -> Any:
    themes: ThemeStore = request.app.state.themes
    return {"themes": [row.to_public() for row in themes.list(str(account.household_id))]}


@router.post("/api/themes")
def add_theme(new: NewTheme, account: CurrentAccount, request: Request) -> Any:
    """Approve a subject the pictures may be about. It starts nothing on its own."""
    themes: ThemeStore = request.app.state.themes
    try:
        label = clean_label(new.label)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    theme = themes.add(make_theme(str(account.household_id), label, str(account.id)))
    return theme.to_public()


@router.post("/api/themes/{theme_id}/remove")
def remove_theme(theme_id: str, account: CurrentAccount, request: Request) -> Any:
    themes: ThemeStore = request.app.state.themes
    try:
        theme = themes.remove(str(account.household_id), theme_id)
    except Exception as exc:  # storage SDKs raise their own not-found types
        raise HTTPException(status_code=404, detail="unknown_theme") from exc
    return theme.to_public()


@router.get("/api/device/{household_id}/themes")
def device_themes(household_id: str, _: DeviceKey, request: Request) -> Any:
    """What the home server may paint about, as the parent last left it."""
    themes: ThemeStore = request.app.state.themes
    return {"themes": [row.to_public() for row in themes.list(household_id)]}
