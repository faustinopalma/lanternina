# Crucipuzzle

- **Numero** 356 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Griglie»
- **Si chiama anche** parole intrecciate, parole nascoste, word search, sopa de letras, crucipuzzle serpeggiante
- **In una riga** parole nascoste in una griglia di lettere.
- **Contratto** voce breve
- **Fonti** `it-crucipuzzle.txt` e `word-search.txt`, prese il 30 agosto 2026 e rilette; `it-settimana-enigmistica.txt`, presa il 1 settembre 2026. `it-crucipuzzle.txt` è la pagina `Parole intrecciate`: in italiano `Crucipuzzle` è un rimando, controllato il 1 settembre 2026 con `build/check_titoli_352.py`
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Il caso limite della sezione: **la griglia è già piena**. Le lettere ci sono tutte, le parole anche, e non si scrive niente — si cerchia.

Rispetto alla voce 352, cruciverba il foglio dichiara una cosa in più di tutte le altre voci: non solo il disegno e le domande, ma anche le risposte, e già scritte al posto giusto. Quello che resta a chi risolve non è produrre: è **trovare**, che è il verbo della voce 58, cercare.

**La parte italiana è la chiave**, e cambia la natura della cosa. `it-crucipuzzle.txt`, riletta il 1 settembre 2026: «le lettere eventualmente restanti formano una parola nascosta (chiave) della quale è fornita la definizione». Un crucipuzzle senza chiave finisce quando finisce e nessuno sa se è finito bene; un crucipuzzle con la chiave si verifica da solo, perché se una parola è stata cerchiata storta quello che avanza è rumore.

Parti mobili:

- **Se l'elenco delle parole è dato.** Con l'elenco è una ricerca; senza, bisogna riconoscere le parole invece di verificarle, e resta solo il tema.
- **Quante direzioni.** Orizzontali e verticali per i più piccoli; con le diagonali e i versi rovesciati sono otto.
- **Se la parola è dritta.** Nel crucipuzzle serpeggiante piega di novanta gradi a qualunque lettera, e `word-search.txt` lo dà come molto più difficile.
- **Che cosa si fa delle lettere avanzate.** Niente, oppure la chiave italiana, oppure — nella variante di Kappa Publishing — un messaggio composto da tutte le parole scritte al contrario.

## Da dove viene

`word-search.txt`, riletta il 1 settembre 2026, dà una data e poi la complica da sé: Norman E. Gibat sul *Selenby Digest* del 1° marzo 1968 a Norman, Oklahoma, ma lo spagnolo Pedro Ocón de Oro pubblicava *sopas de letras* già prima, e c'è una terza rivendicazione riportata con un linguaggio che non è neutrale. Il dettaglio che dice di più sul genere è un altro: gli schemi piacquero, **alcune maestre di Norman ne chiesero delle ristampe per la classe**, una ne mandò copia ad amici in altre scuole del paese, e da lì qualcuno vendette l'idea a un'agenzia. Il crucipuzzle è passato dalla rivista alla classe e dalla classe al mondo.

In Italia il gioco è dentro *La Settimana Enigmistica* con la sua numerazione progressiva: `it-settimana-enigmistica.txt`, presa il 1 settembre 2026, porta come esempio del sistema di catalogazione della rivista proprio uno schema di questo tipo — «il gioco Parole intrecciate 2956 del 13 giugno 2009 è il 56º gioco della rivista numero 4029».

## Varianti e parenti

- **Crucipuzzle (word search)** (voce 128, crucipuzzle (word search)) — **il confine da dichiarare**: là la forma in generale, la storia, le strategie di ricerca e la costruzione; qui il gioco dentro la sezione delle griglie, la chiave come verifica e il conto delle collocazioni. La voce 128, crucipuzzle (word search) è stata riletta contro le fonti prima di appoggiarcisi e non è stata trovata sbagliata nei punti che le fonti di questo blocco toccano.
- **Cruciverba** (voce 352, cruciverba) — **la riga di differenza**: là il foglio dichiara il disegno e le domande, qui dichiara anche le risposte e dove sono.
- **Crucintarsio** (voce 355, crucintarsio) — il gradino precedente: là le parole sono date e vanno collocate, qui sono date e sono già collocate.
- **Crucipuzzle serpeggiante** — la parola piega di novanta gradi a ogni lettera; con le pieghe di quarantacinque e la stessa lettera riusabile diventa un'altra cosa. Alcuni serpeggianti tracciano una figura: un quadrato, un ferro di cavallo, una ciambella.
- **Zigzag, kakuro, crossnumber** (voce 358, zigzag, kakuro, crossnumber) — il collegamento è proprio il serpeggiante, e la voce 358, zigzag, kakuro, crossnumber spiega perché.
- **Parole intrecciate illustrate** — al posto dell'elenco ci sono immagini che raffigurano le parole.
- **Parole intrecciate da completare** — in alcune caselle c'è un quadratino da riempire: si cerca e insieme si scrive.
- **Crucipuzzle con domanda** — in fondo alla pagina una domanda di cultura generale, e nella griglia una parola in più che non sta nell'elenco.
- **Steganografia** (voce 135, steganografia) — la parentela vera, e passa dalla chiave: il crucipuzzle italiano è steganografia con le istruzioni allegate.
- **Griglia di Cardano** (voce 141, griglia di Cardano) — l'altro modo di leggere un messaggio dentro una griglia di lettere: là con una maschera forata, qui per sottrazione.

## Che cosa se ne sa

**È l'unica forma della sezione in cui il foglio non toglie niente prima, e controlla tutto dopo.** Una parola di cinque lettere in una griglia otto per otto, con le otto direzioni ammesse, ha **192 collocazioni** — contate per enumerazione in `build/check_352.py`: 64 orizzontali nei due versi, 64 verticali, 64 diagonali. La chiave italiana non ne toglie nessuna: non dice dove guardare, dice se si è guardato bene. In tutte le altre voci della sezione qualcosa restringe lo spazio prima che si cominci; qui lo spazio resta intero e la verifica arriva alla fine.

**Che si possa cercare a lungo senza modo di sapere che non c'è niente lo dimostra uno scherzo.** `word-search.txt` riporta che alcuni insegnanti distribuiscono il primo aprile crucipuzzle che non contengono nessuna parola. Che lo scherzo funzioni è la misura del problema, ed è la ragione per cui la chiave è una buona idea.

**Le griglie generate da un computer lasciano una traccia.** La stessa fonte: le parole tendono a essere disposte secondo schemi regolari, e trovatane una spesso basta guardare le righe, le colonne o le diagonali adiacenti — magari una sì e una no. Vale per tutto quello che si genera in serie, e riguarda direttamente il progetto.

**Nessuna misura di effetto in nessuna delle due fonti.** `word-search.txt` dice che i crucipuzzle si usano in classe, specialmente nelle lingue straniere, e che altri insegnanti li usano come attività ricreativa; non dice se servano a qualcosa e non cita nessuno studio. `it-crucipuzzle.txt` è dichiarata dalla fonte stessa un abbozzo, ed è lunga meno di duemila caratteri.

**Il sistema non può comporre una griglia, uno script sì.** Il sistema non sa manipolare le lettere dentro le parole (misurato, `ideas/10 §6`), e una griglia di crucipuzzle non è fatta d'altro. Ma piazzare parole in un rettangolo e riempire il resto è un lavoro di conta, non di lingua: la griglia stampata più sotto è stata costruita da `build/check_352.py`, che verifica anche che ognuna delle cinque parole vi compaia **una volta sola** e che le lettere avanzate siano esattamente quelle della chiave.

## Esempi trovati

Da Norman, Oklahoma, 1968: il primo schema di Gibat, ristampato su richiesta delle maestre della città.

Dalla Spagna, prima del 1968: le *sopas de letras* di Pedro Ocón de Oro.

Da Kappa Publishing: riviste che si chiamano *The Magazine with the Last Message*, perché le lettere non usate compongono un messaggio finale; e la variante opposta, in cui il messaggio è composto da tutte le parole scritte al contrario.

Dalle aule: crucipuzzle senza nessuna parola dentro, distribuiti il primo aprile.

Dalla televisione: *Now You See It*, un programma della CBS di metà anni Settanta, era un crucipuzzle adattato per lo schermo.

## Una nostra versione

La voce 128, crucipuzzle (word search) fa costruire uno schema e fa tornare il conto delle lettere. Qui invece se ne stampa uno vero, piccolo, e la chiave fa da verifica.

> **Le lettere che avanzano**
>
> ```
>    T A V O L O
>    S L Q U I M
>    E C A I S U
>    D I S N I R
>    I E D E A O
>    A P O R T A
>
>    LANA   MURO   PORTA   SEDIA   TAVOLO
>
>  Le 12 lettere che avanzano, lette riga per riga,
>  dicono che cosa si fa qui.
>
>    --------------------------------------------
> ```
>
> Le cinque parole sono in orizzontale, in verticale o in diagonale, e ognuna c'è una volta sola. Se le hai cerchiate tutte e bene, quello che resta si legge. Se non si legge, una l'hai cerchiata storta — e non serve nessuno per dirtelo.

Le lettere avanzate, lette riga per riga, danno *qui ci si siede*. La griglia è sei per sei, le cinque parole occupano ventiquattro caselle e ne restano dodici, che sono esattamente le lettere della chiave: il conto è stato imposto allo script, non trovato dopo.

La verifica sta dentro il materiale, e in un modo che nessun'altra voce della sezione ha: **non dice dove cercare e dice se si è cercato bene.** È il rovescio di tutte le altre, in cui il foglio aiuta prima e non controlla dopo.

**Dove si romperebbe.** Il sistema non può generare una griglia nuova né verificarne una ricevuta; una griglia prodotta da lui conterrebbe parole spezzate e parole assenti, e chi la ricevesse la cercherebbe a lungo, come nello scherzo del primo aprile. Uno script lo può fare, e l'ha fatto. Sul pannello da quattro righe la griglia sei per sei entra per intero — sei righe da undici caratteri sono meno di metà della larghezza, e le righe sono sei contro quattro, quindi ci vogliono due schermate.

## Da riprendere alla rassegna

**Una verifica che arriva dopo vale quanto un aiuto che arriva prima, e non è la stessa cosa.** In tutte le altre voci della sezione il foglio riduce lo spazio di ricerca; qui lo lascia intero e mette un controllo alla fine. Alla rassegna le due mosse vanno tenute distinte, perché costano diversamente: un aiuto va calibrato, un controllo no.

**La chiave italiana è un pezzo di ingegneria che nessuno chiama così.** Fa quello che nel resto dell'elenco fa il foglio delle soluzioni, senza il foglio delle soluzioni, e senza dire niente a chi sta ancora cercando. Da imitare ovunque un compito abbia molti pezzi e nessun modo di sapere quando è finito.

**Il passaggio dalla rivista alla classe e dalla classe al mondo** è un percorso di diffusione che vale la pena guardare: non è un gioco che la scuola ha adottato, è un gioco che la scuola ha esportato.

