"""Core domain objects.

These live on the hub. Nothing here is barred from a model prompt: the cloud tier holds
personal material on the same terms as the house (see docs/THREAT-MODEL.md).
``LearnerProfile.prompt_hints`` is what callers send today because it is the only subset
anyone has asked for.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .ids import ExerciseId, LearnerId, RoutineId, SessionId, SheetId


class ActivityKind(StrEnum):
    INTERACTIVE_GAME = "interactive_game"  # on the LCD, driven by the buttons
    PRINTED_EXERCISE = "printed_exercise"  # a sheet to print, do, and read back
    ROUTINE_PROMPT = "routine_prompt"  # a daily-routine nudge on an e-paper display


class Difficulty(StrEnum):
    """Coarse on purpose. This is a content setting the parent chooses, not a measurement
    of the person — the system does not assess or score anyone. See docs/NON-GOALS.md."""

    GENTLE = "gentle"
    STEADY = "steady"
    STRETCH = "stretch"


class ContentVariety(StrEnum):
    """How often content changes form. The parent's starting point, not a ceiling."""

    FAMILIAR = "familiar"
    BALANCED = "balanced"
    FREQUENT = "frequent"


@dataclass(frozen=True, slots=True)
class LearnerProfile:
    """Who this is, as far as the house is concerned. It lives on the hub.

    What reaches a model is :meth:`prompt_hints`, which is narrower than this type — not
    because a name may not be sent, since that ban was dropped on 19 August 2026, but
    because no field beyond these has been asked for yet. Widening it is a decision
    somebody makes for a named field, not a default.

    Contains the minimum needed to pick appropriate content. It holds no diagnosis and no
    clinical data, and nothing here is a verdict: what the system learns from what comes
    back does not live in this type.
    """

    id: LearnerId
    display_name: str
    # Free-text preferences the parent writes, e.g. "likes animals, dislikes loud sounds".
    interests: tuple[str, ...] = ()
    avoid: tuple[str, ...] = ()
    default_difficulty: Difficulty = Difficulty.GENTLE
    content_variety: ContentVariety = ContentVariety.BALANCED
    # Reading support: max words per line the displays should show.
    max_words_per_line: int = 6
    language: str = "it"

    def prompt_hints(self) -> dict[str, Any]:
        """What callers send today: the content settings, and neither name nor id — because
        no wider field has been asked for, not because one may not be sent."""
        return {
            "interests": list(self.interests),
            "avoid": list(self.avoid),
            "difficulty": str(self.default_difficulty),
            "content_variety": str(self.content_variety),
            "language": self.language,
            "max_words_per_line": self.max_words_per_line,
        }


@dataclass(frozen=True, slots=True)
class Exercise:
    """A unit of generated content, before it is laid out or displayed."""

    id: ExerciseId
    kind: ActivityKind
    title: str
    instructions: str
    # Question/answer material; shape depends on `kind`. Validated by the content agent.
    items: tuple[dict[str, Any], ...] = ()
    difficulty: Difficulty = Difficulty.GENTLE
    created_at: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RoutineStep:
    """One step of a daily routine, shown as a prompt at a scheduled time."""

    id: RoutineId
    label: str
    # Local time in 24h "HH:MM". Wall-clock, not an interval — routines anchor to the day.
    at: str
    days: tuple[int, ...] = (0, 1, 2, 3, 4, 5, 6)  # Monday = 0
    icon: str = ""


@dataclass(frozen=True, slots=True)
class PlannedActivity:
    """One entry in a day's plan. Still only a suggestion until the parent approves it."""

    kind: ActivityKind
    exercise_id: ExerciseId | None
    routine_id: RoutineId | None
    scheduled_for: str  # "HH:MM"
    rationale: str = ""


@dataclass(frozen=True, slots=True)
class DayPlan:
    learner_id: LearnerId
    date: str  # ISO "YYYY-MM-DD"
    activities: tuple[PlannedActivity, ...]
    generated_at: float = 0.0


class SessionOutcome(StrEnum):
    COMPLETED = "completed"
    PARTIAL = "partial"
    ABANDONED = "abandoned"
    NEEDS_REVIEW = "needs_review"


@dataclass(frozen=True, slots=True)
class Session:
    """A record that an activity happened. Kept so the parent can look back.

    It records *what the system did*, not conclusions about the person. There is no score,
    no trend line, and no derived rating anywhere in this type.
    """

    id: SessionId
    learner_id: LearnerId
    kind: ActivityKind
    started_at: float
    ended_at: float | None = None
    exercise_id: ExerciseId | None = None
    sheet_id: SheetId | None = None
    outcome: SessionOutcome | None = None
    notes: str = ""
