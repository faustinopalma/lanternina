r"""Judge the afternoons an experiment already produced, and count what came back.

    $env:PYTHONPATH="."
    .\.venv\Scripts\python.exe -m tools.judge_many experiments/07-something
    .\.venv\Scripts\python.exe -m tools.judge_many experiences/un-pomeriggio-di-nuvole.json

`tools/devise_many.py` writes one JSON per afternoon into `experiments/NN-name/`. This reads
them, sends each to `agents/experience_judge.py`, and writes `judged.json` beside them. A
single file is accepted too, which is how the first run was the one written by hand.

What it is for: the hours spent changing a prompt. Run it, change one block, run it again,
and compare the counts. A finding that appears in eight afternoons out of ten is a prompt
problem; one that appears in one is an afternoon.

**The router is built without a content-safety gate, and that is the safety property.**
`FoundryRouter.analyze` is internal reasoning and does not pass the gate; `generate_for_user`
raises without one. So a router built this way can read and reason and cannot produce a word
for a person, which is exactly what a diagnostic should be allowed to do.

**The reverse-solving comparison is left to a person, on purpose.** The judge is shown the
moments and not the script, and works out what it thinks the question and the answer are.
Whether that matches what the author meant is printed side by side and read by whoever is
doing the prompt work. Automating that comparison is another model call and another thing
that can be wrong, and it has not yet been worth it.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent.parent


async def judge_one(path: Path) -> dict[str, Any]:
    from agents.experience_judge import ExperienceJudge, contradictions
    from shared.experience import Experience

    document = json.loads(path.read_text(encoding="utf-8"))
    experience = Experience.from_dict(document)
    ctx = _context()
    verdict = await ExperienceJudge().judge(ctx, experience=experience)
    return {
        "file": path.name,
        "title": document.get("title", ""),
        # What the author wrote, so the person reading this can compare it with what the
        # judge worked out from the moments alone. This is the reverse-solve.
        "script": document.get("script", ""),
        **verdict.to_dict(),
        "contradictions": list(contradictions(verdict)),
    }


def _context() -> Any:
    """A router that can reason and cannot generate, which is what a diagnostic needs.

    No gate is built, so `generate_for_user` raises and `analyze` — the only thing the judge
    calls — works. Content Safety is not configured here and does not need to be.
    """
    import os
    import time

    from orchestrator.router import FoundryConfig, FoundryRouter
    from shared.agents import AgentContext
    from shared.ids import LearnerId

    router = FoundryRouter(FoundryConfig.from_env(dict(os.environ)))
    return AgentContext(router=router, learner_id=LearnerId(""), learner_hints={}, now=time.time())


async def run(folder: Path) -> int:
    # A single file is allowed so that the first run can be the calibration one: judging
    # `experiences/un-pomeriggio-di-nuvole.json`, which a person wrote, says whether the
    # judge is worth believing before ten machine-written afternoons are handed to it.
    if folder.is_file():
        files = [folder]
        # Never beside the input: `experiences/` is a contract directory and
        # `tests/test_experience.py` parses every file in it as an afternoon.
        written_to = HERE / "experiments" / f"judged-{folder.stem}.json"
    else:
        files = sorted(p for p in folder.glob("[0-9][0-9].json"))
        written_to = folder / "judged.json"
    if not files:
        print(f"nessun pomeriggio in {folder}: cercavo NN.json", file=sys.stderr)
        return 2

    rows: list[dict[str, Any]] = []
    for path in files:
        try:
            got = await judge_one(path)
        except Exception as exc:  # noqa: BLE001 - a failed judgement is a result worth keeping
            got = {"file": path.name, "failed": f"{type(exc).__name__}: {exc}"}
        rows.append(got)
        _say(got)

    written_to.parent.mkdir(parents=True, exist_ok=True)
    written_to.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    _summarise(rows, written_to)
    _which_prompt(folder)
    return 0


def _which_prompt(folder: Path) -> None:
    """The fingerprint of the prompt that wrote these, if the run that made them said.

    Read off `runs.json` rather than computed here: the prompt has very likely changed
    since, and stamping today's fingerprint on afternoons written a week ago is the way to
    make a set of counts say something that is not true.
    """
    runs = folder / "runs.json" if folder.is_dir() else None
    if runs is None or not runs.is_file():
        print("prompt: non registrato in questa cartella")
        return
    try:
        found = {str(row.get("prompt", "")) for row in json.loads(runs.read_text("utf-8"))}
    except ValueError:
        return
    named = sorted(one for one in found if one)
    print(f"prompt: {', '.join(named) if named else 'non registrato in questa cartella'}")


def _say(got: dict[str, Any]) -> None:
    if got.get("failed"):
        print(f"{got['file']}  {got['failed']}")
        return
    kind = "si può sbagliare" if got["can_be_wrong"] else "aperta"
    names = ", ".join(f["where"].split(":", 1)[0] for f in got["findings"]) or "niente"
    print(f"\n{got['file']}  [{kind}]  {got['title']}")
    print(f"   domanda letta:  {got['question'] or '— non ha saputo dirla'}")
    print(f"   risposta letta: {got['answer'] or '—'}")
    print(f"   l'autore diceva: {(got['script'] or '—')[:160]}")
    print(f"   rilievi: {names}")
    if got["contradictions"]:
        print(f"   !! rilievi che non appartengono a questo tipo: {got['contradictions']}")


def _summarise(rows: list[dict[str, Any]], written_to: Path) -> None:
    judged = [r for r in rows if not r.get("failed")]
    if not judged:
        print(f"\nniente giudicato; {len(rows)} tentativi")
        return
    counts: Counter[str] = Counter()
    for row in judged:
        counts.update(f["where"].split(":", 1)[0] for f in row["findings"])
    aperte = sum(1 for r in judged if not r["can_be_wrong"])
    senza_domanda = sum(1 for r in judged if r["can_be_wrong"] and not r["question"])
    print(f"\n{len(judged)}/{len(rows)} giudicati, scritto in {written_to}")
    print(f"  aperte (niente può essere sbagliato): {aperte}")
    print(f"  hanno una risposta e il giudice non ha saputo dire quale: {senza_domanda}")
    print("  rilievi, su quanti pomeriggi:")
    for name, n in counts.most_common():
        print(f"     {n:3}/{len(judged)}  {name}")
    if not counts:
        print("     nessuno")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path)
    args = parser.parse_args(argv)
    folder = args.folder if args.folder.is_absolute() else HERE / args.folder
    return asyncio.run(run(folder))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
