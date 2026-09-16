# 10 - A label for an object

## Household brief

The adolescent likes looking closely at objects and chooses a safe, familiar item to display on a shelf or table. For this reference the adult offers a large smooth stone and a large wooden spoon; the person selects the stone. Neither is sharp or small enough to swallow. No collecting outside, washing, tasting, naming minerals or recalling where the object came from is required. The adult can read aloud and mark a description chosen by pointing. At most three printed sheets are available: two guides and an optional final label. The final label is an output, not an extra photographed-return requirement.

## Parent output

Title: Il cartellino per il mio oggetto

Overview: Si osserva un oggetto scelto e si decide quale dettaglio mettere sul suo cartellino. La stampante prepara le guide e il cartellino finale. Restano oggetto e descrizione da mettere vicini. Serve un oggetto sicuro scelto con il genitore. Non bisogna indovinare il materiale o raccontare una storia: si parte da ciò che è visibile.

Themes: osservazione, oggetti, esposizione.

## Script output

Il ragazzo sceglie un oggetto e lo fotografa intero su un foglio bianco. Nel percorso principale è un sasso con una fascia chiara visibile. La lettura descrive la fascia senza attribuire un minerale, una provenienza o un'età. Il seguito propone due descrizioni brevi compatibili con la foto e la possibilità di dirne un'altra al genitore. Il ragazzo sceglie la fascia. La stampa finale riporta quella descrizione senza ridisegnare il sasso: il vero oggetto le sta accanto. Il testo conclusivo non annuncia l'apertura di un museo o un pubblico che non esiste.

## Cycle 1

### Display - cycle 1

```text
Scegli un oggetto da guardare da vicino.
Mettilo sul foglio bianco e fotografalo.
```

### Page - cycle 1

```json
{"kind":"notice","title":"Guarda il tuo oggetto","note":["Scegli uno degli oggetti preparati con il genitore.","Mettilo su un foglio bianco.","Fotografa l'oggetto intero.","Tienilo sul tavolo: faremo il suo cartellino."],"spaces":[],"illustration":"Two separate unselected reference objects: one large rounded stone and one large wooden spoon, both drawn plainly. These show the offered materials, not objects already selected or photographed. No mineral texture clues, colour names, provenance, choice marks, labels or additional text."}
```

### Image prompt - cycle 1

```text
Create a complete portrait page at 1024 by 1536 pixels, pure white with large readable black type. Title: "Guarda il tuo oggetto". Print exactly four lines: "Scegli uno degli oggetti preparati con il genitore." "Mettilo su un foglio bianco." "Fotografa l'oggetto intero." "Tienilo sul tavolo: faremo il suo cartellino." Below, draw a large rounded stone and a large plain wooden spoon as separate unselected reference objects. Use simple black outlines and ample white space. Do not favour either, invent lettering or marks on them, add material names, mineral diagrams, collecting instructions, selection circles or any other words. The drawings identify the available choices and are not claimed to reproduce the person's selected object.
```

### Help - cycle 1

```text
Puoi tenere l'oggetto che hai già scelto.
Chiedi aiuto per farlo entrare intero nella foto.
```

### Hypothetical return - cycle 1

A rounded stone is fully visible on the white sheet. It has a broad pale band across its upper surface and an uneven outer edge. The photograph provides no reliable evidence of material composition, origin or the feel of its surface.

## Cycle 2

### Display - cycle 2

```text
Sul sasso si vede una fascia chiara.
Scegli che cosa scrivere sul cartellino.
```

### Page - cycle 2

```json
{"kind":"notebook","title":"Che cosa vuoi far notare?","note":["Guarda il sasso e ascolta le due frasi.","Segna quella che vuoi sul cartellino.","Puoi dire un'altra frase al genitore.","Fotografa il foglio con la scelta."],"spaces":[{"label":"Questo sasso ha una fascia chiara.","room":"a_line"},{"label":"Il bordo di questo sasso è irregolare.","room":"a_line"}],"illustration":"No image of the stone. Give the two sentence choices equal space and an empty broad response line below each. The actual stone stays on the table for observation. No invented patterns, scientific labels, selected options or additional words."}
```

### Image prompt - cycle 2

```text
Draw a full portrait choice page at 1024 by 1536 pixels on pure white. Use large plain black text. Title: "Che cosa vuoi far notare?". Print these four lines exactly: "Guarda il sasso e ascolta le due frasi." "Segna quella che vuoi sul cartellino." "Puoi dire un'altra frase al genitore." "Fotografa il foglio con la scelta." In the lower portion place two equally prominent sentence choices, each with a long empty response line underneath: "Questo sasso ha una fascia chiara." and "Il bordo di questo sasso è irregolare." Leave enough separation for a broad mark. Do not draw a replacement stone, invent a texture, preselect a sentence or add any other words. The real stone supplies the visual evidence beside this page.
```

### Hypothetical return - cycle 2

One broad mark crosses the response line for the pale-band sentence. The other line is unchanged. No additional statement is written or reported by the parent.

## Final page

This optional third sheet is delivered without asking for another return. Its exact output is included to distinguish a usable result from a verbal promise to produce one.

### Page - final page

```json
{"kind":"label","title":"Il sasso con la fascia","note":["Questo sasso ha una fascia chiara."],"spaces":[],"illustration":"A simple display label occupying the central upper portion of the sheet, with generous white space. No depiction of the stone, decorative border, mineral name, collection number or added text. It must remain readable as a whole uncut sheet placed beside the real object."}
```

### Image prompt - final page

```text
Draw one portrait display-label page at 1024 by 1536 pixels on pure white. Print exactly the title "Il sasso con la fascia" in large plain black type and the sentence "Questo sasso ha una fascia chiara." below it. Keep the text in a spacious central upper area so the entire uncut sheet can stand or lie beside the actual object. Add no drawing of the stone, border, scientific classification, collection number, date, barcode or other words. This is a finished label, not a worksheet or a claim about the object's origin.
```

## Closing output

```text
Il cartellino parla della fascia chiara.
Puoi metterlo accanto al sasso.
```

## Alternative returns

- The spoon was selected: describe visible spoon details and offer two truthful descriptions of that object. Do not force a stone activity after the choice.
- The first photograph has glare that could resemble a pale band: do not use the band as established evidence. Request another angle once or choose a clearly visible outline feature instead.
- The other sentence is selected: the final label describes the irregular edge. The pale-band label is not printed.
- A parent reports a different phrase the adolescent chose: use that phrase if appropriate, distinguishing a personal statement from a visible fact. Do not claim the model read handwriting when the input was a parent report.
- The choice sheet is unchanged: offer a pointed or spoken choice, or end with the object alone. A label is optional.
- Both choices are marked: a label may contain both true observations if the participant agrees. Do not require one answer for the parser's convenience.
- Stop or end time: "Possiamo tenere l'oggetto sul tavolo anche senza cartellino. Per oggi abbiamo finito."

## Comparison checks

The second page must use a feature actually visible in the first photo. A model-generated drawing is not a substitute for the original object's evidence. Geological or historical claims are not derived from appearance. The final label uses the selected wording; it does not expand a short choice into an invented story. Choosing an observation is not a test of expressive vocabulary.
