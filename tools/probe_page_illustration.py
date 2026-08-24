"""Ask the real image model for one illustration per kind, and measure what it costs.

    python tools/probe_page_illustration.py            # all four kinds
    python tools/probe_page_illustration.py --kind map

Needs the container app's environment, and it spends money: four calls at roughly four
cents each. What it answers is the two things `ideas/10 §4` and `§5` leave measured only by
argument — whether a picture asked for as line art fits an ink budget, and whether a model
told four times not to write anything writes anything.

The pages are invented and describe nobody.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import time
from pathlib import Path

import cv2

from printing.ink import ink_fraction, measure
from printing.page_layout import compose
from printing.render import drawing_to_array, drawing_to_pdf
from shared.page import INK_BUDGET, Page, PageKind, Room, Space

PAGES = {
    PageKind.MAP: Page(
        kind=PageKind.MAP,
        title="Le nuvole sopra questa casa",
        illustration="the sky over a row of roofs, with three clouds of different shapes",
        note=("Segna dove stava ciascuna, e come si chiamava.",),
        spaces=(
            Space(label="La prima", room=Room.A_LINE),
            Space(label="Disegna quella che è durata di più", room=Room.A_BOX),
        ),
    ),
    PageKind.DOSSIER: Page(
        kind=PageKind.DOSSIER,
        title="Scheda: la nuvola alta",
        illustration="a single tall cumulus cloud, seen from below",
        note=("Vista dalla finestra di cucina, alle cinque del pomeriggio.",),
        spaces=(
            Space(label="Che forma aveva", room=Room.A_LINE),
            Space(label="Che cosa faceva", room=Room.SOME_LINES),
        ),
    ),
    PageKind.LABEL: Page(
        kind=PageKind.LABEL,
        title="Nuvola, senza nome",
        illustration="one cloud, alone",
        note=("Raccolta il ventiquattro agosto, sopra il cortile.",),
        spaces=(Space(label="Il nome che le dai", room=Room.A_LINE),),
    ),
    PageKind.NOTEBOOK: Page(
        kind=PageKind.NOTEBOOK,
        title="Taccuino del cielo",
        illustration="a quick sketch of clouds moving over a hill",
        note=("Una riga per ogni volta che guardi fuori.",),
        spaces=(Space(label="Che ora era, e che cosa vedevi", room=Room.SOME_LINES),),
    ),
}


async def _once(page: Page, out: Path) -> None:
    from agents.page_illustrator import PageIllustrator, asked_for
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig
    from shared.agents import AgentContext
    from shared.ids import LearnerId
    from shared.seal import Sealer, SealPurpose

    environment = dict(os.environ)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, b"k" * 32, "probe"),
    )
    router = FoundryRouter(FoundryConfig.from_env(environment), gate=gate)
    context = AgentContext(
        router=router, learner_id=LearnerId(""), learner_hints={}, now=time.time()
    )
    try:
        began = time.monotonic()
        picture = await PageIllustrator().draw(context, page)
        seconds = time.monotonic() - began
    finally:
        await gate.aclose()

    drawing = compose(page, picture)
    spent = measure(drawing)
    usage = router.last_usage
    print(
        f"{str(page.kind):9s} {seconds:5.1f} s  picture {ink_fraction(picture) * 100:5.2f}%"
        f"  page {spent * 100:5.2f}%  "
        f"{'within' if spent <= INK_BUDGET else 'REFUSED'}"
        + (f"  {usage.output_tokens} output tokens" if usage else "")
    )
    print(f"    asked: {asked_for(page).splitlines()[1]}")
    cv2.imwrite(str(out / f"illustration-{page.kind}.png"), picture)
    cv2.imwrite(
        str(out / f"illustrated-{page.kind}.png"), drawing_to_array(drawing, dpi=150, text=True)
    )
    (out / f"illustrated-{page.kind}.pdf").write_bytes(drawing_to_pdf(drawing))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=[str(k) for k in PageKind], default="")
    parser.add_argument("--out", default="build")
    asked = parser.parse_args()
    out = Path(asked.out)
    out.mkdir(parents=True, exist_ok=True)

    wanted = [PageKind(asked.kind)] if asked.kind else list(PageKind)
    print(f"budget {INK_BUDGET * 100:.2f}% of the paper\n")
    for number, kind in enumerate(wanted):
        # The deployment is capacity 2 and answers 429 to a second call inside a minute.
        if number:
            time.sleep(25)
        asyncio.run(_once(PAGES[kind], out))
    print(f"\nwritten to {out.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
