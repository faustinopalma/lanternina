"""Revisioned household guidance and feedback awaiting synthesis."""

from __future__ import annotations

import threading
from dataclasses import dataclass, field, replace
from typing import Any, Protocol

from shared.steering import MAX_GUIDANCE_CHARS, MAX_SUMMARY_CHARS, Steering, clean_text

MAX_COMMENT_CHARS = 2000
MAX_PENDING = 50
REASONS = {
    "too_difficult": "Reduce the reasoning or prerequisite knowledge required.",
    "too_easy": "Offer a more substantial challenge.",
    "too_abstract": "Use more concrete material and observable actions.",
    "too_closed": "Allow more choices or more than one defensible result.",
    "too_open": "Give a more defined task and a clear completion criterion.",
    "unclear": "Make instructions and supplied evidence unambiguous.",
    "too_much_reading": "Reduce the reading required to start and continue.",
    "too_much_writing": "Reduce required writing; permit other responses.",
    "too_much_help": "Reduce the adult assistance required.",
    "not_interesting": "Reconsider the topic or activity, using the comment.",
}


class SteeringConflict(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class Feedback:
    id: str
    experience_id: str
    title: str
    reasons: tuple[str, ...]
    comment: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "experienceId": self.experience_id,
            "title": self.title,
            "reasons": list(self.reasons),
            "comment": self.comment,
        }


def clean_feedback(
    identifier: str, experience_id: str, title: str, reasons: list[str], comment: str
) -> Feedback:
    selected = tuple(dict.fromkeys(reasons))
    if any(reason not in REASONS for reason in selected):
        raise ValueError("unknown feedback reason")
    if {"too_difficult", "too_easy"} <= set(selected):
        raise ValueError("choose one difficulty direction")
    if {"too_closed", "too_open"} <= set(selected):
        raise ValueError("choose one openness direction")
    return Feedback(
        identifier, experience_id, title, selected, clean_text(comment, MAX_COMMENT_CHARS)
    )


@dataclass(frozen=True, slots=True)
class Guidance:
    household_id: str
    steering: Steering
    revision: int = 0
    pending: tuple[Feedback, ...] = ()
    history: tuple[Feedback, ...] = ()
    feedback_count: int = 0

    def edited(self, instructions: str, adaptive: str) -> Guidance:
        return replace(
            self,
            steering=Steering(
                clean_text(instructions, MAX_GUIDANCE_CHARS),
                clean_text(adaptive, MAX_SUMMARY_CHARS),
            ),
        )

    def reset_adaptive(self, language: str) -> Guidance:
        return replace(
            self,
            steering=replace(self.steering, adaptive=Steering.initial(language).adaptive),
            pending=(),
            history=(),
            feedback_count=0,
        )

    def receive(self, feedback: Feedback) -> Guidance:
        if any(entry.id == feedback.id for entry in (*self.pending, *self.history)):
            return self
        if len(self.pending) >= MAX_PENDING:
            raise ValueError("feedback synthesis is pending; retry after it completes")
        return replace(
            self, pending=(*self.pending, feedback), feedback_count=self.feedback_count + 1
        )

    def summarized(self, text: str) -> Guidance:
        summary = clean_text(text, MAX_SUMMARY_CHARS)
        if not summary:
            raise ValueError("feedback summary is empty")
        return replace(
            self,
            steering=replace(self.steering, adaptive=summary),
            history=(*self.history, *self.pending)[-50:],
            pending=(),
        )

    def to_public(self, language: str) -> dict[str, Any]:
        initial = Steering.initial(language)
        return {
            "instructions": self.steering.instructions,
            "adaptive": self.steering.adaptive,
            "revision": self.revision,
            "pendingCount": len(self.pending),
            "feedbackCount": self.feedback_count,
            "defaultInstructions": initial.instructions,
            "defaultAdaptive": initial.adaptive,
            "instructionsLimit": MAX_GUIDANCE_CHARS,
            "adaptiveLimit": MAX_SUMMARY_CHARS,
            "reasons": list(REASONS),
            "commentLimit": MAX_COMMENT_CHARS,
        }


class SteeringStore(Protocol):
    def get(self, household_id: str, language: str = "it") -> Guidance: ...

    def save(self, value: Guidance, expected_revision: int) -> Guidance: ...


@dataclass
class InMemorySteeringStore:
    _rows: dict[str, Guidance] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def get(self, household_id: str, language: str = "it") -> Guidance:
        with self._lock:
            return self._rows.get(household_id, Guidance(household_id, Steering.initial(language)))

    def save(self, value: Guidance, expected_revision: int) -> Guidance:
        with self._lock:
            stored = self._rows.get(value.household_id)
            revision = stored.revision if stored else 0
            if revision != expected_revision:
                raise SteeringConflict("guidance_changed")
            saved = replace(value, revision=revision + 1)
            self._rows[value.household_id] = saved
            return saved
