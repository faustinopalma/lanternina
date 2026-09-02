# Enigma auto-referenziale

- **Numero** 158 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi logici»
- **Si chiama anche** autoreferenza, quiz che parla di sé, test auto-referenziale, quine, *self-reference*, *self-referential test*, *strange loop*
- **In una riga** un quiz le cui domande parlano di sé stesso.
- **Fonti** [Self-reference](https://en.wikipedia.org/wiki/Self-reference), [Quine (computing)](https://en.wikipedia.org/wiki/Quine_(computing)), [Liar paradox](https://en.wikipedia.org/wiki/Liar_paradox) e [On-Line Encyclopedia of Integer Sequences](https://en.wikipedia.org/wiki/On-Line_Encyclopedia_of_Integer_Sequences), prese il 30 agosto 2026 da en.wikipedia; il quiz dell'esempio giocabile è costruito e verificato a mano su tutte e ventisette le combinazioni

## Che cos'è

Un testo il cui contenuto è un'affermazione sul testo stesso. Nella forma di gioco: un elenco di domande le cui risposte dipendono dalle risposte che si stanno dando.

Con la voce 157, enigma di teoria dei giochi chiude il capitolo dal lato astratto. Là si ragionava su un avversario che ragiona; **qui si ragiona su una frase che parla di sé**, e non c'è nessun avversario. La differenza con la voce 151, paradosso è quella che rende questa una forma di gioco e quella no: **l'autoreferenza non è per forza contraddittoria.** «Questa frase è scritta in italiano» parla di sé, è vera, e non ha niente di paradossale. Un quiz auto-referenziale ben costruito ha una risposta, e si può trovare.

Parti mobili:

- **Se il riferimento è diretto o indiretto.** «Questa frase» è diretto; una frase che rimanda a un'altra che rimanda alla prima è indiretto, e la fonte lo definisce con precisione: **cicli in un grafo di relazioni di riferimento.**
- **Che cosa esce.** Tre esiti, e sono davvero tre: la frase è contraddittoria; la frase è vera e basta; la frase non si può decidere ma qualunque decisione sarebbe coerente.
- **Su che cosa parla di sé.** Sul numero delle proprie risposte, sulle proprie lettere, sulla propria lunghezza, sul proprio autore.
- **Se c'è una risposta e se è unica.** In un quiz, il costruttore deve garantirlo, e lo si vede sotto.
- **Quanto è lungo il ciclo.** Un passo, due, o un anello che passa per tutto il foglio.

## Da dove viene

L'antenato registrato più antico che la fonte nomina è il **paradosso di Epimenide**, «tutti i cretesi sono bugiardi» detto da un cretese, che è indicato come «una delle prime versioni documentate».

Il nome moderno della cosa in informatica viene da un filosofo. **Willard Van Orman Quine** (1908-2000) studiò a lungo l'autoreferenza indiretta, e in particolare questa espressione, nota come paradosso di Quine:

> «Produce falsità se preceduta dalla propria citazione» produce falsità se preceduta dalla propria citazione.

**Douglas Hofstadter** coniò il termine *quine* — un programma che stampa il proprio codice sorgente — in suo onore, nel libro *Gödel, Escher, Bach* del **1979**. La cosa era più vecchia: **John von Neumann** teorizzava automi auto-riproducenti negli anni Quaranta, e il primo programma auto-riproducente noto fu scritto in Atlas Autocode a Edimburgo negli anni Sessanta da Hamish Dewar, docente e ricercatore di quell'università. Un articolo di Paul Bratley e Jean Millo, *Computer Recreations: Self-Reproducing Automata*, ne parla nel **1972**.

I libri di Hofstadter — *Gödel, Escher, Bach* e *Metamagical Themas* — sono, dice la fonte, quelli che hanno portato questi concetti nella cultura intellettuale generale **negli anni Ottanta**. Da lì viene anche la legge di Hofstadter, che è un esempio di sé stessa: *ci vuole sempre più tempo di quanto ti aspetti, anche quando tieni conto della legge di Hofstadter.*

## Varianti e parenti

- **La frase che parla di sé** — «questa frase è falsa», «questa frase è scritta in italiano», «questa frase contiene cinque parole».
- **L'autoreferenza indiretta** — il paradosso della cartolina, in cui una frase rimanda a un'altra che rimanda alla prima.
- **Il quine** — un programma che stampa sé stesso, possibile in qualunque linguaggio Turing-completo per conseguenza diretta del teorema di ricorsione di Kleene. Per divertimento, dice la fonte, i programmatori gareggiano a scriverne il più corto.
- **La formula di Tupper** — una curiosità matematica che, disegnata, produce l'immagine della propria formula.
- **Il libro fatto solo di recensioni di sé stesso** — proposto da Hofstadter, e da allora realizzato con i wiki.
- **Le successioni auto-referenziali dell'enciclopedia di Sloane** — vedi sotto, perché è il caso più bello.
- **Voce 151, paradosso** — dove l'autoreferenza produce una cosa su cui non c'è niente da fare.
- **Voce 147, enigma di verità e menzogna** — dove «sono un furfante» è autoreferenza messa in bocca a un personaggio, e serve come strumento.
- **Voce 157, enigma di teoria dei giochi** — la fonte segnala che nella teoria dei giochi si producono comportamenti indefiniti quando **due giocatori devono modellare l'uno lo stato mentale dell'altro, portando a un regresso infinito.** È lo stesso anello, con due teste invece di una.
- **Voce 122, acrostico** — l'altra forma dell'elenco in cui un testo dice qualcosa che si legge nel testo stesso, ma lì non è un'affermazione.
- **Voce 84, quiz** — la forma di pagina da cui questa prende l'aspetto e non il contenuto.

Con il capitolo 12, giochi di parole e enigmistica italiana non c'è confine, ed è il caso in cui sembrerebbe di sì: esistono frasi che contano le proprie lettere, e sarebbero un gioco di parole — ma nessuna delle voci del capitolo 12 già scritte le nomina, e per un sistema che non sa contare le lettere dentro le parole quella famiglia è comunque fuori portata. Con il capitolo 13, giochi matematici e ricreativi non c'è confine: nessuna sua voce riguarda l'autoreferenza.

## Che cosa se ne sa

**L'autoreferenza è lo strumento con cui si dimostrano i limiti dei sistemi, e la fonte lo dice come una cosa sola.** «In matematica e in teoria della calcolabilità, l'autoreferenza è il concetto chiave nel dimostrare i limiti di molti sistemi.» Il teorema di Gödel la usa per mostrare che nessun sistema formale coerente della matematica può contenere tutte le verità matematiche, perché non può dimostrare certe verità sulla propria struttura. Il problema della fermata mostra che **c'è sempre un compito che un calcolatore non può eseguire, e cioè ragionare su sé stesso.**

**Addomesticare l'autoreferenza è una delle grandi riuscite dell'informatica, e la frase più bella riguarda la memoria.** La fonte: «l'hardware fa un uso fondamentale dell'autoreferenza nei flip-flop, le unità elementari della memoria digitale, che **convertono relazioni logiche potenzialmente paradossali in memoria distendendo i loro termini nel tempo.**» Un anello che gira in tondo, se lo si lascia girare nel tempo invece che in un istante, smette di essere un paradosso e diventa un ricordo. **È l'osservazione più utile raccolta in questo blocco**, e non riguarda solo l'elettronica: è la stessa mossa già vista alla voce 115, indovinello della persona, dove togliere il tempo a una descrizione produce un enigma. Qui il tempo si rimette, e l'enigma diventa una cosa che funziona.

**C'è un paradosso di Russell dentro una banca dati viva, e ha un numero.** L'enciclopedia in rete delle successioni di interi contiene A053873, «i numeri *n* tali che la successione A*n* contiene *n*», e A053169, «*n* sta in questa successione se e solo se *n* non sta nella successione A*n*». Ogni numero appartiene esattamente a una delle due. Con due eccezioni: **non si può stabilire se 53873 appartenga a A053873** — l'una o l'altra decisione sarebbe coerente —, e **si può dimostrare che 53169 sia e non sia membro di A053169**, che è una forma del paradosso di Russell. Sloane racconta di aver resistito a lungo prima di accettare successioni definite in termini della numerazione dell'enciclopedia stessa, «in parte per il desiderio di mantenere la dignità della banca dati». **Una banca dati di 390 000 voci contiene due voci su cui non ha autorità**, e sono lì.

**Autoreferenza e contraddizione sono cose diverse, e la fonte le separa con due frasi vicine.** «Questa frase è scritta in inglese» è autoreferenziale, vera, non paradossale. «Questa frase è scritta in francese» è autoreferenziale e contraddittoria, e non è un paradosso: **è semplicemente falsa.** Serviva già alla voce 151, paradosso, e serve qui al contrario: è la ragione per cui esiste una forma di gioco e non solo una famiglia di guasti.

**Nella teoria dei giochi l'autoreferenza produce regresso infinito.** Quando due giocatori devono modellare ciascuno lo stato mentale dell'altro, si ottengono comportamenti indefiniti. È lo stesso oggetto della voce 146, enigma di cappelli — dove la catena «tutti sanno che tutti sanno» è invece una risorsa, perché è **finita**: si ferma al numero dei partecipanti. La differenza fra le due situazioni è tutta lì.

**Il gusto per l'autoreferenza è un tratto culturale documentato di un mestiere.** «Pensare in termini di autoreferenza è una parte pervasiva della cultura dei programmatori, con molti programmi e sigle chiamati auto-referenzialmente come forma di umorismo»: GNU per *GNU's not Unix*, PINE per *Pine is not Elm*, e il GNU Hurd che è chiamato con una coppia di sigle che si riferiscono l'una all'altra. Il requisito «scarica il sorgente» della licenza GNU Affero, dice la fonte, **si basa sull'idea del quine.**

**Nessuna misura su chi risolve.** In nessuna delle pagine lette c'è un dato su quanto sia difficile un quiz auto-referenziale, per chi, o a quale età si possa affrontare. È l'ultima voce di questo capitolo e la situazione è la stessa della prima.

## Esempi trovati

Da Magritte, *Il tradimento delle immagini*: le parole «questa non è una pipa» sotto una pipa dipinta, e la fonte annota il punto — **la verità della frase dipende interamente da che cosa indichi «questa»**: la pipa disegnata, il quadro, la parola, o la frase stessa.

Da Escher: mani che disegnano sé stesse.

Da Omero, e la fonte lo dà come forse l'esempio più antico: nell'*Iliade* Elena si lamenta che «per generazioni non ancora nate vivremo nel canto» — dentro il canto stesso.

Da Beckett, *L'ultimo nastro di Krapp*: un uomo che ascolta e registra sé stesso, soprattutto a proposito di altre registrazioni.

Da Calvino, *Se una notte d'inverno un viaggiatore*, che la fonte elenca insieme al *Don Chisciotte*, alla *Tempesta*, a *Jacques il fatalista* e ai *Sei personaggi in cerca d'autore*.

Dalla BBC che dà notizia dei tagli al personale della BBC; e da Wikipedia che ha una voce su Wikipedia.

Dai miti di creazione: l'Ouroboros che si mangia la coda, e il dio egizio che inghiotte il proprio seme per creare sé stesso — che sono, dice la fonte, il modo in cui i miti risolvono il problema di che cosa abbia creato il creatore.

## Un esempio giocabile

Un quiz auto-referenziale ha una difficoltà che nessun'altra forma di questo blocco ha: **chi lo costruisce non può scegliere le risposte, perché le risposte dipendono dalle risposte.** Si scrivono le domande e poi si scopre che cosa esce — o che non esce niente, o che ne escono due. Questo ha tre domande, ventisette combinazioni possibili, e **una sola combinazione coerente**, verificata a mano su tutte e ventisette.

> **Tre domande che parlano di sé stesse**
>
> Ogni domanda si risponde con **A**, **B** o **C**. Una risposta è giusta quando, **dopo che hai riempito tutte e tre**, quello che dice è vero.
>
> ```
>  1. Il numero di risposte B di questo foglio e':
>       A) nessuna     B) una     C) due
>
>  2. Il numero di risposte C di questo foglio e':
>       A) nessuna     B) una     C) due
>
>  3. Quante domande hanno la stessa risposta della
>     domanda che le sta appena sopra?
>       A) nessuna     B) una     C) due
> ```
>
> ```
>   1 ────      2 ────      3 ────
> ```
>
> ---
>
> **Se ti sei impuntato, ecco tutte le possibilità.** Sono ventisette, e non ce ne sono altre. Per ognuna leggi le tre lettere come le tre risposte, controlla se tutte e tre dicono il vero, e cancella la riga se anche una sola non torna.
>
> ```
>   AAA ──      BAA ──      CAA ──
>   AAB ──      BAB ──      CAB ──
>   AAC ──      BAC ──      CAC ──
>   ABA ──      BBA ──      CBA ──
>   ABB ──      BBB ──      CBB ──
>   ABC ──      BBC ──      CBC ──
>   ACA ──      BCA ──      CCA ──
>   ACB ──      BCB ──      CCB ──
>   ACC ──      BCC ──      CCC ──
> ```
>
> Alla fine deve restarne **una sola**. Se te ne restano due, hai sbagliato una riga; se non te ne resta nessuna, pure.
>
> ---
>
> **E poi, la parte che nessun'altra pagina di questo genere ti chiede.**
>
> ```
>  Scrivi tu una quarta domanda, che parli di questo
>  foglio come fanno le altre tre.
>
>  4. ─────────────────────────────────────────────
>     A) ───────  B) ───────  C) ───────
> ```
>
> Poi rifai il conto. **Attento: adesso le combinazioni sono ottantuno, e la tua domanda potrebbe averne lasciate in piedi due, oppure nessuna.** Se non ne resta nessuna, il tuo foglio non è difficile: è impossibile, e va cambiata una domanda. Se ne restano due, il foglio ha due risposte giuste, e in gergo scacchistico si direbbe che è cotto.

**La risposta è C, B, B, e l'ho verificata su tutte e ventisette le combinazioni.** Con quelle tre lettere: le risposte B sono due — la seconda e la terza —, e la prima domanda dice «due», che è vero; le risposte C sono una — la prima —, e la seconda domanda dice «una», che è vero; le coppie di domande consecutive sono due, la seconda contro la prima (B contro C, diverse) e la terza contro la seconda (B contro B, uguali), quindi una sola coppia coincide, e la terza domanda dice «una», che è vero.

L'enumerazione si abbrevia, e vale la pena scriverla perché è la dimostrazione. La seconda domanda fissa quante C ci sono in tutto, e questo taglia le ventisette combinazioni in tre gruppi da quattro più quelle immediatamente incoerenti. Se la seconda risposta è A, non ci sono C da nessuna parte e restano quattro combinazioni, tutte scartate dalla terza domanda o dalla prima. Se è C, le C devono essere due e restano quattro combinazioni, tutte scartate. **Se è B, c'è esattamente una C fra la prima e la terza risposta**, e delle quattro combinazioni possibili tre cadono sul conto delle B; l'unica che regge è C, B, B.

La cosa che rende questa forma diversa da tutte le altre di questo blocco sta nella costruzione, e non nella soluzione. **Chi scrive un quiz auto-referenziale non decide le risposte**: scrive le domande e poi scopre che cosa ne esce, e quello che esce può essere una risposta, nessuna, o molte. È il caso più netto raccolto in tutta l'enciclopedia di **un autore che non sa che cosa sta scrivendo finché non lo verifica**, e l'ultima parte del foglio consegna esattamente quella esperienza invece di raccontarla.

Il numero ventisette è dichiarato apposta. Tre risposte con tre possibilità fanno 3×3×3, il conto si rifà in testa, e stampare tutte le combinazioni rende il foglio finito: **non c'è nessun modo di restare bloccati, perché la strada peggiore — provarle tutte — è stampata.** È la quarta e ultima verifica esaustiva di questo blocco, e la più letterale.

Il limite tecnico da dichiarare è lo stesso delle tre voci precedenti, in una forma più stretta: **costruire un quiz auto-referenziale con una sola risposta coerente non è affidabile**, perché la coerenza è una proprietà da controllare su tutte le combinazioni. Questo è stato costruito e controllato a mano, e con quattro domande da tre risposte le combinazioni diventano ottantuno — ancora fattibili a mano, ma non a occhio.

Su un pannello di poche righe corte una domanda auto-referenziale ci sta e sarebbe giusta lì: «questo pannello contiene quante lettere A?» è una consegna completa in quarantatré caratteri. Ma è anche una domanda che richiede di contare le lettere dentro le parole, e quel conto va fatto a mano.

## Che cosa la rende interessante

**Un anello disteso nel tempo smette di essere un paradosso e diventa memoria.** È la frase della fonte sui flip-flop, ed è la cosa più riusabile di questa voce. Alla voce 115, indovinello della persona si era osservato che **togliere il tempo a un processo produce un enigma**; qui il tempo si rimette a un anello e produce un dispositivo che funziona. **Sono la stessa operazione nei due sensi**, e adesso l'enciclopedia le ha tutte e due. Da provare su ogni forma dell'elenco che giri in tondo.

**Chi costruisce non sa che cosa sta costruendo finché non verifica.** In tutte le altre forme dell'elenco l'autore sceglie la risposta e poi nasconde la strada; qui scrive le domande e la risposta esce da sola, oppure non esce. **È il caso limite del costo di produrre contro il costo di risolvere**, tema di tutto questo blocco, ed è quello in cui i due costi non sono nemmeno confrontabili: risolvere è controllare ventisette righe, costruire è non sapere se ne resterà una.

**Una banca dati viva contiene due voci su cui non ha autorità.** A053873 e A053169 nell'enciclopedia delle successioni di Sloane. Non è un gioco: è un paradosso di Russell dentro un archivio di 390 000 voci consultato da matematici veri, e il curatore racconta di aver esitato per anni ad accettarlo. **Una raccolta abbastanza grande finisce per contenere qualcosa che parla di sé**, e il modo di trattarlo è dichiararlo invece di toglierlo.

**Un quiz auto-referenziale è l'unica forma di questo capitolo che non richieda di sapere niente.** Non serve la lingua, non servono gli scacchi, non serve la matematica, non serve nessun repertorio culturale: servono tre lettere e la pazienza di controllare. **Nessun'altra delle 83 voci del capitolo ha questa proprietà**, e la sola che ci si avvicini è la famiglia dei giochi Nikoli della voce 154, sudoku e affini (Nikoli), che ci arriva per una via diversa.

**Un'affermazione che parla di sé può essere vera, falsa, indecidibile o coerente in due modi.** Sono quattro esiti, non due, e la fonte li mostra tutti e quattro con esempi. L'enciclopedia ha trattato l'autoreferenza come un guasto fino a questa voce; **è invece un materiale con quattro comportamenti, e tre dei quattro si possono consegnare.**
