# 12 - The radio running order

## Household brief

The parent requests a finite logic problem whose answer can be checked against all supplied rules. Reading temporal relations and keeping several constraints available on the page are explicit prerequisites. Supply one page and a pencil. The four episode titles and the radio programme are fictional. No broadcasting equipment, online publication or knowledge of radio production is needed. The participant can annotate candidate orders; the parent can read a rule aloud without supplying the order. Completion means an order and a reason that the other possible positions of the adjacent pair do not work.

### Stable parent instructions

```text
Proponi un problema di logica con una soluzione unica. Metti tutti i vincoli sul foglio e permetti di scrivere tentativi. La lettura di piu condizioni fa parte del compito. Chiedi una spiegazione delle esclusioni; offri un indizio solo su richiesta.
```

### Feedback guidance

```text
Una proposta precedente aveva indizi compatibili con piu risposte, ma ne accettava una sola. Controlla l'unicita prima di proporre un problema chiuso. Gli indizi devono bastare senza conoscere intenzioni nascoste dell'autore.
```

This guidance is invented for the reference and is not a real household history.

## Parent output

Title: Quattro episodi in onda

Overview: Il programma ha quattro spazi e tre regole di ordine. Si cerca la sola sequenza che le rispetta tutte. Sul foglio restano il programma e i tentativi esclusi. Non servono conoscenze sulla radio; il compito richiede di combinare i vincoli, non di scegliere la storia preferita.

Themes: sequenze, deduzione, radio.

## Script output

I quattro episodi occupano una posizione ciascuno. A segue subito C, quindi la coppia C-A rimane unita. Se occupa le prime due posizioni, D non puo precedere C. Se occupa le posizioni centrali, D deve aprire e B deve chiudere, contro il terzo vincolo. La coppia occupa dunque le ultime due posizioni. D apre e B occupa la seconda. L'ordine unico risulta D-B-C-A. Una soluzione corretta puo arrivare anche per enumerazione o per prove annotate. La verifica guarda le regole, non la somiglianza con questa spiegazione. Il partecipante puo completare il lavoro sul solo foglio; una fotografia serve soltanto se desidera un riscontro del sistema.

## Cycle 1

### Display - cycle 1

```text
Ogni episodio occupa uno spazio.
Il foglio contiene tutte le regole.
```

### Page - cycle 1

```json
{"kind":"notebook","title":"Quattro episodi in onda","note":["Ordina A, B, C e D: un episodio per ogni spazio.","A segue subito C. D precede C. B non apre e non chiude.","A: Archivio; B: Binario; C: Cortile; D: Darsena.","Trova l'ordine e mostra quali alternative hai escluso."],"spaces":[{"label":"Primo","room":"a_line"},{"label":"Secondo","room":"a_line"},{"label":"Terzo","room":"a_line"},{"label":"Quarto","room":"a_line"},{"label":"Tentativi e ragionamento","room":"a_box"}],"illustration":"A small outline studio microphone beside the title. No timetable, ordering arrows, episode symbols, letters or text in the drawing. Keep the four answer lines empty and leave most of the lower page available for candidate sequences."}
```

### Image prompt - cycle 1

```text
Draw a complete portrait working page at 1024 by 1536 pixels on white, using clear black type and fine rules. Title: "Quattro episodi in onda". Print the four lines "Ordina A, B, C e D: un episodio per ogni spazio." "A segue subito C. D precede C. B non apre e non chiude." "A: Archivio; B: Binario; C: Cortile; D: Darsena." "Trova l'ordine e mostra quali alternative hai escluso." Under the rules place four empty writing lines in reading order, labelled "Primo", "Secondo", "Terzo" and "Quarto". Below them leave a large open area labelled "Tentativi e ragionamento". Include one small outline studio microphone beside the title. Do not draw any episode order, sample answer or candidate sequence. Do not use decorative lettering that makes A, B, C and D difficult to distinguish. Print each prescribed string exactly once and add no other words or numerals.
```

### Help - cycle 1

```text
Tieni C e A vicini, in questo ordine.
Prova dove puo stare questa coppia nei quattro spazi.
```

### Hypothetical return - cycle 1

The four lines contain D, C, A and B. The working area notes that A follows C and D precedes C. Both recorded checks are correct; the last condition has not been satisfied.

### Continuation for this return

```text
Hai rispettato la coppia C-A e hai messo D prima di C.
Nel tuo ordine B chiude. Il terzo vincolo lo esclude.
Prova un'altra posizione per la coppia C-A.
```

This is feedback on the same page, not a demand for a second printed puzzle. A correct returned order with a valid argument proceeds directly to closure.

## Closing output

```text
L'ordine risulta D, B, C, A.
D precede C; A segue subito C; B occupa il secondo spazio.
La coppia C-A non puo stare prima: mancherebbe posto per D.
Non puo stare al centro: B finirebbe nell'ultimo spazio.
```

## Alternative returns

- A photograph shows D-B-C-A with a different proof: accept any sound reasoning, including an exhaustive candidate table.
- The page is unchanged: offer the adjacent-pair hint or the solution. Do not convert the task into a preference choice without the parent's instruction.
- The photograph omits one position: ask about that position before declaring the order invalid.
- Two episodes share a position: restate the one-episode-per-space rule and keep the participant's work available.
- The answer challenges uniqueness: examine the proposed counterexample against all three rules. A genuine counterexample would invalidate the authored problem, not the participant.
- Stop or end time: keep the unfinished attempts, offer the checked order if wanted and close. Do not infer inability from a partial proof.

## Comparison checks

Enumerating all 24 permutations produces exactly one solution, D-B-C-A. Check that the system distinguishes before from immediately before and validates the third rule rather than stopping after the adjacent pair. The delivered image must not accidentally fill answer lines or reorder the letter legend. A correct final order alone is evidence of the written answer, not proof of unaided deduction. The page/prompt pair is a development reference; no image or physical run has been evaluated.
