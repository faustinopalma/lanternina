"""One-off: ask the real model to design a sheet, and print what it made and what it cost.

The format was filled by hand before this was written, so what is being tested here is not
whether a page can be drawn but whether a model can fill a closed vocabulary well enough to
be worth the trip: whether the JSON parses, whether the marks validate, whether the ink
budget holds, and whether what comes out looks like a sheet somebody would hand to an
adolescent.

Every attempt is written to build/ as a PNG, because the numbers do not say whether it is
any good and only looking does.

    $env:LANTERNINA_FOUNDRY_ENDPOINT=...        # and ACCOUNT_ENDPOINT, DEPLOYMENT
    $env:LANTERNINA_CONTENT_SAFETY_ENDPOINT=...
    python tools/probe_sheet_design.py

The credential is whatever ``DefaultAzureCredential`` finds, which on a development
machine is the Azure CLI login.
"""

from __future__ import annotations

import asyncio
import json
import pathlib
import time

import cv2

from panel.designing import design_sheet
from printing.compose import InkTooHeavy, compose
from printing.render import PageGeometry, drawing_to_array
from shared.ids import ExerciseId, SheetId

# Synthetic, and the kind of thing a parent would actually ask for.
TOPICS = [
    "le tabelline del 6 e del 7",
    "i nomi delle nuvole",
    "mettere in ordine i fatti di una giornata",
]

HINTS: dict[str, object] = {
    "language": "it",
    "interests": ["gatti", "vele"],
    "avoid": ["tempeste"],
    "max_words_per_line": 6,
}

OUT = pathlib.Path("build")


async def main() -> None:
    page = PageGeometry()
    quad = page.quad
    print(f"frame {quad.w:.0f} x {quad.h:.0f} mm\n")

    for index, topic in enumerate(TOPICS, start=1):
        print(f"{index}. {topic}")
        started = time.monotonic()
        try:
            _, design, spent = await design_sheet(
                topic, hints=HINTS, now=time.time(), quad_w_mm=quad.w, quad_h_mm=quad.h
            )
        except Exception as exc:  # noqa: BLE001 - a probe reports, it does not raise
            took = time.monotonic() - started
            print(f"   refused after {took:.1f} s: {type(exc).__name__}: {exc}\n")
            continue
        took = time.monotonic() - started

        kinds: dict[str, int] = {}
        for mark in design.marks:
            kinds[mark.mark] = kinds.get(mark.mark, 0) + 1
        print(f"   {design.title!r} / {design.instructions!r}")
        print(f"   marks {len(design.marks)}: {kinds}")

        try:
            sheet = compose(
                design,
                sheet_id=SheetId(f"sh_probe{index:04d}"),
                exercise_id=ExerciseId(f"ex_probe{index:04d}"),
                page=page,
            )
        except (InkTooHeavy, ValueError) as exc:
            print(f"   cannot be laid out: {type(exc).__name__}: {exc}\n")
            continue

        out = OUT / f"design-{index}.png"
        cv2.imwrite(str(out), drawing_to_array(sheet.drawing, dpi=110, text=True))
        # The design beside the picture, so trying a layout change again costs nothing.
        (OUT / f"design-{index}.json").write_text(
            json.dumps(design.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(
            f"   ink {sheet.stroke_ink_mm2:.0f} mm² of strokes, "
            f"{sheet.coverage:.3%} of the page measured ({sheet.ink_mm2:.0f} mm²)"
        )
        print(f"   answerable: {[str(c.id) for c in sheet.spec.cells]}")
        print(f"   took {took:.1f} s -> {out}")
        if spent is None:
            print("   the backend reported no usage\n")
        else:
            print(
                f"   in {spent.input_tokens} (cached {spent.cached_input_tokens}) "
                f"out {spent.output_tokens} (reasoning {spent.reasoning_tokens})\n"
            )


asyncio.run(main())
