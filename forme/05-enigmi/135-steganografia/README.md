# Steganografia

- **Numero** 135 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi verbali»
- **Si chiama anche** scrittura coperta, messaggio nascosto, testo di copertura, cifrario nullo, *null cipher*, *concealment cipher*, *cover text*, *stegotesto*
- **In una riga** un messaggio nascosto dentro un altro.
- **Fonti** `steganography.txt`, `null-cipher.txt` e `cardan-grille.txt`, prese il 30 agosto 2026 da en.wikipedia
- **Stato della ricerca** fatta, 30 agosto 2026

## Che cos'è

Un messaggio che sta dentro un altro messaggio, in modo che chi guarda non si accorga che ci sia qualcosa da leggere. È la differenza dichiarata rispetto alla crittografia, e `steganography.txt` la mette in una riga: **la crittografia protegge il contenuto di un messaggio, la steganografia nasconde anche il fatto che un messaggio ci sia.** Un testo cifrato attira l'attenzione proprio perché è illeggibile; un testo di copertura ben fatto non attira niente.

Parti mobili:

- **Il testo di copertura.** Deve avere un motivo indipendente di esistere. Una lettera, un elenco della spesa, un articolo di giornale: qualcosa che uno scriverebbe comunque.
- **La regola di estrazione.** La prima lettera di ogni parola; la terza lettera dopo ogni segno di punteggiatura; una parola ogni cinque. È la chiave, e non sta nel foglio.
- **La densità.** Quante lettere del testo portano il messaggio e quante sono riempitivo. Più il messaggio è corto rispetto alla copertura, più è facile nasconderlo — `steganography.txt` lo dice con l'immagine del pagliaio: più grande è il pagliaio, meglio sta l'ago.
- **Se chi guarda sa che c'è qualcosa.** Questa è la parte mobile più importante e la sola che cambia il gioco per intero. Un compito che dice «qui dentro c'è un messaggio» non è steganografia: è un cifrario con una regola strana. La steganografia vera è quando nessuno lo dice.

Se si toglie il testo di copertura resta un cifrario. Se si toglie la regola di estrazione resta un testo qualunque. Se si toglie la segretezza della regola resta un gioco, e funziona lo stesso.

## Da dove viene

I primi due casi registrati sono in Erodoto, intorno al 440 a.C. Istieo fece radere la testa del suo servo più fidato, scrisse il messaggio sul cuoio capelluto, aspettò che i capelli ricrescessero e lo mandò da Aristagora con l'istruzione di farsi radere di nuovo. Demarato scrisse l'avvertimento di un attacco direttamente sul legno di una tavoletta e poi ci stese sopra la cera, che a quel tempo era la superficie su cui si scriveva.

Enea Tattico, nello stesso periodo, elenca venti metodi di comunicazione segreta in un manuale sulla difesa delle fortificazioni: fra questi il **cifrario a puntini di spillo**, cioè bucare con un ago le lettere che compongono il messaggio dentro un testo qualunque. Chi riceve annota le lettere bucate e le mette in fila.

La parola nasce nel 1499 con Johannes Trithemius, che intitola *Steganographia* un trattato che sembra un libro di magia sull'evocazione degli angeli e non lo è: ogni angelo corrisponde a un metodo diverso di scrittura nascosta. Il libro gli costò l'accusa di conversare con i demoni. La *Clavis* pubblicata nel 1606 spiegava come estrarre il segreto dai libri I e II — si prende un'incantazione e si legge una lettera sì e una no, di una parola sì e una no. Il libro III restò considerato un'opera di magia **fino alla fine degli anni Novanta**, quando Jim Reeds e Thomas Ernst, indipendentemente, scoprirono che anche quello era steganografia. Sono quasi quattrocento anni in cui il nascondiglio ha retto.

Il termine tecnico per la variante scritta è **cifrario nullo**: il testo in chiaro è mescolato a una grande quantità di materiale che non conta niente, e per leggerlo si scarta quasi tutto. `null-cipher.txt` lo classifica come una delle tre categorie della crittografia classica, accanto alla sostituzione e alla trasposizione, e nota che è la meno conosciuta delle tre.

## Varianti e parenti

- **Cifrario nullo** — il messaggio è dentro il testo, e si estrae scartando. La variante scritta più comune.
- **Cifrario a puntini** — le lettere che contano sono segnate con un foro di spillo o un punto. Nell'Inghilterra dell'Ottocento si bucavano i giornali per spedire lettere senza pagare l'affrancatura.
- **Steganografia sociale** — nascondere il messaggio in un modo di dire, in un riferimento di cultura popolare, in un nome scritto male. `steganography.txt` la descrive come pratica di comunità sottoposte a censura: il contesto sociale è la chiave.
- **Voce 122, acrostico** — le iniziali dei versi compongono una parola. `null-cipher.txt` dichiara l'acrostico nascosto una forma di cifrario nullo, e l'acrostico dichiarato no.
- **Voce 141, griglia di Cardano** — la regola di estrazione è un oggetto invece di una frase.
- **Voce 136, inchiostro invisibile / luce** — il messaggio non è dentro un altro testo, è sulla stessa carta in una condizione che non si vede.
- **Voce 139, testo troppo piccolo / troppo grande** — il microfilm ridotto a un punto di stampa è steganografia per dimensione.
- **Voce 129, cifrario a sostituzione** — l'opposto dichiarato: si vede che c'è un messaggio e non si legge.
- **Voce 384, mimetismo e camuffamento** — la stessa idea applicata a un'immagine invece che a un testo.
- **Voce 388, oggetto nascosto in piena vista** — la lettera rubata di Poe, che è steganografia senza scrittura.
- **Filigrana digitale** — sembra la stessa cosa e non lo è. Nella steganografia il messaggio deve arrivare intatto; in una filigrana deve resistere a chi cerca di toglierlo, e a volte deve rompersi apposta per denunciare la manomissione.

## Che cosa se ne sa

**Il testo di copertura è la parte difficile, non il messaggio.** Tutte e due le fonti lo dicono, e da lati diversi. `null-cipher.txt`: produrre testi di copertura che sembrino naturali e non insospettiscano è difficile e richiede tempo. `cardan-grille.txt`: «una lingua stentata attira l'attenzione su di sé», e Cardano stesso raccomandava di riscrivere il testo **tre volte** per smussare le irregolarità che tradiscono le parole nascoste. Questo conferma da una terza strada l'osservazione lasciata dalle voci 132, Morse, 133, braille come cifra visiva e 134, semaforo, bandiere, alfabeti alternativi: quello che separa il segno dal rumore che lo copre è il lavoro vero.

**Si smaschera con l'orecchio prima che con l'analisi.** `cardan-grille.txt` dice che un messaggio fatto male si nota per la lingua stentata e per la scrittura irregolare; `invisible-ink.txt`, dalla parte dell'inchiostro, aggiunge che una parola fuori posto come «calore» in una lettera normale può bastare a mettere in allarme un censore. La verifica di una steganografia non è tecnica: si legge il testo ad alta voce e si sente se suona.

**Chi controlla non deve leggere: deve solo restringere il campo.** `steganography.txt` descrive la contromisura fisica — lente d'ingrandimento, reagenti chimici, luce ultravioletta — e dice che è un processo lento con implicazioni evidenti di risorse. Il punto non è che sia impossibile trovare il messaggio: è che nessuno può dedicare ore a ogni foglio. Da qui segue una regola generale sulla forma: **la steganografia non protegge dal controllo, protegge dalla selezione per il controllo.**

**Il caso più curioso di contromisura è la carta.** Nella seconda guerra mondiale i campi di prigionia americani e canadesi davano ai prigionieri tedeschi carta da lettere trattata — i tre prototipi si chiamavano Sensicoat, Anilith e Coatalith — che rendeva visibile qualunque inchiostro invisibile. Morris S. Kantrowitz, direttore tecnico dell'ufficio stampe del governo americano, ne descrisse lo sviluppo sul *Paper Trade Journal* del 24 giugno 1948, e i brevetti sono due, del 1948 e del 1950. Una variante più semplice: carta rigata con un inchiostro solubile in acqua, che sbava appena qualcuno ci scrive sopra con un inchiostro a base d'acqua. **Il supporto che denuncia il messaggio è un'idea che l'enciclopedia non aveva ancora incontrato.**

**Il costo di scrivere e il costo di leggere sono asimmetrici, e in senso contrario a quello dei cruciverba.** Alla voce 125, cruciverba si era osservato che costruire costa più che risolvere. Qui la differenza è più netta: estrarre un messaggio nascosto, quando si conosce la regola, è meccanico e non richiede ingegno; comporre il testo di copertura è un lavoro di scrittura vero. Chi riceve non fa quasi niente.

## Esempi trovati

Da un telegramma tedesco della prima guerra mondiale, riportato da `null-cipher.txt`: un messaggio di ventidue parole che parla di embarghi, situazioni gravi e diritto internazionale. Prendendo l'iniziale di ogni parola si legge che una certa nave salpa da New York a giugno. Il testo di copertura ha esattamente il tono dei telegrammi diplomatici che circolavano in quei mesi, ed è per quello che passò.

Dalla guerra civile inglese: una lettera a Sir John Trevanian, prigioniero dei puritani a Colchester, lunga una pagina e piena di consolazioni. La terza lettera dopo ogni segno di punteggiatura dice che un pannello all'estremità est della cappella scorre. Trevanian chiese di poter pregare da solo nella cappella e non lo videro più.

Da un caso dell'FBI riportato nella stessa pagina: una lettera di un detenuto, apparentemente su un programma di disintossicazione e una causa per l'affidamento dei figli. Una parola ogni cinque compone l'ordine di aggredire qualcuno. È l'esempio che mostra meglio la differenza fra la forma e il suo uso: la stessa struttura di un gioco da settimanale.

Da Trithemius: l'*Ave Maria*, in *Polygraphiae*. Circa 384 alfabeti di ventiquattro lettere, dove ogni lettera corrisponde a una parola di lode a Dio. Il messaggio cifrato esce come una preghiera latina che si può recitare senza che nessuno sospetti niente.

Dalle stampanti a colori: HP, Xerox e altri stampano su ogni pagina una griglia di puntini gialli quasi invisibili che contengono numero di serie, data e ora. Non è un gioco e nessuno ha chiesto il permesso: è steganografia industriale, e sta su ogni foglio a colori uscito da quelle macchine.

## Una nostra versione

La forma chiede di comporre un testo con vincoli di posizione — la prima parola di ogni riga, la terza lettera dopo ogni virgola — e **questo il sistema non lo sa fare né verificare** (misurato, `ideas/10 §6`). Quindi il compito si gira: il sistema stampa la cornice e la regola, e a scrivere è chi legge. La verifica arriva da fuori, perché il messaggio è per qualcuno.

> **Una lettera che dice due cose**
>
> Nel 1917 un tedesco spedì un telegramma su embarghi e diritto internazionale. Prendendo l'iniziale di ogni parola si leggeva il nome di una nave e la data in cui salpava. Chi lo lesse per mestiere non se ne accorse, perché nessuno gli aveva detto di guardare le iniziali.
>
> Adesso tocca a te, e la regola è più facile: **la prima parola di ogni riga.**
>
> Prima decidi il messaggio nascosto. Deve essere per qualcuno che sta in questa casa, e deve essere una cosa che gli vuoi dire davvero — sette o otto parole, non di più. Scrivilo qui, in matita, e poi cancellalo quando hai finito:
>
> ```
>  ─────── ─────── ─────── ─────── ─────── ─────── ───────
> ```
>
> Poi scrivi la lettera. Ogni riga comincia con la parola successiva del messaggio. La lettera deve parlare d'altro e deve reggersi da sola: se qualcuno la legge senza sapere niente, non deve trovarla strana.
>
> ```
>  1 ────────────────────────────────────────────────────
>  2 ────────────────────────────────────────────────────
>  3 ────────────────────────────────────────────────────
>  4 ────────────────────────────────────────────────────
>  5 ────────────────────────────────────────────────────
>  6 ────────────────────────────────────────────────────
>  7 ────────────────────────────────────────────────────
>  8 ────────────────────────────────────────────────────
> ```
>
> Quando hai finito, **rileggila ad alta voce.** Cardano, che di questo mestiere sapeva, diceva di riscrivere il testo tre volte per togliere le storture. Una frase che comincia con la parola sbagliata suona sempre un po' storta, e quella è la parte che ti tradisce.
>
> Poi ritaglia questo pezzo e dallo alla persona a cui è indirizzata. Solo a lei.
>
> ```
>  ┌──────────────────────────────────────┐
>  │  la prima parola di ogni riga        │
>  └──────────────────────────────────────┘
> ```
>
> Una domanda per dopo: la persona ha letto il messaggio giusto, o ne ha letto un altro? Se ne ha letto un altro, dove si era rotta la riga?

Il sistema stampa la regola, otto righe numerate e un cartellino da ritagliare, e non tocca nessuna lettera. Il vincolo di posizione lo esegue una mano. La verifica non è nel foglio: è nella faccia di chi riceve il cartellino e legge. E il compito ha l'uso non enigmistico che rende praticabile tutta questa famiglia — **non c'è niente da indovinare, c'è una cosa da dire a qualcuno.**

La riga finale è la riga già raccolta quindici volte: dove il ragionamento ha vacillato, chiesta qui a una persona che non sapeva che cosa si stesse verificando.

## Da riprendere alla rassegna

**La steganografia è l'unica forma dell'elenco in cui il compito, per esistere, deve non annunciarsi.** Un foglio che dice «qui c'è un messaggio nascosto» ha già distrutto la proprietà che definisce la forma. Questo confligge in modo diretto con un sistema che stampa consegne, e la via d'uscita trovata qui — girare il compito dalla parte di chi scrive — la aggira invece di risolverla. Alla rassegna vale la pena chiedersi se esista un modo onesto di consegnare a qualcuno una cosa senza dirgli che gliela si sta consegnando.

**Il supporto che denuncia il messaggio.** La carta Sensicoat rende visibile quello che ci si scrive sopra di nascosto. È l'inverso del controllo dell'errore nel materiale: invece di dire se il lavoro è venuto bene, dice se c'era un lavoro. Nessuna forma dell'enciclopedia usa questa idea, e in una casa avrebbe un significato che va guardato con attenzione.

**Il testo di copertura come esercizio di scrittura.** Comporre otto righe che si reggano da sole e comincino ognuna con una parola imposta è un vincolo formale nel senso del capitolo 7, che è ancora vuoto. La differenza con il lipogramma della voce 124, lipogramma è che qui il vincolo ha un motivo: non è una regola di gara, è un messaggio da consegnare.

**Quattrocento anni di nascondiglio che ha retto.** Il libro III della *Steganographia* è stato letto per la prima volta alla fine degli anni Novanta. Da guardare accanto all'anagramma di priorità della voce 121, anagramma: sono i due casi in cui la forma ha funzionato *perché* nessuno l'ha risolta.

Da verificare: la data e il testo esatto del telegramma tedesco, che `null-cipher.txt` riporta senza fonte primaria; e il seguito della storia di Trevanian, che nella pagina è dato per assodato ma con un solo riferimento.
