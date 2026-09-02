# Automa cellulare

- **Numero** 374 nell'enciclopedia, capitolo 13 — Giochi matematici e ricreativi
- **Si chiama anche** gioco della vita, automa cellulare elementare, regola su griglia, formica di Langton, *cellular automaton*, *Game of Life*, *Langton's ant*, *elementary CA*
- **In una riga** regole semplici su una griglia che producono cose non previste.
- **Fonti** [Cellular automaton](https://en.wikipedia.org/wiki/Cellular_automaton), [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), [Elementary cellular automaton](https://en.wikipedia.org/wiki/Elementary_cellular_automaton), [Wolfram code](https://en.wikipedia.org/wiki/Wolfram_code), [Rule 30](https://en.wikipedia.org/wiki/Rule_30), [Langton's ant](https://en.wikipedia.org/wiki/Langton%27s_ant), [Gioco della vita](https://it.wikipedia.org/wiki/Gioco_della_vita), lette il 2 settembre 2026

## Che cos'è

Una griglia di caselle, ognuna in uno di pochi stati; per ogni casella un **vicinato**, cioè quali altre caselle la riguardano; e una regola sola, uguale per tutte, che dice lo stato al passo dopo in funzione del vicinato al passo prima. Si sceglie una configurazione di partenza e si applica la regola a tutte le caselle **insieme**. Non c'è altro.

Le parti mobili:

- **Quante dimensioni.** Una riga di caselle, con il tempo che scorre verso il basso e la storia che resta stampata; oppure un piano, dove la storia si cancella a ogni passo.
- **Il vicinato.** Le quattro caselle ortogonali — è quello di von Neumann — o tutte e otto — è quello di Moore. Su una riga, le due accanto.
- **Quanti stati.** Due, quasi sempre. Vivo e morto, bianco e nero.
- **Che cosa si chiede.** Applicare la regola e guardare che cosa viene, oppure — è la versione con una risposta — guardare che cosa è venuto e dire quale fosse la regola.
- **Dove finisce la griglia.** Bordi fissi, oppure lati incollati a formare un toro. «Cellular automaton» avverte che la scelta cambia il valore di ogni casella.

**La differenza dalla voce 371, costruzione con riga e compasso:** là la prova che si è finito stava in tre posti diversi. Qui, nella forma pura, **non sta da nessuna parte perché non c'è niente da provare**: si applica la regola e la griglia fa quello che fa. Non esiste una risposta giusta, non esiste un errore da correggere — chi sbaglia una casella ha semplicemente un altro quadro. **È il valore estremo della scala del blocco**, e la scheda che ne esce funziona solo perché la domanda viene girata al contrario.

## Da dove viene

**Nasce a Los Alamos negli anni Quaranta e non nasce come gioco.** «Cellular automaton»: Stanisław Ulam studiava la crescita dei cristalli con un reticolo; John von Neumann, suo collega, lavorava al problema delle macchine che si riproducono, e il suo primo progetto — un robot che ne costruisce un altro — si rivelò impraticabile per la quantità di pezzi da fornirgli. **Fu Ulam a suggerire di passare a un sistema discreto.** Ne uscì il costruttore universale di von Neumann: una configurazione di **200 000 celle** con **29 stati** per cella, di cui è dimostrato che fa copie di sé stessa all'infinito.

**Il Gioco della vita è del 1970 e ha una data di pubblicazione precisa.** «Conway's Game of Life» e «Gioco della vita»: John Horton Conway comincia a provare regole nel 1968 cercando, secondo Gardner, un insieme che facesse crescere certe configurazioni apparentemente senza limite pur rendendo difficile dimostrarlo. Il gioco esce nel numero di **ottobre 1970** di *Scientific American*, nella rubrica «Mathematical Games» di Martin Gardner. È **un gioco a zero giocatori**: l'evoluzione dipende solo dallo stato iniziale, non c'è modo di vincere e non c'è un ultimo passo.

**Le regole a una dimensione sono del 1983 e hanno un catalogo.** «Wolfram code»: Stephen Wolfram introduce in un articolo di quell'anno il modo di numerare le regole che porta il suo nome, e che è **notazione posizionale applicata a una tabella** — si ordinano le otto configurazioni del vicinato, si legge la colonna dei risultati come un numero in base due, e quel numero è il nome della regola. La regola 30 esce nello stesso 1983; la 110 è dimostrata Turing-completa da **Matthew Cook**, assistente di Wolfram, negli anni Novanta, e la dimostrazione viene pubblicata solo nel **2004** perché Wolfram ne bloccò l'uscita agli atti di un convegno del 1998.

**La formica di Langton è del 1986.** «Langton's ant»: Chris Langton, due regole, un reticolo di caselle bianche e nere. Su casella bianca si gira di novanta gradi a destra, si inverte il colore e si avanza di uno; su casella nera si gira a sinistra, si inverte e si avanza.

## Varianti e parenti

- **Automa elementare** — una riga, due stati, due vicini. Le regole possibili sono 256.
- **Gioco della vita** — due dimensioni, vicinato di Moore, sigla B3/S23.
- **Regole simili al Gioco della vita** — si cambia quali numeri di vicini fanno nascere e sopravvivere. Highlife è B36/S23.
- **Formica di Langton** — non è propriamente un automa cellulare: c'è una testina che si muove, ed è una macchina di Turing bidimensionale.
- **Automa reversibile** — ogni configurazione ha esattamente un passato. In due dimensioni, dire se una regola lo sia è indecidibile.
- **Automa probabilistico** — la regola dà probabilità invece di esiti.
- **Voce 275, emergenza** — la voce che tratta il Gioco della vita come meccanica di gioco; rimanda qui, e il rimando regge. Là interessa che dalle regole esca qualcosa che le regole non dicono; qui interessa la forma della consegna.
- **Voce 368, successione con regola dichiarata** — rimanda qui, e la differenza è la dimensione: là una regola su una fila di numeri, qui su una griglia. **Là la regola dichiarata lascia un termine e uno solo; qui non lascia niente da cercare**, e il salto fra le due voci è tutto lì.
- **Voce 64, simulare** — il verbo, con il Gioco della vita come esempio.
- **Voce 372, aritmetica in altra base** — il numero di una regola è la sua tabella letta in base due.

## Che cosa se ne sa

**Il rapporto fra la lunghezza della regola e quella di ciò che produce è il fatto centrale, e la voce 275, emergenza lo ha già misurato.** Quattro frasi per il Gioco della vita, riassunte in B3/S23. Qui si aggiunge il conto che manca: **le classi di regole elementari, rifatte invece che citate.** «Elementary cellular automaton» afferma che delle 256 regole a una dimensione **88** sono non equivalenti a meno di specchio e complemento, che **64** sono anfichirali — uguali alla propria specchiata — e che **16** coincidono con la propria specchiata complementare. Costruendo le due trasformazioni e contando: 88, 64 e 16, tutti e tre. Torna anche l'esempio della pagina, che la specchiata complementare della regola 110 sia la 193.

**Il disegno di una regola la identifica, e cinque righe bastano.** Facendo girare la regola 30 da una sola casella accesa su una fila di trentuno, e cercando poi fra tutte le 256 regole quali riproducano esattamente quelle righe: con **due** righe ne restano **16**; con **tre**, due; con **cinque**, una sola. Il motivo è che da un seme singolo le otto configurazioni del vicinato non compaiono tutte subito, e finché non sono comparse tutte la regola non è determinata. **Questo è il conto che rende la scheda possibile**, e dice anche quanto disegno stampare.

**La regola 30 è stata usata come generatore di numeri casuali, e il seguito è una smentita misurata.** «Rule 30»: Wolfram propose la colonna centrale come generatore pseudocasuale, e la usò in *Mathematica*; passa molti test standard. Poi Sipper e Tomassini, **1996**, mostrarono che sul test del chi quadro applicato a tutte le colonne si comporta male rispetto ad altri generatori basati su automi. Nel **1° ottobre 2019** Wolfram ha annunciato dei premi per chi risponda a tre domande aperte sulla regola 30. **La regola più studiata di tutte ha ancora tre domande senza risposta**, e la fonte dà prima l'affermazione forte e poi il limite.

**La formica di Langton fa tre cose in fila e la terza non è dimostrata.** «Langton's ant»: per qualche centinaio di mosse disegni semplici e spesso simmetrici; poi un'area irregolare, con una traiettoria pseudocasuale, fino a circa **diecimila passi**; poi comincia a costruire un'«autostrada», un motivo di **104 passi** che si ripete all'infinito. Tutte le configurazioni iniziali provate finora convergono a quel motivo, **e nessuno è riuscito a dimostrare che succeda sempre.** Si sa soltanto che la traiettoria è illimitata. Facendola camminare: dopo cinquecento passi il riquadro toccato è 13×13, dopo cinquemila 31×29, dopo diecimila 49×45, e a dodicimila è 87×57 — cresce in una direzione sola, che è l'autostrada che parte.

**Il Gioco della vita è Turing-completo, e la conseguenza è che non c'è niente da chiedere.** «Conway's Game of Life»: si costruiscono porte logiche con gli alianti, e da quelle un calcolatore. Per il problema della fermata, **è indecidibile se una configurazione bersaglio comparirà mai** partendo da una configurazione data. Non è che la domanda sia difficile: è che non esiste un procedimento che risponda in generale. **È il caso più netto raccolto in 374 voci di forma su cui non c'è nessuna domanda da porre**, e sta accanto alla voce 359, problema di Fermi, dove la domanda c'è e la risposta no.
**Il modo di numerare le regole è notazione posizionale, e lo dice la fonte.** «Wolfram code»: la tabella delle transizioni si legge come un numero di *k* cifre in base *S*, dove *S* è il numero di stati e *k* il numero di configurazioni del vicinato. Con due stati e tre celle di vicinato, *k* = 8 e le regole sono 2⁸ = 256. **Passando a due dimensioni con vicinato di Moore le configurazioni diventano 512 e le regole 2⁵¹², cioè circa 1,34 × 10¹⁵⁴**, che è il numero che «Cellular automaton» riporta.

## Esempi trovati

Da Conway, prima dei calcolatori: le prime configurazioni interessanti furono trovate su carta quadrettata, su lavagne e su goban da Go. «Conway's Game of Life» dice esattamente questo, ed è la riga che rende la forma stampabile.

Dalla scommessa del 1970, nella stessa pagina: cinquanta dollari a chi dimostrasse o smentisse entro fine anno che nessuna configurazione può crescere all'infinito. Vinse in novembre una squadra del MIT guidata da Bill Gosper.

Da «Cellular automaton»: le conchiglie dei generi *Conus* e *Cymbiola*, dove le cellule del pigmento stanno in una fascia stretta lungo il labbro e secernono secondo l'attività delle vicine. Il motivo del *Conus textile* somiglia alla regola 30.

Da «Cellular automaton», sezione sulla generazione di labirinti: gli automi cellulari si usano per costruire labirinti, il che collega questa forma alla voce 164, labirinto su carta.

Da Daniel Dennett, in «Conway's Game of Life»: il Gioco della vita usato per esteso come analogia filosofica, per mostrare che organizzazione e progetto possono emergere senza un progettista.

## Un esempio giocabile

> **Quale delle 256?**
>
> Una regola ha disegnato questo. Ogni casella guarda **sé stessa e le due accanto** nella riga sopra: tre caselle, e per ogni modo in cui possono stare la regola decide se la casella sotto è piena o vuota.
>
> ```
>  ...............#...............
>  ..............###..............
>  .............##..#.............
>  ............##.####............
>  ...........##..#...#...........
>  ..........##.####.###..........
>  .........##..#....#..#.........
>  ........##.####..######........
>
>  la regola e' il numero  ____
> ```
>
> I modi in cui tre caselle possono stare sono otto. Falli in colonna, da `###` a `...`, e per ognuno guarda nel disegno che cosa è venuto sotto. Ti resta una colonna di otto risposte, piene e vuote.
>
> Adesso leggi quella colonna come un numero in base due — pieno vale 1, vuoto vale 0 — e hai il nome della regola. **Poi ridisegna le otto righe partendo da una casella sola e controlla che ti venga uguale.**

Cinque righe di disegno bastano a determinare la regola fra le 256, e con due ne resterebbero sedici: il conto ha deciso quanto disegno stampare. La forma pura — «applica questa regola e guarda» — non ha niente da verificare; girata al contrario ne ha eccome, e la verifica sta dentro il materiale, perché ridisegnare le righe e confrontarle non richiede nessuna risposta scritta. **La lettura in base due è la stessa cosa della voce 372, aritmetica in altra base**, e su questa scheda le due voci si toccano.

## Che cosa la rende interessante

**È il valore estremo della scala del blocco, e per una ragione che non era ancora comparsa: non c'è niente da provare perché non c'è nessuna domanda.** Alla voce 359, problema di Fermi la domanda esisteva e la risposta no. Qui non esiste nemmeno la domanda: la griglia fa quello che fa, e chiedere se sia giusto non ha senso. **Con la voce 359, problema di Fermi fa due modi diversi di non avere una verifica**, e vanno tenuti separati.

**La mossa che salva la forma è girare la domanda al contrario, e vale in generale.** Invece di «che cosa fa questa regola», «quale regola ha fatto questo». La prima non ha risposta, la seconda ne ha una e si controlla ridisegnando. **È la stessa mossa di «trovare la base» della voce 372, aritmetica in altra base**, e adesso sono due su due: ogni volta che una forma applica una regola dichiarata e non lascia niente da cercare, nasconderla è quello che la rende una consegna.

**Il vincolo che chi propone abbia già scritto la risposta morde qui, ed è la terza volta su diciannove voci del capitolo 13.** La scheda stampata non lo tocca, perché la regola e il disegno li sceglie chi compone. Morde sulla forma pura: **far camminare la formica di Langton da una configurazione scelta da chi gioca e chiedere se comparirà l'autostrada è una domanda di cui non conosce la risposta nessuno.** Nel blocco precedente mordeva alla voce 367, gioco combinatorio imparziale per il Chomp; in quello prima alla voce 359, problema di Fermi. **Tre volte su diciannove, e tutte e tre dove una risposta non esiste per nessuno**: è un'affermazione sul capitolo intero, e adesso il capitolo è finito.

**Si può stampare una consegna dichiarando la propria ignoranza, ed è la seconda volta.** Il Chomp della voce 367, gioco combinatorio imparziale lo faceva sulla strategia. La formica lo fa sull'esito: si può scrivere «finora è successo sempre, e nessuno ha dimostrato che succeda sempre», e chi cammina sulla carta quadrettata sta guardando una domanda aperta. Costa una riga e non richiede di mentire.

**La griglia quadrettata è il supporto più economico del capitolo.** Non serve il compasso della voce 371, costruzione con riga e compasso, non servono le forbici della voce 375, topologia ricreativa, non serve la seconda persona della voce 373, paradosso probabilistico. Serve un quaderno a quadretti e una matita, e la formica di Langton ci sta dentro per diecimila passi — che sono più di quanti se ne facciano in un pomeriggio, e questa è la sola cosa da guardare.

