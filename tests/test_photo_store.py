from __future__ import annotations

import io
from pathlib import Path

import pytest
from PIL import Image

from devices.photo_store import PhotoStore

PHOTO = "a" * 32


def jpeg(colour: str = "red") -> bytes:
    output = io.BytesIO()
    Image.new("RGB", (64, 48), colour).save(output, "JPEG")
    return output.getvalue()


def test_receipt_survives_reopen_and_duplicate_is_not_reprocessed(tmp_path: Path) -> None:
    store = PhotoStore(tmp_path / "photos.db")
    assert store.accept(PHOTO, "camera", jpeg(), captured=10, target={"run": "one"})
    store = PhotoStore(store.path)
    assert not store.accept(PHOTO, "camera", jpeg(), captured=20, target={"run": "two"})
    assert store.get(PHOTO)["captured"] == 10
    assert store.claim()["id"] == PHOTO
    assert store.claim() is None
    store.finish(PHOTO, "done", "picture")
    assert store.get(PHOTO)["state"] == "done"


def test_deleted_photo_cannot_be_resurrected_by_a_retry(tmp_path: Path) -> None:
    store = PhotoStore(tmp_path / "photos.db")
    store.accept(PHOTO, "camera", jpeg(), captured=None, target=None)
    store.delete(PHOTO)
    assert not store.accept(PHOTO, "camera", jpeg(), captured=None, target=None)
    assert store.get(PHOTO)["jpeg"] is None
    assert store.listing() == []
    assert store.claim() is None


@pytest.mark.parametrize("camera, data", [("other", jpeg()), ("camera", jpeg("blue"))])
def test_conflicting_receipt_is_rejected(tmp_path: Path, camera: str, data: bytes) -> None:
    store = PhotoStore(tmp_path / "photos.db")
    store.accept(PHOTO, "camera", jpeg(), captured=None, target=None)
    with pytest.raises(ValueError, match="different bytes"):
        store.accept(PHOTO, camera, data, captured=None, target=None)


@pytest.mark.parametrize("photo_id, data", [("../escape", jpeg()), (PHOTO, b"not a JPEG")])
def test_bad_upload_never_receives_a_receipt(tmp_path: Path, photo_id: str, data: bytes) -> None:
    store = PhotoStore(tmp_path / "photos.db")
    with pytest.raises((ValueError, OSError)):
        store.accept(photo_id, "camera", data, captured=None, target=None)
    assert store.listing() == []


def test_restart_requires_review_and_never_replays_claimed_work(tmp_path):
    store = PhotoStore(tmp_path / "photos.db")
    store.accept(PHOTO, "camera", jpeg(), captured=10, target={"run": "one"})
    assert not store.archive_reviewed(PHOTO)
    assert store.claim()["id"] == PHOTO
    restarted = PhotoStore(store.path)
    assert restarted.claim() is None
    assert restarted.archive_reviewed(PHOTO)
    assert restarted.claim() is None
    assert restarted.get(PHOTO)["target"] == "null"
    assert not restarted.accept(PHOTO, "camera", jpeg(), captured=10, target={"run": "one"})
    assert restarted.claim() is None


def test_deletion_wins_over_completion_and_review(tmp_path):
    store = PhotoStore(tmp_path / "photos.db")
    store.accept(PHOTO, "camera", jpeg(), captured=None, target=None)
    store.claim()
    store.delete(PHOTO)
    store.finish(PHOTO, "done", "late completion")
    assert not store.archive_reviewed(PHOTO)
    assert store.get(PHOTO)["state"] == "deleted"
    assert store.get(PHOTO)["jpeg"] is None


@pytest.mark.parametrize("resolve", ["archive_reviewed", "delete"])
def test_another_queued_photo_cannot_replay_an_interrupted_moment(tmp_path, resolve):
    store = PhotoStore(tmp_path / "photos.db")
    target = {"run": "one", "moment": "build", "since": 10}
    store.accept(PHOTO, "camera", jpeg(), captured=11, target=target)
    store.claim()
    store.accept("b" * 32, "camera", jpeg(), captured=12, target=target)
    restarted = PhotoStore(store.path)
    assert restarted.claim() is None
    getattr(restarted, resolve)(PHOTO)
    assert restarted.claim() is None
    assert restarted.get("b" * 32)["state"] == "done"
    assert restarted.get("b" * 32)["target"] == "null"