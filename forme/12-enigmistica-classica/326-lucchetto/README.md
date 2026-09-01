# Lucchetto

- **Numero** 326 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che uniscono o dividono parole»
- **Si chiama anche** lucchetto, biscarto, lucchetto riflesso, XZ/ZY=XY
- **In una riga** due parole con una parte comune che sparisce: la parte comune è la chiave.
- **Fonti** `it-lucchetto.txt`, presa il 30 agosto 2026; `it-biscarto.txt`, `it-cerniera.txt`, `it-doppia-estrazione.txt`, `longest-common-substring.txt`, prese il 1 settembre 2026
- **Stato della ricerca** fatta, 30 agosto 2026, ampliata il 1 settembre 2026

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
- **Cerniera** (329) — lo stesso doppio scarto con le chiavi dalla parte opposta: ZX / YZ = XY, in capo alla prima e in coda alla seconda. La prima stesura di questa scheda diceva «in mezzo a entrambe», che è invece il biscarto centrale; corretto il 1 settembre 2026 su `it-cerniera.txt`.
- **Doppia estrazione** — la chiave sta ai due estremi di tutte e due le parole: ZXZ / ZYZ = XY (`it-doppia-estrazione.txt`).
- **Incastro** (328) — una parola entra dentro l'altra invece di agganciarsi.
- **Sciarada** (323) — due parole si sommano senza che nulla cada.
- **Sciarada incatenata** (325) — XZ / ZY = XZY: la parte comune resta. È il lucchetto senza la sottrazione, e lo precede di mezzo secolo.
- **Catena di parole** — la versione orale e infinita, quella che si fa in macchina.
- **Domino di sillabe** — tessere fisiche che si agganciano per sillaba.

## Che cosa se ne sa

Fonte: `_reference/esercizi-e-sfide/it-lucchetto.txt`, presa il 30 agosto 2026. **La prima stesura di questa scheda era a memoria e sbagliava due cose**: diceva che il lucchetto è uno dei giochi più antichi del repertorio (è del 1950) e dava uno schema approssimativo. La correzione è nel testo qui sopra, e vale la pena tenerla come misura di quanto la memoria sia inaffidabile proprio dove suona più sicura.

Un'osservazione strutturale: il lucchetto è uno dei pochi giochi enigmistici in cui **la meccanica ha una forma fisica ovvia**. Due strisce di carta che si sovrappongono sulla parte comune e la nascondono producono esattamente la stessa operazione, e chi la vede la capisce senza spiegazioni. La maggior parte degli altri giochi del capitolo non ha questa fortuna.

Quello che segue è stato aggiunto il 1 settembre 2026, leggendo le tre pagine della famiglia.

**Le quattro caselle sono tutte piene e ognuna ha un nome proprio.** La chiave può stare in capo o in coda alla prima parola, e in capo o in coda alla seconda: quattro combinazioni. L'enigmistica italiana le ha battezzate tutte e quattro — coda/capo è il lucchetto, capo/coda è la cerniera, capo/capo è il biscarto iniziale, coda/coda è il biscarto finale (`it-biscarto.txt`, `it-cerniera.txt`) — e nessuna delle tre pagine mette insieme la tabella. L'elenco è stampato per esteso in `build/check_323.py`.

**Il capostipite della famiglia è stato inventato tredici anni dopo il suo primo discendente, dalla stessa persona.** Il lucchetto è del 1950; il biscarto, di cui il lucchetto è un caso particolare, è del 1963, ancora di Carminetta. `it-biscarto.txt` lo chiama «il capostipite (in senso logico se non cronologico)»; `it-lucchetto.txt` dice che il biscarto «è stato inventato da Carminetta ma in un momento successivo». La cerniera sta in mezzo, 1955, del Novellino, e si chiamava dapprima *conchiglia*; poi la doppia estrazione, 1973, di Giupin, e la cernita del 1975. Le sette date sono ordinate e verificate in `build/check_323.py`.

**Il gioco è meccanico in un verso e impossibile nell'altro.** Partendo dalle due parole, la chiave si trova leggendo: sulle cinque coppie della scheda qui sotto ce n'è **una sola** per coppia, e il totale è determinato. Partendo dal totale non c'è niente da cercare, perché la chiave non compare nel risultato: guardando *maiale* non c'è nulla che dica se fosse una S. Delimitando a mano la chiave a tre lettere, su un totale di otto e con l'alfabeto italiano di ventuno lettere i candidati sono 7 × (21 + 21² + 21³) = **68 061**, contro i 7 tagli di una sciarada; senza quel limite lo spazio non è grande, è infinito. Conto per formula e per enumerazione in `build/check_323.py`.

Un limite alla frase «una sola per coppia»: non è una legge. *banana / anatra* ha due sovrapposizioni, *a* e *ana*, e nessuna delle due dà una parola. Le cinque coppie della scheda sono state scelte controllando che la chiave fosse unica.

Fuori dalla famiglia, l'operazione «il pezzo più lungo in fondo alla prima che è anche in testa alla seconda» è quella che l'informatica usa per rimettere insieme frammenti sovrapposti. La pagina che se ne occupa, `longest-common-substring.txt`, è stata presa e **non è citabile sui costi**: l'estrazione a testo perde le formule, e le complessità arrivano come «time using» senza l'espressione. Si dice e si va avanti.

## Esempi trovati

Dalla fonte: *mais / sale = maiale*; *luna / nascita = l'uscita*.

Lucchetto doppio: *persona / sonate / tegola = pergola*, dove *sonate* sparisce tutta.

Lucchetti riflessi: *spia / aiola = spola*; *torre / erba = torba*.

Da `it-cerniera.txt`, per confronto: *vita / navi = tana*, e la stessa terna si può girare — *navi / tana = vita*, *tana / vita = navi*. **La cerniera è ciclica e il lucchetto no**, e le tre rotazioni sono state rifatte in `build/check_323.py`.

Da `it-doppia-estrazione.txt`: *atollo / appello = toppe*, e la tripla *pirone / pitone / pilone = rotolo*.

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

La seconda scheda, scritta il 1 settembre 2026, sta sulla carta e non ha bisogno di forbici.

> **La chiave sparisce, e il resto si tiene**
>
> Ogni riga è una coppia di parole che finisce e comincia allo stesso modo. Quelle lettere in comune sono **la chiave**: scrivila, poi buttala via da tutte e due e attacca quello che resta.
>
> ```
>  PRIMA  SECONDA  LA CHIAVE  IL TOTALE
>  sole   letto    ─────────  ─────────
>  luce   cena     ─────────  ─────────
>  carne  nero     ─────────  ─────────
>  pane   netto    ─────────  ─────────
>  pelo   loro     ─────────  ─────────
> ```
>
> Cinque totali, e sono tutte parole di tutti i giorni. Se una non ti viene, la chiave l'hai presa lunga o corta.
>
> Poi la parte che nessuno ti chiede mai. **Prova a fare il contrario**: prendi LUNA e cerca le due parole di partenza. Non ci riuscirai, e non perché sia difficile — scrivi qui perché.
>
> ```
>  ────────────────────────────────────────────────
> ```

Le cinque righe si controllano da sé: la chiave si legge, non si indovina, e su queste cinque coppie ce n'è una sola possibile. **È l'unica scheda del capitolo 12 in cui la verifica non chiede un vocabolario**, perché non si tratta di giudicare se una stringa sia una parola: si tratta di guardare due parole date e vedere dove combaciano.

La seconda domanda chiede una cosa vera e dimostrabile, e la risposta sta a portata di chi legge: la chiave è stata buttata via, quindi guardando *luna* non c'è niente che dica se fosse *ce*, *na* o altro. È lo stesso meccanismo della voce 321, antipodo — chiedere la regola invece della parola —, e qui la regola è un'impossibilità.

Dove si romperebbe: le cinque coppie le abbiamo cercate a mano e verificate con uno script. Un foglio nuovo ogni settimana avrebbe bisogno di un elenco di parole italiane in casa, perché il sistema non sa manipolare le lettere dentro le parole (`ideas/10 §6`).

## Da riprendere alla rassegna

**La distinzione fra sillabe agli estremi e lettere in mezzo** sembra il confine vero del limite tecnico. Un modello sbaglia a contare e a permutare le lettere; sa però dire come comincia e come finisce una parola. Se il confine è questo, una parte del capitolo 12 è recuperabile e un'altra no, e vale la pena stabilire dove passa con una prova invece che a intuito.

**Il gioco reso oggetto** — strisce che si sovrappongono — toglie insieme il problema della generazione e quello della verifica. È la stessa mossa vista alla voce 010, riordino di un testo tagliato a pezzi con i pezzi da rimettere insieme, e comincia a sembrare una strategia generale e non un caso.

**Una famiglia che si è costruita per differenze minime.** Sciarada, sciarada incatenata, biscarto, lucchetto, lucchetto riflesso: ogni gioco nasce cambiando una regola sola del precedente, e ci sono voluti cent'anni. È un modo di generare forme — prendine una e cambia una regola — che si potrebbe applicare a tutto l'elenco alla rassegna.

Quello che segue è del 1 settembre 2026.

**Una forma può essere meccanica in un verso e impossibile nell'altro, e la differenza non è la difficoltà.** Dalle due parole al totale la chiave si legge; dal totale alle due parole la chiave non c'è più. Alla rassegna, per ogni forma che leghi due cose, va chiesto in quale verso l'informazione si conserva: è la domanda che decide se una consegna si possa correggere da sola.

**La verifica torna nel materiale, e per la prima volta in questo capitolo.** Le voci da 311 a 325 chiedono tutte «è una parola italiana?», e quella verifica sta in un vocabolario. Qui no: le due parole sono stampate, e la chiave si trova guardandole.

**Quattro caselle, quattro nomi, e nessuno ha disegnato la tabella.** Lucchetto, cerniera, biscarto iniziale e biscarto finale sono le quattro combinazioni di *capo* e *coda* sulle due parole, e la disciplina le ha nominate una per una senza mai dire che sono una griglia completa.

**Il capostipite arrivato dopo.** Il lucchetto è del 1950 e il biscarto, di cui è un caso particolare, del 1963, dello stesso autore. Vale tre righe su un foglio perché dice qualcosa di vero su come si generalizza: prima si trova la cosa, poi si capisce di che cosa era un caso.

**La riga di differenza.** Rispetto alla voce 323, sciarada, dove le due parole si accostano e basta: qui si sovrappongono su un pezzo comune, e quel pezzo sparisce da tutte e due.
