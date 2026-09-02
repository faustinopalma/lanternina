# Labirinto logico

- **Numero** 165 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi fisici e meccanici»
- **Si chiama anche** labirinto con regole, labirinto multi-stato, *logic maze*, *mazes with rules*, labirinto a numeri, labirinto a dado
- **In una riga** un labirinto le cui regole di movimento sono strane.
- **Fonti** [Logic maze](https://en.wikipedia.org/wiki/Logic_maze), [Robert Abbott (game designer)](https://en.wikipedia.org/wiki/Robert_Abbott_(game_designer)), [Maze](https://en.wikipedia.org/wiki/Maze), prese il 30 agosto 2026

## Che cos'è

Un labirinto in cui il vincolo non sono i muri ma **le regole di movimento**. Il disegno può non avere corridoi affatto: può essere una griglia di numeri, o di frecce, o di caselle colorate. Quello che dice dove si può andare è una regola scritta accanto.

La differenza con la voce 164, labirinto su carta è precisa e la fonte la scrive in una riga: sono labirinti «che usano regole diverse da *non attraversare le linee* per limitare il movimento» («Maze», 30 agosto 2026).

Parti mobili:

- **Che cosa è la regola.** Non si gira a sinistra; ci si sposta di tante caselle quante ne dice il numero su cui si è; si può salire solo su una casella di area maggiore della precedente; si fa rotolare un dado e conta la faccia che sta sopra.
- **Se il labirinto ha più di uno stato.** È il punto tecnico della famiglia. Se tornando su una casella già visitata le possibilità sono diverse — perché si arriva da un'altra parte, o perché il dado ha girato — allora la posizione non basta a dire dove si è.
- **Quanto è dichiarata la regola.** Le regole possono essere scritte in cima, oppure dedotte dai simboli sul foglio.
- **Se la regola cambia per strada.** Nei casi estremi la regola stessa dipende da come si è arrivati.

**Il concetto che tiene insieme tutto è quello di stato.** In un labirinto normale, sapere dove si è basta a sapere che cosa si può fare. In un labirinto logico non basta: bisogna sapere anche qualcos'altro — da dove si viene, che numero mostra il dado, quali caselle si sono già toccate. Levando questa proprietà si torna alla voce precedente.

## Da dove viene

Ha un inventore, una data e un numero di rivista. **Robert Abbott** inventa il labirinto logico, e il primo pubblicato è **Traffic Maze in Floyd's Knob**, uscito nel numero dell'ottobre **1962** dello *Scientific American*, nella rubrica *Mathematical Games* di Martin Gardner («Logic maze», «Robert Abbott (game designer)», 30 agosto 2026).

Quel primo labirinto ha l'aspetto di una griglia di strade con delle frecce a ogni incrocio. Arrivati a un incrocio si possono seguire solo le frecce che portano **dalla strada su cui si è** a un'altra strada. Ne segue che arrivando allo stesso incrocio da due direzioni diverse si hanno possibilità diverse, ed è precisamente questo che lo rende un labirinto multi-stato.

Abbott era un inventore di giochi di carte prima che di labirinti: le regole del suo gioco *Eleusis* furono pubblicate da Gardner nel giugno **1959**, e il suo libro *Abbott's New Card Games* è del 1963. La fonte annota che ebbe un successo modesto e che «si stancò», e da lì passò ai labirinti, raccolti poi in *Mad Mazes* (**1990**) e *SuperMazes* (**1997**).

Vale la pena registrare come Abbott presenta le sue cose difficili, perché è una scelta di consegna. Di *Where are the Cows?* avverte che «potrebbe essere troppo difficile perché qualcuno lo risolva». Di *Theseus and the Minotaur* scrive che «è il labirinto più difficile del libro; è possibile che nessuno lo risolva». **Sono due dichiarazioni d'impossibilità stampate accanto al problema**, ed è la mossa raccolta cinque volte in questa enciclopedia — dire prima che potrebbe non venire — usata da un autore che vende libri di enigmi.

## Varianti e parenti

- **Labirinto a frecce** — il primo di tutti: a ogni incrocio si può svoltare solo dove le frecce lo consentono, e conta da dove si arriva.
- **Labirinto a numeri** — una griglia di cifre; da una casella ci si sposta esattamente del numero che c'è scritto.
- **Labirinto a dado che rotola** — si fa rotolare un dado di casella in casella, e dove si può andare dipende dalla faccia in alto. Se si torna sulla stessa casella il dado può mostrare un'altra faccia, e le scelte sono altre.
- **Labirinto ad aree (A-maze)** — l'area della casella su cui si mette il piede deve aumentare e diminuire alternativamente a ogni passo.
- **Labirinto a inclinazione (*tilt maze*)** — ci si muove in una direzione finché non si sbatte contro qualcosa.
- **Labirinto multi-stato in senso stretto** — le regole di navigazione cambiano a seconda di come si è navigato finora.
- **Labirinto ad anse e trappole** — porte a senso unico. È il caso più semplice di stato: dopo essere passati, quella porta non c'è più.
- **Labirinto su carta** — voce 164, labirinto su carta: i muri al posto delle regole.
- **Puzzle a griglia** — voce 142, puzzle a griglia (chi beve cosa, chi vive dove): una griglia e delle regole, ma senza nessun percorso e senza nessuno stato.
- **Enigma di teoria dei giochi** — voce 157, enigma di teoria dei giochi: là si ragiona sulle posizioni raggiungibili, e la struttura è la stessa.

**Il confine con il capitolo 13.** La voce 366, problema di grafi raccoglie i problemi che chiedono l'idea del grafo. Un labirinto multi-stato **è** un grafo i cui nodi non sono le caselle ma le coppie casella-più-stato, ed è il modo tecnico di risolverlo; qui si descrive la forma di pagina — una griglia stampata, una regola scritta in due righe — e quello che chiede a chi la riceve.

## Che cosa se ne sa

Fonti prese il 30 agosto 2026. «Logic maze» è una pagina di poche righe e non contiene nessuna misura; «Robert Abbott (game designer)» è una biografia. Su che cosa produca questa forma in chi la riceve **non c'è nessun dato**, e non è stato trovato altrove.

Quello che le fonti dicono, e che è utile, riguarda la costruzione. **A un certo punto queste griglie devono essere progettate da un programma.** Testuale: i labirinti a inclinazione e altri disegni nuovi «di solito aumentano la complessità del labirinto, a volte al punto che il labirinto deve essere progettato da un programma per eliminare i percorsi multipli» («Logic maze»). È la stessa cosa già registrata per il cruciverba alla voce 125, cruciverba, per il sudoku alla voce 154, sudoku e affini (Nikoli) e per il puzzle a griglia alla voce 142, puzzle a griglia (chi beve cosa, chi vive dove): **costruire costa più che risolvere**, e la garanzia di unicità è la parte che costa.

Il fatto strutturale, che si può registrare senza fonti perché discende dalla definizione: **una regola in più non rende il problema un po' più difficile, lo rende un altro problema.** Lo stesso disegno con due regole diverse ha due soluzioni diverse, e possono essere lontanissime. Nell'esempio costruito qui sotto una regola sola — non tornare subito indietro — porta la strada minima da sei mosse a quindici, sulla stessa identica griglia.

E un fatto che riguarda chi consegna: **questa è la forma del capitolo con il rapporto più alto fra quanto costa stampare e quanto costa risolvere.** Sedici cifre su una griglia quattro per quattro sono quattro righe di stampa. Nessun muro, nessun disegno, nessuna figura da ritagliare.

## Esempi trovati

Da *Traffic Maze in Floyd's Knob*, ottobre 1962: una griglia di strade con frecce agli incroci, e la regola che a ogni incrocio si possono seguire solo le frecce che partono dalla strada su cui si è.

Da *Where are the Cows?*, in *SuperMazes*: un labirinto che usa auto-riferimento, regole che cambiano e diagrammi di flusso, ed è scritto apposta per confondere un oggetto — per esempio un testo rosso — con il riferimento a quell'oggetto — la parola «rosso» — e con riferimenti ancora più sottili, come la parola «parola». **Si percorre con due mani, che partono da due punti diversi**, e le istruzioni della casella dove sta una mano possono riguardare la casella dove sta l'altra, o caselle già lasciate, o combinazioni delle due.

Da *Theseus and the Minotaur*, in *Mad Mazes*: dichiarato dall'autore come il più difficile del libro, e forse irrisolvibile da chiunque. Ne sono state fatte molte versioni da altri, su carta ed elettroniche.

Dai labirinti a dado: la stessa casella dà scelte diverse a seconda della faccia che il dado mostra in quel momento.

## Un esempio giocabile

Sedici cifre e due righe di regola. Sul foglio c'è una griglia e nient'altro; il resto è la regola.

> **La stessa griglia, due regole, due risposte**
>
> Parti dalla casella in alto a sinistra. Devi arrivare alla **V** in basso a destra.
>
> **La regola:** sulla casella dove sei c'è un numero. Ti sposti di **esattamente quel numero di caselle**, in linea retta, in una delle quattro direzioni — su, giù, a sinistra, a destra. Non si esce dalla griglia. Non si va in diagonale.
>
> ```
>  3   3   1   1
>
>  1   1   1   3
>
>  1   3   1   1
>
>  1   1   2   V
> ```
>
> ```
>  Il numero minimo di mosse e' ─────
>
>  Scrivi qui le caselle che hai toccato, in ordine:
>
>  ───────────────────────────────────────────────────────────
> ```
>
> Adesso **la stessa griglia**, con una regola in più:
>
> **non puoi tornare subito indietro.** Se una mossa ti ha portato verso destra, la mossa dopo non può essere verso sinistra; se ti ha portato in giù, la mossa dopo non può essere in su. Dopo si torna a poter fare tutto.
>
> ```
>  Adesso il numero minimo di mosse e' ─────
> ```
>
> Un avvertimento, perché è quello che rende il secondo compito diverso dal primo e non solo più difficile: **con questa regola non basta più sapere in che casella sei.** Devi ricordarti anche da che parte ci sei arrivato, perché la stessa casella, raggiunta in due modi, non offre le stesse mosse.

I due numeri sono stati calcolati con un programma che esplora tutte le mosse possibili. Senza la seconda regola la strada più corta ha **sei** mosse ed è unica. Con la seconda regola ne ha **quindici**, ed è ancora unica: **due volte e mezzo più lunga, sulla stessa griglia, per una riga di regola.** La strada corta comincia andando tre caselle a destra e poi tornando indietro di una, cioè fa esattamente la cosa che la seconda regola vieta — ed è per questo che il secondo problema non si ottiene aggiustando il primo, ma va rifatto.

Il paragrafo finale è la parte che vale, e non è un aiuto: dice che cosa sia lo *stato*, che è l'unica idea di tutta questa voce, senza usare la parola. Chi lo legge sa che deve tenere il conto di due cose invece che di una, e il resto del lavoro resta intero.

**Il limite, dichiarato:** quindici mosse a mano su una griglia dove ogni casella ha fino a quattro uscite e ogni uscita dipende da come si è arrivati sono parecchie. Il foglio non lo nasconde e sarebbe meglio se dicesse anche quanto costa — cosa che chi ha costruito la griglia sa e chi legge no, ed è la stessa asimmetria già registrata alla voce 160, tangram e puzzle di tassellazione.

## Che cosa la rende interessante

**Una regola in più non è una difficoltà in più: è un altro problema.** Sei mosse contro quindici, stessa griglia. È la dimostrazione più economica raccolta in questa enciclopedia del fatto che la difficoltà di un compito non sta nel materiale, e costa una riga di stampa. Da provare all'indietro su tutte le forme dell'elenco che abbiano una regola dichiarata.

**Lo stato è un'idea che si consegna senza nominarla.** «Devi ricordarti anche da che parte ci sei arrivato» è la definizione operativa di una nozione che in informatica ha un nome tecnico, e in due righe di consegna arriva intera. Alle voci 114, indovinello dell'anno e 119, rebus si era osservato che pochissime forme insegnano qualcosa risolvendosi: questa è la terza.

**È la forma con il rapporto più alto fra costo di stampa e lavoro prodotto di tutto il blocco.** Sedici cifre. Nessun disegno, niente da ritagliare, niente da procurare. Se una sola forma di questo capitolo dovesse entrare per prima in un pomeriggio, il conto la mette in cima.

**Un autore che vende enigmi stampa «forse nessuno ci riuscirà» accanto al problema.** Abbott lo fa due volte, in due libri. È la conferma esterna più forte trovata alla mossa raccolta alle voci 014, 032, 034, 044 e 046: non è una gentilezza da casa, è una scelta editoriale.

**Un labirinto costruito su una confusione fra una cosa e il suo nome.** *Where are the Cows?* usa il rosso e la parola «rosso», e la parola «parola». È lo stesso materiale della voce 158, enigma auto-referenziale, applicato a un percorso invece che a un quiz, e in questa enciclopedia non c'è nessun'altra forma che li tenga insieme.

