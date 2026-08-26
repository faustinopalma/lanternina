"""Where the panel's own account of itself goes.

Two things are set up here and they are not the same thing. **Logging** is lines this code
writes on purpose, and until this module existed nothing configured it — so every
``logger.info`` in the routes went nowhere, and the refusals that would have explained a
quiet afternoon were dropped before anybody could read them. **Telemetry** is the part
nobody writes: how long a request took, which model call was slow, which Cosmos query, and
which of them failed together. That is the half that cannot be recovered from lines.

Container Apps already carries stdout to the Log Analytics workspace `infra/modules/core.bicep`
creates, so a configured logger is enough to be readable in the cloud. Application Insights
is added on top for the second half, and it is optional at runtime: without a connection
string this module configures logging and returns, because the panel has to run on a laptop
with no Azure at all.

**What must not appear here.** A log line is read by whoever can reach the workspace, which
is a wider set than the people a household chose. Nothing in this container may log the
contents of a page that came back, what a reminder says, or anything a model wrote for a
particular person. Ids, counts, durations and outcomes are the vocabulary. `panel/trail.py`
is where what was generated is kept, on purpose and behind a parent's own login.
"""

from __future__ import annotations

import logging
import os
from typing import Any

# What the panel says about itself by default. INFO because the interesting lines are the
# refusals — a gate that said no, a check that caught a score — and those are not warnings:
# they are the system working. DEBUG would carry prompt-shaped material into a shared
# workspace, so it is available and never the default.
DEFAULT_LEVEL = "INFO"

# Azure SDKs log every HTTP request at INFO, which is thousands of lines an hour saying a
# token was fetched. Held at WARNING so the daily ingestion cap buys our own account of
# ourselves rather than the transport's.
#
# The whole `azure` tree rather than the loggers by name. Naming them looked tidier and was
# wrong within the hour: `azure.core.pipeline.policies.http_logging_policy` was silenced and
# `azure.cosmos._cosmos_http_logging_policy` was not, so every Cosmos response still printed
# its headers. A parent logger catches the one the next SDK version invents.
NOISY = (
    "azure",
    "urllib3",
    "httpx",
    "openai",
)

_started = False


def watch(app: Any = None) -> None:
    """Configure logging, and Application Insights when there is one to talk to.

    Idempotent, because a test that builds several apps in one process would otherwise add
    a handler per app and print every line as many times.
    """
    global _started
    if _started:
        return
    _started = True

    level = os.environ.get("LANTERNINA_LOG_LEVEL", DEFAULT_LEVEL).upper()
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        # The line the container writes is the line Log Analytics keeps, so the name of the
        # module has to be in it: `panel.devising` and `panel.routes.experience` are the
        # difference between a refusal to devise and a refusal to continue.
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        force=True,
    )
    for name in NOISY:
        logging.getLogger(name).setLevel(logging.WARNING)

    connection = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING", "").strip()
    if not connection:
        logging.getLogger(__name__).info("no application insights; logging to stdout only")
        return
    _to_azure(connection, app)


def _to_azure(connection: str, app: Any) -> None:
    """Send traces, dependencies and logs to Application Insights.

    Imported here rather than at the top because the package is an extra: a panel installed
    without it must start and serve, with one line saying what it is not doing. That is the
    same shape as every other cloud dependency here — unavailable means reduced capability,
    never a stopped system.
    """
    said = logging.getLogger(__name__)
    try:
        from azure.identity import DefaultAzureCredential
        from azure.monitor.opentelemetry import configure_azure_monitor
    except ImportError:
        said.warning("application insights configured but the package is not installed")
        return
    try:
        configure_azure_monitor(
            connection_string=connection,
            # The component is created with local auth off, so the instrumentation key in
            # the connection string is a name and not a credential. This is the same
            # identity that reads Cosmos and pulls the image.
            credential=DefaultAzureCredential(),
            # The distro instruments FastAPI, httpx and the Azure SDKs on its own, which is
            # the whole reason to use it: the dependency map is built from calls nobody
            # annotated, so it stays true as routes are added.
            logger_name="panel",
            instrumentation_options={
                # Off on purpose. The panel makes no outbound calls this would cover that
                # the httpx instrumentation does not already, and it doubles the spans.
                "psycopg2": {"enabled": False},
                "django": {"enabled": False},
                "flask": {"enabled": False},
            },
        )
    except Exception as exc:  # noqa: BLE001 - telemetry must not keep the panel from starting
        said.warning("application insights not configured: %s", exc)
        return
    if app is not None:
        _instrument(app, said)
    said.info("application insights is on")


def _instrument(app: Any, said: logging.Logger) -> None:
    """Trace each request, so a slow one can be opened rather than guessed at."""
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        FastAPIInstrumentor.instrument_app(
            app,
            # Health is called by the platform every few seconds and says nothing. Left in,
            # it is most of the spans and all of the cost.
            excluded_urls="health",
        )
    except Exception as exc:  # noqa: BLE001 - same reason as above
        said.warning("requests are not traced: %s", exc)
