"""Execute the workbench with this interpreter and retain outputs even on failure."""

from __future__ import annotations

import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    path = root / "research" / "officina.ipynb"
    book = nbformat.read(path, as_version=4)
    client = NotebookClient(
        book, timeout=900, kernel_name="python3", resources={"metadata": {"path": str(root)}}
    )
    client.km = client.create_kernel_manager()
    client.km.kernel_spec.argv = [
        sys.executable,
        "-m",
        "ipykernel_launcher",
        "-f",
        "{connection_file}",
    ]
    began = time.perf_counter()
    try:
        client.execute()
    finally:
        path.write_text(nbformat.writes(book), encoding="utf-8", newline="")
        print(f"Notebook elapsed: {time.perf_counter() - began:.1f} s", flush=True)


if __name__ == "__main__":
    main()
