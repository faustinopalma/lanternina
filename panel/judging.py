"""Reading an afternoon back, straight after it was written.

`agents/experience_judge.py` says what this reads for and why it invents no criteria. This
is the half that runs in the container that holds the identity, the twin of
`panel/devising.py` — and the differences from that twin are the whole design of it.

**It runs after the afternoon is stored, never before.** Measured 3 September 2026: a
devise costs 112–184 s over ten runs, median 143 s, and 138 s in production; this costs
14.4 s. The Container Apps ingress gives up at 240 s, so inside the same reply the slowest
measured devise plus a reading leaves about 42 s. That margin is not the argument on its
own — what decides it is that the two failures are not worth the same. A reading that does
not happen costs a row; a reply that runs out of time costs the afternoon, which was
already written and already paid for. So the house is answered first and this runs after.

**Its router has no content-safety gate, and that is a property rather than an omission.**
`FoundryRouter.analyze` is internal reasoning and does not pass the gate; `generate_for_user`
raises without one. A router built this way can read and reason and cannot produce a word
for a person, which is what a diagnostic should be allowed to do.

**What the judge wrote is screened before a parent reads it.** That does not contradict the
line above: the gate here screens an answer, it does not stand behind a router. A parent
opening the trail reads what a model wrote about their afternoon, and there is one door
model text passes on its way to a person. A refused verdict keeps its finding names — those
are ours, a closed list in `agents/experience_judge.FINDINGS` — and loses the words.

**Nothing here may stop an afternoon.** Every failure returns nothing and is written in the
log. The afternoon was devised, screened, stored and paid for before this was called, and
the call is skipped outright when the household is already at its monthly limit — so it is
counted like every other call and can still never be the one that refuses an afternoon.

**One line goes to the workspace per afternoon, and it carries no words.** Ids, the
fingerprint of the standing instruction, the finding names — a closed list this repository
wrote — a duration and token counts. `panel/observability.py` says what may not be logged
and none of it is here; `agents/experience_deviser.PROMPT_FINGERPRINT` says why a
fingerprint of the instruction rather than of the call is both safe and the only useful
one. The query it is written for, which is the whole reason the line has this shape:

    ContainerAppConsoleLogs_CL
    | where Log_s has 'afternoon judged'
    | extend d = parse_json(substring(Log_s, indexof(Log_s, '{')))
    | extend named = iff(array_length(d.findings) == 0, dynamic(['none']), d.findings)
    | mv-expand finding = named to typeof(string)
    | summarize afternoons = dcount(tostring(d.experience))
        by prompt = tostring(d.prompt), finding
    | order by prompt asc, afternoons desc

`none` is put in where a verdict had no findings, because an afternoon nobody had anything
to say about is the result this is looking for and `mv-expand` drops an empty array. The
string literals are single-quoted so the query survives being passed to `az` on Windows,
where a double quote inside an argument is eaten before the CLI sees it.
"""

from __future__ import annotations

import json
import logging
import os
import secrets
import time
from typing import TYPE_CHECKING, Any

from shared.errors import SafetyBlocked
from shared.ids import LearnerId
from shared.routing import ModelUsage
from shared.seal import Sealer, SealPurpose

from .experiences import ExperienceStore
from .usage import FAILED, KIND_JUDGE, SERVED, LimitStore, UsageStore, at_the_limit, event_from

if TYPE_CHECKING:  # pragma: no cover - the panel imports agents lazily, like its twin
    from agents.experience_judge import Verdict
    from shared.experience import Experience

# What the line in the workspace begins with, so a query has something to match on that
# will not drift when the wording around it does.
SAID = "afternoon judged"


async def judged_and_filed(
    *,
    experiences: ExperienceStore,
    usage: UsageStore,
    limits: LimitStore,
    configured: int,
    household_id: str,
    experience: Experience,
) -> None:
    """Read one afternoon back, keep the verdict beside it, and write the one line.

    Never raises. It is called after the house has already been answered, so there is
    nobody left to raise at: a judgement that could not be made is a row that is not there
    and a line in the log that says so.

    It is counted against the month like every other call and it is skipped at the limit,
    which together are what keep it from ever being the call that refuses an afternoon.
    Its own afternoon is safe because this runs after that one is stored; the next one is
    safe because a household already at its limit is not read back at all.
    """
    from agents.experience_deviser import PROMPT_FINGERPRINT
    from shared.ids import new_id

    said = logging.getLogger(__name__)
    if at_the_limit(usage, limits, household_id, configured):
        # Said rather than passed over. A month with fewer readings than afternoons is
        # otherwise indistinguishable from a fault in this file.
        said.info("%s not read back: the month is at its limit", experience.experience_id)
        return
    verdict: Verdict | None = None
    spent: ModelUsage | None = None
    outcome = FAILED
    try:
        verdict, spent = await judge_experience(experience=experience, now=time.time())
        outcome = SERVED
    except Exception as exc:  # noqa: BLE001 - a diagnostic must not be able to raise
        said.warning("afternoon not judged: %s: %s", type(exc).__name__, exc)
    try:
        usage.record(
            event_from(household_id, KIND_JUDGE, outcome, spent, event_id=str(new_id("use")))
        )
    except Exception as exc:  # noqa: BLE001 - bookkeeping must not eat a verdict
        said.warning("usage not recorded: %s", exc)
    if verdict is None:
        return
    try:
        # The fingerprint goes in with the verdict rather than beside it in another store.
        # It is the only thing that says which version of the prompt wrote this afternoon,
        # and until now nothing did: a record of a reading that cannot say what it read the
        # output of is a record that stops meaning anything the next time a block is edited.
        experiences.judged(
            household_id,
            experience.experience_id,
            {"prompt": PROMPT_FINGERPRINT, **verdict.to_dict()},
        )
    except Exception as exc:  # noqa: BLE001 - the line below is worth writing either way
        said.warning("verdict not kept: %s", exc)
    line = _a_line_about_it(household_id, experience, verdict, spent, PROMPT_FINGERPRINT)
    said.info("%s %s", SAID, json.dumps(line))


def _a_line_about_it(
    household_id: str,
    experience: Experience,
    verdict: Verdict,
    spent: ModelUsage | None,
    fingerprint: str,
) -> dict[str, Any]:
    """The one row per afternoon. Ids, counts, durations and outcomes, and nothing else.

    `contradictions` goes in because a judge that reports a finding belonging to the other
    kind has not understood what it read, and a run where that happens often is a run whose
    counts mean less than they look like they mean.
    """
    from agents.experience_judge import contradictions

    return {
        "household": household_id,
        "experience": experience.experience_id,
        "prompt": fingerprint,
        "canBeWrong": verdict.can_be_wrong,
        "findings": list(verdict.names),
        "contradictions": list(contradictions(verdict)),
        # The judge could not say what the afternoon asks. On one where something can be
        # got wrong, that is the loudest thing this produces.
        "readTheQuestion": bool(verdict.question),
        "degraded": verdict.degraded,
        "latencyS": verdict.metadata.get("latency_s"),
        "inputTokens": spent.input_tokens if spent else 0,
        "outputTokens": spent.output_tokens if spent else 0,
        "reasoningTokens": spent.reasoning_tokens if spent else 0,
    }


async def judge_experience(
    *, experience: Experience, now: float
) -> tuple[Verdict, ModelUsage | None]:
    """One reading of one afternoon, screened, and what the call consumed.

    Raises whatever the router raises when the cloud will not serve it. The caller is
    :func:`judged_and_filed`, which treats every one of those as "no verdict".
    """
    from agents.experience_judge import ExperienceJudge
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig
    from shared.agents import AgentContext

    environment = dict(os.environ)
    router = FoundryRouter(FoundryConfig.from_env(environment))
    context = AgentContext(router=router, learner_id=LearnerId(""), learner_hints={}, now=now)
    verdict = await ExperienceJudge().judge(context, experience=experience)

    # As on the devising path: the seal this gate mints travels nowhere, so a per-process
    # key keeps the gate honest without pretending the seal means anything downstream.
    key = environment.get("LANTERNINA_SAFETY_KEY", "").encode() or secrets.token_bytes(32)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(environment),
        Sealer(SealPurpose.CONTENT_SAFETY, key, "orchestrator.safety"),
    )
    try:
        return await _in_its_own_words(gate, verdict), router.last_usage
    finally:
        await gate.aclose()


async def _in_its_own_words(gate: Any, verdict: Verdict) -> Verdict:
    """The verdict a parent may read: the same one, or the same one without its prose.

    A finding the gate refuses is still a finding. Dropping the whole verdict would lose
    the countable half — the names — over words nobody has to be shown, and the names are
    the half a prompt is measured with.
    """
    from dataclasses import replace

    from shared.safety import ContentKind

    said = "\n".join(
        line
        for line in (verdict.question, verdict.answer, *(one.says for one in verdict.findings))
        if line.strip()
    )
    if not said:
        return verdict
    try:
        await gate.screen(ContentKind.PLAIN_TEXT, said, context="a verdict on an afternoon")
    except SafetyBlocked as exc:
        logging.getLogger(__name__).info("a verdict was refused by the gate: %s", exc)
        return replace(
            verdict,
            question="",
            answer="",
            findings=tuple(replace(one, says="(refused by the gate)") for one in verdict.findings),
            metadata={**verdict.metadata, "refused_by_the_gate": True},
        )
    return verdict
