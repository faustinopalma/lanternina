# 14 - A scene with a visible change

## Household brief

The parent chooses extended creative writing with explicit requirements. Writing 80 to 120 words and revising dialogue are prerequisites for this activity, not inferred traits. Supply two blank sheets, a pencil and one printed brief. The participant can draft on separate paper and retain crossings-out. The story concerns two fictional characters and an ordinary key; nobody supplies family events or personal secrets. Completion means a scene that meets the length, character and event constraints. Its style, ending and interpretation remain open. If the participant requests feedback, the system identifies a specific textual issue rather than giving a general rating.

### Stable parent instructions

```text
Proponi anche scrittura estesa con vincoli chiari. Per questa attivita chiedi una scena di 80-120 parole e una revisione motivata. Lascia liberi tono, nomi e finale. Distingui i vincoli controllabili dalle preferenze stilistiche; non sostituire il testo con quello del modello.
```

### Feedback guidance

```text
Le consegne molto aperte non chiarivano da dove iniziare. Dai una situazione, un cambiamento da far accadere e criteri di conclusione. Il riscontro deve citare una scelta del testo e proporre una revisione circoscritta, senza prescrivere una morale.
```

This is an invented configuration example, not a default or a record of actual feedback.

## Parent output

Title: La chiave cambia mano

Overview: Due personaggi hanno intenzioni diverse e una sola chiave. Si scrive una scena di 80-120 parole in cui la chiave cambia mano. I motivi devono emergere da gesti e dialoghi. Il finale resta libero. Il riscontro, se richiesto, riguarda un passaggio preciso; il testo originale rimane disponibile.

Themes: dialogo, azioni, revisione.

## Script output

Il foglio presenta una situazione iniziale e quattro vincoli. Si puo scrivere su carta separata. Non si richiede una fotografia per dichiarare conclusa la bozza. Se viene restituita per un riscontro, prima si verifica che la trascrizione sia leggibile. Il conteggio usa parole separate da spazi e va confermato sulla trascrizione quando la lettura della foto e incerta. Il modello distingue un vincolo mancante da una scelta stilistica che potrebbe restare. Un cambio di mano soltanto annunciato, ma non avvenuto nella scena, richiede una revisione locale. Non si riscrive tutta la scena, non si impone una riconciliazione e non si deducono sentimenti o vicende personali dell'autore. La seconda stesura, se desiderata, usa lo stesso foglio o carta bianca.

## Cycle 1

### Display - cycle 1

```text
La consegna lascia liberi il tono e il finale.
Puoi scrivere la scena su un foglio bianco.
```

### Page - cycle 1

```json
{"kind":"notice","title":"La chiave cambia mano","note":["Scrivi 80-120 parole con due personaggi e una chiave.","Uno vuole partire; l'altro vuole trattenere la chiave.","Fai capire i motivi con gesti e dialoghi, senza spiegarli da fuori.","Nella scena la chiave deve cambiare mano. Il finale resta libero."],"spaces":[],"illustration":"One ordinary key on an otherwise empty tabletop, drawn in a small precise outline beneath the brief. No hands, faces, door, luggage, clock or other props that prescribe the characters, motives or ending. Leave the rest of the page clear. No words or numbers in the drawing."}
```

### Image prompt - cycle 1

```text
Create a complete portrait writing brief at 1024 by 1536 pixels on pure white. Print the title "La chiave cambia mano" in clear black type. Place these four lines below it with comfortable spacing: "Scrivi 80-120 parole con due personaggi e una chiave." "Uno vuole partire; l'altro vuole trattenere la chiave." "Fai capire i motivi con gesti e dialoghi, senza spiegarli da fuori." "Nella scena la chiave deve cambiare mano. Il finale resta libero." Beneath the instructions draw one ordinary key resting on a plain tabletop in a small precise outline. Keep it visibly an ordinary object, not a fantasy emblem. Do not add hands, faces, luggage, a clock or a door that would dictate a story. No answer boxes or sample story. Preserve ample white space. Print each specified string exactly once and no other text.
```

### Help - cycle 1

```text
Puoi cominciare da una battuta o da un gesto.
Prima di chiudere, controlla il momento in cui la chiave passa.
Il finale non deve risolvere ogni contrasto.
```

### Hypothetical return - cycle 1

The parent confirms this invented transcription. It contains 88 whitespace-delimited words. The text shows the two intentions and an actual transfer; it also explains both characters' inner states from outside the scene, contrary to the selected brief.

```text
Nora teneva la chiave stretta nel pugno. Elia posò lo zaino davanti alla porta. «Il treno parte tra poco.» Nora era preoccupata perché pensava che lui non sarebbe tornato. «Hai lasciato la finestra aperta», disse. Lui guardò il corridoio, poi tornò indietro e chiuse la finestra. Elia era impaziente, ma non voleva ferirla. «Adesso?» Nora aprì il pugno. La chiave passò nella mano di Elia. Prima di infilarla nella serratura, lui appoggiò sul tavolo il biglietto del ritorno. Nora lo girò verso la luce. Nessuno dei due sorrise.
```

### Continuation for this return

```text
La chiave passa di mano e il biglietto rende visibile il ritorno.
La frase su Nora preoccupata spiega invece il motivo da fuori.
Puoi sostituirla con un gesto o una battuta, lasciando intatto il finale.
Controlla anche la frase che descrive Elia impaziente.
```

This response identifies the two specific violations without treating the chosen ending as a defect. It suggests a local revision and does not provide a replacement paragraph to copy.

## Closing output

```text
La scena ha un inizio, un passaggio della chiave e un finale.
Conserva la bozza e l'eventuale revisione.
Il finale puo restare quello che hai scelto.
```

This closing names the structure of the hypothetical return. It does not claim that an unseen revision met all the constraints.

## Alternative returns

- A photograph shows a different valid story: check the published constraints and respond to that story, not to Nora and Elia.
- The transcript is uncertain: request confirmation before counting words or quoting a supposed mistake. Do not turn a reading error into writing feedback.
- The page is unchanged but a separate draft exists: ask for that draft only if feedback is wanted. The printed brief was not a compulsory answer surface.
- A longer or shorter text appears: state the observed count and the selected range. Offer a local cut or expansion without rewriting the scene.
- Both characters agree immediately: this can still work if their initial intentions and the transfer appear. The brief does not require a quarrel or a moral.
- Stop or end time: keep the unfinished draft. Do not require a new ending or a photograph to permit closure.

## Comparison checks

The system must preserve the parent's deliberately chosen writing demand instead of automatically reducing it to a mark or a two-option choice. The numerical range, two-character premise and key transfer can be checked; quality of dialogue and interpretation require a stated editorial judgement. A word count is meaningful only for a verified transcription. The hypothetical passage is authored here for testing, not returned work from a real participant. The final feedback should depend on the text and leave authorship with the participant. No page image has been rendered or physically evaluated.
