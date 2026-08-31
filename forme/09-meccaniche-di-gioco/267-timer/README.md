# Timer

- **Numero** 267 nell'enciclopedia, capitolo 9 — Meccaniche di gioco
- **Si chiama anche** cronometro, orologio di gioco, orologio da scacchi, contaminuti, contasecondi, tempo di riflessione, controllo del tempo, *game clock*, *chess clock*, *time control*, *stopwatch*
- **In una riga** un orologio che misura quanto ci si mette.
- **Fonti** `chess-clock.txt`, `time-control.txt`, `sudden-death-sport.txt`, `timer.txt`, `time-limit-gaming.txt`, `speedrun.txt`, lette il 31 agosto 2026. `countdown.txt`, `hourglass.txt` e `it-clessidra.txt` erano già state lette per la voce 189, conto alla rovescia e non sono rilette qui. I conti sulle quattro regole di orologio sono nostri, verificati in `build/check_267.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Uno strumento che misura quanto dura una cosa, e mostra il numero a chi la sta facendo.

**Tre voci vicine sono già scritte, e i confini fra le quattro sono netti.** La voce 88, sfida contro un tempo dà **un limite dichiarato** e non lo mostra: si sa che sono venti minuti e non si vede quanti ne restano. La voce 189, conto alla rovescia mostra **il limite mentre si consuma**, e la differenza fra le due è tutta lì. La voce 190, classifica dei tempi mette **le misure in fila** e le confronta fra persone. **Questa voce è lo strumento che produce la misura**, ed è l'unica delle quattro in cui non c'è per forza un limite: un cronometro che conta in avanti non impedisce niente, dice soltanto quanto ci hai messo.

**E ha un abitante che le altre tre non hanno: l'orologio doppio.** Un orologio da scacchi è fatto di due orologi affiancati con dei pulsanti che ne fermano uno e ne fanno partire l'altro, **così che i due non corrano mai insieme** (`chess-clock.txt`). Non misura la durata di una partita: misura **quanto tempo ha preso ciascuno dei due**, e mettere in moto il proprio avversario è una mossa.

Parti mobili:

- **Se conta avanti o indietro.** Avanti misura, indietro minaccia.
- **Se il tempo è di uno o diviso fra due.** È la differenza fra un cronometro e un orologio da scacchi.
- **Che cosa succede quando finisce.** Si perde, si paga una penalità in punti, oppure si entra in un tempo supplementare.
- **Se se ne guadagna.** Dopo ogni mossa si può aggiungere un tanto fisso, oppure non contare i primi secondi.
- **Se il tempo non usato si accumula.** È la differenza più grossa fra due regole che sembrano uguali.
- **Chi lo ferma.** Nel doppio lo ferma chi ha appena giocato, ed è il gesto che chiude la propria mossa.

## Da dove viene

**Da un torneo di scacchi, e da una persona con nome e cognome.** `chess-clock.txt`: l'orologio da scacchi è stato inventato da **Thomas Bright Wilson**, del circolo scacchistico di Manchester, e usato per la prima volta in competizione al **torneo di Londra del 1883**. Da lì si è diffuso allo Scrabble da torneo, allo shogi, al Go, alla dama e a quasi ogni gioco da tavolo per due, e — la pagina lo registra — **anche a certi contesti giudiziari, dove a ogni parte è assegnata una quantità di tempo per le sue argomentazioni.**

**La versione analogica ha un dettaglio che ne spiega il nome comune: la bandierina.** Un orologio meccanico ha una bandierina che cade a indicare l'istante esatto in cui il tempo di quel giocatore è finito. I difetti dichiarati sono tre: la precisione, la corrispondenza fra i due orologi, e la corrispondenza fra le due bandierine. E soprattutto: **con un orologio meccanico non si può aggiungere tempo facilmente**, quindi i controlli del tempo più elaborati sono nati con l'elettronica.

**Il primo orologio digitale è del 1973, ed era un esercizio universitario.** Bruce Cheney, studente di ingegneria elettronica alla Cornell e giocatore di scacchi, lo costruì per un corso. Il visore a LED rossi consumava tanto da dover essere attaccato alla presa, e i LED costavano abbastanza che **si potevano mostrare le cifre di un giocatore solo, quello di turno**. Aveva una modalità sola: il tempo scorreva in avanti. Il primo orologio digitale in commercio fu brevettato nel **1975** da Joseph Meshi e Jeffrey R. Ponsor, con il nome Micromate-80; **ne fu costruito uno solo.**

**La regola più diffusa oggi porta il nome di un campione del mondo, ed è del 1988.** Bobby Fischer depositò in quell'anno il brevetto statunitense 4 884 255, concesso nel 1989: **un tempo fisso all'inizio, e un piccolo tanto aggiunto dopo ogni mossa.** L'incremento fu usato per la prima volta nella partita Fischer-Spassky del **1992** e adottato dal campionato del mondo FIDE nel **1998**. La pagina segnala anche la parte del brevetto che nessuno ha adottato: **una voce sintetica che annunciasse quanto tempo restava**, così da non dover guardare l'orologio. E registra una rivendicazione: Meshi chiamava la stessa cosa «accumulazione», ed era una caratteristica del suo Micromate-180, brevetto del 1978.

**La regola concorrente è del 1994 e fa una cosa diversa che sembra la stessa.** Camaratta e Goichberg depositarono il brevetto per un temporizzatore con **ritardo**: fra il momento in cui si preme il pulsante e il momento in cui l'orologio comincia a scendere passa un tempo che si può impostare. Brevetto 5 420 830, concesso il 10 maggio 1995 e ceduto alla Federazione scacchistica americana. **Lo scopo dichiarato è lo stesso dell'incremento**: ridurre la probabilità che chi sta vincendo perda solo perché è finito il tempo.

## Varianti e parenti

- **Cronometro** — conta in avanti e non finisce. È la forma pura di questa voce.
- **Orologio doppio** — due tempi, uno solo dei quali corre.
- **Morte improvvisa** — un tempo fisso per tutta la partita, e chi lo finisce perde. `time-control.txt` la chiama la metodologia più semplice.
- **Tempo supplementare** — finito il tempo principale se ne apre un altro con regole diverse.
- **Penalità invece di sconfitta** — nello Scrabble da torneo: 25 minuti a testa e **dieci punti di penalità per ogni minuto o frazione in eccesso**, e chi sfora di dieci minuti perde comunque.
- **Incremento** — un tanto aggiunto dopo ogni mossa, che si accumula se non lo si usa.
- **Ritardo** — i primi secondi di ogni mossa non contano, e non si accumulano.
- **Byo-yomi** — finito il tempo principale, ogni mossa ha il suo tempo. Nella variante giapponese si hanno più periodi, e sprecarne uno non intacca gli altri.
- **Byo-yomi canadese** — un blocco di mosse in un blocco di tempo, che impone una velocità media invece che una velocità per mossa.
- **Modalità clessidra** — il tempo tolto a uno viene dato all'altro. `time-control.txt` la dichiara di uso raro.
- **Voce 88, sfida contro un tempo** — il limite dichiarato e non mostrato.
- **Voce 189, conto alla rovescia** — il limite mostrato mentre si consuma, e la clessidra fisica.
- **Voce 190, classifica dei tempi** — le misure messe in fila fra persone.
- **Voce 80, tempo** — il tempo come supporto invece che come misura.
- **Voce 54, misurare** — perché un cronometro è uno strumento di misura come un metro, con la stessa domanda sulla precisione dichiarata.

## Che cosa se ne sa

**Le fonti locali non contengono nessuno studio su che cosa faccia un orologio a chi lavora.** `chess-clock.txt` e `time-control.txt` sono descrizioni tecniche e storiche, con note a brevetti, regolamenti e federazioni: sono fonti solide su che cosa esista e su quando, e mute su che cosa produca. **La misura che riguarda la tensione sotto un tempo è già stata raccolta alla voce 190, classifica dei tempi — la legge di Yerkes-Dodson — e non si ripete qui.** `time-limit-gaming.txt` è di 3 kB e definisce la scadenza; non aggiunge niente a quello che è già alla voce 88, sfida contro un tempo.

**Quello che le fonti danno, e che è insolito, è una tassonomia con i confini definiti da numeri di regolamento.** `time-control.txt`: la FIDE classifica sommando il tempo assegnato a ciascuno e l'incremento per mossa moltiplicato per sessanta. Almeno **60 minuti** (120 a livello di maestro) è *classica*; **fra 10 e 60** è *rapida*; **10 o meno** è *lampo*. La stessa pagina dichiara subito che gli standard divergono: Lichess e Chess.com considerano rapide le partite da dieci minuti, e hanno una categoria *bullet* sotto i tre minuti, con *hyperbullet* sotto i trenta secondi e *ultrabullet* sotto i quindici. **Nel Go «qualunque cosa sotto i venti minuti» è considerata lampo.** È lo stesso fenomeno registrato alla voce 259, classifica per le convenzioni di pari merito: un numero apparentemente oggettivo poggia su una convenzione presa altrove.

**Le regole di orologio si possono confrontare esattamente, e sulla stessa partita danno risultati che non si somigliano.** Venti mosse, tempi di riflessione dati, orologio da 300 secondi con dodici secondi di bonus:

```
  la regola                resta
  morte improvvisa        -154 s
  incremento Fischer        86 s
  ritardo semplice         -28 s
  ritardo Bronstein        -28 s
```

(`build/check_267.py`: ogni regola simulata mossa per mossa **e** calcolata in forma chiusa dalla definizione, concordi su tutte e quattro.) **La stessa identica partita finisce con centocinquantaquattro secondi di ritardo o con ottantasei di avanzo, e la differenza non è nel gioco: è nella regola dell'orologio.**

**I due ritardi danno lo stesso residuo, e questo conferma quello che dice la fonte.** `time-control.txt` riporta che il ritardo Bronstein e il ritardo semplice «sono molto simili, ma non uguali»: differiscono in quello che si legge sull'orologio **durante** la mossa, e la fonte citata precisa che «alla fine della mossa, dopo aver premuto, il tempo di riserva rimanente sarà identico». I nostri conti danno −28 secondi in tutti e due i casi. **La differenza fra le due regole è solo in che cosa si vede mentre si pensa, e questo è precisamente il confine con la voce 189, conto alla rovescia.**

**L'incremento supera il ritardo di esattamente i secondi che non si sono usati.** Nella partita d'esempio la differenza è di **114 secondi**, ed è la somma, su tutte le mosse, di quanto ognuna è stata più corta dei dodici secondi di bonus. `time-control.txt` lo dice della variante giapponese del byo-yomi con la formula opposta: «il tempo non usato durante un periodo non si riporta sulle mosse successive». **Chi gioca in fretta accumula con l'incremento e non accumula con il ritardo, e la differenza cresce con quante mosse rapide fa.**

**E la regola può cambiare chi sta peggio, a parità di come si è giocato.** Due giocatori, dieci mosse a testa: A pensa quasi sempre un paio di secondi e una volta sola centocinquanta; B pensa diciassette secondi ogni volta.

```
  la regola               resta ad A   resta a B   sta peggio
  morte improvvisa             138 s       129 s            B
  incremento Fischer           258 s       249 s            B
  ritardo semplice             162 s       249 s            A
```

**A ha pensato in tutto meno di B — 162 secondi contro 171 — e con il ritardo semplice è quello che sta peggio.** La ragione è che il ritardo condona i primi secondi di ogni mossa, e B ha usato quel condono dieci volte mentre A l'ha sprecato nove volte su dieci. **Una regola pensata per essere più clemente premia una forma di gioco e ne punisce un'altra, e non lo dichiara.**

**Il conto su quante strade restano dice quanto una regola sia più larga di un'altra.** Cinque mosse, tempi interi da uno a ventiquattro secondi, orologio da cinquanta secondi: **1 789 860 distribuzioni su 7 962 624 passano con la morte improvvisa** (il 22,48%), e **6 822 456 passano con un ritardo di sei secondi per mossa** (l'85,68%). Nessuna distribuzione passa la morte improvvisa e non il ritardo, come dev'essere. **Sei secondi condonati per mossa moltiplicano per 3,81 i modi di stare dentro il tempo**, ed è il modo di misurare la clemenza di una regola già usato alla voce 261, obiettivo giornaliero.

**La modalità clessidra ha una proprietà che si dimostra e nessuna fonte enuncia.** In quella regola il tempo che uno consuma viene aggiunto all'altro, quindi **la somma dei due orologi non cambia mai**: verificato su una partita di dieci mosse, una sola somma per tutta la durata. Ne segue quello che `time-control.txt` dice a parole — «non c'è nessun tempo massimo assegnato a una partita con questo metodo» — e una cosa in più: **non si perde per essere lenti, si perde per essere più lenti dell'altro di quanto valeva l'assegnazione iniziale.** È un orologio che misura una differenza e non una durata.

## Esempi trovati

Il torneo di Londra del 1883, dove l'orologio doppio di Thomas Bright Wilson viene usato per la prima volta in competizione.

L'orologio digitale di Bruce Cheney, 1973, che poteva mostrare le cifre di un giocatore solo perché i LED costavano troppo, e che andava attaccato alla presa.

Il Micromate-80 del 1975, primo orologio digitale in commercio, di cui fu costruito un solo esemplare.

Il brevetto di Fischer del 1988, e la parte che nessuno ha adottato: la voce che annuncia il tempo restante per non dover guardare l'orologio.

Lo Scrabble da torneo, dove sforare non fa perdere ma costa dieci punti al minuto, e solo dopo dieci minuti fa perdere.

Il byo-yomi giapponese a cinque periodi di un minuto, che secondo `time-control.txt` equivale a «un minuto per mossa più quattro pacchetti da un minuto da usare come servono»: quattro mosse da due minuti, o una mossa da cinque, o qualunque altra combinazione.

I tribunali in cui a ogni parte è assegnata una quantità di tempo: l'orologio da scacchi fuori dal gioco.

## Una nostra versione

**Il limite dominante è il più duro dell'elenco: il sistema non misura il tempo.** Non c'è orologio, non c'è cronometro, non c'è modo di sapere quando un foglio è stato preso in mano. Per il criterio del capitolo — un contatore di eventi sta su un foglio, un contatore di minuti no — questa è la voce che sta più fuori di tutte, insieme alla voce 264, notifica per inattività. La versione migliore che se ne può fare **prende il tempo come dato invece che come misura**: i secondi sono stampati, e il lavoro è sulle regole.

> **La partita che finisce in due modi**
>
> Due persone giocano dieci mosse a testa. Ecco quanti secondi ha pensato ognuna, mossa per mossa. Non c'e' niente da cronometrare: i numeri sono gia' qui.
>
> ```
>   A     2    1    1    2    1  150    1    2    1    1
>   B    18   17   16   18   17   16   18   17   16   18
> ```
>
> Tutti e due partono con **300 secondi**. Adesso applica tre regole vere, che si usano davvero nei tornei.
>
> ```
>   1. Morte improvvisa    il tempo scende e basta.
>
>   2. Incremento          dopo ogni mossa si aggiungono 12 secondi,
>                          li abbia usati o no.
>
>   3. Ritardo             i primi 6 secondi di ogni mossa non contano.
>                          Se pensi meno di 6 secondi, non spendi niente.
> ```
>
> ```
>                       resta ad A        resta a B
>   Morte improvvisa    ──────────        ──────────
>   Incremento          ──────────        ──────────
>   Ritardo             ──────────        ──────────
> ```
>
> **A ha pensato meno di B: 162 secondi contro 171. Contali e verifica.**
>
> E poi la domanda vera: **con quale delle tre regole A sta peggio di B, pur avendo pensato di meno?** Quando l'hai trovata, di' perche', in una riga.
>
> Ultima, e non ha una risposta giusta: **se dovessi scegliere tu la regola prima di sapere come giochi, quale prenderesti?**

Le tre regole sono date per esteso e non c'è niente da indovinare: il lavoro è applicarle e accorgersi che la terza rovescia il verdetto delle prime due. La ragione è che il ritardo condona i primi secondi di ogni mossa e A ne ha sprecato il condono nove volte su dieci. L'ultima domanda è la stessa che si pongono le federazioni, e in quarant'anni non hanno dato la stessa risposta.

**Dove si rompe.** Si rompe due volte. La prima: qui non si misura niente, si legge una misura fatta da altri, e un timer che non misura non è un timer. La seconda: un orologio da scacchi ha bisogno di due persone che si passino il turno, e in casa c'è una persona sola. **Quello che resta è il ragionamento sulla regola**, che è la parte più interessante e la meno praticata: quasi nessuno che usi un cronometro ha mai scelto fra due modi di farlo scorrere.

## Da riprendere alla rassegna

**La stessa prestazione, sotto due regole d'orologio, produce due verdetti opposti.** Centocinquantaquattro secondi di ritardo o ottantasei di avanzo, per la stessa identica partita; e chi ha pensato meno può risultare quello che sta peggio. **La regola con cui si misura un tempo non è meno importante del tempo**, ed è la parte che nessuno mostra. Si accosta al risultato della voce 259, classifica sulle quattro convenzioni di pari merito: là cambiava il numero accanto al nome, qui cambia chi perde.

**Il cronometro che conta in avanti è la sola forma della famiglia del tempo che non minacci niente**, e nessuna delle quattro voci vicine lo era. La voce 88, sfida contro un tempo impone, la voce 189, conto alla rovescia incalza, la voce 190, classifica dei tempi confronta. Un cronometro dice soltanto quanto ci hai messo, e lo dice dopo. **Alla rassegna: quando una famiglia di forme sembra tutta da scartare, conviene cercare il membro che non fa la cosa per cui la famiglia viene scartata.**

**La modalità clessidra è la struttura più elegante del capitolo e nessuno la usa.** La somma dei due orologi non cambia mai, non c'è durata massima, e si perde solo restando indietro rispetto all'altro di quanto valeva l'assegnazione iniziale. `time-control.txt` la liquida in tre parole: «l'uso di questo controllo del tempo è poco comune». **Vale come promemoria che le forme rare non sono rare perché siano state provate e scartate**, ed è il terzo caso in questo capitolo, dopo il grafico di andamento e il byo-yomi canadese.

**Il tempo condonato è un vincolo espresso al rovescio, e conviene guardarlo così.** Sei secondi condonati per mossa moltiplicano per 3,81 i modi di stare dentro cinquanta secondi. **Una regola che regala poco all'inizio di ogni unità è molto più larga di una che regala molto una volta sola**, e questo è un modo di allentare un vincolo che l'elenco non ha ancora incontrato altrove.
