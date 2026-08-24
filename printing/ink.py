"""How much ink a page spends, measured on the page rather than argued about.

"Ecological" is the only word in the brief that can be measured, and this is the
measurement. A page is ink on paper and ink runs out in a house, so a composed page is
rasterised and refused if it covers more of the paper than :data:`~shared.page.INK_BUDGET`
allows.

**Coverage by tone, not by dark pixel count.** An inkjet laying a mid-grey pixel spends
about half the ink of a black one, so the honest figure is the mean darkness of the sheet
and not the fraction of pixels below a threshold. For line art on white the two agree to
within antialiasing; for a photographic illustration they do not agree at all, and the
illustration is where the ink goes.

**A refusal is a complaint and not an exception**, the same shape the six checks in
`shared/experience_checks.py` use, so it can be handed back naming what failed.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from shared.experience_checks import Complaint
from shared.page import INK_BUDGET, Page

from .render import Drawing, drawing_to_array

# Enough to resolve a 0.3 mm rule — about 4 pixels — and cheap enough to run on every page.
# A4 at this density is 1240 x 1754, which is also the size the reader rectifies to.
MEASURE_DPI = 150


def ink_fraction(canvas: NDArray[np.uint8]) -> float:
    """The share of the paper covered, counting a grey pixel as the ink it actually is."""
    return float(np.mean(255.0 - canvas.astype(np.float64)) / 255.0)


def measure(drawing: Drawing) -> float:
    """Rasterise the page as it will print, words and all, and say what it costs."""
    return ink_fraction(drawing_to_array(drawing, dpi=MEASURE_DPI, text=True))


def check_ink(page: Page, drawing: Drawing, budget: float = INK_BUDGET) -> tuple[Complaint, ...]:
    """Nothing, or one complaint saying by how much.

    The number is in the message because a repair request that says "too much ink" leaves
    a model to guess whether it is twice too much or a percent over.
    """
    spent = measure(drawing)
    if spent <= budget:
        return ()
    return (
        Complaint(
            where=f"page[{page.kind}]",
            says=(
                f"this page covers {spent * 100:.2f}% of the paper in ink and the budget "
                f"is {budget * 100:.2f}%. Ask for less of it: a lighter picture, fewer "
                f"filled areas, or a smaller one."
            ),
        ),
    )
