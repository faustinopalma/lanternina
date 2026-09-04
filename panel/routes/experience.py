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

import json
import logging
import time
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from shared.approval import ApprovalState
from shared.capabilities import NEVER_CAME_BACK, HouseCapability
from shared.errors import CloudUnavailable, NoCapacityError, SafetyBlocked
from shared.experience import ASK, Came, Collect, Drawn, Experience, ExperienceError
from shared.page import Page, PageError

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
from ..keeping import KeepingStore, kept_for
from ..preferences import LANGUAGE_NAMES, PreferencesStore
from ..profiles import (
    NoticedStore,
    a_sheet_that_never_came_back,
    how_long_it_was_meant_to_take,
    the_profile,
)
from ..rhythm import RhythmStore
from ..trail import (
    HOUSE_MAY_FILE,
    THE_PLAN,
    WENT_WRONG,
    WHAT_A_READER_MADE_OF_IT,
    WHAT_CAME_BACK,
    WHAT_COMES_AFTER,
    TrailStore,
)
from ..usage import FAILED, KIND_TEXT, REFUSED, SERVED, UsageStore, at_the_limit, event_from
from ..what_happened import (
    ENDINGS,
    Answered,
    WhatHappenedStore,
    as_material,
    clean_reading,
    how_it_has_gone,
    remembered,
    the_ground,
)
from . import Decision
from .trail import filed, opened

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
    # Which run this belongs to, so what gets written can be filed against the afternoon it
    # was written for. Absent means the generation happens and goes unrecorded, which is what
    # a house that predates the trail does.
    runId: str = ""


def _pitch_for(request: Request, household_id: str) -> str:
    """Where this house sits, as sentences about an afternoon. Empty when too little is known.

    Worked out at the moment a prompt is built and kept nowhere. The rows are the record and
    the state is arithmetic over them, so there is one place a wrong pitch can come from
    rather than a stored answer and a way of recomputing it that can disagree.
    """
    seen: NoticedStore = request.app.state.noticed
    memory: WhatHappenedStore = request.app.state.what_happened
    store: ExperienceStore = request.app.state.experiences
    return the_profile(
        seen.list(household_id),
        memory.list(household_id),
        {
            row.id: how_long_it_was_meant_to_take(row.experience)
            for row in store.list(household_id)
        },
    ).as_material()


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

    _kept_while_being_worked_on(request, household_id, what)
    spent: Any = None
    outcome = FAILED
    went_wrong = ""
    try:
        carrying_on, spent = await continue_experience(
            experience=experience.to_dict(),
            after=what.after,
            came=what.came,
            reading=what.reading,
            now=time.time(),
            household_bounds=said.get(household_id).as_material(),
            pitch=_pitch_for(request, household_id),
        )
        outcome = SERVED
    except SafetyBlocked as exc:
        # A refused continuation is a normal outcome, and the only honest one: there is
        # nothing to fall back on, because nobody wrote what comes after this branch.
        outcome = REFUSED
        went_wrong = f"the gate refused the rest of this afternoon: {exc}"
        logging.getLogger(__name__).info("continuation refused: %s", exc)
        raise HTTPException(status_code=422, detail="refused_by_the_gate") from exc
    except RefusedByTheChecks as exc:
        outcome = REFUSED
        went_wrong = f"the checks refused the rest of this afternoon: {exc}"
        logging.getLogger(__name__).info("continuation refused by the checks: %s", exc)
        # Which check, and not only that one refused. The house is the only caller and it
        # holds a device key; the neighbour below has always answered this way, and an
        # afternoon that stops with no recoverable reason makes the next run undiagnosable.
        raise HTTPException(
            status_code=422, detail=f"refused_by_the_checks: {exc}"
        ) from exc
    except ExperienceError as exc:
        went_wrong = f"what came back was not a continuation: {exc}"
        logging.getLogger(__name__).warning("not a continuation: %s", exc)
        raise HTTPException(status_code=502, detail=f"not_a_continuation: {exc}") from exc
    except (NoCapacityError, CloudUnavailable, ValueError) as exc:
        went_wrong = f"the rest of this afternoon could not be written: {exc}"
        logging.getLogger(__name__).warning("afternoon not continued: %s", exc)
        raise HTTPException(status_code=503, detail=f"unavailable: {exc}") from exc
    finally:
        _count(counter, household_id, KIND_TEXT, outcome, spent)
        if went_wrong:
            _write_down(
                request,
                household_id,
                what.runId,
                what.experience,
                kind=WENT_WRONG,
                body=went_wrong,
            )
    _write_down(
        request,
        household_id,
        what.runId,
        what.experience,
        kind=WHAT_COMES_AFTER,
        body=json.dumps(
            [one.to_dict() for one in carrying_on.moments], ensure_ascii=False, indent=2
        ),
    )
    return carrying_on.to_dict()


class WhereItIs(BaseModel):
    """An afternoon in progress, as the house sees it, asking what to do next."""

    model_config = ConfigDict(extra="forbid")

    experience: dict[str, Any]
    happened: list[dict[str, Any]] = []
    minutesLeft: int
    runId: str = ""


@router.post("/api/device/{household_id}/next-move")
async def next_move(
    household_id: str, where: WhereItIs, _: DeviceKey, request: Request
) -> Any:
    """One move, decided from the strategy the parent approved and what has happened.

    Refused the same way a continuation is, and for the same reason: the house has a written
    plan that was approved and always works, so a move it cannot get is a move it does not
    make. Nothing is said to anybody about why.
    """
    settings: Settings = request.app.state.settings
    counter: UsageStore = request.app.state.usage
    if at_the_limit(counter, request.app.state.limit, household_id, settings.monthly_limit):
        raise HTTPException(status_code=429, detail="monthly_cap_reached")

    try:
        afternoon = Experience.from_dict(where.experience)
    except ExperienceError as exc:
        raise HTTPException(status_code=400, detail=f"not_an_experience: {exc}") from exc

    from ..moving import decide_a_move

    spent: Any = None
    outcome = FAILED
    went_wrong = ""
    try:
        move, spent = await decide_a_move(
            afternoon=afternoon,
            happened=where.happened,
            minutes_left=where.minutesLeft,
        )
        outcome = SERVED
    except SafetyBlocked as exc:
        outcome = REFUSED
        went_wrong = f"the gate refused the next move: {exc}"
        logging.getLogger(__name__).info("move refused: %s", exc)
        raise HTTPException(status_code=422, detail="refused_by_the_gate") from exc
    except ExperienceError as exc:
        went_wrong = f"what came back was not a move: {exc}"
        logging.getLogger(__name__).warning("not a move: %s", exc)
        raise HTTPException(status_code=502, detail=f"not_a_move: {exc}") from exc
    except (NoCapacityError, CloudUnavailable, ValueError) as exc:
        went_wrong = f"no move was decided: {exc}"
        logging.getLogger(__name__).warning("no move decided: %s", exc)
        raise HTTPException(status_code=503, detail=f"unavailable: {exc}") from exc
    finally:
        _count(counter, household_id, KIND_TEXT, outcome, spent)
        if went_wrong:
            _write_down(
                request,
                household_id,
                where.runId,
                where.experience,
                kind=WENT_WRONG,
                body=went_wrong,
            )
    _write_down(
        request,
        household_id,
        where.runId,
        where.experience,
        kind=str(move.act),
        heading=move.heading,
        body="\n".join(move.lines),
        why=move.why,
        paper=_printed(move.page),
    )
    return move.to_dict()


def _printed(page: Any) -> str:
    """A page as the words that are on it, in the order they are on it.

    Not the JSON it arrived as. This is a record of a generated thing and the generated
    thing is a document, but braces around a title are our storage showing through, and a
    parent opening the record wants the sheet. The illustration is the last line and in
    brackets: it is the one string on a page that is never lettered onto the paper.

    A page this container cannot read falls back to the JSON rather than to nothing, because
    a record that quietly drops what it could not parse is the worse of the two failures.
    """
    if not page:
        return ""
    try:
        drawn = Page.from_dict(page)
    except (PageError, TypeError):
        return json.dumps(page, ensure_ascii=False, indent=2)
    lines = [drawn.title, *drawn.note, *(f"— {one.label}" for one in drawn.spaces)]
    return "\n".join([one for one in lines if one] + [f"({drawn.illustration})"])


def _kept_while_being_worked_on(
    request: Request, household_id: str, what: WhatCameBack
) -> None:
    """The other half, and only where `panel/keeping.py` says a household is being built on.

    Here rather than anywhere else because here is the one place the reading already crosses
    the wire: the house posts what came back so that the rest of the afternoon can be
    written from it. Every other route stays closed, and the shape a house files what it
    performed with still has no field a reading would fit in.

    The row carries the instant the permission lapses, so it deletes itself even if nobody
    remembers this was ever turned on.
    """
    if not what.runId:
        return
    store: KeepingStore = request.app.state.keeping
    until = kept_for(store, household_id, time.time())
    if not until:
        return
    _write_down(
        request,
        household_id,
        what.runId,
        what.experience,
        kind=WHAT_CAME_BACK,
        heading=what.after,
        body=json.dumps(what.reading, ensure_ascii=False, indent=2),
        why=what.came,
        until=until,
    )


def _write_down(
    request: Request,
    household_id: str,
    run_id: str,
    document: dict[str, Any],
    *,
    kind: str,
    heading: str = "",
    body: str = "",
    why: str = "",
    paper: str = "",
    until: float = 0.0,
) -> None:
    """File a generation against its afternoon, if the house said which one this is."""
    if not run_id:
        return
    store: TrailStore = request.app.state.trail
    now = time.time()
    opened(store, household_id, run_id, document, now)
    filed(
        store,
        household_id,
        run_id,
        kind=kind,
        at=now,
        heading=heading,
        body=body,
        why=why,
        paper=paper,
        until=until,
    )


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
    household_id: str,
    has: WhatTheHouseHas,
    _: DeviceKey,
    request: Request,
    afterwards: BackgroundTasks,
) -> Any:
    """Devise one afternoon for this house and leave it waiting for the parent.

    The house is told what was written, and not that it may run it: what comes back here
    is pending, and it stays pending until somebody decides. So this route can be called
    on any rhythm the hub likes and it still cannot put anything in front of anybody.

    Refused the same way the continuing route is, and for the same reason: there is no
    reduced version of an afternoon, so the cap, the cloud, the gate and a malformed
    answer all end with the house not being offered one.

    The reading of what was written happens after this answer has gone, not inside it.
    `panel/judging.py` has the measurement that decides that.
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
    # Two mechanisms and two sources. What has already been used comes out of every
    # afternoon *proposed* here, because offering one again is the repeat. How much to ask
    # for comes out of the ones that actually ran.
    already = tuple(row.title for row in store.list(household_id) if row.title)
    recent = _drawn_before(store, household_id)
    ground = the_ground(_themes_proposed(store, household_id))
    memory: WhatHappenedStore = request.app.state.what_happened
    ran = memory.list(household_id)
    going = how_it_has_gone(ran)
    pitch = _pitch_for(request, household_id)

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
            # Worked out from what came back off the glass, not chosen by the parent: a
            # setting asking them to grade what somebody can take left the panel on
            # 4 September 2026. It goes to the prompt and never onto the document.
            pitch=pitch,
            sheets=settings_of_the_house.sheets,
            # Empty once it has lapsed, and by then the store has deleted it.
            note=settings_of_the_house.standing(time.time()),
            already=already,
            recent=recent,
            happened=as_material(ran),
            counts=json.dumps(going.to_dict(), ensure_ascii=False),
            direction=going.direction(),
            ground=json.dumps(ground.to_dict(), ensure_ascii=False) if ground.anything() else "",
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
    _read_it_back(afterwards, request, household_id, experience)
    return {"id": stored.id, "title": stored.title, "state": stored.state}


def _read_it_back(
    afterwards: BackgroundTasks, request: Request, household_id: str, experience: Experience
) -> None:
    """Queue the reading of an afternoon that was just written, for after the answer.

    A background task rather than another await, because the two failures are not worth the
    same: a reading that does not happen costs a row, and a reply that runs out of time
    costs an afternoon that was already written and already paid for. `panel/judging.py`
    has the measured latencies.
    """
    from ..judging import judged_and_filed

    afterwards.add_task(
        judged_and_filed,
        experiences=request.app.state.experiences,
        usage=request.app.state.usage,
        limits=request.app.state.limit,
        configured=request.app.state.settings.monthly_limit,
        household_id=household_id,
        experience=experience,
    )


# How many earlier afternoons the next one is drawn against. Five is a month of weekly
# afternoons; more than that and a model is being asked to avoid so much that the honest
# answer is a shrug. Chosen, not measured.
DRAWN_BEFORE = 5


def _themes_proposed(store: ExperienceStore, household_id: str) -> tuple[tuple[str, ...], ...]:
    """The subjects of every afternoon ever proposed here, one tuple each, oldest first.

    All of them and not the last few: `panel/what_happened.the_ground` bands them by how
    long ago, so what would be lost by cutting the list here is exactly the band that says
    a subject may be returned to.
    """
    return tuple(
        tuple(str(theme) for theme in (row.experience.get("themes") or ()) if str(theme))
        for row in store.list(household_id)
    )


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

    ``waiting`` is how many are with the parent, undecided, and ``wanted`` is how many
    they asked to have waiting. The house writes one more whenever the first is under the
    second, at any hour — writing a script puts nothing in a room, and a queue that only
    fills during the afternoon band is empty whenever anybody opens the panel.
    """
    store: ExperienceStore = request.app.state.experiences
    rhythm: RhythmStore = request.app.state.rhythm
    runnable = [
        row
        for row in store.list(household_id, ApprovalState.APPROVED.value)
        if not row.begun_at
    ]
    return {
        "experiences": [row.to_device() for row in runnable],
        "waiting": len(store.list(household_id, ApprovalState.PENDING.value)),
        "wanted": rhythm.get(household_id).scripts_wanted,
    }


class ItBegan(BaseModel):
    """The house saying it started one, and under which run."""

    model_config = ConfigDict(extra="forbid")

    runId: str = ""


@router.post("/api/device/{household_id}/experiences/{experience_id}/begun")
def afternoon_begun(
    household_id: str,
    experience_id: str,
    _: DeviceKey,
    request: Request,
    began: ItBegan | None = None,
) -> Any:
    """The house says it started this one, so it is not handed the same one tomorrow.

    A fact about the house, written by the house. It is not a decision and it does not
    become one: the parent's word stays in ``state``, and nothing here records who did the
    afternoon, how far it got or whether it finished. The first moment stands, so a hub
    that retries does not move it.

    This is also where the trail opens, and it is the right place because it is the only
    call the house always makes. It opened on the first generation instead, and an afternoon
    that ran the whole way on its written plan - nothing came back off the glass, so nothing
    was ever generated - left no record at all. Measured on 26 August 2026: an afternoon ran
    start to finish and the parent's page was empty.
    """
    store: ExperienceStore = request.app.state.experiences
    offered = store.get(household_id, experience_id)
    if offered is None:
        raise HTTPException(status_code=404, detail="unknown_experience")
    row = store.begun(household_id, experience_id, time.time())
    run_id = (began.runId if began else "") or experience_id
    trail: TrailStore = request.app.state.trail
    now = time.time()
    opened(trail, household_id, run_id, offered.experience, now)
    # The plan as it was written, beside what the house then did with it. The two differ
    # whenever the clock made it choose a shorter version or reach for the way out, and
    # that difference is most of what a record of an afternoon is for.
    filed(
        trail,
        household_id,
        run_id,
        kind=THE_PLAN,
        at=now,
        body=json.dumps(
            offered.experience.get("moments") or [], ensure_ascii=False, indent=2
        ),
    )
    # And what one reader made of that plan when it was written, kept on the offered
    # afternoon until now. Filed here rather than at devising because the run has an id
    # only from this moment, and a verdict filed against a run nobody plays is a record in
    # a trail a parent will never open.
    if offered.verdict:
        filed(
            trail,
            household_id,
            run_id,
            kind=WHAT_A_READER_MADE_OF_IT,
            at=now,
            # The question a reader who saw only the moments worked out, as the heading:
            # it is the line worth reading first, and an empty one says the reader could
            # not state what the afternoon asks, which is the loudest thing this produces.
            heading=str(offered.verdict.get("question") or ""),
            body=json.dumps(offered.verdict, ensure_ascii=False, indent=2),
        )
    return {"id": row.id, "begunAt": row.begun_at}


class ItDid(BaseModel):
    """One thing the house put in the room, as the house reports having done it."""

    model_config = ConfigDict(extra="forbid")

    kind: str
    heading: str = ""
    lines: list[str] = Field(default_factory=list)
    why: str = ""
    # The sheet that came out of the printer, when one did. Words the system wrote, like
    # everything else here: it is the page as it was designed, not as it came back.
    page: dict[str, Any] | None = None


@router.post("/api/device/{household_id}/trail/{run_id}")
def it_did(
    household_id: str, run_id: str, what: ItDid, _: DeviceKey, request: Request
) -> Any:
    """File what the house performed. Nothing here has a field a reading would fit in.

    The panel records what it generated; this records what reached the room. They are
    different facts and the second is the one a parent asked for - a page that the printer
    never took is a generation that happened and an act that did not.
    """
    if what.kind not in HOUSE_MAY_FILE:
        raise HTTPException(status_code=400, detail=f"a house does not do {what.kind!r}")
    trail: TrailStore = request.app.state.trail
    filed(
        trail,
        household_id,
        run_id,
        kind=what.kind,
        at=time.time(),
        heading=what.heading,
        body="\n".join(what.lines),
        why=what.why,
        paper=_printed(what.page),
    )
    return {"filed": True}


class HowItWent(BaseModel):
    """What one afternoon came to, filed by the house when it is over."""

    model_config = ConfigDict(extra="forbid")

    experience: dict[str, Any]
    ending: str
    weight: str = ""
    minutes: int = 0
    reached: str = ""
    sheets: list[dict[str, Any]] = []


@router.post("/api/device/{household_id}/what-happened/{run_id}")
def how_it_went(
    household_id: str, run_id: str, what: HowItWent, _: DeviceKey, request: Request
) -> Any:
    """File how an afternoon went, so the next one can be written from it.

    Facts about the run: how far it got, how it ended, and for each sheet whether it came
    back marked, blank, or not at all. The shape has no field for a score, a level or
    anything about the person, which is what bounds this.

    A sheet that never came back also lands in the series the pitch is read off, as a row
    with no placement on it. It is not the same as a blank page and is not counted as one:
    blank means somebody carried the sheet to the glass, and this covers everything from a
    sheet still on the table to a scanner nobody has plugged in.
    """
    if what.ending not in ENDINGS:
        raise HTTPException(status_code=400, detail=f"no afternoon ends {what.ending!r}")
    memory: WhatHappenedStore = request.app.state.what_happened
    memory.remember(
        remembered(
            household_id=household_id,
            run_id=run_id,
            experience=what.experience,
            at=time.time(),
            weight=str(what.weight),
            minutes=int(what.minutes),
            reached=str(what.reached),
            ending=what.ending,
            answered=tuple(
                Answered(
                    moment_id=str(one.get("momentId", "")),
                    came=str(one.get("came", "")),
                    reading=clean_reading(one.get("reading")),
                )
                for one in what.sheets
            ),
        )
    )
    seen: NoticedStore = request.app.state.noticed
    for one in what.sheets:
        if str(one.get("came", "")) == NEVER_CAME_BACK:
            seen.notice(household_id, a_sheet_that_never_came_back())
    return {"remembered": True}


@router.get("/api/what-happened")
def what_happened_here(account: CurrentAccount, request: Request) -> Any:
    """Everything kept about how this household's afternoons went, in plain language.

    TODO(poc): the panel has no section for this yet, so the guarantee is a route and not
    something a parent can reach without one.
    """
    memory: WhatHappenedStore = request.app.state.what_happened
    return {"afternoons": [one.to_public() for one in memory.list(account.household_id)]}


@router.delete("/api/what-happened")
def forget_all_of_it(account: CurrentAccount, request: Request) -> Any:
    """All of it, at once. There is no forgetting one afternoon: choosing which parts of a
    history to keep is the beginning of curating a person.

    Both stores, because they are one memory. Clearing the afternoons and leaving the series
    of placed pages behind would leave the house pitched by a record the parent believes
    they deleted, which is worse than not offering to delete it.
    """
    memory: WhatHappenedStore = request.app.state.what_happened
    memory.forget(account.household_id)
    seen: NoticedStore = request.app.state.noticed
    seen.forget(account.household_id)
    return {"forgotten": True}


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
