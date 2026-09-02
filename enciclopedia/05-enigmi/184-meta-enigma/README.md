# Meta-enigma

- **Numero** 184 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Meccanismi da escape room»
- **Si chiama anche** meta, *metapuzzle*, meta-meta, enigma dei risultati, finale che raccoglie, alimentatori e finale, *feeder e meta*
- **In una riga** le soluzioni degli enigmi precedenti sono i dati del finale. È la struttura delle puzzle hunt.
- **Fonti** [Metapuzzle](https://en.wikipedia.org/wiki/Metapuzzle), [Puzzlehunt](https://en.wikipedia.org/wiki/Puzzlehunt), [Escape room](https://en.wikipedia.org/wiki/Escape_room), lette il 31 agosto 2026. I cinque problemini, il finale e i conti sul backsolving sono nostri, verificati per enumerazione

## Che cos'è

**Questa voce e la voce 182, percorso a imbuto descrivono la stessa architettura, e la cosa va detta prima di tutto il resto.** Le due glosse dell'elenco — «molte cose in parallelo convergono in una» e «le soluzioni degli enigmi precedenti sono i dati del finale» — dicono la stessa cosa con parole diverse. Quella voce lo aveva già notato. La distinzione è questa: **quella voce descrive che cosa la struttura chiede a chi riceve i fogli; questa descrive come chi li prepara la costruisce.** Sono due mestieri diversi sullo stesso oggetto, e il taglio d'autore ha contenuto che l'altro non ha: da dove si comincia a scrivere, che cosa si sceglie per primo, e quale proprietà del finale decide se un alimentatore serve davvero. **Che l'elenco contenga due voci per una cosa sola resta un problema dell'elenco.**

Il confine con il capitolo 6 invece è netto e non è in discussione: **l'evento** in cui delle squadre passano un fine settimana su decine di enigmi legati da un meta è la voce 206, puzzle hunt, e sta là. Qui c'è il meccanismo, non la manifestazione.

Le parti che chi costruisce deve decidere, e l'ordine in cui le decide:

- **La risposta del finale, per prima.** Non si scrivono cinque enigmi e poi si cerca che cosa ne esca: si sceglie che cosa deve uscire e si costruiscono gli enigmi che lo producono.
- **Come le risposte diventano il finale.** Le si somma, le si dispone, le si sovrappone, le si usa come misure.
- **Come si passa dalla soluzione di un enigma al pezzo che serve.** Ha un nome, **estrazione**, ed è un enigma dentro l'enigma.
- **Se il finale è dato o no.** Meta **puro**: le risposte bastano. Meta **a guscio**: le risposte vanno inserite in una struttura consegnata a parte.
- **Quanti piani.** Sopra i metaenigmi si può mettere un **meta-meta**.
- **Quanto vale l'ultimo alimentatore.** È la domanda più importante e quella a cui nessuno risponde in anticipo. Si può calcolare.

## Da dove viene

Dalle *puzzle hunt*, e la definizione più corta è di un progettista di giochi, **Cliff Johnson**, riportata da «Metapuzzle»: **una raccolta di enigmi che, risolti, danno ciascuno un pezzo di un enigma principale.** Quelli che alimentano si chiamano *feeder*, quello finale *meta*.

L'esempio canonico è quello che la fonte porta: cinque enigmi con risposte **BLACK, HAMMER, FROST, KNIFE, UNION** portano alla risposta **JACK**, che si combina con tutte e cinque. Un piano sopra: se quel JACK sta accanto a tre meta con risposte TEN, QUEEN e ACE, il **meta-meta** è KING, la carta che manca a una scala all'asso.

**«Puzzlehunt» è la fonte che descrive il mestiere invece della forma**, ed è per questo che serve a questa voce. Dice tre cose che riguardano chi costruisce. La prima: gli enigmi di una *puzzle hunt* **non hanno istruzioni**, e capire come si affrontano è parte del compito; il metodo può essere suggerito dal titolo e dal *flavor text*. La seconda: la soluzione è di norma una parola o una frase, e il passaggio dalla soluzione al pezzo che serve al meta si chiama **estrazione** — prendere certe lettere, leggere il risultato come Braille o Morse, oppure **riapplicare al risultato il trucco che è servito a ottenerlo.** La terza: i meta si dividono in **a guscio** e **puri** a seconda che serva o no una struttura consegnata a parte.

Nelle escape room la stessa architettura c'è ma non ha nome. «Escape room» la nomina solo come effetto: gli enigmi «sbloccano l'accesso a nuovi oggetti o a nuove aree quando vengono risolti», e la serratura finale è il meta che raccoglie. È la voce 170, serratura a combinazione vista dalla parte di chi la carica.

## Varianti e parenti

- **Meta puro** — le sole risposte contengono tutto quello che serve.
- **Meta a guscio** — le risposte vanno inserite in una struttura data a parte, che da sola non dice niente.
- **Meta-meta** — un piano sopra, che raccoglie i metaenigmi.
- **Rally** — la variante lineare, in cui ogni enigma sblocca la posizione del prossimo invece di alimentare un finale.
- **Estrazione** — il pezzo di mestiere che sta fra la soluzione e il dato.
- **Voce 182, percorso a imbuto** — la stessa architettura vista da chi riceve i fogli. Vedi sopra.
- **Voce 180, combinazione da comporre** — il caso in cui il finale è un codice e basta.
- **Voce 170, serratura a combinazione** — il giunto fisico che accetta o rifiuta il finale.
- **Voce 183, percorso aperto** — quello che resta togliendo il finale.
- **Voce 206, puzzle hunt** — l'evento. Sta al capitolo 6.
- **Voce 155, nonogramma / picross** — l'altra forma in cui costruire è più facile che risolvere per una ragione strutturale.

## Che cosa se ne sa

**Si costruisce all'indietro, e la fonte non lo dice: lo dice la struttura.** Un meta funziona se le risposte degli alimentatori producono il finale; quindi le risposte sono un vincolo, e un enigma con la risposta assegnata in anticipo è un problema diverso — e più facile — da un enigma libero. È la stessa asimmetria già trovata alla voce 164, labirinto su carta e alla voce 155, nonogramma / picross: **chi costruisce lavora in una direzione in cui il problema è più docile.**

**Quanto valga l'ultimo alimentatore dipende da quante dimensioni ha il finale, e adesso c'è il conto.** Questa è la cosa nuova di questa voce, e unifica tre risultati sparsi.

- Se il finale combina le risposte in **un numero solo** — una somma, una combinazione, una posizione — allora conoscendone tutte tranne una, quella che manca è **determinata**. Nell'esempio costruito qui, provando tutti i valori possibili a ognuna delle cinque posizioni si trova sempre **un solo candidato**. Non è un caso e non dipende dall'esempio: un vincolo scalare invertibile ha una soluzione sola.
- Se il finale combina le risposte in **una figura**, no. Alla voce 182, percorso a imbuto, con cinque risposte fra nove caselle, conoscerne quattro lascia **cinque** caselle possibili per aritmetica; a restringere è la figura, che non è un vincolo aritmetico e non si inverte.
- Se il finale è **una parola che sta bene con le altre**, come nel caso canonico, il restringimento non si conta affatto: la fonte dice che il *backsolving* funziona «con un grado maggiore o minore di certezza» e che **non è infallibile** — chi cerca una parola da mettere con JACK può proporre SPRING-HEELED e sentirsi altrettanto sicuro.

**Ne segue una regola per chi costruisce, e non era mai stata scritta: un finale scalare regala sempre l'ultimo pezzo, un finale con più di una dimensione no.** Se si vuole che tutti e cinque gli alimentatori servano, il finale non può essere una somma.

**Il finale toglie molto meno di quanto sembri.** Nell'esempio costruito qui, cinque risposte fra 1 e 6 fanno **7776** combinazioni; quelle che soddisfano il finale sono **200**. Il finale divide per circa trentanove, il che è molto in astratto e nulla in pratica: **nessuno prova duecento combinazioni**, e il valore del finale non sta nel restringere lo spazio, sta nel dire sì o no senza spiegare.

**Il segnale d'errore è aggregato, e questa è la ragione tecnica per cui il mestiere è difficile.** Il finale funziona o non funziona e non dice quale alimentatore sia sbagliato. Chi costruisce deve quindi garantire da solo che tutti e cinque gli enigmi abbiano la risposta che crede, perché non c'è nessun controllo intermedio. **È la stessa fattura già presentata dalla voce 154, sudoku e affini (Nikoli) e dalla voce 142, puzzle a griglia (chi beve cosa, chi vive dove)**, e la via d'uscita resta la stessa: taglie piccole, verificate da un programma scritto apposta.

**Sul numero di alimentatori non c'è nessun dato.** L'esempio canonico ne ha cinque, il meta-meta ne raccoglie quattro; né «Metapuzzle» né «Puzzlehunt» dicono quanti convenga metterne, quanto debbano essere difficili, o quanto duri un meta ben fatto. **Questa è la lacuna più grande fra quelle incontrate nel capitolo**, perché riguarda la sola manopola che chi costruisce controlla per intero.

## Esempi trovati

BLACK, HAMMER, FROST, KNIFE, UNION → JACK, e un piano sopra JACK, TEN, QUEEN, ACE → KING.

Il meta a guscio, in cui le risposte vanno messe dentro una griglia consegnata a parte che da sola non dice niente.

L'estrazione per riapplicazione: si riapplica al risultato lo stesso trucco che è servito a ottenerlo.

L'estrazione per cambio di codice: la soluzione si rilegge come Morse o come Braille.

Gli enigmi senza istruzioni, in cui capire quale sia il compito è metà del compito, e il titolo lo suggerisce.

La serratura finale di una escape room, caricata da tre enigmi che stanno in tre punti diversi della stanza.

## Un esempio giocabile

> **Cinque risposte e una passeggiata**
>
> Cinque problemi. Falli nell'ordine che vuoi. **Ognuno ha per risposta un numero fra 1 e 6**, e nessuno dei cinque, da solo, ti dice niente.
>
> ```
>   1   Quante facce ha una piramide con la base quadrata?      ────
>
>   2   Quante volte compare la cifra 7 fra 1 e 20?             ────
>
>   3   Quanti spigoli ha un tetraedro — la piramide fatta
>       di quattro triangoli?                                   ────
>
>   4   Quanti divisori ha il numero 4?                         ────
>
>   5   Fra 1 e 20, quanti sono i quadrati perfetti?            ────
> ```
>
> **Adesso il finale, e si fa camminando sul righello.**
>
> Ritaglia questa striscia. È lunga trenta centimetri ed è segnata ogni centimetro. **La tacca nera sta al 10.**
>
> ```
>   |----|----|----|----|----█----|----|----|----|----|
>   0    2    4    6    8    10   12   14   16   18   20
> ```
>
> Metti il dito sullo zero. Poi:
>
> ```
>   vai a DESTRA di   (risposta 1)  centimetri
>   vai a SINISTRA di (risposta 2)  centimetri
>   vai a DESTRA di   (risposta 3)  centimetri
>   vai a SINISTRA di (risposta 4)  centimetri
>   vai a DESTRA di   (risposta 5)  centimetri
> ```
>
> Segna dove ti fermi ogni volta:
>
> ```
>   ────   ────   ────   ────   ────
> ```
>
> **Se le cinque risposte sono giuste, il dito finisce sulla tacca nera.** Nessuno te lo conferma: o ci sei o non ci sei.
>
> **Una cosa da guardare, e riguarda chi ha scritto il foglio.**
>
> Il dito arriva sulla tacca. Bene. Adesso immagina di non aver fatto il problema numero 3, e di sapere le altre quattro risposte.
>
> ```
>   Quanti numeri fra 1 e 6 potresti mettere al posto della
>   risposta 3, e finire lo stesso sulla tacca?        ────
> ```
>
> È **uno solo**, e vale per tutte e cinque: sapendone quattro, la quinta è obbligata. **Non hai bisogno di risolvere l'ultimo problema, mai.** Chi ha scritto questo foglio lo sapeva e l'ha lasciato così, perché la cosa da vedere è proprio questa: **un finale che è un numero solo regala sempre l'ultimo pezzo.**

Il foglio è verificato per enumerazione, ricalcolando tutte e cinque le risposte — **5** facce, **2** occorrenze della cifra 7, **6** spigoli, **3** divisori di 4, **4** quadrati perfetti sotto il 20 — e poi la passeggiata: le posizioni toccate sono **5, 3, 9, 6, 10**, tutte dentro la striscia, e l'arrivo è **10**. Le quintuple possibili sono **7776**, quelle che arrivano alla tacca **200**, e a ognuna delle cinque posizioni il candidato compatibile con le altre quattro è **uno solo**.

Il finale è una posizione fisica invece di un numero da scrivere, e questo cambia il tipo di verifica: non si controlla un risultato, si guarda dove è finito il dito. **La verifica è binaria, immediata e non passa da nessuno**, che è il grado più alto della scala raccolta alle voci 167, 168 e 169. Costa una striscia di carta e nessun materiale.

L'ultima parte del foglio non nasconde il difetto: lo fa misurare. Chiedere quanti valori funzionerebbero al posto di una risposta è una domanda a cui si risponde con un conto di dieci secondi, e la risposta — uno — insegna che cos'è un vincolo invertibile senza usare la parola. **È la terza volta che l'ultima consegna di un foglio misura il foglio stesso**, dopo la voce 180, combinazione da comporre e la voce 182, percorso a imbuto, e la prima in cui quello che si misura è un difetto di chi l'ha scritto.

Dove si romperebbe: **non si rompe.** Sta su un foglio, si fa seduti, il materiale è la striscia stampata sul foglio stesso, e la fotografia del foglio compilato mostra le cinque risposte e le cinque posizioni toccate, da cui si ricostruisce tutto. Su un pannello di quattro righe entrerebbe un problema per volta e la passeggiata riga per riga, ma **la striscia no**, e senza striscia il finale torna a essere una somma da fare a mente, cioè un'altra cosa.

## Che cosa la rende interessante

**Il numero di dimensioni del finale decide quanto vale l'ultimo alimentatore, e adesso è contato.** Finale scalare: **un candidato**, sempre, e non dipende dall'esempio. Finale che è una figura: **cinque su nove** nel caso misurato alla voce 182, percorso a imbuto, e a restringere davvero è la figura e non l'aritmetica. Finale che è una parola: non si conta, e la fonte dichiara il metodo fallibile. **È la formulazione generale di tre osservazioni che erano sparse fra le voci 180, 182 e questa**, ed è la cosa che giustifica il taglio d'autore di questa voce.

**Un finale toglie meno di quanto sembri, e non serve a questo.** Da 7776 a 200 è una divisione per trentanove, e nessuno proverebbe duecento combinazioni comunque. **Il valore del finale non è restringere lo spazio: è dire sì o no senza spiegare**, ed è la sola cosa che un foglio stampato sa fare da solo.

**Si costruisce all'indietro, e questo è il mestiere.** Prima la risposta del finale, poi gli enigmi che la producono. Un enigma con la risposta già assegnata è un problema più facile di un enigma libero, che è la stessa asimmetria delle voci 155 e 164. **Per chi deve generare attività e garantirne la correttezza, è la direzione di lavoro giusta e non è quella che verrebbe da sé.**

**L'estrazione è un pezzo di mestiere che l'enciclopedia non ha altrove.** Il passaggio dalla soluzione di un enigma al dato che serve al finale è esso stesso un enigma, e i modi documentati — prendere certe lettere, cambiare codice, riapplicare il trucco al proprio risultato — sono tre trasformazioni generali. **Riapplicare al risultato il metodo che è servito a ottenerlo è la più elegante e la sola che non richieda di maneggiare lettere.**

**L'elenco ha due voci per una cosa sola.** Questa e la voce 182, percorso a imbuto. Il taglio scelto — chi riceve contro chi costruisce — le tiene distinte e produce due testi diversi, ma **è una separazione decisa qui e non una separazione che stava nell'elenco.** Le due vanno lette insieme.
