# Impacchettamento e tassellazione

- **Numero** 376 nell'enciclopedia, capitolo 13 — Giochi matematici e ricreativi
- **Si chiama anche** problema di riempimento, pavimentazione, tassellatura, pentamini, quanti ce ne stanno, *packing problem*, *tiling*, *tessellation*, *sphere packing*
- **In una riga** quante ce ne stanno, e perché non di più.
- **Contratto** voce breve
- **Fonti** `packing-problems.txt`, `sphere-packing.txt`, `circle-packing-in-a-square.txt`, `kissing-number.txt`, `tessellation.txt`, `it-tassellatura.txt`, `aperiodic-tiling.txt`, `einstein-problem.txt`, `penrose-tiling.txt`, `wang-tile.txt`, `squaring-the-square.txt`, `polyomino.txt`, `pentomino.txt`, `it-pentamino.txt`, lette il 2 settembre 2026
- **Stato della ricerca** fatta, 2 settembre 2026

## Che cos'è

Un contenitore e dei pezzi. Si chiede o di metterne dentro il più possibile, o di riempirlo esatto senza buchi e senza sovrapposizioni. `packing-problems.txt` aggiunge che ogni problema di impacchettamento ha il suo gemello di **copertura**, che chiede quanti pezzi servono per coprire ogni punto del contenitore, e lì la sovrapposizione è ammessa.

Le parti mobili:

- **Se il contenitore è finito o è il piano intero.** Sono due discipline: nella scatola si conta, sul piano si misura una densità.
- **Se i pezzi sono uguali o diversi.** Dodici pezzi tutti diversi è un problema; ottanta cerchi uguali è un altro.
- **Se si può ruotare e ribaltare.** Cambia il conto, e cambia il gioco: nei derivati del Tetris si ruota e non si ribalta.
- **Che cosa si chiede di dimostrare.** «Ce ne stanno dodici» si prova mettendoli. «Non ce ne stanno tredici» no.

**La differenza dalla voce 371, costruzione con riga e compasso:** là i tre valori della scala stavano tutti sulla stessa domanda. Qui stanno su **due domande diverse che si assomigliano**. *Si può?* si prova nel materiale, e la disposizione è la sua stessa dimostrazione. *Non si può di più?* non si prova nel materiale in nessun caso, e richiede un argomento — o una macchina. **È l'unica voce del blocco in cui la scala dipende dal verso della domanda**, e il verso non si vede nell'enunciato.

## Da dove viene

**I poligoni regolari che pavimentano il piano da soli sono tre, e il conto è di una riga.** `it-tassellatura.txt`: l'angolo del tassello deve essere un divisore intero di 360 gradi, e questo lascia il triangolo equilatero, il quadrato e l'esagono. `build/check_371.py` scorre tutti i poligoni fino a sessanta lati e trova esattamente 3, 4 e 6. La stessa pagina riporta che le classi di tassellature periodiche del piano sono **esattamente 17**, e che quelle fatte di poligoni regolari con le condizioni consuete sono **11**. **Le due pagine sembrano discordare e non discordano**: `tessellation.txt` dice che le tassellature semiregolari — più di un poligono regolare, stessa disposizione a ogni vertice — sono **otto**, e otto più le tre regolari fanno undici. La prima documenta lo studio di Keplero, *Harmonices Mundi*, **1619**, e gli attribuisce forse la prima spiegazione della struttura esagonale dei favi.

**La domanda «esiste una piastrella sola che pavimenta solo in modo non periodico» è nata nel 1961 e ha avuto risposta nel 2023.** Il filo, in `aperiodic-tiling.txt`, `wang-tile.txt` e `einstein-problem.txt`, si conta in piastrelle: **Hao Wang, 1961**, cerca un algoritmo che decida se un insieme di piastrelle pavimenta il piano; il suo allievo **Robert Berger, 1966**, dimostra che non esiste, traducendo ogni macchina di Turing in un insieme di piastrelle, e come sottoprodotto esibisce il primo insieme aperiodico: **20 426 piastrelle**. Culik, **1996**: tredici. Jeandel e Rao, **2021**: undici, e dimostrato che meno non si può. Poi **novembre 2022**: il matematico dilettante **David Smith** trova il «cappello», una piastrella sola fatta di otto aquiloni incollati; con Kaplan, Myers e Goodman-Strauss ne dà la dimostrazione, e nel maggio **2023** la famiglia degli «spettri», che pavimenta senza nemmeno bisogno di ribaltare. **Da ventimilaquattrocentoventisei a uno in cinquantasette anni**, e l'ultimo passo l'ha fatto un dilettante.

**I pentamini hanno una data di nascita informatica.** `it-pentamino.txt`: il caso 6×10 fu risolto per primo da C. B. e Jenifer Haselgrove nel **1960**; il quadrato 8×8 con un buco 2×2 al centro era stato risolto già nel **1958** da Dana Scott, e l'algoritmo che usò «è stato una delle prime applicazioni informatiche del backtracking». `polyomino.txt` conferma la data del 6×10 e la cifra, 2 339, e aggiunge che i polimini sono nei rompicapo popolari **almeno dal 1907**, e che molti risultati sui pezzi da uno a sei quadretti uscirono sul *Fairy Chess Review* fra il **1937 e il 1957** sotto il nome di «problemi di dissezione». `pentomino.txt` fissa il resto: il primo rompicapo con l'insieme completo sta nei *Canterbury Puzzles* di Henry Dudeney, **1907**; Solomon Golomb li definisce formalmente a partire dal **1953**; e al pubblico li porta Martin Gardner nella rubrica dell'**ottobre 1965**. **Quarantasei anni fra il rompicapo e il nome, e altri dodici prima che li conoscesse qualcuno.**

## Varianti e parenti

- **Riempimento esatto** — nessun buco, nessuna sovrapposizione. I pentamini nel rettangolo.
- **Impacchettamento denso** — quanti cerchi uguali stanno in un quadrato, quante sfere in un metro cubo.
- **Numero di bacio** — quante palle uguali possono toccarne una centrale. In tre dimensioni è **12**.
- **Tassellatura periodica, non periodica, aperiodica** — la terza è quella in cui il pezzo *costringe* alla non periodicità. `penrose-tiling.txt`: le tassellature di Penrose sono l'esempio noto, e la stessa pagina avverte che non esiste «una» tassellatura di Penrose, perché i due rombi ne ammettono infinite che non si distinguono localmente.
- **Quadratura del quadrato** — pavimentare un quadrato con quadrati di lato intero tutti diversi.
- **Copertura** — il problema gemello, con la sovrapposizione ammessa.
- **Voce 159, puzzle a incastro (jigsaw)** — il parente commerciale, dove i pezzi hanno una posizione sola per forma.
- **Voce 370, dissezione geometrica** — là si taglia una figura per rifarne un'altra, qui si riempie un contenitore con pezzi dati.
- **Voce 363, problema di parità** — l'argomento che dimostra che certi riempimenti sono impossibili è quello, e le due voci si toccano sulla scacchiera mutilata.
- **Voce 153, problema di ottimizzazione** — «quanti ce ne stanno» è un problema di ottimizzazione visto da vicino.
- **Voce 275, emergenza** — le tassellature di Penrose come motivo che non si ripete mai.

## Che cosa se ne sa

**La disposizione ovvia smette di essere la migliore, e si può dire esattamente dove.** `circle-packing-in-a-square.txt`: mettere i cerchi in griglia quadrata è ottimo per 1, 4, 9, 16, 25 e 36 cerchi — i sei quadrati perfetti più piccoli — **e smette di esserlo da 49 in poi.** La stessa pagina dice che le soluzioni sono state calcolate per ogni *N* fino a **10 000** ma sono **dimostrate ottime solo per *N* ≤ 30.** Fra il calcolato e il dimostrato ci sono due ordini di grandezza.

**Il numero di bacio in tre dimensioni è dodici, e la difficoltà sta tutta nel tredicesimo.** `kissing-number.txt`: è facile disporne dodici intorno a una centrale e resta parecchio spazio, e non è affatto ovvio che un tredicesimo non ci stia. In una e due dimensioni la risposta è immediata; in tre no. Dodici è anche il numero di coordinazione massimo di un atomo in un reticolo di atomi tutti uguali. `sphere-packing.txt` dà la densità corrispondente: l'impacchettamento più fitto di sfere uguali riempie circa il **74%** del volume, mentre un versamento a caso si ferma intorno al **63,5%**. Che il 74% sia il massimo lo congetturò **Keplero nel 1611**, e Gauss dimostrò nel **1831** che lo è fra tutti gli impacchettamenti reticolari; il caso generale è rimasto aperto quasi quattro secoli.

**I dodici pentamini in un rettangolo 3×20: due riempimenti, e sono stati ricontati.** `build/check_371.py` risolve il problema come copertura esatta: **8** riempimenti contando tutto, **2** a meno delle quattro simmetrie del rettangolo, che è il numero pubblicato da `it-pentamino.txt`. Il rapporto è esattamente quattro, cioè nessun riempimento è simmetrico. **Il conto ha richiesto 172 secondi**, e sulle altre tre scacchiere possibili — 4×15, 5×12, 6×10 — la stessa ricerca non chiude in tempo utile. I numeri della fonte per quelle, che restano non ricontati, sono 368, 1 010 e 2 339.

**Lo spazio che quel riempimento chiude si misura in ordini di grandezza.** Contando per ogni pezzo tutte le sue collocazioni sulla scacchiera 3×20 e moltiplicandole fra loro, le combinazioni indipendenti sono **circa 2 × 10²³**. Le combinazioni che riempiono davvero sono otto. Nel blocco precedente la stessa grandezza andava dai dodici milioni della voce 363, problema di parità al numero con sei milioni di cifre della voce 365, principio dei cassetti: **ventitré cifre stanno in mezzo, e senza il logaritmo non si potevano confrontare.**

**Gli orientamenti dei dodici pentamini, ricontati contro la fonte.** `it-pentamino.txt` li classifica a parole: L, N, P, F e Y in otto modi; Z in quattro; T, V, U e W in quattro per sola rotazione; I in due; X in uno solo. `build/check_371.py` genera i quattro giri e i quattro ribaltamenti di ogni pezzo e li conta: **combaciano tutti e dodici**, per un totale di 63 orientamenti distinti. La stessa pagina aggiunge una cosa che si verifica su carta: **non esiste un polimino con meno di otto quadretti orientabile in due soli modi speculari.**

**La quadratura del quadrato ha un record e una dimostrazione di minimalità.** `squaring-the-square.txt`: il primo quadrato perfetto pubblicato è di Roland Sprague, **1939**, lato 4 205, composto da 55 quadrati. Nel **1978** A. J. W. Duijvestijn trova con una ricerca al calcolatore quello semplice di lato **112** con **21** quadrati, e **21 è dimostrato minimo**. Il gruppo di Cambridge che aprì il campo fra il 1936 e il 1938 — Brooks, Smith, Stone e Tutte, che firmavano insieme come «Blanche Descartes» — lo aveva ridotto a un **circuito elettrico**. **E la cosa non si può fare in tre dimensioni**: non esiste un cubo perfettamente cubato, e la pagina dà la dimostrazione per esteso, in un paragrafo.

**Le tassellature aperiodiche esistevano prima nella materia e nella decorazione.** `aperiodic-tiling.txt`: nel **1984** Dan Shechtman annuncia una lega di alluminio e manganese con un diffrattogramma a simmetria quintupla, che secondo la cristallografia dell'epoca non poteva esistere. E tassellature aperiodiche sono state osservate nelle decorazioni islamiche del santuario di Darb-i Imam in Iran, forse costruite con tecniche *girih* simili a quelle di Penrose. **Il concorso pubblico del 2023 sul «cappello», bandito dal Museum of Mathematics di New York e dallo UK Mathematics Trust, ha ricevuto oltre 245 proposte da 32 paesi.**

## Esempi trovati

Dai pentamini, in `it-pentamino.txt`: riempire il rettangolo con i dodici pezzi. La pagina dice che una soluzione si trova a mano «probabilmente in un paio d'ore», e che contarle tutte è un altro mestiere.

Da Dana Scott, 1958: il quadrato 8×8 con un buco quadrato al centro, che ha **65** soluzioni. La pagina dichiara anche quali posizioni del buco rendono il problema irrisolvibile, e il motivo è la forma dei pezzi P, T e U agli angoli.

Da `squaring-the-square.txt`: il quadrato di lato 112 fatto di 21 quadrati diversi, che è il logo della Trinity Mathematical Society di Cambridge.

Da David Smith, 2022: il «cappello», trovato da un dilettante ritagliando forme di carta. `einstein-problem.txt` lo racconta così, e il *Quanta* citato in nota titola «Un appassionato trova la sfuggente piastrella "einstein" della matematica».

Dal magazzino, in `packing-problems.txt`: il problema di quante scatole rettangolari stanno in un container. È lo stesso problema, e non ha niente di ricreativo.

## Una nostra versione

> **Dodici pezzi, due modi**
>
> Ti do i dodici pentamini — le dodici forme che si fanno con cinque quadretti attaccati — e questa striscia da tre quadretti di altezza:
>
> ```
>  ....................
>  ....................
>  ....................
> ```
>
> Sono sessanta quadretti e i pezzi fanno sessanta quadretti. **Riempila esatta, senza buchi e senza accavallare niente.** I pezzi si possono girare e ribaltare.
>
> Quando ce l'hai fatta, ricopia la tua soluzione qui sotto e prova a trovarne un'altra che non sia la tua rovesciata.
>
> Ce ne sono **due**, contando come una sola quelle che si ottengono girando o specchiando tutta la striscia. Non c'è nessuna terza.

Che la soluzione sia giusta lo dice la striscia: se resta un buco o si accavalla qualcosa, si vede. Che le soluzioni siano due lo dice un conto che non si fa a mano: sono le otto trovate da `build/check_371.py`, divise per le quattro simmetrie del rettangolo. **Le due domande stanno sullo stesso foglio e si verificano in due posti diversi**, ed è per questo che il numero due va stampato invece di essere chiesto. La striscia 3×20 è la più stretta delle quattro possibili, ed è anche quella con meno soluzioni: le altre ne hanno 368, 1 010 e 2 339.

## Da riprendere alla rassegna

**È l'unica voce del blocco in cui la scala si biforca dentro la stessa forma.** «Riempi la striscia» ha la verifica nel materiale, e non c'è tolleranza né inganno: o i sessanta quadretti sono coperti o non lo sono. «Ce ne sono due e non tre» non ha nessuna verifica disponibile a chi riceve il foglio, e la nostra sta in una ricerca esaustiva di tre minuti. **Alla rassegna: la stessa consegna può contenere una domanda controllabile e una no, e la differenza non si vede leggendola.**

**Il fatto da portare via è che l'ovvio smette di funzionare a un punto preciso.** I cerchi in griglia sono ottimi fino a 36 e non più da 49. È il genere di affermazione che vale la pena stampare, perché contraddice l'intuizione e ha un confine esatto invece di un «a volte». Con il tredicesimo bacio, che non c'è ma non si vede perché no, fa due esempi buoni della stessa cosa.

**Cinquantasette anni da ventimila piastrelle a una, e l'ultima l'ha trovata un dilettante ritagliando carta.** Alla rassegna vale come argomento sul capitolo intero: le forme del capitolo 13 hanno un bordo aperto su cui si può ancora entrare senza attrezzatura. È la seconda volta che compare — la prima era il pezzo di Dudeney, chiuso nel dicembre 2024 alla voce 370, dissezione geometrica.

**Il costo materiale è il più alto del blocco.** Dodici pentamini vanno ritagliati, e ritagliarli bene richiede più tempo di quanto ne richieda risolverne uno. La stampa in bianco e nero li dà su carta; il cartoncino li rende usabili più volte. **È l'unica voce del blocco in cui la preparazione dura più della consegna**, e alla rassegna questo va contato, perché la casa ha una persona sola.

**Il vincolo di `ideas/10 §8` non morde**: la soluzione si compone al contrario — la si costruisce e poi si consegna la striscia vuota —, e quello che chi risolve produce è una figura, non un testo da leggere.

