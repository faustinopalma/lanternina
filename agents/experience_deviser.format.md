<!--
The shape of the answer. What follows it in the assembled prompt is the format describing itself — the shape of a moment, the acts, and what a page is — which lives with the format in shared/experience_prompt.*.md because the continuer sends it too.

`themes` and `script` are what the parent approves alongside the overview: what it is about, and how it should go. The script is also what whatever runs the afternoon reads, so it is written for somebody doing it rather than for somebody deciding about it — the limits it names are the ones that matter once the paper is already on the table.
-->
Answer with JSON and nothing else, in this exact shape:
{"title": "<text>", "overview": "<text>", "themes": ["..."], "script": "<text>", "minutes": <whole number>, "drawn": { ... }, "moments": [ ... ]}
Do not write an id, a format version or a list of what the house needs: those are known already and are not yours to write.
  "overview": at most $max_overview characters. What this afternoon is, in the words a parent decides by. Not a summary of the moments — those can be read. Say what it is like to be inside it.
  "themes": at most $max_themes of them, each at most $max_theme characters. What it is about, a few words each, and the first thing the parent reads. Nouns, not sentences.
  "script": at most $MAX_SCRIPT characters, and use them. This is the game itself, written out for whoever runs the afternoon — not a summary, not a statement of intent, not a paragraph about what you hope it will feel like. Write it in these parts, in this order, each headed by its own name on its own line:
    THE WORLD. Where this is set and what is true in it that is not true here. Two or three specifics that do the work of twenty: what the light is like, what the place smells of, what nobody there ever mentions.
    THE QUESTION. What is not known and could be, in one sentence, with an answer you also write down. Then the false answer that will look right for a while, and what makes it come apart.
    THE BEATS. Six to twelve of them, each a line: what happens, and what it makes the person do. Say which beat turns the thing over, and which one is the one where the answer arrives.
    WHAT IS HELD BACK. Three or four things, and the beat at which each is given. Nothing may be held past the last beat.
    WHAT IS MADE. Every object that comes off the printer, one line each: what it is inside the story, what it says, what it asks for, and what a person is meant to do to it. Whoever runs the afternoon draws these from what you write here, so name the thing, not the format — a shipping manifest and not a table, a letter and not a form.
    WHERE IT CAN GO DIFFERENTLY. What happens if the paper comes back full, if it comes back untouched, and if somebody stops caring halfway. Concrete moves, not principles.
    WHAT WOULD SPOIL IT. Two or three, and they should be things you are actually tempted to do.
    Nothing in this is a step to perform in order. It is the material the afternoon is made of, and whoever runs it decides which of it happens.
