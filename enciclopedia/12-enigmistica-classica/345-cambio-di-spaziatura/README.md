# Cambio di spaziatura

- **Numero** 345 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Crittografie»
- **Si chiama anche** cesura, risegmentazione, doppia lettura, false splitting, rebracketing
- **In una riga** la stessa sequenza di lettere divisa in un altro modo dà un'altra frase.
- **Fonti** [Cesura (enigmistica)](https://it.wikipedia.org/wiki/Cesura_(enigmistica)), [Crittografia (enigmistica)](https://it.wikipedia.org/wiki/Crittografia_(enigmistica)), [Enigmistica](https://it.wikipedia.org/wiki/Enigmistica), [Scriptio continua](https://en.wikipedia.org/wiki/Scriptio_continua), [Rebracketing](https://en.wikipedia.org/wiki/Rebracketing), [Text segmentation](https://en.wikipedia.org/wiki/Text_segmentation), prese il 1 settembre 2026

## Che cos'è

Non è un gioco: è la parte meccanica di parecchi giochi, presa da sola. «Cesura (enigmistica)», presa il 1 settembre 2026, comincia dichiarandolo — «la cesura o risegmentazione è un **meccanismo** alla base di molti giochi enigmistici» — e lo definisce come «il frazionamento delle parole inteso a conferire alla stessa sequenza di lettere una doppia lettura e di conseguenza due diversi significati».

Le lettere restano quelle, nello stesso ordine. Cambia dove cadono gli spazi. È l'invariante su cui poggiano la voce 341, crittografia pura, la voce 336, monoverbo e la metà meccanica del rebus.

La stessa pagina aggiunge due distinzioni che non sono la stessa cosa, e conviene tenerle separate.

**Se ci sia cesura.** «Per aversi vera e propria cesura la suddivisione deve avvenire all'interno delle parole chiave.» In *S tolta, gelo si à = Stolta gelosia* i termini che portano il senso — *tolta*, *gelo* — non vengono spezzati, e la fonte conclude che è un gioco **senza cesura**.

**Se la cesura sia totale o parziale.** È totale quando nessuno degli spazi delle due letture cade nello stesso punto; parziale quando almeno uno coincide.

Parti mobili:

- **Quante lettere.** Da questo dipende quanto è grande il problema, e cresce raddoppiando.
- **Se il diagramma c'è.** Con il diagramma la spartizione è una sola; senza, sono tante quante le combinazioni degli spazi.
- **Se il taglio spezza le parole che contano**, che è la differenza fra una cesura e un accostamento.

## Da dove viene

Dall'enigmistica italiana ottocentesca il meccanismo arriva già maturo: «Enigmistica» registra fra i giochi nati intorno a *La gara degli indovini*, dal 1875, le «sciarade a frase» come *Ad empi mento / Adempimento* e i «non-rebus, oggi frasi a sciarada» come *L'O zio è padre del Vi zio / L'ozio è padre del vizio*.

Ma il problema è più vecchio della scrittura con gli spazi, perché per un lungo tratto gli spazi non c'erano. «Scriptio continua», presa il 1 settembre 2026, ricorda che il greco classico e il latino tardo scrivevano senza separare le parole, e che l'ambiguità che ne veniva era nota: *collectamexiliopubem* si può leggere *collectam ex Ilio pubem*, «un popolo raccolto da Troia», oppure *collectam exilio pubem*, «un popolo raccolto per l'esilio». Gli spazi compaiono nelle Bibbie e nei vangeli irlandesi e anglosassoni del settimo e ottavo secolo, e fra il tredicesimo e il quattordicesimo tutti i testi europei li usano.

**Il gioco ha quindi bisogno della convenzione che viola**, ed è più giovane di lei di cinque secoli.

## Varianti e parenti

- **Crittografia pura** (voce 341, crittografia pura) — il gioco che aggiunge, sopra questo meccanismo, una prima lettura da interpretare.
- **Monoverbo** (voce 336, monoverbo) — il caso in cui, dopo il cambio di spaziatura, di spazi non ne resta nessuno.
- **Crittografia mnemonica** (voce 343, crittografia mnemonica) — l'unico gioco della famiglia che non può mai avere una cesura; è la sua definizione in negativo.
- **Sciarada** (voce 323, sciarada) — l'accostamento di due parole che ne fanno una terza, cioè un cambio di spaziatura senza il vincolo delle due letture di senso compiuto.
- **Anagramma a frase** (voce 332, anagramma a frase) — l'altra conservazione: lì le lettere si permutano, qui restano in ordine.
- **Frase bipartita** (voce 351, frase bipartita) — il parente che sposta una pausa invece di uno spazio, e cambia il senso senza toccare la scrittura.
- **Rebus** (voce 346, rebus) — dove la doppia lettura si applica a quello che si vede in un disegno.
- **Falsa divisione** — quando la stessa cosa succede alla lingua da sé, e non a un gioco.

## Che cosa se ne sa

**Le tre doppie letture datate della fonte, ricontate.** Per ognuna si sono confrontate le lettere nude, si sono calcolate le posizioni degli spazi nelle due letture, e si è verificato che le parole chiave dichiarate dalla fonte fossero spezzate o no:

```
 le due letture                                              cesura
 S tolta gelo si a = Stolta gelosia                          assente
 Di schiena S triste reo = Dischi e nastri stereo            totale
 S oste nerba S ilari principi = Sostener basilari principi  parziale
```

Sono di Il Lupino, 1933; Ames, 1974; Galdino da Varese, 1999. Le lettere si conservano in tutt'e tre — tredici, diciannove, ventiquattro — e i verdetti calcolati coincidono con quelli della fonte.

**Il criterio meccanico da solo darebbe la risposta sbagliata sul primo caso.** Confrontando solo le posizioni degli spazi, la prima riga avrebbe uno spazio in comune con la seconda lettura e verrebbe classificata «parziale». La fonte la dice senza cesura, e ha ragione, perché il criterio non sono gli spazi ma **quali parole si spezzino**. Sapere quali parole siano chiave è un giudizio. **Totale contro parziale si calcola; con cesura contro senza cesura no.**

**Il diagramma non è un aiuto: è la soluzione del problema di spaziatura.** Lo spazio di ricerca è contato per due strade — la formula, perché ognuno degli n−1 intervalli fra due lettere ha o non ha uno spazio, e l'enumerazione completa delle maschere, che dà anche la distribuzione per numero di parole e coincide con i coefficienti binomiali. Per *ultrasferiti*, dodici lettere: 2¹¹ = 2 048 spartizioni possibili, 11 con due parole, **una sola** con il diagramma (6 6). Per *risottoalsugo*, tredici lettere: 4 096, 66 con tre parole, una sola con (7 2 4). **Il diagramma divide lo spazio di ricerca per la sua intera grandezza**, e quello che resta a chi risolve non è dove mettere gli spazi: è quali lettere ci siano.

**Fuori dall'enigmistica lo stesso invariante vale, e c'è un tasso.** «Rebracketing» chiama *rebracketing*, *resegmentation* o *metanalysis* la stessa cosa quando capita alla lingua da sé — *a nadder* diventato *an adder*, *a napron* diventato *an apron*, *ewt* diventato *newt* — e ne dà la frequenza: «al massimo è probabile che lo 0,1% del lessico venga risegmentato in un dato secolo». La fonte qualifica il numero due volte nella stessa frase, *at best* e *only probable*, quindi è un tetto e non una misura. Componendo dieci secoli, e supponendo i secoli indipendenti — ipotesi nostra, e non della fonte —, si arriva a **meno dell'1%**. Il gioco fa in un foglio quello che la lingua fa in mille anni su una parola su cento.

**Dove gli spazi non ci sono, il problema è quotidiano invece che ricreativo.** «Text segmentation» elenca le lingue in cui la separazione delle parole non è banale — cinese, giapponese, thai, lao, vietnamita — e porta un caso in cui l'ambiguità è reale: 美国会不同意 si può segmentare in due modi che danno «gli Stati Uniti non saranno d'accordo» oppure «il Congresso americano non è d'accordo». La stessa pagina osserva che anche in inglese lo spazio è solo «una buona approssimazione» del confine di parola, e porta le grafie oscillanti dei composti — *ice box*, *ice-box*, *icebox*.

## Esempi trovati

Da «Cesura (enigmistica)», i tre già riportati, con autore e anno.

Da «Enigmistica», i due ottocenteschi: *Ad empi mento / Adempimento*, undici lettere, e *L'O zio è padre del Vi zio / L'ozio è padre del vizio*, diciannove. Ricontati lettera per lettera.

Da «Scriptio continua», il caso latino *collectamexiliopubem*, venti lettere e due letture entrambe sensate. Calcolando le posizioni degli spazi risulta una **cesura parziale**, secondo la definizione enigmistica del 1933: due spazi su tre coincidono, e si sposta solo quello fra *ex* e *Ilio*. Un manoscritto di duemila anni fa e un rebus italiano del 1974 ricadono nella stessa classificazione, e nessuna delle due fonti sa dell'altra.

Da «Rebracketing», la lista inglese: *newt*, *adder*, *apron*, *umble-pie*, *nickname*, *umpire*, *orange*. E gli scherzi che la pagina stessa registra: *psychotherapist* letto *psycho the rapist*, *together in trouble* letto *to get her in trouble*. La sezione italiana della stessa pagina ha un esempio solo, il toponimo *Cattaro*: **gli esempi italiani di falsa divisione non sono documentati lì**, e non sono stati cercati altrove.

## Un esempio giocabile

Questo è l'unico posto della sezione in cui non serve manipolare lettere: basta confrontare due righe.

> **Le parole senza gli spazi**
>
> Per mille anni si è scritto senza spazi fra le parole. Chi leggeva doveva metterceli lui, e ogni tanto sbagliava: *collectamexiliopubem*, in un manoscritto latino, vuol dire «un popolo raccolto da Troia» oppure «un popolo raccolto per l'esilio», e non c'è modo di saperlo dalla pagina.
>
> Gli enigmisti italiani ci hanno costruito sopra un gioco. Questo è del secolo scorso:
>
> ```
>  LOZIOEPADREDELVIZIO                        19 lettere
>
>  diagramma  5 1 5 3 5      L'ozio e padre del vizio
>  diagramma  2 3 1 5 3 2 3  L'O zio e padre del Vi zio
> ```
>
> I numeri sono le lunghezze delle parole. **Dati quelli, gli spazi vanno in un posto solo.** Senza, i modi di dividere diciannove lettere sarebbero più di duecentomila.
>
> Adesso tocca a te:
>
> ```
>  1  una frase tua          ...............................
>  2  la stessa senza spazi  ...............................
>  3  quante lettere ......  quanti spazi hai tolto ......
> ```
>
> Dai la riga 2 a qualcuno, con il numero delle lettere ma **senza** il diagramma. Guarda quanto ci mette.
>
> **Come sai di aver ragione:** la riga 1 e la riga 2 devono avere le stesse lettere, nello stesso ordine, e nessuna in più.

Il diagramma è la parte da capire: chi riempie la scheda scopre da sé che i numeri non sono un aiuto ma la risposta, e che togliere gli spazi è facile mentre rimetterli, senza quei numeri, è un problema che cresce raddoppiando.

**Dove si romperebbe.** Un modello linguistico non può inventare una frase che si rispazia, perché non sa manipolare le lettere dentro le parole; ma qui non serve, perché la frase la scrive chi risponde e il controllo è un confronto fra due stringhe. Su un pannello di quattro righe l'esempio risolto ci sta; la parte da riempire no, perché è da scrivere.

## Che cosa la rende interessante

**Questa voce sta fuori dalla variabile della sezione, e lo si dichiara invece di forzarla.** Le altre quattro si ordinano su quanta parte della prima lettura sia meccanica: tutta alla voce 341, crittografia pura, niente alla voce 343, crittografia mnemonica. Qui non c'è nessuna prima lettura: c'è solo il meccanismo, e la fonte stessa lo chiama meccanismo e non gioco.

**Il diagramma è il modello di come si dà un controllo dell'errore senza stampare la soluzione.** Non dice la risposta: dichiara una grandezza che la risposta deve avere, e la grandezza si conta con un dito. Da provare su tutte le forme in cui chi risponde produce testo — quasi sempre esiste un numero di quel tipo, e quasi mai lo si stampa.

**La distinzione fra quello che si calcola e quello che si giudica è netta e sta dentro una sola pagina di fonte.** Totale contro parziale è un confronto fra due insiemi di numeri; con cesura contro senza cesura richiede di sapere quali parole portino il senso. Quando una classificazione ha due livelli, spesso solo il secondo è meccanico, e conviene dire quale.

**Un gioco può essere più giovane della convenzione che rompe.** Gli spazi diventano obbligatori fra il tredicesimo e il quattordicesimo secolo; il gioco che li sposta è dell'Ottocento. Vale la pena chiedersi, per le forme dell'elenco che rompono una regola, da quanto tempo la regola esista: se è recente, la forma non può essere antica.

