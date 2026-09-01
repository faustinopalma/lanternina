# Quadrato magico

- **Numero** 362 nell'enciclopedia, capitolo 13 — Giochi matematici e ricreativi
- **Si chiama anche** magic square, quadrato magico perfetto o normale, costante di magia, somma magica, Lo Shu, Luoshu, quadrato di Dürer, wafq al-a'dad
- **In una riga** righe, colonne e diagonali con la stessa somma.
- **Contratto** voce breve
- **Fonti** `magic-square.txt`, `it-quadrato-magico.txt`, `magic-constant.txt`, `luoshu-square.txt`, `durer-magic-square.txt`, `melencolia-i.txt`, `recreational-mathematics.txt`, lette il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Una tabella quadrata di numeri interi tutti diversi in cui ogni riga, ogni colonna e le due diagonali danno la stessa somma. Il numero di righe si chiama **ordine**, la somma si chiama **costante magica**. Se i numeri sono esattamente gli interi da 1 a n², il quadrato si dice **normale**, o perfetto: quasi tutti gli autori intendono questo.

Le parti mobili:

- **L'ordine.** Le tecniche di costruzione sono diverse per n dispari, per n multiplo di quattro e per gli altri pari; `magic-square.txt` fonda su questo la sua classificazione.
- **Che cosa si chiede in più.** Le diagonali spezzate (pandiagonale), la somma di due caselle simmetriche rispetto al centro (associativo), i quadrati 2×2 (perfettissimo). Ognuna di queste è una famiglia con un nome.
- **Se si dà il quadrato vuoto o mezzo pieno.** `magic-square.txt` dice che «risolvere quadrati magici parzialmente completati è un passatempo diffuso», e che le tecniche assomigliano a quelle del sudoku.
- **Se i numeri si sommano o si moltiplicano.** Esistono anche i quadrati moltiplicativi, additivo-moltiplicativi, geometrici e di area.

Le due definizioni in casa non coincidono su un punto piccolo e controllabile: `it-quadrato-magico.txt` chiede che i valori siano tutti distinti, `magic-square.txt` ammette quadrati con valori ripetuti e li chiama **banali** — e mette in quella categoria il quadrato della Sagrada Família. Si tiene la seconda, che classifica invece di escludere, e che spiega perché quel quadrato esista.

## Da dove viene

Dalla Cina, e prima di quasi ogni altra cosa in questo capitolo. `magic-square.txt`: il quadrato di ordine tre era noto ai matematici cinesi già nel **190 a.C.**, e serviva alla divinazione e all'astrologia. Il primo quadrato di ordine quattro databile è indiano, del **550 d.C.**, ed è nel *Brhat Samhita* di Varahamihira, dove serve a comporre profumi: sedici sostanze, e la somma di quattro qualsiasi lungo una riga dà sempre il volume totale della miscela, 18.

`luoshu-square.txt` racconta la leggenda: durante una grande inondazione, dal fiume Luo emerse una tartaruga con dei punti sul guscio disposti in una griglia tre per tre. È il **Lo Shu**, l'unico quadrato magico normale di ordine tre in cui l'1 sta in basso e il 2 in alto a destra; ogni altro si ottiene da lui ruotando o riflettendo. Il quadrato è anche pratica: la fonte dice che servì da base per la pianificazione di città, e per la progettazione di tombe e templi. In nota, il dettaglio che lega il numero al calendario: **quindici sono i giorni di ciascuno dei ventiquattro cicli dell'anno solare cinese.**

In Europa arrivano tardi e come oggetti occulti, attraverso la Spagna e l'Italia; `magic-square.txt` osserva che «l'intera teoria dovette essere riscoperta». Il quadrato di Dürer nella *Melencolia I* del **1514** è, secondo `melencolia-i.txt`, **il primo quadrato magico stampato in Europa**. `it-quadrato-magico.txt` chiude la parabola in una riga: «Il secolo dei Lumi relegò progressivamente i quadrati magici al ruolo di oggetti matematici, e infine di curiosità».

**Sulla data di Frénicle de Bessy le due pagine non concordano.** `it-quadrato-magico.txt` lo dà come 1605–1665 e dice che calcolò gli 880 quadrati di ordine quattro nel 1663; `magic-square.txt` dice che la dimostrazione uscì in due trattati postumi nel 1693, «vent'anni dopo la sua morte», il che porterebbe la morte al 1673. Le due date di morte differiscono di otto anni. Si tiene quello che si può controllare — il numero — e la discordanza resta scritta.

## Varianti e parenti

- **Semimagico** — righe e colonne sì, diagonali no.
- **Associativo** — ogni numero più il suo simmetrico rispetto al centro dà n² + 1.
- **Pandiagonale** — anche le diagonali spezzate. Chiamato anche diabolico, o quadrato di Nasik.
- **Bordato** — resta magico togliendo la cornice esterna. Non esiste di ordine quattro.
- **Perfettissimo (most-perfect)** — pandiagonale, e in più ogni 2×2 e ogni coppia a distanza n/2 sulle diagonali.
- **Multimagico** — resta magico elevando tutti i numeri alla k-esima potenza.
- **Alfamagico** — il numero di lettere del nome di ogni numero forma a sua volta un quadrato magico.
- **Voce 154, sudoku e affini (Nikoli)** — il rapporto è discusso qui sotto, perché le fonti non lo raccontano allo stesso modo.
- **Voce 358, zigzag, kakuro, crossnumber** — l'altra griglia in cui le caselle portano cifre e le righe portano somme.
- **Voce 361, crittarismo (alfametica)** — l'altro modo di nascondere numeri in un oggetto che si controlla sommando.

## Che cosa se ne sa

**La costante magica ha una formula, e i due modi di ricavarla concordano.** M = n(n² + 1)/2, che `magic-constant.txt` scrive così e `it-quadrato-magico.txt` ricava come somma di tutti i numeri divisa per il numero delle righe. Per n da 3 a 8 dà 15, 34, 65, 111, 175, 260; la pagina italiana stampa i primi quindici valori, e tornano tutti. Rifatto per le due strade in `build/check_359.py`.

**Gli 880 quadrati di ordine quattro sono stati rienumerati qui.** `build/check_359.py` li conta tutti, senza fidarsi della fonte: sono **7 040** compresi ruotati e riflessi, cioè **880** classi, che è il numero di Frénicle. Per ordine tre l'enumerazione dà 8 quadrati, che sono le otto immagini del Lo Shu — verificato confrontando l'elenco enumerato con le otto simmetrie del Lo Shu, insieme per insieme.

**Le due pagine non danno lo stesso statuto al numero di ordine cinque.** `magic-square.txt` elenca 275 305 224 come il conteggio, nella successione OEIS A006052; `it-quadrato-magico.txt` scrive che i quadrati di ordine cinque «sono **almeno** 275.305.224», limite inferiore calcolato da Richard Schroeppel. Le due pagine danno la stessa cifra con due statuti diversi, e nessuna delle due può essere controllata qui. Si dichiara la differenza e non si sceglie.

**Il fatto più citato sul quadrato di Dürer non è un fatto sul quadrato di Dürer.** `durer-magic-square.txt` afferma che il quadrato ha «86 combinazioni di somma» che danno 34, e le raggruppa in sei figure — 15 + 21 + 12 + 8 + 12 + 18 —, che sommano proprio a 86. Ma le quaterne di numeri fra 1 e 16 che sommano a 34 sono in tutto **86 quaterne**, e restano 86 anche su una griglia riempita in ordine, che non è magica. Contate in `build/check_359.py` su tutte le 1 820 quaterne possibili. **Il numero 86 è una proprietà dell'insieme {1,…,16} e non della disposizione di Dürer**: quello che la disposizione aggiunge è che molte di quelle quaterne cadano in posti geometricamente belli, e le figure della fonte — che nel testo estratto sono sparite — servivano a mostrare proprio quello.

**Quello che invece il quadrato di Dürer fa davvero, controllato.** Righe, colonne, diagonali, i quattro quadranti, le quattro caselle centrali e i quattro angoli danno tutti 34; ogni coppia simmetrica rispetto al centro dà 17; i quadrati degli otto numeri sulle due diagonali sommano a 748 e i cubi a 9 248; le due caselle centrali dell'ultima riga sono 15 e 14, la data dell'incisione, e ai loro lati stanno 4 e 1, che sono le iniziali di Albrecht Dürer nell'alfabeto. Tutto verificato in `build/check_359.py`.

**Sudoku: una discendenza storica e una strutturale, e non sono la stessa affermazione.** La voce 154, sudoku e affini (Nikoli) chiama il quadrato magico «l'antenato diretto», e lo fa su una catena di date primarie — i quadrati magici svuotati dei giornali francesi dal 1892. `magic-square.txt` dice invece che «le griglie del sudoku non sono quadrati magici ma si basano su un'idea imparentata, i quadrati greco-latini», e `recreational-mathematics.txt` che il sudoku è un caso particolare di quadrato latino, di cui la prima forma nota è di Choi Seok-jeong (1646–1715), cioè **prima di Eulero**. Le due affermazioni non si contraddicono: la prima dice da dove è arrivato il gioco in edicola, la seconda che cos'è l'oggetto. La riga della voce 154, sudoku e affini (Nikoli) regge come storia e non come struttura, e conviene leggerla così.

**Dove sta la verifica: dentro il materiale.** Si sommano le righe. È lo stesso gradino della voce 361, crittarismo (alfametica), ed è il motivo per cui le due stanno vicine.

## Esempi trovati

Il Lo Shu, da `luoshu-square.txt`: i quattro numeri pari agli angoli, i cinque dispari a formare una croce, e 15 in ogni direzione.

Il *Chautisa Yantra*, da `magic-square.txt`: inciso nel dodicesimo secolo sul muro del tempio di Parshvanath a Khajuraho. Il nome viene dalla sua somma, 34; è uno dei tre quadrati pandiagonali di ordine quattro ed è anche perfettissimo.

Il quadrato di Varahamihira, c. 550, da `magic-square.txt`: quattro ingredienti su sedici, e la miscela fa sempre 18.

Il quadrato di Dürer, 1514, da `melencolia-i.txt` e `durer-magic-square.txt`: appeso al muro dietro la figura, con la data nascosta nell'ultima riga. È il talismano di Giove, pianeta che secondo la tradizione scaccia la malinconia.

Il quadrato della Sagrada Família, da `magic-square.txt`: costante 33, l'età di Cristo alla Passione. Ha quattro numeri ridotti di uno rispetto a quello di Dürer, quindi ripete dei valori ed è banale nel senso tecnico. Lee Sallows ha osservato che l'errore era evitabile e ha mostrato quadrati non banali con costante 33.

Il quadrato di primi di Rudolf Ondrejka, da `magic-square.txt`: tre per tre, con nove primi di Chen.

## Una nostra versione

> **Il muro dietro la finestra**
>
> Le sedici caselle vogliono i numeri da 1 a 16, uno per casella. Ogni riga, ogni colonna e le due diagonali devono fare 34. Sei numeri sono già lì.
>
> ```
>  +----+----+----+----+
>  | 16 |    |    | 13 |
>  +----+----+----+----+
>  |    | 10 |    |    |
>  +----+----+----+----+
>  |    |    |  7 |    |
>  +----+----+----+----+
>  |  4 |    |    |  1 |
>  +----+----+----+----+
> ```
>
> C'è un modo solo di finirlo. Quando ci sei arrivato, guarda le due caselle in mezzo all'ultima riga e leggile come un numero di quattro cifre: è l'anno in cui questo quadrato è stato inciso su una lastra di rame, a Norimberga.

I sei numeri dati non sono scelti a caso: sono la diagonale principale e i due angoli restanti. `build/check_359.py` filtra tutti i 7 040 quadrati magici di ordine quattro e ne trova **uno solo** che li contiene, e quell'uno è il quadrato di Dürer. La ricompensa non è la conferma che il quadrato torna — quella si ha sommando —, è la data che compare da sola in fondo.

## Da riprendere alla rassegna

**Un oggetto che si controlla da solo e che regala una data.** La forma sta nel formato senza attriti: si stampa una griglia, si scrivono numeri, la verifica è la somma. Quello che la rende una sera invece che un esercizio è la seconda riga della consegna, che chiede di leggere il risultato come una cosa diversa da un risultato.

**Il fatto più famoso su questa forma è una proprietà dei numeri, non della forma.** Le 86 combinazioni di Dürer sono 86 su qualunque disposizione di 1..16. Alla rassegna vale come regola generale: **quando una fonte celebra un numero, si guarda se quel numero dipenda dall'oggetto o dall'insieme da cui l'oggetto è fatto.** È lo stesso errore di prospettiva del vincolo taciuto trovato alla voce 353, cruciverba senza schema, girato al contrario.

**Le figure perdute non sempre si possono ricalcolare, ma qui si può dire perché mancano.** Le sei figure di `durer-magic-square.txt` erano immagini con le caselle evidenziate in verde; nel testo estratto restano i conteggi e le didascalie. Il conteggio si è potuto rifare, il raggruppamento no. È il caso intermedio fra la tabella del kakuro, che si è ricalcolata per intero, e le crittografie di `it-crittografia-gioco.txt`, che non si sono ricostruite affatto.

**Il quadrato parzialmente riempito è il modo in cui la forma diventa un compito.** La fonte lo dichiara passatempo diffuso, e per noi risolve il problema di chi propone: si sceglie il quadrato, si cancellano caselle finché il completamento resta unico, e la risposta è scritta prima della domanda. Lo stesso procedimento vale per ogni forma di questo capitolo che consegni un oggetto da completare.

