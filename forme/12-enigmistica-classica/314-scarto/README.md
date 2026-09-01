# Scarto

- **Numero** 314 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che tolgono, aggiungono o cambiano lettere»
- **Si chiama anche** scarto di consonante, scarto di vocale, scarto iniziale, scarto finale, scarto di estremi, aferesi, sincope, apocope, decapitazione, sventramento, amputazione, *deletion*
- **In una riga** si toglie una lettera: *scarpa → scapa*, ma solo se resta una parola vera.
- **Contratto** voce breve
- **Fonti** `it-scarto.txt`, `it-zeppa.txt`, `levenshtein-distance.txt`, prese il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Che cosa cambia nella parola: una lettera sparisce. Dove: lo dichiara il nome del gioco. Che cosa deve restare vero dopo: che venga fuori un'altra parola italiana. Le tre righe valgono per tutte e sei le voci di questo blocco, e la terza è la stessa per tutte.

Lo scarto è la forma in cui la variabile prende il **valore più povero**: non si sceglie che cosa mettere, perché non si mette niente. Le altre cinque si descrivono per differenza da qui. La glossa dell'elenco — *scarpa → scapa* — è di proposito un caso che fallisce: *scapa* non è una parola, e togliere una lettera quasi sempre non produce niente.

Ne segue la proprietà che nessun'altra voce del blocco ha. Su una parola di *n* lettere le stringhe candidate sono *n*, e basta: non dipendono dall'alfabeto. Su *porzione* sono otto, mentre la zeppa sulla stessa parola ne dà 181, ventidue volte tante (`build/check_312.py`). Otto è un numero che una persona esaurisce a mano, e **lo scarto è l'unica delle sei forme in cui si possono provare tutti i casi.**

Parti mobili: la posizione — di consonante, di vocale, iniziale, finale, di estremi; e se si fa una volta sola o in successione.

## Da dove viene

Dalla tradizione enigmistica italiana. `it-scarto.txt` registra due nomenclature abbandonate. La prima è fonetica: *aferesi* per lo scarto iniziale, *sincope* per quello interno, *apocope* per quello finale — cadute perché descrivono cambiamenti che non cambiano il significato, e in enigmistica il cambio di significato è obbligatorio. La seconda è ottocentesca e, dice la fonte, «beffardamente sanguinaria»: **decapitazione**, **sventramento**, **amputazione**, ancora registrate dai dizionari, con rimando al De Mauro archiviato nel 2008.

Fuori dall'enigmistica la stessa operazione è una delle tre della distanza di Levenshtein — inserzione, cancellazione, sostituzione — definita da Vladimir Levenštejn nel 1965, in russo, e uscita in inglese nel 1966 (`levenshtein-distance.txt`).

## Varianti e parenti

- **Zeppa** (311) — l'inverso esatto: si aggiunge invece di togliere.
- **Scarto sillabico** (315) — si toglie una sillaba invece di una lettera.
- **Cambio di lettera** (316) — non si toglie niente: una lettera prende il posto di un'altra.
- **Scarto di estremi** — due lettere, una in testa e una in coda: *asporto → sport*.
- **Biscarti** — la famiglia in cui lo scarto si fa due volte, e che comprende il **lucchetto** (326), la cerniera e la doppia estrazione.
- **Scarti in successione** — *partente → parente → parete → prete*.

## Che cosa se ne sa

`it-scarto.txt`, presa il 1 settembre 2026, dà i cinque tipi e gli esempi, e non dà nessuna misura: è una pagina di repertorio.

Quello che si può misurare viene da fuori. **Zeppa, scarto e cambio sono le tre operazioni della distanza di edit, e ognuna delle tre porta da una parola all'altra in un passo solo**; lo scambio di due lettere della voce 318, scambio ne costa due, perché la trasposizione non è fra le tre. Verificato calcolando la distanza su *oro/orco*, *porzione/pozione*, *carta/casta* e *arte/atre* in `build/check_312.py`.

Il limite che vale per l'intero capitolo 12 vale anche qui e non ha eccezioni: **il sistema non sa manipolare le lettere dentro le parole** (`ideas/10 §6`), quindi non può né costruire né verificare uno scarto. Ma per questa voce, e solo per questa, lo spazio di ricerca è abbastanza piccolo da poter essere **stampato per intero**, e allora non c'è più niente da generare.

## Esempi trovati

Da `it-scarto.txt`, riscritti: scarto di consonante *porzione / pozione*; di vocale *bacio / baco*; iniziale *cappello / appello*; finale *Gange / gang*; di estremi *asporto / sport*. E la successione *partente / parente / parete / prete*, che è tre scarti di fila.

Dai dizionari, per via della fonte: *decapitazione* e *amputazione* sono ancora registrate come termini enigmistici, il che rende questo il gioco con il lessico storico più violento dell'elenco.

## Una nostra versione

> **Otto modi di accorciare una parola, e sette non funzionano**
>
> PORZIONE ha otto lettere. Toglierne una si può fare in otto modi, e sono tutti qui sotto: non ce n'è un nono.
>
> ```
>  ORZIONE     PRZIONE     POZIONE     PORIONE
>  PORZONE     PORZINE     PORZIOE     PORZION
> ```
>
> Cerchia quelle che sono parole italiane. **Una lo è.**
>
> Adesso al contrario, e senza rete. Parti da una parola lunga e toglile una lettera per volta; ogni volta deve restare una parola vera. Si arriva più lontano di quanto sembri — *partente, parente, parete, prete* sono tre passi di fila.
>
> ```
>  ────────── → ───────── → ──────── → ────────
> ```
>
> Se ne fai due invece di tre, sono due.

Le otto righe stampate **sono il controllo dell'errore messo nel materiale**, ed è esatto e non parziale: lo spazio di ricerca dello scarto è finito, piccolo, e ci sta su due righe. Nessuna delle altre cinque forme di questo blocco lo permette — la zeppa sulla stessa parola avrebbe 181 righe. La seconda metà gira il gioco dalla parte dell'autore, che è la mossa registrata alla voce 311, zeppa, e serve qui perché la catena non si può stampare per esteso.

Dove si romperebbe: il giudizio «questa è una parola italiana» non lo può dare il sistema, e in casa non c'è un vocabolario garantito. Che *pozione* sia la sola delle otto è un giudizio nostro, dichiarato come tale.

## Da riprendere alla rassegna

**Uno spazio di ricerca che sta su un foglio si stampa invece di essere cercato**, e allora il limite tecnico del capitolo smette di contare. Vale per lo scarto perché *n* lettere danno *n* candidati; non vale per nessun'altra voce di questo blocco. Da cercare altrove nell'elenco: quante altre forme hanno uno spazio di ricerca lineare nella lunghezza del materiale.

**Il termine di paragone di questo blocco.** Le sei forme differiscono nell'enigma e non nel modo di chiedere, e lo scarto è quella in cui si toglie e basta: le altre cinque aggiungono una scelta — che cosa mettere, dove, di che tipo — e ognuna si può descrivere in una riga di differenza da qui.

**La verifica di questa forma sta in una persona o in un vocabolario, e da nessuna parte nel sistema.** È uno dei casi in cui il censimento del controllo dell'errore in `OSSERVAZIONI.md` trova una classe che il progetto non ha: non «nel materiale», non «da nessuna parte», ma **in un libro che si presume in casa**.
