# Costruzione di un motore

- **Numero** 272 nell'enciclopedia, capitolo 9 — Meccaniche di gioco
- **Si chiama anche** motore, *engine building*, circolo virtuoso, anello di retroazione positiva, effetto valanga, «spendere adesso per avere di più dopo», *tableau building*, *pool building*, investimento
- **In una riga** ogni pezzo rende più facile il successivo.
- **Fonti** lette il 31 agosto 2026: `game-mechanics.txt`, `game-balance.txt`, `positive-feedback.txt`, `deck-building-game.txt`, `simcity.txt`. `board-game.txt` letto e non citato: la sezione sulle meccaniche rimanda a `game-mechanics.txt` e non aggiunge niente su questa. Su Wikipedia inglese **`Engine_building` non è la pagina di questa forma**: rimanda a `Engine tuning`, cioè alla messa a punto del motore di un'automobile. La definizione della meccanica sta dentro `Game_mechanics`, in una sottosezione.
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Una struttura in cui quello che si costruisce produce la risorsa con cui si costruisce il pezzo dopo. Non si accumula per arrivare a una soglia: si accumula per accumulare più in fretta.

`game-mechanics.txt`, letto il 31 agosto 2026, la definisce come «un meccanismo che consiste nel costruire e ottimizzare un sistema che produce un flusso di risorse», e aggiunge che nei giochi da tavolo di questo tipo «il giocatore aggiunge e modifica combinazioni di abilità o di risorse per assemblare un circolo virtuoso di esiti via via più potenti e produttivi».

Parti mobili:

- **Il reddito.** Quanto arriva per unità di tempo o di turno, e da che cosa dipende. Se non dipende da niente che si possa cambiare, non c'è motore.
- **Il pezzo.** Che cosa si compra, quanto costa, di quanto alza il reddito. Un pezzo che alza il reddito di una quantità fissa dà crescita lineare; un pezzo che lo moltiplica dà crescita esponenziale, e i due si comportano in modo diverso al punto che non sono la stessa forma.
- **L'orizzonte.** Quanti turni restano. È la parte che decide tutto: lo stesso pezzo è un affare al terzo turno e uno spreco al decimo.
- **Il momento in cui si smette di costruire e si comincia a raccogliere.** Nei giochi che finiscono, il motore serve a qualcos'altro, e chi costruisce fino all'ultimo turno non usa mai quello che ha costruito.
- **Il collo di bottiglia.** La cosa che non cresce, e che quindi decide il tetto. Un motore senza collo di bottiglia diverge.

Togliendo l'orizzonte resta una crescita che non serve a niente. Togliendo il costo del pezzo resta una progressione automatica, cioè la voce 257, livelli. Togliendo il fatto che il pezzo alzi il reddito resta la voce 270, risorse da spendere.

## Da dove viene

Il concetto sta prima nella teoria dei sistemi che nei giochi. `positive-feedback.txt`, letto il 31 agosto 2026: i termini *positivo* e *negativo* furono applicati alla retroazione prima della seconda guerra mondiale, l'idea circolava già negli anni Venti con il circuito rigenerativo, Friis e Jensen la descrissero nel 1924 e l'articolo di Harold Stephen Black del 1934 fu il primo a trattare in dettaglio la retroazione negativa negli amplificatori. La pagina segnala anche la confusione che ne seguì, perché Nyquist e Bode chiamavano *negativa* la retroazione con il segno rovesciato mentre Black la chiamava così per il suo effetto sul guadagno; e riporta che Donella Meadows preferiva i termini *rinforzante* ed *equilibrante*, «positivo» e «negativo» in questo senso non implicando nessun giudizio sulla desiderabilità dell'esito.

Nei giochi il termine si stabilizza tardi e per una via laterale. `deck-building-game.txt`, letto il 31 agosto 2026: *StarCraft: The Board Game*, 2007, fu il primo gioco di costruzione di mazzo; *Dominion*, Rio Grande Games, 2008, fu il primo ad avere successo e a fissare il genere, e la sua diffusione produsse *Thunderstone*, *Ascension*, *Legendary*, *Clank!*. Il meccanismo del genere è esattamente un motore: si comincia con un mazzo piccolo di carte di poco valore, ogni turno se ne pescano alcune, quelle giocate danno la valuta con cui se ne comprano altre dal mercato centrale, e le nuove entrano nel mazzo per i turni successivi.

Il caso più noto in forma di videogioco è precedente. `simcity.txt`, letto il 31 agosto 2026: lo sviluppo del primo *SimCity* comincia nel 1985 con Will Wright, il gioco esce nel 1989 pubblicato da Maxis, e Wright dichiarò di essere partito da una funzione di creazione delle mappe del gioco *Raid on Bungeling Bay*. `game-mechanics.txt` lo usa come esempio della meccanica: il denaro attiva meccanismi di costruzione, che a loro volta aprono anelli di retroazione fra popolazione, posti di lavoro, energia, capacità di trasporto e tipi di zona.

**Un dettaglio della classificazione va detto, perché è strano.** In `game-mechanics.txt` la costruzione di un motore non è una sezione a sé: è una sottosezione della **raccolta di insiemi**, accanto alla posa di tessere. Non è una parentela ovvia, la pagina non la motiva, e non ci sono note sotto quella sezione.

## Varianti e parenti

- **Motore additivo** — ogni pezzo alza il reddito di una quantità fissa. La crescita è lineare, e il totale accumulato cresce come un quadrato.
- **Motore moltiplicativo** — ogni pezzo moltiplica il reddito. Diverge, e chiede quasi sempre un tetto imposto da fuori.
- **Costruzione di mazzo** — le carte comprate tornano in mano e sono loro il reddito. Voce 105, mazzo di carte.
- **Costruzione di quadro** (*tableau building*) — i pezzi restano scoperti davanti a chi gioca invece di entrare in un mazzo. Su Wikipedia inglese `Tableau_building` non esiste come pagina, verificato con l'API il 31 agosto 2026.
- **Albero tecnologico** — i pezzi hanno prerequisiti fra loro, e allora il motore è anche un cancello: voce 263, sblocco di contenuti.
- **Retroazione negativa** — la struttura opposta, in cui il successo rende più difficile il successo dopo.
- **Motore fatto di oggetti invece che di numeri** — quello che si costruisce non è un reddito ma uno strumento, e lo strumento fa il lavoro. Voce 39, tabella e voce 96, registro / catalogo sono i due contenitori tipici.
- **Voce 270, risorse da spendere** — la forma da cui questa si separa: là la risorsa si consuma, qui produce.
- **Voce 271, collezione** — anche là si accumula, ma i pezzi non fanno niente finché la serie non è completa.
- **Voce 275, emergenza** — quello che succede quando gli anelli di retroazione sono più d'uno e interagiscono.
- **Voce 279, simulazione** — un motore osservato invece che pilotato.

## Che cosa se ne sa

**Nessuna delle 906 pagine locali misura questa forma.** Non ci sono esperimenti, non ci sono confronti, non ci sono numeri sull'effetto che ha su chi gioca. Quello che c'è è una descrizione strutturale, e i conti che seguono sono nostri.

**La struttura ha un limite dichiarato dalla teoria dei sistemi, e va riportato per intero.** `positive-feedback.txt` cita Donella Meadows: «gli anelli di retroazione positiva sono all'origine della crescita, dell'esplosione, dell'erosione e del collasso nei sistemi. Un sistema con un anello positivo non controllato finisce per distruggersi. È per questo che ce ne sono così pochi. Di solito, prima o poi, entra in gioco un anello negativo.» La pagina aggiunge che nel mondo reale gli anelli positivi non producono quasi mai crescita indefinita: qualcosa li limita.

**Nei giochi il limite è messo apposta, e la pagina sull'equilibrio spiega con che forma.** `game-balance.txt`, letto il 31 agosto 2026: la potenza va resa una funzione **concava** di una misura del successo grezzo. L'esempio dato è la scala a livelli dei giochi di ruolo — più il personaggio diventa capace, più punti esperienza guadagna nello stesso tempo di gioco, ma più punti esperienza gli servono per salire, e il risultato è che il livello cresce **all'incirca linearmente nel tempo di gioco** invece che esponenzialmente. La stessa pagina dice che con una retroazione positiva netta forte i successi iniziali si moltiplicano molto in fretta e chi gioca arriva a una posizione da cui perdere è quasi impossibile; e che con una retroazione negativa netta forte i pareggi diventano frequenti.

**E dice dove sta il vero freno, che non è il costo ma il collo di bottiglia.** Sempre `game-balance.txt`: le capacità possono dipendere da un collo di bottiglia dove la retroazione positiva è assente o debole — un solo attrezzo alla volta si può usare, e averne un secondo quasi identico in tasca aggiunge poco.

**Un motore rende quanto l'orizzonte gli concede, e il conto è breve.** Su dodici turni, con reddito iniziale 1, un pezzo che costa 3 e alza il reddito di 1 dal turno dopo: chi non compra niente finisce con 12, chi compra bene finisce con **28**, cioè 2,33 volte tanto, e i piani che raggiungono il massimo sono **due su 768 successioni di acquisto valide** (`build/check_272.py`, per programmazione dinamica sugli stati e per enumerazione completa delle 4 096 successioni; i due metodi concordano). Tutti e due i piani migliori comprano **cinque pezzi**, e nessuno dei due compra ai primi due turni, perché prima non si hanno tre monete.

**Il momento oltre il quale un pezzo non si ripaga si calcola in una riga, e sorprende quanto sia presto.** Un pezzo comprato all'inizio del turno *t* rende una unità per ognuno dei 12 − *t* turni che restano e ne costa 3: pareggia al **turno 9** e da lì in poi è in perdita, di 1 al turno 10, di 2 al turno 11, di 3 al turno 12 (`build/check_272.py`, per scansione dei dodici turni e per la disuguaglianza 12 − *t* ≥ 3). **Un quarto della partita è tempo in cui costruire è sbagliato**, e nessuna regola sul tavolo lo dice.

**Aggiungere un pezzo grande a un motore che ha un collo di bottiglia piccolo non serve quasi a niente, e questo si misura.** Con un repertorio di riferimenti da 1 e da 40 servono in media 24,02 oggetti per rappresentare un peso qualsiasi da 1 a 400. Aggiungendo un riferimento da 200 la media scende a **22,00**, cioè si risparmiano 2,02 oggetti; aggiungendo invece un riferimento da 5 scende a **10,03**, cioè se ne risparmiano 14,00 (`build/check_272.py`, minimo calcolato per programmazione dinamica del resto e controllato con la regola avida, che qui concorda su tutti i casi provati). **Il pezzo che fa crescere il motore è quello che toglie il collo di bottiglia, non quello che sembra più potente**, ed è la stessa cosa che `game-balance.txt` dice a parole.

## Esempi trovati

Da *Dominion*, 2008, come lo descrive `deck-building-game.txt`: si parte con un mazzo di dieci carte quasi inutili, si comprano carte che danno più valuta, quelle carte tornano nel mazzo, e da lì in poi ogni giro pesca in media meglio del precedente. Il mazzo è insieme la fabbrica e il prodotto.

Da *SimCity*, 1989, come lo descrive `game-mechanics.txt`: il denaro costruisce zone, le zone attirano popolazione, la popolazione paga tasse, le tasse sono denaro. Quattro anelli intrecciati — persone, posti di lavoro, energia, trasporti — invece di uno solo, ed è questo che rende il gioco difficile da prevedere.

Dalla scala dei punti esperienza dei giochi di ruolo, in `game-balance.txt`: il caso in cui il freno è messo dentro la scala stessa, con soglie che crescono alla stessa velocità con cui cresce il guadagno.

Dall'elettronica, in `positive-feedback.txt`: il circuito rigenerativo degli anni Venti, in cui una parte del segnale in uscita torna in ingresso in fase e aumenta il guadagno. È lo stesso schema, e i giochi lo hanno preso in prestito con settant'anni di ritardo.

Dalla strategia in tempo reale, in `game-balance.txt`: il **mantenimento**, cioè una tassa sulle risorse che cresce con il numero di unità possedute. È un motore a cui è stato attaccato di proposito un freno proporzionale.

## Una nostra versione

> **La bilancia che si costruisce i pesi da sola**
>
> Ti serve una gruccia appesa a un chiodo, due sacchetti di plastica appesi alle due estremità, e un mucchio di monete da 1 centesimo. Quante ne hai, non importa.
>
> **La prima regola.** L'unità è una moneta. Non ti serve sapere quanti grammi pesa: ti serve solo che le monete siano tutte uguali fra loro.
>
> **La seconda regola, ed è quella che conta.** Ogni volta che scopri quanto pesa una cosa, quella cosa diventa un peso. Da quel momento la puoi usare al posto delle monete.
>
> ```
>  QUELLO CHE SO GIA'
>
>  oggetto ................  vale ....... monete   trovato con .............
>  oggetto ................  vale ....... monete   trovato con .............
>  oggetto ................  vale ....... monete   trovato con .............
>  oggetto ................  vale ....... monete   trovato con .............
>  oggetto ................  vale ....... monete   trovato con .............
> ```
>
> Comincia da una cosa leggera — una gomma, un mazzo di carte, una pila stilo — e pesala in monete, contandole.
>
> Poi guarda la riga che hai appena scritto e rispondi: **per pesare la prossima cosa, quante monete ti risparmi usando quello che hai gia'?**
>
> ```
>  quello che voglio pesare .................
>  oggetti che poso sul piatto:
>      ......... x .........   +  ......... x .........   +  ....... monete
>  in tutto sono ....... oggetti invece di ....... monete
> ```
>
> Ultima domanda, e non ha una risposta sola. Ti do' due oggetti da aggiungere al repertorio: **uno che pesa cinque monete e uno che ne pesa duecento.** Ne puoi tenere uno solo. Quale prendi, e perché?

L'unità è scelta e non data, come alla voce 54, misurare. Il motore è la tabella: ogni riga scritta rende più corta la riga dopo, e non c'è nessun contatore da tenere aggiornato, perché quello che cresce è un oggetto scritto sul foglio e non un numero in testa a qualcuno. L'ultima domanda è il collo di bottiglia messo in forma di scelta: **il pezzo da cinque fa risparmiare in media quattordici oggetti, quello da duecento ne fa risparmiare due**, e chi ha davanti la tabella può accorgersene contando invece di crederci.

Dove si romperebbe: se si chiedesse al sistema di verificare i pesi, non potrebbe. La fotografia di questo foglio dice che cosa è stato scritto, non se sia vero. Ma qui la verifica è fisica e non passa da nessuno — la gruccia sta in equilibrio o pende — ed è la famiglia già segnata in `OSSERVAZIONI.md` come la migliore disponibile.

## Da riprendere alla rassegna

**Un motore fatto di risorse chiede un contabile; un motore fatto di oggetti no.** È la seconda volta in questo capitolo che la via d'uscita è la stessa — alla voce 266, vite / tentativi e alla voce 270, risorse da spendere si era rinunciato a obbligare per chiedere di registrare —, ma qui la sostituzione è più forte: non si rinuncia a niente. Una tabella che cresce **è** il motore, e ogni riga scritta è insieme il pezzo comprato e la prova che è stato comprato.

**L'orizzonte è il parametro che decide, e in casa non esiste.** Un pomeriggio non ha un numero di turni dichiarato, quindi non c'è modo di sapere quando smettere di costruire. O l'orizzonte si dichiara sul foglio — «hai sei righe» —, e allora il calcolo del pareggio diventa una cosa che si può fare, oppure il motore non ha un momento in cui si raccoglie e resta un accumulo.

**Il collo di bottiglia è il concetto più esportabile di questa voce.** Vale ovunque una cosa cresca: quello che limita non è quello che manca di più, è quello che non cresce. Da provare come domanda finale su qualunque scheda che chieda di costruire qualcosa in più passi — *che cosa ti ha fatto perdere più tempo, e come lo toglieresti?*

**Il termine non ha una pagina.** `Engine_building` su Wikipedia inglese rimanda alla messa a punto dei motori d'automobile, e la definizione della meccanica vive in tre righe dentro `Game_mechanics`, per giunta come sottosezione della raccolta di insiemi. È il quinto caso raccolto di forma diffusa e mal documentata, e conferma quello che si era già scritto alla chiusura del capitolo 8 e alla voce 260, serie di giorni (streak): le pratiche più diffuse non sono quelle meglio descritte.

**Da guardare accanto alla voce 257, livelli.** Là la scala è data e si sale; qui la scala si costruisce mentre si sale. Sono la stessa curva vista da chi la subisce e da chi la fa, e alla rassegna converrà chiedersi se non sia sempre preferibile la seconda.
