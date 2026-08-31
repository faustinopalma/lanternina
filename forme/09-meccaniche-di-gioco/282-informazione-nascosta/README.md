# Informazione nascosta

- **Numero** 282 nell'enciclopedia, capitolo 9 — Meccaniche di gioco
- **Si chiama anche** informazione imperfetta, informazione asimmetrica, carte coperte, mano nascosta, *hidden information*, *imperfect information*, *hidden movement*, quello che l'altro sa e tu no
- **In una riga** qualcosa che si sa e qualcosa che no.
- **Fonti** `perfect-information.txt`, `information-set.txt`, `kriegspiel-chess.txt`, `battleship-game.txt`, `cluedo.txt`, `scotland-yard-board-game.txt`, `gamblers-fallacy.txt` sezione sulle carte, tutte lette il 31 agosto 2026; `dark-chess.txt`, `stratego.txt` e `card-counting.txt` sono state aperte e non aggiungono niente che le altre non dicano meglio; i conti sono in `build/check_282.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Una parte dello stato del gioco è nota a qualcuno e non a qualcun altro, e questo è il contenuto invece che un incidente. La definizione tecnica è per contrasto: `perfect-information.txt` chiama a informazione perfetta un gioco in cui ogni giocatore, quando decide, «è perfettamente informato di tutti gli eventi già accaduti, compreso l'evento iniziale» — le mani di partenza comprese. Gli scacchi, il tris, la dama, lo shogi e il go stanno di qua; il poker e il bridge stanno di là.

Parti mobili:

- **Che cosa è nascosto.** Una posizione, una carta, un'identità, una regola, un obiettivo.
- **A chi.** Nascosto a uno solo, a tutti tranne uno, o a tutti — nel terzo caso non c'è asimmetria e la forma diventa un'altra cosa.
- **Chi tiene il segreto.** Un giocatore, un arbitro, una busta chiusa, il retro di una carta. In `kriegspiel-chess.txt` la funzione è talmente separata da avere una persona apposta.
- **Quello che si può chiedere.** Un gioco a informazione nascosta è fatto quasi per intero dalle domande che è lecito fare e dalle risposte ammesse. A Kriegspiel un giocatore prova una mossa e l'arbitro risponde soltanto «lecita» o «illecita», e annuncia le catture e gli scacchi.
- **Quando il segreto viene a galla.** Mai, alla fine, oppure a momenti stabiliti. `scotland-yard-board-game.txt` è il caso più netto della terza possibilità.
- **Quello che trapela.** Nessun segreto è ermetico: ogni mossa fatta o non fatta è un dato su quello che sta sotto.

L'oggetto matematico che descrive tutto questo è **l'insieme informativo**: la raccolta dei nodi dell'albero di gioco fra cui chi deve muovere non sa distinguere. `information-set.txt` lo dice con precisione: in un gioco a informazione perfetta ogni insieme informativo contiene esattamente un nodo; negli altri ne contiene molti, e nei disegni si segna con una linea tratteggiata che unisce le posizioni indistinguibili. Il concetto è di John von Neumann, «motivato dal suo studio del poker».

## Da dove viene

Il nascondere è più vecchio di qualunque teoria, ma il primo caso documentato in cui una regola è stata scritta apposta per togliere la vista è il Kriegspiel di Henry Michael Temple, 1899. `kriegspiel-chess.txt`: si gioca su tre scacchiere, una per giocatore e una per l'arbitro; ognuno vede solo i propri pezzi; **si tenta una mossa e l'arbitro dice se è lecita**, e se non lo è si ritenta. Il gioco è dichiaratamente costruito sul Kriegsspiel prussiano di Georg von Reiswitz, che la pagina data al 1812 — mentre la voce 279, simulazione riporta il 1824 come anno della presentazione allo Stato Maggiore. Le due date non si contraddicono: la prima è del gioco del padre, la seconda della versione del figlio adottata dall'esercito. Vale la pena scriverlo, perché nelle citazioni di seconda mano le due si mescolano.

La battaglia navale è nata come gioco di carta e matita durante la prima guerra mondiale, dice `battleship-game.txt`, e si racconta fosse giocata da ufficiali russi già prima; nel 1907 è nominata nel diario di un poeta russo. È stata pubblicata come blocchetto negli anni Trenta — l'edizione *Salvo* è del 1931 — ed è diventata un gioco di plastica con la Milton Bradley solo nel 1967. **Per cinquant'anni è stata una cosa che si faceva su due fogli qualsiasi.**

Il Cluedo è del 1943: `cluedo.txt` racconta che Anthony E. Pratt, musicista e operaio, lo ideò a Birmingham chiuso in casa durante i bombardamenti, ricordando i giochi di delitto che si facevano nelle serate musicali dove suonava. Brevetto nel 1947, pubblicazione rimandata al 1949 per la scarsità del dopoguerra. Pratt vendette i diritti internazionali per 5 000 sterline nel 1953, equivalenti a 121 280 sterline del 2025 secondo la stessa pagina.

## Varianti e parenti

- **Carte in mano** — la forma più comune: ognuno vede le proprie.
- **Posizione nascosta** — Kriegspiel, gli scacchi al buio, la battaglia navale.
- **Movimento nascosto con affioramenti** — in *Scotland Yard*, 1983, Mister X **deve** mostrare dove si trova in cinque momenti stabiliti, e le caselle del suo registro di viaggio hanno una forma diversa proprio per ricordarglielo.
- **Ruolo nascosto** — non si nasconde una cosa ma chi si è. Va alla voce 285, deduzione sociale.
- **Regola nascosta** — non si nasconde lo stato ma la legge che lo governa. Va alla voce 205, gioco a scatola nera.
- **Nebbia di guerra** — lo spazio si scopre camminandoci. È già trattata per intero alla voce 273, esplorazione, con Clausewitz 1832, la prima occorrenza della locuzione nel 1836 e la definizione di Hale del 1896. Questa scheda non la riapre.
- **Informazione che trapela** — le carte già uscite dicono qualcosa su quelle che restano. `gamblers-fallacy.txt`, che altrove smonta l'idea che il caso abbia memoria, registra il caso in cui invece ce l'ha: **tolto un asso dal mazzo, la probabilità di ciascun altro valore passa da 4/52, il 7,69%, a 4/51, il 7,84%**, e «questo effetto è ciò che permette ai sistemi di conteggio delle carte di funzionare al blackjack».
- **Voce 277, gioco solitario** — dove il segreto non è di nessuno: le carte coperte del Klondike non le sa nemmeno chi ha mescolato.
- **Voce 144, enigma di pesatura** e **voce 146, enigma di cappelli** — informazione nascosta senza avversario, dove tutto il gioco è che cosa si può dedurre.
- **Voce 63, inferire da un'assenza** — il verbo che serve per usare quello che non si vede.

## Che cosa se ne sa

Il costo di non vedere è stato già misurato in questa enciclopedia e conviene ripartire da lì: al Klondike, **con tutte le carte scoperte si vince l'81,942% delle volte e con quelle coperte il 42,76%, cioè 39,2 punti percentuali** (voce 277, gioco solitario). Là il non vedere era una condizione del gioco; qui è una scelta di disegno, e la domanda diventa quanto costa e a chi.

Su una griglia si può calcolare. **Sparando a caso su una griglia da dieci per dieci con diciassette caselle occupate — la flotta della battaglia navale — servono in media 95,39 colpi su cento** (`build/check_282.py`, per la forma chiusa del massimo di *k* estrazioni senza reimmissione, *k*(*n*+1)/(*k*+1), e per simulazione su 20 000 partite). Cioè chi non usa niente di quello che vede finisce per scoprire quasi tutta la griglia.

Sulla griglia da sette per sette con quattro navi da 4, 3, 3 e 2 caselle — quella che sta su un foglio — il conto a caso dà **46,15 colpi su 49**, e una strategia elementare che spara a scacchiera e insegue i colpi andati a segno ne chiede **33,40**. La differenza è di **12,75 colpi, il 27,63%** (stesso script, simulazione su 20 000 partite con la flotta disposta a caso). Questa è la parte che il gioco misura: non quanto si vede, ma quanto si ricava da quello che si vede.

E quanto c'è da sapere si conta. **Su una griglia sette per sette le flotte da 4, 3, 3 e 2 caselle disposte senza sovrapporsi sono 4 364 200**, contate per enumerazione esaustiva con maschere di bit e ricontrollate per campionamento di due milioni di quadruple casuali, che dà 4 370 319, cioè lo 0,14% di scarto. Il logaritmo in base due è 22,06: **ventitré domande a risposta secca sono il minimo teorico**, e trentatré colpi sono quello che serve davvero. La distanza fra i due numeri è quanto costa dover fare le domande sotto forma di colpi.

Il Cluedo dà lo stesso conto su un ordine di grandezza più piccolo. `cluedo.txt` scrive che sei personaggi, sei armi e nove stanze «lasciano ai giocatori 324 possibilità»; **il logaritmo in base due è 8,34, quindi nove domande secche basterebbero**, e una partita ne chiede molte di più perché le domande ammesse non sono quelle.

`information-set.txt` aggiunge la ragione formale per cui questa famiglia si comporta diversamente da tutte le altre: **l'incertezza «cambia in modo fondamentale il modo in cui si deve ragionare sulle strategie ottime»**. Non è una difficoltà in più: è un altro tipo di problema.

Nessuna delle fonti locali misura l'effetto dell'informazione nascosta su chi gioca — quanto piaccia, quanto duri l'attenzione, se serva a qualcosa. Non c'è niente, e va detto invece di girarci intorno.

## Esempi trovati

Da `kriegspiel-chess.txt`: l'arbitro annuncia «pedone perduto in d4», e i giocatori possono chiedere se ci siano catture lecite con un pedone. Chi gioca non conosce la posizione avversaria **ma può tenere il conto di quanti pezzi siano rimasti**. La contabilità è l'unica cosa che resta quando si toglie la vista.

Da `scotland-yard-board-game.txt`: se uno dei cinque affioramenti obbligati capita durante una doppia mossa, Mister X posa la pedina, la fa vedere, la toglie e fa la seconda mossa. Il segreto viene mostrato per un istante e per contratto.

Da `cluedo.txt`: tre carte — un sospetto, un'arma, una stanza — vanno in una busta all'inizio, e in alcune edizioni la busta è **uno specchietto**. L'oggetto che contiene la risposta restituisce l'immagine di chi la cerca.

Da `battleship-game.txt`: nell'edizione *Salvo* del 1931 si spara a un numero stabilito di caselle in una volta sola, e si dice quanti colpi sono andati a segno **senza dire quali**. Lo stesso gioco con una risposta più povera è un gioco diverso.

Da `gamblers-fallacy.txt`: il blackjack, cioè il caso in cui contare quello che è già uscito è legale, funziona e cambia le probabilità di un decimo di punto percentuale alla volta.

## Una nostra versione

> **La flotta che non si vede**
>
> Servono due fogli e due persone, ma la seconda non gioca: **risponde soltanto**, e le sue risposte sono tre parole.
>
> **Il foglio di chi sa.** Disegna quattro navi su questa griglia, dritte, in orizzontale o in verticale, senza sovrapporle: una da quattro caselle, due da tre, una da due. Non farle vedere.
>
> ```
>     A  B  C  D  E  F  G
>  1  .  .  .  .  .  .  .
>  2  .  .  .  .  .  .  .
>  3  .  .  .  .  .  .  .
>  4  .  .  .  .  .  .  .
>  5  .  .  .  .  .  .  .
>  6  .  .  .  .  .  .  .
>  7  .  .  .  .  .  .  .
> ```
>
> D'ora in poi puoi dire **soltanto** una di queste tre cose, e nient'altro: «acqua», «colpito», «affondato».
>
> **Il foglio di chi cerca.** Stessa griglia, vuota. A ogni colpo segna: `o` per acqua, `x` per colpito.
>
> ```
>     A  B  C  D  E  F  G
>  1  .  .  .  .  .  .  .
>  2  .  .  .  .  .  .  .
>  3  .  .  .  .  .  .  .
>  4  .  .  .  .  .  .  .
>  5  .  .  .  .  .  .  .
>  6  .  .  .  .  .  .  .
>  7  .  .  .  .  .  .  .
> ```
>
> Le caselle sono quarantanove e le navi ne occupano dodici. **Sparando a caso ci vogliono in media 46 colpi su 49.** Sparando bene ne bastano intorno a 33. Il tuo obiettivo e' **trentadue**, e qui ci sono trentadue caselle da barrare, una per colpo.
>
> ```
>  i primi sedici    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
>  gli altri sedici  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
> ```
>
> Alla fine, una domanda sola, e va fatta a chi ha cercato: **c'e' stato un momento in cui sapevi dov'era una nave prima di averla colpita tutta?** Se si', segna con un cerchio il colpo dopo il quale l'hai saputo, e di' che cosa te l'ha fatto capire.

La seconda persona qui costa tre parole e non deve pensare a niente: è l'arbitro del Kriegspiel ridotto all'osso, e non gioca. La domanda finale è la parte nuova: chiede di individuare il momento in cui l'insieme delle possibilità è collassato — cioè l'insieme informativo di `information-set.txt` — che è un evento reale, databile, e che nessuna scheda di solito chiede. Il numero stampato — 46 a caso, 33 giocando bene — non è un incoraggiamento: è il termine di paragone senza il quale «trentadue colpi» non vuol dire niente, ed è calcolato e non stimato.

Dove si romperebbe: **con una persona sola non si fa.** Il foglio non può tenere un segreto, perché è stampato tutto insieme e chi lo riceve lo vede tutto; e chi dispone la flotta da sé sa dov'è. Piegare la parte bassa del foglio e fissarla è un rimedio che funziona una volta e solo per chi vuole che funzioni — la verifica non è nel materiale, è nella buona fede. È la stessa cosa già trovata alla voce 105, mazzo di carte per il dorso delle carte ritagliate, e cade per la stessa ragione fisica.

## Da riprendere alla rassegna

**L'informazione nascosta è la prima forma del capitolo che non stia nel formato per un motivo diverso da tutti gli altri.** Non chiede al sistema di contare, di misurare il tempo, di vietare o di registrare: chiede che qualcosa resti non letto, e un foglio stampato non sa non farsi leggere. Il terzo criterio del capitolo — una forma sta nel formato quando la verifica è dentro il materiale — qui dice di no in modo netto, perché la verifica sta in quello che l'altro non ha visto.

**Ma l'arbitro è il ruolo più economico incontrato finora,** e vale la pena isolarlo. Tre parole per colpo, nessuna decisione, nessuna competenza: è meno di quanto chieda la seconda persona di qualunque altra forma dell'elenco. Alla rassegna vale la pena censire tutte le forme che si aprirebbero con un arbitro che non gioca, perché sono probabilmente parecchie e il costo è lo stesso.

**Il momento in cui si sa prima di poterlo dimostrare** è una cosa che nessuna scheda dell'enciclopedia chiedeva. È databile, produce una risposta breve e ha un contenuto vero — la differenza fra sapere e provare. Da provare all'indietro sulla voce 144, enigma di pesatura, sulla voce 146, enigma di cappelli e su tutta la seconda metà del capitolo 5.

**Le domande ammesse contano più di quello che è nascosto.** Kriegspiel nasconde una scacchiera intera e concede «lecita o illecita»; *Salvo* nasconde dodici caselle e concede un numero senza le posizioni; il Cluedo nasconde tre carte su ventuno e concede una domanda per volta. Alla rassegna: per ogni forma con qualcosa di coperto, scrivere separatamente che cosa è coperto e che cosa si può chiedere, perché la seconda riga determina la forma più della prima.

**Ventitré domande secche contro trentatré colpi** è la misura di quanto costi dover fare le domande nella lingua del gioco invece che nella lingua dell'informazione. È un rapporto che si può calcolare per molte forme dell'elenco, e finora non lo si era mai fatto.
