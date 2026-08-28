"""What the system wrote, kept; what the adolescent did, not kept.

The asymmetry is the whole feature, so it is what the tests are about. Two of them are the
guarantee and would be the ones to break first if somebody added a field in good faith: the
record has no vocabulary for a person, and what a house sends about a page that came back is
not in the trail even though the generation it caused is.
"""

from __future__ import annotations

import json
import time
from dataclasses import fields
from pathlib import Path
from typing import Any

import afternoons as a
import pytest
from fastapi.testclient import TestClient

from agents.experience_agent import Move
from panel.app import create_app
from panel.config import Settings
from panel.keeping import KEPT_FOR_SECONDS, InMemoryKeepingStore, granted
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.store import InMemoryAccountStore
from panel.trail import (
    WHAT_CAME_BACK,
    WHAT_COMES_AFTER,
    InMemoryTrailStore,
    Made,
    Trail,
    clipped,
)
from shared.capabilities import WENT_WRONG, Act

PARENT = "parent@example.test"
DEVICE_KEY = "device-key-for-tests"
THE_AFTERNOON = json.loads(
    Path("experiences/un-pomeriggio-di-nuvole.json").read_text(encoding="utf-8")
)


def client_for() -> TestClient:
    settings = Settings(dev_auth=True, bootstrap_contact=PARENT, device_key=DEVICE_KEY)
    return TestClient(create_app(store=InMemoryAccountStore(), settings=settings))


def headers() -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: "parent-1", DEV_CONTACT_HEADER: PARENT}


def household_of(client: TestClient) -> str:
    return str(client.get("/api/me", headers=headers()).json()["householdId"])


def moving(monkeypatch: pytest.MonkeyPatch, move: Move) -> None:
    async def _decide(**_: Any) -> Any:
        return move, None

    monkeypatch.setattr("panel.moving.decide_a_move", _decide)


def ask_for_a_move(client: TestClient, household: str, **changes: Any) -> Any:
    body: dict[str, Any] = {
        "experience": THE_AFTERNOON | {"script": "find out who left the ledger"},
        "happened": [],
        "minutesLeft": 40,
        "runId": "aft_1",
    }
    body.update(changes)
    return client.post(
        f"/api/device/{household}/next-move",
        json=body,
        headers={"X-Device-Key": DEVICE_KEY},
    )


# ── The record itself ────────────────────────────────────────────────────────────────


def test_nothing_in_the_record_can_be_about_a_person() -> None:
    """The two shapes, field by field. Every one of them is about a machine or a clock.

    This is the guarantee, and it is a list rather than a principle because a principle does
    not fail when somebody adds `howFar` to a dataclass in good faith.

    `until` is the one field that exists for the exception in `panel/keeping.py`, and it is
    about a clock: it says when a row stops being kept, not anything about whom it concerns.
    """
    about_the_run = {"id", "household_id", "run_id", "at", "experience_id", "began_at"}
    about_what_was_written = {"kind", "heading", "body", "why", "picture_id", "paper"}
    about_how_long_it_is_kept = {"until"}
    about_the_afternoon = {"title", "overview", "script", "made"}
    allowed = (
        about_the_run
        | about_what_was_written
        | about_how_long_it_is_kept
        | about_the_afternoon
    )

    held = {row.name for row in fields(Made)} | {row.name for row in fields(Trail)}

    assert held <= allowed


def test_a_long_body_is_kept_short_rather_than_lost() -> None:
    assert len(clipped("x" * 40_000)) == 20_000
    assert clipped("short") == "short"


def test_one_run_opens_one_trail() -> None:
    """A house that retries must not leave a parent two cards for one afternoon."""
    store = InMemoryTrailStore()
    first = Trail("aft_1", "h1", "e1", "Le nuvole", "una sintesi", 100.0, script="il copione")

    store.began(first)
    store.began(Trail("aft_1", "h1", "e1", "Altro", "altra", 200.0, script="altro copione"))

    assert [row.title for row in store.list("h1")] == ["Le nuvole"]
    kept = store.get("h1", "aft_1")
    assert kept is not None and kept.script == "il copione"


def test_the_cards_come_newest_first_and_without_their_scripts() -> None:
    store = InMemoryTrailStore()
    store.began(Trail("aft_1", "h1", "e1", "Prima", "", 100.0, script="il copione"))
    store.began(Trail("aft_2", "h1", "e2", "Dopo", "", 200.0, script="un altro"))

    cards = store.list("h1")

    assert [row.title for row in cards] == ["Dopo", "Prima"]
    assert [row.script for row in cards] == ["", ""]


def test_what_was_written_comes_back_in_the_order_it_was_written() -> None:
    store = InMemoryTrailStore()
    store.began(Trail("aft_1", "h1", "e1", "Le nuvole", "", 100.0))
    store.wrote(Made("m2", "h1", "aft_1", 120.0, str(Act.HAND_OVER), body="un foglio"))
    store.wrote(Made("m1", "h1", "aft_1", 110.0, str(Act.SAY), body="Guarda fuori."))

    found = store.get("h1", "aft_1")

    assert found is not None
    assert [one.body for one in found.made] == ["Guarda fuori.", "un foglio"]


def test_one_household_cannot_see_another() -> None:
    store = InMemoryTrailStore()
    store.began(Trail("aft_1", "h1", "e1", "Le nuvole", "", 100.0))

    assert store.list("h2") == []
    assert store.get("h2", "aft_1") is None


# ── What the routes put in it ────────────────────────────────────────────────────────


def test_a_move_is_filed_under_the_afternoon_it_was_written_for(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    moving(
        monkeypatch,
        Move(act=Act.SAY, why="the page came back blank", lines=("Guarda fuori.",)),
    )
    household = household_of(client)

    assert ask_for_a_move(client, household).status_code == 200

    cards = client.get("/api/trail", headers=headers()).json()["trails"]
    assert [row["runId"] for row in cards] == ["aft_1"]
    whole = client.get("/api/trail/aft_1", headers=headers()).json()
    assert whole["script"] == "find out who left the ledger"
    assert whole["made"][0]["kind"] == "say"
    assert whole["made"][0]["body"] == "Guarda fuori."
    assert whole["made"][0]["why"] == "the page came back blank"


def test_a_page_is_kept_as_the_words_that_are_on_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The sheet, readable, and not the JSON it arrived as.

    It used to go into the body as the document a model wrote, which was a record nobody
    could read: a parent opening an afternoon wants the page, and braces round a title are
    our storage showing through.
    """
    client = client_for()
    moving(
        monkeypatch,
        Move(
            act=Act.HAND_OVER,
            why="the plan asked for one",
            heading="Le nuvole",
            lines=("Prendi il foglio.",),
            page={
                "kind": "notebook",
                "title": "Le nuvole",
                "illustration": "una finestra su un cielo bianco",
                "note": ["Guarda il cielo e scrivi quello che sembra."],
                "spaces": [{"label": "La prima nuvola", "room": "a_box"}],
            },
        ),
    )
    household = household_of(client)

    ask_for_a_move(client, household)

    made = client.get("/api/trail/aft_1", headers=headers()).json()["made"][0]
    assert made["heading"] == "Le nuvole"
    assert made["body"] == "Prendi il foglio."
    assert made["paper"].splitlines() == [
        "Le nuvole",
        "Guarda il cielo e scrivi quello che sembra.",
        "— La prima nuvola",
        "(una finestra su un cielo bianco)",
    ]


def test_a_page_this_container_cannot_read_is_kept_anyway(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A record that drops what it could not parse is the worse of the two failures."""
    client = client_for()
    moving(
        monkeypatch,
        Move(
            act=Act.HAND_OVER,
            why="the plan asked for one",
            page={"title": "Le nuvole", "cells": [{"label": "Disegnala qui"}]},
        ),
    )
    household = household_of(client)

    ask_for_a_move(client, household)

    made = client.get("/api/trail/aft_1", headers=headers()).json()["made"][0]
    assert json.loads(made["paper"])["cells"] == [{"label": "Disegnala qui"}]


def test_several_moves_stack_up_under_one_afternoon(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    moving(monkeypatch, Move(act=Act.SAY, why="one", lines=("Uno.",)))
    household = household_of(client)

    ask_for_a_move(client, household)
    moving(monkeypatch, Move(act=Act.CLOSE, why="two", lines=("Due.",)))
    ask_for_a_move(client, household)

    whole = client.get("/api/trail/aft_1", headers=headers()).json()
    assert [one["kind"] for one in whole["made"]] == ["say", "close"]
    assert len(client.get("/api/trail", headers=headers()).json()["trails"]) == 1


def test_a_house_that_names_no_run_still_gets_its_move(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The trail is a record, not a gate. A house that predates it is not turned away."""
    client = client_for()
    moving(monkeypatch, Move(act=Act.SAY, why="x", lines=("Uno.",)))
    household = household_of(client)

    assert ask_for_a_move(client, household, runId="").status_code == 200

    assert client.get("/api/trail", headers=headers()).json()["trails"] == []


def test_what_came_back_off_the_glass_is_not_in_the_trail(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The continuation it caused is kept. What caused it is not, and nothing here can hold it.

    A house posts a reading of a page — where the ink was, what the marks say. That is the
    adolescent's half, and the trail records the system's half only.
    """
    from shared.experience import Continuation

    client = client_for()
    rest: dict[str, Any] = {
        "format_version": 2,
        "experience_id": "un-pomeriggio-di-nuvole",
        "after": "l-ultimo-foglio",
        "moments": [
            a.close(
                moment_id="due-nuvole",
                heading="Due nuvole",
                weights=a.weights(lines=("Il foglio resta sul tavolo.",)),
            )
        ],
    }

    async def _continue(**_: Any) -> Any:
        return Continuation.from_dict(rest), None

    monkeypatch.setattr("panel.continuing.continue_experience", _continue)
    household = household_of(client)

    client.post(
        f"/api/device/{household}/experience",
        json={
            "experience": THE_AFTERNOON,
            "after": "l-ultimo-foglio",
            "came": "marks",
            "reading": {
                "cells": [
                    {"cell_id": "la-nuvola", "label": "Disegnala qui", "value": "un cavallo"}
                ]
            },
            "runId": "aft_1",
        },
        headers={"X-Device-Key": DEVICE_KEY},
    )

    whole = client.get("/api/trail/aft_1", headers=headers()).json()
    assert [one["kind"] for one in whole["made"]] == [WHAT_COMES_AFTER]
    assert "un cavallo" not in json.dumps(whole)
    assert "Due nuvole" in whole["made"][0]["body"]


def test_an_afternoon_nobody_ran_is_not_there() -> None:
    client = client_for()
    household_of(client)

    assert client.get("/api/trail/aft_9", headers=headers()).status_code == 404


# ── An afternoon that ran the whole way on its own plan ──────────────────────────────


def offer_and_begin(client: TestClient, household: str) -> Any:
    """Have one devised and then have the house say it began, which is what a real run does."""
    devised = client.post(
        f"/api/device/{household}/experiences",
        json={"capabilities": ["print_a4", "scan_a4", "show_800x480_1bit"]},
        headers={"X-Device-Key": DEVICE_KEY},
    )
    offered_id = devised.json()["id"]
    return client.post(
        f"/api/device/{household}/experiences/{offered_id}/begun",
        json={"runId": "aft_1"},
        headers={"X-Device-Key": DEVICE_KEY},
    )


def test_the_trail_opens_when_the_house_says_it_began(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It opened on the first generation, and an afternoon that never needed one left no
    record at all. Measured in a real house on 26 August 2026: it ran start to finish and
    the parent's page was empty."""
    client = client_for()

    async def _devise(**_: Any) -> Any:
        from shared.experience import Experience

        return Experience.from_dict(THE_AFTERNOON | {"script": "il copione"}), None

    monkeypatch.setattr("panel.devising.devise_experience", _devise)
    household = household_of(client)

    assert offer_and_begin(client, household).status_code == 200

    cards = client.get("/api/trail", headers=headers()).json()["trails"]
    assert [row["runId"] for row in cards] == ["aft_1"]
    whole = client.get("/api/trail/aft_1", headers=headers()).json()
    assert whole["script"] == "il copione"
    # The plan as written, so that what the house then did can be read against it.
    assert whole["made"][0]["kind"] == "plan"
    assert "l-ultimo-foglio" in whole["made"][0]["body"]


def test_the_house_files_what_it_put_in_the_room(monkeypatch: pytest.MonkeyPatch) -> None:
    """What the panel generated and what reached the room are different facts.

    A page a printer never took is a generation that happened and an act that did not, so
    the parent is shown both under one afternoon.
    """
    client = client_for()

    async def _devise(**_: Any) -> Any:
        from shared.experience import Experience

        return Experience.from_dict(THE_AFTERNOON), None

    monkeypatch.setattr("panel.devising.devise_experience", _devise)
    household = household_of(client)
    offer_and_begin(client, household)

    answer = client.post(
        f"/api/device/{household}/trail/aft_1",
        json={
            "kind": "say",
            "heading": "Guarda fuori",
            "lines": ["Che forma ha?"],
            "why": "standard",
        },
        headers={"X-Device-Key": DEVICE_KEY},
    )

    assert answer.status_code == 200
    made = client.get("/api/trail/aft_1", headers=headers()).json()["made"]
    assert [one["kind"] for one in made] == ["plan", "say"]
    assert made[1]["heading"] == "Guarda fuori"
    assert made[1]["body"] == "Che forma ha?"


def test_a_house_cannot_claim_to_have_written_the_plan() -> None:
    """It performs acts and nothing else. Filing a `plan` would be claiming to have
    written one, and the record would stop saying who did what."""
    client = client_for()
    household = household_of(client)

    for kind in ("plan", "continuation", "invented", "came"):
        answer = client.post(
            f"/api/device/{household}/trail/aft_1",
            json={"kind": kind},
            headers={"X-Device-Key": DEVICE_KEY},
        )
        assert answer.status_code == 400, kind


def test_a_house_may_say_what_it_could_not_do() -> None:
    """Not an act and not a person: an afternoon that quietly did less than its plan used
    to be visible only in the journal on the house, where no parent is reading."""
    client = client_for()
    household = household_of(client)

    answer = client.post(
        f"/api/device/{household}/trail/aft_1",
        json={
            "kind": WENT_WRONG,
            "heading": "Le nuvole",
            "lines": ["no page reached the table"],
        },
        headers={"X-Device-Key": DEVICE_KEY},
    )

    assert answer.status_code == 200


def test_the_house_files_the_sheet_that_came_out_of_the_printer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A page is generated like everything else, and until now the only place it survived
    was inside the plan's JSON."""
    client = client_for()

    async def _devise(**_: Any) -> Any:
        from shared.experience import Experience

        return Experience.from_dict(THE_AFTERNOON), None

    monkeypatch.setattr("panel.devising.devise_experience", _devise)
    household = household_of(client)
    offer_and_begin(client, household)

    client.post(
        f"/api/device/{household}/trail/aft_1",
        json={
            "kind": "hand_over",
            "heading": "Le nuvole",
            "lines": ["Prendi il foglio."],
            "page": {
                "kind": "notebook",
                "title": "Le nuvole",
                "illustration": "una finestra",
                "note": [],
                "spaces": [{"label": "La prima", "room": "a_line"}],
            },
        },
        headers={"X-Device-Key": DEVICE_KEY},
    )

    made = client.get("/api/trail/aft_1", headers=headers()).json()["made"]
    assert made[1]["paper"].splitlines() == ["Le nuvole", "— La prima", "(una finestra)"]


def test_a_continuation_the_checks_refused_is_in_the_record(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The afternoon carried on from its written plan and the parent's page said nothing
    had happened. What was paid for and refused is what a record of a machine is for."""
    from panel.devising import RefusedByTheChecks

    async def _continue(**_: Any) -> Any:
        raise RefusedByTheChecks(
            ["this way out is about 'il registro' and never says so"]
        )

    monkeypatch.setattr("panel.continuing.continue_experience", _continue)
    client = client_for()
    household = household_of(client)

    answer = client.post(
        f"/api/device/{household}/experience",
        json={
            "experience": THE_AFTERNOON,
            "after": "l-ultimo-foglio",
            "came": "marks",
            "reading": {"cells": []},
            "runId": "aft_1",
        },
        headers={"X-Device-Key": DEVICE_KEY},
    )

    assert answer.status_code == 422
    made = client.get("/api/trail/aft_1", headers=headers()).json()["made"]
    assert [one["kind"] for one in made] == [WENT_WRONG]
    assert "never says so" in made[0]["body"]


# ── The one half that is kept only while somebody is building this ───────────────────


def continued(client: TestClient, household: str) -> Any:
    return client.post(
        f"/api/device/{household}/experience",
        json={
            "experience": THE_AFTERNOON,
            "after": "l-ultimo-foglio",
            "came": "marks",
            "reading": {
                "describes": ["un cavallo nel terzo riquadro"],
                "written": True,
            },
            "runId": "aft_1",
        },
        headers={"X-Device-Key": DEVICE_KEY},
    )


def a_continuation(monkeypatch: pytest.MonkeyPatch) -> None:
    from shared.experience import Continuation

    rest: dict[str, Any] = {
        "format_version": 2,
        "experience_id": "un-pomeriggio-di-nuvole",
        "after": "l-ultimo-foglio",
        "moments": [
            a.close(
                moment_id="due-nuvole",
                heading="Due nuvole",
                weights=a.weights(lines=("Il foglio resta sul tavolo.",)),
            )
        ],
    }

    async def _continue(**_: Any) -> Any:
        return Continuation.from_dict(rest), None

    monkeypatch.setattr("panel.continuing.continue_experience", _continue)


def test_a_household_nobody_turned_on_keeps_nothing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The default, and what every household in production is."""
    a_continuation(monkeypatch)
    client = client_for()
    household = household_of(client)

    continued(client, household)

    whole = client.get("/api/trail/aft_1", headers=headers()).json()
    assert [one["kind"] for one in whole["made"]] == [WHAT_COMES_AFTER]
    assert "un cavallo" not in json.dumps(whole)


def test_a_household_being_worked_on_keeps_the_other_half(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    a_continuation(monkeypatch)
    client = client_for()
    household = household_of(client)
    client.app.state.keeping.set(  # type: ignore[attr-defined]
        granted(household, by="admin-1", now=time.time())
    )

    continued(client, household)

    made = client.get("/api/trail/aft_1", headers=headers()).json()["made"]
    assert [one["kind"] for one in made] == [WHAT_CAME_BACK, WHAT_COMES_AFTER]
    assert "un cavallo" in made[0]["body"]
    assert made[0]["until"] > time.time()


def test_what_was_kept_while_building_deletes_itself_when_the_permission_lapses(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Deleted, not filtered. A row that is merely left out of an answer is still a row."""
    a_continuation(monkeypatch)
    client = client_for()
    household = household_of(client)
    store = client.app.state.keeping  # type: ignore[attr-defined]
    store.set(granted(household, by="admin-1", now=time.time() - KEPT_FOR_SECONDS + 60))

    continued(client, household)
    trail = client.app.state.trail  # type: ignore[attr-defined]
    assert [one.kind for one in trail.get(household, "aft_1").made] == [
        WHAT_CAME_BACK,
        WHAT_COMES_AFTER,
    ]

    # The permission lapses a minute later, and so does everything it let through.
    store.set(granted(household, by="admin-1", now=time.time() - KEPT_FOR_SECONDS - 1))
    later = time.time() + KEPT_FOR_SECONDS
    monkeypatch.setattr("panel.trail.time.time", lambda: later)

    assert [one.kind for one in trail.get(household, "aft_1").made] == [WHAT_COMES_AFTER]


def test_a_permission_that_lapsed_is_off_and_forgotten() -> None:
    store = InMemoryKeepingStore()
    store.set(granted("h1", by="admin-1", now=time.time() - KEPT_FOR_SECONDS - 1))

    found = store.get("h1")

    assert not found.standing(time.time())
    assert found.set_by == ""


def test_the_permission_is_the_administrator_s_and_not_the_parent_s() -> None:
    """The parent's token reaches no route that mentions it, and no page they see does."""
    client = client_for()
    household = household_of(client)

    answer = client.post(
        f"/api/admin/households/{household}/keeping",
        json={"keeping": True},
        headers=headers(),
    )

    assert answer.status_code == 503


def test_filing_what_was_done_carries_no_field_for_a_reading() -> None:
    """The shape is closed, so a house that tried would be refused rather than stored."""
    client = client_for()
    household = household_of(client)

    answer = client.post(
        f"/api/device/{household}/trail/aft_1",
        json={"kind": "collect", "reading": {"cells": [{"value": "un cavallo"}]}},
        headers={"X-Device-Key": DEVICE_KEY},
    )

    assert answer.status_code == 422


def test_the_trail_is_read_by_a_parent_and_not_by_a_device() -> None:
    """A device key opens the recording routes and none of the reading ones."""
    client = client_for()

    assert client.get("/api/trail", headers={"X-Device-Key": DEVICE_KEY}).status_code != 200
