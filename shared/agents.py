"""Agent interfaces.

Every agent is reached through one of these protocols. No agent imports another agent —
the planner in ``orchestrator/`` is the only thing that holds more than one, and it wires
them together through these types. ``tests/test_boundaries.py`` enforces that mechanically.

Note what :class:`AgentContext` contains, and what it does not:

* it **has** the model router, a clock, and the learner's redacted prompt hints;
* it **has no** approval ledger — an agent cannot approve anything;
* it **has no** safety gate — an agent never sees unscreened text, so it cannot
  accidentally route around screening;
* it **has no** Azure client or model handle — those live behind the router.

Every method returns a :class:`~shared.proposal.Proposal`. That is the whole vocabulary an
agent has for affecting the world.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from .domain import ActivityKind, Difficulty, LearnerProfile
from .ids import ExerciseId, LearnerId
from .page import Page
from .proposal import Proposal
from .routing import ModelRouter, PageImage
from .vision_contracts import WhatCameBack


@dataclass(frozen=True, slots=True)
class AgentContext:
    """Everything an agent is allowed to touch."""

    router: ModelRouter
    learner_id: LearnerId
    # What LearnerProfile.prompt_hints() returns; no wider field has been asked for yet.
    learner_hints: dict[str, Any]
    now: float

    @staticmethod
    def for_learner(
        router: ModelRouter, profile: LearnerProfile, now: float
    ) -> AgentContext:
        return AgentContext(
            router=router,
            learner_id=profile.id,
            learner_hints=profile.prompt_hints(),
            now=now,
        )


@runtime_checkable
class Agent(Protocol):
    """Common surface, mostly so the planner can log and report uniformly."""

    @property
    def name(self) -> str:
        """Stable identifier recorded on every proposal this agent produces."""
        ...


@runtime_checkable
class ContentAgent(Agent, Protocol):
    """Generates activities and the words the learner will see."""

    async def propose_exercise(
        self,
        ctx: AgentContext,
        *,
        kind: ActivityKind,
        difficulty: Difficulty,
        topic_hint: str = "",
    ) -> Proposal:
        """Propose one exercise. Payload kind: EXERCISE_JSON."""
        ...


@runtime_checkable
class PageAgent(Agent, Protocol):
    """Draws the whole page. The words on it were written and screened elsewhere."""

    async def draw(self, ctx: AgentContext, page: Page) -> Any:
        """One page, as a grey image. Payload kind: IMAGE_PNG."""
        ...


@runtime_checkable
class VisionAgent(Agent, Protocol):
    """Reads a page against the blank it was printed from. Produces observations.

    The one agent that does not emit a Proposal: a reading is a description of ink on
    paper, not content headed for anybody. It says what was added and whether the sheet
    looks like the one that was handed over, and it has no field in which to say anything
    about the person who wrote on it.
    """

    async def read(
        self,
        ctx: AgentContext,
        *,
        blank: PageImage,
        came_back: PageImage,
        about: str = "",
    ) -> WhatCameBack:
        """What is on the second image that is not on the first.

        Must set ``degraded`` rather than inventing an answer when it could not tell, and
        must never say whether anything is right: there is nothing here to get wrong.
        """
        ...


@runtime_checkable
class SchedulingAgent(Agent, Protocol):
    """Decides what happens when, across the day."""

    async def propose_day_plan(
        self, ctx: AgentContext, *, date: str, available_exercises: tuple[ExerciseId, ...]
    ) -> Proposal:
        """Propose a plan for one day. Payload kind: EXERCISE_JSON (a serialised DayPlan)."""
        ...


@runtime_checkable
class PrintAgent(Agent, Protocol):
    """Turns approved content into a printable sheet that vision can read back."""

    async def propose_sheet(
        self, ctx: AgentContext, *, exercise_payload: str, exercise_id: ExerciseId
    ) -> Proposal:
        """Propose a print layout for an already-approved exercise.

        The layout must satisfy :mod:`shared.sheet`: four corner markers, a QR code in
        ``qr_rect``, and every answerable region declared as a :class:`CellSpec`.
        Payload kind: PRINT_LAYOUT_JSON.
        """
        ...
