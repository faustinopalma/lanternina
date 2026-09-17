from __future__ import annotations

import json

import pytest

from panel.steering import InMemorySteeringStore, SteeringConflict, clean_feedback
from shared.steering import Steering


def test_guidance_round_trip_and_household_isolation() -> None:
    store = InMemorySteeringStore()
    original = store.get("one")
    saved = store.save(original.edited("Use equations.", "Give a defined goal."), 0)
    assert saved.revision == 1
    assert json.loads(saved.steering.as_material()) == {
        "parentInstructions": "Use equations.",
        "conductInstructions": original.steering.conduct,
        "reviewInstructions": original.steering.review,
        "feedbackGuidance": "Give a defined goal.",
    }
    assert store.get("two").steering == Steering.initial()


def test_summary_cannot_overwrite_a_concurrent_parent_edit_or_reset() -> None:
    store = InMemorySteeringStore()
    original = store.get("one")
    parent = store.save(original.edited("My direction", "My correction"), 0)
    with pytest.raises(SteeringConflict):
        store.save(original.summarized("Stale summary"), 0)
    feedback = clean_feedback("event", "activity", "Title", ["too_open"], "More specific goals")
    pending = store.save(parent.receive(feedback), parent.revision)
    reset = store.save(pending.reset_adaptive("it"), pending.revision)
    assert reset.steering.instructions == "My direction"
    assert not reset.pending and not reset.history and reset.feedback_count == 0
    with pytest.raises(SteeringConflict):
        store.save(pending.summarized("Forgotten feedback"), pending.revision)


def test_feedback_accumulates_without_modifying_stable_text() -> None:
    current = InMemorySteeringStore().get("one", "en")
    first = clean_feedback("a", "activity", "Title", ["too_easy"], "Use two constraints")
    second = clean_feedback("b", "other", "Other title", ["too_open"], "Give a result to check")
    current = current.receive(first).receive(first).receive(second)
    assert len(current.pending) == 2 and current.feedback_count == 2
    summarized = current.summarized("Two constraints, with a verifiable goal.")
    assert summarized.steering.instructions == current.steering.instructions
    assert len(summarized.history) == 2 and not summarized.pending


@pytest.mark.parametrize(
    "reasons", [["unknown"], ["too_difficult", "too_easy"], ["too_closed", "too_open"]]
)
def test_invalid_feedback_is_rejected(reasons: list[str]) -> None:
    with pytest.raises(ValueError):
        clean_feedback("a", "activity", "Title", reasons, "")


def test_parent_routes_preserve_text_and_reject_stale_edits() -> None:
    from tests.test_preferences import client_for, headers

    client = client_for()
    initial = client.get("/api/steering", headers=headers()).json()
    assert initial["instructions"] and initial["adaptive"]
    answer = client.post(
        "/api/steering",
        headers=headers(),
        json={"revision": 0, "instructions": "Use two constraints.", "adaptive": "Defined goals."},
    )
    assert answer.status_code == 200
    assert answer.json()["revision"] == 1
    assert (
        client.post(
            "/api/steering", headers=headers(), json={"revision": 0, "adaptive": "Stale"}
        ).status_code
        == 409
    )
    reset = client.post(
        "/api/steering", headers=headers(), json={"revision": 1, "action": "reset_adaptive"}
    ).json()
    assert reset["instructions"] == "Use two constraints."
    assert reset["adaptive"] == initial["defaultAdaptive"]
    assert client.get("/api/steering", headers=headers()).json()["instructions"] == (
        "Use two constraints."
    )
    restored = client.post(
        "/api/steering", headers=headers(), json={"revision": 2, "action": "restore_instructions"}
    )
    assert restored.status_code == 200
    assert restored.json()["instructions"] == Steering.initial().instructions
    assert restored.json()["adaptive"] == reset["adaptive"]
    assert client.get("/api/steering").status_code in {401, 403, 503}


def test_cosmos_guidance_uses_partition_and_conditional_replace() -> None:
    from azure.core import MatchConditions
    from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceNotFoundError

    from panel.cosmos_store import CosmosSteeringStore

    class Container:
        row = None
        collide = False

        def read_item(self, *, item, partition_key):
            assert item == f"steering-{partition_key}"
            if self.row is None:
                raise CosmosResourceNotFoundError(status_code=404)
            return dict(self.row)

        def create_item(self, *, body):
            self.row = {**body, "_etag": "one"}

        def replace_item(self, *, item, body, etag, match_condition):
            assert etag == self.row["_etag"]
            assert match_condition == MatchConditions.IfNotModified
            assert item == body["id"] and body["type"] == "steering"
            if self.collide:
                raise CosmosHttpResponseError(status_code=412)
            self.row = {**body, "_etag": str(body["revision"])}

    store = CosmosSteeringStore.__new__(CosmosSteeringStore)
    container = Container()
    store._container = container
    current = store.get("family", "en")
    current = store.save(current.edited("Stable", "Adaptive"), 0)
    assert store.get("family").steering.instructions == "Stable"
    container.collide = True
    with pytest.raises(SteeringConflict):
        store.save(current.edited("Lost", "Lost"), 1)
    container.collide = False
    store.save(current.reset_adaptive("en"), 1)
    assert store.get("family").steering.adaptive == Steering.initial("en").adaptive
    assert store.get("family").steering.conduct == current.steering.conduct
    container.row.pop("conduct")
    container.row.pop("review")
    migrated = store.get("family", "en")
    assert migrated.steering.instructions == "Stable"
    assert migrated.steering.conduct == Steering.initial("en").conduct
    assert migrated.steering.review == Steering.initial("en").review
    saved = store.save(migrated.edited("Stable", "Adaptive", conduct=""), 2)
    assert store.get("family", "en").steering.conduct == ""
    assert saved.steering.review == migrated.steering.review


def test_each_prompt_can_be_edited_and_restored_without_changing_the_others() -> None:
    from tests.test_preferences import client_for, headers

    client = client_for()
    initial = client.get("/api/steering", headers=headers()).json()
    revision = 0
    for field in ("instructions", "conduct", "review"):
        result = client.post(
            "/api/steering", headers=headers(), json={"revision": revision, field: "My text"}
        )
        assert result.status_code == 200
        revision += 1
        assert result.json()[field] == "My text"
        for other in {"instructions", "conduct", "review", "adaptive"} - {field}:
            assert result.json()[other] == initial[other]
        result = client.post(
            "/api/steering", headers=headers(),
            json={"revision": revision, "action": f"restore_{field}"},
        )
        assert result.status_code == 200
        revision += 1
        assert result.json()[field] == initial[field]


def test_rejection_feedback_reaches_summary_and_preserves_parent_text(monkeypatch) -> None:
    from panel import steering_summary
    from panel.experiences import OfferedExperience
    from tests.test_preferences import client_for, headers, household_of

    client = client_for()
    household = household_of(client)
    client.app.state.experiences.offer(
        OfferedExperience(
            id="activity",
            household_id=household,
            experience={"title": "A puzzle"},
            created_at=1,
        )
    )
    observed = []

    async def fake_summary(current, language):
        observed.append(steering_summary.summary_prompt(current, language))
        return "Ask for a defined result with two constraints.", None

    monkeypatch.setattr(steering_summary, "summarize", fake_summary)
    answer = client.post(
        "/api/experiences/activity/decision",
        headers=headers(),
        json={"state": "rejected", "reasons": ["too_open"], "note": "Give a defined result."},
    )
    assert answer.status_code == 200
    assert "Give a defined result." in observed[0]
    chosen = client.get("/api/steering", headers=headers()).json()
    assert chosen["pendingCount"] == 0 and chosen["feedbackCount"] == 1
    assert chosen["adaptive"] == "Ask for a defined result with two constraints."
    assert chosen["instructions"] == chosen["defaultInstructions"]
    assert (
        client.post(
            "/api/experiences/activity/decision",
            headers=headers(),
            json={"state": "approved", "reasons": ["too_easy"]},
        ).status_code
        == 400
    )


def test_failed_summary_keeps_feedback_for_retry(monkeypatch) -> None:
    from panel import steering_summary
    from tests.test_preferences import client_for, headers, household_of

    client = client_for()
    household = household_of(client)
    store = client.app.state.steering
    initial = store.get(household)
    store.save(initial.receive(clean_feedback("a", "x", "Title", ["too_easy"], "")), 0)

    async def fail(*args):
        raise RuntimeError("model unavailable")

    monkeypatch.setattr(steering_summary, "summarize", fail)
    assert client.post("/api/steering/synthesize", headers=headers()).status_code == 200
    assert store.get(household).pending
    assert store.get(household).steering == initial.steering


def test_reset_during_synthesis_does_not_reintroduce_feedback(monkeypatch) -> None:
    from panel import steering_summary
    from tests.test_preferences import client_for, headers, household_of

    client = client_for()
    household = household_of(client)
    store = client.app.state.steering
    store.save(store.get(household).receive(clean_feedback("a", "x", "Title", [], "More clues")), 0)

    async def reset(current, language):
        store.save(current.reset_adaptive(language), current.revision)
        return "A stale summary", None

    monkeypatch.setattr(steering_summary, "summarize", reset)
    client.post("/api/steering/synthesize", headers=headers())
    assert store.get(household).steering == Steering.initial()
    assert not store.get(household).pending


def test_all_activity_agents_receive_both_parent_texts_and_ignore_legacy_pitch() -> None:
    from agents.experience_agent import the_prompt as next_prompt
    from agents.experience_continuer import the_prompt as continue_prompt
    from agents.experience_deviser import the_prompt as devise_prompt

    steering = Steering(
        "Use a verifiable question with two constraints.", "Allow algebra.",
        conduct="Offer help only when requested.", review="Explain the first incorrect step.",
    )
    prompts = [
        devise_prompt(
            language="en",
            capabilities=frozenset(),
            steering=steering,
            pitch="HIDDEN_CALIBRATION",
            counts="HIDDEN_COUNTS",
            direction="HIDDEN_DIRECTION",
        ),
        continue_prompt(
            experience={},
            after="read",
            came="marks",
            reading={},
            steering=steering,
            pitch="HIDDEN_CALIBRATION",
        ),
        next_prompt(
            script="",
            themes=[],
            plan={},
            tools=frozenset(),
            happened=[],
            minutes_left=20,
            steering=steering,
        ),
    ]
    for prompt in prompts:
        assert steering.instructions in prompt and steering.adaptive in prompt
        assert steering.conduct in prompt and steering.review in prompt
        assert "HIDDEN_" not in prompt
        assert "takes precedence" in prompt


def test_neutral_defaults_and_static_activity_prompts() -> None:
    from agents.experience_continuer import _INSTRUCTION as continuation
    from agents.experience_deviser import _INSTRUCTION as planning
    from shared.steering import MAX_GUIDANCE_CHARS, MAX_SUMMARY_CHARS, clean_text

    for language in ("it", "en"):
        value = Steering.initial(language)
        assert clean_text(value.instructions, MAX_GUIDANCE_CHARS) == value.instructions
        assert clean_text(value.adaptive, MAX_SUMMARY_CHARS) == value.adaptive
        for text in (value.instructions, value.conduct, value.review, value.adaptive):
            assert text.strip()
            assert "disabil" not in text.lower() and "diagnos" not in text.lower()
    for text in (planning, continuation):
        for removed in (
            "mostly on their own",
            "Nothing asks for speed",
            "something learnt at school",
            "never school-like",
            "one thing at a time",
            "moderate intellectual",
            "How this activity should be pitched",
            "material correspondence with several",
        ):
            assert removed not in text


def test_fixed_cores_remain_small_and_do_not_override_configurable_choices() -> None:
    from agents.experience_agent import _INSTRUCTION as runner
    from agents.experience_continuer import _INSTRUCTION as continuation
    from agents.experience_deviser import _INSTRUCTION as planning

    for text, ceiling in ((planning, 10000), (continuation, 7500), (runner, 3500)):
        assert len(text) < ceiling
        for retired in (
            "Nothing can be failed", "nothing is corrected", "no diagram",
            "Never take the option that comes to you first", "THE WORLD",
            "about 6 words", "one thing at a time",
        ):
            assert retired not in text
