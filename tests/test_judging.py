"""Reading an afternoon back: where the verdict goes, and what it must never take with it.

Three of these are the guarantee rather than the feature. The reading must not be able to
cost a house its afternoon — not the one it reads and not the next one. The line that goes
to the workspace must carry no words. And the fingerprint that makes a prompt version
countable must be the same for two houses and contain neither of them.
"""

from __future__ import annotations

import json
import logging
import re
import time
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from agents.experience_deviser import PROMPT_FINGERPRINT
from agents.experience_judge import Verdict
from panel.app import create_app
from panel.config import Settings
from panel.experiences import InMemoryExperienceStore
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.store import InMemoryAccountStore
from panel.trail import WHAT_A_READER_MADE_OF_IT
from panel.usage import (
    KIND_JUDGE,
    KIND_TEXT,
    SERVED,
    InMemoryLimitStore,
    InMemoryUsageStore,
    UsageEvent,
    month_of,
    over_limit,
)
from shared.experience import Experience
from shared.experience_checks import Complaint

PARENT = "parent@example.test"
DEVICE_KEY = "device-key-for-tests"
THE_AFTERNOON = json.loads(
    Path("experiences/un-pomeriggio-di-nuvole.json").read_text(encoding="utf-8")
)

# Words that appear nowhere else, so finding one in a log line is proof and not a guess.
QUESTION = "quale finestra guardava chi ha scritto il biglietto"
ANSWER = "quella che dà sul cortile"
SAYS = "la risposta è già scritta nel terzo momento"


def a_verdict() -> Verdict:
    return Verdict(
        can_be_wrong=True,
        question=QUESTION,
        answer=ANSWER,
        findings=(Complaint(where="given_away: m3", says=SAYS),),
        metadata={"latency_s": 28.4, "request_id": "req-1"},
    )


def client_for() -> TestClient:
    settings = Settings(dev_auth=True, bootstrap_contact=PARENT, device_key=DEVICE_KEY)
    return TestClient(create_app(store=InMemoryAccountStore(), settings=settings))


def headers() -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: "parent-1", DEV_CONTACT_HEADER: PARENT}


def household_of(client: TestClient) -> str:
    return str(client.get("/api/me", headers=headers()).json()["householdId"])


def devising(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _devise(**_: Any) -> Any:
        return Experience.from_dict(THE_AFTERNOON), None

    monkeypatch.setattr("panel.devising.devise_experience", _devise)


def judging(monkeypatch: pytest.MonkeyPatch, outcome: Any) -> list[Any]:
    """Stand in for the cloud. ``outcome`` is a verdict to return or an exception."""
    read: list[Any] = []

    async def _judge(*, experience: Experience, now: float) -> Any:
        read.append(experience)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome, None

    monkeypatch.setattr("panel.judging.judge_experience", _judge)
    return read


def offer(client: TestClient, household: str) -> str:
    answer = client.post(
        f"/api/device/{household}/experiences",
        json={"capabilities": ["print_a4", "scan_a4", "show_800x480_1bit"]},
        headers={"X-Device-Key": DEVICE_KEY},
    )
    assert answer.status_code == 200
    return str(answer.json()["id"])


def begin(client: TestClient, household: str, offered_id: str) -> Any:
    return client.post(
        f"/api/device/{household}/experiences/{offered_id}/begun",
        json={"runId": "aft_1"},
        headers={"X-Device-Key": DEVICE_KEY},
    )


# ── Where the verdict goes ───────────────────────────────────────────────────────────


def test_every_afternoon_that_was_devised_is_read_back(monkeypatch: pytest.MonkeyPatch) -> None:
    client = client_for()
    devising(monkeypatch)
    read = judging(monkeypatch, a_verdict())
    household = household_of(client)

    offered_id = offer(client, household)

    assert [one.experience_id for one in read] == [offered_id]


def test_the_verdict_reaches_the_trail_whole_beside_the_plan_it_judges(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Whole, because a verdict summarised is a verdict somebody has already interpreted.

    Beside the plan and not beside the afternoon's own record of what it did: this is a
    reading of what was written, made before anybody had done any of it.
    """
    client = client_for()
    devising(monkeypatch)
    judging(monkeypatch, a_verdict())
    household = household_of(client)
    offered_id = offer(client, household)

    assert begin(client, household, offered_id).status_code == 200

    made = client.get("/api/trail/aft_1", headers=headers()).json()["made"]
    assert [one["kind"] for one in made] == ["plan", WHAT_A_READER_MADE_OF_IT]
    verdict = json.loads(made[1]["body"])
    assert verdict["question"] == QUESTION
    assert verdict["answer"] == ANSWER
    assert verdict["findings"] == [{"where": "given_away: m3", "says": SAYS}]
    # Which prompt wrote the afternoon this reads. Nothing said it before, so two records
    # from either side of a prompt change looked the same.
    assert verdict["prompt"] == PROMPT_FINGERPRINT
    # The question first, because an afternoon whose question a reader could not state is
    # the loudest thing this produces and it should not need opening to be seen.
    assert made[1]["heading"] == QUESTION


def test_the_verdict_is_behind_the_parents_login(monkeypatch: pytest.MonkeyPatch) -> None:
    client = client_for()
    devising(monkeypatch)
    judging(monkeypatch, a_verdict())
    household = household_of(client)
    begin(client, household, offer(client, household))

    assert client.get("/api/trail/aft_1").status_code != 200


def test_a_house_cannot_file_a_verdict_about_itself() -> None:
    """It performs acts. A house that could file one could say its own plan was read and
    found sound, and the record would stop saying who wrote what."""
    client = client_for()
    household = household_of(client)

    answer = client.post(
        f"/api/device/{household}/trail/aft_1",
        json={"kind": WHAT_A_READER_MADE_OF_IT},
        headers={"X-Device-Key": DEVICE_KEY},
    )

    assert answer.status_code == 400


def test_a_reading_that_could_not_be_made_costs_the_afternoon_nothing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The afternoon was devised, screened, stored and paid for before this ran."""
    client = client_for()
    devising(monkeypatch)
    judging(monkeypatch, RuntimeError("the cloud is not there"))
    household = household_of(client)

    offered_id = offer(client, household)

    assert begin(client, household, offered_id).status_code == 200
    made = client.get("/api/trail/aft_1", headers=headers()).json()["made"]
    assert [one["kind"] for one in made] == ["plan"]


# ── The page that exists while the prompts are being changed ─────────────────────────


def test_the_readings_page_carries_the_whole_verdict_and_unpacks_the_finding(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`agents/experience_judge.py` keeps the finding name inside `where`, ahead of a
    colon, because `Complaint` is what a repair loop consumes. Splitting it on this side of
    the wire keeps that encoding out of the browser."""
    client = client_for()
    devising(monkeypatch)
    judging(monkeypatch, a_verdict())
    household = household_of(client)
    offered_id = offer(client, household)

    rows = client.get("/api/verdicts", headers=headers()).json()["verdicts"]

    assert [one["experienceId"] for one in rows] == [offered_id]
    assert rows[0]["question"] == QUESTION
    assert rows[0]["answer"] == ANSWER
    assert rows[0]["prompt"] == PROMPT_FINGERPRINT
    assert rows[0]["findings"] == [
        {"name": "given_away", "where": "m3", "says": SAYS}
    ]
    # Before it is decided on, which is the whole reason this page exists and also the
    # reason it is temporary. `panel/routes/verdicts.py` says so.
    assert rows[0]["state"] == "pending"


def test_the_readings_page_is_behind_the_parents_login() -> None:
    client = client_for()

    assert client.get("/api/verdicts").status_code != 200


def test_an_afternoon_nobody_read_is_not_on_the_readings_page(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = client_for()
    devising(monkeypatch)
    judging(monkeypatch, RuntimeError("the cloud is not there"))
    household = household_of(client)
    offer(client, household)

    assert client.get("/api/verdicts", headers=headers()).json()["verdicts"] == []


# ── What it may cost ─────────────────────────────────────────────────────────────────


def test_a_judgement_is_counted_like_every_other_call() -> None:
    """It is not free and the month must not pretend it is: the figures are what says
    whether this container's count agrees with what Azure charges."""
    usage = InMemoryUsageStore()
    for n in range(3):
        usage.record(
            UsageEvent(id=f"j{n}", household_id="hh_1", at=0.0, kind=KIND_JUDGE, outcome=SERVED)
        )

    assert usage.summary("hh_1", "1970-01").by_kind[KIND_JUDGE].billed_calls == 3
    assert over_limit(usage, "hh_1", 3, now=0.0)


def test_a_house_at_its_limit_is_not_read_back_at_all(monkeypatch: pytest.MonkeyPatch) -> None:
    """The two halves that keep a reading from ever refusing an afternoon. Its own is safe
    because this runs after that one is stored; the next one is safe because a household
    already at its limit is not read back, so the reading cannot be the call that crosses.

    What it costs is small enough to write down: a reading is at most one per devised
    afternoon, and `panel/usage.py` counts an ordinary month at 1302 calls of which
    devising is the rarest path, so the month reaches its limit at most a few per cent
    sooner than it would have.
    """
    import asyncio

    from panel.judging import judged_and_filed

    usage = InMemoryUsageStore()
    usage.record(
        UsageEvent(id="t0", household_id="hh_1", at=time.time(), kind=KIND_TEXT, outcome=SERVED)
    )
    read = judging(monkeypatch, a_verdict())

    asyncio.run(
        judged_and_filed(
            experiences=InMemoryExperienceStore(),
            usage=usage,
            limits=InMemoryLimitStore(),
            configured=1,
            household_id="hh_1",
            experience=Experience.from_dict(THE_AFTERNOON),
        )
    )

    assert read == []
    assert usage.summary("hh_1", month_of(time.time())).by_kind[KIND_JUDGE].calls == 0


def test_the_reading_is_never_awaited_inside_the_reply_to_the_house() -> None:
    """A devise takes 120-180 s measured and the ingress gives up at 240, so a reading of
    about 30 s inside the same reply spends the margin that belongs to the afternoon.

    Read off the source because there is no way to observe it from a test client: the
    client runs background tasks before it hands the response back.
    """
    import ast

    source = Path("panel/routes/experience.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    awaited = {
        node.value.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Await)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
    }
    assert "judged_and_filed" not in awaited
    assert "add_task" in {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }


# ── What may leave the container ─────────────────────────────────────────────────────


def test_the_line_in_the_workspace_carries_ids_and_counts_and_no_words(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """`panel/observability.py`: nothing in this container may log what a model wrote for a
    particular person. A finding name is ours, from a closed list; the words beside it are
    not."""
    import asyncio

    from panel.judging import SAID, judged_and_filed

    experience = Experience.from_dict(THE_AFTERNOON)
    judging(monkeypatch, a_verdict())

    with caplog.at_level(logging.INFO, logger="panel.judging"):
        asyncio.run(
            judged_and_filed(
                experiences=InMemoryExperienceStore(),
                usage=InMemoryUsageStore(),
                limits=InMemoryLimitStore(),
                configured=0,
                household_id="hh_1",
                experience=experience,
            )
        )

    written = [one.getMessage() for one in caplog.records]
    said = [one for one in written if one.startswith(SAID)]
    assert len(said) == 1, written
    line = json.loads(said[0][len(SAID) :])
    assert line["household"] == "hh_1"
    assert line["experience"] == experience.experience_id
    assert line["findings"] == ["given_away"]
    assert line["latencyS"] == 28.4
    assert len(line["prompt"]) == 12
    whole = "\n".join(written)
    for word in (QUESTION, ANSWER, SAYS, experience.title, experience.overview):
        assert word not in whole
        # And the form `json.dumps` writes it in. This assertion is not decoration: with
        # only the line above, a leak of "quella che dà sul cortile" went undetected,
        # because the default escaping turns the à into \u00e0 and the substring stops
        # matching. Italian afternoons are full of accents, so the plain check alone would
        # have been blind to most of what it is guarding.
        assert json.dumps(word)[1:-1] not in whole


def test_the_verdict_kept_is_the_verdict_read(monkeypatch: pytest.MonkeyPatch) -> None:
    """The store keeps what the judge said, unedited, so the trail can hand it over whole."""
    import asyncio

    from panel.experiences import OfferedExperience
    from panel.judging import judged_and_filed

    experience = Experience.from_dict(THE_AFTERNOON)
    experiences = InMemoryExperienceStore()
    experiences.offer(
        OfferedExperience(
            id=experience.experience_id,
            household_id="hh_1",
            experience=experience.to_dict(),
            created_at=0.0,
        )
    )
    usage = InMemoryUsageStore()
    judging(monkeypatch, a_verdict())

    asyncio.run(
        judged_and_filed(
            experiences=experiences,
            usage=usage,
            limits=InMemoryLimitStore(),
            configured=0,
            household_id="hh_1",
            experience=experience,
        )
    )

    kept = experiences.get("hh_1", experience.experience_id)
    assert kept is not None
    assert kept.verdict == {"prompt": PROMPT_FINGERPRINT, **a_verdict().to_dict()}
    # And not in what a parent reads while deciding. See the docstring of `to_public`.
    assert "verdict" not in kept.to_public()
    read = usage.summary("hh_1", month_of(time.time())).by_kind[KIND_JUDGE]
    assert (read.calls, read.billed_calls) == (1, 1)


def test_a_reading_that_failed_is_still_counted(monkeypatch: pytest.MonkeyPatch) -> None:
    """It reached the model or it did not, and the month has to be able to say which."""
    import asyncio

    from panel.judging import judged_and_filed

    usage = InMemoryUsageStore()
    judging(monkeypatch, RuntimeError("the cloud is not there"))

    asyncio.run(
        judged_and_filed(
            experiences=InMemoryExperienceStore(),
            usage=usage,
            limits=InMemoryLimitStore(),
            configured=0,
            household_id="hh_1",
            experience=Experience.from_dict(THE_AFTERNOON),
        )
    )

    read = usage.summary("hh_1", month_of(time.time())).by_kind[KIND_JUDGE]
    assert (read.calls, read.billed_calls) == (1, 0)


# ── Which prompt wrote it ────────────────────────────────────────────────────────────


def test_the_fingerprint_covers_every_block_this_agent_can_send() -> None:
    """A block added and forgotten here would make a prompt change invisible in the counts,
    which is the one thing the fingerprint exists to prevent."""
    import agents.experience_deviser as deviser

    covered = deviser.what_is_not_about_a_house()
    stem = Path(deviser.__file__).with_suffix("")
    for path in sorted(stem.parent.glob(f"{stem.name}.*.md")):
        name = path.name.split(".")[1]
        block = deviser.SAYS.text(name)
        # The longest run of the block that holds no placeholder, so a block that reaches
        # the text with its numbers filled in still counts as covered.
        longest = max(re.split(r"\$\w+", block), key=len)[:80]
        assert longest in covered, f"{name} is not in the fingerprint"


def test_the_fingerprint_holds_nothing_about_a_house() -> None:
    """It goes to a workspace. `panel/observability.py` says what may not."""
    import agents.experience_deviser as deviser

    covered = deviser.what_is_not_about_a_house()
    note = "il nonno è morto tre settimane fa"
    with_a_house = deviser.the_prompt(
        language="italiano",
        capabilities=frozenset(),
        interests=("le nuvole",),
        note=note,
        already=("Il quaderno del vento",),
    )

    assert note in with_a_house
    assert note not in covered
    assert "le nuvole" not in covered
    assert "Il quaderno del vento" not in covered
    assert len(deviser.PROMPT_FINGERPRINT) == 12
    assert deviser.PROMPT_FINGERPRINT == deviser.PROMPT_FINGERPRINT
