"""Minimal local server for TRMNL-compatible e-paper firmware."""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import struct
import time
from collections.abc import Mapping
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 480

# Measured on the kit in the house (model xiao_epaper_display, firmware 1.8.12): it sends
# Battery-Voltage and leaves Percent-Charged empty, because there is no fuel gauge. The
# thresholds below are therefore *derived* from a standard single-cell LiPo discharge
# curve — estimated, not measured on this cell — and a LiPo also sags under load and
# recovers afterwards, so one sample can read low while charge remains. Good enough to
# decide when to say something; not good enough to print as a number.
# Calibrating properly means running one cell down while logging voltage. Not done yet.
BATTERY_LOW_VOLTS = 3.70  # about a fifth left
BATTERY_CRITICAL_VOLTS = 3.60  # about a tenth left

# E-paper holds an image with no power, so once the message is up there is nothing to
# gain by waking often. Sleeping longer is what keeps the message readable for longer.
LOW_BATTERY_REFRESH = 3600
CRITICAL_BATTERY_REFRESH = 21600

# On USB there is no battery to spend, so the panel stays responsive instead: a change
# made in the house appears within this many seconds. The firmware handles small values
# (its own not-connected retry is 5 s), so this is a comfort choice, not a limit.
#
# ⚠️ This board cannot sense USB. In the firmware, get_usb_status() is implemented only for
# BOARD_TRMNL_X and BOARD_TRMNL_GEN2; everything else returns UNKNOWN, which the header
# builder sends as "USB-Connected: false". So a display on mains is marked as such in the
# registry, by us, and the header is only believed when it says true.
USB_REFRESH = 30

LEVEL_OK = "ok"
LEVEL_LOW = "low"
LEVEL_CRITICAL = "critical"

# How many device reports to keep. A display talks a handful of times an hour, so this is
# days of history in a file measured in kilobytes. Bounded on purpose: an unbounded log on
# the device that must never fill its own disk is a slow-motion outage.
DEVICE_LOG_KEEP = 300
# One report, truncated. The device writes this text, so it is untrusted input: it is
# stored and shown, never interpreted.
DEVICE_LOG_MAX_CHARS = 2000


def normalize_mac(value: str) -> str:
    return value.strip().upper().replace("-", ":")


@dataclass(frozen=True, slots=True)
class Config:
    base_url: str
    screen_file: Path
    registry_file: Path
    refresh_rate: int = 600
    # How often to look when mains powered. Battery is not being spent, so waiting is
    # pointless.
    usb_refresh_rate: int = USB_REFRESH
    # Where each device's last report is kept. Empty disables recording.
    status_file: Path | None = None
    # Where the displays' own logs are kept. Empty throws them away, which is what this
    # server did until it turned out they were the only thing explaining a failure.
    device_log_file: Path | None = None
    # Shown instead of the usual screen as the cell empties. Two tones, two moments.
    low_battery_file: Path | None = None
    critical_battery_file: Path | None = None

    @classmethod
    def from_env(cls) -> Config:
        status = os.environ.get("TRMNL_STATUS_FILE", "").strip()
        low = os.environ.get("TRMNL_LOW_BATTERY_FILE", "").strip()
        critical = os.environ.get("TRMNL_CRITICAL_BATTERY_FILE", "").strip()
        return cls(
            base_url=os.environ["TRMNL_BASE_URL"].rstrip("/"),
            screen_file=Path(os.environ["TRMNL_SCREEN_FILE"]),
            registry_file=Path(os.environ["TRMNL_DEVICE_REGISTRY"]),
            refresh_rate=int(os.environ.get("TRMNL_REFRESH_RATE", "600")),
            usb_refresh_rate=int(
                os.environ.get("TRMNL_USB_REFRESH_RATE", str(USB_REFRESH))
            ),
            status_file=Path(status) if status else None,
            device_log_file=(
                Path(os.environ["TRMNL_DEVICE_LOG_FILE"])
                if os.environ.get("TRMNL_DEVICE_LOG_FILE", "").strip()
                else None
            ),
            low_battery_file=Path(low) if low else None,
            critical_battery_file=Path(critical) if critical else None,
        )

    def screen_url(self, token: str, origin: str = "") -> str:
        # The display re-resolves this host at every download, and mDNS is the step that
        # was failing; the socket it is already connected on cannot fail to resolve.
        return f"{origin or self.base_url}/screen/{token}.bmp"


@dataclass(frozen=True, slots=True)
class Device:
    mac: str
    token: str
    friendly_id: str
    provisioned: bool = False
    # Declared, not sensed: this display is permanently powered.
    mains: bool = False


def load_devices(path: Path) -> dict[str, Device]:
    document = json.loads(path.read_text(encoding="utf-8"))
    return {
        normalize_mac(mac): Device(
            mac=normalize_mac(mac),
            token=str(values["token"]),
            friendly_id=str(values["friendly_id"]),
            provisioned=bool(values.get("provisioned", False)),
            mains=bool(values.get("mains", False)),
        )
        for mac, values in document.get("devices", {}).items()
    }


def _write_devices(path: Path, devices: dict[str, Device]) -> None:
    document = {
        "version": 1,
        "devices": {
            item.mac: {
                "token": item.token,
                "friendly_id": item.friendly_id,
                "provisioned": item.provisioned,
                "mains": item.mains,
            }
            for item in sorted(devices.values(), key=lambda value: value.mac)
        },
    }
    existing = path.stat() if path.exists() else None
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    temporary.chmod(0o640)
    # Keep owner and group. The registry is root:lanternina and the server reads it
    # through that group; a rewrite run as root would otherwise leave it root:root and
    # lock the server out of its own registry, which looks exactly like a dead device.
    if existing is not None and hasattr(os, "chown"):
        os.chown(temporary, existing.st_uid, existing.st_gid)
    temporary.replace(path)


def register_device(path: Path, mac: str) -> Device:
    normalized = normalize_mac(mac)
    devices = load_devices(path) if path.exists() else {}
    if normalized in devices:
        return devices[normalized]

    device = Device(
        mac=normalized,
        token=secrets.token_hex(24),
        friendly_id=normalized.replace(":", "")[-6:],
    )
    devices[normalized] = device
    _write_devices(path, devices)
    return device


def mark_provisioned(path: Path, mac: str) -> Device:
    normalized = normalize_mac(mac)
    devices = load_devices(path)
    current = devices[normalized]
    provisioned = Device(
        current.mac, current.token, current.friendly_id, True, current.mains
    )
    devices[normalized] = provisioned
    _write_devices(path, devices)
    return provisioned


def set_mains(path: Path, mac: str, mains: bool) -> Device:
    """Declare whether this display is permanently powered. The board cannot tell us."""
    normalized = normalize_mac(mac)
    devices = load_devices(path)
    current = devices[normalized]
    updated = Device(
        current.mac, current.token, current.friendly_id, current.provisioned, mains
    )
    devices[normalized] = updated
    _write_devices(path, devices)
    return updated


def _number(raw: str) -> float | None:
    """Parse a header the device sent, or return None. An absent reading must not
    become a zero: "0 volts" and "did not say" mean very different things."""
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def record_status(path: Path, device: Device, headers: Mapping[str, str]) -> dict[str, object]:
    """Store what this device reported on this poll. Returns the entry written."""
    entry: dict[str, object] = {
        "friendlyId": device.friendly_id,
        "lastSeen": time.time(),
        "batteryVoltage": _number(headers.get("Battery-Voltage", "")),
        "percentCharged": _number(headers.get("Percent-Charged", "")),
        "batteryHealth": _number(headers.get("Battery-Health", "")),
        "charging": headers.get("Battery-Charging", "") == "1",
        "usbConnected": headers.get("USB-Connected", "").lower() == "true",
        "rssi": _number(headers.get("RSSI", "")),
        "firmware": headers.get("FW-Version", ""),
        "model": headers.get("Model", ""),
        "refreshRate": _number(headers.get("Refresh-Rate", "")),
    }

    document: dict[str, Any] = {"version": 1, "devices": {}}
    if path.exists():
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            # A corrupt status file must not stop a device from being served.
            document = {"version": 1, "devices": {}}
    document.setdefault("devices", {})[device.mac] = entry

    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)
    return entry


def battery_level(voltage: float | None) -> str:
    """Coarse on purpose. None means the device did not say, which is not the same as full."""
    if voltage is None:
        return LEVEL_OK
    if voltage <= BATTERY_CRITICAL_VOLTS:
        return LEVEL_CRITICAL
    if voltage <= BATTERY_LOW_VOLTS:
        return LEVEL_LOW
    return LEVEL_OK


def usb_connected(headers: Mapping[str, str]) -> bool:
    return headers.get("USB-Connected", "").lower() == "true"


def last_state(path: Path | None, mac: str) -> tuple[float | None, bool]:
    """Voltage and USB flag from this device's last report. Both unknown is a valid answer."""
    if path is None or not path.exists():
        return None, False
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None, False
    entry = document.get("devices", {}).get(normalize_mac(mac))
    if not isinstance(entry, dict):
        return None, False
    voltage = entry.get("batteryVoltage")
    return (
        float(voltage) if isinstance(voltage, (int, float)) else None,
        bool(entry.get("usbConnected", False)),
    )


def recorded_level(path: Path | None, mac: str, mains: bool = False) -> str:
    """The level the screen choice uses, so picture and sleep never disagree."""
    if mains:
        return LEVEL_OK
    voltage, on_usb = last_state(path, mac)
    return LEVEL_OK if on_usb else battery_level(voltage)


def log_messages(body: Any) -> list[str]:
    """Pull the human-readable lines out of whatever shape the device sent."""
    if isinstance(body, str):
        return [body.strip()] if body.strip() else []
    found: list[str] = []
    if isinstance(body, dict):
        for key, value in body.items():
            if key in {"log_message", "message"} and isinstance(value, str):
                found.append(value.strip())
            else:
                found.extend(log_messages(value))
    elif isinstance(body, list):
        for item in body:
            found.extend(log_messages(item))
    return [line for line in found if line]


def record_device_log(path: Path, mac: str, raw: bytes) -> dict[str, Any]:
    """Append one report from a display, keeping the file bounded."""
    text = raw.decode("utf-8", errors="replace")[:DEVICE_LOG_MAX_CHARS]
    try:
        body: Any = json.loads(text)
    except ValueError:
        body = text
    entry: dict[str, Any] = {"at": time.time(), "mac": mac, "body": body}

    kept: list[str] = []
    if path.exists():
        try:
            kept = path.read_text(encoding="utf-8").splitlines()[-(DEVICE_LOG_KEEP - 1) :]
        except OSError:
            kept = []
    kept.append(json.dumps(entry, ensure_ascii=False))
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text("\n".join(kept) + "\n", encoding="utf-8")
    temporary.replace(path)
    return entry


def validate_screen(path: Path) -> bytes:
    data = path.read_bytes()
    if len(data) < 30 or data[:2] != b"BM":
        raise ValueError("screen must be a BMP file")
    width, height = struct.unpack_from("<ii", data, 18)
    bits_per_pixel = struct.unpack_from("<H", data, 28)[0]
    if (width, abs(height), bits_per_pixel) != (DISPLAY_WIDTH, DISPLAY_HEIGHT, 1):
        raise ValueError("screen must be an 800x480 1-bit BMP")
    return data


def screen_for(shared: Path, friendly_id: str) -> Path:
    """Where a display's own picture lives, beside the one they all share.

    A display with a job of its own — the sheet on the printer, what to do next — writes
    here and stops following the picture. Absent is the normal state, not a fault.
    """
    return shared.with_name(f"{shared.stem}-{friendly_id}{shared.suffix}")


def make_handler(config: Config) -> type[BaseHTTPRequestHandler]:
    # Validated once here so a broken file fails at startup, not in front of a device.
    last_good = validate_screen(config.screen_file)

    def current_screen(device: Device) -> bytes:
        """Re-read on every request, so new content needs no restart."""
        nonlocal last_good
        level = recorded_level(config.status_file, device.mac, device.mains)
        farewell = _valid_or_none(
            config.critical_battery_file
            if level == LEVEL_CRITICAL
            else config.low_battery_file
            if level == LEVEL_LOW
            else None
        )
        if farewell is not None:
            return farewell
        own = _valid_or_none(screen_for(config.screen_file, device.friendly_id))
        if own is not None:
            return own
        try:
            last_good = validate_screen(config.screen_file)
        except (OSError, ValueError):
            # A half-written file must never blank the display.
            pass
        return last_good

    def _valid_or_none(path: Path | None) -> bytes | None:
        if path is None:
            return None
        try:
            return validate_screen(path)
        except (OSError, ValueError):
            return None

    class Handler(BaseHTTPRequestHandler):
        server_version = "LanterninaTRMNL/0.1"

        def do_GET(self) -> None:
            path = urlsplit(self.path).path
            if path == "/health":
                self._json(HTTPStatus.OK, {"status": "ok"})
            elif path == "/api/setup":
                self._setup()
            elif path == "/api/display":
                self._display()
            elif self._device_for_screen_path(path) is not None:
                device = self._device_for_screen_path(path)
                assert device is not None
                self._bytes(HTTPStatus.OK, "image/bmp", current_screen(device))
            else:
                self._json(HTTPStatus.NOT_FOUND, {"status": 404})

        def do_POST(self) -> None:
            if urlsplit(self.path).path != "/api/log":
                self._json(HTTPStatus.NOT_FOUND, {"status": 404})
                return
            if not self._authorized():
                self._json(HTTPStatus.FORBIDDEN, {"status": 403})
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(min(length, 64 * 1024)) if length else b""
            device = self._device_for_request()
            if config.device_log_file is not None and device is not None:
                try:
                    entry = record_device_log(config.device_log_file, device.mac, raw)
                    for line in log_messages(entry["body"])[:3]:
                        self.log_message("display %s says: %s", device.friendly_id, line)
                except OSError as exc:
                    # Bookkeeping must never stop a device from being served.
                    self.log_message("could not record device log: %s", exc)
            self.send_response(HTTPStatus.NO_CONTENT)
            self.end_headers()

        def _setup(self) -> None:
            device = self._device_for_request()
            if device is None:
                self._json(HTTPStatus.NOT_FOUND, {"status": 404})
                return
            self._json(
                HTTPStatus.OK,
                {
                    "status": 200,
                    "api_key": device.token,
                    "friendly_id": device.friendly_id,
                    "image_url": config.screen_url(device.token, self._origin()),
                    "filename": "lanternina-ready",
                },
            )

        def _display(self) -> None:
            device = self._device_for_request()
            if device is None or self.headers.get("Access-Token", "") != device.token:
                self._json(HTTPStatus.FORBIDDEN, {"status": 403})
                return

            if config.status_file is not None:
                try:
                    record_status(config.status_file, device, self.headers)
                except OSError as exc:
                    # Never let bookkeeping stop a device from getting its picture.
                    self.log_message("could not record status: %s", exc)

            level = battery_level(_number(self.headers.get("Battery-Voltage", "")))
            on_usb = device.mains or usb_connected(self.headers)
            if on_usb:
                # Charging pins the voltage near full, so a battery notice while plugged
                # in would be both wrong and impossible to act on.
                level = LEVEL_OK
            refresh = (
                config.usb_refresh_rate
                if on_usb
                else {
                    LEVEL_CRITICAL: CRITICAL_BATTERY_REFRESH,
                    LEVEL_LOW: LOW_BATTERY_REFRESH,
                }.get(level, config.refresh_rate)
            )
            # `filename` is the firmware's cache key, so it follows the bytes: any new
            # picture changes it, and an unchanged one does not.
            fingerprint = hashlib.sha256(current_screen(device)).hexdigest()[:12]
            self._json(
                HTTPStatus.OK,
                {
                    "status": 0,
                    "image_url": config.screen_url(device.token, self._origin()),
                    "filename": f"lanternina-{level}-{fingerprint}",
                    "refresh_rate": str(refresh),
                    "update_firmware": False,
                    "firmware_url": None,
                    "reset_firmware": False,
                },
            )

        def _origin(self) -> str:
            """This server's address as reached by this very device, port included."""
            try:
                host, port = self.connection.getsockname()[:2]
            except OSError:
                return ""
            return f"http://{host}:{port}"

        def _authorized(self) -> bool:
            device = self._device_for_request()
            return device is not None and self.headers.get("Access-Token", "") == device.token

        def _device_for_request(self) -> Device | None:
            return load_devices(config.registry_file).get(
                normalize_mac(self.headers.get("ID", ""))
            )

        def _device_for_screen_path(self, path: str) -> Device | None:
            prefix = "/screen/"
            suffix = ".bmp"
            if not path.startswith(prefix) or not path.endswith(suffix):
                return None
            token = path[len(prefix) : -len(suffix)]
            return next(
                (
                    device
                    for device in load_devices(config.registry_file).values()
                    if device.token == token
                ),
                None,
            )

        def _json(self, status: HTTPStatus, body: dict[str, object]) -> None:
            payload = json.dumps(body, separators=(",", ":")).encode()
            self._bytes(status, "application/json", payload)

        def _bytes(self, status: HTTPStatus, content_type: str, body: bytes) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def log_request(self, code: int | str = "-", size: int | str = "-") -> None:
            path = urlsplit(self.path).path
            if path.startswith("/screen/"):
                path = "/screen/<token>.bmp"
            self.log_message(
                '"%s %s %s" %s %s', self.command, path, self.request_version, code, size
            )

        def log_message(self, format: str, *args: object) -> None:
            super().log_message(format, *args)

    return Handler


def main() -> None:
    config = Config.from_env()
    port = int(os.environ.get("TRMNL_PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), make_handler(config))
    server.serve_forever()


if __name__ == "__main__":
    main()