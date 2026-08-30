# Puzzle di dissezione

- **Numero** 161 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi fisici e meccanici»
- **Si chiama anche** dissezione, puzzle di trasformazione, Richter puzzle, equiscomponibilità, congruenza a forbici, *scissors congruence*, dissezione a cerniera
- **In una riga** tagliare una figura e ricomporla in un'altra.
- **Fonti** `dissection-puzzle.txt`, `dissection-problem.txt`, `hinged-dissection.txt`, `wallace-bolyai-gerwien.txt`, `fold-and-cut.txt`, `tessellation.txt`, prese il 30 agosto 2026
- **Stato della ricerca** fatta, 30 agosto 2026

## Che cos'è

Si ha una figura sola. La si taglia in pezzi, e con gli stessi pezzi si compone una figura diversa. Niente entra e niente esce: cambia solo il contorno.

Il verbo è **tagliare**, e questo la separa dalle due voci vicine. Nella voce 160, tangram e puzzle di tassellazione i pezzi arrivano già tagliati e la domanda è dove metterli; nella voce 159, puzzle a incastro (jigsaw) la figura di arrivo è quella di partenza. Qui il taglio è il compito, e la figura di arrivo è un'altra.

Parti mobili:

- **Quanti pezzi.** È la manopola principale e ha un numero minimo, che a volte è noto e a volte no. Meno pezzi è più difficile da trovare e più bello da guardare.
- **Se il taglio è dato o va trovato.** Consegnare la figura con le linee già tracciate è un esercizio di ritaglio; consegnarla nuda è il rompicapo.
- **Se la figura di arrivo è dichiarata.** «Fanne un quadrato» e «fanne qualcosa di regolare» sono due compiti diversi.
- **Se i pezzi si possono girare o solo traslare.** Traslare soltanto è molto più vincolante, e su carta stampata da una faccia sola girare un pezzo si vede.
- **Se i pezzi restano attaccati.** Nella dissezione a cerniera i pezzi sono legati a catena in punti fissi e la trasformazione avviene facendo ruotare la catena senza staccare mai niente.

## Da dove viene

È la forma geometrica più antica raccolta in questo capitolo. Le descrizioni più remote risalgono al tempo di Platone (427-347 a.C.) e chiedono di fare **un quadrato grande da due quadrati uguali usando quattro pezzi**; altre dissezioni antiche erano rappresentazioni grafiche del teorema di Pitagora. L'*Ostomachion* attribuito ad Archimede fa la stessa cosa con quattordici pezzi, ottenuti suddividendo i quattro precedenti (`dissection-puzzle.txt`, 30 agosto 2026).

Nel decimo secolo i matematici arabi usano dissezioni geometriche nei commenti agli *Elementi* di Euclide. Nel Settecento lo studioso cinese Tai Chen ne descrive una per approssimare π.

Il salto di popolarità è di fine Ottocento, quando giornali e riviste cominciano a pubblicarle: **Sam Loyd** negli Stati Uniti e **Henry Dudeney** in Gran Bretagna sono i più stampati. Martin Gardner ci dedica la rubrica *Mathematical Games* del novembre 1961, con una tabella delle dissezioni migliori note fra quadrato, pentagono, esagono e croce greca.

**Il teorema che sta sotto è del 1807 e ha tre nomi.** Il teorema di Wallace-Bolyai-Gerwien dice che due poligoni si possono tagliare l'uno nell'altro **se e solo se hanno la stessa area**. William Wallace lo aveva dimostrato nel 1807; secondo altre fonti Farkas Bolyai e Gerwien lo dimostrarono indipendentemente nel 1833 e nel 1835 (`wallace-bolyai-gerwien.txt`, 30 agosto 2026). La dimostrazione è **costruttiva e non richiede l'assioma della scelta**, e la pagina lo dice con una frase che vale per noi: i pezzi «si possono, in teoria, ritagliare con le forbici da un foglio e rimettere insieme a mano». Con un avvertimento nella riga dopo: **il numero di pezzi che quella procedura produce supera di molto il minimo necessario.**

**Su una data due fonti si contraddicono, e c'è un modo di decidere.** Il problema del merciaio — triangolo equilatero in quadrato con quattro pezzi — è dato da `dissection-puzzle.txt` come «proposto nel 1907 da Henry Dudeney», e da `hinged-dissection.txt` come introdotto nel libro *The Canterbury Puzzles* del 1907. Ma `dissection-problem.txt` lo data al **1902**, con una citazione primaria: *Weekly Dispatch*, rubrica «Puzzles and Prizes», numero del 6 aprile, discussione il 20 aprile, soluzione il 4 maggio. Si tiene il 1902, per due ragioni: la citazione è a un giornale con tre date precise, e **il conto torna** — quando nel 2024 Erik Demaine, Tonan Kamata e Ryuhei Uehara pubblicano la dimostrazione che con tre pezzi non si può fare, lo *Scientific American* titola «un enigma vecchio di 122 anni», e 2024 meno 122 fa 1902, non 1907. Il 1907 è la data del libro, non quella del problema.

## Varianti e parenti

- **Dissezione a due figure** — da una figura data a una figura dichiarata. Il problema del merciaio ne è l'esemplare classico.
- **Dissezione a molte figure** — il tangram, dove gli stessi pezzi fanno migliaia di sagome; la fonte lo classifica dentro questa famiglia.
- **Dissezione a cerniera** — i pezzi legati a catena in punti fissi. Dudeney la rende famosa nel 1907; nel **2007** Erik Demaine e altri dimostrano che **due poligoni di area uguale hanno sempre una dissezione a cerniera**, e danno l'algoritmo per costruirla (`hinged-dissection.txt`).
- **Dissezione a cerniera di torsione** — la cerniera sta su uno spigolo invece che su un vertice, e il pezzo si ribalta. Se anche questa esista sempre, nel 2002 era ancora una domanda aperta.
- **Puzzle del quadrato mancante** — l'illusione in cui due figure di area diversa sembrano fatte degli stessi pezzi. Non è una dissezione: è una dissezione falsa, ed è per questo che sta qui.
- **Puzzle che svanisce** — la stessa illusione con degli oggetti disegnati, che spostando i pezzi diventano uno di meno.
- **Equiscomposizione** — la partizione in triangoli di area uguale. La fonte dà un fatto secco: **un quadrato non si può dividere in un numero dispari di triangoli di area uguale** (teorema di Monsky).
- **Taglio** — voce 43, taglio: là il taglio è il supporto su cui arriva la domanda, e la figura ritagliata è il risultato; qui il taglio è il rompicapo, e il risultato è una seconda figura.
- **Piegatura** — voce 42, piegatura: la trasformazione senza forbici, che è la voce 162, puzzle di piegatura.
- **Piega e taglia** — il teorema del piega-e-taglia: qualunque figura a lati dritti si ricava da un foglio piegato piatto con **un solo taglio dritto** (`fold-and-cut.txt`). È il punto in cui questa voce e la successiva si toccano.

**Il confine con il capitolo 13.** La voce 370, dissezione geometrica raccoglie la stessa operazione dal lato del problema matematico: quanti pezzi servono al minimo, e come si dimostra. Qui si descrive la forma di pagina — una figura stampata, delle forbici, e una figura da ottenere — e quello che chiede a chi la riceve. Le due voci hanno lo stesso oggetto e due domande diverse, ed è la stessa separazione fissata alla voce 142, puzzle a griglia (chi beve cosa, chi vive dove).

## Che cosa se ne sa

Fonti prese il 30 agosto 2026. Questa è una delle poche voci del capitolo in cui quello che si sa è **dimostrato**, e non misurato su delle persone: sulla resa didattica della dissezione le pagine lette non riportano nessun dato.

**L'area è l'unica cosa che conta, ed è un teorema.** Due poligoni si tagliano l'uno nell'altro se e solo se hanno la stessa area. Ne segue una conseguenza pratica che cambia il modo di consegnare questa forma: **chi riceve la figura può calcolare da solo l'obiettivo.** Se il pezzo di carta ha area 36, il quadrato che se ne ricava ha lato 6, e non c'è bisogno che nessuno lo dica.

**Il minimo numero di pezzi è difficile e ha appena avuto una risposta.** Dudeney trasforma un triangolo equilatero in un quadrato con quattro pezzi nel 1902. Che **con tre non si possa** è stato dimostrato nel dicembre 2024 da Demaine, Kamata e Uehara: centoventidue anni per chiudere una domanda che si enuncia in una riga. La stessa fonte annota che il risultato è stato indicato dallo *Scientific American* fra i dieci maggiori del 2025.

**La procedura che il teorema fornisce non è quella che si vorrebbe usare.** Il metodo costruttivo passa per un rettangolo intermedio di larghezza unitaria e produce molti più pezzi del necessario. È la distinzione fra sapere che una cosa si può fare e saperla fare bene, e in questa famiglia le due cose sono lontanissime.

**Tarski ha un limite inferiore.** Se il primo poligono è convesso, il numero minimo di pezzi è almeno il rapporto fra il diametro del primo e quello del secondo. Serve a sapere in anticipo che una figura lunga e stretta non diventerà mai un quadrato con pochi pezzi.

**Le dissezioni false sono una famiglia a parte, e assomigliano alle vere.** Il puzzle del quadrato mancante e il paradosso dei due monaci del tangram funzionano perché una differenza di area distribuita su un contorno lungo non si vede. Per un sistema che stampa figure, il rischio è simmetrico: **una dissezione stampata con un errore di un millimetro è indistinguibile da un'illusione riuscita**, e chi ci lavora sopra non ha modo di sapere quale delle due gli è stata data.

## Esempi trovati

Dai greci del tempo di Platone: due quadrati uguali che diventano un quadrato solo, in quattro pezzi.

Dall'*Ostomachion*: gli stessi due quadrati in quattordici pezzi, ottenuti tagliando ancora i quattro.

Da Dudeney, 1902: il triangolo equilatero che diventa un quadrato in quattro pezzi, e i quattro pezzi restano attaccati fra loro come una catena. Si posa e si fa girare.

Da Tai Chen, Settecento: una dissezione usata per approssimare π, cioè un uso non ludico della stessa operazione.

Da Gardner, 1961: la tabella delle dissezioni migliori conosciute fra le figure regolari, che è un elenco di primati aggiornabile e non un insieme di soluzioni.

Dal piega-e-taglia: la stella a cinque punte della bandiera americana, che secondo un articolo dell'*Harper's* del 1873 Betsy Ross avrebbe proposto proprio perché si ottiene piegando e dando un colpo di forbici solo. La descrizione più antica di un problema di questo tipo è giapponese, nel *Wakoku Chiyekurabe* di Kan Chu Sen, **1721**.

## Una nostra versione

Questa forma sta su un foglio meglio di quasi tutte le altre del blocco: il sistema stampa una figura su carta a quadretti, e le forbici fanno tagli dritti senza tradire niente.

> **Un rettangolo che diventa un quadrato, con un taglio solo**
>
> Questo rettangolo è largo nove quadretti e alto quattro.
>
> ```
> ┌─┬─┬─┬─┬─┬─┬─┬─┬─┐
> ├─┼─┼─┼─┼─┼─┼─┼─┼─┤
> ├─┼─┼─┼─┼─┼─┼─┼─┼─┤
> ├─┼─┼─┼─┼─┼─┼─┼─┼─┤
> └─┴─┴─┴─┴─┴─┴─┴─┴─┘
> ```
>
> Ritaglialo. Poi **taglialo in due pezzi soli**, seguendo le righe dei quadretti, in modo che i due pezzi rimessi insieme facciano un **quadrato**.
>
> Prima di tagliare, rispondi a questa, che è la parte che conta:
>
> ```
>  Quanti quadretti ha il rettangolo?  ─────
>
>  Allora il quadrato avrà il lato di  ───── quadretti.
> ```
>
> Adesso sai esattamente che cosa devi ottenere, e non te l'ho detto io.
>
> Il taglio non è dritto: è una **scaletta**. Quando l'avrai trovato, incolla il quadrato qui sotto e scrivi accanto quanti tentativi hai fatto prima.

Il rettangolo ha 36 quadretti, quindi il quadrato ha lato 6, e questo lo ricava chi legge con un conto di una riga. È il caso più netto raccolto in questa enciclopedia in cui **l'obiettivo non viene dichiarato ma calcolato**, ed è possibile solo perché il teorema di Wallace-Bolyai-Gerwien dice che l'area è tutto quello che conta.

La parola «scaletta» è l'unico suggerimento, ed è dosata: dice la famiglia del taglio e non dice dove passa. Toglierla renderebbe il foglio più difficile in un modo che non produce niente — è un caso in cui, secondo la misura di Auble, Franks e Soraci raccolta alla voce 110, indovinello classico (enigma), anticipare non rovina, perché non è la risposta ma la sua forma.

**Il taglio è stato verificato con un programma.** I due pezzi sono due scalette uguali: nel rettangolo, uno occupa le due righe in basso fino alla sesta colonna più le due righe in alto fino alla terza; l'altro è quello che resta. Rimessi insieme coprono il quadrato 6×6 esattamente, e il programma trova otto disposizioni, che sono la stessa a meno di girare il quadrato e scambiare i due pezzi — i quali sono congruenti, ed è la ragione per cui il taglio funziona.

Il limite, ed è lo stesso della voce vicina: **il foglio non sa se il taglio è stato fatto**, e un taglio storto di un millimetro produce un quadrato che non chiude, indistinguibile da un taglio nel posto sbagliato.

## Da riprendere alla rassegna

**L'obiettivo calcolato invece che dichiarato.** L'area è un invariante, quindi chi riceve il foglio può derivare da sé che cosa deve ottenere. È la prima volta che l'enciclopedia incontra una forma in cui il compito **contiene** la propria consegna, e vale la pena cercarne altre: sono le sole in cui il sistema non deve dire la risposta perché non ce n'è bisogno.

**Sapere che si può fare e saperlo fare bene sono due cose diverse, e qui la distanza è misurata in secoli.** Il teorema del 1807 garantisce che una dissezione esiste; il numero minimo di pezzi fra un triangolo e un quadrato è stato chiuso nel 2024. Per un sistema che genera fogli è il caso più chiaro raccolto di un problema **facile da porre e non risolvibile da chi lo pone**, e la via d'uscita è la stessa già usata tre volte: scegliere una taglia in cui la verifica sta in una tabella.

**Una dissezione sbagliata è indistinguibile da un'illusione riuscita.** Il puzzle del quadrato mancante vive esattamente di questo. Le forme che falliscono in silenzio erano sette con la voce 159, puzzle a incastro (jigsaw); questa è la prima in cui il fallimento silenzioso ha una tradizione artistica alle spalle, e non è chiaro se sia un guasto o una risorsa.

**Il taglio come verbo del rompicapo, e non come supporto.** La voce 43, taglio descrive la stessa forbice dal lato del materiale. Alla rassegna vale la pena guardare quante forme dell'elenco cambino capitolo semplicemente cambiando che cosa si sta chiedendo dello stesso gesto, perché sembrano parecchie.

**La carta a quadretti è un'infrastruttura che il sistema non sta usando.** Rende esatti il taglio, la misura e la verifica, costa quanto un foglio bianco, e trasforma «più o meno» in un numero. Da provare all'indietro su tutte le forme geometriche dell'elenco.

