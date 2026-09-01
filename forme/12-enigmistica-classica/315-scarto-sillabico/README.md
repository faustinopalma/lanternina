# Scarto sillabico

- **Numero** 315 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che tolgono, aggiungono o cambiano lettere»
- **Si chiama anche** scarto di sillaba, sincope sillabica
- **In una riga** si toglie una sillaba.
- **Contratto** voce breve
- **Fonti** `it-scarto.txt`, `it-divisione-in-sillabe.txt`, prese il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Che cosa cambia nella parola: sparisce una sillaba. Dove: in un punto qualsiasi. Che cosa deve restare vero dopo: che venga fuori un'altra parola italiana.

Differenza dalla voce 314, scarto, in una riga: **l'unità è la sillaba invece della lettera**, e non cambia nient'altro.

Ne segue una coppia di proprietà che tirano in direzioni opposte, ed è l'unica voce del blocco che le abbia tutte e due.

- **Lo spazio di ricerca è il più piccolo di tutte e sei.** Una parola di tre sillabe si può accorciare in tre modi, contro i sei o gli otto dello scarto di lettera sulla stessa parola. Tre candidati si scrivono su una riga.
- **L'unità è la meno certa di tutte e sei.** Le lettere si contano e nessuno discute; le sillabe no. `it-divisione-in-sillabe.txt` dichiara che le norme sono «completate da alcune convenzioni in parte arbitrarie», che sui sintagmi con apostrofo «le fonti non concordano affatto», e porta un caso in cui due dizionari danno due divisioni: *subacqueo* è *su-bac-queo* per il Garzanti e forse *su-bac-que-o* per il De Mauro.

Le due cose insieme danno il tratto che rende questa voce diversa dalla 314: **l'elenco completo dei candidati si può stampare, ma dipende da una convenzione che non è stabilita.** Tre o quattro candidati, secondo chi ha ragione.

## Da dove viene

`it-scarto.txt` definisce lo scarto come il togliere «una lettera o una sillaba», e da lì in poi tratta soltanto le lettere: i cinque tipi che elenca — di consonante, di vocale, iniziale, finale, di estremi — sono tutti di lettera, e nessuno degli esempi è sillabico. Come per la voce 312, zeppa sillabica, la fonte enigmistica nomina la forma e non la sviluppa.

I nomi fonetici che la tradizione ha abbandonato — aferesi, sincope, apocope — sono gli stessi dello scarto di lettera, e non distinguono l'unità.

## Varianti e parenti

- **Scarto** (314) — la stessa cosa con una lettera sola.
- **Zeppa sillabica** (312) — il gioco al contrario: si aggiunge una sillaba.
- **Scarto sillabico iniziale** — la sillaba tolta è la prima: *marito / rito*.
- **Biscarti** — la famiglia in cui si toglie due volte, con il **lucchetto** (326).
- **Apocope** — la caduta della sillaba finale, che in italiano avviene da sé nel parlato: *professore / professor*.

## Che cosa se ne sa

Nessuna misura nelle fonti prese. `it-scarto.txt` è un repertorio e `it-divisione-in-sillabe.txt` è una pagina di norme ortografiche.

Quello che si può contare è lo spazio di ricerca, e il conto è banale e per questo interessante: **su una parola di *k* sillabe i candidati sono *k*.** Su *marito*, tre sillabe, sono *rito*, *mato*, *mari*, e due su tre sono parole (`build/blocco_312.py`; il giudizio su quali siano parole è nostro, perché in casa non c'è un vocabolario garantito). Su *subacqueo* sono tre o quattro secondo la divisione che si adotta, ed è il caso in cui **il numero di risposte possibili dipende da quale dizionario si tiene in mano.**

Vale il limite dell'intero capitolo: **il sistema non sa manipolare le lettere dentro le parole** (`ideas/10 §6`), e non sa dividere in sillabe.

## Esempi trovati

Nessun esempio sillabico nelle fonti: `it-scarto.txt` dà solo scarti di lettera — *porzione / pozione*, *bacio / baco*, *cappello / appello*, *Gange / gang*, *asporto / sport*, e la successione *partente / parente / parete / prete*.

Da `it-divisione-in-sillabe.txt`, le divisioni che servono a costruire esempi: *te-ne-re*, *la-vo-ro*, *tet-to*, *ac-qua*, *am-pio*, *mol-to*, *o-stri-ca*, e i due *su-bac-queo* / *su-bac-que-o*.

## Una nostra versione

> **Togliere una sillaba, e la sillaba non è sicura**
>
> MARITO si divide MA-RI-TO. Toglierne una si può fare in tre modi, e sono tutti e tre qui:
>
> ```
>  RITO       MATO       MARI
> ```
>
> Cerchia quelle che sono parole. Ce ne sono **due**.
>
> Adesso la parte scomoda. Prendi la parola **SUBACQUEO**. In quante sillabe si divide? Il Garzanti dice SU-BAC-QUEO, tre. Il De Mauro forse SU-BAC-QUE-O, quattro. Non è una domanda con una risposta.
>
> ```
>  La mia divisione:  ─────────────────────────
>  Con la mia, i modi di togliere una sillaba sono:  ────
>  Con l'altra, sono:  ────
> ```
>
> **Se i due numeri sono diversi, questo gioco non ha un numero di risposte, ne ha due.** Scrivi in una riga chi secondo te dovrebbe decidere.

La prima metà è lo spazio di ricerca stampato per intero, che è la mossa della voce 314, scarto, e qui costa una riga invece di due perché le sillabe sono meno delle lettere. La seconda metà è quello che questa voce ha di suo: **la regola del gioco è contestata dalle fonti, e invece di scegliere di nascosto si mette la contestazione sul foglio.** Il conteggio finale è esatto — tre contro quattro — e chi lo fa scopre che una domanda ben posta può avere due risposte per una ragione che non è la sua ignoranza.

Dove si romperebbe: il sistema non sa dividere in sillabe, quindi non può né proporre la parola né controllare la divisione. La citazione dei due dizionari viene da `it-divisione-in-sillabe.txt` e non dai dizionari stessi, e questo va detto sul foglio o no a seconda di chi legge.

## Da riprendere alla rassegna

**Una regola contestata dalle fonti è materiale migliore di una regola stabilita.** Il caso *subacqueo* dà un compito con un conteggio esatto e senza una risposta unica, e la mancanza di risposta ha una causa nominabile invece di essere un'opinione. Da cercare altrove nell'elenco: quali altre forme poggiano su una convenzione che le fonti non hanno chiuso.

**Lo spazio di ricerca più piccolo del blocco sta su una riga**, ed è il caso limite della mossa registrata alla voce 314, scarto. Il confine fra «si può stampare tutto» e «bisogna cercare» passa fra questa voce e la voce 312, zeppa sillabica, e la differenza è solo il verso dell'operazione.

**La differenza dalla voce 314, scarto, in una riga:** l'unità è la sillaba invece della lettera.
