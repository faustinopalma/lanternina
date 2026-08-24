"""The person who is not there, writing on the page.

`devices/pretend.py` is the house without the person: everything real except the hand that
fills the sheet. Until now that hand drew three polylines in three bands of the paper, which
is enough to answer "is there ink" and nothing like enough to answer "what did somebody
write". So the reading — the one part of an afternoon that is a model looking at handwriting
— was being exercised against scribble.

This asks the image model to fill the sheet in: **the same page, written on by a teenager in
blue ballpoint**. It is `images/edits` rather than `images/generations`, so what comes back is
the printed page with handwriting added rather than a new page that resembles it.

**It lives in `tools/` and not in the product.** Nothing here can reach a person: what it
writes goes onto a simulated sheet, is read by the reader, and is deleted with the run. Giving
the panel a route that writes on paper would be giving a model a way to put its own words in
front of somebody, which is the hole `ideas/10 §5` is about.

Measured 24 August 2026: 37.4 s for the first page, and what came back was
*è tipo una macchia di fumo che cambia sempre forma. non si vede bene ma c'è lo stesso*, with
a scribbled cloud in the box and *Nuvola fantasma* on the line — untidy, slanted, Italian, and
the printed page underneath untouched.
"""

from __future__ import annotations

import base64
import os
import re
import time
from typing import Final

import httpx

# What a hand is told to be. Deliberately not "neat": a page a model writes beautifully is a
# page the reader has an easy time with, and the point of this is that it should not.
_HANDS: Final[dict[str, str]] = {
    "teenager": (
        "filled in by a teenager with a blue ballpoint pen: untidy, slanted, not always on "
        "the line, a word crossed out somewhere"
    ),
    "careful": (
        "filled in carefully in pencil, small and even, the way somebody writes when they "
        "mind about it"
    ),
    "hurried": (
        "filled in fast in biro, large and loose, some words trailing off, one box left "
        "half done"
    ),
    "drawing": (
        "filled in mostly by drawing rather than writing: pencil sketches in the spaces, "
        "and only a word or two where a line asks for one"
    ),
}

HANDS: Final[tuple[str, ...]] = tuple(_HANDS)

# What it writes about. Left as one sentence because the page already says what it asks for,
# and a hand told too much stops being somebody answering and starts being somebody reciting.
_WHAT_TO_WRITE: Final = (
    "Answer what the page asks, in Italian, briefly and in your own words — the way somebody "
    "of thirteen would, not the way a form would. Where there is a box to draw in, draw "
    "something rough."
)

_KEEP_THE_PAGE: Final = (
    "Change nothing that is already printed on the page: not the title, not the lines, not "
    "the drawing. Add only what a person would have added, and leave the paper the same size."
)

TIMEOUT_SECONDS: Final = 300


def asked_of(hand: str) -> str:
    """The prompt, so a test can read it without paying for a page."""
    if hand not in _HANDS:
        raise ValueError(f"{hand!r} is not a hand; there is {', '.join(_HANDS)}")
    return (
        f"The same sheet of paper, now {_HANDS[hand]}.\n{_WHAT_TO_WRITE}\n{_KEEP_THE_PAGE}"
    )


def written_on(
    blank: bytes, *, hand: str = "teenager", size: str = "1024x1536", tries: int = 4
) -> bytes:
    """The sheet with somebody's writing on it, as PNG bytes.

    Talks to the account endpoint directly rather than through `orchestrator.router`: this is
    a capability only the simulator has, and putting it in the router would put "write on a
    page" one import away from the code that serves a house.

    Waits out a busy model rather than giving up. The deployment is capacity 2 and the region
    is at its ceiling, so an unattended run of several afternoons meets 429 every time —
    measured 24 August 2026, one soak of three where only one reached an ending.
    """
    from azure.identity import DefaultAzureCredential

    endpoint = os.environ["LANTERNINA_FOUNDRY_ACCOUNT_ENDPOINT"].rstrip("/")
    deployment = os.environ["LANTERNINA_FOUNDRY_IMAGE_DEPLOYMENT"]
    version = os.environ.get("LANTERNINA_FOUNDRY_IMAGE_API_VERSION", "2025-04-01-preview")
    token = (
        DefaultAzureCredential()
        .get_token("https://cognitiveservices.azure.com/.default")
        .token
    )
    for attempt in range(1, tries + 1):
        answer = httpx.post(
            f"{endpoint}/openai/deployments/{deployment}/images/edits?api-version={version}",
            headers={"Authorization": f"Bearer {token}"},
            files={"image": ("page.png", blank, "image/png")},
            data={"prompt": asked_of(hand), "n": "1", "size": size},
            timeout=TIMEOUT_SECONDS,
        )
        if answer.status_code == 200:
            return base64.b64decode(answer.json()["data"][0]["b64_json"])
        if answer.status_code == 429 and attempt < tries:
            time.sleep(retry_after(answer.text))
            continue
        # The body says which of the reasons it was; a status alone leaves the next person
        # guessing between a quota, a key and a refusal.
        raise RuntimeError(f"the hand did not write: {answer.status_code} {answer.text[:300]}")
    raise RuntimeError("the hand did not write: the model stayed busy")


def retry_after(said: str, floor: float = 20.0) -> float:
    """How long the service asked to be left alone, plus a little. Its own number when it
    gives one, because guessing shorter is how a retry becomes a second refusal."""
    found = re.search(r"retry after (\d+) second", said, re.IGNORECASE)
    return max(floor, float(found.group(1)) + 5.0 if found else floor)
