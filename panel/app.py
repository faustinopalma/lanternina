"""The panel the parent talks to.

Deliberately thin for now: a health check, and one route behind the gate. What it is
already careful about is the shape of a refusal — every denial returns the same body and
says nothing about whether the account exists, so the endpoint cannot be used to find out
which addresses are registered.

Future dashboard mutation routes persist state and return. They do not call models,
enqueue work, notify the home server or schedule processing. Work starts only on a
separate request initiated by the server in the home.
"""

from __future__ import annotations

import base64
import logging
import secrets
import time
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from shared.accounts import Account, AccountStatus, AccountStore
from shared.approval import ApprovalState
from shared.errors import (
    AccessDenied,
    AuthNotConfigured,
    CloudUnavailable,
    NoCapacityError,
    SafetyBlocked,
)
from shared.ids import AccountId

from .admin import ADMISSIONS, CurrentAdmin, waiting_view
from .config import Settings
from .devices import (
    KIND_DISPLAY,
    MAX_NAME_LENGTH,
    DeviceStatus,
    DeviceStatusStore,
    InMemoryDeviceStatusStore,
    InMemoryInventoryStore,
    InventoryStore,
    Thing,
    clean_job,
    clean_name,
    merged,
)
from .gate import resolve_account
from .pictures import (
    DEFAULT_PAGE_SIZE,
    PAGE_SIZES,
    InMemoryPictureArchive,
    PictureArchive,
    PictureRecord,
)
from .preferences import (
    InMemoryPreferencesStore,
    PreferencesStore,
    clean_preferences,
)
from .principal import principal_from_headers
from .proposals import DECIDABLE, InMemoryProposalStore, ProposalRecord, ProposalStore
from .rhythm import InMemoryRhythmStore, RhythmStore, clean_rhythm
from .store import InMemoryAccountStore
from .themes import InMemoryThemeStore, ThemeStore, clean_label, make_theme
from .tokens import TokenVerifier
from .usage import (
    FAILED,
    KIND_IMAGE,
    REFUSED,
    SERVED,
    InMemoryUsageStore,
    UsageStore,
    event_from,
    month_of,
    over_cap,
)


def verifier_for(app: FastAPI) -> TokenVerifier | None:
    """Built on first use, so an identity provider that is unreachable at startup answers
    503 rather than stopping the container from starting at all."""
    settings: Settings = app.state.settings
    if not settings.oidc_configured:
        return None
    if app.state.verifier is None:
        app.state.verifier = TokenVerifier.from_authority(
            settings.oidc_authority, settings.oidc_audience
        )
    return app.state.verifier


def current_account(request: Request) -> Account:
    """Module scope on purpose: `from __future__ import annotations` postpones the
    annotation, and FastAPI cannot resolve a name that only exists inside a closure."""
    settings: Settings = request.app.state.settings
    principal = principal_from_headers(
        request.headers, settings, verifier_for(request.app)
    )
    return resolve_account(principal, request.app.state.store, settings)


CurrentAccount = Annotated[Account, Depends(current_account)]


class Decision(BaseModel):
    state: str
    note: str = ""


class SubmittedProposal(BaseModel):
    """What the home server sends up for review, sealed exactly as the gate left it."""

    id: str
    kind: str
    agent: str
    rationale: str = ""
    createdAt: float = 0.0
    payload: dict[str, Any] = Field(default_factory=dict)
    payloadSeal: dict[str, Any] = Field(default_factory=dict)
    expiresAt: float | None = None


class ShownPicture(BaseModel):
    """A picture a display has shown, archived so it can be put back later."""

    id: str
    theme: str = ""
    kind: str = "ok"
    createdAt: float = 0.0
    imageBase64: str


class NewTheme(BaseModel):
    label: str


class NewRhythm(BaseModel):
    """When the display may change, and how often. Saving it starts nothing."""

    quietFrom: str
    quietUntil: str
    cadenceMinutes: int


class NewPreferences(BaseModel):
    """What the content is made of. These are the fields the hub may put in a prompt.

    Unknown fields are refused rather than dropped: a body carrying a name would
    otherwise be accepted and quietly ignored, which reads as working.
    """

    model_config = ConfigDict(extra="forbid")

    interests: list[str] = Field(default_factory=list)
    avoid: list[str] = Field(default_factory=list)
    difficulty: str
    variety: str
    maxWordsPerLine: int
    language: str


class ReportedDevice(BaseModel):
    """What the hub says about one thing in the house. The hub decides a display's level:
    it holds the thresholds and knows whether the display is declared mains powered.

    A printer or a scanner arrives here too, found over mDNS, carrying nothing but its
    identity — which is why everything except the id has a default.
    """

    id: str
    kind: str = KIND_DISPLAY
    name: str = ""
    address: str = ""
    lastSeen: float = 0.0
    level: str = "ok"
    voltage: float | None = None
    rssi: float | None = None
    firmware: str = ""
    model: str = ""


class NewAssignment(BaseModel):
    """What the parent decided about one thing. Both parts are optional: naming a printer
    and giving it the job are two moments, and neither should undo the other.

    Unknown fields are refused rather than dropped, so a body carrying something we do not
    store cannot look as though it was saved.
    """

    model_config = ConfigDict(extra="forbid")

    job: str | None = None
    name: str | None = None


def require_device(request: Request) -> str:
    """Identify the server in the home. Closed unless a key is configured."""
    settings: Settings = request.app.state.settings
    if not settings.device_configured:
        raise HTTPException(status_code=503, detail="device_not_configured")
    presented = request.headers.get("X-Device-Key", "")
    if not secrets.compare_digest(presented, settings.device_key):
        raise HTTPException(status_code=403, detail="not_authorised")
    return presented


DeviceKey = Annotated[str, Depends(require_device)]


def create_app(
    store: AccountStore | None = None,
    settings: Settings | None = None,
    proposals: ProposalStore | None = None,
    pictures: PictureArchive | None = None,
    themes: ThemeStore | None = None,
    devices: DeviceStatusStore | None = None,
    inventory: InventoryStore | None = None,
    usage: UsageStore | None = None,
    rhythm: RhythmStore | None = None,
    preferences: PreferencesStore | None = None,
) -> FastAPI:
    app = FastAPI(title="Lanternina", docs_url=None, redoc_url=None)
    app.state.settings = settings if settings is not None else Settings.from_env()
    app.state.store = store if store is not None else _account_store(app.state.settings)
    app.state.proposals = (
        proposals if proposals is not None else _proposal_store(app.state.settings)
    )
    app.state.pictures = (
        pictures if pictures is not None else _picture_archive(app.state.settings)
    )
    app.state.themes = themes if themes is not None else _theme_store(app.state.settings)
    app.state.devices = devices if devices is not None else _device_store(app.state.settings)
    app.state.inventory = (
        inventory if inventory is not None else _inventory_store(app.state.settings)
    )
    app.state.usage = usage if usage is not None else _usage_store(app.state.settings)
    app.state.rhythm = rhythm if rhythm is not None else _rhythm_store(app.state.settings)
    app.state.preferences = (
        preferences if preferences is not None else _preferences_store(app.state.settings)
    )
    app.state.verifier = None
    app.state.admin_verifier = None

    # Named origins only. The token travels in a header, not a cookie, so credentials stay
    # off and a wildcard would buy nothing except a wider blast radius.
    if app.state.settings.origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=list(app.state.settings.origins),
            allow_credentials=False,
            allow_methods=["GET", "POST"],
            allow_headers=["Authorization", "Content-Type"],
        )

    @app.exception_handler(AccessDenied)
    async def _denied(_: Request, __: AccessDenied) -> JSONResponse:
        # One body for every refusal: "unknown" and "not yet approved" must be
        # indistinguishable from outside.
        return JSONResponse(status_code=403, content={"detail": "not_authorised"})

    @app.exception_handler(AuthNotConfigured)
    async def _unconfigured(_: Request, __: AuthNotConfigured) -> JSONResponse:
        return JSONResponse(status_code=503, content={"detail": "auth_not_configured"})

    @app.get("/health")
    def health() -> dict[str, str]:
        """No auth, no store, no I/O — this is what a cold start is measured against."""
        return {"status": "ok"}

    @app.get("/api/me")
    def me(account: CurrentAccount) -> dict[str, Any]:
        return {
            "accountId": account.id,
            "householdId": account.household_id,
            "status": account.status,
        }

    @app.get("/api/admin/me")
    def admin_me(admin: CurrentAdmin) -> dict[str, Any]:
        """Who the administration surface believes is calling.

        It exists so the page can tell "you hold no administrator role" apart from
        "nobody is waiting": both would otherwise be an empty list.
        """
        return {"subject": admin.subject, "contact": admin.contact}

    @app.get("/api/admin/accounts")
    def waiting_accounts(_: CurrentAdmin, request: Request) -> Any:
        """The sign-ups awaiting a decision, oldest first. Deliberately not a search over
        every account: a route that answers questions about one address is a way to find
        out who is registered."""
        store: AccountStore = request.app.state.store
        return {"accounts": [waiting_view(row) for row in store.pending()]}

    @app.post("/api/admin/accounts/{account_id}/decision")
    def admit_account(
        account_id: str, decision: Decision, admin: CurrentAdmin, request: Request
    ) -> Any:
        """Admit or refuse one sign-up. This is the whole effect: a status changes, and
        who changed it is recorded. Nothing is generated and nobody is notified."""
        if decision.state not in {status.value for status in ADMISSIONS}:
            raise HTTPException(status_code=400, detail="unsupported_state")
        store: AccountStore = request.app.state.store
        try:
            row = store.decide(
                AccountId(account_id),
                AccountStatus(decision.state),
                decided_by=admin.subject,
                note=decision.note,
            )
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="unknown_account") from exc
        return waiting_view(row)

    @app.get("/api/proposals")
    def list_proposals(account: CurrentAccount, request: Request, state: str = "pending") -> Any:
        store: ProposalStore = request.app.state.proposals
        rows = store.list(str(account.household_id), state or None)
        return {"proposals": [row.to_public() for row in rows]}

    @app.post("/api/proposals/{proposal_id}/decision")
    def decide_proposal(
        proposal_id: str, decision: Decision, account: CurrentAccount, request: Request
    ) -> Any:
        """Record what the parent decided. This is the whole effect: it starts nothing."""
        if decision.state not in {s.value for s in DECIDABLE}:
            raise HTTPException(status_code=400, detail="unsupported_state")
        store: ProposalStore = request.app.state.proposals
        try:
            row = store.decide(
                str(account.household_id),
                proposal_id,
                decision.state,
                decided_by=str(account.id),
                note=decision.note,
            )
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="unknown_proposal") from exc
        return row.to_public()

    @app.post("/api/device/{household_id}/proposals")
    def submit_proposals(
        household_id: str, submitted: list[SubmittedProposal], _: DeviceKey, request: Request
    ) -> Any:
        """The home server offers a batch for review. Nothing is shown to anyone yet."""
        store: ProposalStore = request.app.state.proposals
        stored = [
            store.submit(
                ProposalRecord(
                    id=item.id,
                    household_id=household_id,
                    kind=item.kind,
                    agent=item.agent,
                    rationale=item.rationale,
                    created_at=item.createdAt or time.time(),
                    payload=item.payload,
                    payload_seal=item.payloadSeal,
                    expires_at=item.expiresAt,
                )
            )
            for item in submitted
        ]
        return {"stored": [row.id for row in stored]}

    @app.get("/api/device/{household_id}/proposals")
    def device_proposals(
        household_id: str,
        _: DeviceKey,
        request: Request,
        state: str = ApprovalState.APPROVED.value,
    ) -> Any:
        """What the home server asked for. It pulls; nothing is ever pushed to the house."""
        store: ProposalStore = request.app.state.proposals
        rows = store.list(household_id, state or None)
        return {"proposals": [row.to_device() for row in rows]}

    @app.post("/api/device/{household_id}/pictures")
    def archive_picture(
        household_id: str, shown: ShownPicture, _: DeviceKey, request: Request
    ) -> Any:
        """Keep a picture that was shown, so it can be put back on a display later."""
        archive: PictureArchive = request.app.state.pictures
        record = archive.save(
            PictureRecord(
                id=shown.id,
                household_id=household_id,
                theme=shown.theme,
                created_at=shown.createdAt or time.time(),
                kind=shown.kind,
            ),
            base64.b64decode(shown.imageBase64),
        )
        return record.to_public()

    @app.get("/api/device/{household_id}/pictures")
    def device_pictures(household_id: str, _: DeviceKey, request: Request) -> Any:
        archive: PictureArchive = request.app.state.pictures
        return {"pictures": [row.to_public() for row in archive.list(household_id)]}

    @app.get("/api/device/{household_id}/pictures/{picture_id}")
    def device_picture(
        household_id: str, picture_id: str, _: DeviceKey, request: Request
    ) -> Any:
        """Hand back one archived picture, so the home server can show it again."""
        archive: PictureArchive = request.app.state.pictures
        try:
            record, image = archive.get(household_id, picture_id)
        except Exception as exc:  # storage SDKs raise their own not-found types
            raise HTTPException(status_code=404, detail="unknown_picture") from exc
        return {**record.to_public(), "imageBase64": base64.b64encode(image).decode()}

    @app.get("/api/pictures")
    def list_pictures(
        account: CurrentAccount,
        request: Request,
        page: int = 1,
        perPage: int = DEFAULT_PAGE_SIZE,
    ) -> Any:
        archive: PictureArchive = request.app.state.pictures
        size = perPage if perPage in PAGE_SIZES else DEFAULT_PAGE_SIZE
        household = str(account.household_id)
        wanted = max(1, page)
        rows, total = archive.page(household, offset=(wanted - 1) * size, limit=size)
        pages = max(1, -(-total // size))
        if wanted > pages:
            # A larger page size can leave the parent standing past the end. Show the last
            # page rather than an empty one.
            wanted = pages
            rows, total = archive.page(household, offset=(wanted - 1) * size, limit=size)
        return {
            "pictures": [row.to_public() for row in rows],
            "page": wanted,
            "perPage": size,
            "pages": pages,
            "total": total,
            "pageSizes": list(PAGE_SIZES),
        }

    @app.get("/api/pictures/{picture_id}/content")
    def picture_content(picture_id: str, account: CurrentAccount, request: Request) -> Response:
        archive: PictureArchive = request.app.state.pictures
        try:
            _record, image = archive.get(str(account.household_id), picture_id)
        except Exception as exc:
            raise HTTPException(status_code=404, detail="unknown_picture") from exc
        return Response(content=image, media_type="image/bmp")

    @app.get("/api/themes")
    def list_themes(account: CurrentAccount, request: Request) -> Any:
        themes: ThemeStore = request.app.state.themes
        return {"themes": [row.to_public() for row in themes.list(str(account.household_id))]}

    @app.post("/api/themes")
    def add_theme(new: NewTheme, account: CurrentAccount, request: Request) -> Any:
        """Approve a subject the pictures may be about. It starts nothing on its own."""
        themes: ThemeStore = request.app.state.themes
        try:
            label = clean_label(new.label)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        theme = themes.add(make_theme(str(account.household_id), label, str(account.id)))
        return theme.to_public()

    @app.post("/api/themes/{theme_id}/remove")
    def remove_theme(theme_id: str, account: CurrentAccount, request: Request) -> Any:
        themes: ThemeStore = request.app.state.themes
        try:
            theme = themes.remove(str(account.household_id), theme_id)
        except Exception as exc:  # storage SDKs raise their own not-found types
            raise HTTPException(status_code=404, detail="unknown_theme") from exc
        return theme.to_public()

    @app.get("/api/device/{household_id}/themes")
    def device_themes(household_id: str, _: DeviceKey, request: Request) -> Any:
        """What the home server may paint about, as the parent last left it."""
        themes: ThemeStore = request.app.state.themes
        return {"themes": [row.to_public() for row in themes.list(household_id)]}

    @app.get("/api/rhythm")
    def read_rhythm(account: CurrentAccount, request: Request) -> Any:
        store: RhythmStore = request.app.state.rhythm
        return store.get(str(account.household_id)).to_public()

    @app.post("/api/rhythm")
    def write_rhythm(new: NewRhythm, account: CurrentAccount, request: Request) -> Any:
        """Record when the display may change. It persists and returns: the hub reads it
        on its next run, and nothing here reaches into the house."""
        store: RhythmStore = request.app.state.rhythm
        try:
            chosen = clean_rhythm(
                str(account.household_id),
                quiet_from=new.quietFrom,
                quiet_until=new.quietUntil,
                cadence_minutes=new.cadenceMinutes,
                updated_by=str(account.id),
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return store.set(chosen).to_public()

    @app.get("/api/device/{household_id}/rhythm")
    def device_rhythm(household_id: str, _: DeviceKey, request: Request) -> Any:
        """The hours and the spacing the hub applies, as the parent last left them."""
        store: RhythmStore = request.app.state.rhythm
        return store.get(household_id).to_public()

    @app.get("/api/preferences")
    def read_preferences(account: CurrentAccount, request: Request) -> Any:
        store: PreferencesStore = request.app.state.preferences
        return store.get(str(account.household_id)).to_public()

    @app.post("/api/preferences")
    def write_preferences(new: NewPreferences, account: CurrentAccount, request: Request) -> Any:
        """Record what the content is made of. It persists and returns: the hub reads it
        on its next run, and nothing here starts a generation."""
        store: PreferencesStore = request.app.state.preferences
        try:
            chosen = clean_preferences(
                str(account.household_id),
                interests=new.interests,
                avoid=new.avoid,
                difficulty=new.difficulty,
                variety=new.variety,
                max_words_per_line=new.maxWordsPerLine,
                language=new.language,
                updated_by=str(account.id),
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return store.set(chosen).to_public()

    @app.get("/api/device/{household_id}/preferences")
    def device_preferences(household_id: str, _: DeviceKey, request: Request) -> Any:
        """The settings the hub generates from, as the parent last left them. The hub adds
        the name locally; nothing that identifies a person has a field on this route."""
        store: PreferencesStore = request.app.state.preferences
        return store.get(household_id).to_public()

    @app.post("/api/device/{household_id}/devices")
    def report_devices(
        household_id: str, reported: list[ReportedDevice], _: DeviceKey, request: Request
    ) -> Any:
        """The hub says what it found, and is told what each thing is for.

        State, not history. The report never carries a job or a name: those are the
        parent's, and a discovery pass that overwrote them would undo a choice made in the
        panel every five minutes.
        """
        store: DeviceStatusStore = request.app.state.devices
        inventory: InventoryStore = request.app.state.inventory
        recorded: list[str] = []
        for item in reported:
            seen = item.lastSeen or time.time()
            if item.kind == KIND_DISPLAY:
                store.record(
                    DeviceStatus(
                        id=item.id,
                        household_id=household_id,
                        name=item.name or item.id,
                        last_seen=seen,
                        level=item.level,
                        voltage=item.voltage,
                        rssi=item.rssi,
                        firmware=item.firmware,
                        model=item.model,
                    )
                )
            inventory.see(
                Thing(
                    id=item.id,
                    household_id=household_id,
                    kind=item.kind,
                    label=item.name,
                    model=item.model,
                    address=item.address,
                    last_seen=seen,
                )
            )
            recorded.append(item.id)
        # The whole inventory comes back, not only what was just reported: the hub caches
        # it, and a printer that was switched off this minute still has a job.
        return {
            "recorded": recorded,
            "things": [row.to_public() for row in inventory.list(household_id)],
        }

    @app.get("/api/device/{household_id}/whoami")
    def whoami(household_id: str, _: DeviceKey) -> Any:
        """Which identity this container authenticates as. Claims only, never the token."""
        from .painting import identity_claims

        try:
            return identity_claims()
        except Exception as exc:
            raise HTTPException(status_code=503, detail=f"no token: {exc}") from exc

    @app.get("/api/devices")
    def list_devices(account: CurrentAccount, request: Request) -> Any:
        """Everything in the house, in one list, with whatever the hub last said about it."""
        store: DeviceStatusStore = request.app.state.devices
        inventory: InventoryStore = request.app.state.inventory
        household = str(account.household_id)
        return {
            "devices": merged(inventory.list(household), store.list(household)),
            # Stated while the parent types rather than enforced afterwards by truncation.
            "nameLimit": MAX_NAME_LENGTH,
        }

    @app.post("/api/devices/{thing_id}")
    def assign_device(
        thing_id: str, new: NewAssignment, account: CurrentAccount, request: Request
    ) -> Any:
        """Give a thing its job and its name. Nothing happens: choosing a printer prints
        nothing, and the hub finds out on its next run."""
        inventory: InventoryStore = request.app.state.inventory
        household = str(account.household_id)
        known = {row.id: row for row in inventory.list(household)}.get(thing_id)
        if known is None:
            raise HTTPException(status_code=404, detail="unknown_device")
        try:
            job = None if new.job is None else clean_job(known.kind, new.job)
            name = None if new.name is None else clean_name(new.name)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return inventory.assign(household, thing_id, job=job, name=name).to_public()

    @app.post("/api/devices/{thing_id}/remove")
    def forget_device(thing_id: str, account: CurrentAccount, request: Request) -> Any:
        """Take a thing off the list. Nothing leaves on its own for going quiet, so this
        is the only way out, and it is a decision somebody took."""
        inventory: InventoryStore = request.app.state.inventory
        inventory.forget(str(account.household_id), thing_id)
        return {"removed": thing_id}

    @app.post("/api/device/{household_id}/paint")
    async def paint_picture(
        household_id: str, _: DeviceKey, request: Request, theme: str = ""
    ) -> Any:
        """Paint one picture now, and hand back the bitmap ready for the panel.

        The home server calls this when it wants a new picture. Nothing here is scheduled:
        the cadence belongs to the house, which is the only place that knows what is
        happening in the room.
        """
        from devices.epaper import render_picture_bytes
        from shared.ids import new_id

        from .painting import choose_theme, paint

        settings: Settings = request.app.state.settings
        counter: UsageStore = request.app.state.usage
        if over_cap(counter, household_id, settings.monthly_picture_cap):
            # Reaching the cap is a decision, not a fault: the display keeps its picture.
            raise HTTPException(status_code=429, detail="monthly_cap_reached")

        themes: ThemeStore = request.app.state.themes
        chosen = theme or choose_theme([row.label for row in themes.list(household_id)])

        reported: list[Any] = []
        outcome = FAILED
        try:
            picture_id, image_b64, _ = await paint(chosen, on_usage=reported.append)
            outcome = SERVED
        except SafetyBlocked as exc:
            # A refused picture is a normal outcome: the display keeps what it has.
            outcome = REFUSED
            raise HTTPException(status_code=409, detail=f"refused: {exc}") from exc
        except (NoCapacityError, CloudUnavailable, ValueError) as exc:
            raise HTTPException(status_code=503, detail=f"unavailable: {exc}") from exc
        finally:
            try:
                counter.record(
                    event_from(
                        household_id,
                        KIND_IMAGE,
                        outcome,
                        reported[0] if reported else None,
                        event_id=str(new_id("use")),
                    )
                )
            except Exception as exc:  # noqa: BLE001 - bookkeeping must not eat a picture
                # The call was already made and paid for; failing here would spend the
                # money and deliver nothing. Loud in the log, silent to the house.
                logging.getLogger(__name__).warning("usage not recorded: %s", exc)

        bitmap = render_picture_bytes(image_b64)
        archive: PictureArchive = request.app.state.pictures
        archive.save(
            PictureRecord(
                id=picture_id,
                household_id=household_id,
                theme=chosen,
                created_at=time.time(),
            ),
            bitmap,
        )
        return {
            "id": picture_id,
            "theme": chosen,
            "imageBase64": base64.b64encode(bitmap).decode(),
        }

    @app.get("/api/usage")
    def read_usage(account: CurrentAccount, request: Request, period: str = "") -> Any:
        """What this household's pictures consumed this month, as the backend reported it.

        Numbers about machines, never about a person, and never a target to hit.
        """
        counter: UsageStore = request.app.state.usage
        settings: Settings = request.app.state.settings
        summary = counter.summary(
            str(account.household_id), period or month_of(time.time())
        )
        return {"usage": summary.to_public(), "cap": settings.monthly_picture_cap}

    return app


def _account_store(settings: Settings) -> AccountStore:
    if not settings.cosmos_configured:
        return InMemoryAccountStore()
    from .cosmos_store import CosmosAccountStore

    return CosmosAccountStore(settings.cosmos_endpoint, settings.cosmos_database)


def _proposal_store(settings: Settings) -> ProposalStore:
    if not settings.cosmos_configured:
        return InMemoryProposalStore()
    from .cosmos_store import CosmosProposalStore

    return CosmosProposalStore(settings.cosmos_endpoint, settings.cosmos_database)


def _picture_archive(settings: Settings) -> PictureArchive:
    if not settings.blob_configured:
        return InMemoryPictureArchive()
    from .pictures import BlobPictureArchive

    return BlobPictureArchive(settings.blob_endpoint, settings.pictures_container)


def _theme_store(settings: Settings) -> ThemeStore:
    if not settings.cosmos_configured:
        return InMemoryThemeStore()
    from .cosmos_store import CosmosThemeStore

    return CosmosThemeStore(settings.cosmos_endpoint, settings.cosmos_database)


def _device_store(settings: Settings) -> DeviceStatusStore:
    if not settings.cosmos_configured:
        return InMemoryDeviceStatusStore()
    from .cosmos_store import CosmosDeviceStatusStore

    return CosmosDeviceStatusStore(settings.cosmos_endpoint, settings.cosmos_database)


def _inventory_store(settings: Settings) -> InventoryStore:
    if not settings.cosmos_configured:
        return InMemoryInventoryStore()
    from .cosmos_store import CosmosInventoryStore

    return CosmosInventoryStore(settings.cosmos_endpoint, settings.cosmos_database)


def _usage_store(settings: Settings) -> UsageStore:
    if not settings.cosmos_configured:
        return InMemoryUsageStore()
    from .cosmos_store import CosmosUsageStore

    return CosmosUsageStore(settings.cosmos_endpoint, settings.cosmos_database)


def _rhythm_store(settings: Settings) -> RhythmStore:
    if not settings.cosmos_configured:
        return InMemoryRhythmStore()
    from .cosmos_store import CosmosRhythmStore

    return CosmosRhythmStore(settings.cosmos_endpoint, settings.cosmos_database)


def _preferences_store(settings: Settings) -> PreferencesStore:
    if not settings.cosmos_configured:
        return InMemoryPreferencesStore()
    from .cosmos_store import CosmosPreferencesStore

    return CosmosPreferencesStore(settings.cosmos_endpoint, settings.cosmos_database)


app = create_app()
