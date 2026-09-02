# Enigma di attraversamento

- **Numero** 143 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi logici»
- **Si chiama anche** lupo capra e cavolo, il traghettatore, *river crossing puzzle*, *transport puzzle*, missionari e cannibali, mariti gelosi, il ponte e la torcia
- **In una riga** lupo, capra, cavolo.
- **Fonti** [River crossing puzzle](https://en.wikipedia.org/wiki/River_crossing_puzzle), [Wolf, goat and cabbage problem](https://en.wikipedia.org/wiki/Wolf,_goat_and_cabbage_problem) e [Missionaries and cannibals problem](https://en.wikipedia.org/wiki/Missionaries_and_cannibals_problem), prese il 30 agosto 2026 da en.wikipedia

## Che cos'è

Delle cose stanno su una sponda e devono arrivare sull'altra. La barca porta poco, e certe cose non si possono lasciare sole insieme. Si tratta di trovare la sequenza di viaggi che porta tutti dall'altra parte senza che succeda niente.

Con questa voce il capitolo cambia asse per la seconda volta. Nelle otto voci precedenti c'era qualcosa da leggere o da riconoscere; da qui in poi non c'è niente da leggere. **C'è una situazione con delle regole e una configurazione da raggiungere**, e quello che la distingue dalle tre voci che seguono è che cosa si conserva: qui **chi sta su quale sponda.**

Parti mobili:

- **Quanto porta la barca.** È il parametro che decide tutto, e ha un nome tecnico: il **numero di Alcuino** di un problema è la dimensione minima della barca perché l'attraversamento sia possibile.
- **Quali coppie sono in conflitto.** Il lupo e la capra, la capra e il cavolo; il lupo e il cavolo no. Da qui la struttura, che si disegna come un grafo: i vertici sono le cose, gli spigoli le coppie che non possono restare sole.
- **Se il conflitto è di numero invece che di identità.** Nei missionari e cannibali non conta chi è con chi, conta che su nessuna sponda i cannibali siano più dei missionari.
- **Se qualcuno può tornare indietro.** Non è un parametro: è la cosa che chi risolve non pensa. Ci si torna sotto.
- **Se ci sono altre risorse.** Nel problema del ponte e della torcia c'è una torcia sola e quattro persone che camminano a velocità diverse, e la torcia deve tornare indietro con qualcuno.

## Da dove viene

I problemi di attraversamento più antichi che si conoscano stanno nelle **_Propositiones ad Acuendos Juvenes_ — «problemi per aguzzare i giovani» —, un manoscritto le cui copie più antiche sono del IX secolo, tradizionalmente attribuito ad Alcuino di York** (morto nell'804). Il manoscritto ne contiene tre: il lupo, la capra e il cavolo; i missionari e i cannibali; e una terza che è quella dei pesi — un uomo e una donna dello stesso peso, con due bambini che pesano ciascuno la metà, e una barca che regge il peso di un adulto solo.

Il secondo dei tre ha cambiato vestito quattro volte, e l'elenco è istruttivo. In Alcuino sono **fratelli e sorelle**, con il vincolo che nessuna donna stia in compagnia di un altro uomo se non c'è suo fratello. Dal XIII al XV secolo il problema si diffonde nell'Europa settentrionale e le coppie diventano **mariti e mogli**. Poi diventano **padroni e servitori**. La formulazione con **missionari e cannibali non compare prima della fine dell'Ottocento**. Nel 2020 una vignetta sul problema ha portato l'ente esaminatore inglese AQA a ritirare un libro di testo. Millecento anni di travestimenti, e l'ultimo non ha retto.

Il lupo, la capra e il cavolo sono entrati nel folclore di molte culture, e hanno un numero di catalogo: **H506.3 nell'indice dei motivi di Stith Thompson, e ATU 1579 nella classificazione Aarne-Thompson.** La fonte elenca dove è stato raccolto: afroamericani, Camerun, Capo Verde, Danimarca, Etiopia, Ghana, Italia, Romania, Russia, Scozia, Sudan, Uganda, Zambia, Zimbabwe. In alcune parti dell'Africa la barca porta due cose invece di una, e allora si aggiunge il vincolo che nemmeno il lupo e il cavolo possano restare soli.

C'è anche una versione che viene da una leggenda cinese, dipinta su un pannello del Settecento dall'artista giapponese **Maruyama Ōkyo**, oggi al British Museum. Secondo la leggenda, quando una tigre ha tre cuccioli uno di essi è un leopardo, ed è più feroce degli altri. Il pannello mostra la tigre che traghetta i cuccioli uno alla volta, e il problema è come farlo senza lasciare il leopardo solo con nessuno dei due fratelli. È lo stesso problema del lupo, della capra e del cavolo. **La stessa variante è registrata anche come un koan del Ryōan-ji, tempio zen di Kyoto** — e questo la collega direttamente alla voce 118, koan.

## Varianti e parenti

- **Lupo, capra e cavolo** — tre oggetti A, B, C tali che né A con B né B con C possono restare soli. Le varianti cosmetiche sono infinite: volpe, gallina e grano; volpe, oca e mais; pantera, maiale e polenta.
- **Missionari e cannibali** — il conflitto è di numero, non di identità.
- **Mariti gelosi** — la stessa cosa con l'identità che conta: nessuna donna può stare con un altro uomo se non c'è suo marito. Una soluzione del problema dei mariti gelosi è sempre anche una soluzione di quello dei missionari, non viceversa.
- **Il ponte e la torcia** — quattro persone di notte, un ponte che regge due persone, una torcia sola. Il vincolo non è chi con chi, è il tempo.
- **Il problema dei pesi di Alcuino** — nessun conflitto fra le cose, solo una portata.
- **Voce 145, enigma di travaso** — la vicina più stretta: anche lì una configurazione da raggiungere con mosse legali, ma quello che si conserva è una quantità invece di una posizione.
- **Voce 171, puzzle a scorrimento (15, Sokoban)** — la stessa struttura senza narrazione: uno spazio di stati e delle mosse legali.
- **Voce 64, simulare** — il verbo. La griglia che si riempie mossa per mossa è materiale eseguibile, non una risposta.
- **Voce 366, problema di grafi** — nel capitolo 13. Il confine è che lì il grafo è la cosa da studiare, qui è un modo di guardare una storia.
- **Voce 118, koan** — per la versione della tigre, che è registrata come koan del Ryōan-ji. È l'unica intersezione documentata fra le due voci.

## Che cosa se ne sa

**La difficoltà non sta nella pianificazione: sta in una mossa che nessuno prova.** La fonte lo scrive per esteso, ed è il dato più utile di tutta la voce. La chiave della soluzione è **accorgersi che il contadino può riportare indietro delle cose.** «Spesso non è chiaro dal modo in cui la storia è raccontata, ma non è mai vietato. Saperlo rende il problema facile da risolvere anche per bambini piccoli.» E la fonte aggiunge che il centro dell'enigma non è organizzare dei compiti, ma il pensiero creativo, come nel problema dei nove punti. **Non è una difficoltà di calcolo: è che una mossa consentita non viene nemmeno considerata.**

Gurdjieff, nelle sue memorie, ne trae la stessa cosa in un'altra lingua: chi risolve «non deve solamente usare l'ingegno che ogni uomo normale dovrebbe avere, ma non deve essere pigro né risparmiare le proprie forze, e deve attraversare il fiume più volte del necessario per raggiungere lo scopo».

**Il conto esatto è sette, e la sua forma è la cosa interessante: quattro andate e tre ritorni.** Porta la capra; torna a vuoto; porta il lupo o il cavolo; **torna con la capra**; porta l'altro; torna a vuoto; porta la capra. Il terzo ritorno non è a vuoto, ed è quello che nessuno immagina.

**La risposta cambia a seconda di una regola che nessuno scrive.** Nel problema dei mariti gelosi la soluzione più breve conosciuta è di **undici viaggi**. Ma se una donna che è nella barca ferma a riva conta come «da sola», cioè come non in presenza degli uomini che sono a terra, allora **ne bastano nove**. E se invece si richiede che i mariti siano scesi a terra per contare come presenti, una delle mosse della soluzione da undici diventa impossibile. **Tre risposte diverse per lo stesso testo, e la differenza sta tutta in che cosa significhi «essere sulla sponda».** È il caso più netto raccolto dall'enciclopedia di un enunciato la cui soluzione dipende da una convenzione taciuta.

**I numeri delle generalizzazioni sono netti, e alcuni sono sorprendenti.** Con una barca da due persone, due coppie hanno bisogno di cinque viaggi, e **con quattro coppie o più il problema non ha soluzione.** Con una barca da tre passano fino a cinque coppie; con una barca da quattro passa un numero qualunque di coppie. E se si aggiunge un'isola in mezzo al fiume, un numero qualunque di coppie passa con una barca da due. La variante dell'isola è di Cadet de Fontenay, 1879, ed è stata risolta completamente da Ian Pressman e David Singmaster nel 1989.

**È un problema classico dell'intelligenza artificiale, e per una ragione precisa.** Saul Amarel lo usò come esempio di **rappresentazione** di un problema: lo stato si scrive come un vettore ⟨m, c, b⟩ — quanti missionari, quanti cannibali, e da che parte è la barca — e le mosse diventano sottrazioni e addizioni di vettori. Poi si costruisce un albero, si buttano via i nodi in cui i cannibali sono in maggioranza, e si va avanti finché non si arriva a ⟨0,0,0⟩. **Il punto di Amarel non era risolvere il problema: era che scegliere come scriverlo è metà del lavoro.**

**La verifica non richiede nessuno.** È la proprietà che conta più di tutte: una sequenza di mosse si controlla eseguendola. Se in un momento qualsiasi la capra resta sola col cavolo, si vede. Non serve una soluzione stampata, non serve un adulto, e non serve che chi ha scritto il foglio conosca la risposta. **Il problema che chiude il capitolo 5 — un enigma ha una risposta e qualcuno deve saperla — qui non si pone affatto.**

## Esempi trovati

Da Alcuino, IX secolo: le tre versioni, in latino, in un manoscritto pensato per esercitare i giovani. Il titolo lo dice già.

Da Maruyama Ōkyo, Settecento: la tigre che traghetta i cuccioli, dipinta su un pannello. Il problema è dentro un quadro e non è scritto da nessuna parte.

Dal Ryōan-ji: la stessa storia registrata come koan.

Da Lewis Carroll, che ne era appassionato, e dalle raccolte di matematica ricreativa che l'hanno ristampato da allora.

Dalla televisione e dai videogiochi: *Professor Layton and the Curious Village*, *Broken Sword*, un episodio dei *Simpson* in cui Homer deve attraversare un fiume con Maggie, il cane e un barattolo di veleno per topi che sembra caramelle, e un episodio di *Bull* in cui l'avvocato **scarta ogni giurato che sappia risolvere l'indovinello.**

Dal folclore africano: la variante con la barca da due posti e il vincolo aggiuntivo, che non è una semplificazione ma un problema diverso.

## Un esempio giocabile

Il foglio porta la storia e una griglia di stato, e chi lo scrive non deve sapere la risposta: la sequenza si verifica eseguendola. Questa è la prima forma di tutto il blocco in cui non c'è nessun limite tecnico da aggirare.

> **I tre cuccioli**
>
> Una leggenda cinese dice che quando una tigre ha tre cuccioli, uno dei tre non è una tigre: è un leopardo, ed è più feroce degli altri due. Un pittore giapponese l'ha dipinta nel Settecento, e nel quadro la tigre sta traghettando i cuccioli attraverso un fiume.
>
> Li porta uno alla volta, perché in bocca ce ne sta uno solo.
>
> **Se il leopardo resta su una sponda con uno dei suoi fratelli senza la madre, se lo mangia.** I due fratelli tigre fra loro vanno d'accordo.
>
> Come li porta tutti e tre dall'altra parte?
>
> Segna qui ogni viaggio. Su ogni riga scrivi chi c'è su ciascuna sponda **dopo** il viaggio.
>
> ```
>       sponda di qua              sponda di là
>  ─────────────────────────  ─────────────────────────
>  1 ───────────────────────  ─────────────────────────
>  2 ───────────────────────  ─────────────────────────
>  3 ───────────────────────  ─────────────────────────
>  4 ───────────────────────  ─────────────────────────
>  5 ───────────────────────  ─────────────────────────
>  6 ───────────────────────  ─────────────────────────
>  7 ───────────────────────  ─────────────────────────
>  8 ───────────────────────  ─────────────────────────
> ```
>
> Non c'è una soluzione stampata da nessuna parte, e non serve: **se il leopardo è rimasto solo con un fratello, lo vedi nella riga che hai appena scritto.**
>
> ---
>
> Se dopo un po' non ne esci, leggi questa riga e non prima.
>
> > Rileggi le regole. **Da nessuna parte c'è scritto che la madre debba tornare a vuoto.**

La griglia stampata è materiale eseguibile e non un modo di rispondere — è la terza funzione della griglia, quella osservata alla voce 64, simulare. La verifica è nel materiale, e appartiene alla famiglia raccolta alle voci 7, classificazione in insiemi, 10, riordino di un testo tagliato a pezzi, 26, istruzioni e 45, composizione fisica.

Il suggerimento sta in fondo e dice apertamente di non leggerlo prima. È la struttura di Auble, Franks e Soraci, raccolta alla voce 110, indovinello classico (enigma): **se la parola chiave arriva prima, l'effetto sparisce del tutto.** Qui la parola chiave è «tornare indietro», e vale meno di cinque parole.

Il vestito è quello dei cuccioli e non quello del lupo e della capra, per una ragione sola: chi ha già sentito il lupo e la capra non sta risolvendo niente. La leggenda cinese è documentata, il quadro esiste, e la struttura logica è identica.

Sul display da quattro righe la forma non ci sta: la griglia dello stato è quello che rende il problema affrontabile, e otto righe non ci stanno in quattro. Ma **l'enunciato ci sta**, e il display può portarlo la mattina lasciando il foglio con la griglia per il pomeriggio: è la rete di supporti della voce 82, rete di supporti, con il pannello che porta la domanda e il foglio che porta il lavoro.

## Che cosa la rende interessante

**La mossa consentita che nessuno prova in considerazione.** Non è una difficoltà di calcolo e non è un trabocchetto: è una regola che non c'è, e che chi legge aggiunge da solo. La fonte dice che saperlo rende il problema facile «anche per bambini piccoli», cioè che tutta la difficoltà sta lì. **È una struttura che l'enciclopedia non aveva ancora nominato: l'enigma in cui l'ostacolo è un divieto immaginario.** Da cercare altrove, e da guardare accanto al vincolo negativo, che è il suo opposto esatto.

**Tre risposte per lo stesso testo, e la differenza è una convenzione taciuta.** Undici viaggi o nove, a seconda che stare nella barca ferma a riva conti come stare a riva. Vale per ogni consegna che questa enciclopedia stamperà: **quello che non è definito verrà definito da chi risponde, e non allo stesso modo.** La nota di Life alla voce 142, puzzle a griglia (chi beve cosa, chi vive dove) — «destra vuol dire la vostra destra» — è la stessa cosa vista dal lato di chi scrive bene.

**Un enunciato in cui il contenuto non è neutrale.** I missionari e i cannibali erano fratelli e sorelle in Alcuino, poi mariti e mogli, poi padroni e servitori, e cannibali solo dall'Ottocento; nel 2020 un libro di testo è stato ritirato. La struttura logica non è cambiata mai. **Una forma che si può rivestire di qualunque cosa verrà rivestita di qualcosa, e quel qualcosa non è mai casuale.** Da tenere presente per qualunque consegna.

**È la prima forma del capitolo in cui la verifica non richiede nessuno e nessuna soluzione stampata.** Non serve un adulto, non serve un foglio delle risposte, non serve che chi ha scritto sappia. Vale la pena elencare insieme tutte le forme con questa proprietà: sono le uniche che si possono proporre senza che nessuno debba sapere la risposta.

Da verificare: la lettura effettiva del pannello di Maruyama Ōkyo al British Museum, che qui è riportata solo attraverso la voce di Wikipedia. E la formulazione originale latina delle tre proposizioni di Alcuino, che non è stata cercata.
