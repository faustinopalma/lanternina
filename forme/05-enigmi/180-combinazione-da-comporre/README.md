# Combinazione da comporre

- **Numero** 180 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Meccanismi da escape room»
- **Si chiama anche** codice da raccogliere, cifre sparse, *feeder puzzles*, estrazione, enigmi che alimentano, quattro pezzi e un numero
- **In una riga** quattro cifre che vengono da quattro posti diversi.
- **Fonti** `metapuzzle.txt`, `puzzlehunt.txt`, `escape-room.txt`, lette il 31 agosto 2026. I quattro problemini dell'esempio, la regola d'ordine e i conti sul provare a caso sono nostri, verificati in `build/check_180.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Un codice che nessuno possiede per intero. Ogni pezzo viene da un posto diverso, e chi lo raccoglie deve fare due cose distinte: **ottenere ogni pezzo**, e **capire in che ordine vanno.**

Il confine con la voce 170, serratura a combinazione va tenuto e non è sottile: **là il tema è il giunto**, cioè un meccanismo che accetta o rifiuta e che collega due attività; **qui il tema è il contenuto**, cioè che le cifre si raccolgono una per volta da fonti indipendenti. Si possono avere l'una senza l'altra: una serratura la cui combinazione è scritta su un foglietto è la 170 senza la 180; quattro cifre raccolte e poi semplicemente lette a voce sono la 180 senza la 170.

Parti mobili:

- **Quanti pezzi** e **quanto è grande ogni pezzo.** Quattro cifre da dieci fanno diecimila possibilità; quattro lettere italiane ne fanno **194 481**. La taglia dell'alfabeto decide tutto quello che segue.
- **Come si estrae il pezzo dalla soluzione.** Nelle *puzzle hunt* questo passo ha un nome, **estrazione**, ed è un enigma dentro l'enigma: prendere certe lettere di certe parole, leggere un risultato come Morse o braille, oppure riapplicare al risultato lo stesso trucco che è servito a ottenerlo.
- **Come si sa l'ordine.** È il problema vero, e quasi nessuna descrizione lo affronta. Si può numerare le fonti, colorarle, disporle nello spazio, oppure **dare una regola che determini l'ordine a partire dalle cifre stesse.**
- **Se c'è un controllo.** Una somma che deve tornare, una lunghezza, una parola che deve risultare.
- **Se i pezzi sono tutti necessari.** Se non lo sono, c'è un pezzo di troppo, ed è un'altra forma.

**A differenza della voce 179, chiave nascosta, qui il gradiente c'è.** Tre pezzi su quattro sono un progresso reale, e questo cambia l'esperienza: non si è mai fermi. Ma è anche la debolezza della forma, e ha un nome documentato.

## Da dove viene

Viene dalle *puzzle hunt*, e il vocabolario è loro. `puzzlehunt.txt` descrive la struttura: gruppi di enigmi sono collegati da un **metaenigma**, che si risolve combinando o confrontando le risposte degli enigmi «alimentatori» — *feeder puzzles*. La distinzione che la fonte fa è utile: in un metaenigma **a guscio** le risposte vanno inserite in una struttura fornita a parte; in uno **puro** le sole risposte contengono già tutto quello che serve.

La regola che governa il genere è che **non ci sono istruzioni**: un enigma da *puzzle hunt* di solito non dice come si risolve, e capire l'approccio è parte del compito. Il titolo e un testo introduttivo possono suggerirlo. La risposta è in genere una parola o una frase, e il passaggio finale dalla soluzione alla risposta è l'estrazione.

`metapuzzle.txt` dà l'esempio canonico e conviene riportarlo perché è chiaro: cinque enigmi con risposte BLACK, HAMMER, FROST, KNIFE e UNION portano alla risposta JACK, che si combina con tutte e cinque per fare parole o espressioni. E porta anche il livello successivo: se quel JACK sta accanto a tre metaenigmi con risposte TEN, QUEEN e ACE, la risposta del **meta-meta** è KING, la carta che manca a una scala all'asso.

**E qui c'è il difetto strutturale, che ha un nome.** La forma stessa rende spesso possibile indovinare le risposte degli enigmi che la alimentano **senza risolverli**. La tecnica si chiama **backsolving**: risolti quattro dei cinque e capito il metaenigma, si tira a indovinare il quinto. La fonte è onesta anche sul suo limite: **non è infallibile** — nell'esempio, chi cerca una parola che stia con JACK potrebbe indovinare UNION oppure sbagliare con SPRING-HEELED con la stessa facilità.

Nelle escape room la stessa struttura c'è ma con un nome diverso: gli enigmi «sbloccano l'accesso a nuovi oggetti o a nuove aree quando vengono risolti». La forma raccolta qui è il caso in cui quello che si sblocca è un numero.

## Varianti e parenti

- **Metaenigma puro** — le risposte alimentatrici bastano da sole.
- **Metaenigma a guscio** — le risposte vanno inserite in una struttura data a parte, che è quasi sempre una griglia.
- **Meta-meta** — un livello sopra, che raccoglie i metaenigmi.
- **Rally** — variante in cui ogni enigma risolto rivela **dove** sta il prossimo invece di dare una cifra. È la voce 181, percorso lineare.
- **Voce 170, serratura a combinazione** — il giunto che accetta o rifiuta. Sono fatte per stare insieme e sono due cose.
- **Voce 179, chiave nascosta** — l'altro pezzo di caccia di questo blocco; là si trova una cosa sola, qui se ne compongono quattro.
- **Voce 182, percorso a imbuto** — la stessa architettura vista come forma di percorso invece che come contenuto di un codice.
- **Voce 184, meta-enigma** — la voce successiva ma due, nella stessa sezione di questo capitolo, e la sua glossa dice che è la struttura delle *puzzle hunt*. **Il confine con questa e con la voce 182, percorso a imbuto va scritto quando si scriverà quella**, perché le tre descrivono la stessa architettura da tre lati.
- **Voce 131, codice a numeri (A=1)** e **voce 5, corrispondenza (matching)** — i modi di trasformare una risposta in una cifra, cioè l'estrazione.

## Che cosa se ne sa

**Quattro cifre non si difendono, e il conto lo dimostra.** In `build/check_180.py` abbiamo enumerato i casi: quattro cifre libere sono **10 000** combinazioni; sapendone una al posto giusto ne restano 1000, due 100, **tre soltanto dieci.** E il caso più istruttivo: **sapendo tutte e quattro le cifre ma non il loro ordine ne restano ventiquattro**, che a cinque secondi per tentativo sono **due minuti.** Chi ha risolto tre problemi su quattro non ha bisogno del quarto, e chi li ha risolti tutti e quattro non ha bisogno di capire l'ordine. **È il backsolving della fonte, con i numeri.**

**Non è un difetto da correggere, perché non si può.** Aumentare l'alfabeto aiuta poco: quattro lettere italiane sono 194 481 combinazioni in totale, ma chi ne conosce tre deve provarne ventuno, cioè meno di due minuti. **Nessuna scelta di taglia rende costoso indovinare l'ultimo pezzo**, e l'unica risposta onesta è progettare sapendo che l'ultimo pezzo è regalato.

**Un controllo di somma non vede l'ordine, e questo si può dimostrare in una riga.** Se le quattro cifre devono sommare a un numero dato, quel controllo passa per tutte le ventiquattro disposizioni — lo abbiamo verificato per enumerazione, e le somme delle ventiquattro permutazioni sono tutte uguali. Ne segue una cosa utile da sapere quando si progetta: **un controllo sulle cifre prende gli errori di calcolo e non prende gli errori di ordine**, e servono due controlli diversi per due guasti diversi.

**E un controllo di somma si può ingannare per compensazione.** Se due dei quattro problemi vengono sbagliati in modo che un errore sia più tre e l'altro meno tre, la somma torna e il controllo dice che va tutto bene. Vale per qualunque somma di controllo, e va detto.

**Il segnale d'errore è aggregato**, come alla voce 170, serratura a combinazione: dice che qualcosa non torna e non dice che cosa. È l'unico tipo di segnale del genere in tutta l'enciclopedia, costa zero da stampare, e **obbliga a ricontrollare invece che a proseguire.**

**Sulla difficoltà di questa forma non c'è nessuna misura**, in nessuna delle pagine lette. Non si sa quanto tempo prenda comporre un codice da quattro fonti, non si sa quanto spesso il backsolving venga usato davvero, e non c'è nessun dato su quante persone si blocchino sull'ordine invece che sui pezzi. **Va verificato.**

## Esempi trovati

BLACK, HAMMER, FROST, KNIFE, UNION → JACK: cinque risposte che diventano i dati di una sesta.

JACK, TEN, QUEEN, ACE → KING: lo stesso, un piano sopra.

Il metaenigma a guscio, in cui le risposte vanno messe dentro una griglia consegnata a parte, e la griglia da sola non dice niente.

L'estrazione nelle *puzzle hunt*: prendere certe lettere della soluzione, o leggerla come Morse, o riapplicarle il trucco che è servito a ottenerla.

Il rally, in cui ogni enigma risolto non dà una cifra ma dice dove sta il prossimo.

Il backsolving: chi ha quattro risposte su cinque non risolve la quinta, la indovina — e a volte indovina male.

## Una nostra versione

> **Quattro numeri e un ordine**
>
> Qui sotto ci sono quattro problemi. **Ognuno ha per risposta una cifra sola**, da 0 a 9. Risolvili in qualunque ordine ti pare.
>
> ```
>   A   Un numero di due cifre. Le due cifre sommate fanno 7,
>       moltiplicate fanno 12. Scrivi la più grande delle due.        ────
>
>   B   Con le cifre 1, 2 e 3, quanti numeri di tre cifre tutte
>       diverse si possono scrivere?                                  ────
>
>   C   Su carta a quadretti disegni un rettangolo che ha il
>       contorno lungo 14 quadretti e dentro ne contiene 10.
>       Quanto è lungo il lato lungo?                                 ────
>
>   D   Quanti numeri di due cifre hanno le due cifre uguali?         ────
> ```
>
> **Il controllo.** Somma le quattro cifre che hai trovato. **Deve venire 24.**
>
> ```
>   la mia somma:  ────
> ```
>
> Se non viene 24, uno dei quattro l'hai sbagliato. **Il controllo non ti dice quale**, e non c'è modo di farglielo dire: è un sì o un no su tutti e quattro insieme.
>
> **L'ordine.** Adesso hai quattro cifre e non sai in che ordine vanno. La regola è questa:
>
> ```
>   la più piccola va per prima
>   la più grande va per ultima
>   delle due che restano, prima quella dispari
>
>   il codice è:  ──  ──  ──  ──
> ```
>
> **Una cosa da guardare, adesso che hai finito.**
>
> ```
>   Se avessi risolto solo tre problemi su quattro, quante cifre
>   avresti dovuto provare per trovare l'ultima?          ────
>
>   Se avessi risolto tutti e quattro i problemi ma non avessi
>   la regola dell'ordine, quanti codici diversi avresti
>   dovuto provare?                                       ────
> ```
>
> Le risposte sono **dieci** e **ventiquattro**. A cinque secondi per tentativo, ventiquattro prove sono due minuti. Vuol dire che **l'ultimo pezzo di una combinazione a quattro cifre è sempre regalato**, e chi costruisce una cosa del genere farebbe bene a saperlo invece di illudersi.

Le quattro risposte sono **4, 6, 5 e 9**, e ognuno dei quattro problemi ha una risposta sola: verificato per enumerazione in `build/check_180.py`, che controlla tutte le coppie di cifre per il primo, tutte le permutazioni per il secondo, tutti i rettangoli fino a venti quadretti di lato per il terzo, e tutti i numeri di due cifre per il quarto. La somma è **24** in tutti i casi, e la regola d'ordine si applica senza ambiguità perché fra le due cifre centrali una è dispari e l'altra è pari — il codice è **4569**.

Il controllo della somma è la parte progettata, e fa due lavori. Prende gli errori di calcolo, che sono il guasto probabile quando si risolvono quattro problemini di fila; e **non prende gli errori di ordine**, perché la somma delle quattro cifre è la stessa in tutte le ventiquattro disposizioni. Chi guarda le due cose insieme scopre da solo che un controllo prende quello che prende, e questa è una cosa che nessuna spiegazione insegnerebbe meglio.

L'ultima parte è l'unica in cui il foglio parla di sé stesso, e lo fa con dei numeri che chi legge può ricontrollare. È l'inverso della mossa consueta: invece di nascondere che il sistema è debole, **lo dichiara e ne fa il contenuto.**

Dove si romperebbe: **niente**, ed è il caso più facile del blocco. Sta tutto su un foglio, si risolve seduti, non serve nessun materiale, non serve nessuno, e la fotografia del foglio compilato basta al sistema per sapere che cosa è successo. L'unico limite è che il codice non apre niente: perché lo apra serve la voce 170, serratura a combinazione, e cioè un lucchetto vero o una busta chiusa preparata da qualcun altro. **Sul pannello da quattro righe entrerebbe un problema per volta, uno al giorno, e il quarto giorno la somma** — che è forse la versione migliore di tutte, e non è quella stampata qui.

## Da riprendere alla rassegna

**L'ultimo pezzo di una combinazione è sempre regalato, e adesso c'è il numero.** Dieci prove per una cifra, ventiquattro per l'ordine di quattro cifre, ventuno per una lettera italiana. **Nessuna scelta di taglia lo evita.** Alla rassegna la domanda non è come impedirlo, ma se convenga: una struttura in cui chi si blocca su un pezzo può proseguire lo stesso è più robusta di una in cui non può, e questo è un pregio travestito da difetto.

**Un controllo prende un guasto e non un altro, e lo si può far scoprire.** La somma delle cifre non vede l'ordine. Mostrare i due guasti accanto costa due righe e insegna che cos'è un controllo meglio di qualunque definizione. **Da provare su ogni forma dell'elenco che abbia una verifica parziale**, e sono molte.

**Il segnale aggregato arriva a due occorrenze.** Voce 170 e questa. Dice sì o no su tutto insieme, costa zero, e cambia il comportamento di chi lo riceve: non si prosegue, si ricontrolla. **È il meccanismo più economico raccolto per far tornare indietro qualcuno su quello che ha già fatto.**

**Un foglio che dichiara la propria debolezza e ne fa il contenuto.** L'ultima domanda dell'esempio chiede quanto sarebbe stato facile barare. È la prima volta, in tutta l'enciclopedia, che una consegna misura sé stessa, e vale la pena chiedersi dove altro si possa fare.

**Una forma progettata per essere spezzata fra più persone, usata da una sola.** Le *puzzle hunt* danno enigmi diversi a membri diversi di una squadra, e il metaenigma li ricuce. Con una persona sola la struttura resta ma perde la ragione per cui esiste, e diventa quattro problemi in fila con un controllo in fondo. **Alla rassegna vale la pena separare le forme che perdono qualcosa quando la persona è una da quelle che non perdono niente**, perché finora sono state trattate tutte allo stesso modo.

