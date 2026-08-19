"""The server in the home, driving both halves of the loop.

Two commands, and the direction of each is the point:

``offer``  generates a batch and offers it to the panel for review. Nothing is shown to
           anyone as a result.
``show``   asks the panel what the parent approved, verifies the safety seal itself,
           mints the approval seal with a key the cloud does not have, and renders the
           result for the display.

Both are started here, in the house. The cloud never pushes anything down: it answers
questions it was asked. That is why the panel has no way to reach this machine.

The seal keys must be stable across runs, because the safety seal is minted while
generating and verified later in a different process. Ephemeral keys would fail closed —
correctly, but confusingly — so this refuses to start without them.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from agents.content import HouseholdContentAgent
from devices.epaper import render_epaper_bmp, render_epaper_png, render_picture_bmp
from orchestrator.router import FoundryConfig, FoundryRouter
from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig
from shared.agents import AgentContext
from shared.approval import ApprovalDecision, ApprovalState, ApprovedItem
from shared.domain import ActivityKind, ContentVariety, Difficulty, LearnerProfile
from shared.errors import SafetyBlocked, UnusableGeneration
from shared.ids import LearnerId, ProposalId, new_proposal_id, new_request_id
from shared.proposal import Proposal, ProposalKind
from shared.routing import Capability, ModelRequest
from shared.safety import (
    ContentKind,
    SafetyCategory,
    SafetyVerdict,
    ScreenedPayload,
    ScreeningRecord,
)
from shared.seal import Seal, Sealer, SealPurpose
from tools.generate_batch import ROUTINE_STEPS, TOPICS

# Who the learner is stays in the house: both come from the gitignored .env, neither has a
# field in the panel, and prompt_hints() is what keeps them out of every prompt.
LOCAL_LEARNER_ID = LearnerId(os.environ.get("LANTERNINA_LEARNER_ID", "lr_local"))
LOCAL_LEARNER_NAME = os.environ.get("LANTERNINA_LEARNER_NAME", "")

# The fallback list, used only when the panel cannot be reached. The real themes are the
# ones the parent keeps in the panel; these exist so a picture can still be painted when
# the cloud is down, which is the one thing that must not stop.
#
# Approving a theme rather than each picture is what makes an hourly change possible at
# all. It is also a real weakening, and worth naming: a picture goes up that no adult has
# seen.
# What is left in its place is narrower — the theme bounds the subject, the safety gate
# screens every picture, and the parent can withdraw a theme at any time.
APPROVED_THEMES = (
    "animali del bosco",
    "il sistema solare",
    "fiori di campo",
    "gatti che dormono",
    "montagne e nuvole",
    "frutta sul tavolo di cucina",
)

# Written for a screen with two levels and no backlight: fine detail and text both
# disappear once the picture is dithered, so neither is asked for.
PICTURE_PROMPT = (
    "Black and white ink illustration of {theme}. Bold clean outlines, large simple "
    "shapes, strong contrast, generous white space, calm and friendly. "
    "No text, no letters, no numbers, no watermark, no border, no frame."
)

# What the panel says when its own battery is emptying. It has to be understood without
# reading, so it is carried entirely by the picture: no number, no bar, no icon.
_STYLE = (
    "Black and white ink illustration, bold clean outlines, large simple shapes, strong "
    "contrast, generous white space. No text, no letters, no numbers, no watermark, "
    "no border, no frame."
)
BATTERY_PROMPTS = {
    # About a fifth left: a remark, not an alarm.
    "low": (
        f"{_STYLE} A small paper lantern sitting on a windowsill at dusk, its flame "
        "burned low and gentle, a thin curl of smoke, one moth keeping it company. "
        "Quiet and warm, slightly sleepy, not sad."
    ),
    # About a tenth left: theatrical on purpose, and funny rather than distressing.
    "critical": (
        f"{_STYLE} A little paper lantern character with tiny arms, flopped backwards "
        "across a cushion like an opera singer fainting, one hand on its forehead, its "
        "flame reduced to a single spark. A cat watches, unimpressed. Comic and "
        "theatrical, affectionate, clearly a joke and not frightening."
    ),
}


def _keys() -> tuple[bytes, bytes]:
    safety = os.environ.get("LANTERNINA_SAFETY_KEY", "")
    approval = os.environ.get("LANTERNINA_APPROVAL_KEY", "")
    if not safety or not approval:
        raise SystemExit(
            "set LANTERNINA_SAFETY_KEY and LANTERNINA_APPROVAL_KEY: the loop spans two "
            "processes, so the seals have to outlive one of them"
        )
    return safety.encode(), approval.encode()


def learner_profile(panel: str, household: str, key: str) -> LearnerProfile:
    """The household's settings, as the parent last left them in the panel.

    The name and id are added here and only here. Everything else comes down from the
    panel, which holds exactly the fields `prompt_hints()` allows out and no other.

    A silent panel gives the plain defaults rather than stopping the batch: cloud
    unavailable means content that is less tuned, not a house with nothing to offer.
    """
    request = urllib.request.Request(
        f"{panel}/api/device/{household}/preferences", headers={"X-Device-Key": key}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            answer = json.loads(response.read())
        return LearnerProfile(
            id=LOCAL_LEARNER_ID,
            display_name=LOCAL_LEARNER_NAME,
            interests=tuple(str(item) for item in answer.get("interests") or ()),
            avoid=tuple(str(item) for item in answer.get("avoid") or ()),
            default_difficulty=Difficulty(str(answer["difficulty"])),
            content_variety=ContentVariety(str(answer["variety"])),
            max_words_per_line=int(answer["maxWordsPerLine"]),
            language=str(answer["language"]),
        )
    except (urllib.error.URLError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"non leggo le impostazioni del nucleo ({exc}): uso quelle di partenza")
        return LearnerProfile(id=LOCAL_LEARNER_ID, display_name=LOCAL_LEARNER_NAME)


def _request(url: str, key: str, *, payload: Any = None) -> Any:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        headers={"X-Device-Key": key, "Content-Type": "application/json"},
        method="POST" if data is not None else "GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"the panel refused the request: HTTP {exc.code} {exc.read()!r}") from exc


async def offer(args: argparse.Namespace) -> int:
    safety_key, _ = _keys()
    profile = learner_profile(args.panel, args.household, args.key)
    topics = profile.interests or TOPICS
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(dict(os.environ)),
        Sealer(SealPurpose.CONTENT_SAFETY, safety_key, "orchestrator.safety"),
    )
    try:
        router = FoundryRouter(FoundryConfig.from_env(dict(os.environ)), gate=gate)
        agent = HouseholdContentAgent()
        ctx = AgentContext.for_learner(router, profile, time.time())

        produced: list[Proposal] = []
        for index in range(args.exercises):
            try:
                produced.append(
                    await agent.propose_exercise(
                        ctx,
                        kind=ActivityKind.PRINTED_EXERCISE,
                        difficulty=profile.default_difficulty,
                        topic_hint=topics[index % len(topics)],
                    )
                )
            except (SafetyBlocked, UnusableGeneration) as exc:
                print(f"scartata: {type(exc).__name__}: {exc}")
        for index in range(args.prompts):
            label, at = ROUTINE_STEPS[index % len(ROUTINE_STEPS)]
            try:
                produced.append(await agent.propose_routine_prompt(ctx, step_label=label, at=at))
            except (SafetyBlocked, UnusableGeneration) as exc:
                print(f"scartata: {type(exc).__name__}: {exc}")
    finally:
        await gate.aclose()

    body = [
        {
            "id": str(proposal.id),
            "kind": str(proposal.kind),
            "agent": proposal.agent,
            "rationale": proposal.rationale,
            "createdAt": proposal.created_at,
            "payload": proposal.payload.sealable(),
            "payloadSeal": proposal.payload.seal.to_dict(),
        }
        for proposal in produced
    ]
    stored = _request(f"{args.panel}/api/device/{args.household}/proposals", args.key, payload=body)
    for proposal in produced:
        print(f"  {proposal.kind}: {proposal.rationale}")
    print(f"\n{len(stored['stored'])} proposte in attesa di revisione nel pannello")
    return 0


def show(args: argparse.Namespace) -> int:
    safety_key, approval_key = _keys()
    answer = _request(
        f"{args.panel}/api/device/{args.household}/proposals?state=approved", args.key
    )
    rows = answer["proposals"]
    if not rows:
        print("il genitore non ha ancora approvato niente: lascio lo schermo com'e")
        return 0

    wanted = str(args.kind)
    chosen = [row for row in rows if row["kind"] == wanted] or rows
    row = chosen[-1]

    item = _approved_item(row, approval_key)
    render = render_epaper_bmp if args.out.suffix.lower() == ".bmp" else render_epaper_png
    image = render(item, safety_key=safety_key, approval_key=approval_key)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(image)
    print(f"approvato: {row['rationale']}")
    print(f"schermo:   {args.out} ({len(image)} byte)")
    return 0


def _approved_themes(args: argparse.Namespace) -> tuple[tuple[str, ...], str]:
    """The themes the parent keeps in the panel, or the local fallback, and which it was."""
    if not (args.panel and args.household and args.key):
        return APPROVED_THEMES, "elenco locale"
    try:
        answer = _request(f"{args.panel}/api/device/{args.household}/themes", args.key)
    except (SystemExit, urllib.error.URLError, OSError):
        return APPROVED_THEMES, "elenco locale (pannello irraggiungibile)"
    labels = tuple(str(row["label"]) for row in answer.get("themes", []))
    if not labels:
        return APPROVED_THEMES, "elenco locale (nessun tema nel pannello)"
    return labels, "pannello"


async def picture(args: argparse.Namespace) -> int:
    """Paint one picture from an approved theme and render it for the display."""
    safety_key, approval_key = _keys()
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(dict(os.environ)),
        Sealer(SealPurpose.CONTENT_SAFETY, safety_key, "orchestrator.safety"),
    )
    theme = args.theme or random.choice(APPROVED_THEMES)
    prompt = PICTURE_PROMPT.format(theme=theme)
    source = "scelto a mano" if args.theme else ""
    if not args.theme:
        approved, source = _approved_themes(args)
        theme = random.choice(approved)
        prompt = PICTURE_PROMPT.format(theme=theme)
    if args.battery:
        # The parent approves themes for the pictures; this one is the panel talking
        # about itself, so it does not come from that list.
        theme = f"avviso batteria: {args.battery}"
        prompt = BATTERY_PROMPTS[args.battery]
        source = "avviso di sistema"
    try:
        router = FoundryRouter(FoundryConfig.from_env(dict(os.environ)), gate=gate)
        started = time.perf_counter()
        payload = await router.generate_for_user(
            ModelRequest(
                capability=Capability.IMAGE_GENERATION,
                prompt=prompt,
                request_id=new_request_id(),
                purpose=f"picture/{theme}",
                content_kind=ContentKind.IMAGE_PNG,
                metadata={"size": args.size},
            )
        )
        elapsed = time.perf_counter() - started
    finally:
        await gate.aclose()

    item = _picture_item(payload, theme, approval_key)
    image = render_picture_bmp(item, safety_key=safety_key, approval_key=approval_key)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(image)

    severities = ", ".join(f"{k}={v}" for k, v in sorted(payload.record.severities.items()))
    print(f"tema:      {theme}")
    print(f"origine:   {source}")
    print(f"screening: {payload.record.verdict} ({severities or 'nessuna categoria'})")
    print(f"generata in {elapsed:.1f}s")
    print(f"schermo:   {args.out} ({len(image)} byte, 800x480, 1 bit)")
    if args.keep_source:
        source = args.out.with_suffix(".source.png")
        source.write_bytes(base64.b64decode(payload.body))
        print(f"originale: {source}")

    if args.panel and args.household and args.key:
        record = _request(
            f"{args.panel}/api/device/{args.household}/pictures",
            args.key,
            payload={
                "id": str(item.proposal.id),
                "theme": theme,
                "kind": args.battery or "ok",
                "createdAt": item.proposal.created_at,
                "imageBase64": base64.b64encode(image).decode(),
            },
        )
        print(f"archiviata: {record['id']}")
    return 0


def restore(args: argparse.Namespace) -> int:
    """Put a picture from the archive back on the display."""
    if args.id:
        answer = _request(
            f"{args.panel}/api/device/{args.household}/pictures/{args.id}", args.key
        )
        image = base64.b64decode(answer["imageBase64"])
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_bytes(image)
        print(f"ripristinata: {answer['theme'] or answer['id']}")
        print(f"schermo:      {args.out} ({len(image)} byte)")
        return 0

    listed = _request(f"{args.panel}/api/device/{args.household}/pictures", args.key)
    rows = listed["pictures"]
    if not rows:
        print("l'archivio e vuoto")
        return 0
    for row in rows:
        when = time.strftime("%d/%m %H:%M", time.localtime(row["createdAt"]))
        print(f"  {row['id']}  {when}  {row['kind']:8}  {row['theme']}")
    print(f"\n{len(rows)} immagini. Rimettine una con --id <id>.")
    return 0


def _picture_item(payload: ScreenedPayload, theme: str, approval_key: bytes) -> ApprovedItem:
    """Seal a picture as approved because its theme was approved.

    The decision records the theme it inherits from, so a picture can always be traced
    back to the thing the parent actually said yes to.
    """
    proposal = Proposal(
        id=new_proposal_id(),
        kind=ProposalKind.PICTURE,
        agent="picture",
        learner_id=LOCAL_LEARNER_ID,
        payload=payload,
        rationale=f"tema approvato: {theme}",
        created_at=time.time(),
    )
    decision = ApprovalDecision(
        proposal_id=proposal.id,
        state=ApprovalState.APPROVED,
        decided_by=f"theme:{theme}",
        decided_at=time.time(),
        note="il genitore ha approvato il tema, non questa singola immagine",
    )
    sealer = Sealer(SealPurpose.PARENT_APPROVAL, approval_key, "home-server")
    draft = {"proposal": proposal.sealable(), "decision": decision.to_dict()}
    return ApprovedItem(proposal=proposal, decision=decision, seal=sealer.seal(draft))


def _approved_item(row: dict[str, Any], approval_key: bytes) -> ApprovedItem:
    """Rebuild what the cloud stored, then seal the parent's decision locally.

    The approval seal is minted here and nowhere else: the cloud holds the record of the
    decision, never the authority to make content deliverable.
    """
    payload = _payload_from(row["payload"], row["payloadSeal"])
    proposal = Proposal(
        id=ProposalId(str(row["id"])),
        kind=ProposalKind(str(row["kind"])),
        agent=str(row["agent"]),
        learner_id=LOCAL_LEARNER_ID,
        payload=payload,
        rationale=str(row.get("rationale") or ""),
        created_at=float(row.get("createdAt") or 0.0),
        expires_at=row.get("expiresAt"),
    )
    decision = ApprovalDecision(
        proposal_id=proposal.id,
        state=ApprovalState.APPROVED,
        decided_by=str(row.get("decidedBy") or "parent"),
        decided_at=float(row.get("decidedAt") or time.time()),
    )
    sealer = Sealer(SealPurpose.PARENT_APPROVAL, approval_key, "home-server")
    draft = {"proposal": proposal.sealable(), "decision": decision.to_dict()}
    return ApprovedItem(proposal=proposal, decision=decision, seal=sealer.seal(draft))


def _payload_from(payload: dict[str, Any], seal: dict[str, Any]) -> ScreenedPayload:
    record = payload["record"]
    return ScreenedPayload(
        kind=ContentKind(str(payload["kind"])),
        body=str(payload["body"]),
        record=ScreeningRecord(
            verdict=SafetyVerdict(str(record["verdict"])),
            severities={
                SafetyCategory(name): int(value)
                for name, value in (record.get("severities") or {}).items()
            },
            screener=str(record.get("screener") or ""),
            policy_version=str(record.get("policy_version") or "0"),
            screened_at=float(record.get("screened_at") or 0.0),
            detail=str(record.get("detail") or ""),
        ),
        seal=Seal(
            purpose=SealPurpose(str(seal["purpose"])),
            digest=str(seal["digest"]),
            signature=str(seal["signature"]),
            issued_at=float(seal["issued_at"]),
            issuer=str(seal["issuer"]),
            version=int(seal.get("version") or 1),
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", default="", help="base URL of the panel API")
    parser.add_argument("--household", default="")
    parser.add_argument("--key", default=os.environ.get("LANTERNINA_DEVICE_KEY", ""))
    sub = parser.add_subparsers(dest="command", required=True)

    offer_parser = sub.add_parser("offer", help="generate a batch and send it for review")
    offer_parser.add_argument("--exercises", type=int, default=2)
    offer_parser.add_argument("--prompts", type=int, default=2)

    show_parser = sub.add_parser("show", help="render what the parent approved")
    show_parser.add_argument("--kind", default=ProposalKind.ROUTINE_PROMPT.value)
    show_parser.add_argument("--out", type=Path, default=Path("build/display.bmp"))

    picture_parser = sub.add_parser("picture", help="paint one picture from an approved theme")
    picture_parser.add_argument("--theme", default="", help="defaults to one at random")
    picture_parser.add_argument(
        "--battery",
        choices=sorted(BATTERY_PROMPTS),
        default="",
        help="paint the notice the panel shows about its own battery instead",
    )
    picture_parser.add_argument("--size", default="1536x1024")
    picture_parser.add_argument("--out", type=Path, default=Path("build/picture.bmp"))
    picture_parser.add_argument("--keep-source", action="store_true")

    restore_parser = sub.add_parser("restore", help="list the archive, or put one picture back")
    restore_parser.add_argument("--id", default="", help="omit to list what is kept")
    restore_parser.add_argument("--out", type=Path, default=Path("build/display.bmp"))

    args = parser.parse_args()
    if args.command == "picture":
        return asyncio.run(picture(args))
    if not (args.panel and args.household):
        raise SystemExit("offer, show and restore need --panel and --household")
    if not args.key:
        raise SystemExit("no device key: pass --key or set LANTERNINA_DEVICE_KEY")
    if args.command == "offer":
        return asyncio.run(offer(args))
    if args.command == "restore":
        return restore(args)
    return show(args)


if __name__ == "__main__":
    sys.exit(main())
