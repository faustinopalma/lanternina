# Classifica

- **Numero** 259 nell'enciclopedia, capitolo 9 — Meccaniche di gioco
- **Si chiama anche** graduatoria, tabellone, ordine di arrivo, standings, *leaderboard*, *ranking*, lega, girone, piazzamento
- **In una riga** i partecipanti in fila secondo un punteggio.
- **Fonti** `ranking.txt`, `gamification.txt`, `elo-rating-system.txt`, `duolingo.txt`, `high-score.txt`, `motivation-second-language.txt`, `leaderboard.txt` (che è una pagina di disambiguazione e non contiene niente), lette il 31 agosto 2026. I conti sulle quattro strategie di pareggio sono nostri, verificati in `build/check_259.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Più partecipanti hanno un numero ciascuno. I numeri si mettono in ordine, e ognuno riceve un posto.

**Sull'asse dichiarato all'apertura del capitolo — che cosa produce il numero — questa è la forma in cui il numero non viene prodotto affatto.** Nella voce 256, punti c'è una somma, nella voce 257, livelli una soglia, nella voce 258, distintivi / badge un fatto; qui il totale di ciascuno resta esattamente quello che era, e l'unica cosa nuova è **il confronto con gli altri**. `gamification.txt`: le classifiche «ordinano i giocatori secondo il loro successo relativo, misurandoli contro un criterio di successo dato».

**Va tenuta separata da due voci già scritte, e i confini sono diversi fra loro.** La voce 190, classifica dei tempi ordina secondo la **durata di un singolo tentativo** della stessa cosa, e sta al capitolo 5 perché nasce dalle sale giochi e dalle escape room; là il numero è una misura di un evento, qui è un totale che si è accumulato facendo cose diverse. La voce 88, sfida contro un tempo non ha nessun confronto con nessuno: c'è un tempo dato e o ci si sta o no. **Le tre differiscono su che cosa venga messo in fila: una durata, un accumulo, o niente.**

Parti mobili:

- **Come si numerano i pari merito.** Non è un dettaglio: ci sono quattro modi standard e danno numeri diversi.
- **Quanti sono dentro.** Tutti, i primi dieci, o trenta persone scelte a caso.
- **Se si vede il fondo.** Una classifica troncata e una completa mettono in gara persone diverse.
- **Ogni quanto si azzera.** Una settimana, una stagione, mai.
- **Che cosa si somma.** Il volume di quello che si è fatto, oppure la difficoltà di chi si è battuto: sono due classifiche diverse dello stesso gruppo.
- **Se si retrocede.** Uscire dalla classifica scendendo è un'altra forma rispetto a smettere di salire.

## Da dove viene

**La struttura matematica è più vecchia dei giochi ed è precisa.** `ranking.txt`: un ordinamento è una relazione fra elementi tale che, presi due qualsiasi, il primo sta sopra, sotto, o alla pari del secondo. In matematica è un ordine debole, o preordine totale; **non è un ordine totale**, perché due elementi diversi possono avere lo stesso posto. La pagina dà l'esempio: i materiali sono totalmente preordinati per durezza, mentre i gradi di durezza sono totalmente ordinati. E dichiara che cosa serve una classifica: **ridurre misure dettagliate a una successione di numeri ordinali**, così che un'informazione complessa si possa valutare secondo un criterio.

**Il pari merito ha quattro soluzioni standard, con quattro nomi.** La stessa pagina le distingue con la scorciatoia dei numeri prodotti per quattro elementi in cui il secondo e il terzo pareggiano: **1224** (competizione standard: il buco si lascia dopo i pari merito, e chi sta sotto non è toccato), **1334** (competizione modificata: il buco si lascia prima), **1223** (densa: nessun buco), **1234** (ordinale: tutti hanno un numero diverso, e i pari merito si separano in modo arbitrario ma coerente). SPSS le chiama Low, High, Sequential; R le chiama min, max, dense.

**Dai giochi arriva la classifica come cosa da guardare, e la data è quella della voce 190, classifica dei tempi:** *Sea Wolf* della Midway nel 1976 conserva il punteggio più alto, *Space Invaders* nel luglio 1978 lo rende una gara fra sconosciuti, *Star Fire* nel dicembre 1978 permette di scrivere le proprie iniziali accanto (`high-score.txt`).

**Il sistema che ordina per forza dell'avversario invece che per volume nasce negli scacchi.** `elo-rating-system.txt`: la Federazione scacchistica degli Stati Uniti usava un sistema numerico ideato da **Kenneth Harkness** perché i soci potessero seguire il proprio progresso **in termini diversi dalle vittorie e dalle sconfitte in torneo**. Era ragionevolmente equo, ma in certe circostanze dava numeri che molti giudicavano imprecisi. **Arpad Elo**, maestro di scacchi e professore di fisica, propose il sostituto: la USCF lo adottò nel **1960**, la FIDE nel **1970**, e Elo lo descrisse per esteso in *The Rating of Chessplayers, Past and Present*, 1978.

**La classifica settimanale di sconosciuti è recente e ha una forma precisa.** `duolingo.txt`: le leghe mettono in competizione **gruppi fino a trenta persone scelte a caso**, e la posizione è determinata dai punti esperienza fatti **in una settimana**. Le leghe sono dieci, dal bronzo al diamante.

## Varianti e parenti

- **Tabellone dei migliori** — solo i primi, con il resto invisibile.
- **Classifica completa** — tutti in fila, fondo compreso.
- **Lega a fasce** — non una classifica sola, ma molte, e si sale e si scende di fascia. È la forma di Duolingo.
- **Punteggio relativo** — il numero dipende dalla forza di chi si è battuto. È il sistema Elo.
- **Scala a sfide** — non si batte un numero, si sfida una persona e si scambia posto. Descritta alla voce 190, classifica dei tempi.
- **Grafico del proprio andamento** — la stessa cosa con sé stessi al posto degli altri. `gamification.txt` lo tratta come un elemento distinto e opposto.
- **Punteggi stampati che non sono di nessuno** — le sigle «AAA» dei cabinati, messe apposta perché ci sia sempre qualcosa da battere.
- **Voce 256, punti** — il totale che viene messo in fila.
- **Voce 190, classifica dei tempi** — la fila fatta su una durata invece che su un accumulo.
- **Voce 88, sfida contro un tempo** — il caso senza confronto.
- **Voce 9, confronto a coppie** — l'ordinamento ridotto a due elementi, che è la sua unità minima.

## Che cosa se ne sa

**Il risultato che vale di più è che la classifica ha un opposto, e l'opposto è misurato meglio di lei.** `gamification.txt` tratta i **grafici di andamento** come un elemento separato: informano su come si va rispetto a **come si andava prima**, e non rispetto agli altri. La pagina lo dice nei termini della teoria: la classifica usa uno **standard di riferimento sociale**, il grafico uno **standard di riferimento individuale**, e mostrando l'andamento in un periodo fisso il secondo mette a fuoco i miglioramenti. La conclusione riportata: questo favorisce un orientamento alla padronanza, «che è particolarmente utile all'apprendimento».

**È la stessa cosa già trovata alla voce 254, dibattito, arrivandoci da un'altra parte:** misurare quanto una cosa è cambiata è diverso da misurare dove è arrivata, e la prima è quasi sempre più giusta verso chi partiva più indietro.

**Sull'effetto motivazionale delle classifiche la fonte dichiara che è misto, e dà due condizioni.** Werbach e Hunter, riportati da `gamification.txt`: le classifiche motivano **se mancano pochi punti al livello o alla posizione successiva**, e demotivano **se ci si trova in fondo**. E gli effetti positivi della competizione «sono più probabili se i concorrenti stanno all'incirca allo stesso livello di prestazione». **Sono direzioni con una condizione, non grandezze: la pagina non dà nessun numero.**

**La lega di trenta sconosciuti è la risposta di progetto a quella condizione**, e va letta così: se la competizione funziona solo fra pari, il modo di ottenerla è rimescolare il gruppo ogni settimana invece di scegliere chi ci sta dentro.

**Sull'apprendimento con questi meccanismi c'è un risultato nullo, e va riportato per quello che è.** `duolingo.txt` cita uno studio del 2017 (Rachels e Rockinson-Szapkiw, pubblicato nel 2018) che **non ha trovato differenze significative** fra bambini di scuola elementare che imparavano lo spagnolo con l'app e bambini che lo imparavano in classe: entrambi i gruppi mostravano un aumento simile di risultati e di senso di efficacia. È un confronto fra due modi di insegnare e non isola la classifica, ma è l'unico dato locale su un sistema di leghe applicato all'apprendimento.

**La stessa pagina riporta un effetto collaterale, senza misurarlo:** la ludicizzazione ha portato a imbrogli, manomissioni e strategie di gioco che entrano in conflitto con l'apprendimento vero. È una segnalazione, non uno studio.

**Elo dice quanto una differenza di punteggio predice, e questo sì è un numero.** Due giocatori con lo stesso punteggio sono attesi vincere lo stesso numero di partite; **cento punti di differenza corrispondono a un risultato atteso del 64%, duecento punti al 76%**, e ogni quattrocento punti di vantaggio moltiplicano per dieci il risultato atteso rispetto all'avversario. La pagina svolge anche un esempio: un giocatore da 1613 in cinque partite ottiene 2,5 punti contro i 2,88 attesi, e scende a 1601 con un fattore K di 32.

**Le quattro strategie di pareggio danno numeri diversi allo stesso ordine, e si può contare quanto.** Su otto partecipanti con due pari merito a coppie e uno a tre, **sette su otto ricevono un numero diverso a seconda della strategia**, e l'unico che riceve sempre lo stesso è il primo (`build/check_259.py`, ogni strategia calcolata per definizione — contando quanti stanno sopra — e camminando la lista ordinata, concordi, con controprova per complemento). I numeri effettivamente assegnati sono 1, 2, 4, 7, 8 nella competizione standard; 1, 3, 6, 7, 8 nella modificata; 1, 2, 3, 4, 5 nella densa; e tutti gli interi da 1 a 8 nell'ordinale. **L'ordine è lo stesso in tutti e quattro i casi. Cambia solo che numero si legge accanto al proprio nome, e cambia per quasi tutti.**

**Con un partecipante solo tutte e quattro le strategie danno 1.** Non è una curiosità: è la dimostrazione che una classifica di una persona non contiene informazione, comunque la si calcoli. **Il sistema ha una persona sola, e questo è il limite dominante della voce.**

**Una delle pagine chieste non contiene niente.** `leaderboard.txt` è una disambiguazione di 1 470 byte che rimanda a una serie di videogiochi di golf, a un formato di banner pubblicitario e alla pagina sui punteggi. Era già stato scoperto scrivendo la voce 190, classifica dei tempi, ed è stato riverificato oggi.

## Esempi trovati

Le leghe di Duolingo: dieci fasce, trenta persone scelte a caso, e la posizione decisa dai punti fatti in una settimana.

Il sistema Elo negli scacchi, adottato dalla federazione americana nel 1960 e da quella internazionale nel 1970, e poi applicato a tennis, calcio, football americano, baseball, pallacanestro, biliardo, giochi da tavolo e sport elettronici.

Il sistema Harkness che lo ha preceduto, nato perché i soci potessero seguire il proprio progresso in termini diversi dalle vittorie e dalle sconfitte.

I punteggi «AAA» stampati nella memoria dei cabinati, che non appartengono a nessuno e servono perché ci sia sempre qualcosa da battere.

Le quattro convenzioni di pari merito, che convivono nello stesso mondo: SPSS le chiama Low, High e Sequential, R le chiama min, max e dense, e nessuna delle due nomina la quarta allo stesso modo.

## Una nostra versione

> **La fila dei quattro numeri**
>
> Qui sotto ci sono otto risultati di una gara. Il primo ha fatto 41, l'ultimo 15, e in mezzo c'e chi ha pareggiato.
>
> ```
>   A  41        1224     1334     1223     1234
>   B  37       ─────    ─────    ─────    ─────
>   C  37       ─────    ─────    ─────    ─────
>   D  30       ─────    ─────    ─────    ─────
>   E  30       ─────    ─────    ─────    ─────
>   F  30       ─────    ─────    ─────    ─────
>   G  22       ─────    ─────    ─────    ─────
>   H  15       ─────    ─────    ─────    ─────
> ```
>
> **Le quattro colonne sono quattro modi veri di numerare la stessa fila, e si usano tutti.** Le regole sono queste:
>
> ```
>   1224  il tuo numero e uno piu quelli che stanno sopra di te
>   1334  il tuo numero e quanti stanno sopra di te, piu i pari merito, piu te
>   1223  il tuo numero e uno piu i punteggi diversi che stanno sopra di te
>   1234  tutti hanno un numero diverso, e i pari merito si separano in ordine alfabetico
> ```
>
> Riempi le trentadue caselle. Poi rispondi: **c'e qualcuno a cui le quattro colonne danno lo stesso numero?** E se ci fosse un solo partecipante, quanti numeri diversi verrebbero fuori?

Le regole sono date per esteso e non c'è niente da indovinare: il lavoro è applicarle e accorgersi che non coincidono. L'ultima domanda ha una risposta sola — uno — e serve a mostrare che una classifica di una persona è vuota qualunque convenzione si usi. Il primo classificato è l'unico invariante, ed è il fatto che rende visibile quanto la posizione dipenda dalla convenzione.

**Dove si rompe.** Questa versione funziona perché i partecipanti sono dati sul foglio invece di essere persone vere. Una classifica vera richiede più persone e un registro che tenga i loro totali, e il sistema non ha né le une né l'altro. La via d'uscita già registrata alla voce 190, classifica dei tempi — i punteggi stampati che non sono di nessuno — funziona anche qui: **con tre punteggi finti stampati ci sono quattro posizioni possibili, e tre di esse hanno qualcuno appena sopra**, che è la condizione che secondo la fonte rende una classifica motivante.

## Da riprendere alla rassegna

**La classifica ha un gemello meglio documentato, e nessuno lo usa.** Il grafico del proprio andamento fa lo stesso lavoro con uno standard di riferimento individuale, e la fonte gli attribuisce l'orientamento alla padronanza. Non richiede altre persone, non richiede un registro condiviso, e richiede lo stesso registro personale che manca. **Da guardare alla rassegna come la sostituzione più diretta disponibile per l'intera famiglia del confronto.**

**Il pari merito è il posto dove una classifica smette di essere oggettiva.** Quattro convenzioni, tutte in uso, che danno numeri diversi a sette persone su otto. **Un numero che dipende dalla convenzione con cui è stato calcolato non è un fatto su chi lo porta**, e questo va accostato al risultato già raccolto alla voce 250, scienza partecipata (citizen science): se un numero verrà confrontato con un altro, conta più che i due siano fatti uguali che non che siano giusti.

**La lega di trenta sconosciuti rimescolati ogni settimana è la stessa mossa della ridondanza al posto della selezione**, già registrata alla voce 250, scienza partecipata (citizen science). Non si sceglie chi confrontare: si sorteggia, e si sorteggia di nuovo. In tutti e due i casi il problema di sapere qualcosa sulle persone viene aggirato invece che risolto.

**Elo misura contro la difficoltà, non contro il volume.** Una classifica per punti premia chi ha fatto di più; una per punteggio relativo premia chi ha battuto qualcuno di più forte. **È la stessa distinzione fra somma e soglia che apre questo capitolo, spostata sull'avversario**, ed è l'unico modo trovato per fare una classifica che non premi la quantità.

**Con una persona sola una classifica non dice niente, e questo si dimostra invece di sostenerlo.** Tutte e quattro le convenzioni danno 1. Quello che resta praticabile è il confronto con un riferimento stampato — vero, dichiarato finto, o proprio di ieri —, e le tre cose vanno tenute distinte alla rassegna perché non fanno lo stesso effetto.
