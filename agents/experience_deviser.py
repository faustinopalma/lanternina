"""Devise an afternoon from scratch, for one house, before anybody has approved anything.

This is the other half of `agents/experience_continuer.py`. That one writes the rest of an
afternoon once a page has come back; this one writes the beginning, when there is no
afternoon yet and nothing has happened. Between them an experience is devised rather than
chosen from a list, which is the difference `ideas/08 §3` says the whole thing turns on.

What bounds a model here is what bounds it there, and neither is in the prompt.

* **The format.** :class:`~shared.experience.Experience` parses what comes back and
  refuses what it does not define. :mod:`shared.experience_prompt` describes it for the
  model's benefit; it is not what enforces it.
* **The checks.** :func:`shared.experience_checks.check` refuses a document that parses
  perfectly and cannot be run well — a way out that reaches for an object nobody was
  given, a plan whose shortest form does not fit its own window, a word off the block
  list. Devising is offline, so a devise → check → repair → recheck loop costs waiting
  rather than risk, which is the whole reason the checks are worth having.
* **The gate.** ``orchestrator.safety.screen_experience`` screens every word before the
  document is stored, because a parent reads an overview and approves from that.

**Repair sends back only what failed.** :meth:`ExperienceDeviser.repair` hands the model
its own document and the complaints, and asks for the fields those complaints name. A full
regeneration would change an afternoon that was mostly right and reopen everything already
settled — including the ten dimensions, which is how a repair loop becomes a slow random
walk.

Three fields are not asked for and are filled in here: the id, the format version, and
which capabilities the afternoon needs. The last is the interesting one — the moments
already say what the house must be able to do, ``NEEDS`` maps each act to its capability,
and a model made to restate that can only get it wrong. It stays a field on the document
because an afternoon written by hand can still declare it and be checked against it.

What a devised afternoon is given about the household is the equipment, the language, what
the parent already wrote in their settings as interests and as things to avoid, and the
dimensions the last few afternoons here were drawn along. There is nothing about a person
in it: no name, no profile, no learner, and no record of what anybody did. That is not
caution here, it is the type — an experience has no field that could hold one.
"""

from __future__ import annotations

import json
import secrets
from collections.abc import Sequence
from typing import Any, Final

from shared.agents import AgentContext
from shared.capabilities import NEEDS, HouseCapability
from shared.experience import (
    EXPERIENCE_FORMAT_VERSION,
    MAX_MINUTES,
    MAX_MOMENTS,
    MAX_OVERVIEW,
    MAX_SHARED_DIMENSIONS,
    MAX_STRATEGY,
    MAX_THEME,
    MAX_THEMES,
    MAX_TITLE,
    MIN_MINUTES,
    Drawn,
    Experience,
    ExperienceError,
    moment_from_dict,
)
from shared.experience_checks import Complaint
from shared.experience_prompt import (
    HOW_THE_TEXT_READS,
    THE_ACTS,
    THE_LIMITS,
    THE_MARKS_ON_A_PAGE,
    THE_SHAPE_OF_A_MOMENT,
    THE_TEN_DIMENSIONS,
    WHAT_MAKES_IT_WORTH_DOING,
    WHAT_TO_REFUSE_BY_DEFAULT,
)
from shared.ids import new_request_id
from shared.prompts import beside
from shared.routing import Capability, ModelRequest
from shared.safety import ContentKind

# A whole afternoon in format 2 is several times the document format 1 carried: every
# moment gained three weighings, four rungs of help and a way out.
# `experiences/un-pomeriggio-di-nuvole.json` was 3 123 characters as compact JSON in format
# 1 and is 10 543 in format 2 — measured 23 August 2026, the same seven moments, which is
# 1 060 characters more per moment. This leaves room for a longer one arriving
# pretty-printed, and it is the reason the number moved rather than a guess about models.
MAX_EXPERIENCE_CHARS: Final = 20000

SAYS: Final = beside(__file__)

# The order is the argument: what shape the answer has, then what a moment is, then what
# holds an afternoon together, then how it reads. Each block is a file next to this one.
_FORMAT: Final = (
    SAYS.text(
        "format",
        max_overview=MAX_OVERVIEW,
        max_themes=MAX_THEMES,
        max_theme=MAX_THEME,
        max_strategy=MAX_STRATEGY,
    )
    + THE_SHAPE_OF_A_MOMENT
    + THE_ACTS
    + THE_MARKS_ON_A_PAGE
)

_RULES: Final = (
    SAYS.text("rules-head", max_moments=MAX_MOMENTS, max_title=MAX_TITLE, max_overview=MAX_OVERVIEW)
    + THE_LIMITS
    + SAYS.text("rules-tail", min_minutes=MIN_MINUTES, max_minutes=MAX_MINUTES)
)

_ASKING: Final = SAYS.text("asking")

_MANNER: Final = (
    SAYS.text("manner-head")
    + HOW_THE_TEXT_READS
    + WHAT_TO_REFUSE_BY_DEFAULT
    + WHAT_MAKES_IT_WORTH_DOING
    + SAYS.text("manner-tail")
)

_INSTRUCTION: Final = (
    SAYS.text("task")
    + _FORMAT
    + THE_TEN_DIMENSIONS
    + _RULES
    + _ASKING
    + _MANNER
)

# What is said when the format refuses an answer. The format and the rules follow it, so a
# repair is written against the same shape the first attempt was.
_REPAIR: Final = SAYS.text("repair")


def the_prompt(
    *,
    language: str,
    capabilities: frozenset[HouseCapability],
    interests: tuple[str, ...] = (),
    avoid: tuple[str, ...] = (),
    already: tuple[str, ...] = (),
    recent: Sequence[Drawn] = (),
) -> str:
    """The whole thing the model is sent, standing instruction and household both.

    Its own function so that what is sent can be read without running anything:
    `tools/prompts.py` renders it into `docs/prompts/`, and a test refuses a change here
    that has not been rendered. What a parent typed in the panel arrives quoted as JSON,
    which is what keeps it material rather than instruction.
    """
    return (
        f"{_INSTRUCTION}\n"
        + SAYS.text(
            "household",
            language=language,
            capabilities=", ".join(sorted(str(c) for c in capabilities)),
            interests=json.dumps(list(interests), ensure_ascii=False),
            avoid=json.dumps(list(avoid), ensure_ascii=False),
            already=json.dumps(list(already), ensure_ascii=False),
        )
        + _not_again(recent)
    )


class ExperienceDeviser:
    """Writes a whole afternoon, screened by the caller before a parent is shown it."""

    name = "experience_deviser"

    async def devise(
        self,
        ctx: AgentContext,
        *,
        capabilities: frozenset[HouseCapability],
        language: str,
        interests: tuple[str, ...] = (),
        avoid: tuple[str, ...] = (),
        already: tuple[str, ...] = (),
        recent: Sequence[Drawn] = (),
    ) -> Experience:
        """One afternoon, parsed. Raises when what came back is not one."""
        return experience_in(
            await self.ask(
                ctx,
                capabilities=capabilities,
                language=language,
                interests=interests,
                avoid=avoid,
                already=already,
                recent=recent,
            )
        )

    async def ask(
        self,
        ctx: AgentContext,
        *,
        capabilities: frozenset[HouseCapability],
        language: str,
        interests: tuple[str, ...] = (),
        avoid: tuple[str, ...] = (),
        already: tuple[str, ...] = (),
        recent: Sequence[Drawn] = (),
    ) -> str:
        """The answer as it came back, before anything tries to read it.

        Separate from :meth:`devise` because of what happens when it does not parse. Two
        of seven answers from the real service on 23 August 2026 were refused for a line of
        45 characters and for a fifth line on a screen, and a caller holding only the
        exception has nothing to hand back to be corrected. Keeping the text is what makes
        :meth:`repair_unreadable` possible.

        ``interests`` and ``avoid`` are what the parent already wrote in the panel's
        settings, quoted as material rather than obeyed as instructions. ``already`` is
        the titles of afternoons this house has been offered before, so that the next one
        is a different afternoon — titles of documents, and nothing about who did them or
        how it went. ``recent`` is what those afternoons were drawn along, which is the
        constraint that can actually be checked afterwards: a title can be changed without
        changing anything.
        """
        payload = await ctx.router.analyze(
            ModelRequest(
                capability=Capability.PLANNING,
                prompt=the_prompt(
                    language=language,
                    capabilities=capabilities,
                    interests=interests,
                    avoid=avoid,
                    already=already,
                    recent=recent,
                ),
                request_id=new_request_id(),
                max_output_chars=MAX_EXPERIENCE_CHARS,
                purpose="devising an afternoon",
                content_kind=ContentKind.EXERCISE_JSON,
            )
        )
        return payload.text

    async def repair(
        self,
        ctx: AgentContext,
        *,
        refused: Experience,
        complaints: Sequence[Complaint],
        language: str,
    ) -> Experience:
        """The same afternoon with the refused fields written again.

        The whole document goes up because a way out cannot be rewritten without knowing
        what came before it. What comes back is a whole document too — asking for a patch
        would need a merge, and a merge of a model's JSON into an approved shape is a
        second parser with none of the first one's refusals.

        What makes this a repair rather than a second attempt is the instruction: change
        what the complaints name and leave the rest alone, including the ten dimensions.
        Measured against the real service on 23 August 2026, that instruction is what makes
        the difference — the first version said only what was wrong, and the model rewrote
        the offending phrase without its article and left the fault exactly where it was.
        """
        return await self._again(
            ctx,
            answer=json.dumps(_without_what_is_ours(refused), ensure_ascii=False),
            complaints=complaints,
            language=language,
            experience_id=refused.experience_id,
        )

    async def repair_unreadable(
        self, ctx: AgentContext, *, answer: str, refusal: str, language: str
    ) -> Experience:
        """The same answer, for an afternoon the format would not read at all.

        There is no :class:`~shared.experience.Experience` to hand back here, only the text
        that failed to become one, so the answer goes up as it came down. The refusal is
        already written for whoever has to fix it — ``a line is 45 characters; at most 44``
        names the rule and the offending number — which is the whole reason the parser's
        messages are worded the way they are.
        """
        return await self._again(
            ctx,
            answer=answer,
            complaints=(Complaint(where="the document", says=refusal),),
            language=language,
            experience_id="",
        )

    async def _again(
        self,
        ctx: AgentContext,
        *,
        answer: str,
        complaints: Sequence[Complaint],
        language: str,
        experience_id: str,
    ) -> Experience:
        payload = await ctx.router.analyze(
            ModelRequest(
                capability=Capability.PLANNING,
                prompt=(
                    _REPAIR + f"{_FORMAT}{_RULES}"
                    f"Write every word of it in {language}.\n"
                    f"What was refused, field by field:\n"
                    + "".join(f"  {complaint}\n" for complaint in complaints)
                    + f"The afternoon: {answer}\n"
                ),
                request_id=new_request_id(),
                max_output_chars=MAX_EXPERIENCE_CHARS,
                purpose="repairing a refused afternoon",
                content_kind=ContentKind.EXERCISE_JSON,
            )
        )
        return experience_in(payload.text, experience_id=experience_id)


def _not_again(recent: Sequence[Drawn]) -> str:
    """The last few combinations, as something the next one may not be.

    An empty list says nothing at all rather than saying "avoid nothing", which is a
    sentence a model will find a way to be about.
    """
    if not recent:
        return ""
    drawn = [before.to_dict() for before in recent]
    return SAYS.text(
        "not-again",
        drawn=json.dumps(drawn, ensure_ascii=False),
        max_shared=MAX_SHARED_DIMENSIONS,
    )


def _without_what_is_ours(experience: Experience) -> dict[str, Any]:
    """The document as the model wrote it, without the three fields it did not write."""
    values = experience.to_dict()
    for ours in ("format_version", "experience_id", "requires"):
        values.pop(ours, None)
    return values


def experience_in(text: str, *, experience_id: str = "") -> Experience:
    """Parse an afternoon out of what a model said, filling in what it was not asked for."""
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        raise ExperienceError("the answer holds no object")
    try:
        parsed: Any = json.loads(text[start : end + 1])
    except ValueError as exc:
        raise ExperienceError(f"the answer is not JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ExperienceError("the answer is not an object")
    raw = parsed.get("moments", [])
    if not isinstance(raw, list):
        raise ExperienceError("moments must be a list")
    # Parsed once here to derive what the house must be able to do, and parsed again by
    # `Experience.from_dict` below. A moment that does not parse raises on this pass, which
    # is the same refusal one line earlier.
    needs = sorted({str(NEEDS[moment_from_dict(m).act]) for m in raw})
    return Experience.from_dict(
        {
            "format_version": EXPERIENCE_FORMAT_VERSION,
            # Not `shared.ids.new_id`: an experience id is a-z, 0-9 and hyphen, and the
            # house's `x_ab12` form has an underscore in it. A repair keeps the id it was
            # given, so a document refused and rewritten is the same afternoon.
            "experience_id": experience_id or f"aftn-{secrets.token_hex(4)}",
            "title": parsed.get("title", ""),
            "overview": parsed.get("overview", ""),
            "themes": parsed.get("themes", []),
            "strategy": parsed.get("strategy", ""),
            "minutes": parsed.get("minutes", 0),
            "requires": needs,
            "drawn": parsed.get("drawn"),
            "moments": raw,
        }
    )
