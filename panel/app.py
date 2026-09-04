"""The panel the parent talks to — assembled here, and described elsewhere.

What this file does is put the application together: the stores it will use, the origins it
answers, the shape of a refusal, and the sections whose routes live in `panel/routes/`. It
held every one of those routes as well until 20 August 2026, by which point it was 987
lines: the file that says how the thing is built also said what each endpoint does.

Two routes stay here because they are about the application rather than about a section:
the health check, which is what a cold start is measured against, and `/api/me`, which is
the gate answering about itself.

Dashboard mutation routes persist state and return. They do not call models, enqueue work,
notify the home server or schedule processing. Work starts only on a separate request
initiated by the server in the home.
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from shared.accounts import AccountStore
from shared.errors import AccessDenied, AuthNotConfigured

from .config import Settings
from .devices import (
    DeviceStatusStore,
    InMemoryDeviceStatusStore,
    InMemoryInventoryStore,
    InventoryStore,
)
from .drafts import DraftStore, InMemoryDraftStore
from .experiences import ExperienceStore, InMemoryExperienceStore
from .gate import CurrentAccount
from .guidelines import GuidelineStore, InMemoryGuidelineStore
from .keeping import InMemoryKeepingStore, KeepingStore
from .messages import InMemoryMessageStore, MessageStore
from .observability import watch
from .pictures import InMemoryPictureArchive, PictureArchive
from .preferences import InMemoryPreferencesStore, PreferencesStore
from .profiles import InMemoryNoticedStore, NoticedStore
from .proposals import InMemoryProposalStore, ProposalStore
from .reminders import InMemorySentenceStore, SentenceStore
from .requests import InMemoryRequestStore, RequestStore
from .rhythm import InMemoryRhythmStore, RhythmStore
from .routes import admin, painting
from .routes import devices as device_routes
from .routes import draft as draft_routes
from .routes import experience as experience_routes
from .routes import guidelines as guideline_routes
from .routes import messages as message_routes
from .routes import paper as paper_routes
from .routes import pictures as picture_routes
from .routes import preferences as preference_routes
from .routes import proposals as proposal_routes
from .routes import reminders as reminder_routes
from .routes import requests as request_routes
from .routes import rhythm as rhythm_routes
from .routes import themes as theme_routes
from .routes import trail as trail_routes
from .routes import usage as usage_routes
from .routes import verdicts as verdict_routes
from .store import InMemoryAccountStore
from .themes import InMemoryThemeStore, ThemeStore
from .tokens import TokenVerifier
from .trail import InMemoryTrailStore, TrailStore
from .usage import InMemoryLimitStore, InMemoryUsageStore, LimitStore, UsageStore
from .what_happened import InMemoryWhatHappenedStore, WhatHappenedStore

# Registered in the order they were written in when they shared one file. No two of them
# claim the same path, so the order is a reading convenience and not a rule — but leaving
# it alone means no route changed behaviour by being moved.
SECTIONS = (
    admin,
    proposal_routes,
    picture_routes,
    theme_routes,
    reminder_routes,
    rhythm_routes,
    preference_routes,
    device_routes,
    painting,
    usage_routes,
    request_routes,
    experience_routes,
    message_routes,
    guideline_routes,
    paper_routes,
    trail_routes,
    draft_routes,
    # Temporary, for the weeks the prompts are being changed. `panel/routes/verdicts.py`
    # says what has to be true before it can go.
    verdict_routes,
)


def create_app(
    store: AccountStore | None = None,
    settings: Settings | None = None,
    proposals: ProposalStore | None = None,
    pictures: PictureArchive | None = None,
    themes: ThemeStore | None = None,
    devices: DeviceStatusStore | None = None,
    inventory: InventoryStore | None = None,
    usage: UsageStore | None = None,
    limit: LimitStore | None = None,
    rhythm: RhythmStore | None = None,
    preferences: PreferencesStore | None = None,
    reminders: SentenceStore | None = None,
    requests: RequestStore | None = None,
    experiences: ExperienceStore | None = None,
    messages: MessageStore | None = None,
    guidelines: GuidelineStore | None = None,
    trail: TrailStore | None = None,
    keeping: KeepingStore | None = None,
    what_happened: WhatHappenedStore | None = None,
    noticed: NoticedStore | None = None,
    drafts: DraftStore | None = None,
) -> FastAPI:
    app = FastAPI(title="Lanternina", docs_url=None, redoc_url=None)
    # Before anything else builds: a store that cannot reach Cosmos says so through a
    # logger, and until this ran there was no handler for it to say it through.
    watch(app)
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
    app.state.limit = limit if limit is not None else _limit_store(app.state.settings)
    app.state.rhythm = rhythm if rhythm is not None else _rhythm_store(app.state.settings)
    app.state.preferences = (
        preferences if preferences is not None else _preferences_store(app.state.settings)
    )
    app.state.reminders = (
        reminders if reminders is not None else _reminders_store(app.state.settings)
    )
    app.state.requests = (
        requests if requests is not None else _request_store(app.state.settings)
    )
    app.state.experiences = (
        experiences if experiences is not None else _experience_store(app.state.settings)
    )
    app.state.messages = (
        messages if messages is not None else _message_store(app.state.settings)
    )
    app.state.guidelines = (
        guidelines if guidelines is not None else _guideline_store(app.state.settings)
    )
    app.state.trail = trail if trail is not None else _trail_store(app.state.settings)
    app.state.keeping = (
        keeping if keeping is not None else _keeping_store(app.state.settings)
    )
    app.state.what_happened = (
        what_happened
        if what_happened is not None
        else _what_happened_store(app.state.settings)
    )
    app.state.noticed = (
        noticed if noticed is not None else _noticed_store(app.state.settings)
    )
    app.state.drafts = drafts if drafts is not None else _draft_store(app.state.settings)
    # Both identity providers are built on first use, by `panel/gate.py` and
    # `panel/admin.py`: one that is unreachable at startup must answer 503 rather than
    # keep the container from starting at all, so the slots begin empty.
    unbuilt: TokenVerifier | None = None
    app.state.verifier = unbuilt
    app.state.admin_verifier = unbuilt

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

    for section in SECTIONS:
        app.include_router(section.router)
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


def _experience_store(settings: Settings) -> ExperienceStore:
    if not settings.cosmos_configured:
        return InMemoryExperienceStore()
    from .cosmos_store import CosmosExperienceStore

    return CosmosExperienceStore(settings.cosmos_endpoint, settings.cosmos_database)


def _draft_store(settings: Settings) -> DraftStore:
    if not settings.cosmos_configured:
        return InMemoryDraftStore()
    from .cosmos_store import CosmosDraftStore

    return CosmosDraftStore(settings.cosmos_endpoint, settings.cosmos_database)


def _trail_store(settings: Settings) -> TrailStore:
    if not settings.cosmos_configured:
        return InMemoryTrailStore()
    from .cosmos_store import CosmosTrailStore

    return CosmosTrailStore(settings.cosmos_endpoint, settings.cosmos_database)


def _keeping_store(settings: Settings) -> KeepingStore:
    if not settings.cosmos_configured:
        return InMemoryKeepingStore()
    from .cosmos_store import CosmosKeepingStore

    return CosmosKeepingStore(settings.cosmos_endpoint, settings.cosmos_database)


def _what_happened_store(settings: Settings) -> WhatHappenedStore:
    if not settings.cosmos_configured:
        return InMemoryWhatHappenedStore()
    from .cosmos_store import CosmosWhatHappenedStore

    return CosmosWhatHappenedStore(settings.cosmos_endpoint, settings.cosmos_database)


def _noticed_store(settings: Settings) -> NoticedStore:
    if not settings.cosmos_configured:
        return InMemoryNoticedStore()
    from .cosmos_store import CosmosNoticedStore

    return CosmosNoticedStore(settings.cosmos_endpoint, settings.cosmos_database)


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


def _limit_store(settings: Settings) -> LimitStore:
    if not settings.cosmos_configured:
        return InMemoryLimitStore()
    from .cosmos_store import CosmosLimitStore

    return CosmosLimitStore(settings.cosmos_endpoint, settings.cosmos_database)


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


def _reminders_store(settings: Settings) -> SentenceStore:
    if not settings.cosmos_configured:
        return InMemorySentenceStore()
    from .cosmos_store import CosmosSentenceStore

    return CosmosSentenceStore(settings.cosmos_endpoint, settings.cosmos_database)


def _request_store(settings: Settings) -> RequestStore:
    if not settings.cosmos_configured:
        return InMemoryRequestStore()
    from .cosmos_store import CosmosRequestStore

    return CosmosRequestStore(settings.cosmos_endpoint, settings.cosmos_database)


def _message_store(settings: Settings) -> MessageStore:
    if not settings.cosmos_configured:
        return InMemoryMessageStore()
    from .cosmos_store import CosmosMessageStore

    return CosmosMessageStore(settings.cosmos_endpoint, settings.cosmos_database)


def _guideline_store(settings: Settings) -> GuidelineStore:
    if not settings.cosmos_configured:
        return InMemoryGuidelineStore()
    from .cosmos_store import CosmosGuidelineStore

    return CosmosGuidelineStore(settings.cosmos_endpoint, settings.cosmos_database)


app = create_app()
