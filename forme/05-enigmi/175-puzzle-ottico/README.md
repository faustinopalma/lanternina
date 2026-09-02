# Puzzle ottico

- **Numero** 175 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi fisici e meccanici»
- **Si chiama anche** camera oscura, foro stenopeico, caleidoscopio, fantasma di Pepper, catottrica, giochi di specchi, giochi d'ombra, ombre cinesi
- **In una riga** specchi, lenti, ombre.
- **Fonti** `camera-obscura.txt`, `kaleidoscope.txt`, `peppers-ghost.txt`, `shadow-play.txt`, lette il 31 agosto 2026; `optical-illusion.txt` e `impossible-object.txt` scorse lo stesso giorno e lasciate al capitolo 14, che è di quello che parlano. I conti dell'esempio sono nostri, in `build/check_175.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Un apparecchio ottico usato come meccanismo di un enigma. Non è l'occhio che sbaglia: è la luce che fa qualcosa di reale, e il compito è capire che cosa.

**Questo confine è il punto della voce e va scritto subito.** Nel capitolo 14 ci saranno le illusioni: la voce 378, illusione ottica geometrica, la voce 382, anamorfosi, la voce 389, moiré, la voce 394, prospettiva forzata. Lì il fenomeno è il contenuto, e il fatto interessante è che l'occhio si inganni. **Qui l'occhio non si inganna affatto**: uno specchio riflette davvero, un foro proietta davvero un'immagine, un'ombra ha davvero quella forma, e chi guarda deve scoprire perché. La differenza pratica è che un'illusione resta illusione anche dopo che è stata spiegata, mentre un enigma ottico, spiegato, diventa una macchina che si può costruire.

Dentro il capitolo 5 il confine è già stato tracciato tre volte, e vale qui per intero: alla voce 137, specchio uno specchio decifra un testo, alla voce 138, testo capovolto o ruotato si gira la pagina, alla voce 140, sovrapposizione di due fogli se ne mettono due in controluce. **Quelle tre sono operazioni su una pagina scritta.** Questa voce è quello che resta quando non c'è nessuna scrittura da decifrare.

Parti mobili:

- **Che cosa fa il lavoro.** Un foro (proietta), uno specchio (riflette e moltiplica), una lente o una goccia (ingrandisce), un'ombra (semplifica una forma in un contorno).
- **Se l'apparecchio si vede.** Nel fantasma di Pepper il vetro deve essere invisibile, altrimenti l'effetto non c'è. Nella camera oscura il foro si vede benissimo e non toglie niente.
- **Che cosa si chiede.** Prevedere che cosa apparirà, spiegare perché è così, oppure costruire l'apparecchio che produce un effetto dato.
- **Se il fenomeno è a disposizione.** Un'ombra richiede il sole o una lampada, un foro stenopeico richiede una fonte piccola e luminosa. **Alcune parti di questa famiglia dipendono dal tempo che fa**, e nessun'altra forma dell'elenco ha questo vincolo.

## Da dove viene

La camera oscura è documentata da due parti del mondo e da molto lontano. Il testo cinese **Mozi**, quarto secolo a.C., contiene quella che `camera-obscura.txt` dà per la prima descrizione scritta di un'immagine da foro, **e la spiegazione è già quella giusta**: la luce che viene dai piedi di una persona illuminata colpisce sotto il foro e forma la parte alta dell'immagine, quella che viene dalla testa colpisce sopra e forma la parte bassa. Ventiquattro secoli fa, e non c'è niente da correggere.

Sul versante greco la cosa compare come **una domanda senza risposta**, ed è la parte più utile di tutta la voce. Nei *Problemi*, libro XV, attribuiti ad Aristotele o a un suo seguace, si chiede: perché quando il sole passa attraverso aperture quadrate, per esempio in un graticcio di vimini, non produce una figura rettangolare ma circolare? E poco oltre: perché durante un'eclissi di sole, guardando attraverso un setaccio o attraverso le foglie di un platano, o incrociando le dita di una mano su quelle dell'altra, i raggi arrivano a terra a forma di mezzaluna? L'autore prova a spiegarlo con due coni di luce e sbaglia. **La fonte scrive che filosofi e scienziati dell'Occidente rimuginarono su questa contraddizione — la luce va dritta, eppure i buchi quadrati fanno macchie tonde — finché non fu generalmente accettato che quelle macchie erano immagini del sole.**

Le altre date: gnomoni forati che proiettano l'immagine del sole sono descritti nello *Zhoubi Suanjing* cinese, e la posizione del cerchio luminoso dice l'ora del giorno e il periodo dell'anno; nelle culture mediorientali ed europee l'invenzione fu attribuita molto più tardi all'astronomo egiziano Ibn Yunus, intorno al **1000 d.C.** Euclide, nell'*Ottica* di circa il **300 a.C.**, descrive la visione come un cono con il vertice nell'occhio.

La pagina riporta anche una teoria e la marca come tale, e vale la pena tenerla nella sua forma cauta: **ci sono teorie** secondo cui effetti da camera oscura, attraverso fori minuscoli nelle tende o negli schermi di pelle, avrebbero ispirato le pitture rupestri paleolitiche, e le deformazioni degli animali in molte di quelle pitture verrebbero dalle distorsioni che si vedono quando la superficie di proiezione non è dritta.

Il caleidoscopio è recente e ha una data precisa: **David Brewster**, brevetto britannico numero 4136, concesso il **10 luglio 1817**. Il nome è suo e viene dal greco *kalós*, *eîdos*, *skopéō* — osservazione di forme belle. La riflessione multipla fra due specchi era però nota da molto prima: Giambattista della Porta la descrive nella *Magia Naturalis* (1558-1589), e nel **1646 Athanasius Kircher** costruisce due specchi che si aprono e si chiudono come un libro e si mettono ad angoli diversi, mostrando poligoni regolari fatti di settori riflessi di 360 gradi. **Quella è già la regola che l'esempio qui sotto fa scoprire**, ed era in un libro trecentosettant'anni fa.

Il fantasma di Pepper prende il nome da **John Henry Pepper**, che rese celebre l'effetto la vigilia di Natale del **1862** al teatro di Regent Street, a Londra, in una riduzione di un racconto di Dickens. Il successo fu immediato, lo spettacolo si spostò in un teatro più grande e andò in scena per tutto il **1863**; il principe di Galles ci portò la moglie appena sposata. Il brevetto è del 1863, in comune con Henry Dircks.

## Varianti e parenti

- **Camera oscura** — una scatola, una tenda o una stanza con un foro piccolo su un lato. L'immagine arriva **capovolta e rovesciata da destra a sinistra**, con i colori e la prospettiva intatti.
- **Gnomone forato** — la stessa cosa puntata sul sole, per leggere l'ora e la stagione dalla posizione della macchia.
- **Caleidoscopio** — due o più superfici riflettenti a un angolo, e un oggetto che si moltiplica in una figura simmetrica.
- **Fantasma di Pepper** — un vetro inclinato a 45 gradi che riflette una stanza nascosta e ben illuminata; il pubblico non vede il vetro e vede una figura in mezzo alla scena. Si accende e si spegne cambiando le luci, non spostando niente.
- **Ombre cinesi e teatro d'ombre** — una figura ritagliata fra una lampada e un telo; quello che si vede è solo il contorno, e questa perdita di informazione è la forma.
- **Goccia d'acqua come lente** — una goccia su una superficie trasparente ingrandisce quello che ha sotto. È la lente più economica che esista, e **quanto ingrandisca in pratica va verificato.**
- **Voce 137, specchio** — lo specchio come decifratore di un testo. Confine dichiarato sopra.
- **Voce 138, testo capovolto o ruotato** e **voce 140, sovrapposizione di due fogli** — le altre due operazioni fisiche su una pagina già raccolte in questo capitolo.
- **Voce 382, anamorfosi** — l'immagine che si compone solo da un punto o in uno specchio. È del capitolo 14 e non viene presa qui.
- **Voce 389, moiré** e **voce 390, immagine da comporre in controluce** — due trame sovrapposte e due fogli in controluce; sono tutte e due del capitolo 14, e nessuna delle due è questa.
- **Voce 393, sezione e proiezione** — dato un solido, che ombra fa. È il contenuto geometrico dell'ombra, e sta nel capitolo 14.
- **Voce 54, misurare** — la misura indiretta, che quella voce aveva indicato come il filone più bello e meno praticato. L'esempio qui sotto è un caso di misura indiretta.
- **Voce 65, provare** — prevedere prima di guardare, che è la struttura dell'esempio.

## Che cosa se ne sa

**Il foro ha una misura giusta, e la fonte dà due criteri.** Per un'immagine ragionevolmente nitida l'apertura è tipicamente **più piccola di un centesimo della distanza dallo schermo**. Restringendo il foro l'immagine si fa più nitida e più debole; sotto una certa misura la nitidezza si perde di nuovo per diffrazione. L'ottimo, dice `camera-obscura.txt`, si ha con un diametro **circa uguale alla media geometrica fra la lunghezza d'onda della luce e la distanza dallo schermo**: con luce a 550 nanometri e uno schermo a 30 centimetri sono 0,41 millimetri, cioè un foro di spillo. **È l'unico caso in questo capitolo in cui il parametro di un'attività ha una formula.**

**L'immagine è capovolta perché la luce va dritta, e questo è stato scritto prima che qualcuno avesse una teoria della luce.** La spiegazione del Mozi è un ragionamento geometrico su due raggi, e sta in due righe. Vale la pena notarlo: **il fenomeno più antico di questa famiglia si spiega con l'unica cosa che tutti sanno già**, cioè che la luce non gira gli angoli.

**L'occhio funziona così, e la fonte mette una nota che conviene riportare.** L'analogia fra occhio e camera oscura compare all'inizio del Cinquecento e nel Seicento serve a illustrare l'idea teologica di un universo costruito come una macchina; ha avuto un'influenza enorme sullo studio della percezione. Ma `camera-obscura.txt` aggiunge che **la proiezione di immagini capovolte è un principio fisico dell'ottica che precede la comparsa della vita, e non è una caratteristica di tutta la visione biologica.** È una fonte che si smarca dalla propria analogia, e non capita spesso.

**Il caleidoscopio si diffuse più in fretta di quanto potesse essere costruito bene, e i numeri sono impressionanti.** In tre mesi se ne vendettero circa **duecentomila** fra Londra e Parigi; Brewster calcolò che al massimo **mille** fossero copie autorizzate e costruite correttamente, e che la maggior parte delle altre non desse l'impressione giusta dell'invenzione. Siccome pochissimi avevano visto un caleidoscopio vero, pubblicò un trattato sui principi e sulla costruzione corretta. **È il primo caso raccolto in questa enciclopedia di una forma diventata popolarissima nella sua versione rotta**, e riguarda chiunque debba diffondere delle istruzioni.

**Chi sta dentro l'illusione non la vede.** Nel fantasma di Pepper gli attori sul palco non possono vedere dove appare la figura riflessa, perché non stanno nel punto giusto; Pepper metteva **segni nascosti sul pavimento** per dire loro dove appoggiare i piedi. È la formulazione più netta incontrata del problema che riguarda chiunque prepari qualcosa per un altro: **l'effetto esiste in un posto solo, e chi lo costruisce di solito non è in quel posto.**

**Il fantasma di Pepper si vende oggi con il nome sbagliato.** La fonte scrive che quando la tecnica viene usata per far comparire sul palco artisti morti — Tupac Shakur, Michael Jackson — **è spesso descritta erroneamente come «olografica»**, e che ne esistono versioni domestiche con una piramide di plastica trasparente e lo schermo di un telefono. Un effetto del 1862 venduto come tecnologia nuova.

**Sulle attività di questo genere non c'è nessuna misura in nessuna delle pagine lette.** Non si sa quanto sia difficile prevedere che l'immagine sarà capovolta, né che cosa resti dopo. Le fonti descrivono apparecchi, non esperienze, e la differenza va dichiarata.

## Esempi trovati

Il graticcio di vimini di Aristotele: buchi quadrati, macchie di luce tonde, e nessuno che sappia spiegarlo per duemila anni.

Le mezzelune sotto un platano durante un'eclissi parziale, che ogni foglia proietta senza essere un apparecchio.

Lo gnomone forato cinese, che è un orologio e un calendario fatti con un buco.

La stanza-camera oscura del Settecento, con lo specchio inclinato in cima alla tenda per raddrizzare l'immagine e la carta da lucido sul tavolo per ricalcarla.

I due specchi di Kircher, 1646, che si aprono come un libro e mostrano poligoni regolari a seconda dell'angolo.

Il fantasma di Pepper del Natale 1862, e il trucco della ragazza che diventa gorilla dei baracconi, che è lo stesso apparecchio con due stanze nascoste.

La piramide di plastica trasparente sopra lo schermo di un telefono, venduta come ologramma.

## Una nostra versione

> **Perché il sole fa macchie tonde**
>
> **Non guardare mai il sole, nemmeno per un istante e nemmeno attraverso il buco.** Qui si guarda soltanto la macchia di luce che cade per terra.
>
> Ti serve: **un giorno di sole**, un cartoncino, uno spillo o la punta di una forbice, e un foglio bianco da appoggiare per terra.
>
> **Fai nel cartoncino quattro buchi diversi**, larghi più o meno come questi:
>
> ```
>       ●            ■            ▲          ✚
>     tondo       quadrato    triangolo    croce
>    ~4 mm        ~4 mm        ~4 mm       ~4 mm
> ```
>
> **Uno.** Tieni il cartoncino con i buchi verso il sole e il foglio bianco poco sotto, a **dieci centimetri**. Guarda le quattro macchie. Poi allontana il foglio, piano: venti centimetri, mezzo metro, un metro, due metri.
>
> ```
>   a 10 cm le macchie sono:  ────────────────────────────────
>   a 50 cm sono:             ────────────────────────────────
>   a 2 m sono:               ────────────────────────────────
>
>   A che distanza il quadrato ha smesso di essere quadrato?  ────────
> ```
>
> Sono tutte tonde, da lontano. Il buco quadrato fa una macchia tonda, e quello a croce pure.
>
> **Due, ed è la domanda vera.** Questa cosa la chiese Aristotele, o qualcuno della sua scuola, nel quarto secolo prima di Cristo, guardando la luce che passava fra i vimini di un cesto. Ci vollero circa duemila anni perché la risposta fosse accettata. Scrivi la tua:
>
> ```
>   Perché il buco quadrato fa una macchia tonda?
>   ───────────────────────────────────────────────────────────────────
>   ───────────────────────────────────────────────────────────────────
> ```
>
> **Tre. Adesso misura il sole.** Prendi il buco tondo e misura con un righello quanto è larga la macchia a **cinquanta centimetri** e quanto è larga a **due metri**.
>
> ```
>   larghezza a 50 cm  ──────── mm
>   larghezza a 200 cm ──────── mm
>
>   differenza fra le due  ──────── mm
>   diviso 1500 (i millimetri fra le due distanze)  ────────
>
>   moltiplicato per 150 000 000 (i chilometri che ci separano dal sole)
>
>   il sole è largo circa ──────────── chilometri
> ```
>
> Il numero vero è **1 392 700 chilometri**. Di quanto ti sei scostato?
>
> Un'ultima cosa da notare, ed è la ragione per cui si misura due volte invece che una: **la larghezza del buco non compare nel conto.** Sparisce da sola quando fai la differenza. Puoi rifarlo con il buco a croce e viene lo stesso numero.

Il primo compito è l'enigma di Aristotele riprodotto con un cartoncino, e ha una verifica che non passa da nessuno: **le macchie sono tonde o non lo sono, e si vedono.** Il secondo chiede la spiegazione, e non c'è nessuna risposta stampata sul foglio — non per pudore, ma perché la risposta la può controllare chi la dà: se hai capito che ogni punto del buco proietta un'immagine del sole e che le immagini si sovrappongono, sai già prevedere che cosa succede allargando il buco, e puoi provarlo.

Il terzo compito è una misura indiretta, e il numero finale si confronta con uno vero. I conti sono in `build/check_175.py`: con il diametro angolare del sole di 0,00930 radianti, la macchia larga *b* millimetri a distanza *d* vale **b = foro + d × 0,00930**, quindi la crescita fra cinquanta centimetri e due metri è di **13,9 millimetri** qualunque sia il buco, e il diametro che se ne ricava è **1 391 280 chilometri**, cioè lo **0,10%** sotto il valore vero. Chi misura con un righello sbaglierà di più, ed è per questo che il foglio chiede di quanto ci si è scostati invece di chiedere se è giusto.

La parte che fa il lavoro è **la sottrazione**. Misurare una volta sola non basterebbe, perché la macchia contiene il buco e nessuno sa quanto è largo il buco che ha fatto con lo spillo; misurando due volte e sottraendo, la larghezza del buco se ne va da sola. È la stessa mossa della voce 54, misurare — due misure della stessa cosa — usata qui non per mostrare l'errore ma **per eliminare un'incognita**, e non era ancora comparsa.

Dove si romperebbe: serve il sole, e questo è un vincolo che nessun'altra forma dell'elenco ha. Con una lampada non funziona, perché una lampadina non è abbastanza lontana e la sua immagine non è tonda. **Il foglio va stampato sapendo che potrebbe restare sul tavolo per una settimana**, e conviene che lo dica. Il ritorno possibile è una fotografia del foglio bianco con le quattro macchie, che si legge benissimo, più i numeri scritti a mano.

## Da riprendere alla rassegna

**Un enigma che è rimasto aperto duemila anni e che si riapre con un cartoncino.** La domanda di Aristotele sui vimini è più bella di qualunque indovinello costruito apposta, costa un buco e un giorno di sole, e ha il pregio che nessuno la trova banale. **Da cercare sistematicamente: quali altre domande antiche restino riproducibili con niente**, perché sono le uniche il cui interesse non dipende da chi le pone.

**Sottrarre due misure per far sparire un'incognita.** Non è la stessa cosa che misurare due volte per vedere l'errore. Qui la seconda misura serve a togliere di mezzo una quantità che non si conosce e non si vuole conoscere, e rende esatto un esperimento fatto con uno spillo. **Da provare su ogni attività di misura che dipenda da un attrezzo fatto in casa.**

**Una forma può diffondersi nella sua versione rotta.** Duecentomila caleidoscopi in tre mesi, al massimo mille costruiti bene, e l'inventore costretto a pubblicare un trattato su come si fa. Per un progetto che stampa istruzioni è la cosa più utile della voce: **la parte difficile non è inventare l'oggetto, è che chi lo costruisce ottenga quello che deve ottenere.**

**Chi costruisce un effetto non sta nel posto da cui si vede.** Gli attori di Pepper avevano segni sul pavimento perché il fantasma non lo vedevano. Vale per chiunque prepari un foglio per un altro, e suggerisce una mossa concreta: **stampare, insieme alla cosa, il modo di sapere se è venuta bene senza vederla.**

**Alcune attività dipendono dal tempo che fa,** e nessun'altra famiglia dell'elenco ha questo vincolo. Un foglio che richiede il sole non è un foglio che si consegna oggi per oggi. Alla rassegna vale la pena separare le forme che si fanno subito da quelle che restano in attesa di una condizione, perché sono due oggetti diversi anche se si stampano uguali.

