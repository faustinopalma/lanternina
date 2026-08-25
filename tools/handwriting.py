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

import os
from typing import Final

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
    measured 24 August 2026, one soak of three where only one reached an ending. The waiting
    is the client's own, so it reads `Retry-After` rather than the sentence in the body.
    """
    import base64
    import io

    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    from openai import AzureOpenAI

    client = AzureOpenAI(
        azure_endpoint=os.environ["LANTERNINA_FOUNDRY_ACCOUNT_ENDPOINT"],
        api_version=os.environ.get(
            "LANTERNINA_FOUNDRY_IMAGE_API_VERSION", "2025-04-01-preview"
        ),
        azure_ad_token_provider=get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        ),
        timeout=TIMEOUT_SECONDS,
        max_retries=tries,
    )
    page = io.BytesIO(blank)
    # Named, because the service reads the format off the filename rather than the bytes.
    page.name = "page.png"
    answer = client.images.edit(
        model=os.environ["LANTERNINA_FOUNDRY_IMAGE_DEPLOYMENT"],
        image=page,
        prompt=asked_of(hand),
        n=1,
        size=size,
    )
    if not answer.data or not answer.data[0].b64_json:
        raise RuntimeError("the hand did not write: the model answered without a page")
    return base64.b64decode(answer.data[0].b64_json)

