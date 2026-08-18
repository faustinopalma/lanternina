#!/usr/bin/env python3
"""Prompt locally for the one Wi-Fi configuration used to provision displays."""

from __future__ import annotations

import getpass
import json
import os
from pathlib import Path

OUTPUT = Path("/etc/lanternina/trmnl-provisioning.json")


def main() -> None:
    ssid = input("Wi-Fi SSID: ").strip()
    password = getpass.getpass("Wi-Fi password: ")
    if not ssid or not password:
        raise SystemExit("SSID and password cannot be empty")
    document = {
        "ssid": ssid,
        "password": password,
        "base_url": "http://lanternina.local:8080",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    temporary = OUTPUT.with_suffix(".tmp")
    temporary.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    temporary.chmod(0o600)
    os.replace(temporary, OUTPUT)
    print(f"Configuration stored in {OUTPUT}")


if __name__ == "__main__":
    main()