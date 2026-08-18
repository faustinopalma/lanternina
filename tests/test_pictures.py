"""The picture archive: what was shown, kept, and put back.

The property that matters is that the bytes come back identical — a picture that returns
subtly altered would reach the display as a picture, not as an error, and nothing
downstream would notice.
"""

from __future__ import annotations

import base64

from fastapi.testclient import TestClient

from panel.app import create_app
from panel.config import Settings
from panel.pictures import InMemoryPictureArchive
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.store import InMemoryAccountStore

PARENT = "parent@example.test"
DEVICE_KEY = "device-key-for-tests"
# A 1-bit BMP is mostly bytes with no structure to accidentally repair, which is the point.
IMAGE = bytes(range(256)) * 4


def client_for() -> TestClient:
    settings = Settings(dev_auth=True, bootstrap_contact=PARENT, device_key=DEVICE_KEY)
    return TestClient(
        create_app(
            store=InMemoryAccountStore(),
            settings=settings,
            pictures=InMemoryPictureArchive(),
        )
    )


def headers() -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: "parent-1", DEV_CONTACT_HEADER: PARENT}


def household_of(client: TestClient) -> str:
    return str(client.get("/api/me", headers=headers()).json()["householdId"])


def archive(client: TestClient, household: str, picture_id: str = "pic_1") -> None:
    response = client.post(
        f"/api/device/{household}/pictures",
        json={
            "id": picture_id,
            "theme": "animali del bosco",
            "kind": "ok",
            "createdAt": 10.0,
            "imageBase64": base64.b64encode(IMAGE).decode(),
        },
        headers={"X-Device-Key": DEVICE_KEY},
    )
    assert response.status_code == 200, response.text


def test_a_shown_picture_comes_back_byte_for_byte() -> None:
    client = client_for()
    household = household_of(client)
    archive(client, household)

    answer = client.get(
        f"/api/device/{household}/pictures/pic_1", headers={"X-Device-Key": DEVICE_KEY}
    ).json()
    assert base64.b64decode(answer["imageBase64"]) == IMAGE
    assert answer["theme"] == "animali del bosco"


def test_the_parent_sees_the_history_and_can_open_one() -> None:
    client = client_for()
    household = household_of(client)
    archive(client, household)

    listed = client.get("/api/pictures", headers=headers()).json()["pictures"]
    assert [row["id"] for row in listed] == ["pic_1"]

    content = client.get("/api/pictures/pic_1/content", headers=headers())
    assert content.status_code == 200
    assert content.headers["content-type"] == "image/bmp"
    assert content.content == IMAGE


def test_the_newest_picture_comes_first() -> None:
    client = client_for()
    household = household_of(client)
    archive(client, household, "pic_old")
    client.post(
        f"/api/device/{household}/pictures",
        json={
            "id": "pic_new",
            "theme": "il sistema solare",
            "createdAt": 99.0,
            "imageBase64": base64.b64encode(IMAGE).decode(),
        },
        headers={"X-Device-Key": DEVICE_KEY},
    )
    listed = client.get("/api/pictures", headers=headers()).json()["pictures"]
    assert [row["id"] for row in listed] == ["pic_new", "pic_old"]


def test_another_household_history_is_not_visible() -> None:
    client = client_for()
    archive(client, "hh_someone_else")
    assert client.get("/api/pictures", headers=headers()).json()["pictures"] == []


def test_an_unknown_picture_is_a_404_not_a_crash() -> None:
    client = client_for()
    response = client.get("/api/pictures/pic_missing/content", headers=headers())
    assert response.status_code == 404


def test_the_history_is_paged_and_the_page_size_is_bounded() -> None:
    """An hourly picture makes about 740 a month, so the gallery asks for a page at a time."""
    client = client_for()
    household = household_of(client)
    for index in range(5):
        archive(client, household, f"pic_{index}")

    assert len(client.get("/api/pictures?limit=2", headers=headers()).json()["pictures"]) == 2
    # Neither a silly request nor a greedy one is honoured as asked.
    assert len(client.get("/api/pictures?limit=0", headers=headers()).json()["pictures"]) == 1
    assert len(client.get("/api/pictures?limit=9999", headers=headers()).json()["pictures"]) == 5
