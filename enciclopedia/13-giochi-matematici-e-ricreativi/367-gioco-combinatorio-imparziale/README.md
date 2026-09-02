# Gioco combinatorio imparziale

- **Numero** 367 nell'enciclopedia, capitolo 13 — Giochi matematici e ricreativi
- **Si chiama anche** gioco imparziale, gioco combinatorio, Nim, gioco del ventuno, gioco di sottrazione, *impartial game*, *combinatorial game*, *subtraction game*, *misère*
- **In una riga** Nim e parenti: c'è una strategia vincente e si può trovare.
- **Fonti** [Nim](https://en.wikipedia.org/wiki/Nim), [Combinatorial game theory](https://en.wikipedia.org/wiki/Combinatorial_game_theory), [Impartial game](https://en.wikipedia.org/wiki/Impartial_game), [Sprague–Grundy theorem](https://en.wikipedia.org/wiki/Sprague%E2%80%93Grundy_theorem), [Chomp](https://en.wikipedia.org/wiki/Chomp), lette il 2 settembre 2026; [Nim](https://it.wikipedia.org/wiki/Nim), presa lo stesso giorno, è una pagina di disambiguazione di 1 610 byte e non contiene niente sul gioco

## Che cos'è

Due giocatori a turno, niente dadi, niente carte coperte, e **le mosse che uno può fare sono esattamente quelle che può fare l'altro**. Quest'ultima condizione è tutta la definizione: «Impartial game» dice che un gioco è imparziale quando le mosse dipendono solo dalla posizione e non da chi tocca. Gli scacchi non lo sono, perché il Bianco non muove i pezzi del Nero; il Nim sì, perché chiunque può togliere qualunque gettone.

Le parti mobili:

- **Chi vince alla fine.** Chi fa l'ultima mossa — è la convenzione normale — oppure chi la subisce, ed è la convenzione *misère*. Cambia poco all'aspetto del gioco e moltissimo alla teoria: «Nim» dice che sotto la convenzione *misère* solo i giochi «mansueti» si giocano con la stessa strategia.
- **Quanti mucchi.** Con un mucchio solo la strategia si trova provando; con tre bisogna aver capito qualcosa.
- **Quanto si può togliere.** Tutto quello che si vuole da un mucchio è il Nim; al massimo *k* è il gioco di sottrazione, e allora la strategia è un resto di divisione.
- **Se la strategia esiste, se si conosce, e se si può scrivere.** Sono tre cose diverse, ed è questa la parte interessante — vedi il Chomp qui sotto.

## Da dove viene

«Nim»: varianti del Nim si giocano da tempo antichissimo, forse dalla Cina — assomiglia al *jiǎn-shízǐ*, «raccogliere sassi» —, e i primi riferimenti europei sono di inizio Cinquecento. Il nome lo conia **Charles L. Bouton**, di Harvard, che nel **1901** ne pubblica la teoria completa; l'*Oxford English Dictionary* lo fa risalire al tedesco *nimm*, «prendi».

Poi il gioco diventa una macchina. Alla Fiera mondiale di New York del **1939** la Westinghouse espone il **Nimatron**; fra maggio e ottobre 1940 pochi visitatori riescono a batterlo, e chi ci riesce riceve un gettone con scritto «Nim Champ». Nel 1951 la Ferranti ne costruisce uno per il Festival of Britain, e nel 1952 tre ingegneri della W. L. Maxson ne fanno uno da 23 chilogrammi che vince regolarmente. **È uno dei primi giochi elettronici della storia**, e la ragione è che la strategia sta in tre porte logiche.

La teoria generale è degli anni Trenta: «Combinatorial game theory» e «Sprague–Grundy theorem» datano a **R. P. Sprague (1936)** e **P. M. Grundy (1939)**, indipendentemente, il teorema che ogni gioco imparziale in convenzione normale equivale a un mucchio solo di Nim. Negli anni Sessanta Berlekamp, Conway e Guy allargano la teoria ai giochi *partigiani*, quelli in cui i due giocatori hanno mosse diverse; ne escono *On Numbers and Games* (1976) e *Winning Ways* (1982).

Il Chomp è più giovane e ha due paternità: «Chomp» attribuisce a **David Gale** la formulazione con la tavoletta di cioccolato e a **Frederik Schuh** un gioco equivalente, pubblicato prima, espresso in termini di divisori di un intero.

## Varianti e parenti

- **Gioco di sottrazione** — si può togliere da 1 a *k*; la strategia è tenere il mucchio a un multiplo di *k*+1.
- **Il gioco del ventuno** — si conta a turno dicendo uno, due o tre numeri, e chi dice 21 perde. La strategia vincente è dire sempre un multiplo di quattro.
- **Il gioco del cento** — si parte da zero e si somma da 1 a 10; vince chi arriva a 100. La strategia è arrivare a 89.
- **Chomp** — la tavoletta di cioccolato con il quadretto avvelenato.
- **Grundy's game** — si divide un mucchio in due parti di dimensione diversa.
- **Nim goloso** — si può prendere solo dal mucchio più grande.
- **Gioco di Wythoff** — si può togliere anche lo stesso numero da tutti i mucchi.
- **Voce 157, enigma di teoria dei giochi** — rimanda qui, e il rimando regge: là il Nim sta come forma di pagina, «un gioco stampato la cui analisi è l'esercizio». Quella voce dice che il confine è «particolarmente sottile, perché la strategia del Nim si scrive in binario e quello è matematica». Le fonti lette adesso confermano che il confine sta dove lo aveva messo.
- **Voce 156, problema di scacchi** — rimanda qui per dire che gli scacchi **non** sono imparziali, e la ragione che dà — il Bianco non può muovere i pezzi del Nero — è parola per parola quella di «Combinatorial game theory».
- **Voce 172, cubo di Rubik e combinatori** — rimanda qui per dire che là il giocatore è uno solo. Regge.
- **Voce 363, problema di parità** — la strategia del Nim a due mucchi uguali è un invariante: si copia la mossa dell'altro e la differenza resta zero.

## Che cosa se ne sa

**La strategia del Nim si scrive in una riga e si controlla in tre.** «Nim»: si sommano le dimensioni dei mucchi in binario senza riporti — la somma di Nim —, e si muove sempre lasciando somma zero. Su tre file da 3, 4 e 5 la somma di Nim vale 2, le mosse legali sono **12 mosse**, e quelle che vincono sono **una sola**: togliere due gettoni dalla fila da tre. Contato. Il valore di Grundy calcolato per ricorsione — cioè cercando il più piccolo numero non raggiungibile, senza mai toccare il binario — su tutte le 120 posizioni sotto (3,4,5) coincide ogni volta con la somma di Nim. Due strade indipendenti per lo stesso numero.

**Il Chomp è il caso interessante, e la ragione è che la strategia si sa che c'è e non si sa quale.** «Chomp»: per una tavoletta rettangolare qualunque, tranne l'1×1, **vince chi comincia**, e la dimostrazione è un furto di strategia — se il secondo avesse una risposta vincente alla mossa «mangio solo il quadretto in basso a destra», il primo poteva giocare quella risposta come prima mossa. **La dimostrazione non produce nessuna mossa.** Verificato per esaurimento che su ogni tavoletta fino a 5×5 vince chi comincia; sulla tavoletta 4×5 le posizioni sono **126** e la prima mossa vincente è una sola. Per tavolette grandi il conto cresce come un coefficiente binomiale, e nessuno sa scrivere la strategia.

**Il teorema che riduce tutto a un mucchio solo.** «Sprague–Grundy theorem»: ogni gioco imparziale in convenzione normale equivale a un mucchio di Nim, e la dimensione di quel mucchio è il valore di Grundy della posizione. È il motivo per cui una voce dell'enciclopedia sui giochi imparziali è una voce sola e non venti: **sono tutti lo stesso gioco travestito.**

**Dove sta la prova che si è finito: in chi gioca contro.** Non c'è una risposta stampata, non c'è niente da rileggere nel materiale, e l'argomento da solo non basta: chi crede di aver capito la strategia lo scopre perdendo. È l'unica voce del blocco in cui la verifica sta in una persona, ed è la classe che il censimento del controllo dell'errore aveva trovato al 14,5% sui due capitoli letti per intero.

**Un gioco risolto resta giocabile, e c'è un dato.** Il Nimatron fu battuto da pochi visitatori in sei mesi di fiera, nel 1940, mentre la teoria completa era pubblicata dal 1901. **Sapere che un gioco è risolto e saperlo giocare sono due cose diverse**, e per una casa questo è un fatto utile: una forma non si consuma perché qualcuno ne conosce la soluzione.

**La fonte italiana non esiste.** «Nim» è una pagina di disambiguazione di 1 610 byte che elenca codici e nomi propri. È il terzo caso del capitolo in cui un concetto centrale non ha una voce in italiano, dopo il gioco matematico e l'invariante.

## Esempi trovati

Da «Nim»: la partita d'esempio con tre mucchi da 3, 4 e 5, che è quella su cui è costruita la scheda qui sotto.

Dalla stessa pagina: il Nim si gioca — e ha un peso simbolico — in *L'anno scorso a Marienbad*, il film di Alain Resnais del 1961. E il Nim fu l'argomento della rubrica di Martin Gardner sullo *Scientific American* del febbraio 1958.

Dalla stessa pagina, il Nim circolare: dieci oggetti in cerchio, e si tolgono uno, due o tre oggetti **adiacenti**; a un certo punto tre non se ne possono più prendere.

Da «Chomp»: la partita d'esempio su una tavoletta 4×5, con la nota che, siccome è dimostrato che il primo giocatore può vincere, almeno una delle sue mosse in quella partita è un errore. **La fonte stampa una partita e dichiara di non sapere quale mossa sia sbagliata.**

Da «Impartial game», l'elenco dei giochi imparziali: Nim, Sprouts, Kayles, Quarto, Cram, Chomp, Sottrai un quadrato, Notakto.

## Un esempio giocabile

Due giochi su un foglio, e il secondo è lì per il motivo opposto al primo.

> **Tre file, e poi la tavoletta**
>
> **Il primo gioco.** Tre file di gettoni.
>
> ```
>  FILA 1  o o o
>  FILA 2  o o o o
>  FILA 3  o o o o o
> ```
>
> A turno si cancella **quanti gettoni si vuole, purché da una fila sola** — almeno uno. Chi cancella l'ultimo gettone di tutti **vince**.
>
> Gioca cinque partite contro qualcuno, e cambia chi comincia. Poi rispondi a questa:
>
> ```
>  In quali situazioni sai gia' che perderai, comunque muovi?
>  ................................................
> ```
>
> **Un suggerimento, e uno solo:** prova con due file soltanto, e guarda che cosa succede quando sono uguali.
>
> ---
>
> **Il secondo gioco.** Una tavoletta di cioccolato quattro per cinque. Il quadretto **X**, in alto a sinistra, è avvelenato.
>
> ```
>   X  .  .  .  .
>   .  .  .  .  .
>   .  .  .  .  .
>   .  .  .  .  .
> ```
>
> A turno si sceglie un quadretto e si mangia **quello e tutti quelli che stanno sotto e a destra**. Chi è costretto a mangiare la **X** perde.
>
> Anche qui, cinque partite.
>
> ---
>
> Del primo gioco c'è una ricetta, e con un po' di partite si trova.
>
> Del secondo si sa una cosa sola: **chi comincia può vincere sempre.** Lo si sa perché, se avesse una risposta vincente chi va secondo, il primo poteva giocare quella risposta subito. Nessuno sa quale sia la ricetta, e non la sa nemmeno chi ti ha stampato questo foglio.

Le due metà stanno insieme perché la seconda si capisce solo per differenza dalla prima. Il primo gioco premia chi cerca la regola; il secondo dice che la regola può non esserci, e che questo non impedisce di sapere chi vince. La riga finale è la sola cosa stampata che chi legge non potrebbe ricavarsi da solo, e non è una soluzione: è una notizia.

## Che cosa la rende interessante

**La differenza da questa voce alla voce 366, problema di grafi**, che è il termine di paragone del blocco: là la prova che si è finito sta in quattro posti diversi secondo la domanda; qui sta sempre nello stesso, e quel posto è **una persona** — l'avversario. È l'unica voce del blocco che chieda due partecipanti, ed è quello che la rende più cara di tutte le altre.

**Un gioco in cui si sa chi vince e non si sa come è una consegna che non ha bisogno di soluzione.** È l'esempio più netto trovato finora di una forma che si può stampare senza sapere la risposta e senza mentire. Il vincolo di chi propone — si stampa solo qualcosa di cui si sia già scritta la risposta — qui morde, ed è l'unica voce del blocco in cui morde; ma il Chomp lo aggira dicendo la verità, cioè che nessuno la sa.

**Un avversario in casa costa poco e cambia tutto.** Le forme raccolte finora presuppongono quasi sempre una persona sola con un foglio. Questa ne vuole due, non chiede nient'altro, e produce da sé la ripetizione che altrove va costruita: cinque partite non annoiano come cinque esercizi.

**La teoria dice che sono tutti lo stesso gioco.** Il teorema di Sprague-Grundy manda tutta la famiglia su un mucchio solo di Nim. Vale la pena chiedersi se la varietà di questi giochi sia una varietà per chi li gioca o solo per chi li guarda da fuori.
