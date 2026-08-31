# Turno

- **Numero** 280 nell'enciclopedia, capitolo 9 — Meccaniche di gioco
- **Si chiama anche** mossa, giocata, round, tornata, fase, tick, *turn*, *move*, *play*, gioco a turni, uno alla volta, tocca a te
- **In una riga** il tempo diviso in unità, e una cosa per unità.
- **Fonti** `timekeeping-in-games.txt`, `game-mechanics.txt` sezione «Turns», `simultaneous-action-selection.txt`, `initiative-rpg.txt`, tutte lette il 31 agosto 2026; i conti sono in `build/check_280.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Il tempo di un'attività viene diviso in segmenti, e dentro ogni segmento succede una cosa e poi si passa al segmento dopo. Il segmento si chiama turno. La definizione che dà `game-mechanics.txt` è già tutta lì: «un turno è un segmento di gioco riservato a certe azioni prima di passare al turno successivo, dove la sequenza degli eventi in gran parte si ripete».

Parti mobili:

- **Che cosa fa finire un turno.** Un numero di azioni, una cosa fatta, un evento esterno, oppure — ed è un caso soltanto — un tempo trascorso. Il turno non è un orologio: è quello che si mette al posto dell'orologio.
- **Di chi è il turno.** `game-mechanics.txt` separa i **turni di giocatore**, in cui uno agisce e gli altri aspettano, dai **turni di gioco**, in cui tutti contribuiscono allo stesso turno. Monopoli e gli scacchi hanno i primi; *Civilization* mette una serie di turni di giocatore e poi un giro di scambi a cui partecipano tutti.
- **Chi comincia.** `timekeeping-in-games.txt` elenca tre convenzioni per i giochi a turni alternati: **fisso**, il primo è sempre lo stesso; **a rotazione**; **a sorte**. E ne aggiunge una quarta, il punteggio di iniziativa, calcolato su una caratteristica, sulla posizione o su un tiro di dado.
- **Se i turni sono uguali fra loro.** Non è detto. Il gioco da tavolo *Imperium Romanum II*, 1985, ha una fase di tassazione e mobilitazione ogni tre turni e non negli altri; in *Napoleon*, 1974, un turno su tre è un turno di notte in cui non si può combattere.
- **Quanto rappresenta un turno.** Un turno può rappresentare un'ora, un giorno, un anno. In *Dialect* un gruppo di turni è un'era di una società; in *The Quiet Year* ogni turno è una settimana; in *Visigoths vs. Mall Goths* il turno di ogni squadra è un'ora precisa al centro commerciale.

Togliendo la divisione si ottiene il tempo continuo, dove tutti agiscono insieme e chi è più rapido guadagna. Togliendo invece l'alternanza e tenendo la divisione si ottiene il turno simultaneo, che è la cosa descritta alla fine della sezione «Varianti e parenti».

## Da dove viene

Non c'è una data di nascita, perché la divisione in turni è più vecchia di qualunque cosa la descriva: gli scacchi, il go e i giochi di dadi la usano da secoli senza chiamarla in nessun modo. Il nome tecnico arriva con la letteratura sui giochi da tavolo e poi con i videogiochi, dove serviva un termine per distinguere due modi di far passare il tempo.

Sull'inglese di Wikipedia **non esiste una pagina dedicata al turno**: `Turn-based_game` rimanda a `Timekeeping in games`, cioè alla gestione del tempo in generale, e `Turn-based_strategy` rimanda a `Strategy video game` (verificato con l'API di MediaWiki il 31 agosto 2026, `build/check_titoli_280.py`). La cosa più elementare del capitolo non ha una voce propria; sta dentro la voce sull'orologio, che è quasi il contrario di quello che è.

I sistemi di iniziativa dei giochi di ruolo — chi agisce prima, dentro un turno collettivo — vengono dichiaratamente dai giochi di guerra da tavolo, dice `initiative-rpg.txt`, e sono la parte del turno che è stata formalizzata di più: quattro metodi elencati, dal numero di iniziativa di *Dungeons & Dragons* alla scelta di *Marvel Heroic Roleplaying*, dove chi ha appena agito sceglie il prossimo, e l'ultimo del giro sceglie chi comincerà il giro dopo.

I turni cronometrati sono più recenti e nascono contro un abuso: `timekeeping-in-games.txt` cita gli scacchi da scambio a quattro giocatori, dove uno può prendere un pezzo, darlo al compagno e poi **aspettare** a muovere sulla propria scacchiera, così che il compagno usi il vantaggio per molte mosse. Il rimedio è dieci secondi a mossa, e per ogni dieci secondi in più l'avversario toglie un pedone.

## Varianti e parenti

- **Turno di giocatore** — uno agisce, gli altri guardano.
- **Turno di gioco** — un solo turno a cui tutti contribuiscono.
- **Turno simultaneo** — tutti scelgono insieme e in segreto, poi si scopre. `simultaneous-action-selection.txt` dice che serve un metodo «segreto ma vincolante» per impegnarsi alla propria mossa; in *Diplomacy*, 1959, si scrivono gli ordini e si scoprono insieme.
- **Fase** — un turno diviso in parti dedicate a cose diverse. In *Agricola*, 2007, ogni turno ha manutenzione, rifornimento e lavoro, e una quarta fase di raccolto ogni tanto.
- **Tick** — un turno che dura sempre lo stesso tempo reale, e che ricarica un numero di azioni. È la forma che sta dalla parte dell'orologio.
- **Round** — un intervallo comune più lungo della singola azione, dentro il quale si decide.
- **Iniziativa** — l'ordine dentro il turno, deciso da una caratteristica o da un tiro.
- **Interruzione** — agire fuori dal proprio turno, spendendo qualcosa. `timekeeping-in-games.txt` cita gli attacchi di opportunità di *Dungeons & Dragons* e l'azione preparata.
- **Orologio di avanzamento** — un cerchio a spicchi che il conduttore riempie via via, per le cose che non stanno dentro un turno solo. Viene da *Blades in the Dark*.
- **Linea del tempo** — i giocatori costruiscono l'ordine degli eventi invece di subirlo: in *Microscope* si inventa una cronologia e poi si sceglie quale pezzo giocare.
- **Voce 267, timer** — l'altra metà della famiglia del tempo, e lì sta tutto l'orologio: byo-yomi, modalità clessidra, e tre regole d'orologio che sulla stessa partita danno −154 s, +86 s e −28 s. Questa scheda non lo riapre.
- **Voce 80, tempo** — la domanda che si risolve aspettando o tornando dopo, che è il turno esteso a più giorni.
- **Voce 104, gioco da tavolo** — il posto dove il turno vive normalmente.
- **Voce 189, conto alla rovescia** e **voce 88, sfida contro un tempo** — le due forme in cui il tempo è continuo e incalza.

## Che cosa se ne sa

Le fonti locali non riportano nessuna misura sul turno: `timekeeping-in-games.txt` ha una sezione lunga di dibattito fra sostenitori del tempo reale e sostenitori dei turni, e **sono argomenti, non dati** — nessuna grandezza, nessun confronto, nessuna nota sotto le affermazioni. È la stessa cosa già registrata per `simulation.txt` alla voce 279, simulazione. La riportiamo per quello che è.

Fra quegli argomenti, uno riguarda direttamente chi legge questi fogli: **con i turni «un giocatore con riflessi più lenti non è in svantaggio rispetto a uno più veloce; conta solo la capacità di pensare e risolvere il problema che si ha davanti»**. Il turno è il dispositivo che toglie la velocità dalla partita. Nel verso opposto, la fonte registra che i giochi a turni «hanno troppe regole e sono difficili da padroneggiare», e che aspettare il turno degli altri stanca.

Quello che si può calcolare, invece, è che cosa aggiunge la divisione in turni. **Sei turni con quattro azioni possibili in ognuno danno 4 096 successioni distinte, e soltanto 84 esiti distinti se l'ordine non contasse**: l'ordine porta 48,76 volte l'informazione che porta il conteggio (`build/check_280.py`, per enumerazione delle successioni ridotte a multinsieme e per la formula di stelle e barre). Il turno è precisamente quello che fa esistere l'ordine: senza turni resterebbe la somma, che alla voce 256, punti si è già visto perdere per costruzione che cosa sia stato fatto.

Sulla stessa base: **il 38,09% di quelle successioni usa tutte e quattro le azioni almeno una volta** (enumerazione e inclusione ed esclusione, stesso script). Sei turni non bastano a garantire varietà; se la varietà serve, va chiesta.

E la scelta di chi comincia non è neutra, con un conto che si fa una volta sola. **Tre giocatori, dodici turni: fisso dà dodici primi turni a uno e zero agli altri; a rotazione dà quattro a testa; a sorte lascia il 2,3116% di probabilità che qualcuno non cominci mai un turno, e un divario atteso di 3,37 turni fra chi comincia di più e chi comincia di meno** (`build/check_280.py`, per enumerazione esatta delle 531 441 assegnazioni e per inclusione ed esclusione, con il divario ricontrollato sulle composizioni multinomiali). Nessuna delle tre convenzioni è più semplice delle altre da scrivere su un foglio, e producono partite diverse. È la quinta volta in questo capitolo che una convenzione di conteggio decide un esito senza che nessuno la dichiari — dopo la voce 259, classifica, la voce 267, timer, la voce 271, collezione e la voce 268, scelta con conseguenza.

`simultaneous-action-selection.txt` aggiunge un limite del turno simultaneo che è strutturale e non di gusto: **alcune mosse non si possono fare insieme perché una impedisce l'altra** — l'alfiere che prende la regina e la regina che prende l'alfiere non possono succedere tutti e due. I giochi che lo permettono separano il movimento dal combattimento, come *Junta*, dove nessun pezzo viene tolto finché tutti non si sono mossi.

## Esempi trovati

Da `timekeeping-in-games.txt`, il turno che rappresenta un'unità di mondo e non di tavolo: in *The Quiet Year* ogni turno è una settimana che avvicina la distruzione di una comunità; in *Dialect* un gruppo di turni è un'era.

Dagli scacchi da scambio: dieci secondi a mossa, e un pedone tolto per ogni dieci secondi in più. È una regola che punisce con il materiale invece che con il tempo.

Da *Ultima III: Exodus*, 1983: il gioco era a turni, ma se chi giocava aspettava troppo il gioco emetteva da sé un comando di «passo», e i nemici si muovevano. Il turno resta, e chi non lo usa lo perde.

Da `initiative-rpg.txt`, il metodo di *Marvel Heroic Roleplaying*: chi ha appena agito sceglie chi agisce dopo, fra quelli che non hanno ancora agito, e l'ultimo del giro sceglie chi aprirà il giro seguente. L'ordine dei turni diventa una mossa del gioco.

Da `game-mechanics.txt`: *Civilization* alterna turni di giocatore e un giro di scambi collettivo, cioè usa i due tipi di turno nella stessa partita.

Dai giochi per corrispondenza, citati come uso ancora vivo del termine: partite di go e di scacchi che durano mesi, in cui il turno è l'unica unità di tempo che esista, perché il tempo reale non ha nessun ruolo.

## Una nostra versione

> **Sei turni, e un turno non è un minuto**
>
> Questo foglio divide un pomeriggio in sei turni. Un turno non dura un tempo: **finisce quando succede una certa cosa**, e la cosa la scegli tu, adesso, prima di cominciare.
>
> Deve essere una cosa che succede da sé: che non decidi tu, che non puoi affrettare, e che da dove sei si sente o si vede.
>
> ```
>  Un turno finisce quando ....................................
> ```
>
> In ogni turno fai **una cosa sola**, scelta fra queste quattro. Puoi ripetere.
>
> ```
>  A   guardare una cosa sola, per tutto il turno, senza fare altro
>  B   spostare un oggetto da dov'e a dove starebbe meglio
>  C   scrivere una riga su quello che e successo nel turno prima
>  D   chiedere una cosa a qualcuno che e in casa
> ```
>
> Segna la lettera appena il turno finisce, non prima.
>
> ```
>  turno    1    2    3    4    5    6
>  lettera  _    _    _    _    _    _
> ```
>
> Alla fine hai sei lettere in fila. **Riscrivile in ordine alfabetico e mettile sotto le prime.** Adesso ci sono due righe che dicono la stessa cosa in due modi.
>
> Due domande: che cosa sa la prima riga che la seconda non sa? E c'è una coppia di turni che, scambiati di posto, avrebbero cambiato il pomeriggio — oppure no?

La consegna che fa il lavoro è la prima: il turno finisce per un evento e non per un tempo, e l'evento lo nomina chi legge. Il sistema non misura il tempo e non sa che cosa ci sia in casa, e qui non gli serve nessuna delle due cose. Le quattro azioni sono poche apposta: con sei turni e quattro azioni le successioni possibili sono 4 096, e il 38% di esse usa tutte e quattro le lettere, quindi la varietà non è garantita e non viene chiesta. La riscrittura in ordine alfabetico è la manovra vera: mette accanto la successione e il suo conteggio, cioè le due cose fra cui c'è il fattore 48,76 calcolato sopra, e la domanda che segue non ha una risposta stampata da nessuna parte.

Dove si romperebbe: se i sei turni dovessero durare tutti uguali, il foglio non potrebbe farci niente, perché non ha un orologio. E se chi legge sceglie un evento che non succede mai, il pomeriggio si ferma al primo turno senza che nessuno se ne accorga — è la stessa cosa già osservata alla voce 113, indovinello per enumerazione e alla voce 144, enigma di pesatura, cioè una forma che fallisce in silenzio. Una riga di rimedio costa poco: «se dopo un po' non è ancora successo, cambia la cosa e scrivi qui quale hai messo».

## Da riprendere alla rassegna

**Il turno è il modo in cui il tempo entra in un formato che non ha un orologio.** Il criterio del capitolo diceva che un contatore che conta eventi sta dentro un foglio e uno che conta minuti no; il turno è l'operazione che trasforma il secondo nel primo, e si scrive con una riga. Alla rassegna vale la pena riguardare tutte le forme scartate per il tempo — la voce 260, serie di giorni (streak), la voce 261, obiettivo giornaliero, la voce 264, notifica per inattività, la voce 267, timer — e chiedersi se un turno definito da un evento le rimetterebbe in gioco.

**Chi definisce l'evento che chiude il turno decide il ritmo,** e nel nostro caso non può essere il sistema. È il terzo caso in cui l'ignoranza del sistema diventa la premessa invece dell'ostacolo, dopo la pianta della casa alla voce 95, mappa e il pezzo mancante alla voce 109, kit.

**Il turno toglie la velocità dalla partita,** e la fonte lo dice come argomento fra tifoserie. Se regge, è la trasformazione che rende praticabile in casa quasi tutto quello che il capitolo mette sotto cronometro; e va accostata alla misura già stabilita due volte — Yerkes-Dodson 1908 alla voce 88, sfida contro un tempo e Luchins 1942 alla voce 145, enigma di travaso — secondo cui il tempo peggiora i compiti nuovi.

**Un turno simultaneo fa esistere una seconda persona senza farla aspettare,** ed è la sesta via d'uscita per le forme a due, dopo l'insieme dato, la procedura che non richiede fiducia, il foglio indirizzato a qualcun altro in casa, il foglio di chi conduce e il gioco in solitario. Costa quello che dice `simultaneous-action-selection.txt`: un modo segreto ma vincolante di impegnarsi, che su carta è un foglio piegato.

**Il fatto che il turno non abbia una voce propria** — e stia dentro quella sull'orologio — è un indizio su come la letteratura guarda questa famiglia. Da tenere accanto all'osservazione già registrata alla chiusura del capitolo 8: le pratiche più diffuse non sono le più documentate.
