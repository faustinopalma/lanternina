# 07 - A sign for the door

## Household brief

The adolescent wants a sign for their own room. Before approval, the family agrees on two meanings: knock before entering, or come in. Both remain requests subject to ordinary safety needs, not locks or guarantees of isolation. The adult will actually respect the chosen request in ordinary circumstances. Supply removable tape suitable for the door. The person recognises a knock and an open doorway when demonstrated, but need not read either word alone. The adult reads both choices without indicating a preferred answer. Two sheets, one photographed choice and no required photo of the finished door.

## Parent output

Title: Il cartello per la mia porta

Overview: Si sceglie se chiedere di bussare o invitare a entrare. La stampante prepara le due scelte e poi il cartello scelto. Resta un messaggio da mettere sulla porta con il genitore. Serve nastro rimovibile. La famiglia concorda prima come rispondere al cartello; stamparlo non basta a renderlo utile.

Themes: spazio personale, comunicazione, scelta.

## Script output

Il ragazzo sceglie fra due richieste che la famiglia ha già accettato di usare. Il genitore può far sentire un colpo alla porta e mostrare un ingresso aperto mentre legge le parole. Nel percorso principale viene cerchiata la mano che bussa. Si stampa il cartello con la parola Bussa. La stampa finale non chiede un'altra scelta o una prova di lettura. Dopo la consegna il genitore aiuta a fissarla. Si conclude dicendo che il cartello è pronto, senza affermare che sia già sulla porta o che tutti lo abbiano rispettato.

## Cycle 1

### Display - cycle 1

```text
Che cosa vuoi dire a chi arriva?
Scegli uno dei due disegni sul foglio.
```

### Page - cycle 1

```json
{"kind":"notebook","title":"Un messaggio sulla porta","note":["Scegli un messaggio con chi è con te.","Cerchia il disegno che vuoi usare.","Puoi cambiare idea.","Fotografa il foglio con la scelta."],"spaces":[{"label":"Bussa","room":"a_box"},{"label":"Entra","room":"a_box"}],"illustration":"Place a clear reference icon immediately beside each corresponding labelled empty choice area: a hand knocking on a closed door beside Bussa; an open door with a clear empty doorway beside Entra. Draw no person entering, padlock or warning sign. Keep both options equally prominent; leave the response areas unmarked."}
```

### Image prompt - cycle 1

```text
Create one white portrait choice page at 1024 by 1536 pixels with large plain black text. Title: "Un messaggio sulla porta". Print these four lines exactly: "Scegli un messaggio con chi è con te." "Cerchia il disegno che vuoi usare." "Puoi cambiare idea." "Fotografa il foglio con la scelta." Below, make two equally large vertically separated choice areas. Label the first "Bussa" and place a clear line drawing of a hand knocking on a closed door immediately beside its empty response area. Label the second "Entra" and place a clear line drawing of an open door and empty doorway beside its empty response area. Leave room to circle each drawing broadly. No locks, stop symbols, preferred choice marks, people or extra words. Keep the symbols distinct without relying on colour.
```

### Help - cycle 1

```text
Questo disegno chiede di bussare.
L'altro invita a entrare.
```

The adult points to the matching drawings while reading. The software must not assume the listener knows which option an unaccompanied deictic word identifies.

### Hypothetical return - cycle 1

The knocking-hand drawing and its label are surrounded by one broad oval. The open-door drawing has no added mark. No reason for the choice is inferred.

## Cycle 2

### Display - cycle 2

```text
È pronto il cartello che chiede di bussare.
Puoi metterlo sulla porta con il genitore.
```

### Page - cycle 2

```json
{"kind":"notice","title":"Bussa","note":[],"spaces":[],"illustration":"One large clear black outline icon of a hand knocking on a closed door, centred under the single title. Mature neutral signage, generous white space. No lock, warning symbol, face, decorative frame, instructions or other text."}
```

### Image prompt - cycle 2

```text
Draw a finished portrait door sign at 1024 by 1536 pixels on pure white. The only word is "Bussa", in very large plain black type at the top. Below, draw one large unambiguous outline icon of a hand knocking on a closed door. Use simple mature signage with bold clean strokes and broad white margins. No padlock, warning triangle, smiling face, decorative frame, instructions, extra letters or text. This is the sign to use, not a worksheet to complete. Do not require cutting for the message to remain readable.
```

### Delivered result - cycle 2

This cycle asks for no return. Only after successful page delivery may the display announce that the sign is ready. A print failure cannot be counted as a delivered sign.

## Closing output

```text
Il cartello è pronto.
Puoi cambiare messaggio quando vuoi.
```

## Alternative returns

- The open-door choice is marked: print a sign titled "Entra" with the open-door icon. No knocking-hand sign is delivered.
- Both choices are marked: ask once which message to use now. If the person wants both, a parent can keep the choice sheet as two options; do not claim that both opposite messages apply simultaneously.
- The choice sheet is unchanged: offer a spoken or pointed choice recorded by the parent, or finish without printing a final sign.
- The photograph is unclear: keep the choice unknown. Do not infer a desire for privacy from a diagnosis or previous refusal.
- A change of mind arrives before printing: use the latest recorded choice. After printing, offer changing the sign within a newly agreed paper budget rather than ignoring the change.
- Stop or end time: "Non serve scegliere adesso. Teniamo il foglio con i due messaggi."

## Comparison checks

The preference changes the final object. The final sign contains no instructional clutter. Meaning is established socially before the activity, not invented by the model. The system distinguishes generated, printed, attached and respected: none implies the next. No second photographed return is added simply to match a workflow template.
