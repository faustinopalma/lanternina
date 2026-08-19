"""Ask the panel to read a page, and fall back to arithmetic if it cannot be reached.

The model is the reader. The pixel counting in ``vision/read_sheet.py`` is what the house
says when the cloud is unreachable, and it says so: the reading comes back marked
``degraded``, which is the flag the rest of the system already understands.

That ordering is the whole point of this module. Before it, two constants decided whether
a box had a mark in it, and on 19 August 2026 they reported four ticked boxes as empty and
called it certain. Thresholds are the wrong instrument here: nobody in a house can tune
one, and the quantity they measure — what fraction of a rectangle is dark — is only
loosely related to the question, which is whether somebody put a mark in a box.

Stdlib plus OpenCV, which the hub already has. No credential lives here: the panel holds
the identity that reaches Foundry, and this sends a device key over TLS.
"""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request
from dataclasses import replace

import cv2
import numpy as np
from numpy.typing import NDArray

from shared.sheet import SheetSpec
from shared.vision_contracts import PageReading
from vision.read_sheet import read_cells

# A page is a few hundred kilobytes and the model takes seconds to look at it. Long enough
# that a slow answer is still an answer, short enough that the person who put the sheet on
# the glass is not left in front of a blank display.
READ_TIMEOUT_SECONDS = 90


class PanelUnreachable(RuntimeError):
    """The panel did not answer. Not a fault to show anybody: the house carries on."""


def read_page(
    rectified: NDArray[np.uint8],
    spec: SheetSpec,
    *,
    panel: str,
    household: str,
    key: str,
    timeout: int = READ_TIMEOUT_SECONDS,
) -> PageReading:
    """Read the page with the model, or locally and marked degraded if that fails."""
    try:
        return ask_panel(
            rectified, spec, panel=panel, household=household, key=key, timeout=timeout
        )
    except (PanelUnreachable, urllib.error.URLError, OSError, ValueError, KeyError):
        return replace(read_cells(rectified, spec), degraded=True)


def ask_panel(
    rectified: NDArray[np.uint8],
    spec: SheetSpec,
    *,
    panel: str,
    household: str,
    key: str,
    timeout: int = READ_TIMEOUT_SECONDS,
) -> PageReading:
    """Post the rectified crop and the sheet's own description of where its boxes are."""
    if not (panel and household and key):
        raise PanelUnreachable("no panel is configured")
    ok, encoded = cv2.imencode(".png", rectified)
    if not ok:
        raise ValueError("the rectified page could not be encoded")
    height, width = rectified.shape[:2]
    body = json.dumps(
        {
            "imageBase64": base64.b64encode(encoded.tobytes()).decode(),
            "width": int(width),
            "height": int(height),
            "sheet": spec.to_dict(),
        }
    ).encode()
    request = urllib.request.Request(
        f"{panel.rstrip('/')}/api/device/{household}/read-sheet",
        data=body,
        headers={"X-Device-Key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            answer = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        # The body says which of the several reasons it was. A message carrying only the
        # status leaves the next person to guess between a key, a quota and a model.
        detail = exc.read().decode("utf-8", "replace")[:300]
        raise PanelUnreachable(f"the panel refused: {exc.code} {detail}") from exc
    return PageReading.from_dict(answer)
