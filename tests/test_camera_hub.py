from __future__ import annotations

import io
import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest
from PIL import Image

from devices.camera_hub import CameraHub, captured_at, make_handler, render_photo
from devices.house import House
from tests.test_photo_store import PHOTO, jpeg


def test_photo_frame_contains_the_whole_portrait() -> None:
    image = Image.open(io.BytesIO(render_photo(jpeg())))
    assert image.size == (800, 480)
    assert image.mode == "1"


@pytest.mark.parametrize("header", [{}, {"X-Capture-Age": "-2"}, {"X-Captured-At": "nan"}])
def test_unknown_or_invalid_capture_time_is_not_current(header: dict[str, str]) -> None:
    assert captured_at(header, 100) is None


def test_upload_requires_camera_identity_and_durable_receipt(tmp_path: Path) -> None:
    hub = CameraHub(
        {
            "database": str(tmp_path / "photos.db"),
            "cameras": {"CAM": "secret"},
            "family_password": "separate",
        },
        House(sheets_dir=tmp_path),
        tmp_path / "s.bmp",
    )
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(hub))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}/photos/{PHOTO}"
    headers = {"Content-Type": "image/jpeg", "X-Camera-Id": "CAM"}
    try:
        with pytest.raises(urllib.error.HTTPError) as denied:
            urllib.request.urlopen(urllib.request.Request(url, jpeg(), headers, method="PUT"))
        assert denied.value.code == 401
        headers["Authorization"] = "Bearer secret"
        for expected in (201, 200):
            with urllib.request.urlopen(
                urllib.request.Request(url, jpeg(), headers, method="PUT")
            ) as response:
                assert response.status == expected
                assert json.load(response) == {"id": PHOTO, "stored": True}
        assert hub.store.get(PHOTO)["jpeg"] == jpeg()
        with pytest.raises(urllib.error.HTTPError) as denied:
            urllib.request.urlopen(urllib.request.Request(url, headers=headers))
        assert denied.value.code == 401
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
