"""Mechanical enforcement of the architectural boundaries.

These tests exist because a rule written in a document survives exactly as long as
everyone remembers it. Each test here corresponds to a claim made in the README and in
docs/ARCHITECTURE.md, and fails when that claim stops being true — including in a fork
whose author never read either file.

They inspect source with `ast` rather than importing, so a violation is caught even in a
module that cannot be imported (missing optional dependency, syntax under construction).
"""

from __future__ import annotations

import ast
import re
from dataclasses import fields
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
PACKAGES = ("shared", "orchestrator", "agents", "vision", "panel")


def _python_files(package: str) -> list[Path]:
    root = REPO / package
    if not root.is_dir():
        return []
    return [p for p in root.rglob("*.py") if "__pycache__" not in p.parts]


def _imported_modules(path: Path) -> set[str]:
    """Top-level module names imported by `path`, e.g. {'azure', 'agents'}."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            # level > 0 is a relative import: resolve it against the package on disk.
            if node.level:
                anchor = path.parent
                for _ in range(node.level - 1):
                    anchor = anchor.parent
                found.add(anchor.relative_to(REPO).parts[0])
            elif node.module:
                found.add(node.module.split(".")[0])
    return found


def _imported_paths(path: Path) -> set[str]:
    """Full dotted module names imported by `path`, e.g. {'azure.cosmos'}."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            found.add(node.module)
    return found


def _identifiers(path: Path) -> set[str]:
    """Identifiers defined or referenced in `path`. Excludes comments and docstrings."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.arg):
            names.add(node.arg)
        elif isinstance(node, ast.keyword) and node.arg:
            names.add(node.arg)
    return names


# ── Agents are isolated from each other ──────────────────────────────────────────────


def test_no_agent_imports_another_agent() -> None:
    """The planner composes agents. Agents must not know each other exist."""
    modules = {p.stem for p in _python_files("agents") if p.stem != "__init__"}
    for path in _python_files("agents"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            target = None
            if isinstance(node, ast.ImportFrom) and node.module:
                parts = node.module.split(".")
                if parts[0] == "agents" and len(parts) > 1:
                    target = parts[1]
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    parts = alias.name.split(".")
                    if parts[0] == "agents" and len(parts) > 1:
                        target = parts[1]
            if target and target in modules and target != path.stem:
                pytest.fail(
                    f"{path.relative_to(REPO)} imports agents.{target}. "
                    "Agents are composed by the planner, never wired to each other."
                )


FORBIDDEN_FOR_AGENTS = {"orchestrator", "panel", "vision", "httpx", "requests", "urllib3"}


def test_agents_reach_the_world_only_through_the_router() -> None:
    for path in _python_files("agents"):
        leaked = _imported_modules(path) & FORBIDDEN_FOR_AGENTS
        assert not leaked, (
            f"{path.relative_to(REPO)} imports {sorted(leaked)}. Agents get a ModelRouter "
            "in AgentContext and nothing else."
        )


# ── One router, one door to the models ───────────────────────────────────────────────

# Cloud inference SDKs: permitted only inside the router and the safety gate.
# Matched on the full dotted path, because `azure` alone is too coarse: `azure.identity`
# and `azure.cosmos` are infrastructure, not model backends. This rule protects the single
# door to inference, not the choice of database.
MODEL_SDK_PREFIXES = (
    "azure.ai.",
    "openai",
    "agent_framework",
    "anthropic",
)

# Everything `shared` must stay clear of. It is types and protocols: any SDK here would be
# inherited by every package that imports it.
CLOUD_SDKS = {
    "azure",
    "openai",
    "agent_framework",
    "anthropic",
}

# On-device inference runtimes: forbidden everywhere, including the router.
# No model runs on this device — the mini-PC executes conventional code only and every
# LLM/vision call goes to Microsoft Foundry. One inference path, not two.
LOCAL_RUNTIMES = {
    "transformers",
    "llama_cpp",
    "ctransformers",
    "onnxruntime",
    "onnxruntime_genai",
    "ollama",
    "vllm",
    "torch",
    "tensorflow",
    "mlx",
}


def test_only_the_router_touches_a_cloud_model_backend() -> None:
    """Every model call goes through orchestrator/router.py, so degradation and
    screening cannot be routed around by adding a second client somewhere."""
    allowed = {REPO / "orchestrator" / "router.py", REPO / "orchestrator" / "safety.py"}
    for package in PACKAGES:
        for path in _python_files(package):
            if path in allowed:
                continue
            leaked = sorted(
                module
                for module in _imported_paths(path)
                if module.startswith(MODEL_SDK_PREFIXES)
            )
            assert not leaked, (
                f"{path.relative_to(REPO)} imports {leaked}. "
                "Only the router may hold a model backend."
            )


def test_nothing_runs_a_model_on_the_device() -> None:
    """Inference is an Azure concern. The device renders images, serves a web panel, drives
    a printer and a scanner, and talks to serial.

    Adding an on-device runtime would create a second inference path with its own failure
    modes, its own content-safety story, and weights to ship and update. If that ever
    becomes the right call, it is a design decision — not something that arrives with a
    convenient import.
    """
    for package in PACKAGES:
        for path in _python_files(package):
            leaked = _imported_modules(path) & LOCAL_RUNTIMES
            assert not leaked, (
                f"{path.relative_to(REPO)} imports {sorted(leaked)}. No model runs on the "
                "device; see docs/ARCHITECTURE.md."
            )


def test_shared_stays_dependency_free() -> None:
    """`shared` is types and protocols. If it grows I/O, every package inherits it."""
    banned = (
        CLOUD_SDKS
        | LOCAL_RUNTIMES
        | {"cv2", "fastapi", "uvicorn", "serial", "requests", "httpx"}
    )
    for path in _python_files("shared"):
        leaked = _imported_modules(path) & banned
        assert not leaked, f"{path.relative_to(REPO)} imports {sorted(leaked)}"


# ── Agents cannot approve, and cannot see unscreened text ────────────────────────────


def test_proposal_has_no_field_an_agent_could_use_to_self_approve() -> None:
    from shared.proposal import Proposal

    names = {f.name for f in fields(Proposal)}
    forbidden = {"approved", "status", "state", "decision", "published", "delivered"}
    assert not (names & forbidden), (
        f"Proposal gained {sorted(names & forbidden)}. Approval state belongs to the "
        "ledger; a proposal must have nowhere to record its own verdict."
    )


def test_agent_context_carries_no_authority() -> None:
    from shared.agents import AgentContext

    names = {f.name for f in fields(AgentContext)}
    forbidden = {"ledger", "approval", "sealer", "key", "safety_key", "approval_key", "gate"}
    assert not (names & forbidden), (
        f"AgentContext gained {sorted(names & forbidden)}. An agent that can approve or "
        "seal its own output is the failure this design exists to prevent."
    )


def test_proposal_payload_is_screened_by_type() -> None:
    """The safety chokepoint is a type, not a convention: a Proposal cannot hold a
    bare string, so there is no path that puts unscreened text in front of the learner."""
    from shared.proposal import Proposal
    from shared.safety import ScreenedPayload

    payload = next(f for f in fields(Proposal) if f.name == "payload")
    assert payload.type in (ScreenedPayload, "ScreenedPayload"), (
        f"Proposal.payload is {payload.type!r}; it must be ScreenedPayload."
    )


def test_a_continuation_cannot_reach_a_house_without_passing_the_gate() -> None:
    """A continuation is not a Proposal, so no type is holding this one.

    A parent approves an experience once, from its overview, so what a continuation puts
    on a display has been read by no adult. Two things keep the gate on that path: the
    module that produces one calls it, and the route cannot produce one for itself.
    """
    producer = REPO / "panel" / "continuing.py"
    assert "screen_continuation" in _identifiers(producer), (
        f"{producer.relative_to(REPO)} hands a continuation to a house without screening "
        "it. See ideas/08 §2a."
    )
    route = REPO / "panel" / "routes" / "experience.py"
    assert "agents" not in _imported_modules(route), (
        f"{route.relative_to(REPO)} reaches an agent directly, which is a way round the "
        "gate in panel/continuing.py."
    )


def test_a_devised_afternoon_cannot_be_stored_without_passing_the_gate() -> None:
    """The same door, one step earlier. What is devised is stored where a parent reads
    it, so screening it after storage would mean the words were already kept."""
    producer = REPO / "panel" / "devising.py"
    assert "screen_experience" in _identifiers(producer), (
        f"{producer.relative_to(REPO)} offers an afternoon to a parent without screening "
        "it. See ideas/08 §2a."
    )


# ── What is left of the camera rules ─────────────────────────────────────────────────
#
# `vision/` is empty, so the test below currently guards nothing. It is kept as the shape
# of the check the handheld camera will need, not as evidence about the system today — the
# README says so in Status rather than claiming them in its table.
#
# Narrowed on 30 August 2026. The list used to name techniques rather than uses:
# `landmarks` is how a scanned sheet is deskewed, `detectMultiScale` finds a printed
# marker as readily as a face, and `imwrite` is how anybody debugs an image pipeline. A ban
# on those forbids the tooling and not the harm, and the harm has a name: taking a person
# as the subject. What is left is the vocabulary that only makes sense pointed at somebody,
# plus continuous capture, which is a different thing again.

FORBIDDEN_IN_VISION = {
    # inference about a person, forbidden even as an intermediate step
    "FaceDetectorYN",
    "FaceRecognizerSF",
    "face_recognition",
    "detect_faces",
    "face_encodings",
    "emotion",
    "affect",
    "gaze",
    "age_estimate",
    "gender",
    "identify_person",
    # continuous capture: a frame nobody asked for
    "StreamingResponse",
    "VideoWriter",
}


def test_vision_does_not_look_at_people_or_stream() -> None:
    """Faces will be in frame; what is forbidden is inferring anything from them.

    Where a photograph goes is not enforced here. It is enforced by `RawFrame`, which
    raises rather than being pickled, copied or written out — a guarantee about the object
    rather than a guess from an identifier.
    """
    for path in _python_files("vision"):
        leaked = _identifiers(path) & FORBIDDEN_IN_VISION
        assert not leaked, (
            f"{path.relative_to(REPO)} references {sorted(leaked)}. Nothing here takes a "
            "person as its subject, and nothing captures without a button press."
        )


def test_raw_frames_cannot_be_serialised() -> None:
    """The seal on a type nothing constructs. Kept as a working technique, not as a
    guarantee the product makes — see shared/vision_contracts.py."""
    import copy
    import pickle

    import shared.vision_contracts as vc
    from shared.errors import RetentionViolation

    frame = vc.RawFrame.__new__(vc.RawFrame)  # no numpy needed to test the escape hatches
    for attempt in (
        lambda: pickle.dumps(frame),
        lambda: copy.copy(frame),
        lambda: copy.deepcopy(frame),
        frame.__getstate__,
    ):
        with pytest.raises(RetentionViolation):
            attempt()


# ── What a returned page said is read, and not kept ──────────────────────────────────


def test_what_a_page_said_cannot_be_pickled_copied_or_cached() -> None:
    """The reading lasts as long as the afternoon needs it.

    The one door left open is `to_dict`, which is the body of the request that carries the
    reading to the panel writing the continuation. Everything else is closed, because none
    of it is how somebody would decide to keep a reading — it is how one ends up kept
    anyway, in a cache, on a queue, in a session, in a background job's payload.

    That a reading is never written down is enforced elsewhere and by absence:
    `tests/test_trail.py` names the fields the record has, and none of them would hold one.
    """
    import copy
    import pickle

    from shared.errors import RetentionViolation
    from shared.vision_contracts import WhatCameBack

    reading = WhatCameBack(
        written=True, same_sheet=True, describes=("three lines at the top",), read_at=1.0
    )
    for attempt in (
        lambda: pickle.dumps(reading),
        lambda: copy.copy(reading),
        lambda: copy.deepcopy(reading),
        reading.__getstate__,
    ):
        with pytest.raises(RetentionViolation):
            attempt()
    assert reading.to_dict()["describes"] == ["three lines at the top"]


# ── Where a verdict would do damage: the schema, the panel, the prompts ──────────────

# **These were one set until 4 September 2026, and holding them together was the mistake.**
# They are two different commitments and only one of them still stands everywhere.
#
# Hooking is refused outright: nothing here may work by making it hard to stop, and that is
# a property of the product rather than of where a word appears. The list stays enforced in
# the stored shape, in the panel, in the browser and in the prompts.
ENGAGEMENT = {
    "streak",
    "streaks",
    "daily_goal",
    "goal_met",
    "time_spent",
    "session_length",
    "engagement",
    "engagement_score",
    "retention",
    "leaderboard",
    "points",
    "xp",
    "level_up",
}

# Judgement is now a thing the system keeps and never a thing it shows. The rule that no
# record of how somebody is doing may exist anywhere was removed on 4 September 2026: a
# profile is kept at system level, it is what lets an afternoon be pitched at the right
# level, and refusing to hold one was refusing to do the work well.
#
# What did not move is where it may appear. It reaches the model that writes an afternoon
# and the model that runs one. It reaches no display, no sheet, and no page a parent reads.
# So this list is still enforced in the browser and still refused as a field a prompt asks a
# model to fill in — and is no longer refused across `shared` and `panel`, because that is
# where the profile has to live.
ASSESSMENT = {
    "score",
    "scores",
    "grade",
    "grades",
    "rating",
    "ranking",
    "accuracy_rate",
    "success_rate",
    "progress_percent",
    "ability",
    "proficiency",
    "mastery",
    "diagnosis",
}

# `shared` is the document format and `panel` is what a parent reads, so a name that
# appears here is a name that gets written down or shown. `shared/blocklist.py` is the one
# file that has to spell the words, because listing them is what it is for.
SCHEMA_AND_PANEL = ("shared", "panel")
NAMES_THE_WORDS_ON_PURPOSE = "shared/blocklist.py"


def _stored_or_shown_names(path: Path) -> set[str]:
    """Names that survive the process: keys in a document, and fields of a type."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            names.add(node.value)
        elif isinstance(node, ast.ClassDef):
            for statement in node.body:
                if isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
                    names.add(statement.target.id)
    return names


def test_nothing_stored_or_shown_works_by_making_it_hard_to_stop() -> None:
    """Narrowed on 27 August 2026 from every identifier to the stored shape and the panel,
    and narrowed again on 4 September to hooking alone.

    The wide version was a lint on words standing in for a ban on behaviour. It ruled out
    calling a content setting `difficulty`, a puzzle's in-fiction tally `score`, or a job's
    advancement `progress` — none of which is a claim about anybody. What is left is the one
    thing no field may hold whatever the code around it says: a streak, a daily goal, a
    figure for time spent. Those are the machinery of retention and this system refuses it.
    """
    offences: list[str] = []
    for package in SCHEMA_AND_PANEL:
        for path in _python_files(package):
            where = path.relative_to(REPO).as_posix()
            if where == NAMES_THE_WORDS_ON_PURPOSE:
                continue
            leaked = _stored_or_shown_names(path) & ENGAGEMENT
            if leaked:
                offences.append(f"{where}: {sorted(leaked)}")
    assert not offences, "hooking vocabulary in the stored shape:\n" + "\n".join(offences)


def test_the_panel_in_the_browser_shows_neither_a_hook_nor_a_verdict() -> None:
    """Both lists, on the other side of the wire, and this is where the second one survives.

    A profile is kept and it is not shown. The panel is where a number about a person would
    be easiest to add and hardest to notice — it already draws counts, dates and lists — so
    the browser is the surface the rule is written on. `_` is optional in the pattern so a
    camelCase spelling is caught as readily as a snake_case one.
    """
    words = "|".join(term.replace("_", "_?") for term in sorted(ENGAGEMENT | ASSESSMENT))
    marker = re.compile(rf"(?i)(?<![\w-])({words})(?![\w-])")

    offences: list[str] = []
    for path in (REPO / "web" / "src").rglob("*.ts*"):
        found = sorted({m.group(0) for m in marker.finditer(path.read_text(encoding="utf-8"))})
        if found:
            offences.append(f"{path.relative_to(REPO)}: {found}")
    assert not offences, "engagement/assessment vocabulary in the panel:\n" + "\n".join(
        offences
    )


def test_no_prompt_asks_a_model_for_a_verdict() -> None:
    """A prompt may forbid a score — several do, and that is the sentence working.

    What it may not do is ask for one, so the check is on the field names a prompt declares
    rather than on the word: `"score":` in a shape the model is told to fill in, never `no
    score` in a sentence telling it not to.

    Both lists, and the second one is deliberate: a profile is written by something that
    weighs what happened, never by asking the model that just wrote an afternoon to grade
    the person who did it.
    """
    words = "|".join(sorted(ENGAGEMENT | ASSESSMENT))
    asked_for = re.compile(rf"""["']({words})["']\s*:""")

    offences: list[str] = []
    prompts = [
        *(REPO / "agents").rglob("*.md"),
        *(REPO / "shared").rglob("*.md"),
        *(REPO / "docs" / "prompts").rglob("*.md"),
    ]
    for path in prompts:
        found = sorted({m.group(1) for m in asked_for.finditer(path.read_text("utf-8"))})
        if found:
            offences.append(f"{path.relative_to(REPO)}: {found}")
    assert not offences, "a prompt asks a model for a verdict:\n" + "\n".join(offences)


# ── The content language is a setting, not a property of the data ────────────────────

# The two files that translate between the stored shape and the current one. They are the
# only place in the running system where an Italian key may be named; everywhere else it
# would put the language back into the data. `web/src/test/` is excluded for the same
# reason `tests/` is not scanned at all: a fixture has to be able to spell the old shape.
LEGACY_KEY_READERS = ("shared/exercise.py", "web/src/lib/sheet.ts")
LEGACY_KEY_FIXTURES = "web/src/test/"


def test_no_italian_field_name_outside_the_two_readers() -> None:
    """A body in English would otherwise still be a document with a field called `domanda`.

    Prose is not the target: the prompts are written in Italian and say "scelte" in a
    sentence. What is forbidden is naming a key. In Python that means a quoted literal,
    because a dict key always carries its quotes; in TypeScript also a property access or
    an object-literal key, because there it usually does not.
    """
    from shared.exercise import LEGACY_KEYS

    words = "|".join(sorted(LEGACY_KEYS.values()))
    in_python = re.compile(rf"""["']({words})["']""")
    in_typescript = re.compile(rf"""[.'"]({words})\b|\b({words})\s*\??\s*:""")

    offences: list[str] = []
    for package in (*PACKAGES, "devices", "tools", "printing"):
        for path in _python_files(package):
            where = path.relative_to(REPO).as_posix()
            found = sorted({m.group(1) for m in in_python.finditer(path.read_text("utf-8"))})
            if found and where not in LEGACY_KEY_READERS:
                offences.append(f"{where}: {found}")
    for path in (REPO / "web" / "src").rglob("*.ts*"):
        where = path.relative_to(REPO).as_posix()
        if where in LEGACY_KEY_READERS or where.startswith(LEGACY_KEY_FIXTURES):
            continue
        found = sorted({m.group(0) for m in in_typescript.finditer(path.read_text("utf-8"))})
        if found:
            offences.append(f"{where}: {found}")
    assert not offences, "Italian field names outside the readers:\n" + "\n".join(offences)
