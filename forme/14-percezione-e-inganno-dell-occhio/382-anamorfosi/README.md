# Anamorfosi

- **Numero** 382 nell'enciclopedia, capitolo 14 — Percezione e inganno dell'occhio
- **Si chiama anche** anamorfismo, prospettiva depravata, prospettiva curiosa, anamorfosi a specchio o catottrica, anamorfosi obliqua, tabula scalata, *anamorphosis*, *anamorphic perspective*
- **In una riga** un'immagine che si compone solo guardandola da un punto o in uno specchio.
- **Contratto** voce breve
- **Fonti** `anamorphosis.txt`, `it-anamorfismo.txt`, `the-ambassadors-holbein.txt`, `ames-room.txt`, `trompe-loeil.txt`, lette il 2 settembre 2026. I conti dell'esempio sono nostri, in `build/check_378.py`
- **Stato della ricerca** fatta, 2 settembre 2026

## Che cos'è

Una proiezione deformata che richiede a chi guarda di occupare un punto preciso, o di usare uno strumento, o tutti e due, perché l'immagine torni riconoscibile (`anamorphosis.txt`). Da ogni altro punto è una macchia.

Parti mobili:

- **Che cosa raddrizza l'immagine.** La posizione dell'occhio (anamorfosi obliqua), uno specchio curvo — cilindrico o conico — appoggiato sul disegno (catottrica), o un supporto ondulato con due immagini sui due versanti (*tabula scalata*).
- **Quanto è estrema la deformazione.** Nelle anamorfosi rinascimentali basta guardare di sbieco; nelle più spinte l'immagine dritta è irriconoscibile.
- **Se il punto di vista è dichiarato.** Un segno sul foglio, oppure niente, e allora trovarlo è il compito.
- **Quante immagini contiene il supporto.** Una, oppure due che si escludono.

**Qui la prova non sta né in uno strumento né in un argomento: sta nella posizione della testa di chi guarda**, e questa è una risposta nuova alla domanda che ha retto il capitolo 13. Il foglio contiene **una** risposta, l'occhio non ne vede nessuna finché non si sposta, e quando si sposta la vede tutta insieme.

## Da dove viene

**L'esempio noto più antico è di Leonardo**, nel *Codice Atlantico* (1483–1518): l'occhio disegnato in anamorfosi. Leonardo eseguì poi commissioni anamorfiche di grande formato per il re di Francia (`anamorphosis.txt`).

Prima c'è un antefatto e una gara. `anamorphosis.txt` riporta che le pitture di Lascaux potrebbero usare la tecnica, perché gli angoli obliqui della grotta deformerebbero altrimenti le figure; e riporta da Plinio e da Tzetze la gara fra Alcamene e Fidia per una Minerva: quella di Alcamene era bella e quella di Fidia grottesca, ma montate sui pilastri fu la seconda a risultare bella.

**Il Seicento la trasforma in scienza applicata.** Salomon de Caus, *Perspective*, **1612**; Jean-François Niceron, *La perspective curieuse*, **1638**, che distingue tre tipi di anamorfosi su larga scala: ottica (si guarda in orizzontale), anottrica (verso l'alto) e catottrica (dall'alto in basso). Il primo manuale europeo di anamorfosi a specchio è del **1630 circa** ed è del matematico Vaulezard. L'anamorfosi a specchio era già praticata in Cina sotto i Ming, a mano libera invece che con la griglia, e la pagina considera probabile che l'influenza sia andata dalla Cina all'Europa e non viceversa.

**È servita anche a nascondere.** Ritratti anamorfici segreti di sovrani deposti: uno di Edoardo VI del **1546**, visibile solo attraverso un foro nella cornice; molti di Carlo I dopo l'esecuzione del **1649**; e uno a specchio di Bonnie Prince Charlie, al West Highland Museum, riconoscibile solo mettendo un cilindro lucido nel punto giusto — possederne uno, dopo Culloden nel 1746, sarebbe stato tradimento.

## Varianti e parenti

- **Anamorfosi obliqua** — una trasformazione affine del soggetto; si guarda di sbieco.
- **Anamorfosi catottrica** — uno specchio cilindrico o conico appoggiato sul disegno. `anamorphosis.txt` fa notare la differenza pratica: a differenza di quella prospettica, **si può guardare da molte angolazioni**.
- **Tabula scalata** — un supporto ondulato con un'immagine diversa su ogni versante. Di fronte è un miscuglio; da destra una cosa, da sinistra un'altra.
- **Trompe-l'œil** — `trompe-loeil.txt`: «ingannare l'occhio», la pittura che fa sembrare reale un oggetto dipinto. È il fine; l'anamorfosi è uno dei mezzi.
- **Cupola dipinta** — Andrea Pozzo dipinge a Sant'Ignazio, a Roma, l'interno di una cupola su un soffitto piatto, perché i monaci vicini si lamentavano della luce tolta. **C'è un punto solo in cui la cupola non è deformata.**
- **Stanza di Ames** — una stanza di quadrilateri irregolari che da un buco appare rettangolare, e che fa sembrare le persone giganti o nane a seconda dell'angolo in cui stanno.
- **Scritte sull'asfalto** — allungate apposta perché chi guida le legga dritte, e le insegne dipinte sui campi da gioco, che stanno in piedi solo dal punto della telecamera (`it-anamorfismo.txt`).
- **Voce 381, impossibile geometrico** — la stessa tecnica costruisce nello spazio gli oggetti impossibili: `anamorphosis.txt` ha una sezione apposta, e dice che il cubo di Necker e il triangolo di Penrose si possono scolpire in tre dimensioni con l'illusione anamorfica.
- **Voce 394, prospettiva forzata** — la fotografia che sfrutta la stessa geometria su oggetti veri.
- **Voce 175, puzzle ottico** — quella scheda dichiara che questa voce è del capitolo 14 e non viene presa lì. Regge.
- **Voce 138, testo capovolto o ruotato** — quella scheda chiama questa forma «il parente tridimensionale» degli ambigrammi. Riletta: regge, e le due si toccano proprio sulla *tabula scalata*, che è un ambigramma di supporto.

## Che cosa se ne sa

**La geometria è tutta qui e si calcola con una divisione.** Mettendo l'occhio a 40 mm sopra il foglio e la prima riga a 120 mm da lui, un quadro dritto alto 20 mm si stende sul foglio in questo modo: la riga alta *z* cade a 120 × 40 / (40 − *z*) millimetri. `build/check_378.py` fa il conto per undici righe e verifica la cosa che conta, cioè che **gli angoli sotto cui l'occhio vede le righe sul foglio coincidano con quelli sotto cui vedrebbe il quadro dritto**, e lo stesso per la larghezza di ogni sbarra. Il disegno deformato è **lungo 120 mm dove il quadro dritto ne misura 20**, cioè sei volte tanto, e sta su un A4. I passi si allargano andando avanti: il primo è 6,32 mm, l'ultimo 21,82.

**La deformazione non è uniforme, e il rapporto ha una forma chiusa.** L'ultimo passo sta al primo come *h*(*h* − *dz*) sta a (*h* − *L* + *dz*)(*h* − *L*), dove *h* è l'altezza dell'occhio, *L* l'altezza del quadro e *dz* il passo: **3,45 volte** con questi numeri. Lo script asserisce la formula, non il numero, così che cambiando l'esempio il controllo resti valido.

**Il quadro più famoso della famiglia, e una discordanza sul come lo si guarda.** *Gli ambasciatori* di Hans Holbein il Giovane, **1533**: la macchia grigia in basso è un teschio. `anamorphosis.txt` dice che si vede guardando da un angolo acuto, e ipotizza che il quadro fosse appeso accanto a una scala per far comparire il teschio all'improvviso. `the-ambassadors-holbein.txt` è più preciso e più cauto: **la maggior parte degli studiosi ritiene che vada guardato di lato — da in alto a destra o da in basso a sinistra —, altri che si usasse un tubo di vetro per vederlo di fronte.** Aggiunge che una tesi di Edgar Samuel del 1962 propone un'ottica apposita, e che uno studio con il Warburg Institute e la British Optical Association ha escluso i dispositivi complessi. `it-anamorfismo.txt` sceglie una versione sola — da destra, con la testa vicina al piano — e non ha note.

**La stanza di Ames ha tre date e una delle pagine lo dichiara.** `anamorphosis.txt` scrive che fu inventata da Adelbert Ames Jr. nel **1946**. `ames-room.txt` scrive che Ames la brevettò nel **1940**, che secondo Behrens «già nel 1934 Ames progettò la sua prima stanza distorta», che altri autori dicono 1946, e conclude che **la data esatta non è stabilita**. Si tiene la pagina che dichiara l'incertezza, e si registra che la pagina generale ha scelto una delle tre senza dirlo.

**La tecnica è ancora in uso, e uno dei suoi impieghi si guarda ogni giorno.** Le scritte allungate sull'asfalto e i marchi dipinti sui campi da gioco (`it-anamorfismo.txt`), e i formati cinematografici anamorfici — CinemaScope, Panavision, Omnimax — che comprimono lateralmente in ripresa e riespandono in proiezione.

**Un caso in cui l'immagine era fatta di persone.** Arthur Mole, fotografo commerciale americano, durante la Grande Guerra: la *Human Statue of Liberty* del **1919** — **12 000 persone nella fiamma della torcia e 6 000 in tutto il resto della figura** —, che si ricompone solo dalla torre di ripresa. La sproporzione fra i due numeri è la misura della deformazione.

## Esempi trovati

Da Holbein, 1533: un teschio disteso sul pavimento di un quadro, che si alza in piedi quando ci si sposta.

Da Sant'Ignazio a Roma: una cupola che non c'è, con un disco di marmo sul pavimento che segna il punto da cui guardarla.

Dal West Highland Museum: un principe in esilio dentro una macchia, e uno specchio cilindrico che lo tira fuori.

Dall'asfalto: la parola che si legge dritta dal parabrezza e che, passandoci sopra, è lunghissima.

Da Julian Beever, e in Italia da Alessandro Diddi e da Manu Invisible (`it-anamorfismo.txt`): disegni su marciapiede e su muro che da un punto escono dal piano.

## Una nostra versione

> **Il punto da cui la scala è dritta**
>
> Segna una crocetta in fondo al foglio, sul bordo corto. Tutte le distanze si misurano da lì.
>
> Disegna undici sbarre orizzontali, centrate sulla mezzeria del foglio. Ognuna sta a una distanza dalla crocetta e ha una sua lunghezza:
>
> ```
>  sbarra       a  lunga
>       0  120 mm  30 mm
>       1  126 mm  32 mm
>       2  133 mm  33 mm
>       3  141 mm  35 mm
>       4  150 mm  38 mm
>       5  160 mm  40 mm
>       6  171 mm  43 mm
>       7  185 mm  46 mm
>       8  200 mm  50 mm
>       9  218 mm  55 mm
>      10  240 mm  60 mm
> ```
>
> Guardato dall'alto è una scala storta, con i pioli sempre più larghi e sempre più lontani.
>
> Adesso appoggia il foglio sul tavolo, metti il mento sopra la crocetta e **abbassa l'occhio fino a quattro centimetri dal foglio**, guardando lungo il foglio.
>
> Da lì i pioli sono **tutti uguali e tutti alla stessa distanza**. Non da mezzo centimetro più su, non da un dito più a destra.
>
> Poi rifallo con un disegno tuo: prendi un quadretto alto 2 cm, dividilo in dieci righe, e riporta ogni riga alla distanza scritta qui sopra.

Undici numeri, un righello e nessun altro materiale. Chi stampa conosce la risposta prima — la scala dritta è quella che ha deformato — e chi guarda la verifica da sé, muovendo la testa.

**Qui la fotografia non serve a niente, ed è la prima volta nel blocco.** Il sistema legge una fotografia del foglio, e una fotografia presa da sopra restituisce esattamente la macchia deformata: dell'effetto non resta traccia. Non è un problema di risoluzione o di bianco e nero, è che l'oggetto da verificare non sta sul foglio, sta nella posizione dell'occhio. Quello che si può chiedere indietro è il disegno rifatto dal lettore, che è una consegna vera e una prova indiretta.

## Da riprendere alla rassegna

**La prima voce in cui il verificatore è escluso per geometria.** Non «la fotografia viene male», ma «l'effetto non è nel piano fotografato». Alla rassegna: le forme di questo genere si consegnano lo stesso, e quello che torna indietro è la costruzione invece del risultato. Vale probabilmente anche per la voce 394, prospettiva forzata e per la voce 395, stereogramma.

**Un'immagine che è lunga sei volte quello che rappresenta.** Il rapporto fra l'ingombro e il contenuto è il costo di questa forma in carta, e si calcola prima: dipende solo dall'altezza dell'occhio e da quella del quadro. Con l'occhio a 4 cm e la prima riga a 12 cm, **un quadro dritto più alto di 23,8 mm non ci sta su un A4**, e avvicinandosi a 4 cm la lunghezza va all'infinito.

**La riga di differenza.** Alla voce 378, illusione ottica geometrica la prova sta in uno strumento. Alla voce 381, impossibile geometrico sta in un argomento. Alla voce 379, ambiguità figura-sfondo e alla voce 380, figura reversibile non sta in nessun posto. Qui sta **nella posizione del corpo di chi guarda**, ed è un valore che la scala non aveva in 381 voci.

