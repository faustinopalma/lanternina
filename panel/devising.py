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

from panel.preferences import DEFAULT_DIFFICULTY, DEFAULT_VARIETY, WORDS_PER_LINE
from shared.agents import AgentContext
from shared.capabilities import HouseCapability
from shared.experience import Drawn, Experience, ExperienceError
from shared.experience_checks import Complaint, check
from shared.ids import LearnerId
from shared.routing import ModelUsage
from shared.seal import Sealer, SealPurpose

# How many times a refused afternoon is handed back to be repaired. One.
REPAIRS: int = 1


class RefusedByTheChecks(ValueError):
    """An afternoon that parses and cannot be run well, after it was given its repair."""

    def __init__(self, complaints: Sequence[Complaint]) -> None:
        super().__init__("; ".join(str(complaint) for complaint in complaints))
        self.complaints = tuple(complaints)


async def devise_experience(
    *,
    capabilities: frozenset[HouseCapability],
    language: str,
    interests: tuple[str, ...],
    avoid: tuple[str, ...],
    already: tuple[str, ...],
    recent: Sequence[Drawn] = (),
    subjects: Sequence[str] = (),
    brief: str = "",
    difficulty: str = DEFAULT_DIFFICULTY,
    variety: str = DEFAULT_VARIETY,
    note: str = "",
    words_per_line: int = WORDS_PER_LINE,
    now: float,
) -> tuple[Experience, ModelUsage | None]:
    """One afternoon, checked, repaired if it had to be, screened, and what it consumed.

    ``difficulty`` is the shape the parent chose in the panel, and it arrives as a word
    rather than as a sentence so that the sentence sent to the model lives beside the rest
    of the prompt. It says how many things an afternoon holds together at once. It reaches
    the prompt and nothing else: no afternoon carries a field for it, and
    `tests/test_experience.py` refuses one that does.

    ``brief`` is a parent's own idea, worked on in the panel and approved. It replaces the
    invitation to invent rather than sitting beside it, and nothing else is relaxed: the
    format, the checks and the gate all run unchanged, so a script asking for a scoreboard
    is refused the same way whoever wrote it.

    Raises whatever the router raises when the cloud will not serve it,
    :class:`~shared.errors.SafetyBlocked` when the gate refuses it,
    :class:`~shared.experience.ExperienceError` when it is not an experience at all, and
    :class:`RefusedByTheChecks` when it is one that cannot be run well.
    """
    from agents.experience_deviser import (
        DISTANCES,
        SHAPES,
        ExperienceDeviser,
        experience_in,
    )
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
    # An empty learner and empty hints: an experience carries nothing about a person, and
    # handing the agent nothing is the cheapest way to keep that true as the prompt grows.
    context = AgentContext(router=router, learner_id=LearnerId(""), learner_hints={}, now=now)
    deviser = ExperienceDeviser()
    log = logging.getLogger(__name__)
    try:
        answer = await deviser.ask(
            context,
            capabilities=capabilities,
            language=language,
            interests=interests,
            avoid=avoid,
            already=already,
            recent=recent,
            subjects=subjects,
            brief=brief,
            shape=SHAPES.get(difficulty, SHAPES[DEFAULT_DIFFICULTY]),
            distance=DISTANCES.get(variety, DISTANCES[DEFAULT_VARIETY]),
            note=note,
            words_per_line=words_per_line,
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
        complaints = check(experience, recent=recent)
        for _ in range(REPAIRS):
            if not complaints:
                break
            # The complaints go in the log because a check that fires every time is a
            # defect in the prompt, and nothing else here would ever show that.
            log.info("afternoon refused by the checks: %s", "; ".join(map(str, complaints)))
            experience = await deviser.repair(
                context, refused=experience, complaints=complaints, language=language
            )
            complaints = check(experience, recent=recent)
        if complaints:
            raise RefusedByTheChecks(complaints)
        # The chokepoint. Nothing above it may return early past it: the parse and the
        # checks can refuse, but only screening lets something through.
        await screen_experience(gate, experience, context="devising an afternoon")
    finally:
        await gate.aclose()
    return experience, router.last_usage
