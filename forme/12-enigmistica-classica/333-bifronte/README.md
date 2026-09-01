# Bifronte

- **Numero** 333 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che uniscono o dividono parole»
- **Si chiama anche** parola rovesciabile, lettura inversa, *anacyclique*, *semordnilap*, bifronte a frase, frase bifronte, bifronte sillabico
- **In una riga** una parola che letta al rovescio ne dà un'altra: *amor / Roma*.
- **Fonti** `it-bifronte-vero.txt`, presa il 1 settembre 2026. La prima stesura di questa scheda, del 30 agosto 2026, non aveva nessuna fonte locale e lo dichiarava; quello che segue è stato controllato su quella pagina, salvo dove si dice il contrario
- **Stato della ricerca** fatta, 30 agosto 2026; ampliata il 1 settembre 2026

## Che cos'è

Una parola che, letta al rovescio, ne dà un'altra. *Amor* e *Roma*. *Erba* ed *abre*, no: deve essere una parola vera anche l'altra.

Si distingue dal palindromo, che al rovescio dà sé stesso. Il bifronte dà qualcos'altro, ed è per questo più raro e più usabile come gioco: due parole al prezzo di una.

Parti mobili:

- **Se il rovesciamento è di lettere o di sillabe.** Il *bifronte sillabico* rovescia le sillabe e non le lettere, ed è molto più abbondante.
- **Se le due parole hanno un rapporto.** *Amor / Roma* è celebre perché il rapporto c'è.
- **Se si rovescia una frase intera** invece di una parola.
- **Se il rovesciamento è nella scrittura o nel suono.** Sono due giochi diversi che si confondono spesso.

## Da dove viene

Tradizione enigmistica italiana. *Roma / Amor* è un topos medievale con una letteratura sua, usato in iscrizioni e in poesia molto prima di essere un gioco.

`it-bifronte-vero.txt`, presa il 1 settembre 2026, dà la data che mancava: l'enigmistica italiana ha **ufficializzato nel 1932** la distinzione fra bifronte e palindromo, estendendola all'antipodo. La pagina aggiunge che la distinzione «fatica a venir accolta dai dizionari» per la sua settorialià, e smonta una convinzione corrente: **non è una specialità italiana.** Il francese lo chiama *anacyclique*, l'inglese *semordnilap*, che è la parola *palindromes* scritta al rovescio.

Ha un parente antichissimo nella **scrittura bustrofedica** — righe che vanno alternativamente da sinistra a destra e da destra a sinistra, come ara un bue — usata in greco arcaico e in etrusco. Lì il rovesciamento non era un gioco: era il modo di scrivere.

## Varianti e parenti

- **Palindromo** (334) — al rovescio dà sé stesso invece di un'altra parola. La distinzione è del 1932.
- **Bifronte a frase** e **frase bifronte** — il rovesciamento produce una frase, o parte da una: *animale = è la mina*, *amori di dea = aedi di Roma*.
- **Bifronte senza capo** — si scarta la prima lettera e poi si rovescia: *tartina* dà *anitra*.
- **Bifronte senza coda** — si scarta l'ultima: *attesa* dà *setta*.
- **Bifronte senza estremi** — si scartano tutte e due: *esubero* dà *rebus*. La fonte lo chiama anche, per gioco, *bifronte senza capo né coda*.
- **Bifronte a cambio di capo** — con una lettera sostituita. La fonte lo dice infrequente.
- **Bifronte sillabico** — si rovesciano le sillabe e non le lettere: *losca nomea = ameno scalo*, che a lettere non funziona affatto.
- **Anagramma** (331) — riordinamento libero invece che rovesciamento.
- **Antipodo** (321) — la prima lettera va in fondo: un rovesciamento parziale.
- **Ambigramma** — una scritta che letta capovolta dice la stessa cosa, o un'altra. È il bifronte in forma grafica.
- **Scrittura speculare** — Leonardo, e i testi che si leggono allo specchio.
- **Bustrofedico** — il rovesciamento come sistema di scrittura.

## Che cosa se ne sa

La prima stesura di questa scheda, il 30 agosto 2026, dichiarava che nessuna delle 74 fonti prese quel giorno trattava il bifronte come gioco codificato, e che definizione e varianti venivano dalla memoria. `it-bifronte-vero.txt`, presa il 1 settembre 2026, le copre tutte e due: colloca il bifronte nella **famiglia delle letture inverse**, dà la data del 1932, i nomi stranieri e sette varianti. Rifatti a macchina in `build/check_334.py`: i dieci bifronti di parola e i quattro a frase della pagina tornano tutti, e **nessuno di essi è anche un palindromo**, che è il controllo che rende la distinzione del 1932 verificabile invece che dichiarata.

Una cosa la fonte la dice e vale la pena rifarla: **il bifronte sillabico non è un bifronte con un'unità diversa, è un altro gioco.** *Losca nomea* e *ameno scalo* sono lo stesso testo a sillabe rovesciate, e a lettere non hanno niente in comune — controllato.

Due osservazioni restano dalla prima stesura.

**Il rovesciamento è fra le operazioni sulle lettere quella che un modello sbaglia più spesso**, insieme al conteggio. Il sistema non può costruire bifronti e non può verificarli.

**Ma il rovesciamento ha una forma fisica**, e questa è la parte interessante. Uno specchio rovescia. Un foglio girato in controluce rovescia. Un testo scritto su un vetro e guardato dall'altra parte rovescia. Nessuna di queste richiede al sistema di sapere in che ordine stanno le lettere: richiede a chi gioca di procurarsi uno specchio, e lo specchio è esatto.

Questa è la differenza fra chiedere a un modello di manipolare simboli e chiedere al mondo di farlo, ed è la stessa mossa vista alla voce 326, lucchetto con le strisce di carta.

## Esempi trovati

*Roma / Amor*, che è il caso celebre.

*Ella / alle*, *era / are*, *enoteca / acetone*: la tradizione ne ha cataloghi.

Da `it-bifronte-vero.txt`, riscritti e rifatti tutti in `build/check_334.py`: *Adige / egida*, *amitto / ottima*, *arco / ocra*, *eraso / osare*, *idem / medi*, *onagro / organo*, *Suez / Zeus*, *Ares / sera*. E a frase: *animale = è la mina*, *Italia = ai lati*, *Isabella = alle basi*, *amori di dea = aedi di Roma*.

Dalla stessa pagina, le versioni con lo scarto: *tartina* dà *anitra* togliendo il capo, *attesa* dà *setta* togliendo la coda, *esubero* dà *rebus* togliendoli tutti e due.

Da Leonardo: la scrittura speculare dei taccuini, che si legge con uno specchio ed è il bifronte applicato a interi quaderni.

Dagli ambigrammi di Scott Kim e Douglas Hofstadter: scritte progettate per leggersi anche capovolte.

Dalle ambulanze: la scritta rovesciata sul cofano, che si legge nello specchietto retrovisore. È un bifronte con uno scopo pratico e nessuno lo chiama così.

## Una nostra versione

> **Il quaderno che si legge allo specchio**
>
> Leonardo scriveva così tutti i suoi taccuini. Non si sa perché: forse per non farsi leggere, forse perché era mancino e non sbavava l'inchiostro.
>
> Scrivi **una riga sola** in modo che si legga solo allo specchio. Comincia da destra e fai ogni lettera al contrario.
>
> ```
>  ──────────────────────────────────────────
> ```
>
> Sarà più difficile di quanto sembra, e verrà storta. La sua veniva storta per i primi vent'anni.
>
> Poi va' allo specchio e leggila. Se è sbagliata da qualche parte, lo vedi subito — ed è l'unico modo che c'è di accorgersene.

Lo specchio è il correttore, e non ha opinioni. Il sistema non deve costruire niente e non deve verificare niente: deve solo raccontare Leonardo in due righe e stampare una riga vuota. «La sua veniva storta per i primi vent'anni» è falso alla lettera e vero nella sostanza, e va sostituito con qualcosa di verificabile prima di stamparlo davvero.

## Da riprendere alla rassegna

**Il mondo come processore di simboli.** Uno specchio, una piega, la controluce, un foglio girato: sono operazioni esatte su lettere che il sistema non saprebbe fare. Da censire alla rassegna tutte le forme del capitolo 12 che hanno un equivalente fisico — sembrano essere più di quante si direbbe, e sarebbero la via d'accesso a una famiglia che altrimenti è chiusa per intero.

**Attenzione all'aneddoto che si racconta bene.** «Veniva storta per vent'anni» funziona come consegna e non è verificato. La tentazione di scrivere una cosa vera-abbastanza è forte proprio nelle consegne brevi, dove nessuno metterebbe una nota.

**Una voce senza fonti può restare giusta, ed è un caso e non un metodo.** Questa scheda è stata scritta il 30 agosto 2026 a memoria e dichiarandolo; il 1 settembre è arrivata `it-bifronte-vero.txt`, e la definizione, la distinzione dal palindromo e la variante sillabica reggono tutte. Quello che mancava non erano errori ma **fatti**: la data del 1932, i nomi francese e inglese, le quattro varianti con lo scarto di un estremo. Alla rassegna vale la pena guardare quante delle voci marcate *va verificato* stiano così, cioè non sbagliate ma povere.

Da verificare: la ragione della scrittura speculare di Leonardo (le due ipotesi correnti sono segretezza e mancinismo, e non è chiaro quale regga).
