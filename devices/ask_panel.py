"""Ask the panel to draw a page, and to say what came back on one.

No credential lives here: the panel holds the identity that reaches Foundry, and this sends
a device key over TLS. Stdlib plus OpenCV, which the hub already has.

**No cloud, no page and no reading.** There is nothing underneath either of these. A page
that cannot be drawn means the moment plays its ``instead``, which was written and screened
when the afternoon was approved. A page that comes back while the panel is unreachable waits,
and nothing is said about it to anybody. That is a real loss and it is the trade `ideas/08`
records: keeping a local reading meant keeping the sheet a template of declared boxes.
"""

from __future__ import annotations

import base64
import json
import time
import urllib.error
import urllib.request

import cv2
import numpy as np
from numpy.typing import NDArray

from shared.vision_contracts import WhatCameBack

# Drawing a whole page took 18.8 to 24.1 s against the real deployment on 24 August 2026, and
# a reading 4.4 to 5.5 s. Long enough that a slow answer is still an answer, short enough that
# nobody is left standing in front of a display that says nothing.
DRAW_TIMEOUT_SECONDS = 180
READ_TIMEOUT_SECONDS = 90
# What the image deployment asks to be left alone for when it is over its rate: it says
# "retry after 17 seconds", and this is that with room.
BUSY_SECONDS = 25.0


class PanelUnreachable(RuntimeError):
    """The panel did not answer, so nothing is known and nothing is guessed."""


def _ask(
    url: str, body: dict[str, object], *, key: str, timeout: int
) -> dict[str, object]:
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
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
    if not isinstance(answer, dict):
        raise PanelUnreachable("the panel answered with something that is not an object")
    return answer


def draw_page(
    page: dict[str, object],
    *,
    panel: str,
    household: str,
    key: str,
    run_id: str = "",
    timeout: int = DRAW_TIMEOUT_SECONDS,
    tries: int = 2,
) -> NDArray[np.uint8]:
    """The page a model drew, as one grey image. Raises :class:`PanelUnreachable`.

    Tries again once when the cloud says it is busy, because that is a transient thing and
    the alternative is an afternoon that plays its ``instead`` for a reason that would have
    gone away in half a minute. It does not try again for anything else: a refusal, a bad
    key and a page the format would not take are all answers, and repeating them costs money.
    """
    if not (panel and household and key):
        raise PanelUnreachable("no panel is configured")
    for attempt in range(1, tries + 1):
        try:
            answer = _ask(
                f"{panel.rstrip('/')}/api/device/{household}/page",
                {"page": page, "runId": run_id},
                key=key,
                timeout=timeout,
            )
        except PanelUnreachable as exc:
            if attempt < tries and _busy(str(exc)):
                time.sleep(BUSY_SECONDS)
                continue
            raise
        break
    encoded = answer.get("imageBase64")
    if not isinstance(encoded, str) or not encoded:
        raise PanelUnreachable("the panel answered without a page")
    drawn = cv2.imdecode(
        np.frombuffer(base64.b64decode(encoded), dtype=np.uint8), cv2.IMREAD_GRAYSCALE
    )
    if drawn is None:
        raise PanelUnreachable("what the panel sent is not an image")
    return np.asarray(drawn, dtype=np.uint8)


def _busy(said: str) -> bool:
    """Whether the cloud said it was over its rate, rather than saying no."""
    return "429" in said or "RateLimitReached" in said


def read_page(
    blank: NDArray[np.uint8],
    came_back: NDArray[np.uint8],
    *,
    about: str,
    panel: str,
    household: str,
    key: str,
    timeout: int = READ_TIMEOUT_SECONDS,
) -> WhatCameBack:
    """What is on the sheet that was not on the blank.

    Both images go, in that order. There is no spec and no list of boxes: what the page was
    for is one sentence of context, and the answer describes ink.
    """
    if not (panel and household and key):
        raise PanelUnreachable("no panel is configured")
    height, width = came_back.shape[:2]
    answer = _ask(
        f"{panel.rstrip('/')}/api/device/{household}/read-page",
        {
            "blankBase64": _png(blank),
            "cameBackBase64": _png(came_back),
            "width": int(width),
            "height": int(height),
            "about": about,
        },
        key=key,
        timeout=timeout,
    )
    try:
        return WhatCameBack.from_dict(answer)
    except (ValueError, KeyError, TypeError) as exc:
        # An answer that cannot be read is not a reading. Salvaging part of one produces a
        # sentence about a page nobody looked at.
        raise PanelUnreachable(f"the panel answered something unreadable: {exc}") from exc


def _png(image: NDArray[np.uint8]) -> str:
    ok, encoded = cv2.imencode(".png", image)
    if not ok:
        raise ValueError("the page could not be encoded")
    return base64.b64encode(encoded.tobytes()).decode()
