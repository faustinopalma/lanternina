# Puzzle a scorrimento (15, Sokoban)

- **Numero** 171 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi fisici e meccanici»
- **Si chiama anche** gioco del 15, gioco del quindici, taquin, sliding puzzle, sliding block puzzle, n-puzzle, Klotski, Huarong Dao, Rush Hour, Sokoban, gioco delle tessere che scorrono
- **In una riga** tessere che si muovono solo negli spazi liberi, fino a una configurazione voluta.
- **Fonti** `sliding-puzzle.txt`, `15-puzzle.txt`, `klotski.txt`, `rush-hour-puzzle.txt`, `sokoban.txt`, `transport-puzzle.txt`, `mechanical-puzzle.txt` sezione «Sequential movement», `it-gioco-del-15.txt`, lette il 31 agosto 2026. I conti sul telaio 3×3 dell'esempio sono nostri, fatti con `build/check_171.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Un telaio, dei pezzi che lo riempiono quasi tutto, e almeno una casella vuota. I pezzi non si sollevano mai: scivolano dentro il telaio, e l'unico posto in cui possono andare è lo spazio libero. Il compito è arrivare a una configurazione voluta.

Il divieto di sollevare è quello che definisce la famiglia. `sliding-puzzle.txt` lo dice per separare questi rompicapi da quelli di ricomposizione: i pezzi non si tolgono dalla tavola, quindi trovare le mosse e i passaggi che ogni mossa apre è tutto il problema. Nel puzzle a incastro della voce 159, puzzle a incastro (jigsaw) un pezzo si prende in mano e si prova dove capita; qui non si può, e la difficoltà non sta nel riconoscere dove va un pezzo ma nel raggiungerlo.

Parti mobili:

- **Quanto vuoto c'è.** Con una casella libera su sedici il telaio è quasi bloccato; con quattro caselle libere il gioco diventa facile e smette di essere un rompicapo.
- **La forma dei pezzi.** Tutti uguali e quadrati (gioco del 15), di misure diverse (Klotski, dove c'è un blocco 2×2 e vari 1×2), lunghi e vincolati a una direzione sola (Rush Hour, dove le automobili non ruotano).
- **Chi spinge.** Nel Sokoban un personaggio sta dentro la griglia e spinge le casse. Spingere non è muovere: si può solo spingere, mai tirare, e il personaggio deve arrivare dalla parte giusta.
- **Che cosa si vuole.** Tutta la configurazione (gioco del 15), un pezzo solo portato in un punto (Klotski, Rush Hour), tutte le casse sui bersagli (Sokoban).
- **Se le mosse si contano,** e come si contano. Nel gioco del 15 far scivolare tre tessere di fila nella stessa direzione è una mossa o tre, e i due conti danno numeri diversi per lo stesso rompicapo.

La parte mobile che cambia tutto è **se le mosse sono reversibili.** Nel gioco del 15, in Klotski e in Rush Hour ogni mossa si può disfare rifacendola all'indietro: si può perdere tempo, non si può rovinare niente. Nel Sokoban no. `sokoban.txt` lo scrive esplicitamente: tirare le casse non è possibile, quindi una cassa spinta contro un muro o in un angolo può restare bloccata per sempre, e la situazione che ne nasce — un *deadlock* — rende il rompicapo insolubile qualunque cosa si faccia dopo, a meno di tornare indietro di parecchi passi. **Sono due forme diverse sotto lo stesso nome:** una in cui non si può fallire e una in cui si può fallire senza accorgersene.

## Da dove viene

Il capostipite è il gioco del 15, e la sua storia è documentata bene perché è stata contestata. `15-puzzle.txt` la ricostruisce così: **Noyes Palmer Chapman**, direttore dell'ufficio postale di Canastota, nello stato di New York, mostra ad amici già nel **1874** un antenato del gioco, sedici blocchi numerati da disporre in righe di quattro che sommino a 34 — cioè un quadrato magico. Copie del gioco migliorato arrivano a Syracuse, poi a Watch Hill, poi a Hartford, dove gli studenti della American School for the Deaf cominciano a fabbricarlo; **entro il dicembre 1879** si vende a Hartford e a Boston. Matthias Rice, che a Boston ha una falegnameria, comincia a produrlo e lo fa vendere con il nome di *Gem Puzzle*. Nel gennaio 1880 un dentista di Worcester offre un premio in denaro per una soluzione, e il gioco diventa una mania negli Stati Uniti nel **1880**. Chapman chiede il brevetto il **21 febbraio 1880** e se lo vede rifiutare, probabilmente perché troppo simile al brevetto «Puzzle-Blocks» US 207124 concesso a Ernest U. Kinsey il 20 agosto 1878.

**Sam Loyd non c'entra niente, e questa è la terza volta in due blocchi.** Dal 1891 alla morte, nel 1911, Loyd sostiene di aver inventato il gioco; il suo primo articolo sul rompicapo è del 1886 e la rivendicazione arriva cinque anni dopo. `sliding-puzzle.txt` scrive che gli viene attribuito a torto anche il merito di averlo reso popolare. La pagina italiana `it-gioco-del-15.txt` **dice l'opposto**: che il gioco fu «popolarizzato nel 1891 da Samuel Loyd». Si tiene la versione inglese, perché è quella che porta le date primarie — l'articolo del 1886, la rivendicazione del 1891, il rifiuto del brevetto del 1880 — mentre la pagina italiana non ne porta nessuna. Le due divergono anche su un dettaglio minore: per la pagina inglese Chapman era *postmaster*, cioè direttore dell'ufficio postale, per quella italiana «postino»; nessuna delle due cita una fonte per questo, e **va verificato**.

Il seguito della storia di Loyd è la cosa più utile di tutta la voce. Loyd offre **mille dollari** — circa 35 800 dollari del 2025, secondo la conversione data dalla pagina — a chi riesca a scambiare fra loro le tessere 14 e 15 lasciando tutto il resto in ordine. **Non è possibile, e lo si sapeva da più di dieci anni:** Johnson e Story lo avevano dimostrato nel **1879** con un argomento di parità. Il premio era al riparo per costruzione.

Klotski ha invece un'origine confusa, e la fonte lo dichiara. `klotski.txt` scrive che non si sa quale versione sia l'originale, che le rivendicazioni sono molte e in conflitto, e che diversi paesi si dicono all'origine del gioco. Le date certe sono brevetti: Henry Walton nel 1893 per un rompicapo di rettangoli uguali; Frank E. Moss nel 1900 per uno con sei quadrati e quattro rettangoli, fra i primi con pezzi di misure diverse; **Lewis W. Hardy nel 1909** con il *Pennant Puzzle*, prodotto a Chicago dalla OK Novelty Co., che ha lo stesso obiettivo di Klotski; John Harold Fleming in Inghilterra nel **1934**, con un brevetto che include una soluzione in 79 passi. La versione cinese, *Huarong Dao*, compare in un resoconto del **1938**: Lin Dekuan, del Politecnico del Nordovest, vede dei bambini di un villaggio della contea di Chenggu giocarci con pezzi di carta. Il nome «Klotski» è invece recentissimo — viene dalla versione per Windows 3.x della ZH Computer, **1991**, poi inclusa nel Microsoft Windows Entertainment Pack — e prima di allora, dice la fonte, la categoria non aveva un nome d'uso comune.

Rush Hour è di **Nob Yoshigahara**, anni Settanta, venduto negli Stati Uniti dal **1996**. Sokoban è di **Hiroyuki Imabayashi**, che nel **1981** lo scrive in BASIC per il NEC PC-8001 come passatempo, con grafica testuale e cinque livelli; l'idea gli viene dal movimento di un personaggio che spinge bagagli in un gioco d'azione del 1980, dove i bagagli servivano da riparo contro le radiazioni. Fonda la Thinking Rabbit e ne fa il primo titolo commerciale. **La data della pubblicazione non è ferma:** i documenti ufficiali danno la fondazione al 1982 e l'uscita al dicembre 1982, altre fonti danno il 1983, con aprile, maggio e giugno tutti attestati. La fonte riporta il disaccordo invece di scegliere, ed è corretto riportarlo così.

## Varianti e parenti

- **Gioco del 15** — quindici tessere uguali in un telaio 4×4, una casella vuota, e l'ordine numerico come meta. Le versioni con altri numeri di tessere si chiamano 8-puzzle, 24-puzzle, e in generale *n*-puzzle.
- **Puzzle a scorrimento con lettere** — molto diffusi dagli anni Cinquanta agli Ottanta secondo `sliding-puzzle.txt`; hanno più soluzioni possibili, perché le parole che si possono formare sono più di una.
- **Klotski, Huarong Dao, L'Âne Rouge** — pezzi di misure diverse, e un solo pezzo da portare all'uscita.
- **Rush Hour** — pezzi lunghi che si muovono solo lungo il proprio asse; è la stessa idea con un vincolo di direzione in più.
- **Sokoban** — non si scivola, si spinge; e spingere è irreversibile.
- **Minus Cube** — versione tridimensionale prodotta in Unione Sovietica, con le stesse operazioni del gioco del 15.
- **Voce 172, cubo di Rubik e combinatori** — l'altra forma in cui i pezzi non escono mai e metà delle configurazioni non si raggiunge. La differenza è che lì non c'è nessun vuoto: il vincolo non è lo spazio ma la meccanica degli strati.
- **Voce 165, labirinto logico** — anche lì una regola di movimento strana trasforma una griglia in un rompicapo, ma i pezzi sono uno solo e non si spinge niente.
- **Voce 164, labirinto su carta** — il parente in cui la strada è disegnata invece che aperta dalle mosse.
- **Voce 143, enigma di attraversamento** — `transport-puzzle.txt` mette i due nella stessa categoria: rompicapi in cui niente si aggiunge e niente si perde, e la difficoltà è la strada nello spazio degli stati. Lì però il vincolo è una regola dichiarata a parole, qui è la forma del telaio.
- **Voce 159, puzzle a incastro (jigsaw)** — il confine è il sollevamento: là si prende in mano, qui no.
- **Voce 45, composizione fisica** — la forma larga di cui questa è il caso vincolato.
- **Voce 363, problema di parità** e **voce 364, invariante** — il capitolo 13 raccoglie i problemi che chiedono un'idea matematica, e la dimostrazione di Johnson e Story sta lì. Qui si descrive la forma di pagina: che il telaio abbia metà delle configurazioni irraggiungibili è un fatto sulla forma, e come si dimostri appartiene a quelle voci.

## Che cosa se ne sa

**Metà delle configurazioni non si raggiunge.** Johnson e Story, 1879, mostrano con un argomento di parità che metà delle posizioni di partenza dell'*n*-puzzle sono irrisolvibili, comunque si giochi (`15-puzzle.txt`). L'invariante è la parità della permutazione delle sedici caselle sommata alla parità della distanza a scacchiera della casella vuota dall'angolo in basso a destra, e non cambia mai perché ogni mossa cambia tutte e due. Gli stessi due autori mostrano che sulle tavole *m*×*n* con *m* e *n* almeno 2 tutte le permutazioni pari sono risolvibili: **le classi sono esattamente due**, e la parità è l'unico invariante non banale.

L'abbiamo rifatto sul telaio 3×3 con `build/check_171.py`, per avere numeri nostri invece che ricordati. Delle **362 880** disposizioni possibili di otto tessere e un vuoto, **181 440** si raggiungono dalla configurazione ordinata, cioè esattamente la metà; e le raggiungibili sono esattamente quelle con un numero pari di inversioni fra le tessere. Lo stesso programma conferma il numero che la fonte dà per l'8-puzzle: **la posizione più lontana sta a 31 mosse di una tessera**.

**Le distanze massime sono note e sono piccole.** Per il gioco del 15 le soluzioni ottime vanno da 0 a **80** mosse di una tessera, o 43 se si contano come una sola le scivolate consecutive nella stessa direzione. Quante siano le posizioni che richiedono 80 mosse **la pagina non lo dice in modo coerente**: il testo principale ne dà diciassette, citando Korf, mentre una nota riporta Brüngger e altri, secondo cui Gasser ne aveva trovate nove e loro ne hanno scoperte due nuove — undici. Si tiene il numero 80, su cui le due concordano, e il conteggio resta incerto.

**Trovare una soluzione è facile, trovare la più corta è difficile.** Per l'*n*-puzzle generalizzato risolvere è facile, ma calcolare la soluzione minima è NP-difficile (Ratner e Warmuth, 1986 e 1990), e lo è anche approssimarla entro una costante additiva. Per Rush Hour generalizzato a tavole grandi decidere se una configurazione abbia soluzione è PSPACE-completo; Tromp e Cilibrasi hanno mostrato nel **2005** che resta PSPACE-completo anche con automobili di sola lunghezza 2. Per il Sokoban decidere la risolvibilità è NP-difficile e PSPACE-completo.

**Klotski ha un minimo dimostrato al calcolatore: 81 mosse**, contando come una mossa lo spostamento di un pezzo in qualunque posizione raggiungibile. La prima soluzione in 81 passi pubblicata è di **Martin Gardner**, sullo *Scientific American* del febbraio **1964**. La prima soluzione pubblicata in assoluto, non ottima, è del pedagogista cinese Xǔ Chún Fǎng, nel libro 數學漫談 del marzo **1952**, e usa 100 passi. Il primato Guinness per la risoluzione più veloce di un Klotski 4×5 è di **3,99 secondi**, Lim Kai Yi, 13 giugno 2024.

**Il Sokoban è molto più grande di tutti gli altri, e il numero lo dice.** Nel banco di prova standard XSokoban, novanta problemi, le casse vanno da 6 a 34 e le soluzioni riportate vanno da **97 a 674 spinte**. La fonte fa il confronto da sé: sono lunghezze che superano di molto le 80 mosse del gioco del 15 e le 20 del cubo di Rubik. La stima dello spazio di ricerca per un labirinto 20×20 **è andata persa nell'estrazione del testo** — la pagina scrive «10» e l'esponente non c'è — e quindi non la si riporta.

**Le macchine restano indietro, e la fonte dice dove.** Il primo risolutore automatico documentato, *Rolling Stone*, viene dall'Università dell'Alberta; il successivo, *Festival*, è stato il primo a risolvere l'intero banco di prova, che aveva resistito per più di vent'anni. Nonostante questo, dice `sokoban.txt`, **alcuni problemi che gli esseri umani risolvono restano fuori portata dei risolutori migliori**, e le persone ci arrivano spezzando il problema in sottoproblemi, riconoscendo schemi ed eccezioni, e riusando quello che hanno imparato dai problemi precedenti. È il quarto caso raccolto in cui le macchine falliscono dove il capitolo è più interessante, dopo il puzzle della zebra, la scacchiera mutilata e l'unicità delle griglie.

**Il difetto documentato della famiglia è la monotonia.** Recensendo tre cloni di Sokoban per console, Tom R. Halfhill scrive che i problemi sono «essenzialmente gli stessi», che la varietà si riduce al numero di casse, alla loro posizione e alla forma della stanza, e conclude che tutti e tre richiedono di gradire lo stesso tipo di rompicapo ripetuto. È l'osservazione che riguarda più da vicino un sistema che stampa un foglio al giorno.

**È una struttura a scatola di pezzi e molti problemi,** come il tangram della voce 160, tangram e puzzle di tassellazione: Rush Hour si vende con sedici veicoli e quaranta schede di partenza, e le espansioni sono altre schede più un veicolo. Il materiale resta, e il foglio successivo porta solo una configurazione nuova.

**Bobby Fischer risolveva il gioco del 15 in diciassette secondi**, cronometrato, e lo ha mostrato in televisione l'8 novembre 1972. È un aneddoto, non una misura di quanto sia difficile; vale come limite superiore alla difficoltà per chi ci si allena.

## Esempi trovati

Il gioco del 15 nella sua forma standard: quindici tessere numerate in un telaio quattro per quattro, una casella libera, e l'ordine da 1 a 15 con il vuoto in fondo a destra.

Il *14-15 puzzle* di Loyd: la stessa tavola con le ultime due tessere scambiate, e mille dollari a chi la sistema. Non si può.

Il *Pennant Puzzle* di Hardy, 1909: nove pezzi di misure diverse in un telaio 4×5, e il blocco grande da portare in fondo.

Huarong Dao, nella versione con i personaggi del *Romanzo dei tre regni*: il blocco 2×2 è Cao Cao, che deve scappare, e gli altri pezzi sono i suoi generali e i soldati che gli sbarrano la strada. La fonte nota che la disposizione ricorda gli scacchi cinesi, il che complica ulteriormente l'attribuzione dell'origine.

Rush Hour: griglia 6×6, un'automobile rossa, un'uscita su un lato, e altri veicoli messi di traverso. Le automobili sono lunghe due caselle, i camion tre, e nessuno può girare.

Sokoban: un magazzino visto dall'alto, muri, casse e piazzole. Il magazziniere spinge, non tira, e le piazzole sono tante quante le casse.

*The Legend of Zelda: A Link to the Past*, 1991: un enigma in cui bisogna spingere dei blocchi per liberare la strada verso un baule. La fonte lo porta come esempio di quanto la meccanica sia entrata in giochi che non sono rompicapi.

## Una nostra versione

> **Le due che sembrano uguali**
>
> Ritaglia le otto tessere lungo le linee. Il telaio è il riquadro qui sotto: le tessere ci stanno dentro esatte, e resta libera una casella. **Le tessere non si sollevano mai.** Si fanno scivolare, e l'unico posto in cui possono andare è il buco.
>
> ```
>   ┌───┬───┬───┐
>   │ 1 │ 2 │ 3 │
>   ├───┼───┼───┤     questa è la meta:
>   │ 4 │ 5 │ 6 │     le otto tessere in ordine,
>   ├───┼───┼───┤     e il buco in fondo a destra
>   │ 7 │ 8 │   │
>   └───┴───┴───┘
> ```
>
> Adesso due partenze. Disponi le tessere come nella prima, portala alla meta, e conta le mosse. Poi fai la stessa cosa con la seconda.
>
> ```
>    PARTENZA A              PARTENZA B
>   ┌───┬───┬───┐          ┌───┬───┬───┐
>   │ 7 │ 2 │ 4 │          │ 1 │ 2 │ 3 │
>   ├───┼───┼───┤          ├───┼───┼───┤
>   │ 5 │   │ 6 │          │ 4 │ 5 │ 6 │
>   ├───┼───┼───┤          ├───┼───┼───┤
>   │ 8 │ 3 │ 1 │          │ 8 │ 7 │   │
>   └───┴───┴───┘          └───┴───┴───┘
> ```
>
> **A si fa in venti mosse.** Se ne fai di più va bene lo stesso: venti è il minimo, non un obbligo.
>
> **B non si fa.** Non è difficile: è impossibile, e non perché manchi qualcosa. Sono in ordine tutte e otto le tessere tranne due, e quelle due non si possono scambiare fra loro in nessun modo, nemmeno con un milione di mosse. Nel 1891 un uomo di nome Sam Loyd offrì mille dollari a chi ci riuscisse sulla versione con quindici tessere. Non li pagò mai, e sapeva perché: dodici anni prima due matematici avevano già dimostrato che non si può.
>
> Prima di crederci, **provaci**. Poi c'è la domanda vera, ed è l'unica che qui non ha una risposta stampata:
>
> ```
>   Muovi una tessera qualsiasi, in A. Che cosa NON è cambiato?
>   ───────────────────────────────────────────────────────────────────
>   Muovine un'altra. È ancora vero?
>   ───────────────────────────────────────────────────────────────────
>   Se una cosa non cambia mai, che cosa ti dice su dove puoi arrivare?
>   ───────────────────────────────────────────────────────────────────
> ```

Il foglio è una cosa sola stampata due volte: le stesse otto tessere servono per tutte e due le partenze, e per tutte quelle che verranno. La parte che fa il lavoro è **B**, che è una consegna il cui compito è fallire, e che si dichiara impossibile in anticipo perché altrimenti sarebbe una perdita di tempo mascherata da rompicapo — il difetto che la voce 167, puzzle di districamento ha registrato nel caso peggiore. Le venti mosse di A sono il minimo verificato con `build/check_171.py`, e sono stampate per dare una taratura: chi ne fa quaranta sa di aver girato in tondo, chi ne fa venticinque sa di essere andato quasi dritto.

L'ultima domanda è l'unica parte che nessuno deve correggere: si risponde muovendo una tessera e guardando. Non serve conoscere l'invariante per porla, e chi ci arriva ha trovato da solo il motivo per cui B non si fa. Che cosa sia un invariante, e come si dimostri che quello è l'unico, appartiene alla voce 364, invariante e alla voce 363, problema di parità; qui è il controllo a costo zero che rende l'oggetto capace di dire di no da solo.

Dove si romperebbe: le tessere ritagliate con le forbici non stanno dentro il telaio con la precisione del legno, quindi **si sollevano**, e il divieto che definisce la forma diventa una regola d'onore invece che un fatto meccanico. È lo stesso guasto delle linguette delle forbici della voce 159, puzzle a incastro (jigsaw), ed è la ragione per cui il foglio dice «non si sollevano mai» in grassetto invece di darlo per scontato. Un Sokoban su carta ha il problema opposto e più grave: siccome spingere è irreversibile, per tornare indietro servirebbe una gomma, e la griglia dopo dieci ripensamenti è illeggibile. La versione che regge è a monete o a fagioli su una griglia stampata, e allora il foglio deve stampare la griglia e non le mosse.

## Da riprendere alla rassegna

**Un rompicapo in cui non si può fallire e uno in cui si può, sotto lo stesso nome.** Scivolare è reversibile, spingere no. Per un foglio stampato la differenza è materiale: nel primo caso la carta sopravvive a qualunque numero di ripensamenti, nel secondo il primo errore costa una gomma o un foglio nuovo. **Da guardare su tutte le forme del capitolo:** quali mosse si possono disfare, e quanto costa disfarle.

**Una consegna dichiarata impossibile in anticipo, e verificabile da chi la riceve.** La partenza B non chiede di risolvere: chiede di provare, arrendersi e capire perché. Con la terza figura del tangram della voce 160, tangram e puzzle di tassellazione e con la voce 152, problema impossibile fanno tre; questa è però la prima in cui **l'impossibilità è dichiarata sul foglio prima di cominciare**, e il compito è capire il motivo invece di scoprirlo.

**Un numero minimo stampato come taratura e non come voto.** «Si fa in venti mosse» dice a chi risolve quanto è andato vicino, senza che nessuno debba giudicare. Costa una riga e richiede solo che chi stampa il foglio abbia fatto il conto. Da provare su ogni forma dell'elenco che abbia mosse contabili.

**Un materiale che serve per molti fogli.** Otto tessere ritagliate una volta valgono per tutte le partenze future, come i sette pezzi del tangram. Per un sistema che stampa un foglio al giorno, il costo del secondo foglio è quasi zero.

**Il difetto della monotonia è documentato dai recensori, non dedotto.** «Sono essenzialmente gli stessi» detto di tre giochi che cambiano solo numero e posizione delle casse. Vale la pena tenerlo accanto a ogni forma che si generi variando dei parametri, che è quasi tutto quello che un sistema automatico può fare.

**Terza attribuzione falsa di Sam Loyd, e la regolarità è ormai un dato.** Dopo il *Libro di Tan* e *Pigs in Clover* c'è il gioco del 15, e stavolta la falsificazione è doppia: rivendica un'invenzione altrui e ne trae un premio impossibile da vincere. Le attribuzioni dubbie raccolte arrivano a nove, e **il conto delle volte in cui la pagina italiana è più indulgente di quella inglese arriva a due.**

