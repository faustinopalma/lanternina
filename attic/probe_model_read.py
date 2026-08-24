"""One-off: scan the glass and have the panel's vision model read it.

Until 21 August 2026 this printed two readings side by side, the model's and the local
arithmetic's, which was the only way to tell an improvement from a coincidence. The
arithmetic is in `attic/` and there is one reading now; a panel that does not answer
raises here rather than becoming a quieter answer.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

from devices.print_sheet import recall
from devices.read_page import read_page
from devices.scan_sheet import find_scanner, scan_page
from vision.read_sheet import detect_markers, read_qr, rectify

sheets = Path(sys.argv[1])
panel = os.environ.get("LANTERNINA_PANEL_URL", "")
household = os.environ.get("LANTERNINA_HOUSEHOLD", "")
key = os.environ.get("LANTERNINA_DEVICE_KEY", "")

started = time.time()
page = scan_page(find_scanner("ET-2870"))
rectified = rectify(page, detect_markers(page))
spec = recall(sheets, read_qr(rectified).sheet_id)
print(f"scanned and rectified in {time.time() - started:.1f} s: {spec.sheet_id}")

asked = time.time()
remote = read_page(rectified, spec, panel=panel, household=household, key=key)
print(f"model       : {[c.value for c in remote.cells if c.value] or 'nothing'}")
print(f"  doubtful  : {[str(c.cell_id) for c in remote.cells if c.needs_review]}")
print(f"  took      : {time.time() - asked:.1f} s   metadata {remote.metadata}")
