# Lucchetto

- **Numero** 326 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che uniscono o dividono parole»
- **Come la classificava il primo giro** aperto — promemoria, non un verdetto
- **In una riga** due parole con una parte comune che sparisce: la parte comune è la chiave.
- **Stato della ricerca** fatta, 30 agosto 2026

## Che cos'è

Tre parole legate dallo schema **XZ / ZY = XY**. Le prime due condividono la parte Z: la prima ce l'ha in coda, la seconda in capo. Z si scarta da entrambe, e i resti si uniscono nella terza parola.

*mais / sale = maiale.* La parte comune è *s*: cade da *mai̱s* e da *̱sale*, e resta *mai + ale*.

Appartiene alla famiglia dei **biscarti**, così chiamati perché gli scarti sono due: prima in coda, poi in capo. Può essere **multiplo** — un lucchetto doppio ha schema XZ / ZK / KY = XY, e la parola centrale sparisce per intero: *persona / sonate / tegola = pergola*.

Parti mobili:

- **La lunghezza della parte comune.** Una lettera, una sillaba, di più.
- **Quante parole si concatenano** — tre, quattro, cinque.
- **Il verso.** Nel **lucchetto riflesso** le lettere della parte comune compaiono in ordine inverso nelle due parole, secondo lo schema XZz / zZY = XY: *spia / aiola = spola*, *torre / erba = torba*.
- **Se le tre parole hanno un rapporto di senso.** Come nella zeppa, il gioco riuscito è quello in cui il senso e la meccanica dicono la stessa cosa.

## Da dove viene

**È recente, e questo mi ha sorpreso.** Il lucchetto è stato teorizzato solo **nel 1950**, dall'enigmista Pietro Mercatanti, che si firmava *Carminetta*. Deriva logicamente dal **biscarto**, inventato dallo stesso autore ma dopo.

Sta in un punto preciso della storia del repertorio: è la prima evoluzione della **sciarada incatenata**, che a sua volta è il nodo fra la famiglia ottocentesca delle sciarade e quella novecentesca dei biscarti. Nella sciarada incatenata lo scarto è uno solo, e l'altro segmento comune viene riutilizzato per formare la terza parola: XZ / ZY = XZY.

La differenza fra i due giochi è quindi una sola cosa — se la parte comune sopravvive o sparisce — e ci sono voluti cent'anni perché qualcuno provasse a farla sparire.

## Varianti e parenti

- **Lucchetto riflesso** (327) — la parte comune in ordine inverso: XZz / zZY = XY.
- **Biscarto** — il gioco da cui il lucchetto deriva logicamente, dello stesso autore.
- **Cerniera** (329) — la parte comune sta in mezzo a entrambe invece che agli estremi.
- **Incastro** (328) — una parola entra dentro l'altra invece di agganciarsi.
- **Sciarada** (323) — due parole si sommano senza che nulla cada.
- **Sciarada incatenata** (325) — XZ / ZY = XZY: la parte comune resta. È il lucchetto senza la sottrazione, e lo precede di mezzo secolo.
- **Catena di parole** — la versione orale e infinita, quella che si fa in macchina.
- **Domino di sillabe** — tessere fisiche che si agganciano per sillaba.

## Che cosa se ne sa

Fonte: `_reference/esercizi-e-sfide/it-lucchetto.txt`, presa il 30 agosto 2026. **La prima stesura di questa scheda era a memoria e sbagliava due cose**: diceva che il lucchetto è uno dei giochi più antichi del repertorio (è del 1950) e dava uno schema approssimativo. La correzione è nel testo qui sopra, e vale la pena tenerla come misura di quanto la memoria sia inaffidabile proprio dove suona più sicura.

Un'osservazione strutturale: il lucchetto è uno dei pochi giochi enigmistici in cui **la meccanica ha una forma fisica ovvia**. Due strisce di carta che si sovrappongono sulla parte comune e la nascondono producono esattamente la stessa operazione, e chi la vede la capisce senza spiegazioni. La maggior parte degli altri giochi del capitolo non ha questa fortuna.

## Esempi trovati

Dalla fonte: *mais / sale = maiale*; *luna / nascita = l'uscita*.

Lucchetto doppio: *persona / sonate / tegola = pergola*, dove *sonate* sparisce tutta.

Lucchetti riflessi: *spia / aiola = spola*; *torre / erba = torba*.

Da gioco orale: la catena in cui *casa → sabbia → biada → dado*, che è il lucchetto senza la sottrazione ed è quello che si fa in macchina.

Da materiale didattico: le tessere sillabiche che si incastrano solo se la sillaba combacia — e qui la verifica è nell'oggetto, non in chi corregge.

## Una nostra versione

Il sistema non può costruire un lucchetto. Può fornire il materiale fisico e lasciare che il lucchetto lo faccia chi gioca.

> **Le strisce che si mangiano**
>
> In fondo al foglio ci sono dodici strisce, ognuna con una parola. Ritagliale.
>
> Due strisce si possono agganciare se **la fine dell'una è l'inizio dell'altra**. Sovrapponile su quella parte, così che si veda una volta sola.
>
> Quando lo fai, leggi che cosa resta se togli anche quella. A volte non resta niente. A volte resta una parola.
>
> ```
>  ho trovato   ─────────  +  ─────────   e resta  ─────────
>  ho trovato   ─────────  +  ─────────   e resta  ─────────
>  ho trovato   ─────────  +  ─────────   e resta  ─────────
> ```
>
> Con dodici strisce gli agganci possibili sono più di tre. Trovane tre e hai finito; se ne trovi otto, il foglio non basta e va bene lo stesso.

Le dodici strisce sono materiale, e il materiale si corregge da sé: la sillaba combacia o no, e si vede sovrapponendo. Il sistema deve solo stampare dodici parole scelte perché alcune si aggancino — il che è alla sua portata, perché la sillaba iniziale e finale di una parola sono cose che un modello sa dire, a differenza delle lettere in mezzo.

## Da riprendere alla rassegna

**La distinzione fra sillabe agli estremi e lettere in mezzo** sembra il confine vero del limite tecnico. Un modello sbaglia a contare e a permutare le lettere; sa però dire come comincia e come finisce una parola. Se il confine è questo, una parte del capitolo 12 è recuperabile e un'altra no, e vale la pena stabilire dove passa con una prova invece che a intuito.

**Il gioco reso oggetto** — strisce che si sovrappongono — toglie insieme il problema della generazione e quello della verifica. È la stessa mossa vista alla voce 010 con i pezzi da rimettere insieme, e comincia a sembrare una strategia generale e non un caso.

**Una famiglia che si è costruita per differenze minime.** Sciarada, sciarada incatenata, biscarto, lucchetto, lucchetto riflesso: ogni gioco nasce cambiando una regola sola del precedente, e ci sono voluti cent'anni. È un modo di generare forme — prendine una e cambia una regola — che si potrebbe applicare a tutto l'elenco alla rassegna.
