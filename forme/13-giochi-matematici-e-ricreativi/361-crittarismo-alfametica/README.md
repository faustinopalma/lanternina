# Crittarismo (alfametica)

- **Numero** 361 nell'enciclopedia, capitolo 13 — Giochi matematici e ricreativi
- **Si chiama anche** aritmetica verbale, verbal arithmetic, cryptarithm, cryptarithmetic, alphametic, alfametica, word addition, somma di parole, digimetico, divisione scheletrica
- **In una riga** un'operazione in cui le lettere stanno per cifre: `SEND + MORE = MONEY`.
- **Contratto** voce breve
- **Fonti** `verbal-arithmetic.txt`, `henry-dudeney.txt`, `sam-loyd.txt`, lette il 1 settembre 2026; nessuna pagina italiana, e il perché è scritto qui sotto
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Un'operazione aritmetica scritta con lettere al posto delle cifre. Chi risolve deve trovare quale cifra sta sotto ogni lettera. `verbal-arithmetic.txt` dà tre regole, e sono tutto quello che serve: **lettere diverse valgono cifre diverse**, **la prima cifra di un numero non è zero**, e un buon problema **ha una soluzione sola**.

Le parti mobili:

- **L'operazione.** Somma, moltiplicazione, divisione. La somma è la forma comune.
- **Quante lettere.** Al massimo dieci, perché le cifre sono dieci.
- **Se le parole vogliono dire qualcosa.** È qui che la glossa dell'elenco sbaglia.
- **Se qualche cifra è data.** Toglie lavoro, e cambia il gioco in un compito di verifica.

**La glossa tratta «crittarismo» e «alfametica» come due nomi della stessa cosa, e la fonte li distingue.** `verbal-arithmetic.txt`: il nome *cryptarithm* fu coniato nel maggio 1931 dall'enigmista Minos — pseudonimo di Simon Vatriquant — sulla rivista belga *Sphinx*, e tradotto *cryptarithmetic* da Maurice Kraitchik nel 1942; **nel 1955 J. A. H. Hunter introdusse la parola *alphametic* per designare i crittarismi le cui lettere formano parole o frasi di senso compiuto.** L'alfametica è un caso particolare del crittarismo, non un suo sinonimo: un crittarismo con lettere qualsiasi resta un crittarismo. La riga dell'elenco mette fra parentesi come glossa quello che è una restrizione, ed è la prima glossa sbagliata trovata nel capitolo 13.

## Da dove viene

Da nessuno che si sappia. `verbal-arithmetic.txt` dice che questi giochi sono antichi e l'inventore è ignoto, e smonta con una data l'idea corrente che li abbia inventati Sam Loyd: nel dicembre 1864 l'*American Agriculturist* ne pubblicò uno, il «Puzzle No. 109», quando Loyd aveva ventitré anni e Dudeney sette. `henry-dudeney.txt` aggiunge la lettura che quella pubblicazione permette: **l'assenza di regole spiegate nel giornale agricolo suggerisce che il gioco fosse già popolare in America nel 1864.** Un fatto ricavato da quello che una fonte non dice.

Il classico è di Dudeney, uscito sullo *Strand Magazine* del luglio 1924:

`SEND + MORE = MONEY`

`henry-dudeney.txt` precisa la sua specialità: Dudeney fu il maggiore esponente di questi giochi, «e i suoi erano sempre alfametici», cioè con lettere che formano frasi. La distinzione di Hunter è nata per descrivere il lavoro di Dudeney trent'anni dopo che l'aveva fatto.

**In italiano il nome che porta questa voce dell'elenco non ha una pagina.** `Crittarismo` non esiste su Wikipedia in italiano, controllato con `build/check_titoli_359.py` il 1 settembre 2026; e nemmeno `Alphametic` e `Cryptarithm` in inglese, che sono rimandi a `Verbal arithmetic`. Il gioco ha tre nomi in inglese e nessuna trattazione in italiano.

## Varianti e parenti

- **Alfametica** — le lettere formano parole o frasi. Il caso di Dudeney.
- **Digimetico** — al posto delle lettere ci sono cifre che stanno per altre cifre.
- **Divisione scheletrica** — una divisione lunga in cui quasi tutte le cifre sono sostituite da asterischi.
- **Sudoku e kakuro criptici** — `verbal-arithmetic.txt` dice che l'alfametica si combina con l'uno e con l'altro.
- **Voce 358, zigzag, kakuro, crossnumber** — l'altra forma in cui lettere e cifre si scambiano di posto, e sta anch'essa in questo capitolo per metà.
- **Voce 131, codice a numeri (a=1)** — il rovescio esatto: là i numeri stanno per lettere.
- **Voce 354, cruciverba crittografato** — la stessa sostituzione, ma dentro una griglia di parole invece che dentro un'addizione.
- **Voce 154, sudoku e affini (Nikoli)** — il sudoku killer, con somme dichiarate su gruppi di caselle, è il ponte fra le due.

## Che cosa se ne sa

**Lo spazio è grande e la deduzione lo azzera.** `SEND + MORE = MONEY` ha otto lettere; le assegnazioni di otto cifre distinte fra dieci sono **1 814 400**, e la fonte dà proprio questo numero come esempio di forza bruta. `verbal-arithmetic.txt` stampa anche la deduzione a mano, in undici passi, che parte da «dalla colonna 5, M = 1, perché è l'unico riporto possibile» e arriva a Y = 2. In `build/check_359.py` il problema è risolto due volte, con il metodo per colonne e con l'enumerazione completa delle 1 814 400 assegnazioni: **i due metodi danno la stessa soluzione unica**, ed è quella della fonte — O=0, M=1, Y=2, E=5, N=6, D=7, R=8, S=9, cioè 9567 + 1085 = 10652.

**Il secondo esempio della fonte torna anche lui.** `TO + GO = OUT` ha soluzione unica: 21 + 81 = 102.

**L'alfametica più lunga che la fonte conosce è verificabile, e verifica.** Anton Pavlis, 1983, quarantuno addendi che formano una frase inglese di senso compiuto — *SO MANY MORE MEN SEEM TO SAY THAT THEY MAY SOON TRY…* — con somma `TESTS`. La fonte dà la chiave nella forma `MANYOTHERS = 2764195083`. Contati gli addendi: sono **41**, come dice. Sommati con quella chiave: **90 393**, che è esattamente `TESTS`. La chiave usa tutte e dieci le cifre.

**Il problema è NP-completo solo se si cambia base.** `verbal-arithmetic.txt` lo dichiara e ne dà subito la ragione: in base dieci le assegnazioni possibili sono al più 10! e si controllano in tempo lineare, quindi la generalizzazione a basi arbitrarie è necessaria perché la difficoltà esista. È un caso raro in cui una fonte spiega perché ha dovuto generalizzare per poter dire una cosa.

**Dove sta la verifica: dentro il materiale.** Chi ha finito rifà l'addizione con le cifre trovate. Non serve nessuno, non serve una risposta stampata, e non serve conoscere l'italiano né l'inglese: le parole sono etichette.

## Esempi trovati

Da `verbal-arithmetic.txt`, Dudeney, *Strand Magazine*, luglio 1924: `SEND + MORE = MONEY`.

Da `verbal-arithmetic.txt`, di autore ignoto: `TO + GO = OUT`.

Da `verbal-arithmetic.txt`, *American Agriculturist*, dicembre 1864, «Puzzle No. 109»: il caso che smonta l'attribuzione a Loyd. La fonte lo nomina in nota e non lo riporta.

Da `verbal-arithmetic.txt`, Anton Pavlis, 1983: quarantuno addendi e la parola `TESTS`.

Da `verbal-arithmetic.txt`: la divisione scheletrica, in cui la fonte dice che quasi tutte le cifre sono asterischi. Anche di questa non c'è esempio nel testo estratto.

## Una nostra versione

> **Due notti fanno un sogno**
>
> Ogni lettera vale una cifra, sempre la stessa. Lettere diverse valgono cifre diverse, e nessun numero comincia per zero.
>
> ```
>      N O T T E
>    + N O T T E
>    -----------
>    = S O G N O
>
>    E =   G =   N =
>    O =   S =   T =
> ```
>
> C'è una risposta sola. Comincia dalla colonna di destra: E + E finisce per O, e questo da solo taglia quasi tutto.

Sei lettere, quindi **151 200** assegnazioni possibili; una sola funziona, e sono 30115 + 30115 = 60230. Costruita e verificata in `build/check_359.py` con i due metodi, per colonne e a forza bruta. La somma è di una parola con sé stessa, e questo è l'aiuto nascosto: la colonna delle unità diventa `2E` e le cifre possibili per E si dimezzano subito.

## Da riprendere alla rassegna

**Il limite del capitolo precedente non morde qui, e vale la pena dire perché.** Il sistema non sa contare le lettere dentro le parole e non deve chiedere qualcosa di cui non abbia già scritto la risposta (`ideas/10 §8`). Un'alfametica si compone al contrario — si sceglie prima la chiave, poi si guarda quali parole tornano — quindi la risposta è scritta prima della domanda. Comporre resta difficile e **risolvere non chiede al sistema niente che non sappia fare**: sostituire cifre e sommare.

**È il terzo gradino della scala del blocco.** La variabile è dove sta la prova che si è finito: da nessuna parte alla voce 359, problema di Fermi, in una risposta stampata alla voce 360, rompicapo classico, e qui dentro il materiale — si rifà l'addizione. Il gradino successivo è la voce 363, problema di parità, dove la prova sta dentro l'argomento.

**Una forma risolvibile senza sapere la lingua.** Come per la voce 355, crucintarsio, qui le lettere sono simboli e non parole: chi risolve non ha bisogno di riconoscerle. È la seconda forma dell'elenco con questa proprietà, e per una casa in cui chi propone e chi risponde non hanno lo stesso vocabolario conta.

**Una glossa può nominare una restrizione come se fosse un sinonimo.** «Crittarismo (alfametica)» mette fra parentesi il sottoinsieme, e chi legge la riga crede che il gioco sia solo quello con le parole di senso compiuto. È la prima riga sbagliata trovata nel capitolo 13, e sbaglia in un modo nuovo rispetto alle quindici del capitolo 12: non dice una cosa falsa, restringe la cosa vera.

