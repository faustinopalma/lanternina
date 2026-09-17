<!--
The shape of the answer. What follows it in the assembled prompt is the format describing itself — the shape of a moment, the acts, and what a page is — which lives with the format in shared/experience_prompt.*.md because the continuer sends it too.

`themes` and `script` are what the parent approves alongside the overview: what it is about, and how it should go. The script is also what whatever runs the activity reads, so it is written for somebody doing it rather than for somebody deciding about it — the limits it names are the ones that matter once the paper is already on the table.

The overview asked for the wrong thing until 3 September 2026, and it asked for it in one sentence: *say what it is like to be inside it*. It got exactly that. Measured on the fifteen overviews generated that day: eight of them open with the same two words — «Un pomeriggio quieto» or «Un'indagine quieta» — every one describes an atmosphere, none says what the person will do, what the house has to supply, or what is left at the end. A parent handed three of those reads the same fog three times. `panel/experiences.py::to_public` shows the overview, the themes and the script to the parent, and `ideas/08 §2` says approval is given to them, so this is the one string the whole gate rests on.
-->
Plan one activity using the three configurable prompts. Answer with JSON and nothing else:
{"title": "<text>", "overview": "<text>", "themes": ["..."], "script": "<text>", "minutes": <whole number>, "drawn": { ... }, "moments": [ ... ]}
Do not write an id, a format version or a list of what the house needs: those are known already and are not yours to write.
overview: at most $max_overview characters, describing the task, preparation, prerequisites and assistance for parental approval.
themes: at most $max_themes strings of at most $max_theme characters.
script: at most $MAX_SCRIPT characters. Record the goal, material, reasoning or result criteria, execution and alternatives needed to run the approved activity. State the whole-activity sheet budget. The executable moments must contain everything the participant needs; the script is not delivered to the participant or page maker.
