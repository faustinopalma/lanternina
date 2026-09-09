"""Inspect interrupted camera work and explicitly archive it without replaying effects."""

from __future__ import annotations

import argparse
import base64
import json
import ssl
import time
import urllib.request
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", help="photo ID already reviewed against the activity state")
    parser.add_argument("--config", type=Path, default=Path("/etc/lanternina/camera.json"))
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    credential = base64.b64encode(("family:" + config["family_password"]).encode()).decode()
    path = f"/photos/{args.archive}/archive" if args.archive else "/photos"
    request = urllib.request.Request(
        f"https://{config['hub_address']}:8443{path}",
        headers={"Authorization": "Basic " + credential},
        method="POST" if args.archive else "GET",
    )
    with urllib.request.urlopen(request, context=ssl.create_default_context(
        cafile=config["certificate"],
    ), timeout=30) as response:
        result = json.load(response)
    if not args.archive:
        result = [row for row in result if row["state"] in ("processing", "failed")]
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    began = time.monotonic()
    try:
        main()
    finally:
        print(f"elapsed: {time.monotonic() - began:.1f}s")