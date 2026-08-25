"""How what a parent said reaches an afternoon that is already running.

`shared/message.py` says what may be said and `devices/run_experience.hear` applies it.
Neither of them says how it gets there, and this is that: a row the panel holds, and the
house coming for it on the look it already makes.

The claims worth holding down are the ones the rules are made of, and each fails on an
implementation that looks right. There is nowhere to put a sentence. The press writes a row
and spends nothing. The house gets it because it asked, and says which one it heard, so a
message written in the meantime survives. And the whole way through, nothing is drawn.

One of them cannot be tested here and is stated rather than asserted: the store the panel
runs on has to outlive the process, because the container app scales to zero between a
parent pressing and the house asking ten minutes later. `InMemoryMessageStore` is the twin
these tests use; `panel.cosmos_store.CosmosMessageStore` is what runs.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from devices import afternoon as house_timer
from devices import pretend as simulated
from devices.house import House
from devices.run_experience import Afternoon, begin
from panel.app import create_app
from panel.config import Settings
from panel.messages import MESSAGE_LIFETIME_SECONDS, InMemoryMessageStore, clean_message
from panel.principal import DEV_CONTACT_HEADER, DEV_SUBJECT_HEADER
from panel.store import InMemoryAccountStore
from panel.usage import InMemoryUsageStore
from shared.experience import Experience
from shared.message import MessageError, Says

PARENT = "parent@example.test"
DEVICE_KEY = "device-key-for-tests"
THE_AFTERNOON = Path("experiences/un-pomeriggio-di-nuvole.json")
THE_TIMER = Path("deploy/lanternina-afternoon.timer")
# A moment in the middle of an afternoon, named by the calendar rather than asserted. It is
# the clock the runs are played against; anything that goes through the store's own hour of
# life is written from the running clock instead, or it ages out of being offered.
WHEN = time.mktime((2026, 8, 24, 14, 0, 0, 0, 0, -1))


@pytest.fixture
def store() -> InMemoryMessageStore:
    return InMemoryMessageStore()


@pytest.fixture
def counter() -> InMemoryUsageStore:
    return InMemoryUsageStore()


@pytest.fixture
def client(store: InMemoryMessageStore, counter: InMemoryUsageStore) -> TestClient:
    settings = Settings(dev_auth=True, bootstrap_contact=PARENT, device_key=DEVICE_KEY)
    return TestClient(
        create_app(
            store=InMemoryAccountStore(),
            settings=settings,
            messages=store,
            usage=counter,
        )
    )


def headers() -> dict[str, str]:
    return {DEV_SUBJECT_HEADER: "parent-1", DEV_CONTACT_HEADER: PARENT}


def as_the_house() -> dict[str, str]:
    return {"X-Device-Key": DEVICE_KEY}


def household_of(client: TestClient) -> str:
    return str(client.get("/api/me", headers=headers()).json()["householdId"])


def a_house(tmp_path: Path, household: str = "") -> House:
    return House(
        sheets_dir=tmp_path / "state",
        pretend=tmp_path / "pretend",
        household=household,
        device_key=DEVICE_KEY,
    )


def an_afternoon_under_way(house: House) -> None:
    begin(
        house,
        Experience.from_dict(json.loads(THE_AFTERNOON.read_text(encoding="utf-8"))),
        now=WHEN,
        send=False,
    )


def running(house: House) -> Afternoon:
    path = sorted((house.sheets_dir / "afternoons").glob("*.json"))[0]
    return Afternoon.from_dict(json.loads(path.read_text(encoding="utf-8")))


def screens(house: House) -> int:
    pretending = house.pretending
    assert pretending is not None
    return len(
        [line for line in simulated.read_transcript(pretending) if line["what"] == "display"]
    )


def through(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    """Point the house's two calls at this panel, so the whole channel is exercised."""

    def get(url: str, key: str, timeout: int) -> Any:
        answer = client.get(url, headers={"X-Device-Key": key})
        answer.raise_for_status()
        return answer.json()

    def post(url: str, key: str, body: dict[str, Any], timeout: int) -> Any:
        answer = client.post(url, json=body, headers={"X-Device-Key": key})
        answer.raise_for_status()
        return answer.json()

    monkeypatch.setattr(house_timer, "_get", get)
    monkeypatch.setattr(house_timer, "_post", post)


# ── There is nowhere to put a sentence ───────────────────────────────────────────────


def test_a_sentence_cannot_be_sent_at_all(client: TestClient) -> None:
    """The defence against free text is not screening it. It is having no field for it."""
    answer = client.post(
        "/api/message", json={"says": "he is being lazy, push him"}, headers=headers()
    )

    assert answer.status_code == 400
    assert "not something a parent may say" in answer.json()["detail"]


def test_a_note_beside_a_message_is_refused_by_the_body(client: TestClient) -> None:
    """Refused on both sides of the API, so the field cannot be added to one of them."""
    answer = client.post(
        "/api/message",
        json={"says": "close_now", "note": "she seems tired"},
        headers=headers(),
    )

    assert answer.status_code == 422


def test_an_hour_that_is_not_on_the_clock_is_refused(client: TestClient) -> None:
    answer = client.post(
        "/api/message", json={"says": "end_by", "at": "25:00"}, headers=headers()
    )

    assert answer.status_code == 400


def test_the_route_takes_the_hour_the_parent_chose(client: TestClient) -> None:
    """"HH:MM" on the wire, minutes past midnight in the house. The arithmetic is on this
    side, which is where the parent's own unit stops."""
    answer = client.post(
        "/api/message", json={"says": "end_by", "at": "17:30"}, headers=headers()
    )

    assert answer.status_code == 200
    assert answer.json()["minutes"] == 17 * 60 + 30


def test_the_store_refuses_what_the_vocabulary_does_not_carry() -> None:
    with pytest.raises(MessageError):
        clean_message("h1", says="pause")


# ── The press is inert ───────────────────────────────────────────────────────────────


def test_the_press_writes_a_row_and_spends_nothing(
    client: TestClient, store: InMemoryMessageStore, counter: InMemoryUsageStore
) -> None:
    household = household_of(client)

    client.post("/api/message", json={"says": "close_now"}, headers=headers())

    assert [row.said.says for row in store.pending(household)] == [Says.CLOSE_NOW]
    period = time.strftime("%Y-%m", time.gmtime())
    assert counter.summary(household, period).total.calls == 0


def test_the_parent_can_see_it_is_still_waiting(client: TestClient) -> None:
    """A parent who moved the hour and saw nothing has no way to tell whether it landed.
    What they are shown is their own message, and nothing about the afternoon."""
    client.post("/api/message", json={"says": "end_by", "at": "17:30"}, headers=headers())

    waiting = client.get("/api/messages", headers=headers()).json()["messages"]

    assert [row["says"] for row in waiting] == ["end_by"]


# ── The house comes for it ───────────────────────────────────────────────────────────


def test_the_device_key_is_needed_to_collect(client: TestClient) -> None:
    household = household_of(client)

    refused = client.get(
        f"/api/device/{household}/messages", headers={"X-Device-Key": "wrong"}
    )

    assert refused.status_code == 403


def test_the_house_gets_it_only_when_it_asks_and_clears_it_by_id(client: TestClient) -> None:
    household = household_of(client)
    client.post("/api/message", json={"says": "end_by", "at": "17:30"}, headers=headers())

    said = client.get(f"/api/device/{household}/messages", headers=as_the_house()).json()
    assert [row["says"] for row in said["messages"]] == ["end_by"]

    heard = client.post(
        f"/api/device/{household}/messages/{said['messages'][0]['id']}/heard",
        headers=as_the_house(),
    )

    assert heard.json()["heard"] is True
    left = client.get(f"/api/device/{household}/messages", headers=as_the_house()).json()
    assert left["messages"] == []


def test_a_message_written_while_the_house_was_busy_survives(
    store: InMemoryMessageStore,
) -> None:
    """The house asked, the parent said something else, then the house said it had heard
    the first. Clearing by id is what keeps the second.

    Written just now rather than at :data:`WHEN`: a message is only offered for an hour, so a
    fixed calendar instant stops being a message the store will hand over as the day goes on.
    These two tests passed at 13:41 on 24 August 2026 and failed at 14:30.
    """
    now = time.time()
    first = store.add(clean_message("h1", says=Says.END_BY, at="17:30", now=now - 60))
    second = store.add(clean_message("h1", says=Says.CLOSE_NOW, now=now))

    assert store.heard("h1", first.id) is True
    assert [row.id for row in store.pending("h1")] == [second.id]


def test_they_are_handed_over_oldest_first(store: InMemoryMessageStore) -> None:
    """``hear`` folds them in order, so the order is part of what is handed over."""
    now = time.time()
    later = store.add(clean_message("h1", says=Says.CLOSE_NOW, now=now))
    earlier = store.add(clean_message("h1", says=Says.END_BY, at="17:30", now=now - 60))

    assert [row.id for row in store.pending("h1")] == [earlier.id, later.id]


def test_a_message_nobody_collected_stops_being_offered(store: InMemoryMessageStore) -> None:
    long_ago = time.time() - MESSAGE_LIFETIME_SECONDS - 1
    store.add(clean_message("h1", says=Says.CLOSE_NOW, now=long_ago))

    assert store.pending("h1") == []


def test_the_lifetime_outlives_a_house_that_missed_several_looks() -> None:
    """An hour, and not a multiple of the timer.

    It was written as six looks of a ten-minute timer, which read as a derivation and was
    a coincidence: the two numbers matched. On 25 August 2026 the timer went to one minute
    so the parent could press "begin now", and the derivation would have cut a parent's
    sentence from an hour to six minutes — a hub rebooting would have dropped it.

    So what is checked is the property the number is for: it survives a house that missed
    many looks, and it does not survive so long that a sentence about one afternoon can
    arrive inside the next.
    """
    every = re.search(r"OnCalendar=\*:0/(\d+):00", THE_TIMER.read_text(encoding="utf-8"))

    assert every is not None
    looks = MESSAGE_LIFETIME_SECONDS / (int(every.group(1)) * 60)
    assert looks >= 6, "a message must outlive a house that missed a few looks"
    assert MESSAGE_LIFETIME_SECONDS <= 2 * 60 * 60, "and must not reach the next afternoon"


# ── The whole channel, panel to run file ─────────────────────────────────────────────


def test_the_end_hour_a_parent_typed_reaches_the_run(
    client: TestClient, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`ideas/09 §23`, "done when": the hour moves in the panel and the afternoon in the
    house is over by it. Nothing was sent — the house asked, and this is that request."""
    house = a_house(tmp_path, household_of(client))
    through(client, monkeypatch)
    an_afternoon_under_way(house)
    was = running(house).over_at
    client.post("/api/message", json={"says": "end_by", "at": "15:00"}, headers=headers())

    changed = house_timer.listen(house, WHEN)

    assert changed and "15:00" in changed[0]
    assert running(house).over_at < was
    # Heard, so the next look does not apply the same hour to a later afternoon.
    left = client.get(
        f"/api/device/{house.household}/messages", headers=as_the_house()
    ).json()
    assert left["messages"] == []


def test_the_look_draws_nothing(
    client: TestClient, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`ideas/09 §8`: nothing a parent sends may produce a text that reveals the channel
    exists. Screens are counted rather than read, because a screen is what gives it away."""
    house = a_house(tmp_path, household_of(client))
    through(client, monkeypatch)
    an_afternoon_under_way(house)
    quiet = screens(house)
    client.post("/api/message", json={"says": "close_now"}, headers=headers())

    house_timer.listen(house, WHEN)

    assert screens(house) == quiet


def test_a_panel_that_will_not_answer_leaves_the_afternoon_as_it_was(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Reduced capability, not a stopped afternoon: it goes on exactly as it was going."""

    def refuse(*args: Any, **kwargs: Any) -> Any:
        raise OSError("no route to the panel")

    monkeypatch.setattr(house_timer, "_get", refuse)
    house = a_house(tmp_path)
    an_afternoon_under_way(house)
    was = running(house).over_at

    assert house_timer.listen(house, WHEN) == []
    assert running(house).over_at == was


def test_something_the_house_cannot_read_is_left_rather_than_cleared(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The two sides disagreeing about what may be said is ours to fix, and saying it was
    heard would hide it. It stops being offered within the hour anyway."""
    cleared: list[str] = []

    def get(url: str, key: str, timeout: int) -> Any:
        return {"messages": [{"id": "say_1", "says": "pause", "writtenAt": WHEN}]}

    def post(url: str, key: str, body: dict[str, Any], timeout: int) -> Any:
        cleared.append(url)
        return {}

    monkeypatch.setattr(house_timer, "_get", get)
    monkeypatch.setattr(house_timer, "_post", post)
    house = a_house(tmp_path)
    an_afternoon_under_way(house)

    assert house_timer.listen(house, WHEN) == []
    assert cleared == []
