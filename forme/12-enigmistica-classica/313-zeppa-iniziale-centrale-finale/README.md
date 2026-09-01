# Zeppa iniziale, centrale, finale

- **Numero** 313 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che tolgono, aggiungono o cambiano lettere»
- **Si chiama anche** aggiunta iniziale, aggiunta finale, aggiunta di estremi, protesi, epentesi, paragoge
- **In una riga** la posizione dell'aggiunta è dichiarata nel nome del gioco.
- **Contratto** voce breve
- **Fonti** `it-zeppa.txt`, `it-scarto.txt`, prese il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Che cosa cambia nella parola: entra una lettera. Dove: **in un punto dichiarato prima**. Che cosa deve restare vero dopo: che venga fuori un'altra parola italiana.

Differenza dalla voce 314, scarto, in una riga: si aggiunge invece di togliere, e **il nome del gioco dice già dove**.

Questa è la voce in cui il titolo non accompagna la consegna: la è. Chi legge «aggiunta iniziale» sa tutto, e non resta niente da spiegare. È l'economia registrata alla voce 311, zeppa — il titolo come metà della consegna — portata al caso in cui il titolo è la consegna intera.

Dichiarare la posizione costa poco a chi scrive e toglie molto a chi cerca. Su *carta*, una zeppa libera dà 121 stringhe candidate; un'aggiunta iniziale ne dà 21, cioè **una su 5,8** (`build/check_312.py`).

```
 aggiunta iniziale     21
 zeppa, nel corpo      81
 aggiunta finale       21
 libera               121
```

I tre sottoinsiemi non sommano a 121 perché si sovrappongono: infilare una `c` prima di *carta* e infilarla dopo la prima lettera danno la stessa stringa.

## Da dove viene

Dalla tradizione enigmistica italiana, e con un'incongruenza che la fonte stessa nomina. `it-zeppa.txt` scrive che il gioco si chiama **zeppa** solo quando la lettera entra nel corpo della parola — dall'immagine del cuneo del falegname — mentre agli estremi cambia nome e diventa **aggiunta iniziale**, **aggiunta finale** o **aggiunta di estremi**. La pagina aggiunge che «non esiste alcun motivo» perché il nome cambi secondo la posizione, e che si mantiene per tradizione.

I nomi fonetici corrispondenti — *protesi* per l'aggiunta iniziale, *epentesi* per la zeppa, *paragoge* per l'aggiunta finale — sono caduti in disuso perché descrivono aggiunte che non cambiano il significato.

`it-scarto.txt` mostra che il gioco simmetrico ha la stessa struttura di nomi — scarto iniziale, scarto finale, scarto di estremi — e in più può dichiarare se la lettera sia vocale o consonante, cosa che la zeppa non fa mai. **La stessa fonte segnala l'asimmetria come un'incongruenza del repertorio.**

## Varianti e parenti

- **Zeppa** (311) — la forma senza posizione dichiarata.
- **Zeppa sillabica** (312) — l'unità cambia invece della posizione.
- **Scarto** (314) — lo stesso repertorio di posizioni, dalla parte di chi toglie.
- **Aggiunta di estremi** — due lettere, una davanti e una dietro: *astronomi / gastronomia*.
- **Bizeppa** — la stessa lettera due volte.
- **Raddoppiamento** — la lettera aggiunta gemina una consonante: *cane / canne*.

## Che cosa se ne sa

`it-zeppa.txt`, presa il 1 settembre 2026, è una pagina di repertorio: dà i nomi, gli esempi, e nessuna misura.

Quello che si può calcolare è quanto vale la dichiarazione della posizione, ed è il numero sopra: da 121 candidati a 21, su una parola di cinque lettere. La riduzione non dipende dalla parola ma dalla sua lunghezza — le posizioni interne sono *n* − 1 e le estreme sono due, quindi **più la parola è lunga, più dichiarare la posizione vale.** Su *cane*, quattro lettere, il fattore è 4,8; su *carta*, cinque, è 5,8.

Vale il limite dell'intero capitolo: **il sistema non sa manipolare le lettere dentro le parole** (`ideas/10 §6`), e la posizione dichiarata non lo aiuta, perché ridurre lo spazio di ricerca non serve a chi non sa cercarci dentro.

## Esempi trovati

Da `it-zeppa.txt`, riscritti: aggiunta iniziale *alice / calice*; aggiunta finale *sport / sporta*; aggiunta di estremi *astronomi / gastronomia*; zeppa nel corpo *oro / orco* e *abito / arbitro*; una successione, *cane / canne / canone / cannone*.

Da `it-scarto.txt`, la stessa griglia rovesciata: *cappello / appello* è un'aggiunta iniziale letta al contrario, *Gange / gang* una finale, *asporto / sport* una di estremi.

## Una nostra versione

> **Tre giochi diversi con la stessa parola**
>
> La parola è **ORTO**. In tutti e tre i riquadri devi metterci una lettera in più e ottenere un'altra parola vera. Cambia solo dove ti è permesso metterla.
>
> ```
>  DAVANTI    _ ORTO      ────────  ────────  ────────
>  IN MEZZO   O_RTO ecc   ────────  ────────  ────────
>  IN FONDO   ORTO_       ────────  ────────  ────────
> ```
>
> Il primo riquadro ha esattamente ventuno possibilità, cioè le lettere dell'alfabeto italiano una per volta. Si provano tutte in un minuto, e ne funzionano cinque.
>
> Il terzo riquadro ne ha ventuno anche lui. **Ma resterà vuoto, e la domanda vera di questo foglio è perché.** Scrivi la tua idea qui: ────────────────────
>
> Poi guarda venti parole italiane a caso, su qualunque pagina, e conta per che cosa finiscono.

I tre riquadri sono la stessa operazione con tre vincoli diversi, affiancati apposta: la differenza fra i giochi si vede senza spiegarla. Il primo si esaurisce a mano — ventuno tentativi, dichiarati come numero — e ne escono *corto*, *morto*, *porto*, *sorto*, *torto*, che sono cinque.

Il terzo riquadro è la parte che fa il lavoro. Resta vuoto perché **le parole italiane finiscono quasi sempre per vocale**, e aggiungere una lettera dopo una vocale finale non produce quasi mai niente. L'osservazione è nostra e va verificata: le fonti prese non la enunciano, ma `it-sillaba.txt` dà la distinzione fra sillaba aperta e chiusa, e l'unico esempio di aggiunta finale che `it-zeppa.txt` porta — *sport / sporta* — parte da un prestito che finisce per consonante. L'ultima riga fa fare a chi legge il conteggio che decide la questione.

Dove si romperebbe: il sistema non può controllare nessuna delle risposte, e non saprebbe dire se *corto* sia una parola. La scelta di *orto* è nostra, e che le cinque siano cinque è un giudizio nostro, dichiarato: in casa non c'è un vocabolario garantito.

## Da riprendere alla rassegna

**Uno spazio di ricerca dichiarato come numero è una consegna.** «Provale tutte, sono ventuno» dice quanto costa finire, e chi legge decide se cominciare sapendo il prezzo. È la stessa idea del diagramma fra parentesi registrato alla voce 311, zeppa, e dello spazio stampato della voce 11, risposta breve.

**Un riquadro che resta vuoto per una ragione strutturale vale più di uno pieno.** Il terzo riquadro non è un errore di disegno: è la sola parte del foglio che produca una scoperta, e la produce perché il vuoto è garantito dalla lingua e non dalla difficoltà. Da cercare altrove: quante forme dell'elenco hanno un caso in cui il fallimento è certo e informativo.

**Tre vincoli affiancati sulla stessa materia mostrano la differenza senza enunciarla.** Costa tre righe invece di un paragrafo, e da provare ovunque una voce dell'elenco abbia dei sottotipi che si distinguono per un parametro solo.

**La differenza dalla voce 314, scarto, in una riga:** si aggiunge invece di togliere, e la posizione è dichiarata nel titolo.
