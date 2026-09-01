# Spostamento

- **Numero** 319 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che tolgono, aggiungono o cambiano lettere»
- **Si chiama anche** metatesi, spostamento di consonante, spostamento di vocale, spostamento di sillaba, dislocazione, *movement*
- **In una riga** una lettera si sposta altrove nella parola.
- **Contratto** voce breve
- **Fonti** `it-spostamento.txt`, `it-scambio.txt`, `damerau-levenshtein-distance.txt`, prese il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Una lettera lascia il suo posto e va altrove nella parola; le altre si stringono per riempire il buco e nessuna prende il suo posto. *Arrosti* dà *artrosi*: la T è passata dalla sesta casella alla terza. Come per tutto il capitolo, deve venir fuori un'altra parola italiana.

La differenza dallo scambio è che le lettere coinvolte sono una e non due. Quando la lettera si sposta di un posto solo, però, le due cose coincidono, e le fonti lo sanno: `it-scambio.txt` dice che lo scambio «non può essere distinto dallo spostamento o metatesi quando le lettere scambiate sono contigue» e che «esistono opinioni contrastanti»; `it-spostamento.txt` propende per lo scambio, «ma non tutti sono d'accordo».

Differenza dalla voce 321, antipodo, che è il termine di paragone di questo blocco: là non si sceglie niente. **Qui si scelgono due cose, che cosa muovere e dove metterlo, ed è lo spazio di ricerca più grande di tutto il blocco** — 47 stringhe diverse su una parola di otto lettere, contro le 27 dello scambio e le 2 dell'antipodo (`build/check_318.py`).

Parti mobili: il tipo della lettera — di consonante o di vocale; l'unità, lettera o sillaba; e se lo spostamento avviene dentro una parola o attraverso due parole di una frase.

## Da dove viene

Dall'enigmistica italiana, e `it-spostamento.txt` porta in cima l'avviso che la voce non cita fonti sufficienti: quello che segue va preso come repertorio e non come storia accertata.

La fonte fa però un'osservazione che è di terminologia e non di gioco, e che vale la pena di riportare per intero perché è un ragionamento e non un'etichetta: **chiamarlo spostamento o metatesi non è indifferente**, perché solo il primo nome regge la specificazione — spostamento *di consonante*, spostamento *di vocale* — mentre metatesi non si declina. Il nome più preciso è quello che si lascia restringere.

Sull'unità sillabica la fonte dà una regola che si può applicare e che non è ovvia: **lo spostamento di una sillaba resta valido anche se nella parola d'arrivo quel pezzo non è più una sillaba**, per esempio perché la sua consonante iniziale finisce dopo una S e la rende impura. Il gioco è definito sulla parola di partenza.

## Varianti e parenti

- **Spostamento di consonante, di vocale** — le due specificazioni che il nome ammette.
- **Spostamento di sillaba** — l'unità più grande, con la regola sulla sillaba che si disfa.
- **Scambio** (318) — due lettere si scambiano invece che una sola spostarsi; le due coincidono sulle lettere contigue.
- **Metatesi** (320) — lo stesso fenomeno visto dalla linguistica, dove è un mutamento storico e non una mossa.
- **Antipodo** (321) — la trasposizione senza scelte.
- **Sciarada a metatesi** — la fonte registra questo cumulo: si accostano due pezzi come in una sciarada e poi si sposta una lettera. È, dice, un caso particolare di **sciarada alterna** (324).
- **Anagramma** (331) — spostamenti ripetuti a volontà.

## Che cosa se ne sa

`it-spostamento.txt`, presa il 1 settembre 2026, è priva di note e non contiene nessuna misura. Quello che si può misurare viene da fuori e dai conti.

**Spostare una lettera costa due modifiche, e non c'è modo di farlo costare una.** La distanza di Levenshtein la conta come una cancellazione più un'inserzione; la distanza di Damerau–Levenshtein aggiunge la trasposizione ma solo fra caratteri adiacenti, e uno spostamento a distanza non ne è uno. Calcolato sui tre esempi della fonte — *arrosti / artrosi*, *bioccolo / bocciolo*, *strato nevoso / stato nervoso* —, tutti e tre danno 2 con tutte e due le distanze, e in tutti e tre la parola d'arrivo non compare fra le stringhe a una operazione dalla parola di partenza (`build/check_318.py`, con due metodi: programmazione dinamica e enumerazione completa).

Il secondo conto riguarda il formato, ed è il motivo per cui questa voce non si può trattare come le altre. Su *arrosti*, sette lettere, lo spostamento libero produce **30 stringhe diverse**: troppe per una pagina utile e troppe per essere provate a mano. Ma se si dichiara *quale* lettera si sposta — la T — restano **6 stringhe**, cinque volte meno, e ci stanno su due righe.

**È la seconda volta che restringere una regola allarga quello che si riesce a fare**, dopo la voce 317, cambio di vocale, di consonante, di sillaba, dove il cambio ristretto alle vocali passava da cento candidati a otto. Qui la restrizione è di un tipo diverso — non sul tipo della lettera ma sulla sua identità —, e produce lo stesso effetto: uno spazio di ricerca che si stampa.

Il limite del capitolo resta: **il sistema non sa manipolare le lettere dentro le parole** (`ideas/10 §6`), quindi le sei stringhe le ha generate uno script nostro e non il sistema.

## Esempi trovati

Da `it-spostamento.txt`, riscritti: spostamento di consonante *arrosti / artrosi*, e la versione su frase *strato nevoso / stato nervoso*, dove la R attraversa lo spazio fra due parole; spostamento di vocale *bioccolo / bocciolo*.

Da `it-scambio.txt`: gli scambi di estremi come *astio / ostia* sono i casi in cui l'altra mossa fa un lavoro che lo spostamento non farebbe con una sola lettera.

## Una nostra versione

> **Una lettera, sei caselle, una sola parola**
>
> In ARROSTI c'è una T. Toglila e rimettila da qualche altra parte: la parola ha sei posti liberi dove ricacciarla, e questi sono tutti e sei. Non ce n'è un settimo.
>
> ```
>  ARROSIT   ARROTSI   ARRTOSI
>  ARTROSI   ATRROSI   TARROSI
> ```
>
> Una sola è una parola italiana. Cerchiala, e se non la riconosci chiedi a qualcuno che sa che cos'è l'artrosi.
>
> Adesso togli la rete. Se invece della T si può spostare **qualunque** lettera, i tentativi diventano trenta invece di sei: cinque volte tanti, e non ci stanno più su questo foglio. Prova lo stesso, ma su una frase, dove è più facile:
>
> ```
>  STRATO NEVOSO   →   ─────── ────────
> ```
>
> Si sposta una lettera sola, e può passare da una parola all'altra.

Le sei righe **sono lo spazio di ricerca per intero, ma solo perché la regola è stata ristretta prima**: la lettera che si muove è dichiarata. Senza quella restrizione la stessa parola darebbe trenta righe, e la scheda tornerebbe a essere un invito a indovinare.

La seconda metà dichiara il costo della libertà con il numero — trenta contro sei — invece di lasciarlo sentire. E sceglie la frase invece della parola perché lo spazio fra due parole dà alla lettera un posto dove andare che si vede a occhio.

Dove si romperebbe: *artrosi* è una parola che un adolescente può non conoscere, e la scheda lo dice invece di fingere che sia ovvia. Il giudizio su che cosa sia una parola italiana resta fuori dal sistema.

## Da riprendere alla rassegna

**Restringere una regola allarga quello che si riesce a fare, per la seconda volta.** Alla voce 317, cambio di vocale, di consonante, di sillaba la restrizione era sul tipo della lettera; qui è sulla sua identità. Due restrizioni diverse, lo stesso effetto: lo spazio di ricerca scende sotto la soglia della pagina. Alla rassegna vale la pena chiedersi se questa sia una proprietà generale — che ogni forma con uno spazio troppo grande abbia una restrizione che la riporta dentro — o se dipenda dal caso.

**Il nome più preciso è quello che si lascia restringere.** *Spostamento* ammette «di consonante» e «di vocale», *metatesi* no, e la fonte enigmistica sceglie il primo per questo. È un criterio di nomenclatura che vale anche per l'elenco delle forme.

**Dichiarare il costo della libertà con un numero.** Trenta contro sei è una riga che si può stampare accanto alla consegna, e trasforma «adesso è più difficile» in una quantità. Da provare altrove: quasi tutte le forme di questo capitolo hanno una versione libera e una vincolata, e il rapporto fra i due spazi è calcolabile.

**Differenza dal termine di paragone.** Rispetto alla voce 321, antipodo, dove non si sceglie niente, qui si sceglie due volte — che cosa muovere e dove —, e lo spazio passa da 2 a 47 su una parola di otto lettere: è il più grande delle quattro trasposizioni.
