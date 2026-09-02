# Problema di grafi

- **Numero** 366 nell'enciclopedia, capitolo 13 — Giochi matematici e ricreativi
- **Si chiama anche** problema di rete, punti e collegamenti, teoria dei grafi, cammino euleriano, circuito euleriano, giro del cavallo, commesso viaggiatore, *graph problem*, *Eulerian path*, *knight's tour*, *travelling salesman*
- **In una riga** i ponti di Königsberg, il commesso viaggiatore, il giro del cavallo.
- **Fonti** [Seven Bridges of Königsberg](https://en.wikipedia.org/wiki/Seven_Bridges_of_K%C3%B6nigsberg), [Problema dei ponti di Königsberg](https://it.wikipedia.org/wiki/Problema_dei_ponti_di_K%C3%B6nigsberg), [Eulerian path](https://en.wikipedia.org/wiki/Eulerian_path), [Graph theory](https://en.wikipedia.org/wiki/Graph_theory), [Teoria dei grafi](https://it.wikipedia.org/wiki/Teoria_dei_grafi), [Handshaking lemma](https://en.wikipedia.org/wiki/Handshaking_lemma), [Knight's tour](https://en.wikipedia.org/wiki/Knight%27s_tour), [Travelling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem), lette il 2 settembre 2026

## Che cos'è

Si butta via tutto tranne che cosa è collegato a che cosa. Restano dei punti e dei tratti fra i punti, e la domanda si fa su quelli: si può percorrere ogni tratto una volta sola, si può toccare ogni punto una volta sola, qual è il giro più corto.

Le parti mobili:

- **Che cosa si chiede di percorrere.** I collegamenti tutti una volta — è il cammino euleriano — oppure i punti tutti una volta — è il cammino hamiltoniano. Sembrano la stessa domanda scambiata di posto, e non lo sono affatto: la prima si decide contando, la seconda no.
- **Se la risposta è sì o no, oppure un numero.** «Si può?» ha due risposte. «Qual è il più corto?» ne ha tante quante sono i giri.
- **Se il disegno è dato o va fatto.** Il salto vero è la prima volta: guardare una città e vederci quattro punti e sette tratti.
- **Quanto è grande.** Sette ponti si provano a mano; otto capanni no.

**Questa è la voce del blocco in cui la scala del blocco si vede tutta intera.** Dove stia la prova che si è finito, in questa forma, dipende da quale delle domande si fa sullo stesso disegno: nell'argomento per i ponti, nel materiale per il giro del cavallo, in una macchina per i quattro colori, e da nessuna parte per il commesso viaggiatore. Le altre cinque voci del blocco si descrivono per differenza da questa, e la riga di differenza sta in fondo a ognuna.

## Da dove viene

**I sette ponti di Königsberg, 1736.** «Seven Bridges of Königsberg» e «Problema dei ponti di Königsberg»: la città prussiana stava sui due lati del Pregel e comprendeva due isole, unite fra loro e alle rive da sette ponti; si chiedeva una passeggiata che li attraversasse tutti una volta sola. Euler dimostrò che non esiste. La memoria fu presentata all'Accademia di San Pietroburgo il **26 agosto 1735** e pubblicata nel **1741** come *Solutio problematis ad geometriam situs pertinentis*. «Graph theory» e «Teoria dei grafi» concordano nel farne il primo testo della disciplina; la pagina italiana aggiunge che è anche il primo problema di geometria topologica, «che non dipende da alcuna misurazione».

Lo stesso scritto contiene il **lemma delle strette di mano**, che «Handshaking lemma» attribuisce a Euler nello stesso 1736: la somma dei gradi di tutti i punti vale il doppio del numero dei collegamenti, e quindi i punti di grado dispari sono sempre in numero pari. Che la condizione di Euler fosse anche sufficiente lo dimostrò **Carl Hierholzer**, pubblicato postumo nel **1873** («Eulerian path»).

**Il giro del cavallo è molto più vecchio, e non nasce come matematica.** «Knight's tour» fa risalire il primo riferimento noto al **IX secolo**, nel *Kavyalankara* di Rudrata, un'opera sanscrita di poetica: il percorso del cavallo su mezza scacchiera è lì una figura retorica, e i quattro versi di otto sillabe si leggono sia da sinistra a destra sia seguendo i salti. Nel XIV secolo Vedanta Desika compone due strofe di trentadue sillabe di cui la seconda si ottiene dalla prima con un giro del cavallo su una scacchiera 4×8. Euler ci arriva nel **1759**; la prima ricetta pratica è la regola di Warnsdorff, **1823**.

**Il commesso viaggiatore è il più giovane e il più applicato.** «Travelling salesman problem»: un manuale per commessi del **1832** lo enuncia con esempi di giri per Germania e Svizzera, senza matematica; la formulazione moderna è degli anni Trenta, e nel **1954** Dantzig, Fulkerson e Johnson risolvono all'ottimo un'istanza di **49 città** con i piani di taglio. Nel 1972 Karp dimostra che il problema del ciclo hamiltoniano è NP-completo, e da lì la difficoltà ha una spiegazione. Il record d'istanza risolta esattamente è del **2006**: 85 900 città, da un disegno di microchip.

## Varianti e parenti

- **Cammino euleriano** — ogni collegamento una volta. Esiste se e solo se il grafo è connesso e i punti di grado dispari sono zero o due.
- **Cammino hamiltoniano** — ogni punto una volta. Non c'è nessun criterio che si legga contando.
- **Giro del cavallo** — un cammino hamiltoniano sul grafo dei salti del cavallo; chiuso, se l'ultima casella è a un salto dalla prima.
- **Commesso viaggiatore** — il giro chiuso più corto per tutti i punti.
- **Quattro colori** — colorare le regioni di una mappa, che è un problema di grafi travestito da disegno.
- **Voce 152, problema impossibile** — la forma di pagina dei ponti: là il compito è accorgersi che non si può. **Quella voce dichiara che la divisione fra i due capitoli è «una comodità di elenco», da riguardare quando il capitolo 13 sarà scritto.** È rimasta vera e il confine regge: là si consegna un compito che si scopre impossibile provandolo, qui si consegna un disegno e si chiede una proprietà del disegno. Quello che va corretto è un dettaglio: quella scheda dice che i ponti «hanno fondato la teoria dei grafi», e le due pagine lette adesso dicono qualcosa di più preciso, cioè che sono il primo testo che tratta i grafi come oggetti matematici.
- **Voce 153, problema di ottimizzazione** — rimanda qui per il commesso viaggiatore, e il rimando regge: là sta come forma di pagina, «si consegna un disegno e si chiede un numero che diminuisce», qui sta come contenuto.
- **Voce 164, labirinto su carta** — rimanda qui perché un labirinto perfetto è un albero. Regge.
- **Voce 165, labirinto logico** — un labirinto multi-stato è un grafo i cui punti sono coppie casella-più-stato.
- **Voce 156, problema di scacchi** — dove sta il giro del cavallo come forma di pagina.
- **Voce 143, enigma di attraversamento** — la storia della barca è un grafo, ma là il grafo è un modo di guardare e non l'oggetto.
- **Voce 363, problema di parità** — l'argomento che chiude il giro del cavallo su una scacchiera con un numero dispari di caselle.

## Che cosa se ne sa

**La dimostrazione dei ponti si può rifare per esaurimento, e il conto è piccolo.** Provando tutti i **20 160** ordini dei sette ponti a partire da ognuna delle quattro zone, le passeggiate valide sono **zero**. Le due strade concordano: i gradi sono 3, 3, 3 e 5, quindi quattro punti dispari, e il criterio ne ammette al massimo due. Sui cinque ponti rimasti oggi, che «Seven Bridges of Königsberg» elenca, la stessa enumerazione trova **12 passeggiate**: il problema è stato risolto dalla guerra e dall'urbanistica.

**Il giro del cavallo su una scacchiera qualunque: il teorema di Schwenk, rifatto invece che citato.** «Knight's tour» dice che su una scacchiera *m*×*n* con *m* ≤ *n* un giro chiuso esiste sempre tranne in tre casi — i due lati tutti e due dispari, il lato minore uguale a 1, 2 o 4, oppure il lato minore 3 con l'altro uguale a 4, 6 o 8. Verificato su tutte le scacchiere fino a 6×6: venti fallimenti provati per esaurimento e un giro trovato dove il teorema dice che c'è. La 6×6 resta fuori dal conto perché la ricerca non finisce in tempo utile, ed è la prima riga di questa voce che dichiara un limite dello strumento invece che della fonte.

**La stessa pagina dà lo stesso numero due volte con due nomi diversi.** «Knight's tour» scrive che su 8×8 i giri chiusi orientati sono **26 534 728 821 064** e che quelli non orientati sono la metà; poche righe più sotto, parlando della forza bruta, scrive che «ci sono 13 267 364 410 532 giri del cavallo». La seconda cifra è esattamente la metà della prima — verificato — quindi non è il numero dei giri del cavallo, è il numero dei giri **chiusi non orientati**. È lo stesso genere di scivolone già visto sui quadrati magici: il numero è giusto e il suo statuto no. La stessa pagina registra anche che un conteggio pubblicato, 33 439 123 484 294, fu poi corretto da Brendan McKay nel 1997.

**Le persone sono brave al commesso viaggiatore, e c'è la misura.** «Travelling salesman problem»: gli esseri umani producono soluzioni quasi ottime in fretta, e con uno scarto che va dall'**1% su grafi di 10-20 punti all'11% su grafi di 120**. Le due ipotesi correnti sono che si usi il contorno convesso o che si eviti di far incrociare i tratti. La stessa pagina avverte che i risultati individuali variano molto e che la geometria del grafo conta. **È l'unica misura di prestazione umana trovata in tutto il capitolo**, e dice che questa forma è alla portata di chi la riceve.

**Sui nostri otto capanni la ricerca a occhio funziona, e il conto lo mostra.** Enumerando tutti i **2 520** giri chiusi si trova il più corto a **42 passi**, per due strade indipendenti — le permutazioni e la programmazione dinamica sui sottoinsiemi, che concordano. La ricetta del vicino più vicino, che è quella che viene in mente per prima, dà fra 42 e 50 passi secondo il capanno da cui si comincia: **dal migliore punto di partenza trova l'ottimo, dal peggiore sbaglia del 19%.** Non è la ricetta a essere buona o cattiva: è la partenza.

**Dove sta la prova che si è finito: dipende dalla domanda, e sullo stesso disegno prende quattro valori diversi.** Per i ponti sta **nell'argomento**: si contano i ponti di ogni zona e si è finito. Per il giro del cavallo sta **nel materiale**: si ripercorre il giro e si guarda se le caselle sono tutte segnate. Per il commesso viaggiatore **non sta da nessuna parte**: si può misurare un giro, non si può sapere che sia il più corto senza guardarli tutti. E per i quattro colori sta **in una macchina**: «Graph theory» racconta che la dimostrazione del 1976 di Appel e Haken controllò al calcolatore **1 936 configurazioni** e per questo non fu accettata subito; vent'anni dopo Robertson, Sanders, Seymour e Thomas la rifecero con **633**. Nessuna delle due si rilegge a mano. **È il quinto posto in cui la verifica può stare, e le quattro classi del censimento non lo prevedevano.**

## Esempi trovati

Da Königsberg: quattro zone, sette ponti, nessun percorso.

Da Bristol, «Seven Bridges of Königsberg»: due rive e due isole come a Königsberg, ma i 45 ponti principali sono disposti in modo che il circuito euleriano esista. È diventato una passeggiata di beneficenza con un libro e la copertura dei giornali. **La stessa forma di problema, con la risposta opposta, produce un'attività di città.**

Da «Knight's tour»: i due versi sanscriti di Vedanta Desika, dove il secondo si ottiene dal primo con un giro del cavallo. E i capitoli di *La vita istruzioni per l'uso* di Georges Perec, che seguono un giro del cavallo su una scacchiera 10×10.

Da «Travelling salesman problem»: i piccioni di un esperimento del 2011 volano fra le mangiatoie scegliendo quasi sempre la più vicina, ma pianificano qualche passo avanti quando la differenza di costo diventa grande. E il *Physarum polycephalum*, che è una muffa, cambia forma fino a collegare le fonti di cibo con un percorso quasi ottimo.

Dal manuale per commessi viaggiatori del 1832: il problema enunciato per intero, con gli itinerari, e nessuna matematica.

## Un esempio giocabile

Due domande sullo stesso genere di disegno, in quest'ordine, perché la seconda si capisce solo dopo la prima.

> **Il giro del guardiano**
>
> **Prima parte.** Un parco con quattro zone — le due rive di un canale e due isolette — e sette ponti, messi così:
>
> ```
>   I SETTE PONTI
>
>  riva di qua   -  isola grande   due ponti
>  riva di qua   -  isola piccola  un ponte
>  riva di la'   -  isola grande   due ponti
>  riva di la'   -  isola piccola  un ponte
>  isola grande  -  isola piccola  un ponte
>
>   QUANTI NE TOCCA OGNI ZONA
>
>  riva di qua    ....
>  riva di la'    ....
>  isola grande   ....
>  isola piccola  ....
> ```
>
> Il guardiano vorrebbe passare su ogni ponte **una volta sola** e finire il giro. Provaci: scrivi l'ordine dei ponti. Poi riempi il secondo riquadro, e guarda i quattro numeri.
>
> Se una zona non è né la prima né l'ultima del giro, ogni volta che ci entri da un ponte devi uscirne da un altro. **Quindi i suoi ponti vanno a coppie.** Adesso rileggi i quattro numeri.
>
> ---
>
> **Seconda parte.** Nel parco ci sono otto capanni. Si cammina solo lungo i vialetti, che vanno dritti in orizzontale e in verticale, e un passo è un quadretto.
>
> ```
>   .  .  .  .  .  .  .  .  .  E
>   .  .  .  .  F  .  .  .  .  .
>   G  .  .  .  .  .  .  .  .  .
>   .  .  .  .  .  .  .  .  .  .
>   .  .  .  .  .  .  .  .  .  .
>   .  .  H  .  .  .  .  .  .  C
>   .  .  .  .  .  D  .  .  .  .
>   .  .  .  .  .  .  .  .  .  .
>   .  .  .  .  .  .  .  .  .  .
>   A  .  .  .  .  .  B  .  .  .
> ```
>
> Parti da A, passa da tutti e otto, torna ad A. **Scrivi il giro e conta i passi.**
>
> ```
>  giro:   A ── ── ── ── ── ── ── ── A     passi: ......
>  giro:   A ── ── ── ── ── ── ── ── A     passi: ......
>  giro:   A ── ── ── ── ── ── ── ── A     passi: ......
> ```
>
> Sotto i 50 si fa. Sotto i 45 si fa. **Sotto i 42 nessuno ci riesce, e non ti dico perché.**

La prima parte è chiusa da un argomento che chi legge costruisce riempendo quattro caselle: la risposta non è stampata da nessuna parte e non serve. La seconda non è chiusa da niente — i giri sono 2 520 e provarli tutti non è un compito da pomeriggio —, e la riga finale è l'unica onestà possibile: dice il valore del minimo senza dire che è il minimo, così quello che si può verificare resta verificabile e quello che non si può resta fuori.

## Che cosa la rende interessante

**Il salto della forma è buttare via il disegno.** Le zone diventano punti, i ponti tratti, e la forma del fiume non conta più. «Problema dei ponti di Königsberg» dice che il confronto fra la mappa e il grafo «costituisce una buona indicazione dell'idea che la topologia prescinda dalla forma rigida degli oggetti». Per una casa che stampa fogli è un'operazione economica: la stessa domanda si consegna come mappa disegnata o come elenco di collegamenti, e il secondo formato non ha bisogno di un disegnatore.

**Una forma sola porta quattro posti diversi in cui può stare la verifica, e il posto lo sceglie la domanda, non il disegno.** Questo è il pezzo da tenere: la scelta fra «si può?» e «qual è il più corto?» non è una scelta di difficoltà, è una scelta di che cosa si può controllare.

**Una misura di prestazione umana esiste, ed è dalla parte giusta.** L'1% di scarto su venti punti dice che questa forma non chiede di essere bravi in matematica: chiede di guardare. È la sola voce del capitolo per cui una fonte dica quanto bene se la cavi chi la riceve.

**Il termine di paragone del blocco è questa voce, e la ragione è nuova.** Le tredici volte precedenti il termine di paragone era la voce in cui la variabile prendeva il valore più povero; qui è la voce che contiene la scala intera. Le altre cinque si descrivono per differenza da questa, ognuna dichiarando quale dei quattro posti occupa.
