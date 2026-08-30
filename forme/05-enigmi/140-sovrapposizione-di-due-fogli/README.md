# Sovrapposizione di due fogli

- **Numero** 140 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi verbali»
- **Si chiama anche** crittografia visiva, condivisione visiva di un segreto, *visual cryptography*, *visual secret sharing*, moiré, sovrapposizione in controluce, due lucidi
- **In una riga** la risposta appare mettendo due pagine in controluce.
- **Fonti** `visual-cryptography.txt` e `moire-pattern.txt`, prese il 30 agosto 2026 da en.wikipedia
- **Stato della ricerca** fatta, 30 agosto 2026

## Che cos'è

Nessuno dei due fogli dice niente. Messi uno sopra l'altro e guardati in controluce, dicono una cosa. Il gesto è **sovrapporre**, e distingue questa voce dalle vicine: alla voce 137, specchio si affianca uno specchio, alla voce 138, testo capovolto o ruotato si gira la pagina, qui ce ne vogliono due.

Ci sono tre meccanismi diversi che producono lo stesso gesto, e vale la pena tenerli separati perché si comportano in modo molto diverso.

**Complementarità.** Ogni cella del primo foglio ha una metà nera scelta a caso; il secondo foglio, cella per cella, sceglie la stessa metà o l'altra. Sovrapposti, «stessa metà» dà mezza cella nera e «altra metà» dà una cella tutta nera. Ne esce un'immagine in due grigi. Preso da solo, ciascuno dei due fogli è indistinguibile da un disegno casuale.

**Interferenza.** I due fogli portano due trame regolari quasi uguali — quasi, non uguali: spostate, ruotate di poco, o con un passo leggermente diverso. Dalla sovrapposizione nasce una terza figura, molto più grande delle due trame, che non sta in nessuno dei due fogli. È il moiré.

**Divisione del contenuto.** Un foglio porta metà dei tratti delle lettere e l'altro il resto. Non c'è nessun principio, solo un taglio. È il caso semplice, ed è quello che si costruisce a mano in cinque minuti.

Parti mobili:

- **Se un foglio da solo dice qualcosa.** Nella complementarità no, per costruzione. Nel moiré nemmeno, ma per un'altra ragione: una trama regolare non è casuale, è solo priva di informazione. Nella divisione del contenuto sì, e spesso troppo.
- **Il registro.** Quanto precisamente i due fogli devono combaciare. È il parametro che decide se la cosa funziona su carta o solo su lucidi.
- **Chi ha il secondo foglio.** È la parte mobile che trasforma la forma: se ce l'ha la stessa persona è un enigma, se ce l'ha qualcun altro è una serratura a due chiavi.

## Da dove viene

La versione formale è recente e ha una data. Nel 1994 **Moni Naor e Adi Shamir** presentarono uno schema di condivisione visiva di un segreto: un'immagine in bianco e nero viene divisa in *n* parti stampate su altrettanti lucidi, e **solo chi le ha tutte e *n* può decifrarla, mentre *n* − 1 parti non dicono assolutamente niente.** La decifrazione non richiede nessun calcolo: si mettono i lucidi uno sopra l'altro e si guarda. Esistono generalizzazioni, fra cui lo schema *k su n*, in cui bastano due lucidi qualsiasi presi da un insieme più grande.

La pagina segnala che alcuni antecedenti stanno in brevetti degli anni Sessanta, e altri nel lavoro sulla percezione e sulla comunicazione sicura. Non li elenca.

Il moiré è molto più vecchio del suo nome scientifico, e il nome viene dai tessuti: *moire* è la seta marezzata, quella con l'aspetto «bagnato», ottenuta pressando due strati di tessuto da umidi. La spaziatura simile ma imperfetta dei fili produce il disegno caratteristico, che resta quando il tessuto asciuga. In francese il sostantivo è in uso dal Seicento, prestito dall'inglese *mohair*; il verbo *moirer* è del Settecento e l'aggettivo *moiré* è attestato almeno dal 1823.

## Varianti e parenti

- **Crittografia visiva a due parti** — il caso base: due lucidi, e sovrapposti danno l'immagine.
- **Schema *k* su *n*** — le parti sono molte e ne bastano due qualsiasi.
- **Moiré di linee** — due strati con linee correlate. Muovendo uno strato la figura si sposta più veloce del movimento: si chiama *optical moiré speedup*, ed è un ingranditore di movimento.
- **Moiré di forma** — uno strato opaco con sottili righe trasparenti sopra uno strato in cui una forma si ripete periodicamente. **La figura che ne esce è ingrandita**, in una direzione o in tutte e due. Il caso quotidiano è guardare una rete metallica attraverso una seconda rete identica: la struttura fine resta visibile anche da molto lontano.
- **Voce 389, moiré** — nel capitolo 14, quello della percezione. Il confine va dichiarato ed è lo stesso già usato per il capitolo 12: **lì il moiré si descrive come fenomeno dell'occhio, cioè come una figura che si vede e non c'è; qui si descrive come operazione sul foglio, cioè come una cosa che bisogna fare alla carta per leggerla.** Quella voce non è ancora scritta.
- **Voce 390, immagine da comporre in controluce** — sempre nel capitolo 14, ed è la vicina più stretta di tutte. Anche quella non è ancora scritta, e il confine è lo stesso: la 390 guarderà che cosa succede all'occhio quando due immagini si sommano, questa guarda che cosa bisogna stampare perché si possano sommare.
- **Voce 141, griglia di Cardano** — anche lì si appoggia un foglio su un altro, ma uno dei due è una maschera con dei buchi e l'altro è un testo che si legge già da solo. Qui nessuno dei due si legge.
- **Voce 5, corrispondenza (matching)** — la parentela lontana: due colonne che si appaiano. Qui l'appaiamento lo fa la luce invece della matita.
- **Voce 81, altra persona** — quando il secondo foglio ce l'ha qualcun altro, la forma diventa una ragione materiale per cui due persone devono incontrarsi.

## Che cosa se ne sa

**La proprietà di sicurezza è forte e si dice in una riga.** Un foglio da solo non dice niente sull'immagine: è indistinguibile da una distribuzione casuale di coppie di mezze celle. E c'è di più, e `visual-cryptography.txt` lo scrive esplicitamente: **avendo un foglio, si può costruire un secondo foglio falso che, sovrapposto al primo, produce qualunque immagine si voglia.** Questo vuol dire che un foglio solo non è la prova di niente — non solo non rivela il segreto, ma non testimonia nemmeno che ci fosse un segreto. È la stessa proprietà del blocco monouso, e la pagina lo dice: con due lucidi si può realizzare un *one-time pad*, dove uno è la chiave casuale condivisa e l'altro il testo cifrato.

**Il moiré ingrandisce, e questo è il suo uso tecnico.** Nell'industria si misura la deformazione dei materiali disegnando una griglia sull'oggetto e sovrapponendole una griglia di riferimento: **la scala della figura di moiré è molto più grande della deflessione che la causa**, e per questo la misura diventa facile. La stessa idea è stata provata per costruire cursori e manopole senza elettronica dentro: due strati stampati, uno fermo e uno mobile, e una fotocamera qualunque legge spostamenti minuscoli dalla figura amplificata.

**Un segnale marittimo funziona con questo principio, e va guardato perché è una consegna già fatta.** Le *Inogon leading marks* sono fari costieri che, per effetto moiré, mostrano frecce che puntano verso la linea di passaggio sicuro; **quando la nave attraversa quella linea le frecce diventano bande verticali, e poi ricominciano a puntare nell'altro senso.** Lo stesso sistema è installato negli aeroporti per aiutare i piloti a restare in mezzo alla linea mentre parcheggiano. È un'informazione continua e senza numeri, che dice contemporaneamente da che parte sei e quanto sei lontano.

**Il moiré è quasi sempre un difetto, e la parola stessa lo dice.** Nella stampa a colori la sovrapposizione dei retini in ciano, giallo, magenta e nero produce inevitabilmente un moiré; il mestiere consiste nello scegliere angoli e frequenze che lo rendano così fitto da non vedersi. La pagina è netta: **nelle arti grafiche «moiré» significa un moiré eccessivamente visibile.** E la sua comparsa non è del tutto prevedibile — gli stessi retini danno buoni risultati con certe immagini e moiré visibile con altre. Ai giornalisti televisivi si insegna a non mettere giacche a spina di pesce per lo stesso motivo.

**Le banconote sfruttano il difetto.** Molte contengono disegni circolari o ondulati fitti, scelti apposta perché uno scanner ci produca sopra un moiré vistoso quando qualcuno prova a copiarle. È l'unico caso raccolto in cui una forma viene stampata **perché si rompa** in mano a chi non deve usarla.

**Quello che le fonti non dicono.** Nessuna delle due riporta un numero su quanta luce passi attraverso due fogli di carta comune sovrapposti, e questo è esattamente il dato che serve a noi. La crittografia visiva è descritta su lucidi, sempre. Se funzioni su carta da stampante tenuta contro una finestra **va verificato**, e si verifica in cinque minuti.

## Esempi trovati

Da Naor e Shamir, 1994: due lucidi che sembrano rumore e che sovrapposti mostrano una parola. È l'immagine standard con cui si insegna la cosa, e la si trova riprodotta ovunque.

Dalla rete metallica guardata attraverso un'altra rete metallica: la struttura fine resta leggibile a grande distanza. È l'esempio che la fonte dà per l'ingrandimento di forma, e non costa niente perché le reti ci sono già.

Dai fari di Southampton Water, sulla sponda orientale di fronte alla raffineria di Fawley: un segnale che mostra frecce finché non si è in rotta e bande verticali quando ci si è.

Dalle fotografie di uno schermo televisivo fatte con una macchina digitale: due griglie di scansione che litigano. La fonte dà anche il rimedio, che è un numero — inquadrare lo schermo a trenta gradi.

Dalle banconote e dai filtri *descreen* degli scanner: la stessa figura, una volta voluta e una volta tolta.

Dal microscopio a illuminazione strutturata: il moiré usato per ottenere immagini con una risoluzione più fine del limite di diffrazione, cioè per vedere una cosa più piccola di quanto la luce consenta.

## Una nostra versione

Il sistema stampa più fogli per volta e in bianco e nero, e questa è la prima forma del capitolo in cui i suoi limiti giocano a favore: **due fogli costano quanto uno.** Il vincolo vero è un altro, ed è materiale — la carta non è un lucido. In controluce contro una finestra la carta da 80 grammi lascia passare abbastanza luce da distinguere il bianco dal nero, ma il contrasto è debole e non l'ho misurato.

> **Il foglio che non dice niente**
>
> Questo foglio è pieno di quadretti, e ogni quadretto ha una metà nera. Da che parte sta la metà nera è stato deciso tirando a sorte, quadretto per quadretto. **Non c'è niente scritto qui dentro. Davvero niente.**
>
> ```
>  ┼─────────────────────────────────────────────────┼
>  │ ▐ ▌▐ ▌▌▐ ▌▐ ▐ ▌▌▐▐ ▌▐ ▌▐▐ ▌▌▐ ▌▐ ▌▐ ▌▌▐ ▐ ▌▐ ▌ │
>  │ ▌▐▐ ▌▐ ▌▐ ▌▌▐ ▐ ▌▐▐ ▌▌▐ ▌▐ ▌▐ ▌▌▐ ▐ ▌▐ ▌▐ ▌▐ ▌ │
>  │        (dodici righe di quadretti sorteggiati)    │
>  ┼─────────────────────────────────────────────────┼
>       (i quattro crocini agli angoli servono dopo)
> ```
>
> Sull'altro foglio c'è la stessa griglia, vuota. Riempila così, un quadretto alla volta:
>
> - vuoi che il quadretto, alla fine, sia **nero**? Anneriscine la metà **opposta** a quella già nera qui;
> - vuoi che resti **grigio**? Anneriscine la **stessa** metà.
>
> I quadretti neri disegnano quello che vuoi tu. Una parola, una freccia, un numero, una faccia. **Io che ho stampato questo foglio non lo saprò mai**, perché ho stampato solo il sorteggio.
>
> Quando hai finito, appoggia i due fogli uno sull'altro facendo combaciare i quattro crocini, e tienili contro una finestra.
>
> Poi c'è una cosa strana da provare, e vale più del disegno. Prendi un terzo foglio con la griglia vuota, e riempilo per far comparire **una cosa completamente diversa.** Funziona uguale. Quindi guarda il primo foglio e dimmi: **guardandolo da solo, si può capire quale delle due cose ci fosse dentro?**
>
> ```
>  ────────────────────────────────────────────────────
> ```

Il sistema stampa il sorteggio e la griglia vuota, e non sa che cosa uscirà: è la tabella stampata vuota già raccolta alle voci 129, cifrario a sostituzione, 131, codice a numeri (A=1) e 134, semaforo, bandiere, alfabeti alternativi, e qui è la forma più pura, perché il contenuto non esiste finché qualcuno non lo scrive. La verifica è fisica e immediata — la finestra dice sì o no — e appartiene alla famiglia raccolta alle voci 7, classificazione in insiemi, 10, riordino di un testo tagliato a pezzi, 26, istruzioni, 42, piegatura e 45, composizione fisica.

L'ultima domanda è la parte che insegna qualcosa: il primo foglio non contiene il segreto, e non contiene nemmeno l'informazione che ci fosse un segreto. Chi arriva a rispondersi di no ha capito da solo perché un blocco monouso non si rompe, e ci è arrivato con dei quadretti.

Due limiti dichiarati. Il registro: i quadretti devono essere grandi — otto millimetri, con le metà da quattro — perché due fogli allineati a mano non stanno mai a mezzo millimetro, e i crocini agli angoli servono a questo. E la luce: su carta da stampante il contrasto fra grigio e nero è debole, la finestra deve essere quella giusta, e **se non funziona non è colpa di chi ha riempito la griglia** — va detto sul foglio prima, non dopo.

## Da riprendere alla rassegna

**È la forma in cui il sistema può stampare un segreto che non conosce.** Non «stampa la cornice e la mano scrive dentro», che è già stato osservato sei volte: qui il foglio stampato è metà di un messaggio la cui altra metà non esiste ancora, e resta metà di qualunque messaggio si decida dopo. Alla rassegna vale la pena chiedersi quante altre forme abbiano questa proprietà, perché è la risposta più netta trovata finora alla domanda su chi sappia la risposta.

**Il secondo foglio dato a qualcun altro è una serratura a due chiavi, e non richiede fiducia.** Sta accanto al taglia-e-scegli della voce 72, negoziare: nessuno dei due può leggere da solo e nessuno dei due deve credere all'altro. È la sesta forma di procedura che non richiede fiducia raccolta dall'enciclopedia, e la prima fatta di carta.

**Il moiré ingrandisce un movimento troppo piccolo per essere visto,** ed è una cosa che l'elenco non ha da nessuna parte: una forma il cui esito è **vedere una cosa che c'era e che era sotto la soglia.** Vicina alla voce 63, inferire da un'assenza e alla voce 52, osservare, e diversa da tutte e due perché lo strumento è un foglio.

**Una figura stampata perché si rompa in mano a chi non deve usarla.** Le banconote contengono disegni scelti apposta perché uno scanner li guasti. Nessuna forma dell'enciclopedia è progettata per fallire in una condizione precisa, ed è un'idea che vale la pena tenere da parte.

**Il confine con il capitolo 14 si pone due volte e nello stesso modo.** Le voci 389, moiré e 390, immagine da comporre in controluce descriveranno il lato dell'occhio; questa descrive il lato del foglio. Quando quel capitolo si scriverà, questa distinzione va rifatta da lì, e conviene che le tre voci si citino a vicenda.

Da verificare: quanto passa la luce attraverso due fogli di carta da stampante sovrapposti, e se il contrasto fra mezza cella nera e cella intera nera si distingua a occhio in controluce. Tutte le fonti descrivono la cosa su lucidi.
