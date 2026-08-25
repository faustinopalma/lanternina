"""The house asking for an afternoon, and asking what happens next inside one.

Every route here points the same way, and the direction is the whole design. An experience
is devised because the hub asked whether there was one to be had, and continued because
the hub posted what came back off its own glass. Nothing here can reach a house, start an
afternoon, extend one or change one that is running — there is no path in that direction,
which is what makes "a write from the panel is inert" true of this feature rather than
merely intended. The parent's two routes below record a decision and nothing else.

What arrives from a house is an experience, which carries nothing about a person, and a
reading, which describes ink. No name, no profile, no learner.

What goes back has been screened. On the continuing path that is not decoration: the
parent approved the experience once from its overview, so those are the only eyes on it
before an adolescent's.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from shared.approval import ApprovalState
from shared.capabilities import HouseCapability
from shared.errors import CloudUnavailable, NoCapacityError, SafetyBlocked
from shared.experience import ASK, Came, Collect, Drawn, Experience, ExperienceError

from ..config import Settings
from ..experiences import (
    DECIDABLE,
    WITHDRAWABLE_FROM,
    ExperienceStore,
    OfferedExperience,
    backlog_of,
)
from ..gate import CurrentAccount, DeviceKey
from ..guidelines import GuidelineStore
from ..preferences import LANGUAGE_NAMES, PreferencesStore
from ..rhythm import RhythmStore
from ..usage import FAILED, KIND_TEXT, REFUSED, SERVED, UsageStore, at_the_limit, event_from
from . import Decision

router = APIRouter()


class SeveralDecisions(BaseModel):
    """The same decision, given to a handful of afternoons in one sitting."""

    model_config = ConfigDict(extra="forbid")

    ids: list[str]
    state: str
    note: str = ""


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

    The monthly limit is refused rather than degraded, unlike the reminders route. There is
    no reduced version of the rest of an afternoon: half a continuation is not one.
    """
    settings: Settings = request.app.state.settings
    counter: UsageStore = request.app.state.usage
    if at_the_limit(counter, request.app.state.limit, household_id, settings.monthly_limit):
        raise HTTPException(status_code=429, detail="monthly_cap_reached")

    experience = _asked(what)
    # What this house allows to be changed on the fly. Read here rather than sent by the
    # hub: the hub holds a device key and no parent, so a bound arriving from it would be
    # a bound nobody in the house had written.
    said: GuidelineStore = request.app.state.guidelines
    from ..continuing import continue_experience
    from ..devising import RefusedByTheChecks

    spent: Any = None
    outcome = FAILED
    try:
        carrying_on, spent = await continue_experience(
            experience=experience.to_dict(),
            after=what.after,
            came=what.came,
            reading=what.reading,
            now=time.time(),
            household_bounds=said.get(household_id).as_material(),
        )
        outcome = SERVED
    except SafetyBlocked as exc:
        # A refused continuation is a normal outcome, and the only honest one: there is
        # nothing to fall back on, because nobody wrote what comes after this branch.
        outcome = REFUSED
        logging.getLogger(__name__).info("continuation refused: %s", exc)
        raise HTTPException(status_code=422, detail="refused_by_the_gate") from exc
    except RefusedByTheChecks as exc:
        outcome = REFUSED
        logging.getLogger(__name__).info("continuation refused by the checks: %s", exc)
        # Which check, and not only that one refused. The house is the only caller and it
        # holds a device key; the neighbour below has always answered this way, and an
        # afternoon that stops with no recoverable reason makes the next run undiagnosable.
        raise HTTPException(
            status_code=422, detail=f"refused_by_the_checks: {exc}"
        ) from exc
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


# ── Devising one, and deciding about it ──────────────────────────────────────────────


class WhatTheHouseHas(BaseModel):
    """The equipment an afternoon must be devised for, as the house itself reports it."""

    model_config = ConfigDict(extra="forbid")

    capabilities: list[str] = Field(default_factory=list)


@router.post("/api/device/{household_id}/experiences")
async def devise_afternoon(
    household_id: str, has: WhatTheHouseHas, _: DeviceKey, request: Request
) -> Any:
    """Devise one afternoon for this house and leave it waiting for the parent.

    The house is told what was written, and not that it may run it: what comes back here
    is pending, and it stays pending until somebody decides. So this route can be called
    on any rhythm the hub likes and it still cannot put anything in front of anybody.

    Refused the same way the continuing route is, and for the same reason: there is no
    reduced version of an afternoon, so the cap, the cloud, the gate and a malformed
    answer all end with the house not being offered one.
    """
    settings: Settings = request.app.state.settings
    counter: UsageStore = request.app.state.usage
    if at_the_limit(counter, request.app.state.limit, household_id, settings.monthly_limit):
        raise HTTPException(status_code=429, detail="monthly_cap_reached")

    try:
        capabilities = frozenset(HouseCapability(name) for name in has.capabilities)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"not a capability: {exc}") from exc
    if not capabilities:
        raise HTTPException(status_code=400, detail="a house with no equipment has no afternoon")

    store: ExperienceStore = request.app.state.experiences
    preferences: PreferencesStore = request.app.state.preferences
    settings_of_the_house = preferences.get(household_id)
    # Titles only. What is kept about earlier afternoons is what they were called, so that
    # the next one differs — never who did them, how far they got or what came back.
    already = tuple(row.title for row in store.list(household_id) if row.title)
    recent = _drawn_before(store, household_id)

    from ..devising import RefusedByTheChecks, devise_experience

    spent: Any = None
    outcome = FAILED
    try:
        experience, spent = await devise_experience(
            capabilities=capabilities,
            language=LANGUAGE_NAMES.get(
                settings_of_the_house.language, settings_of_the_house.language
            ),
            interests=settings_of_the_house.interests,
            avoid=settings_of_the_house.avoid,
            already=already,
            recent=recent,
            now=time.time(),
        )
        outcome = SERVED
    except SafetyBlocked as exc:
        outcome = REFUSED
        logging.getLogger(__name__).info("afternoon refused: %s", exc)
        raise HTTPException(status_code=422, detail="refused_by_the_gate") from exc
    except RefusedByTheChecks as exc:
        outcome = REFUSED
        logging.getLogger(__name__).info("afternoon refused by the checks: %s", exc)
        raise HTTPException(
            status_code=422, detail=f"refused_by_the_checks: {exc}"
        ) from exc
    except ExperienceError as exc:
        logging.getLogger(__name__).warning("not an experience: %s", exc)
        raise HTTPException(status_code=502, detail=f"not_an_experience: {exc}") from exc
    except (NoCapacityError, CloudUnavailable, ValueError) as exc:
        logging.getLogger(__name__).warning("afternoon not devised: %s", exc)
        raise HTTPException(status_code=503, detail=f"unavailable: {exc}") from exc
    finally:
        _count(counter, household_id, KIND_TEXT, outcome, spent)

    stored = store.offer(
        OfferedExperience(
            id=experience.experience_id,
            household_id=household_id,
            experience=experience.to_dict(),
            created_at=time.time(),
        )
    )
    return {"id": stored.id, "title": stored.title, "state": stored.state}


# How many earlier afternoons the next one is drawn against. Five is a month of weekly
# afternoons; more than that and a model is being asked to avoid so much that the honest
# answer is a shrug. Chosen, not measured.
DRAWN_BEFORE = 5


def _drawn_before(store: ExperienceStore, household_id: str) -> tuple[Drawn, ...]:
    """The dimensions the last few afternoons here were drawn along.

    Ten short phrases per afternoon, all of them about the afternoon. This is the thing
    `ideas/09 §10` says makes variety checkable instead of hoped for, and it is the reason
    the field exists at all.

    A row this container can no longer read is skipped rather than refused: an old document
    in a store is not a reason to leave a house with no afternoon.
    """
    drawn: list[Drawn] = []
    for row in store.list(household_id)[-DRAWN_BEFORE:]:
        try:
            drawn.append(Drawn.from_dict(row.experience.get("drawn")))
        except ExperienceError:
            continue
    return tuple(drawn)


@router.get("/api/device/{household_id}/experiences")
def afternoons_for_the_house(household_id: str, _: DeviceKey, request: Request) -> Any:
    """What the house may run, and whether one is still with the parent.

    Approved only. There used to be a parameter here that chose a state, and it is gone:
    a house able to pull a pending document could run one, and then the single decision
    this whole feature rests on would be held up by the hub's own code rather than by the
    panel. It pulls; nothing is ever pushed to a house.

    ``waiting`` is how many are with the parent, undecided. The house needs it so that it
    does not ask for a second afternoon while the first is still unread — it is the depth
    of somebody's inbox, and it says nothing about anybody's afternoon.
    """
    store: ExperienceStore = request.app.state.experiences
    runnable = [
        row
        for row in store.list(household_id, ApprovalState.APPROVED.value)
        if not row.begun_at
    ]
    return {
        "experiences": [row.to_device() for row in runnable],
        "waiting": len(store.list(household_id, ApprovalState.PENDING.value)),
    }


@router.post("/api/device/{household_id}/experiences/{experience_id}/begun")
def afternoon_begun(
    household_id: str, experience_id: str, _: DeviceKey, request: Request
) -> Any:
    """The house says it started this one, so it is not handed the same one tomorrow.

    A fact about the house, written by the house. It is not a decision and it does not
    become one: the parent's word stays in ``state``, and nothing here records who did the
    afternoon, how far it got or whether it finished. The first moment stands, so a hub
    that retries does not move it.
    """
    store: ExperienceStore = request.app.state.experiences
    if store.get(household_id, experience_id) is None:
        raise HTTPException(status_code=404, detail="unknown_experience")
    row = store.begun(household_id, experience_id, time.time())
    return {"id": row.id, "begunAt": row.begun_at}


@router.get("/api/experiences")
def list_afternoons(account: CurrentAccount, request: Request, state: str = "pending") -> Any:
    """What is waiting for a decision, and how far what is already approved carries.

    Both in one answer, because they are read together: a parent deciding whether to spend
    ten minutes on this now wants to know whether the house is about to run dry.
    """
    store: ExperienceStore = request.app.state.experiences
    household_id = str(account.household_id)
    rows = store.list(household_id, state or None)
    rhythm: RhythmStore = request.app.state.rhythm
    days = len(rhythm.get(household_id).afternoon_days)
    return {
        "experiences": [row.to_public() for row in rows],
        "backlog": backlog_of(store.list(household_id), days_a_week=days).to_public(),
    }


@router.post("/api/experiences/decisions")
def decide_several(
    decisions: SeveralDecisions, account: CurrentAccount, request: Request
) -> Any:
    """One sitting, several afternoons.

    A parent who opens the panel once a week is deciding about a handful at a time, and
    one request per card turns a sitting into a sequence of things that can each fail
    halfway. Every id is answered for: the reply says what each one became, so a card that
    could not be decided is visible rather than silently unchanged.
    """
    if decisions.state not in {s.value for s in DECIDABLE}:
        raise HTTPException(status_code=400, detail="unsupported_state")
    if not decisions.ids:
        raise HTTPException(status_code=400, detail="no_experiences")
    store: ExperienceStore = request.app.state.experiences
    household_id = str(account.household_id)
    decided: list[dict[str, Any]] = []
    for experience_id in decisions.ids:
        try:
            row = store.decide(
                household_id,
                experience_id,
                decisions.state,
                decided_by=str(account.id),
                note=decisions.note,
            )
        except KeyError:
            decided.append({"id": experience_id, "state": "unknown"})
            continue
        decided.append(row.to_public())
    rhythm: RhythmStore = request.app.state.rhythm
    days = len(rhythm.get(household_id).afternoon_days)
    return {
        "decided": decided,
        "backlog": backlog_of(store.list(household_id), days_a_week=days).to_public(),
    }


@router.post("/api/experiences/{experience_id}/decision")
def decide_afternoon(
    experience_id: str, decision: Decision, account: CurrentAccount, request: Request
) -> Any:
    """Record what the parent decided about an afternoon. It starts nothing.

    Approving does not run it and does not tell anybody: the house asks on its own rhythm
    and finds it then. Withdrawing is a second decision on something already approved, and
    it applies to the future only — an afternoon already begun is beyond reach from here,
    because there is no route in that direction at all.
    """
    if decision.state not in {s.value for s in DECIDABLE}:
        raise HTTPException(status_code=400, detail="unsupported_state")
    store: ExperienceStore = request.app.state.experiences
    if decision.state == ApprovalState.WITHDRAWN.value:
        current = store.get(str(account.household_id), experience_id)
        if current is None:
            raise HTTPException(status_code=404, detail="unknown_experience")
        if current.state not in WITHDRAWABLE_FROM:
            raise HTTPException(status_code=409, detail="not_approved")
    try:
        row = store.decide(
            str(account.household_id),
            experience_id,
            decision.state,
            decided_by=str(account.id),
            note=decision.note,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="unknown_experience") from exc
    return row.to_public()
