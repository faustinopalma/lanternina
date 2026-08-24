"""How far the house may improvise here, written by the parent.

Two routes and no third. The parent reads what this household has said and writes it
again; there is no route for the house, because the house never asks for these on their
own — they are read on the continuing path, inside the answer to a request the house made
about a page that came off its own glass. A separate route would be a second place that
decides what the model is told.

`panel/guidelines.py` says why the fixed bounds have no field: they go out beside the
parent's so that what they are adding to is legible, and a body carrying them is refused
rather than ignored.

Writing is inert, like every other write here. One row changes and nothing else happens.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from ..gate import CurrentAccount
from ..guidelines import GuidelineStore, clean_lines

router = APIRouter()


class NewGuidelines(BaseModel):
    """The parent's lines, and only those.

    ``extra="forbid"`` is what keeps `fixed` read-only: it goes out on every read, so a
    browser sending back what it received would otherwise look as though it had edited
    ours. It is refused instead.
    """

    model_config = ConfigDict(extra="forbid")

    lines: list[str] = Field(default_factory=list)


@router.get("/api/guidelines")
def read_guidelines(account: CurrentAccount, request: Request) -> Any:
    store: GuidelineStore = request.app.state.guidelines
    return store.get(str(account.household_id)).to_public()


@router.post("/api/guidelines")
def write_guidelines(new: NewGuidelines, account: CurrentAccount, request: Request) -> Any:
    """Record how far this house may improvise. Nothing is generated and nothing is sent."""
    store: GuidelineStore = request.app.state.guidelines
    try:
        said = clean_lines(
            str(account.household_id), new.lines, updated_by=str(account.id)
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return store.set(said).to_public()
