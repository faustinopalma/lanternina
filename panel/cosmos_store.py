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

import time
from typing import Any

from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

from shared.accounts import Account, AccountStatus
from shared.ids import AccountId, new_account_id, new_household_id

from .devices import DeviceStatus
from .preferences import (
    DEFAULT_DIFFICULTY,
    DEFAULT_LANGUAGE,
    DEFAULT_VARIETY,
    DEFAULT_WORDS_PER_LINE,
    Preferences,
)
from .proposals import ProposalRecord
from .rhythm import Rhythm
from .themes import Theme
from .usage import UsageEvent, UsageSummary, summarise

ACCOUNTS_CONTAINER = "families"
PROPOSALS_CONTAINER = "proposals"
THEMES_CONTAINER = "sources"
DEVICES_CONTAINER = "sources"
RHYTHM_CONTAINER = "sources"
PREFERENCES_CONTAINER = "sources"
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
        existing = self._read(record.household_id, record.id)
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

    def _read(self, household_id: str, proposal_id: str) -> ProposalRecord | None:
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
                "quietFromMinutes": rhythm.quiet_from_minutes,
                "quietUntilMinutes": rhythm.quiet_until_minutes,
                "cadenceMinutes": rhythm.cadence_minutes,
                "updatedAt": rhythm.updated_at,
                "updatedBy": rhythm.updated_by,
            }
        )
        return rhythm


def _to_rhythm(document: dict[str, Any]) -> Rhythm:
    return Rhythm(
        household_id=str(document["familyId"]),
        quiet_from_minutes=_minutes(document, "quietFromMinutes", "quietFromHour", 22 * 60),
        quiet_until_minutes=_minutes(document, "quietUntilMinutes", "quietUntilHour", 7 * 60),
        cadence_minutes=_minutes(document, "cadenceMinutes", "cadenceHours", 60),
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
    else: there is no field for her name here, and the hub never sends one.
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
