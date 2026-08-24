"""Ask the real service for an afternoon, and print what it cost.

Not a test. `tests/test_experience_deviser.py` stands the model in for and checks the parts
this repository owns; this asks the service that will actually be asked. The reason for
having both is written down rather than assumed: of the defects found in the devising
prompt so far, three came from the real service and none from a test with a fake model
(`ideas/08 §6`). A prompt that grew by the ten dimensions, the six properties of the text,
the three weights, the help ladder and the way out is a prompt whose failures nobody can
guess.

What it prints, and why each number is here rather than a feeling about how it went:

* how long the call took, and how many characters came back — the format-2 document is
  three times the size of a format-1 one, so the output cap is a thing that can now be hit;
* every complaint the checks made, in full, because a check that fires every time is a
  defect in the prompt;
* whether the repair fixed it, and what the second round cost;
* the ten dimensions it drew, because "never the option that comes first" is the one
  instruction in the whole prompt that cannot be checked by code.

It needs the endpoints of the real account and a signed-in identity with the data-plane
roles. It stores nothing and writes nothing except to the screen.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import time

from shared.capabilities import HouseCapability
from shared.experience import DIMENSIONS, Experience, Weight, longest_at
from shared.experience_checks import check


def _report(experience: Experience, seconds: float) -> None:
    body = json.dumps(experience.to_dict(), ensure_ascii=False, separators=(",", ":"))
    print(f"  {seconds:.1f} s, {len(body)} characters, {len(experience.moments)} moments")
    print(f"  title: {experience.title}")
    print(f"  says it lasts {experience.minutes} min; longest path short/standard/extended: "
          f"{longest_at(experience.moments, Weight.SHORT)}/"
          f"{longest_at(experience.moments, Weight.STANDARD)}/"
          f"{longest_at(experience.moments, Weight.EXTENDED)} min")
    for name in DIMENSIONS:
        print(f"    {name:9s} {getattr(experience.drawn, name)}")
    for moment in experience.moments:
        out = moment.way_out
        print(f"    {moment.id:24s} {str(moment.act):10s} "
              f"way out {out.minutes:2d} min from {out.in_hand!r}")


async def _once(language: str, interests: tuple[str, ...], avoid: tuple[str, ...]) -> None:
    from agents.experience_deviser import ExperienceDeviser, experience_in
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig
    from shared.agents import AgentContext
    from shared.experience import ExperienceError
    from shared.ids import LearnerId
    from shared.seal import Sealer, SealPurpose

    environment = dict(os.environ)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, b"k" * 32, "probe"),
    )
    router = FoundryRouter(FoundryConfig.from_env(environment), gate=gate)
    context = AgentContext(
        router=router, learner_id=LearnerId(""), learner_hints={}, now=time.time()
    )
    deviser = ExperienceDeviser()
    capabilities = frozenset(
        {
            HouseCapability.SHOW_800X480_1BIT,
            HouseCapability.PRINT_A4,
            HouseCapability.SCAN_A4,
        }
    )
    try:
        began = time.monotonic()
        answer = await deviser.ask(
            context,
            capabilities=capabilities,
            language=language,
            interests=interests,
            avoid=avoid,
        )
        first = time.monotonic() - began
        try:
            experience = experience_in(answer)
        except ExperienceError as exc:
            print(f"devised: {first:.1f} s, refused by the format: {exc}")
            began = time.monotonic()
            experience = await deviser.repair_unreadable(
                context, answer=answer, refusal=str(exc), language=language
            )
            print("read again after one repair:")
            _report(experience, time.monotonic() - began)
        else:
            print("devised:")
            _report(experience, first)

        complaints = check(experience)
        if not complaints:
            print("  checks: nothing to complain about")
            return
        print(f"  checks: {len(complaints)} complaint(s)")
        for complaint in complaints:
            print(f"    {complaint}")

        began = time.monotonic()
        repaired = await deviser.repair(
            context, refused=experience, complaints=complaints, language=language
        )
        print("repaired:")
        _report(repaired, time.monotonic() - began)
        again = check(repaired)
        print(f"  checks after the repair: {len(again)} complaint(s)")
        for complaint in again:
            print(f"    {complaint}")
    finally:
        await gate.aclose()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", default="italiano")
    parser.add_argument("--interests", default="")
    parser.add_argument("--avoid", default="")
    parser.add_argument("--times", type=int, default=1)
    args = parser.parse_args(argv)

    interests = tuple(w.strip() for w in args.interests.split(",") if w.strip())
    avoid = tuple(w.strip() for w in args.avoid.split(",") if w.strip())
    for attempt in range(args.times):
        if args.times > 1:
            print(f"-- attempt {attempt + 1} of {args.times} " + "-" * 40)
        try:
            asyncio.run(_once(args.language, interests, avoid))
        except Exception as exc:  # a probe reports what happened rather than raising
            print(f"  failed: {type(exc).__name__}: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
