"""The workbench a notebook sits on: the prompts on disk, and this process reading them again.

`research/run.py` is the measurement — six households, four iterations, an hour, eight axes.
This is the other half: one afternoon at a time, with the prompt open in the editor beside
it, so a sentence can be changed and its effect looked at before an hour is spent finding
out whether it moved a number.

**Nothing here holds a copy of a prompt.** The blocks stay where they are, in the `.md`
files beside the modules that send them, and this only makes the running process read them
again. That is the whole design decision: a workbench with its own copy of the text would
drift from the product exactly the way `research/run.py` drifted from `panel/devising.py`
in September, and the divergence would not announce itself.

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

# `$env:NAME = "value"` in env.ps1. Parsed rather than duplicated, because the values were
# read out of the deployed container app and a second copy of them would be a second thing
# to keep true.
_SETS: Final = re.compile(r'^\$env:(\w+)\s*=\s*"([^"]*)"', re.MULTILINE)

# The modules that assemble prompt text into constants at import, innermost first. Order is
# the argument: `agents/experience_deviser.py` quotes the shared blocks into `_INSTRUCTION`
# when it is imported, so reloading it before the module those blocks live in would rebuild
# the instruction out of the text that was already there.
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

    Same file the PowerShell prologue sources, so a notebook and a terminal run reach the
    same endpoint and the same deployment. Credentials are not in it and never were: the
    router builds a `DefaultAzureCredential`, which finds the signed-in `az` session in the
    `AZURE_CONFIG_DIR` this file names.
    """
    found = dict(_SETS.findall((path or HERE / "env.ps1").read_text(encoding="utf-8")))
    os.environ.update(found)
    return found


def blocks(module: str) -> list[tuple[str, int]]:
    """Every prompt block this module can send, by name and length in characters.

    Read off the files rather than off the module, so a block that exists on disk and is
    quoted by nothing still shows up — which is the state a block is in just after it has
    been added and just before it has been forgotten.
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
    """Put a block back, and say where it went. Reloading is a separate step on purpose.

    Writing without reloading is what a person does when they want to see the diff first,
    and reloading without writing is what they do after editing in the editor. Neither is
    the wrong order, so neither is bolted onto the other.
    """
    stem = ROOT / (module.replace(".", "/"))
    path = stem.with_name(f"{stem.name}.{name}.md")
    path.write_text(text, encoding="utf-8", newline="")
    return path


def reload_prompts() -> str:
    """Re-read every `.md` and rebuild the assembled instructions. Returns the fingerprint.

    The fingerprint is `agents.experience_deviser.PROMPT_FINGERPRINT`, and it is returned
    rather than printed because it is the one thing worth writing down beside a result: two
    afternoons under the same twelve hex digits were devised by the same prompt, and two
    under different ones cannot be compared no matter how they read.
    """
    import shared.prompts

    shared.prompts.forget()
    for name in IN_ORDER:
        module = sys.modules.get(name)
        if module is not None:
            importlib.reload(module)
    return str(importlib.import_module("agents.experience_deviser").PROMPT_FINGERPRINT)
