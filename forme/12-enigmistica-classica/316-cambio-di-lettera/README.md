# Cambio di lettera

- **Numero** 316 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che tolgono, aggiungono o cambiano lettere»
- **Si chiama anche** cambio, sostituzione, coppia minima, *minimal pair*, *word ladder*, *doublets*, *word golf*
- **In una riga** se ne sostituisce una: *pane → pace*.
- **Contratto** voce breve
- **Fonti** `it-cambio.txt`, `it-coppia-minima.txt`, `word-ladder.txt`, `hamming-distance.txt`, prese il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Che cosa cambia nella parola: una lettera prende il posto di un'altra. Dove: in un punto dichiarato dal nome. Che cosa deve restare vero dopo: che venga fuori un'altra parola italiana.

Differenza dalla voce 314, scarto, in una riga: **non si toglie e non si aggiunge, e la lunghezza resta la stessa.**

La lunghezza costante ha una conseguenza che nessun'altra voce del blocco ha. Quando due stringhe sono lunghe uguali si può contare in quante posizioni differiscono, e quel conteggio si chiama **distanza di Hamming**; per zeppe e scarti non è definita, perché le lunghezze non coincidono. Il cambio è l'unica delle sei forme a cui si applichi, e per un cambio solo vale 1 (`build/check_312.py`).

Parti mobili, dalla fonte: il tipo di lettera cambiata — consonante, vocale, o l'una per l'altra — e la posizione, iniziale, interna, finale.

## Da dove viene

`it-cambio.txt` scrive una cosa che vale la pena riportare per intero: «Non si parla mai di *un cambio*, ma se ne specifica la natura». Il nome nudo non esiste nel repertorio, e **anche «cambio di lettera» è già un tipo specificato**: la lettera sta in mezzo alla parola, e se è consonante diventa vocale o viceversa. La pagina porta in cima due avvisi, uno che dice che le fonti mancano e uno che dice che è formattata male, «troppo grassetto»: è un repertorio senza note.

Fuori dall'enigmistica la stessa operazione è lo strumento centrale della fonologia. `it-coppia-minima.txt`: una coppia minima è una coppia di parole che si distinguono per un solo suono, e la ricerca delle coppie minime «è essenziale per stabilire l'inventario dei fonemi» di una lingua. *Balla* e *palla*, *detto* e *tetto*, *va* e *fa*. **Il gioco enigmistico e il metodo scientifico sono la stessa operazione con due scopi diversi.**

In inglese la forma ha una data. `word-ladder.txt`: Lewis Carroll dice di aver inventato il gioco a Natale del **1877**, per Julia ed Ethel Arnold; la prima menzione nel suo diario è del 12 marzo 1878, con il nome *Word-links*; lo pubblicò come *Doublets* su *Vanity Fair* a partire dal numero del 29 marzo 1879, e nello stesso anno ne uscì un libro da Macmillan. Nabokov lo chiama *word golf* in *Fuoco pallido*. **Questo chiude la questione lasciata aperta dalla voce 311, zeppa**, dove la paternità dei *doublets* era a memoria.

La distanza di Hamming porta il nome di Richard Hamming e viene dal suo articolo del **1950** sui codici correttori d'errore (`hamming-distance.txt`).

## Varianti e parenti

- **Cambio di vocale, di consonante, di sillaba** (317) — la stessa cosa, ristretta.
- **Scarto** (314) — si toglie invece di sostituire.
- **Zeppa** (311) — si aggiunge invece di sostituire.
- **Scambio** (318) — due lettere si scambiano di posto, che non è una sostituzione.
- **Coppia minima** — la stessa operazione in fonologia, con lo scopo di trovare i fonemi.
- **Scala di parole** (*word ladder*) — cambi in successione, da una parola a un'altra data.

## Che cosa se ne sa

Le due pagine enigmistiche non misurano niente. I numeri vengono dalle altre.

**Il numero minimo di passi di una scala di parole è la distanza di Hamming fra le due parole**, dice `word-ladder.txt`, e non può essere meno: ogni passo raddrizza al più una posizione. È una soglia che chi gioca può calcolare da sé contando, senza sapere se una soluzione esista.

**Su cinque lettere, quasi nove parole su dieci hanno almeno un vicino.** Donald Knuth ha studiato al calcolatore le scale di cinque lettere su una raccolta di 5 757 parole inglesi comuni, nomi propri esclusi, e ne ha trovate **671 senza nessun vicino**, che chiamò *aloof* — parola che è essa stessa di quel tipo. Rifatto il conto: 671 su 5 757 è l'11,66%, quindi l'88,34% ne ha almeno uno (`build/check_312.py`). Il dato è inglese, su quella lista, e non si trasferisce all'italiano senza rifarlo.

**Distanza di Hamming e di Levenshtein non coincidono nemmeno a lunghezza uguale.** `levenshtein-distance.txt` porta *flaw* e *lawn*: Levenshtein 2 — si toglie la *f* davanti e si mette una *n* in fondo —, Hamming 4. Verificato ricalcolando tutte e due.

Vale il limite dell'intero capitolo: **il sistema non sa manipolare le lettere dentro le parole** (`ideas/10 §6`).

## Esempi trovati

Da `it-cambio.txt`, riscritti: di consonante *carta / casta*; di vocale *Roma / rima*; di lettera *cieco / circo*; di iniziale *casta / pasta*; di finale *conto / conte*. E una successione, *pazzo / pezzo / pizzo / pozzo / puzzo*.

Da `it-coppia-minima.txt`: *balla / palla*, *detto / tetto*, *va / fa*.

Da `word-ladder.txt`: la scala di Carroll da HEAD a TAIL, e la nota che ha un passo in più del minimo perché la terza lettera cambia due volte.

## Una nostra versione

> **Il numero che sai prima di cominciare**
>
> Da CANE si vuole arrivare a CASA cambiando **una lettera per volta**, e ogni passo deve essere una parola vera.
>
> Prima di provare, conta: in quante posizioni CANE e CASA sono diverse?
>
> ```
>  C A N E
>  C A S A
>  ─ ─ ─ ─   diverse in ──── posizioni
> ```
>
> Quel numero è il **minimo assoluto** di passi. Meno non si può, perché ogni passo sistema al massimo una posizione. Di più sì.
>
> ```
>  CANE  →  ────────  →  CASA
> ```
>
> Adesso scegli tu due parole della stessa lunghezza e conta le posizioni diverse. Quello è il tuo minimo. Poi prova a costruire la scala.
>
> **Avvertimento onesto: potrebbe non esistere.** In inglese, su 5 757 parole di cinque lettere, 671 non hanno nemmeno un vicino a una lettera di distanza. In italiano nessuno l'ha contato.

La parte che fa il lavoro è che **il numero si calcola prima e senza sapere la risposta**: si contano le posizioni diverse, e quel conteggio è esatto, si fa a occhio, e non richiede né vocabolario né sistema. È l'unico numero certo che questo blocco produca su un foglio. L'avvertimento in fondo è la mossa già registrata più volte di dire in anticipo che può non venire, e qui in più porta un dato vero.

Dove si romperebbe: il sistema non può verificare che *case* sia una parola, né generare la coppia di partenza. Che CANE-CASE-CASA sia una scala di due passi, cioè esattamente il minimo, è verificato in `build/blocco_312.py`; che *case* sia una parola italiana è un giudizio nostro.

## Da riprendere alla rassegna

**Una soglia calcolabile a mano vale più di una risposta verificabile a macchina.** Contare le posizioni diverse fra due parole è esatto, costa dieci secondi, e dice qualcosa di vero sul problema prima che il problema sia risolto. È la stessa struttura della voce 304, finisce con una scoperta, dove il numero atteso si scrive prima: qui il numero non è una previsione, è un limite dimostrato.

**Il gioco e il metodo scientifico coincidono, e dirlo è la consegna.** Il cambio di lettera è la coppia minima, cioè lo strumento con cui si stabilisce l'inventario dei fonemi di una lingua. È il terzo caso in cui la spiegazione storica costa tre righe e fa il lavoro meglio della spiegazione della regola, dopo la voce 333, bifronte e la voce 346, rebus.

**La differenza dalla voce 314, scarto, in una riga:** si sostituisce invece di togliere, e la lunghezza non cambia.
