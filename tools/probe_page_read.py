"""Does the new reading work against the real service? Ask it, do not assume.

`ideas/10 §3`. `tests/test_page_reader.py` holds the refusals against a stub; a stub cannot
say whether a vision model, given a blank page and the same page written on, reports what was
added without saying anything about the person who added it. That is the question, and this
project has been caught before by tests that passed against a fake model while three defects
waited in the real one.

    python tools/probe_page_read.py

It needs the endpoints of the real account and a signed-in identity with the data-plane
roles, the same as `tools/probe_devise.py`. It stores nothing except two PNGs under `build/`
so the pages it asked about can be looked at afterwards.

Prints what the model said for three cases: a page written on, the same page untouched, and a
different page altogether. What has to be true is that the first is described, the second is
reported as empty rather than invented, and the third is reported as a different sheet without
that becoming a complaint.
"""

from __future__ import annotations

import asyncio
import io
import os
from pathlib import Path

from PIL import Image, ImageDraw
from printing.render import PageGeometry, build_drawing, drawing_to_array
from shared.sheet import CellKind, CellSpec, Rect, SheetSpec

from agents.page_reader import PageReader
from shared.agents import AgentContext
from shared.ids import CellId, ExerciseId, LearnerId, SheetId
from shared.routing import PageImage


def a_sheet(name: str, boxes: list[tuple[float, float, float, float]]) -> SheetSpec:
    return SheetSpec(
        sheet_id=SheetId(f"sh_{name}"),
        exercise_id=ExerciseId(f"ex_{name}"),
        title=f"Foglio {name}",
        qr_rect=Rect(x=0.86, y=0.92, w=0.1, h=0.06),
        cells=tuple(
            CellSpec(
                id=CellId(f"c{index}"),
                kind=CellKind.DRAWING_AREA,
                rect=Rect(x=x, y=y, w=w, h=h),
            )
            for index, (x, y, w, h) in enumerate(boxes)
        ),
    )


def rendered(spec: SheetSpec) -> Image.Image:
    array = drawing_to_array(build_drawing(spec, PageGeometry()), dpi=150, text=True)
    return Image.fromarray(array).convert("L")


def written_on(page: Image.Image) -> Image.Image:
    """A house in the left box and a few words on the right, drawn badly on purpose: what
    the reader has to cope with is handwriting, not a font."""
    filled = page.copy()
    pen = ImageDraw.Draw(filled)
    width, height = filled.size
    x, y = 0.18 * width, 0.28 * height
    pen.polygon([(x, y + 90), (x + 70, y), (x + 140, y + 90)], outline=0, width=4)
    pen.rectangle([x + 20, y + 90, x + 120, y + 190], outline=0, width=4)
    pen.rectangle([x + 55, y + 140, x + 85, y + 190], outline=0, width=3)
    for line in range(3):
        top = 0.22 * height + line * 34
        pen.line([(0.6 * width, top), (0.6 * width + 190, top)], fill=0, width=5)
    return filled


def as_page(page: Image.Image) -> PageImage:
    buffer = io.BytesIO()
    page.convert("RGB").save(buffer, format="PNG")
    return PageImage(png=buffer.getvalue(), width=page.width, height=page.height)


async def main() -> int:
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig
    from shared.seal import Sealer, SealPurpose

    boxes = [(0.12, 0.2, 0.32, 0.3), (0.55, 0.18, 0.33, 0.22)]
    blank = rendered(a_sheet("mappa", boxes))
    other = rendered(a_sheet("elenco", [(0.15, 0.12, 0.7, 0.6)]))
    filled = written_on(blank)

    Path("build").mkdir(exist_ok=True)
    blank.save("build/probe-page-blank.png")
    filled.save("build/probe-page-filled.png")

    environment = dict(os.environ)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, b"k" * 32, "probe"),
    )
    router = FoundryRouter(FoundryConfig.from_env(environment), gate=gate)
    ctx = AgentContext(router=router, learner_id=LearnerId(""), learner_hints={}, now=0.0)
    reader = PageReader()

    cases = {
        "scritta sopra": (blank, filled),
        "mai toccata": (blank, blank),
        "un altro foglio": (blank, other),
    }
    for label, (first, second) in cases.items():
        came = await reader.read(
            ctx,
            blank=as_page(first),
            came_back=as_page(second),
            about="disegna qualcosa nel riquadro a sinistra e scrivi nelle righe a destra",
        )
        print(f"\n-- {label} --")
        print(f"  scritto: {came.written} | stesso foglio: {came.same_sheet}")
        print(f"  degradato: {came.degraded} | {came.metadata.get('latency_s')} s")
        for line in came.describes:
            print(f"    - {line}")
        if not came.describes:
            print("    (niente da descrivere)")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
