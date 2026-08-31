# Ramificazione

- **Numero** 269 nell'enciclopedia, capitolo 9 — Meccaniche di gioco
- **Si chiama anche** biforcazione, albero della storia, storia a bivi, libro-gioco, «se vai a nord vai al 98», *branching narrative*, *branching storyline*, *CYOA*, *multiple endings*, *route*
- **In una riga** la storia va diversamente. È quello che questo formato già fa.
- **Fonti** `gamebook.txt`, `choose-your-own-adventure.txt`, `nonlinear-gameplay.txt`, `visual-novel.txt`, `interactive-fiction.txt`, `nonlinear-narrative.txt`, lette il 31 agosto 2026. I conti sui costi di un albero e sulle letture necessarie sono nostri, verificati in `build/check_269.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Il testo non è una fila. A certi punti si divide, e quello che si legge dopo dipende da quale strada si è presa.

**Va tenuta separata dalla voce 268, scelta con conseguenza, che è il nodo, mentre questa è l'albero.** Là si guarda una decisione e ci si chiede se cambiarla cambi qualcosa; qui si guarda la struttura intera e ci si chiede quanto costi scriverla, quanto se ne veda in una lettura, e quante letture servano per vederla tutta.

**E il confine con la voce 263, sblocco di contenuti è già scritto lì, e va ripetuto:** uno sblocco rimanda e non toglie — tutto il contenuto resta raggiungibile, cambia soltanto l'ordine —, **una ramificazione fa perdere le strade non prese.** Chi legge un ramo non legge l'altro, e per leggerlo deve ricominciare.

**Attenzione a una parola che copre due cose diverse.** `nonlinear-narrative.txt` chiama «narrazione non lineare» il racconto che non segue l'ordine cronologico: cominciare *in medias res*, i salti indietro, le trame parallele. **Non è questa forma.** Quella è una scelta di chi scrive su come disporre eventi già decisi; questa è una scelta di chi legge su quali eventi accadranno. La pagina è stata letta e serve solo a segnare il confine.

Parti mobili:

- **Quanti rami per bivio.** Due o tre nei libri-gioco.
- **Se i rami si richiudono.** Un albero che non si richiude mai raddoppia a ogni bivio; uno che si richiude resta piccolo.
- **Quanti finali.** È l'unico numero che di solito viene dichiarato.
- **Se i finali sono equivalenti.** `gamebook.txt`: nei libri-gioco solitari c'è spesso **un solo finale «riuscito»**, e tutto il resto sono fallimenti, il che rende il libro un enigma; nei romanzi a trama ramificata i finali tendono a essere parecchi e ugualmente validi.
- **Se si torna indietro.** Con un dito nella pagina si torna sempre, e nessun libro può impedirlo.
- **Come si nascondono le strade.** Nei libri-gioco con la numerazione mescolata: i paragrafi non sono nell'ordine in cui si leggono.

## Da dove viene

**Da un'idea che ha dovuto aspettare cinque anni e nove rifiuti.** `choose-your-own-adventure.txt`: Edward Packard racconta che l'idea nasce dalle storie della buonanotte alle figlie, attorno a un personaggio di nome Pete: «Quella sera non sapevo più che cosa fargli fare, così ho chiesto a loro che cosa avrebbero fatto». Le due bambine proposero strade diverse e Packard scrisse un finale per ognuna. Nel **1970** cerca un editore e viene **rifiutato da nove case editrici**; mette da parte l'idea. Nel **1975** convince Ray Montgomery della Vermont Crossroads Press, e *Sugarcane Island* vende ottomila copie, molte per un piccolo editore locale.

**Poi i numeri diventano grandi.** La serie *Choose Your Own Adventure* nasce alla Bantam nel **1979** con *The Cave of Time*; fra il 1979 e il 1998 la Bantam ne pubblica **184 titoli**, che vendono **più di 250 milioni di copie** e sono tradotti in **40 lingue**. La serie viene interrotta nel 1999 e ripresa da un'altra casa, Chooseco, nel 2003. Nel gennaio 2019 Chooseco fa causa a Netflix per il film *Black Mirror: Bandersnatch*, e la causa si chiude con un accordo nel novembre 2020.

**I precursori sono letterari e sono più vecchi.** `gamebook.txt`: *Consider the Consequences!*, 1930; la commedia di Ayn Rand del 1936 con la giuria presa dal pubblico; Borges nel 1941, con un romanzo immaginario a **due biforcazioni e nove finali**; il libro per bambini *Treasure Hunt*, 1945. Negli anni Sessanta ci provano in molti paesi: Guimard in francese nel 1961, Cortázar con *Rayuela* nel 1963, Max Aub nel 1964, l'Oulipo dal 1967, e in italiano **Gianni Rodari con *Tante storie per giocare*, 1971**. Il primo libro-gioco a tutti gli effetti secondo la fonte è **_Lucky Les_ di E. W. Hildick, 1967**, che si dichiarava nella quarta di copertina «un gioco in forma di libro».

**E c'è un antenato che non è letterario, ed è quello che riguarda questo progetto.** `gamebook.txt` riconosce come influenza precoce **i materiali di istruzione programmata**, applicati nella serie di manuali interattivi *TutorText*, pubblicati dalla fine degli anni Cinquanta ai primi anni Settanta: presentano una serie di problemi con più risposte possibili; **se la risposta è giusta si passa al problema seguente, se è sbagliata si riceve una spiegazione e si torna a scegliere.** La pagina dichiara che questa tecnica didattica «avrebbe costituito la base di molte successive serie narrative di libri-gioco». **La ramificazione è nata come strumento di correzione prima di essere uno strumento di racconto.**

**Nei videogiochi la forma ha un genere in cui è la norma e una regione in cui è dominante.** `visual-novel.txt`: nel **2006 i romanzi visuali erano oltre il 70% del mercato dei giochi per calcolatore in Giappone**. Camingue, Cartendottir e Melcer, su un corpo di cinquantaquattro titoli, trovano che **nove definizioni del genere su trenta** includono la ramificazione, e che **il 18% dei giochi non ha nessuna ramificazione.**

## Varianti e parenti

- **Albero puro** — non si richiude mai, e raddoppia a ogni bivio.
- **Albero che si richiude** — i rami convergono su un evento inevitabile. `nonlinear-gameplay.txt` lo classifica come compromesso fra lineare e ramificato.
- **Struttura a somma** — il finale dipende da quante volte si è scelto in un certo modo, non da quale strada si è fatta. Descritta alla voce 268, scelta con conseguenza.
- **Libro-gioco solitario** — con dadi, oggetti e punti ferita, ed è un enigma con un finale giusto.
- **Romanzo a trama ramificata** — senza regole, e con finali tutti buoni allo stesso modo.
- **Ipertesto** — la ramificazione senza numeri di paragrafo, e senza un ordine di lettura suggerito.
- **Percorsi multipli con protagonisti diversi** — la stessa vicenda vista da persone diverse, e le scelte dell'una cambiano quello che succede all'altra.
- **Voce 268, scelta con conseguenza** — il singolo nodo di questo albero.
- **Voce 263, sblocco di contenuti** — dove niente si perde e cambia solo l'ordine.
- **Voce 43, taglio** — perché su carta un ramo che non si deve vedere è una piega o una busta.
- **Voce 22, diario / registro** — perché in un albero grande chi legge finisce per tenere il conto di dov'è stato.

## Che cosa se ne sa

**Le fonti non contengono nessuno studio sull'effetto della ramificazione su chi legge, ma contengono i costi e le reazioni, e sono precisi.** `nonlinear-gameplay.txt`: le storie lineari costano meno tempo e meno denaro; diversi giochi di *Wing Commander* avevano storie ramificate e **furono abbandonate perché troppo care**; le storie ramificate aumentano le probabilità di difetti e di assurdità; e **alcuni giocatori hanno reagito male perché è difficile e noioso arrivare al «valore pieno» di tutto il contenuto.**

**L'ultima è l'unica affermazione della voce che si possa trasformare in un numero, e il numero è grande.** Un albero binario pieno di cinque bivi ha trentadue finali e sessantatré paragrafi; una lettura ne attraversa sei. **Chi legge una volta vede il 9,5% del libro.** Con sei bivi scende al 5,5%, con otto all'1,8%.

**E la stessa cosa si può dire dal lato del lettore che vuole vedere tutto.** Se ogni lettura arrivasse a uno dei finali scelto a caso fra tutti — **ipotesi che in un libro vero è falsa**, perché i finali non sono equiprobabili e chi legge non sceglie a caso —, per vederli tutti servirebbero in media:

```
   finali    letture attese
        7             18,15
       12             37,24
       20             71,95
       44            192,40
       85            427,19
```

(`build/check_269.py`: calcolate per la formula del collezionista di figurine, *n* volte l'*n*-esimo numero armonico, **e** per la somma a inclusione ed esclusione delle probabilità di non aver finito, che è un'altra strada allo stesso numero; concordi su tutti i valori.)

**I numeri delle righe non sono inventati.** `choose-your-own-adventure.txt`: nella serie **il numero di finali va da 44 nei primi titoli a 7 negli ultimi**. `visual-novel.txt`: *428: Shibuya Scramble*, 2008, può arrivare a **85 finali**; `nonlinear-gameplay.txt` attribuisce a *Star Ocean: The Second Story* **86 finali** con centinaia di permutazioni, e lo dichiara un riferimento per il numero di esiti possibili di un videogioco. **Un libro da quarantaquattro finali chiede in media centonovantadue letture per essere visto tutto, e ne ha centonovantadue perché ha quarantaquattro finali, non perché sia lungo.**

**La struttura che costa meno per finale non è l'albero, e il confronto sta in tre righe.** Cinque scelte binarie:

```
  la struttura      finali   paragrafi   letti in una volta   quota vista
  albero pieno          32          63                    6           10%
  imbuto                 1          11                    6           55%
  a somma                6          11                    6           55%
```

(`build/check_269.py`: i conteggi dell'albero pieno ricavati costruendo esplicitamente i nodi livello per livello **e** dalla forma chiusa, concordi fino a otto livelli.) **La struttura a somma costa gli stessi undici paragrafi dell'imbuto, che non ha nessun bivio vero, e ne consegna sei finali invece di uno.**

**Un vincolo che vale per qualunque albero, e che si può dimostrare.** Un albero binario stretto con *L* finali ha esattamente *L*−1 nodi interni: verificato per enumerazione su tutti gli alberi distinti da uno a sette foglie — 1, 1, 2, 5, 14, 42 e 132 alberi rispettivamente, tutti con lo stesso numero di nodi interni. **Quarantaquattro finali richiedono almeno quarantatré punti di diramazione e almeno ottantasette paragrafi**, comunque si disegni l'albero. È un pavimento, non una stima.

**Nessuna delle 850 pagine locali dice se chi legge un libro a bivi ricordi meglio, capisca di più, o torni più volentieri.** Le fonti raccontano che cosa è stato pubblicato, quanto ha venduto e quanto è costato produrlo. **Va verificato**, ed è una lacuna notevole per una forma che ha venduto duecentocinquanta milioni di copie in vent'anni.

**Una nota di metodo sulla fonte più grande.** `choose-your-own-adventure.txt` dichiara che nella serie **non c'è nessuno schema riconoscibile** né nel numero di pagine per finale, né nel rapporto fra finali buoni e cattivi, né nel modo in cui il lettore si muove avanti e indietro nelle pagine, e attribuisce a questo «un senso realistico di imprevedibilità». **È una fonte che dichiara l'assenza di una regolarità invece di inventarne una**, e questo la rende più affidabile di quanto sarebbe se ne avesse trovata una.

## Esempi trovati

*Choose Your Own Adventure*: 184 titoli fra il 1979 e il 1998, oltre 250 milioni di copie, 40 lingue, da 44 finali nei primi titoli a 7 negli ultimi.

*Inside UFO 54-40*, dove esiste un finale — il pianeta paradiso — **che non si può raggiungere con nessuna sequenza di scelte**, e a cui si arriva solo barando o girando pagina per sbaglio. L'unico modo di uscirne è chiudere il libro e ricominciare.

*Lucky Les*, 1967, che si dichiarava «un gioco in forma di libro».

*Tante storie per giocare* di Gianni Rodari, 1971.

I manuali *TutorText*, dalla fine degli anni Cinquanta: risposta giusta, si va avanti; risposta sbagliata, si riceve una spiegazione e si sceglie di nuovo.

*Buffalo Castle*, 1975, primo modulo che unisce una narrazione a bivi a un regolamento di gioco di ruolo, e che permetteva di giocare **senza un arbitro**.

*428: Shibuya Scramble*, 2008, con un massimo di 85 finali, dove si alternano i punti di vista di più personaggi e le scelte di uno hanno conseguenze per un altro.

Le avventure grafiche che si biforcano e poi riconvergono su un evento inevitabile, che `nonlinear-gameplay.txt` descrive come il compromesso più diffuso.

## Una nostra versione

**Questa è la voce che il formato regge meglio di tutto il capitolo, e la glossa dell'elenco lo dice già: «è quello che questo formato già fa».** Un foglio stampato con dei bivi non chiede né orologio né registro; chiede soltanto carta. Il limite vero è un altro e si conta: **la carta costa**, e un albero pieno raddoppia a ogni bivio. Su un A4 non ci stanno sessantatré paragrafi.

> **Il foglio che si legge in sei modi**
>
> Questo foglio ha sedici riquadri numerati. Comincia dal **1** e finisci quando arrivi a un riquadro che non manda da nessuna parte.
>
> ```
>   ┌────┬────┬────┬────┐
>   │  1 │  2 │  3 │  4 │
>   ├────┼────┼────┼────┤
>   │  5 │  6 │  7 │  8 │
>   ├────┼────┼────┼────┤
>   │  9 │ 10 │ 11 │ 12 │
>   ├────┼────┼────┼────┤
>   │ 13 │ 14 │ 15 │ 16 │
>   └────┴────┴────┴────┘
> ```
>
> Adesso il conto, e riguarda questo foglio. Immagina di volerlo fare **con cinque bivi veri**, dove ogni strada resta separata fino in fondo.
>
> ```
>   1 bivio    ──►   2 finali,  3 riquadri
>   2 bivi     ──►   4 finali,  7 riquadri
>   3 bivi     ──►   8 finali, 15 riquadri
>   4 bivi     ──►  ────────── , ────────── riquadri
>   5 bivi     ──►  ────────── , ────────── riquadri
> ```
>
> **Riempi le quattro caselle. Poi di' quanti riquadri di quel foglio leggeresti in una volta sola, e che frazione del foglio e'.**
>
> E infine la domanda che decide la forma: **c'e' un modo di avere sei finali diversi scrivendo solo undici riquadri?** C'e', ed e' questo: non contare quale strada hai fatto, conta **quante volte hai scelto la porta di sinistra.** Cinque bivi, sei totali possibili — da zero a cinque — e sei finali.
>
> Provalo: torna sui tuoi passi, cambia una sola scelta, e guarda se il totale cambia. **Cambia sempre.**

Il conto è la forma: chi lo fa scopre che l'albero pieno costa sessantatré riquadri e ne fa leggere sei, e che la stessa carta spesa in modo diverso dà sei finali con undici. La verifica finale — cambiare una scelta e vedere che il totale cambia sempre — è la stessa della voce 268, scelta con conseguenza vista dal lato della struttura invece che del nodo.

**Dove si rompe.** Si rompe sulla carta e sul dito. Sulla carta: un albero pieno di cinque bivi non ci sta su un foglio, e già a quattro è scomodo; la numerazione mescolata dei libri-gioco esiste proprio per questo, e su una pagina sola non si può mescolare granché. Sul dito: **niente impedisce di leggere tutti i riquadri**, e un ramo che si vede non è un ramo perso. Nascondere richiede una piega o una busta — si veda la voce 43, taglio — e ogni piega è una cosa in più che qualcuno deve fare a mano.

## Da riprendere alla rassegna

**L'albero pieno è la struttura più cara e meno vista di tutte, e i due numeri stanno insieme.** Sessantatré paragrafi per farne leggere sei: **il 90% di quello che si scrive non viene letto**, e per farlo leggere tutto servirebbero, con finali equiprobabili, centonovantadue letture su un libro da quarantaquattro finali. **Nessuna delle fonti mette questi due fatti nella stessa frase**, e per un progetto che stampa fogli è la prima cosa da guardare.

**La struttura a somma è il modo di avere bivi senza pagare l'albero**, e vale per tutto quello che il progetto potrebbe stampare: undici paragrafi, sei finali, ogni scelta che conta sempre. Confermata dal lato del peso alla voce 268, scelta con conseguenza e dal lato del costo qui. **Da provare come struttura predefinita per qualunque foglio a bivi.**

**Il vero antenato della forma è didattico e non narrativo, e questo cambia come la si guarda.** L'istruzione programmata dei manuali *TutorText* — risposta giusta, avanti; risposta sbagliata, spiegazione e si riprova — è la stessa struttura del libro-gioco, arrivata vent'anni prima e con un altro scopo. **Il ramo sbagliato lì non era un finale: era una correzione**, e nessuna delle forme del capitolo 8 che riguardano l'errore lo ha incontrato per questa strada. Si accosta alla voce 231, impalcatura (scaffolding) e alla voce 243, effetto test (retrieval practice).

**Esiste un finale che non si può raggiungere scegliendo, ed è stampato nel libro.** Il pianeta paradiso di *Inside UFO 54-40* si trova solo barando o sbagliando pagina. **Alla rassegna vale come domanda aperta e non come modello**: una cosa che sta nel foglio e a cui nessun percorso legittimo porta è una forma di contenuto che nessuna delle duecentosessantanove voci scritte finora contempla.
