"""What `research/officina.ipynb` sits on: the prompts on disk, and this process reading them again.

`research/run.py` is the measurement — six households, four iterations, an hour, eight axes.
This is the other half: one afternoon at a time, with the prompt open in the editor beside
it. The blocks stay in the `.md` files beside the modules that send them; nothing here holds
a copy of one.

    import research.bench as bench
    bench.environment()                 # the deployed API's own settings, from env.ps1
    bench.blocks("agents.experience_deviser")
    bench.reload_prompts()              # after editing a .md, before calling again

⚠️ After a block is settled, `python -m tools.prompts --write` renders `docs/prompts/` and
`tests/test_prompts_rendered.py` fails until it has been run.
"""

from __future__ import annotations

import importlib
import os
import re
import sys
from pathlib import Path
from typing import Final

HERE: Final = Path(__file__).resolve().parent
ROOT: Final = HERE.parent

# `$env:NAME = "value"` in env.ps1. Parsed rather than duplicated: the values were read out
# of the deployed container app.
_SETS: Final = re.compile(r'^\$env:(\w+)\s*=\s*"([^"]*)"', re.MULTILINE)

# The modules that assemble prompt text into constants at import, innermost first. Order
# matters: an agent quotes the shared blocks into its instruction when it is imported.
IN_ORDER: Final = (
    "shared.experience_prompt",
    "agents.experience_deviser",
    "agents.experience_continuer",
    "agents.experience_judge",
    "agents.page_maker",
    "research.calls",
    "research.play",
)


def environment(path: Path | None = None) -> dict[str, str]:
    """Put the settings a run needs into this process. Returns what was set.

    Credentials are not in that file: the router builds a `DefaultAzureCredential`, which
    finds the signed-in `az` session in the `AZURE_CONFIG_DIR` it names.
    """
    found = dict(_SETS.findall((path or HERE / "env.ps1").read_text(encoding="utf-8")))
    os.environ.update(found)
    return found


def blocks(module: str) -> list[tuple[str, int]]:
    """Every prompt block this module can send, by name and length in characters.

    Read off the files and not off the module, so a block that is quoted by nothing still
    shows up.
    """
    stem = ROOT / (module.replace(".", "/"))
    return sorted(
        (path.name.split(".", 1)[1].removesuffix(".md"), len(path.read_text(encoding="utf-8")))
        for path in stem.parent.glob(f"{stem.name}.*.md")
    )


def read(module: str, name: str) -> str:
    """One block as it is on disk, comments and all."""
    stem = ROOT / (module.replace(".", "/"))
    return stem.with_name(f"{stem.name}.{name}.md").read_text(encoding="utf-8")


def write(module: str, name: str, text: str) -> Path:
    """Put a block back, and say where it went. Reloading it is a separate step."""
    stem = ROOT / (module.replace(".", "/"))
    path = stem.with_name(f"{stem.name}.{name}.md")
    path.write_text(text, encoding="utf-8", newline="")
    return path


def reload_prompts() -> str:
    """Re-read every `.md` and rebuild the assembled instructions. Returns the fingerprint.

    `agents.experience_deviser.PROMPT_FINGERPRINT`, which is what a result is worth writing
    down beside: two afternoons under different digits do not compare.
    """
    import shared.prompts

    shared.prompts.forget()
    for name in IN_ORDER:
        module = sys.modules.get(name)
        if module is not None:
            importlib.reload(module)
    return str(importlib.import_module("agents.experience_deviser").PROMPT_FINGERPRINT)


def everything() -> dict[str, str]:
    """Every block the deviser sends, rendered, under a short name.

    The format's own numbers are filled in; the placeholders that carry a household's
    material are left as `$name` for the caller to fill. Comments never reach a model and
    are not here either.
    """
    import shared.experience_prompt as fmt
    from agents import experience_deviser as deviser
    from research import calls

    return {
        "task": deviser.SAYS.text("task"),
        "format": deviser.SAYS.text(
            "format",
            max_overview=deviser.MAX_OVERVIEW,
            max_themes=deviser.MAX_THEMES,
            max_theme=deviser.MAX_THEME,
            MAX_SCRIPT=deviser.MAX_SCRIPT,
        ),
        "shape-of-a-moment": fmt.THE_SHAPE_OF_A_MOMENT,
        "acts": fmt.THE_ACTS,
        "marks-on-a-page": fmt.THE_MARKS_ON_A_PAGE,
        "ten-dimensions": fmt.THE_TEN_DIMENSIONS,
        "rules-head": deviser.SAYS.text(
            "rules-head",
            max_moments=deviser.MAX_MOMENTS,
            max_title=deviser.MAX_TITLE,
            max_overview=deviser.MAX_OVERVIEW,
        ),
        "limits": fmt.THE_LIMITS,
        "rules-tail": deviser.SAYS.text(
            "rules-tail", min_minutes=deviser.MIN_MINUTES, max_minutes=deviser.MAX_MINUTES
        ),
        "asking": deviser.SAYS.text("asking"),
        "manner-head": deviser.SAYS.text("manner-head"),
        "how-the-text-reads": fmt.HOW_THE_TEXT_READS,
        "what-to-refuse": fmt.WHAT_TO_REFUSE_BY_DEFAULT,
        "only-what-you-can-answer": fmt.ONLY_WHAT_YOU_CAN_ANSWER,
        "worth-doing": fmt.WHAT_MAKES_IT_WORTH_DOING,
        "manner-tail": deviser.SAYS.text("manner-tail"),
        "method": deviser.SAYS.text("method"),
        "household": deviser.SAYS.text("household"),
        "pitch": deviser.SAYS.text("pitch"),
        "stand-in": calls.SAYS.text("adolescent"),
    }


def to_paste(key: str, text: str) -> str:
    """One block as the line of Python that overrides it, to paste into a cell and edit."""
    return f'P["{key}"] = r"""\n{text.strip()}\n"""'
