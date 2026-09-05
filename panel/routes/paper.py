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

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from shared.errors import CloudUnavailable, NoCapacityError, SafetyBlocked
from shared.ids import new_id
from shared.page import Page, PageError
from shared.routing import PageImage

from ..config import Settings
from ..gate import DeviceKey
from ..pictures import PictureArchive, PictureRecord
from ..profiles import NoticedStore
from ..trail import WHAT_WAS_DRAWN, TrailStore
from ..usage import (
    FAILED,
    KIND_IMAGE,
    KIND_PLACE,
    KIND_READ,
    REFUSED,
    SERVED,
    UsageStore,
    at_the_limit,
    event_from,
)
from .trail import filed

router = APIRouter()


class PageToDraw(BaseModel):
    """What the afternoon says the page is. The drawing is decided from this and nothing else."""

    model_config = ConfigDict(extra="forbid")

    page: dict[str, Any] = Field(default_factory=dict)
    # Which afternoon this belongs to, so the drawing can be filed under it. Absent means a
    # caller that predates the field, and the page is still drawn: a record is worth less
    # than a page reaching the table.
    runId: str = ""


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
    household_id: str, wanted: PageToDraw, _: DeviceKey, request: Request
) -> Any:
    """Draw the whole page and hand it back as a PNG.

    A refusal is not an error the house has to explain. The moment it belongs to carries an
    ``instead``, written and screened when the afternoon was approved, so an afternoon whose
    page cannot be drawn carries on without paper.
    """
    settings: Settings = request.app.state.settings
    counter: UsageStore = request.app.state.usage
    if at_the_limit(counter, request.app.state.limit, household_id, settings.monthly_limit):
        raise HTTPException(status_code=429, detail="monthly_cap_reached")

    try:
        page = Page.from_dict(wanted.page)
    except PageError as exc:
        raise HTTPException(status_code=400, detail=f"not a page: {exc}") from exc

    from ..paper import draw_page

    spent: Any = None
    outcome = FAILED
    try:
        png, asked, spent = await draw_page(page, now=time.time())
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
    _keep_the_drawing(request, household_id, wanted.runId, png, page, asked)
    return {"imageBase64": base64.b64encode(png).decode()}


def _keep_the_drawing(
    request: Request,
    household_id: str,
    run_id: str,
    png: bytes,
    page: Page,
    asked: str,
) -> None:
    """File the sheet as an image, under the afternoon, beside what was asked for.

    Recording happens where generating happens, and until 5 September 2026 this was the one
    generation that happened nowhere: the PNG went back to the house and no copy and no
    request survived, so a parent could read the words a page carried but never see the page
    or why it looked the way it did.

    Never raises. The page has already been drawn and paid for, and a record that could fail
    the request would be a record with a hold over an afternoon.
    """
    if not run_id:
        return
    archive: PictureArchive = request.app.state.pictures
    trail: TrailStore = request.app.state.trail
    now = time.time()
    picture_id = str(new_id("pic"))
    try:
        archive.save(
            PictureRecord(
                id=picture_id,
                household_id=household_id,
                theme=page.title,
                created_at=now,
                kind="page",
                media="image/png",
            ),
            png,
        )
    except Exception as exc:  # noqa: BLE001 - storage SDKs raise their own types
        logging.getLogger(__name__).warning("the drawn page was not kept: %s", exc)
        picture_id = ""
    filed(
        trail,
        household_id,
        run_id,
        kind=WHAT_WAS_DRAWN,
        at=now,
        heading=page.title,
        picture_id=picture_id,
        asked=asked,
    )


@router.post("/api/device/{household_id}/read-page")
async def read_a_page(
    household_id: str,
    pages: PagesToCompare,
    _: DeviceKey,
    request: Request,
    afterwards: BackgroundTasks,
) -> Any:
    """Say what is on the sheet that was not on the blank.

    What comes back describes ink — a house drawn in the left box, three lines at the top —
    and whether it looks like the sheet that was handed over. It never says whether anything
    is right, and there is no field in which it could.

    The same two images are placed on the axes an afternoon is pitched along, and that runs
    **after** this answer has gone. Somebody is standing at the scanner: a reading was
    measured at 14.4 s on 3 September 2026 and the placing is another call of the same
    shape, so putting it inside this reply would make every afternoon wait for its own
    measurement. What a late replica costs is one row of a series and nothing else.
    """
    settings: Settings = request.app.state.settings
    counter: UsageStore = request.app.state.usage
    if at_the_limit(counter, request.app.state.limit, household_id, settings.monthly_limit):
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
    _place_it(afterwards, request, household_id, blank, came_back, pages.about)
    return came.to_dict()


def _place_it(
    afterwards: BackgroundTasks,
    request: Request,
    household_id: str,
    blank: PageImage,
    came_back: PageImage,
    asked_for: str,
) -> None:
    """Queue the placing, and only when this household has room for another call.

    Skipped at the limit rather than counted outside it. There is one placing per page read,
    so a placing exempt from the cap would make the real spend at that moment exactly twice
    what the cap says, and a cap a category of call can double is not a cap. That argument
    is `panel/judging.py`'s, and it applies here with the same arithmetic.
    """
    settings: Settings = request.app.state.settings
    counter: UsageStore = request.app.state.usage
    if at_the_limit(counter, request.app.state.limit, household_id, settings.monthly_limit):
        return
    afterwards.add_task(
        _placed_and_filed,
        request.app.state.noticed,
        counter,
        household_id,
        blank,
        came_back,
        asked_for,
    )


async def _placed_and_filed(
    store: NoticedStore,
    counter: UsageStore,
    household_id: str,
    blank: PageImage,
    came_back: PageImage,
    asked_for: str,
) -> None:
    """Place one page and keep the row. Never raises: the page has already gone home.

    A placing that fails is a shorter series, which `shared/profile.read_from` already
    handles by counting how many placements it has before it leans on them. An exception
    escaping a background task would be logged as a failure of the request that spawned it,
    which is the request that succeeded.
    """
    from ..paper import place_the_page

    spent: Any = None
    outcome = FAILED
    try:
        noticed, spent = await place_the_page(
            blank, came_back, asked_for=asked_for, now=time.time()
        )
        outcome = SERVED
        store.notice(household_id, noticed)
    except Exception as exc:  # noqa: BLE001 - a measurement may not cost the page it measures
        logging.getLogger(__name__).info("a page was not placed: %s", exc)
    finally:
        _count(counter, household_id, KIND_PLACE, outcome, spent)


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
