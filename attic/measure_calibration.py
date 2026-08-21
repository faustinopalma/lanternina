"""Measure the calibration sheet and say what the thresholds should be.

Retired 21 August 2026 with the arithmetic it measures. Run from the repository root as
`python attic/measure_calibration.py`.

Run it with the sheet on the glass. It scans once, reads every declared box, and prints
three groups: what an untouched box measures, what a printed area of known size measures,
and what a hand-made mark measures. The gap between the last two groups and the first is
the only thing that decides a threshold, and this is the only way to see it.

Nothing is changed by running this. The numbers come out; the decision stays with a person
looking at them, because one sheet is one sample and a threshold set from it would be a
guess wearing a measurement's clothes.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ink_arithmetic import (  # noqa: E402
    INK_PRESENT,
    INK_UNCERTAIN,
    ink_fraction,
    page_ink_threshold,
)

from devices.print_sheet import recall  # noqa: E402
from devices.scan_sheet import find_scanner, scan_page  # noqa: E402
from shared.ids import SheetId  # noqa: E402
from vision.read_sheet import detect_markers, rectify  # noqa: E402


def verdict(fraction: float) -> str:
    if fraction >= INK_PRESENT:
        return "segno"
    return "incerta" if fraction >= INK_UNCERTAIN else "vuota"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scanner", default="ET-2870")
    parser.add_argument("--sheets", type=Path, default=Path("/var/lib/lanternina/state/sheets"))
    parser.add_argument("--sheet-id", default="sh_taratura")
    args = parser.parse_args()

    page = scan_page(find_scanner(args.scanner))
    flat = rectify(page, detect_markers(page))
    spec = recall(args.sheets, SheetId(args.sheet_id))
    threshold = page_ink_threshold(flat)

    print(f"soglia di grigio sulla pagina: {threshold}")
    print(f"attuali: vuota < {INK_UNCERTAIN}   incerta < {INK_PRESENT} <= segno\n")

    groups: dict[str, list[tuple[str, str, float]]] = {"vuote": [], "stampate": [], "a mano": []}
    for cell in spec.cells:
        fraction = ink_fraction(flat, cell.rect.to_pixels(), threshold)
        if fraction is None:
            continue
        name = str(cell.id)
        where = (
            "vuote"
            if name.startswith("vuota")
            else "stampate"
            if name.startswith("stampata")
            else "a mano"
        )
        groups[where].append((name, cell.label, fraction))

    for where, rows in groups.items():
        print(f"— {where} —")
        for name, label, fraction in rows:
            print(f"  {name:14s} {label:26s} {fraction:.4f}  {verdict(fraction)}")
        if rows:
            values = [row[2] for row in rows]
            print(f"  {'':14s} {'':26s} min {min(values):.4f}  max {max(values):.4f}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
