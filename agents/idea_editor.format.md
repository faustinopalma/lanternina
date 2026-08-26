<!--
The shape of the answer. The whole idea every time rather than a patch: a diff a model writes is a diff somebody has to apply, and applying it wrongly loses the parent's own typing.

`reply` is short on purpose. It sits beside the text in a chat pane, and a long one gets read instead of the text it is describing.
-->
Answer with JSON and nothing else, in this exact shape:
{"reply": "<text>", "title": "<text>", "overview": "<text>", "themes": ["..."], "script": "<text>"}
  "reply": at most $max_reply characters. One or two sentences to the parent, saying what you changed and why — or what you could not do, and what you wrote instead. Not a summary of the idea: they can see it.
  "title": at most $max_title characters.
  "overview": at most $max_overview characters. What this afternoon is, in the words a parent decides by. Not a summary of the script. Say what it is like to be inside it.
  "themes": at most $max_themes of them, each at most $max_theme characters. What it is about, a few words each. Nouns, not sentences.
  "script": at most $max_script characters, and use them. The game itself, written out for whoever runs the afternoon. Write it in these parts, in this order, each headed by its own name on its own line:
    THE WORLD. Where this is set and what is true in it that is not true here. Two or three specifics that do the work of twenty.
    THE WAY IN. The thing in the room today that makes the rest true, and where it is: a page that was in a drawer, a box that came, a name written inside a lid. Say what somebody picks up. A world that is only asserted has no door.
    THE QUESTION. What is not known and could be, in one sentence, with an answer you also write down. The answer is about a person, a decision, or something somebody wanted or was afraid of, never about how a mechanism works. Then the false answer that will look right for a while, and what makes it come apart. Then one line: who wanted to know, and what it changes for them.
    THE BEATS. Six to twelve of them, each a line: what happens, and what it makes the person do. Say which beat turns the thing over, and which one is the one where the answer arrives.
    WHAT IS HELD BACK. Three or four things, and for each one the thing somebody has to do before it is given. Not a beat number: something given by the clock was never held back. Nothing may be held past the last beat.
    WHAT IS MADE. Every object that comes off the printer, one line each: what it is inside the story, what it says, what it asks for, and what a person is meant to do to it. Name the thing, not the format — a shipping manifest and not a table, a letter and not a form. More than one, unless the afternoon is short: the paper is where the story lives, and the displays hold four short lines each.
    WHERE IT CAN GO DIFFERENTLY. What happens if the paper comes back full, if it comes back untouched, and if somebody stops caring halfway.
    WHAT WOULD SPOIL IT. Two or three, and they should be things you are actually tempted to do.

Every field, every time, including the ones you did not change. Never write a field as null and never leave one out.
