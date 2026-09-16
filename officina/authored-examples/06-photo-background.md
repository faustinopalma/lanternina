# 06 - A background for a photograph

## Household brief

The adolescent wants a photograph of a familiar object they choose. For this reference, they select a large plain dark mug with no writing. The adult supplies the mug, a white A4 sheet and a clean patterned cloth that is not needed for another purpose. The mug is unbreakable and empty. Only the mug and prepared surface are photographed. The adult can hold the camera at a useful angle and later show the two original photographs together in the authenticated family panel, identifying which was first. This brief explicitly requires that comparison surface; without it, use a different activity or print faithful copies outside the image generator. There are three printed guides and three returns, the last being a recorded choice.

## Parent output

Title: La foto della mia tazza

Overview: Si fotografa una tazza su due sfondi e si sceglie la foto da tenere per questa attività. La stampante prepara due guide brevi e un foglio di scelta. Servono la tazza, un foglio bianco e un telo a fantasia. Il genitore mostra le due foto originali una accanto all'altra. La scelta riguarda ciò che piace al ragazzo, non una fotografia migliore secondo il modello.

Themes: fotografia, oggetti, sfondi.

## Script output

Il primo scatto usa un foglio bianco come superficie. Il secondo usa il telo a fantasia, lasciando la tazza uguale. Le guide non impongono misure, inquadrature perfette o una risposta sui colori. Il genitore mostra le due foto originali insieme e indica quale è la prima e quale la seconda. Il ragazzo sceglie e la scelta viene segnata sul foglio. Nel percorso principale sceglie la seconda foto. Si conclude conservando quella scelta nel risultato dell'attività. Il sistema non cancella l'altra foto senza una richiesta e non rigenera l'immagine scelta.

## Cycle 1

### Display - cycle 1

```text
Metti la tazza sul foglio bianco.
Fai una foto della tazza intera.
```

### Page - cycle 1

```json
{"kind":"notice","title":"La tazza sul bianco","note":["Metti la tazza sul foglio bianco.","Fotografa tutta la tazza.","Lascia la tazza sul tavolo: faremo un'altra foto."],"spaces":[],"illustration":"One large plain mug with handle on a white rectangular sheet, shown obliquely so the mug and the sheet boundary are distinct. The mug is empty and unmarked. No camera settings, arrows, measurements, background objects or additional text."}
```

### Image prompt - cycle 1

```text
Draw one complete portrait page at 1024 by 1536 pixels. Use pure white paper, large plain black lettering and clear black line drawings. Print exactly the title "La tazza sul bianco" and these three lines: "Metti la tazza sul foglio bianco." "Fotografa tutta la tazza." "Lascia la tazza sul tavolo: faremo un'altra foto." Below, draw one large plain empty mug with a handle resting on a rectangular sheet. Use a slightly oblique view to separate the mug from the paper edge. This is a generic material illustration, not a replica of the participant's actual mug. No writing on the mug, camera controls, measurements, arrows or extra words. Keep the entire drawing inside generous margins.
```

### Help - cycle 1

```text
Puoi chiedere aiuto per tenere la fotocamera.
Nella foto deve entrare anche il manico.
```

### Hypothetical return - cycle 1

The full mug and handle are visible on a plain pale sheet. The object is not cropped. The observation records this as the first photograph. It makes no claim about aesthetic quality or independent camera use.

## Cycle 2

### Display - cycle 2

```text
Nella prima foto la tazza è sul foglio bianco.
Ora prova il telo a fantasia.
```

### Page - cycle 2

```json
{"kind":"notice","title":"La stessa tazza sul telo","note":["Togli il foglio e stendi il telo.","Metti la stessa tazza sul telo.","Fotografa di nuovo tutta la tazza."],"spaces":[],"illustration":"The same generic plain mug resting on a flat piece of cloth with a sparse checked pattern. The mug and its handle remain easy to distinguish from the cloth. No decorative objects or labels. Do not imply an exact reproduction of a real photograph or that this background is preferred."}
```

### Image prompt - cycle 2

```text
Make one complete portrait page, 1024 by 1536 pixels, black on white with large plain text. Title: "La stessa tazza sul telo". Print exactly "Togli il foglio e stendi il telo." "Metti la stessa tazza sul telo." "Fotografa di nuovo tutta la tazza." Draw one plain empty mug with a handle on a flat cloth with widely spaced checked lines. The outline of the mug must remain clear against the cloth. Show the entire material without camera settings or a finished photographic frame. The picture identifies a changed surface; it does not claim to reproduce either real photo. No ranking, extra words or colour-dependent information.
```

### Hypothetical return - cycle 2

The mug and handle are fully visible on patterned fabric. The system has retained the first photograph and can compare the backgrounds. Small changes in mug angle are not treated as a failed experimental control.

## Cycle 3

### Display - cycle 3

```text
Guarda le due foto con chi è con te.
Scegli quella che vuoi tenere per questa attività.
```

### Page - cycle 3

```json
{"kind":"notebook","title":"Quale foto vuoi tenere?","note":["Guarda le due foto originali con il genitore.","Indica quella che vuoi tenere per questa attività.","Segna la scelta qui sotto.","Fotografa il foglio con la scelta."],"spaces":[{"label":"Prima foto: foglio bianco","room":"a_line"},{"label":"Seconda foto: telo a fantasia","room":"a_line"}],"illustration":"No pictorial content. Give equal space and visual weight to the two printed choice labels. Leave their response lines empty. Do not invent thumbnails, decorate one choice, add scores or draw selection marks."}
```

### Image prompt - cycle 3

```text
Draw a white portrait choice sheet at 1024 by 1536 pixels, with large plain black text. Title: "Quale foto vuoi tenere?". Under it print exactly these four lines: "Guarda le due foto originali con il genitore." "Indica quella che vuoi tenere per questa attività." "Segna la scelta qui sotto." "Fotografa il foglio con la scelta." In the lower half, place two equally prominent labels, each above its own long empty response line: "Prima foto: foglio bianco" and "Seconda foto: telo a fantasia". The parent will identify the photographs on the separate viewing surface. Do not generate replacement photographs, thumbnails, mug drawings, checkmarks or any additional wording. Allow large marks rather than requiring a signature or written reason.
```

### Hypothetical return - cycle 3

A large cross appears on the response line under the second-photo label only. The choice may have been marked with assistance. The system selects the second stored photograph for the activity result without silently deleting the first.

## Closing output

```text
Hai scelto la foto sul telo a fantasia.
Quella è la foto di questa attività.
```

## Alternative returns

- The first photo is cropped: ask once to include the whole mug, or accept the partial composition if the person explicitly wants it. Do not confuse a framing request with a cognitive judgement.
- The second setup is unchanged: report that the white sheet is still visible and offer the cloth once. If they want the first photo, end there.
- A different object appears: ask whether the person changed the subject intentionally. Do not describe it as the same mug.
- The first photo is chosen: retain that choice and close with the first-photo wording. Do not overrule it because the second looks more decorative.
- Both are chosen: keep both as the result; no single answer is necessary.
- An unclear photograph of the choice arrives: show or read the two choices again once. No selection is inferred from apparent attention.
- Stop or end time: keep the photos already taken and say "Le foto restano disponibili. Non serve scegliere adesso."

## Comparison checks

The second capture must be associated with the same activity and the earlier capture retained as evidence. The choice is about original photographs, not model-made copies. Identity matching should tolerate uncertainty and lighting changes. Do not convert this preference into a general profile of visual ability or taste. The declared adult viewing step is a real dependency, not invisible support.
