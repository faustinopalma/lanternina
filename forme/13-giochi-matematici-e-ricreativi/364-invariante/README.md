# Invariante

- **Numero** 364 nell'enciclopedia, capitolo 13 — Giochi matematici e ricreativi
- **Si chiama anche** invariante, invariant, quantità conservata, grandezza che non cambia, argomento di invarianza, MU puzzle, sistema MIU
- **In una riga** la stessa idea generalizzata: si cerca la quantità che resta uguale.
- **Contratto** voce breve
- **Fonti** `invariant-mathematics.txt`, `mu-puzzle.txt`, `15-puzzle.txt`, lette il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Una proprietà che le mosse ammesse non cambiano mai. `invariant-mathematics.txt` la definisce così: una proprietà di un oggetto matematico che resta immutata dopo che le si applicano operazioni o trasformazioni di un certo tipo. Come forma di problema, si consegna un sistema di regole e uno stato d'arrivo, e si chiede se ci si arrivi; la risposta si trova inventando la quantità giusta.

Le parti mobili:

- **Il sistema.** Uno stato di partenza e alcune regole di trasformazione.
- **La quantità da inventare.** È il vero compito, e non è dichiarata. La voce 363, problema di parità è il caso in cui la quantità ha due valori soli.
- **Se il traguardo è raggiungibile o no.** Se lo è, si chiede la strada; se non lo è, si chiede il motivo. La stessa pagina, due domande diverse.
- **Quante regole.** Il sistema MIU ne ha quattro, ed è il minimo perché la cosa sia interessante.

`invariant-mathematics.txt` mette il caso più semplice per primo, e vale la pena riportarlo: **contare è un invariante.** Comunque si ordinino gli oggetti di un insieme finito, il numero a cui si arriva è lo stesso. La cardinalità è invariante sotto il processo del contare.

## Da dove viene

L'idea è di tutta la matematica, e la voce dell'elenco riguarda la sua forma di gioco. Il caso canonico è il **rompicapo MU**, che Douglas Hofstadter pose in *Gödel, Escher, Bach*. Si parte dalla stringa `MI` e si vuole arrivare a `MU` usando solo queste quattro regole:

- se una stringa finisce per I, si può aggiungere U in fondo;
- quello che sta dopo la M si può raddoppiare;
- tre I di fila si possono sostituire con una U;
- due U di fila si possono togliere.

**Le regole non sono in `mu-puzzle.txt`.** La sezione «The puzzle» della pagina inglese arriva vuota nel testo estratto, perché le regole erano dentro un riquadro; sono state prese da `invariant-mathematics.txt`, che le stampa per esteso insieme a una derivazione di esempio. È la trappola nota delle figure che spariscono, e il rimedio è stato una seconda fonte in casa e non una ricostruzione.

Il motivo per cui Hofstadter lo pone, secondo `mu-puzzle.txt`, non è il gioco: è mettere a confronto il ragionare **dentro** un sistema formale — derivare teoremi — con il ragionare **sul** sistema. Chi resta dentro può provare regole per ore; chi esce vede in un minuto che è impossibile.

## Varianti e parenti

- **Monovariante** — una quantità che non resta uguale ma può solo crescere, o solo calare. Serve a dimostrare che un processo finisce. **Non ha una pagina su Wikipedia in inglese**, controllato il 1 settembre 2026 con `build/check_titoli_359.py`.
- **Insieme invariante** — un sottoinsieme che una trasformazione manda in sé stesso.
- **Punto fisso** — l'elemento che la trasformazione lascia dov'è.
- **Voce 363, problema di parità** — il caso in cui l'invariante è pari o dispari, e la voce accanto.
- **Voce 145, enigma di travaso** — quello che non cambia versando è il massimo comune divisore delle capacità, e per questo certe quantità non si ottengono.
- **Voce 174, puzzle idraulico** e **voce 172, cubo di Rubik e combinatori** — due forme di pagina il cui «non si può» è un invariante.
- **Voce 171, puzzle a scorrimento (15, Sokoban)** — l'invariante di Johnson e Story, che è la parità di una permutazione sommata a quella di una distanza.

## Che cosa se ne sa

**L'invariante del rompicapo MU, e la sua verifica per esaurimento.** La quantità è il numero di I nella stringa, e la proprietà è che **non è mai un multiplo di tre**. All'inizio è 1; il raddoppio non fa diventare multiplo di tre ciò che non lo è; togliere tre non lo fa diventare. `MU` ha zero I, e zero è multiplo di tre. In `build/check_359.py` si generano tutte le stringhe raggiungibili da `MI` con un tetto di 19 caratteri: sono **13 265 stringhe**, `MU` non c'è, e nessuna ha un numero di I multiplo di tre.

**Il criterio decidibile della fonte regge, controllato.** `mu-puzzle.txt` afferma che una stringa è derivabile da `MI` se e solo se è fatta di una sola M seguita da I e U, comincia per M, e il numero di I non è multiplo di tre. Delle 340 stringhe fino a nove caratteri che il criterio dichiara derivabili, **si raggiungono tutte e 340** — passando, per alcune, da stringhe più lunghe di nove caratteri. La condizione non è solo necessaria: è anche sufficiente.

**L'invariante può essere la somma di due quantità che cambiano tutte e due.** È il caso del gioco del quindici: `15-puzzle.txt` scrive che ogni mossa cambia sia la parità della permutazione sia la parità della distanza del vuoto dall'angolo, e per questo la loro somma resta. Nessuna delle due, da sola, è invariante. Wilson nel 1974 ha generalizzato il gioco a un grafo qualsiasi e ha trovato che, salvo un grafo eccezionale su sette vertici, si ottengono tutte le permutazioni **a meno che il grafo sia bipartito**, e in quel caso esattamente le pari.

**Una quantità invariante descrive uno spazio infinito con una riga.** Le stringhe del sistema MIU sono infinite, e la condizione «il numero di I non è multiplo di tre» le classifica tutte. È il caso limite dello spazio di ricerca stampabile per intero: non si stampa l'elenco, si stampa la regola che lo genera.

**Dove sta la verifica: dentro l'argomento.** Come per la voce 363, problema di parità, e per lo stesso motivo. La differenza è che là l'invariante lo regala il foglio — basta colorare la scacchiera —, qui va inventato.

## Esempi trovati

Da `invariant-mathematics.txt` e `mu-puzzle.txt`: il rompicapo MU, con la derivazione `MI → MII → MIIII → MUI → MUIUI → MUIUIU → …` che la prima pagina stampa per mostrare come ci si perde.

Da `invariant-mathematics.txt`: la somma degli angoli interni di un triangolo, che vale 180° e non cambia sotto rotazioni, traslazioni, riflessioni e cambi di scala; e il rapporto fra circonferenza e diametro, che è invariante perché tutti i cerchi sono simili.

Da `invariant-mathematics.txt`: la tricolorabilità dei nodi, che è quello che permette di dire che due nodi sono diversi.

Da `15-puzzle.txt`: l'invariante di Johnson e Story, 1879, e la sua conseguenza — metà delle posizioni sono irraggiungibili.

Da `invariant-mathematics.txt`: contare. Il numero a cui si arriva non dipende dall'ordine in cui si contano le cose.

## Una nostra versione

> **Il barattolo dei fagioli**
>
> Nel barattolo ci sono sette fagioli bianchi e cinque neri. Si tolgono due fagioli a caso e si guarda:
>
> ```
>  esci con         rientra    bianchi  neri
>  bianco e bianco  un nero         -2    +1
>  nero e nero      un nero          0    -1
>  bianco e nero    un bianco        0    -1
> ```
>
> Ogni volta i fagioli nel barattolo calano di uno. Alla fine ne resta uno solo.
>
> **Prima di cominciare, scrivi qui di che colore sarà: ......**
>
> Poi giocaci davvero, mescolando bene, e guarda se avevi ragione. Poi rifallo con sei bianchi.

Bastano dodici fagioli e un barattolo, e la scheda non deve sapere quali fagioli usciranno. La colonna dei bianchi dice tutto: cambia di due o di zero, mai di uno, quindi **la parità dei bianchi non cambia mai** — e l'ultimo fagiolo è bianco se all'inizio i bianchi erano dispari, nero se erano pari. Verificato in `build/check_359.py` giocando ogni partenza fino alla fine: su **156 partenze** l'esito segue sempre la parità, senza eccezioni. La domanda con sei bianchi è il controllo: cambia la risposta, e chi ha capito lo sa prima di giocare.

## Da riprendere alla rassegna

**È il gradino più alto della scala del blocco, ed è anche l'unico oggetto del blocco che non è di carta.** Il barattolo con i fagioli è una macchina fisica che si comporta come un teorema; il foglio serve solo a dire le regole e a raccogliere la previsione. **Una scheda che chiede una previsione e poi manda a controllarla nel mondo mette la verifica fuori dalla casa senza che nessuno debba correggere niente.**

**Chiedere di scrivere la previsione prima di giocare è la mossa, e costa una riga.** Senza quella riga il gioco è un passatempo; con quella riga è un esperimento, e chi sbaglia impara qualcosa. Vale per ogni forma dell'enciclopedia in cui succede qualcosa di osservabile.

**L'invariante è la sesta e più economica forma di «spazio di ricerca stampabile per intero».** Alla voce 351, frase bipartita erano cinque posizioni, alla voce 358, zigzag, kakuro, crossnumber trentaquattro coppie; qui lo spazio è infinito e la riga che lo descrive è una sola. Il modo in cui una forma comprime il suo spazio è una grandezza che alla rassegna conviene misurare da sola.

**Il capitolo 13 non ha ancora incontrato il muro del capitolo 12.** Il sistema non sa contare le lettere dentro le parole e non deve chiedere qualcosa di cui non abbia scritto la risposta. In queste sei voci il muro morde una volta sola — alla voce 359, problema di Fermi, che non ha una risposta —, e in tutte le altre cinque non morde affatto, perché sono forme che si compongono a partire dalla risposta. È la differenza fra un capitolo che gioca con le parole e uno che gioca con le regole, e alla rassegna cambia il peso dei due.

