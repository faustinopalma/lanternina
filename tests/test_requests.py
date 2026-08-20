"""The one channel from the panel into the house.

The claims worth holding down are the ones the rule is made of, and each of them fails on
an implementation that looks right: the press persists a row and calls nothing, the house
gets what was asked for only when it asks, the second press replaces the first rather than
queueing behind it, and clearing is by id so a press that lands while the house is busy
with the previous one survives.

The last one is expiry. A request nobody collected stops being offered after a day, which
is the widest spacing a parent may set between pictures, so it is the longest a request
can legitimately be waiting.
"""

from __future__ import annotations

import base64
import time
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from devices import pull_picture
from panel.app import create_app
from panel.config import Settings
from panel.pictures import InMemoryPictureArchive, PictureRecord
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.requests import (
    KIND_SHOW_AGAIN,
    REQUEST_LIFETIME_SECONDS,
    HouseRequest,
    InMemoryRequestStore,
    clean_request,
)
from panel.rhythm import MAX_CADENCE_MINUTES
from panel.store import InMemoryAccountStore

PARENT = "parent@example.test"
DEVICE_KEY = "device-key-for-tests"
IMAGE = b"a rendered bitmap"


def client_for(
    archive: InMemoryPictureArchive, store: InMemoryRequestStore
) -> TestClient:
    settings = Settings(dev_auth=True, bootstrap_contact=PARENT, device_key=DEVICE_KEY)
    return TestClient(
        create_app(
            store=InMemoryAccountStore(),
            settings=settings,
            pictures=archive,
            requests=store,
        )
    )


def headers() -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: "parent-1", DEV_CONTACT_HEADER: PARENT}


def household_of(client: TestClient) -> str:
    return str(client.get("/api/me", headers=headers()).json()["householdId"])


def archived(archive: InMemoryPictureArchive, household: str, picture_id: str) -> None:
    archive.save(
        PictureRecord(
            id=picture_id,
            household_id=household,
            theme="the sea",
            created_at=time.time(),
        ),
        IMAGE,
    )


def test_the_lifetime_is_the_widest_spacing_a_parent_may_set() -> None:
    """Not a round number chosen for looking tidy: past a day the hub was off, and a
    picture asked for yesterday is not what somebody wants appearing tomorrow."""
    assert REQUEST_LIFETIME_SECONDS == MAX_CADENCE_MINUTES * 60


def test_the_press_persists_a_row_and_reaches_into_nothing() -> None:
    archive = InMemoryPictureArchive()
    store = InMemoryRequestStore()
    client = client_for(archive, store)
    household = household_of(client)
    archived(archive, household, "pic-1")

    answer = client.post("/api/pictures/pic-1/again", headers=headers())

    assert answer.status_code == 200
    assert answer.json()["kind"] == KIND_SHOW_AGAIN
    assert answer.json()["subject"] == "pic-1"
    standing = store.get(household)
    assert standing is not None and standing.subject == "pic-1"


def test_a_picture_the_household_does_not_have_is_refused() -> None:
    archive = InMemoryPictureArchive()
    store = InMemoryRequestStore()
    client = client_for(archive, store)
    household = household_of(client)

    answer = client.post("/api/pictures/pic-missing/again", headers=headers())

    assert answer.status_code == 404
    assert store.get(household) is None


def test_the_second_press_replaces_the_first() -> None:
    archive = InMemoryPictureArchive()
    store = InMemoryRequestStore()
    client = client_for(archive, store)
    household = household_of(client)
    archived(archive, household, "pic-1")
    archived(archive, household, "pic-2")

    client.post("/api/pictures/pic-1/again", headers=headers())
    client.post("/api/pictures/pic-2/again", headers=headers())

    standing = store.get(household)
    assert standing is not None and standing.subject == "pic-2"


def test_the_house_reads_it_and_clears_it() -> None:
    archive = InMemoryPictureArchive()
    store = InMemoryRequestStore()
    client = client_for(archive, store)
    household = household_of(client)
    archived(archive, household, "pic-1")
    client.post("/api/pictures/pic-1/again", headers=headers())

    asked = client.get(
        f"/api/device/{household}/request", headers={"X-Device-Key": DEVICE_KEY}
    ).json()["request"]
    assert asked["subject"] == "pic-1"

    cleared = client.post(
        f"/api/device/{household}/request/{asked['id']}/done",
        headers={"X-Device-Key": DEVICE_KEY},
    )
    assert cleared.json()["cleared"] is True
    assert (
        client.get(
            f"/api/device/{household}/request", headers={"X-Device-Key": DEVICE_KEY}
        ).json()["request"]
        is None
    )


def test_a_press_that_lands_while_the_house_is_busy_survives() -> None:
    """The house asked, then the parent pressed again, then the house said "done" about
    the first. Clearing by id is what keeps the second press."""
    store = InMemoryRequestStore()
    first = clean_request("h1", kind=KIND_SHOW_AGAIN, subject="pic-1")
    store.put(first)
    second = clean_request("h1", kind=KIND_SHOW_AGAIN, subject="pic-2")
    store.put(second)

    assert store.clear("h1", first.id) is False
    standing = store.get("h1")
    assert standing is not None and standing.subject == "pic-2"


def test_a_request_nobody_collected_stops_being_offered() -> None:
    store = InMemoryRequestStore()
    now = time.time()
    store.put(
        HouseRequest(
            id="ask-1",
            household_id="h1",
            kind=KIND_SHOW_AGAIN,
            subject="pic-1",
            asked_at=now - REQUEST_LIFETIME_SECONDS - 1,
        )
    )

    assert store.get("h1") is None


def test_the_device_key_is_needed_to_collect() -> None:
    archive = InMemoryPictureArchive()
    store = InMemoryRequestStore()
    client = client_for(archive, store)
    household = household_of(client)

    assert (
        client.get(f"/api/device/{household}/request", headers={"X-Device-Key": "wrong"})
    ).status_code == 403


def test_a_kind_the_panel_does_not_know_is_refused() -> None:
    with pytest.raises(ValueError):
        clean_request("h1", kind="paintSomething", subject="pic-1")


def test_the_hub_puts_the_picture_back_instead_of_painting(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The point of the whole channel, on the side that acts: the house was about to
    spend a generation and serves the parent's choice instead."""
    target = tmp_path / "screen.bmp"
    cleared: list[str] = []
    monkeypatch.setattr(pull_picture, "install", lambda path, image: path.write_bytes(image))
    monkeypatch.setattr(
        pull_picture, "archived_picture", lambda *args: b"the archived bitmap"
    )
    monkeypatch.setattr(
        pull_picture,
        "request_done",
        lambda panel, household, key, request_id: cleared.append(request_id),
    )

    asked: dict[str, Any] = {"id": "ask-1", "kind": KIND_SHOW_AGAIN, "subject": "pic-1"}
    served = pull_picture.serve_request("https://panel.invalid", "h1", "k", target, asked)

    assert served is True
    assert target.read_bytes() == b"the archived bitmap"
    assert cleared == ["ask-1"]


def test_a_picture_the_archive_no_longer_has_clears_the_request(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Otherwise every later run tries the same missing picture and never paints."""
    cleared: list[str] = []
    monkeypatch.setattr(pull_picture, "archived_picture", lambda *args: None)
    monkeypatch.setattr(
        pull_picture,
        "request_done",
        lambda panel, household, key, request_id: cleared.append(request_id),
    )

    asked: dict[str, Any] = {"id": "ask-1", "kind": KIND_SHOW_AGAIN, "subject": "gone"}
    served = pull_picture.serve_request(
        "https://panel.invalid", "h1", "k", tmp_path / "screen.bmp", asked
    )

    assert served is False
    assert cleared == ["ask-1"]


def test_a_kind_the_hub_does_not_know_leaves_it_to_paint(tmp_path: Path) -> None:
    """A kind added to the panel does not have to reach the hub on the same day."""
    asked: dict[str, Any] = {"id": "ask-1", "kind": "somethingLater", "subject": "x"}
    assert (
        pull_picture.serve_request(
            "https://panel.invalid", "h1", "k", tmp_path / "screen.bmp", asked
        )
        is False
    )


def test_the_hub_reads_the_archived_picture_off_the_panel() -> None:
    """The bytes the hub installs are the ones the archive holds, unchanged."""
    archive = InMemoryPictureArchive()
    store = InMemoryRequestStore()
    client = client_for(archive, store)
    household = household_of(client)
    archived(archive, household, "pic-1")

    answer = client.get(
        f"/api/device/{household}/pictures/pic-1", headers={"X-Device-Key": DEVICE_KEY}
    )

    assert base64.b64decode(answer.json()["imageBase64"]) == IMAGE
