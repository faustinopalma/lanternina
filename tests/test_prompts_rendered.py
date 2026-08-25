"""What is in `docs/prompts/` is what is being sent.

A prompt is assembled from several `.md` files and several numbers, and the assembly is the
part nobody can hold in their head. Rendering it into the repository makes it readable; this
test is what keeps the rendering true. Change a prompt and forget to render, and this fails
with the name of the file to regenerate.

    python -m tools.prompts --write
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.prompts import RENDERED, every_prompt, rendered

ALL = every_prompt()


@pytest.mark.parametrize("one", ALL, ids=[one.name for one in ALL])
def test_the_rendered_prompt_is_the_one_being_sent(one) -> None:
    path = RENDERED / f"{one.name}.txt"
    assert path.exists(), f"{path} is missing; run: python -m tools.prompts --write"
    said = path.read_text(encoding="utf-8")
    assert said == rendered(one), (
        f"{path} is out of date; run: python -m tools.prompts --write"
    )


def test_nothing_is_rendered_that_no_prompt_answers_for() -> None:
    """A prompt removed from the code takes its rendering with it."""
    on_disk = {path.stem for path in Path(RENDERED).glob("*.txt")}
    assert on_disk == {one.name for one in ALL}
