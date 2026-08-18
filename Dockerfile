# The panel. Only the panel: nothing here reads a camera or scans a sheet, so nothing here
# needs opencv. It does carry azure-cosmos and azure-identity, which store decisions and
# prove who is asking, plus Pillow and the image path of the router: the panel paints a
# picture when the server in the home asks for one.

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# pyproject is the single source of truth for versions, so the image cannot drift from
# what the tests ran against.
COPY pyproject.toml README.md ./
COPY shared/ ./shared/
COPY panel/ ./panel/
# Painting on request needs the one door to the models and the panel renderer.
COPY orchestrator/ ./orchestrator/
COPY devices/ ./devices/

RUN pip install --no-cache-dir ".[panel]"

RUN useradd --create-home --uid 10001 lanternina
USER 10001

# Must match apiTargetPort in infra/modules/app.bicep, or ingress accepts the connection
# and then times out with no useful error.
EXPOSE 8000

CMD ["uvicorn", "panel.app:app", "--host", "0.0.0.0", "--port", "8000"]
