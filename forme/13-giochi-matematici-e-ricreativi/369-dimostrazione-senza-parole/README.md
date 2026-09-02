# Dimostrazione senza parole

- **Numero** 369 nell'enciclopedia, capitolo 13 — Giochi matematici e ricreativi
- **Si chiama anche** dimostrazione visiva, prova per figura, *proof without words*, *visual proof*, gnomone, dimostrazione per riarrangiamento
- **In una riga** un disegno che rende evidente un'identità.
- **Contratto** voce breve
- **Fonti** `proof-without-words.txt`, `triangular-number.txt`, `squared-triangular-number.txt`, lette il 2 settembre 2026
- **Stato della ricerca** fatta, 2 settembre 2026

## Che cos'è

Una figura che mostra perché un'affermazione è vera, senza dire niente. `proof-without-words.txt` la definisce come «l'illustrazione di un'identità o di un enunciato matematico che si può dimostrare autoevidente per mezzo di un diagramma, senza nessun testo esplicativo di accompagnamento».

Le parti mobili:

- **Che cosa fa il disegno.** Conta la stessa cosa in due modi, oppure sposta dei pezzi senza cambiarne l'area. Sono i due meccanismi, e non ce ne sono altri nelle pagine lette.
- **Se il caso disegnato basta.** La stessa fonte pone la condizione: quando il diagramma mostra un caso particolare di un enunciato generale, **per essere una dimostrazione deve essere generalizzabile**. Il disegno mostra sempre un caso; quello che lo rende una prova è che si veda come continuare.
- **Se c'è la scritta.** Sotto la figura si può mettere l'identità, oppure niente, oppure la richiesta di scriverla.
- **Se si dà la figura o la si fa fare.** Guardare una figura e costruirla sono due compiti diversi, e il secondo è quello che si può controllare.

## Da dove viene

La forma è antica quanto la geometria greca, ma il nome e il genere editoriale sono recenti. `proof-without-words.txt`: *Mathematics Magazine* e *The College Mathematics Journal* pubblicano da anni una rubrica fissa intitolata «Proof without words»; **Roger B. Nelsen** ne ha raccolti due volumi, nel **1993** e nel **1997**, per la Mathematical Association of America.

Le identità sono molto più vecchie. `squared-triangular-number.txt` attribuisce a **Nicomaco di Gerasa** (circa 60-120 d.C.), alla fine del capitolo 20 dell'*Introduzione all'aritmetica*, l'osservazione da cui segue che la somma dei primi cubi è il quadrato di un numero triangolare — anche se Nicomaco si ferma all'osservazione e non trae la conseguenza. La stessa pagina elenca sette dimostrazioni geometriche raccolte da Nelsen nel 1993, una puramente visiva di Katherine Kanim del 2004, e una di Row del 1893 che somma i numeri di una tavola pitagorica in due modi diversi.

`triangular-number.txt` fa una precisazione storica che vale la pena riportare, perché smonta l'aneddoto più raccontato della matematica scolastica: la storia secondo cui Gauss avrebbe scoperto da ragazzino la formula della somma dei primi *n* numeri è **apocrifa**; Gauss non fu il primo a trovarla, l'origine risale probabilmente ai pitagorici del V secolo a.C., e le due formule sono descritte dal monaco irlandese **Dicuil** intorno all'**816** nel suo *Computus*.

## Varianti e parenti

- **Gnomone** — le squadre a L che si aggiungono a un quadrato: la *n*-esima ha 2*n*−1 caselle, e da qui la somma dei dispari.
- **Riarrangiamento** — i quattro triangoli rettangoli dentro un quadrato di lato *a*+*b*, che dimostrano il teorema di Pitagora spostandosi.
- **Doppio conteggio** — la stessa quantità contata per righe e per colonne, come nella tavola di Row.
- **Numeri figurati** — triangolari, quadrati, esagonali: la figura è la definizione.
- **Voce 370, dissezione geometrica** — la voce accanto, e il confine è netto: là i pezzi si tagliano davvero, qui restano sulla pagina. Il riarrangiamento pitagorico è la zona in cui le due si toccano.
- **Voce 363, problema di parità** — l'altra forma in cui una figura chiude un insieme infinito di casi. Là la figura è la scacchiera colorata, e chiude dicendo che una cosa non si può; qui chiude dicendo che una cosa vale sempre.
- **Voce 33, disegno dal vero** e **voce 49, fotografia** — le altre due voci dell'enciclopedia in cui il prodotto è un'immagine. Qui l'immagine è un argomento, e questa è una categoria che non compariva.
- **Voce 32, controesempio** — il rovescio: là una figura sola abbatte un'affermazione, qui una figura sola la regge.

## Che cosa se ne sa

**Le fonti negano che sia una dimostrazione, e lo fanno più volte.** `proof-without-words.txt` riporta tre affermazioni convergenti: che «una dimostrazione senza parole non è la stessa cosa di una dimostrazione matematica, perché omette i dettagli dell'argomento logico»; che «le dimostrazioni senza parole non sono davvero dimostrazioni, in senso stretto, perché i dettagli tipicamente mancano» (Benson e altri, 2004); e Spivak, «fondare l'argomento su un'immagine geometrica non è però una dimostrazione». Una recensione della MAA arriva a scrivere che il termine, «si può sostenere, è applicato qui in modo lasco». La pagina conclude che i matematici le usano **come illustrazioni e come strumenti didattici per idee già dimostrate formalmente**.

**La stessa pagina dice anche il contrario, e la contraddizione è apparente.** L'apertura le definisce «più eleganti delle dimostrazioni formali o rigorose, per la loro natura autoevidente», e più sotto dice che possono fornire «intuizioni preziose che aiutano a formulare o a capire meglio una dimostrazione vera». Non è una contraddizione fra fonti: è la stessa pagina che distingue fra il valore didattico, che afferma, e lo statuto logico, che nega. **Le due affermazioni convivono se si legge la prima come una frase su chi guarda e la seconda come una frase su che cosa è provato.**

**Che cosa chiude, in numeri.** L'identità che la nostra figura mostra — la somma dei primi *n* numeri dispari fa *n*² — vale per ogni *n*, cioè per un insieme infinito di casi, e la figura ne disegna uno. `build/check_365.py` la verifica per formula fino a *n* = 400 e per una seconda strada fino a 40: si costruisce il quadrato *n*×*n* e si conta quante caselle stanno in ogni squadra a L, ottenendo 1, 3, 5, 7, … Le due strade non sono la stessa scritta due volte — una somma i dispari, l'altra conta le caselle di una griglia — e concordano. Lo stesso programma verifica il teorema di Nicomaco fino a *n* = 300.

**Dove sta la prova che si è finito: nella figura, e le fonti discutono se basti.** È il caso estremo della scala del blocco. Non c'è niente da rileggere, nessuno a cui chiedere, niente da provare: chi vede, ha finito; chi non vede, non ha niente da controllare. **È anche l'unico posto della scala di cui una fonte dica esplicitamente che non è un posto valido.**

**Un aneddoto di scuola è falso, e l'ha smontato una fonte che non se ne occupava.** La storia di Gauss bambino è definita apocrifa da `triangular-number.txt`, che aggiunge una data — Dicuil, 816 — e un'ipotesi più antica, i pitagorici. Serve qui perché quella storia è il modo più diffuso di raccontare esattamente questa identità.

## Esempi trovati

Da `proof-without-words.txt`, la somma dei dispari: in un angolo di una griglia un quadretto vale 1; lo si circonda su due lati con una striscia di tre, e viene un blocco 2×2, cioè 4; altri cinque e viene 3×3, cioè 9. E così avanti.

Dalla stessa pagina, Pitagora: un quadrato di lato *a*+*b* con quattro triangoli rettangoli negli angoli lascia in mezzo un quadrato di area *c*²; spostando i quattro triangoli, lo spazio libero si divide in due quadrati di area *a*² e *b*².

Dalla stessa pagina, la disuguaglianza di Jensen, disegnata come una curva convessa che «stira» una distribuzione.

Da `triangular-number.txt`: la dimostrazione senza parole che ogni numero esagonale è un numero triangolare di lato dispari. E il problema delle strette di mano, la cui risposta per *n* persone è il triangolare di *n*−1.

Da `squared-triangular-number.txt`: la tavola pitagorica di Row, 1893, sommata per righe — ogni riga è *i* volte un numero triangolare — e sommata per gnomoni annidati, dove ogni gnomone fa un cubo.

## Una nostra versione

La forma dà il meglio quando la figura non è data ma va completata, perché è l'unico modo di verificare che sia stata vista.

> **Senza una parola**
>
> ```
>   1  2  3  4  5
>   2  2  3  4  5
>   3  3  3  4  5
>   4  4  4  4  5
>   5  5  5  5  5
>
>  la squadra 1  ha  ....  caselle
>  la squadra 2  ha  ....  caselle
>  la squadra 3  ha  ....  caselle
>  la squadra 4  ha  ....  caselle
>  la squadra 5  ha  ....  caselle
> ```
>
> Il quadrato è cinque per cinque. Le caselle segnate con lo stesso numero formano una **squadra a L**. Conta quante caselle ha ognuna e scrivilo.
>
> ```
>  I cinque numeri che hai scritto, sommati, fanno ......
>  E il quadrato ha ...... caselle.
> ```
>
> ---
>
> Adesso disegna qui sotto lo stesso quadrato **fatto di sei squadre**, e scrivi i sei numeri.
>
> ```
>  ..................................
>  ..................................
>  ..................................
>  ..................................
>  ..................................
>  ..................................
> ```
>
> ```
>  1 + 3 + 5 + 7 + 9 = 25
>  1 + 3 + 5 + 7 + 9 + ...... = ......
> ```
>
> ---
>
> **Una riga sola, e poi hai finito.** Scrivi a parole che cosa dimostra questa figura, in modo che valga anche per un quadrato di lato cento.
>
> ```
>  ..................................................
> ```

La figura è data per *n* = 5 e va rifatta per *n* = 6: è il modo di controllare che sia stata vista e non guardata. L'ultima domanda è il rovescio esatto del nome della forma — si chiede di rimettere le parole —, e le fonti dicono che senza quel passo la figura non è una dimostrazione. Chi si sbaglia lo scopre da solo, perché i suoi numeri non sommano al totale del quadrato.

## Da riprendere alla rassegna

**La differenza da questa voce alla voce 366, problema di grafi**, che è il termine di paragone del blocco: là la prova che si è finito prende quattro valori diversi secondo la domanda; qui ne prende uno, ed è il più estremo dell'enciclopedia — **la verifica è il disegno stesso**, e chi non lo vede non ha niente su cui appoggiarsi. È l'unica volta in cui una fonte contesta che quel posto sia un posto.

**Chiedere di rimettere le parole è una consegna nuova, e vale oltre questa voce.** Il foglio dà una figura che dimostra e chiede la frase. È un compito che si può porre su qualunque immagine che porti un argomento — una mappa, un grafico, uno schema —, e per una casa che stampa in bianco e nero è economico quanto qualunque altra cosa.

**Una figura è una dimostrazione solo se si vede come continuare.** La condizione della fonte — generalizzabile — è anche il criterio di disegno: la nostra scheda la soddisfa chiedendo il caso successivo. Alla rassegna, ogni volta che si consegna un esempio invece di una regola, la domanda da porsi è la stessa.

**Questa forma non ha bisogno di leggere.** Non c'è testo da capire, non ci sono numeri da manipolare, e la parte scritta arriva alla fine e su richiesta. Insieme alla voce 365, principio dei cassetti è la voce del capitolo con la soglia d'ingresso più bassa.
