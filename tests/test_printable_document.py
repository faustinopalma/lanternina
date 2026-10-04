from __future__ import annotations

import pytest

from printing.document import LayoutError, inspect, render, render_bounded


def source():
    return {"title": "Garden plan", "language": "en", "paragraphs": ["Plan a small garden."],
            "steps": ["Choose three objects. Draw them inside the plot without overlap.",
                      "Explain one choice using sunlight or shade."], "note": [],
            "spaces": [{"label": "Explain your choice", "room": "some_lines"}],
            "diagram": {"kind": "grid", "columns": 12, "row_count": 8, "split_at": 6,
                        "labels": ["Left six columns: sun. Right six columns: shade."]}}


def test_native_pdf_has_exact_text_embedded_fonts_and_preview():
    document = render(source())
    assert document.pdf.startswith(b"%PDF")
    assert len(document.previews) == 1
    assert document.previews[0].startswith(b"\x89PNG")
    audit = document.audit["selected"]
    assert audit["valid"] and audit["balanced"]
    assert audit["fonts"]
    assert inspect(document.pdf, ["missing text"])["missing"] == ["missing text"]


def test_model_text_is_literal_not_typst_code():
    data = source()
    data["steps"] = ['#read("secret.txt") [literal] $x$ <tag>']
    document = render(data)
    assert inspect(document.pdf, data["steps"])["missing"] == []


def test_separate_renderer_process_returns_complete_document():
    document = render_bounded(source())
    assert document.pdf.startswith(b"%PDF")
    assert len(document.previews) == document.audit["selected"]["pages"]


def test_table_caption_is_printed_and_checked():
    data = source()
    data["diagram"] = {"kind": "table", "labels": ["Follow the stages in order."],
                       "rows": [["Stage", "Minutes"], ["Harbor to Spring", "18"]]}
    document = render(data)
    assert not inspect(document.pdf, data["diagram"]["labels"])["missing"]


def test_grid_owns_the_drawing_field_without_an_extra_blank_box():
    import pymupdf

    data = source()
    data["spaces"].insert(0, {"label": "Garden drawing", "room": "a_box"})
    document = render(data)
    with pymupdf.open(stream=document.pdf, filetype="pdf") as pdf:
        rectangles = [drawing["rect"] for page in pdf for drawing in page.get_drawings()
                      if drawing["rect"].height > 1]
        assert len(rectangles) == 12 * 8
        assert "Garden drawing" in "".join(page.get_text() for page in pdf)


def test_excess_content_is_refused_instead_of_truncated():
    data = source()
    data["steps"] = ["Read all of this sentence. " * 60] * 12
    with pytest.raises(LayoutError):
        render(data)


def test_garden_instructions_balance_with_a_full_working_grid():
    data = source()
    data.update({
        "title": "Il piano del giardino", "language": "it",
        "paragraphs": [
            "Progetta un piccolo giardino immaginario: scegli tre elementi diversi, "
            "disponili sulla pianta e spiega una delle tue scelte. Ti servono questo "
            "foglio stampato e una penna.",
            "La griglia rappresenta il giardino visto dall'alto. Le dimensioni degli "
            "elementi sono espresse in caselle. Puoi scegliere liberamente quali tre "
            "usare e dove collocarli: non c'e una soluzione unica.",
        ],
        "steps": [
            "Leggi le dimensioni indicate nella legenda della griglia e scegli tre "
            "elementi diversi tra aiuola, panca, stagno e pergola.",
            "Disegna direttamente nella griglia Pianta: colloca i tre elementi i tre "
            "rettangoli scelti, rispettando le loro dimensioni, e scrivi il nome dentro "
            "ciascuno. Puoi ruotarli e puoi farli attraversare il confine tra sole e ombra, "
            "ma devono restare dentro il giardino e non sovrapporsi.",
            "Nella disposizione lascia completamente libero un quadrato di 2x2 caselle "
            "nella zona al sole e un altro di 2x2 caselle nella zona in ombra.",
            "Nello spazio Spiega una scelta con sole o ombra scrivi una frase che indichi "
            "quale elemento hai collocato in una certa posizione e perche, collegando "
            "la scelta al sole o all'ombra.",
            "Per finire, verifica che siano riconoscibili tre elementi diversi, con le "
            "dimensioni richieste e senza caselle condivise, che i due quadrati liberi "
            "siano presenti e che la frase spieghi una collocazione.",
        ],
        "spaces": [
            {"label": "Pianta: colloca i tre elementi", "room": "a_box"},
            {"label": "Spiega una scelta con sole o ombra", "room": "some_lines"},
        ],
    })
    data["diagram"]["labels"] = [
        "Griglia 12x8: 6 colonne a sinistra al sole, 6 a destra in ombra.",
        "Aiuola 4x2; panca 2x1; stagno 2x2; pergola 3x2. Misure in caselle.",
    ]
    document = render(data)
    selected = document.audit["selected"]
    assert selected["valid"] and selected["balanced"]
    assert selected["pages"] <= 2


@pytest.mark.asyncio
async def test_instruction_requests_screen_final_text_and_reject_truncation():
    import json
    from unittest.mock import AsyncMock

    from agents.document_writer import prepare
    from orchestrator.router import StubRouter
    from shared.agents import AgentContext
    from shared.ids import LearnerId
    from shared.page import Page, PageKind, Room, Space

    page = Page(PageKind.NOTEBOOK, "Garden", "", spaces=(Space("Reason", Room.A_LINE),))
    draft = {"language": "en", "paragraphs": ["Choose a place."],
             "steps": ["In Reason, explain the light."], "note": [],
             "field_coverage": ["Reason"], "diagram": None,
             "illustration": False, "asset_blockers": []}
    review = {"text_pass": True, "issues": [], "asset_blockers": []}
    router = StubRouter(replies=[json.dumps(draft), json.dumps(review)])
    context = AgentContext(router=router, learner_id=LearnerId(""), learner_hints={}, now=0)
    gate = AsyncMock()
    trace, usages = [], []
    result, image = await prepare(context, page, {"language": "en"}, gate=gate,
                                  trace=trace, usages=usages)
    assert result["steps"] == draft["steps"] and image is None
    assert len(router.seen) == 2
    assert all(request.max_output_chars == 24000 for request in router.seen)
    assert "In Reason, explain the light." in gate.screen.call_args.args[1]
    truncated = StubRouter(replies=["x" * 24001])
    context = AgentContext(router=truncated, learner_id=LearnerId(""), learner_hints={}, now=0)
    with pytest.raises(ValueError, match="truncated"):
        await prepare(context, page, {}, gate=gate, trace=[], usages=[])


def test_document_endpoint_preserves_master_and_household_isolation(monkeypatch):
    import base64
    from unittest.mock import AsyncMock

    from fastapi.testclient import TestClient

    from panel.app import create_app
    from panel.config import Settings
    from shared.page import Page, PageKind
    from tests.device_auth import bind_household

    app = create_app(settings=Settings(dev_auth=True, bootstrap_contact="p@example.test",
                                      device_key="test-device-key"))
    client = TestClient(app)
    parent = {"x-dev-subject": "parent", "x-dev-contact": "p@example.test"}
    household = client.get("/api/me", headers=parent).json()["householdId"]
    bind_household(client, household)
    document = render(source())
    monkeypatch.setattr("panel.paper.compose_document", AsyncMock(return_value=document))
    response = client.post(f"/api/device/{household}/page",
        headers={"X-Device-Key": "test-device-key"},
        json={"format": "pdf-v1", "document": {"language": "en"}, "runId": "run",
              "page": Page(PageKind.NOTEBOOK, "Garden", "A rectangular garden plot").to_dict()})
    assert response.status_code == 200, response.text
    assert base64.b64decode(response.json()["pdfBase64"]) == document.pdf
    rows = app.state.pages.list(household)
    master = next(row for row in rows if row.media == "application/pdf")
    path = f"/api/pages/{master.id}/content"
    downloaded = client.get(path, headers=parent)
    assert downloaded.content == document.pdf
    assert downloaded.headers["content-type"] == "application/pdf"
    assert client.get(path, headers={"x-dev-subject": "other"}).status_code != 200
    assert len(rows) == 3
    assert client.delete("/api/trail/run", headers=parent).status_code == 200
    assert app.state.pages.list(household) == []
    assert client.get(path, headers=parent).status_code == 404


def test_bulk_delete_covers_all_document_artifacts_without_trail_details(monkeypatch):
    from fastapi.testclient import TestClient

    from panel.app import create_app
    from panel.config import Settings
    from panel.pictures import PictureRecord

    app = create_app(settings=Settings(dev_auth=True, bootstrap_contact="p@example.test"))
    client = TestClient(app)
    parent = {"x-dev-subject": "parent", "x-dev-contact": "p@example.test"}
    household = client.get("/api/me", headers=parent).json()["householdId"]
    archive = app.state.pages
    for index in range(60):
        archive.save(PictureRecord(f"doc_{index}", household, "Document", index,
                                   kind="document"), b"artifact")
    archive.save(PictureRecord("old", household, "Raster", 0), b"raster")
    archive.save(PictureRecord("doc_other", "other", "Document", 0,
                               kind="document"), b"other family")
    monkeypatch.setattr(app.state.trail, "list", lambda _: [])
    assert client.delete("/api/trail", headers=parent).status_code == 200
    assert [record.id for record in archive.list(household, limit=None)] == ["old"]
    assert archive.get("other", "doc_other")[1] == b"other family"