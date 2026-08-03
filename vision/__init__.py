"""Vision — single-shot capture, ArUco detection, rectification, QR decode, cell reading.

Two constraints shape this whole package:

1. **Only the rectified region inside the marker quadrilateral is ever retained.** The
   full frame lives in a :class:`shared.vision_contracts.RawFrame`, which cannot be
   pickled, copied or written out. Nothing in this package accepts a ``RawFrame`` and
   returns bytes except the rectifier, and it returns only the crop.
2. **Capture is single-shot, on a button press.** There is no streaming endpoint, no
   timer loop and no motion trigger in this package, and none may be added — see
   docs/NON-GOALS.md.

This package does no face detection, no person detection and no emotion inference. It
looks for four printed markers and a QR code.
"""
