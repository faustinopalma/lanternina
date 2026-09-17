"""The record of what the system wrote, and the parent's two ways of reading it.

The parent approves an idea. What happens after that is written as the afternoon goes, and
none of it is approved by anybody — there is no moment where a parent could stand between a
generated page and the room without stopping the afternoon to do it. So the trade is made in
the open: no veto on each piece, and in exchange every piece is readable afterwards, in full,
beside the script it came from.

**Recording happens where generating happens**, which is here. Not on the house: a house that
reported its own work would be reporting what it managed to do, and the two differ exactly
when it is worth knowing. What went out of this container is what this container writes down.

**Filing never raises.** The generation was already made and already paid for, so a trail that
could fail a request would be a record with a hold over an afternoon.

Reading is two routes because a card and a script are different sizes. The list carries
titles; the script and everything under it arrive only when a parent opens one.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from shared.ids import new_id

from ..gate import CurrentAccount, DeviceKey
from ..trail import CurrentTrail, Made, Trail, TrailStore, clipped

router = APIRouter()


class CurrentRun(BaseModel):
    model_config = ConfigDict(extra="forbid")

    runId: str = Field(min_length=1, max_length=200)
    title: str = Field(max_length=500)
    beganAt: float = Field(ge=0, allow_inf_nan=False)
    endsAt: float = Field(ge=0, allow_inf_nan=False)
    momentId: str = Field(max_length=200)
    heading: str = Field(max_length=500)
    phase: Literal["waiting", "ending", "unreadable"]
    waitingSince: float = Field(ge=0, allow_inf_nan=False)


class CurrentRuns(BaseModel):
    model_config = ConfigDict(extra="forbid")

    runs: list[CurrentRun] = Field(max_length=10)


@router.post("/api/device/{household_id}/trail-current")
def report_current(
    household_id: str, current: CurrentRuns, _: DeviceKey, request: Request
) -> Any:
    store: TrailStore = request.app.state.trail
    store.report_current(CurrentTrail(
        household_id, time.time(), tuple(run.model_dump() for run in current.runs)
    ))
    return {"recorded": True}


@router.get("/api/trail-current")
def current_activity(account: CurrentAccount, request: Request) -> Any:
    store: TrailStore = request.app.state.trail
    return store.current(str(account.household_id)).to_public()


@router.get("/api/trail")
def the_afternoons(account: CurrentAccount, request: Request) -> Any:
    """The cards: one per afternoon that ran, newest first, without their scripts."""
    store: TrailStore = request.app.state.trail
    return {"trails": [row.summary() for row in store.list(str(account.household_id))]}


@router.get("/api/trail/{run_id}")
def one_afternoon(run_id: str, account: CurrentAccount, request: Request) -> Any:
    """The script in full, and every generated thing under it in the order it was made."""
    store: TrailStore = request.app.state.trail
    found = store.get(str(account.household_id), run_id)
    if found is None:
        raise HTTPException(status_code=404, detail="unknown_run")
    return found.to_public()


@router.delete("/api/trail")
def throw_it_away(account: CurrentAccount, request: Request) -> Any:
    """Delete this household's activity record, leaving its settings and approvals intact."""
    store: TrailStore = request.app.state.trail
    return {"forgotten": store.forget_everything(str(account.household_id))}


@router.delete("/api/trail/{run_id}")
def throw_one_away(run_id: str, account: CurrentAccount, request: Request) -> Any:
    """Delete one run and its entries for the authenticated household."""
    store: TrailStore = request.app.state.trail
    return {"forgotten": store.forget(str(account.household_id), run_id)}


def opened(
    store: TrailStore, household_id: str, run_id: str, document: dict[str, Any], at: float
) -> None:
    """Make sure this run has a trail, from the document the house was working from.

    Called on every generation rather than once, because the store is idempotent on the run
    and there is no earlier moment the panel is certain to see. The script is copied rather
    than pointed at: an experience can be withdrawn afterwards, and the trail has to keep
    showing the words the afternoon actually ran on.
    """
    _quietly(
        store.began,
        Trail(
            run_id=run_id,
            household_id=household_id,
            experience_id=str(document.get("experienceId") or document.get("id") or ""),
            title=str(document.get("title") or ""),
            overview=str(document.get("overview") or ""),
            began_at=at,
            script=clipped(str(document.get("script") or "")),
        ),
    )


def filed(
    store: TrailStore,
    household_id: str,
    run_id: str,
    *,
    kind: str,
    at: float,
    heading: str = "",
    body: str = "",
    why: str = "",
    paper: str = "",
    picture_id: str = "",
    asked: str = "",
    until: float = 0.0,
) -> None:
    """Write down one thing the system wrote."""
    _quietly(
        store.wrote,
        Made(
            id=str(new_id("made")),
            household_id=household_id,
            run_id=run_id,
            at=at,
            kind=kind,
            heading=heading,
            body=clipped(body),
            why=why,
            paper=clipped(paper),
            picture_id=picture_id,
            asked=clipped(asked),
            until=until,
        ),
    )


def _quietly(write: Any, record: Any) -> None:
    try:
        write(record)
    except Exception as exc:  # noqa: BLE001 - a trail must not be able to stop an afternoon
        logging.getLogger(__name__).warning("not recorded in the trail: %s", exc)
