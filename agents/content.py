"""The content agent: proposes activities and the words an adolescent will read.

What this agent can do is bounded by its inputs, not by its manners. It receives an
:class:`~shared.agents.AgentContext` holding a model router, redacted prompt hints and a
clock — no ledger, no sealer, no network client. Every method returns a
:class:`~shared.proposal.Proposal`, which has nowhere to record its own approval.

It never sees unscreened text: ``router.generate_for_user`` screens and seals before
returning, so the payload this agent wraps has already passed the gate.

The prompts describe what to make, not who it is for. The system may work out what to ask
for from what came back before — that decision is the planner's — but what reaches the
model is a description of the material, never a claim about a person.
"""

from __future__ import annotations

import json
from typing import Any

from shared.domain import ActivityKind, Difficulty
from shared.errors import UnusableGeneration
from shared.exercise import EXERCISES, INSTRUCTIONS, RATIONALE, TITLE
from shared.ids import new_proposal_id, new_request_id
from shared.proposal import Proposal, ProposalKind
from shared.routing import Capability, ModelRequest
from shared.safety import ContentKind, ScreenedPayload

# Content settings, glossed for the model. These describe the shape of the material asked
# for — never an estimate of what somebody can do.
_DIFFICULTY_GLOSS = {
    Difficulty.GENTLE: "passi molto brevi, una sola idea per volta, frasi semplici",
    Difficulty.STEADY: "due o tre passaggi collegati, frasi brevi",
    Difficulty.STRETCH: "qualche passaggio in piu, purche ogni passo resti chiaro da solo",
}

_KIND_GLOSS = {
    ActivityKind.PRINTED_EXERCISE: "un foglio da stampare, da fare con una matita",
    ActivityKind.INTERACTIVE_GAME: "una attivita breve da fare con due pulsanti",
    ActivityKind.ROUTINE_PROMPT: "un promemoria per un momento della giornata",
}

_EXERCISE_SHAPE = (
    '{"title": "...", "instructions": "...", '
    '"exercises": [{"question": "...", "choices": ["...", "..."], "answer": "..."}], '
    '"rationale": "..."}'
)


class HouseholdContentAgent:
    """First working version. Text only: layout and pictograms are other agents' work."""

    name = "content"

    async def propose_exercise(
        self,
        ctx: Any,
        *,
        kind: ActivityKind,
        difficulty: Difficulty,
        topic_hint: str = "",
    ) -> Proposal:
        prompt = self._exercise_prompt(ctx.learner_hints, kind, difficulty, topic_hint)
        payload = await ctx.router.generate_for_user(
            ModelRequest(
                capability=Capability.STRUCTURED_GENERATION,
                prompt=prompt,
                request_id=new_request_id(),
                max_output_chars=1600,
                purpose=f"exercise/{kind}/{difficulty}",
                content_kind=ContentKind.EXERCISE_JSON,
            )
        )
        body = self._parsed(payload)
        for field_name in (TITLE, INSTRUCTIONS, EXERCISES):
            if not body.get(field_name):
                raise UnusableGeneration(f"generated exercise has no {field_name}")

        return Proposal(
            id=new_proposal_id(),
            kind=ProposalKind.EXERCISE,
            agent=self.name,
            learner_id=ctx.learner_id,
            payload=payload,
            rationale=str(body.get(RATIONALE) or f"attivita {kind} richiesta dal genitore"),
            created_at=ctx.now,
        )

    async def propose_routine_prompt(
        self, ctx: Any, *, step_label: str, at: str = ""
    ) -> Proposal:
        """Propose the words for one routine step, for an e-paper display."""
        hints = ctx.learner_hints
        when = f" verso le {at}" if at else ""
        prompt = (
            f"Scrivi il testo di un promemoria gentile per questo momento: {step_label}{when}.\n"
            f"Lingua: {hints.get('language', 'it')}. "
            f"Una sola frase, al massimo {hints.get('max_words_per_line', 6) * 2} parole, "
            "senza punto esclamativo e senza fretta.\n"
            "La frase e quella che si legge sul display: non ripetere l'etichetta del "
            "passo e non iniziare con parole come 'Promemoria' o 'Ricorda'.\n"
            f"{self._boundaries(hints)}\n"
            "Rispondi con la sola frase, senza virgolette."
        )
        payload = await ctx.router.generate_for_user(
            ModelRequest(
                capability=Capability.TEXT_GENERATION,
                prompt=prompt,
                request_id=new_request_id(),
                max_output_chars=200,
                purpose=f"routine/{step_label}",
                content_kind=ContentKind.ROUTINE_PROMPT,
            )
        )
        return Proposal(
            id=new_proposal_id(),
            kind=ProposalKind.ROUTINE_PROMPT,
            agent=self.name,
            learner_id=ctx.learner_id,
            payload=payload,
            rationale=f"promemoria per il passo di routine '{step_label}'",
            created_at=ctx.now,
        )

    # -- prompt construction ------------------------------------------------------------

    def _exercise_prompt(
        self,
        hints: dict[str, Any],
        kind: ActivityKind,
        difficulty: Difficulty,
        topic_hint: str,
    ) -> str:
        interests = ", ".join(hints.get("interests") or []) or "nessun tema indicato"
        topic = topic_hint or interests
        choices = (
            "Ogni esercizio ha da 2 a 4 scelte, perche il foglio viene letto da una "
            "telecamera e solo le caselle da barrare si leggono senza rete."
            if kind is ActivityKind.PRINTED_EXERCISE
            else "Ogni esercizio ha esattamente 2 scelte, una per pulsante."
        )
        return (
            f"Prepara {_KIND_GLOSS[kind]} su questo tema: {topic}.\n"
            f"Lingua: {hints.get('language', 'it')}. "
            f"Forma richiesta: {_DIFFICULTY_GLOSS[difficulty]}.\n"
            f"Da 3 a 5 esercizi. {choices}\n"
            "Le scelte sono parole o brevi gruppi di parole: senza simboli, senza caselle, "
            "senza lettere o numeri iniziali. Le caselle le disegna il foglio.\n"
            f"Le righe di testo non superano {hints.get('max_words_per_line', 6)} parole.\n"
            f"{self._boundaries(hints)}\n"
            f"In '{RATIONALE}' spiega al genitore in una frase perche proponi questo.\n"
            f"Rispondi con solo JSON, senza ``` e senza altro testo, in questa forma: "
            f"{_EXERCISE_SHAPE}"
        )

    @staticmethod
    def _boundaries(hints: dict[str, Any]) -> str:
        avoid = ", ".join(hints.get("avoid") or [])
        line = f"Da evitare in modo assoluto: {avoid}." if avoid else ""
        variety = hints.get("content_variety", "balanced")
        familiar = {
            "familiar": "Resta su una forma gia vista: la stessa struttura di sempre.",
            "balanced": "Una forma riconoscibile, con un dettaglio nuovo.",
            "frequent": "Cambia forma rispetto al solito: proponi qualcosa di diverso.",
        }
        return f"{line} {familiar.get(str(variety), '')}".strip()

    @staticmethod
    def _parsed(payload: ScreenedPayload) -> dict[str, Any]:
        """Validate the sealed body without touching it — editing would break the seal."""
        try:
            parsed = json.loads(payload.body)
        except json.JSONDecodeError as exc:
            raise UnusableGeneration(f"generated exercise is not JSON: {exc}") from exc
        if not isinstance(parsed, dict):
            raise UnusableGeneration("generated exercise is not a JSON object")
        return parsed
