# Sblocco progressivo dello spazio

- **Numero** 186 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Meccanismi da escape room»
- **Si chiama anche** apertura progressiva, porta che si apre, area sbloccata, avanzamento a chiave, *gating*, *unlockable*, stanza dentro la stanza
- **In una riga** una porta che si apre e mostra altro.
- **Fonti** `escape-room.txt`, `it-escape-room.txt`, `metroidvania.txt`, `nonlinear-gameplay.txt`, `alternate-reality-game.txt`, lette il 31 agosto 2026. La griglia e il messaggio dell'esempio sono nostri, verificati in `build/check_186.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Lo spazio disponibile cresce. All'inizio si vede una parte; risolto qualcosa, se ne apre un'altra, e quello che c'era prima resta. Non è una fila di compiti: è **una fila di ambienti**, e ogni ambiente contiene più compiti di quanti ne servano ad aprire il successivo.

Parti mobili:

- **Che cosa apre.** Una chiave, un numero, un oggetto, oppure — ed è il caso più interessante — soltanto aver capito qualcosa.
- **Se quello che c'era resta.** Se resta, chi ha sbagliato può tornarci; se sparisce, ogni stanza è un compito a sé.
- **Quanto è grande il pezzo che si apre.** Una porta e una stanza sono due cose diverse: la prima aggiunge un oggetto, la seconda cambia dove si sta.
- **Se si vede quello che è chiuso.** Una porta visibile e chiusa dice che c'è dell'altro; una parete no. La differenza è tutta sull'attesa.
- **Se aprire consuma.** Una busta aperta non si richiude.

**La proprietà che la definisce è che il materiale disponibile cambia mentre si lavora.** Ogni altra forma di questo capitolo consegna tutto e basta, o consegna un pezzo per volta e ritira il precedente. Questa accumula, ed è l'unica in cui **quello che si ha in mano alla fine è più di quello che si aveva all'inizio.**

È la stessa catena della voce 181, percorso lineare fatta di porte invece che di fogli, e la differenza non è cosmetica: in una catena di fogli il passo precedente si esaurisce, in una catena di stanze la stanza precedente resta aperta e continua a servire.

## Da dove viene

**Dalle escape room, dove è la definizione stessa del funzionamento.** `escape-room.txt` scrive che gli enigmi «sbloccano l'accesso a nuovi oggetti o a nuove aree quando vengono risolti», e nota che, malgrado il nome, il gioco non è necessariamente confinato in una stanza sola. La fonte italiana aggiunge il modo in cui la cosa è scandita: le stanze hanno «stadi multipli che devono essere risolti per far avanzare la trama», e la stessa pagina descrive le prime sessioni giapponesi di Takao Kato dove la ricompensa di un enigma era **un gettone da mettere in una macchinetta, che dava un foglietto con un altro indizio** (`it-escape-room.txt`).

Le due pagine divergono su una data e la cosa va detta: l'inglese colloca la nascita del Real Escape Game nel **2007**, l'italiana nel **2008**. Nessuna delle due porta una fonte primaria per quella cifra. Non si usa nessuna delle due per un'affermazione, e il fatto che valga è che il genere nasce fra 2007 e 2008 in Giappone.

**Nei videogiochi ha un nome e una storia, ed è un genere intero.** `metroidvania.txt` descrive una mappa di mondo interconnessa «di cui alcune parti restano inaccessibili finché non si acquisiscono oggetti, strumenti, armi, capacità o conoscenza», e ricostruisce l'intenzione originale: creare un'avventura non lineare «che richiedesse al giocatore di ripercorrere i propri passi, fornendo potenziamenti permanenti invece che temporanei come facevano gli altri giochi dell'epoca». **Il potenziamento permanente è la parte che conta**: è quello che rende una stanza aperta una cosa che resta aperta.

La stessa pagina registra due dettagli di mestiere che valgono per chiunque costruisca una cosa così. Il primo: quello che sblocca è spesso **protetto da un avversario finale**, cioè aprire costa. Il secondo, da uno dei produttori di *Ori and the Will of the Wisps*: «tutto è così interconnesso che se cambi un aspetto del gioco è inevitabile che influenzi tutto il resto». **Una struttura ad accumulo va provata per intero ogni volta che se ne cambia un pezzo**, che è un costo che una fila di fogli indipendenti non ha.

**E c'è la variante che toglie la porta.** Il termine **metroidbrainia**, coniato nel settembre 2015, indica i giochi in cui l'avanzamento è vincolato **solo dalla conoscenza di chi gioca**: tutto è aperto fin dal primo momento, e le aree importanti sono chiuse «semplicemente perché chi gioca non sa come raggiungerle o usarle». La fonte cita *Outer Wilds* (2019), *Fez* (2012), *Return of the Obra Dinn* (2018), *Tunic* (2022). **Per un sistema che stampa fogli è l'unica delle due versioni realizzabile**, e la ragione sta nella sezione seguente.

Il confine con il capitolo 6 è netto: **là si descriverà l'itinerario, cioè come una serie di luoghi si tiene insieme in un percorso e in una storia — la voce 193, caccia al tesoro e la voce 204, ARG (alternate reality game); qui c'è la forma di pagina e che cosa chiede a chi la riceve.**

## Varianti e parenti

- **Sblocco a chiave** — serve un oggetto, e l'oggetto è protetto.
- **Sblocco a codice** — serve un numero, e il numero viene da un enigma.
- **Sblocco per conoscenza** — non serve niente: serve aver capito. È il metroidbrainia.
- **Sblocco a busta** — la porta è una busta chiusa, e aprirla la consuma.
- **Ritorno sui propri passi** — quello che si è aperto resta, e serve dopo.
- **Voce 181, percorso lineare** — la stessa catena fatta di fogli invece che di porte, e senza accumulo.
- **Voce 183, percorso aperto** — il contrario esatto: tutto disponibile subito.
- **Voce 170, serratura a combinazione** — il giunto che fa da porta.
- **Voce 179, chiave nascosta** — quello che si trova dietro una porta, molto spesso.
- **Voce 188, oggetto che cambia significato** — la stessa idea ridotta a un oggetto solo.
- **Voce 166, labirinto fisico** — l'altra forma dell'elenco in cui lo spazio della casa è il materiale.

## Che cosa se ne sa

**Il sistema non può chiudere una porta, e questo è il fatto principale della voce.** Un foglio A4 mostra tutto quello che ha nel momento in cui lo si guarda; una busta si apre; un foglio piegato si spiega. Le tre cose che assomigliano a una serratura sono tutte imperfette, e conviene averle scritte per quello che sono.

- **La busta chiusa.** Funziona, non costa niente, e richiede che qualcuno l'abbia chiusa. È una porta vera al prezzo di una seconda persona, che è la risorsa più scarsa del progetto.
- **La dipendenza di dati.** Il testo si può leggere avanti e non serve a niente, perché ogni passo opera sul risultato del precedente. È la soluzione trovata alla voce 181, percorso lineare, e su un foglio è l'unica che regga da sola. Ma **non apre uno spazio: nasconde un valore.**
- **La conoscenza.** Tutto è stampato e visibile, e quello che è chiuso è chiuso perché non si è ancora capito che cos'è. **È la sola delle tre che apra davvero uno spazio senza richiedere né una serratura né una persona**, e ha un nome documentato dal 2015.

**Ne segue una conclusione secca: per un foglio stampato, l'unico sblocco progressivo praticabile è il metroidbrainia.** Non per eleganza, per aritmetica delle risorse disponibili.

**Quello che si apre deve restare aperto, e la fonte lo dice come scelta di progetto.** I potenziamenti permanenti invece che temporanei sono citati come l'idea che ha fatto il genere. Su un foglio è gratis — la carta non si richiude — e vale la pena notare che **il supporto del progetto ha per default la proprietà che quel genere ha dovuto inventarsi.**

**Costruire una struttura ad accumulo costa più che costruirne una lineare, ed è dichiarato.** Cambiare un pezzo obbliga a riprovare tutto il resto, perché tutto è collegato. Con il costo delle storie ramificate registrato alla voce 191, finale buono e finale cattivo fanno due casi in cui la fonte dichiara che una struttura più ricca costa in modo più che proporzionale.

**Non c'è nessun dato su quante stanze convenga fare.** Né le pagine sulle escape room né quelle sui videogiochi contano gli ambienti, e l'unico numero disponibile resta la durata di una stanza — dai 45 ai 60 minuti, fino a due ore per le più lunghe.

**Il segnale d'errore, in una struttura a porte, è aggregato per stanza e locale nel complesso.** Chi sbaglia dentro una stanza non apre la porta e lo sa subito, ma non sa quale delle cose della stanza abbia sbagliato. **È una via di mezzo fra i due estremi misurati alle voci 181 e 182**, e la prima incontrata: il segnale dice dove sei fermo e non dice su che cosa.

## Esempi trovati

Il gettone dato in premio per un enigma, da mettere in una macchinetta che restituisce un foglietto con l'indizio successivo, alle prime sessioni giapponesi.

La stanza che si scopre non essere una stanza sola, e la parete che era una porta.

Il potenziamento permanente che apre un passaggio che si era visto e lasciato indietro un'ora prima.

Il *metroidbrainia*, in cui la mappa è aperta dall'inizio e a chiudere è soltanto quello che chi gioca non ha ancora capito.

Le escape room in scatola, in cui le porte sono buste sigillate e aprirle le consuma: ogni avventura è giocabile una volta sola.

## Una nostra versione

> **Tre parti, e la seconda non si legge**
>
> **PARTE UNO.** Trentasei parole.
>
> ```
>      1         2         3         4         5         6
>   1  LAMPADA   GUARDA    FINESTRA  PORTA     LIBRO     CHIAVE
>   2  SEDIA     SPECCHIO  SOTTO     SCALA     VASO      CESTO
>   3  TAPPETO   QUADRO    TENDA     IL        PENNA     SCATOLA
>   4  TAVOLO    CUSCINO   ARMADIO   BOTTIGLIA FOGLIO    PIATTO
>   5  DELLA     OROLOGIO  SPAZZOLA  CORDA     NASTRO    BICCHIERE
>   6  FORCHETTA CUCCHIAIO CUCINA    COLTELLO  TAZZA     PENTOLA
> ```
>
> **PARTE DUE.** Sei coppie di numeri. Le prime tre sono già fatte.
>
> ```
>   1-2  →  GUARDA
>   2-3  →  SOTTO
>   3-4  →  IL
>   4-1  →  ────────
>   5-1  →  ────────
>   6-3  →  ────────
> ```
>
> Rileggi le sei parole di seguito. **È una cosa da fare, e si fa alzandosi.**
>
> **PARTE TRE.** Puoi leggerla adesso. Non ti serve.
>
> ```
>   Disegna quello che hai visto, e che nessuno guarda mai.
>
>   ┌──────────────────────────────────────────────────────────┐
>   │                                                          │
>   │                                                          │
>   │                                                          │
>   │                                                          │
>   │                                                          │
>   └──────────────────────────────────────────────────────────┘
> ```
>
> **Due domande in fondo, e sono sul foglio e non sulla casa.**
>
> ```
>   Hai letto la parte tre prima di aver fatto la parte due?
>   □ sì   □ no
>
>   Se sì: ti è servito a qualcosa?   □ sì   □ no
> ```
>
> Se hai risposto sì e poi no, hai appena visto come funziona una porta fatta di carta. **Non c'è nessuna serratura: c'è solo che, senza aver fatto la parte due, la parte tre non vuol dire niente.**

La griglia è verificata in `build/check_186.py`: trentasei parole tutte diverse, nessuna ripetuta, la più lunga di nove caratteri dentro colonne da dieci, e le sei coppie che danno esattamente **GUARDA SOTTO IL TAVOLO DELLA CUCINA**. Ogni parola del messaggio compare una volta sola nella griglia, quindi non ci sono letture alternative.

Le prime tre coppie sono risolte, e non per gentilezza: **sono la consegna.** Nessuna riga spiega che il primo numero è la riga e il secondo la colonna, perché tre esempi lo dicono meglio di una regola — è la mossa già registrata alla voce 341, crittografia pura, e qui serve a rendere la porta apribile senza istruzioni.

La porta di questo foglio è la parte tre, ed è stampata in chiaro fin dall'inizio. **Chi legge avanti trova una consegna che non può eseguire**, perché non ha ancora guardato sotto niente. È l'unico tipo di serratura che un foglio possieda davvero, e le due caselle in fondo servono a farla vedere invece che a dichiararla.

Il messaggio manda in un posto che esiste in ogni casa e sotto cui non guarda nessuno. **Lo spazio che si apre è la casa**, e il foglio non ha dovuto nasconderci niente: bastava mandarci.

Dove si romperebbe: **si rompe se in casa non c'è un tavolo da cucina**, e questo è un difetto vero e riparabile — la consegna può nominare una funzione invece di un oggetto, come già fatto in tutto il blocco precedente. Per il resto sta su un foglio, si fa da soli, e la fotografia del disegno è il ritorno. Sul pannello da quattro righe funzionerebbe meglio che su carta, perché le tre parti arriverebbero davvero una per volta e la porta sarebbe una porta: **è la sola voce del blocco in cui il pannello batte il foglio.**

## Da riprendere alla rassegna

**Il sistema non può chiudere una porta, e le tre alternative hanno tre prezzi diversi.** La busta costa una seconda persona; la dipendenza di dati non apre uno spazio, nasconde un valore; la conoscenza non costa niente ed è l'unica che apra davvero. **Per un foglio stampato, l'unico sblocco progressivo praticabile è quello per conoscenza**, e questa è una conclusione tecnica e non una preferenza.

**Il supporto del progetto ha per default la proprietà che un intero genere ha dovuto inventarsi.** I potenziamenti permanenti — quello che si apre resta aperto — sono citati come l'idea fondativa del genere metroidvania. Su carta è gratis, perché un foglio non si richiude. **Vale la pena censire quali altre proprietà costose altrove siano gratuite qui**, perché sono quelle su cui conviene costruire.

**Un segnale d'errore per stanza sta fra i due estremi già misurati.** Chi non apre la porta sa di essere fermo e non sa su che cosa. **È il terzo tipo di controllo incontrato**, dopo quello locale e immediato della voce 181, percorso lineare e quello aggregato e finale della voce 182, percorso a imbuto, e il primo che dia una delle due informazioni e non l'altra.

**Una struttura ad accumulo va riprovata per intero a ogni modifica, e la fonte lo dichiara.** Con il costo delle storie ramificate fanno due casi in cui una struttura più ricca costa in modo più che proporzionale. **Per un sistema che comporrà attività a partire da pezzi è un avvertimento sul limite di quella composizione.**

**Il metroidbrainia è la stessa candidatura a voce nuova già segnalata alla voce 183, percorso aperto**, e vista da qui si capisce perché non stia né qui né là: è un percorso aperto in cui però qualcosa si apre, e uno sblocco progressivo in cui però non si apre niente. **Sta esattamente sul confine fra due voci dell'elenco**, e i confini sono il posto in cui l'elenco è più probabilmente incompleto.
