"""One module per section of the panel, each holding its own routes.

The stores were separated long ago — `panel/devices.py`, `panel/themes.py`, one module per
kind of thing the panel keeps. The routes were not: on 20 August 2026 `panel/app.py` had
reached 987 lines and held every one of them, so the file that says how the application is
assembled also said what each endpoint does. Here they sit one section to a module, and
`panel/app.py` is wiring again.

Two things are shared and neither is a route. `Decision` is the body of every decision a
person records — a sign-up admitted, a proposal approved — because both are a state and a
note. And the dependencies live in `panel/gate.py` and `panel/admin.py`: a module here
imports the `Annotated` alias rather than building its own. With postponed annotations
FastAPI re-evaluates them through `get_type_hints`, which sees module scope only, so the
alias has to be a module-level name in the file where the route is written — and importing
it makes it one. A dependency that is not resolvable there is not an error: every request
to that route answers 422, which reads as the client having sent something wrong.
"""

from __future__ import annotations

from pydantic import BaseModel


class Decision(BaseModel):
    """A state and a note. Recording it is the entire effect: nothing is started."""

    state: str
    note: str = ""
