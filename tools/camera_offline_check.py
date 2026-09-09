"""Exercise a diagnostic offline upload without interrupting power or replaying an activity."""

from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

from tools.camera_usb import open_port


def run(arguments: list[str], *, check: bool = True, capture: bool = False
    ) -> subprocess.CompletedProcess:
    began = time.monotonic()
    try:
        return subprocess.run(arguments, check=check, timeout=100, capture_output=capture,
                      text=True)
    finally:
        print(f"command elapsed: {time.monotonic() - began:.1f}s", flush=True)


def main() -> None:
    config = json.loads(Path("/etc/lanternina/camera.json").read_text())
    if len(config["cameras"]) != 1:
        raise ValueError("this acceptance check requires exactly one enrolled camera")
    mac = next(iter(config["cameras"]))
    def rows() -> list[dict]:
        with sqlite3.connect(config["database"]) as database:
            database.row_factory = sqlite3.Row
            return [dict(row) for row in database.execute(
                "SELECT id, target FROM photos WHERE jpeg IS NOT NULL"
            )]

    before = {row["id"] for row in rows()}
    command = [sys.executable, "-m", "tools.camera_usb"]
    try:
        run(command + ["USB_TEST_ON", "--mac", mac])
        port_name = f"/dev/serial/by-id/usb-Espressif_USB_JTAG_serial_debug_unit_{mac}-if00"
        idle_began = time.monotonic()
        with open_port(port_name) as port:
            while time.monotonic() - idle_began < 30:
                if b"busy=0" in port.readline():
                    break
            else:
                raise TimeoutError("camera did not become idle before the offline check")
        run(["systemctl", "stop", "lanternina-camera"])
        failed = run(command + ["CAPTURE", "--mac", mac], check=False, capture=True)
        print(failed.stdout, flush=True)
        if failed.returncode == 0 or "upload=" not in failed.stdout or "accepted=0" not in (
            failed.stdout
        ):
            raise RuntimeError("expected a saved capture with a failed upload, not BUSY")
        run(["systemctl", "start", "lanternina-camera"])
        began = time.monotonic()
        accepted = ""
        with open_port(port_name) as port:
            while time.monotonic() - began < 90:
                line = port.readline().decode("utf-8", "replace").strip()
                if "upload=" in line and "accepted=1" in line:
                    accepted = line.split("upload=", 1)[1].split()[0]
                    print(line, flush=True)
                if accepted and "busy=0" in line and "queued=0" in line:
                    arrived = [row for row in rows() if row["id"] not in before]
                    if len(arrived) != 1 or arrived[0]["id"] != accepted:
                        raise RuntimeError("expected exactly one new durable photograph")
                    if arrived[0]["target"] != "null":
                        raise RuntimeError("diagnostic upload was assigned to an activity")
                    print(f"VERDICT: offline retry delivered {accepted} once; queue empty")
                    return
        raise TimeoutError("offline photograph did not drain within 90 seconds")
    finally:
        run(["systemctl", "start", "lanternina-camera"])
        run(command + ["USB_TEST_OFF", "--mac", mac])


if __name__ == "__main__":
    began = time.monotonic()
    try:
        main()
    finally:
        print(f"elapsed: {time.monotonic() - began:.1f}s", flush=True)