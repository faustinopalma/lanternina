"""One-off: post a sheet to the panel's reading route without scanning anything.

The image is not a page, so the answer is never a reading. What it is for is the other
half: whether the route, the credential and the model deployment are wired up at all,
which a 37-second scan should not have to be spent discovering.
"""

from __future__ import annotations

import base64
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

spec = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
panel = os.environ["LANTERNINA_PANEL_URL"].rstrip("/")
household = os.environ["LANTERNINA_HOUSEHOLD"]

body = json.dumps(
    {
        "imageBase64": base64.b64encode(b"not a page").decode(),
        "width": 10,
        "height": 10,
        "sheet": spec,
    }
).encode()
request = urllib.request.Request(
    f"{panel}/api/device/{household}/read-sheet",
    data=body,
    headers={
        "X-Device-Key": os.environ["LANTERNINA_DEVICE_KEY"],
        "Content-Type": "application/json",
    },
    method="POST",
)
try:
    with urllib.request.urlopen(request, timeout=90) as response:
        print(response.status, response.read().decode()[:600])
except urllib.error.HTTPError as exc:
    print(exc.code, exc.read().decode()[:600])
