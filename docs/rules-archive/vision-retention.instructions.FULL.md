---
name: 'Vision — capture and retention' description: 'Retention and capture rules for the vision pipeline: single-shot only, rectified crop only, no person detection.' applyTo: 'vision/**'
---

# Vision package rules

The camera in this system is a **scanner pointed at a sheet of paper**, on a fixed 90° arm with a narrow field of view. It is not an observer of a person. Everything here follows from that.

## Retention

- The only image that may be persisted, transmitted, logged, or returned across a package boundary is `RectifiedPage` — the region inside the ArUco quadrilateral.
- A full frame lives only in `RawFrame`, in memory, inside one capture scope. Never write it to disk, never pickle or copy it, never put it in a log or an exception message, never send it to a model.
- Always consume a frame with `with camera.capture_once() as frame:` so the buffer is released on exit, including on the error path.
- Do not add a debug flag that dumps frames. If a capture needs diagnosing, save the rectified crop and the marker coordinates.

## Capture triggering

- Single-shot on a physical button press. That is the only trigger.
- Do not add: a streaming or preview endpoint, a timer or polling loop, motion detection, auto-capture on marker presence, or burst capture. Not even temporarily, not behind a flag, not "just for the demo".

## What this package may detect

- Permitted: ArUco markers, QR codes, the page quadrilateral, ink presence in a declared cell rectangle.
- Forbidden, including as an intermediate step: face detection or recognition, person or body detection, hand or gesture tracking, emotion or attention inference.
- If a frame does not contain a recognisable sheet, fail with `MarkersNotFound`. Do not fall back to analysing whatever else is in the frame.

## Reading cells

- A reading is an observation about ink, never a judgement about the person. Return what is in the cell; never a correctness verdict phrased as an evaluation of her.
- Below confidence, set `needs_review=True`. Never guess a value to avoid an empty result.
- When the cloud is unavailable, read only the cell kinds in `sheet.LOCALLY_READABLE`, mark everything else `needs_review`, and set `degraded=True`. Never silently skip cells.
- Refuse a sheet whose `spec_version` this code does not understand rather than reading it with the wrong cell geometry — misattributed answers are worse than no answer.
