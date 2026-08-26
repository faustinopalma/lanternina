"""Cosmos-backed stores for accounts and proposals.

Cosmos is reachable only through a private endpoint, so this code runs in the container
app and not on a laptop. That is a deliberate consequence of the tenant policy that forces
``publicNetworkAccess=Disabled``, and the reason both stores have in-memory twins the
tests run against.

Authentication is Entra only: the account is created with ``disableLocalAuth=true``, so
there is no key to leak and the identity is the container's managed identity.

``familyId`` is the partition key everywhere. Household isolation is therefore a property
of the read, not of a WHERE clause somebody eventually forgets.
"""

from __future__ import annotations

import re
import time
from collections.abc import Sequence
from dataclasses import replace
from typing import Any

from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

from shared.accounts import Account, AccountStatus
from shared.ids import AccountId, new_account_id, new_household_id
from shared.message import Message, Says

from .devices import DeviceStatus, Thing, order_of
from .experiences import OfferedExperience
from .guidelines import Guidelines
from .messages import PendingMessage
from .preferences import (
    DEFAULT_DIFFICULTY,
    DEFAULT_LANGUAGE,
    DEFAULT_VARIETY,
    DEFAULT_WORDS_PER_LINE,
    Preferences,
)
from .proposals import ProposalRecord
from .reminders import Sentence
from .requests import HouseRequest
from .rhythm import (
    DEFAULT_AFTERNOON_FROM_MINUTES,
    DEFAULT_AFTERNOON_UNTIL_MINUTES,
    DEFAULT_PICTURES_FROM_MINUTES,
    DEFAULT_PICTURES_UNTIL_MINUTES,
    DEFAULT_SCRIPTS_WANTED,
    Rhythm,
)
from .themes import Theme
from .trail import Made, Trail
from .usage import Limit, UsageEvent, UsageSummary, summarise

ACCOUNTS_CONTAINER = "families"
PROPOSALS_CONTAINER = "proposals"
THEMES_CONTAINER = "sources"
DEVICES_CONTAINER = "sources"
INVENTORY_CONTAINER = "sources"
RHYTHM_CONTAINER = "sources"
PREFERENCES_CONTAINER = "sources"
GUIDELINES_CONTAINER = "sources"
REMINDERS_CONTAINER = "sources"
MESSAGES_CONTAINER = "sources"
REQUESTS_CONTAINER = "sources"
EXPERIENCES_CONTAINER = "sources"
TRAILS_CONTAINER = "sources"
LIMIT_CONTAINER = "sources"
USAGE_CONTAINER = "usage"


def _client(endpoint: str, credential: Any | None = None) -> CosmosClient:
    return CosmosClient(endpoint, credential=credential or DefaultAzureCredential())


class CosmosAccountStore:
    """Conforms to :class:`~shared.accounts.AccountStore`."""

    def __init__(self, endpoint: str, database: str, credential: Any | None = None) -> None:
        self._container = (
            _client(endpoint, credential)
            .get_database_client(database)
            .get_container_client(ACCOUNTS_CONTAINER)
        )

    def by_subject(self, subject: str) -> Account | None:
        rows = list(
            self._container.query_items(
                query="SELECT * FROM c WHERE c.type = 'account' AND c.subject = @subject",
                parameters=[{"name": "@subject", "value": subject}],
                enable_cross_partition_query=True,
            )
        )
        return _to_account(rows[0]) if rows else None

    def register(self, *, subject: str, contact: str) -> Account:
        existing = self.by_subject(subject)
        if existing is not None:
            # Signing in again must never reset a decision already taken.
            return existing
        account = Account(
            id=new_account_id(),
            household_id=new_household_id(),
            subject=subject,
            contact=contact,
            status=AccountStatus.PENDING,
            created_at=time.time(),
        )
        self._container.create_item(_from_account(account))
        return account

    def pending(self) -> list[Account]:
        rows = self._container.query_items(
            query="SELECT * FROM c WHERE c.type = 'account' AND c.status = 'pending'",
            enable_cross_partition_query=True,
        )
        return sorted((_to_account(row) for row in rows), key=lambda a: a.created_at)

    def has_active(self) -> bool:
        rows = list(
            self._container.query_items(
                query="SELECT TOP 1 c.id FROM c WHERE c.type = 'account' AND c.status = 'active'",
                enable_cross_partition_query=True,
            )
        )
        return bool(rows)

    def decide(
        self, account_id: AccountId, status: AccountStatus, *, decided_by: str, note: str = ""
    ) -> Account:
        if not decided_by:
            raise ValueError("a decision must record who made it")
        rows = list(
            self._container.query_items(
                query="SELECT * FROM c WHERE c.type = 'account' AND c.id = @id",
                parameters=[{"name": "@id", "value": str(account_id)}],
                enable_cross_partition_query=True,
            )
        )
        if not rows:
            raise KeyError(account_id)
        document = rows[0]
        document.update(
            {
                "status": str(status),
                "decidedAt": time.time(),
                "decidedBy": decided_by,
                "note": note,
            }
        )
        self._container.upsert_item(document)
        return _to_account(document)


class CosmosProposalStore:
    """Conforms to :class:`~panel.proposals.ProposalStore`."""

    def __init__(self, endpoint: str, database: str, credential: Any | None = None) -> None:
        self._container = (
            _client(endpoint, credential)
            .get_database_client(database)
            .get_container_client(PROPOSALS_CONTAINER)
        )

    def submit(self, record: ProposalRecord) -> ProposalRecord:
        # Idempotent on id: a home server that retries must not create a second copy.
        existing = self.get(record.household_id, record.id)
        if existing is not None:
            return existing
        self._container.create_item(_from_record(record))
        return record

    def list(self, household_id: str, state: str | None = None) -> list[ProposalRecord]:
        query = "SELECT * FROM c WHERE c.familyId = @family"
        parameters: list[dict[str, Any]] = [{"name": "@family", "value": household_id}]
        if state is not None:
            query += " AND c.state = @state"
            parameters.append({"name": "@state", "value": state})
        rows = self._container.query_items(
            query=query, parameters=parameters, partition_key=household_id
        )
        return sorted((_to_record(row) for row in rows), key=lambda r: r.created_at)

    def decide(
        self, household_id: str, proposal_id: str, state: str, *, decided_by: str, note: str = ""
    ) -> ProposalRecord:
        if not decided_by:
            raise ValueError("a decision must record who made it")
        document = self._container.read_item(item=proposal_id, partition_key=household_id)
        document.update(
            {"state": state, "decidedAt": time.time(), "decidedBy": decided_by, "note": note}
        )
        self._container.upsert_item(document)
        return _to_record(document)

    def get(self, household_id: str, proposal_id: str) -> ProposalRecord | None:
        from azure.cosmos import exceptions

        try:
            document = self._container.read_item(item=proposal_id, partition_key=household_id)
        except exceptions.CosmosResourceNotFoundError:
            return None
        return _to_record(document)


class CosmosThemeStore:
    """Conforms to :class:`~panel.themes.ThemeStore`."""

    def __init__(self, endpoint: str, database: str, credential: Any | None = None) -> None:
        self._container = (
            _client(endpoint, credential)
            .get_database_client(database)
            .get_container_client(THEMES_CONTAINER)
        )

    def add(self, theme: Theme) -> Theme:
        self._container.create_item(
            {
                "id": theme.id,
                "familyId": theme.household_id,
                "type": "theme",
                "label": theme.label,
                "createdAt": theme.created_at,
                "createdBy": theme.created_by,
                "active": theme.active,
            }
        )
        return theme

    def list(self, household_id: str, *, active_only: bool = True) -> list[Theme]:
        query = "SELECT * FROM c WHERE c.familyId = @family AND c.type = 'theme'"
        if active_only:
            query += " AND c.active = true"
        rows = self._container.query_items(
            query=query,
            parameters=[{"name": "@family", "value": household_id}],
            partition_key=household_id,
        )
        return sorted((_to_theme(row) for row in rows), key=lambda t: t.created_at)

    def remove(self, household_id: str, theme_id: str) -> Theme:
        document = self._container.read_item(item=theme_id, partition_key=household_id)
        # Kept rather than deleted: a picture already shown stays traceable to the thing
        # the parent once said yes to.
        document["active"] = False
        self._container.upsert_item(document)
        return _to_theme(document)


def _to_theme(document: dict[str, Any]) -> Theme:
    return Theme(
        id=str(document["id"]),
        household_id=str(document["familyId"]),
        label=str(document.get("label") or ""),
        created_at=float(document.get("createdAt") or 0.0),
        created_by=str(document.get("createdBy") or ""),
        active=bool(document.get("active", True)),
    )


class CosmosSentenceStore:
    """Conforms to :class:`~panel.reminders.SentenceStore`."""

    def __init__(self, endpoint: str, database: str, credential: Any | None = None) -> None:
        self._container = (
            _client(endpoint, credential)
            .get_database_client(database)
            .get_container_client(REMINDERS_CONTAINER)
        )

    def add(self, sentence: Sentence) -> Sentence:
        self._container.create_item(_from_sentence(sentence))
        return sentence

    def list(self, household_id: str) -> list[Sentence]:
        rows = self._container.query_items(
            query="SELECT * FROM c WHERE c.familyId = @family AND c.type = 'reminder'",
            parameters=[{"name": "@family", "value": household_id}],
            partition_key=household_id,
        )
        return sorted((_to_sentence(row) for row in rows), key=lambda s: s.created_at)

    def rewrite(self, household_id: str, sentence_id: str, text: str) -> Sentence:
        document = self._container.read_item(item=sentence_id, partition_key=household_id)
        # A changed sentence is one nobody has read: whatever the house made of the old
        # wording was made of words that are no longer there.
        document["text"] = text
        document["readAt"] = 0.0
        document["at"] = ""
        document["days"] = []
        document["question"] = ""
        document["words"] = []
        self._container.upsert_item(document)
        return _to_sentence(document)

    def record_reading(
        self,
        household_id: str,
        sentence_id: str,
        *,
        read_at: float,
        at: str,
        days: tuple[str, ...],
        question: str,
    ) -> Sentence:
        document = self._container.read_item(item=sentence_id, partition_key=household_id)
        document["readAt"] = read_at
        document["at"] = at
        document["days"] = list(days)
        document["question"] = question
        self._container.upsert_item(document)
        return _to_sentence(document)

    def record_wording(
        self, household_id: str, sentence_id: str, *, words: tuple[str, ...]
    ) -> Sentence:
        document = self._container.read_item(item=sentence_id, partition_key=household_id)
        document["words"] = list(words)
        self._container.upsert_item(document)
        return _to_sentence(document)

    def remove(self, household_id: str, sentence_id: str) -> None:
        from azure.cosmos import exceptions

        try:
            self._container.delete_item(item=sentence_id, partition_key=household_id)
        except exceptions.CosmosResourceNotFoundError:
            # Removing something already gone is what the parent asked for.
            pass


def _from_sentence(sentence: Sentence) -> dict[str, Any]:
    return {
        "id": sentence.id,
        "familyId": sentence.household_id,
        "type": "reminder",
        "text": sentence.text,
        "createdAt": sentence.created_at,
        "createdBy": sentence.created_by,
        "readAt": sentence.read_at,
        "at": sentence.at,
        "days": list(sentence.days),
        "question": sentence.question,
        "words": list(sentence.words),
    }


def _to_sentence(document: dict[str, Any]) -> Sentence:
    return Sentence(
        id=str(document["id"]),
        household_id=str(document["familyId"]),
        text=str(document.get("text") or ""),
        created_at=float(document.get("createdAt") or 0.0),
        created_by=str(document.get("createdBy") or ""),
        read_at=float(document.get("readAt") or 0.0),
        at=str(document.get("at") or ""),
        days=tuple(str(day) for day in document.get("days") or ()),
        question=str(document.get("question") or ""),
        words=tuple(str(word) for word in document.get("words") or ()),
    )


class CosmosMessageStore:
    """Conforms to :class:`~panel.messages.MessageStore`.

    This is the store the in-memory twin cannot stand in for. A message is written by a
    parent and collected by the house within ten minutes, and the container app scales to
    zero in between — so a message held in a process is a message lost by the next
    request, and the failure looks exactly like a house that did not obey.
    """

    def __init__(self, endpoint: str, database: str, credential: Any | None = None) -> None:
        self._container = (
            _client(endpoint, credential)
            .get_database_client(database)
            .get_container_client(MESSAGES_CONTAINER)
        )

    def add(self, pending: PendingMessage) -> PendingMessage:
        self._container.create_item(
            {
                "id": pending.id,
                "familyId": pending.household_id,
                "type": "message",
                "says": str(pending.said.says),
                "minutes": pending.said.minutes,
                "writtenAt": pending.said.written_at,
                "writtenBy": pending.written_by,
            }
        )
        return pending

    def pending(self, household_id: str) -> list[PendingMessage]:
        now = time.time()
        rows = self._container.query_items(
            query="SELECT * FROM c WHERE c.familyId = @family AND c.type = 'message'",
            parameters=[{"name": "@family", "value": household_id}],
            partition_key=household_id,
        )
        fresh: list[PendingMessage] = []
        for document in rows:
            message = _to_message(document)
            if message.stale(now):
                self.heard(household_id, message.id)
                continue
            fresh.append(message)
        return sorted(fresh, key=lambda row: row.said.written_at)

    def heard(self, household_id: str, message_id: str) -> bool:
        from azure.cosmos import exceptions

        try:
            self._container.delete_item(item=message_id, partition_key=household_id)
        except exceptions.CosmosResourceNotFoundError:
            return False
        return True


def _to_message(document: dict[str, Any]) -> PendingMessage:
    return PendingMessage(
        id=str(document["id"]),
        household_id=str(document["familyId"]),
        said=Message(
            says=Says(str(document.get("says") or "")),
            written_at=float(document.get("writtenAt") or 0.0),
            minutes=int(document.get("minutes") or 0),
        ),
        written_by=str(document.get("writtenBy") or ""),
    )


class CosmosExperienceStore:
    """Conforms to :class:`~panel.experiences.ExperienceStore`."""

    def __init__(self, endpoint: str, database: str, credential: Any | None = None) -> None:
        self._container = (
            _client(endpoint, credential)
            .get_database_client(database)
            .get_container_client(EXPERIENCES_CONTAINER)
        )

    def offer(self, record: OfferedExperience) -> OfferedExperience:
        from azure.cosmos import exceptions

        try:
            self._container.create_item(_from_offered(record))
        except exceptions.CosmosResourceExistsError:
            # Idempotent on id, like the in-memory store: a house that retries must not
            # leave a parent two copies of one afternoon to refuse.
            existing = self._container.read_item(item=record.id, partition_key=record.household_id)
            return _to_offered(existing)
        return record

    def list(self, household_id: str, state: str | None = None) -> list[OfferedExperience]:
        rows = self._container.query_items(
            query="SELECT * FROM c WHERE c.familyId = @family AND c.type = 'experience'",
            parameters=[{"name": "@family", "value": household_id}],
            partition_key=household_id,
        )
        found = [_to_offered(row) for row in rows]
        if state is not None:
            found = [row for row in found if row.state == state]
        return sorted(found, key=lambda row: row.created_at)

    def get(self, household_id: str, experience_id: str) -> OfferedExperience | None:
        from azure.cosmos import exceptions

        try:
            document = self._container.read_item(item=experience_id, partition_key=household_id)
        except exceptions.CosmosResourceNotFoundError:
            return None
        return _to_offered(document)

    def decide(
        self, household_id: str, experience_id: str, state: str, *, decided_by: str, note: str = ""
    ) -> OfferedExperience:
        if not decided_by:
            raise ValueError("a decision must record who made it")
        document = self._container.read_item(item=experience_id, partition_key=household_id)
        document["state"] = state
        document["decidedAt"] = time.time()
        document["decidedBy"] = decided_by
        document["note"] = note
        self._container.upsert_item(document)
        return _to_offered(document)

    def begun(self, household_id: str, experience_id: str, at: float) -> OfferedExperience:
        document = self._container.read_item(item=experience_id, partition_key=household_id)
        if document.get("begunAt"):
            return _to_offered(document)
        document["begunAt"] = at
        self._container.upsert_item(document)
        return _to_offered(document)


def _from_offered(record: OfferedExperience) -> dict[str, Any]:
    return {
        "id": record.id,
        "familyId": record.household_id,
        "type": "experience",
        "experience": record.experience,
        "createdAt": record.created_at,
        "state": record.state,
        "decidedAt": record.decided_at,
        "decidedBy": record.decided_by,
        "note": record.note,
        "begunAt": record.begun_at,
    }


def _to_offered(document: dict[str, Any]) -> OfferedExperience:
    decided = document.get("decidedAt")
    return OfferedExperience(
        id=str(document["id"]),
        household_id=str(document["familyId"]),
        experience=dict(document.get("experience") or {}),
        created_at=float(document.get("createdAt") or 0.0),
        state=str(document.get("state") or ""),
        decided_at=None if decided is None else float(decided),
        decided_by=str(document.get("decidedBy") or ""),
        note=str(document.get("note") or ""),
        begun_at=float(document.get("begunAt") or 0.0),
    )


class CosmosTrailStore:
    """Conforms to :class:`~panel.trail.TrailStore`.

    Two document types in one container, both partitioned on the household: the trail, which
    is written once when an afternoon begins, and each thing made, which is appended and never
    read back by anything but the parent's page. Nothing here is ever updated after it is
    written, which is what makes it a record rather than a state.
    """

    def __init__(self, endpoint: str, database: str, credential: Any | None = None) -> None:
        self._container = (
            _client(endpoint, credential)
            .get_database_client(database)
            .get_container_client(TRAILS_CONTAINER)
        )

    def began(self, trail: Trail) -> Trail:
        from azure.cosmos import exceptions

        try:
            self._container.create_item(_from_trail(trail))
        except exceptions.CosmosResourceExistsError:
            # Idempotent on the run: a house that retries its first move must not open a
            # second trail for one afternoon.
            existing = self._container.read_item(
                item=_trail_id(trail.run_id), partition_key=trail.household_id
            )
            return _to_trail(existing)
        return trail

    def wrote(self, record: Made) -> Made:
        from azure.cosmos import exceptions

        try:
            self._container.create_item(_from_made(record))
        except exceptions.CosmosResourceExistsError:
            pass
        return record

    def list(self, household_id: str) -> list[Trail]:
        # The script is left out on purpose. A card needs a title and a date; carrying a
        # few thousand characters of script per card would make the page pay for something
        # nobody has clicked on yet.
        rows = self._container.query_items(
            query=(
                "SELECT c.id, c.familyId, c.runId, c.experienceId, c.title, c.overview,"
                " c.beganAt FROM c WHERE c.familyId = @family AND c.type = 'trail'"
            ),
            parameters=[{"name": "@family", "value": household_id}],
            partition_key=household_id,
        )
        return sorted(
            (_to_trail(row) for row in rows), key=lambda row: row.began_at, reverse=True
        )

    def get(self, household_id: str, run_id: str) -> Trail | None:
        from azure.cosmos import exceptions

        try:
            document = self._container.read_item(
                item=_trail_id(run_id), partition_key=household_id
            )
        except exceptions.CosmosResourceNotFoundError:
            return None
        made = self._container.query_items(
            query=(
                "SELECT * FROM c WHERE c.familyId = @family AND c.type = 'made'"
                " AND c.runId = @run"
            ),
            parameters=[
                {"name": "@family", "value": household_id},
                {"name": "@run", "value": run_id},
            ],
            partition_key=household_id,
        )
        found = _to_trail(document)
        return Trail(
            run_id=found.run_id,
            household_id=found.household_id,
            experience_id=found.experience_id,
            title=found.title,
            overview=found.overview,
            began_at=found.began_at,
            script=found.script,
            made=tuple(sorted((_to_made(row) for row in made), key=lambda one: one.at)),
        )


def _trail_id(run_id: str) -> str:
    """The run is the key. Prefixed because things made share the container with it."""
    return f"trail_{run_id}"


def _from_trail(trail: Trail) -> dict[str, Any]:
    return {
        "id": _trail_id(trail.run_id),
        "familyId": trail.household_id,
        "type": "trail",
        "runId": trail.run_id,
        "experienceId": trail.experience_id,
        "title": trail.title,
        "overview": trail.overview,
        "beganAt": trail.began_at,
        "script": trail.script,
    }


def _to_trail(document: dict[str, Any]) -> Trail:
    return Trail(
        run_id=str(document.get("runId") or ""),
        household_id=str(document.get("familyId") or ""),
        experience_id=str(document.get("experienceId") or ""),
        title=str(document.get("title") or ""),
        overview=str(document.get("overview") or ""),
        began_at=float(document.get("beganAt") or 0.0),
        script=str(document.get("script") or ""),
    )


def _from_made(record: Made) -> dict[str, Any]:
    return {
        "id": record.id,
        "familyId": record.household_id,
        "type": "made",
        "runId": record.run_id,
        "at": record.at,
        "kind": record.kind,
        "heading": record.heading,
        "body": record.body,
        "why": record.why,
        "pictureId": record.picture_id,
    }


def _to_made(document: dict[str, Any]) -> Made:
    return Made(
        id=str(document["id"]),
        household_id=str(document.get("familyId") or ""),
        run_id=str(document.get("runId") or ""),
        at=float(document.get("at") or 0.0),
        kind=str(document.get("kind") or ""),
        heading=str(document.get("heading") or ""),
        body=str(document.get("body") or ""),
        why=str(document.get("why") or ""),
        picture_id=str(document.get("pictureId") or ""),
    )


class CosmosRhythmStore:
    """Conforms to :class:`~panel.rhythm.RhythmStore`.

    One document per household, overwritten: this is a current choice, not a history of
    what the parent tried.
    """

    def __init__(self, endpoint: str, database: str, credential: Any | None = None) -> None:
        self._container = (
            _client(endpoint, credential)
            .get_database_client(database)
            .get_container_client(RHYTHM_CONTAINER)
        )

    def get(self, household_id: str) -> Rhythm:
        rows = list(
            self._container.query_items(
                query="SELECT * FROM c WHERE c.familyId = @family AND c.type = 'rhythm'",
                parameters=[{"name": "@family", "value": household_id}],
                partition_key=household_id,
            )
        )
        if not rows:
            return Rhythm(household_id=household_id)
        return _to_rhythm(rows[0])

    def set(self, rhythm: Rhythm) -> Rhythm:
        self._container.upsert_item(
            {
                "id": f"rhythm-{rhythm.household_id}",
                "familyId": rhythm.household_id,
                "type": "rhythm",
                "picturesFromMinutes": rhythm.pictures_from_minutes,
                "picturesUntilMinutes": rhythm.pictures_until_minutes,
                "cadenceMinutes": rhythm.cadence_minutes,
                "afternoonDays": list(rhythm.afternoon_days),
                "afternoonFromMinutes": rhythm.afternoon_from_minutes,
                "afternoonUntilMinutes": rhythm.afternoon_until_minutes,
                "timeZone": rhythm.time_zone,
                "scriptsWanted": rhythm.scripts_wanted,
                "updatedAt": rhythm.updated_at,
                "updatedBy": rhythm.updated_by,
            }
        )
        return rhythm


def _to_rhythm(document: dict[str, Any]) -> Rhythm:
    # A document written before 25 August 2026 holds a quiet window, which was the same
    # hours said inside out. It is not converted: the two bands now mean different things
    # to different parts of the house, and a guessed conversion would be a setting nobody
    # chose. Such a document reads as the defaults and the parent chooses once.
    return Rhythm(
        household_id=str(document["familyId"]),
        pictures_from_minutes=int(
            document.get("picturesFromMinutes") or DEFAULT_PICTURES_FROM_MINUTES
        ),
        pictures_until_minutes=int(
            document.get("picturesUntilMinutes") or DEFAULT_PICTURES_UNTIL_MINUTES
        ),
        cadence_minutes=_minutes(document, "cadenceMinutes", "cadenceHours", 60),
        # A document written before afternoons existed has no days, which is the same
        # thing as a household that has not chosen any: the house begins none.
        afternoon_days=tuple(str(day) for day in (document.get("afternoonDays") or ())),
        afternoon_from_minutes=int(
            document.get("afternoonFromMinutes") or DEFAULT_AFTERNOON_FROM_MINUTES
        ),
        afternoon_until_minutes=int(
            document.get("afternoonUntilMinutes") or DEFAULT_AFTERNOON_UNTIL_MINUTES
        ),
        # A document written before the zone existed has none, and the hub falls back to
        # its own machine — which is what it was already doing.
        time_zone=str(document.get("timeZone") or ""),
        scripts_wanted=int(document.get("scriptsWanted") or DEFAULT_SCRIPTS_WANTED),
        updated_at=float(document.get("updatedAt") or 0.0),
        updated_by=str(document.get("updatedBy") or ""),
    )


def _minutes(document: dict[str, Any], key: str, hours_key: str, default: int) -> int:
    """Documents written before the rhythm was minutes still hold whole hours."""
    if document.get(key) is not None:
        return int(document[key])
    if document.get(hours_key) is not None:
        return int(document[hours_key]) * 60
    return default


class CosmosPreferencesStore:
    """Conforms to :class:`~panel.preferences.PreferencesStore`.

    One document per household, overwritten. The document carries the settings and nothing
    else: there is no field for a name here, and the hub never sends one.
    """

    def __init__(self, endpoint: str, database: str, credential: Any | None = None) -> None:
        self._container = (
            _client(endpoint, credential)
            .get_database_client(database)
            .get_container_client(PREFERENCES_CONTAINER)
        )

    def get(self, household_id: str) -> Preferences:
        rows = list(
            self._container.query_items(
                query="SELECT * FROM c WHERE c.familyId = @family AND c.type = 'preferences'",
                parameters=[{"name": "@family", "value": household_id}],
                partition_key=household_id,
            )
        )
        if not rows:
            return Preferences(household_id=household_id)
        return _to_preferences(rows[0])

    def set(self, preferences: Preferences) -> Preferences:
        self._container.upsert_item(
            {
                "id": f"preferences-{preferences.household_id}",
                "familyId": preferences.household_id,
                "type": "preferences",
                "interests": list(preferences.interests),
                "avoid": list(preferences.avoid),
                "difficulty": preferences.difficulty,
                "variety": preferences.variety,
                "maxWordsPerLine": preferences.max_words_per_line,
                "language": preferences.language,
                "updatedAt": preferences.updated_at,
                "updatedBy": preferences.updated_by,
            }
        )
        return preferences


def _to_preferences(document: dict[str, Any]) -> Preferences:
    return Preferences(
        household_id=str(document["familyId"]),
        interests=tuple(str(item) for item in document.get("interests") or ()),
        avoid=tuple(str(item) for item in document.get("avoid") or ()),
        difficulty=str(document.get("difficulty") or DEFAULT_DIFFICULTY),
        variety=str(document.get("variety") or DEFAULT_VARIETY),
        max_words_per_line=int(document.get("maxWordsPerLine") or DEFAULT_WORDS_PER_LINE),
        language=str(document.get("language") or DEFAULT_LANGUAGE),
        updated_at=float(document.get("updatedAt") or 0.0),
        updated_by=str(document.get("updatedBy") or ""),
    )


class CosmosGuidelineStore:
    """Conforms to :class:`~panel.guidelines.GuidelineStore`.

    One document per household, overwritten. The parent's lines are kept as they wrote
    them; the fixed bounds are a module constant in `panel/guidelines.py` and have no
    document, which is the storage half of their not being editable.
    """

    def __init__(self, endpoint: str, database: str, credential: Any | None = None) -> None:
        self._container = (
            _client(endpoint, credential)
            .get_database_client(database)
            .get_container_client(GUIDELINES_CONTAINER)
        )

    def get(self, household_id: str) -> Guidelines:
        rows = list(
            self._container.query_items(
                query="SELECT * FROM c WHERE c.familyId = @family AND c.type = 'guidelines'",
                parameters=[{"name": "@family", "value": household_id}],
                partition_key=household_id,
            )
        )
        if not rows:
            return Guidelines(household_id=household_id)
        return _to_guidelines(rows[0])

    def set(self, guidelines: Guidelines) -> Guidelines:
        self._container.upsert_item(
            {
                "id": f"guidelines-{guidelines.household_id}",
                "familyId": guidelines.household_id,
                "type": "guidelines",
                "lines": list(guidelines.lines),
                "updatedAt": guidelines.updated_at,
                "updatedBy": guidelines.updated_by,
            }
        )
        return guidelines


def _to_guidelines(document: dict[str, Any]) -> Guidelines:
    return Guidelines(
        household_id=str(document["familyId"]),
        lines=tuple(str(line) for line in document.get("lines") or ()),
        updated_at=float(document.get("updatedAt") or 0.0),
        updated_by=str(document.get("updatedBy") or ""),
    )


class CosmosDeviceStatusStore:
    """Conforms to :class:`~panel.devices.DeviceStatusStore`.

    One document per display, overwritten on each report: this is a current state, not a
    history. Keeping every reading would be a log of when the house is awake.
    """
    def __init__(self, endpoint: str, database: str, credential: Any | None = None) -> None:
        self._container = (
            _client(endpoint, credential)
            .get_database_client(database)
            .get_container_client(DEVICES_CONTAINER)
        )

    def record(self, status: DeviceStatus) -> DeviceStatus:
        self._container.upsert_item(
            {
                "id": f"device-{status.id.replace(':', '')}",
                "familyId": status.household_id,
                "type": "device",
                "mac": status.id,
                "name": status.name,
                "level": status.level,
                "voltage": status.voltage,
                "rssi": status.rssi,
                "firmware": status.firmware,
                "model": status.model,
                "lastSeen": status.last_seen,
            }
        )
        return status

    def list(self, household_id: str) -> list[DeviceStatus]:
        rows = self._container.query_items(
            query="SELECT * FROM c WHERE c.familyId = @family AND c.type = 'device'",
            parameters=[{"name": "@family", "value": household_id}],
            partition_key=household_id,
        )
        return sorted((_to_status(row) for row in rows), key=lambda s: s.name)


def _to_status(document: dict[str, Any]) -> DeviceStatus:
    return DeviceStatus(
        id=str(document.get("mac") or document["id"]),
        household_id=str(document["familyId"]),
        name=str(document.get("name") or ""),
        last_seen=float(document.get("lastSeen") or 0.0),
        level=str(document.get("level") or "ok"),
        voltage=document.get("voltage"),
        rssi=document.get("rssi"),
        firmware=str(document.get("firmware") or ""),
        model=str(document.get("model") or ""),
    )


class CosmosInventoryStore:
    """Conforms to :class:`~panel.devices.InventoryStore`.

    One document per thing in the house, kept until somebody removes it by hand. Nothing
    drops out because it went quiet: a printer that is switched off answers no mDNS query,
    and that is exactly the moment the parent goes looking for it.
    """

    def __init__(self, endpoint: str, database: str, credential: Any | None = None) -> None:
        self._container = (
            _client(endpoint, credential)
            .get_database_client(database)
            .get_container_client(INVENTORY_CONTAINER)
        )

    def see(self, thing: Thing) -> Thing:
        known = {row.id: row for row in self.list(thing.household_id)}.get(thing.id)
        fresh = (
            thing
            if known is None
            else replace(
                known,
                kind=thing.kind or known.kind,
                label=thing.label or known.label,
                model=thing.model or known.model,
                address=thing.address or known.address,
                name_refused=thing.name_refused,
                last_seen=max(thing.last_seen, known.last_seen),
                # A report never un-forgets: what belongs on the list is the parent's say.
                forgotten_at=known.forgotten_at,
            )
        )
        if known is None:
            fresh = replace(fresh, first_seen=fresh.first_seen or fresh.last_seen)
        self._container.upsert_item(_from_thing(fresh))
        return fresh

    def assign(
        self,
        household_id: str,
        thing_id: str,
        *,
        jobs: Sequence[str] | None = None,
        name: str | None = None,
    ) -> Thing:
        rows = {row.id: row for row in self.list(household_id)}
        current = rows[thing_id]
        updated = replace(
            current,
            jobs=current.jobs if jobs is None else tuple(jobs),
            name=current.name if name is None else name,
            name_refused=current.name_refused if name is None else False,
        )
        self._container.upsert_item(_from_thing(updated))
        return updated

    def list(self, household_id: str) -> list[Thing]:
        rows = self._container.query_items(
            query="SELECT * FROM c WHERE c.familyId = @family AND c.type = 'thing'",
            parameters=[{"name": "@family", "value": household_id}],
            partition_key=household_id,
        )
        return sorted((_to_thing(row) for row in rows), key=order_of)

    def forget(self, household_id: str, thing_id: str) -> None:
        """Marked, not deleted: the hub reports it again within minutes and a deleted row
        came back stripped of its job and its name."""
        rows = {row.id: row for row in self.list(household_id)}
        current = rows.get(thing_id)
        if current is not None:
            self._container.upsert_item(_from_thing(replace(current, forgotten_at=time.time())))

    def recall(self, household_id: str, thing_id: str) -> Thing:
        rows = {row.id: row for row in self.list(household_id)}
        current = replace(rows[thing_id], forgotten_at=0.0)
        self._container.upsert_item(_from_thing(current))
        return current


def _thing_document_id(thing_id: str) -> str:
    """A MAC has colons and an mDNS name has dots; neither is a safe Cosmos item id."""
    return "thing-" + re.sub(r"[^A-Za-z0-9._-]", "-", thing_id)


def _jobs_in(document: dict[str, Any]) -> tuple[str, ...]:
    stored = document.get("jobs")
    if isinstance(stored, list):
        return tuple(str(job) for job in stored if str(job))
    single = str(document.get("job") or "")
    return (single,) if single else ()


def _from_thing(thing: Thing) -> dict[str, Any]:
    return {
        "id": _thing_document_id(thing.id),
        "familyId": thing.household_id,
        "type": "thing",
        "key": thing.id,
        "kind": thing.kind,
        "name": thing.name,
        "label": thing.label,
        "jobs": list(thing.jobs),
        "model": thing.model,
        "address": thing.address,
        "nameRefused": thing.name_refused,
        "lastSeen": thing.last_seen,
        "firstSeen": thing.first_seen,
        "forgottenAt": thing.forgotten_at,
    }


def _to_thing(document: dict[str, Any]) -> Thing:
    return Thing(
        id=str(document.get("key") or document["id"]),
        household_id=str(document["familyId"]),
        kind=str(document.get("kind") or ""),
        name=str(document.get("name") or ""),
        label=str(document.get("label") or ""),
        # `job` is what documents written before 19 August 2026 carry, and the parent's
        # choice is the one thing here nothing else can reconstruct.
        jobs=_jobs_in(document),
        model=str(document.get("model") or ""),
        address=str(document.get("address") or ""),
        name_refused=bool(document.get("nameRefused", False)),
        last_seen=float(document.get("lastSeen") or 0.0),
        first_seen=float(document.get("firstSeen") or 0.0),
        forgotten_at=float(document.get("forgottenAt") or 0.0),
    )


class CosmosUsageStore:
    """Conforms to :class:`~panel.usage.UsageStore`.

    One document per call, never updated. A figure somebody has relied on must stay
    reproducible, so a correction here would be a new event rather than an edit.
    """

    def __init__(self, endpoint: str, database: str, credential: Any | None = None) -> None:
        self._container = (
            _client(endpoint, credential)
            .get_database_client(database)
            .get_container_client(USAGE_CONTAINER)
        )

    def record(self, event: UsageEvent) -> UsageEvent:
        from azure.cosmos import exceptions

        try:
            self._container.create_item(
                {
                    "id": event.id,
                    "familyId": event.household_id,
                    "type": "usage",
                    "at": event.at,
                    "period": event.period,
                    "kind": event.kind,
                    "outcome": event.outcome,
                    "deployment": event.deployment,
                    "requestId": event.request_id,
                    "inputTokens": event.input_tokens,
                    "outputTokens": event.output_tokens,
                    "cachedInputTokens": event.cached_input_tokens,
                    "reasoningTokens": event.reasoning_tokens,
                    "size": event.size,
                    "quality": event.quality,
                }
            )
        except exceptions.CosmosResourceExistsError:
            # The point of the id: a retried write is the same event, not a second one.
            pass
        return event

    def summary(self, household_id: str, period: str) -> UsageSummary:
        rows = self._container.query_items(
            query=(
                "SELECT * FROM c WHERE c.familyId = @family AND c.type = 'usage' "
                "AND c.period = @period"
            ),
            parameters=[
                {"name": "@family", "value": household_id},
                {"name": "@period", "value": period},
            ],
            partition_key=household_id,
        )
        return summarise(household_id, period, [_to_usage(row) for row in rows])


def _to_usage(document: dict[str, Any]) -> UsageEvent:
    return UsageEvent(
        id=str(document["id"]),
        household_id=str(document["familyId"]),
        at=float(document.get("at") or 0.0),
        kind=str(document.get("kind") or ""),
        outcome=str(document.get("outcome") or ""),
        deployment=str(document.get("deployment") or ""),
        request_id=str(document.get("requestId") or ""),
        input_tokens=int(document.get("inputTokens") or 0),
        output_tokens=int(document.get("outputTokens") or 0),
        cached_input_tokens=int(document.get("cachedInputTokens") or 0),
        reasoning_tokens=int(document.get("reasoningTokens") or 0),
        size=str(document.get("size") or ""),
        quality=str(document.get("quality") or ""),
    )


class CosmosLimitStore:
    """Conforms to :class:`~panel.usage.LimitStore`.

    One document per household, written only when somebody sets it. No document means the
    configured default still applies, so raising the default in the deployment still
    reaches every household that has never touched it.
    """

    def __init__(self, endpoint: str, database: str, credential: Any | None = None) -> None:
        self._container = (
            _client(endpoint, credential)
            .get_database_client(database)
            .get_container_client(LIMIT_CONTAINER)
        )

    def get(self, household_id: str) -> Limit | None:
        rows = list(
            self._container.query_items(
                query="SELECT * FROM c WHERE c.familyId = @family AND c.type = 'limit'",
                parameters=[{"name": "@family", "value": household_id}],
                partition_key=household_id,
            )
        )
        if not rows:
            return None
        return Limit(
            household_id=household_id,
            calls=int(rows[0].get("calls") or 0),
            changed_at=float(rows[0].get("changedAt") or 0.0),
            changed_by=str(rows[0].get("changedBy") or ""),
        )

    def set(self, limit: Limit) -> Limit:
        self._container.upsert_item(
            {
                "id": f"limit-{limit.household_id}",
                "familyId": limit.household_id,
                "type": "limit",
                "calls": limit.calls,
                "changedAt": limit.changed_at,
                "changedBy": limit.changed_by,
            }
        )
        return limit


class CosmosRequestStore:
    """Conforms to :class:`~panel.requests.RequestStore`.

    One document per household, overwritten: this is what the parent is asking for now,
    not a record of everything they have ever asked. The id inside it is what the hub
    clears by, so the row can be replaced without the hub losing the newer one.
    """
    def __init__(self, endpoint: str, database: str, credential: Any | None = None) -> None:
        self._container = (
            _client(endpoint, credential)
            .get_database_client(database)
            .get_container_client(REQUESTS_CONTAINER)
        )

    def _document_id(self, household_id: str) -> str:
        return f"request-{household_id}"

    def put(self, asked: HouseRequest) -> HouseRequest:
        self._container.upsert_item(
            {
                "id": self._document_id(asked.household_id),
                "familyId": asked.household_id,
                "type": "request",
                "requestId": asked.id,
                "kind": asked.kind,
                "subject": asked.subject,
                "askedAt": asked.asked_at,
                "askedBy": asked.asked_by,
            }
        )
        return asked

    def get(self, household_id: str) -> HouseRequest | None:
        rows = list(
            self._container.query_items(
                query="SELECT * FROM c WHERE c.familyId = @family AND c.type = 'request'",
                parameters=[{"name": "@family", "value": household_id}],
                partition_key=household_id,
            )
        )
        if not rows:
            return None
        standing = _to_request(rows[0])
        if standing.stale(time.time()):
            self.clear(household_id, standing.id)
            return None
        return standing

    def clear(self, household_id: str, request_id: str) -> bool:
        from azure.cosmos import exceptions

        standing = self._raw(household_id)
        if standing is None or str(standing.get("requestId") or "") != request_id:
            return False
        try:
            self._container.delete_item(
                self._document_id(household_id), partition_key=household_id
            )
        except exceptions.CosmosResourceNotFoundError:
            # Two hubs, or one hub retrying: already gone is the outcome that was wanted.
            return False
        return True

    def _raw(self, household_id: str) -> dict[str, Any] | None:
        rows = list(
            self._container.query_items(
                query="SELECT * FROM c WHERE c.familyId = @family AND c.type = 'request'",
                parameters=[{"name": "@family", "value": household_id}],
                partition_key=household_id,
            )
        )
        return rows[0] if rows else None


def _to_request(document: dict[str, Any]) -> HouseRequest:
    return HouseRequest(
        id=str(document.get("requestId") or ""),
        household_id=str(document["familyId"]),
        kind=str(document.get("kind") or ""),
        subject=str(document.get("subject") or ""),
        asked_at=float(document.get("askedAt") or 0.0),
        asked_by=str(document.get("askedBy") or ""),
    )


def _from_account(account: Account) -> dict[str, Any]:
    return {
        "id": str(account.id),
        "familyId": str(account.household_id),
        "type": "account",
        "subject": account.subject,
        "contact": account.contact,
        "status": str(account.status),
        "createdAt": account.created_at,
        "decidedAt": account.decided_at,
        "decidedBy": account.decided_by,
        "note": account.note,
    }


def _to_account(document: dict[str, Any]) -> Account:
    return Account(
        id=AccountId(str(document["id"])),
        household_id=str(document["familyId"]),
        subject=str(document["subject"]),
        contact=str(document["contact"]),
        status=AccountStatus(str(document["status"])),
        created_at=float(document.get("createdAt") or 0.0),
        decided_at=document.get("decidedAt"),
        decided_by=str(document.get("decidedBy") or ""),
        note=str(document.get("note") or ""),
    )


def _from_record(record: ProposalRecord) -> dict[str, Any]:
    return {
        "id": record.id,
        "familyId": record.household_id,
        "type": "proposal",
        "kind": record.kind,
        "agent": record.agent,
        "rationale": record.rationale,
        "createdAt": record.created_at,
        "payload": record.payload,
        "payloadSeal": record.payload_seal,
        "state": record.state,
        "decidedAt": record.decided_at,
        "decidedBy": record.decided_by,
        "note": record.note,
        "expiresAt": record.expires_at,
    }


def _to_record(document: dict[str, Any]) -> ProposalRecord:
    return ProposalRecord(
        id=str(document["id"]),
        household_id=str(document["familyId"]),
        kind=str(document.get("kind") or ""),
        agent=str(document.get("agent") or ""),
        rationale=str(document.get("rationale") or ""),
        created_at=float(document.get("createdAt") or 0.0),
        payload=dict(document.get("payload") or {}),
        payload_seal=dict(document.get("payloadSeal") or {}),
        state=str(document.get("state") or "pending"),
        decided_at=document.get("decidedAt"),
        decided_by=str(document.get("decidedBy") or ""),
        note=str(document.get("note") or ""),
        expires_at=document.get("expiresAt"),
    )
