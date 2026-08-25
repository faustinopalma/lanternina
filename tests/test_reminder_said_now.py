"""Saying a reminder again, freshly, at the moment it goes up.

Until 25 August 2026 a sentence was worded once in its life and the display picked one of
four for ever. On the wall that read as a reminder that never changed, and — for the three
sentences in the house, whose wordings had never been generated at all — as the parent's
own typing, typo and scheduling note included: "lavarsi i identi dopo pranzo (circa alle
13:30)".

Two properties are pinned here and neither is about the words being good. The first is
that nothing about a showing is written down: this route generates, hands over and
forgets, because a row saying "this reminder was said at 13:30 today" is a record of how
often somebody was reminded of something. The second is that nothing here can stop a
reminder appearing — a refusal, an unreachable cloud and a reached limit all come back as
an empty answer, and the house shows what it already has.
"""

from __future__ import annotations

import time
from typing import Any

import pytest
from fastapi.testclient import TestClient

from panel import wording
from panel.app import create_app
from panel.config import Settings
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.reminders import InMemorySentenceStore, SentenceStore
from panel.store import InMemoryAccountStore
from panel.usage import (
    KIND_IMAGE,
    KIND_TEXT,
    InMemoryLimitStore,
    InMemoryUsageStore,
    month_of,
)
from shared.errors import CloudUnavailable, SafetyBlocked

PARENT = "parent@example.test"
DEVICE_KEY = "device-key-for-tests"


def a_client(usage: InMemoryUsageStore, store: SentenceStore, limit: int = 2000) -> TestClient:
    return TestClient(
        create_app(
            store=InMemoryAccountStore(),
            settings=Settings(
                dev_auth=True,
                bootstrap_contact=PARENT,
                device_key=DEVICE_KEY,
                monthly_limit=limit,
            ),
            usage=usage,
            limit=InMemoryLimitStore(),
            reminders=store,
        )
    )


def headers() -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: "parent-1", DEV_CONTACT_HEADER: PARENT}


def household_of(client: TestClient) -> str:
    return str(client.get("/api/me", headers=headers()).json()["householdId"])


def a_placed_sentence(store: SentenceStore, household: str) -> str:
    from panel.reminders import make_sentence

    kept = store.add(make_sentence(household, "lavarsi i denti dopo pranzo", "parent-1"))
    store.record_reading(household, kept.id, read_at=time.time(), at="13:30", days=(), question="")
    store.record_wording(household, kept.id, words=("I denti.",))
    return kept.id


def as_the_house() -> dict[str, str]:
    return {"X-Device-Key": DEVICE_KEY}


def test_the_words_come_back_and_nothing_about_the_showing_is_kept(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    usage = InMemoryUsageStore()
    store = InMemorySentenceStore()
    client = a_client(usage, store)
    household = household_of(client)
    sentence_id = a_placed_sentence(store, household)

    async def _said(text: str, at: str, *, now: float) -> tuple[str, str, Any]:
        return "Un minuto per i denti.", "toothbrush", None

    async def _drawn(subject: str, *, on_usage: Any = None) -> str:
        return "ZmFrZQ=="

    monkeypatch.setattr(wording, "say_sentence_now", _said)
    monkeypatch.setattr("panel.painting.decorate", _drawn)

    before = store.list(household)
    answer = client.post(
        f"/api/device/{household}/reminders/{sentence_id}/words", headers=as_the_house()
    )

    assert answer.status_code == 200
    said = answer.json()
    assert said["words"] == "Un minuto per i denti."
    assert said["decorationBase64"] == "ZmFrZQ=="
    # The sentence is exactly as it was: no showing, no count, no moment.
    assert store.list(household) == before


def test_both_calls_are_counted_apart(monkeypatch: pytest.MonkeyPatch) -> None:
    """A wording and a drawing cost differently, and the usage page tells them apart."""
    usage = InMemoryUsageStore()
    store = InMemorySentenceStore()
    client = a_client(usage, store)
    household = household_of(client)
    sentence_id = a_placed_sentence(store, household)

    async def _said(text: str, at: str, *, now: float) -> tuple[str, str, Any]:
        return "I denti.", "toothbrush", None

    async def _drawn(subject: str, *, on_usage: Any = None) -> str:
        return "ZmFrZQ=="

    monkeypatch.setattr(wording, "say_sentence_now", _said)
    monkeypatch.setattr("panel.painting.decorate", _drawn)

    client.post(
        f"/api/device/{household}/reminders/{sentence_id}/words", headers=as_the_house()
    )

    counted = usage.summary(household, month_of(time.time()))
    assert counted.by_kind[KIND_TEXT].calls == 1
    assert counted.by_kind[KIND_IMAGE].calls == 1


def test_a_refused_wording_still_answers_so_the_reminder_appears(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The house falls back to what it has. A 500 here would be a blank wall at 13:30."""
    usage = InMemoryUsageStore()
    store = InMemorySentenceStore()
    client = a_client(usage, store)
    household = household_of(client)
    sentence_id = a_placed_sentence(store, household)

    async def _refused(text: str, at: str, *, now: float) -> tuple[str, str, Any]:
        raise SafetyBlocked("no")

    monkeypatch.setattr(wording, "say_sentence_now", _refused)

    answer = client.post(
        f"/api/device/{household}/reminders/{sentence_id}/words", headers=as_the_house()
    )

    assert answer.status_code == 200
    assert answer.json() == {"words": "", "decorationBase64": ""}


def test_a_drawing_that_will_not_come_does_not_take_the_words_with_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    usage = InMemoryUsageStore()
    store = InMemorySentenceStore()
    client = a_client(usage, store)
    household = household_of(client)
    sentence_id = a_placed_sentence(store, household)

    async def _said(text: str, at: str, *, now: float) -> tuple[str, str, Any]:
        return "I denti.", "toothbrush", None

    async def _no_picture(subject: str, *, on_usage: Any = None) -> str:
        raise CloudUnavailable("not today")

    monkeypatch.setattr(wording, "say_sentence_now", _said)
    monkeypatch.setattr("panel.painting.decorate", _no_picture)

    said = client.post(
        f"/api/device/{household}/reminders/{sentence_id}/words", headers=as_the_house()
    ).json()

    assert said["words"] == "I denti."
    assert said["decorationBase64"] == ""


def test_a_sentence_naming_nothing_drawable_costs_no_picture(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """"none" is an answer the prompt asks for, and the cheapest one."""
    usage = InMemoryUsageStore()
    store = InMemorySentenceStore()
    client = a_client(usage, store)
    household = household_of(client)
    sentence_id = a_placed_sentence(store, household)
    drawn: list[str] = []

    async def _said(text: str, at: str, *, now: float) -> tuple[str, str, Any]:
        return "I denti.", "", None

    async def _drawn(subject: str, *, on_usage: Any = None) -> str:
        drawn.append(subject)
        return "ZmFrZQ=="

    monkeypatch.setattr(wording, "say_sentence_now", _said)
    monkeypatch.setattr("panel.painting.decorate", _drawn)

    client.post(
        f"/api/device/{household}/reminders/{sentence_id}/words", headers=as_the_house()
    )

    assert drawn == []


def test_at_the_limit_nothing_is_asked_for_and_the_house_still_hears_back() -> None:
    """The reminders route degrades rather than refusing, and so does this one."""
    usage = InMemoryUsageStore()
    store = InMemorySentenceStore()
    client = a_client(usage, store, limit=1)
    household = household_of(client)
    sentence_id = a_placed_sentence(store, household)
    from panel.usage import SERVED, UsageEvent

    usage.record(
        UsageEvent(
            id="use-1", household_id=household, at=time.time(), kind=KIND_TEXT, outcome=SERVED
        )
    )

    answer = client.post(
        f"/api/device/{household}/reminders/{sentence_id}/words", headers=as_the_house()
    )

    assert answer.status_code == 200
    assert answer.json() == {"words": "", "decorationBase64": ""}


def test_a_sentence_the_house_does_not_have_is_a_404() -> None:
    usage = InMemoryUsageStore()
    client = a_client(usage, InMemorySentenceStore())
    household = household_of(client)

    answer = client.post(
        f"/api/device/{household}/reminders/rm_nothing/words", headers=as_the_house()
    )

    assert answer.status_code == 404
