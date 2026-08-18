#!/bin/sh
set -eu

base_url=${1:-http://127.0.0.1:8080}
registry=/etc/lanternina/trmnl-devices.json

python3 - "$base_url" "$registry" <<'PY'
import json
import struct
import sys
import urllib.request

base_url, registry_path = sys.argv[1:]
devices = json.load(open(registry_path, encoding="utf-8")).get("devices", {})
if not devices:
    with urllib.request.urlopen(f"{base_url}/health") as response:
        print(f"health={response.status} devices=0")
    raise SystemExit

mac, values = next(iter(devices.items()))
token = values["token"]

def fetch(path, headers=None):
    request = urllib.request.Request(f"{base_url}{path}", headers=headers or {})
    with urllib.request.urlopen(request) as response:
        return response.status, response.read()

setup_status, setup_body = fetch("/api/setup", {"ID": mac})
display_status, display_body = fetch(
    "/api/display", {"ID": mac, "Access-Token": token}
)
screen_status, bitmap = fetch(f"/screen/{token}.bmp")
setup = json.loads(setup_body)
display = json.loads(display_body)
print(
    f"http setup={setup_status} display={display_status} screen={screen_status} "
    f"token_present={bool(setup.get('api_key'))}"
)
print(
    f"display_status={display.get('status')} refresh_rate={display.get('refresh_rate')} "
    f"ota={display.get('update_firmware')}"
)
print(
    f"bmp_bytes={len(bitmap)} width={struct.unpack_from('<i', bitmap, 18)[0]} "
    f"height={abs(struct.unpack_from('<i', bitmap, 22)[0])} "
    f"bpp={struct.unpack_from('<H', bitmap, 28)[0]}"
)
PY