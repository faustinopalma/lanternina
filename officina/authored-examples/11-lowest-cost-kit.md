# 11 - The lowest-cost display kit

## Household brief

The parent chooses a closed arithmetic problem with several candidate solutions. Addition, multiplication and comparison of whole-number prices are explicit prerequisites; a calculator is available. Supply a pencil and one printed page. All prices are invented for the task. Nobody buys anything, and no account, shop or personal budget is involved. The participant may work independently or ask for the stated hint. The parent sets the end time. Completion means a valid purchase list and an argument that no cheaper list meets the quantities, not merely spending less than the budget.

### Stable parent instructions

```text
Proponi problemi con un obiettivo verificabile e tutti i dati sul foglio. Si possono usare somme, moltiplicazioni e una calcolatrice. Chiedi di confrontare alternative, non solo di indovinare una risposta. Dai un indizio se richiesto; mostra la soluzione alla chiusura.
```

### Feedback guidance

```text
Le ultime proposte lasciavano libero il risultato ma non chiarivano quando il lavoro fosse concluso. Per i problemi numerici, indica il criterio di riuscita e chiedi una breve giustificazione. Non aggiungere difficolta estranee ai dati forniti.
```

This is authored example guidance, not a claimed synthesis from real feedback. The default texts remain unchanged outside this example.

## Parent output

Title: Il kit che costa meno

Overview: Si scelgono pacchi di cartoncini e mollette per preparare un piccolo allestimento. Il catalogo contiene quattro offerte. Bisogna rispettare le quantita e trovare la spesa minima, spiegando quali alternative sono state confrontate. Si usa un foglio; la calcolatrice resta disponibile. Non ci sono acquisti reali.

Themes: prezzi, vincoli, confronto di soluzioni.

## Script output

Il foglio contiene catalogo, quantita e budget. Si cercano almeno 18 cartoncini e 8 mollette, acquistando solo pacchi interi. I due prodotti si possono confrontare separatamente: non ci sono sconti combinati. Il minimo per i cartoncini e 12 euro, con tre pacchi da 6. Il minimo per le mollette e 5 euro, con un pacco da 3 e uno da 5. Il totale minimo e 17 euro; restano 3 euro. Una lista che costa 20 euro puo rispettare il budget senza essere minima. Se arriva questa risposta, si nomina la condizione ancora da controllare e si offre il confronto delle mollette. Una risposta minima senza argomento riceve una domanda sulla verifica, non una nuova attivita. Il genitore puo chiudere senza restituire una fotografia e confrontare il foglio con la soluzione.

## Cycle 1

### Display - cycle 1

```text
Il budget non basta come controllo.
Cerca la spesa minima e conserva il confronto.
```

### Page - cycle 1

```json
{"kind":"notebook","title":"Il kit che costa meno","note":["Servono almeno 18 cartoncini e 8 mollette. Budget: 20 euro.","Cartoncini: pacco da 6 a 4 euro; pacco da 10 a 7 euro.","Mollette: pacco da 3 a 2 euro; pacco da 5 a 3 euro.","Scegli i pacchi interi meno costosi. Spiega il confronto."],"spaces":[{"label":"Pacchi scelti e spesa totale","room":"some_lines"},{"label":"Alternative confrontate","room":"a_box"}],"illustration":"A small outline of blank rectangular display cards and ordinary clips in the upper right corner. These are product symbols, not countable packets or clues. Leave the central calculation area empty. No prices, quantities, coins, numbers or text in the illustration."}
```

### Image prompt - cycle 1

```text
Draw a complete portrait working page at 1024 by 1536 pixels on pure white. Set the title "Il kit che costa meno" in clear black lettering. Below it print four separate catalog and instruction lines: "Servono almeno 18 cartoncini e 8 mollette. Budget: 20 euro." "Cartoncini: pacco da 6 a 4 euro; pacco da 10 a 7 euro." "Mollette: pacco da 3 a 2 euro; pacco da 5 a 3 euro." "Scegli i pacchi interi meno costosi. Spiega il confronto." Keep every price attached to its product and quantity. Add several empty writing lines labelled "Pacchi scelti e spesa totale" and a large open calculation area labelled "Alternative confrontate". Put a small outline motif of blank cards and ordinary clips in the upper right corner, clearly separate from the catalog. It illustrates the products and must not imply packet quantities. Leave the lower half available for calculations. No completed answer, suggested purchase, extra numerals, currency signs or additional text. All prescribed strings appear exactly once.
```

### Help - cycle 1

```text
Confronta prima i cartoncini, poi le mollette.
Puoi comprare piu pezzi di quelli richiesti.
La calcolatrice serve anche a controllare i totali.
```

### Hypothetical return - cycle 1

The page lists three packs of six cards and two packs of five clips, with a correctly added total of 18 euros. The list is feasible but costs one euro more than the minimum. The reader can report the written quantities and total; the arithmetic check belongs to the activity logic, not an inferred judgement about the person.

### Continuation for this return

```text
La tua lista copre entrambe le quantita e costa 18 euro.
Confronta due pacchi da 5 mollette con un pacco da 3 e uno da 5.
Puoi correggere il totale sullo stesso foglio.
```

No second image or printed page is needed. If the participant requests the answer or ends the activity, use the closing output instead of requiring a correction.

## Closing output

```text
Il minimo e 17 euro.
Tre pacchi da 6 cartoncini costano 12 euro.
Un pacco da 3 e uno da 5 mollette costano 5 euro.
Il kit contiene 18 cartoncini e 8 mollette. Restano 3 euro.
```

## Alternative returns

- A photograph shows only a total: ask which packs it includes if a check is wanted. Do not invent the purchase list.
- The page is unchanged: offer the first comparison or the solution. An unchanged page is not itself a stop request.
- A minimum-cost answer lacks justification: ask how cheaper candidates were excluded; accept a table, calculations or a parent-transcribed explanation.
- A higher-cost feasible answer appears: distinguish satisfying the quantities from minimizing cost. Name the exact difference without describing the participant's ability.
- The photograph is unreadable: request one clearer photograph or use a parent report. Keep the claimed result unverified if neither is available.
- Stop or end time: disclose the solution if requested and leave the calculations intact. Do not start another optimization problem.

## Comparison checks

The evidence is finite. Under a total cost below 17 euros, independently minimizing each product is valid because there are no combined discounts. For cards, zero large packs requires three small packs at 12 euros; one large pack requires two small packs at 15 euros; two large packs cost 14 euros; more large packs cannot be cheaper. For clips, zero large packs requires three small packs at 6 euros; one large and one small pack cost 5 euros; two large packs cost 6 euros. Counts above these thresholds only add cost. The unique cheapest pack combination costs 17 euros. This result is derived from the invented catalog, not a claim about current retail prices.

Check whether the system preserves the parent's explicit arithmetic prerequisites and closed goal. The image must reproduce all four offers exactly, and the continuation must identify the actual one-euro improvement rather than offer generic praise. The existing Page contract limits notes to four lines; this example fits those limits without moving a necessary premise into an invisible illustration field. No image has yet been rendered or physically inspected.
