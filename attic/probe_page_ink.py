"""Print one page of each kind and say what it costs in ink.

Run it to see the four layouts and the numbers behind `ideas/10 §4`:

    python tools/probe_page_ink.py            # writes build/page-<kind>.pdf and .png
    python tools/probe_page_ink.py --grey 128 # with a flat mid-grey standing in for a picture

The words are invented and describe nothing about anybody. The picture is a synthetic
gradient rather than a model call: what is being measured here is the layout and the
arithmetic, and a real illustration is measured when one exists.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np
from numpy.typing import NDArray

from printing.ink import MEASURE_DPI, measure
from printing.page_layout import compose
from printing.render import drawing_to_array, drawing_to_pdf
from shared.page import INK_BUDGET, Page, PageKind

PAGES = {
    PageKind.MAP: Page(
        kind=PageKind.MAP,
        title="Le nuvole sopra questa casa",
        illustration="a hand-drawn map of a sky with three cloud shapes over rooftops",
        note=("Segna dove stava ciascuna, e come si chiamava.",),
        spaces=(),
    ),
    PageKind.DOSSIER: Page(
        kind=PageKind.DOSSIER,
        title="Scheda: la nuvola alta",
        illustration="a pen-and-ink study of a single cumulus cloud",
        note=(
            "Una nuvola vista dalla finestra di cucina, alle cinque del pomeriggio.",
            "Quello che si sa di lei sta qui sotto.",
        ),
        spaces=(),
    ),
    PageKind.LABEL: Page(
        kind=PageKind.LABEL,
        title="Nuvola, senza nome",
        illustration="a single cloud, centred, line art on white",
        note=("Raccolta il ventiquattro agosto, sopra il cortile.",),
        spaces=(),
    ),
    PageKind.NOTEBOOK: Page(
        kind=PageKind.NOTEBOOK,
        title="Taccuino del cielo",
        illustration="a small sketch of clouds in the corner of a notebook page",
        note=("Una riga per ogni volta che guardi fuori.",),
        spaces=(),
    ),
}


def spaces_for(page: Page) -> Page:
    from shared.page import Room, Space

    return Page(
        kind=page.kind,
        title=page.title,
        illustration=page.illustration,
        note=page.note,
        spaces=(
            Space(label="Che forma aveva", room=Room.A_LINE),
            Space(label="Disegnala", room=Room.A_BOX),
            Space(label="Che cosa faceva", room=Room.SOME_LINES),
        ),
    )


def a_picture(kind: str, side: int = 768) -> NDArray[np.uint8]:
    """A stand-in with a known cost: a radial gradient, light at the edges."""
    grid = np.linspace(-1.0, 1.0, side, dtype=np.float64)
    x, y = np.meshgrid(grid, grid)
    radius = np.sqrt(x * x + y * y)
    if kind == "flat":
        return np.full((side, side), 128, dtype=np.uint8)
    return np.clip(255 - 160 * np.clip(1.2 - radius, 0.0, 1.0), 0, 255).astype(np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="build", help="where the pages are written")
    parser.add_argument(
        "--picture", choices=("none", "gradient", "flat"), default="gradient"
    )
    asked = parser.parse_args()
    out = Path(asked.out)
    out.mkdir(parents=True, exist_ok=True)

    print(f"budget {INK_BUDGET * 100:.2f}% of the paper, measured at {MEASURE_DPI} dpi\n")
    print(f"{'kind':10} {'words only':>12} {'with picture':>14}  verdict")
    for kind, plain in PAGES.items():
        page = spaces_for(plain)
        bare = compose(page, None)
        picture = None if asked.picture == "none" else a_picture(asked.picture)
        full = compose(page, picture)
        with_picture = measure(full)
        verdict = "within" if with_picture <= INK_BUDGET else "REFUSED"
        print(
            f"{str(kind):10} {measure(bare) * 100:11.2f}% {with_picture * 100:13.2f}%  {verdict}"
        )
        (out / f"page-{kind}.pdf").write_bytes(drawing_to_pdf(full))
        cv2.imwrite(
            str(out / f"page-{kind}.png"), drawing_to_array(full, dpi=150, text=True)
        )
    print(f"\nwritten to {out.resolve()}")


if __name__ == "__main__":
    main()
