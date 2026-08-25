"""The monthly limit: where it sits, who may set it, and what the panel is told.

The properties worth pinning are the ones a quiet failure would hide. A limit that stops
the house without saying so is the fault this file exists to prevent, so the route has to
report that it was reached, not only how high it is. A limit set at or below what the month
has already spent would leave the parent pressing a button that changes nothing. And a
limit somebody chose must never be reported as the default: the whole point is that a house
running on a raised limit says so.
"""

from __future__ import annotations

import time

import pytest
from fastapi.testclient import TestClient

from panel import painting
from panel.app import create_app
from panel.config import Settings
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.reminders import InMemorySentenceStore
from panel.store import InMemoryAccountStore
from panel.themes import InMemoryThemeStore
from panel.usage import (
    KIND_IMAGE,
    MAX_MONTHLY_LIMIT,
    SERVED,
    InMemoryLimitStore,
    InMemoryUsageStore,
    Limit,
    UsageEvent,
    clean_limit,
    limit_of,
)

PARENT = "parent@example.test"
DEVICE_KEY = "device-key-for-tests"


def an_event(event_id: str, household_id: str) -> UsageEvent:
    return UsageEvent(
        id=event_id,
        household_id=household_id,
        at=time.time(),
        kind=KIND_IMAGE,
        outcome=SERVED,
    )


def a_client(
    usage: InMemoryUsageStore, limits: InMemoryLimitStore, configured: int = 2
) -> TestClient:
    return TestClient(
        create_app(
            store=InMemoryAccountStore(),
            settings=Settings(
                dev_auth=True,
                bootstrap_contact=PARENT,
                device_key=DEVICE_KEY,
                monthly_limit=configured,
            ),
            themes=InMemoryThemeStore(),
            usage=usage,
            limit=limits,
            reminders=InMemorySentenceStore(),
        )
    )


def headers() -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: "parent-1", DEV_CONTACT_HEADER: PARENT}


def household_of(client: TestClient) -> str:
    return str(client.get("/api/me", headers=headers()).json()["householdId"])


def test_an_untouched_fuse_is_the_configured_one() -> None:
    """Otherwise raising the deployment's figure would reach nobody."""
    limits = InMemoryLimitStore()

    assert limit_of(limits, "house-1", 2000) == 2000

    limits.set(Limit(household_id="house-1", calls=5000))
    assert limit_of(limits, "house-1", 2000) == 5000
    # Another household is untouched: the limit is per house, not per deployment.
    assert limit_of(limits, "house-2", 2000) == 2000


def test_the_limit_is_a_plain_number_and_may_stop_the_house(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It was refused below what the month had spent, which made the field explain itself
    instead of taking a figure. A limit is a limit: set under the month's own total it
    means the house stops now, and the page says so where it happens."""
    assert clean_limit(40) == 40

    usage = InMemoryUsageStore()
    client = a_client(usage, InMemoryLimitStore(), configured=2000)
    household = household_of(client)
    usage.record(an_event("use-1", household))
    usage.record(an_event("use-2", household))

    said = client.post("/api/usage/limit", json={"calls": 1}, headers=headers()).json()

    assert said["limit"] == 1
    assert said["reached"] is True


def test_the_panel_cannot_switch_the_limit_off() -> None:
    """Zero means "no limit at all" to over_limit. That is a deployment decision, not a click."""
    with pytest.raises(ValueError, match="between 1 and"):
        clean_limit(0)
    with pytest.raises(ValueError, match="between 1 and"):
        clean_limit(MAX_MONTHLY_LIMIT + 1)
    assert clean_limit(MAX_MONTHLY_LIMIT) == MAX_MONTHLY_LIMIT


def test_the_panel_is_told_the_fuse_went_and_not_only_how_high_it_is() -> None:
    usage = InMemoryUsageStore()
    client = a_client(usage, InMemoryLimitStore(), configured=2)
    household = household_of(client)

    quiet = client.get("/api/usage", headers=headers()).json()
    assert quiet["reached"] is False
    assert quiet["limit"] == 2

    usage.record(an_event("use-1", household))
    usage.record(an_event("use-2", household))

    gone = client.get("/api/usage", headers=headers()).json()
    assert gone["reached"] is True
    assert gone["spent"] == 2
    assert gone["maxLimit"] == MAX_MONTHLY_LIMIT


def test_a_chosen_limit_is_never_reported_as_the_configured_one() -> None:
    usage = InMemoryUsageStore()
    client = a_client(usage, InMemoryLimitStore(), configured=2)
    household = household_of(client)
    usage.record(an_event("use-1", household))
    usage.record(an_event("use-2", household))

    raised = client.post("/api/usage/limit", json={"calls": 50}, headers=headers())

    assert raised.status_code == 200
    said = raised.json()
    assert said["limit"] == 50
    assert said["reached"] is False
    # Who and when, so a house running on a moved Limit says so on its own page.
    assert said["changedAt"] > 0
    assert said["changedBy"] != ""


def test_raising_the_fuse_lets_the_refused_work_carry_on(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The point of the button. Without this the limit is a wall with a light on it."""
    usage = InMemoryUsageStore()
    client = a_client(usage, InMemoryLimitStore(), configured=1)
    household = household_of(client)
    usage.record(an_event("use-1", household))

    refused = client.post(
        f"/api/device/{household}/paint", headers={"X-Device-Key": DEVICE_KEY}
    )
    assert refused.status_code == 429

    client.post("/api/usage/limit", json={"calls": 50}, headers=headers())

    reached: list[str] = []

    async def _painted(theme: str, on_usage: object = None) -> tuple[str, str, str]:
        reached.append(theme)
        raise RuntimeError("far enough: the limit let it through")

    monkeypatch.setattr(painting, "paint", _painted)
    # The stub raises rather than faking a bitmap: reaching it is the whole assertion, and
    # what the route does with a picture is another file's business.
    with pytest.raises(RuntimeError, match="far enough"):
        client.post(f"/api/device/{household}/paint", headers={"X-Device-Key": DEVICE_KEY})

    assert reached, "the call must reach the model once the limit has been raised"


def test_a_limit_outside_what_the_panel_may_set_is_refused_with_the_reason() -> None:
    usage = InMemoryUsageStore()
    client = a_client(usage, InMemoryLimitStore(), configured=2)
    household_of(client)

    answer = client.post("/api/usage/limit", json={"calls": 0}, headers=headers())

    assert answer.status_code == 400
    assert "between 1 and" in answer.json()["detail"]
