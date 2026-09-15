"""Create a clean numbered workbench notebook without overwriting previous iterations."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path

import nbformat


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", type=int)
    parser.add_argument("label")
    args = parser.parse_args()
    folder = Path(__file__).resolve().parent
    iteration = f"{args.number:03d}-{args.label}"
    if any(folder.glob(f"{args.number:03d}-*.ipynb")):
        raise FileExistsError(f"Iteration {args.number} already exists")
    book = nbformat.read(folder / "001-material-correspondence.ipynb", as_version=4)
    book.cells = book.cells[:12]
    for index, cell in enumerate(book.cells):
        cell.id = f"iteration-{args.number:03d}-cell-{index + 1:02d}"
        cell.metadata = {
            "id": cell.id,
            "language": "python" if cell.cell_type == "code" else "markdown",
        }
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    book.cells[0].source = book.cells[0].source.replace(
        "Officina 001: Material Correspondence", f"Officina {args.number:03d}: {args.label}"
    )
    setup = book.cells[1].source
    assert setup.count("ITERATION = '001-material-correspondence'") == 1
    book.cells[1].source = setup.replace(
        "ITERATION = '001-material-correspondence'", f"ITERATION = {iteration!r}"
    ) + '''
PROMPT_SNAPSHOT = {
    str(path.relative_to(ROOT)): path.read_text(encoding="utf-8")
    for package in ("agents", "shared")
    for path in (ROOT / package).glob("*.md")
}
PROVENANCE = {
    "iteration": ITERATION,
    "prompt_fingerprint": FINGERPRINT,
    "git_head": subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip(),
    "synthetic": True,
}
'''
    book.cells[7].source += '''
if RUN.exists():
    (RUN / "prompt-snapshot.json").write_text(
        json.dumps(PROMPT_SNAPSHOT, ensure_ascii=False, indent=2),
        encoding="utf-8", newline="",
    )
    (RUN / "provenance.json").write_text(
        json.dumps(PROVENANCE, indent=2), encoding="utf-8", newline="",
    )
'''
    for cell in book.cells:
        if cell.cell_type == "code":
            ast.parse(cell.source)
    nbformat.validate(book)
    destination = folder / f"{iteration}.ipynb"
    with destination.open("x", encoding="utf-8", newline="") as output:
        nbformat.write(book, output)
    print(destination)


if __name__ == "__main__":
    main()