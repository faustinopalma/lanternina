"""Authenticated camera intake, family archive and asynchronous activity delivery."""

from __future__ import annotations

import base64
import hmac
import io
import json
import math
import os
import ssl
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps

from devices.epaper import _encode
from devices.house import House, printer_in, replace, scanner_in, screen_in
from devices.photo_store import MAX_PHOTO_BYTES, PHOTO_ID, PhotoStore
from devices.pull_picture import picture_target
from devices.run_experience import camera_target, carry_on
from devices.trmnl_byos import photo_for


def captured_at(headers: Any, now: float) -> float | None:
    age = headers.get("X-Capture-Age")
    absolute = headers.get("X-Captured-At")
    try:
        captured = now - float(age) if age is not None else float(absolute)
    except (TypeError, ValueError):
        return None
    return captured if math.isfinite(captured) and 0 < captured <= now else None


def render_photo(jpeg: bytes) -> bytes:
    with Image.open(io.BytesIO(jpeg)) as image:
        photo = ImageOps.exif_transpose(image).convert("L")
        photo = ImageOps.autocontrast(ImageOps.contain(photo, (768, 448)), cutoff=1)
        canvas = Image.new("L", (800, 480), 255)
        canvas.paste(photo, ((800 - photo.width) // 2, (480 - photo.height) // 2))
        return _encode(canvas.convert("1"), "BMP")


class CameraHub:
    def __init__(self, config: dict[str, Any], house: House, shared: Path):
        self.config = config
        self.house = house
        self.shared = shared
        self.store = PhotoStore(Path(config["database"]))
        self.changed = threading.Event()
        self.sync_changed = threading.Event()
        self.processing = threading.Lock()

    def process_one(self) -> bool:
        with self.processing:
            row = self.store.claim()
            if row is None:
                return False
            try:
                target = json.loads(row["target"])
                if target:
                    result = carry_on(self.house, photograph=row["jpeg"], target=target)
                else:
                    from devices.inventory import holders, load_jobs

                    jobs = Path(
                        os.environ.get("LANTERNINA_JOBS_FILE", "")
                        or self.shared.with_name("jobs.json")
                    )
                    displays = [
                        str(device["label"])
                        for device in holders(load_jobs(jobs), "photo")
                        if device.get("label")
                    ]
                    if not displays:
                        label, _ = picture_target(self.shared, jobs)
                        displays = [label] if label else []
                    if displays:
                        label = min(
                            displays,
                            key=lambda value: (
                                photo_for(self.shared, value).stat().st_mtime
                                if photo_for(self.shared, value).exists()
                                else 0
                            ),
                        )
                        path = photo_for(self.shared, label)
                        replace(path, render_photo(row["jpeg"]))
                        replace(path.with_suffix(".json"), json.dumps({"id": row["id"]}).encode())
                        result = f"photograph displayed on {label}"
                    else:
                        result = "photograph archived; no picture display assigned"
                self.store.finish(row["id"], "done", result)
            except Exception as exc:
                self.store.finish(row["id"], "failed", type(exc).__name__)
                print(f"camera processing failed: {type(exc).__name__}", flush=True)
            return True

    def worker(self) -> None:
        while True:
            self.changed.wait(30)
            self.changed.clear()
            while self.process_one():
                pass
            self.sync_changed.set()

    def sync_worker(self) -> None:
        from devices.sync_photos import synchronize

        while True:
            self.sync_changed.wait(60)
            self.sync_changed.clear()
            try:
                synchronize(self)
            except Exception as exc:
                print(f"photo synchronization failed: {type(exc).__name__}", flush=True)

    def delete(self, photo_id: str) -> None:
        with self.processing:
            self.store.delete(photo_id)
            for metadata in self.shared.parent.glob(f"{self.shared.stem}-*-photo.json"):
                if json.loads(metadata.read_text())["id"] == photo_id:
                    metadata.with_suffix(".bmp").unlink(missing_ok=True)
                    metadata.unlink(missing_ok=True)


def make_handler(hub: CameraHub) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            camera = self.headers.get("X-Camera-Id", "").upper()
            token = hub.config["cameras"].get(camera)
            if not token or not hmac.compare_digest(
                self.headers.get("Authorization", ""), "Bearer " + token
            ):
                self.respond(401, b"{}")
                return
            if self.path != "/status":
                self.respond(404, b"{}")
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 2048 or self.headers.get("Transfer-Encoding"):
                    raise ValueError("invalid status length")
                values = json.loads(self.rfile.read(size))
                voltage = values.get("voltage")
                if voltage is not None:
                    voltage = float(voltage)
                    if not math.isfinite(voltage) or not 2.5 <= voltage <= 4.5:
                        raise ValueError("invalid battery voltage")
                usb = values.get("usb") is True
                rssi = float(values["rssi"])
                if not math.isfinite(rssi) or not -120 <= rssi <= 0:
                    raise ValueError("invalid RSSI")
                level = (
                    "usb"
                    if usb
                    else "unknown"
                    if voltage is None
                    else ("critical" if voltage < 3.6 else "low" if voltage < 3.7 else "ok")
                )
                hub.store.record_camera(
                    {
                        "id": camera,
                        "kind": "camera",
                        "name": "XIAO " + camera.replace(":", "")[-6:],
                        "model": "XIAO ESP32S3 Sense",
                        "lastSeen": time.time(),
                        "level": level,
                        "voltage": voltage,
                        "rssi": rssi,
                        "firmware": str(values.get("firmware", ""))[:64],
                        "address": self.client_address[0],
                    }
                )
            except (ValueError, TypeError, KeyError, AttributeError):
                self.respond(400, b"{}")
                return
            hub.sync_changed.set()
            self.respond(200, b'{"received":true}')

        def setup(self) -> None:
            self.request.settimeout(20)
            super().setup()

        def respond(self, status: int, content: bytes, kind: str = "application/json") -> None:
            self.send_response(status)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; style-src 'unsafe-inline'; "
                "script-src 'unsafe-inline'; frame-ancestors 'none'",
            )
            self.end_headers()
            self.wfile.write(content)

        def family(self) -> bool:
            expected = (
                "Basic "
                + base64.b64encode(("family:" + hub.config["family_password"]).encode()).decode()
            )
            if hmac.compare_digest(self.headers.get("Authorization", ""), expected):
                return True
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Lanternina photos"')
            self.send_header("Content-Length", "0")
            self.end_headers()
            return False

        def do_PUT(self) -> None:
            photo_id = self.path.removeprefix("/photos/")
            camera = self.headers.get("X-Camera-Id", "").upper()
            token = hub.config["cameras"].get(camera)
            if not token or not hmac.compare_digest(
                self.headers.get("Authorization", ""), "Bearer " + token
            ):
                self.respond(401, b"{}")
                return
            if not self.path.startswith("/photos/") or not PHOTO_ID.fullmatch(photo_id):
                self.respond(404, b"{}")
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= MAX_PHOTO_BYTES:
                    self.respond(413, b"{}")
                    return
                if (
                    self.headers.get("Transfer-Encoding")
                    or self.headers.get("Content-Type") != "image/jpeg"
                ):
                    self.respond(415, b"{}")
                    return
                body = self.rfile.read(length)
                if len(body) != length:
                    raise ValueError("incomplete upload")
                captured = captured_at(self.headers, time.time())
                created = hub.store.accept(
                    photo_id,
                    camera,
                    body,
                    captured=captured,
                    target=camera_target(
                        hub.house.sheets_dir,
                        captured if self.headers.get("X-Captured-At") else None,
                    ),
                )
            except OverflowError:
                self.respond(507, b"{}")
                return
            except (ValueError, OSError):
                self.respond(400, b"{}")
                return
            hub.changed.set()
            self.respond(
                201 if created else 200, json.dumps({"id": photo_id, "stored": True}).encode()
            )

        def do_GET(self) -> None:
            if not self.family():
                return
            if self.path == "/":
                self.respond(
                    200,
                    Path(__file__).with_name("camera_gallery.html").read_bytes(),
                    "text/html; charset=utf-8",
                )
            elif self.path == "/photos":
                self.respond(200, json.dumps(hub.store.listing()).encode())
            elif self.path.startswith("/photos/"):
                photo_id = self.path.removeprefix("/photos/")
                row = hub.store.get(photo_id) if PHOTO_ID.fullmatch(photo_id) else None
                if row and row["jpeg"] is not None:
                    self.respond(200, row["jpeg"], "image/jpeg")
                else:
                    self.respond(404, b"{}")
            else:
                self.respond(404, b"{}")

        def do_DELETE(self) -> None:
            if not self.family():
                return
            photo_id = self.path.removeprefix("/photos/")
            if (
                self.headers.get("X-Photo-Action") != "delete"
                or not self.path.startswith("/photos/")
                or not PHOTO_ID.fullmatch(photo_id)
            ):
                self.respond(400, b"{}")
                return
            hub.delete(photo_id)
            self.respond(200, b"{}")

        def log_message(self, format: str, *args: object) -> None:
            pass

    return Handler


def main() -> None:
    config = json.loads(
        Path(os.environ.get("LANTERNINA_CAMERA_CONFIG", "/etc/lanternina/camera.json")).read_text()
    )
    house = House(
        printer=printer_in(os.environ),
        scanner=scanner_in(os.environ),
        screen=screen_in(os.environ),
        sheets_dir=Path(os.environ["LANTERNINA_SHEETS_DIR"]),
        panel=os.environ.get("LANTERNINA_PANEL_URL", ""),
        household=os.environ.get("LANTERNINA_HOUSEHOLD", ""),
        device_key=os.environ.get("LANTERNINA_DEVICE_KEY", ""),
    )
    hub = CameraHub(config, house, Path(os.environ["TRMNL_SCREEN_FILE"]))
    server = ThreadingHTTPServer(
        (config.get("listen", "0.0.0.0"), config.get("port", 8443)), make_handler(hub)
    )
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(config["certificate"], config["private_key"])
    server.socket = context.wrap_socket(
        server.socket, server_side=True, do_handshake_on_connect=False
    )
    threading.Thread(target=hub.worker, daemon=True).start()
    threading.Thread(target=hub.sync_worker, daemon=True).start()
    hub.changed.set()
    server.serve_forever()


if __name__ == "__main__":
    main()
