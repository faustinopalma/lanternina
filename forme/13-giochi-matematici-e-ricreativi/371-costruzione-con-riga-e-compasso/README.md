# Costruzione con riga e compasso

- **Numero** 371 nell'enciclopedia, capitolo 13 — Giochi matematici e ricreativi
- **Si chiama anche** costruzione euclidea, geometria con riga e compasso, disegno geometrico, i tre problemi classici, *straightedge and compass construction*, *ruler and compass*, *classical construction*
- **In una riga** e le costruzioni impossibili, che sono la parte interessante.
- **Contratto** voce breve
- **Fonti** `straightedge-and-compass.txt`, `constructible-polygon.txt`, `constructible-number.txt`, `doubling-the-cube.txt`, `angle-trisection.txt`, `squaring-the-circle.txt`, `neusis-construction.txt`, `drawing-compass.txt`, `it-riga-e-compasso.txt`, `it-duplicazione-del-cubo.txt`, `mathematics-of-paper-folding.txt`, lette il 2 settembre 2026
- **Stato della ricerca** fatta, 2 settembre 2026

## Che cos'è

Due strumenti e cinque mosse. La riga non ha tacche e serve solo a tirare un tratto fra due punti o a prolungarne uno; il compasso ha apertura qualunque e serve solo a disegnare un cerchio dati il centro e un punto. Le cinque mosse, in `straightedge-and-compass.txt`: la retta per due punti, il cerchio di centro un punto e passante per un altro, e i punti nuovi che nascono dall'incrocio di due rette, di una retta e un cerchio, di due cerchi.

Le parti mobili:

- **Che cosa si consegna.** Una figura da ottenere — l'esagono, la bisettrice, il pentagono — oppure la domanda se si possa ottenere. La seconda è la parte che ha tenuto occupata la matematica per due millenni.
- **Quali strumenti si concedono.** Tolto o aggiunto un attrezzo, cambia l'insieme delle cose costruibili, e cambia in modo misurabile.
- **Se si accetta un'approssimazione.** «Vicino quanto basta» e «esatto» sono due compiti diversi, e sul foglio si somigliano.
- **Se la costruzione deve finire.** Un numero finito di passi, non il limite di una successione di tentativi sempre più fini.

**La regola che conta è quella che spiega tutte le altre**, e `straightedge-and-compass.txt` la scrive per esteso: ogni costruzione deve essere esatta, non è permesso andare a occhio né usare tacche sul righello, e ogni costruzione deve terminare. Il motivo dichiarato è uno solo: **quei divieti esistono perché si possa dimostrare che la costruzione è esattamente corretta.** La forma è nata per mettere la prova dentro lo strumento.

**Questa è la voce del blocco in cui la scala del blocco si vede tutta intera.** Dove stia la prova che si è finito, qui, prende tre valori sullo stesso foglio: **nello strumento** quando la costruzione riesce — il compasso torna al primo segno e la figura è chiusa —; **in un argomento di algebra** quando la costruzione è impossibile, e quell'argomento è del 1837 e del 1882 e non lo rifà nessuno nella stanza; **da nessuna parte** quando la costruzione è approssimata, perché la figura sbagliata sembra chiusa esattamente come quella giusta. Le altre sei voci del blocco si descrivono per differenza da questa, e la riga di differenza sta in fondo a ognuna.

## Da dove viene

**I greci sapevano fare parecchio e sapevano di non saper fare tre cose.** `straightedge-and-compass.txt`: costruivano somme, differenze, prodotti, rapporti e radici quadrate di lunghezze date, la metà di un angolo, il quadrato di area doppia, il quadrato equivalente a un poligono, e i poligoni regolari di 3, 4 e 5 lati, con il raddoppio dei lati a piacere. Non riuscivano a trisecare un angolo qualunque, a quadrare il cerchio, a duplicare il cubo, né a fare i poligoni regolari con altri numeri di lati. **Credevano che quei problemi fossero ostinati, non impossibili.**

**La duplicazione del cubo arriva con tre racconti d'origine diversi, e le fonti non ne scelgono uno.** `doubling-the-cube.txt` e `it-duplicazione-del-cubo.txt`: in una versione gli abitanti di Delo consultano l'oracolo di Delfi per fermare una peste e si sentono ordinare di raddoppiare l'altare cubico di Apollo; in un'altra, che Plutarco riporta, andarono all'oracolo per le loro liti interne e la risposta fu che dovevano occuparsi di geometria invece che di guerre. La terza è più antica di tutte e sta in una lettera di Eratostene a Tolomeo III, citata settecento anni dopo da Eutocio: un poeta tragico fa dire a Minosse, davanti al sepolcro cubico di Glauco, che è piccolo per un re e che va raddoppiato. **Tre racconti per lo stesso problema, e nessuna delle due pagine prova a decidere.** Archita di Taranto lo risolse con una costruzione tridimensionale; Eratostene con uno strumento, il mesolabio. Platone, secondo Plutarco, rimproverò chi lo risolveva con mezzi meccanici.

**Le tre impossibilità hanno due date, non tre.** Il **1837** è di Pierre Wantzel, e non è un articolo per problema: è **un articolo solo**, sei pagine del *Journal de Mathématiques Pures et Appliquées*, che chiude la duplicazione del cubo, la trisezione dell'angolo **e** la questione dei poligoni regolari, mostrando che le lunghezze costruibili sono radici di polinomi di grado una potenza di due. `constructible-number.txt` lo riassume in una frase — «nello stesso articolo risolse anche il problema di determinare quali poligoni regolari siano costruibili» — e aggiunge la formulazione moderna: i numeri costruibili formano un campo, che è la chiusura euclidea dei razionali. Il **1882** è di Ferdinand von Lindemann, e chiude la quadratura del cerchio dimostrando che π è trascendente, cioè che non è radice di nessun polinomio a coefficienti razionali. Fra la prima domanda e l'ultima risposta stanno più di venti secoli.

**In mezzo c'è Gauss, che fa il contrario di una dimostrazione d'impossibilità.** Nel **1796** costruisce il poligono regolare di **17 lati**, che nessuno aveva mai costruito; cinque anni dopo, nelle *Disquisitiones Arithmeticae*, enuncia la condizione sufficiente perché un poligono di *n* lati sia costruibile. Dichiara senza dimostrarla che è anche necessaria, e non pubblica mai la prova: quella la dà Wantzel nel 1837 (`constructible-polygon.txt`).

## Varianti e parenti

- **Solo compasso** — il teorema di Mohr–Mascheroni: tutto quello che si costruisce con riga e compasso si costruisce col solo compasso, purché i dati e i risultati siano punti.
- **Solo riga** — non basta: con la sola riga non si estrae una radice quadrata né si trova il punto medio di un segmento. Il teorema di Poncelet–Steiner dice che basta aggiungere **un** cerchio già disegnato con il suo centro.
- **Riga con due tacche** — la costruzione per *neusis*, che `neusis-construction.txt` fa risalire ad Archimede e a Pappo: si triseca l'angolo e si duplica il cubo. Newton la usò e la difese; l'Ottocento la cacciò dai libri.
- **Piegatura della carta** — gli assiomi di Huzita–Hatori. Vedi sotto: costruiscono esattamente quello che riga, compasso e un tracciatore di coniche costruiscono insieme.
- **Costruzione approssimata** — si accetta un errore e si guadagna semplicità. È una famiglia intera, non un ripiego.
- **Voce 152, problema impossibile** — la forma di pagina: un compito che si scopre impossibile provandolo. Quella scheda rimanda qui per le tre impossibilità classiche, e il rimando regge; una cosa che dice va precisata, ed è nella sezione seguente.
- **Voce 162, puzzle di piegatura** — rimanda qui e dichiara che la piegatura risolve due dei tre problemi classici e non il terzo. Ricontrollato contro le fonti nuove: **regge alla lettera**.
- **Voce 42, piegatura** — la carta come supporto, senza la domanda geometrica.
- **Voce 46, modello in scala** — l'altra forma in cui una figura si controlla misurandola.
- **Voce 377, problema di ottimizzazione con vincoli fisici** — l'altra voce del blocco in cui la prova sta in uno strumento, e lo strumento è uno spago.

## Che cosa se ne sa

**Il criterio di Gauss–Wantzel, rifatto invece che citato.** Un poligono regolare di *n* lati si costruisce se e solo se *n* è il prodotto di una potenza di due per primi di Fermat **distinti**; i primi di Fermat noti sono cinque — 3, 5, 17, 257, 65 537 — e per questo i poligoni costruibili con un numero dispari di lati **noti** sono 2⁵ − 1 = 31. `build/check_371.py` ricalcola l'elenco dal criterio e lo confronta con la successione A003401 stampata dentro `constructible-polygon.txt`, letta dal file e non ricopiata: **65 termini, identici.** Un secondo metodo, che moltiplica ogni sottoinsieme dei cinque primi per ogni potenza di due invece di applicare il criterio a ogni numero, dà lo stesso insieme.

**Fra i primi cento poligoni se ne costruiscono meno di un quarto.** Da 3 a 100 ci sono 98 candidati e 24 costruibili: 3, 4, 5, 6, 8, 10, 12, 15, 16, 17, 20, 24, 30, 32, 34, 40, 48, 51, 60, 64, 68, 80, 85, 96. Sotto il 21 i sette che non si fanno sono 7, 9, 11, 13, 14, 18 e 19. **L'ettagono è il primo, e sta al settimo posto**: la forma che non si può fare è la seconda che verrebbe in mente a chiunque dopo l'esagono.

**Il numero di poligoni costruibili non si sa, e il motivo è che non si sa quanti siano i primi di Fermat.** `constructible-polygon.txt` dice che i successivi ventotto numeri di Fermat, da F₅ a F₃₂, sono tutti composti, e che se i primi di Fermat fossero *q* i poligoni dispari costruibili sarebbero 2^*q* − 1. **La domanda è aperta da Gauss e riguarda un oggetto che si disegna con un compasso.**

**Un'approssimazione può sbagliare alla quinta cifra e restare invisibile sul foglio, e i due numeri stanno insieme.** La costruzione di Adam Adamandy Kochański, gesuita polacco, **1685**: `squaring-the-circle.txt` dà il valore ottenuto come √(40/3 − 2√3). `build/check_371.py` lo calcola: **3,141533339** contro π = 3,141592654, cioè sbaglia dalla **quinta** cifra decimale. Su un cerchio di raggio 10 centimetri il lato del quadrato equivalente sbaglia di **0,0017 mm**, che è meno di un decimo dello spessore di una riga di matita. **La figura sbagliata e quella giusta si sovrappongono.**

**Lo stesso vale per l'ettagono che si fa nelle botteghe, e il buco si può misurare.** La costruzione approssimata usa come lato la metà del lato del triangolo equilatero inscritto, cioè √3/2 raggi, contro il valore vero 2 sen(π/7) = 0,867767 raggi. `build/check_371.py`: dopo sette passi di compasso su un cerchio di raggio 10 cm resta un buco di **1,35 mm** su un giro di 628 mm, cioè lo **0,215%** del cerchio. Un buco di un millimetro e mezzo si chiude spostando l'ultimo segno, e nessuno se ne accorge.

**Da qui viene la precisazione alla voce 152, problema impossibile.** Quella scheda dice che la quadratura del cerchio è «la più antica e la più lenta»: la duplicazione del cubo ha almeno un racconto d'origine più antico, e le fonti lette adesso non permettono di ordinarle per età. Il resto della sua riga — che le ultime due si risolvono con strumenti più potenti e la prima no — è confermato parola per parola da `mathematics-of-paper-folding.txt` e da `angle-trisection.txt`.

**La piegatura è più potente del compasso, e adesso si può dire di quanto.** `straightedge-and-compass.txt`: le pieghe che soddisfano gli assiomi di Huzita–Hatori costruiscono **esattamente** lo stesso insieme di punti che si costruisce con riga, compasso e uno strumento capace di tracciare coniche. Quindi risolvono le equazioni di terzo e quarto grado, e con esse la duplicazione del cubo e la trisezione. La quadratura del cerchio resta fuori anche per loro, perché π non è radice di nessuna equazione. `mathematics-of-paper-folding.txt` aggiunge il criterio parallelo a quello di Gauss: si piega un poligono regolare di *n* lati se e solo se *n* è prodotto di primi di **Pierpont** distinti, potenze di due e potenze di tre.

**La pagina italiana è corretta e si dichiara da sé incompleta.** `it-riga-e-compasso.txt` porta in cima l'avviso che non cita le fonti necessarie; definisce la costruzione come l'ottenere graficamente una figura con i due soli strumenti, e non aggiunge nessuna misura a quello che dicono le pagine inglesi. È stata letta e serve solo a confermare la definizione.

**Il problema attira ancora, e la storia lo registra.** `squaring-the-circle.txt`: Thomas Hobbes si convinse da vecchio di aver quadrato il cerchio; Charles Dodgson, che è Lewis Carroll, scambiò più di venti lettere con un quadratore convinto che π valesse 3,2, e scrisse di essersi tristemente persuaso di non avere nessuna possibilità di convincerlo dell'errore. Nel **1894** Edwin Goodwin propose all'assemblea dell'Indiana una legge che permettesse allo Stato di usare il suo metodo gratis: passò alla camera senza obiezioni e si arenò al senato fra le risate della stampa. Il suo metodo poneva π uguale a 3,2, lo stesso numero del corrispondente di Dodgson.

## Esempi trovati

Dal 1796: il diciassettagono di Gauss, che a diciannove anni decise per questo di fare il matematico invece che il filologo.

Da Archimede, in `angle-trisection.txt`: la trisezione con la spirale, in *Sulle spirali*, intorno al 225 a.C. Funziona, e non è ammessa.

Da Archita, in `it-duplicazione-del-cubo.txt`: la duplicazione del cubo ottenuta incrociando tre superfici nello spazio. È la prima soluzione conosciuta, e non usa né riga né compasso.

Da Eratostene: il mesolabio, uno strumento costruito apposta per inserire due medie proporzionali fra due segmenti. La risposta a un problema di geometria è un oggetto di legno.

Dalle botteghe, in `drawing-compass.txt`: il compasso a punte fisse per riportare una distanza, il compasso ad asta per i cerchi grandi, il compasso di riduzione per ingrandire un disegno conservando gli angoli. Lo strumento della dimostrazione è anche un attrezzo da lavoro.

## Una nostra versione

> **Il compasso sa contare fino a sei**
>
> Traccia un cerchio e **non toccare più l'apertura del compasso**. Punta su un punto qualunque del bordo e fai un segno; punta sul segno e fanne un altro; vai avanti.
>
> Torni sul primo segno? Dopo quanti passi? Unisci i segni e guarda che cosa è venuto.
>
> Adesso prova a fare la stessa cosa con **sette** segni, a occhio, aggiustando l'apertura finché non ti torna.
>
> Ti tornerà. Il buco che ti resta l'ultima volta è più piccolo di due millimetri, e lo chiudi spostando l'ultimo segno di niente. **Il tuo ettagono è sbagliato, e non c'è modo di vederlo.**
>
> Con la riga e il compasso, e senza barare, questi si fanno e questi no:
>
> ```
>  lati  si fa?  lati  si fa?
>     3  si'       12  si'
>     4  si'       13  no
>     5  si'       14  no
>     6  si'       15  si'
>     7  no        16  si'
>     8  si'       17  si'
>     9  no        18  no
>    10  si'       19  no
>    11  no        20  si'
> ```
>
> Guarda la colonna dei sì e prova a indovinare la regola. È stata trovata nel 1796 da un ragazzo di diciannove anni, e ci sono voluti altri quarantuno anni per dimostrare che non ne esiste una migliore.

L'esagono si verifica da solo: il compasso torna al primo segno e la figura è chiusa. L'ettagono no, e questa è la parte da consegnare — non «non ci riesci», ma «ci riesci e sbagli lo stesso». La tabella è generata dal criterio in `build/blocco_371.py`, non scritta a mano, e la regola che si chiede di indovinare non è indovinabile: serve a far guardare i numeri, e la risposta sta sotto.

## Da riprendere alla rassegna

**È il termine di paragone del blocco 371-377, e lo è per la stessa ragione della voce 366, problema di grafi**: non perché stia a un estremo della scala, ma perché la contiene tutta. Sullo stesso foglio, la prova che si è finito sta nello strumento (l'esagono che chiude), in un argomento che nessuno rifà (Wantzel 1837, Lindemann 1882) e da nessuna parte (l'ettagono approssimato che chiude lo stesso). **Le altre sei voci si collocano rispetto a questi tre valori.**

**Lo strumento che dimostra può mentire, e questa voce è dove lo si vede meglio.** Le regole della costruzione classica esistono perché la figura sia una prova; e le due costruzioni approssimate che questa voce misura — 0,0017 mm per Kochański, 1,35 mm per l'ettagono — producono figure che sono indistinguibili da una prova. Alla rassegna: **ogni volta che la verifica sta dentro il materiale, va chiesto quanto vale l'errore che il materiale non mostra.**

**Il compasso è lo strumento più economico raccolto in tutta l'enciclopedia per una verifica esatta.** Non richiede una risposta scritta, non richiede una persona, non misura niente in unità: due punti coincidono o no. Con la sovrapposizione della voce 162, puzzle di piegatura fa due, e sono le due verifiche binarie e immediate del progetto.

**Una figura si può chiedere anche a chi non legge volentieri.** Il compito è una riga e mezzo, l'attrezzo costa poco, e quello che ne esce è un teorema. Con la voce 365, principio dei cassetti e la voce 369, dimostrazione senza parole fa tre, ed è la terza soglia d'ingresso bassa del capitolo 13.

**Il vincolo di `ideas/10 §8` non morde qui**: la costruzione si compone al contrario — si sceglie il poligono, si stampa la tabella, si sa che cosa deve venire —, e quello che chi riceve produce non deve tornare indietro come testo da leggere. La stessa cosa vale per cinque delle sette voci del blocco.

