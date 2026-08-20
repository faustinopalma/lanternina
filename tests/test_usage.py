"""Counting what the model calls cost.

The properties worth pinning are the ones that would be silently wrong otherwise: a call
the safety gate refused was still paid for and must still be counted, an event replayed
must not count twice, the figures the backend reports about caching and reasoning must
survive into the record rather than being flattened into "one picture", and a picture, a
wording and a reading must be readable apart rather than summed into a figure whose name
fits only one of them.

The other half is the cap. Every path that writes an event also has to read the cap before
it spends: a path that counts without checking can only be stopped by a different path
happening to run first, which is not a thing that can be relied on.
"""

from __future__ import annotations

import base64
import time
from typing import Any

import pytest
from fastapi.testclient import TestClient

from panel import painting
from panel.app import create_app
from panel.config import Settings
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.reminders import InMemorySentenceStore
from panel.rhythm import DEFAULT_CADENCE_MINUTES
from panel.store import InMemoryAccountStore
from panel.themes import InMemoryThemeStore
from panel.usage import (
    DEFAULT_MONTHLY_CALL_CAP,
    FAILED,
    KIND_IMAGE,
    KIND_READ,
    KIND_TEXT,
    REFUSED,
    SERVED,
    InMemoryUsageStore,
    UsageEvent,
    event_from,
    month_of,
    over_cap,
)
from shared.errors import CloudUnavailable, SafetyBlocked
from shared.ids import CellId, ExerciseId, SheetId
from shared.routing import ModelUsage
from shared.sheet import CellKind, CellSpec, Rect, SheetSpec
from shared.vision_contracts import PageReading

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
    assert summary.total.calls == 1
    assert summary.total.output_tokens == 196


def test_a_failed_call_is_visible_but_not_billed() -> None:
    store = InMemoryUsageStore()
    store.record(an_event("use-1"))
    store.record(an_event("use-2", outcome=FAILED, output_tokens=0))

    summary = store.summary("house-1", month_of(time.time()))
    assert summary.total.calls == 2
    assert summary.total.billed_calls == 1


def test_a_refused_call_is_billed_because_the_model_ran() -> None:
    store = InMemoryUsageStore()
    store.record(an_event("use-1", outcome=REFUSED))

    assert store.summary("house-1", month_of(time.time())).total.billed_calls == 1


def test_a_picture_and_a_wording_are_counted_apart_as_well_as_together() -> None:
    store = InMemoryUsageStore()
    store.record(an_event("use-1"))
    store.record(an_event("use-2", kind=KIND_TEXT, output_tokens=31))

    summary = store.summary("house-1", month_of(time.time()))
    assert summary.total.calls == 2
    assert summary.by_kind[KIND_IMAGE].calls == 1
    assert summary.by_kind[KIND_IMAGE].output_tokens == 196
    assert summary.by_kind[KIND_TEXT].calls == 1
    assert summary.by_kind[KIND_TEXT].output_tokens == 31


def test_a_kind_nobody_used_is_reported_as_zero_not_left_out() -> None:
    # A missing key would read as "no such thing" on a page that has to say which kind
    # each figure belongs to.
    summary = InMemoryUsageStore().summary("house-1", month_of(time.time()))

    assert summary.by_kind[KIND_IMAGE].calls == 0
    assert summary.by_kind[KIND_TEXT].calls == 0
    assert summary.by_kind[KIND_READ].calls == 0


def test_a_reading_is_its_own_kind_and_not_a_wording() -> None:
    """A reading produces no words anybody sees. Folding it into the written words would
    give back a figure whose name says less than it holds."""
    store = InMemoryUsageStore()
    store.record(an_event("use-1", kind=KIND_READ, output_tokens=140))
    store.record(an_event("use-2", kind=KIND_TEXT, output_tokens=31))

    summary = store.summary("house-1", month_of(time.time()))
    assert summary.by_kind[KIND_READ].output_tokens == 140
    assert summary.by_kind[KIND_TEXT].output_tokens == 31
    assert summary.total.output_tokens == 171


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


def test_the_cap_counts_a_wording_as_well_as_a_picture() -> None:
    store = InMemoryUsageStore()
    store.record(an_event("use-1"))
    store.record(an_event("use-2", kind=KIND_TEXT))

    assert over_cap(store, "house-1", 2) is True


def test_the_cap_leaves_room_for_a_month_of_ordinary_use() -> None:
    """The cap stops a fault; it does not decide how much a working house may do.

    Three paths pay, so the month is added up over all three: a picture at the spacing the
    parent gets by default with the night pause switched off, ten pages on the glass a
    day, and one new reminder a day, which is read once and worded once in its life. The
    figure this pins is the same one written above the constant.
    """
    days = 31
    pictures = days * (24 * 60 // DEFAULT_CADENCE_MINUTES)
    readings = days * 10
    reminders = days * 2
    ordinary = pictures + readings + reminders

    assert (pictures, readings, reminders, ordinary) == (744, 310, 62, 1116)
    assert DEFAULT_MONTHLY_CALL_CAP > ordinary


def test_the_count_is_per_household() -> None:
    store = InMemoryUsageStore()
    store.record(an_event("use-1"))
    store.record(an_event("use-2", household_id="house-2"))

    assert store.summary("house-1", month_of(time.time())).total.calls == 1
    assert store.summary("house-2", month_of(time.time())).total.calls == 1


def client_for(store: InMemoryUsageStore, cap: int = 1000) -> TestClient:
    settings = Settings(
        dev_auth=True,
        bootstrap_contact=PARENT,
        device_key=DEVICE_KEY,
        monthly_call_cap=cap,
    )
    return TestClient(
        create_app(
            store=InMemoryAccountStore(),
            settings=settings,
            themes=InMemoryThemeStore(),
            usage=store,
            reminders=InMemorySentenceStore(),
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
    assert summary.total.billed_calls == 1
    assert summary.total.output_tokens == 196


def test_the_parent_can_read_the_month(monkeypatch: pytest.MonkeyPatch) -> None:
    store = InMemoryUsageStore()
    client = client_for(store, cap=42)
    household = household_of(client)
    store.record(an_event("use-1", household_id=household))
    store.record(an_event("use-2", household_id=household, kind=KIND_TEXT, output_tokens=31))
    store.record(an_event("use-3", household_id=household, kind=KIND_READ, output_tokens=140))

    body = client.get("/api/usage", headers=headers()).json()
    assert body["cap"] == 42
    assert body["usage"]["total"]["calls"] == 3
    assert body["usage"]["total"]["outputTokens"] == 367
    # Every figure the parent reads arrives under the kind it belongs to.
    assert body["usage"]["byKind"][KIND_IMAGE]["outputTokens"] == 196
    assert body["usage"]["byKind"][KIND_TEXT]["outputTokens"] == 31
    assert body["usage"]["byKind"][KIND_READ]["outputTokens"] == 140
    # Nothing here may look like a target to reach.
    assert "goal" not in body and "streak" not in body


# ── Reading a page ───────────────────────────────────────────────────────────────────

READING_REPORTED = ModelUsage(
    deployment="gpt-5.6-sol-2026-07-09",
    request_id="0dc0e4c3-0d38-4d1f-9dfe-4a6f1e2a5b90",
    input_tokens=1180,
    output_tokens=220,
    reasoning_tokens=64,
)


def a_spec() -> SheetSpec:
    return SheetSpec(
        sheet_id=SheetId("sh_test"),
        exercise_id=ExerciseId("ex_test"),
        title="Una casella",
        cells=(
            CellSpec(
                id=CellId("q1c1"),
                kind=CellKind.CHOICE_BOX,
                rect=Rect(0.1, 0.5, 0.2, 0.05),
                label="sole",
                group="q1",
            ),
        ),
        qr_rect=Rect(0.78, 0.025, 0.18, 0.118),
    )


def a_page_body() -> dict[str, Any]:
    return {
        "imageBase64": base64.b64encode(b"\x89PNG\r\n\x1a\n").decode(),
        "width": 1240,
        "height": 1754,
        "sheet": a_spec().to_dict(),
    }


def send_page(client: TestClient, household: str) -> Any:
    return client.post(
        f"/api/device/{household}/read-sheet",
        json=a_page_body(),
        headers={"X-Device-Key": DEVICE_KEY},
    )


def a_reading() -> PageReading:
    return PageReading(
        sheet_id=SheetId("sh_test"),
        exercise_id=ExerciseId("ex_test"),
        cells=(),
        read_at=1.0,
    )


def test_reading_a_page_is_counted(monkeypatch: pytest.MonkeyPatch) -> None:
    """The reading path spends the same money as the picture path and used to leave no
    trace of it, so the cap could not see it and the parent could not either."""
    store = InMemoryUsageStore()
    client = client_for(store)
    household = household_of(client)

    async def _reads(page: Any, spec: Any, *, now: float) -> Any:
        return a_reading(), READING_REPORTED

    monkeypatch.setattr("panel.reading.read_sheet", _reads)
    assert send_page(client, household).status_code == 200

    summary = store.summary(household, month_of(time.time()))
    assert summary.by_kind[KIND_READ].calls == 1
    assert summary.by_kind[KIND_READ].input_tokens == 1180
    assert summary.by_kind[KIND_READ].reasoning_tokens == 64
    # It is a reading, so nothing of it lands under the words somebody reads.
    assert summary.by_kind[KIND_TEXT].calls == 0


def test_a_reading_the_cloud_refused_is_counted_and_not_billed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = InMemoryUsageStore()
    client = client_for(store)
    household = household_of(client)

    async def _fails(page: Any, spec: Any, *, now: float) -> Any:
        raise CloudUnavailable("no route to Foundry")

    monkeypatch.setattr("panel.reading.read_sheet", _fails)
    assert send_page(client, household).status_code == 503

    summary = store.summary(household, month_of(time.time()))
    assert summary.by_kind[KIND_READ].calls == 1
    assert summary.by_kind[KIND_READ].billed_calls == 0


def test_the_cap_refuses_a_reading_before_the_model_is_called(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The house falls back on its own arithmetic and marks the reading degraded, which
    is what it already does when the panel cannot be reached at all."""
    store = InMemoryUsageStore()
    client = client_for(store, cap=1)
    household = household_of(client)
    store.record(an_event("use-1", household_id=household))

    async def _must_not_run(page: Any, spec: Any, *, now: float) -> Any:
        raise AssertionError("the cap must be checked before the page is read")

    monkeypatch.setattr("panel.reading.read_sheet", _must_not_run)
    assert send_page(client, household).status_code == 429


# ── Reading the parent's sentences ───────────────────────────────────────────────────


def ask_for_reminders(client: TestClient, household: str) -> Any:
    return client.post(
        f"/api/device/{household}/reminders", headers={"X-Device-Key": DEVICE_KEY}
    )


def add_reminder(client: TestClient, text: str) -> str:
    written = client.post("/api/reminders", json={"text": text}, headers=headers())
    assert written.status_code == 200
    return str(written.json()["id"])


def placing(said: dict[str, tuple[Any, Any, Any]], reported: ModelUsage | None) -> Any:
    async def read(sentences: Any, *, now: float) -> Any:
        nothing = (None, None, None)
        return {one: said.get(one, nothing) for one, _ in sentences}, reported

    return read


def test_reading_the_parents_sentences_is_counted(monkeypatch: pytest.MonkeyPatch) -> None:
    store = InMemoryUsageStore()
    client = client_for(store)
    household = household_of(client)
    written = add_reminder(client, "lavarsi i denti alle 21:00")

    monkeypatch.setattr(
        "panel.reading.read_sentences", placing({written: ("21:00", [], "")}, READING_REPORTED)
    )

    async def _no_words(text: str, at: str, *, now: float) -> Any:
        return (), None

    monkeypatch.setattr("panel.wording.word_sentence", _no_words)
    assert ask_for_reminders(client, household).status_code == 200

    summary = store.summary(household, month_of(time.time()))
    assert summary.by_kind[KIND_READ].calls == 1
    assert summary.by_kind[KIND_READ].input_tokens == 1180


def test_the_cap_stops_the_reading_without_stopping_the_house(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reduced capability, not a stopped house: the reminders already placed still come
    back, and the hub is told its answer is short. A 429 would take those with it."""
    store = InMemoryUsageStore()
    client = client_for(store, cap=2)
    household = household_of(client)
    old = add_reminder(client, "mercoledì porta fuori il bidone")

    async def _no_words(text: str, at: str, *, now: float) -> Any:
        return (), None

    monkeypatch.setattr("panel.wording.word_sentence", _no_words)
    monkeypatch.setattr(
        "panel.reading.read_sentences", placing({old: ("18:30", ["wed"], "")}, None)
    )
    first = ask_for_reminders(client, household).json()
    assert first["degraded"] is False

    new = add_reminder(client, "annaffiare le piante alle 19:00")

    async def _must_not_run(sentences: Any, *, now: float) -> Any:
        raise AssertionError("the cap must be checked before the sentences are read")

    monkeypatch.setattr("panel.reading.read_sentences", _must_not_run)
    answer = ask_for_reminders(client, household).json()
    assert answer["degraded"] is True
    assert [row["id"] for row in answer["reminders"]] == [old]
    # And the sentence is still unread, so it will be read when there is room again.
    listed = client.get("/api/reminders", headers=headers()).json()["reminders"]
    assert {row["id"]: row["read"] for row in listed} == {old: True, new: False}


def test_the_cap_stops_a_wording(monkeypatch: pytest.MonkeyPatch) -> None:
    """The reading of a batch is one call and the wording is one per sentence in it, so
    the cap can be passed in the middle of a batch. It is checked here too."""
    store = InMemoryUsageStore()
    client = client_for(store, cap=1)
    household = household_of(client)
    written = add_reminder(client, "lavarsi i denti alle 21:00")

    monkeypatch.setattr(
        "panel.reading.read_sentences", placing({written: ("21:00", [], "")}, None)
    )

    async def _must_not_run(text: str, at: str, *, now: float) -> Any:
        raise AssertionError("the cap must be checked before a wording is asked for")

    monkeypatch.setattr("panel.wording.word_sentence", _must_not_run)
    answer = ask_for_reminders(client, household).json()

    # The reading was paid for and passed the cap; the reminder still arrives, in the
    # parent's own words.
    assert answer["reminders"][0]["words"] == []
    assert store.summary(household, month_of(time.time())).total.calls == 1
