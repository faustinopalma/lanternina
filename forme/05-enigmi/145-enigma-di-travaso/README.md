# Enigma di travaso

- **Numero** 145 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi logici»
- **Si chiama anche** problema delle brocche, problema dei recipienti, travaso, *water pouring puzzle*, *water jug problem*, *decanting problem*, *measuring puzzle*, problema di Luchins
- **In una riga** misurare quattro litri con due recipienti.
- **Fonti** `water-pouring-puzzle.txt` e `einstellung-effect.txt`, prese il 30 agosto 2026 da en.wikipedia
- **Stato della ricerca** fatta, 30 agosto 2026

## Che cos'è

Ci sono dei recipienti di capacità note e senza tacche. Si può riempirne uno fino all'orlo, svuotarlo del tutto, o versare da uno all'altro finché il primo non è vuoto o il secondo non è pieno. Serve arrivare ad avere una certa quantità in un recipiente.

È il terzo enigma di stato del blocco, e quello che si conserva è diverso dalle altre due volte. Alla voce 143, enigma di attraversamento si teneva il conto di chi stava su quale sponda; alla voce 144, enigma di pesatura si contava quanta informazione si era raccolta; **qui quello che conta è quali quantità sono raggiungibili**, e la risposta si dà in una riga di aritmetica prima di versare qualunque cosa.

Parti mobili:

- **Le capacità.** Sono il problema: da tre e cinque litri si può ottenere qualunque numero intero di litri, da quattro e sei no.
- **Se c'è un rubinetto e uno scarico.** Nella versione base la quantità d'acqua totale è fissa; nella variante con rubinetto e scarico si può riempire e buttare quanto si vuole, e riempire o svuotare conta come un passo.
- **Quanti recipienti.** Due è il caso classico, tre è quello che compare nell'esperimento più noto.
- **Se si contano i passi.** Con l'obiettivo «in meno mosse possibile» diventa un problema di ottimizzazione; senza, è solo un problema di raggiungibilità.
- **Che i recipienti non abbiano tacche.** È l'ipotesi che si dichiara sempre e che nessuno guarda: sono di forma irregolare e non graduati, quindi **non si può misurare nessuna quantità che non riempia esattamente un recipiente.** Senza questa ipotesi il problema non esiste.

## Da dove viene

Cowley, nel 1926, scrive che il problema standard — tre recipienti da 8, 5 e 3 litri, si parte con 8 nel primo e si deve arrivare a 4 e 4 — **«risale al medioevo»**, e ne segnala la presenza nel manuale di matematica di Bachet, del Seicento. La fonte non dà una data più precisa.

La sua vita moderna comincia altrove, e non come gioco. Nel **1942 Abraham S. Luchins**, con Edith Hirsch Luchins, usa una serie di problemi di brocche per misurare una cosa che con le brocche non ha niente a che vedere: la tendenza a continuare a risolvere un problema nel modo in cui lo si è risolto prima, anche quando esiste un modo più semplice. Il fenomeno prende il nome tedesco **Einstellung**, che vuol dire «impostazione», e da lì viene il nome dell'effetto.

E poi c'è il cinema. Nel 1995 *Die Hard with a Vengeance* mette in scena la variante con rubinetto e scarico — due recipienti da tre e cinque litri, e bisogna farne quattro esatti —, al punto che una delle denominazioni correnti del problema, riportata dalla fonte, è **«Die Hard with a Vengeance puzzles»**.

## Varianti e parenti

- **Due recipienti** — il caso minimo, e quello in cui la condizione di risolubilità si vede meglio.
- **Tre recipienti a somma fissa** — nessun rubinetto: la quantità d'acqua totale non cambia mai. È la versione medievale, 8-5-3.
- **Con rubinetto e scarico** — riempire e buttare contano come passi. È la versione dei film e quella dell'esperimento di Luchins.
- **Voce 143, enigma di attraversamento** e **voce 144, enigma di pesatura** — le altre due forme di stato del blocco.
- **Voce 152, problema impossibile** — il parente stretto: qui la domanda «si può fare?» ha una risposta secca e calcolabile prima di provare.
- **Voce 364, invariante** — nel capitolo 13. Il legame è diretto: quello che non cambia mai, in un travaso, è che ogni quantità ottenibile è un multiplo del massimo comune divisore delle capacità.
- **Voce 54, misurare** — il parente materiale, e il rovescio esatto. Lì si misura con un'unità; qui non c'è nessuna unità e nessuna tacca, e la misura esce dalla combinazione di due capacità.
- **Voce 171, puzzle a scorrimento (15, Sokoban)** — la stessa struttura di stati e mosse, senza acqua.

## Che cosa se ne sa

**Si sa in anticipo se una cosa è possibile, e la condizione sta in una riga.** Per l'identità di Bézout, un problema di travaso ha soluzione **se e solo se la quantità voluta è un multiplo del massimo comune divisore delle capacità dei recipienti.** Con recipienti da 3 e da 5 il massimo comune divisore è 1, quindi si può ottenere qualunque numero intero di litri; con recipienti da 4 e da 6 è 2, quindi i litri dispari non si ottengono, e nessuna sequenza di travasi ci arriverà mai. **È il primo caso, in questo capitolo, in cui si può dimostrare che una cosa non si può fare senza provare a farla.**

**Le mosse reversibili e quelle irreversibili si distinguono, e da qui si risolve all'indietro.** Le sole mosse che si possono annullare in un passo sono versare **da** un recipiente pieno o versare **in** un recipiente vuoto; l'unica irreversibile è versare da un recipiente parzialmente pieno in un altro parzialmente pieno. Restringendosi alle mosse reversibili si può costruire la soluzione partendo dal risultato voluto, e per il problema 8-5-3 si scopre così che **le soluzioni sono esattamente due**, una di sette passi e una di otto. Risolvere all'indietro non è un trucco: è una conseguenza della struttura.

**La soluzione ottimale ha una forma geometrica.** La variante con rubinetto e scarico si risolve con un grafico baricentrico a forma di biliardo — cioè seguendo una pallina che rimbalza su una griglia di rette a pendenza −1. La fonte lo dice e non lo spiega; il fatto rilevante è che **un problema di travasi si può guardare come una traiettoria invece che come una sequenza di decisioni.**

**Qui c'è il dato misurato più forte del blocco, ed è su chi risolve.** Nell'esperimento di Luchins il gruppo sperimentale riceveva cinque problemi di allenamento, tutti risolvibili con la stessa formula — riempire il recipiente grande e travasarne via una volta il medio e due volte il piccolo —, seguiti da quattro problemi critici. Il gruppo di controllo non faceva gli esercizi di allenamento. Uno dei problemi critici era il **problema di estinzione**, costruito in modo che la formula abituale non funzionasse affatto. Gli altri si potevano risolvere sia con la formula lunga sia con una molto più corta.

I numeri sono questi. In condizioni normali, **il 70% dei soggetti del gruppo sperimentale continuò a usare la formula lunga nei problemi critici, e il 58% fallì il problema di estinzione** — mentre praticamente tutto il gruppo di controllo usò la soluzione semplice. E quando Luchins scriveva sul foglio, prima dei problemi critici, l'avvertenza **«non essere cieco», oltre la metà passò alla soluzione più semplice.** Due parole.

**Sotto pressione di tempo il numero diventa quasi totale, e la fonte lo racconta in un modo che va riportato per intero.** Luchins somministrò gli stessi problemi a una classe elementare dicendo ai bambini che la prova era a tempo, che velocità e precisione sarebbero state riviste dal preside e dagli insegnanti, e che avrebbe influito sui voti; e gli sperimentatori erano istruiti a commentare quanto fossero più lenti dei bambini delle classi inferiori. La fonte annota che durante l'esperimento si osservarono facce ansiose e a volte in lacrime, e aggiunge, fra parentesi, che **metodi del genere erano comuni negli anni Cinquanta e oggi violerebbero le norme etiche della ricerca.** Il risultato: **solo tre studenti su novantotto risolsero il problema di estinzione**, e la rigidità passò dal 70% al 98%, il fallimento dal 58% al 97%. Con studenti universitari lo stesso, anche quando erano stati avvertiti prima di usare il metodo diretto.

**Questo è il dato più diretto raccolto finora a sostegno di una regola già formulata.** Alla voce 88, sfida contro un tempo, dalla legge di Yerkes-Dodson del 1908, si era ricavato che ogni forma che chieda di inventare o capire peggiora sotto un tempo. Qui non è una legge generale applicata: è la stessa cosa misurata su un compito preciso, e il salto è dal 58% al 97%.

**Un fenomeno vicino ha un nome proprio: la fissità funzionale** (Duncker, 1945), cioè l'incapacità di scoprire un uso nuovo per un oggetto per averlo già usato in un contesto diverso. Duncker segnala che vale non solo per gli oggetti fisici ma anche per quelli mentali, ed è esattamente il caso della formula di Luchins.

## Esempi trovati

Dal problema medievale: 8, 5 e 3 litri, dall'inizio [8,0,0] alla fine [4,4,0] in sette passi.

Da Bachet, Seicento: lo stesso problema in un manuale di matematica.

Da Luchins, 1942: recipienti da 21, 127 e 3 unità, e cento unità da ottenere. Si riempie quello da 127 e se ne versa via quanto basta a riempire una volta quello da 21 e due volte quello da 3.

Dallo stesso esperimento, un problema critico: recipienti da 15, 39 e 3, e diciotto unità da ottenere. La formula lunga funziona — 39 meno 15 meno due volte 3 fa 18 — ma **basta riempire il primo e il terzo**, che fa 15 più 3. Quasi tutto il gruppo di controllo fece la seconda cosa, la maggioranza del gruppo allenato la prima.

Da *Die Hard with a Vengeance*, 1995: recipienti da tre e da cinque, quattro litri esatti, un rubinetto e un tempo.

## Una nostra versione

Il sistema stampa i problemi e la tabella; l'aritmetica è quella di una lista di numeri interi, che non è il maneggio delle lettere e non è il soddisfacimento di vincoli, ed è l'unica cosa che il sistema deve saper fare. La verifica è nel foglio: ogni riga si controlla con una sottrazione.

> **Sette problemi di brocche**
>
> Hai tre recipienti senza tacche, un rubinetto e un lavandino. Puoi riempirne uno fino all'orlo, svuotarlo del tutto, o versare da uno all'altro finché il primo è vuoto o il secondo è pieno. Devi ottenere la quantità richiesta.
>
> Non c'è acqua vera: si fa a matita. Per ogni problema scrivi **come** fai.
>
> ```
>            A     B     C     devi ottenere      come fai
>  1        14   163    25          99         ─────────────────
>  2        18    43    10           5         ─────────────────
>  3         9    42     6          21         ─────────────────
>  4        20    59     4          31         ─────────────────
>  5        21   127     3         100         ─────────────────
>  6        28    76     3          25         ─────────────────
>  7        15    39     3          18         ─────────────────
> ```
>
> ---
>
> Adesso la parte che conta, e leggila solo dopo aver finito tutti e sette.
>
> I primi cinque problemi si risolvono tutti nello stesso modo: **B meno A meno due volte C.** Se hai fatto così, hai fatto bene: funziona.
>
> Il numero 6 non si risolve così. Prova: 76 − 28 − 6 fa 42, e a te ne servivano 25. **Ci sei riuscito lo stesso?** Se sì, come? Se no, guarda 28 e 3 e prova a sottrarre.
>
> Il numero 7 si risolve in tutti e due i modi. **Quale hai usato?**
>
> ```
>  ────────────────────────────────────────────────────────────
> ```
>
> Nel 1942 uno psicologo di nome Luchins ha dato questi problemi a due gruppi di persone. Un gruppo aveva fatto prima i cinque di allenamento, l'altro no. Nel primo gruppo **il 70% ha usato la formula lunga anche dove ce n'era una corta, e il 58% non è riuscito a risolvere il numero 6.** Nel secondo gruppo, quasi tutti hanno fatto la cosa semplice.
>
> Poi Luchins ha provato a scrivere due parole sul foglio, prima dei problemi difficili: **«non essere cieco».** Oltre la metà è passata alla soluzione semplice.
>
> Ultima domanda. Se ti fosse stato scritto prima, avrebbe funzionato anche con te? **E se ti fosse stato scritto prima, avresti fatto i primi cinque in modo diverso?**

Il foglio è la riproduzione di un esperimento, non un gioco, e questo va detto: **la parte che insegna qualcosa arriva dopo, ed è su di sé.** L'esito atteso non è risolvere sette problemi — sono tutti facili — ma accorgersi di aver continuato a fare una cosa che aveva smesso di essere la migliore.

È la terza occorrenza in questo blocco dell'esercizio il cui esito è la perdita di una convinzione, dopo la scala di ventuno righe della voce 130, cifrario di Cesare e l'inchiostro invisibile che si vede in controluce della voce 136, inchiostro invisibile / luce. Qui la convinzione persa è di aver ragionato.

Tre cose sui numeri. Le capacità e gli obiettivi dei problemi 5 e 7 sono quelli riportati da `einstellung-effect.txt`; **gli altri cinque li ho costruiti io e l'aritmetica l'ho verificata una per una** — 163−14−50 = 99, 43−18−20 = 5, 42−9−12 = 21, 59−20−8 = 31, e per il numero 6, 76−28−6 = 42 mentre 28−3 = 25. La serie originale completa di Luchins non è nella fonte.

E una cosa sul tempo: **su questo foglio non c'è nessun cronometro, e non è un dettaglio.** Il fallimento nel problema di estinzione passa dal 58% al 97% quando si mette fretta, ed è misurato. Le condizioni in cui Luchins lo ha misurato sui bambini — il preside, i voti, i commenti sulla lentezza — la fonte stessa le dichiara incompatibili con le norme etiche di oggi.

Sul display da quattro righe ci sta un problema per volta, e sarebbe un'altra cosa: senza la tabella dei sette non c'è nessuna abitudine da formare, e senza abitudine non c'è niente da scoprire. È il caso della voce 63, inferire da un'assenza — quattro righe non sono un foglio più piccolo — nella sua forma più netta, perché qui la struttura *è* la serie.

## Da riprendere alla rassegna

**Due parole scritte prima cambiano il risultato di più della metà dei casi, ed è misurato.** «Non essere cieco» costa una riga e sposta oltre il 50% dei soggetti dalla soluzione lunga a quella corta. Nessuna consegna raccolta finora ha un rapporto così alto fra quanto costa scriverla e quanto cambia. **Va provata all'indietro su tutto l'elenco**, nella forma generale: una riga che avverta che la strada battuta potrebbe non essere la migliore.

**Ma c'è un rovescio, e riguarda quando dirlo.** Se l'avvertenza arriva prima dei cinque problemi di allenamento, l'abitudine non si forma e non c'è niente da scoprire. È la stessa struttura di Auble, Franks e Soraci della voce 110, indovinello classico (enigma): la parola chiave data prima toglie l'effetto. **Qui però la posta è più alta**, perché quello che si scopre non è la risposta a un enigma ma qualcosa su di sé, e vale la pena guardare alla rassegna che cosa comporti costruire un foglio che prima induce un'abitudine e poi la mostra.

**Si può sapere prima se una cosa è possibile, e non c'è niente di simile nell'elenco.** Il massimo comune divisore delle capacità dice, senza fare nessuna prova, quali quantità sono raggiungibili e quali no. È una forma di certezza che nessun'altra voce del capitolo offre — negli enigmi verbali non esiste modo di sapere prima se una parola c'è.

**La conferma misurata che il tempo peggiora i compiti nuovi.** Dal 58% al 97% di fallimenti sullo stesso problema, cambiando solo la pressione. Alla voce 88, sfida contro un tempo la regola era stata ricavata da Yerkes-Dodson e proposta come ipotesi da provare all'indietro; qui c'è il dato su un compito singolo. **Sono due prove indipendenti della stessa cosa**, e a questo punto la regola può essere trattata come stabilita: il cronometro va sulle cose che si sanno già fare.

Da verificare: la serie completa dei problemi di Luchins, che nella fonte compare solo per due voci; e il testo di Cowley del 1926 che fa risalire il problema al medioevo, che è citato ma non riportato.
