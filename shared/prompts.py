"""The text this system gives a model, kept beside the code that sends it.

**A prompt file is named after the module that sends it and the block it is.**
`agents/experience_deviser.py` sends `agents/experience_deviser.rules.md` and
`agents/experience_deviser.manner.md`, and a sorted directory listing puts every prompt
directly under its own module. One file per block, so a block has a name rather than a
position, and the name says both whose it is and what it does.

Three shapes were considered and this is the third. One file per module with headings
inside needs a section syntax and puts unrelated blocks in one document. A folder per agent
scopes best but turns every agent into a package to hold a directory. This gets the
proximity of the folder without moving any code, and adding a block is adding a file.

What stays in Python is the assembly: which blocks go in what order, and where the
household's own material is quoted. That is where the decisions are; the prose is not code
and had no business being in it.

**Placeholders are `$name`, not `{name}`.** The prompts are full of JSON examples and every
brace in them is literal, so `str.format` would fight the text on every line. Substitution
raises on a name the caller did not supply, so a placeholder that lost its value fails at
import rather than reaching a model as the word `$max_line`.

**The numbers come from the format, never from the file.** `$max_line` is filled from
`shared/experience.MAX_LINE`. Writing 44 into the Markdown would be writing the limit down
twice, and the second copy would go on saying 44 after the first moved — which is the exact
failure the format's own self-description was written to end.

**A comment is `<!-- ... -->` and never reaches the model.** That is where the record of
what was measured lives: which afternoon showed the prompt was wrong, on what date, and by
how much. A reader needs it and the model must not have it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from string import Template
from typing import Any

_COMMENT = re.compile(r"<!--.*?-->\n?", re.DOTALL)


@dataclass(frozen=True, slots=True)
class Prompts:
    """The Markdown belonging to one module. Each file is read once and kept."""

    stem: Path

    def text(self, name: str, **fill: Any) -> str:
        """One block, comments out and placeholders filled from what the caller knows.

        Raises FileNotFoundError naming what is there, or KeyError naming the placeholder
        that was not supplied, so prose and the code that fills it cannot drift apart
        quietly.
        """
        said = _READ.get((self.stem, name))
        if said is None:
            path = self.stem.with_name(f"{self.stem.name}.{name}.md")
            if not path.is_file():
                here = sorted(
                    p.name.split(".")[1]
                    for p in self.stem.parent.glob(f"{self.stem.name}.*.md")
                )
                raise FileNotFoundError(
                    f"{path.name} is missing; {self.stem.name} has: {', '.join(here) or 'none'}"
                )
            said = _COMMENT.sub("", path.read_text(encoding="utf-8")).strip("\n") + "\n"
            _READ[(self.stem, name)] = said
        return Template(said).substitute(fill) if fill else said


_READ: dict[tuple[Path, str], str] = {}


def beside(module_file: str) -> Prompts:
    """The prompts belonging to this module. Pass ``__file__``."""
    path = Path(module_file).resolve()
    return Prompts(path.with_suffix(""))
