"""One-off: scan the sheet on the glass and print the ink fraction of every cell.

Says what the reader measured and what it concluded, side by side, so that a wrong answer
can be told apart from a wrong threshold. Nothing is written to disk.
"""

from __future__ import annotations

import sys
from pathlib import Path

from devices.print_sheet import recall
from devices.scan_sheet import find_scanner, scan_page
from shared.ids import SheetId
from vision.read_sheet import (
    INK_PRESENT,
    INK_UNCERTAIN,
    detect_markers,
    ink_fraction,
    page_ink_threshold,
    read_cells,
    read_qr,
    rectify,
)

sheets = Path(sys.argv[1])
page = scan_page(find_scanner("ET-2870"))
rectified = rectify(page, detect_markers(page))
payload = read_qr(rectified)
spec = recall(sheets, SheetId(str(payload.sheet_id)))
grey = page_ink_threshold(rectified)
print(f"sheet {spec.sheet_id} '{spec.title}'  grey threshold {grey}")
print(f"thresholds: present >= {INK_PRESENT}, doubtful >= {INK_UNCERTAIN}")
for cell in spec.cells:
    fraction = ink_fraction(rectified, cell.rect.to_pixels(), grey)
    print(f"  {cell.id:8s} {cell.label:12s} {fraction!r}")
reading = read_cells(rectified, spec)
print("reported marked:", [c.value for c in reading.cells if c.value])
print("reported doubtful:", [str(c.cell_id) for c in reading.cells if c.needs_review])
