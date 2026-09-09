from __future__ import annotations

import base64

from tests.test_photo_store import jpeg
from tests.test_pictures import DEVICE_KEY, client_for, headers, household_of


def upload(client, household, photo_id, when):
    return client.post(
        f"/api/device/{household}/photos",
        headers={"X-Device-Key": DEVICE_KEY},
        json={
            "id": photo_id,
            "camera": "camera",
            "receivedAt": when,
            "capturedAt": when,
            "imageBase64": base64.b64encode(jpeg()).decode(),
        },
    )


def test_parent_sees_original_and_deletion_cannot_be_undone_by_retry():
    client = client_for()
    household = household_of(client)
    photo_id = "a" * 32
    assert upload(client, household, photo_id, 100).status_code == 200
    assert client.get(f"/api/photos/{photo_id}/content", headers=headers()).content == jpeg()
    body = {"mode": "single", "id": photo_id}
    ids = client.post("/api/photos/delete-preview", headers=headers(), json=body).json()["ids"]
    assert ids == [photo_id]
    assert client.post(
        "/api/photos/delete", headers=headers(), json={**body, "ids": ids}
    ).json() == {
        "deleted": ids,
        "failed": [],
    }
    assert upload(client, household, photo_id, 100).json()["deleted"] is True
    assert client.get(f"/api/photos/{photo_id}/content", headers=headers()).status_code == 404
    assert client.get("/api/photos", headers=headers()).json()["total"] == 0


def test_range_is_half_open_and_delete_all_is_snapshot_not_future_photos():
    client = client_for()
    household = household_of(client)
    for number, when in enumerate([99, 100, 199, 200]):
        assert upload(client, household, f"{number:032x}", when).status_code == 200
    body = {"mode": "range", "start": 100, "end": 200}
    ids = client.post("/api/photos/delete-preview", headers=headers(), json=body).json()["ids"]
    assert set(ids) == {f"{number:032x}" for number in (1, 2)}
    client.post("/api/photos/delete", headers=headers(), json={**body, "ids": ids})
    all_ids = client.post(
        "/api/photos/delete-preview", headers=headers(), json={"mode": "all"}
    ).json()["ids"]
    upload(client, household, "f" * 32, 300)
    client.post("/api/photos/delete", headers=headers(), json={"mode": "all", "ids": all_ids})
    assert [row["id"] for row in client.get("/api/photos", headers=headers()).json()["photos"]] == [
        "f" * 32,
    ]


def test_invalid_dates_and_cross_household_access_do_not_delete():
    client = client_for()
    household_of(client)
    upload(client, "other", "a" * 32, 100)
    for body in (
        {"mode": "range"},
        {"mode": "range", "start": 200, "end": 100},
        {"mode": "all", "start": 1},
        {"mode": "range", "start": "", "end": 200},
    ):
        assert (
            client.post("/api/photos/delete-preview", headers=headers(), json=body).status_code
            == 422
        )
    assert client.get("/api/photos", headers=headers()).json()["photos"] == []
    assert client.get(f"/api/photos/{'a' * 32}/content", headers=headers()).status_code == 404
    assert (
        client.post(
            "/api/photos/delete",
            headers=headers(),
            json={
                "mode": "all",
                "ids": ["a" * 32],
            },
        ).json()["deleted"]
        == []
    )
    assert client.app.state.photos.get("other", "a" * 32) == jpeg()
