<!--
The lookup step, added 3 September 2026 at the parent's request: the agent should have knowledge it can draw on rather than knowledge poured into its prompt.

The arithmetic is what settles the shape. A record is about 2 300 characters and there are 180 of them, so the corpus in full is roughly 460 kB against a devise prompt of 27 kB. A name is about 47. So the catalogue of names is 2% of the corpus and buys the one thing the model cannot supply for itself — that there are a hundred and eighty of these and not the ten anybody reaches for — and the records it asks for arrive in full in the call after this one.

Why the model chooses rather than the code: `ideas/11 §3` ruled out similarity search, and it was right that a query about subjects cannot search a corpus of forms. This is neither. The model is holding the household and the catalogue at once and is the only thing in the system that can judge which form suits which afternoon. What the code keeps is the filter — a house is never offered a form it cannot run — and the fallback, because an afternoon may not be lost over the way its form was chosen.

`why` is not used by anything. It is in the answer because a choice with a reason attached is a choice that can be read in a log afterwards, and because asking for it costs one line and makes the choosing less careless.
-->
You are about to devise one afternoon for one adolescent to spend at home. First you are choosing what to build it out of.

Below is a catalogue of methods that work on paper, filtered to the ones this house can actually run. Each line is an id and a name. Some are marked as a move: a move is not something to do on its own — it is applied to a form and changes what the form asks of somebody.

The parent wrote down these interests, as a place to begin: $interests
And these things to keep away from: $avoid
Afternoons already offered here: $already
How the afternoon should be pitched: $pitch

Choose one form and one move. Choose what would make the best afternoon for this house — not what is easiest to write, and not the first one that looks familiar. If the interests point at something, let them; if nothing fits them, choose the form that would make the strangest good afternoon rather than the safest one.

Answer with JSON and nothing else, in this exact shape, using ids exactly as they appear in the catalogue:
{"form": "<id>", "move": "<id>", "why": "<one short sentence>"}

$catalogue
