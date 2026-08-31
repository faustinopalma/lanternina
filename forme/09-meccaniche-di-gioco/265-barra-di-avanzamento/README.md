# Barra di avanzamento

- **Numero** 265 nell'enciclopedia, capitolo 9 — Meccaniche di gioco
- **Si chiama anche** barra di progresso, indicatore di avanzamento, percentuale completata, «sei al 64%», tessera a timbri, cartellina dei bollini, *progress bar*, *progress tracker*, *completion meter*
- **In una riga** quanto manca alla fine, mostrato mentre si va.
- **Fonti** `progress-bar.txt`, `progress-indicator.txt`, `throbber.txt`, `loading-screen.txt`, `perceived-performance.txt`, `goal-pursuit.txt`, `zeigarnik-effect.txt`, `gamification.txt`, lette il 31 agosto 2026. I conti sulle due tessere e sullo scarto fra barra e lavoro sono nostri, verificati in `build/check_265.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

C'è una cosa lunga da fare, e mentre la si fa si vede quanta ne resta. La quantità fatta e la quantità totale stanno in un rapporto, e il rapporto si disegna.

**Sull'asse dell'apertura del capitolo — che cosa produce il numero, si veda la voce 256, punti — questa è la somma della voce 256, punti divisa per un totale noto.** La differenza non è il numeratore: è **il denominatore**. Un punteggio cresce e basta; una barra ha una fine dichiarata, e da quella fine ricava una seconda informazione — quanto manca — che il punteggio non contiene.

**Va tenuta separata dal grafico di andamento descritto alla voce 259, classifica.** Il grafico mostra come si va rispetto a **come si andava prima**: non ha un traguardo, e la sua unità di misura è il miglioramento. La barra mostra come si va rispetto a **dove si finisce**: ha un traguardo, e la sua unità di misura è il residuo. Le due sono state accostate perché usano tutte e due uno standard di riferimento individuale invece che sociale, ma la barra sa dove finisce e il grafico no. **Un grafico non può arrivare a cento.**

Parti mobili:

- **Il denominatore.** Quanti pezzi in tutto. È la parte che si può scegliere, e sceglierla è già mezza forma.
- **Da dove parte.** Da zero, oppure da un pezzo già fatto che è stato regalato.
- **Se dice il fatto o il residuo.** «Hai fatto sei» e «te ne mancano quattro» sono lo stesso stato con due cornici.
- **Se è determinata o no.** `progress-bar.txt` chiama **indeterminata** la barra usata quando non si sa quanto sia lungo il compito: si muove senza dire a che punto è, e a quel punto assomiglia a un mulinello più che a una barra.
- **Se i pezzi sono uguali.** Se non lo sono, la barra dice una cosa e il lavoro ne dice un'altra.
- **Quante barre.** Una per il tutto, e una per il pezzo in corso: `progress-bar.txt` registra che le installazioni lunghe ne mostrano spesso due insieme.
- **Chi la muove.** Un programma che stima, oppure una mano che riempie una casella.

## Da dove viene

**Prima dei calcolatori, e da un ufficio.** `progress-bar.txt`: nel **1896** Karol Adamiecki sviluppa un diagramma che chiama *armonogramma*, e che oggi si conosce come diagramma di Gantt. Adamiecki lo pubblica solo nel **1931**, e in polacco; nel frattempo Henry Gantt disegna il suo attorno al **1910-1915** e lo diffonde in Occidente, e il nome resta a lui. **La prima barra di avanzamento non misura una macchina: misura un cantiere.**

**Nel calcolo, due date e due nomi.** La prima barra grafica compare nella tesi di dottorato di **Mitchell Model, 1979**, *Monitoring System Behavior in a Complex Computational Environment*, allo Xerox PARC. Nel **1985 Brad Myers** presenta al convegno CHI un articolo sugli «indicatori di percentuale completata», e da lì la cosa entra nell'uso comune.

**Il parente che dichiara di non sapere niente ha un nome proprio.** `throbber.txt`: un mulinello è un'immagine animata che segnala che qualcosa sta succedendo, e **a differenza di una barra non dice quanta parte dell'azione sia stata completata**. È la stessa forma privata del denominatore, e la distinzione è netta: dove non si conosce il totale, l'onestà è muoversi senza numeri.

**La schermata di caricamento è il contenitore in cui la barra è nata come intrattenimento.** `loading-screen.txt` la descrive come l'immagine mostrata mentre un programma carica, e nomina i due abitanti: il mulinello, che segnala attività, e la barra, che stima lo stato di completamento e quanto resta.

## Varianti e parenti

- **Barra determinata** — c'è un totale, e la frazione è calcolata.
- **Barra indeterminata** — non c'è un totale; si muove per dire che qualcosa sta succedendo.
- **Mulinello** — la stessa cosa senza forma di barra, e senza nessuna promessa.
- **Tessera a timbri** — la barra su carta, con le caselle al posto dei pixel. È la forma su cui è stato fatto l'esperimento migliore di questa voce.
- **Barra con avanzamento regalato** — comincia già a un quinto, e il quinto non lo si è fatto.
- **Due barre insieme** — una per il tutto, una per il pezzo in corso.
- **Barra a ritroso** — mostra il residuo invece del fatto. Confina con la voce 189, conto alla rovescia, che però conta minuti e non pezzi.
- **Elenco con le spunte** — la stessa informazione senza il rapporto, e con i nomi delle cose.
- **Voce 257, livelli** — la soglia, che è una barra con una tacca sola.
- **Voce 259, classifica** — dove il gemello, il grafico di andamento, misura il miglioramento invece del residuo.
- **Voce 261, obiettivo giornaliero** — il denominatore fissato per una giornata.
- **Voce 40, linea del tempo** — la stessa geometria applicata a fatti invece che a lavoro.

## Che cosa se ne sa

**L'esperimento migliore di questa voce non riguarda una barra su uno schermo: riguarda una tessera a timbri di un autolavaggio, e dà due numeri.** `goal-pursuit.txt` riporta Nunes e Drèze, *Journal of Consumer Research*, 2006, l'**effetto dell'avanzamento regalato**. Trecento tessere fedeltà distribuite ai clienti di un autolavaggio professionale. Metà avevano **dieci caselle, di cui due già timbrate**: mancavano otto lavaggi. L'altra metà avevano **otto caselle vuote**: mancavano otto lavaggi. **Lo stesso lavoro, disegnato in due modi.** Il tempo medio fra un lavaggio e l'altro è risultato più corto per chi aveva la tessera regalata, e il tasso di riscossione — le tessere completate e consegnate — è stato **del 34% contro il 19%**, differenza dichiarata statisticamente significativa. **La pagina non dice come le due metà siano state assegnate**, e questo va tenuto presente: è un esperimento sul campo, non un'assegnazione a caso dichiarata.

**Il conto che la accompagna si fa da soli, e dice esattamente di quanto la prima tessera sia avanti.** A parità di lavaggi ancora da fare, la tessera regalata mostra sempre una percentuale più alta, e lo scarto si chiude in modo regolare:

```
     lavaggi fatti   tessera da 10 con 2 regalati   tessera da 8   scarto
                 0                          20,0%           0,0%     20,0
                 2                          40,0%          25,0%     15,0
                 4                          60,0%          50,0%     10,0
                 6                          80,0%          75,0%      5,0
                 8                         100,0%         100,0%      0,0
```

(`build/check_265.py`: lo scarto calcolato per differenza delle due frazioni **e** per la forma chiusa (8−k)/40, concordi su tutte e nove le righe.) **Lo scarto è massimo all'inizio — venti punti percentuali — e cala di due punti e mezzo per ogni lavaggio.** Cioè: il vantaggio della tessera regalata è tutto nel momento in cui non si è ancora fatto niente, che è il momento in cui si decide se cominciare.

**Il gradiente verso l'obiettivo è del 1932 ed è nato sui ratti.** `goal-pursuit.txt`: Clark Hull osserva che i ratti aumentano lo sforzo man mano che la distanza dal cibo diminuisce, e formula l'ipotesi che la motivazione cresca in modo monotono dall'inizio alla fine. **La pagina non dà nessuna grandezza per il caso umano**, e usa la formula «è stata usata per prevedere il comportamento umano».

**Poi c'è la scoperta che la cornice conta quanto lo stato, ed è misurata su un caso preciso.** Bonezzi e colleghi, 2011: a studenti universitari sono stati dati 15 dollari da destinare a un ente che aveva un obiettivo di 300 dollari. A un gruppo l'avanzamento era presentato come **quanto era già stato raccolto**, all'altro come **quanto mancava**. Il primo gruppo ha donato di più **nelle fasi iniziali**, il secondo **nelle fasi finali**. Da qui il gradiente a U: la motivazione è più alta all'inizio e alla fine, e più bassa in mezzo. **Sono le due letture dello stesso stato — sommano sempre a uno — e producono comportamenti diversi in momenti diversi.**

**Il meccanismo che l'industria cita per giustificare le barre è quello che non ha retto alla replica, e questo va detto per intero.** `zeigarnik-effect.txt` descrive l'effetto Zeigarnik — si ricordano meglio i compiti interrotti che quelli finiti — pubblicato nel 1927 su *Psychologische Forschung* dopo che Kurt Lewin aveva notato che un cameriere ricordava meglio le ordinazioni non ancora pagate. La stessa pagina elenca, alla voce «usi», gli **indicatori di avanzamento** dei programmi in abbonamento, con l'esempio letterale: «il tuo profilo è completo al 64%». **E la stessa pagina dice che l'effetto non ha retto**: più tentativi di replica in altri paesi non hanno trovato differenze significative fra compiti finiti e interrotti, e una rassegna sistematica con meta-analisi del **2025** non ha trovato **nessun vantaggio di memoria per i compiti non finiti**, mentre ha trovato una tendenza generale a **riprendere** i compiti — l'effetto Ovsiankina, che è un'altra cosa. La conclusione riportata: l'effetto Ovsiankina è una tendenza generale, l'effetto Zeigarnik «manca di validità universale». **La barra al 64% funziona forse, ma non per la ragione con cui viene venduta.**

**La barra costa una parte di quello che misura, e la fonte lo dice senza girarci intorno.** `perceived-performance.txt`: disegnare e aggiornare una barra mentre si carica un file «soddisfa chi guarda, ma ruba tempo al processo che sta davvero caricando il file», di solito pochissimo. E la frase che vale per tutta la famiglia: **tutte queste tecniche devono sfruttare l'incapacità di chi guarda di giudicare la prestazione vera**, altrimenti sarebbero considerate dannose.

**Su quanto una barra aiuti, la ricerca di Myers è una direzione senza grandezza.** `progress-bar.txt`: Myers fece svolgere ricerche in una base di dati, ad alcuni con la barra e ad altri senza; chi aspettava guardando la barra descrisse un'esperienza complessivamente più positiva, e Myers concluse che la barra riduceva l'ansia ed era più efficiente. **Nessun numero, nessuna numerosità, nessuna dispersione.** È la trappola già registrata più volte in questo capitolo, e qui la fonte è del 1985.

**Una barra che avanza per numero di passi mente quando i passi sono disuguali, e si può misurare di quanto.** Cinque passi di peso 1, 1, 2, 3 e 8 — quindici in tutto:

```
     passi finiti   la barra dice   il lavoro fatto e'   scarto
                1           20,0%                 6,7%     13,3
                2           40,0%                13,3%     26,7
                3           60,0%                26,7%     33,3
                4           80,0%                46,7%     33,3
                5          100,0%               100,0%      0,0
```

(`build/check_265.py`: lo scarto massimo trovato per scansione dei prefissi **e** cercato su tutti i 60 ordinamenti distinti dei cinque passi, concordi.) **L'ordine dal più corto al più lungo è quello che rende la barra più bugiarda — trentatré punti percentuali —, e l'ordine che comincia dai pezzi grossi la rende esatta**: con la successione 3, 8, 1, 1, 2 la barra non corre mai avanti al lavoro. `progress-bar.txt` registra il fenomeno senza quantificarlo: le barre mostrano spesso accelerazioni, rallentamenti e pause, e per questo «possono essere disegnate perché sembrino più veloci».

## Esempi trovati

Le trecento tessere dell'autolavaggio di Nunes e Drèze, che sono la barra di avanzamento su carta e insieme l'esperimento migliore che ne sia stato fatto.

Il diagramma di Adamiecki del 1896, pubblicato in polacco nel 1931 e conosciuto con il nome di un altro.

La tesi di Mitchell Model del 1979, che contiene la prima barra grafica di cui la pagina abbia notizia.

«Il tuo profilo è completo al 64%», riportato da `zeigarnik-effect.txt` come esempio di indicatore di avanzamento nei programmi in abbonamento.

Le due barre sovrapposte delle installazioni lunghe: una per il tutto e una per il file che si sta copiando adesso.

La barra a bastone di barbiere delle barre indeterminate, che si muove senza avanzare.

## Una nostra versione

**Il limite dominante qui è mite, e conviene dirlo subito.** Una barra conta pezzi, non minuti: applicando il criterio del capitolo, sta dentro un foglio senza ripieghi, purché il totale stia sul foglio. Quello che il sistema non può fare è una barra che attraversi i giorni, perché non tiene nessun registro; ma una barra della singola pagina è solo una fila di caselle stampate. **Il pezzo interessante non è disegnarla: è che il denominatore lo si può scegliere, e la scelta si vede.**

> **Le due tessere dell'autolavaggio**
>
> Nel 2006 due ricercatori hanno dato trecento tessere fedeltà ai clienti di un autolavaggio. Metà avevano una tessera, metà l'altra. Eccole:
>
> ```
>   Tessera A   [X][X][ ][ ][ ][ ][ ][ ][ ][ ]
>   Tessera B   [ ][ ][ ][ ][ ][ ][ ][ ]
> ```
>
> Su tutte e due, il lavaggio gratis arriva quando la tessera e' piena. La A ha dieci caselle e due sono gia' timbrate, regalate all'inizio. La B ne ha otto e sono tutte vuote.
>
> **Prima domanda, e rispondi prima di contare: quale delle due prenderesti?**
>
> **Seconda domanda: quanti lavaggi devi pagare, con l'una e con l'altra?**
>
> ```
>   Con la A:  ────────      Con la B:  ────────
> ```
>
> **Terza: dopo quattro lavaggi, che percentuale mostra la A? E la B?**
>
> ```
>   La A dice  ──────%       La B dice  ──────%
> ```
>
> Adesso il fatto. Di quelle trecento tessere vere, **le tessere A completate e riscosse sono state il 34%, le B il 19%.** Quasi il doppio, per lo stesso identico numero di lavaggi da pagare.
>
> **Ultima domanda, e non ha una risposta scritta da nessuna parte: se avessi saputo prima che le due tessere chiedono la stessa cosa, avresti risposto diverso alla prima domanda? E adesso che lo sai, la A ti dà comunque piu' voglia di cominciare?**

La forma è tutta nella prima domanda posta prima del conto: la risposta d'istinto e la risposta contata differiscono, e la differenza è l'oggetto. Le due tessere sono la stessa richiesta, e il 34% contro il 19% è il prezzo di come è disegnata. L'ultima domanda non si può sbagliare, e chiede a chi legge di guardare una cosa su di sé dopo averla vista dall'esterno.

**Dove si rompe.** Non si rompe nel disegno: dieci caselle e otto caselle stanno su un foglio in bianco e nero. Si rompe nell'uso, se le caselle vanno riempite in giorni diversi, perché allora la tessera deve sopravvivere fra una volta e l'altra e qualcuno deve ricordarsi di timbrarla. **Una barra dentro un foglio è carta; una barra fra un foglio e l'altro è un registro su una persona**, ed è la stessa linea che separa la voce 22, diario / registro dalla voce 260, serie di giorni (streak).

## Da riprendere alla rassegna

**Il denominatore è la parte che si sceglie, e nessuna fonte lo tratta come una scelta.** Le stesse otto cose da fare, presentate come otto su otto o come dieci su dieci con due regalate, hanno prodotto tassi di riscossione del 19% e del 34%. **Quando il progetto stamperà una fila di caselle, il numero di caselle sarà una decisione con una misura sotto**, e questa è la misura.

**Il grafico di andamento e la barra sono stati accostati troppo in fretta, e vanno separati.** La barra ha una fine e misura il residuo; il grafico non ha una fine e misura il miglioramento. La cosa che il capitolo ha trovato di più promettente alla voce 259, classifica è il secondo, non la prima. **Da guardare come due strumenti diversi, e da chiedersi quale dei due il formato possa reggere: la barra sì dentro un foglio, il grafico solo con un registro.**

**Un indicatore consuma una parte di quello che indica.** La formulazione di `perceived-performance.txt` è la più utile raccolta finora sul costo di mostrare qualcosa: disegnare la barra ruba tempo al caricamento, e la tecnica funziona solo perché chi guarda non sa giudicare la prestazione vera. **Vale su carta come su schermo: ogni casella stampata è inchiostro che non è una domanda.**

**Il meccanismo con cui si giustifica una forma può non reggere alla replica, e la forma resta in piedi lo stesso.** L'effetto Zeigarnik è citato ovunque come ragione degli indicatori di avanzamento, e una meta-analisi del 2025 non ha trovato il vantaggio di memoria. L'effetto vicino che ha retto — la tendenza a riprendere quello che si è cominciato — è un'altra cosa e sostiene un'altra forma. **Alla rassegna: quando una forma è difesa da una spiegazione, controllare la spiegazione separatamente dalla forma.**
