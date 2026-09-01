# Problema di parità

- **Numero** 363 nell'enciclopedia, capitolo 13 — Giochi matematici e ricreativi
- **Si chiama anche** argomento di parità, parity argument, argomento di colorazione, coloring argument, scacchiera mutilata, mutilated chessboard, dimostrazione di impossibilità, pari e dispari
- **In una riga** si dimostra che una cosa è impossibile guardando che qualcosa non cambia mai.
- **Contratto** voce breve
- **Fonti** `mutilated-chessboard.txt`, `parity-mathematics.txt`, `parity-permutation.txt`, `15-puzzle.txt`, lette il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Un problema la cui risposta è «non si può», e la cui dimostrazione sta in una riga: si trova una quantità che ogni mossa lascia pari o lascia dispari, si guarda che all'inizio è pari e alla fine dovrebbe essere dispari, e si è finito. Chi risolve non trova un oggetto: trova un motivo.

Le parti mobili:

- **La quantità.** Il numero di caselle di un colore, la parità di una permutazione, la somma dei posti occupati.
- **Che cosa la conserva.** Ogni mossa legale, e questo va controllato mossa per mossa: è tutta la dimostrazione.
- **Se il foglio lo dice o no.** La scacchiera a colori regala metà dell'argomento. Una scacchiera bianca non lo regala.
- **Se si chiede la risposta o il motivo.** Sono due compiti diversi: «riesci?» è una domanda a cui si risponde con un tentativo, «perché no?» è una domanda a cui si risponde con una riga.

**La glossa dell'elenco non distingue questa voce dalla successiva.** «Si dimostra che una cosa è impossibile guardando che qualcosa non cambia mai» è la definizione di invariante, e la voce 364, invariante dice «la stessa idea generalizzata». La parola *parità* non compare nella glossa: quello che distingue le due voci è che qui la quantità che non cambia è **pari o dispari**, che è l'invariante più piccolo che esista — due valori soli. È una riga dell'elenco che descrive giusto la cosa sbagliata.

## Da dove viene

Il caso di scuola ha un autore e una data. `mutilated-chessboard.txt`: la **scacchiera mutilata** fu posta dal filosofo Max Black nel libro *Critical Thinking* del **1946**, già con un'indicazione della soluzione per colori. Si prende una scacchiera 8×8, si tolgono due angoli opposti — restano 62 caselle — e si chiede di coprirla con 31 tessere da due caselle. Non si può: ogni tessera copre una casella chiara e una scura, quindi ne copre sempre lo stesso numero dei due colori; ma due angoli opposti hanno lo stesso colore, quindi ne restano 30 di un colore e 32 dell'altro.

Il problema è diventato famoso negli anni Cinquanta attraverso Solomon Golomb (1954), Martin Gardner sullo *Scientific American* (1957), George Gamow e Marvin Stern (1958) e Claude Berge (1958). Dal 1964 vive una seconda vita che non c'entra con i giochi: John McCarthy lo propose come banco di prova per le dimostrazioni automatiche, ed è **esponenzialmente difficile per la risoluzione** nella formulazione logica che ne diede. La stessa pagina dice che è studiato in scienze cognitive come caso d'intuizione creativa — che era la ragione per cui Black lo aveva inventato — e in filosofia della matematica per la natura della dimostrazione.

L'altro caso classico è più vecchio ancora. `15-puzzle.txt`: nel **1879** Johnson e Story dimostrarono con un argomento di parità che metà delle posizioni di partenza del gioco del quindici non si risolvono, comunque si muova. L'invariante è la parità della permutazione di tutte e sedici le caselle sommata alla parità della distanza a scacchiera del vuoto dall'angolo in basso a destra: ogni mossa cambia tutte e due, quindi la loro somma resta.

## Varianti e parenti

- **Argomento di colorazione** — la stessa idea con più di due colori.
- **Parità di una permutazione** — `parity-permutation.txt`: le permutazioni di un insieme finito si dividono in due classi, pari e dispari, e ogni scambio passa dall'una all'altra.
- **Giro del re** — un pezzo che si muove di una casella alterna i colori, quindi un percorso che tocca tutte e 64 le caselle non può finire nell'angolo opposto a quello di partenza. Vale anche per il cavallo.
- **Teorema di De Bruijn** — la stessa colorazione in tre dimensioni: non si riempie una scatola 6 × 6 × 6 con mattoni 1 × 2 × 4.
- **Voce 364, invariante** — la generalizzazione, e la voce accanto.
- **Voce 152, problema impossibile** — la forma di pagina; là il compito è accorgersi che non si può, qui è dimostrarlo.
- **Voce 171, puzzle a scorrimento (15, Sokoban)** — la forma di pagina del gioco del quindici.
- **Voce 172, cubo di Rubik e combinatori**, **voce 163, puzzle di fiammiferi (stecchini)**, **voce 173, puzzle a bilanciamento** — tre forme dell'elenco che hanno configurazioni irraggiungibili, e il motivo è ogni volta un invariante.

## Che cosa se ne sa

**Quanto grande è lo spazio che l'argomento chiude.** Le coperture con tessere da due caselle di una scacchiera 8×8 intera sono **12 988 816**, contate in `build/check_359.py` con due metodi indipendenti — una programmazione dinamica sul profilo spezzato e la formula prodotto di Kasteleyn, che concordano. Sulla scacchiera mutilata sono zero. **Una riga di ragionamento sostituisce l'esame di dodici milioni di casi**, e questo è il rapporto più alto fra spazio e argomento di tutto il blocco.

**Il teorema che completa l'argomento, verificato per esaurimento.** `mutilated-chessboard.txt` riporta il teorema di Gomory, pubblicato nel 1973: se si tolgono due caselle **di colore diverso**, la scacchiera si copre sempre. Su una scacchiera 6×6 `build/check_359.py` prova tutte e 630 le coppie di caselle: le **306** coppie dello stesso colore danno zero coperture, e tutte le **324** coppie di colore diverso ne danno almeno una. Nessuna eccezione. La condizione sui colori non è solo necessaria, è anche sufficiente.

**Il limite del teorema sta nella stessa pagina, due righe più sotto.** Gomory vale per una casella di ciascun colore; togliendone di più, anche in numero uguale per colore, si può ottenere una regione che non si copre e per cui l'argomento dei colori non funziona. Chi si ferma alla prima frase porta a casa un teorema più forte di quello che c'è.

**Ci sono almeno tre dimostrazioni diverse, e le altre due non usano i colori.** Una, di Shmuel Winograd, è per induzione sulle righe e conclude che il numero totale di tessere dev'essere pari, mentre ne servono 31. L'altra conta i bordi dei due colori lungo il perimetro. Sono due modi di misurare la stessa disparità.

**La parità non è una proprietà della base dieci.** `parity-mathematics.txt`: in una base pari un numero è dispari se e solo se la sua ultima cifra è dispari, in una base dispari se e solo se la somma delle cifre lo è. La pagina lo mostra in base sette, dove 11 è pari e 124 è dispari. Serve qui perché dice che cosa sia davvero l'invariante: non l'ultima cifra, ma il resto della divisione per due, che si legge in modi diversi secondo come si scrive il numero.

**Dove sta la verifica: dentro l'argomento.** Nessuno deve dire se la risposta è giusta, e non serve niente di stampato: chi ha capito il conto dei colori sa di aver finito, e chi non lo ha capito continua a provare. È il quarto e ultimo gradino della scala del blocco.

## Esempi trovati

Da `mutilated-chessboard.txt`, Max Black, 1946: la scacchiera senza due angoli opposti e le 31 tessere.

Da `15-puzzle.txt`: Sam Loyd offrì mille dollari — la fonte li ragguaglia a 35 833 dollari del 2025 — a chi riuscisse a scambiare il 14 e il 15 lasciando tutto il resto al suo posto. La cosa era già stata dimostrata impossibile una dozzina d'anni prima, nel 1879, perché richiede di passare da una permutazione pari a una dispari. **Il premio più famoso della storia dei rompicapi era per un compito già dimostrato impossibile.**

Da `mutilated-chessboard.txt`: il giro del *wazir*, pezzo di scacchi eterodosso che si muove di una casella in orizzontale o in verticale. Non può partire da un angolo, toccare tutte le caselle una volta sola e finire nell'angolo opposto, perché ogni mossa cambia colore e i due angoli sono dello stesso. Da qui segue anche l'impossibilità di un Numbrix con l'1 in un angolo e il 64 in quello opposto.

Da `mutilated-chessboard.txt`: il teorema di De Bruijn, che con la stessa colorazione in tre dimensioni dice che una scatola 6 × 6 × 6 non si riempie con mattoni 1 × 2 × 4.

## Una nostra versione

> **Trentaquattro pezzi di scotch**
>
> Questo è il pavimento di un ripostiglio, sei piastrelle per sei. Due sono rotte, e sono segnate con una X.
>
> ```
>   X  .  .  .  .  .
>   .  .  .  .  .  .
>   .  .  .  .  .  .
>   .  .  .  .  .  .
>   .  .  .  .  .  .
>   .  .  .  .  .  X
> ```
>
> Devi coprire tutte le altre con strisce lunghe due piastrelle, orizzontali o verticali, senza sovrapporle e senza uscire. Ne servono diciassette.
>
> Provaci. Poi, quando ti sei stancato, colora le piastrelle come una scacchiera e riguarda il disegno.
>
> ```
>   X  #  .  #  .  #
>   #  .  #  .  #  .
>   .  #  .  #  .  #
>   #  .  #  .  #  .
>   .  #  .  #  .  #
>   #  .  #  .  #  X
> ```
>
> Se hai capito perché non si può, prova a togliere due piastrelle diverse in modo che invece si possa. Ce ne sono molti modi, e uno basta.

Il pavimento intero si copre in 6 728 modi; con quei due angoli via, in zero. Togliendo invece la piastrella in alto a sinistra e quella accanto all'angolo in basso a destra — una per colore — i modi tornano a essere **580 modi**. Tutti e tre i numeri sono contati in `build/check_359.py`. La seconda griglia è l'aiuto, e arriva dopo il tentativo: **è un controllo, non un suggerimento**, perché non riduce lo spazio, lo spiega.

## Da riprendere alla rassegna

**È la prima forma dell'enciclopedia in cui la ricompensa è sapere che non c'è niente da trovare.** Chi risolve non consegna un oggetto: smette di cercarlo, e sa perché. Alla rassegna va guardato che cosa succede a una consegna del genere quando nessuno guarda il foglio dopo — perché qui non serve nessuno.

**L'aiuto che spiega invece di restringere.** La seconda griglia non toglie nemmeno una possibilità: le coperture restano zero prima e zero dopo. È l'opposto della distinzione trovata alla voce 356, crucipuzzle, dove una verifica che arriva dopo non era un aiuto che arriva prima; qui l'aiuto arriva dopo **ed è tutto quello che serve.** Vale la pena tenere separate tre cose e non due: quello che restringe, quello che verifica, e quello che fa capire.

**Un premio famoso per un compito già dimostrato impossibile.** I mille dollari di Loyd sono la prova che una domanda posta bene si vende anche quando la risposta è nota da dodici anni. Da riprendere accanto alla voce 152, problema impossibile.

**Il rapporto fra lo spazio e l'argomento è dodici milioni a uno.** È il numero più alto del blocco e forse dell'enciclopedia. Se alla rassegna si cerca la forma che dà più densità per riga stampata, questa è la candidata: sei righe di griglia, una riga di argomento, e cade tutto.

