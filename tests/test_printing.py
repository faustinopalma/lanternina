"""Guarantees for the printable sheet.

The point of these tests is not that a sheet renders. It is that a sheet renders *and
reads back to the same geometry*, because generator and reader drifting apart is the
failure that misattributes an answer to the wrong question.
"""

from __future__ import annotations

import cv2
import numpy as np
import pytest
from numpy.typing import NDArray

from printing.render import (
    LABEL_SIZE_MM,
    PageGeometry,
    SheetLayoutError,
    _text_width_mm,
    build_drawing,
    drawing_to_array,
    drawing_to_pdf,
    drawing_to_svg,
)
from shared.ids import CellId, ExerciseId, SheetId
from shared.sheet import (
    ARUCO_DICT_NAME,
    CellKind,
    CellSpec,
    Heading,
    QrPayload,
    Rect,
    SheetSpec,
)
from tools.check_scan import (
    INK_PRESENT,
    INK_UNCERTAIN,
    ink_fraction,
    page_ink_threshold,
    rectify,
)
from tools.make_test_sheet import build_test_spec

DPI = 300
MM_PER_INCH = 25.4
# A printer that placed a marker a third of a millimetre out would still be usable; a
# generator that placed it there would be a bug.
TOLERANCE_PX = 3.0


def render(page: PageGeometry, spec: SheetSpec) -> NDArray[np.uint8]:
    return drawing_to_array(build_drawing(spec, page), dpi=DPI)


def detect_markers(image: NDArray[np.uint8]) -> dict[int, NDArray[np.float32]]:
    dictionary = cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, ARUCO_DICT_NAME))
    detector = cv2.aruco.ArucoDetector(dictionary, cv2.aruco.DetectorParameters())
    corners, ids, _ = detector.detectMarkers(image)
    if ids is None:
        return {}
    return {int(i): c.reshape(4, 2) for c, i in zip(corners, ids.flatten(), strict=True)}


@pytest.fixture
def page() -> PageGeometry:
    return PageGeometry()


@pytest.fixture
def spec(page: PageGeometry) -> SheetSpec:
    return build_test_spec(page, SheetId("sh_testcard"), ExerciseId("ex_testcard"))


def test_all_four_markers_are_found(page: PageGeometry, spec: SheetSpec) -> None:
    assert sorted(detect_markers(render(page, spec))) == [0, 1, 2, 3]


def test_markers_land_where_the_geometry_says(page: PageGeometry, spec: SheetSpec) -> None:
    """Finding four markers is not enough — furniture drawn across one still decodes."""
    found = detect_markers(render(page, spec))
    scale = DPI / MM_PER_INCH

    for marker_id, expected in page.marker_rects.items():
        points = found[marker_id]
        assert points[:, 0].min() == pytest.approx(expected.x * scale, abs=TOLERANCE_PX)
        assert points[:, 1].min() == pytest.approx(expected.y * scale, abs=TOLERANCE_PX)
        assert points[:, 0].max() == pytest.approx(expected.right * scale, abs=TOLERANCE_PX)
        assert points[:, 1].max() == pytest.approx(expected.bottom * scale, abs=TOLERANCE_PX)


def test_inner_corners_reconstruct_the_quad(page: PageGeometry, spec: SheetSpec) -> None:
    """Normalised cell coordinates are meaningless unless this quadrilateral is right."""
    found = detect_markers(render(page, spec))
    scale = DPI / MM_PER_INCH
    quad = page.quad

    # Corners come back clockwise from each marker's own top-left, so the corner facing
    # the page centre is at a different index for each of the four.
    inner = {
        0: found[0][2],
        1: found[1][3],
        2: found[2][0],
        3: found[3][1],
    }
    assert inner[0][0] == pytest.approx(quad.x * scale, abs=TOLERANCE_PX)
    assert inner[0][1] == pytest.approx(quad.y * scale, abs=TOLERANCE_PX)
    assert inner[2][0] == pytest.approx(quad.right * scale, abs=TOLERANCE_PX)
    assert inner[2][1] == pytest.approx(quad.bottom * scale, abs=TOLERANCE_PX)


def test_qr_identifies_the_sheet_and_carries_nothing_else(
    page: PageGeometry, spec: SheetSpec
) -> None:
    decoded, _, _ = cv2.QRCodeDetector().detectAndDecode(render(page, spec))
    payload = QrPayload.decode(decoded)

    assert payload.sheet_id == spec.sheet_id
    assert payload.spec_version == spec.spec_version
    # The sheet is looked up locally by id; the page itself must not carry content.
    assert spec.title not in decoded


def test_layout_refuses_a_cell_inside_a_marker_quiet_zone(page: PageGeometry) -> None:
    """Refusing to draw beats printing a sheet that rectifies slightly wrong."""
    intruding = SheetSpec(
        sheet_id=SheetId("sh_bad"),
        exercise_id=ExerciseId("ex_bad"),
        title="overlaps a marker",
        cells=(
            CellSpec(
                id=CellId("intruder"),
                kind=CellKind.CHECKBOX,
                rect=Rect(x=0.0, y=0.0, w=0.05, h=0.03),
            ),
        ),
        qr_rect=Rect(x=0.4, y=0.4, w=0.1, h=0.07),
    )
    with pytest.raises(SheetLayoutError, match="quiet zone"):
        build_drawing(intruding, page)


def test_svg_is_sized_in_millimetres(page: PageGeometry, spec: SheetSpec) -> None:
    """Physical units are what let a misprinted scale be caught with a real ruler."""
    svg = drawing_to_svg(build_drawing(spec, page))

    assert f'width="{page.width_mm}mm"' in svg
    assert f'height="{page.height_mm}mm"' in svg
    assert "50 mm" in svg


def test_the_pdf_carries_multiplication_signs_and_accents(page: PageGeometry) -> None:
    """Read off a sheet that came out of the printer on 20 August 2026: `6 × 2 =` printed
    as `6 ? 2 =` and `attività` as `attivit?`.

    The font is declared /WinAnsiEncoding, which is cp1252, so those bytes are exactly
    what it expects. The content stream was being encoded as ASCII with "replace", which
    undid filtering `_pdf_text` had already done correctly.
    """
    spec = SheetSpec(
        sheet_id=SheetId("sh_accents"),
        exercise_id=ExerciseId("ex_accents"),
        title="6 × 2 =",
        cells=(
            CellSpec(
                id=CellId("c1"),
                kind=CellKind.WORD_LINE,
                rect=Rect(0.1, 0.4, 0.6, 0.04),
                label="6 × 2 =",
            ),
        ),
        qr_rect=Rect(0.78, 0.025, 0.18, 0.118),
        headings=(Heading(Rect(0.05, 0.2, 0.8, 0.04), "Quale attività, perché, così", 5.0),),
    )

    pdf = drawing_to_pdf(build_drawing(spec, page))

    assert "6 × 2 =".encode("cp1252") in pdf
    assert "Quale attività, perché, così".encode("cp1252") in pdf
    assert b"?" not in pdf.split(b"stream", 1)[1].split(b"endstream", 1)[0]


def test_a_label_that_would_run_off_the_paper_goes_under_its_box(
    page: PageGeometry,
) -> None:
    """Read off the third sheet a model designed: a wide tick box with a long label beside
    it printed with the label half outside the page."""
    wide = CellSpec(
        id=CellId("c1"),
        kind=CellKind.CHOICE_BOX,
        rect=Rect(0.45, 0.4, 0.5, 0.04),
        label="Leggo qualche pagina.",
    )
    narrow = CellSpec(
        id=CellId("c2"),
        kind=CellKind.CHOICE_BOX,
        rect=Rect(0.05, 0.6, 0.04, 0.03),
        label="sole",
    )
    spec = SheetSpec(
        sheet_id=SheetId("sh_labels"),
        exercise_id=ExerciseId("ex_labels"),
        title="",
        cells=(wide, narrow),
        qr_rect=Rect(0.78, 0.025, 0.18, 0.118),
    )

    drawing = build_drawing(spec, page)
    placed = {text: (x, y) for x, y, text in drawing.labels}

    right_edge = page.width_mm - page.margin_mm
    for text, (x, _) in placed.items():
        assert x + _text_width_mm(text, LABEL_SIZE_MM) <= right_edge, text
    # The narrow one still reads beside its box, which is the order a choice is read in.
    assert placed["sole"][0] > page.to_page(narrow.rect).right


def test_a_writing_line_starts_after_its_label(page: PageGeometry) -> None:
    """`6 × 2 = ______` is one line. Drawn under the rule instead, the label printed as a
    caption under an empty line and nothing joined the two."""
    labelled = CellSpec(
        id=CellId("c1"),
        kind=CellKind.WORD_LINE,
        rect=Rect(0.1, 0.4, 0.6, 0.04),
        label="6 × 2 =",
    )
    bare = CellSpec(
        id=CellId("c2"), kind=CellKind.WORD_LINE, rect=Rect(0.1, 0.6, 0.6, 0.04)
    )
    spec = SheetSpec(
        sheet_id=SheetId("sh_rules"),
        exercise_id=ExerciseId("ex_rules"),
        title="",
        cells=(labelled, bare),
        qr_rect=Rect(0.78, 0.025, 0.18, 0.118),
    )

    drawing = build_drawing(spec, page)
    with_label, without = sorted(drawing.strokes, key=lambda s: s.vertices[0][1])

    assert with_label.vertices[0][0] > without.vertices[0][0]
    # The label is on the rule's own baseline, so the two read as one line.
    assert any(y == with_label.vertices[0][1] for _, y, _ in drawing.labels)


def scanned(page: PageGeometry, spec: SheetSpec, seed: int = 0) -> NDArray[np.uint8]:
    """A render roughened the way a real scan is: paper texture, not a clean bitmap."""
    image = render(page, spec).astype(np.int16)
    rng = np.random.default_rng(seed)
    image += rng.normal(0.0, 6.0, image.shape).astype(np.int16)
    image -= 6  # scanners rarely return a pure 255 white
    return np.clip(image, 0, 255).astype(np.uint8)


def test_empty_cells_read_empty_on_a_noisy_scan(page: PageGeometry, spec: SheetSpec) -> None:
    """The bug this catches: per-cell Otsu turned paper texture into 30-78% ink.

    A clean synthetic render hides it, because a uniform patch makes Otsu degenerate
    harmlessly. Only a page with texture shows that an empty cell has no second mode to
    find.
    """
    image = scanned(page, spec)
    rectified = rectify(image, detect_markers(image))
    threshold = page_ink_threshold(rectified)

    for cell in spec.cells:
        fraction = ink_fraction(rectified, cell.rect.to_pixels(), threshold)
        assert fraction is not None, f"cell {cell.id!r} was not sampled at all"
        assert fraction <= INK_UNCERTAIN, f"empty cell {cell.id!r} read as {fraction:.1%} ink"


def test_a_marked_cell_still_reads_as_covered(page: PageGeometry, spec: SheetSpec) -> None:
    """Positive control: without it, the test above passes by reporting nothing at all."""
    image = scanned(page, spec)
    target = spec.cells[0]
    area = page.to_page(target.rect)
    scale = DPI / MM_PER_INCH
    cv2.rectangle(
        image,
        (round((area.x + 2) * scale), round((area.y + 2) * scale)),
        (round((area.right - 2) * scale), round((area.bottom - 2) * scale)),
        color=40,
        thickness=-1,
    )

    rectified = rectify(image, detect_markers(image))
    threshold = page_ink_threshold(rectified)
    marked = ink_fraction(rectified, target.rect.to_pixels(), threshold)
    others = [
        ink_fraction(rectified, c.rect.to_pixels(), threshold) for c in spec.cells[1:]
    ]

    assert marked is not None and marked >= INK_PRESENT
    assert all(f is not None and f <= INK_UNCERTAIN for f in others)


def test_a_flat_wide_cell_is_still_sampled(page: PageGeometry, spec: SheetSpec) -> None:
    """A width-derived inset used to swallow the height of the word line and return 0%."""
    image = scanned(page, spec)
    rectified = rectify(image, detect_markers(image))
    threshold = page_ink_threshold(rectified)

    word = next(c for c in spec.cells if c.id == "word")
    assert word.rect.h < word.rect.w / 4, "this test needs a genuinely flat cell"
    assert ink_fraction(rectified, word.rect.to_pixels(), threshold) is not None
