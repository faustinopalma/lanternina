"""Devising an afternoon, because the house asked whether there was one to be had.

Why here and not in the house: this container holds the managed identity with access to
Foundry and to Content Safety, so nothing in the home needs a credential of its own. The
same reason `panel/continuing.py` and `panel/wording.py` are here.

When this runs is not decided here, and that is the rule this feature would break if it
were. A write from the panel is inert, so a parent asking for an afternoon cannot cause
one to be written: nothing in the panel calls this. It is called inside the reply to a
request the hub made, on the rhythm the hub already has, and what comes back waits for a
parent to read it.

The gate is called before the document is stored, not before it is played. An experience
sits in the panel where a parent reads it, so screening it late would mean an adult was
shown model output nobody had looked at — and by then the same words have been stored.

**The checks run before the gate, and a refused afternoon is repaired once.** The order
matters: the checks cost nothing and the gate costs a network call, so there is no reason
to screen a document that is going to be sent back anyway. One repair and no more, because
the point of the loop is to fix the one thing a model usually gets wrong, not to keep
trying — a second failure is a defect in the prompt and should be visible as a house that
was offered no afternoon rather than hidden behind three retries.
"""

from __future__ import annotations

import logging
import os
import secrets
from collections.abc import Sequence
from typing import Any

from panel.preferences import DEFAULT_SHEETS, WORDS_PER_LINE
from shared.agents import AgentContext
from shared.capabilities import HouseCapability
from shared.experience import Drawn, Experience, ExperienceError
from shared.experience_checks import Complaint, check
from shared.ids import LearnerId
from shared.methods import CATALOGUE, Method, by_id, draw, index, load, runnable
from shared.routing import ModelUsage
from shared.seal import Sealer, SealPurpose

# How many times a refused afternoon is handed back to be repaired. One.
REPAIRS: int = 1


class RefusedByTheChecks(ValueError):
    """An afternoon that parses and cannot be run well, after it was given its repair."""

    def __init__(self, complaints: Sequence[Complaint]) -> None:
        super().__init__("; ".join(str(complaint) for complaint in complaints))
        self.complaints = tuple(complaints)


async def _what_to_build_out_of(
    deviser: Any,
    context: Any,
    *,
    capabilities: frozenset[HouseCapability],
    interests: tuple[str, ...],
    avoid: tuple[str, ...],
    already: tuple[str, ...],
    pitch: str,
    log: logging.Logger,
) -> tuple[Method | None, Method | None]:
    """One form and one move out of `methods/`, asked for by the model and drawn if it cannot.

    The filter is here because this is where the house's equipment is known, and it is what
    makes *a house is never offered a form it cannot run* a property rather than a hope.
    The choosing is a model call over names only; everything that can go wrong with it ends
    in a draw, because a step that exists to improve an afternoon may never be the step that
    costs one.
    """
    here = runnable(load(), capabilities=capabilities)
    if not here:
        return (None, None)
    try:
        wants_form, wants_move, why = await deviser.choose(
            context,
            catalogue=index(here, sample=CATALOGUE),
            interests=interests,
            avoid=avoid,
            already=already,
            pitch=pitch,
        )
        asked = by_id(here, [wants_form, wants_move])
        form = next((one for one in asked if not one.is_a_move), None)
        move = next((one for one in asked if one.is_a_move), None)
        if form is not None and move is not None:
            log.info("chose %r with %r: %s", form.method_id, move.method_id, why)
            return (form, move)
        log.info("the choice named %r and %r; drawing instead", wants_form, wants_move)
    except Exception as exc:  # noqa: BLE001 - a failed lookup may not cost the afternoon
        log.info("choosing a method failed, drawing instead: %s", exc)
    form, move = draw(here)
    if form is not None and move is not None:
        log.info("drew %r with %r", form.method_id, move.method_id)
    return (form, move)


async def devise_experience(
    *,
    capabilities: frozenset[HouseCapability],
    language: str,
    interests: tuple[str, ...],
    avoid: tuple[str, ...],
    already: tuple[str, ...],
    recent: Sequence[Drawn] = (),
    happened: str = "",
    counts: str = "",
    direction: str = "",
    ground: str = "",
    brief: str = "",
    pitch: str = "",
    note: str = "",
    sheets: int = DEFAULT_SHEETS,
    words_per_line: int = WORDS_PER_LINE,
    built_from: dict[str, str] | None = None,
    now: float,
) -> tuple[Experience, ModelUsage | None]:
    """One afternoon, checked, repaired if it had to be, screened, and what it consumed.

    ``pitch`` is :meth:`shared.profile.Profile.as_material`: one sentence per axis this
    house has enough evidence for, saying how much an afternoon should hold, how much a
    sheet should ask for and how long it should run. Empty is ordinary and means the block
    is left out. It reaches the prompt and nothing else: no afternoon carries a field for
    it, and `tests/test_experience.py` refuses one that does.

    ``brief`` is a parent's own idea, worked on in the panel and approved. It replaces the
    invitation to invent rather than sitting beside it, and nothing else is relaxed: the
    format, the checks and the gate all run unchanged, so a script asking for a scoreboard
    is refused the same way whoever wrote it.

    ``built_from`` is a sink a caller may pass to learn which method this afternoon was made
    out of; it is filled with ``form`` and ``move`` ids and left alone otherwise. It is a
    parameter rather than a third value in the tuple because it is a diagnostic and only the
    research loop wants it — and rather than a log line the loop reads back, because a log
    line that somebody rewords stops being read and says nothing about having stopped.

    Raises whatever the router raises when the cloud will not serve it,
    :class:`~shared.errors.SafetyBlocked` when the gate refuses it,
    :class:`~shared.experience.ExperienceError` when it is not an experience at all, and
    :class:`RefusedByTheChecks` when it is one that cannot be run well.
    """
    from agents.experience_deviser import ExperienceDeviser, experience_in
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import (
        AzureContentSafetyGate,
        ContentSafetyConfig,
        screen_experience,
    )

    environment = dict(os.environ)
    # As on the continuing path: the seal this gate mints travels nowhere, because the
    # house is handed moments and not a sealed payload. A per-process key keeps the gate
    # honest without pretending otherwise.
    key = environment.get("LANTERNINA_SAFETY_KEY", "").encode() or secrets.token_bytes(32)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, key, "orchestrator.safety"),
    )
    router = FoundryRouter(FoundryConfig.from_env(environment), gate=gate)
    # No learner and no hints: what an afternoon is written from is the household's
    # settings and what its afternoons came to, both of which are arguments above.
    context = AgentContext(router=router, learner_id=LearnerId(""), learner_hints={}, now=now)
    deviser = ExperienceDeviser()
    log = logging.getLogger(__name__)
    form, move = await _what_to_build_out_of(
        deviser,
        context,
        capabilities=capabilities,
        interests=interests,
        avoid=avoid,
        already=already,
        pitch=pitch,
        log=log,
    )
    if built_from is not None and form is not None and move is not None:
        built_from["form"] = form.method_id
        built_from["move"] = move.method_id
    try:
        answer = await deviser.ask(
            context,
            capabilities=capabilities,
            language=language,
            interests=interests,
            avoid=avoid,
            already=already,
            recent=recent,
            happened=happened,
            counts=counts,
            direction=direction,
            ground=ground,
            brief=brief,
            pitch=pitch,
            note=note,
            sheets=sheets,
            words_per_line=words_per_line,
            form=form,
            move=move,
        )
        try:
            experience = experience_in(answer)
        except ExperienceError as exc:
            # A document the format will not read at all. Two of seven answers from the
            # real service on 23 August 2026 were refused this way, both for a line one
            # character or one line over, and before this the house was simply offered no
            # afternoon. The parser's message names the rule and the offending number, so
            # it is worth handing back.
            log.info("afternoon refused by the format: %s", exc)
            experience = await deviser.repair_unreadable(
                context, answer=answer, refusal=str(exc), language=language
            )
        complaints = check(experience, recent=recent, sheets_at_most=sheets)
        for _ in range(REPAIRS):
            if not complaints:
                break
            # The complaints go in the log because a check that fires every time is a
            # defect in the prompt, and nothing else here would ever show that.
            log.info("afternoon refused by the checks: %s", "; ".join(map(str, complaints)))
            experience = await deviser.repair(
                context, refused=experience, complaints=complaints, language=language
            )
            complaints = check(experience, recent=recent, sheets_at_most=sheets)
        if complaints:
            raise RefusedByTheChecks(complaints)
        # The chokepoint. Nothing above it may return early past it: the parse and the
        # checks can refuse, but only screening lets something through.
        await screen_experience(gate, experience, context="devising an afternoon")
    finally:
        await gate.aclose()
    return experience, router.last_usage
