"""The house asking for a page to be drawn, and asking what came back on one.

Two routes, both called by the hub with its device key, and there is no route the other
way. The panel cannot put a page in front of anybody: it answers a request the house chose
to make, which is what keeps "a write from the panel is inert" true of paper as well.

What arrives is a page — a kind, a title, a note, labels, and what its drawing shows — or
two images. Neither carries a name, a profile or a learner, and there is no field in which
one could.
"""

from __future__ import annotations

import base64
import logging
import time
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from shared.errors import CloudUnavailable, NoCapacityError, SafetyBlocked
from shared.page import Page, PageError
from shared.routing import PageImage

from ..config import Settings
from ..gate import DeviceKey
from ..usage import (
    FAILED,
    KIND_IMAGE,
    KIND_READ,
    REFUSED,
    SERVED,
    UsageStore,
    event_from,
    over_cap,
)

router = APIRouter()


class PageToDraw(BaseModel):
    """What the afternoon says the page is. The drawing is decided from this and nothing else."""

    model_config = ConfigDict(extra="forbid")

    page: dict[str, Any] = Field(default_factory=dict)


class PagesToCompare(BaseModel):
    """The sheet as it was handed over, and what came off the glass.

    Two images and a sentence of context. There is no list of boxes, no id and no expected
    answer: the reading is "what is on the second that is not on the first".
    """

    model_config = ConfigDict(extra="forbid")

    blankBase64: str
    cameBackBase64: str
    width: int = 0
    height: int = 0
    about: str = ""


@router.post("/api/device/{household_id}/page")
async def draw_a_page(
    household_id: str, asked: PageToDraw, _: DeviceKey, request: Request
) -> Any:
    """Draw the whole page and hand it back as a PNG.

    A refusal is not an error the house has to explain. The moment it belongs to carries an
    ``instead``, written and screened when the afternoon was approved, so an afternoon whose
    page cannot be drawn carries on without paper.
    """
    settings: Settings = request.app.state.settings
    counter: UsageStore = request.app.state.usage
    if over_cap(counter, household_id, settings.monthly_call_cap):
        raise HTTPException(status_code=429, detail="monthly_cap_reached")

    try:
        page = Page.from_dict(asked.page)
    except PageError as exc:
        raise HTTPException(status_code=400, detail=f"not a page: {exc}") from exc

    from ..paper import draw_page

    spent: Any = None
    outcome = FAILED
    try:
        png, spent = await draw_page(page, now=time.time())
        outcome = SERVED
    except SafetyBlocked as exc:
        outcome = REFUSED
        logging.getLogger(__name__).info("page refused: %s", exc)
        raise HTTPException(status_code=422, detail="refused_by_the_gate") from exc
    except (NoCapacityError, CloudUnavailable, ValueError) as exc:
        logging.getLogger(__name__).warning("page not drawn: %s", exc)
        raise HTTPException(status_code=503, detail=f"unavailable: {exc}") from exc
    finally:
        _count(counter, household_id, KIND_IMAGE, outcome, spent)
    return {"imageBase64": base64.b64encode(png).decode()}


@router.post("/api/device/{household_id}/read-page")
async def read_a_page(
    household_id: str, pages: PagesToCompare, _: DeviceKey, request: Request
) -> Any:
    """Say what is on the sheet that was not on the blank.

    What comes back describes ink — a house drawn in the left box, three lines at the top —
    and whether it looks like the sheet that was handed over. It never says whether anything
    is right, and there is no field in which it could.
    """
    settings: Settings = request.app.state.settings
    counter: UsageStore = request.app.state.usage
    if over_cap(counter, household_id, settings.monthly_call_cap):
        raise HTTPException(status_code=429, detail="monthly_cap_reached")

    from ..paper import read_the_page

    blank = PageImage(
        png=base64.b64decode(pages.blankBase64), width=pages.width, height=pages.height
    )
    came_back = PageImage(
        png=base64.b64decode(pages.cameBackBase64), width=pages.width, height=pages.height
    )
    spent: Any = None
    outcome = FAILED
    try:
        came, spent = await read_the_page(
            blank, came_back, about=pages.about, now=time.time()
        )
        outcome = SERVED
    except (NoCapacityError, CloudUnavailable, ValueError) as exc:
        raise HTTPException(status_code=503, detail=f"unavailable: {exc}") from exc
    finally:
        _count(counter, household_id, KIND_READ, outcome, spent)
    return came.to_dict()


def _count(
    counter: UsageStore, household_id: str, kind: str, outcome: str, spent: Any
) -> None:
    """Write down what a call consumed. Never raises: the call was already made and paid
    for, so failing here would spend the money and deliver nothing."""
    from shared.ids import new_id

    try:
        counter.record(
            event_from(household_id, kind, outcome, spent, event_id=str(new_id("use")))
        )
    except Exception as exc:  # noqa: BLE001 - bookkeeping must not eat a page
        logging.getLogger(__name__).warning("usage not recorded: %s", exc)
