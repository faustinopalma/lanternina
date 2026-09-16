# 04 - A place for three objects

## Household brief

The adolescent agrees to arrange a small part of their own table. The adult supplies their notebook, familiar over-ear headphones and a broad pencil. Use headphones with no connected electrical device; keep any cable loose on the table and away from the body. Clear a reachable working area without removing the adolescent's possessions without consent. The person can grasp or indicate the objects, with physical support if needed. There is no correct decorative layout or assumed dominant hand. Print at most two sheets. Photograph only this prepared area.

## Parent output

Title: Il posto delle mie cose

Overview: Si sceglie dove mettere quaderno, cuffie e matita e si prova a usarli in quella posizione. La stampante prepara una guida e, se serve, un suggerimento legato alla foto. Resta una disposizione da tenere sul proprio tavolo. Servono i tre oggetti. Il genitore chiede prima il permesso di spostarli: riordinare non è un obbligo.

Themes: oggetti personali, disposizione, uso del tavolo.

## Script output

Il ragazzo dispone tre oggetti reali come preferisce. La prima foto serve a vedere dove sono, non a giudicare l'ordine. Nel percorso principale il cavo delle cuffie attraversa il quaderno. Il seguito chiede di aprire il quaderno e prendere la matita; propone di spostare qualcosa solo se il ragazzo vuole. La seconda foto mostra una disposizione diversa. Si conclude conservando la scelta, senza affermare che sia più comoda finché la persona non lo comunica. Se la prima disposizione va già bene, non serve cambiarla.

## Cycle 1

### Display - cycle 1

```text
Scegli dove mettere quaderno, cuffie e matita.
Puoi provare più di una disposizione.
```

### Page - cycle 1

```json
{"kind":"notice","title":"Il posto delle mie cose","note":["Metti sul tavolo quaderno, cuffie e matita.","Sistemali come vuoi usarli.","Puoi lasciarli anche dove sono.","Fotografa soltanto questo pezzo del tavolo."],"spaces":[],"illustration":"Three large separate black outline drawings: a closed notebook, over-ear headphones with a loose short cable, and a broad pencil. Objects are shown individually, not in a model tabletop arrangement. No arrows, preferred positions, left/right labels, additional objects or text."}
```

### Image prompt - cycle 1

```text
Produce one portrait instruction page, 1024 by 1536 pixels, on pure white with large plain black text. Print the title "Il posto delle mie cose" and exactly four lines: "Metti sul tavolo quaderno, cuffie e matita." "Sistemali come vuoi usarli." "Puoi lasciarli anche dove sono." "Fotografa soltanto questo pezzo del tavolo." Below, draw three separate familiar objects in black outline: a closed notebook, over-ear headphones with a loose short cable, and a broad pencil. Leave ample space between them. This identifies the materials; it must not show a recommended arrangement or impose symmetry. No arrows, labels, hands, background room, screens or extra words. All content remains inside wide print margins.
```

### Help - cycle 1

```text
Puoi iniziare dal quaderno.
Indica dove vuoi metterlo, se preferisci.
```

### Hypothetical return - cycle 1

The notebook is in the middle, the pencil beside it and the headphones behind it. The cable crosses the closed notebook. The photo cannot establish reach, comfort, intended hand use or whether the arrangement was made independently.

## Cycle 2

### Display - cycle 2

```text
Il cavo passa sopra il quaderno.
Prova ad aprire il quaderno dove si trova.
```

### Page - cycle 2

```json
{"kind":"notice","title":"Prova la disposizione","note":["Apri il quaderno.","Prendi la matita e appoggiala su una pagina.","Se vuoi, sposta qualcosa.","Fotografa la disposizione che vuoi tenere."],"spaces":[],"illustration":"A simple open notebook with a pencil resting on one page. A separate small drawing identifies a pair of over-ear headphones. Do not redraw the participant's table, prescribe where headphones go or show a hand preference. No visible notebook writing, arrows, position labels or other text."}
```

### Image prompt - cycle 2

```text
Draw a complete white portrait page at 1024 by 1536 pixels. Use large black sans-serif text. Print exactly "Prova la disposizione" as the title, followed by "Apri il quaderno." "Prendi la matita e appoggiala su una pagina." "Se vuoi, sposta qualcosa." "Fotografa la disposizione che vuoi tenere." Below, draw an open blank notebook with a broad pencil resting on a page. Separately, draw over-ear headphones as a small material reminder. Use clear outline drawings without shading. Do not invent a photograph of the participant's table, recommend positions, depict left or right handedness, add arrows or print any other text. Leave substantial white space and wide margins.
```

### Hypothetical return - cycle 2

The notebook is now open. A pencil is on its right-hand page. The headphones remain behind it, and the cable lies beside rather than across the notebook. This does not prove that reaching was comfortable.

## Closing output

```text
Ora il cavo passa accanto al quaderno aperto.
Puoi tenere questa disposizione.
```

## Alternative returns

- The first layout already leaves the notebook clear: say "Prova ad aprire il quaderno e prendere la matita." Do not announce a cable obstruction.
- The layout is unchanged and the person wants to keep it: accept it. An unchanged image is not noncompliance.
- The person says the pencil is hard to reach: offer "Indica un posto più vicino per la matita." Use that stated difficulty, not a guessed motor limitation.
- An object is absent from the photograph: report it as outside view or not visible. Ask once before saying it has been lost.
- A new layout looks neat but no comfort report exists: describe the arrangement only. Do not claim improvement or independence.
- Stop or refusal to rearrange: "Lasciamo le tue cose dove vuoi. Per oggi abbiamo finito."

## Comparison checks

The reason for a follow-up must come from visible placement or a stated difficulty. Tidiness is not the success criterion. Camera framing must exclude unrelated personal papers. The workflow must distinguish a scene photo from a blank returned sheet and must not diagnose comfort from object geometry.
