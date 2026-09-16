# 13 - What the temperature data support

## Household brief

The parent requests numerical analysis followed by criticism of a causal claim. Computing an arithmetic mean and reading several experimental conditions are explicit prerequisites. A calculator is available. Supply one printed page and a pencil. The temperatures are invented data for a paper exercise, not measurements from an experiment. No hot liquid, apparatus or physical trial is required. Completion means two means, a justified statement about what was observed and a proposed comparison that would address the confounding conditions. The task has exact arithmetic but allows several sound experimental designs.

### Stable parent instructions

```text
Usa dati numerici e chiedi di distinguere un calcolo da una conclusione sulle cause. La media aritmetica e un prerequisito scelto. Fornisci i dati e le condizioni; non semplificare la discussione in una scelta di gusto. Accetta piu progetti di verifica se controllano le condizioni rilevanti.
```

### Feedback guidance

```text
Le proposte recenti chiedevano di spiegare un risultato prima di verificare se i dati bastassero. Lascia spazio per dire che una causa non e stabilita. Una risposta precisa puo dichiarare un limite invece di inventare una spiegazione.
```

These are synthetic example texts. They do not classify the participant or replace the neutral defaults.

## Parent output

Title: Due bicchieri, una conclusione

Overview: Si calcolano due temperature medie e si controlla una spiegazione proposta. Un bicchiere rivestito era piu lontano dalla finestra; il confronto cambia quindi due condizioni insieme. Sul foglio si separano risultato numerico e causa, poi si progetta una prova piu informativa. Si lavora solo su dati inventati, senza preparare bevande.

Themes: dati, medie, progettazione di prove.

## Script output

La media di A vale 27 gradi Celsius; quella di B vale 24 gradi Celsius. B presenta una media inferiore di 3 gradi nelle letture fornite. Il confronto non stabilisce l'effetto del rivestimento: cambia anche la posizione rispetto alla finestra e mancano le temperature iniziali. Non si puo dedurre la velocita di raffreddamento da sole temperature finali. Una proposta di verifica puo usare bicchieri uguali con lo stesso volume e la stessa temperatura iniziale, tempi uguali, condizioni ambientali confrontabili e posizioni scambiate nelle ripetizioni. Non occorre eseguire la prova. Se il partecipante conclude soltanto che B ha la media minore, il risultato descrittivo viene accettato; si chiede separatamente se basta a sostenere una causa. Se nota un ulteriore controllo necessario, viene valutato nel merito.

## Cycle 1

### Display - cycle 1

```text
Le temperature sono inventate per questo esercizio.
Controlla separatamente i conti e la spiegazione.
```

### Page - cycle 1

```json
{"kind":"notebook","title":"Due bicchieri, una conclusione","note":["Dati inventati. A scoperto, B rivestito; letture dopo 10 minuti.","A: 28, 26, 27 gradi C, vicino alla finestra.","B: 24, 25, 23 gradi C, lontano dalla finestra.","Calcola le medie. I dati provano che il rivestimento B isola?"],"spaces":[{"label":"Medie in gradi C","room":"some_lines"},{"label":"Che cosa sostengono i dati","room":"some_lines"},{"label":"Condizioni di una nuova prova","room":"a_box"}],"illustration":"A small schematic of a window and two identical cups, one near the window and one farther away. The farther cup has a plain sleeve. No steam, sunbeam, thermometer, temperature arrows, words or result indicators. It depicts the stated placements without claiming a heating or cooling mechanism."}
```

### Image prompt - cycle 1

```text
Draw a complete portrait analysis page at 1024 by 1536 pixels on white. Use legible black lettering. Title: "Due bicchieri, una conclusione". Print "Dati inventati. A scoperto, B rivestito; letture dopo 10 minuti." "A: 28, 26, 27 gradi C, vicino alla finestra." "B: 24, 25, 23 gradi C, lontano dalla finestra." "Calcola le medie. I dati provano che il rivestimento B isola?" Preserve the order and punctuation of all six temperatures. Provide several empty lines under "Medie in gradi C", several more under "Che cosa sostengono i dati", and a large open area under "Condizioni di una nuova prova". A small schematic near the top shows a window, a bare cup nearby and an identical cup with a plain sleeve farther away. Do not draw sunshine, steam, heat-flow arrows, thermometers or any implied result. Keep the analysis spaces empty. Every specified string appears once; add no extra words or numerical labels.
```

### Help - cycle 1

```text
Per ogni media somma le tre letture e dividi per tre.
Oltre al rivestimento, quali condizioni cambiano?
Conosci le temperature di partenza?
```

### Hypothetical return - cycle 1

The arithmetic gives 27 and 24 correctly. The conclusion says that the sleeve lowered the temperature by three degrees. The proposed new trial specifies equal starting temperatures but retains the same near/far placements.

### Continuation for this return

```text
Le medie sono corrette: 27 e 24 gradi.
La differenza tra le medie non misura da sola l'effetto del rivestimento.
Nella nuova prova restano diverse le posizioni. Come le confronteresti?
```

The reply uses the actual omitted control. If a different valid design is returned, the system discusses that design instead of requiring the authored wording.

## Closing output

```text
I dati danno una media di 27 gradi per A e di 24 per B.
Il rivestimento non e l'unica differenza tra le prove.
Servono condizioni confrontabili per attribuirgli un effetto.
Il progetto della nuova prova resta sul foglio.
```

## Alternative returns

- A photograph contains correct means and a cautious conclusion: accept that distinction. Do not insist that the sleeve works or fails.
- The participant identifies different starting temperatures as a possibility: this is a valid missing control, not a distraction.
- The page is unchanged: offer the arithmetic hint or discuss the conditions aloud through a parent report; do not infer a stop request.
- A mean is miscalculated: identify the affected sum or division before discussing the causal claim. Do not discard a sound design because of that arithmetic error.
- An unreadable photograph leaves an apparent correction ambiguous: retain uncertainty and request one clearer view if wanted.
- Stop or end time: show the two means if requested and preserve any unfinished trial design. No physical experiment is started automatically.

## Comparison checks

The arithmetic has an exact answer; the causal question does not have a supported positive conclusion from these data. A lower final temperature is not itself evidence of better insulation or faster cooling. The baseline, time, volume, vessel and location controls should be considered when evaluating a proposed trial, without demanding a specific script. The image may show relative placement but must not introduce a sunbeam that silently supplies an additional causal premise. Temperatures and the three-degree difference are computed from invented values; they are not experimental evidence. No image has been rendered.
