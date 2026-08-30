# Escludere

- **Numero** 59 nell'enciclopedia, capitolo 2 — Che cosa mette in moto la risposta
- **Si chiama anche** eliminare, scartare, restringere il campo, per esclusione, togliere quelli che non vanno, *process of elimination*, *narrowing down*
- **In una riga** arrivare a una cosa togliendo tutte le altre, un pezzo per volta.
- **Fonti** `_reference/esercizi-e-sfide/twenty-questions.txt`, `binary-search.txt`, `mastermind-board-game.txt`, `single-access-key.txt`, prese il 30 agosto 2026
- **Stato della ricerca** fatta, 30 agosto 2026

## Che cos'è

Arrivare a una cosa togliendo tutte le altre. Non si guarda il bersaglio: si guarda l'insieme, e lo si dimezza finché resta una cosa sola.

Parti mobili:

- **L'insieme di partenza.** Deve essere noto, o almeno delimitato. Senza confini non si esclude niente.
- **La domanda.** Ogni domanda taglia l'insieme in due parti, e la sua qualità sta in quanto sono uguali le due parti.
- **Quante domande si hanno.** Un numero fissato — venti, dieci, tre — trasforma il compito da «trova» a «trova con poche mosse», e sono due cose diverse.
- **Se le risposte sono affidabili.** Con una risposta sbagliata ammessa, il problema cambia natura e diventa quello che in matematica si chiama gioco di Rényi–Ulam.
- **Chi fa le domande.** Il verbo cambia completamente se le domande le pone chi cerca o se sono già stampate.

## Da dove viene

Il gioco delle venti domande è attestato almeno dagli anni 1780: la scrittrice Hannah More annotò di aver insegnato «the play of twenty questions» a una cena londinese in cui c'erano Joshua Reynolds e Lord North (`twenty-questions.txt`, presa il 30 agosto 2026). Venti domande binarie distinguono al massimo 2²⁰, cioè 1.048.576 oggetti, e per questo il gioco viene usato per introdurre la teoria dell'informazione.

La stessa pagina riporta una cosa che vale la pena tenere. Nel 1901 Charles Sanders Peirce discusse le venti domande dentro la sua economia della ricerca e scrisse che «venti ipotesi abili accerteranno quello che duecentomila stupide potrebbero non accertare», e che il segreto sta nello spezzare un'ipotesi nelle sue componenti logiche più piccole, rischiandone una per volta. Non vuol dire chiedere di un milione di soggetti uno alla volta: vuol dire chiedere «l'ha fatto un animale?» prima di chiedere «l'ha fatto un cavallo?».

La versione formale è la ricerca binaria (`binary-search.txt`, stessa data), e la versione da tavolo è *Mastermind*, inventato nel 1970 da Mordecai Meirowitz e pubblicato nel 1971–72 da Invicta Plastics; deriva dal gioco con carta e penna *Bulls and Cows* (`mastermind-board-game.txt`, stessa data). La chiave dicotomica dei naturalisti è l'esclusione messa per iscritto e resa riusabile (`single-access-key.txt`).

## Varianti e parenti

- **Venti domande** — le domande le fa chi cerca, e il costo è dichiarato.
- **Indovina chi?** — le stesse domande, ma l'insieme è stampato e si abbatte fisicamente.
- **Mastermind** — non si esclude con domande ma con tentativi, e il ritorno è parziale.
- **Chiave dicotomica** — le domande sono già scritte, e in un ordine deciso da un altro.
- **Puzzle a griglia** (142) — l'esclusione su una tabella: ogni indizio cancella caselle.
- **Enigma di verità e menzogna** (147) — si escludono mondi, non oggetti.
- **Cercare** (58) — guardare finché si trova, invece di togliere finché resta.
- **Dedurre** (60) — l'esclusione è spesso un modus tollens ripetuto.
- **Raggruppare** (57) — la stessa operazione tenuta invece che scartata.

## Che cosa se ne sa

Da `twenty-questions.txt` (presa il 30 agosto 2026): la strategia migliore è porre domande che dividano a metà le possibilità rimaste, ed è la stessa cosa che fa una ricerca binaria. La pagina segnala anche un limite dell'analogia con il metodo scientifico: un'ipotesi, per la sua ampiezza, può essere più difficile da verificare che da falsificare, o viceversa — nel gioco le due direzioni costano uguale, nella ricerca no.

Da `single-access-key.txt` (stessa data): una chiave dicotomica è più facile da seguire con due alternative che con molte, perché le alternative complesse — quelle con «e», «o», «non» — diventano illeggibili appena sono più di due.

L'osservazione pratica: **la parte interessante dell'esclusione non è la risposta, è la domanda che si è scelto di fare.** Una risposta giusta ottenuta in sedici domande e una ottenuta in cinque dicono cose diverse di chi le ha fatte, e solo la seconda è un ragionamento.

Seconda osservazione: **l'esclusione ha una verifica gratuita**, cioè il conto delle domande. Non serve nessun giudizio per dire se è andata bene; basta un numero, e quel numero si può battere la volta dopo.

## Esempi trovati

Dal gioco *Indovina chi?*: le facce che si abbassano una alla volta, che sono la rappresentazione fisica dell'insieme che si restringe.

Dalla botanica: la chiave dicotomica, dove le domande sono state scelte da qualcun altro secoli fa e chi identifica non le può cambiare.

Da *Mastermind*: l'esclusione con informazione parziale, in cui ogni tentativo dice quanti pioli sono giusti ma non quali.

Dalla medicina: la diagnosi differenziale, che è una chiave dicotomica in cui alcuni rami costano un esame e altri una domanda.

Dalla logica: il *modus tollens*, che è l'esclusione ridotta a una riga sola — se fosse così, allora quello; non è quello, dunque non è così.

## Una nostra versione

> **Cinque domande, non una di più**
>
> Ho pensato a una cosa che c'è in questa casa. È una cosa sola, ed è in una stanza in cui sei entrato oggi.
>
> Hai **cinque domande**. A ognuna rispondo soltanto sì o no. Cinque domande bastano a distinguere trentadue cose, se ognuna taglia a metà quello che resta — e in questa casa di cose ce ne sono migliaia. Quindi non ti basteranno, a meno che le prime due non siano molto grosse.
>
> ```
>  1  ───────────────────────────────────  □ sì  □ no
>     dopo questa domanda restano circa ─────── cose
>  2  ───────────────────────────────────  □ sì  □ no
>     dopo questa domanda restano circa ─────── cose
>  3  ───────────────────────────────────  □ sì  □ no
>     dopo questa domanda restano circa ─────── cose
>  4  ───────────────────────────────────  □ sì  □ no
>     dopo questa domanda restano circa ─────── cose
>  5  ───────────────────────────────────  □ sì  □ no
>     dopo questa domanda restano circa ─────── cose
>
>  La mia risposta:  ────────────────────
>  La domanda che, riguardandola, era sprecata:  la numero ──
> ```
>
> La riga sotto ogni domanda è la parte che serve. Una domanda che lascia in piedi quasi tutto è una domanda buttata, e ci si accorge di averla fatta solo dopo averla scritta.

Il numero di domande fissato rende il compito misurabile senza un giudizio. La stima di quante cose restano è il pezzo che trasforma il gioco in un ragionamento: chiede di valutare la propria mossa mentre la si fa, che è esattamente quello che Peirce chiamava economia della ricerca. La consegna dice in anticipo che cinque domande non basteranno, il che toglie la delusione e sposta l'obiettivo su come si taglia.

Nel nostro formato c'è un limite reale: **serve un'altra persona che risponda sì o no**, e il sistema ne ha una sola. Il foglio può essere stampato e usato con il genitore, e allora funziona; da solo, no. La variante che regge senza secondo giocatore è quella in cui il bersaglio lo sceglie chi gioca e l'insieme è dato — le pagine di un libro, i giorni dell'anno — e le domande servono a battere il proprio record.

## Da riprendere alla rassegna

**Chiedere di stimare quanto una mossa ha ristretto il campo** è una riga che si può aggiungere a molte forme e che nessuna versione scolastica ha. Rende visibile la qualità della domanda, che altrimenti non lascia traccia — come *quello che si è scartato* nelle schede 017 e 049.

**Il costo dichiarato in mosse** è una verifica che non passa da nessuno: il conto è il conto. Da guardare insieme alle altre forme con verifica fisica o aritmetica, che in `OSSERVAZIONI.md` sono già segnalate come la famiglia più numerosa.

**L'esclusione richiede un rispondente**, ed è la stessa mancanza di cadavere squisito, jigsaw e dibattito. Ma qui il rispondente può essere un insieme dato invece che una persona, e questa è una via d'uscita da provare su tutte le forme a due persone.

**Peirce sull'economia della ricerca** — spezzare un'ipotesi nelle sue parti minime e rischiarne una per volta — è un principio di disegno per le nostre consegne prima ancora che un contenuto da proporre.
