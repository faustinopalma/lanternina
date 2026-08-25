<!--
The shape of the answer. What follows it in the assembled prompt is the format describing itself — the shape of a moment, the acts, and what a page is — which lives with the format in shared/experience_prompt.*.md because the continuer sends it too.

`themes` and `strategy` are what the parent approves alongside the overview: what it is about, and how it should go. The strategy is also what whatever runs the afternoon reads, so it is written for somebody doing it rather than for somebody deciding about it — the limits it names are the ones that matter once the paper is already on the table.
-->
Answer with JSON and nothing else, in this exact shape:
{"title": "<text>", "overview": "<text>", "themes": ["..."], "strategy": "<text>", "minutes": <whole number>, "drawn": { ... }, "moments": [ ... ]}
Do not write an id, a format version or a list of what the house needs: those are known already and are not yours to write.
  "overview": at most $max_overview characters. What this afternoon is, in the words a parent decides by. Not a summary of the moments — those can be read. Say what it is like to be inside it.
  "themes": at most $max_themes of them, each at most $max_theme characters. What it is about, a few words each, and the first thing the parent reads. Nouns, not sentences.
  "strategy": at most $max_strategy characters, written for whoever runs the afternoon rather than for whoever approves it. Say what is not known and could be — the real question the afternoon turns on — and what is held back, and when it is given. Then where it can afford to wander, what to lean on if interest drops, and the two or three things that would spoil it. Concrete: name the object that should be in their hands at the end. Not a list of steps — the moments are the steps.
