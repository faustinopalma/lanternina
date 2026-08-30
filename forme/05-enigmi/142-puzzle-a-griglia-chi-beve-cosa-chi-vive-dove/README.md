# Puzzle a griglia (chi beve cosa, chi vive dove)

- **Numero** 142 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi logici»
- **Si chiama anche** puzzle della zebra, enigma di Einstein, *zebra puzzle*, *logic grid puzzle*, *Einstein's riddle*, puzzle delle cinque case, puzzle a matrice, *table puzzle*
- **In una riga** una tabella di persone, cose e attributi, e un elenco di indizi che la riempie in un modo solo.
- **Fonti** `zebra-puzzle.txt` e `logic-puzzle.txt`, prese il 30 agosto 2026 da en.wikipedia
- **Stato della ricerca** fatta, 30 agosto 2026

## Che cos'è

Ci sono cinque case, cinque persone, cinque bevande, cinque animali. Ogni persona ha una cosa sola di ogni categoria e nessuna cosa è condivisa. Poi c'è un elenco di indizi — «lo spagnolo ha il cane», «il latte si beve nella casa di mezzo» — e da lì si arriva a una sola disposizione possibile.

Non c'è niente da riconoscere e niente da capire di traverso. È deduzione pura su una tabella, e questa voce sta a sé nel capitolo: le sette che la precedono nascondono qualcosa, le quattro che la seguono chiedono di raggiungere una configurazione. Qui non c'è nessun nascondiglio e non c'è nessuna mossa: c'è una griglia da riempire.

Parti mobili:

- **Quante categorie.** `logic-puzzle.txt` dice che possono essere un numero qualunque, ma che la complessità cresce di conseguenza, e che quasi tutti ne hanno **due, tre o al massimo quattro.** Il puzzle della zebra ne ha cinque, ed è per questo che è il caso celebre.
- **Quanti elementi per categoria.** Tre è un gioco da cinque minuti, cinque è mezz'ora.
- **Che tipo di indizio.** Diretto («l'inglese sta nella casa rossa»), negativo («né Misty né Rex è il pastore tedesco»), posizionale («la casa verde è subito a destra di quella avorio»), di adiacenza («accanto alla casa dove sta il cavallo»).
- **Se la griglia è data.** Nei *table puzzle* non c'è: al suo posto c'è una piantina, o niente, e chi risolve deve inventarsi come tenere il conto.
- **Se la domanda finale è tutta la tabella o una casella.** Il puzzle della zebra chiede due cose sole — chi beve l'acqua e chi possiede la zebra — ma per rispondere bisogna riempire tutto.

## Da dove viene

Il gioco a matrice come lo si conosce discende dai sillogismi. `logic-puzzle.txt` fa risalire il primo enigma logico a **Charles Lutwidge Dodgson**, cioè Lewis Carroll, e al suo *The Game of Logic*, dove si dimostra «alcuni levrieri non sono grassi» partendo da «nessuna creatura grassa corre bene» e «alcuni levrieri corrono bene». Dodgson arriva poi a costruire enigmi con **fino a otto premesse.**

Nella seconda metà del Novecento **Raymond Smullyan** allarga il ramo con *The Lady or the Tiger?*, *To Mock a Mockingbird* e *Alice in Puzzle-Land*, e rende popolari i cavalieri e i furfanti, che sono la voce 147, enigma di verità e menzogna.

La versione a griglia ha una data e un luogo precisi. Il puzzle della zebra compare su **Life International del 17 dicembre 1962**, con cinque case, cinque nazionalità, cinque bevande, cinque animali e cinque marche di sigarette. Il numero del **25 marzo 1963** pubblicò la soluzione e i nomi di **diverse centinaia di solutori** da tutto il mondo.

L'attribuzione popolare è falsa, e la fonte lo dice con l'argomento che la chiude: il puzzle è spesso chiamato «enigma di Einstein» perché una leggenda urbana vuole che lo abbia inventato da ragazzo, e a volte è attribuito a Lewis Carroll. Non c'è nessuna prova né per l'uno né per l'altro, e **la versione di Life nomina marche di sigarette che non esistevano né ai tempi di Carroll né nell'infanzia di Einstein.** È il terzo caso di attribuzione sbagliata incontrato in questo blocco, dopo il professor Zapp della voce 139, testo troppo piccolo / troppo grande e la griglia di Fleissner della voce 141, griglia di Cardano.

## Varianti e parenti

- **Puzzle a griglia con matrice** — la forma da rivista: si stampa la matrice, si segnano × e ✓, e la deduzione si propaga da sola.
- **Table puzzle** — la stessa deduzione senza matrice, perché sarebbe troppo grande o perché c'è un altro aiuto visivo. `logic-puzzle.txt` fa l'esempio della piantina di un paese al posto della griglia, in un enigma sulla posizione dei negozi.
- **Sillogismo** — l'antenato: due premesse e una conclusione. Il *Game of Logic* di Carroll ne fa un gioco da tavolo con dei gettoni.
- **Voce 147, enigma di verità e menzogna** — la stessa deduzione, ma con l'affidabilità di chi parla come variabile in più.
- **Voce 154, sudoku e affini (Nikoli)** — la stessa struttura senza parole: `logic-puzzle.txt` li mette esplicitamente nella stessa famiglia, insieme ai nonogrammi e ai labirinti logici.
- **Voce 155, nonogramma / picross** — deduzione su griglia il cui esito è un disegno.
- **Voce 60, dedurre** — il verbo di cui questa è la forma-oggetto.
- **Voce 39, tabella** — la forma di pagina che la contiene. È l'unico caso in cui la tabella non è il modo di rispondere ma il luogo del ragionamento.
- **Voce 360, rompicapo classico** — nel capitolo 13. Il confine con i giochi matematici va dichiarato, e passa di qui: **quel capitolo raccoglie i problemi che chiedono un'idea matematica — parità, cassetti, grafi —, mentre questo puzzle non chiede nessuna matematica e nessuna idea. Chiede di tenere il conto senza sbagliare.** Il capitolo 13 è ancora tutto da fare, e quando si scriverà questa distinzione va rifatta da lì.

## Che cosa se ne sa

**È un problema di soddisfacimento di vincoli, ed è usato come metro.** La pagina lo dichiara due volte: il puzzle della zebra è stato usato come banco di prova per gli algoritmi che risolvono problemi di soddisfacimento di vincoli — c'è un articolo di Prosser del 1993 sugli algoritmi ibridi — e, **più di recente, come banco di prova per la capacità di ragionamento logico dei modelli linguistici di grandi dimensioni** (Lin e altri, *ZebraLogic: On the Scaling Limits of LLMs for Logical Reasoning*, arXiv 2502.01100, luglio 2025). Il titolo dice già l'esito. Per noi questo è il dato tecnico che conta: **la macchina che stampa i nostri fogli non è affidabile né a risolvere questi enigmi né a costruirli**, e non per il limite sulle lettere ma per un limite diverso e documentato.

**Il costo di produrre e il costo di risolvere divergono, e qui più che altrove.** Risolverne uno da cinque categorie è mezz'ora di attenzione senza nessuna idea difficile. Costruire un elenco di indizi che ammetta **esattamente una** soluzione è un problema di soddisfacimento di vincoli, cioè la stessa cosa che serve a risolverlo, presa dal lato peggiore: bisogna dimostrare che non ce ne siano altre. È la stessa osservazione già lasciata dalla voce 125, cruciverba sui cruciverba costruiti da un programma dal 1976, e qui vale in forma più netta perché il problema ha un nome.

**Il numero di indizi giusto non è ovvio, e c'è chi se l'è chiesto per iscritto.** Fra i riferimenti della pagina compare una comunicazione a una conferenza del 2009 intitolata *Is Einstein's Puzzle Over-Specified?* — l'enigma di Einstein è sovraspecificato? Della comunicazione ho **solo il titolo**, riportato nella bibliografia della fonte, e non l'ho letta: quindi non so quale sia la risposta. Ma la domanda è quella giusta, e riguarda direttamente chi costruisce: **un indizio in meno e le soluzioni sono molte, uno in più e non serve a niente**, e chi scrive gli indizi non ha modo di accorgersene guardandoli.

**La soluzione si costruisce a pezzi, e la fonte mostra come.** Per l'indizio 10 il norvegese sta nella prima casa; per il 15 la seconda è blu; quindi la casa del norvegese non è blu, né rossa dove sta l'inglese, né verde o avorio che sono adiacenti fra loro. Dev'essere gialla, e quindi il norvegese fuma Kools. **Quattro esclusioni e una conclusione**, e da lì il resto scende. È esattamente il verbo della voce 59, escludere, e mostra che la difficoltà non sta in nessun passo: sta nel non perdere il filo fra un passo e l'altro.

**Il contenuto è arbitrario, e la fonte lo dichiara.** Le altre versioni cambiano colori, nazionalità, marche, bevande e animali, e questo non cambia la logica del puzzle. Ne segue una proprietà utile: **quando gli elementi di una categoria non dicono niente a chi risolve, la tabella funziona lo stesso.** Le cinque marche di sigarette americane del 1962 oggi non le riconosce nessuno, e il gioco regge.

**Nessuna delle due fonti misura niente su chi risolve.** Non c'è un dato su quanto tempo ci voglia, su quanti ci riescano, su che età. Le diverse centinaia di solutori pubblicate da Life nel 1963 sono l'unico numero disponibile, e non è un numero: è un elenco di nomi, e dice solo che almeno quelli ce l'hanno fatta.

## Esempi trovati

Da Life International, 17 dicembre 1962: quindici indizi, cinque categorie, e due domande in fondo — chi beve l'acqua, chi possiede la zebra. Il testo aggiunge in nota che le case sono di colori diversi, gli abitanti di nazionalità diverse, e che nell'indizio 6 «destra» vuol dire la vostra destra. **Quella nota è metà della consegna**, e senza si può risolvere un puzzle diverso.

Da alcune versioni successive: la casa verde è a *sinistra* di quella avorio invece che a destra. La logica è la stessa, la soluzione no.

Da Lewis Carroll: i levrieri che non sono grassi, e otto premesse.

Dalle riviste di enigmistica: la matrice stampata accanto agli indizi, con le crocette da segnare.

Da *Dishonored 2*: una versione semplificata del puzzle della zebra è un cancello, e non si passa finché non si risolve. È la voce 179, chiave nascosta con una serratura logica invece che meccanica.

## Una nostra versione

Il sistema può stampare la matrice vuota e le regole della notazione, e non può costruire l'elenco di indizi: garantire che la soluzione sia una sola è un problema di soddisfacimento di vincoli, e il modello che stampa questi fogli è misurato male proprio su questo. Quindi si gira il compito, e la cosa da costruire diventa il gioco.

> **Fabbricane uno che funzioni**
>
> Prima un esempio già risolto, così vedi come è fatto.
>
> > Ada, Bruno e Carla. Uno beve tè, uno latte, uno succo. Uno sta in cucina, uno sul balcone, uno sul divano.
> >
> > 1. Chi beve il latte sta sul divano.
> > 2. Ada non beve latte e non beve succo.
> > 3. Carla sta in cucina.
> >
> > Dal 2, Ada beve tè. Dal 3, Carla è in cucina, quindi non è lei sul divano, quindi per l'1 non è lei a bere il latte. Resta Bruno, sul divano. A Carla il succo. Ad Ada il balcone. **Una sola disposizione, e non ce ne sono altre.**
> >
> > Adesso togli l'indizio 3 e riprova: le disposizioni possibili diventano più di una. Trovane due.
>
> Tocca a te. Scegli tre persone che conosci e due categorie di cose — quello che vuoi: che scarpe hanno, dove si siedono a tavola, che musica ascoltano. **Prima riempi la tabella con la verità**, poi coprila.
>
> ```
>              ────────────    ────────────
>  ──────────  ────────────    ────────────
>  ──────────  ────────────    ────────────
>  ──────────  ────────────    ────────────
> ```
>
> Poi scrivi gli indizi. Il difficile non è scriverli: è **scriverne abbastanza da lasciare una risposta sola, e non uno di più.**
>
> ```
>  1  ──────────────────────────────────────
>  2  ──────────────────────────────────────
>  3  ──────────────────────────────────────
>  4  ──────────────────────────────────────
> ```
>
> E qui c'è l'unico modo di saperlo: **dallo a qualcuno in casa e stai zitto.**
>
> - Se arriva alla tua stessa risposta, va bene.
> - Se arriva a una risposta **diversa**, il tuo gioco ne ammetteva due, e non è un errore suo: aggiungi un indizio e riprova.
> - Se non arriva a nessuna risposta, gli indizi erano contraddittori. Guarda quali due non possono stare insieme.
>
> ```
>  quanti indizi al primo tentativo  ──────
>  quanti alla fine                  ──────
>  che cosa ti eri dimenticato       ────────────────────────
> ```

Il sistema stampa una matrice vuota, un esempio già risolto e un procedimento; il gioco lo fa chi legge. La verifica non è nel foglio ed è la migliore che ci sia: **una seconda persona che non sa che cosa si sta verificando** — la struttura raccolta alle voci 103, partitura / spartito, 107, gioco di ruolo e 108, copione teatrale.

La parte che insegna qualcosa non è la costruzione: è che una risposta diversa dalla propria **non è un errore di chi risponde ma un difetto del gioco.** Non è una consolazione: è la definizione di che cosa vuol dire che un elenco di indizi funziona.

L'esempio già risolto in apertura è la mossa raccolta alle voci 126, cruciverba crittico e 341, crittografia pura: per una forma opaca, tre righe già svolte spiegano più di qualunque regola.

Su un display da quattro righe la forma non ci sta. Servono la tabella intera e gli indizi insieme, e questo è il caso già descritto alla voce 63, inferire da un'assenza: quattro righe non sono un foglio più piccolo.

## Da riprendere alla rassegna

**Tre attribuzioni false in dodici voci, tutte e tre documentate come false dalla fonte stessa.** Il professor Zapp che non è mai esistito, le griglie di Fleissner che sono di Klüber o di Hindenburg, l'enigma di Einstein che Einstein non ha mai visto. In tutti e tre i casi l'errore è stato ripetuto per decenni perché era una storia migliore. **È materiale per una forma che l'elenco non ha: verificare un'attribuzione**, e le tre prove sono di tipo diverso — un registro accademico, una data di pubblicazione, e un anacronismo interno al testo. Quest'ultimo è il più bello: le sigarette non esistevano ancora.

**Il contenuto è arbitrario per costruzione, e questo è raro.** Colori, nazionalità, animali e marche si possono sostituire in blocco senza toccare la logica. Nessun'altra forma del capitolo lo consente — un indovinello, cambiando l'oggetto, diventa un altro indovinello. Da qui segue che è **l'unica forma dell'elenco in cui si potrebbe far scegliere a chi legge di che cosa parla il compito**, e vale la pena chiedersi che cosa cambi quando le persone della tabella sono quelle di casa.

**Costruire e risolvere qui non sono nemmeno lo stesso mestiere.** Risolvere è tenere il conto; costruire è dimostrare che non esiste una seconda soluzione, cioè fare un'affermazione universale. È la distinzione fra verificare e dimostrare, e sta dentro un gioco da rivista. Alla rassegna vale la pena chiedersi quante forme dell'elenco abbiano questa asimmetria, e da quale delle due parti convenga mettere chi gioca.

**Un indizio in meno e ce ne sono molte, uno in più e non serve.** La domanda posta dal titolo *Is Einstein's Puzzle Over-Specified?* riguarda ogni consegna che questa enciclopedia proponga: quanti vincoli servono perché ci sia una cosa da fare, e da quale vincolo in poi si sta solo aggiungendo testo.

Da verificare: quella comunicazione del 2009, di cui ho solo il titolo. E se esista una versione italiana canonica del puzzle della zebra nelle riviste di enigmistica, che non è stata cercata.
