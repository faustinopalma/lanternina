"""Ask the real model for whole pages, and look at what comes out.

    python tools/probe_page.py                # one page of each kind
    python tools/probe_page.py --kind label

Needs the container app's environment, and it spends money: about four cents and twenty
seconds a page. What it answers is the only question that matters about the ask — whether a
page drawn from one prompt is a page somebody would pick up, spells its Italian, and does
not flood an inkjet.

The pages are invented and describe nobody.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import time
from pathlib import Path

import cv2

from printing.paper import ink_fraction, to_paper, to_pdf
from shared.page import Page, PageKind, Room, Space

PAGES = {
    PageKind.MAP: Page(
        kind=PageKind.MAP,
        title="Il cielo sopra questa casa",
        illustration="rooftops seen from above, with clouds drifting across them",
        note=("Il registro di quello che si è visto, tenuto da chi guarda fuori.",),
        spaces=(
            Space(label="Dove stava la prima", room=Room.A_LINE),
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
            Space(label="Che cosa faceva mentre la guardavi", room=Room.SOME_LINES),
        ),
    ),
    PageKind.LABEL: Page(
        kind=PageKind.LABEL,
        title="La nuvola che non c'era",
        illustration="one imaginary cloud, alone, seen from below",
        note=("Trovata da nessuno, sopra questa casa, il ventiquattro.",),
        spaces=(
            Space(label="Disegnala qui", room=Room.A_BOX),
            Space(label="Come si chiama", room=Room.A_LINE),
        ),
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
    from agents.page_maker import PageMaker
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
        drawn_png, _asked = await PageMaker().draw(context, page)
        seconds = time.monotonic() - began
    finally:
        await gate.aclose()

    import cv2 as _cv2
    import numpy as _np

    drawn = _np.asarray(
        _cv2.imdecode(_np.frombuffer(drawn_png, dtype=_np.uint8), _cv2.IMREAD_GRAYSCALE),
        dtype=_np.uint8,
    )
    sheet = to_paper(drawn)
    usage = router.last_usage
    print(
        f"{str(page.kind):9s} {seconds:5.1f} s  {drawn.shape[1]}x{drawn.shape[0]}"
        f"  ink {ink_fraction(sheet) * 100:5.2f}%"
        + (f"  {usage.output_tokens} output tokens" if usage else "")
    )
    print(f"    words it was told to letter: {' | '.join(page.words())}")
    cv2.imwrite(str(out / f"whole-{page.kind}.png"), sheet)
    (out / f"whole-{page.kind}.pdf").write_bytes(to_pdf(drawn))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=[str(k) for k in PageKind], default="")
    parser.add_argument("--out", default="build")
    asked = parser.parse_args()
    out = Path(asked.out)
    out.mkdir(parents=True, exist_ok=True)

    wanted = [PageKind(asked.kind)] if asked.kind else list(PageKind)
    for number, kind in enumerate(wanted):
        # The deployment is capacity 2 and answers 429 to a second call inside a minute.
        if number:
            time.sleep(40)
        asyncio.run(_once(PAGES[kind], out))
    print(f"\nwritten to {out.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
