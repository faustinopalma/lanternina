"""A parent working on an idea: the conversation, the text, and what becomes of it.

**These routes spend money, and they are the only ones a parent can spend it with.**
`docs/NON-GOALS.md` was amended rather than quietly bent. What the inertness rule protects
is the house: nothing here starts an afternoon, wakes the hub, notifies anybody, or puts
anything in a room. A parent working on their own draft touches none of that, the monthly
limit governs it like every other call, and what comes out still waits to be approved and
still waits for the house to come and ask.

Four things a parent can do to a draft, and the shapes below are all of them. **Say**
something, which costs a call and rewrites the text. **Type**, which costs nothing and is
the same inert write every other panel route is — a parent who wants to change one word
should not have to ask for it. **Approve**, which hands the script to the deviser as a brief
and stores what comes back the way an approved afternoon is stored. **Close**, which throws
it away.

Nothing here carries anything about an adolescent, and there is no field one would fit in.
"""

from __future__ import annotations

import logging
import time
from dataclasses import replace
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from shared.approval import ApprovalState
from shared.capabilities import HouseCapability
from shared.errors import CloudUnavailable, NoCapacityError, SafetyBlocked
from shared.experience import ExperienceError
from shared.ids import new_id

from ..config import Settings
from ..drafts import (
    APPROVED,
    CLOSED,
    MAX_TURNS,
    OPEN,
    THE_PARENT,
    THE_SYSTEM,
    Draft,
    DraftStore,
    Said,
    cleaned,
)
from ..experiences import ExperienceStore, OfferedExperience
from ..gate import CurrentAccount
from ..preferences import LANGUAGE_NAMES, PreferencesStore
from ..usage import FAILED, KIND_TEXT, REFUSED, SERVED, UsageStore, at_the_limit, event_from

router = APIRouter()

# What a house is assumed to have when a parent's idea is turned into an afternoon. The
# hub reports its own equipment when it asks for one; here nobody is asking, so this is the
# floor every household in this project has. An afternoon needing more than this would be
# refused by the runner rather than by us, which is the right place for that to happen.
ASSUMED = frozenset(
    {
        HouseCapability.PRINT_A4,
        HouseCapability.SCAN_A4,
        HouseCapability.SHOW_800X480_1BIT,
    }
)


class WhereToStart(BaseModel):
    """Blank, or from an afternoon that already exists."""

    model_config = ConfigDict(extra="forbid")

    fromExperience: str = ""


@router.post("/api/drafts")
def start_one(where: WhereToStart, account: CurrentAccount, request: Request) -> Any:
    """Open a draft. Inert: no model is called until the parent says something."""
    store: DraftStore = request.app.state.drafts
    household = str(account.household_id)
    now = time.time()
    draft = Draft(id=str(new_id("dft")), household_id=household, created_at=now, updated_at=now)
    if where.fromExperience:
        experiences: ExperienceStore = request.app.state.experiences
        offered = experiences.get(household, where.fromExperience)
        if offered is None:
            raise HTTPException(status_code=404, detail="unknown_experience")
        # A copy. Editing a draft never reaches back into what it was opened from, so a
        # parent can take an afternoon apart without losing the one they had.
        document = offered.experience
        draft = replace(
            draft,
            title=str(document.get("title") or ""),
            overview=str(document.get("overview") or ""),
            themes=tuple(str(one) for one in (document.get("themes") or ())),
            script=str(document.get("script") or ""),
            started_from=where.fromExperience,
        )
    return store.start(draft).to_public()


@router.get("/api/drafts")
def the_drafts(account: CurrentAccount, request: Request) -> Any:
    """The cards. No conversation and no script: a list of drafts is not a read."""
    store: DraftStore = request.app.state.drafts
    return {"drafts": [row.summary() for row in store.list(str(account.household_id))]}


@router.get("/api/drafts/{draft_id}")
def one_draft(draft_id: str, account: CurrentAccount, request: Request) -> Any:
    return _theirs(request, account, draft_id).to_public()


class Typed(BaseModel):
    """The text as the parent left it. Absent fields keep what was there."""

    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    overview: str | None = None
    themes: list[str] | None = None
    script: str | None = None


@router.post("/api/drafts/{draft_id}/text")
def typed(draft_id: str, what: Typed, account: CurrentAccount, request: Request) -> Any:
    """The parent typed in the text themselves. Inert, like every other panel write.

    Nothing is called and nothing is checked here beyond the format's own lengths. A parent
    changing one word should not have to ask a model for it, and should not pay for it.
    """
    store: DraftStore = request.app.state.drafts
    draft = _open(_theirs(request, account, draft_id))
    try:
        kept = replace(
            draft,
            title=_or(what.title, draft.title, "the title"),
            overview=_or(what.overview, draft.overview, "the overview"),
            script=_or(what.script, draft.script, "the script"),
            themes=(
                draft.themes
                if what.themes is None
                else tuple(str(one).strip() for one in what.themes if str(one).strip())
            ),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return store.save(kept).to_public()


class Saying(BaseModel):
    """One thing the parent said to the model about their draft."""

    model_config = ConfigDict(extra="forbid")

    words: str = Field(min_length=1)


@router.post("/api/drafts/{draft_id}/say")
async def say(draft_id: str, what: Saying, account: CurrentAccount, request: Request) -> Any:
    """One turn: the parent's message goes up, the rewritten idea comes back.

    Refused rather than degraded when the cap is reached or the cloud is away. There is no
    reduced version of a rewrite, and a parent who is told plainly can type it themselves —
    the text is right there and open.
    """
    settings: Settings = request.app.state.settings
    counter: UsageStore = request.app.state.usage
    household = str(account.household_id)
    if at_the_limit(counter, request.app.state.limit, household, settings.monthly_limit):
        raise HTTPException(status_code=429, detail="monthly_cap_reached")

    store: DraftStore = request.app.state.drafts
    draft = _open(_theirs(request, account, draft_id))
    if len(draft.said) >= MAX_TURNS:
        raise HTTPException(status_code=409, detail="conversation_too_long")
    try:
        words = cleaned(what.words, "what you said")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not words:
        raise HTTPException(status_code=400, detail="say something")

    preferences: PreferencesStore = request.app.state.preferences
    chosen = preferences.get(household)
    from ..editing import rewrite_the_idea

    spent: Any = None
    outcome = FAILED
    try:
        idea, spent = await rewrite_the_idea(
            language=LANGUAGE_NAMES.get(chosen.language, chosen.language),
            title=draft.title,
            overview=draft.overview,
            themes=draft.themes,
            script=draft.script,
            said=draft.carrying(),
            asking=words,
            now=time.time(),
        )
        outcome = SERVED
    except SafetyBlocked as exc:
        outcome = REFUSED
        logging.getLogger(__name__).info("a turn was refused: %s", exc)
        raise HTTPException(status_code=422, detail="refused_by_the_gate") from exc
    except ExperienceError as exc:
        logging.getLogger(__name__).warning("not an idea: %s", exc)
        raise HTTPException(status_code=502, detail=f"not_an_idea: {exc}") from exc
    except (NoCapacityError, CloudUnavailable, ValueError) as exc:
        logging.getLogger(__name__).warning("the idea was not rewritten: %s", exc)
        raise HTTPException(status_code=503, detail=f"unavailable: {exc}") from exc
    finally:
        _count(counter, household, outcome, spent)

    now = time.time()
    kept = store.save(
        replace(
            draft,
            title=idea.title,
            overview=idea.overview,
            themes=idea.themes,
            script=idea.script,
            said=(
                *draft.said,
                Said(who=THE_PARENT, words=words, at=now),
                Said(who=THE_SYSTEM, words=idea.reply, at=now),
            ),
        )
    )
    return kept.to_public()


@router.post("/api/drafts/{draft_id}/approve")
async def approve(draft_id: str, account: CurrentAccount, request: Request) -> Any:
    """Turn the idea into an afternoon a house can run, approved and waiting.

    The deviser writes the plan from the script as a brief, and nothing is relaxed because
    a parent wrote it: the format, the checks and the gate all run. A refusal comes back
    with its reason, because the parent can change the text and try again — which is the
    whole point of them having the text.
    """
    settings: Settings = request.app.state.settings
    counter: UsageStore = request.app.state.usage
    household = str(account.household_id)
    if at_the_limit(counter, request.app.state.limit, household, settings.monthly_limit):
        raise HTTPException(status_code=429, detail="monthly_cap_reached")

    store: DraftStore = request.app.state.drafts
    draft = _open(_theirs(request, account, draft_id))
    if not draft.script.strip():
        raise HTTPException(status_code=400, detail="nothing_to_approve")

    preferences: PreferencesStore = request.app.state.preferences
    chosen = preferences.get(household)
    from ..devising import RefusedByTheChecks
    from ..editing import afternoon_from

    spent: Any = None
    outcome = FAILED
    try:
        experience, spent = await afternoon_from(
            brief=_brief(draft),
            capabilities=ASSUMED,
            language=LANGUAGE_NAMES.get(chosen.language, chosen.language),
            interests=chosen.interests,
            avoid=chosen.avoid,
            difficulty=chosen.difficulty,
            variety=chosen.variety,
            sheets=chosen.sheets,
            note=chosen.standing(time.time()),
            now=time.time(),
        )
        outcome = SERVED
    except SafetyBlocked as exc:
        outcome = REFUSED
        logging.getLogger(__name__).info("a draft was refused by the gate: %s", exc)
        raise HTTPException(status_code=422, detail="refused_by_the_gate") from exc
    except RefusedByTheChecks as exc:
        outcome = REFUSED
        logging.getLogger(__name__).info("a draft was refused by the checks: %s", exc)
        raise HTTPException(status_code=422, detail=f"refused_by_the_checks: {exc}") from exc
    except ExperienceError as exc:
        logging.getLogger(__name__).warning("a draft did not become an afternoon: %s", exc)
        raise HTTPException(status_code=502, detail=f"not_an_experience: {exc}") from exc
    except (NoCapacityError, CloudUnavailable, ValueError) as exc:
        logging.getLogger(__name__).warning("the afternoon was not written: %s", exc)
        raise HTTPException(status_code=503, detail=f"unavailable: {exc}") from exc
    finally:
        _count(counter, household, outcome, spent)

    experiences: ExperienceStore = request.app.state.experiences
    now = time.time()
    stored = experiences.offer(
        OfferedExperience(
            id=experience.experience_id,
            household_id=household,
            experience=experience.to_dict(),
            created_at=now,
            # Approved on the way in, and that is not a shortcut: the parent wrote this one
            # and pressed approve on it. Asking them to find it in the pending list and
            # approve it again would be asking twice for one decision.
            state=ApprovalState.APPROVED.value,
            decided_at=now,
            decided_by=str(account.id),
        )
    )
    store.save(replace(draft, state=APPROVED, became=stored.id))
    return {"id": stored.id, "title": stored.title, "state": stored.state}


@router.post("/api/drafts/{draft_id}/close")
def close(draft_id: str, account: CurrentAccount, request: Request) -> Any:
    """Throw it away. Kept as a row so a parent can see what they abandoned."""
    store: DraftStore = request.app.state.drafts
    draft = _theirs(request, account, draft_id)
    if draft.state == APPROVED:
        raise HTTPException(status_code=409, detail="already_approved")
    return store.save(replace(draft, state=CLOSED)).to_public()


def _theirs(request: Request, account: CurrentAccount, draft_id: str) -> Draft:
    store: DraftStore = request.app.state.drafts
    found = store.get(str(account.household_id), draft_id)
    if found is None:
        raise HTTPException(status_code=404, detail="unknown_draft")
    return found


def _open(draft: Draft) -> Draft:
    if draft.state != OPEN:
        raise HTTPException(status_code=409, detail=f"the draft is {draft.state}")
    return draft


def _or(given: str | None, kept: str, name: str) -> str:
    if given is None:
        return kept
    if not isinstance(given, str):
        raise ValueError(f"{name} is text")
    return given


def _brief(draft: Draft) -> str:
    """The draft as one document for the deviser. The script does most of the work."""
    parts = [f"TITLE: {draft.title}" if draft.title else ""]
    if draft.overview:
        parts.append(f"OVERVIEW: {draft.overview}")
    if draft.themes:
        parts.append(f"THEMES: {', '.join(draft.themes)}")
    parts.append(draft.script)
    return "\n\n".join(one for one in parts if one)


def _count(counter: UsageStore, household_id: str, outcome: str, spent: Any) -> None:
    """Write down what a call consumed. Never raises: the call was already paid for."""
    try:
        counter.record(
            event_from(household_id, KIND_TEXT, outcome, spent, event_id=str(new_id("use")))
        )
    except Exception as exc:  # noqa: BLE001 - bookkeeping must not eat a turn
        logging.getLogger(__name__).warning("usage not recorded: %s", exc)
