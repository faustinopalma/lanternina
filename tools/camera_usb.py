"""Issue an explicit development capture over the enrolled camera's USB serial port."""

from __future__ import annotations

import argparse
import json
import sqlite3
import time
from pathlib import Path


def open_port(name: str):
    import serial

    return serial.Serial(name, 115200, timeout=1, write_timeout=3)


def authenticated_since(mac: str, since: float) -> bool:
    config = json.loads(Path("/etc/lanternina/camera.json").read_text())
    with sqlite3.connect(config["database"]) as database:
        row = database.execute("SELECT report FROM camera_status WHERE id=?", (mac,)).fetchone()
    return bool(row and json.loads(row[0]).get("lastSeen", 0) >= since)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("CAPTURE", "CAPTURE_SETTLED", "STATUS", "STORAGE", "USB_TEST_ON", "USB_TEST_OFF"),
    )
    parser.add_argument("--mac", default="94:A9:90:D0:9D:D0")
    parser.add_argument("--authenticated-since", type=float)
    args = parser.parse_args()
    began = time.monotonic()
    port_name = (
        "/dev/serial/by-id/usb-Espressif_USB_JTAG_serial_debug_unit_" + args.mac.upper() + "-if00"
    )
    try:
        with open_port(port_name) as port:
            port.reset_input_buffer()
            port.write((args.command + "\n").encode("ascii"))
            acknowledged = False
            short_probe = False
            usb_status = False
            while time.monotonic() - began < 60:
                line = port.readline().decode("utf-8", "replace").strip()
                if not line:
                    continue
                print(line, flush=True)
                if "command=BUSY" in line or "UNKNOWN_OR_NO_USB" in line:
                    raise RuntimeError("camera did not accept the command")
                if args.command == "USB_TEST_ON" and line == (
                    "usb_test=on button_triggers_disabled_until_disconnect"
                ):
                    return
                if args.command == "USB_TEST_OFF" and line == "usb_test=off":
                    return
                if args.command == "STATUS" and line.startswith("status usb="):
                    if args.authenticated_since is None:
                        return
                    usb_status = "filesystem=1" in line and f"identity={args.mac.upper()}" in line
                if usb_status and authenticated_since(args.mac.upper(), args.authenticated_since):
                    print(
                        "VERDICT: USB identity, filesystem and fresh authenticated status verified"
                    )
                    return
                if args.command == "STORAGE":
                    short_probe |= "length=16 opened=1" in line
                    if "length=37" in line:
                        if not short_probe:
                            raise RuntimeError("short filename probe failed")
                        return
                if args.command in ("CAPTURE", "CAPTURE_SETTLED"):
                    if "capture_failed=" in line or "accepted=0" in line:
                        raise RuntimeError("capture or delivery failed")
                    acknowledged |= "upload=" in line and "accepted=1" in line
                    if acknowledged and "busy=0" in line and "queued=0" in line:
                        print("VERDICT: photograph acknowledged; queue empty; USB awake")
                        return
            raise TimeoutError("camera did not complete the command within 60 seconds")
    finally:
        print(f"elapsed: {time.monotonic() - began:.1f}s", flush=True)


if __name__ == "__main__":
    main()
