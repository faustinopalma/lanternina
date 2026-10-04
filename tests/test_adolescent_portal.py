"""The adolescent portal never grants parent permissions."""

from __future__ import annotations

import io
import json
import time

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from panel.app import create_app
from panel.config import Settings
from tests.device_auth import bind_household


def portal():
    app = create_app(settings=Settings(
        dev_auth=True, bootstrap_contact="parent@example.test",
        device_key="test-device-key",
    ))
    client = TestClient(app)
    parent = {"x-dev-subject": "parent", "x-dev-contact": "parent@example.test"}
    teen = {"x-dev-subject": "teen", "x-dev-contact": "teen@example.test"}
    assert client.get("/api/me", headers=parent).status_code == 200
    bind_household(client, client.get("/api/me", headers=parent).json()["householdId"])
    return app, client, parent, teen


def invitation(app, client, parent):
    response = client.post("/api/adolescents/invitations", headers=parent,
                           json={"email": "teen@example.test"})
    assert response.status_code == 201
    assert response.json()["status"] == "ready"
    return response.json()["code"]


def test_session_routes_roles_without_registering_or_granting_access() -> None:
    app, client, parent, teen = portal()
    assert client.get("/api/session").status_code == client.get("/api/portal/me").status_code == 503
    response = client.get("/api/session", headers=parent)
    assert response.json() == {"destination": "parent"}
    assert response.headers["cache-control"] == "no-store"
    assert client.get("/api/session", headers=teen).json() == {"destination": "new"}
    assert app.state.store.by_subject("teen") is None
    token = invitation(app, client, parent)
    assert client.get("/api/session", headers=teen).json() == {"destination": "adolescent"}
    assert client.get("/api/portal/me", headers=teen).status_code == 403
    client.post("/api/portal/accept", headers=teen, json={"token": token})
    member = client.get("/api/adolescents", headers=parent).json()["members"][0]
    client.delete(f"/api/adolescents/{member['id']}", headers=parent)
    assert client.get("/api/session", headers=teen).json() == {"destination": "adolescent"}
    assert client.get("/api/me", headers=teen).status_code == 403
    assert app.state.store.by_subject("teen") is None


def test_invitation_registration_and_revocation() -> None:
    app, client, parent, teen = portal()
    token = invitation(app, client, parent)
    assert token not in str(app.state.portal.read())
    assert token not in client.get("/api/adolescents", headers=parent).text
    assert client.get("/api/portal/me", headers=teen).status_code == 403
    assert client.post("/api/portal/accept", headers=teen, json={"token": token}).status_code == 200
    assert client.get("/api/portal/me", headers=teen).status_code == 200
    assert client.get("/api/photos", headers=teen).status_code == 403
    assert client.get("/api/adolescents", headers=teen).status_code == 403
    member = client.get("/api/adolescents", headers=parent).json()["members"][0]
    assert client.delete(f"/api/adolescents/{member['id']}", headers=parent).status_code == 200
    assert client.get("/api/portal/me", headers=teen).status_code == 403
    assert client.post("/api/portal/accept", headers=teen, json={"token": token}).status_code == 410


def test_invitation_requires_matching_account_and_expires() -> None:
    app, client, parent, teen = portal()
    token = invitation(app, client, parent)
    wrong = {**teen, "x-dev-contact": "another@example.test"}
    response = client.post("/api/portal/accept", headers=wrong, json={"token": token})
    assert response.status_code == 403
    app.state.portal.change(lambda data: next(iter(data["invitations"].values())).update(
        expiresAt=0,
    ))
    assert client.post("/api/portal/accept", headers=teen, json={"token": token}).status_code == 410


def test_revoked_invitation_can_be_permanently_deleted() -> None:
    app, client, parent, teen = portal()
    token = invitation(app, client, parent)
    record = client.get("/api/adolescents", headers=parent).json()["invitations"][0]
    path = f"/api/adolescents/{record['id']}"
    assert client.delete(path + "/permanent", headers=parent).status_code == 409
    assert client.delete(path, headers=parent).status_code == 200
    assert client.delete(path + "/permanent", headers=parent).status_code == 200
    assert client.get("/api/adolescents", headers=parent).json() == {
        "members": [], "invitations": [],
    }
    assert app.state.portal.read()["invitations"] == {}
    assert client.post("/api/portal/accept", headers=teen, json={"token": token}).status_code == 410


def test_removed_member_stays_revoked_after_restart(portal_blob_container) -> None:
    from panel.adolescents import BlobPortalStore
    from shared.accounts import AccountStatus

    app, client, parent, teen = portal()
    app.state.portal = BlobPortalStore(portal_blob_container)
    token = invitation(app, client, parent)
    assert client.post("/api/portal/accept", headers=teen, json={"token": token}).status_code == 200
    member = client.get("/api/adolescents", headers=parent).json()["members"][0]
    path = f"/api/adolescents/{member['id']}"
    other = app.state.store.register(subject="other-parent", contact="other@example.test")
    app.state.store.decide(other.id, AccountStatus.ACTIVE, decided_by="test")
    other_headers = {"x-dev-subject": "other-parent", "x-dev-contact": "other@example.test"}
    other_code = invitation(app, client, other_headers)
    other_before = client.get("/api/adolescents", headers=other_headers).json()
    assert client.delete(path + "/permanent", headers=parent).status_code == 409
    assert client.delete(path + "/permanent", headers=teen).status_code == 403
    assert client.delete(path + "/permanent").status_code == 503
    assert client.delete(path + "/permanent", headers=other_headers).status_code == 404
    assert client.delete(path, headers=parent).status_code == 200
    new_token = invitation(app, client, parent)
    assert client.delete(path + "/permanent", headers=parent).json() == {"deleted": True}
    app.state.portal = BlobPortalStore(portal_blob_container)
    assert client.get("/api/adolescents", headers=parent).json() == {
        "members": [], "invitations": [],
    }
    assert client.get("/api/adolescents", headers=other_headers).json() == other_before
    assert app.state.portal.read()["members"] == {}
    assert app.state.portal.known_subject("teen")
    assert client.get("/api/portal/me", headers=teen).status_code == 403
    assert client.get("/api/me", headers=teen).status_code == 403
    assert client.get("/api/session", headers=teen).json() == {"destination": "adolescent"}
    assert app.state.store.by_subject("teen") is None
    for old_token in (token, new_token):
        assert client.post("/api/portal/accept", headers=teen,
                           json={"token": old_token}).status_code == 410
    assert client.delete(path + "/permanent", headers=parent).status_code == 404
    assert client.post("/api/portal/accept", headers=teen,
                       json={"token": other_code}).status_code == 200


@pytest.mark.parametrize("status", ["revoked", "expired", "failed"])
def test_permanent_invitation_deletion_is_scoped_and_removes_personal_data(status) -> None:
    from shared.accounts import AccountStatus

    app, client, parent, teen = portal()
    invitation(app, client, parent)
    record = client.get("/api/adolescents", headers=parent).json()["invitations"][0]
    app.state.portal.change(lambda data: next(iter(data["invitations"].values())).update(
        status="ready" if status == "expired" else status, expiresAt=0,
    ))
    other = app.state.store.register(subject="other-parent", contact="other@example.test")
    app.state.store.decide(other.id, AccountStatus.ACTIVE, decided_by="test")
    path = f"/api/adolescents/{record['id']}/permanent"
    assert client.delete(path, headers={"x-dev-subject": "other-parent"}).status_code == 404
    assert client.delete(path, headers=parent).status_code == 200
    saved = app.state.portal.read()
    assert saved["invitations"] == {}
    assert "teen@example.test" not in json.dumps(saved)
    assert record["id"] not in json.dumps(saved)


def test_deleting_invitations_does_not_reset_the_daily_limit() -> None:
    app, client, parent, teen = portal()
    for _attempt in range(10):
        invitation(app, client, parent)
        record = client.get("/api/adolescents", headers=parent).json()["invitations"][0]
        path = f"/api/adolescents/{record['id']}"
        assert client.delete(path, headers=parent).status_code == 200
        assert client.delete(path + "/permanent", headers=parent).status_code == 200
    assert client.post("/api/adolescents/invitations", headers=parent,
                       json={"email": "teen@example.test"}).status_code == 429
    app.state.portal.change(lambda data: [row.update(createdAt=0)
                                         for row in data["invitationHistory"]])
    invitation(app, client, parent)
    assert app.state.portal.read()["invitationHistory"] == []


def test_resend_replaces_old_invitation_and_parent_cannot_accept() -> None:
    app, client, parent, teen = portal()
    old = invitation(app, client, parent)
    new = invitation(app, client, parent)
    assert client.post("/api/portal/accept", headers=teen, json={"token": old}).status_code == 410
    assert client.post("/api/portal/accept", headers=parent, json={"token": new}).status_code == 409
    assert client.post("/api/portal/accept", headers=teen, json={"token": new}).status_code == 200


def test_adolescent_cannot_register_as_parent_even_after_revocation() -> None:
    app = create_app(settings=Settings(dev_auth=True, bootstrap_contact="teen@example.test"))
    app.state.portal.change(
        lambda data: data["members"].update({"teen": {"active": False}})
    )
    client = TestClient(app)
    response = client.get("/api/me", headers={
        "x-dev-subject": "teen", "x-dev-contact": "teen@example.test",
    })
    assert response.status_code == 403
    assert app.state.store.by_subject("teen") is None


def test_photo_upload_is_private_idempotent_and_reaches_home(tmp_path) -> None:
    from devices.camera_hub import CameraHub
    from devices.house import House
    from devices.sync_photos import synchronize

    app, client, parent, teen = portal()
    token = invitation(app, client, parent)
    client.post("/api/portal/accept", headers=teen, json={"token": token})
    image = io.BytesIO()
    Image.new("RGB", (30, 20), "red").save(image, "JPEG", exif=b"Exif\x00\x00private")
    photo_id = "a" * 32
    path = f"/api/portal/photos/{photo_id}"
    assert client.post(path, content=image.getvalue(), headers=teen).status_code == 200
    assert client.post(path, content=image.getvalue(), headers=teen).status_code == 200
    assert client.get("/api/portal/photos", headers=teen).json()["total"] == 1
    assert client.get("/api/photos", headers=parent).json()["total"] == 1
    content = client.get(path + "/content", headers=teen)
    assert b"private" not in content.content
    assert content.headers["cache-control"] == "no-store"
    household = client.get("/api/me", headers=parent).json()["householdId"]
    hub = CameraHub({"database": str(tmp_path / "photos.db")}, House(
        panel="https://panel", household=household, device_key="test-device-key",
        sheets_dir=tmp_path,
    ), tmp_path / "screen.bmp")

    def ask(url, body, **kwargs):
        response = client.post(url.removeprefix("https://panel"), json=body,
                               headers={"X-Device-Key": kwargs["key"]})
        assert response.status_code == 200, response.text
        return response.json()

    assert synchronize(hub, ask) == 1
    assert hub.store.get(photo_id)["jpeg"] == content.content
    assert hub.process_one()
    assert synchronize(hub, ask) == 1
    assert client.get("/api/portal/photos", headers=teen).json()["photos"][0]["state"] == "done"
    assert client.post(path, content=image.getvalue(), headers=teen).json()["state"] == "done"
    assert client.delete(path, headers=teen).status_code == 200
    synchronize(hub, ask)
    assert hub.store.get(photo_id)["jpeg"] is None
    assert client.get(path + "/content", headers=teen).status_code == 404
    assert client.post(path, content=image.getvalue(), headers=teen).status_code == 410


def test_upload_refuses_non_images_and_unauthenticated_calls() -> None:
    app, client, parent, teen = portal()
    token = invitation(app, client, parent)
    client.post("/api/portal/accept", headers=teen, json={"token": token})
    path = "/api/portal/photos/" + "b" * 32
    assert client.post(path, content=b"not a photo", headers=teen).status_code == 400
    assert client.post(path, content=b"x", headers=parent).status_code == 403
    assert client.get(path + "/content", headers=teen).status_code == 404


@pytest.mark.parametrize("outcome", ["matched", "unrelated", "uncertain", "no_activity"])
def test_mobile_photo_uses_camera_matching_and_advances_only_once(
    tmp_path, monkeypatch, outcome,
) -> None:
    from devices.camera_hub import CameraHub
    from devices.house import House
    from devices.run_experience import Afternoon, begin
    from devices.sync_photos import synchronize
    from shared.vision_contracts import PhotoMatch, WhatCameBack
    from tests.test_pretend import an_experience

    app, client, parent, teen = portal()
    token = invitation(app, client, parent)
    assert client.post("/api/portal/accept", headers=teen, json={"token": token}).status_code == 200
    household = client.get("/api/me", headers=parent).json()["householdId"]
    house = House(
        panel="https://panel", household=household, device_key="test-device-key",
        sheets_dir=tmp_path / "state", pretend=tmp_path / "pretend",
    )
    hub = CameraHub({"database": str(tmp_path / "photos.db")}, house, tmp_path / "screen.bmp")
    monkeypatch.setattr("devices.run_experience._tell_the_panel", lambda *args: None)
    monkeypatch.setattr("devices.hands.draw_page", lambda *args, **kwargs: np.full(
        (64, 64), 255, dtype=np.uint8,
    ))
    run_ids = ("aft_first", "aft_second") if outcome != "no_activity" else ()
    for run_id in run_ids:
        begin(house, an_experience(), run_id=run_id, now=time.time() - 60,
              send=False, max_open=2)
    paths = [house.sheets_dir / "afternoons" / f"{run_id}.json" for run_id in run_ids]
    before = [path.read_bytes() for path in paths]
    matched = []
    read = []
    displayed = []

    def match(image, candidates, **kwargs):
        matched.append(image)
        assert len(candidates) == 2
        assert all(candidate["expected"] for candidate in candidates)
        return PhotoMatch(candidate=1 if outcome == "matched" else None,
                          rotation=90, uncertain=outcome == "uncertain")

    def reading(blank, image, **kwargs):
        read.append(image)
        return WhatCameBack(written=True, same_sheet=True, describes=("a mark",), read_at=0.0)

    def display(photo_id, image):
        displayed.append((photo_id, image))
        return "photograph displayed"

    monkeypatch.setattr("devices.camera_hub.match_photo", match)
    monkeypatch.setattr("devices.run_experience.read_page", reading)
    monkeypatch.setattr(hub, "display_photo", display)
    image = io.BytesIO()
    Image.new("RGB", (30, 20), "red").save(image, "JPEG")
    photo_id = "d" * 32
    path = f"/api/portal/photos/{photo_id}"
    assert client.post(path, content=image.getvalue(), headers=teen).status_code == 200
    original = client.get(path + "/content", headers=teen).content

    def ask(url, body, **kwargs):
        response = client.post(url.removeprefix("https://panel"), json=body,
                               headers={"X-Device-Key": kwargs["key"]})
        assert response.status_code == 200, response.text
        return response.json()

    assert synchronize(hub, ask) == 1
    assert hub.process_one()
    assert synchronize(hub, ask) == 1
    archived = client.get("/api/portal/photos", headers=teen).json()["photos"][0]
    assert archived["state"] == "done"
    assert client.get(path + "/content", headers=teen).content == original
    assert hub.store.get(photo_id)["jpeg"] == original
    assert len(matched) == (0 if outcome == "no_activity" else 1)
    assert len(displayed) == (1 if outcome in {"unrelated", "no_activity"} else 0)
    if outcome == "matched":
        assert paths[0].read_bytes() == before[0]
        advanced = Afternoon.from_dict(json.loads(paths[1].read_bytes()))
        assert advanced.waiting_at == "l-ultimo-foglio"
        assert advanced.answered == ("come-e-tornato:marks",)
        assert len(read) == 1
        assert read[0].shape[:2] == (30, 20)
    else:
        assert [saved.read_bytes() for saved in paths] == before
        assert read == []
    after = [saved.read_bytes() for saved in paths]
    assert client.post(path, content=image.getvalue(), headers=teen).json()["state"] == "done"
    assert synchronize(hub, ask) == 0
    assert not hub.process_one()
    assert [saved.read_bytes() for saved in paths] == after


def test_code_invitation_needs_no_email_delivery() -> None:
    app, client, parent, teen = portal()
    response = client.post("/api/adolescents/invitations", headers=parent,
                           json={"email": "teen@example.test"})
    assert response.status_code == 201
    assert response.headers["cache-control"] == "no-store"
    assert not hasattr(app.state, "invitation_mailer")
    assert client.get("/api/adolescents", headers=parent).json()["invitations"][0][
        "status"
    ] == "ready"
    assert client.get("/api/portal/me", headers=teen).status_code == 403
    code = response.json()["code"]
    assert client.post("/api/portal/accept", headers=teen, json={"token": code}).status_code == 200


def test_redemption_attempts_are_limited_and_expire(monkeypatch) -> None:
    app, client, parent, teen = portal()
    token = invitation(app, client, parent)
    for _attempt in range(20):
        response = client.post("/api/portal/accept", headers=teen, json={"token": "z" * 43})
        assert response.status_code == 410
    response = client.post("/api/portal/accept", headers=teen, json={"token": token})
    assert response.status_code == 429
    assert response.headers["retry-after"] == "900"
    app.state.portal.change(lambda data: [row.update(since=0)
                                         for row in data["redemptions"].values()])
    assert client.post("/api/portal/accept", headers=teen, json={"token": token}).status_code == 200


def test_other_household_cannot_read_photos_or_revoke_access() -> None:
    from shared.accounts import AccountStatus

    app, client, parent, teen = portal()
    token = invitation(app, client, parent)
    client.post("/api/portal/accept", headers=teen, json={"token": token})
    member = client.get("/api/adolescents", headers=parent).json()["members"][0]
    other = app.state.store.register(subject="other-parent", contact="other@example.test")
    app.state.store.decide(other.id, AccountStatus.ACTIVE, decided_by="test")
    other_headers = {"x-dev-subject": "other-parent", "x-dev-contact": "other@example.test"}
    assert client.get("/api/adolescents", headers=other_headers).json()["members"] == []
    assert client.delete(
        f"/api/adolescents/{member['id']}", headers=other_headers,
    ).status_code == 404
    image = io.BytesIO()
    Image.new("RGB", (30, 20), "red").save(image, "JPEG")
    path = "/api/portal/photos/" + "c" * 32
    assert client.post(path, content=image.getvalue(), headers=teen).status_code == 200
    assert client.get("/api/photos", headers=other_headers).json()["total"] == 0
    assert client.get("/api/photos/" + "c" * 32 + "/content",
                      headers=other_headers).status_code == 404
    app.state.portal.change(lambda data: data["members"].update({"sibling": {
        **data["members"]["teen"], "id": "another-member",
    }}))
    sibling = {"x-dev-subject": "sibling", "x-dev-contact": "sibling@example.test"}
    assert client.get(path + "/content", headers=sibling).status_code == 404
    assert client.delete(path, headers=sibling).status_code == 404
    app.state.store.decide(
        app.state.store.by_subject("parent").id, AccountStatus.SUSPENDED, decided_by="test",
    )
    assert client.get("/api/portal/me", headers=teen).status_code == 403
    household = app.state.portal.read()["members"]["teen"]["household"]
    pulled = client.post(f"/api/device/{household}/portal-photos/pull", json={},
                         headers={"X-Device-Key": "test-device-key"})
    assert pulled.json() == {"photos": []}


def test_invite_rate_limit_and_competing_acceptance() -> None:
    from concurrent.futures import ThreadPoolExecutor

    app, client, parent, teen = portal()
    token = invitation(app, client, parent)

    def accept_as(subject):
        return client.post("/api/portal/accept", json={"token": token},
                           headers={**teen, "x-dev-subject": subject}).status_code

    with ThreadPoolExecutor(max_workers=2) as pool:
        statuses = list(pool.map(accept_as, ["first", "second"]))
    assert sorted(statuses) == [200, 410]
    for _attempt in range(9):
        invitation(app, client, parent)
    response = client.post("/api/adolescents/invitations", headers=parent,
                           json={"email": "teen@example.test"})
    assert response.status_code == 429


@pytest.fixture
def portal_blob_container():
    import json
    from types import SimpleNamespace

    from azure.core import MatchConditions
    from azure.core.exceptions import ResourceModifiedError, ResourceNotFoundError

    class Blob:
        content = None
        etag = 0
        race = False

        def download_blob(self):
            if self.content is None:
                raise ResourceNotFoundError("missing")
            snapshot = self.content
            return SimpleNamespace(
                readall=lambda: snapshot, properties=SimpleNamespace(etag=self.etag),
            )

        def upload_blob(self, content, overwrite, **kwargs):
            if self.race:
                self.race = False
                data = json.loads(self.content)
                data["members"]["other"] = {"active": True}
                self.content = json.dumps(data).encode()
                self.etag += 1
            if overwrite:
                assert kwargs["match_condition"] == MatchConditions.IfNotModified
                if kwargs["etag"] != self.etag:
                    raise ResourceModifiedError("changed")
            self.content = content
            self.etag += 1

    blob = Blob()
    return SimpleNamespace(get_blob_client=lambda _: blob)


def test_blob_store_survives_restart_and_retries_a_concurrent_change(portal_blob_container) -> None:
    from panel.adolescents import BlobPortalStore

    container = portal_blob_container
    blob = container.get_blob_client("portal/access.json")
    store = BlobPortalStore(container)
    store.change(lambda data: data["members"].update({"teen": {"active": True}}))
    blob.race = True
    store.change(lambda data: data["members"]["teen"].update(active=False))
    restored = BlobPortalStore(container)
    assert restored.known_subject("teen")
    assert restored.read()["members"] == {"teen": {"active": False}, "other": {"active": True}}


def test_concurrent_uploads_cannot_take_the_same_last_slot(monkeypatch) -> None:
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier

    from panel.photos import Photo

    app, client, parent, teen = portal()
    token = invitation(app, client, parent)
    client.post("/api/portal/accept", headers=teen, json={"token": token})
    member = app.state.portal.read()["members"]["teen"]
    for index in range(199):
        app.state.photos.save(member["household"], Photo(
            f"{index:032x}", "portal:" + member["id"], None, 100, 1, 1, "done", "digest",
        ), b"jpeg")
    barrier = Barrier(2)
    original = app.state.photos.list

    def synchronized_listing(household):
        rows = original(household)
        barrier.wait(timeout=5)
        return rows

    monkeypatch.setattr(app.state.photos, "list", synchronized_listing)
    image = io.BytesIO()
    Image.new("RGB", (30, 20), "red").save(image, "JPEG")

    def upload(identifier):
        return client.post("/api/portal/photos/" + identifier, headers=teen,
                           content=image.getvalue()).status_code

    with ThreadPoolExecutor(max_workers=2) as pool:
        statuses = list(pool.map(upload, ["a" * 32, "b" * 32]))
    assert sorted(statuses) == [200, 429]
    assert len(original(member["household"])) == 200