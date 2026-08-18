"""Counting what the pictures cost.

The properties worth pinning are the ones that would be silently wrong otherwise: a call
the safety gate refused was still paid for and must still be counted, an event replayed
must not count twice, and the figures the backend reports about caching and reasoning must
survive into the record rather than being flattened into "one picture".
"""

from __future__ import annotations

import time

import pytest
from fastapi.testclient import TestClient

from panel import painting
from panel.app import create_app
from panel.config import Settings
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.store import InMemoryAccountStore
from panel.themes import InMemoryThemeStore
from panel.usage import (
    FAILED,
    KIND_IMAGE,
    REFUSED,
    SERVED,
    InMemoryUsageStore,
    UsageEvent,
    event_from,
    month_of,
    over_cap,
)
from shared.errors import SafetyBlocked
from shared.routing import ModelUsage

PARENT = "parent@example.test"
DEVICE_KEY = "device-key-for-tests"

REPORTED = ModelUsage(
    deployment="gpt-image-2-2026-04-21",
    request_id="6d158052-14c2-446f-bb5c-011b8d7f3ee1",
    input_tokens=12,
    output_tokens=196,
    cached_input_tokens=2816,
    reasoning_tokens=66,
    size="1024x1024",
    quality="low",
)


def an_event(event_id: str, **overrides: object) -> UsageEvent:
    fields: dict[str, object] = {
        "id": event_id,
        "household_id": "house-1",
        "at": time.time(),
        "kind": KIND_IMAGE,
        "outcome": SERVED,
        "output_tokens": 196,
    }
    fields.update(overrides)
    return UsageEvent(**fields)  # type: ignore[arg-type]


def test_the_same_event_recorded_twice_counts_once() -> None:
    store = InMemoryUsageStore()
    store.record(an_event("use-1"))
    store.record(an_event("use-1"))

    summary = store.summary("house-1", month_of(time.time()))
    assert summary.calls == 1
    assert summary.output_tokens == 196


def test_a_failed_call_is_visible_but_not_billed() -> None:
    store = InMemoryUsageStore()
    store.record(an_event("use-1"))
    store.record(an_event("use-2", outcome=FAILED, output_tokens=0))

    summary = store.summary("house-1", month_of(time.time()))
    assert summary.calls == 2
    assert summary.billed_calls == 1


def test_a_refused_call_is_billed_because_the_model_ran() -> None:
    store = InMemoryUsageStore()
    store.record(an_event("use-1", outcome=REFUSED))

    assert store.summary("house-1", month_of(time.time())).billed_calls == 1


def test_what_the_backend_reported_survives_into_the_event() -> None:
    event = event_from("house-1", KIND_IMAGE, SERVED, REPORTED, event_id="use-1")

    assert event.request_id == REPORTED.request_id
    assert event.cached_input_tokens == 2816
    assert event.reasoning_tokens == 66
    assert event.quality == "low"


def test_an_absent_report_gives_an_event_of_zeroes_not_a_guess() -> None:
    event = event_from("house-1", KIND_IMAGE, FAILED, None, event_id="use-1")

    assert event.input_tokens == 0
    assert event.output_tokens == 0
    assert event.deployment == ""


def test_a_cap_of_zero_never_stops_anything() -> None:
    store = InMemoryUsageStore()
    for index in range(5):
        store.record(an_event(f"use-{index}"))

    assert over_cap(store, "house-1", 0) is False
    assert over_cap(store, "house-1", 5) is True
    assert over_cap(store, "house-1", 6) is False


def test_the_count_is_per_household() -> None:
    store = InMemoryUsageStore()
    store.record(an_event("use-1"))
    store.record(an_event("use-2", household_id="house-2"))

    assert store.summary("house-1", month_of(time.time())).calls == 1
    assert store.summary("house-2", month_of(time.time())).calls == 1


def client_for(store: InMemoryUsageStore, cap: int = 1000) -> TestClient:
    settings = Settings(
        dev_auth=True,
        bootstrap_contact=PARENT,
        device_key=DEVICE_KEY,
        monthly_picture_cap=cap,
    )
    return TestClient(
        create_app(
            store=InMemoryAccountStore(),
            settings=settings,
            themes=InMemoryThemeStore(),
            usage=store,
        )
    )


def headers() -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: "parent-1", DEV_CONTACT_HEADER: PARENT}


def household_of(client: TestClient) -> str:
    return str(client.get("/api/me", headers=headers()).json()["householdId"])


def test_the_cap_refuses_before_the_model_is_called(monkeypatch: pytest.MonkeyPatch) -> None:
    store = InMemoryUsageStore()
    client = client_for(store, cap=1)
    household = household_of(client)
    store.record(an_event("use-1", household_id=household))

    def _must_not_run(*args: object, **kwargs: object) -> None:
        raise AssertionError("the cap must be checked before anything is generated")

    monkeypatch.setattr(painting, "paint", _must_not_run)

    answer = client.post(
        f"/api/device/{household}/paint", headers={"X-Device-Key": DEVICE_KEY}
    )
    assert answer.status_code == 429


def test_a_refused_picture_is_still_counted(monkeypatch: pytest.MonkeyPatch) -> None:
    store = InMemoryUsageStore()
    client = client_for(store)
    household = household_of(client)

    async def _refuses(theme: str, size: str = "", *, on_usage: object = None) -> None:
        if on_usage is not None:
            on_usage(REPORTED)  # type: ignore[operator]
        raise SafetyBlocked("the gate said no")

    monkeypatch.setattr(painting, "paint", _refuses)

    answer = client.post(
        f"/api/device/{household}/paint", headers={"X-Device-Key": DEVICE_KEY}
    )
    assert answer.status_code == 409

    summary = store.summary(household, month_of(time.time()))
    assert summary.billed_calls == 1
    assert summary.output_tokens == 196


def test_the_parent_can_read_the_month(monkeypatch: pytest.MonkeyPatch) -> None:
    store = InMemoryUsageStore()
    client = client_for(store, cap=42)
    household = household_of(client)
    store.record(an_event("use-1", household_id=household))

    body = client.get("/api/usage", headers=headers()).json()
    assert body["cap"] == 42
    assert body["usage"]["calls"] == 1
    assert body["usage"]["outputTokens"] == 196
    # Nothing here may look like a target to reach.
    assert "goal" not in body and "streak" not in body
