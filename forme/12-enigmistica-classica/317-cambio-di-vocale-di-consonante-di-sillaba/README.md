# Cambio di vocale, di consonante, di sillaba

- **Numero** 317 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che tolgono, aggiungono o cambiano lettere»
- **Si chiama anche** cambio di vocale, cambio di consonante, cambio d'iniziale, cambio di finale, cambio a frase, frase a cambio
- **In una riga** la stessa cosa, ristretta.
- **Contratto** voce breve
- **Fonti** `it-cambio.txt`, `it-coppia-minima.txt`, prese il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Che cosa cambia nella parola: una lettera prende il posto di un'altra, **e si dichiara prima di che tipo**. Dove: dichiarato anche quello. Che cosa deve restare vero dopo: che venga fuori un'altra parola italiana.

Differenza dalla voce 314, scarto, in una riga: si sostituisce invece di togliere, la lunghezza resta, e il tipo di lettera è dichiarato. Differenza dalla voce 316, cambio di lettera, in una riga: **il tipo è dichiarato, e questo è tutto.**

La restrizione non è un dettaglio del repertorio: è quello che rende il gioco finibile a mano. Su *carta* un cambio senza vincoli dà 100 stringhe candidate; ristretto alle vocali ne dà 8, e alle consonanti 45 (`build/check_312.py`).

```
 cambio, qualunque lettera   100
 cambio di vocale              8
 cambio di consonante         45
```

Otto si scrivono su una riga e si guardano tutti; cento no. **Dichiarare il tipo è l'unico modo, in questo blocco, di ottenere uno spazio di ricerca piccolo senza rimpicciolire la parola.**

## Da dove viene

Dalla tradizione enigmistica italiana. `it-cambio.txt` elenca cinque tipi: **di consonante** — in mezzo alla parola —, **di vocale** — in mezzo —, **di lettera** — in mezzo, e se è consonante diventa vocale o viceversa —, **d'iniziale** e **di finale**. La pagina insiste che il nome nudo non si usa mai e che la natura del cambio va sempre specificata.

Porta anche due estensioni fuori dalla parola singola. Il **cambio a frase**, in cui il mutamento avviene fra una parola e una frase — *lancia / l'ascia* — e la **frase a cambio**, in cui avviene fra due frasi — *la mica / l'amaca*. E una nota di confine che vale la pena tenere: **il cambio di genere non appartiene alla famiglia dei cambi**, ma a quella dei falsi derivati, che è la voce 322, falso accrescitivo, falso diminutivo.

La pagina ha in cima due avvisi, uno sulla mancanza di fonti e uno sulla formattazione.

## Varianti e parenti

- **Cambio di lettera** (316) — la stessa cosa senza il tipo dichiarato.
- **Scarto** (314) — si toglie invece di sostituire.
- **Zeppa sillabica** (312) — l'unità sillabica dalla parte di chi aggiunge.
- **Falso accrescitivo, falso diminutivo** (322) — dove finisce il cambio di genere, che non è un cambio.
- **Cambio a frase** — fra una parola e una frase: *lancia / l'ascia*.
- **Cambi in successione** — *pazzo / pezzo / pizzo / pozzo / puzzo*, cinque parole con lo stesso scheletro.

## Che cosa se ne sa

`it-cambio.txt` è un repertorio senza note e senza misure, e lo dichiara da sé con l'avviso in cima.

Il conto che si può fare è quanto vale la restrizione, ed è sopra: da 100 a 8 sulle vocali di *carta*, cioè un dodicesimo e mezzo. Il rapporto non è costante — dipende da quante vocali e quante consonanti ha la parola — e su *porzione* la stessa restrizione dà 16 candidati contro 160, cioè un decimo.

Il caso limite è il più interessante, e la fonte lo porta senza commentarlo. Fissando **posizione e tipo insieme** — la vocale della seconda posizione — lo spazio di ricerca diventa esattamente cinque, perché le vocali grafiche italiane sono cinque. *Pazzo, pezzo, pizzo, pozzo, puzzo* è quello spazio esaurito, e sono parole tutte e cinque. **Questa è la sola forma di tutto il blocco in cui l'elenco completo dei candidati sta in una riga e non dipende da nessuna convenzione contestata**, a differenza della voce 315, scarto sillabico.

Vale il limite dell'intero capitolo: **il sistema non sa manipolare le lettere dentro le parole** (`ideas/10 §6`).

## Esempi trovati

Da `it-cambio.txt`, riscritti: di consonante *carta / casta*; di vocale *Roma / rima*; di lettera *cieco / circo*; di iniziale *casta / pasta*; di finale *conto / conte*; a frase *lancia / l'ascia*; frase a cambio di vocale *la mica / l'amaca*; e la successione *pazzo / pezzo / pizzo / pozzo / puzzo*.

Da `it-coppia-minima.txt`, gli stessi cambi visti da un fonologo: *balla / palla* è un cambio d'iniziale di consonante, *detto / tetto* pure, e servono a mostrare che /b/ e /p/, /d/ e /t/ sono fonemi distinti dell'italiano.

## Una nostra versione

> **Cinque parole con lo stesso scheletro**
>
> Le vocali italiane sono cinque. Prendi lo scheletro **P — Z Z O** e mettici dentro tutte e cinque, una per volta. Non c'è niente da cercare: le possibilità sono cinque e le scrivi in dieci secondi.
>
> ```
>  P A Z Z O     P E Z Z O     P I Z Z O     P O Z Z O     P U Z Z O
> ```
>
> Sono parole tutte e cinque. **Non capita quasi mai.**
>
> Adesso tocca a te. Trova uno scheletro con un buco solo dove funzionino **almeno tre vocali su cinque**. Scrivi tutte e cinque le parole comunque, anche quelle che non esistono: servono a far vedere quante ne hai scartate.
>
> ```
>  scheletro  ─ ─ ─ ─ ─
>  A ────────  E ────────  I ────────  O ────────  U ────────
>  quante funzionano:  ──── su 5
> ```
>
> Ultima riga, e non ha risposta giusta: **quale delle cinque parole trovate ti sembra la più lontana dalle altre?**

Lo scheletro con un buco è lo spazio di ricerca reso piccolo dalla restrizione invece che dall'operazione, ed è la differenza da tutto il resto del blocco: la parola resta lunga, e a diventare corto è l'elenco delle cose da provare. Cinque righe stampate coprono tutti i casi, quindi **il controllo dell'errore è nel materiale e non manca niente**. La richiesta di scrivere anche le parole che non esistono è quella che rende visibile il lavoro: senza, restano solo le tre riuscite e non si vede che erano cinque tentativi.

Dove si romperebbe: il sistema non può proporre uno scheletro né dire se *pizzo* sia una parola. Che le cinque di P—ZZO siano tutte parole è un giudizio nostro, e su M—LA ne contiamo tre — *mela*, *mola*, *mula* — sempre a giudizio nostro.

## Da riprendere alla rassegna

**Restringere una regola può allargare quello che si riesce a fare.** Il cambio libero su una parola di cinque lettere ha cento risposte possibili e non si finisce; ristretto alle vocali ne ha otto e si finisce. È il contrario dell'intuizione che un vincolo in più renda un compito più difficile, ed è la seconda volta che compare — la prima è la voce 124, lipogramma, dove la difficoltà si regola con una tabella di frequenze.

**Chiedere di scrivere anche i tentativi falliti** costa due righe di stampa e cambia che cosa resta sul foglio: cinque righe invece di tre, e il rapporto fra provato e riuscito diventa leggibile. Da provare su ogni forma dell'elenco che chieda di trovare qualcosa.

**La differenza dalla voce 314, scarto, in una riga:** si sostituisce invece di togliere, la lunghezza resta, e il tipo di lettera è dichiarato prima.
