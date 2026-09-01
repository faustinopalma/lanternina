# Antipodo

- **Numero** 321 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che tolgono, aggiungono o cambiano lettere»
- **Si chiama anche** antipodo diretto, antipodo inverso, antipodo sillabico, antipodo palindromo, antipodo bifronte, cambio di antipodo, nodo, anagramma dell'avvenire
- **In una riga** si sposta la prima lettera in fondo o viceversa: *amaro → maroa*.
- **Contratto** voce breve
- **Fonti** `it-antipodo.txt`, `it-scambio.txt`, `damerau-levenshtein-distance.txt`, prese il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Che cosa cambia nella parola: niente, le lettere restano tutte. Che cosa cambia: il loro ordine. Che cosa deve restare vero dopo: che venga fuori un'altra parola italiana. Le tre righe valgono per le quattro voci di trasposizione di questo blocco, e la terza è la stessa per tutte.

La regola sta in una riga: **si tiene ferma la prima lettera e si scrive al rovescio tutto il resto.** *Ballo* dà *bolla*. La fonte la enuncia in due tempi — si porta la prima lettera in fondo, poi si legge tutto a rovescio — e i due modi danno la stessa cosa, come si vede su *minate → inatem → metani*, che è *M-inate / M-etani*. L'antipodo inverso fa il contrario: ferma l'ultima lettera, al rovescio tutto il resto. *Marte* dà *trame*.

**La glossa dell'elenco è sbagliata a metà, e vale la pena dirlo.** *Amaro → maroa* si ferma al passo intermedio e lo chiama risultato: l'antipodo di *amaro* è *aoram*, e l'inverso è *ramao*. Nessuno dei due è una parola, quindi *amaro* non ha antipodo — il che è il caso normale, non l'eccezione.

L'antipodo è la forma in cui la variabile di questo blocco prende il **valore più povero**: non si sceglie che cosa muovere, perché la mossa è decisa dalla parola. Da una parola escono due stringhe e due sole, sempre, qualunque sia la sua lunghezza. Le altre tre trasposizioni si descrivono per differenza da qui.

Parti mobili: diretto o inverso; a lettere o a sillabe; e se ci si aggiunge un'altra operazione — cambiando la lettera che si sposta si ha il cambio di antipodo.

## Da dove viene

Dall'enigmistica italiana dell'Ottocento, con una data. `it-antipodo.txt` registra che lo schema comparve per la prima volta nel **1878**, sulle pagine de *L'Aguzzaingegno*, sotto il nome di **anagramma dell'avvenire**; il nome attuale glielo diede l'enigmista Ugone di Soana. Il cambio di antipodo nacque lo stesso anno e si chiamava **nodo**. La fonte appoggia la ricostruzione su un articolo di Stefano Bartezzaghi su *la Repubblica* del 7 gennaio 2005, consultato in copia archiviata.

Il nome dice la cosa giusta: gli antipodi sono i due punti opposti di una sfera, e qui la parola viene letta dalla parte opposta tenendo fermo un capo.

## Varianti e parenti

- **Antipodo inverso** — si tiene ferma l'ultima lettera invece della prima.
- **Antipodo sillabico** — l'unità è la sillaba, e anche la lettura a rovescio è sillabica: *balena / banale*.
- **Antipodo palindromo** — il caso in cui la lettura a rovescio coincide con quella diretta e la parola torna sé stessa: *mottetto*, *minimo*, *sasso*.
- **Cambio di antipodo** — l'antipodo più un cambio di lettera: *dottore / cerotto*.
- **Bifronte** (333) — la lettura inversa senza nessuna lettera tenuta ferma. L'antipodo è un bifronte a cui si sottrae una lettera dal giro.
- **Palindromo** (334) — la parola che coincide con la propria lettura inversa; è il caso in cui l'antipodo palindromo diventa banale.
- **Anagramma** (331) — la fonte dice che ogni schema enigmistico senza scarto si riconduce all'anagramma, e l'antipodo è uno di quelli: le lettere sono le stesse, cambia l'ordine.
- **Scambio** (318) — l'altra trasposizione che non tocca la lunghezza, ma con le posizioni da scegliere.

## Che cosa se ne sa

`it-antipodo.txt`, presa il 1 settembre 2026, è una pagina di repertorio con una nota bibliografica sola, e non dà nessuna misura. Gli otto esempi che elenca sono stati rifatti applicando la regola, e tornano tutti e otto, compresi i due che cumulano l'antipodo con un cambio (`build/check_318.py`).

Il numero che questa voce porta è la dimensione dello spazio di ricerca, ed è **due**. Non due su una parola breve e di più su una lunga: **due sempre.** È l'unica forma del capitolo 12 in cui lo spazio non cresce con la parola. Sulla stessa parola di otto lettere, *maschera*, lo scambio dà 27 stringhe diverse e lo spostamento 47.

Da qui segue una proprietà che si può scoprire su un foglio: **l'antipodo restituisce la parola di partenza esattamente quando ciò che segue la prima lettera si legge uguale nei due sensi.** *Mottetto* è *m* più *ottetto*, e *ottetto* è palindromo. Verificato come equivalenza — non solo sui casi che tornano, ma anche su quelli che non tornano — in `build/check_318.py`.

Il limite del capitolo vale anche qui: **il sistema non sa manipolare le lettere dentro le parole** (`ideas/10 §6`). Ma con due candidati soli il sistema non serve, perché non c'è niente da cercare.

## Esempi trovati

Da `it-antipodo.txt`, riscritti: *ballo / bolla*; antipodo inverso *Marte / trame*; sillabico *balena / banale*; palindromo *mottetto*, e palindromo inverso *minimo*; sillabico palindromo *sasso*. E i due che cumulano un cambio: *dottore / cerotto*, *acceso / seccai*.

Da `it-scambio.txt`: lo scambio di estremi *astio / ostia* è la trasposizione confinante, ed è quella con cui l'antipodo si confonde più facilmente — lì si scambiano la prima e l'ultima lettera, qui si rovescia tutto il resto.

## Una nostra versione

> **Ogni parola ne ha due, non una di più**
>
> Tieni ferma la prima lettera e scrivi al rovescio tutto il resto: BALLO diventa B + OLLA. Poi rifallo tenendo ferma l'ultima. Sono le sole due strade, e le fai tutte e due in dieci secondi.
>
> ```
>  PAROLA     ANTIPODO    INVERSO
>  BALLO      ─────────   ─────────
>  MARTE      ─────────   ─────────
>  CARTA      ─────────   ─────────
>  AMARO      ─────────   ─────────
>  MOTTETTO   ─────────   ─────────
> ```
>
> Cerchia quelle che sono parole italiane. Su dieci caselle ne troverai due.
>
> Una riga ti darà un risultato strano: **la parola stessa.** Non è un errore ed è la parte interessante. Guarda che cosa hanno di speciale le lettere che hai rovesciato, e scrivi qui la regola:
>
> ```
>  ────────────────────────────────────────────────
> ```
>
> Poi trovane un'altra che si comporti allo stesso modo.

Le dieci caselle **sono lo spazio di ricerca per intero**, e questa è l'unica forma del capitolo in cui una tabella di cinque righe lo esaurisce. La bassa resa — due su dieci — è dichiarata prima, così che il vuoto sia un risultato e non un fallimento.

La seconda parte non chiede una parola: chiede una regola, e la regola è vera, dimostrabile e alla portata di chi legge. È il pezzo che il sistema non potrebbe né porre né correggere, e che il foglio porta senza sforzo.

Dove si romperebbe: il giudizio «questa è una parola italiana» resta fuori dal sistema, e in casa un vocabolario non è garantito. Che *bolla* e *trame* siano le sole due delle dieci è un giudizio nostro, dichiarato come tale in `build/check_318.py`.

## Da riprendere alla rassegna

**Uno spazio di ricerca costante, non piccolo: costante.** Alla voce 314, scarto lo spazio era lineare nella lunghezza della parola e quindi stampabile; qui non dipende dalla parola affatto. Da cercare altrove nell'elenco quante forme abbiano questa proprietà, perché è quella che rende il limite tecnico del capitolo del tutto irrilevante.

**Il termine di paragone di questo blocco.** Le quattro trasposizioni — voce 318, scambio, voce 319, spostamento, voce 320, metatesi e questa scheda — differiscono in una cosa sola: **quanto si sceglie di ciò che si muove.** Qui non si sceglie niente. Le altre tre aggiungono una scelta, e ognuna si può descrivere in una riga di differenza da qui.

**Il valore di una voce e la grandezza del suo spazio di ricerca non vanno insieme.** Questa è la forma con meno libertà del blocco ed è quella con più cose dentro: una data, un nome scartato, sei varianti nominate e un punto fisso dimostrabile. Da tenere presente alla rassegna, dove la tentazione sarà di ordinare le forme per quanto lasciano fare.

**La verifica sta in un vocabolario**, come per tutto il capitolo, e non in una delle cinque classi del censimento del controllo dell'errore. Qui però è dimezzata: la seconda domanda del foglio — quale sia la regola del punto fisso — si verifica da sé, perché chi la scrive la può provare su altre parole.
