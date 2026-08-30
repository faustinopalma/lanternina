# Sudoku e affini (Nikoli)

- **Numero** 154 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi logici»
- **Si chiama anche** Number Place, *sūji wa dokushin ni kagiru*, sudoku, giochi Nikoli, puzzle logici senza lingua, *pencil puzzles*, *culture independent puzzles*
- **In una riga** Slitherlink, Kakuro, Nurikabe, Masyu, Hitori, Fillomino, Hashiwokakero, Heyawake, Light Up, Number Link, Shikaku.
- **Fonti** `sudoku.txt`, `mathematics-of-sudoku.txt`, `nikoli-publisher.txt`, `nikoli-puzzle-types.txt` — questi ultimi due sono la stessa pagina — e `logic-puzzle.txt`, prese il 30 agosto 2026 da en.wikipedia; `it-sudoku.txt`, stessa data, da it.wikipedia; il conto delle 288 griglie 4×4 è nostro
- **Stato della ricerca** fatta, 30 agosto 2026

## Che cos'è

Una griglia parzialmente riempita e una regola breve. Si completa la griglia in modo che la regola valga dappertutto, e **il modo di farlo è uno solo.**

Qui il capitolo cambia asse per l'ultima volta. Nelle prime quattro voci del blocco c'era un testo da ragionare; **da qui in poi non c'è nessun testo.** La differenza rispetto alla voce 142, puzzle a griglia (chi beve cosa, chi vive dove) è netta e la dichiara la fonte stessa, che è l'editore di questi giochi: Nikoli è nota, dice la pagina, per una biblioteca di giochi «indipendenti dalla cultura», e porta come esempio contrario proprio il cruciverba, «che si appoggia a una lingua e a un alfabeto specifici». **Là ci sono le parole; qui no**, e un sudoku si consegna identico in qualunque lingua senza tradurre niente. `logic-puzzle.txt` li mette nella stessa famiglia — enigmi di deduzione — e distingue quelli «completamente non verbali», elencando sudoku, nonogrammi e labirinti logici.

Parti mobili:

- **La regola.** Nel sudoku è una riga sola: ogni riga, ogni colonna e ogni riquadro contengono tutte le cifre una volta.
- **Che cosa si scrive nelle caselle.** Cifre, caselle nere, tratti, ponti, lampadine. Le cifre del sudoku non sono numeri: sono nove simboli distinti, e si potrebbero sostituire con nove colori senza cambiare niente.
- **Quanti indizi si danno.** È la manopola della difficoltà, e ha un minimo dimostrato.
- **Dove stanno gli indizi.** Nikoli impose la simmetria rotazionale: gli indizi disposti in modo che la griglia ruotata di mezzo giro abbia gli indizi negli stessi posti.
- **Se la soluzione è unica.** Non è un dettaglio di qualità: **è la definizione.** Un sudoku con due soluzioni non è un sudoku difficile, è rotto, e chi lo risolve non ha modo di saperlo.

## Da dove viene

La discendenza ha tre gradini, e le due pagine lette non la raccontano allo stesso modo.

Il primo gradino sono i **quadrati magici svuotati.** Nell'Ottocento gli enigmisti francesi cominciarono a togliere numeri dai quadrati magici. *Le Siècle*, quotidiano di Parigi, pubblica il **19 novembre 1892** un quadrato magico 9×9 con sottoquadrati 3×3 parzialmente completato — non era un sudoku, perché conteneva numeri a due cifre e si risolveva con l'aritmetica invece che con la logica. Il **6 luglio 1895** il rivale *La France* lo raffina in qualcosa che è quasi un sudoku moderno e lo chiama *carré magique diabolique*: righe, colonne e diagonali spezzate contengono solo i numeri da 1 a 9, i sottoquadrati non sono segnati ma contengono comunque 1-9, e **il vincolo in più sulle diagonali porta a una soluzione unica.** Questi giochi settimanali durano una decina d'anni sui giornali francesi e spariscono intorno alla prima guerra mondiale.

Il secondo gradino è **Howard Garns**, architetto in pensione di Connersville, Indiana, settantaquattrenne, che disegna anonimamente il sudoku moderno e lo pubblica nel **1979** su Dell Magazines con il nome *Number Place*. Il modo in cui è stato identificato è un ragionamento e vale la pena riportarlo: **il suo nome era sempre nell'elenco dei collaboratori nei numeri che contenevano Number Place e sempre assente da quelli che non lo contenevano.** Garns muore nel 1989 senza vedere che cosa era diventato.

Il terzo è il Giappone. **Maki Kaji**, presidente della Nikoli, lo introduce sul *Monthly Nikolist* nell'**aprile 1984** con il nome *Sūji wa dokushin ni kagiru*, «le cifre devono essere solitarie» — in giapponese *dokushin* vuol dire celibe. Il nome viene poi abbreviato prendendo il primo kanji di ciascuna delle due parole: *sudoku*. Nel **1986** Nikoli introduce le due innovazioni che fanno il gioco come lo conosciamo: **non più di 32 indizi**, e **indizi disposti in modo simmetrico.**

Fuori dal Giappone arriva grazie a **Wayne Gould**, che nel 1997 vede un sudoku parzialmente risolto in una libreria giapponese e passa sei anni a scrivere un programma che ne produca in fretta di nuovi con soluzione unica. Il primo giornale non giapponese a pubblicarne uno è il *Conway Daily Sun* del New Hampshire, nel **settembre 2004**; il *Times* di Londra a novembre. Gould li offriva gratis in cambio della citazione e di un collegamento al suo sito.

Il nome della casa editrice, per inciso, è quello di un cavallo: **Nikoli** vinse le Irish 2 000 Guineas nel 1980, e Maki Kaji amava le corse.

## Varianti e parenti

- **I giochi Nikoli** — la fonte ne elenca decine con i nomi giapponesi: Slitherlink, Kakuro, Nurikabe, Masyu, Hitori, Fillomino, Hashiwokakero (i ponti), Heyawake, Light Up (*bijutsukan*, il museo), Numberlink, Shikaku, LITS, Kuromasu, Country Road, Goishi Hiroi. **Ognuno ha una regola diversa e la stessa struttura**: griglia, regola breve, soluzione unica.
- **Sudoku di altre dimensioni** — 4×4 con riquadri 2×2, 6×6, 16×16.
- **Sudoku a incastro (*jigsaw*)** — i riquadri non sono quadrati. La fonte segnala un fatto che sembra un dettaglio e non lo è: per lati primi e maggiori di 3, **certe suddivisioni non ammettono nessuna soluzione**, quindi esistono griglie a incastro su cui nessun sudoku è costruibile.
- **Sudoku killer** — con somme dichiarate su gruppi di caselle. È il ponte con la voce 361, crittarismo (alfametica).
- **Greater Than Sudoku** — al posto degli indizi, dodici segni di maggiore e minore fra caselle adiacenti.
- **Clueless Sudoku** — nove sudoku disposti in quadrato, e le nove caselle centrali formano un decimo sudoku senza nessun indizio.
- **Voce 142, puzzle a griglia (chi beve cosa, chi vive dove)** — il vicino diretto, e il confine è la lingua.
- **Voce 155, nonogramma / picross** — l'altra griglia senza lingua di questo blocco, e la differenza è che là il risultato è un disegno.
- **Voce 128, crucipuzzle (word search)** — l'altra griglia dell'elenco in cui si cerca dentro una tabella, con le lettere.
- **Voce 362, quadrato magico** — l'antenato diretto, nel capitolo 13, giochi matematici e ricreativi. Là si somma, qui no: **il sudoku è quello che resta di un quadrato magico quando si toglie l'aritmetica.**
- **Voce 361, crittarismo (alfametica)** — sempre nel capitolo 13, ed è il caso in cui la griglia chiede un conto.

Il confine con il capitolo 13 è quello già fissato: **là stanno i problemi che chiedono un'idea matematica, qui la forma di pagina.** Il sudoku non chiede nessuna idea matematica — chiede di tenere il conto di quello che è escluso — e per questo sta di qua, anche se la matematica che se ne è fatta è parecchia. Con il capitolo 12, giochi di parole e enigmistica italiana non c'è nessun contatto, ed è il caso più netto del blocco: questa forma esiste **apposta** per non averlo.

## Che cosa se ne sa

**Il minimo di indizi è 17, ed è stato dimostrato per esaurimento nel 2014.** Gary McGuire, Bastian Tugemann e Gilles Civario provarono, con una ricerca esaustiva al calcolatore basata sull'enumerazione degli insiemi trasversali, che nessun sudoku con soluzione unica può avere meno di 17 indizi. Se ne conoscono decine di migliaia con esattamente 17. **È il numero più utile della voce, ed è anche un esempio di quello che è costato ottenerlo**: la risposta a «quanti bastano» è un teorema dimostrato al calcolatore trentacinque anni dopo l'invenzione del gioco.

**C'è un secondo vincolo sugli indizi, e si dimostra in una riga.** Gli indizi di un sudoku ben posto devono contenere **almeno otto delle nove cifre**, perché se due cifre non compaiono affatto si possono scambiare in tutta la soluzione e ottenerne una seconda. La regola generale che la fonte dà è: un sudoku *n*²×*n*² deve usare almeno *n*²−1 cifre distinte fra gli indizi. **Per un 4×4 questo vuol dire almeno tre cifre su quattro** — la conseguenza è nostra, la regola è della fonte — ed è un controllo che costa un'occhiata e non richiede di risolvere niente.

**Le griglie complete sono 6 670 903 752 021 072 936 960**, cioè circa 6,67 × 10²¹. Tenendo conto delle simmetrie — rotazioni, riflessioni, permutazioni, rietichettature — le soluzioni **essenzialmente diverse** sono 5 472 730 538. Il rapporto fra i due numeri è la cosa interessante: **quasi tutta quella quantità è ripetizione.**

**Il numero dei sudoku minimi non si conosce.** Un sudoku minimo è uno da cui non si può togliere nessun indizio senza perdere l'unicità. La fonte dice che il loro numero è noto solo per stima statistica — circa 3,10 × 10³⁷, con un errore relativo dello 0,065% —, il che è una cosa che vale la pena notare: **si conosce esattamente il numero delle soluzioni e solo per stima il numero dei problemi.** È la stessa asimmetria fra risolvere e produrre già raccolta tre volte, qui in forma numerica.

**Risolvere un sudoku generale è NP-completo**, per griglie *n*²×*n*² qualsiasi. Per il 9×9 gli algoritmi a forza bruta con ritorno all'indietro e i *dancing links* bastano; crescendo *n* esplode. Il sudoku si può anche esprimere come un problema di colorazione di grafo: costruire una 9-colorazione, data una 9-colorazione parziale.

**Le simmetrie sono rare.** Ci sono 26 tipi di simmetria possibili per una griglia piena, ma si trovano **in circa lo 0,005% delle griglie**. La simmetria che Nikoli impose agli indizi nel 1986 è quindi una scelta editoriale su una popolazione che non ce l'ha quasi mai.

**Sull'origine le due pagine si contraddicono, e scarto quella italiana.** `it-sudoku.txt` apre dicendo che «il gioco fu inventato dal matematico svizzero Eulero da Basilea (1707-1783)». La pagina inglese non nomina Euler da nessuna parte nella storia del gioco, e attribuisce con date primarie: i giornali francesi del 1892 e del 1895, Garns nel 1979, Nikoli nel 1984. **Tengo la seconda.** Euler studiò i quadrati latini, che sono un altro oggetto — una griglia latina non ha il vincolo dei riquadri, che è precisamente quello che rende un sudoku un sudoku. Le due pagine divergono anche su Wayne Gould, che per la pagina inglese è un giudice di Hong Kong e per quella italiana un ex giudice neozelandese: **va verificato**, e nessuna delle due dà una fonte per questo dettaglio.

**Un dato di diffusione che l'unica pagina italiana aggiunge:** nel 2005 «sudoku» fu eletta parola dell'anno dalla Oxford University Press.

**Nessuna misura su chi risolve.** In nessuna delle pagine lette c'è un dato su quanto ci si metta, a che età si cominci, o che effetto faccia. C'è invece una quantità di matematica sul gioco, che è esattamente il rovescio della situazione della maggior parte delle voci di questo capitolo.

## Esempi trovati

Da *Le Siècle*, 19 novembre 1892: il quadrato magico svuotato che non era ancora un sudoku.

Da *La France*, 6 luglio 1895: il *carré magique diabolique*, con i sottoquadrati non segnati ma già presenti.

Da Dell Magazines, 1979: *Number Place*, senza il nome dell'autore in copertina.

Dal *Monthly Nikolist*, aprile 1984: *le cifre devono essere solitarie*.

Dal catalogo Nikoli, i nomi giapponesi che dicono la regola: *hashi o kakero*, «costruisci i ponti»; *kuromasu wa dokoda*, «dove sono le caselle nere»; *bijutsukan*, «il museo», per il gioco che in inglese si chiama Light Up; *hitori ni shitekure*, «lasciami solo». **È la stessa economia già osservata alla voce 311, zeppa: il titolo è metà della consegna**, e qui succede in una lingua sola.

Dal Clueless Sudoku: nove griglie che ne formano una decima senza nessun indizio.

## Una nostra versione

Il sudoku 9×9 non si può costruire a mano con la garanzia dell'unicità, e il sistema che stampa questi fogli non è affidabile a farlo. Il 4×4 sì, e con il 4×4 si può fare la cosa che il 9×9 non permette: **costruirne uno e dimostrare da soli che ha una soluzione sola.**

> **Fabbricare un sudoku**
>
> Un sudoku piccolo: quattro righe, quattro colonne, quattro riquadri da due per due. Le cifre sono 1, 2, 3, 4. La regola è una sola:
>
> ```
>  in ogni riga, in ogni colonna e in ogni riquadro
>  ci sono 1, 2, 3 e 4, ognuno una volta sola.
> ```
>
> **Primo: riempi una griglia intera.** Tutte e sedici le caselle, senza buchi, rispettando la regola.
>
> ```
>   ┌────┬────┰────┬────┐
>   │    │    ┃    │    │
>   ├────┼────╂────┼────┤
>   │    │    ┃    │    │
>   ┝━━━━┿━━━━╋━━━━┿━━━━┥
>   │    │    ┃    │    │
>   ├────┼────╂────┼────┤
>   │    │    ┃    │    │
>   └────┴────┸────┴────┘
> ```
>
> I modi di riempirla sono **288**. Ne hai scelto uno, e adesso è la soluzione del gioco che stai per costruire.
>
> **Secondo: ricopiala qui, e poi comincia a cancellare.**
>
> ```
>   ┌────┬────┰────┬────┐        ┌────┬────┰────┬────┐
>   │    │    ┃    │    │        │    │    ┃    │    │
>   ├────┼────╂────┼────┤        ├────┼────╂────┼────┤
>   │    │    ┃    │    │        │    │    ┃    │    │
>   ┝━━━━┿━━━━╋━━━━┿━━━━┥        ┝━━━━┿━━━━╋━━━━┿━━━━┥
>   │    │    ┃    │    │        │    │    ┃    │    │
>   ├────┼────╂────┼────┤        ├────┼────╂────┼────┤
>   │    │    ┃    │    │        │    │    ┃    │    │
>   └────┴────┸────┴────┘        └────┴────┸────┴────┘
> ```
>
> **Una cancellazione per volta**, e dopo ognuna fai questa prova, che non richiede di fidarsi di nessuno:
>
> ```
>  Riparti dalla griglia bucata come se non l'avessi
>  fatta tu. Riempi solo le caselle in cui entra
>  UNA SOLA cifra. Poi rileggi e riempi le nuove.
>  Vai avanti finche' puoi.
>
>  - se arrivi in fondo, la cancellazione va bene:
>    il gioco ha ancora una soluzione sola;
>  - se ti blocchi, rimetti l'ultima cifra che hai
>    tolto e prova a toglierne un'altra.
> ```
>
> **Terzo: un controllo gratis, prima ancora di cominciare.** Guarda le cifre che ti sono rimaste negli indizi. **Se ne mancano due** — se per esempio nel gioco non compare nessun 2 e nessun 4 — il gioco è rotto, e non c'è bisogno di provarlo: chi lo risolve può scambiare quelle due cifre in tutta la soluzione e ottenerne una seconda, altrettanto valida. Fra gli indizi ne devono comparire **almeno tre su quattro**.
>
> **Quarto: quanti riesci a toglierne?**
>
> ```
>  indizi rimasti nel mio gioco:  ────
> ```
>
> Per il sudoku grande, quello da nove per nove, il minimo è **diciassette**, ed è stato dimostrato nel 2014 con una ricerca esaustiva al calcolatore. Per il quattro per quattro il minimo non te lo dico, perché non lo so: **trovarlo è il gioco.**
>
> **Quinto, se ti va:** ricopia solo la griglia bucata su un foglio pulito e dalla a qualcuno. Tu la soluzione ce l'hai.

**Il conto delle 288 griglie è nostro** e si rifà così: la prima riga si può scrivere in 24 modi; fissata quella, la seconda in 4; e le ultime due righe in 4 oppure in 2 a seconda di quale seconda riga si è scelta — 4 per le due seconde righe che sono la prima riga «ruotata di due», 2 per le altre due. Fa 24 × (4+2+2+4) = 288. Le due enumerazioni delle ultime due righe sono state fatte a mano, caso per caso, e le altre due ricavate per simmetria.

La procedura di cancellazione è **la settima via d'uscita già raccolta — la procedura che non richiede fiducia — applicata a un problema che di solito ne richiede molta.** Chi costruisce un sudoku deve garantire l'unicità della soluzione, che è un'affermazione universale; qui non la garantisce dimostrandola, la garantisce **costruendola**, perché una griglia che si riempie con la regola «entra una sola cifra» ha per forza una sola soluzione. Il controllo si fa a matita e il foglio non deve sapere niente.

Il controllo delle cifre mancanti è il pezzo migliore, perché **costa un'occhiata e taglia via un guasto invisibile.** Un sudoku a cui mancano due cifre fra gli indizi sembra un sudoku normale, si risolve, e chi lo risolve arriva a una risposta che non è quella che l'autore aveva in mente — senza mai accorgersi che ce n'era un'altra. È la stessa famiglia dei fallimenti in silenzio già raccolta alle voci 113, 128 e 144.

Il limite tecnico va scritto qui e non nel foglio: **il sistema che stampa non può costruire un sudoku 9×9 con soluzione unica e non può verificarne uno.** Non per il limite sulle lettere — qui di lettere non ce ne sono — ma perché l'unicità è un'affermazione su tutte le griglie possibili. Il 4×4 aggira il problema spostandolo: **non lo risolve la macchina, lo risolve la procedura in mano a chi costruisce.**

Sul pannello da quattro righe da 44 caratteri una griglia 4×4 ci starebbe — quattro righe da nove caratteri — ma non ci sta la cornice dei riquadri, e senza quella la regola non si vede. È un caso in cui il pannello ha lo spazio e non ha il disegno.

## Da riprendere alla rassegna

**Esiste una famiglia intera di giochi progettata per non dipendere da nessuna lingua, e ha un editore e una data.** Nikoli, 1980, con il criterio dichiarato dei giochi «indipendenti dalla cultura». Per un sistema che stampa fogli in italiano a una persona sola, **è l'unica famiglia dell'elenco che non porta con sé il contesto in cui è nata** — che è il modo più comune di sbagliare secondo il contratto di questa enciclopedia. Da guardare per intero: sono decine di giochi, tutti con la stessa struttura, e nessuno chiede di sapere niente.

**Il nome giapponese è la regola.** *Costruisci i ponti*, *dove sono le caselle nere*, *lasciami solo*. È la stessa economia raccolta alla voce 311, zeppa per l'enigmistica italiana, e qui è sistematica invece che occasionale. **Un catalogo di giochi in cui ogni titolo è la consegna** è una cosa che l'elenco non ha, e costa quanto scegliere bene i nomi.

**L'unicità della soluzione è la definizione, non la qualità.** In quasi tutte le altre forme dell'elenco una seconda soluzione è un difetto di redazione; qui è la fine del gioco, e non si vede. **Da elencare tutte le forme dell'elenco che hanno questa proprietà**, perché sono quelle in cui un sistema che genera senza verificare fa il danno più grande.

**Il costo di produrre e il costo di risolvere, quarta conferma, e stavolta con i numeri.** Le griglie piene sono 6,67 × 10²¹ e si contano esattamente; i problemi minimi si stimano a 3,10 × 10³⁷ con lo 0,065% di errore, e non si contano. Il minimo di indizi è 17 e ci sono voluti trentacinque anni e una ricerca esaustiva al calcolatore. **Risolvere è un pomeriggio, produrre è un articolo del 2014**, e nel resto dell'elenco la stessa distanza c'è ma non è mai stata misurabile così.

**Un vincolo che si controlla senza risolvere.** «Fra gli indizi devono comparire almeno *n*²−1 cifre distinte» è un controllo di validità che costa un'occhiata e che non richiede di sapere la soluzione. È l'unica cosa del genere incontrata, e vale la pena cercare, per ogni forma dell'elenco che debba garantire qualcosa, **se esista un controllo necessario e a costo zero** da mettere accanto a quello vero.

**Due pagine si contraddicono sull'inventore, e la versione più bella è quella falsa.** «Inventato da Eulero» è una frase memorabile e non regge davanti alle date della pagina inglese. È il quarto caso in due blocchi — con il professor Zapp, le griglie di Fleissner e l'enigma di Einstein — e la regolarità comincia a essere un dato: **le attribuzioni sbagliate vanno tutte verso un nome più grande.**
