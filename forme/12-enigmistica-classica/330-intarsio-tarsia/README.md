# Intarsio (tarsia)

- **Numero** 330 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che uniscono o dividono parole»
- **Si chiama anche** tarsia, intarsio a frase, lettura alterna, parola intarsiata
- **In una riga** una parola si distribuisce dentro un'altra a lettere alterne.
- **Contratto** voce breve
- **Fonti** `it-intarsio.txt` e `riffle-shuffle-permutation.txt`, prese il 1 settembre 2026; `it-incastro.txt`, presa il 30 agosto 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Le lettere della seconda parola entrano dentro la prima **a gruppi di grandezza qualsiasi**, nel loro ordine, con un vincolo: il capo e la coda della prima parola devono restare agli estremi del totale. *sano* e *ponte* danno *spontaneo* — la S in testa, la O in fondo, e in mezzo le due parole intrecciate.

La riga di differenza dal termine di paragone del blocco, la voce 328, incastro: **là la seconda parola entra intera, qui entra spezzata.** È la definizione che ne dà `it-intarsio.txt`, presa il 1 settembre 2026, e non una parafrasi nostra: «il frazionamento della seconda parola lo distingue dall'incastro, nel quale la stessa rimane intera».

Il secondo vincolo — capo e coda della prima agli estremi — è quello che distingue l'intarsio dalla sciarada alterna, dove il totale può finire con la seconda parola. Ne segue un fatto di conteggio che la pagina scrive in prosa: **la prima parola viene spezzata una volta di più della seconda.** Nei nostri cinque esempi è sempre tre contro due.

La fonte dice anche che il gioco **non si riassume in una formula**, perché il numero dei segmenti è libero. È l'unico schema di questa sezione a non averne una.

La glossa dell'elenco è imprecisa su tutti e due i punti: «a lettere alterne» descrive la voce 324, sciarada alterna, dove i blocchi sono regolari, e non dice niente del vincolo su capo e coda, che è la sola cosa che separa i due giochi.

## Da dove viene

`it-intarsio.txt` non dà né una data né un inventore, e lo si dichiara: è una pagina di 2 059 byte che definisce, distingue e porta due esempi. La colloca nella **famiglia delle letture alterne**, che è una delle famiglie in cui l'enigmistica italiana raggruppa i suoi schemi, accanto a quella dei biscarti a cui appartiene la voce 329, cerniera.

Il nome viene dal mestiere: l'intarsio è il legno di un colore incastrato dentro il legno di un altro, e la *tarsia* è la stessa tecnica. La pagina italiana `Tarsia` è una disambiguazione di 2 509 byte e non è stata usata; il titolo giusto per lo schema enigmistico è `Intarsio_(enigmistica)`, ed è quello che si è preso.

## Varianti e parenti

- **Intarsio a frase** — il totale è una frase: *matassa / tiro = matita rossa*.
- **Intarsio a più parole** — la fonte dice che si può fare con più di due, senza esempi.
- **Incastro** (328) — la seconda parola entra intera invece che spezzata.
- **Sciarada alterna** (324) — i blocchi sono regolari e il vincolo su capo e coda non c'è.
- **Sciarada** (323) — un solo punto di contatto.
- **Anagramma** (331) — l'ordine delle lettere di ciascuna parola non si conserva più.
- **Mescolata a ventaglio** — la stessa operazione nella matematica delle permutazioni: `riffle-shuffle-permutation.txt` chiama così l'intreccio di due sequenze che conserva l'ordine interno di ognuna, ed è il mazzo di carte tagliato e sfogliato.

## Che cosa se ne sa

`it-intarsio.txt` non contiene nessuna misura. I conti seguono dalla definizione e sono stati fatti in `build/check_328.py`.

**Quante spartizioni sono intarsi.** Sulle 127 spartizioni di un totale di otto lettere contate alla voce 328, incastro, quelle con capo e coda della prima parola agli estremi e almeno quattro giunzioni sono **42**: le 35 con quattro giunzioni e le 7 con sei. Contro le 21 dell'incastro, sono il doppio esatto. Su un totale di nove lettere diventano 99. Verificato per formula binomiale e per enumerazione.

**Quanti modi ci sono di intrecciare due parole date.** Prese *sano* e *ponte*, gli intrecci che rispettano il vincolo su capo e coda sono **21** — tanti quanti i modi di scegliere due posizioni fra le sette interne — e di questi 3 lasciano *ponte* intera, cioè sono incastri. Ma le stringhe **distinte** sono soltanto 18, non 21, perché la N e la O compaiono in tutte e due le parole e tre coppie di intrecci diversi finiscono per scrivere la stessa cosa. Delle 18, tre sono incastri e quindici intarsi. Contato per composizioni e per enumerazione delle maschere.

**Ne segue che l'intarsio ha il verso facile dalla parte opposta rispetto alla sciarada.** Alla voce 323, sciarada lo spazio di ricerca stampabile era quello di chi parte dal totale; qui partendo dal totale di nove lettere ci sono 99 letture e partendo dalle due parole 18 intrecci, ed è quest'ultimo che sta su un foglio.

La verifica sta in un **vocabolario**, come per il resto del capitolo 12.

## Esempi trovati

Da `it-intarsio.txt`, riscritti: *asine / censo = ascensione*, dove *asine* è spezzata in *as*, *i*, *ne* e *censo* in *cens*, *o*. E l'intarsio a frase *matassa / tiro = matita rossa*.

Tutti e due sono stati rifatti a macchina cercando ogni modo di leggere la prima parola dentro il totale: nel primo caso i modi sono due e uno solo dà *censo*, nel secondo sono due e uno solo dà *tiro*. **Anche gli esempi della fonte, quindi, non sono letture uniche**, ed è un fatto sul gioco e non su questi due.

## Una nostra versione

> **Diciotto modi di intrecciare, e uno solo dice qualcosa**
>
> Prendi SANO e PONTE. Devi intrecciarle: le lettere di ognuna restano nel loro ordine, ma si alternano a gruppi come vuoi tu. Una sola regola: la S deve restare la prima lettera e la O l'ultima.
>
> I modi sono **diciotto**, e sono tutti qui.
>
> ```
>   1  sanponteo   2  sapnonteo   3  saponnteo
>   4  saponteno   5  sapontneo   6  spanonteo
>   7  spaonnteo   8  spaonteno   9  spaontneo
>  10  spoannteo  11  spoanteno  12  spoantneo
>  13  sponanteo  14  sponateno  15  sponatneo
>  16  spontaeno  17  spontaneo  18  sponteano
> ```
>
> Uno solo è una parola italiana. Scrivi il numero: ────
>
> Poi conta, su quello giusto: in quanti pezzi è finita SANO? ──── E PONTE? ────
>
> Uno dei due numeri è sempre più grande dell'altro di uno. Prova a dire perché — la risposta sta nella regola sulla S e sulla O.

Le diciotto righe sono **lo spazio di ricerca per intero**, e ci stanno su sei. La differenza con la voce 323, sciarada è il verso: là si stampava quello di chi parte dal totale, qui quello di chi parte dalle due parole, perché è il più piccolo dei due.

L'ultima domanda non ha una risposta da cercare: si ricava. Se la prima parola comincia e finisce il totale, i suoi pezzi e quelli della seconda si alternano cominciando e finendo con la prima, quindi i primi sono uno di più. È un ragionamento di due righe che si fa guardando il foglio, e non richiede di sapere niente.

Il limite tecnico del capitolo non morde: le diciotto stringhe si producono intrecciando due parole date, e il sistema non deve giudicarle. Il giudizio «questa è una parola italiana» resta fuori.

## Da riprendere alla rassegna

**La riga di differenza.** Rispetto al termine di paragone del blocco, la voce 328, incastro, qui la seconda parola entra spezzata invece che intera. Tutto il resto — le lettere che si conservano, l'ordine interno che si conserva, il vincolo su capo e coda — è comune alle due.

**Una consegna che si chiude su sé stessa.** Chiedere in quanti pezzi sono finite le due parole, e poi perché uno dei due numeri sia sempre più grande dell'altro di uno, trasforma un esercizio di riconoscimento in un piccolo teorema che si dimostra guardando il foglio. È il tipo di domanda che il capitolo 12 permette raramente, perché quasi sempre la risposta sta in un vocabolario.

**Il verso stampabile non è sempre lo stesso.** Alla voce 323, sciarada e alla voce 328, incastro conveniva stampare le letture del totale; qui conviene stampare gli intrecci delle due parole. Alla rassegna: per ogni forma con due versi, quale dei due spazi di ricerca stia su un foglio è una domanda da porre, e la risposta cambia da forma a forma.

**Gli esempi delle fonti non sono letture uniche.** Rifacendo a macchina i due esempi di `it-intarsio.txt` si trova che ciascuno ammette due modi di leggere la prima parola dentro il totale. Non è un difetto della pagina: è che l'intarsio, a differenza del lucchetto della voce 326, lucchetto, non determina niente.
