"""Does a filled page land nearer its own blank than another page's? Measure, do not assume.

`ideas/10 §3`. The proposal is to drop the QR and recover which sheet came back off the glass
from an embedding: a page with handwriting on it is a small perturbation of the blank it was
printed from, so its vector should sit nearer that blank than any other. Plausible is not
measured, and a page-identity mechanism that is merely plausible fails silently — it reads the
wrong page and carries the afternoon on from false evidence.

Real pages, not synthetic ones. The pages come out of `printing/render.py`, the same path the
printer gets, because a test on two rectangles would pass for the wrong reason — this project
has been caught by exactly that before, with an ink threshold that worked on a uniform square
and produced twelve false positives on paper.

    python tools/probe_embed.py

Prints the cosine similarity of each filled page against every blank. What has to be true is
that the diagonal wins, and by a margin worth trusting.
"""

from __future__ import annotations

import base64
import io
import json
import os
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from printing.render import PageGeometry, build_drawing, drawing_to_array
from shared.sheet import CellKind, CellSpec, Rect, SheetSpec

from shared.ids import CellId, ExerciseId, SheetId

DEPLOYMENT = "embed-v-4-0"
API_VERSION = "2024-05-01-preview"


def a_sheet(name: str, boxes: list[tuple[float, float, float, float]]) -> SheetSpec:
    return SheetSpec(
        sheet_id=SheetId(f"sh_{name}"),
        exercise_id=ExerciseId(f"ex_{name}"),
        title=f"Foglio {name}",
        qr_rect=Rect(x=0.86, y=0.92, w=0.1, h=0.06),
        cells=tuple(
            CellSpec(
                id=CellId(f"c{index}"),
                kind=CellKind.DRAWING_AREA,
                rect=Rect(x=x, y=y, w=w, h=h),
            )
            for index, (x, y, w, h) in enumerate(boxes)
        ),
    )


def rendered(spec: SheetSpec) -> Image.Image:
    # Text on, because the words are part of what makes one page unlike another.
    array = drawing_to_array(build_drawing(spec, PageGeometry()), dpi=150, text=True)
    return Image.fromarray(array).convert("L")


def written_on(page: Image.Image, seed: int) -> Image.Image:
    """Somebody wrote on it: a few strokes, which is what handwriting is to a whole page."""
    filled = page.copy()
    pen = ImageDraw.Draw(filled)
    rng = np.random.default_rng(seed)
    width, height = filled.size
    for _ in range(24):
        x = float(rng.uniform(0.15, 0.85)) * width
        y = float(rng.uniform(0.2, 0.9)) * height
        pen.line(
            [(x, y), (x + float(rng.uniform(-90, 90)), y + float(rng.uniform(-40, 40)))],
            fill=0,
            width=5,
        )
    return filled


def as_data_url(page: Image.Image) -> str:
    buffer = io.BytesIO()
    page.convert("RGB").save(buffer, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()


def embed(pages: list[Image.Image], endpoint: str, token: str) -> np.ndarray:
    body = {
        "model": DEPLOYMENT,
        "input": [{"image": as_data_url(page)} for page in pages],
        # The route already says these are images; this field says what they are for, and
        # both sides of the comparison are the same kind of thing.
        "input_type": "document",
    }
    request = urllib.request.Request(
        f"{endpoint}/models/images/embeddings?api-version={API_VERSION}",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as answer:
            got = json.loads(answer.read())
    except urllib.error.HTTPError as exc:
        # The body says what the shape should have been; the status alone says nothing.
        raise SystemExit(f"{exc.code}: {exc.read().decode()[:600]}") from exc
    vectors = np.array([row["embedding"] for row in got["data"]], dtype=float)
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)


def main() -> int:
    from azure.identity import DefaultAzureCredential

    endpoint = os.environ.get(
        "LANTERNINA_AI_ENDPOINT", "https://ai-lanternina-dev-ssveb.services.ai.azure.com"
    ).rstrip("/")
    token = DefaultAzureCredential().get_token(
        "https://cognitiveservices.azure.com/.default"
    ).token

    designs = {
        "una": [(0.1, 0.15, 0.35, 0.25), (0.55, 0.15, 0.35, 0.25), (0.1, 0.5, 0.8, 0.3)],
        "due": [(0.1, 0.2, 0.8, 0.5)],
        "tre": [(0.15, 0.1, 0.3, 0.15), (0.15, 0.35, 0.3, 0.15), (0.15, 0.6, 0.3, 0.15)],
    }
    names = list(designs)
    blanks = [rendered(a_sheet(name, designs[name])) for name in names]
    filled = [written_on(page, seed) for seed, page in enumerate(blanks)]

    Path("build").mkdir(exist_ok=True)
    vectors = embed(blanks + filled, endpoint, token)
    blank_vectors, filled_vectors = vectors[: len(names)], vectors[len(names) :]
    similarity = filled_vectors @ blank_vectors.T

    print("righe: la pagina compilata; colonne: la pagina bianca")
    print("            " + "".join(f"{name:>10}" for name in names))
    right = 0
    for index, name in enumerate(names):
        row = "".join(f"{value:>10.4f}" for value in similarity[index])
        nearest = names[int(np.argmax(similarity[index]))]
        right += nearest == name
        print(f"{name + ' scritta':>12}{row}   -> {nearest}")
    margin = min(
        similarity[i, i] - max(v for j, v in enumerate(similarity[i]) if j != i)
        for i in range(len(names))
    )
    print(f"\n{right} su {len(names)} riconosciute; margine minimo {margin:+.4f}")
    return 0 if right == len(names) else 1


if __name__ == "__main__":
    raise SystemExit(main())
