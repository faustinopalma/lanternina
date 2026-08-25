"""Vision — empty, and honestly so.

The package that read a printed sheet through four markers and a QR code was retired: a
page is now read by handing a model the blank and what came back off the glass, and that
lives in ``agents/page_reader.py``. Nothing has replaced it here yet.

What will land here is the handheld camera path: a photograph arrives from a battery device
with one button, and something is proposed from it minutes later. Two rules will apply to
it, and neither is about framing — faces will be in frame:

1. **Nothing infers anything about a person.** No face detection, no emotion or attention
   inference, no age or identity inference, at any step including an intermediate one.
2. **Capture happens only on a button press.** No streaming endpoint, no timer loop, no
   motion trigger, and nothing in the cloud or in the parent's panel that can take a
   photograph.

See docs/NON-GOALS.md. Neither is enforced by a test today, because there is nothing here
to enforce them against.
"""
