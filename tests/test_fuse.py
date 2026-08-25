"""The fuse: where it sits, who may move it, and what the panel is told when it goes.

The properties worth pinning are the ones a quiet failure would hide. A fuse that stops
the house without saying so is the fault this file exists to prevent, so the route has to
report that it went, not only how high it is. A fuse raised to a figure already spent
would leave the parent pressing a button that changes nothing. And a fuse moved by a
parent must never be reported as the configured default: the whole point is that a house
running on a raised fuse says so.
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
    MAX_MONTHLY_CALL_CAP,
    SERVED,
    Fuse,
    InMemoryFuseStore,
    InMemoryUsageStore,
    UsageEvent,
    cap_of,
    clean_cap,
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
    usage: InMemoryUsageStore, fuses: InMemoryFuseStore, cap: int = 2
) -> TestClient:
    return TestClient(
        create_app(
            store=InMemoryAccountStore(),
            settings=Settings(
                dev_auth=True,
                bootstrap_contact=PARENT,
                device_key=DEVICE_KEY,
                monthly_call_cap=cap,
            ),
            themes=InMemoryThemeStore(),
            usage=usage,
            fuse=fuses,
            reminders=InMemorySentenceStore(),
        )
    )


def headers() -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: "parent-1", DEV_CONTACT_HEADER: PARENT}


def household_of(client: TestClient) -> str:
    return str(client.get("/api/me", headers=headers()).json()["householdId"])


def test_an_untouched_fuse_is_the_configured_one() -> None:
    """Otherwise raising the deployment's figure would reach nobody."""
    fuses = InMemoryFuseStore()

    assert cap_of(fuses, "house-1", 2000) == 2000

    fuses.set(Fuse(household_id="house-1", calls=5000))
    assert cap_of(fuses, "house-1", 2000) == 5000
    # Another household is untouched: the fuse is per house, not per deployment.
    assert cap_of(fuses, "house-2", 2000) == 2000


def test_the_fuse_cannot_be_set_below_what_is_already_spent() -> None:
    """A raise that changes nothing would look like a panel that does not work."""
    with pytest.raises(ValueError, match="already spent 40"):
        clean_cap(40, spent=40)
    assert clean_cap(41, spent=40) == 41


def test_the_panel_cannot_switch_the_fuse_off() -> None:
    """Zero means "no fuse at all" to over_cap. That is a deployment decision, not a click."""
    with pytest.raises(ValueError, match="between 1 and"):
        clean_cap(0, spent=0)
    with pytest.raises(ValueError, match="between 1 and"):
        clean_cap(MAX_MONTHLY_CALL_CAP + 1, spent=0)
    assert clean_cap(MAX_MONTHLY_CALL_CAP, spent=0) == MAX_MONTHLY_CALL_CAP


def test_the_panel_is_told_the_fuse_went_and_not_only_how_high_it_is() -> None:
    usage = InMemoryUsageStore()
    client = a_client(usage, InMemoryFuseStore(), cap=2)
    household = household_of(client)

    quiet = client.get("/api/usage", headers=headers()).json()
    assert quiet["reached"] is False
    assert quiet["cap"] == 2

    usage.record(an_event("use-1", household))
    usage.record(an_event("use-2", household))

    gone = client.get("/api/usage", headers=headers()).json()
    assert gone["reached"] is True
    assert gone["spent"] == 2
    assert gone["maxCap"] == MAX_MONTHLY_CALL_CAP


def test_a_raised_fuse_is_never_reported_as_the_configured_one() -> None:
    usage = InMemoryUsageStore()
    client = a_client(usage, InMemoryFuseStore(), cap=2)
    household = household_of(client)
    usage.record(an_event("use-1", household))
    usage.record(an_event("use-2", household))

    raised = client.post("/api/usage/fuse", json={"calls": 50}, headers=headers())

    assert raised.status_code == 200
    said = raised.json()
    assert said["cap"] == 50
    assert said["reached"] is False
    # Who and when, so a house running on a moved fuse says so on its own page.
    assert said["raisedAt"] > 0
    assert said["raisedBy"] != ""


def test_raising_the_fuse_lets_the_refused_work_carry_on(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The point of the button. Without this the fuse is a wall with a light on it."""
    usage = InMemoryUsageStore()
    client = a_client(usage, InMemoryFuseStore(), cap=1)
    household = household_of(client)
    usage.record(an_event("use-1", household))

    refused = client.post(
        f"/api/device/{household}/paint", headers={"X-Device-Key": DEVICE_KEY}
    )
    assert refused.status_code == 429

    client.post("/api/usage/fuse", json={"calls": 50}, headers=headers())

    reached: list[str] = []

    async def _painted(theme: str, on_usage: object = None) -> tuple[str, str, str]:
        reached.append(theme)
        raise RuntimeError("far enough: the fuse let it through")

    monkeypatch.setattr(painting, "paint", _painted)
    # The stub raises rather than faking a bitmap: reaching it is the whole assertion, and
    # what the route does with a picture is another file's business.
    with pytest.raises(RuntimeError, match="far enough"):
        client.post(f"/api/device/{household}/paint", headers={"X-Device-Key": DEVICE_KEY})

    assert reached, "the call must reach the model once the fuse has been raised"


def test_a_fuse_below_what_is_spent_is_refused_with_the_reason() -> None:
    usage = InMemoryUsageStore()
    client = a_client(usage, InMemoryFuseStore(), cap=2)
    household = household_of(client)
    usage.record(an_event("use-1", household))
    usage.record(an_event("use-2", household))

    answer = client.post("/api/usage/fuse", json={"calls": 2}, headers=headers())

    assert answer.status_code == 400
    assert "already spent 2" in answer.json()["detail"]
