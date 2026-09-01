# Cruciverba crittografato

- **Numero** 354 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Griglie»
- **Si chiama anche** parole crociate crittografate, aneddoto crittografato, cipher crossword, codeword, Code Breaker, Kaidoku
- **In una riga** ogni lettera è un numero, e non ci sono definizioni.
- **Contratto** voce breve
- **Fonti** `it-cruciverba.txt` e `it-settimana-enigmistica.txt`, prese il 1 settembre 2026; `crossword.txt`, presa il 30 agosto 2026 e riletta. La pagina `Cruciverba crittografato` non esiste in italiano e `Cipher crossword` in inglese rimanda a `Crossword`, controllato il 1 settembre 2026 con `build/check_titoli_352.py`: la trattazione sta dentro le due pagine generali
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Il cruciverba della voce 352, cruciverba **senza le definizioni**. La griglia c'è, ogni casella bianca porta un numero, caselle con lo stesso numero contengono la stessa lettera, e numeri diversi stanno per lettere diverse. Non c'è niente da sapere: c'è da decifrare.

**La glossa dell'elenco è giusta**, e vale la pena scriverlo, perché nel capitolo 12 le righe in cui glossa e fonti non coincidono sono già quindici, elencate in `OSSERVAZIONI.md`. `it-cruciverba.txt`, presa il 1 settembre 2026: «è un tipo di parole crociate in cui le parole non sono descritte da definizioni: ogni casella bianca è numerata e a numero uguale corrisponde lettera uguale».

**La stessa pagina però enuncia al rovescio la condizione che rende il gioco risolvibile.** Scrive: «Ovviamente non esiste il caso che una lettera sia presente in due caselle diverse», che è falso come sta scritto — una lettera sta in tutte le caselle che portano il suo numero. Quello che intende dirlo è che due numeri diversi non possono valere la stessa lettera, cioè che la corrispondenza è biunivoca, e `crossword.txt` lo formula per esteso e senza ambiguità: «no two numbers stand for the same letter». Si tiene la formulazione inglese e si dichiara che l'italiana è scritta male.

Parti mobili:

- **Quanto viene regalato.** Nella tradizione italiana si dà una parola intera in grassetto; in quella inglese almeno una lettera. Nella variante «parole crociate senza definizioni» la lettera data è priva di numero, e la soluzione si ricava dalla sola combinazione dei numeri chiave — per esempio una parola che ha la stessa lettera al primo, al terzo e al quinto posto.
- **Se l'alfabeto è tutto usato.** `crossword.txt` dice che i crittografati inglesi sono quasi sempre pangrammatici, cioè usano tutte e ventisei le lettere, e che per questo conviene cominciare cercando dove stiano la Q e la U.
- **Quanto è grande.** Esiste in versione mini e in versione gigante: l'*aneddoto crittografato* occupa due pagine e racconta un fatto realmente accaduto a un personaggio della storia, della musica o della letteratura.

## Da dove viene

`crossword.txt`, riletta il 1 settembre 2026, lo dà come inventato in Germania nell'Ottocento, pubblicato poi sotto vari nomi commerciali — *Code Breakers*, *Code Crackers*, *Kaidoku* — e avverte di non confonderlo con il cruciverba crittico, che è un'altra cosa: là gli enigmi sono le definizioni, qui le definizioni non ci sono.

La stessa pagina nota che questi schemi «sono più vicini a un codice che a un questionario» e chiedono un'abilità diversa: determinare quali numeri siano vocali è una tecnica crittografica elementare, e serve. `it-settimana-enigmistica.txt` registra le *Parole crociate crittografate* fra i giochi sempre presenti sulla rivista, ma a collocazione variabile.

## Varianti e parenti

- **Cruciverba** (voce 352, cruciverba) — **la riga di differenza**: là il foglio dichiara il disegno e le domande, qui il disegno e una parola sola.
- **Cruciverba senza schema** (voce 353, cruciverba senza schema) — l'altro modo di togliere: là sparisce il disegno invece delle domande.
- **Cifrario a sostituzione** (voce 129, cifrario a sostituzione) — il ponte diretto: questo gioco è una sostituzione monoalfabetica in cui il testo cifrato è disposto in griglia e la griglia fa da controllo.
- **Cruciverba crittico** (voce 126, cruciverba crittico) — da non confondere, e la fonte lo dice esplicitamente.
- **Aneddoto crittografato** — la versione gigante su due pagine, con un fatto vero al posto delle parole sparse.
- **Parole crociate senza definizioni** — la variante in cui la lettera regalata non porta numero.
- **Zigzag, kakuro, crossnumber** (voce 358, zigzag, kakuro, crossnumber) — la forma vicina in cui i numeri nelle caselle non sono un codice ma quello che va scritto.
- **Steganografia** (voce 135, steganografia) — il parente lontano: là il messaggio si nasconde dentro un altro, qui si nasconde dietro una corrispondenza.

## Che cosa se ne sa

**Il conto della voce misura quanto vale la lettera regalata, e su una croce minuscola vale già molto.** In `build/check_352.py`, sulla croce di due parole italiane di cinque lettere che si incontrano sulla terza: **9 caselle**, 6 numeri distinti, alfabeto italiano di 21 lettere. Le corrispondenze possibili sono 21·20·19·18·17·16 = **39 070 080 corrispondenze**; regalando la lettera di un numero ne restano 1 860 480, cioè un fattore 21 esatto — che è il numero delle lettere, come dev'essere.

**Ma il conto dice anche perché il gioco vero non può essere piccolo.** Su una croce di due parole quelle 1 860 480 corrispondenze non si riducono a una: molte danno due parole italiane, e non c'è modo di scegliere. Quello che chiude il problema non è il regalo, è la **quantità di incroci**: solo quando le parole sono molte e si incontrano più volte, la richiesta che tutte siano parole vere lascia una corrispondenza sola. Il regalo serve a cominciare, non a finire. Verificato per costruzione: la croce stampata più sotto ammette più di una lettura, e la scheda lo dichiara invece di fingere il contrario.

**Le frequenze delle lettere sono lo strumento, e sono la stessa cosa della voce 129, cifrario a sostituzione.** `crossword.txt` lo dice in una riga: «molte tecniche crittografiche di base, come determinare quali siano probabilmente le vocali, sono decisive per risolverli». La differenza con un crittogramma nudo è che qui la griglia fa da secondo controllo: una lettera sbagliata rompe una parola perpendicolare, e si vede.

**Il pangramma è un vincolo dichiarato che serve a chi risolve.** Dire che tutte e ventisei le lettere compaiono è un'informazione: quando ne restano poche, si sa che devono esserci ancora tutte, e le più rare — Q, X, Z — hanno posizioni obbligate. È lo stesso genere di mossa dell'acrostico della voce 349, acrostico e delle maiuscole del mesostico: dichiarare accanto alla domanda una proprietà che la risposta deve avere, senza rivelarla.

**Il sistema può stampare un crittografato ma non può costruirne uno buono.** Sostituire una lettera con un numero non chiede di guardare dentro le parole quando la sostituzione la fa uno script: si applica a una griglia già scritta. Costruire la griglia sì. Quella stampata più sotto è stata composta a mano e verificata in `build/blocco_352.py`, che controlla che ogni casella porti il numero della sua lettera e che due lettere non condividano un numero.

## Esempi trovati

Dalla tradizione italiana: si regala una parola intera in grassetto, e si parte dalla corrispondenza fra i suoi numeri e le sue lettere.

Dalla tradizione inglese: si regala almeno una lettera, e siccome la soluzione è quasi sempre pangrammatica il punto di partenza consigliato è cercare dove debbano stare la Q e la U — che in inglese vanno quasi sempre insieme e in quell'ordine.

Dalla variante senza definizioni: la lettera data è priva di numero, e si entra da uno schema come «una parola che ha la stessa lettera al primo, al terzo e al quinto posto».

Dall'*aneddoto crittografato*: due pagine, un fatto realmente accaduto a un personaggio noto, e nessuna definizione.

## Una nostra versione

> **Sei numeri e una lettera**
>
> ```
>  Caselle con lo stesso numero, lettera uguale.
>  Numeri diversi, lettere diverse.
>
>    |   |   | 3 |   |   |
>    |   |   | 7 |   |   |
>    | 5 | 1 | 2 | 9 | 7 |
>    |   |   | 9 |   |   |
>    |   |   | 7 |   |   |
>
>    Si sa soltanto che il 7 vale A.
>
>  Le due parole sono italiane e si incrociano sulla
>  terza lettera. Trovale.
> ```
>
> Le corrispondenze possibili fra sei numeri e ventun lettere sono 39 070 080. Sapere che cosa vale il 7 ne toglie venti su ventuno. Le altre le devi togliere tu, e non ci riuscirai fino in fondo: **su una croce così piccola le soluzioni sono più d'una.** Trovane quante puoi, poi disegna tu una griglia più grande e guarda a che punto le soluzioni diventano una sola.

Le nostre due parole sono PORTA in orizzontale e CARTA in verticale, che condividono la R. La scheda non le dichiara uniche, perché non lo sono: ed è questo il contenuto. Un crittografato con nove caselle è un crittogramma; diventa un cruciverba quando gli incroci sono abbastanza da chiudere il conto, e l'ultima riga chiede di trovare dove sia quel punto.

**Dove si romperebbe.** Il sistema non può comporre la griglia: le due parole e la loro lettera comune sono state scelte a mano e verificate da uno script. Può però stampare una griglia già composta e sostituire le lettere con i numeri, che è un'operazione meccanica. Sul pannello da quattro righe la griglia non entra; entra la riga «il 7 vale A», che da sola non dice niente.

## Da riprendere alla rassegna

**Un aiuto può aprire un problema senza chiuderlo, e le due cose vanno contate separatamente.** La lettera regalata toglie venti possibilità su ventuno e non basta; a chiudere è il numero degli incroci, che non è un aiuto ma la forma stessa del gioco. Alla rassegna vale la pena distinguere, in ogni forma, che cosa permetta di *cominciare* da che cosa permetta di *finire*.

**È l'unica forma della sezione in cui non serve sapere niente.** Nel cruciverba servono le definizioni, nel crucintarsio serve riconoscere le parole; qui basta l'alfabeto e un po' di pazienza sulle frequenze. Chi non ha letto molto non è svantaggiato, e questo nell'elenco è raro.

**La riga di differenza.** Rispetto alla voce 352, cruciverba il foglio qui non dichiara le domande, e le sostituisce con una corrispondenza biunivoca e un regalo.

