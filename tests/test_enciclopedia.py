"""Il contratto delle voci in `enciclopedia/` vale anche quando nessuno lo guarda."""

from __future__ import annotations

from tools.enciclopedia_check import WHERE, check


def test_ogni_voce_rispetta_il_contratto() -> None:
    """Sezioni, campi dell'intestazione, rimandi col nome accanto, niente di irraggiungibile.

    Le voci sono state scritte in sessioni diverse e da chi non aveva letto le altre: senza
    un controllo che gira, la seconda meta' dell'enciclopedia non somiglia alla prima.
    """
    pages = sorted(WHERE.rglob("*/README.md"))
    assert pages, f"nessuna voce sotto {WHERE}: il test passerebbe su niente"
    wrong = [one for page in pages for one in check(page)]
    assert not wrong, "\n".join(wrong)
