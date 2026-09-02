# Moiré

- **Numero** 389 nell'enciclopedia, capitolo 14 — Percezione e inganno dell'occhio
- **Si chiama anche** frange di moiré, figura di interferenza, marezzatura, *moiré pattern*, *moiré fringe*, effetto retino, battimento ottico
- **In una riga** due trame sovrapposte che generano una terza figura.
- **Contratto** voce breve
- **Fonti** `moire-pattern.txt`, `line-moire.txt`, `shape-moire.txt`, `superimposition.txt`, `halftone.txt`, `aliasing.txt`, `wave-interference.txt`, `newtons-rings.txt`, `beat-acoustics.txt`, `vernier-scale.txt`, `it-nonio.txt`, `lenticular-printing.txt`, `op-art.txt`, `bridget-riley.txt`, `it-moire.txt`, lette il 2 settembre 2026. I conti sono nostri, in `build/check_385.py`
- **Stato della ricerca** fatta, 2 settembre 2026

## Che cos'è

Due trame regolari sovrapposte, e una terza figura che si vede e che non sta in nessuna delle due. `moire-pattern.txt`: perché la figura compaia, **le due trame non devono essere identiche** — spostate, ruotate, o con un passo leggermente diverso.

La terza figura è molto più grande delle trame che la producono, e questo è il punto: **il moiré è un ingranditore senza lente.** Una differenza troppo piccola per essere vista diventa una banda larga qualche centimetro.

Parti mobili:

- **Come differiscono le due trame.** Di passo, oppure di angolo. Sono due casi con due formule diverse e, per noi, con due limiti diversi.
- **Di quanto differiscono.** È l'unico parametro: più piccola la differenza, più larghe e distanti le bande.
- **Che cosa portano le trame.** Righe parallele, curve, o una forma ripetuta.
- **Se una delle due si muove.** Muovendola, la figura si sposta molto più in fretta di lei.
- **Se le trame sono regolari.** Anche due nuvole di punti a caso, uguali fra loro e ruotate di poco, producono una figura.

## Da dove viene

**Il nome viene dai tessuti, non dall'ottica.** `moire-pattern.txt`: *moire* è la seta marezzata, quella con l'aspetto «bagnato», ottenuta pressando due strati di tessuto ancora umidi; la spaziatura simile ma imperfetta dei fili produce il disegno, che resta all'asciutto. In francese il sostantivo è in uso dal Seicento, prestito dall'inglese *mohair* attestato nel 1610; il verbo *moirer* è del Settecento e l'aggettivo *moiré* è attestato almeno dal 1823.

In italiano `Moiré` non è la voce del fenomeno: `it-moire.txt` è una pagina di disambiguazione di 1 147 byte che elenca un finissaggio tessile, un comune francese e, come terza riga, l'*effetto moiré*. Sul fenomeno non dice niente, e vale la regola dei due kilobyte e mezzo.

**Il fenomeno fisico ha parenti più antichi e più famosi.** `newtons-rings.txt`: gli anelli di Newton — le frange di interferenza fra una superficie sferica e una piana — sono descritti da Robert Hooke nella *Micrographia* del 1665 e studiati da Newton nel 1666, mentre la peste teneva chiuso il Trinity College. `wave-interference.txt` e `beat-acoustics.txt`: la stessa matematica dà i battimenti, cioè il tono lento che si sente accordando due corde quasi uguali.

**In grafica il moiré è nato come difetto, e la parola stessa lo dice.** `halftone.txt`: la stampa a colori sovrappone quattro retini di punti, e per non farne uscire un moiré visibile li si ruota l'uno rispetto all'altro di angoli scelti. Nelle arti grafiche «moiré» significa un moiré **eccessivamente** visibile. `aliasing.txt` lo colloca in una famiglia più larga: quando si riduce la risoluzione senza filtrare, l'aliasing si presenta sotto forma di figura di moiré.

**In arte è diventato un mestiere negli anni Sessanta.** `op-art.txt`: la *Op art* è quasi sempre in bianco e nero, e `bridget-riley.txt` racconta che nel 1965 il quadro *Current* del 1964 finì sulla copertina del catalogo della mostra *The Responsive Eye* al Museum of Modern Art, che ebbe **oltre 180 000 visitatori** e stroncature quasi unanimi dalla critica.

## Varianti e parenti

- **Moiré di passo** — due trame parallele con passi leggermente diversi. Le bande stanno a distanza `p(p+δp)/δp`.
- **Moiré di rotazione** — due trame uguali ruotate di un angolo. Le bande stanno a distanza `(p/2)/sin(α/2)`, e per angoli piccoli `p/α`.
- **Moiré di linee** — `line-moire.txt`: due strati trasparenti con motivi correlati. Muovendo uno strato la figura si sposta più in fretta: *optical moiré speedup*.
- **Moiré di forma** — `shape-moire.txt`: uno strato opaco con righe trasparenti sottili sopra uno strato in cui una forma si ripete. La forma esce **stirata** lungo un asse e non lungo l'altro, con un fattore che è di nuovo un rapporto fra i due passi.
- **Figure di Glass** — `superimposition.txt`: due strati identici di righe o di punti sparsi **a caso**, ruotati di poco, producono lo stesso genere di figura. Prendono il nome da Leon Glass, 1969.
- **Nonio** — `vernier-scale.txt` dichiara che il principio del moiré è lo stesso della scala del nonio, e `it-nonio.txt` la descrive: una scala secondaria che si legge guardando **quale tacca coincide**. Pierre Vernier, 1631; in molte lingue si chiama *nonius*, dal matematico portoghese Pedro Nunes.
- **Stampa lenticolare** — `lenticular-printing.txt`: una schiera di lenti sopra un'immagine tagliata a strisce, che cambia quando si sposta la testa. Richiede la lente, e la lente noi non la stampiamo.
- **Voce 140, sovrapposizione di due fogli** — quella scheda dichiara il confine con questa e lo dichiara così: **lì il moiré si descrive come operazione sul foglio, cioè come una cosa da fare alla carta per leggerla; qui come fenomeno dell'occhio, cioè come figura che si vede e non c'è.** Riletta contro le fonti nuove: regge, e questa scheda la riprende dal proprio lato.
- **Voce 175, puzzle ottico** — quella scheda nomina questa fra le voci del capitolo 14. Regge.
- **Voce 390, immagine da comporre in controluce** — l'altra voce del blocco fatta di due fogli. Là quello che compare è stato deciso da qualcuno; qui non lo ha deciso nessuno.

## Che cosa se ne sa

**L'ingrandimento è il rapporto fra il passo e la differenza, e su carta lo decide la stampante.** A 600 punti per pollice il passo minimo è **0,0423 mm**. Con righe ogni ventiquattro punti — 1,016 mm — e una differenza di **un punto solo**, che è la più piccola stampabile, le bande stanno a `24 × 25 = 600` punti, cioè **25,4 mm** esatti, e l'ingrandimento è ventiquattro volte. `build/check_385.py` lo ottiene per formula e poi rifacendolo: costruisce davvero le due trame punto per punto, somma l'inchiostro e cerca il periodo della copertura con l'autocorrelazione, senza sapere in anticipo quanto valga. I due metodi danno lo stesso numero.

**E qui c'è il tetto, che è del foglio e non dell'occhio.** Con righe ogni *n* punti e una differenza di un punto, le bande stanno a `n(n+1)` punti; per averne almeno una intera su un A4 alto 297 mm servono meno di 7 016 punti, cioè **n ≤ 83**. **L'ingrandimento massimo di un moiré di passo stampato su un foglio è 83 volte.** Non lo limita la vista: lo limitano insieme la risoluzione della stampante, che fissa la differenza minima, e l'altezza della carta, che fissa la banda massima.

**La rotazione non ha quel tetto, perché l'angolo lo fa la mano.** Ruotando due trame identiche di un decimo di grado l'ingrandimento è **573 volte**, con la stessa stampante. È la prima volta nel capitolo che due varianti della stessa forma hanno due limiti tecnici completamente diversi, e la differenza non è di grado: una dipende dalla precisione di stampa e l'altra no.

**La formula spicciola per la rotazione è buona più di quanto meriti.** `D ≈ p/α` invece di `D = (p/2)/sin(α/2)` sbaglia sempre per difetto, e l'errore **cresce con l'angolo restando sotto lo 0,13% fino a dieci gradi**. Vuol dire che la distanza fra le bande si predice con una divisione, e che chi misura la distanza può ricavare l'angolo allo stesso prezzo.

**Il moiré è un misuratore, e la fonte lo dice per prima.** `moire-pattern.txt`: per misurare l'angolo fra due trame si può guardare l'orientamento delle bande oppure la loro distanza, e **per angoli piccoli conviene misurare la distanza**, perché l'errore va come l'inverso della distanza invece che proporzionalmente. È la stessa idea con cui in industria si misura la deformazione dei materiali: si disegna una griglia sull'oggetto e le si sovrappone una griglia di riferimento, e la figura è molto più grande della deflessione che la causa.

**Le due trame non devono essere regolari.** Le figure di Glass escono anche da due copie identiche di una nuvola di punti sparsi a caso. Per noi vuol dire che la seconda trama può essere una fotocopia della prima, e che non c'è niente da progettare.

**Il bianco e nero non morde e la fotografia sì, in un modo particolare.** La forma è definita sul contrasto, quindi due colori non servono. Ma il sistema legge una fotografia del foglio, e una fotografia di due trame fini produce **il suo** moiré, che si somma a quello vero: è lo stesso motivo per cui ai giornalisti televisivi si insegna a non mettere giacche a spina di pesce, e per cui i programmi degli scanner hanno un filtro *descreen*. La fonte dà anche un rimedio, ed è geometrico: inquadrare a trenta gradi.

## Esempi trovati

Dalla seta marezzata, dal Seicento: due strati di tessuto pressati da umidi.

Dalla rete metallica guardata attraverso una seconda rete identica: la struttura fine resta visibile a grande distanza.

Dai fari costieri *Inogon*: frecce che puntano verso la linea di passaggio sicuro e che diventano bande verticali quando la si attraversa. Gli stessi apparecchi sono installati negli aeroporti per tenere l'aereo in mezzo alla linea mentre parcheggia.

Dalle banconote: disegni circolari fitti messi apposta perché uno scanner ci produca sopra un moiré vistoso.

Dal grafene: due strati sovrapposti e ruotati di un «angolo magico» danno una superreticolo di moiré, e a quell'angolo il materiale diventa superconduttore.

Dagli anelli di Newton, 1665 e 1666: la stessa figura fatta con la luce invece che con l'inchiostro.

## Una nostra versione

> **Due fogli di righe, e una figura che non c'è su nessuno dei due**
>
> Ti do due fogli identici, coperti di righe parallele sottili, una ogni **1,016 mm** — che sono ventiquattro punti della stampante, il passo più vicino al millimetro che sappia fare. Guardali uno alla volta: non c'è niente da vedere, sono righe.
>
> Adesso mettili uno sopra l'altro contro la finestra, e **ruota lentamente quello davanti**. Compaiono delle bande chiare e scure, larghe, che non stanno su nessuno dei due fogli.
>
> Fai cinque giri. Ogni volta ferma la mano, misura col righello **quanto distano due bande chiare**, e scrivi qui:
>
> ```
>  giro  fra due bande  angolo che ne viene
>  1        ......  mm        ......  gradi
>  2        ......  mm        ......  gradi
>  3        ......  mm        ......  gradi
>  4        ......  mm        ......  gradi
>  5        ......  mm        ......  gradi
> ```
>
> **L'angolo si ricava dalla distanza**, e la regola è una divisione: l'angolo in gradi è circa **58 diviso la distanza fra le bande in millimetri**. Il 58 dipende dal passo delle righe: con righe larghe il doppio sarebbe 116.
>
> Poi prova a misurare l'angolo direttamente, con un goniometro, e confronta i due numeri. **Quale dei due modi ti fidi di più? E perché, secondo te, chi misura le deformazioni dei materiali usa il primo?**

Con righe a 1,016 mm — ventiquattro punti di stampante — le bande stanno così:

```
 se le giri di  le bande stanno a
 0,5 gradi                 116 mm
 1 grado                    58 mm
 2 gradi                    29 mm
 3 gradi                    19 mm
 5 gradi                    12 mm
 10 gradi                    6 mm
```

La consegna è girata al contrario: non si chiede di guardare il moiré, si chiede di **misurare** una cosa che non si può misurare direttamente e di verificarla con uno strumento. È lo stesso uso industriale, ridotto a un righello, e la risposta è controllabile perché il goniometro c'è.

Il foglio costa quanto due fogli e non richiede nessuna precisione di registro: spostando i fogli le bande si spostano, ma non spariscono. Questa è la differenza tecnica più netta fra questa voce e la voce 390, immagine da comporre in controluce, e vale la pena averla misurata: qui l'allineamento non conta, là decide tutto.

Il limite dichiarato: due fogli di carta comune tenuti contro una finestra lasciano passare poca luce e le righe del foglio di dietro si vedono male. Su lucido o su carta velina funziona meglio, e quanto meglio non è stato misurato.

## Da riprendere alla rassegna

**È un ingranditore che si stampa, e il suo fattore si sceglie.** Nessun'altra forma dell'enciclopedia rende visibile una grandezza che sta sotto la soglia della vista senza uno strumento comprato. Alla rassegna sta accanto alla voce 63, inferire da un'assenza e alla voce 52, osservare, e si distingue da tutte e due perché lo strumento è un foglio.

**Il limite di stampa è stato misurato invece che dichiarato, e ha due valori.** Il moiré di passo è legato alla risoluzione della stampante e all'altezza della carta, e si ferma a un ingrandimento di 83 volte; il moiré di rotazione non è legato a niente e a un decimo di grado ingrandisce 573 volte. **Prima di dire che una forma visiva dipende dalla precisione di stampa, va guardato quale delle sue varianti ci dipenda.**

**Una consegna girata al contrario che non toglie niente alla forma.** Alla voce 383, pareidolia girare la domanda spostava la sorpresa dallo sguardo al numero; qui misurare le bande per ricavare l'angolo è quello che fa chi usa la cosa per mestiere, e il fenomeno resta intero perché per misurare bisogna prima vederlo. Alla rassegna: la mossa costa niente quando la forma è già uno strumento di misura.

**La riga di differenza.** Alla voce 385, cecità al cambiamento il foglio contiene sei differenze e l'occhio non ne prende nessuna; qui nessuno dei due fogli contiene niente e l'occhio ne prende una, ingrandita ventiquattro volte. È il valore opposto sulla grandezza del blocco, e obbliga a dire di quale foglio si parli: la lettura non sta su nessuno dei due, sta nella coppia.

