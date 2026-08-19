"""Render an approved item for a TRMNL-class e-paper display.

The device draws nothing on its own: it fetches a PNG this module produced. That makes
the delivery boundary topological rather than customary — the panel cannot show content
that did not come through here, and this function refuses anything whose seals do not
verify.

Output is 800x480, 1-bit. The panel is 4-greyscale, but pure black on white is what stays
readable at a distance on e-paper, and it keeps the file small.

Nothing here can render a fault: if the item is not deliverable this raises, and the
caller leaves the previous image on the display. Faults belong in the parent panel.
"""

from __future__ import annotations

import base64
import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from io import BytesIO
from typing import Final

from PIL import Image, ImageDraw, ImageFont, ImageOps

from shared.approval import ApprovedItem
from shared.delivery import assert_deliverable
from shared.exercise import CHOICES, EXERCISES, INSTRUCTIONS, QUESTION, TITLE, field
from shared.safety import ContentKind

WIDTH: Final = 800
HEIGHT: Final = 480
MARGIN: Final = 36

# Tried in order. The first two are what the mini-PC and this workstation actually have;
# the bitmap fallback keeps the function total, at the cost of an ugly render.
_FONT_CANDIDATES: Final = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/segoeui.ttf",
    "/Library/Fonts/Arial.ttf",
)
_BOLD_CANDIDATES: Final = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "/Library/Fonts/Arial Bold.ttf",
)


@dataclass(frozen=True, slots=True)
class _Fonts:
    title: ImageFont.FreeTypeFont | ImageFont.ImageFont
    body: ImageFont.FreeTypeFont | ImageFont.ImageFont
    small: ImageFont.FreeTypeFont | ImageFont.ImageFont


def _load(candidates: tuple[str, ...], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    print("no TTF found; falling back to the bitmap font", file=sys.stderr)
    return ImageFont.load_default()


def _fonts() -> _Fonts:
    return _Fonts(
        title=_load(_BOLD_CANDIDATES, 44),
        body=_load(_FONT_CANDIDATES, 32),
        small=_load(_FONT_CANDIDATES, 26),
    )


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: object, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if draw.textlength(candidate, font=font) <= max_width or not current:  # type: ignore[arg-type]
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def render_epaper_png(
    item: ApprovedItem, *, safety_key: bytes, approval_key: bytes, now: float | None = None
) -> bytes:
    """Return the 1-bit PNG for ``item``, or raise if it may not be shown."""
    return _encode(
        _render(item, safety_key=safety_key, approval_key=approval_key, now=now), "PNG"
    )


def render_epaper_bmp(
    item: ApprovedItem, *, safety_key: bytes, approval_key: bytes, now: float | None = None
) -> bytes:
    """Return the 1-bit BMP the TRMNL firmware expects."""
    return _encode(
        _render(item, safety_key=safety_key, approval_key=approval_key, now=now), "BMP"
    )


def _encode(canvas: Image.Image, image_format: str) -> bytes:
    buffer = BytesIO()
    canvas.save(buffer, format=image_format)
    data = buffer.getvalue()
    return _with_conforming_palette(data) if image_format == "BMP" else data


def _with_conforming_palette(data: bytes) -> bytes:
    """Zero the reserved byte of every palette entry, which BMP requires and Pillow does not.

    Found on the display, not in a test: Pillow 11 on the hub writes the fourth byte of the
    white entry as 0xFF, and the firmware silently refused the file and drew its own screen
    instead. The picture from the cloud, written by a different Pillow, had 0x00 there and
    always worked. One byte, and the two files were otherwise identical.
    """
    if len(data) < 54 or data[:2] != b"BM":
        return data
    pixels = int.from_bytes(data[10:14], "little")
    header = int.from_bytes(data[14:18], "little")
    palette = 14 + header
    if palette >= pixels or (pixels - palette) % 4:
        return data
    patched = bytearray(data)
    for entry in range(palette + 3, pixels, 4):
        patched[entry] = 0
    return bytes(patched)


def render_picture_bmp(
    item: ApprovedItem, *, safety_key: bytes, approval_key: bytes, now: float | None = None
) -> bytes:
    """Return an approved picture as a full-bleed, dithered 1-bit BMP."""
    assert_deliverable(item, safety_key=safety_key, approval_key=approval_key, now=now)
    payload = item.proposal.payload
    if payload.kind is not ContentKind.IMAGE_PNG:
        raise ValueError(f"not a picture: {payload.kind}")
    return render_picture_bytes(payload.body)


def render_picture_bytes(image_b64: str) -> bytes:
    """Render a base64 PNG for the panel, with no approval ceremony.

    Used where the picture was screened but no parent seal exists, which is the case when
    the cloud paints from a theme the parent approved once. The caller is responsible for
    having screened it: this function only knows about pixels.
    """
    picture = Image.open(BytesIO(base64.b64decode(image_b64))).convert("L")
    # Autocontrast first: e-paper has no backlight, and a flat midtone image reads as grey
    # mush once it is reduced to two levels.
    canvas = ImageOps.autocontrast(_cover(picture), cutoff=1)
    # Then flatten the extremes. Without this, paper-white areas sit a few levels below 255
    # and the dither scatters visible speckle across what should be empty background.
    canvas = canvas.point(lambda v: 255 if v > 240 else (0 if v < 15 else v))
    # Floyd-Steinberg, the opposite choice from text: a picture needs the dither that a
    # sentence would only blur.
    return _encode(canvas.convert("1"), "BMP")


def _cover(picture: Image.Image) -> Image.Image:
    """Scale to fill 800x480 and centre-crop, so nothing is letterboxed."""
    scale = max(WIDTH / picture.width, HEIGHT / picture.height)
    resized = picture.resize(
        (max(WIDTH, round(picture.width * scale)), max(HEIGHT, round(picture.height * scale))),
        Image.LANCZOS,
    )
    left = (resized.width - WIDTH) // 2
    top = (resized.height - HEIGHT) // 2
    return resized.crop((left, top, left + WIDTH, top + HEIGHT))


def _render(
    item: ApprovedItem, *, safety_key: bytes, approval_key: bytes, now: float | None = None
) -> Image.Image:
    assert_deliverable(item, safety_key=safety_key, approval_key=approval_key, now=now)

    canvas = Image.new("L", (WIDTH, HEIGHT), 255)
    draw = ImageDraw.Draw(canvas)
    fonts = _fonts()
    payload = item.proposal.payload
    inner = WIDTH - 2 * MARGIN

    if payload.kind is ContentKind.EXERCISE_JSON:
        content = json.loads(payload.body)
        y = _draw_block(draw, str(field(content, TITLE, "")), fonts.title, MARGIN, inner, 52)
        y = _draw_block(draw, str(field(content, INSTRUCTIONS, "")), fonts.body, y + 8, inner, 40)
        for entry in field(content, EXERCISES, []):
            if y > HEIGHT - 90:
                break
            question = str(field(entry, QUESTION, ""))
            choices = "   ".join(f"[ ] {c}" for c in field(entry, CHOICES, []))
            y = _draw_block(draw, question, fonts.body, y + 14, inner, 38)
            y = _draw_block(draw, choices, fonts.small, y, inner, 32)
    else:
        # A single sentence, centred: the routine prompt and the reply after a sheet.
        lines = _wrap(draw, payload.body.strip(), fonts.title, inner)
        block = len(lines) * 56
        y = max(MARGIN, (HEIGHT - block) // 2)
        for line in lines:
            width = draw.textlength(line, font=fonts.title)  # type: ignore[arg-type]
            draw.text(((WIDTH - width) / 2, y), line, font=fonts.title, fill=0)
            y += 56

    # Pure threshold, no dithering: text on e-paper stays crisper without it.
    return canvas.point(lambda v: 255 if v > 127 else 0).convert("1")


def render_notice_bmp(heading: str, lines: Sequence[str]) -> bytes:
    """The house speaking about itself: a sheet waiting, a scanner ready.

    No seal is verified here, and that is not a hole in the delivery boundary. The seals
    attest that model output was screened and approved; these words are literals in the
    repository, so there is nobody to attest and nothing to screen. What must never happen
    is this becoming a way to draw text that came from anywhere else, so it takes strings
    from the caller and the caller is the hub, not an agent.
    """
    canvas = Image.new("L", (WIDTH, HEIGHT), 255)
    draw = ImageDraw.Draw(canvas)
    fonts = _fonts()
    inner = WIDTH - 2 * MARGIN

    y = _draw_block(draw, heading, fonts.title, MARGIN + 24, inner, 52)
    y += 18
    for line in lines:
        y = _draw_block(draw, line, fonts.body, y, inner, 42)
        y += 10
    return _encode(canvas.point(lambda v: 255 if v > 127 else 0).convert("1"), "BMP")


# Two paths draw this: the display server answers a press with it, and the scan writes it a
# moment later. One definition, so the bytes are the same and the display has no reason to
# redraw between the two.
WAITING_HEADING: Final = "Sto leggendo"
WAITING_LINES: Final = ("Lascia il foglio dov'è.", "Ci metto qualche secondo.")


def render_waiting_bmp() -> bytes:
    return render_notice_bmp(WAITING_HEADING, WAITING_LINES)


# What a display shows before anybody has said what it is for. Its own id, large, so the
# row in the panel and the object on the shelf can be matched without a cable or a log.
# It is a name and not a state: nothing here says anything is wrong.
UNASSIGNED_LINES: Final = ("Questo schermo non ha ancora un compito.",)


def render_id_bmp(friendly_id: str) -> bytes:
    return render_notice_bmp(friendly_id, UNASSIGNED_LINES)


def _draw_block(
    draw: ImageDraw.ImageDraw, text: str, font: object, y: int, width: int, step: int
) -> int:
    for line in _wrap(draw, text, font, width):
        if y > HEIGHT - step:
            break
        draw.text((MARGIN, y), line, font=font, fill=0)  # type: ignore[arg-type]
        y += step
    return y
