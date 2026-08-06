# The panel. Only the panel: nothing here reads a camera, renders a sheet, or talks to a
# model, so nothing here needs opencv, Pillow or the Azure SDKs.

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# pyproject is the single source of truth for versions, so the image cannot drift from
# what the tests ran against.
COPY pyproject.toml README.md ./
COPY shared/ ./shared/
COPY panel/ ./panel/

RUN pip install --no-cache-dir ".[panel]"

RUN useradd --create-home --uid 10001 lanternina
USER 10001

# Must match apiTargetPort in infra/modules/app.bicep, or ingress accepts the connection
# and then times out with no useful error.
EXPOSE 8000

CMD ["uvicorn", "panel.app:app", "--host", "0.0.0.0", "--port", "8000"]
