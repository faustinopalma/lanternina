# Cifrario a sostituzione

- **Numero** 129 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi verbali»
- **Si chiama anche** substitution cipher, cifrario monoalfabetico, alfabeto convenzionale, cifrario dei massoni, pigpen, tris cifrato, nomenclatore, crittogramma
- **In una riga** ogni lettera diventa un'altra.
- **Fonti** `substitution-cipher.txt`, `pigpen-cipher.txt`, `nyctography.txt`, `frequency-analysis.txt`, `letter-frequency.txt`, `cipher.txt`, tutte prese il 30 agosto 2026
- **Stato della ricerca** fatta, 30 agosto 2026

## Che cos'è

Una tabella a due colonne. A sinistra le lettere dell'alfabeto, a destra quello con cui vengono sostituite: altre lettere, numeri, segni geometrici, quello che si vuole. Si scrive scorrendo la tabella da sinistra a destra e si legge scorrendola da destra a sinistra.

`substitution-cipher.txt`, presa il 30 agosto 2026, dà la distinzione che vale più di ogni altra cosa in questa voce: **il cifrario a sostituzione e la trasposizione sono le due sole operazioni possibili su un testo, e sono complementari.** In una trasposizione le unità restano quelle e cambia il loro ordine; in una sostituzione l'ordine resta quello e cambiano le unità. La trasposizione, in questa enciclopedia, è la voce 121, anagramma. Non c'è una terza cosa.

**Il tratto che separa questo cifrario dai cinque che seguono in questo capitolo è che la sua chiave è arbitraria.** Non c'è niente da capire, niente da calcolare, e nessuna convenzione universale: o la tabella ce l'hai o non ce l'hai. Nel cifrario di Cesare (voce 130, cifrario di Cesare) la chiave è una regola aritmetica con ventuno possibilità; nel codice a numeri (voce 131, codice a numeri (A=1)) è una corrispondenza che sanno tutti; nel Morse (voce 132, Morse) è un codice storico che si trova ovunque. Qui la chiave è una scelta libera, e questo la rende insieme la più sicura del gruppo e la più fragile, perché **se il foglio con la tabella si perde, il messaggio è perso**.

Parti mobili:

- **L'unità sostituita.** Una lettera per volta è il caso semplice; due o tre lettere per volta si chiama cifrario poligrafico; e c'è il caso in cui a essere sostituite sono intere parole.
- **Se la tabella cambia strada facendo.** Una tabella sola per tutto il messaggio è un cifrario **monoalfabetico**; più tabelle che si alternano sono un cifrario **polialfabetico**, e la differenza è enorme perché un polialfabetico non si rompe contando le lettere.
- **Con che cosa si sostituisce.** Altre lettere, cifre, o simboli. `substitution-cipher.txt` avverte che i simboli non aggiungono niente alla sicurezza: qualunque insieme di segni strani si può ritrascrivere in lettere e trattare come al solito. Aggiungono però moltissimo all'aspetto, e l'aspetto è quasi tutto quello che serve in casa.
- **Come si costruisce la tabella.** Il metodo tradizionale parte da una parola chiave: si scrive la parola togliendo le lettere ripetute, poi si continua con le lettere restanti in ordine. Ha un difetto documentato: **le ultime lettere dell'alfabeto, che sono anche le più rare, tendono a restare in fondo** e quindi a corrispondere a sé stesse o quasi. La tabella costruita a caso è più forte.
- **Come si scrive il risultato.** La convenzione è a gruppi di cinque lettere, senza spazi e senza punteggiatura, per non regalare i confini delle parole; se il messaggio non è divisibile per cinque si riempie con lettere nulle, che decifrate danno ovvie sciocchezze e si buttano. Viene dal telegrafo.

## Da dove viene

È vecchio quanto la scrittura segreta, e non ha un inventore. Quello che ha una data è **il modo di romperlo**: intorno all'**850 dopo Cristo** il filosofo arabo **Al-Kindi** scrive un *Manoscritto sulla decifrazione dei messaggi crittografici*, che contiene la prima descrizione pubblicata di come si spezza un cifrario a sostituzione semplice. Il metodo che descrive oggi si chiama **analisi delle frequenze**, e in inglese, più onestamente, *counting letters*: contare le lettere. (`substitution-cipher.txt` e `frequency-analysis.txt`, 30 agosto 2026)

Il **nomenclatore** è la variante che ha dominato la diplomazia europea dal Quattrocento al Settecento: un foglietto con tabelle di sostituzione per lettere, sillabe e parole intere, di solito verso numeri. Prende il nome dal funzionario che annunciava i titoli dei dignitari in visita, perché all'inizio la parte a codice conteneva solo nomi di persone importanti. Il *Grande Cifrario* dei Rossignol, usato da Luigi XIV, era uno di questi. `substitution-cipher.txt` racconta la storia con una nota amara: **gli analisti dei governi rompevano sistematicamente i nomenclatori già dalla metà del Cinquecento, e sistemi migliori esistevano dal 1467, ma la risposta abituale alla decrittazione fu semplicemente fare tabelle più grandi.** Alla fine del Settecento alcuni nomenclatori avevano cinquantamila simboli, e non servivano a niente.

Il **cifrario pigpen** — detto anche massonico, rosacrociano, di Napoleone, o del tris — sostituisce le lettere con frammenti di una griglia: ogni lettera è l'angolo di casella in cui si trova, con o senza un punto. Nel **1531** Cornelio Agrippa descrive una forma primitiva di quello rosacrociano, attribuendola a una tradizione cabalistica ebraica; quel sistema, che più tardi verrà chiamato *la Cabala delle nove camere*, usava l'alfabeto ebraico e serviva a **simbolismo religioso e non a nascondere niente**. I massoni cominciano a usarlo all'inizio del Settecento per i verbali e per la corrispondenza fra logge, e lo usano tanto che il cifrario porta il loro nome. Ci sono lapidi incise così: una delle pietre più antiche del cimitero di Trinity Church a New York, aperto nel 1697, porta un'iscrizione in pigpen che dice *ricordati della morte*. (`pigpen-cipher.txt`, 30 agosto 2026)

Della stessa fonte vanno riportati due usi che non sono giochi. Il **7 luglio 1730** il pirata francese Olivier Levasseur gettò alla folla un foglio scritto in pigpen che avrebbe contenuto il luogo del suo tesoro; il tesoro non è mai stato trovato e la configurazione esatta del cifrario non è mai stata determinata. E nel **1852** Major Logue, allevatore irlandese nell'Australia occidentale, usò il pigpen **nel proprio diario per annotare in modo discreto di aver partecipato all'uccisione di almeno diciannove Yamatji**, un popolo aborigeno australiano: le frasi cifrate nel diario sono esattamente quelle che ammettono gli omicidi. Un cifrario nasconde una cosa a chi legge per caso, e quello che si nasconde non è sempre un gioco.

Un'ultima origine, e non è di nascondimento affatto. Nel **1891 Lewis Carroll** — Charles Lutwidge Dodgson — inventa la **nictografia**: un alfabeto in cui ogni lettera è un quadratino fatto di punti agli angoli e di segmenti sui lati, e uno strumento, il *nictografo*, che è un cartoncino con sedici fori quadrati da un quarto di pollice. Serviva a una cosa sola: **scrivere al buio.** Carroll si svegliava di notte con dei pensieri e non voleva accendere la candela. Lo aveva prima chiamato *tiflografo*, da *typhlos*, cieco, e poi *nictografo*, da *nyctos*, notte. Riuscì a far somigliare ventitré dei ventisei simboli alla lettera che rappresentavano, e per sapere dove cominciasse ogni quadratino si diede una regola: **ogni lettera contiene un grosso punto nero nell'angolo in alto a sinistra.** (`nyctography.txt`, 30 agosto 2026)

## Varianti e parenti

- **Cruciverba crittografato** (voce 354, cruciverba crittografato) — **il confine da dichiarare**: lì il gioco italiano in cui ogni casella porta un numero e numeri uguali sono lettere uguali, con le sue convenzioni di gara; qui il cifrario a sostituzione come sistema di scrittura.
- **Cifrario di Cesare** (voce 130, cifrario di Cesare) — il caso particolare in cui la tabella non è arbitraria ma è uno scorrimento.
- **Codice a numeri** (voce 131, codice a numeri (A=1)) — il caso particolare in cui la tabella è l'ordine dell'alfabeto stesso.
- **Anagramma** (voce 121, anagramma) — l'altra operazione, la trasposizione: stesse unità, altro ordine.
- **Atbash** — l'alfabeto rovesciato: la prima lettera diventa l'ultima. È il cifrario a sostituzione più antico che abbia un nome.
- **Pigpen** — la tabella è geometrica: ogni lettera è la forma della casella in cui sta. Ne esistono molte disposizioni — griglia, griglia, X, X oppure griglia, X, griglia, X — e la variante di Newark usa da uno a tre trattini invece dei punti, il che dà l'illusione di molti più segni di quanti ce ne siano davvero.
- **Nomenclatore** — la tabella contiene anche sillabe e parole intere, e non si distingue quali.
- **Cifrario polialfabetico** — più tabelle che si alternano; il Vigenère è il caso classico.
- **Cifrario omofonico** — una lettera frequente ha più simboli, apposta per appiattire il conteggio.
- **Nictografia** — un alfabeto sostitutivo inventato per scrivere senza vedere.
- **Braille come cifra visiva** (voce 133, Braille come cifra visiva) — il parente diretto della nictografia: anche lì una lettera è una configurazione dentro una cornice fissa.
- **Corrispondenza (matching)** (voce 5, corrispondenza (matching)) — la forma di pagina che un cifrario è, quando la tabella si stampa vuota.
- **Traduzione** (voce 19, traduzione) — il verbo, e non è una metafora: cifrare è tradurre in una lingua che ha le stesse parole e altre lettere.
- **Steganografia** (voce 135, steganografia) — l'altra strada: non rendere illeggibile il messaggio, ma far sì che nessuno sospetti che ci sia.

## Che cosa se ne sa

**Sull'effetto niente**, in nessuna delle sei fonti prese il 30 agosto 2026. Sulla forza del cifrario, invece, ci sono numeri, e sono numeri veri.

Le tabelle possibili su ventisei lettere sono 26 fattoriale, circa 88 bit, e la fonte lo dice per poi smontarlo: **il cifrario è debolissimo lo stesso.** La misura che conta si chiama **distanza di unicità**, ed è questa: per l'inglese **bastano 27,6 lettere di testo cifrato** per rompere un cifrario a sostituzione ad alfabeto mescolato. In pratica ne servono una cinquantina, e a volte meno se il testo contiene forme riconoscibili. (`substitution-cipher.txt`, 30 agosto 2026)

Il metodo è quello di Al-Kindi. Si contano le lettere del testo cifrato e si confrontano con le frequenze della lingua. In inglese la sequenza è *etaoin shrdlu*; **in italiano è e a i o n l r t s c d u**, e `letter-frequency.txt` l'attribuisce a Simon Singh e Stefano Galli, *Codici e Segreti*, Rizzoli 1999. Poi si passa alle coppie e alle terne, che dicono di più: in inglese la coppia più frequente è *th* e la terna più frequente è *the*, e trovarle risolve tre lettere in un colpo. Un'altra leva è **la forma delle parole**: *tater*, *ninth* e *paper* hanno tutte lo schema ABACD, e uno schema si riconosce anche senza sapere le lettere.

Su questo c'è un dettaglio che vale la pena di isolare, perché rovescia l'intuizione: **il cifrario a simboli strani non è più forte di quello a lettere**. La fonte lo dice esplicitamente del pigpen, e poi lo dice ancora più duramente: il pigpen è talmente noto che **chi lo intercetta non ha bisogno di romperlo — lo legge, esattamente come lo legge il destinatario.** Quello che i simboli comprano non è segretezza: è l'aspetto di una cosa segreta. E la stessa fonte nota, senza ironia, che proprio per la sua semplicità il pigpen compare spessissimo nei libri di cifrari per bambini.

Sul nostro sistema, e questa è la voce in cui il limite morde di più: **il sistema non sa manipolare le lettere dentro le parole** (misurato, `ideas/10 §6`). Non può cifrare, non può decifrare, e non può controllare un testo cifrato. Un messaggio cifrato dal sistema sarebbe sbagliato in modo invisibile, e il danno sarebbe totale — chi lo decifra non otterrebbe un errore, otterrebbe un'assurdità, e non avrebbe modo di sapere di chi sia la colpa.

**L'unica strada era già stata trovata alla scheda 5, corrispondenza (matching): una legenda data, o meglio una legenda stampata vuota e riempita da chi risponde.** Una tabella a due colonne è una macchina, e la seconda colonna la scrive una mano. Il sistema stampa la cornice e non tocca nessuna lettera; l'operazione di cifratura diventa una consultazione, che è lenta ma non si sbaglia in silenzio, perché una lettera cercata nella tabella o si trova o non si trova.

## Esempi trovati

Da `substitution-cipher.txt`, con la chiave *zebras*: `flee at once. we are discovered!` diventa `SIAA ZQ LKBA. VA ZOA RFPBLUAOAR!`, e scritto a gruppi di cinque `SIAAZ QLKBA VAZOA RFPBL UAOAR`.

Dalla stessa fonte, con la chiave *grandmother*, lo stesso messaggio diventa `MCDD GS JIAD. WD GPD NHQAJVDPDN!`

Dai cataloghi dei commessi viaggiatori: una cifratura minima in cui le cifre dei prezzi diventano lettere. `MAT` sta per 120, `PAPR` per 5256, `OFTK` per 7803. La parola chiave del negozio è una parola di dieci lettere diverse.

Da Trinity Church, New York, su una lapide di fine Seicento: un'iscrizione in pigpen che dice *ricordati della morte*.

Da Olivier Levasseur, 7 luglio 1730: un foglio in pigpen gettato alla folla, mai decifrato con certezza.

Dal diario di Major Logue, 1852: le frasi in pigpen sono quelle che ammettono gli omicidi, e il resto della pagina è in chiaro.

Da Lewis Carroll, ottobre 1891, in una lettera alla rivista *The Lady*: «Chiunque abbia provato, come ho fatto io tante volte, ad alzarsi dal letto alle due di notte d'inverno, accendere una candela e annotare un pensiero felice che altrimenti si dimenticherebbe, sarà d'accordo con me che comporta molto disagio». E la chiusa, che è la ragione per cui la nictografia esiste: «Pensate al numero di ore solitarie che un cieco passa spesso senza far niente, quando volentieri metterebbe per iscritto i propri pensieri, e capirete che dono gli si può fare con un piccolo taccuino indelebile, un cartoncino con file di fori quadrati, e insegnandogli l'alfabeto quadrato».

## Una nostra versione

La tabella si stampa vuota. E l'uso che si sceglie non è nascondere: è **scrivere al buio**, che è quello per cui la nictografia fu inventata, e che si verifica da solo.

> **L'alfabeto quadrato**
>
> Nel 1891 Lewis Carroll — quello di Alice — si svegliava di notte con dei pensieri e non voleva accendere la candela per scriverli. Allora si inventò un alfabeto in cui ogni lettera è un quadratino: punti agli angoli e trattini sui lati. Si può scrivere senza vedere, perché le dita sanno dove sono gli angoli di un quadrato.
>
> Si diede una regola sola, e senza quella non funzionava: **ogni lettera ha un punto grosso nell'angolo in alto a sinistra**, così quando rileggi sai da che parte comincia il quadratino.
>
> Fattelo tu.
>
> ```
>   Ogni lettera è un quadrato così:     * ─ ─ ─ ┐    il punto grosso
>                                        │       │    sta sempre qui
>                                        │       │
>                                        └ ─ ─ ─ ┘
>
>   Puoi usare: i 3 angoli liberi, e i 4 lati. Sono 7 posti,
>   e con 7 posti si fanno piu' di cento segni diversi.
> ```
>
> ```
>   A  ────────    F  ────────    N  ────────    S  ────────
>   B  ────────    G  ────────    O  ────────    T  ────────
>   C  ────────    H  ────────    P  ────────    U  ────────
>   D  ────────    I  ────────    Q  ────────    V  ────────
>   E  ────────    L  ────────    R  ────────    Z  ────────
>                  M  ────────
> ```
>
> **Un consiglio di Carroll, e gli costò due tentativi.** Fai in modo che la maggior parte dei segni **somigli alla lettera vera** — lui ci riuscì con ventitré lettere su ventisei. La L è un angolo. La T è un lato in alto e uno in mezzo. La O sono tutti e quattro i lati. Le lettere che somigliano a sé stesse non si dimenticano.
>
> **La prova, e si fa una volta sola.** Stanotte, quando spegni la luce, tieni questo foglio e una matita sul comodino. Scrivi **tre righe al buio**: qualsiasi cosa, anche una sciocchezza.
>
> ```
>   ─────────────────────────────────────────────────────────
>   ─────────────────────────────────────────────────────────
>   ─────────────────────────────────────────────────────────
> ```
>
> **Domattina rileggile e trascrivile.**
>
> ```
>   ─────────────────────────────────────────────────────────
>   ─────────────────────────────────────────────────────────
>   ─────────────────────────────────────────────────────────
> ```
>
> ```
>   Lettere che non sono riuscito a rileggere:  ────────────────
>   Con quale altra le ho confuse?              ────────────────
>   Come cambio quel segno?                     ────────────────
> ```
>
> **Le lettere che hai confuso non sono un tuo errore: sono un difetto dell'alfabeto.** Carroll ha buttato via il primo nictografo per questo — scriveva dentro un rettangolo ritagliato nel cartoncino e la mattina non si capiva niente. Cambia il segno e riprova domani.

La tabella stampata vuota è l'unica forma in cui questa voce sta in casa, ed è la stessa cosa già notata alla scheda 5, corrispondenza (matching): **una legenda data — o meglio, una legenda da riempire — è il modo di usare un cifrario senza chiedere a nessuna macchina di toccare una lettera.** Qui il sistema stampa ventuno righe e non sa che cosa ci finirà.

L'uso scelto non è nascondere. È il quarto caso di questo blocco in cui **una forma enigmistica ha un impiego documentato in cui nessuno deve indovinare niente**: Carroll voleva scrivere al buio, non tenere segreto qualcosa. Il problema che chiude quasi tutto il capitolo — qualcuno deve sapere la risposta — non si pone.

La verifica è fisica e non è opinabile: la mattina dopo o si rilegge o non si rilegge. E l'ultima riga — *quale segno cambio* — sposta l'errore sulla notazione invece che su chi scrive, come alla voce 103, partitura / spartito.

**Dove si romperebbe.** Se il sistema stampasse un messaggio già cifrato, sarebbe sbagliato e nessuno se ne accorgerebbe: la tabella qui è vuota apposta. Il pannello da quattro righe non può portare la tabella — ventuno righe non ci stanno — ma può portare la sola cosa che serve la sera: *stanotte, tre righe al buio*.

## Da riprendere alla rassegna

**Sostituzione e trasposizione sono le due sole operazioni su un testo,** e l'enciclopedia le ha adesso tutte e due: la voce 121, anagramma e questa. Ogni gioco di lettere dell'elenco è una delle due, o un misto. Alla rassegna vale la pena riordinare il capitolo 12 secondo questo asse invece che per nome del gioco, e vedere se le due colonne si riempiono in modo uguale.

**I simboli strani comprano l'aspetto, non la segretezza,** e la fonte lo dice senza pietà del pigpen: chi lo intercetta lo legge come lo legge il destinatario. Per noi la conseguenza è liberatoria invece che deprimente — se quello che si vuole è che una cosa **sembri** un codice, un cifrario noto va benissimo, e nessuno deve rompere niente.

**Una tabella stampata vuota è una macchina, e il sistema può stamparla senza saperne il contenuto.** Vale per i cifrari, per le legende delle mappe, per le notazioni inventate. È l'unica famiglia in cui il limite del sistema sulle lettere non morde affatto, ed è già arrivata due volte per strade indipendenti — alla scheda 5, corrispondenza (matching) e alla voce 116, indovinello dell'oggetto che scrive.

**La risposta storica alla decrittazione fu fare tabelle più grandi, e non funzionò per tre secoli.** I nomenclatori arrivarono a cinquantamila simboli mentre esistevano dal 1467 sistemi che non avevano quel difetto. È un caso di scuola di che cosa succede quando si risponde a un problema aumentando la quantità di una cosa che era già la cosa sbagliata, e sarebbe una consegna a sé.

**Un cifrario è quasi sempre stato usato per nascondere qualcosa a qualcuno, e non sempre per gioco.** Il diario di Major Logue del 1852 cifra le righe in cui ammette diciannove omicidi, e il resto della pagina è in chiaro. Se questa forma entrasse in una casa, il racconto storico che l'accompagna può essere quello dei massoni e delle lapidi, o quello del diario australiano, e non sono la stessa cosa. Alla rassegna va deciso se la storia vera di una forma vada raccontata anche quando è brutta.
