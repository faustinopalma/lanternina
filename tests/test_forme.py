"""Il contratto delle voci in `forme/` vale anche quando nessuno lo guarda."""

from __future__ import annotations

from tools.forme_check import WHERE, check


def test_ogni_voce_rispetta_il_contratto() -> None:
    """Sezioni, campi dell'intestazione e rimandi con il nome accanto.

    Le voci sono scritte in sessioni diverse e da chi non ha letto le altre: senza un
    controllo che gira, la seconda meta' dell'enciclopedia non somiglia alla prima.
    """
    wrong = [one for page in sorted(WHERE.rglob("*/README.md")) for one in check(page)]
    assert not wrong, "\n".join(wrong)
