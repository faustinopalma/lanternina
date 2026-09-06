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
