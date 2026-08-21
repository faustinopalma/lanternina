"""The house asking what happens next, and the model thinking inside the answer.

One route, and its direction is the whole design. An experience is played by the hub. When
an outcome says ``ask``, the hub posts what came back off its own glass and receives the
rest of the afternoon in the reply. Nothing here can reach a house, start an afternoon,
extend one or change one that is running — there is no path in that direction, which is
what makes "a write from the panel is inert" true of this feature rather than merely
intended.

What arrives is an experience, which carries nothing about a person, and a reading, which
describes ink. No name, no profile, no learner.

What goes back has been screened. That is not decoration on this path: the parent approved
the experience once from its overview, so these are the only eyes on it before an
adolescent's.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict

from shared.errors import CloudUnavailable, NoCapacityError, SafetyBlocked
from shared.experience import ASK, Came, Collect, Experience, ExperienceError

from ..config import Settings
from ..gate import DeviceKey
from ..usage import FAILED, KIND_TEXT, REFUSED, SERVED, UsageStore, event_from, over_cap

router = APIRouter()


class WhatCameBack(BaseModel):
    """A page came back, the plan said ask, and this is everything there is to say."""

    model_config = ConfigDict(extra="forbid")

    experience: dict[str, Any]
    after: str
    came: str
    reading: dict[str, Any]


@router.post("/api/device/{household_id}/experience")
async def continue_afternoon(
    household_id: str, what: WhatCameBack, _: DeviceKey, request: Request
) -> Any:
    """Write the rest of an afternoon, screen it, and hand it back.

    Refusals are all of one shape here, and that shape is on purpose: an afternoon that is
    not continued stops, which is what an afternoon nobody continues does anyway. So the
    cap, the cloud, the gate and a malformed answer all end the same way for the house —
    it does not get moments, and nothing is said to anybody about the page.

    The monthly cap is refused rather than degraded, unlike the reminders route. There is
    no reduced version of the rest of an afternoon: half a continuation is not one.
    """
    settings: Settings = request.app.state.settings
    counter: UsageStore = request.app.state.usage
    if over_cap(counter, household_id, settings.monthly_call_cap):
        raise HTTPException(status_code=429, detail="monthly_cap_reached")

    experience = _asked(what)
    from ..continuing import continue_experience

    spent: Any = None
    outcome = FAILED
    try:
        carrying_on, spent = await continue_experience(
            experience=experience.to_dict(),
            after=what.after,
            came=what.came,
            reading=what.reading,
            now=time.time(),
        )
        outcome = SERVED
    except SafetyBlocked as exc:
        # A refused continuation is a normal outcome, and the only honest one: there is
        # nothing to fall back on, because nobody wrote what comes after this branch.
        outcome = REFUSED
        logging.getLogger(__name__).info("continuation refused: %s", exc)
        raise HTTPException(status_code=422, detail="refused_by_the_gate") from exc
    except ExperienceError as exc:
        logging.getLogger(__name__).warning("not a continuation: %s", exc)
        raise HTTPException(status_code=502, detail=f"not_a_continuation: {exc}") from exc
    except (NoCapacityError, CloudUnavailable, ValueError) as exc:
        logging.getLogger(__name__).warning("afternoon not continued: %s", exc)
        raise HTTPException(status_code=503, detail=f"unavailable: {exc}") from exc
    finally:
        _count(counter, household_id, KIND_TEXT, outcome, spent)
    return carrying_on.to_dict()


def _asked(what: WhatCameBack) -> Experience:
    """Check that this is a real afternoon asking a real question, before paying for one.

    The experience is parsed rather than passed through, and the moment named is looked up
    in it: a house asking about a branch that does not say ``ask`` would otherwise buy a
    continuation for a step somebody already wrote. What goes to the model afterwards is
    what came out of the parse, so a document that arrived with a control character in a
    heading reaches the prompt without it.
    """
    try:
        experience = Experience.from_dict(what.experience)
    except ExperienceError as exc:
        raise HTTPException(status_code=400, detail=f"not an experience: {exc}") from exc
    try:
        came = Came(what.came)
    except ValueError as exc:
        raise HTTPException(
            status_code=400, detail=f"a page cannot come back {what.came!r}"
        ) from exc
    try:
        moment = experience.moment(what.after)
    except ExperienceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not isinstance(moment, Collect):
        raise HTTPException(status_code=400, detail=f"{what.after!r} does not read a page")
    if not [o for o in moment.outcomes if o.when is came and o.then == ASK]:
        raise HTTPException(
            status_code=400,
            detail=f"{what.after!r} already says what happens when a page comes back {came}",
        )
    return experience


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
    except Exception as exc:  # noqa: BLE001 - bookkeeping must not eat a continuation
        logging.getLogger(__name__).warning("usage not recorded: %s", exc)
