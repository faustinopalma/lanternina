# Cubo di Rubik e combinatori

- **Numero** 172 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi fisici e meccanici»
- **Si chiama anche** cubo magico, twisty puzzle, rompicapo a mosse sequenziali, combination puzzle, sequential move puzzle, Pyraminx, Megaminx, torre di Hanoi, cubo Soma, speedcubing
- **In una riga** un solido che si gira a strati e torna in ordine con una sequenza di mosse.
- **Fonti** `rubiks-cube.txt`, `combination-puzzle.txt`, `gods-algorithm.txt`, `tower-of-hanoi.txt`, `soma-cube.txt`, `it-cubo-di-rubik.txt`, `mechanical-puzzle.txt` sezione «Sequential movement», lette il 31 agosto 2026. I conti sul rompicapo a cinque carte dell'esempio sono nostri, fatti con `build/check_172.py`; il controllo aritmetico sui 275 sono in `build/check_172b.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Un oggetto fatto di pezzi che si spostano in gruppo. Una mossa non prende un pezzo: prende un intero strato e lo gira, e con lui tutti i pezzi che ci stanno dentro. Il compito è arrivare a una configurazione riconoscibile — tutti i colori insieme, tutti i numeri in ordine — partendo da una mescolata.

`combination-puzzle.txt` dà la definizione più utile: **la costruzione meccanica definisce le regole.** Non c'è un regolamento scritto da rispettare, c'è un oggetto che consente certe operazioni e non altre. Da lì viene la proprietà che fa la famiglia: gli attaccatempi che si potrebbero ottenere staccando gli adesivi, o smontando il cubo e rimontandolo, sono molti di più di quelli che si ottengono girando gli strati, e **la maggior parte delle configurazioni non si raggiunge affatto.**

Parti mobili:

- **Che cosa si gira.** Una faccia (cubo di Rubik), un angolo (Skewb), uno spigolo. Cambiando l'asse di rotazione dallo stesso solido escono rompicapi diversi.
- **Quanti strati.** Dal 2×2×2 al 21×21×21 di produzione industriale, e fino al 49×49×49 costruito una volta sola.
- **Se i pezzi sono distinguibili.** Le facce centrali del cubo originale non hanno un verso, quindi possono restare girate senza che si veda; marcarle — un *supercubo* — aggiunge 2048 configurazioni distinguibili e cambia il rompicapo senza cambiare l'oggetto.
- **Se la meccanica è necessaria.** Non lo è. Basta che le regole delle operazioni siano definite: esistono rompicapi combinatori che si realizzano solo in software, come il tesseratto 3×3×3×3 in quattro dimensioni.
- **Che cos'è una mossa,** e quindi come si contano. Un quarto di giro e un mezzo giro possono valere uno o due, e i due conti danno due numeri diversi per lo stesso rompicapo.

La parte mobile che distingue questa famiglia dalla voce 171, puzzle a scorrimento (15, Sokoban) è che **qui non c'è nessun vuoto.** Nel gioco del 15 il movimento è possibile solo perché una casella è libera; qui l'oggetto è pieno e si muove lo stesso, perché a muoversi sono strati interi. Ne segue la differenza pratica: nel gioco del 15 le mosse legali dipendono da dove si trova il buco e cambiano a ogni passo, nel cubo sono sempre le stesse dodici.

Il modo in cui la si risolve ha un nome proprio e non è quello che si crede. Nel gergo di chi risolve il cubo, un **algoritmo** è una sequenza di mosse memorizzata di cui si conosce l'effetto. Molti algoritmi sono costruiti apposta per cambiare solo una piccola parte dell'oggetto senza toccare quello che è già a posto — per esempio ruotare tre angoli lasciando fermo tutto il resto — e si applicano ripetutamente in punti diversi finché non è finito. **Non si risolve un cubo pensando: si risolve applicando trasformazioni locali di cui si è imparato l'effetto.**

## Da dove viene

**Ernő Rubik non stava costruendo un rompicapo.** Insegnava disegno e architettura al dipartimento di architettura d'interni dell'Accademia di arti e mestieri applicati di Budapest, a metà degli anni Settanta, e `rubiks-cube.txt` corregge esplicitamente la versione diffusa secondo cui il cubo sarebbe nato come strumento didattico per spiegare gli oggetti tridimensionali: il suo scopo vero era **un problema strutturale**, far muovere molte parti piccole in modo indipendente tenendole insieme in un unico meccanismo coerente. Che fosse un rompicapo se ne accorse solo dopo averlo mescolato per la prima volta e aver provato a rimetterlo a posto. **Ci mise circa un mese, per tentativi.**

Questa è la cosa più importante di tutta la voce, e non riguarda il cubo. **Chi ha costruito l'oggetto non conosceva la risposta**, e l'ha dovuta cercare come chiunque altro. Il vincolo che chiude questo capitolo — un enigma ha una risposta e qualcuno deve saperla — qui non si pone, per la stessa ragione della voce 169, scatola a segreto: la risposta sta dentro la cosa, non dentro una persona.

Le date: domanda di brevetto ungherese per il «cubo magico» il **30 gennaio 1975**, brevetto HU170062 concesso nello stesso anno; primi lotti di prova alla fine del **1977**, venduti nei negozi di giocattoli di Budapest; **febbraio 1979**, Tibor Laczi lo porta alla fiera di Norimberga, dove lo nota Tom Kremer della Seven Towns; **settembre 1979**, accordo con la Ideal Toys; **gennaio-febbraio 1980**, debutto internazionale alle fiere di Londra, Parigi, Norimberga e New York; **maggio 1980**, primo lotto ufficiale esportato dall'Ungheria. Il nome nuovo lo volle la Ideal, che cercava qualcosa di registrabile: fra i nomi considerati c'erano «Il nodo gordiano» e «Oro inca».

Il cubo aveva dei precursori con i brevetti in regola. **Larry D. Nichols** inventa nel marzo **1970** un 2×2×2 con i pezzi rotabili in gruppo, tenuto insieme da magneti, e ottiene il brevetto statunitense 3 655 201 l'11 aprile **1972**, due anni prima del cubo di Rubik. La sua società fa causa alla Ideal nel 1982: nel 1986 la corte d'appello stabilisce che il Pocket Cube 2×2×2 viola il brevetto di Nichols, **ma non il 3×3×3.** In parallelo Terutoshi Ishigi, ingegnere autodidatta con una ferriera vicino a Tokyo, deposita un meccanismo quasi identico e ottiene un brevetto giapponese nel 1976; la fonte lo dà per una reinvenzione indipendente, spiegando perché — fino al 1999 l'ufficio brevetti giapponese non richiedeva la novità mondiale.

La mania: fra il **1980 e il 1983** si stimano **200 milioni** di cubi venduti nel mondo. Nel marzo 1981 il *Guinness dei primati* organizza un campionato di velocità a Monaco, e nello stesso mese il cubo è in copertina sullo *Scientific American*. Nel 1981 **tre dei dieci libri più venduti negli Stati Uniti spiegavano come risolverlo**, e il più venduto dell'anno era *The Simple Solution to Rubik's Cube* di James G. Nourse, oltre sei milioni di copie. Uno di quei libri, *You Can Do The Cube*, lo scrisse **Patrick Bossert, tredici anni**, con una notazione grafica sua pensata per chi non sapeva niente. Nell'ottobre 1982 il *New York Times* scrive che la mania è finita.

La torre di Hanoi è più vecchia e la sua origine è **inventata dall'autore come parte del prodotto.** La costruisce il matematico francese **Édouard Lucas** e la presenta nel **1883** come un gioco scoperto da «N. Claus (de Siam)» — anagramma di «Lucas d'Amiens». Con il gioco veniva un libretto che ne raccontava le origini in Tonchino e la leggenda dei bramini di Benares, che spostano sessantaquattro dischi d'oro con le stesse regole, e quando avranno finito il mondo finirà. Al ritmo di una mossa al secondo, sessantaquattro dischi richiedono 2⁶⁴ − 1 secondi, cioè **585 miliardi di anni, circa quarantadue volte l'età stimata dell'universo.**

Il cubo Soma nasce durante una lezione. **Piet Hein**, nel **1933**, mentre Werner Heisenberg parla di meccanica quantistica, si accorge che i pezzi fatti di al più quattro cubetti uniti per le facce e con almeno un angolo rientrante sono esattamente sette, e che 3 + (6 × 4) fa 27, cioè un cubo 3×3×3. Lo rende famoso Martin Gardner nella rubrica *Mathematical Games* dello *Scientific American* del settembre **1958**.

## Varianti e parenti

- **Cubi di ordine diverso** — dal 2×2×2 al 7×7×7, che la World Cube Association ammette in gara; oltre, dice la fonte, i cubi diventano ingombranti e soggetti a guasti meccanici, e il tempo medio di risoluzione cresce come il quadrato dell'ordine.
- **Altri solidi** — Pyraminx (tetraedro), Skewb Diamond (ottaedro), Megaminx (dodecaedro), Dogic (icosaedro), Alexander's Star. La stessa idea su qualunque poliedro regolare.
- **Rompicapi che cambiano forma** — Rubik's Snake, Square One: mescolandoli smettono di essere il solido di partenza.
- **Torre di Hanoi** — il caso più piccolo della famiglia: tre paletti, dischi di misure diverse, e il divieto di mettere un disco grande su uno piccolo. È l'unico rompicapo di questo genere di cui si conosca l'algoritmo ottimo per qualunque taglia.
- **Cubo Soma** — sette pezzi da comporre in un cubo. Sta al confine con la voce 160, tangram e puzzle di tassellazione: là si copre una figura piatta, qui se ne riempie una solida, e i pezzi si prendono in mano.
- **Voce 171, puzzle a scorrimento (15, Sokoban)** — l'altra famiglia in cui i pezzi non escono mai e metà delle configurazioni non si raggiunge. Il vincolo lì è lo spazio vuoto, qui è la meccanica degli strati.
- **Voce 167, puzzle di districamento** — anche lì l'oggetto è la regola, ma il compito è separare due pezzi invece di riordinarli.
- **Voce 109, kit** — un cubo è una scatola di pezzi che non si svuota mai: la stessa cosa produce infiniti problemi.
- **Voce 102, ricetta** — un algoritmo del cubo è una sequenza da eseguire e da modificare, e si scrive nello stesso modo.
- **Voce 367, gioco combinatorio imparziale** — il capitolo 13 raccoglie i giochi in cui due avversari si alternano e c'è una strategia vincente da trovare. Qui il giocatore è uno solo e non c'è nessuno da battere: il confine è netto e non si pone quasi mai.
- **Voce 363, problema di parità** e **voce 364, invariante** — il motivo per cui certe configurazioni non si raggiungono è un invariante, e la sua dimostrazione appartiene a quelle voci. Qui si descrive la forma di pagina.

## Che cosa se ne sa

**Il numero delle configurazioni, e quello della pubblicità.** Il cubo 3×3×3 ha 8! modi di disporre gli angoli, 3⁷ orientamenti degli angoli, 12!/2 disposizioni degli spigoli e 2¹¹ orientamenti, cioè **43 252 003 274 489 856 000**, circa 4,3 × 10¹⁹. La pubblicità originale annunciava «oltre 3 000 000 000 (tre miliardi) di combinazioni ma una sola soluzione»: **sbagliava per dieci ordini di grandezza**, e non per prudenza — il numero vero non lo sapeva nessuno al momento di scrivere la scatola.

**Le configurazioni raggiungibili sono un dodicesimo di quelle costruibili.** Smontando il cubo e rimontandolo a caso si ottengono 519 024 039 293 878 272 000 disposizioni, dodici volte tante, e solo un dodicesimo è risolvibile: non esiste nessuna sequenza di mosse che scambi due soli pezzi o giri un solo angolo. Le dodici classi si chiamano *universi* o *orbite*. **Rimontare un cubo a caso lo lascia risolvibile una volta su dodici**, ed è il modo più economico di rompere l'oggetto senza toccarlo.

**Una contraddizione fra le due pagine, e stavolta la decide un conto.** `rubiks-cube.txt` dice che avendo un cubo per ogni configurazione si coprirebbe la superficie terrestre **275** volte; `it-cubo-di-rubik.txt`, che per il resto è una traduzione fedele, dice **257**. Il conto fatto in `build/check_172b.py` con il lato standard di 5,7 cm dà **275,5 volte** la superficie terrestre e **260,6 anni luce** di torre, e la pagina inglese dà 261 anni luce: le due cifre inglesi sono coerenti fra loro e con lo stesso lato, mentre 257 richiederebbe un cubo da 5,5 cm, che darebbe 251 anni luce e non 261. **Si scarta il 257: è una trasposizione di cifre.**

**Il numero di Dio è venti, ed è stato dimostrato.** Dal 1995 si sapeva che venti era un limite inferiore. Singmaster lo aveva congetturato «avventatamente» nel 1980. Kunkle e Cooperman scendono a 26 nel 2007, Rokicki a 22 nel 2008, e nel **luglio 2010** una squadra che comprende Rokicki, con i calcolatori messi a disposizione da Google, dimostra che **nessuna configurazione richiede più di venti mosse**, e che milioni ne richiedono esattamente venti. `gods-algorithm.txt` definisce la nozione in generale: il numero di Dio di un rompicapo è il valore massimo, su tutte le configurazioni di partenza, della lunghezza della soluzione ottima.

**Una sequenza ripetuta torna sempre al punto di partenza, e il numero di volte è il suo periodo.** Un mezzo giro ha periodo 2, un quarto di giro periodo 4, e **il periodo massimo sul cubo è 1260.** È il fatto più utile della voce per chi debba costruire un'attività: qualunque sequenza si scelga a caso, ripetendola si torna a casa, e non si può rovinare niente.

**Le tecniche umane sono catalogate e si contano.** Un metodo per principianti a strati richiede **da tre a otto algoritmi**; il CFOP di Jessica Fridrich, usato da chi va veloce, ne ha **centoventi** in tutto. Il metodo di Philip Marshall ne chiede due soli, a costo di una media di sessantacinque mosse per risolverlo. **La stessa cosa si fa con tre regole o con centoventi, e il prezzo è la lunghezza:** è la relazione più netta fra quanto si impara e quanto si lavora incontrata finora.

**Le prestazioni, per quello che valgono.** Record del mondo su un singolo cubo 3×3×3: **2,76 secondi**, Teodor Zajder, 8 febbraio 2026. Bendato, memorizzazione compresa: 11,56 secondi. Un robot: 0,38 secondi. E la gara che interessa di più qui è quella del **minor numero di mosse**, in cui si ha un'ora per progettare la soluzione e il record è **16 mosse**, ottenuto da quattro persone diverse fra il 2019 e il 2024. È l'unica gara della famiglia in cui non conta la velocità della mano.

**Il cubo Soma ha 240 soluzioni distinte**, escluse rotazioni e riflessioni, e Conway e Guy le trovarono tutte a mano nel **1961**. La confezione della Parker Brothers ne dichiarava 1 105 920, contando anche rotazioni e riflessioni di ognuna e le rotazioni dei singoli pezzi: **due numeri veri per la stessa cosa**, e la differenza è solo che cosa si conta come diverso.

**Il cubo Soma è stato usato per misurare la motivazione, e il risultato riguarda tutto questo progetto.** Nel 1969 Edward Deci chiese ai partecipanti di risolverne il più possibile in un tempo dato, con incentivi diversi, e ne ricavò la teoria dello spiazzamento della motivazione intrinseca. **È l'unico caso, in tutta l'enciclopedia, in cui una forma raccolta qui è stata lo strumento con cui si è dimostrato che pagare qualcuno per fare una cosa che gli piace gliela fa piacere di meno.**

**La leggenda della torre di Hanoi è stata scritta dall'inventore per vendere il gioco,** e questo la rende un caso diverso dalle otto attribuzioni dubbie già raccolte: qui non c'è nessuno che si prenda un merito altrui, c'è un autore che si toglie il proprio e regala l'origine a dei bramini immaginari. `tower-of-hanoi.txt` registra che le varianti della leggenda si sono poi moltiplicate da sole — il tempio diventa un monastero, i sacerdoti diventano monaci, il luogo cambia, e in qualche versione i monaci fanno una mossa al giorno.

## Esempi trovati

Il cubo di Rubik 3×3×3, sei facce di sei colori, ognuna girabile indipendentemente.

Il Pocket Cube 2×2×2, che è il cubo di Nichols di due anni prima, e che in tribunale è risultato tale.

La torre di Hanoi: tre paletti, dischi di diametro decrescente, e il divieto di posare un disco su uno più piccolo. Con tre dischi si fa in sette mosse; con *n* dischi ne servono 2ⁿ − 1, e questa è una delle poche formule chiuse di tutto il capitolo.

Il cubo Soma di Piet Hein: sette pezzi fatti di cubetti, da comporre in un 3×3×3, e poi in tutte le altre figure che il manuale propone.

Il *supercubo*: un cubo normale con le facce centrali marcate, in cui si può arrivare a una soluzione apparente e scoprire che i centri sono girati.

I cubi che non sono cubi: 2×2×4, 2×3×4, 3×3×5. Girandoli smettono di essere parallelepipedi e prendono forme irregolari, e questa è la loro difficoltà.

Il tesseratto 3×3×3×3 del programma MagicCube4D, che esiste solo come regola perché in tre dimensioni non si può costruire.

## Una nostra versione

> **Cinque carte e due mosse**
>
> Ritaglia cinque cartellini e scrivici sopra A, B, C, D, E. Mettili in fila su un tavolo, in quest'ordine. Le posizioni sono cinque e restano ferme; a muoversi sono le carte.
>
> Hai due mosse sole, e **ognuna sposta tre carte alla volta**, mai una.
>
> ```
>   S   le tre carte di SINISTRA girano in tondo:
>       quella in 1 va in 2, quella in 2 va in 3, quella in 3 va in 1
>
>   D   le tre carte di DESTRA girano in tondo:
>       quella in 3 va in 4, quella in 4 va in 5, quella in 5 va in 3
>
>   posizioni:   1   2   3   4   5
>               ─── ─── ─── ─── ───
>               └─── S ───┘
>                       └─── D ───┘
>
>   la posizione 3 è in tutte e due: è quella che tiene insieme il rompicapo
> ```
>
> Puoi fare anche le due mosse all'indietro. Chiamale **S'** e **D'**: sono la stessa cosa girata dall'altra parte, e disfano quello che S e D hanno fatto.
>
> **Primo.** Metti le carte così, e riportale in ordine ABCDE.
>
> ```
>            E   D   C   B   A
>           ─── ─── ─── ─── ───
> ```
>
> Si fa in cinque mosse. Se ne fai di più non hai sbagliato: cinque è il minimo.
>
> **Secondo.** Riparti da ABCDE. Fai S, poi D. Poi ancora S, poi D. Poi ancora, e ancora. **Quante volte devi ripetere «S poi D» prima che le carte tornino da sole nell'ordine di partenza?** Scrivi il numero qui: ────
>
> Non c'è modo di sbagliare questa: se continui, prima o poi torna. Vale per qualunque sequenza tu scelga, anche una inventata da te — provane una lunga e conta.
>
> **Terzo, ed è il vero.** Le tue mosse spostano sempre tre carte vicine. Servirebbe qualcosa di più mirato.
>
> ```
>   Trova una sequenza di mosse che lasci ferme la carta in 1 e la carta in 3,
>   e sposti soltanto le altre tre.
>
>   Scrivila qui: ──────────────────────────────────────────────────
>
>   Ce n'è una di tre mosse.
> ```
>
> Quello che hai appena scritto, chi risolve il cubo di Rubik lo chiama **un algoritmo**: una sequenza di cui si sa l'effetto, che tocca poco e lascia in pace il resto. Un cubo si risolve così, non a forza di pensarci. Un principiante ne impara fra tre e otto; chi va in gara ne sa centoventi.

Le carte sono cinque perché tutto quello che il foglio afferma si può controllare a mano. Con `build/check_172.py`: le disposizioni possibili sono **120**, quelle raggiungibili con S e D sono **60**, cioè esattamente la metà, e la più lontana da ABCDE sta a **sei** mosse — il numero di Dio di questo rompicapo, che sul cubo vero è venti. La fila rovesciata EDCBA si rimette a posto in cinque mosse, per esempio con S D' S D' S. Ripetendo «S poi D» si torna a casa dopo **cinque** ripetizioni. E la sequenza S D S' lascia ferme la prima e la terza carta e sposta le altre tre: è un algoritmo di tre mosse, ed è costruito nel modo in cui si costruiscono quelli veri — si sposta qualcosa, si fa la mossa che serve, si rimette a posto.

Le tre consegne hanno tre verifiche diverse, e nessuna passa da una seconda persona. La prima si vede: le carte sono in ordine oppure no. La seconda **non può fallire**, perché qualunque sequenza ripetuta torna al punto di partenza; l'unica cosa che si può sbagliare è contare. La terza si controlla guardando due posizioni: se in 1 e in 3 c'è quello che c'era prima e le altre tre sono cambiate, è giusta, e non importa quale delle sequenze possibili si sia trovata.

Dove si romperebbe: il cubo vero è un oggetto e questo non lo è. Cinque cartellini si possono sollevare e rimettere dove si vuole, quindi **il vincolo che definisce la forma è di nuovo una regola d'onore**, come nella voce 171, puzzle a scorrimento (15, Sokoban). E soprattutto manca la cosa che rende il cubo quello che è: la sensazione della mano che gira uno strato e vede muoversi otto pezzi insieme senza averlo deciso. Su carta la mossa va eseguita spostando tre cartellini uno per volta, cioè **facendo a mano quello che l'oggetto farebbe da solo**, e il rompicapo diventa più lento e più esatto.

## Da riprendere alla rassegna

**Chi costruisce l'oggetto può non conoscere la risposta.** Rubik mise un mese a risolvere il proprio cubo. È la seconda occorrenza dopo la scatola a segreto della voce 169, scatola a segreto, e insieme dicono una cosa più larga di tutte e due: **il vincolo che chiude questo capitolo si scioglie quando l'oggetto è più vecchio della domanda.** Da cercare sistematicamente alla rassegna, perché è la via d'uscita che non chiede niente a nessuno.

**Una consegna che non può fallire.** «Ripeti una sequenza qualsiasi finché non torna a posto» ha sempre una risposta, per qualunque sequenza, e l'unica cosa che si può sbagliare è contare. Non è il vuoto autorizzato e non è il fallimento annunciato: è **un compito senza modo di sbagliare che non è per questo banale**, perché il numero non si indovina. Non ce n'erano altri nell'elenco.

**Il prezzo di sapere meno si paga in lunghezza, ed è misurato.** Da tre a otto algoritmi per risolvere il cubo lentamente, centoventi per risolverlo in fretta, due soli a costo di sessantacinque mosse in media. È la prima volta che l'enciclopedia può mettere accanto **quanto si impara** e **quanto si lavora** con due numeri della stessa fonte, e la relazione va cercata altrove.

**Un rompicapo si mescola in un secondo e si risolve in un mese.** L'asimmetria fra costruire e risolvere, che alla voce 164, labirinto su carta stava dalla parte di chi costruisce, qui è ancora più larga, e con un rischio nuovo: mescolare a caso un oggetto smontato lo lascia risolvibile **una volta su dodici**. Per un sistema che stampa configurazioni di partenza, il rischio è produrre l'impossibile senza accorgersene, ed è lo stesso del gioco del 15.

**Una forma di questo elenco è stata lo strumento di un esperimento sulla motivazione.** Il cubo Soma nelle mani di Deci, 1969. Se una delle attività raccolte qui è servita a dimostrare che il premio spegne l'interesse, la cosa riguarda ogni riga che questo progetto stamperà accanto a un compito.

**Un'origine inventata dall'autore stesso, come parte del prodotto.** La leggenda dei bramini di Benares è di Lucas, che firmò il gioco con un anagramma del proprio nome. Le attribuzioni dubbie raccolte diventano dieci, ma questa è di un genere nuovo: non toglie un merito a nessuno, **regala il proprio a un'invenzione narrativa**, e ha funzionato tanto bene che la leggenda si è poi moltiplicata da sola.

