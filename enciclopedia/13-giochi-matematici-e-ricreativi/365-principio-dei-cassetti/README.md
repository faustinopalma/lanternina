# Principio dei cassetti

- **Numero** 365 nell'enciclopedia, capitolo 13 — Giochi matematici e ricreativi
- **Si chiama anche** principio della piccionaia, legge del buco della piccionaia, principio di Dirichlet, principio del cassetto, *pigeonhole principle*, *Schubfachprinzip*, *drawer principle*
- **In una riga** se ci sono più oggetti che cassetti, un cassetto ne ha due.
- **Fonti** [Pigeonhole principle](https://en.wikipedia.org/wiki/Pigeonhole_principle), [Principio dei cassetti](https://it.wikipedia.org/wiki/Principio_dei_cassetti), [Theorem on friends and strangers](https://en.wikipedia.org/wiki/Theorem_on_friends_and_strangers), [Ramsey theory](https://en.wikipedia.org/wiki/Ramsey_theory), lette il 2 settembre 2026

## Che cos'è

Si conta due volte — quante cose, quanti posti — e se le cose sono più dei posti si conclude che due cose stanno insieme. Non si guarda niente e non si trova niente: si sa.

Le parti mobili:

- **Che cosa sono i cassetti.** Quasi mai un cassetto: il numero dei capelli, il giorno del compleanno, il resto di una divisione, il colore di un calzino. Trovare i cassetti è tutto il lavoro, e nessuna consegna li dà già fatti.
- **Quanti oggetti in più.** Uno solo basta per concludere che due stanno insieme. Con *n* oggetti in *m* cassetti, un cassetto ne ha almeno ⌈*n*/*m*⌉, e questo è il conto che serve quando si vuole dire «almeno tre» invece di «almeno due».
- **Se si chiede l'esistenza o l'esempio.** Sono due compiti diversi e il secondo è molto più caro: il principio dice che due persone a Roma hanno lo stesso numero di capelli, e non dice chi.
- **Se il numero dei cassetti è ovvio.** «Nessuno ha più di un milione di capelli» è un'ipotesi, e va dichiarata. Chi non la dichiara ha una dimostrazione che non regge.

## Da dove viene

«Pigeonhole principle»: il primo riferimento scritto sembra una frase del gesuita francese **Jean Leurechon**, nelle *Selectæ Propositiones* del **1622** — «è necessario che due uomini abbiano lo stesso numero di capelli, di scudi, o di altre cose». Il principio per esteso, con altri esempi, compare due anni dopo in un libro spesso attribuito a Leurechon e forse di Jean Appier Hanzelet.

Il nome che si usa è più recente: **Peter Gustav Lejeune Dirichlet**, **1834**, lo chiama *Schubfachprinzip*, principio del cassetto, e scrive di perle distribuite fra cassetti. «Principio dei cassetti» aggiunge che in russo si chiama principio di Dirichlet, «da non confondersi con il principio dello stesso nome sulle funzioni armoniche». L'inglese *pigeonhole* non sono i piccioni: sono le caselle aperte per la posta negli uffici e nelle università.

La generalizzazione ha un nome e una data più tarde. «Ramsey theory»: la teoria di Ramsey — da **Frank P. Ramsey** — pone sempre la stessa domanda, «quanto deve essere grande una struttura perché sia garantito che contenga una certa cosa?», e il principio dei cassetti è il suo caso più piccolo. Il teorema sugli amici e gli estranei, che «Theorem on friends and strangers» enuncia così — **in una comitiva di sei persone ce ne sono sempre tre che si conoscono tutte fra loro, oppure tre che non si conoscono affatto** —, si dimostra con tre righe di principio dei cassetti.

## Varianti e parenti

- **Forma quantificata** — con *n* oggetti in *m* cassetti, uno ne ha almeno ⌈*n*/*m*⌉ e uno al massimo ⌊*n*/*m*⌋.
- **Forma forte** — con quantità diverse per cassetto: se si distribuiscono *q*₁+…+*q*ₙ−*n*+1 oggetti in *n* scatole, o la prima ne ha almeno *q*₁, o la seconda almeno *q*₂, e così via.
- **Forma probabilistica** — anche quando gli oggetti sono meno dei cassetti c'è una probabilità che due si scontrino: «Pigeonhole principle» dà 25% per 2 oggetti in 4 cassetti, 69,76% per 5 in 10 e 93,45% per 10 in 20.
- **Teorema di Ramsey** — la generalizzazione: colorando i lati di un grafo completo abbastanza grande, un sottografo completo monocromatico c'è per forza.
- **Teorema sugli amici e gli estranei** — il caso R(3,3) = 6.
- **Voce 144, enigma di pesatura** — rimanda qui e il rimando regge: «lo stesso tipo di ragionamento, si conta prima e si conclude senza guardare». Con una precisazione che le fonti lette adesso permettono: nella pesatura il conto dice quante pesate **bastano** e si costruisce la strategia, qui il conto dice che una cosa **c'è** e non si costruisce niente.
- **Voce 363, problema di parità** e **voce 364, invariante** — le altre due forme in cui si conclude contando invece che cercando. La differenza: là si conclude che una cosa non esiste, qui che esiste.
- **Voce 366, problema di grafi** — il teorema sugli amici e gli estranei è un problema di grafi, e la nostra versione qui sotto è una colorazione dei quindici lati di un grafo completo su sei punti.
- **Voce 359, problema di Fermi** — l'altra forma del capitolo che poggia su un'ipotesi dichiarata a spanne. Là l'ipotesi produce un numero, qui produce una certezza.

## Che cosa se ne sa

**La forma dimostra che una cosa c'è e non dice quale, e la fonte lo mette fra le sue caratteristiche primarie.** «Ramsey theory»: i risultati di questa famiglia «sono non costruttivi: possono mostrare che una struttura esiste, ma non danno nessun procedimento per trovarla, all'infuori della ricerca a forza bruta», e cita il principio dei cassetti come esempio. **Questa è la riga che colloca la voce sulla scala del blocco**, ed è l'unica del blocco in cui la prova sta in due posti diversi secondo che cosa si chieda: la certezza sta nell'argomento, l'esempio non sta da nessuna parte.

**Il conto sui sei a tavola, rifatto per esaurimento.** Provando tutte le **32 768** colorazioni dei quindici lati fra sei persone, quelle senza un terzetto tutto uguale sono **zero**. Con cinque persone le colorazioni sono **1 024** e quelle buone sono **12**. Il dodici non è un caso: è 4!/2, cioè il numero dei cicli di lunghezza cinque su cinque punti, e ogni soluzione a cinque è un pentagono di un colore e un pentagramma dell'altro. Seconda strada, diversa dalla prima: la formula di Goodman per il minimo numero di terzetti monocromatici dà 0 per cinque persone e **2** per sei, e l'enumerazione dà gli stessi due numeri.

**La stessa domanda con un numero più grande costa quanto tutta la matematica.** «Ramsey theory» avverte che i limiti di questa teoria «crescono esponenzialmente, o anche come la funzione di Ackermann», e che il numero di Graham — uno dei più grandi mai usati in una dimostrazione seria — è un limite superiore per un problema di questa famiglia. Sei persone si contano in un pomeriggio; il caso successivo, R(5,5), non è noto.

**Quanto spazio chiude una frase.** «Principio dei cassetti» conclude che a Roma ci sono almeno due persone con lo stesso numero di capelli, prendendo un milione e uno di cassetti e più di un milione di abitanti. I modi di assegnare a ogni abitante il suo numero di capelli sono un numero di **6 000 007 cifre** — calcolato con il logaritmo, perché scriverlo non si può —, e a deciderli tutti bastano due righe. Alla voce 363, problema di parità lo stesso rapporto era di dodici milioni di casi, che è un numero di otto cifre: qui l'esponente è **sei milioni di cifre**, e le due grandezze non si confrontano sullo stesso asse.

**L'ipotesi che rende vera la conclusione non è nella conclusione.** «Nessuno ha più di un milione di capelli» è una stima, e la fonte inglese la dichiara — «è ragionevole supporre, come limite superiore» —, quella italiana anche. Se l'ipotesi cade, cade tutto. **È la stessa struttura del problema di Fermi**, con la differenza che lì il risultato è un numero approssimato e qui è una certezza: una certezza appoggiata su una stima, che è una cosa più strana di quanto sembri.

**Il principio dice qualcosa sui programmi, e le due pagine lo dicono in due modi.** Nessun algoritmo di compressione senza perdita può rimpicciolire tutti i file: «Principio dei cassetti» lo dimostra contando i file di *M*+1 bit contro tutti quelli più corti; «Pigeonhole principle» dice la stessa cosa e aggiunge le collisioni nelle tabelle hash. È il caso in cui il principio si applica a se stessi invece che a una comitiva.

## Esempi trovati

Da «Pigeonhole principle», i calzini: da un cassetto con calzini neri e blu, tre presi al buio bastano per averne due dello stesso colore.

Dalla stessa pagina, le strette di mano: in una comitiva ci sono sempre due persone che stringono la mano allo stesso numero di persone. La dimostrazione è più fine delle altre, perché i cassetti sono *n* e le persone anche: quello che salva il conto è che «zero» e «tutti gli altri» non possono essere pieni tutti e due.

Dalla stessa pagina, i compleanni: fra 367 persone due compiono gli anni lo stesso giorno, con certezza e non con probabilità.

Dalla stessa pagina, i sottoinsiemi: sei numeri qualsiasi presi fra 1 e 9 contengono sempre due che sommano a 10. I cassetti sono {1,9}, {2,8}, {3,7}, {4,6} e {5}, cioè cinque.

Da «Principio dei cassetti»: cinque persone che vogliono giocare a calcetto in quattro squadre e nessuna delle cinque vuole stare in squadra con un'altra.

Da «Theorem on friends and strangers»: la comitiva di sei.

## Un esempio giocabile

La forma dà il meglio quando chi legge prova prima e capisce dopo, e per questo la scheda comincia dal caso in cui si riesce.

> **Sei a tavola**
>
> Sei persone a cena: **A B C D E F**. Ogni due si conoscevano già, oppure no. Le coppie sono quindici, e sono queste. Scrivi **S** se si conoscevano e **N** se no — come vuoi tu, decidi tu.
>
> ```
>         B    C    D    E    F
>   A    __   __   __   __   __
>   B         __   __   __   __
>   C              __   __   __
>   D                   __   __
>   E                        __
>
>   E ADESSO IN CINQUE
>
>         B    C    D    E
>   A    __   __   __   __
>   B         __   __   __
>   C              __   __
>   D                   __
> ```
>
> **La regola:** non devono esserci tre persone che si conoscevano tutte e tre fra loro, e nemmeno tre che non si conoscevano affatto.
>
> Comincia dalla tabella piccola, quella in cinque. **Si può fare.** Quando ce l'hai, passa a quella grande.
>
> ---
>
> Quando ti sei stancato, prendi una persona qualunque della tabella grande — mettiamo **A** — e guarda le cinque caselle della sua riga. Sono cinque lettere fra S e N.
>
> ```
>  Quante ce ne sono uguali fra loro, al minimo?   ......
> ```
>
> Chiamiamo **X Y Z** le tre persone che con A hanno la stessa lettera. Adesso guarda le tre caselle fra X e Y, fra Y e Z, fra X e Z.
>
> ```
>  Se una di quelle tre ha la lettera di A, chi sono i tre uguali?   ...............
>  Se nessuna delle tre ce l'ha, chi sono i tre uguali?              ...............
> ```

La tabella piccola serve a rendere credibile la grande: chi ha riempito quella in cinque non sospetta che l'altra sia impossibile, e continua a provare. Le tre domande in fondo sono la dimostrazione smontata in tre passi, e la prima delle tre è il principio dei cassetti — cinque caselle, due lettere possibili, quindi almeno tre uguali. Nessuna risposta è stampata da nessuna parte e non ce n'è bisogno: chi arriva in fondo lo sa da sé.

## Che cosa la rende interessante

**Questa forma non ha bisogno di sapere niente.** Non c'è vocabolario, non c'è aritmetica, non c'è una regola da ricordare: c'è da contare fino a cinque. È la voce del capitolo con il gradino d'ingresso più basso, e la conclusione che produce è un teorema.

**La differenza da questa voce alla voce 366, problema di grafi**, che è il termine di paragone del blocco: là la prova che si è finito prende quattro valori diversi secondo la domanda; qui ne prende due sulla stessa domanda — **la certezza sta nell'argomento, l'esempio non sta da nessuna parte** —, ed è l'unico caso del blocco in cui si separano.

**Che una cosa esista e non si sappia quale è una situazione utile e mai usata.** Tutte le forme raccolte finora chiedono di trovare qualcosa. Questa chiede di sapere che c'è. Vale la pena chiedersi che cosa si possa costruire su una consegna che finisce con una certezza invece che con un oggetto.

**Una certezza appoggiata a una stima.** Il conto sui capelli è esatto, l'ipotesi sul milione no. È la stessa struttura del problema di Fermi vista da un'altra parte, e per una casa che stampa fogli è una lezione a costo zero: si può dichiarare l'ipotesi e restare rigorosi.
