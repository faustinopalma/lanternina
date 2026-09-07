# Lanternina — working rules

Lanternina is a home system that offers activities to an adolescent, with a parent steering. It is for adolescents, without asking which ones: interest, appetite for novelty and comfort with text on a page vary across the whole range of cognitive ability, and none of that is recorded here as a property of anybody.

**The design rules are being rewritten from scratch.** The ones that used to live in this file were written before anybody had run an afternoon, and several of them turned out to forbid things nobody meant to forbid. They have been taken out rather than patched. What replaces them will come from the research in `enciclopedia/` — 395 entries compiling every way a thing to do can be put to somebody, deliberately without applying any rule while it compiled, because filtering while listing means listing only what had already been thought of.

Until that research has been reviewed, **nothing here constrains what may be proposed or built.** Propose the thing that makes the afternoon better, say why, and write the reasoning in `ideas/`. `docs/EVIDENCE.md` is where the reading behind a decision goes when there is one.

What follows is craft, not design: how to work in this repository, and how to write in it.

---

## 1. How to work in this repo

- Python 3.11+, `from __future__ import annotations`, dataclasses for contracts. Line length 100. Type hints where they earn their place.
- Comments explain *why*, in one line. Do not narrate the next line.
- Stubs must be honest: raise `NotImplementedError` or return obviously fake data. Never write a stub that looks like it works.
- **Read before you write.** `shared/` is written and load-bearing; check a package with `file_search` before adding to it.
- Verify empirically rather than from memory: probe the API, print the numbers, and prefer a test that fails on the broken version over one that merely passes on the fixed one.
- Prompt blocks live as `<module>.<block>.md` beside the `.py`. After changing one, re-render the snapshots with `python -m tools.prompts --write`.

## 2. How we write

Applies to everything that stays in the repository, in Italian and in English alike. The reference for the tone is the author's thesis, <https://laquantistica.com>: plain, unhurried, specific, never raising its voice.

- **Declarative and calm.** State what a thing does. No bold as emphasis-by-shouting.
- **Subject, verb, object, in that order.** Do not front a number or a fragment and explain it afterwards: "The container makes six calls" and not "Six, and every one of them is the call the container makes". Do not invert for emphasis: "There is a cell wherever the product loops on its own" and not "Where the product loops on its own, there is a cell". The inverted forms read as literary and cost the reader a second pass.
- **A verb, not an apposition.** "The diagram names roles and not deployments" and not "A role and not a deployment: which model answers each one is the router's business". If a sentence has a colon in the middle and no verb before it, it is this defect.
- **An aphorism may follow a plain statement and may not replace one.** Say the fact first, in the plainest words available, and only then say the thing that generalises it. A sentence that is only memorable leaves the reader guessing at what happened.
- **Direct concepts over metaphors.** An analogy is allowed only when it does explanatory work, and is made literal in the next sentence.
- **No superlatives and no marketing adjectives** — not "powerful", "seamless", "robust". When something is hard or unresolved, say so plainly.
- **Numbers with units, and their provenance** — measured, computed or estimated. That is the part a reader cannot reconstruct on their own.
- **Limits next to the claim,** in the same paragraph, not in a footnote.
- **A choice is explained by its tradeoff,** in one sentence: what it buys and what it costs.
- **No comparison that flatters us.** Describe what was done and why; do not rank this work against other people's work or a hypothetical worse author.
- **Short sentences.** A subordinate clause has to carry a reason, otherwise cut it.
- **No hard-wrapped prose.** In Markdown, a paragraph is one line; the editor wraps it. Hard wrapping does not help diffs — change one word and the whole paragraph reflows. The exceptions are Python, where ruff enforces a line length of 100, and the prompt files, where every newline reaches a model.
- **A string in the panel earns its place only if it changes what the parent does next.** Why the software works the way it does goes in a comment or a conversation, never in the interface.
- Credits, acknowledgements and open questions stay factual and brief.
