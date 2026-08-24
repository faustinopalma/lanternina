"""One-off: scan the glass, rectify, and say why the code did or did not decode.

Writes only the rectified crop, which is the one image this system may keep, and only to
a temporary path the caller names. Delete it when the question is answered.
"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2

from devices.scan_sheet import find_scanner, scan_page
from shared.sheet import RECTIFIED_HEIGHT, RECTIFIED_WIDTH
from vision.read_sheet import detect_markers, rectify

out = Path(sys.argv[1])
page = scan_page(find_scanner("ET-2870"))
print("scan", page.shape)
found = detect_markers(page)
print("markers", sorted(found))
rectified = rectify(page, found)
print("rectified", rectified.shape)
cv2.imwrite(str(out), rectified)

raw, points, _ = cv2.QRCodeDetector().detectAndDecode(rectified)
print("whole page ->", repr(raw), "points", None if points is None else points.tolist())

# The declared rectangle, plus a generous margin, in case the search is losing it in a
# page that is mostly white.
x0 = int(0.70 * RECTIFIED_WIDTH)
y0 = 0
x1 = RECTIFIED_WIDTH
y1 = int(0.22 * RECTIFIED_HEIGHT)
crop = rectified[y0:y1, x0:x1]
cv2.imwrite(str(out.with_name(out.stem + "-corner.png")), crop)
raw2, _, _ = cv2.QRCodeDetector().detectAndDecode(crop)
print("corner ->", repr(raw2), "crop", crop.shape)

for scale in (2, 3):
    bigger = cv2.resize(crop, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    raw3, _, _ = cv2.QRCodeDetector().detectAndDecode(bigger)
    print(f"corner x{scale} ->", repr(raw3))
