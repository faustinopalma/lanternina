"""The panel the parent talks to.

Deliberately thin for now: a health check, and one route behind the gate. What it is
already careful about is the shape of a refusal — every denial returns the same body and
says nothing about whether the account exists, so the endpoint cannot be used to find out
which addresses are registered.
"""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from shared.accounts import Account, AccountStore
from shared.errors import AccessDenied, AuthNotConfigured

from .config import Settings
from .gate import resolve_account
from .principal import principal_from_headers
from .store import InMemoryAccountStore
from .tokens import TokenVerifier


def verifier_for(app: FastAPI) -> TokenVerifier | None:
    """Built on first use, so an identity provider that is unreachable at startup answers
    503 rather than stopping the container from starting at all."""
    settings: Settings = app.state.settings
    if not settings.oidc_configured:
        return None
    if app.state.verifier is None:
        app.state.verifier = TokenVerifier.from_authority(
            settings.oidc_authority, settings.oidc_audiences
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


def create_app(store: AccountStore | None = None, settings: Settings | None = None) -> FastAPI:
    app = FastAPI(title="Lanternina", docs_url=None, redoc_url=None)
    app.state.store = store if store is not None else InMemoryAccountStore()
    app.state.settings = settings if settings is not None else Settings.from_env()
    app.state.verifier = None

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

    return app


app = create_app()
