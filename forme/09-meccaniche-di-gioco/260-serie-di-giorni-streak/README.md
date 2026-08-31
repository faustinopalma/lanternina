# Serie di giorni (streak)

- **Numero** 260 nell'enciclopedia, capitolo 9 — Meccaniche di gioco
- **Si chiama anche** serie, catena, filotto, striscia, giorni di fila, non spezzare la catena, *streak*, *don't break the chain*
- **In una riga** giorni consecutivi contati, e il conto riparte se si salta.
- **Fonti** `duolingo.txt`, `compulsion-loop.txt`, `reinforcement.txt`, `gamification.txt`, `token-economy.txt`, lette il 31 agosto 2026. **Nessuna delle 812 pagine locali ha una voce dedicata a questa forma**: Duolingo è l'unica che ne descriva una. I conti sulla fragilità della catena sono nostri, verificati in `build/check_260.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Si conta da quanti giorni di fila una cosa è stata fatta. Il numero sale di uno al giorno. Se un giorno salta, il numero torna a zero.

Le parti sono tre, e la terza è quella che definisce la forma: **il conteggio**, **la condizione giornaliera**, e **l'azzeramento**. Senza azzeramento è un totale, e sta alla voce 256, punti. Senza condizione giornaliera è un conteggio qualsiasi. Con tutte e tre, quello che si accumula non è una quantità: è **una cosa che si può perdere tutta insieme**.

**Il confine con la voce 22, diario / registro è già scritto là, ed è la riga più utile che questa voce abbia:** una cosa che chiede di tornare ogni giorno assomiglia a una serie da non interrompere, e «la differenza non è nel diario, è in **chi conta i giorni**. Se li conta il sistema, è una streak. Se non li conta nessuno, è un quaderno.» **La forma non sta nell'oggetto sul tavolo: sta in che cosa fa qualcun altro mentre l'oggetto è sul tavolo.**

Parti mobili:

- **Che cosa conta come giorno fatto.** Una lezione qualsiasi, o un minimo. Duolingo sceglie la prima: qualunque lezione conta.
- **Se si può recuperare.** Un giorno saltato che si può ricomprare cambia la forma da vincolo a listino.
- **Che cosa succede al numero.** Torna a zero, oppure si conserva come record precedente.
- **Se qualcuno guarda.** Una serie privata e una serie visibile sono due cose diverse.
- **Se è condivisa.** Duolingo permette di tenere una serie insieme a un massimo di cinque persone, e allora il giorno saltato è saltato per tutti.
- **Il simbolo.** Duolingo usa il fuoco. È l'unico caso in cui una fonte locale dichiara il simbolo di una meccanica.

## Da dove viene

**Le fonti locali non contengono una storia di questa forma, e la cosa va detta.** Nessuna delle 812 pagine ha una voce dedicata alla serie di giorni; le informazioni che seguono stanno dentro pagine su altro. È il caso più netto di forma diffusa e non documentata incontrato finora in questo capitolo.

**Il fondo teorico c'è, ed è il condizionamento operante.** `reinforcement.txt` descrive un caso che assomiglia molto alla serie di giorni senza chiamarla così: il **rapporto fisso** (FR), in cui il rinforzo arriva dopo ogni ennesima risposta. Il suo effetto tipico è documentato: l'attività rallenta subito dopo il rinforzo e poi accelera fino al successivo — la **pausa dopo il rinforzo** — e la pagina precisa che quella pausa dipende da quanto è pesante il prossimo tratto da fare, non da quello appena finito. La stessa pagina definisce lo **sforzamento del rapporto** (*ratio strain*): se il numero di risposte richieste cresce troppo in fretta, il comportamento si disorganizza come nell'estinzione.

**La forma vera è però un altro schema, e sta in `compulsion-loop.txt`:** lo **schema di evitamento**, in cui chi gioca lavora per rimandare una conseguenza negativa. Una serie di giorni non promette niente per il giorno trentuno; **minaccia di cancellare i trenta precedenti.** La pagina lo elenca fra le due strategie che rafforzano un anello di compulsione, insieme al rapporto variabile della voce 262, ricompensa a intervalli variabili.

**L'esempio documentato è Duolingo, e la descrizione è breve.** `duolingo.txt`: qualunque lezione completata conta per la serie giornaliera; il simbolo visivo nell'app è il fuoco; la «serie fra amici» permette di mantenerla insieme a un massimo di cinque persone; e le serie «incoraggiano una pratica quotidiana costante e aiutano a costruire l'abitudine di imparare regolarmente». **Quest'ultima frase è un'affermazione della pagina, senza nota e senza misura.**

**C'è un evento che dice quanto la cosa attecchisca, ed è del 2025.** Quando l'amministratore delegato di Duolingo annunciò che l'azienda sarebbe diventata «AI-first», sostituendo lavoratori a contratto con l'automazione, molti utenti disdissero l'abbonamento e **interruppero la propria serie per protesta**. Una forma la cui rottura volontaria è un gesto politico è una forma che aveva un valore per chi la teneva.

## Varianti e parenti

- **Serie con recupero** — un giorno perso si può ricomprare, con una moneta di gioco o con un oggetto.
- **Serie condivisa** — due o più persone tengono la stessa catena, e chi salta la spezza per tutti.
- **Record della serie più lunga** — il numero azzerato resta come miglior risultato, e allora l'azzeramento non cancella tutto.
- **Non spezzare la catena** — la versione di carta: una croce sul calendario ogni giorno, e la catena di croci che si guarda.
- **Schema a rapporto fisso** — il parente di laboratorio: il premio dopo ogni ennesima risposta.
- **Schema di evitamento** — il parente esatto: si lavora per rimandare una perdita.
- **Voce 22, diario / registro** — la stessa carta, senza nessuno che conti i giorni.
- **Voce 242, ripasso distanziato (spaced repetition)** — l'altra forma dell'elenco costruita sul calendario, ma che chiede di **non** farlo tutti i giorni.
- **Voce 261, obiettivo giornaliero** — la quantità da fare entro sera, che spesso è la condizione della serie.
- **Voce 80, tempo** — perché una serie è, per costruzione, una domanda che si risolve aspettando.

## Che cosa se ne sa

**Non c'è nessuna misura dell'effetto delle serie di giorni nelle fonti locali.** L'unica affermazione è quella di `duolingo.txt` sull'abitudine, che non ha nota. **Va verificato.** Quello che c'è di misurato riguarda gli schemi di rinforzo in laboratorio, che sono la struttura e non la forma.

**Una catena è molto più fragile del conteggio che la accompagna, e la differenza si calcola.** Su trenta giorni, con nove giorni su dieci riusciti e ogni giorno indipendente dagli altri: i giorni fatti sono in media **27**, le interruzioni **3**, ma la probabilità che la catena non si spezzi mai è **4,24%** — e la catena più lunga dura in media **15,81 giorni** (`build/check_260.py`, per programmazione dinamica sugli stati e per la formula *p*ⁿ, concordi, con la programmazione dinamica controllata per enumerazione completa delle 4 096 successioni a dodici giorni). **Il conteggio dice ventisette e la catena dice sedici: sono due misure della stessa persona, e differiscono di un fattore 1,71.**

**Il crollo è ripido.** Su trenta giorni la catena resta intatta nel 4,24% dei casi con nove giorni su dieci, nello 0,12% con otto su dieci, nello 0,0023% con sette su dieci. **La probabilità di arrivare in fondo scende sotto la metà già al settimo giorno** con nove giorni su dieci, e al quarto con otto su dieci. Una serie lunga, quindi, non è una misura di costanza: è una misura di costanza **e** di fortuna, e la seconda pesa più della prima man mano che i giorni passano.

**Questi conti valgono se i giorni sono indipendenti, e non lo sono.** Chi ha fatto ventinove giorni di fila ha più probabilità di fare il trentesimo di chi non ne ha fatto nessuno, e non solo perché è un tipo costante: **è la serie stessa a cambiare la probabilità**, che è esattamente il motivo per cui la forma esiste. L'ipotesi di indipendenza è comoda e falsa, e i numeri qui sopra vanno letti come il caso in cui la serie non stia facendo il suo lavoro.

**Sulla struttura, invece, c'è materiale solido e riguarda che cosa succede quando si smette di dare il premio.** `reinforcement.txt`: gli schemi parziali resistono all'estinzione più di quello continuo, gli schemi a rapporto più di quelli a intervallo, e quelli variabili più di quelli fissi. Una serie di giorni è uno schema a rapporto fisso, cioè **il più prevedibile e il meno resistente** della famiglia. Quello che la tiene in piedi non è il rinforzo: è la perdita minacciata.

## Esempi trovati

La serie giornaliera di Duolingo, con il fuoco come simbolo, contata da qualunque lezione completata.

La «serie fra amici» dello stesso servizio, tenuta insieme a un massimo di cinque persone.

Le interruzioni di serie del 2025 come forma di protesta, dopo l'annuncio sull'automazione.

Lo schema a rapporto fisso in laboratorio, con la pausa dopo il rinforzo e lo sforzamento del rapporto quando il tratto da fare cresce troppo in fretta.

Lo schema di evitamento nel disegno dei giochi, in cui non si lavora per ottenere ma per rimandare una perdita.

## Una nostra versione

> **Le sette caselle, e quello che c'e dentro**
>
> Ecco una catena da sette giorni, disegnata come si disegnano di solito.
>
> ```
>   [ x ] [ x ] [ x ] [ x ] [   ] [ x ] [ x ]     catena: 0
> ```
>
> **Sei giorni su sette, e la catena dice zero.** E adesso la stessa settimana contata in un altro modo:
>
> ```
>   [ x ] [ x ] [ x ] [ x ] [   ] [ x ] [ x ]     giorni: 6
>                                                 la piu lunga: 4
>                                                 ripartenze: 1
> ```
>
> Tre numeri per la stessa settimana, e nessuno dei tre e sbagliato. **Scegline uno e scrivi qui perche.**
>
> ```
>   Il numero che guardo e: ─────────    perche: ────────────────────────
> ```
>
> Poi la parte che il calendario non chiede mai: **che cosa e successo il quinto giorno?**
>
> ```
>   ──────────────────────────────────────────────────────────
> ```

La settimana è stampata già compilata, quindi non c'è nessun impegno da prendere e nessuna catena da tenere. Il lavoro è accorgersi che tre modi di contare la stessa settimana danno zero, sei e quattro. L'ultima domanda è quella che nessun sistema a serie pone, perché per un sistema a serie il giorno saltato non ha contenuto.

**Dove si rompe.** Questa forma è, in tutte le sue versioni vere, definita da una successione di giorni, e **il sistema non misura il tempo**: non sa quando è oggi, non sa quando è stato ieri, e non può accorgersi di un giorno mancato. È il limite dominante della voce e non c'è modo di aggirarlo. Quello che resta praticabile è una settimana **già finita e stampata**, cioè la serie guardata da fuori invece che tenuta da dentro — che è un oggetto diverso, e lo si dichiara.

## Da riprendere alla rassegna

**Chi conta i giorni è la variabile, e la si può mettere a zero.** La riga della voce 22, diario / registro vale per tutto questo capitolo: la stessa carta, con o senza qualcuno che tenga il conto, è una forma o un'altra. **Da guardare alla rassegna come una domanda da porre a ogni meccanica: che cosa resta se nessuno tiene il conto?**

**Il conteggio e la catena sono due misure diverse della stessa persona, e differiscono molto.** Ventisette giorni fatti e sedici giorni di catena più lunga. **Chi sceglie quale dei due mostrare sta scegliendo che cosa premiare**, e la scelta non è visibile a chi legge il numero. Va accostata alle quattro convenzioni di pari merito della voce 259, classifica: in tutti e due i casi un numero apparentemente oggettivo dipende da una decisione presa altrove.

**La serie è l'unica forma raccolta finora che minacci invece di promettere.** Lo schema di evitamento è nominato dalla fonte come una delle due leve che rafforzano un anello di compulsione. È una descrizione, non un verdetto, e la annoto qui perché è la prima volta in duecentosessanta voci che una forma funzioni togliendo.

**Chiedere che cosa è successo nel giorno saltato.** In tutte le fonti il giorno mancato è solo l'evento che azzera; nessuna gli attribuisce contenuto. **È lo stesso movimento già raccolto come «chiedere quello che si è scartato» — voci 017 e 049 —, applicato a una assenza invece che a una scelta**, e sta vicino alla voce 63, inferire da un'assenza.

**Una catena lunga misura costanza e fortuna insieme, e non dice in che proporzione.** Sotto la metà già al settimo giorno con nove giorni su dieci fatti. Chi confronta due catene sta confrontando due numeri che contengono cose diverse: **da tenere presente ovunque il progetto usi una successione come misura.**
