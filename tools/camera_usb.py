"""Issue an explicit development capture over the enrolled camera's USB serial port."""

from __future__ import annotations

import argparse
import time


def open_port(name: str):
    import serial

    return serial.Serial(name, 115200, timeout=1, write_timeout=3)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("CAPTURE", "STATUS", "STORAGE"))
    parser.add_argument("--mac", default="94:A9:90:D0:9D:D0")
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
            while time.monotonic() - began < 60:
                line = port.readline().decode("utf-8", "replace").strip()
                if not line:
                    continue
                print(line, flush=True)
                if "command=BUSY" in line or "UNKNOWN_OR_NO_USB" in line:
                    raise RuntimeError("camera did not accept the command")
                if args.command == "STATUS" and line.startswith("status usb="):
                    return
                if args.command == "STORAGE":
                    short_probe |= "length=16 opened=1" in line
                    if "length=37" in line:
                        if not short_probe:
                            raise RuntimeError("short filename probe failed")
                        return
                if args.command == "CAPTURE":
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
