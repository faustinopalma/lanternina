"""Compare two prompt versions with fixed methods, or rejudge saved synthetic documents."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import subprocess
import time
from pathlib import Path
from string import Template
from unittest.mock import patch

from panel.devising import devise_experience
from research import bench
from research.households import CAN, Household, Memory, arguments
from shared import prompts
from shared.experience import Experience
from shared.methods import load, runnable

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "b60df1c3fbef0fa5a87e1c45107d49bcac206409"
BLOCKS = (
    "agents/experience_deviser.task.md",
    "agents/experience_deviser.format.md",
    "agents/experience_continuer.manner-head.md",
    "shared/experience_prompt.the-marks-on-a-page.md",
    "shared/experience_prompt.the-shape-of-a-moment.md",
    "shared/experience_prompt.only-what-you-can-answer.md",
    "shared/experience_prompt.what-makes-it-worth-doing.md",
)
CASES = (
    ("hypotheses", "facts-printed-three-explanations", ("le cose che si rompono",)),
    ("construction", "paper-that-has-to-hold", ("le costruzioni di carta",)),
    ("drawing", "draw-with-one-thing-taken-away", ("il disegno",)),
)


def save(path: Path, rows: list[dict]) -> None:
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8", newline="")


async def judge(experience: Experience) -> dict:
    from agents.experience_judge import _INSTRUCTION, ExperienceJudge
    from research.calls import a_context

    context = a_context(time.time())
    try:
        verdict = await asyncio.wait_for(
            ExperienceJudge().judge(context, experience=experience), timeout=120
        )
        return {
            "verdict": verdict.to_dict(),
            "judgePrompt": _INSTRUCTION,
            "judgeFingerprint": hashlib.sha256(_INSTRUCTION.encode()).hexdigest()[:12],
        }
    except Exception as error:
        return {"judgeError": f"{type(error).__name__}: {error}"}
    finally:
        await context.router._gate.aclose()


async def rejudge(path: Path) -> None:
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not rows or not any("experience" in row for row in rows):
        raise ValueError("No generated experiences to judge")
    output = path.with_name("rejudged.json")
    if output.exists():
        raise FileExistsError(output)
    results = []
    for row in rows:
        if "experience" not in row:
            continue
        began = time.monotonic()
        result = {"case": row["case"], "variant": row["variant"]}
        result.update(await judge(Experience.from_dict(row["experience"])))
        result["seconds"] = round(time.monotonic() - began, 2)
        results.append(result)
        save(output, results)
        print(json.dumps(result, ensure_ascii=False, default=str).split('"judgePrompt"')[0],
              flush=True)


async def compare(output: Path, baseline: str) -> None:
    if output.exists():
        raise FileExistsError(output)
    output.mkdir(parents=True)
    old = {}
    for filename in BLOCKS:
        source = subprocess.check_output(
            ["git", "show", f"{baseline}:{filename}"], cwd=ROOT, encoding="utf-8"
        )
        old[(ROOT / filename).resolve()] = prompts._COMMENT.sub("", source).strip("\n") + "\n"
    original_text = prompts.Prompts.text

    def old_text(self, name, **fill):
        source = old.get(self.stem.with_name(f"{self.stem.name}.{name}.md"))
        if source is None:
            return original_text(self, name, **fill)
        return Template(source).substitute(fill) if fill else source

    corpus = runnable(load(), capabilities=CAN)
    move = next(method for method in corpus if method.method_id == "a-box-ticked-in-the-moment")
    rows = []
    for case_index, (case, method_id, interests) in enumerate(CASES):
        form = next(method for method in corpus if method.method_id == method_id)
        if form.is_a_move or not move.is_a_move:
            raise ValueError("Expected one form and one move")
        house = Household(name=case, interests=interests, sheets=2)

        async def fixed_method(*args, chosen_form=form, chosen_move=move, **kwargs):
            return chosen_form, chosen_move

        variants = ("baseline", "revised") if case_index % 2 == 0 else ("revised", "baseline")
        for variant in variants:
            began = time.monotonic()
            calls = []
            row = {
                "case": case, "variant": variant, "baselineCommit": baseline,
                "form": form.method_id, "move": move.method_id, "calls": calls,
            }
            experience = None
            from orchestrator.router import FoundryRouter

            original_analyze = FoundryRouter.analyze

            async def recorded(router, request, records=calls, analyze=original_analyze):
                call = {"purpose": request.purpose, "sent": request.prompt}
                records.append(call)
                tick = time.monotonic()
                try:
                    response = await analyze(router, request)
                    call.update(received=response.text, truncated=response.truncated)
                    return response
                except Exception as error:
                    call["error"] = f"{type(error).__name__}: {error}"
                    raise
                finally:
                    call["seconds"] = round(time.monotonic() - tick, 2)

            print(f"START {case} {variant}", flush=True)
            try:
                with (
                    patch.object(prompts.Prompts, "text", old_text if variant == "baseline"
                                 else original_text),
                    patch("panel.devising._what_to_build_out_of", fixed_method),
                    patch.object(FoundryRouter, "analyze", recorded),
                ):
                    row["promptFingerprint"] = bench.reload_prompts()
                    experience, _usage = await asyncio.wait_for(
                        devise_experience(**arguments(house, Memory()), now=time.time()),
                        timeout=360,
                    )
                    row["experience"] = experience.to_dict()
            except Exception as error:
                row["error"] = f"{type(error).__name__}: {error}"
            finally:
                bench.reload_prompts()
            if experience is not None:
                row.update(await judge(experience))
            row["seconds"] = round(time.monotonic() - began, 2)
            rows.append(row)
            save(output / "comparison.json", rows)
            print(f"DONE {case} {variant} calls={len(calls)} elapsed={row['seconds']}s", flush=True)


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rejudge", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--baseline", default=BASELINE)
    args = parser.parse_args()
    if (args.rejudge is None) == (args.output is None):
        parser.error("Choose either --rejudge FILE or --output NEW_DIRECTORY")
    bench.environment()
    began = time.monotonic()
    try:
        if args.rejudge is not None:
            await rejudge(args.rejudge)
        else:
            await compare(args.output, args.baseline)
    finally:
        print(f"elapsed={time.monotonic() - began:.1f}s", flush=True)


if __name__ == "__main__":
    asyncio.run(main())