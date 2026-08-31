# Punti

- **Numero** 256 nell'enciclopedia, capitolo 9 — Meccaniche di gioco
- **Si chiama anche** punteggio, score, gettoni, crediti, XP, punti esperienza, monete, stelline, bollini, *points*
- **In una riga** ogni cosa fatta vale un numero, e i numeri si sommano.
- **Fonti** `gamification.txt`, `high-score.txt` (che è la stessa pagina di `score-gaming.txt`), `experience-point.txt`, `token-economy.txt`, `overjustification-effect.txt`, `behavior-management.txt`, `it-gamification.txt`, lette il 31 agosto 2026. I conti sui totali sono nostri, verificati in `build/check_256.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

A ogni cosa che si può fare è associato un numero. Chi la fa incassa quel numero. I numeri incassati si sommano, e il totale è quello che si guarda.

**Questo capitolo comincia qui, e le prime quattro voci vanno tenute separate su un asse solo: che cosa produce il numero.** Nei punti il numero è **una somma**: cresce di quanto si è fatto e non ha un tetto naturale. Nella voce 257, livelli il numero è **una soglia superata**, cioè un gradino ricavato dalla somma. Nella voce 258, distintivi / badge non c'è né somma né soglia ma **un fatto avvenuto una volta**, che è vero o falso. Nella voce 259, classifica il numero di ciascuno non cambia affatto: cambia che adesso ha **un posto rispetto agli altri**. L'asse regge sulle fonti e non è stato deciso a tavolino: `gamification.txt` definisce i punti come ciò che «rappresenta numericamente il progresso di chi gioca», i distintivi come «rappresentazioni visive di risultati raggiunti», e le classifiche come ciò che «ordina i giocatori secondo il loro successo relativo».

**L'asse ha una crepa, ed è dichiarata dalla stessa pagina:** un distintivo può essere assegnato al raggiungimento di un certo numero di punti, e allora poggia su una somma. Le quattro forme si sovrappongono in pratica; l'asse serve a dire che cosa ognuna aggiunge, non a sostenere che si trovino separate.

Parti mobili:

- **Il tariffario.** Quanto vale ogni cosa. È la parte che dichiara che cosa conta, e la dichiara più chiaramente di qualunque frase.
- **Se si spendono.** Un punto che resta è una misura; un punto che si spende è una moneta, e le due cose si comportano in modo opposto.
- **Se si perdono.** La sottrazione di punti ha un nome tecnico — *response cost* — e cambia la forma in profondità.
- **Chi tiene il conto.** Un totale ha bisogno di qualcuno o qualcosa che se lo ricordi da una volta all'altra.
- **Se il totale ha un tetto.** Senza tetto la cosa non finisce mai; con un tetto diventa un obiettivo.
- **Quanto sono grandi i numeri.** Dieci punti e diecimila punti fanno lo stesso lavoro aritmetico e non lo stesso effetto.

## Da dove viene

**Da due posti diversi, e non si sono mai incontrati fino a poco fa.**

Il primo è la sala giochi. `high-score.txt`: il punteggio nei videogiochi è «una quantità astratta associata a un giocatore o a una squadra», misurata in punti, e nell'epoca dei cabinati aveva un peso che oggi non ha più — perché per limiti tecnici quei giochi **non si potevano vincere né finire**, erano cicli di gioco senza fine, e il punteggio era l'unica cosa che distinguesse una partita da un'altra. La stessa pagina segnala che nei giochi moderni il punteggio è spesso «una componente laterale e facoltativa»: si può giocare ignorandolo.

Il secondo è il laboratorio di psicologia, e lì i punti si chiamano gettoni. `token-economy.txt`: un'economia a gettoni è un sistema di gestione delle contingenze basato sul rinforzo sistematico di un comportamento stabilito. Ha **tre requisiti di base** — i gettoni, i rinforzatori di scambio, e i comportamenti bersaglio specificati — e la pagina elenca che cosa si è usato come gettone nella pratica: monete, segni di spunta, immagini di piccoli soli o di stelle, punti su un contatore, crocette su un cartellone. Sono oggetti «comparabilmente privi di valore fuori dal rapporto fra paziente e clinico o fra insegnante e studente», e il loro valore sta tutto nel fatto di essere scambiabili con altro.

**La riga che questa voce deve portare è nella definizione di che cosa *non* è un'economia a gettoni.** La pagina è esplicita: un operatore che dà gettoni a qualcuno solo perché gli sembra che si stia comportando bene **non sta facendo un'economia a gettoni**, perché non lo sta facendo in modo sistematico. I criteri devono essere specificati e chiari; se il comportamento bersaglio è rifare il letto, chi dà e chi riceve devono sapere che aspetto ha un letto ben fatto. La pagina ammette poi che la specifica è spesso difficile: «mangiare in modo educato» e «collaborare positivamente» sono comportamenti che non si riescono a definire.

Il terzo posto è il gioco di ruolo, e da lì viene il nome più diffuso. `experience-point.txt`: il termine *experience point* è di Gary Gygax e Dave Arneson, in *Dungeons & Dragons*; Arneson aveva introdotto un sistema di avanzamento di livello giocando a una modifica di *Chainmail*. L'abbreviazione naturale, EP, era già occupata da *electrum pieces*, un pezzo del sistema monetario del gioco; **XP fu suggerita da Lawrence Schick, una delle prime persone assunte alla TSR**, per far finire i manuali in tempo.

La parola *gamification* compare in rete nel contesto del software nel 2008 e non diventa comune fino al 2010 (`gamification.txt`). La pagina italiana aggiunge un dettaglio e insieme lo smentisce: la ludicizzazione «è divenuta nota al grande pubblico nel febbraio 2010» grazie alla conferenza di Jesse Schell al D.I.C.E. Summit di Las Vegas, «anche se il termine non venne mai utilizzato in quel discorso» (`it-gamification.txt`).

## Varianti e parenti

- **Punti che si accumulano** — il totale sale e basta. È il punteggio da sala giochi.
- **Punti da spendere** — si incassano e si consumano per comprare qualcosa. È l'economia a gettoni, ed è anche il sistema *cash-in* di certi giochi di ruolo, dove i punti spesi vengono cancellati dalla scheda del personaggio.
- **Punti riscattabili, punti di reputazione, punti esperienza** — le tre famiglie che `gamification.txt` distingue per la funzione che svolgono.
- **Sottrazione di punti (*response cost*)** — una multa in gettoni per un comportamento indesiderato, dichiarata prima che il sistema parta.
- **Punti risparmiati** — l'economia a gettoni li usa per dividere un premio grosso in parti, così che si possa mettere da parte invece di spendere subito.
- **Moltiplicatori** — il numero del livello che moltiplica i punti, i bonus di tempo, le combinazioni riuscite di fila.
- **Voce 257, livelli** — la soglia ricavata dal totale.
- **Voce 258, distintivi / badge** — il fatto avvenuto una volta, che non si somma.
- **Voce 259, classifica** — il confronto, che non produce il numero ma lo ordina.
- **Voce 53, contare** — perché un punteggio è prima di tutto un conteggio, e i conteggi si possono sbagliare in modo sistematico.
- **Voce 244, autovalutazione con rubrica** — la griglia a criteri, che è la stessa aritmetica applicata a un giudizio.

## Che cosa se ne sa

**La cosa più solida che si sappia sui punti non riguarda i punti: riguarda che cosa succede quando si tolgono.** `overjustification-effect.txt`: dare un incentivo esterno atteso per un'attività che era già gratificante di per sé può ridurre la motivazione a farla. Il primo esperimento è di Edward Deci, 1971: chi risolveva un rompicapo veniva osservato durante la pausa in tre giornate. Il gruppo di controllo non era pagato mai; il gruppo sperimentale non era pagato il primo giorno, era pagato il secondo, e non era pagato il terzo. Il secondo giorno il gruppo pagato passò significativamente più tempo del controllo sul rompicapo durante la pausa; **il terzo giorno, tolto il pagamento, ne passò significativamente meno.**

**La fonte dà la direzione e non la grandezza**, ed è il rovescio da dichiarare: «significativamente più» e «significativamente meno» sono quello che c'è scritto, e nessun numero accompagna il risultato nella pagina.

**Dove invece un numero c'è, il risultato è più interessante di quanto sembri.** Un esperimento della Southern Methodist University su **188 studentesse universitarie**: un gruppo era pagato in base alla competenza — chi andava sopra la media prendeva di più, chi andava sotto prendeva di meno —, l'altro era pagato per il solo completamento, in proporzione alle ripetizioni o alle ore. Poi a metà di ciascun gruppo fu detto che aveva fatto bene e all'altra metà che aveva fatto male, **indipendentemente da come avesse fatto davvero.** Il primo gruppo continuò a giocare più a lungo del secondo. La conclusione della pagina: quando la ricompensa non riflette la competenza, più ricompensa dà meno motivazione; **quando la riflette, più ricompensa dà più motivazione.**

**Non è vero che i punti tolgano sempre qualcosa, e la fonte lo dice con due eccezioni precise.** Una meta-analisi del 2001 riporta che le ricompense possono **aumentare** la motivazione intrinseca per compiti che ne suscitavano poca all'inizio; e le ricompense date per un compito che non interessava, o per aver fatto meglio di altri, aumentano la motivazione invece di ridurla. La stessa pagina segnala che alcune attività richiedono un livello di padronanza prima che la loro attrattiva si veda, e che in quei casi un incentivo esterno serve ad arrivarci — citando proprio le economie a gettoni come esempio in cui ha funzionato.

**L'età sposta il risultato, e il verso è quello che rende la cosa rilevante qui.** L'effetto negativo delle contingenze esterne sulla motivazione intrinseca «sembra più severo per i bambini che per gli studenti universitari». La spiegazione proposta è che gli universitari abbiano una maggiore capacità cognitiva di separare la parte informativa da quella di controllo di una ricompensa. **Sull'adolescenza, che sta in mezzo, le pagine lette non dicono niente: va verificato.** E il quadro non è pulito nemmeno per i bambini: Feingold e Mahoney, 1975, non trovarono nessuna riduzione della motivazione intrinseca in bambini dopo l'introduzione di ricompense a gettoni in un'attività di gioco.

**Il fatto che decide se il danno c'è si chiama contingenza, ed è la parte praticabile di tutta questa letteratura.** Se la ricompensa è chiaramente legata al fare il compito — *task-contingent* — chi la riceve è meno propenso ad attribuire il proprio comportamento a un interesse genuino. Se è slegata dal compito, per esempio data per la sola partecipazione, il collegamento non si forma e la motivazione intrinseca resta dov'era. Sono due tariffari diversi, e la differenza è nel testo del tariffario.

**Sull'efficacia dei punti come strumento di condotta c'è un numero, ed è vecchio e generico.** `behavior-management.txt` riporta che Cotton, 1988, ha passato in rassegna **37 studi** su gettoni, lodi e altri sistemi di ricompensa, trovandoli efficaci nella gestione del comportamento in classe. La pagina non dà una grandezza, non dice quali studi, e non distingue i gettoni dalla lode: **è una direzione, non una misura.**

**Un totale è una somma, e una somma perde per costruzione l'informazione su che cosa si sia fatto.** Con sei cose che valgono 1, 1, 2, 3, 5 e 8 punti ci sono 64 modi di farne un pezzo qualsiasi, e producono **21 totali distinti**: tutti i numeri da 0 a 20, nessuno escluso. Ma **solo due di quei ventuno totali identificano quello che è stato fatto**, e sono i due estremi — lo zero e il venti. Il totale 10 si ottiene in **quattro modi** diversi, e i totali 9 e 11 in cinque (`build/check_256.py`, per enumerazione dei sottoinsiemi e per convoluzione dei polinomi generatori, concordi). **Chi legge un totale sa quanto, e non sa che cosa**, tranne quando il totale è il massimo o il minimo possibile.

## Esempi trovati

Le economie a gettoni negli ospedali e nelle classi, con il listino esposto: quanti gettoni costa ogni cosa che si può comprare, scritto in anticipo e dato ai partecipanti.

I punti esperienza di *Dungeons & Dragons*, che si accumulano e fanno salire di livello, e i sistemi *cash-in* di *Final Fantasy XIII* e *Warhammer Fantasy Roleplay*, dove i punti si spendono e vengono cancellati.

Il tetto di *RuneScape*: nessun giocatore può superare il livello 120, che richiede **104 273 167 punti esperienza**, e nessuna singola abilità può superare i 200 milioni di punti.

Il punteggio nei giochi da sala, dove serviva a distinguere una partita da un'altra perché la partita non poteva finire.

I moltiplicatori: nei giochi di enigmi il numero del livello moltiplica i punti, così che a difficoltà maggiore corrispondano totali più alti.

XKeyscore, il programma di raccolta di informazioni della NSA, che assegna punti «skilz» per addestrare gli analisti nuovi. Compare in una riga sola di `gamification.txt`, che lo classifica come ludicizzazione dell'apprendimento e non lo descrive.

## Una nostra versione

> **Il pomeriggio da dieci punti**
>
> Qui sotto c'e un listino. Ogni cosa vale quello che c'e scritto, e le cose si possono fare in qualunque ordine.
>
> ```
>   1  Guardare fuori dalla finestra per un minuto intero
>   1  Scrivere una parola che oggi non hai ancora detto
>   2  Misurare una cosa della cucina con una cosa della cucina
>   3  Disegnare un oggetto senza staccare la matita
>   5  Convincere qualcuno di casa a fare una delle cose qui sopra
>   8  Inventare la settima riga di questo listino, e farla
> ```
>
> **Non devi arrivare al totale piu alto che puoi. Devi arrivare esattamente a dieci.**
>
> ```
>   Ho fatto: ────  ────  ────  ────    totale: ──────
> ```
>
> Quando hai finito, una domanda sola: **dieci si puo fare in quattro modi diversi, e tu ne hai scelto uno.** Perche quello?

Il bersaglio esatto trasforma la somma in una scelta: con un tetto libero conviene fare tutto, con il dieci bisogna decidere. Il listino è la parte che dichiara che cosa conta, e l'ultima riga vale otto perché costa scriverla. La domanda finale è l'unica cosa che il totale da solo non può dire, e il foglio la chiede invece di dedurla.

**Dove si rompe.** Il sistema non registra niente su nessuno, quindi un totale che si accumula da un pomeriggio all'altro non esiste: questo foglio si chiude in un pomeriggio e riparte da zero il successivo. Un tariffario, però, non ha bisogno di nessun registro — sta stampato — e la somma la fa chi gioca. **Su tutte le forme di questo capitolo il limite che morde è che il sistema non tiene un conto su una persona; qui si aggira mettendo il conto sul foglio invece che nel sistema, e accettando che il foglio duri un pomeriggio.**

## Da riprendere alla rassegna

**Il tariffario è la dichiarazione più onesta che una forma possa fare.** Scrivere che una cosa vale otto e un'altra uno dice che cosa conta senza dover spiegare perché, e chi legge può non essere d'accordo — cosa che con una frase di incoraggiamento non può fare. Da guardare come tecnica generale, staccata dai punti: **mettere un numero accanto alle cose è un modo di rendere discutibile una preferenza.**

**Il bersaglio esatto invece del massimo.** «Arriva a dieci» produce una decisione, «fai più punti che puoi» produce volume. È la stessa distinzione già vista alla voce 244, autovalutazione con rubrica fra sommare e guardare il minimo, e vale ovunque il progetto stampi dei numeri.

**La contingenza è la maniglia, non la ricompensa.** La letteratura sull'effetto di sovragiustificazione non dice che i punti facciano male: dice che fanno male quando sono legati al fatto di aver svolto il compito, e non quando informano su come è andata. Un tariffario che dice quanto vale una cosa è una ricompensa legata al compito; una griglia che dice come è andata è informazione. **La differenza sta nel testo, non nel numero.**

**Il totale non dice che cosa è stato fatto, e questo è un difetto o una protezione a seconda di chi legge.** Ventuno totali e due soli che identificano il pomeriggio: se il numero deve tornare a qualcuno, è quasi sempre insufficiente; se non deve tornare a nessuno, è esattamente la quantità giusta di informazione.

**Un'economia a gettoni ha bisogno di un listino di cose comprabili, e questo progetto non ne ha uno.** I rinforzatori di scambio delle fonti sono privilegi, servizi e oggetti, tutte cose che stanno fuori dal foglio e in casa. È la prima volta in tutto l'elenco che una forma richiede esplicitamente che qualcuno di casa **abbia qualcosa da dare**, e non solo qualcosa da fare. Da guardare accanto ai nove mestieri della persona di casa già raccolti al capitolo 8.
