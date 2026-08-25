<!--
The shape of the answer. What follows it in the assembled prompt is the format describing
itself — the shape of a moment, the acts, and what a page is — which lives with the format
in shared/experience_prompt.*.md because the continuer sends it too.
-->
Answer with JSON and nothing else, in this exact shape:
{"title": "<text>", "overview": "<text>", "minutes": <whole number>, "drawn": { ... }, "moments": [ ... ]}
Do not write an id, a format version or a list of what the house needs: those are known already and are not yours to write.
