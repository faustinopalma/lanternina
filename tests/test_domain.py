"""Domain settings describe explicit choices, never inferred traits."""

from __future__ import annotations

from shared.domain import ContentVariety, Difficulty, LearnerProfile
from shared.ids import LearnerId


def test_prompt_hints_include_explicit_variety_without_identity() -> None:
    profile = LearnerProfile(
        id=LearnerId("learner-local"),
        display_name="Local name",
        interests=("drawing",),
        default_difficulty=Difficulty.STEADY,
        content_variety=ContentVariety.FREQUENT,
    )

    hints = profile.prompt_hints()

    assert hints["content_variety"] == "frequent"
    assert hints["difficulty"] == "steady"
    assert "id" not in hints
    assert "display_name" not in hints
    assert "performance" not in hints