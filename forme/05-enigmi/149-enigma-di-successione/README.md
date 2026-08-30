# Enigma di successione

- **Numero** 149 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi logici»
- **Si chiama anche** serie numerica, completamento di serie, «trova il numero mancante», successione da indovinare, *number sequence puzzle*, *series completion*
- **In una riga** «quale numero viene dopo».
- **Fonti** `integer-sequence.txt` e `oeis.txt`, prese il 30 agosto 2026 da en.wikipedia; `confirmation-bias.txt` e `inductive-reasoning.txt`, prese il 30 agosto 2026; l'argomento del polinomio interpolante è nostro e non sta in nessuna delle pagine lette
- **Stato della ricerca** fatta, 30 agosto 2026

## Che cos'è

Alcuni termini in fila, e la domanda: quale viene dopo. Il compito non è calcolare: è indovinare la regola che li ha prodotti, e poi applicarla una volta.

È la terza delle quattro voci che si reggono su un enunciato da ragionare, e quello che la rende difficile è diverso da tutte le altre. Alla voce 147, enigma di verità e menzogna il testo poteva mentire; alla voce 148, enigma induttivo il dato era che qualcuno non avesse capito. **Qui il testo non dice niente di falso e non nasconde niente: dà pochi termini e tace sulla regola**, e la difficoltà è che i termini non bastano mai.

Parti mobili:

- **Quanti termini si mostrano.** Tre, cinque, sette. È l'unica manopola vera, e non funziona come sembra: aggiungere termini non rende il problema più facile, rende più stretto l'insieme delle regole che li spiegano.
- **Che cosa si chiede.** Il termine dopo; oppure la regola scritta a parole; oppure il centesimo termine, che obbliga a scrivere la regola perché non si può arrivarci contando.
- **Se la regola è dichiarata.** Se lo è, non è più questa forma: è la voce 368, successione con regola dichiarata, nel capitolo 13, dove si applica una regola data e il lavoro è il calcolo.
- **Di che cosa sono fatti i termini.** Numeri, lettere, figure, parole. Cambia tutto il resto: con le figure il sistema non può verificare, con le lettere nemmeno.
- **Se c'è un buco in mezzo** invece che in fondo. Un termine mancante fra due noti si vincola da due lati, ed è un problema diverso.

La parte mobile che non si vede è la più importante: **quante regole diverse producono quei termini.** Sono sempre infinite, e la domanda «quale viene dopo» è in realtà «a quale regola stava pensando chi ha scritto il foglio».

## Da dove viene

La forma non ha un inventore: è vecchia quanto le tabelle di numeri, e nessuna delle pagine lette la data. Quello che ha una storia è il repertorio.

**Neil Sloane** comincia a raccogliere successioni di interi nel **1964**, da studente di dottorato, per il proprio lavoro di combinatoria; la raccolta all'inizio sta su schede perforate. Ne pubblica due estratti: *A Handbook of Integer Sequences*, **1973**, con 2 372 successioni in ordine lessicografico; e *The Encyclopedia of Integer Sequences*, con Simon Plouffe, **1995**, con 5 488. Quando la raccolta arriva a 16 000 voci smette di stare in un libro: diventa un servizio via posta elettronica nell'**agosto 1994** e un sito nel **1996**, l'*On-Line Encyclopedia of Integer Sequences*. Nel 1998 Sloane fonda anche il *Journal of Integer Sequences*. A novembre 2025 la banca dati contiene **più di 390 000 successioni** e cresce di una trentina di voci al giorno, cioè di circa diecimila l'anno.

Il dettaglio che riguarda questa voce è la funzione di ricerca: **si può cercare per sottosuccessione.** Chi ha davanti quattro numeri e non sa che cosa siano li scrive e ottiene l'elenco di tutte le regole note che li producono — che di solito non è una. È il rovescio esatto del compito scolastico, ed esiste dal 1996.

Il contesto in cui questa forma è stata misurata è un altro: il **compito 2-4-6 di Peter Wason**, **1960**, *On the failure to eliminate hypotheses in a conceptual task*. Si dà la terna 2, 4, 6 e si dice che segue una regola; chi partecipa può proporre altre terne e viene detto se rispettano la regola o no. La regola vera è «tre numeri in ordine crescente», e quasi nessuno la trova, perché quasi nessuno propone una terna che spera venga rifiutata.

## Varianti e parenti

- **Il termine mancante in mezzo** — vincolato da due lati.
- **La successione di figure** — stessa struttura, termini disegnati.
- **La successione di lettere** — dove il passo è nell'alfabeto invece che nei numeri.
- **La successione con più regole possibili dichiarate** — si chiede quante ne trovi, e non quale sia giusta.
- **Il compito 2-4-6** — la stessa forma girata: invece di dire il termine dopo si propongono casi e si riceve un sì o un no.
- **Voce 368, successione con regola dichiarata** — il confine più netto di questa voce, nel capitolo 13, giochi matematici e ricreativi. Là la regola è data e il lavoro è applicarla; qui la regola è tutto quello che c'è da trovare. Sono la stessa fila di numeri usata per due compiti opposti.
- **Voce 61, indurre** — il verbo, e questa è la forma di pagina che lo mette in scena più direttamente di ogni altra.
- **Voce 59, escludere** — quello che bisognerebbe fare e quasi nessuno fa: proporre un caso per vederlo cadere.
- **Voce 150, enigma di situazione (lateral thinking)** — il vicino sull'altro lato, dove pure si propongono ipotesi e si riceve un sì o un no, ma la risposta la dà una persona.
- **Voce 69, vincolare** — il rovescio: dichiarare la regola invece di indovinarla.

Con il capitolo 12 questa voce non confina in nessun punto: non ci sono lettere da spostare e nessun gioco enigmistico italiano corrisponde. Vale la pena dirlo, perché per le voci vicine il confine c'era.

## Che cosa se ne sa

**Nessun numero finito di termini determina la regola, e la dimostrazione è costruttiva.** Dati *k* numeri qualsiasi in fila, esiste un polinomio di grado *k*−1 che passa esattamente per quei punti — e un altro di grado *k* che passa per quei punti e per un (*k*+1)-esimo scelto a piacere. Quindi **per qualunque continuazione si voglia, esiste una regola perfettamente legittima che la produce.** Nessuna delle pagine lette lo afferma in questa forma: `integer-sequence.txt` si limita a dire che una successione si può dare per formula esplicita, per relazione fra i termini, o per una proprietà che i suoi membri hanno e gli altri interi no. **L'argomento è nostro**, ed è verificabile da chiunque abbia in mano l'interpolazione. Non è una curiosità: è la ragione per cui questa forma, presa alla lettera, non ha una risposta.

**Quali successioni le persone trovino interessanti è stato misurato, e il risultato ha un nome.** Nel 2009 Philippe Guglielmetti usò la banca dati di Sloane per misurare quanto ogni intero fosse «importante», contando in quante successioni compaia. Il grafico mostra **due nuvole di punti separate da un buco netto** — lo *Sloane's gap*: i numeri «interessanti», che compaiono molto più spesso, sono essenzialmente i primi, le potenze e i numeri altamente composti. Nicolas Gauvrit, Jean-Paul Delahaye e Hector Zenil hanno studiato il fenomeno e spiegano la posizione delle due nuvole con la complessità algoritmica, ma **il buco fra le due con fattori sociali: una preferenza artificiale per le successioni di primi, i numeri pari, le progressioni geometriche e quelle alla Fibonacci.** È il dato più utile di questa voce: la regola che chi scrive «ha in mente» non è casuale, e non è nemmeno matematica. È culturale, e si può nominare.

**Chi risolve non prova a smentirsi, ed è misurato dal 1960.** Nel compito 2-4-6, i partecipanti proponevano quasi soltanto terne che confermavano l'ipotesi che avevano in testa — 8, 10, 12 se pensavano «pari crescenti» — e per questo quasi nessuno arrivava alla regola vera, che era molto più larga di quello che immaginavano. Ne segue una consegna di una riga già raccolta alla voce 61, indurre: **proponi un caso che speri venga rifiutato.**

**Dove mettere il suggerimento è una decisione con un numero attaccato.** Luchins, 1942: due parole scritte prima dei problemi critici spostano oltre il 50% dei soggetti dalla soluzione lunga a quella corta. Ma il rovescio vale in pieno qui: **se si scrive prima che le continuazioni possibili sono infinite, non resta niente da scoprire**, perché quello è esattamente il fatto interessante. La scelta presa qui sotto è di lasciarlo scoprire e di dare invece una struttura che renda impossibile fermarsi.

**Nessuna fonte dice a che età o con quanta facilità si risolva una successione.** Le pagine lette sono di matematica e di banche dati. **Va verificato** se la psicologia cognitiva abbia misure sul completamento di serie: nelle pagine prese non ce ne sono.

## Esempi trovati

Dal libro di Sloane: 0, 1, 1, 2, 3, 5, 8, 13, … che è Fibonacci, definita implicitamente da una relazione fra i termini; e 0, 3, 8, 15, … che è *n*²−1, definita esplicitamente da una formula. Due successioni date in due modi diversi, e nessuno dei due si legge dai termini.

Dalla stessa pagina, un terzo modo che non è né l'uno né l'altro: i numeri perfetti, definiti da una proprietà che i loro membri hanno e gli altri no — **e per i quali non esiste nessuna formula del termine *n*-esimo.** Una successione perfettamente definita di cui non si sa scrivere il termine dopo.

Dal compito 2-4-6: la terna che tutti leggono come «pari crescenti» e che invece segue la regola «tre numeri in ordine crescente».

Dalla banca dati di Sloane, la voce numero 100 000, aggiunta nel 2004: conta le tacche sull'osso di Ishango.

## Una nostra versione

La forma presa alla lettera non ha una risposta, e questo è il suo contenuto invece che il suo difetto. Il foglio lo dice facendolo, non spiegandolo.

> **Tre modi di andare avanti**
>
> Ecco tre numeri:
>
> ```
>              1     2     4     ?
> ```
>
> La domanda che ti aspetti è «quale viene dopo». Non è questa.
>
> **Trova tre regole diverse che producono 1, 2, 4 e che poi vanno avanti in tre modi diversi.**
>
> Una regola vale se, partendo da capo e applicandola, **ti restituisce 1, 2, 4**. Questo è tutto quello che le si chiede, e lo puoi controllare da solo: rifai i primi tre passi e guarda se tornano. Non c'è nessuna soluzione stampata da nessuna parte, e non serve.
>
> ```
>  REGOLA A, scritta a parole
>  ────────────────────────────────────────────────────────
>  ────────────────────────────────────────────────────────
>  e allora la fila e':  1   2   4   ──   ──   ──
>
>  REGOLA B, scritta a parole
>  ────────────────────────────────────────────────────────
>  ────────────────────────────────────────────────────────
>  e allora la fila e':  1   2   4   ──   ──   ──
>
>  REGOLA C, scritta a parole
>  ────────────────────────────────────────────────────────
>  ────────────────────────────────────────────────────────
>  e allora la fila e':  1   2   4   ──   ──   ──
> ```
>
> **La terza è la più difficile.** Le prime due vengono quasi da sole; la terza chiede di smettere di cercare una regola che assomigli alle prime due.
>
> ---
>
> Quando le hai, una domanda che non ha una risposta breve:
>
> ```
>  Se ti avessi chiesto «quale numero viene dopo»
>  e tu avessi risposto con la tua REGOLA C,
>  avresti sbagliato?
> ```
>
> ---
>
> **E se ti va, l'ultimo pezzo.** Scrivi tu tre numeri — non questi — e dalli a qualcuno in casa dicendo soltanto «quale viene dopo». Poi guarda che cosa risponde, e poi digli che tu ne avevi in mente un'altra. **Non è uno scherzo: è la cosa che questo foglio dimostra.**

Le regole ci sono e sono state verificate a mano. «Raddoppia» dà 1, 2, 4, 8, 16, 32. «Aggiungi uno, poi due, poi tre, poi quattro» dà 1, 2, 4, 7, 11, 16. «Scrivi tutti i numeri saltando i multipli di tre» dà 1, 2, 4, 5, 7, 8. Tre regole legittime, tre quarti termini diversi — 8, 7 e 5 —, e nessuna delle tre è più giusta delle altre. Non sono nel foglio, e non devono esserci: **una quarta regola diversa da queste è altrettanto valida, e chi la trova non ha modo di sbagliarsi.**

La cosa che fa il lavoro è il criterio di validità: **una regola vale se rigenera i termini dati.** Non serve nessuno che corregga, non serve una soluzione stampata, e il problema che chiude questo capitolo — un enigma ha una risposta e qualcuno deve saperla — semplicemente non si presenta, perché la risposta non è una. È la stessa struttura del controllo dell'errore nel materiale, applicata a una regola invece che a un oggetto.

L'ultimo pezzo è la mossa già raccolta molte volte, girare il gioco dalla parte di chi costruisce, e qui serve a una cosa in più: **produce l'esperienza di essere quello che sa la risposta, e di scoprire che la risposta era arbitraria.**

Sul pannello da quattro righe da 44 caratteri i tre numeri e la domanda ci stanno, e sarebbe una consegna vera. Le tre regole scritte a parole no.

## Da riprendere alla rassegna

**Una forma senza risposta unica non è una forma rotta.** Questa presa alla lettera non ha una soluzione, e non per un difetto di chi la pone: per un fatto matematico. La conseguenza è che **si può consegnare senza che nessuno sappia niente**, ed è la prima voce del capitolo di cui si possa dire. Alla rassegna vale la pena separare, in tutto l'elenco, le forme che hanno una risposta da quelle che hanno un criterio di validità — perché le seconde non hanno bisogno di nessuno.

**La regola che chi scrive ha in mente è culturale, ed è misurata.** Lo *Sloane's gap* dice che i numeri che compaiono nelle successioni raccolte non sono quelli che la matematica renderebbe frequenti: sono i primi, le potenze e le progressioni alla Fibonacci, e gli autori dello studio attribuiscono il buco a una preferenza artificiale. **Chi scrive una successione «da indovinare» sta pescando in quel repertorio senza saperlo**, e chi la risolve indovina la cultura di chi l'ha scritta. Da guardare accanto alla voce 84, quiz, che ha lo stesso difetto con un nome diverso.

**Il rovescio di Luchins morde qui più che altrove.** Dire prima che le continuazioni sono infinite toglie l'unica cosa che c'è da scoprire; non dirlo lascia fermo chi non trova neanche la prima regola. La via presa — nessun suggerimento, ma una struttura in tre caselle che si può cominciare a riempire senza sapere niente — è la stessa già usata alla voce 147, enigma di verità e menzogna, e con due occorrenze comincia a essere una mossa: **quando il suggerimento rovinerebbe il compito, si stampa la forma della risposta invece del suggerimento.**

**Cercare una successione per i suoi primi termini si fa da trent'anni, e il risultato non è mai uno solo.** La banca dati di Sloane è consultabile per sottosuccessione dal 1996 e restituisce elenchi. È un fatto che riguarda ogni compito di questo tipo consegnato oggi, e non è un problema di onestà: **è la dimostrazione pratica, e a portata di chiunque, che quel compito non aveva una risposta.**
