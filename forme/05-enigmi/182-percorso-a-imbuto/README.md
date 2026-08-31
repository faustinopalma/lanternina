# Percorso a imbuto

- **Numero** 182 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Meccanismi da escape room»
- **Si chiama anche** metaenigma, meta, *metapuzzle*, enigma finale, struttura a convergenza, enigmi alimentatori, *feeder puzzles*
- **In una riga** molte cose in parallelo convergono in una.
- **Fonti** `metapuzzle.txt`, `puzzlehunt.txt`, `escape-room.txt`, lette il 31 agosto 2026. I cinque problemini dell'esempio e la figura che ne esce sono nostri, verificati in `build/check_182.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Più compiti indipendenti, tutti disponibili subito, le cui risposte sono i dati di un ultimo compito. Nessuno dei primi dice niente da solo; l'ultimo non esiste finché non ci sono gli altri.

La definizione che `metapuzzle.txt` riporta è di un progettista di giochi, Cliff Johnson, ed è la più corta possibile: **una raccolta di enigmi che, risolti, danno ciascuno un pezzo di un enigma principale.** Quelli che alimentano si chiamano *feeder*, quello finale si chiama *meta*.

Come la voce 181, percorso lineare, **questa non è una forma con un contenuto: è una forma dell'ordine in cui le cose si aprono.** Quello che ha di suo è la topologia, ed è esattamente il rovescio della catena.

Parti mobili:

- **Quanti alimentatori.** Da tre a una decina; oltre, il finale diventa un lavoro di trascrizione.
- **Se il finale è dato o no.** In un meta **puro** le risposte da sole bastano; in un meta **a guscio** le risposte vanno inserite in una struttura consegnata a parte — una griglia, uno schema, un disegno.
- **Come si estrae il pezzo.** Il passaggio dalla soluzione di un alimentatore al pezzo che serve al finale ha un nome nelle *puzzle hunt*, **estrazione**, ed è un enigma dentro l'enigma.
- **Se il finale si può risolvere con dei pezzi mancanti.** Quasi sempre sì, e la cosa ha un nome.
- **Come si sa che il finale è giusto.** Nel caso classico non c'è nessuna regola: si sa perché **ha senso**, e questo è il punto più delicato della forma.

**La proprietà che la definisce è che non ha un punto di rottura unico.** Chi si blocca su un alimentatore ne fa un altro; chi non ne risolve uno può spesso arrivare in fondo lo stesso. È il contrario della catena, dove il primo passo che non viene ferma tutto.

## Da dove viene

Dalle *puzzle hunt*, dove è la struttura portante. `puzzlehunt.txt` descrive un evento in cui delle squadre risolvono una serie di enigmi, molti dei quali **legati fra loro proprio da metaenigmi**, e in cui gli enigmi di solito non hanno istruzioni: capire come si affrontano è parte del compito. La soluzione di un enigma è in genere una parola o una frase.

L'esempio canonico è quello che la fonte porta, e va riportato perché è il modo più chiaro di far vedere la struttura: cinque enigmi con risposte **BLACK, HAMMER, FROST, KNIFE, UNION** portano alla risposta del meta, **JACK**, che si combina con tutte e cinque per fare parole o espressioni. E ce n'è un piano sopra: se quel JACK sta accanto a tre meta con risposte TEN, QUEEN e ACE, la risposta del **meta-meta** è KING, la carta che manca a una scala all'asso.

**Il difetto strutturale è documentato e ha un nome.** La struttura stessa rende spesso possibile indovinare, con più o meno sicurezza, le risposte degli enigmi che alimentano il finale **senza risolverli**: si chiama **backsolving**. Chi ha risolto BLACK, HAMMER, FROST, KNIFE e ha capito che il meta è JACK può indovinare UNION invece di risolvere il quinto enigma. La fonte è onesta sul limite: **non è infallibile** — lo stesso solutore potrebbe indovinare SPRING-HEELED con la stessa facilità, e sbagliare.

Il parente stretto sta al capitolo 6 e va nominato: la voce 184, meta-enigma. **Là il metaenigma sarà descritto come la struttura di un evento, con la storia e l'itinerario che lo tengono insieme; qui si descrive che cosa chiede a chi riceve il foglio.** Le tre forme dell'ordine sono divise fra i due capitoli — lineare e a imbuto qui, aperto e meta là — e questo è un fatto sull'elenco più che sulle forme.

## Varianti e parenti

- **Meta puro** — le sole risposte contengono tutto quello che serve.
- **Meta a guscio** — le risposte vanno inserite in una struttura data a parte, che da sola non dice niente.
- **Meta-meta** — un piano sopra, che raccoglie i metaenigmi.
- **Rally** — variante lineare, in cui ogni enigma sblocca la posizione del prossimo. È la voce 181, percorso lineare.
- **Voce 180, combinazione da comporre** — la stessa architettura vista come contenuto di un codice invece che come forma di percorso. **Là il tema è che le cifre vengono da posti diversi, qui che nessuna di esse dice niente da sola.**
- **Voce 170, serratura a combinazione** — il giunto che accetta o rifiuta il risultato del finale.
- **Voce 183, percorso aperto** — capitolo 6: tutto disponibile e nessun finale che raccoglie.
- **Voce 184, meta-enigma** — capitolo 6, dove sarà l'architettura di un evento.
- **Voce 155, nonogramma / picross** — l'altra forma dell'elenco in cui il risultato è una figura che appare, e in cui riconoscerla è la verifica.

## Che cosa se ne sa

**Non c'è nessun punto di rottura unico, ed è la sola differenza che conta rispetto alla catena.** Un imbuto con cinque alimentatori e uno bloccato ne ha quattro che funzionano; una catena di cinque con uno bloccato ne ha uno. Questo cambia due cose insieme: **chi lavora sceglie che cosa affrontare**, e quindi la difficoltà si livella da sola; e non serve nessun sistema di aiuti, che alla voce 181, percorso lineare era invece una conseguenza obbligata della struttura.

**Il segnale d'errore è aggregato e arriva alla fine.** Il finale funziona o non funziona, e non dice quale alimentatore sia sbagliato. È lo stesso della voce 170, serratura a combinazione e della voce 180, combinazione da comporre, ed è l'opposto esatto del segnale locale e immediato della catena. **Le due voci consecutive 181 e 182 sono le due estremità di quello che un controllo può fare.**

**Il backsolving funziona nei due sensi, e non si può togliere.** Dal finale agli alimentatori — indovinare la risposta che manca —, e dagli alimentatori al finale con dei pezzi in meno. La fonte lo registra come una proprietà della struttura, non come un errore di chi la costruisce. **Ne segue che questa forma non protegge niente**, e che il suo pregio è esattamente questo: nessuno resta fermo.

**La verifica del finale, nel caso classico, non ha una regola.** JACK è giusto perché sta con tutte e cinque le parole, e chi lo trova lo sa senza che nessuno glielo dica. **È l'unico caso in tutta l'enciclopedia in cui la verifica è un giudizio di senso**, e non un conto, non un incastro, non un oggetto che si apre. Le forme raccolte finora avevano verifiche che si potevano descrivere; questa no.

**E qui c'è il limite tecnico che riguarda questo progetto per intero.** Il metaenigma canonico è costruito su **combinazioni di parole**: BLACKJACK, JACKHAMMER, JACK FROST, JACKKNIFE, LABOR UNION JACK. Il sistema non sa manipolare le lettere dentro le parole — è misurato, sta in `ideas/10 §6` — quindi **non può né costruire né verificare un metaenigma di quel tipo.** Non è un limite di gusto: è il limite più duro che questa famiglia incontri, e la voce lo dichiara invece di aggirarlo.

**La via d'uscita usata nell'esempio è sostituire il giudizio di senso con un riconoscimento di figura.** Se le risposte sono numeri da 1 a 9 e i numeri sono caselle di una griglia, il finale è **una figura che appare**, e chi la guarda sa se è una figura o no senza che nessuna regola glielo dica. La proprietà che rendeva il meta interessante — una verifica istantanea che nessuno sa enunciare — resta; quella che lo rendeva impossibile da generare — la manipolazione delle parole — se ne va. È la stessa idea del nonogramma della voce 155, nonogramma / picross applicata a una struttura invece che a una griglia.

**Il backsolving nel nostro esempio si conta, e vale poco.** Se una delle cinque risposte manca, le caselle ancora possibili sono **cinque su nove**, perché le quattro trovate sono escluse. Non è granché come restringimento; a restringere davvero è la figura, che con quattro caselle su cinque suggerisce la quinta a chiunque la guardi. **Questo è il punto: la parte che aiuta a indovinare non è aritmetica, ed è la stessa che rende il finale verificabile.**

**Sui tempi non c'è niente di specifico.** Le escape room durano dai 45 ai 60 minuti in tutto, e le *puzzle hunt* possono durare giorni; nessuna delle due fonti dice quanto valga un alimentatore né quanti convenga metterne.

## Esempi trovati

BLACK, HAMMER, FROST, KNIFE, UNION → JACK. Cinque risposte che diventano i dati di una sesta, e la sesta si riconosce perché sta con tutte.

JACK, TEN, QUEEN, ACE → KING: la carta che manca a una scala all'asso, un piano sopra.

Il meta a guscio: le risposte vanno messe dentro una griglia consegnata a parte, e la griglia da sola non dice niente.

L'estrazione: prendere certe lettere della soluzione, o leggerla come Morse o braille, o riapplicarle il trucco che è servito a ottenerla.

Il backsolving che sbaglia: chi cerca una parola che stia con JACK può proporre SPRING-HEELED e sentirsi sicuro.

Le componenti *run-around* delle *puzzle hunt*, in cui certi enigmi si affrontano solo andando in un posto preciso.

## Una nostra versione

> **Cinque risposte e una figura**
>
> Qui sotto ci sono cinque problemi. **Non sono in fila: puoi farli in qualunque ordine, e se uno non ti viene passa al prossimo.**
>
> Ognuno ha per risposta **un numero fra 1 e 9**.
>
> ```
>   A   Quanti numeri di due cifre hanno le due cifre che,
>       sommate, fanno 1?                                        ────
>
>   B   Fra 1 e 20, quanti numeri sono multipli di 5?            ────
>
>   C   Quanti numeri primi ci sono sotto il 18?                 ────
>
>   D   Quanti divisori ha 24?                                   ────
>
>   E   Fra 1 e 99, quanti sono i quadrati perfetti —
>       cioè i numeri che si ottengono moltiplicando un
>       numero per sé stesso?                                    ────
> ```
>
> **Adesso il finale.** Le caselle della griglia qui sotto si contano da sinistra a destra e dall'alto in basso, da 1 a 9.
>
> ```
>      1  2  3
>      4  5  6
>      7  8  9
> ```
>
> **Annerisci le cinque caselle che hai trovato.**
>
> ```
>      ┌──┬──┬──┐
>      │  │  │  │
>      ├──┼──┼──┤
>      │  │  │  │
>      ├──┼──┼──┤
>      │  │  │  │
>      └──┴──┴──┘
>
>   Che cosa è venuto fuori?  ────────────────────────────────
> ```
>
> Nessuno ti dice se è giusto. **Lo sai perché è qualcosa**, e se avessi sbagliato un problema non lo sarebbe.
>
> **Due cose da guardare, quando hai finito.**
>
> ```
>   Se avessi saltato uno dei cinque problemi, quante caselle
>   sarebbero rimaste possibili, contando solo che devono
>   essere diverse dalle altre quattro?                   ────
>
>   E guardando la figura mezza fatta, quante ne avresti
>   davvero prese in considerazione?                      ────
> ```
>
> La prima risposta è **cinque**. La seconda quasi certamente **una**, e non per un conto: perché una figura a cui manca un pezzo si vede.

I cinque problemi sono verificati per enumerazione in `build/check_182.py`, che elenca in ogni caso tutti i numeri che soddisfano la condizione: le risposte sono **1** (solo il 10), **4** (5, 10, 15, 20), **7** (2, 3, 5, 7, 11, 13, 17), **8** (i divisori di 24) e **9** (i quadrati da 1 a 81). Sono tutte diverse e tutte fra 1 e 9. Annerite sulla griglia danno la colonna di sinistra e la riga di sotto, cioè **una L**.

La figura è la parte progettata, e sostituisce il giudizio di senso del metaenigma classico. Nell'esempio della fonte si sa che JACK è giusto perché sta con cinque parole; qui si sa che è giusto perché **è una lettera invece di cinque macchie sparse.** In tutti e due i casi la verifica è istantanea e nessuno sa enunciarla; la differenza è che questa il sistema la sa produrre, e quella no.

L'ultima parte del foglio misura il backsolving invece di nasconderlo. Il conto aritmetico dà cinque caselle possibili, che non è un gran restringimento; la figura ne dà una. **Quello che aiuta a indovinare e quello che permette di verificare sono la stessa cosa**, e questa è la proprietà che rende la forma insieme robusta e permeabile.

Dove si romperebbe: **niente**, come per la voce 180, combinazione da comporre. Sta su un foglio, si fa seduti, non serve materiale né altre persone, e la fotografia della griglia annerita dice al sistema tutto quello che è successo — anzi, è l'unico esempio del blocco in cui **la fotografia si legge meglio del testo scritto a mano**, perché cinque caselle nere si riconoscono e cinque numeri scritti male no. Sul pannello da quattro righe entrerebbe un problema per volta ma non la griglia, e la figura finale andrebbe disegnata a mano su un foglio a parte: **la forma si spezza esattamente nel punto in cui converge.**

## Da riprendere alla rassegna

**Una verifica che nessuno sa enunciare e che tutti sanno fare.** JACK sta con cinque parole; cinque caselle annerite fanno una L. In tutti e due i casi chi guarda sa se è giusto, e nessuna regola lo dice. **È l'unico tipo di verifica di questo genere in tutta l'enciclopedia**, e alla rassegna va guardato con attenzione, perché è la sola che non richieda né una risposta custodita né un oggetto che si apra.

**Sostituire il senso con una figura rende generabile una forma che non lo era.** Il metaenigma canonico è fatto di parole combinate, e il sistema non le sa maneggiare; una figura su una griglia sì. **Da provare su tutte le forme del capitolo 12 e su tutte quelle bloccate dallo stesso limite**, perché è una via d'uscita nuova: non gira il gioco dalla parte dell'autore, cambia il canale della verifica.

**Una struttura senza punto di rottura unico si livella da sola.** Chi non risolve un alimentatore ne fa un altro, e non serve nessun sistema di aiuti. Rispetto alla catena, che ha bisogno di indizi a pagamento per non incepparsi, **l'imbuto ottiene gratis quello che quella deve comprare.** Per un sistema che non può accorgersi che qualcuno si è bloccato, è una differenza decisiva.

**Quello che aiuta a barare è quello che permette di verificare.** Il backsolving esiste perché il finale ha una struttura riconoscibile, e il finale è verificabile per la stessa ragione. Non si possono separare, e la fonte lo tratta come un fatto e non come un difetto. **Alla rassegna vale la pena cercare altre forme in cui il pregio e il buco sono la stessa proprietà.**

**Il foglio misura sé stesso, seconda occorrenza.** Come alla voce 180, combinazione da comporre, l'ultima consegna chiede quanto sarebbe stato facile indovinare. Due volte in tre voci non è più un caso, ed è una mossa che costa due righe: **far calcolare a chi ha finito quanto della sua fatica era necessaria.**

