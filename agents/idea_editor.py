"""The parent's own idea, rewritten as they talk about it.

The parent could approve or refuse what a model devised, and nothing else. This is the
other direction, and the thing it must not become is a second deviser: it writes no plan,
no moments, no weights and no ways out. It writes the four things a parent judges an
afternoon by — title, overview, themes, script — and hands back a sentence about what it
changed.

**Everything the parent has typed reaches this prompt as material, and the prompt says so.**
That is the same rule the settings travel under, with one difference stated in
`docs/NON-GOALS.md`: here the parent is steering on purpose and watching the result, so
their words shape *this draft* and nothing else. They never become standing instructions,
they reach no other prompt, and what comes out is screened on approval like anything else.

**It never invents an afternoon whole from silence.** A blank draft and a first message is
the one case where it writes from nothing, and even then the parent is holding the pen: what
comes back is theirs to keep, type over, or throw away.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from typing import Any, Final

from shared.agents import AgentContext
from shared.experience import (
    MAX_OVERVIEW,
    MAX_SCRIPT,
    MAX_THEME,
    MAX_THEMES,
    MAX_TITLE,
    ExperienceError,
    plain,
)
from shared.ids import new_request_id
from shared.prompts import beside
from shared.routing import Capability, ModelRequest
from shared.safety import ContentKind

SAYS: Final = beside(__file__)

_INSTRUCTION: Final = SAYS.text("instruction")

_FORMAT: Final = SAYS.text(
    "format",
    max_title=MAX_TITLE,
    max_overview=MAX_OVERVIEW,
    max_themes=MAX_THEMES,
    max_theme=MAX_THEME,
    max_script=MAX_SCRIPT,
    max_reply=280,
)

# What the model may write back in the chat. Two sentences: it is a note beside the work,
# not a second place to read the idea, and a long one would be read instead of the text.
MAX_REPLY: Final = 280


class Idea:
    """What one turn produced. Not an :class:`~shared.experience.Experience` — no plan."""

    __slots__ = ("reply", "title", "overview", "themes", "script")

    def __init__(
        self,
        *,
        reply: str,
        title: str,
        overview: str,
        themes: tuple[str, ...],
        script: str,
    ) -> None:
        self.reply = reply
        self.title = title
        self.overview = overview
        self.themes = themes
        self.script = script

    def to_dict(self) -> dict[str, Any]:
        return {
            "reply": self.reply,
            "title": self.title,
            "overview": self.overview,
            "themes": list(self.themes),
            "script": self.script,
        }


def the_prompt(
    *,
    language: str,
    title: str,
    overview: str,
    themes: Sequence[str],
    script: str,
    said: Sequence[Any],
    asking: str,
) -> str:
    """The whole thing the model is sent, standing instruction and draft both.

    Its own function so that what is sent can be read without running anything, like every
    other prompt here. Everything the parent typed goes in as JSON, which is what keeps a
    sentence that looks like an instruction to the model a sentence in a draft.
    """
    return (
        f"{_INSTRUCTION}\n"
        + SAYS.text(
            "draft",
            language=language,
            title=json.dumps(title, ensure_ascii=False),
            overview=json.dumps(overview, ensure_ascii=False),
            themes=json.dumps(list(themes), ensure_ascii=False),
            script=json.dumps(script, ensure_ascii=False),
            conversation=json.dumps(
                [{"who": one.who, "words": one.words} for one in said], ensure_ascii=False
            ),
            asking=json.dumps(asking, ensure_ascii=False),
            blank="yes" if not (title or overview or script) else "no",
        )
        + _FORMAT
    )


class IdeaEditor:
    """Rewrites an idea from what the parent said. Screened by the caller."""

    name = "idea_editor"

    async def ask(
        self,
        ctx: AgentContext,
        *,
        language: str,
        title: str,
        overview: str,
        themes: Sequence[str],
        script: str,
        said: Sequence[Any],
        asking: str,
    ) -> str:
        """The answer as it came back, before anything tries to read it."""
        payload = await ctx.router.analyze(
            ModelRequest(
                capability=Capability.PLANNING,
                prompt=the_prompt(
                    language=language,
                    title=title,
                    overview=overview,
                    themes=themes,
                    script=script,
                    said=said,
                    asking=asking,
                ),
                request_id=new_request_id(),
                kind=ContentKind.TEXT,
            )
        )
        return str(payload.text or "")


def idea_in(text: str) -> Idea:
    """Read one answer. Raises :class:`ExperienceError` when it is not an idea.

    The bounds are the format's own, so a draft that passes here is a draft the deviser can
    be given and a parent can be shown. A model that writes past them is corrected by being
    refused, which the caller turns into a turn that changed nothing.
    """
    try:
        parsed = json.loads(_only_json(text))
    except (ValueError, TypeError) as exc:
        raise ExperienceError(f"the answer is not JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ExperienceError("the answer is not an object")

    reply = plain(str(parsed.get("reply") or ""), MAX_REPLY, "the reply")
    title = plain(str(parsed.get("title") or ""), MAX_TITLE, "the title")
    overview = plain(str(parsed.get("overview") or ""), MAX_OVERVIEW, "the overview")
    script = str(parsed.get("script") or "")
    if len(script) > MAX_SCRIPT:
        raise ExperienceError(f"the script is longer than {MAX_SCRIPT} characters")
    raw = parsed.get("themes") or []
    if not isinstance(raw, list):
        raise ExperienceError("the themes are a list")
    themes = tuple(plain(str(one), MAX_THEME, "a theme") for one in raw[:MAX_THEMES])
    return Idea(reply=reply, title=title, overview=overview, themes=themes, script=script)


def _only_json(text: str) -> str:
    """The object in the answer, whatever was said around it.

    A model that wraps its JSON in a fence or a sentence has still answered; refusing that
    would cost a turn to punish something nobody in the house can see.
    """
    said = text.strip()
    start = said.find("{")
    end = said.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ExperienceError("there is no object in the answer")
    return said[start : end + 1]
