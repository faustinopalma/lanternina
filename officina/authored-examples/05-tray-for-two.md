# 05 - A tray for two

## Household brief

The adolescent wants to prepare a tray for themselves and a willing familiar person. The adult supplies a stable tray large enough for two places, two unbreakable empty cups and two cloth napkins. All four items are placed visibly beside the tray. No food, drinks, heat, glass or carrying a loaded tray is involved. The adolescent can match one cup to one napkin with demonstration if needed. Use at most two guide sheets, and skip the second if the arrangement is already complete.

## Parent output

Title: Un vassoio per due

Overview: Si prepara un posto per sé e uno per un'altra persona. La stampante mostra gli oggetti da mettere sul vassoio e può indicare quello che manca. Alla fine ci sono due posti pronti. Servono un vassoio, due bicchieri infrangibili e due tovaglioli. Il genitore resta vicino; l'attività non include versare bevande o portare il vassoio.

Themes: ospitalità, oggetti, abbinamenti.

## Script output

Il vassoio serve a due persone realmente presenti o attese dal genitore. Si mettono due tovaglioli e un bicchiere vicino a ciascuno. La guida mostra questa corrispondenza senza chiedere di contare a mente. Nel percorso principale tornano due tovaglioli e un solo bicchiere. Il seguito riguarda soltanto il secondo posto. Se entrambi i posti sono già preparati, si conclude subito. Il modello non aggiunge posate o cibo per ottenere un altro scambio. Nessuno deve usare gli oggetti durante l'attesa della lettura.

## Cycle 1

### Display - cycle 1

```text
Prepara un posto per te e uno per chi è con te.
Il foglio mostra quali oggetti usare.
```

### Page - cycle 1

```json
{"kind":"notice","title":"Un vassoio per due","note":["Metti i due tovaglioli sul vassoio.","Metti un bicchiere vicino a ogni tovagliolo.","I bicchieri restano vuoti.","Fotografa il vassoio intero."],"spaces":[],"illustration":"One large top-down outline of a tray containing exactly two separate cloth napkins. Beside each napkin stands one empty cup, drawn clearly as a cup, with no overlap. Both pairs have equal spacing. No food, cutlery, liquid, numbered places, hands, decorative border or additional text."}
```

### Image prompt - cycle 1

```text
Create one complete portrait instruction sheet at 1024 by 1536 pixels, using strong black outlines on pure white and large readable text. Title: "Un vassoio per due". Print exactly these four lines: "Metti i due tovaglioli sul vassoio." "Metti un bicchiere vicino a ogni tovagliolo." "I bicchieri restano vuoti." "Fotografa il vassoio intero." Below, draw a large tray from slightly above so cups are recognisable. It contains exactly two cloth napkins, spaced apart, with exactly one empty cup beside each. Each cup and napkin forms a visually clear pair. No objects overlap or touch the rim. Do not add liquid, plates, cutlery, food, numbers, rewards, colour coding or any other words. This is an example of the requested arrangement, not an image claimed to be the person's result.
```

### Help - cycle 1

```text
Metti prima un tovagliolo.
Vicino a quel tovagliolo va un bicchiere.
```

### Hypothetical return - cycle 1

The full tray is visible with two separate napkins. A cup stands beside the left napkin; no cup is visible beside the right one or elsewhere on the tray. The reader does not report the location of the unused cup outside the frame.

## Cycle 2

### Display - cycle 2

```text
Il tovagliolo a destra è senza bicchiere.
Puoi aggiungere l'altro bicchiere.
```

### Page - cycle 2

```json
{"kind":"notice","title":"Il secondo posto","note":["Prendi l'altro bicchiere vuoto.","Mettilo vicino al tovagliolo senza bicchiere.","Fotografa di nuovo il vassoio."],"spaces":[],"illustration":"One large isolated cloth napkin with an empty cup immediately beside it. This is a reference for one pair, not a redraw of the whole tray. No left/right letters, arrows, additional cups, liquid, food or text."}
```

### Image prompt - cycle 2

```text
Draw a white portrait activity page, 1024 by 1536 pixels, with large plain black lettering. Print the title "Il secondo posto" and these three lines exactly: "Prendi l'altro bicchiere vuoto." "Mettilo vicino al tovagliolo senza bicchiere." "Fotografa di nuovo il vassoio." Draw one large cloth napkin and exactly one empty cup beside it, both entirely visible and clearly separate. This picture shows only the pair to make, not the whole photographed tray. No arrows, left/right lettering, extra objects, liquid or additional text. Use wide margins and clean outlines.
```

### Hypothetical return - cycle 2

Two cups are now visible, each beside a different napkin. The tray remains on the table. No person drinking or receiving it is visible.

## Closing output

```text
C'è un bicchiere vicino a ogni tovagliolo.
I due posti sono pronti.
```

## Alternative returns

- Two complete places appear in the first photograph: close immediately. Do not manufacture a missing cup or print the second guide.
- Two cups share one napkin: say "I bicchieri sono vicini allo stesso tovagliolo. Spostane uno vicino all'altro tovagliolo." This is moving an existing item, not adding a third.
- The tray is unchanged: offer to prepare one pair together or finish. Do not label the adolescent inattentive.
- A cup is hidden behind another: report uncertainty and request one clearer angle. Do not confuse occlusion with absence.
- The other cup is no longer available: accept a one-person setup or stop after asking the participant. Do not send them searching through cupboards.
- Stop or end time: "Lasciamo il vassoio sul tavolo. Puoi finire con chi è con te, se vuoi."

## Comparison checks

The agent must count visible objects and their pairing, not merely react to a nonblank photograph. A correct first return needs no repair exchange. No actual hospitality, thirst, social confidence or independence is inferred from the arrangement. The task uses a real purpose without turning the person into unpaid household labour or making participation compulsory.
