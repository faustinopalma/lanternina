# 03 - The notebook cover

## Household brief

The adolescent wants a cover for an existing notebook and can choose between two bold patterns or add broad strokes. The adult supplies the notebook, a thick pencil or marker, and removable tape. The notebook must be small enough for an A4 sheet to cover its front; the adult handles fitting and attachment. Copying an exact pattern, handwriting and naming a favourite colour are unnecessary. Use two printed sheets. A partly decorated cover is usable.

## Parent output

Title: La copertina del mio quaderno

Overview: Si sceglie un motivo e si completa una copertina da mettere sul proprio quaderno. La stampante prepara il foglio di scelta e la copertina scelta. Servono un quaderno e nastro rimovibile, oltre alla matita. Il genitore aiuta a fissare il foglio. Non c'è un disegno da riprodurre perfettamente.

Themes: quaderni, motivi grafici, disegno.

## Script output

Il foglio iniziale mostra due motivi grandi: righe e onde. Il ragazzo sceglie segnando un motivo; se indica con il dito, il genitore registra soltanto la scelta indicata. Nel percorso principale torna un cerchio intorno alle onde. Il seguito stampa una copertina con due onde iniziate e molto spazio libero. Si possono prolungare, aggiungerne altre o cambiare il motivo. Il risultato diventa la copertina: non viene sostituito da una versione più ordinata disegnata dal modello. Si conclude quando il ragazzo decide di tenerlo, anche se ha fatto pochi segni.

## Cycle 1

### Display - cycle 1

```text
Scegli un motivo per il tuo quaderno.
Cerchia quello che vuoi usare.
```

### Page - cycle 1

```json
{"kind":"notebook","title":"Una copertina da scegliere","note":["Guarda le righe e le onde.","Cerchia il motivo che vuoi usare.","Puoi anche indicarlo a chi è con te.","Fotografa il foglio quando la scelta è segnata."],"spaces":[],"illustration":"Two equally sized large pattern samples side by side. Left: three straight parallel diagonal black strokes. Right: three smooth parallel wavy black strokes. Neither sample is selected, more decorated or framed as better. No letters, pattern names, notebook title, icons or additional text."}
```

### Image prompt - cycle 1

```text
Draw a complete portrait choice page at 1024 by 1536 pixels, with a pure white background and bold black marks. Use large plain sans-serif text. Print exactly the title "Una copertina da scegliere" and four lines: "Guarda le righe e le onde." "Cerchia il motivo che vuoi usare." "Puoi anche indicarlo a chi è con te." "Fotografa il foglio quando la scelta è segnata." Below, show two equally large unselected samples with ample space to circle either: three straight parallel diagonal strokes on the left and three smooth parallel wavy strokes on the right. Neither sample has a border, rating, tick or decorative advantage. No letters or captions under the samples. Leave the rest white and add no other words.
```

### Help - cycle 1

```text
Puoi passare il dito sopra un motivo.
Poi indica quello che vuoi sul quaderno.
```

### Hypothetical return - cycle 1

A broad closed mark surrounds the wavy sample only. The straight strokes have no added mark. This establishes a recorded selection, not a stable preference for curved shapes.

## Cycle 2

### Display - cycle 2

```text
Hai scelto le onde.
Sul nuovo foglio puoi aggiungerne altre.
```

### Page - cycle 2

```json
{"kind":"notebook","title":"Il mio quaderno","note":["Continua le onde oppure aggiungi i segni che vuoi.","Puoi lasciare spazi bianchi.","Quando vuoi tenerla così, fotografa la copertina."],"spaces":[],"illustration":"An almost empty notebook front cover. Two bold smooth wave strokes begin near the lower left and stop well before the page centre, leaving most of the page available for the participant. No completed pattern, decorative frame, name line or extra words. Keep title and notes in the upper part, away from the drawing area."}
```

### Image prompt - cycle 2

```text
Create a portrait notebook cover on pure white paper, 1024 by 1536 pixels. The title is "Il mio quaderno". Print these three easily readable instruction lines in a compact upper area: "Continua le onde oppure aggiungi i segni che vuoi." "Puoi lasciare spazi bianchi." "Quando vuoi tenerla così, fotografa la copertina." Use a large plain title and black text. Below, leave most of the page empty. Start exactly two bold smooth wave strokes near the lower left, ending before the centre so the participant can extend or change them. Do not finish the pattern, fill the margins, add a name field, impose symmetry or print any other words. This is paper for the participant's own design, not a completed decorative illustration.
```

### Hypothetical return - cycle 2

Three new long wavy strokes and one angular zigzag are visible. Large blank areas remain. No name has been added. The reader describes both kinds of mark without labelling the zigzag an error.

## Closing output

```text
La copertina ha onde e un segno a zigzag.
Ora puoi fissarla sul quaderno con il genitore.
```

## Alternative returns

- The straight sample is selected: the second page starts straight diagonal strokes, and the display says "Hai scelto le righe." Printing waves anyway fails the reference.
- Both samples are circled: offer "Vuoi usare righe e onde insieme?" On confirmation, supply both. Do not insist on a single preference.
- The cover is unchanged but the participant says to keep it: accept it. No extra mark is required to finish.
- The photograph cannot distinguish a circle from a shadow: ask once which sample was chosen. Do not use earlier activities to guess.
- Unrelated marks appear: preserve them and ask whether this is the cover to keep. Do not redraw them into tidy waves.
- Stop or end time: "Il foglio resta tuo, anche così. Puoi usarlo come copertina quando vuoi."

## Comparison checks

The chosen pattern changes the actual image prompt. An unexpected decorative choice remains valid. The system never replaces the participant's marks with its own rendition. The adult's fitting task is declared in advance; an A4 page does not fit every notebook automatically.
