# Simulare

- **Numero** 64 nell'enciclopedia, capitolo 2 — Che cosa mette in moto la risposta
- **Si chiama anche** far finta, riprodurre in piccolo, modellare, fare le prove, giocare a essere, *simulation*, *model*, *role play*, *dry run*
- **In una riga** far succedere una cosa in una versione ridotta o finta, per vedere come va senza pagarne il prezzo.
- **Fonti** [Simulation](https://en.wikipedia.org/wiki/Simulation) e [Cellular automaton](https://en.wikipedia.org/wiki/Cellular_automaton), lette il 30 agosto 2026; le regole del *Gioco della vita* sono a memoria

## Che cos'è

Costruire una versione ridotta di una cosa e farla funzionare, per vedere che cosa succede. La differenza rispetto al modello è il tempo: un modello rappresenta, una simulazione fa passare il modello attraverso dei passi.

Parti mobili:

- **Che cosa si tiene e che cosa si butta.** È la scelta che decide tutto: una simulazione è fatta soprattutto di quello che ha deciso di ignorare.
- **La scala.** Più piccolo, più lento, più veloce, con meno persone.
- **Il passo.** Un turno, un giorno, un metro. Discreto o continuo.
- **Se è deterministica.** Con un dado, due esecuzioni uguali danno risultati diversi; senza, sempre lo stesso.
- **Chi ci sta dentro.** Se c'è una persona che decide dentro il ciclo, è una simulazione interattiva e diventa anche un gioco di ruolo.
- **La validità.** Sapere se la simulazione dice qualcosa del mondo è un problema aperto e separato dal farla girare.

## Da dove viene

La pagina «Simulation» (presa il 30 agosto 2026) definisce la simulazione come rappresentazione imitativa di un processo che potrebbe esistere nel mondo reale, e propone una distinzione utile: il **modello** rappresenta le caratteristiche o i comportamenti scelti di un sistema, la **simulazione** ne rappresenta l'evoluzione nel tempo. Un'altra formulazione che la stessa pagina riporta: la simulazione è sperimentazione con l'aiuto di un modello.

Si simula quando il sistema vero non si può toccare: perché non è accessibile, perché sarebbe pericoloso o inaccettabile, perché è in progetto e non ancora costruito, o perché non esiste. Quest'ultimo caso è quello che interessa qui.

La pagina distingue la **simulazione fisica** — oggetti veri messi al posto di quelli veri, scelti perché più piccoli o più economici — dalla simulazione al calcolatore, e la **simulazione interattiva** con una persona dentro il ciclo, come nei simulatori di volo. Distingue anche fra simulazione stocastica, in cui esecuzioni ripetute con le stesse condizioni danno risultati diversi, e deterministica, in cui danno sempre lo stesso.

Un caso limite interessante è l'automa cellulare («Cellular automaton», stessa data): una griglia regolare di celle, ciascuna in uno di un numero finito di stati, un vicinato definito per ogni cella, e una regola fissa che dà il nuovo stato a partire dallo stato attuale e da quelli dei vicini. La regola è di solito la stessa per tutte le celle e non cambia nel tempo. Il concetto nasce negli anni Quaranta con Stanislaw Ulam e John von Neumann a Los Alamos, e resta accademico fino agli anni Settanta, quando il *Gioco della vita* di Conway — un automa cellulare bidimensionale — lo fa uscire dall'università. La simulazione si esegue a mano su carta quadrettata, e l'unica cosa che serve è saper contare fino a otto.

## Varianti e parenti

- **Simulazione a turni su carta** — una griglia, una regola, e passi eseguiti a mano.
- **Automa cellulare** (nel capitolo di matematica ricreativa) — la simulazione ridotta al minimo assoluto.
- **Gioco di ruolo** (107) — simulazione con una persona dentro, e la regola è sociale.
- **Gioco da tavolo** (104) — una simulazione con vincitore.
- **Modello in scala** (46) — il modello senza il tempo.
- **Serious game** — simulazione costruita per far imparare qualcosa, non per vincere.
- **Previsione** (28) — la metà che dà senso a una simulazione: dire prima come andrà.
- **Provare** (65) — simulare è provare su un sistema finto, e costa meno per lo stesso motivo.
- **Progettare** (66) — si simula per decidere, e questo è il caso più comune fuori dalla scuola.

## Che cosa se ne sa

Da «Simulation» (presa il 30 agosto 2026): i problemi centrali della modellazione sono l'acquisizione di fonti valide sulle caratteristiche da rappresentare, l'uso di approssimazioni e assunzioni semplificatrici dentro il modello, e la fedeltà e validità dei risultati. Verifica e validazione sono un campo di studio in corso. Tradotto: **il risultato di una simulazione non è un fatto, è la conseguenza delle scelte fatte prima di partire**, e questa è esattamente la cosa che una simulazione ben fatta può far vedere a chi la esegue.

L'osservazione pratica: **una simulazione a mano su carta è più istruttiva di una al calcolatore**, perché chi esegue i passi è costretto a leggere la regola dieci volte e a vedere dove non copre. Non ha una fonte: **va verificata**.

Seconda osservazione: **la parte che produce ragionamento non è far girare la simulazione, è cambiare un numero e rifarla.** Una sola esecuzione produce un risultato; due esecuzioni con una differenza producono una relazione, che è l'unica cosa che valga la pena portarsi via.

Terza: **una simulazione dichiara le proprie assunzioni per costruzione.** Se qualcosa non è nella regola, non succede. È il raro caso in cui la lista di quello che si sta ignorando è disponibile a chi guarda, e chiederla è gratis.

## Esempi trovati

Dagli automi cellulari: il *Gioco della vita* di Conway, eseguito su carta quadrettata con una gomma.

Dalla scuola: la simulazione di un'elezione, di un'assemblea, di un processo — il gioco di ruolo usato come simulazione di istituzioni.

Dall'epidemiologia: il modello a compartimenti, che nella versione minima è tre numeri e due regole.

Dall'ingegneria: la galleria del vento, che è simulazione fisica — l'oggetto è vero e piccolo, l'aria è vera e veloce.

Dalla cucina: la mezza dose, che è una simulazione della ricetta e insegna che non tutto si dimezza allo stesso modo.

## Un esempio giocabile

> **La città che si spegne**
>
> Una griglia 10 × 10. Ogni casella è una casa, e ogni casa la sera accende o non accende la luce.
>
> **La regola**, che vale per tutte le case, ogni sera:
>
> ```
>  Guarda le case che toccano la tua, comprese quelle in diagonale (sono 8,
>  o meno se stai sul bordo). Conta quante avevano la luce accesa IERI sera.
>
>   · se erano 2 o 3   →  stasera accendi
>   · se erano 0, 1     →  stasera resti al buio (ti senti solo)
>   · se erano 4 o più  →  stasera resti al buio (troppa confusione)
> ```
>
> Comincia annerendo dodici caselle a caso e disegna **cinque sere**, una griglia per sera.
>
> ```
>  sera 1   sera 2   sera 3   sera 4   sera 5
>  (griglie stampate, 10 × 10, cinque volte)
>
>  Case accese la sera 1: ────   la sera 5: ────
>  È successo qualcosa che si ripete uguale? Da quale sera? ────
>  Una cosa che questa regola NON sa fare, e che in una città vera succede:
>  ───────────────────────────────────────────────
>
>  Adesso rifallo cambiando UNA cosa sola: parti da sei case invece che da
>  dodici, nella stessa disposizione ristretta. Che cosa cambia?
>  ───────────────────────────────────────────────
> ```
>
> Le regole sono quelle del *Gioco della vita*, l'automa cellulare inventato da John Conway; secondo «Cellular automaton» è negli anni Settanta che rende popolare la cosa. Le ho riscritte con altre parole. Non c'è niente da vincere: la griglia fa quello che fa.

Le griglie stampate fanno tutto il lavoro: la simulazione si esegue con una matita e non serve nient'altro. La regola è scritta in termini di case e non di celle, il che dà un motivo per eseguirla senza pretendere che significhi qualcosa di vero — la consegna non sostiene che le città funzionino così.

La domanda su quello che la regola non sa fare è la parte che vale: chiede la lista delle assunzioni, che in una simulazione è sempre disponibile e non viene mai chiesta. E rifare tutto cambiando un numero solo è la differenza fra eseguire e sperimentare.

Su carta regge, con un costo: cinque griglie 10 × 10 su un A4 stanno, ma strette; due fogli sono meglio. Il limite vero è un altro: **chi ha scritto la consegna non può verificare che le cinque griglie siano giuste**, perché dovrebbe eseguire la stessa simulazione e confrontarla cella per cella. La verifica sta nella regola stessa: chi sbaglia una cella se ne accorge alla sera dopo, perché la figura smette di comportarsi come le altre.

## Che cosa la rende interessante

**Chiedere che cosa il modello non sa fare** è il parente diretto di *chiedere che cosa un sistema non riesce a dire*, schede 017 e 019, e della voce 63, inferire da un'assenza. Quarta occorrenza in tre capitoli lontani: qui la lista delle assunzioni è disponibile per costruzione, il che la rende il caso più pulito.

**Rifare cambiando una cosa sola** è il metodo sperimentale ridotto a una riga di consegna, e riappare nella voce 65, provare. Vale la pena guardare se sia una struttura di momento a sé — due esecuzioni con una differenza — invece che una richiesta.

**La griglia stampata come materiale eseguibile.** Non serve a scrivere una risposta: serve a far girare qualcosa. È un terzo uso della griglia, dopo quello che rende praticabile una forma lunga e quello che rende visibile un'assenza.

**L'esecuzione non ha bisogno di essere verificata da nessuno.** La regola è il proprio controllo dell'errore, come i pezzi che entrano in un modo solo di Montessori. Quante forme abbiano un controllo dell'errore fatto di una regola invece che di un oggetto resta una domanda aperta.
