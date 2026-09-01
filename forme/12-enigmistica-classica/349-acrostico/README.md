# Acrostico

- **Numero** 349 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Rebus e forme miste»
- **Si chiama anche** acrostico, acrostic, capoverso parlante, doppio acrostico, anacrostico, double-crostic, notarikon
- **In una riga** le iniziali dei versi compongono una parola.
- **Contratto** voce breve
- **Fonti** `it-acrostico.txt`, `it-gioco-enigmistico.txt`, `acrostic-puzzle.txt`, `it-notarikon.txt`, `it-telestico.txt`, `word-square.txt`, prese il 1 settembre 2026. `acrostic.txt` è già la fonte della voce 122, acrostico e qui non si ripete
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Un testo in cui le lettere iniziali di ogni riga, lette in verticale, dicono un'altra cosa. `it-acrostico.txt`, presa il 1 settembre 2026, allarga la definizione più di quanto ci si aspetti: non solo le lettere, ma anche «le sillabe o le parole iniziali», e non solo di versi — «sono definiti acrostici anche i termini che risultano dalle lettere iniziali di singole parole anziché di versi».

**In enigmistica italiana l'acrostico non è un gioco: è uno schema.** `it-gioco-enigmistico.txt`, presa lo stesso giorno, tiene separate le due parole, e insiste sulla distinzione: uno schema è una relazione fra parole, un gioco è quello che qualcuno costruisce sfruttando lo schema. L'acrostico compare in quella pagina in un elenco preciso — «gli schemi complessi, desueti o rari come l'acrostico, il mesostico, il telestico, il logogrifo, il metanagramma» — cioè fra le relazioni che quasi nessuno usa più per costruire giochi pubblicati. È l'unica voce di questa sezione che la disciplina dichiara in disuso.

La cosa che lo distingue da tutto il resto del capitolo è dove sta la seconda lettura. Nelle voci da 341 a 348 la seconda lettura è fatta delle stesse lettere della prima, rimesse insieme in un altro modo. Qui la seconda lettura è **un sottoinsieme** della prima: una lettera per riga, e tutte le altre restano dove sono e non servono. Nessuna lettera si sposta, nessuna si conta.

Parti mobili:

- **L'unità.** La lettera, la sillaba, o la parola intera.
- **L'unità di riga.** Il verso, la frase, il paragrafo, o la parola — nell'acrostico per parole ogni parola conta come una riga.
- **Quanto si vuole che si veda.** È la stessa parte mobile che la voce 122, acrostico ha isolato, e decide se l'acrostico sia una firma o un nascondiglio.
- **Se il testo di superficie deve stare in piedi.** Sempre: altrimenti la colonna verticale è l'unica cosa che c'è, e non nasconde niente.

## Da dove viene

La storia antica sta nella voce 122, acrostico. Qui interessa il ramo italiano, che `it-acrostico.txt` percorre per intero.

Nel medioevo italiano l'acrostico è una firma o una dedica: Boccaccio dedicò l'*Amorosa visione* a Maria d'Aquino con l'acrostico formato dai capoversi delle terzine, e il sonetto 5 del *Canzoniere* di Petrarca — «Quando io movo i sospiri a chiamar voi» — è uno dei componimenti acrostici medievali più noti. Nell'Ottocento diventa una parola d'ordine politica: la scritta *Viva V.E.R.D.I.*, che alcuni patrioti avrebbero scritto sui muri di Modena nel 1859, dissimula *Viva Vittorio Emanuele Re D'Italia*. Nel Novecento entra a scuola come mnemotecnica: *Ma con gran pena le reca giù* per le sezioni delle Alpi — Marittime, Cozie, Graie, Pennine, Lepontine, Retiche, Carniche, Giulie —, che è un acrostico per sillabe e non per lettere.

Il gioco a schema, quello che si compra in edicola, ha invece una data precisa e non è italiano. `acrostic-puzzle.txt`, presa il 1 settembre 2026, attribuisce l'invenzione a Elizabeth Kingsley, sulla *Saturday Review* nel **1934**, con il nome *double-crostic*. Kingsley, Doris Nash Wortman e Thomas Middleton lo portarono sul *New York Times* dal 1952 al 1999, con una cadenza dichiarata di non più di uno ogni due settimane.

## Varianti e parenti

- **Acrostico** (voce 122, acrostico) — **il confine da dichiarare**: lì la forma letteraria, la sua storia biblica e classica, il suo uso come firma e come nascondiglio; qui lo schema come lo classifica l'enigmistica italiana, il ramo italiano della sua storia, e il gioco a schema del Novecento.
- **Mesostico, telestico** (voce 350, mesostico, telestico) — la stessa cosa con le lettere centrali o finali. Le tre si trovano spesso insieme nello stesso componimento.
- **Abecedario** — l'acrostico che scandisce l'alfabeto, e il più antico.
- **Acrostico per parole** — le iniziali delle parole invece che dei versi: *Viva V.E.R.D.I.* è di questa specie.
- **Notarikon** — il metodo con cui la cabala ricava una parola dalle iniziali di altre, che `it-notarikon.txt` accosta alla formazione di un acronimo e mette accanto a ghematria e temurah come uno dei tre metodi antichi.
- **Anacrostico (double-crostic)** — il gioco a schema: un elenco di definizioni numerate e una citazione a caselle, e le iniziali delle risposte compongono autore e titolo.
- **Quadrato del Sator** — un acrostico che si legge nei due sensi e in tutte e due le direzioni; `word-square.txt` scrive che un quadrato di parole è un tipo di acrostico.
- **Steganografia** (voce 135, steganografia) — la famiglia in cui finisce quando serve a nascondere.
- **Poesia enigmatica** (voce 339, poesia enigmatica) — dove il *Viva V.E.R.D.I.* è già stato usato, come esempio di consegna che sta fuori dal foglio.

## Che cosa se ne sa

**La colonna verticale è lunga quanto il numero delle righe, e non dipende da quanto le righe siano lunghe.** Detto così sembra ovvio e non lo è: vuol dire che allungare i versi non allunga la parola nascosta, la diluisce. Contato in `build/check_346.py` sui due componimenti che `it-telestico.txt` riporta per esteso, le lettere lette in verticale sono il **5,6%** del totale in tutti e due i casi. Un acrostico è un testo intero speso per una parola, ed è il rapporto peggiore fra materiale e messaggio di tutto il capitolo 12.

**In compenso la posizione non va cercata: la dichiara la forma.** È il conto che ordina questa sezione, ed è nella tabella di `OSSERVAZIONI.md`: nel rebus della voce 346, rebus le spartizioni possibili delle 22 lettere sono 2 097 152 e il diagramma ne lascia una; qui la posizione possibile è **una sola** e non serve dichiararla, perché è la prima lettera di ogni riga e la sa chiunque. **L'acrostico è la forma più economica della sezione: costa zero al foglio e zero a chi risolve.** Quello che costa è accorgersi che c'è.

**E accorgersene è quasi gratis, se qualcuno dice di guardare.** Nella scheda qui sotto due testi di sette righe fanno 413 lettere; per decidere quale dei due nasconde qualcosa se ne guardano quattordici, cioè il 3,4%. Contato in `build/blocco_346.py`. La difficoltà di un acrostico non sta nella verifica, che è banale, ma nell'ipotesi: senza il sospetto, quelle quattordici lettere non le guarda nessuno.

**Il gioco a schema conserva le lettere, come una crittografia.** `acrostic-puzzle.txt` spiega perché si chiami anche *anacrostico*: è la fusione di *anagram* e *acrostic*, «perché la soluzione è un anagramma delle risposte alle definizioni». Cioè le lettere della citazione e quelle delle risposte sono le stesse, contate. È la stessa conservazione della sezione 12.4 e per una ragione diversa: là le lettere restavano perché si spostavano solo gli spazi, qui perché le caselle sono numerate.

**Sul sistema, questa voce sposta il confine e non lo supera.** La voce 122, acrostico aveva ipotizzato che l'acrostico fosse l'unica forma di lettere che il sistema sappia costruire, perché l'unica lettera da maneggiare è la prima di una riga, cioè un confine e non un interno. L'ipotesi resta **da verificare** — la prova è chiedere una decina di acrostici e guardare la colonna di sinistra, e non è stata fatta. Quello che si può dire adesso è più preciso: **se l'ipotesi regge, regge per l'acrostico e per il telestico e non per il mesostico**, perché il mesostico chiede una lettera in mezzo a una parola. Il confine del limite tecnico cade dentro questo blocco, fra questa voce e la voce 350, mesostico, telestico.

## Esempi trovati

Da Boccaccio: i capoversi delle terzine dell'*Amorosa visione* compongono la dedica a Maria d'Aquino.

Da Petrarca: il sonetto 5 del *Canzoniere*, «Quando io movo i sospiri a chiamar voi».

Da Modena, 1859: *Viva V.E.R.D.I.* per *Viva Vittorio Emanuele Re D'Italia* — un acrostico per iniziali di parola, e non di verso.

Dalla scuola: *Ma con gran pena le reca giù*, per le otto sezioni delle Alpi. È un acrostico per sillabe, ed è probabilmente il più recitato in Italia.

Dalla Bibbia ebraica, Ester 5,4: nell'espressione «Venga oggi il re con Aman» le iniziali delle quattro parole ebraiche formano il tetragramma. `it-acrostico.txt` aggiunge un dettaglio che vale per noi: tre antichi manoscritti evidenziano quelle iniziali in maiuscolo, e la masora le segnala in rubrica, cioè in rosso. **Il testo non basta: serve un segno tipografico che dica dove guardare.**

Da Douglas Hofstadter: *Gödel, Escher, Bach* fa ampio uso dell'acrostico.

Dal 1934: il *double-crostic* di Elizabeth Kingsley, che Isaac Asimov preferiva ai cruciverba — «i Crostici non hanno il pubblico dei cruciverba, perché sembrano difficili. Non lo sono, e sono infinitamente più interessanti».

## Una nostra versione

Il gioco vero dell'acrostico non è comporlo: è accorgersi che c'è. La scheda mette due testi accanto e chiede quale dei due nasconde qualcosa, che è una domanda con una risposta sola e che nessuno pone mai.

> **Uno dei due nasconde una parola**
>
> Sono due biglietti come tanti. In uno di loro, se leggi in verticale la prima lettera di ogni riga, esce una parola. Nell'altro no.
>
> ```
>  UNO
>
>  Sul tavolo resta il piatto di ieri sera.
>  Tutti dicono che non e' colpa di nessuno.
>  Ancora una volta il gatto e' entrato in casa.
>  Sono le sei e non ha smesso di piovere.
>  E la luce del corridoio continua a spegnersi.
>  Resta da capire chi ha spostato la chiave.
>  Adesso non ne parliamo piu'.
>
>  DUE
>
>  Oggi ho trovato la matita sotto il divano.
>  Non era dove l'avevo lasciata.
>  Tutte le volte succede la stessa cosa.
>  E nessuno ammette di averla presa.
>  La prossima volta la lego al tavolo.
>  Un giorno capiro' chi e' stato.
>  Adesso vado a fare merenda.
>
>  Quale dei due nasconde una parola?  ---
>  La parola e':  -------------------------
>  Lettere che hai dovuto guardare:  ---  su 413
> ```
>
> L'ultima riga è la parte seria. Fra i due biglietti ci sono quattrocentotredici lettere; per rispondere ne servono quattordici. **Il problema di un acrostico non è controllarlo: è pensare di controllarlo.**
>
> Nel 1859, a Modena, qualcuno scriveva *Viva V.E.R.D.I.* sui muri. Chi passava leggeva il nome di un compositore.

La verifica sta tutta nel materiale, e la risposta è unica: uno dei due testi dà una parola italiana, l'altro dà `ONTELUA`. Non serve un foglio delle soluzioni e non serve nessuno.

Il numero finale non è un abbellimento: è la cosa che la scheda insegna. Tutte le altre forme di questo capitolo si difendono rendendo difficile la verifica; l'acrostico si difende rendendo difficile il sospetto, ed è un modo di nascondere che costa meno di tutti gli altri.

Dove si romperebbe: sul display da quattro righe per quarantaquattro caratteri ci sta mezzo biglietto, quindi la scheda è di carta. In compenso quattro righe di display sono esattamente un acrostico di quattro lettere, e questa è una cosa da provare.

## Da riprendere alla rassegna

**La riga di differenza.** Questa voce e la voce 350, mesostico, telestico stanno su una variabile diversa da quella delle prime tre della sezione: non «di che cosa è fatto l'esposto», ma **dove sta la lettera che si legge, e chi lo dichiara.** Qui sta all'inizio della riga e lo dichiara la forma stessa; alla voce 350, mesostico, telestico sta alla fine — e lo dichiara ancora la forma — oppure in mezzo, e allora non lo dichiara nessuno. La voce 351, frase bipartita non sta su nessuna delle due variabili, e lo dice dentro di sé. Il termine di paragone delle prime tre è la voce 346, rebus.

**È la forma più economica del capitolo, e costa zero in tutte e due le direzioni.** Chi compone non deve contare niente, chi risolve non deve cercare niente. Alla rassegna vale la pena tenerla accanto al censimento del controllo dell'errore come caso limite: la verifica è nel materiale e si fa con un dito, e il costo è tutto spostato sull'ipotesi.

**Il segno tipografico che dice dove guardare è antico quanto la forma.** Tre manoscritti biblici mettono in maiuscolo le iniziali che contano, e la masora le scrive in rosso. Il progetto stampa in bianco e nero e non ha il rosso, ma ha il maiuscolo e la spaziatura, e sono la stessa leva. Da segnare accanto alla voce 122, acrostico, dove la stessa cosa era stata notata come parte mobile e non come tradizione.

**Una forma può essere dichiarata desueta dalla sua disciplina e restare la più usata fuori.** L'enigmistica italiana mette l'acrostico fra gli schemi «desueti o rari»; intanto lo recitano tutte le classi d'Italia per le Alpi, e lo usano le lettere di dimissioni. **Quando una fonte tecnica dice che una forma non si usa più, conviene chiedersi dove sia andata.**
