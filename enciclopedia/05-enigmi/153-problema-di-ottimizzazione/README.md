# Problema di ottimizzazione

- **Numero** 153 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi logici»
- **Si chiama anche** il problema del commesso viaggiatore, il giro più corto, il cammino minimo, problema del postino, *travelling salesman problem*, *TSP*, *shortest path*, e in Menger *Botenproblem*, problema del messaggero
- **In una riga** il percorso più corto.
- **Fonti** [Travelling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem) e [Shortest path problem](https://en.wikipedia.org/wiki/Shortest_path_problem), prese il 30 agosto 2026 da en.wikipedia; il conto sui 181 440 giri non viene dalle fonti

## Che cos'è

Un compito in cui tutte le risposte sono valide e alcune sono migliori. Non si cerca la soluzione: si cerca **la soluzione migliore fra quelle che funzionano tutte.**

Questa voce sta da sola nel capitolo, e la ragione è il verbo. Ovunque altrove — negli enigmi, nei paradossi, nelle griglie — c'è una risposta e le altre sono sbagliate. Alla voce 152, problema impossibile non ce n'è nessuna. **Qui ce ne sono migliaia, sono tutte giuste, e si confrontano.** Chi consegna un giro qualunque ha risolto il problema; chi ne consegna uno più corto lo ha risolto meglio. Non è una differenza di grado: è un altro tipo di compito, e in tutto l'elenco delle 395 forme è quasi l'unico.

Parti mobili:

- **Che cosa si minimizza.** La lunghezza, il tempo, il numero di mosse, il costo, il numero di fogli. Deve essere una cosa sola, e va dichiarata.
- **Che cosa vincola.** Passare per tutti i punti; passare una volta sola; tornare al punto di partenza. Togliere uno di questi vincoli cambia il problema.
- **Se si sa quando si è finito.** È la parte mobile che decide tutto. Nella maggior parte dei casi **non si sa**: si ha un giro corto e non si ha nessun modo di sapere se ce ne sia uno più corto.
- **Quante soluzioni ci sono.** Un numero enorme e calcolabile — ed è calcolabile anche da chi risolve, il che rende la cosa interessante invece che frustrante.
- **Se c'è una regola che dà subito una risposta decente.** Quasi sempre sì, e quasi mai è la migliore.

## Da dove viene

Le origini, dice la fonte, non sono chiare. Un manuale per commessi viaggiatori del **1832** nomina il problema e dà esempi di giri per la Germania e la Svizzera, senza nessuna trattazione matematica.

La formulazione matematica arriva nell'Ottocento con **William Rowan Hamilton** e **Thomas Kirkman**; il gioco *icosian* di Hamilton era un rompicapo da tavolo basato sul trovare un ciclo hamiltoniano. La forma generale è studiata negli anni Trenta a Vienna e a Harvard, e **Karl Menger** la definisce con un nome che vale la pena tenere — *Botenproblem*, il problema del messaggero, «perché in pratica questa domanda dovrebbe essere risolta da ogni postino». Menger scrive anche, nello stesso passo, le due cose che contano ancora:

> «Naturalmente il problema è risolubile con un numero finito di prove. Regole che spingano il numero delle prove al di sotto del numero delle permutazioni dei punti dati non sono note. La regola per cui si dovrebbe andare prima dal punto di partenza al punto più vicino, poi al punto più vicino a questo, eccetera, in generale non dà il percorso più corto.»

Il nome moderno è del **1949**, in un rapporto della RAND Corporation di Julia Robinson, *On the Hamiltonian game (a traveling salesman problem)*. Prima ancora, **Merrill M. Flood** ci lavora negli anni Trenta cercando di risolvere un problema di percorsi di scuolabus, e Hassler Whitney a Princeton lo chiama «il problema dei 48 stati».

Il risultato che apre l'epoca moderna è di **Dantzig, Fulkerson e Johnson** alla RAND: esprimono il problema come programma lineare intero, inventano il metodo dei piani di taglio e **risolvono un'istanza da 49 città all'ottimo**, cioè costruiscono un giro e dimostrano che nessun altro può essere più corto. Gli bastarono 26 tagli, e usarono un modello fatto di spago.

## Varianti e parenti

- **Il cammino minimo fra due punti** — la versione facile: non bisogna passare per tutti.
- **Il problema del postino** — bisogna percorrere tutte le strade invece di visitare tutti i punti. È il rovescio esatto, e sta vicino alla voce 152, problema impossibile.
- **Il problema del compratore viaggiatore**, il **problema dei veicoli**, il **ring star** — tre generalizzazioni che la fonte elenca.
- **La versione decisionale** — invece di «qual è il più corto», «esiste un giro lungo al massimo *L*?». La fonte segnala che questa è NP-completa mentre l'originale è NP-difficile: **cambiare la domanda cambia la classe del problema**, e la domanda più modesta è quella più trattabile.
- **La prelevazione in magazzino** — i percorsi di chi raccoglie gli ordini sono modellati come varianti di questo problema. È l'applicazione più concreta e la meno raccontata.
- **Voce 377, problema di ottimizzazione con vincoli fisici** — il vicino nel capitolo 13, giochi matematici e ricreativi, e il confine è lo spago: là il percorso più breve si ottiene con un oggetto teso invece che con un conto. Curiosamente, Dantzig, Fulkerson e Johnson usarono proprio uno spago, quindi il confine è meno netto di come lo pone l'elenco.
- **Voce 366, problema di grafi** — nello stesso capitolo 13, ed è dove il commesso viaggiatore sta come contenuto matematico. Qui sta come forma di pagina: **si consegna un disegno e si chiede un numero che diminuisce.**
- **Voce 89, sfida contro sé stessi** — la struttura di consegna più vicina fuori da questo capitolo.
- **Voce 70, decidere** — il verbo, quando i criteri sono più di uno.
- **Voce 56, ordinare** — il verbo, quando quello che si cerca è una sequenza.

Con il capitolo 12, giochi di parole e enigmistica italiana non c'è nessun contatto: non ci sono lettere, non c'è lingua, e nessun gioco enigmistico corrisponde.

## Che cosa se ne sa

**Le persone sono brave a questo problema, e c'è la misura.** La fonte lo riporta per la variante euclidea, cioè punti su un piano: gli esseri umani producono soluzioni quasi ottime **in fretta e in modo quasi lineare**, con prestazioni che vanno da **l'1% peggio dell'ottimo per grafi da 10-20 nodi all'11% peggio per grafi da 120 nodi.** È il dato più utile di tutta la voce: **con dieci punti, quello che uno disegna a occhio è a un centesimo dal meglio possibile.** Il primo numero della *Journal of Problem Solving* era dedicato a questo, e una ricognizione del 2011 elencava decine di articoli.

**Come lo facciano non si sa, e le due ipotesi principali sono utilizzabili.** La fonte le nomina: l'**ipotesi dell'involucro convesso** — si parte dal contorno esterno dei punti — e l'**euristica dell'evitare gli incroci**. La seconda è quella che si può usare su un foglio, perché **si può controllare guardando**: se due tratti del giro si incrociano, si possono sempre scambiare e accorciare. Non serve nessun conto.

**La fonte avverte anche di non generalizzare.** «Ulteriori prove suggeriscono che le prestazioni umane sono piuttosto variabili, e che sia le differenze individuali sia la geometria del grafo sembrano influenzare i risultati.» La media dell'1% non descrive nessuna persona in particolare.

**Non sono solo le persone.** Il *Physarum polycephalum*, un ameboide, posto davanti a una configurazione di fonti di cibo adatta la propria forma fino a creare un cammino efficiente fra di esse, che è una soluzione approssimata dello stesso problema. Api e bombi fanno lo stesso raccogliendo nettare. E uno studio del 2011 sui piccioni — intitolato *Let the Pigeon Drive the Bus*, dal libro per bambini — mostra che i piccioni scelgono in gran parte in base alla vicinanza, **ma sanno pianificare qualche tappa in avanti quando la differenza di costo fra il percorso efficiente e quello per vicinanza diventa grande.**

**La regola facile non funziona, e lo si sapeva negli anni Trenta.** Andare sempre al punto più vicino non dà il percorso più corto: lo dice Menger nella stessa pagina in cui definisce il problema. È una regola che si applica senza pensare, dà una risposta valida in mezzo minuto, ed è quasi sempre battibile. **Come apertura di una consegna è perfetta proprio per questo.**

**Il problema è difficile per le macchine in un senso preciso, e questa è una delle poche forme del capitolo in cui la difficoltà non pesa.** È NP-difficile: il tempo di calcolo nel caso peggiore può crescere più che polinomialmente. Ma le euristiche sono buone: istanze con decine di migliaia di città si risolvono all'ottimo, e con milioni di città si approssima entro una piccola frazione dell'1%. **La differenza rispetto al puzzle della zebra e alla scacchiera mutilata è che qui non serve una risposta esatta**, e una risposta approssimata è una risposta legittima.

**Non c'è nessuna misura, nelle pagine lette, di che effetto faccia consegnare un compito senza risposta giusta.** È la domanda che questa voce lascia aperta, e riguarda tutto il capitolo 3.

## Esempi trovati

Dal manuale del 1832 per commessi viaggiatori: giri di esempio per la Germania e la Svizzera, senza matematica.

Da Dantzig, Fulkerson e Johnson, RAND: 49 città risolte all'ottimo, con 26 tagli e un modello di spago.

Da Beardwood, Halton e Hammersley, *The Shortest Path Through Many Points*, 1959, sugli atti della Cambridge Philosophical Society: una formula asintotica per la lunghezza del giro più corto.

Dal gioco *icosian* di Hamilton: un rompicapo da salotto che chiedeva un ciclo hamiltoniano.

Da TSPLIB: la raccolta di istanze di riferimento, molte delle quali sono **elenchi di città vere e disposizioni di circuiti stampati veri.**

Dall'astronomia: chi osserva molte sorgenti vuole minimizzare il tempo di spostamento del telescopio.

Dal sequenziamento del DNA: le «città» sono frammenti e la «distanza» è una misura di somiglianza.

## Un esempio giocabile

Il foglio deve dare tre cose: una risposta valida subito, un modo di misurarla, e un motivo per non fermarsi. Nessuna delle tre richiede che qualcuno sappia la risposta migliore — e nessuno la sa.

> **Il giro più corto**
>
> Dieci posti da visitare. Devi passare per tutti e dieci una volta sola e tornare da dove sei partito.
>
> ```
>  ┌──────────────────────────────────────────┐
>  │                                          │
>  │      A                        B          │
>  │                                          │
>  │                   C                      │
>  │   D                                      │
>  │                             E            │
>  │                                          │
>  │         F              G                 │
>  │                                          │
>  │   H                              I       │
>  │                J                         │
>  │                                          │
>  └──────────────────────────────────────────┘
> ```
>
> **Primo giro: senza pensarci.** Parti da A e applica questa regola, che non richiede nessuna decisione:
>
> ```
>  vai sempre al punto piu' vicino
>  fra quelli in cui non sei ancora stato.
> ```
>
> Alla fine torna ad A. Traccia il giro con la matita, poi misuralo con un righello, tratto per tratto, e somma.
>
> ```
>  giro 1, in ordine:  A ── ── ── ── ── ── ── ── ── ── A
>  lunghezza:  ──────── mm
> ```
>
> **Secondo giro: fallo più corto.** Ricopia i dieci punti su un foglio bianco e prova un'altra strada.
>
> ```
>  giro 2, in ordine:  ── ── ── ── ── ── ── ── ── ── ──
>  lunghezza:  ──────── mm
> ```
>
> **Una cosa da controllare, e vale per qualunque giro.** Guarda se **due tratti del tuo giro si incrociano.** Se si incrociano, c'è sempre un modo di scambiarli che accorcia il giro. Trovali, scambiali, rimisura.
>
> ```
>  giro 3, in ordine:  ── ── ── ── ── ── ── ── ── ── ──
>  lunghezza:  ──────── mm
> ```
>
> ---
>
> **Adesso la domanda vera, e non ha una risposta breve.**
>
> ```
>  Come fai a sapere che non ce n'e' uno piu' corto?
> ```
>
> Un modo ci sarebbe: provarli tutti. I giri diversi che passano per dieci punti sono **centottantunomilaquattrocentoquaranta**. A uno al secondo, senza mai fermarsi, sono **cinquanta ore.**
>
> Quindi no: non lo sai, e non lo saprai. **Quello che hai è un numero che è diminuito tre volte, e il numero è vero.**
>
> ---
>
> Se vuoi, l'ultimo pezzo: dai una copia dei dieci punti a qualcun altro in casa, senza dirgli il tuo numero, e confrontate dopo. Non è una gara: è che due persone che partono dallo stesso disegno arrivano a due giri diversi, e questo è il fatto interessante.

**I conti sono stati fatti a mano.** I giri distinti che toccano dieci punti e tornano al punto di partenza sono (10−1)!/2, perché il punto di partenza si può fissare e il giro percorso al contrario è lo stesso giro: 9! fa 362 880, e diviso due fa **181 440**. A uno al secondo sono 181 440 secondi, cioè 3 024 minuti, cioè **50,4 ore**. Nessuno dei due numeri viene da una fonte: sono qui perché si possono rifare.

La regola stampata all'inizio è la mossa che tiene in piedi il foglio. **Dà una risposta valida a chi non sa da dove cominciare, non richiede nessuna decisione, e si applica in due minuti** — e siccome Menger sapeva già negli anni Trenta che non dà il percorso più corto, il primo numero è quasi sempre battibile. È la stessa cosa già osservata alla voce 21, lettera per la prima frase stampata, e qui il piolo basso è una regola invece che una frase.

Il controllo degli incroci è un controllo dell'errore nel materiale, e si vede a occhio: **se due tratti si incrociano il giro non è ottimo, e non serve nessun conto e nessuno che lo dica.** Non dimostra che il giro sia il migliore — non lo dimostra niente — ma dimostra che non lo è, e questo è tutto quello che serve per continuare.

Il numero 181 440 non è messo per impressionare: è la ragione per cui la domanda «come fai a sapere» ha «non lo sai» come risposta corretta. **Il foglio consegna un'impossibilità pratica invece di una frustrazione**, ed è la stessa differenza già vista fra la voce 151, paradosso e la voce 152, problema impossibile.

Su un pannello di poche righe corte la disposizione dei dieci punti non ci sta, e questa è una forma da foglio senza rimedio. Ci starebbe una cosa sola, ed è il numero: «il tuo giro più corto finora: 412 mm».

Il limite tecnico da dichiarare è che **chi stampa il foglio non può certificare l'ottimo** della configurazione che ha stampato. Ma qui non deve: nessuno lo chiede, e la consegna è costruita perché nessuno lo debba chiedere.

## Che cosa la rende interessante

**È quasi l'unica forma dell'elenco in cui tutte le risposte sono giuste e alcune sono migliori.** Non «non c'è una risposta giusta», che è il caso di metà del capitolo 1: qui c'è un ordine fra le risposte, misurabile, e non c'è un massimo raggiungibile. **Nessuno deve sapere niente, e nessuno può barare**, perché il numero si misura con un righello. Molti compiti che hanno una risposta sola si possono riformulare così: chiedere invece la risposta più corta, più leggera, più economica.

**Le persone sono a un centesimo dall'ottimo con dieci punti, ed è misurato.** Da 1% peggio con 10-20 nodi a 11% peggio con 120. Non è un'osservazione sulla forma: è una misura di quanto sia adatta a chi la riceve, e non ce ne sono altre così nette in tutto l'elenco. **Da usare per dimensionare: dieci punti è dove si riesce quasi sempre, centoventi è dove si comincia a perdere.**

**La misura invece della risposta, quarta occorrenza.** Le lettere che passano attraverso un muro in cinque minuti (voce 131, codice a numeri (A=1)); i passi da cui si legge un sistema di segni inventato (voce 134, semaforo, bandiere, alfabeti alternativi); i corpi tipografici che si leggono da lontano (voce 139, testo troppo piccolo / troppo grande); e adesso i millimetri di un giro. **Con quattro casi non è più un'osservazione: è una famiglia**, e ha una proprietà comune che va scritta — il secondo tentativo va meglio del primo, e non c'è niente da correggere.

**Una regola stampata che dà una risposta valida senza pensare è il piolo più basso raccolto finora.** Non è un suggerimento e non toglie niente al problema, perché la risposta che produce è quella da battere. Per ogni forma con una soglia d'ingresso alta si può cercare una regola meccanica che produca una risposta mediocre. Nel giro più corto si chiama euristica del vicino più prossimo e ha novant'anni.

**Il numero delle soluzioni possibili è un contenuto, e si può stampare.** 181 440 giri per dieci punti; cinquanta ore per provarli tutti. Sono due numeri che chi legge può rifare e che spiegano perché la domanda non ha risposta. **Da provare su ogni forma dell'elenco in cui lo spazio delle possibilità sia calcolabile**, perché è il modo più economico di far capire che cosa sia un problema difficile.
