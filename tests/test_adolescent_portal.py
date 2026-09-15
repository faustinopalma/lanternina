"""The adolescent portal never grants parent permissions."""

from __future__ import annotations

import io

from fastapi.testclient import TestClient
from PIL import Image

from panel.app import create_app
from panel.config import Settings


def portal():
    app = create_app(settings=Settings(
        dev_auth=True, bootstrap_contact="parent@example.test",
        device_key="test-device-key",
    ))
    client = TestClient(app)
    parent = {"x-dev-subject": "parent", "x-dev-contact": "parent@example.test"}
    teen = {"x-dev-subject": "teen", "x-dev-contact": "teen@example.test"}
    assert client.get("/api/me", headers=parent).status_code == 200
    return app, client, parent, teen


def invitation(app, client, parent):
    response = client.post("/api/adolescents/invitations", headers=parent,
                           json={"email": "teen@example.test"})
    assert response.status_code == 201
    assert response.json()["status"] == "ready"
    return response.json()["code"]


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


def test_blob_store_survives_restart_and_retries_a_concurrent_change() -> None:
    import json
    from types import SimpleNamespace

    from azure.core import MatchConditions
    from azure.core.exceptions import ResourceModifiedError, ResourceNotFoundError

    from panel.adolescents import BlobPortalStore

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
    container = SimpleNamespace(get_blob_client=lambda _: blob)
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