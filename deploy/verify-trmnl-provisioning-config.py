#!/usr/bin/env python3
"""Validate the root-owned TRMNL provisioning config without printing secrets."""

from __future__ import annotations

import json
from pathlib import Path

PATH = Path("/etc/lanternina/trmnl-provisioning.json")


def main() -> None:
    document = json.loads(PATH.read_text(encoding="utf-8"))
    checks = {
        "ssid_present": bool(document.get("ssid")),
        "password_present": bool(document.get("password")),
        "base_url_correct": document.get("base_url") == "http://lanternina.local:8080",
    }
    for name, value in checks.items():
        print(f"{name}={str(value).lower()}")
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()