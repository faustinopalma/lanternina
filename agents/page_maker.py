"""Ask for the whole page, and nothing else. This module is one prompt.

Until 24 August 2026 this project composed the page itself: a layout per kind of object,
text set from strings, an illustration placed in a rectangle. The parent had already tried
the other way — one prompt, one image, the whole sheet — and liked the pages that came out,
so the composing is in `attic/` and what is left is the ask.

**What that costs, stated once and next to the claim.** Words drawn into pixels are screened
by Content Safety as an *image* and never as *words*: the gate looks at the picture, not at
what it says. That is the reason the composing existed, and it is the reason this file is
short — everything it can do about it is done here, by saying what the page may contain.
`ideas/10 §5` records the decision and who made it.

**The words are given, not invented.** The afternoon has already been written and screened
as text, so the ask quotes it and tells the model to letter exactly that. A model that
writes its own captions is a model writing to a person through a hole in the gate.

**Bytes in, bytes out, and Pillow rather than OpenCV.** This runs in the panel container,
which holds the credential that reaches the model and deliberately holds no vision stack:
the first version imported `cv2` and the deployed route answered 500 with
``No module named 'cv2'``. Nothing here needs an array — a PNG arrives, the paper is made
paper, and a PNG goes back to the house, which does have OpenCV and decodes it there.
"""

from __future__ import annotations

import base64
import io
from typing import Final

from PIL import Image

from shared.agents import AgentContext
from shared.ids import new_request_id
from shared.manner import Manner, a_manner
from shared.page import Page, PageKind, Room
from shared.prompts import beside
from shared.routing import Capability, ModelRequest
from shared.safety import ContentKind

# Portrait, and the closest the deployment comes to A4's 1:1.414. On A4 this lands at about
# 124 dpi across, which is coarse for small print and right for something drawn by hand.
SIZE: Final = "1024x1536"

# Everything at least this light is paper. Measured on 24 August 2026, on illustrations the
# real model returned: what looks like a white background is a faint even tone, and it was
# more than half the ink on the page. Flattening it took two pictures from 2.94 % to 1.38 %
# and from 2.54 % to 0.97 %. Between 245 and 220 the answer moves by 0.03 percentage points,
# so the number is a threshold and not a knob.
WHITE_AT: Final = 245

# Everything this module says to a model lives in `page_maker.*.md`, beside this file.
SAYS: Final = beside(__file__)

# What kind of object the paper is. One sentence each, and each one describes a thing that
# exists in the world rather than a style: a model given a genre draws the genre. Both of
# these are lettered into the middle of a sentence, so neither keeps a trailing newline.
_FOR_KIND: Final[dict[PageKind, str]] = {
    kind: SAYS.text(f"kind-{kind.value}").rstrip("\n") for kind in PageKind
}

_ROOM: Final[dict[Room, str]] = {
    room: SAYS.text(f"room-{room.value.replace('_', '-')}").rstrip("\n") for room in Room
}

_HOW_IT_IS_DRAWN: Final = SAYS.text("how-it-is-drawn")

_ONLY_THESE_WORDS: Final = SAYS.text("only-these-words").rstrip("\n")


def asked_for(page: Page, manner: Manner | None = None) -> str:
    """The whole ask, from the page's own words. Outside the class so a test can read it.

    ``manner`` says how it is drawn and never what it says, which is why it is safe to vary:
    the words come from the afternoon and are quoted below whatever the manner is. Without
    one, the same page asked for twice comes back twice the same — `shared/manner.py`.
    """
    lines = [_FOR_KIND[page.kind], ""]
    lines.append(f'Letter this large, as the title: "{page.title}"')
    if page.note:
        said = " ".join(page.note)
        lines.append(f'Letter this smaller, under the title: "{said}"')
    for space in page.spaces:
        room = _ROOM[space.room]
        lines.append(f'Leave {room}, with "{space.label}" lettered above it')
    lines.append("")
    lines.append(f"What the drawing on the page shows: {page.illustration}")
    if manner is not None:
        lines.append(manner.as_sentence())
    lines.append("")
    lines.append(_HOW_IT_IS_DRAWN)
    lines.append(_ONLY_THESE_WORDS)
    return "\n".join(lines)


class PageMaker:
    """One page, whole, drawn by the model and screened by the gate the router holds."""

    name = "page_maker"

    async def draw(self, ctx: AgentContext, page: Page) -> tuple[bytes, str]:
        """The page as a grey PNG and the request that produced it, or raise.

        The request comes back rather than being rebuilt by the caller: the manner is drawn
        here and at random, so asking again would describe a different page from the one on
        the paper. A parent reading a sheet that came out wrong needs the words that were
        actually sent, not a plausible reconstruction of them.

        The caller decides what a failure means. On this path it means the moment plays its
        ``instead``, which is written and screened long before anything broke.
        """
        drawn = a_manner()
        asked = asked_for(page, drawn)
        payload = await ctx.router.generate_for_user(
            ModelRequest(
                capability=Capability.IMAGE_GENERATION,
                prompt=asked,
                request_id=new_request_id(),
                purpose=f"drawing a {page.kind}",
                content_kind=ContentKind.IMAGE_PNG,
                metadata={"size": SIZE, "manner": drawn.to_dict()},
            )
        )
        return on_paper(base64.b64decode(payload.body)), asked


def on_paper(png: bytes) -> bytes:
    """A PNG as the sheet that will be printed, with the paper made paper.

    Two things happen and only the first is obvious. Colour goes, because the page prints in
    black and is measured by tone. And everything at least :data:`WHITE_AT` becomes white,
    because an image model's white is a faint even wash and on an inkjet that wash is ink
    spent on nothing. The dark lines are left exactly as they came.
    """
    try:
        drawn = Image.open(io.BytesIO(png))
    except OSError as exc:
        raise ValueError("the page that came back is not an image") from exc
    grey = drawn.convert("L").point(lambda tone: 255 if tone >= WHITE_AT else tone)
    out = io.BytesIO()
    grey.save(out, format="PNG")
    return out.getvalue()
