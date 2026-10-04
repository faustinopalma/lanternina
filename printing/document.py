"""Compose and inspect printable documents before they leave the panel."""

from __future__ import annotations

import base64
import json
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any


@dataclass(frozen=True, slots=True)
class Document:
    pdf: bytes
    previews: tuple[bytes, ...]
    audit: dict[str, Any]


class LayoutError(ValueError):
    pass


def overview(previews: tuple[bytes, ...]) -> bytes:
    import io

    from PIL import Image

    images = [Image.open(io.BytesIO(png)).convert("L") for png in previews]
    if not images:
        raise ValueError("a document needs at least one preview")
    canvas = Image.new("L", (max(image.width for image in images),
                             sum(image.height for image in images) + 20 * (len(images) - 1)), 255)
    offset = 0
    for image in images:
        canvas.paste(image, (0, offset))
        offset += image.height + 20
    output = io.BytesIO()
    canvas.save(output, "PNG")
    return output.getvalue()


def canonical(text: str) -> str:
    return "".join(unicodedata.normalize("NFKC", text).split()).replace("\u00ad", "")


def inspect(pdf: bytes, words: list[str]) -> dict[str, Any]:
    import pymupdf

    with pymupdf.open(stream=pdf, filetype="pdf") as document:
        extracted = canonical("\n".join(page.get_text() for page in document))
        missing = [word for word in words if canonical(word) not in extracted]
        fractions = []
        issues = []
        fonts = set()
        for number, page in enumerate(document, 1):
            if abs(page.rect.width - 210 * 72 / 25.4) > 1:
                issues.append(f"page {number}: not A4 width")
            if abs(page.rect.height - 297 * 72 / 25.4) > 1:
                issues.append(f"page {number}: not A4 height")
            bottom = 16 * 72 / 25.4
            lines = []
            for block in page.get_text("dict")["blocks"]:
                if block["type"] == 1:
                    bottom = max(bottom, block["bbox"][3])
                    continue
                for line in block.get("lines", []):
                    rect = pymupdf.Rect(line["bbox"])
                    if rect.y0 > 280 * 72 / 25.4:
                        continue
                    if not page.rect.contains(rect):
                        issues.append(f"page {number}: text outside page")
                    if rect.x0 < 16 * 72 / 25.4 or rect.x1 > 194 * 72 / 25.4:
                        issues.append(f"page {number}: text outside margins")
                    for previous in lines:
                        overlap = rect & previous
                        if overlap.width > 1 and overlap.height > 2:
                            issues.append(f"page {number}: overlapping text")
                    lines.append(rect)
                    bottom = max(bottom, rect.y1)
            for drawing in page.get_drawings():
                bottom = max(bottom, drawing["rect"].y1)
            if not lines:
                issues.append(f"page {number}: blank page")
            for font in page.get_fonts():
                fonts.add(font[3])
                if not document.extract_font(font[0])[3]:
                    issues.append(f"page {number}: font not embedded")
            fraction = (bottom * 25.4 / 72 - 16) / 264
            if fraction > 1.005:
                issues.append(f"page {number}: content below margin")
            fractions.append(round(fraction, 4))
        count = len(document)
    balanced = count == 1 or (
        count == 2 and min(fractions) >= 0.72 and max(fractions) - min(fractions) <= 0.18
    )
    return {"pages": count, "missing": missing, "issues": issues, "fonts": sorted(fonts),
            "fractions": fractions, "balanced": balanced,
            "valid": 1 <= count <= 2 and not missing and not issues}


def render(source: dict[str, Any], illustration: bytes | None = None) -> Document:
    import pymupdf
    import typst

    words = [source["title"], *source["paragraphs"], *source["steps"],
             *source.get("note", []), *(space["label"] for space in source["spaces"])]
    diagram = source.get("diagram")
    if diagram:
        words.extend(diagram.get("labels", []))
        words.extend(str(cell) for row in diagram.get("rows", []) for cell in row)
    candidates = [("flow", 85, 4, 176), ("flow", 70, 2, 176), ("flow", 60, 2, 176),
                  ("responses", 85, 4, 176), ("responses", 110, 4, 176),
                  ("workspace", 85, 4, 176), ("workspace", 110, 4, 176),
                  ("workbook", 110, 4, 155), ("workbook", 110, 4, 145),
                  ("workbook", 110, 4, 135), ("workbook", 110, 4, 125),
                  ("workbook", 110, 4, 115), ("workbook", 110, 4, 105),
                  ("workbook", 110, 4, 95)]
    if diagram and diagram["kind"] == "table":
        candidates.extend(("table", 110, 4, row) for row in (6, 7, 8, 9))
    audits = []
    accepted = []
    with TemporaryDirectory(prefix="lanternina-document-") as directory:
        root = Path(directory)
        (root / "document.typ").write_bytes(Path(__file__).with_suffix(".typ").read_bytes())
        if illustration:
            (root / "illustration.png").write_bytes(illustration)
        for split, image_mm, spacing_mm, reading_mm in candidates:
            layout = {"split": split, "image": image_mm, "spacing": spacing_mm,
                      "reading": reading_mm, "expanded": image_mm == 110,
                      "table-break": reading_mm if split == "table" else 0}
            data = {**source, "note": source.get("note", []), "diagram": diagram,
                    "illustrated": illustration is not None, "layout": layout}
            boxes = [space["label"] for space in source["spaces"] if space["room"] == "a_box"]
            data["grid-field"] = ""
            if len(boxes) == 1 and diagram and diagram["kind"] == "grid":
                data["grid-field"] = boxes[0]
            (root / "source.json").write_text(json.dumps(data), encoding="utf-8")
            pdf = typst.compile(str(root / "document.typ"), root=str(root))
            audit = {"layout": layout, **inspect(pdf, words)}
            audits.append(audit)
            if audit["valid"] and audit["balanced"]:
                accepted.append((pdf, audit))
                if audit["pages"] == 1:
                    break
    if not accepted:
        raise LayoutError("document needs layout review: " + json.dumps(audits))
    pdf, selected = min(accepted, key=lambda item: (
        item[1]["pages"], max(item[1]["fractions"]) - min(item[1]["fractions"]),
    ))
    with pymupdf.open(stream=pdf, filetype="pdf") as document:
        previews = tuple(page.get_pixmap(dpi=120, alpha=False).tobytes("png") for page in document)
    return Document(pdf, previews, {"version": 1, "selected": selected, "candidates": audits})


def render_bounded(source: dict[str, Any], illustration: bytes | None = None) -> Document:
    payload = {"source": source, "image": base64.b64encode(illustration).decode()
               if illustration else None}
    try:
        result = subprocess.run(
            [sys.executable, "-m", "printing.document"], input=json.dumps(payload).encode(),
            capture_output=True, timeout=30, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise LayoutError("document composition exceeded 30 seconds") from exc
    if result.returncode:
        raise LayoutError(result.stderr.decode("utf-8", errors="replace")[-12000:])
    value = json.loads(result.stdout)
    return Document(base64.b64decode(value["pdf"]),
                    tuple(base64.b64decode(page) for page in value["previews"]), value["audit"])


if __name__ == "__main__":
    payload = json.load(sys.stdin)
    document = render(payload["source"], base64.b64decode(payload["image"])
                      if payload.get("image") else None)
    json.dump({"pdf": base64.b64encode(document.pdf).decode(),
               "previews": [base64.b64encode(page).decode() for page in document.previews],
               "audit": document.audit}, sys.stdout)