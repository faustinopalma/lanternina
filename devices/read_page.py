"""Ask the panel to read a page. If it cannot be reached, the page is not read.

The model is the reader, and until 21 August 2026 there was a second one underneath: the
pixel counting in `vision/read_sheet.py`, used when the cloud was unreachable and marked
``degraded``. It is in `attic/` now, and what replaces it is a sentence rather than a
mechanism — **no cloud, no reading**. A page that comes back while the panel is
unreachable waits, and nothing is said about it to anybody.

That is a real loss and it is the point of the trade. The arithmetic kept the paper path
alive with no network at all, and it bought that by making a sheet a form: the only pages
it can read are pages made of boxes in declared places. A page a model designs is not that
shape, so keeping the fallback would have meant keeping the template that fed it.

Stdlib plus OpenCV, which the hub already has. No credential lives here: the panel holds
the identity that reaches Foundry, and this sends a device key over TLS.
"""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request

import cv2
import numpy as np
from numpy.typing import NDArray

from shared.sheet import SheetSpec
from shared.vision_contracts import PageReading

# A page is a few hundred kilobytes and the model takes seconds to look at it. Long enough
# that a slow answer is still an answer, short enough that the person who put the sheet on
# the glass is not left in front of a blank display.
READ_TIMEOUT_SECONDS = 90


class PanelUnreachable(RuntimeError):
    """The panel did not answer, so nobody knows what is on the page and nobody guesses."""


def read_page(
    rectified: NDArray[np.uint8],
    spec: SheetSpec,
    *,
    panel: str,
    household: str,
    key: str,
    timeout: int = READ_TIMEOUT_SECONDS,
) -> PageReading:
    """Post the rectified crop and the sheet's own description of where its boxes are.

    Raises :class:`PanelUnreachable` for anything that stops an answer arriving. The
    caller decides what to put on a display; it does not get a reading either way.
    """
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
    except (OSError, ValueError) as exc:
        # `URLError` is an `OSError`, so naming it here as well would say nothing.
        raise PanelUnreachable(f"the panel did not answer: {exc}") from exc
    try:
        return PageReading.from_dict(answer)
    except (ValueError, KeyError, TypeError) as exc:
        # An answer that cannot be read is not a reading. Salvaging part of one produces
        # something that looks whole by the time it reaches a display.
        raise PanelUnreachable(f"the panel's answer was not a reading: {exc}") from exc
