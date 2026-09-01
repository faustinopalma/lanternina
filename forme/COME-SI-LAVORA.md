# Come si lavora su `forme/`

Le parti che non cambiano da una sessione all'altra. Il prompt di sessione contiene solo l'obiettivo e quello che è cambiato davvero, e rimanda qui per tutto il resto. Un prompt che riscrive tutto ogni volta perde le trappole vecchie e ne introduce di nuove: è già successo, e nell'ultima sessione dava tre numeri sbagliati per una famiglia intera di voci.

Da leggere insieme a `forme/README.md`, che è il contratto di una voce, e alla voce modello `forme/02-che-cosa-mette-in-moto-la-risposta/054-misurare/README.md`.

---

## 1. Regole di lavoro

- **L'elenco si compila libero.** Non si applica nessuna regola del progetto mentre si scrive: una forma si descrive per quello che è, anche se qui non si userebbe mai. Niente verdetti, niente «chiuso», «vietato», «non ci sta». La rassegna verrà quando l'elenco sarà completo. Se viene da giudicare, lo si scrive in `OSSERVAZIONI.md` come cosa da guardare, non nella voce come decisione.
- **È fatta per essere letta.** Non è una base di dati: una voce deve poter essere aperta da sola e capita da sola. Per questo ogni rimando a un'altra voce porta **il numero e il nome**.
- **Le fonti si citano con il nome del file e la data.** Quando una cosa la si sa e non l'ha letta, si scrive «va verificato». Quando una fonte scaricata non dice niente, lo si dichiara nella voce invece di girarci intorno: è la riga che distingue un'enciclopedia da un ricordo ben scritto. Se due fonti si contraddicono, si dice quale si scarta e perché. **Non si mette nella riga «Fonti» un file che poi non si cita nel corpo**: se è stato letto e non serve, lo si dice con una riga.
- **Non si forzano le osservazioni.** Un blocco può chiudersi con «questo blocco non ha lasciato niente di nuovo», e scriverlo è un esito valido. Tre osservazioni vere valgono più di otto di cui quattro costruite per riempire la sezione.
- **Non si contano le occorrenze a memoria, mai.** Se non si possono elencare le precedenti trovandole in `OSSERVAZIONI.md`, si scrive «ancora una volta» e basta.
- Lo stile è quello di `.github/copilot-instructions.md §2`: dichiarativo, calmo, niente superlativi, numeri con la loro provenienza, i limiti accanto all'affermazione, in Markdown un paragrafo è una riga sola.
- I commit e i push li fa chi lavora, senza chiedere conferma.

## 2. Il contratto ridotto dei capitoli 12, 13 e 14

Le voci dei capitoli 12 (enigmistica classica), 13 (giochi matematici e ricreativi) e 14 (percezione e inganno dell'occhio) hanno un **contratto ridotto: voce breve, dichiarata come tale nell'intestazione.** Differiscono nell'enigma e non nel modo di chiedere, e la profondità piena lì produce riempitivo. Le sette sezioni restano, e restano nell'ordine; quello che cambia è la lunghezza attesa di ognuna.

Si dichiara con la riga `- **Contratto** voce breve`, **subito dopo «In una riga»**. Le righe di intestazione diventano sei, quindi il comando del §8 va lanciato con `-TotalCount 8`. `forme_check.py` non guarda l'intestazione e passa comunque.

**Quando un blocco è fatto di forme che si somigliano, si scrive per primo il termine di paragone** — la voce in cui la variabile del blocco prende il valore più povero — e le altre si descrivono per differenza da lei. La regola ha funzionato dodici volte: voci 287, 298, 300, 310, 314, 321, 323, 328, 335, 341, 346 e 352. **La riga di differenza va stampata dentro ogni voce**, in fondo alla sezione della rassegna, perché chi apre una voce sola non ha in mente le altre. **Povero non vuol dire povera**: la voce in cui la variabile vale meno può essere quella con più cose dentro, ed è successo alla voce 321, antipodo. **E il termine di paragone può essere già scritto**: allora si rilegge contro le fonti nuove *prima* di appoggiarcisi, perché una voce vecchia sbagliata non produce una voce sbagliata, ne produce quattro (voce 341, crittografia pura).

**Un blocco può contenere una voce che sulla variabile non sta, e la si dichiara invece di forzarla.** Nel blocco 328-332 la cerniera apparteneva a un'altra famiglia; scriverlo dentro la voce è costato una riga, e cercare una variabile che le comprendesse tutte e cinque sarebbe costato una voce sbagliata. **E le voci fuori possono essere due nello stesso blocco**: nel 352-358 lo schema libero sta fuori perché il suo vincolo riguarda chi compila, e il kakuro perché cambia l'alfabeto delle caselle invece di quello che il foglio dichiara.

**E un blocco può avere due variabili invece di una, con due termini di paragone.** Il blocco 346-351 si è spezzato in tre voci sulla forma dell'esposto, due sulla posizione della lettera che si legge, e una fuori da tutte e due. Non è un ripiego: sei voci che si somigliano di rado si ordinano su una scala sola. Quello che serve, quando succede, è **una grandezza che le attraversi tutte** anche se la variabile non le ordina — lì era quante posizioni deve provare chi legge e quante ne toglie il foglio —, e una tabella che la stampi.

## 3. Ambiente

- Python nel venv: `.\.venv\Scripts\python.exe`. **Il `python` di sistema non ha né pytest né ruff.**
- Test: `.\.venv\Scripts\python.exe -m pytest tests\test_forme.py -q`. Lint: `.\.venv\Scripts\python.exe -m ruff check .`. Lunghezza riga 100.
- Le fonti scaricate stanno in `_reference/esercizi-e-sfide/`, gitignored. Ogni `.html` ha il suo `.txt` accanto. `SOURCES.md` dice che cosa c'è e quando è stato preso. **Un indirizzo in più non è una fonte in più**: lo script dichiara più indirizzi delle pagine esistenti, e la differenza sono i doppioni e i 404 vecchi.
- Per vedere gli accenti nell'output: `$env:PYTHONUTF8='1'` e `[Console]::OutputEncoding=[Text.Encoding]::UTF8` prima del comando.
- PowerShell: `python -c "..."` su più righe si blocca sul prompt di continuazione. Gli script vanno in `build/` e si lanciano. Niente heredoc: i messaggi di commit vanno in `build/commit-*.txt` e si usano con `git commit -F`, senza lettere accentate.
- `Select-Object Name, @{n='kB';e={...}}` in una pipeline dà output illeggibile. Si usa `ForEach-Object { "{0} {1}" -f $_.Name, $_.Length }`.
- **All'inizio della sessione: `git status --short` e `git log --oneline -3`.** Se un file è modificato e non si sa perché, si guarda il diff prima di scrivere.
- **Dopo ogni modifica a un file lungo: `git diff --numstat`.** Uno strumento di modifica può scrivere sopra una versione anteriore all'ultimo commit e cancellare il lavoro di una sessione intera; è successo a `OSSERVAZIONI.md` — 64 righe tolte in un'operazione che era solo un'aggiunta — e la sola spia è il numero delle righe tolte. Il ripristino è `git checkout -- <file>` e la riscrittura.

## 4. Come si prendono fonti nuove

**Prima di scaricare, tre controlli e non uno.**

1. `build/check_titoli_<n>.py` manda `https://<lang>.wikipedia.org/w/api.php?action=query&format=json&redirects=1&titles=A|B|C…` e stampa per ogni titolo se esista **e dove rimandi**. Quaranta titoli per chiamata. **Serve sempre l'intestazione `{"User-Agent": "lanternina-research/1.0"}`: senza, Wikipedia risponde 403.** Si legge la freccia, non solo il sì.
2. Poi si cerca il nome nello script, con un ciclo solo su tutti i candidati:
   `foreach ($x in $lista) { $m = Select-String -Path tools\fetch_exercise_sources.py -Pattern $x -SimpleMatch; if ($m) { "GIA' $x" } }`
   **Attenzione: questo controllo cerca l'indirizzo**, quindi sbaglia nei due versi. Per difetto non trova una pagina che sta in casa sotto un titolo che rimanda — `Score_(video_games)` non risultava presente perché era stata presa da `Score_(game)`; nella lista vanno messi anche i titoli-rimando noti. Per eccesso segnala presente un titolo che è **sottostringa** di un altro indirizzo — `Permutation` dentro `Riffle_shuffle_permutation` —, e il rimedio è cercare `/wiki/<Titolo>"` con la virgoletta finale invece del titolo nudo.
3. Poi `build/check_fonti_<n>.py` sulle pagine scaricate **e su tutte quelle che si intende citare**: stampa prime tre righe e dimensioni, **e trova i doppioni sul corpo del testo ignorando la riga «Retrieved from»**, che è l'unico modo che funziona.

La ricerca a testo pieno su `https://en.wikipedia.org/w/index.php?search=<parole>&title=Special:Search&fulltext=1` resta utile per un'altra cosa: fa emergere pagine che nessuno cercava e che servono.

Per aggiungere fonti: gli indirizzi vanno in `tools/fetch_exercise_sources.py` (i gruppi in fondo sono i più recenti), si rilancia — salta quelle già prese — e poi `.\.venv\Scripts\python.exe tools\forme_text.py`. **Gli indirizzi con lettere accentate vanno scritti percentuali** (`Serendipit%C3%A0`): un solo accento fa fallire tutto lo scaricamento con `UnicodeEncodeError`. Lo stesso per gli apostrofi (`Conway%27s_Game_of_Life`) e per il trattino lungo (`Dunning%E2%80%93Kruger_effect`).

**Il momento giusto per scegliere le fonti è dopo aver letto la fonte principale, non prima.** Un elenco di candidati costruito sull'ipotesi che si ha sul blocco diventa inutile per metà quando l'ipotesi cambia: nel blocco 346-351, quattordici pagine su ventitré non sono state citate da nessuna voce, ed erano tutte di due famiglie scelte prima di aprire `it-rebus.txt`. Nel blocco 352-358, con l'ordine invertito — prima `it-cruciverba.txt`, poi lo scarico — le pagine citate sono state **otto su otto**. Non è un danno gravissimo — una pagina in casa resta in casa —, ma un secondo scarico corto dopo la prima lettura costa meno di un primo scarico lungo. **Quali pagine di uno scarico siano poi state citate si conta**, e il numero va in `OSSERVAZIONI.md`.

**Un indirizzo sbagliato nello script fallisce in silenzio e resta lì per sempre.** `Bifronte_(enigmistica)` non esiste, il file `it-bifronte.txt` non è mai stato creato, e la voce che ne aveva bisogno ha scritto «nessuna fra le pagine locali» come se fosse una constatazione. **L'unico posto in cui il buco si vede è il conteggio finale dello scaricamento** — `1201/1205` —, e va letto a ogni scarico: un mancante è una riga da guardare, non un residuo.

**Le fonti nominate nel prompt di sessione si controllano prima di citarle.** Un prompt ne ha elencate tre come «già in casa» e nessuna delle tre esisteva con quel nome; `build/check_fonti_<n>.py` le ha prese tutte e tre al primo colpo.

Quando nessuna pagina copre una cosa, la si cerca fuori: `fetch_webpage` su una ricerca e poi sulla pagina vera funziona. **Una fonte primaria fuori da Wikipedia può essere una pagina di vendita**, e allora va presa per quello che è e dichiarata.

## 5. Trappole sulle fonti

- **Un titolo può esistere, non essere un rimando, e riguardare tutt'altro.** `Quitting` è un film cinese del 2001, `Completionist` è un disco, `Notifica` è un atto giuridico, `Scantron` è un'azienda. `Deadline` ed `Endgame` sono disambiguazioni. E un titolo può rimandare a un argomento diverso: `Engine_building` porta alla messa a punto dei motori d'automobile, e `Metanalisi` in italiano porta alla `Meta-analisi` statistica invece che alla risegmentazione linguistica, che sta sotto `Rebracketing`. **Esistenza, freccia e prime righe sono tre controlli diversi e vanno fatti tutti e tre.** **E il titolo sbagliato può proporlo la fonte principale**: `crossword.txt` dà `crusadex` come nome inglese del crucintarsio, e `Crusadex` su Wikipedia porta alle Crociate.
- **Un nome può avere troppi referenti invece che nessuno.** *Zigzag* ha una pagina in italiano che è la linea spezzata della geometria, e come nome di gioco potrebbe indicare almeno tre cose diverse. Quando succede non si sceglie: si elencano i candidati e si dichiara che la riga dell'elenco non ha un referente accertabile.
- **La freccia di un rimando è un'affermazione sul contenuto, e può smentire una voce dell'elenco prima che si scarichi qualcosa.** `Monoverbo` rimanda a `Crittografia (enigmistica)`, e quel rimando dice che il monoverbo non è un gioco ma la crittografia con la soluzione in una parola sola; `Enigma_(enigmistica)` rimanda a `Indovinello`, e quel rimando dice che in italiano le due cose sono la stessa voce. Costa zero e si legge prima dello scarico.
- **Lo stesso indirizzo può stare due volte in `fetch_exercise_sources.py` sotto due nomi**, e il doppione resta in casa per sessioni senza che nessuno lo veda: `lateral-thinking-puzzle.txt` e `situation-puzzle.txt` sono la stessa pagina. Lo trova solo il confronto sul corpo con un hash, che va fatto **anche sulle pagine già in casa** e non solo su quelle appena prese.
- **Il nome di un file locale può essere giusto e la pagina riguardare un'altra disciplina.** `handover.txt` è il passaggio di una chiamata fra due celle telefoniche; `self-monitoring.txt` è il tratto di Mark Snyder; `self-assessment.txt` è la voce sul movente; `peer-tutoring.txt` è *Peer mentoring*; `serialization.txt` è la conversione di strutture dati. **Le prime tre righe vanno lette anche quando il nome è quello che si cercava.**
- **Il controllo dei doppioni per dimensione e prima riga non funziona**: due copie della stessa pagina differiscono di pochi byte. Il confronto va fatto sul corpo, togliendo la riga «Retrieved from», e con un hash.
- **Sotto i due kilobyte e mezzo una pagina è quasi sempre una disambiguazione o un rimando al Wikizionario**, e due nomi diversi possono rimandare alla stessa terza pagina. Vale anche quando il titolo è esattamente quello del concetto cercato: `Interleaving` esiste, non è un rimando, e sono 2 071 byte di elenco. **Ma è una statistica, non un criterio**: `it-cesura-enigmistica.txt` è di 2 474 byte ed è la fonte principale di una voce, con tre esempi datati e due definizioni. La dimensione dice dove guardare per prime; le prime tre righe restano l'unico controllo.
- **Le figure e i riquadri di una pagina non arrivano nel testo estratto, e con loro se ne vanno gli esempi.** `it-crittografia-gioco.txt` propone sette crittografie e ne restano solo le soluzioni in nota. **Quando le note spiegano qualcosa che nel testo non c'è, il pezzo mancante è una figura**: si dichiara, non si ricostruisce a naso. **Ma se la figura è una tabella calcolabile, si ricalcola**: `it-kakuro.txt` perde la tabella delle combinazioni uniche e conserva l'affermazione generale, che è bastata a rifarla per intero.
- **Una fonte può enunciare al rovescio la condizione che rende risolvibile il gioco che descrive.** `it-cruciverba.txt` sul crittografato scrive che «non esiste il caso che una lettera sia presente in due caselle diverse», che è falso: intende che due numeri non valgono la stessa lettera. Non è una contraddizione fra fonti — è una frase mal costruita là dove la costruzione è il contenuto. Si tiene la formulazione controllabile e si dichiara l'altra.
- **Lo stesso vale per l'incolonnamento: una proprietà che sta nella disposizione non sopravvive all'estrazione.** `it-telestico.txt` attribuisce a cinque esametri di Folengo di essere insieme acrostici, mesostici e telestici; le iniziali e le finali si ricontano, il mesostico no, perché gli spazi interni sono stati normalizzati. Si dichiara che non è verificabile.
- **Una pagina di pochi kB su una pratica famosa può non contenere nessuna misura.** Si dichiara e si va avanti. **Una pagina enorme con un nome promettente può essere un glossario**: la dimensione non dice niente sull'utilità.
- **Alcune fonti hanno in cima un navbox o un blocco di codice della citazione, e non il testo.** Si cerca con grep prima di concludere che la fonte è vuota.
- **Prima di dire che una fonte non dice una cosa la si cerca con grep in tutto il file.**
- **Le affermazioni più forti di una pagina sono spesso le meno sostenute**, e più una fonte dice quello che si sperava, più conviene guardare la nota.
- **Una fonte presa perché risolve un problema va letta fino alla restrizione, non solo fino all'aggiunta.** La distanza di Damerau–Levenshtein aggiunge la trasposizione alle tre operazioni di Levenshtein, ma **solo fra caratteri adiacenti**: bastava quella parola per ribaltare la conclusione di un blocco intero.
- **Il limite che rende ambiguo un numero può stare nella stessa pagina, due righe più sotto**, e non in nota. Chi si ferma alla prima frase porta a casa una misura che non c'è.
- **Una fonte italiana può non avere l'avviso in cima ed essere scritta in registro promozionale.** La mancanza di note sotto le affermazioni forti è un segnale più affidabile dell'avviso in cima.

Lettura: la ricerca testuale nel workspace salta le cartelle gitignored, quindi per i `.txt` serve `includeIgnoredFiles`; `read_file` con percorso assoluto funziona ed è il modo più veloce, tre o quattro in parallelo. **Per una fonte da 40 kB o più conviene prima un `grep_search` con `^## |^### ` e poi un `read_file` sulle righe che servono.**

## 6. Trappole sui numeri

- **Le fonti danno spesso la direzione e non la grandezza.** A volte il numero c'è e manca il verso della causa.
- **Un numero può essere fabbricato e circolare lo stesso** (lo studio di Harvard sugli obiettivi scritti, accertato inesistente da *Fast Company* nel 1996).
- **Un numero può dipendere da una convenzione che la fonte non dichiara**, e allora anche la direzione dell'effetto può essere sbagliata — e succede anche nelle specifiche tecniche. **E due numeri veri della stessa pagina possono venire da convenzioni diverse**: il «25% di probabilità» (quattro alternative) accostato alla penalità di 1/4 (calibrata su cinque). **Il rimedio: cercare la grandezza che non dipende dalla convenzione.**
- **Un aggettivo o un arrotondamento della fonte può essere smentito dai numeri della fonte stessa.** «Costantemente in aumento» per un 9,03% l'anno seguito da un 1,44%; «dopo sei mesi» per 165 giorni. Quando una fonte qualifica un andamento o arrotonda un intervallo, si ricalcola.
- **Una fonte può sommare i valori già arrotondati** e dichiarare il totale come esatto. Si rifà, e si dice anche se il risultato finale non cambia.
- **Una pagina può dare due volte la stessa stima con estremi diversi.** Si tiene l'intervallo più largo e si dichiara l'incoerenza.
- **Un testo estratto può arrivare mutilo nel punto esatto in cui serve.** Un numero che arriva senza uno dei suoi estremi non è un numero: non si usa, e si dice perché. **Nelle pagine tecniche l'estrazione perde le formule LaTeX**, e le complessità arrivano come «time using» senza l'espressione: quando una frase finisce senza il suo numero, non è un refuso della fonte, è l'estrattore.
- **Una percentuale senza un termine di paragone non dice niente.** **Una riduzione relativa non dice quante persone**, e per delimitarla bisogna aggiungere un'ipotesi che va dichiarata propria. **Una misura di accordo senza la tolleranza dichiarata non dice niente.**
- **Una percentuale senza intervallo di confidenza va corredata**, e quando manca n l'intervallo si può solo delimitare — e lo si calcola. **Un ± con tre decimali implica una dimensione campionaria che si può ricavare.**
- **Un numero preciso su un'associazione non è più forte di una direzione su un esperimento.**
- **L'effetto condizionato all'adesione non è l'effetto**, e a volte le porte sono più di due, in serie. Da fare ogni volta che una letteratura misura chi ha superato un filtro invece di chi è entrato.
- **Quando una fonte afferma un numero che è conseguenza di regole scritte nella fonte stessa, si rifà simulando o risolvendo. Rifare batte confrontare.**
- **Quando una fonte dichiara che un effetto è la somma di due cause e non le compone, comporle decide chi ha ragione.**
- **Quando un modello dice «la strategia ottima prevede X», si guarda quale giocatore vincola.**
- **Due fonti si possono contraddire su un effetto, e vince quella che aggrega.** Ma **due letterature che si contraddicono possono misurare popolazioni diverse**, e allora la contraddizione è apparente e il confine va scritto. **E due fonti in casa possono contraddirsi su una definizione**: si tiene quella che produce una classificazione controllabile, e si scrive nella voce che l'altra dice il contrario. Se una delle due si qualifica da sé — «in un'accezione più stretta» — non si scarta niente, perché la contraddizione è apparente.
- **Due pagine che danno lo stesso numero con lo stesso autore non sono due conferme.**
- **Un fatto può vivere soltanto nel titolo di una nota bibliografica. Non si copia: si rifà.**
- **Un conteggio senza l'elenco che lo produce non è verificabile.** Si stampa sempre l'elenco per esteso, non solo il totale. **E il numero più alto di una lista numerata non è il numero degli elementi** quando due liste condividono la numerazione: lo schema libero di `it-cruciverba.txt` arriva a 68 e ha 79 definizioni. **Attenzione anche all'àncora della regex**: `^` senza `\s*` perde il primo elemento della lista, e uno su trentasette non si vede in nessun modo se non stampando l'elenco.

## 7. Trappole sugli script e sui blocchi stampati

- **Se in un esempio ci sono numeri o una griglia, si scrive uno script che li verifica.** Rileggere non basta, ed è dimostrato molte volte. Gli script stanno in `build/`, gitignored, e si riusano.
- **Un secondo metodo di conteggio si sceglie perché è diverso, non perché è più lungo.** Hanno funzionato: formula e enumerazione completa; probabilità per formula e per enumerazione; DP e linearità dell'attesa; polinomi generatori; inclusione-esclusione; binomiale esatta e normale con correzione di continuità; forma chiusa e simulazione; prodotto diretto e complemento; scansione e somma delle classi.
- **E la stessa idea scritta con un'altra sintassi non è un secondo metodo.** Un `math.prod` e un ciclo che moltiplica sono lo stesso conto. Quando lo spazio è troppo grande per enumerarlo tutto, si enumera un troncamento — le prime quattro righe invece di sette — e si confronta con la formula ristretta allo stesso troncamento.
- **Le asserzioni si scrivono sulla relazione fra due grandezze, non sul valore di una**: sopravvivono a un cambio di esempio.
- **Un'asserzione al bordo di un intervallo fallisce sul caso di parità, ed è un bene.** **Un'asserzione scritta per stupire fallisce su un dato vero.**
- **Il tetto della riga va messo nell'asserzione prima di scrivere il testo del blocco.** È la trappola più ricorrente di tutte, e la rilettura non la prende mai.
- **Quando si modella un errore umano, il modello deve poter produrre gli stessi oggetti che produce la mano**: niente divisione intera dove una persona scriverebbe una frazione.
- **Un enigma inventato per un esempio va risolto prima di dichiararlo unico.** Non si scrive «una sola risposta» senza averle contate. **E quando le soluzioni sono due, il fatto vale più dell'esempio forzato a una**: la cornice di quattro parole della voce 355, crucintarsio ne ha due, l'una la trasposta dell'altra, ed è esattamente la ragione per cui in quei giochi una parola viene regalata.
- **Una funzione che «trova» un oggetto dentro uno spazio va scritta perché li trovi tutti**, e poi si filtra. La prima risposta non è la risposta: cercando la prima parola di un intarsio dentro il totale, la prima lettura valida non era quella della fonte, e la fonte non era in errore — erano due letture entrambe valide.
- **Il conto delle maschere e il conto degli oggetti distinti divergono** ogni volta che i pezzi hanno simboli in comune: ventun modi di intrecciare *sano* e *ponte* danno diciotto stringhe. La differenza va misurata, non assunta uguale a zero.
- **Un vocabolario ricavato dalle pagine scaricate serve a cercare, non a contare.** Le pagine italiane in casa danno quasi trentamila stringhe di lettere, con dentro nomi propri, parole inglesi e frammenti: come strumento di ricerca funziona — ha ritrovato da solo l'esempio di una fonte —, ma un conteggio fatto sopra non è stampabile, perché andrebbe elencato e la maggior parte delle righe non sono parole.
- **Una costante presa dal codice non si ricopia: si legge**, con una regex, così che un cambiamento nel codice faccia fallire lo script invece di smentire la voce in silenzio.
- **Una controprova scritta a mano dentro uno script è una controprova finta.** Quando due metodi discordano, il primo sospettato è quello scritto per ultimo, e il secondo è il dominio.
- **Uno strumento di controllo può essere incompleto e dire di sì.** Quando un controllo segnala un falso allarme, la prima cosa da guardare è il controllo.
- **L'accordo fra due varianti dello stesso strumento non ne misura la precisione.** Due impostazioni dello stesso classificatore concordavano al 78,6% e prendevano il 10% e il 25% contro una lettura a mano: due versioni della stessa idea sbagliata sbagliano insieme. Per misurare uno strumento serve un secondo lettore, non una seconda impostazione, e il campione va scelto **prima** di guardare che cosa dica lo strumento.
- **Una classe definita da un'assenza non ha spie di testo.** Un classificatore a parole chiave la fa sparire — 1,6% contro il 36% letto a mano. Il rimedio non è aggiungere spie: è porre la domanda in due tempi, prima se la cosa esista e poi dove stia.
- **Una frase di commento accanto a un numero giusto non è controllata da niente.** Un'asserzione va messa anche sotto la parte in prosa: una spiegazione sbagliata accanto a un dato corretto sopravvive a qualunque rilettura.
- **E vale anche per i numeri scritti in prosa fuori dai blocchi.** Un conteggio corretto dentro il blocco può essere ricopiato sbagliato nel paragrafo accanto — 36 caratteri diventati 35 — e nessuno strumento lo prende. Il rimedio è una funzione che rilegge la voce e cerca la **frase esatta** con dentro il numero calcolato, non il numero da solo, che comparirebbe ovunque.
- **I blocchi stampati si generano con uno script e si incolla l'output**, e lo script verifica da sé che le colonne coincidano. **La larghezza di una colonna si prende sul massimo fra intestazione e ogni riga di dati, più due.** **E lo script rilegge la voce e asserisce che il blocco ci compaia tale e quale**: senza quella riga, un blocco ritoccato a mano dopo l'incollatura non lo prende nessuno. **L'asserzione deve provare due forme, il blocco nudo e il blocco con `> ` davanti**, perché dentro «Una nostra versione» i blocchi stanno quasi sempre dentro una citazione.
- **Le tabelle non si scrivono a mano nemmeno dentro lo script.** Si tengono come liste di celle e le si impagina con una funzione che calcola le larghezze; il controllo di allineamento serve solo a provare che nessuno le abbia ritoccate dopo. Scritte a mano falliscono il controllo a ogni giro e si finisce per aggiustare il controllo invece della tabella.
- **Un controllo di allineamento si può sbagliare in due modi e nessuno dei due si vede.** Cercare ogni non-spazio preceduto da uno spazio conta le parole dentro una cella come colonne; cercare l'inizio della corsa di spazi invece della sua fine confronta posizioni che dipendono dalla lunghezza del contenuto. La colonna comincia alla **fine** della corsa di due o più spazi.
- **Ma una colonna allineata a destra non comincia da nessuna parte: finisce.** Se l'etichetta dell'intestazione è più stretta del dato più largo, dedurre i confini dall'intestazione taglia le prime cifre di ogni numero — `39 070 080` letto come `9 070 080` — e l'errore è silenzioso. Il controllo che vale spezza ogni riga sulle corse di due o più spazi e poi asserisce **l'inizio** per le colonne a sinistra e **la fine** per quelle a destra. La regex che spezza vuole l'opzionale pigro (`\S(?:.*?\S)??(?=\s\s|$)`): con l'opzionale goloso una cella di un carattere si mangia la successiva.
- **Una sostituzione il cui testo nuovo differisce dal vecchio solo per un a capo lo cancella e basta.** Uno script è morto con un errore di sintassi alla riga successiva. Si rilancia dopo ogni modifica, anche dopo quelle che sembravano non farne nessuna.
- **L'allineamento si controlla con due strumenti**: `build/check_colonne.py <numero>` guarda solo i blocchi con barre verticali, `build/check_stacchi.py <numero>` stampa lunghezza di ogni riga e posizione di ogni stacco. Nessuno dei due sostituisce l'asserzione dentro `blocco_<numero>.py`. Quando le etichette hanno lunghezze diverse, `check_stacchi.py` segnala «forme di riga distinte» anche se le colonne sono incolonnate.
- **`show_blocks.py` toglie gli spazi in testa alla riga**, quindi non serve a controllare l'allineamento.
- **Dentro i blocchi di codice si usano solo caratteri di larghezza uno**, e non lettere accentate: «e» per «è», «piu» per «più», «da'» per «dà». Fuori dai blocchi si scrivono normalmente.
- **`create_file` fallisce su un file che esiste già**, anche in `build/`.
- **Dentro una f-string non si mette un apostrofo dentro un campo quotato con apostrofi.**
- **Le spie di un controllo per parola intera devono elencare le forme flesse**, e un controllo che non trova la spia deve fallire, non scegliere a caso.
- **Non si usa `.Replace()` di PowerShell su tutto il testo di un file.** Si sostituisce il blocco intero con lo strumento di sostituzione, e dopo ogni aggiustamento si lancia `git diff --stat`. **Dopo una sostituzione che tocca un elenco puntato, si rilegge l'elenco.**

## 8. Trappole sulla struttura delle voci

- **Non si ricordano i nomi delle voci: si controllano.** `Select-String -Path docs\EXERCISE-FORMS.md -Pattern '^(N|M|…)\. '` prende venti nomi in un colpo. **Il prompt è la fonte meno verificata del repository.**
- **La glossa dell'elenco non è una fonte.** `docs/EXERCISE-FORMS.md` si consulta per i **nomi** delle voci e per i confini fra i capitoli, non per le definizioni: nel blocco 318-322 due glosse su cinque erano sbagliate, una perché si fermava al passo intermedio e una perché non corrispondeva a nessuna delle due discipline che nominava. Quando una glossa e le fonti divergono, lo si scrive nella voce.
- **E una glossa può essere sbagliata due volte nella stessa riga.** La voce 347 dice «due vignette» dove la fonte dice «due o più scene», e «la lettura passa dall'una all'altra» dove la fonte dice che si legge il rapporto temporale fra loro: il primo errore è un numero, il secondo è il meccanismo. Si legge la glossa fino in fondo contro la fonte, non solo la prima metà.
- **E l'esempio di una glossa può appartenere a un altro gioco anche quando la definizione è giusta.** `A B C = alfabeto muto` non è una crittografia pura; la voce 341 ci aveva costruito sopra tutto il resto. **Un esempio non controllato costa più di una definizione non controllata**, perché una definizione la si confronta con la fonte mentre un esempio si moltiplica.
- **Non si ricordano i confini fra i capitoli: si controllano**, con `Select-String -Path docs\EXERCISE-FORMS.md -Pattern '^## '`.
- **Gli stub esistono già: `create_file` fallisce.** Si sostituisce lo stub **intero**, dall'intestazione all'ultima sezione, in un colpo solo — sostituire solo la testa lascia in fondo le sei sezioni vuote, e `forme_check.py` dice soltanto «le sezioni non sono quelle previste, nell'ordine previsto».
- **Ma una cartella del blocco può contenere una voce già scritta**, perché qualche voce è stata fatta fuori ordine nelle prime sessioni. All'inizio del blocco si legge la riga «Stato della ricerca» di ogni cartella:
  `foreach ($n in 323,324,325) { $p=(Get-ChildItem "forme\12-enigmistica-classica\$n-*\README.md").FullName; "$n : " + (Select-String -Path $p -Pattern '^\- \*\*Stato della ricerca\*\*').Line }`
  Una voce già fatta si **amplia**, non si riscrive, e mantiene la sua data con l'aggiunta di quella nuova.
- **I «parenti» nominati dalle voci vicine si rileggono quando si scrive un blocco.** Una fonte presa oggi controlla una frase scritta due giorni fa: la voce 326 dava la cerniera con la parte comune «in mezzo a entrambe», che è il biscarto centrale. Gli elenchi puntati dei parenti sono il posto dove le voci vecchie accumulano affermazioni che nessuno ha verificato.
- **Ma sostituire lo stub intero non protegge l'intestazione.** L'ordine giusto è **Numero, Si chiama anche, In una riga, Fonti, Stato della ricerca**, una riga per ognuna, e nessuno strumento lo verifica. Il comando, da lanciare **dopo ogni voce**:
  `foreach ($n in 312,313) { $p=(Get-ChildItem "forme\12-enigmistica-classica\$n-*\README.md").FullName; "$n : " + (((Get-Content $p -TotalCount 7) | Select-String '^\- \*\*(\w[^*]*)\*\*' | ForEach-Object { $_.Matches[0].Groups[1].Value }) -join ' | ') + "   sezioni: " + (Select-String -Path $p -Pattern '^## ').Count }`
  Sette sezioni vanno bene, tredici vogliono dire che lo stub è ancora là sotto. **Il nome della cartella del capitolo si controlla con `Get-ChildItem forme\`, non si indovina.**
- **`forme_check.py` controlla anche l'ordine delle sette sezioni** e il messaggio non dice quale sia fuori posto. L'ordine è: Che cos'è, Da dove viene, Varianti e parenti, Che cosa se ne sa, Esempi trovati, Una nostra versione, Da riprendere alla rassegna.
- **`forme_check.py` vuole il nome dopo il numero anche dopo un due punti**: accetta solo virgola, trattino lungo o parentesi aperta. Vale anche per un rimando a sé stessi — dentro la voce 306 si scrive «questa scheda».
- **`build/check_refs.py` cerca «voce N, nome» e non vede «voci N, nome».** Si scrive sempre al singolare e si ripete «voce» per ognuno, e non si incatenano più rimandi nella stessa frase senza un punto in mezzo: la regex è golosa. **Si lancia dopo ogni due voci**, e si guardano solo le righe nuove; le segnalazioni vecchie sono note. `build/check_refs_oss.py` fa lo stesso su `OSSERVAZIONI.md`.
- **Quando il nome dell'elenco contiene una parentesi o una barra, va ricopiato**: «voce 258, distintivi / badge», «voce 260, serie di giorni (streak)», «voce 22, diario / registro».
- **Lo sbaglio più difficile da vedere è quello in cui il nome inventato descrive bene la cosa.** Solo `check_refs.py` lo prende.
- **`--retemplate` riscrive solo gli stub ancora vuoti**; le voci già scritte non le tocca.

## 9. Vincoli del progetto, che restano veri

Il progetto stampa fogli A4 in bianco e nero, mostra quattro righe da 44 caratteri su un display e-paper, e legge una fotografia di un foglio. Niente audio, niente rete in mano, una persona sola. Questo serve a scrivere la sezione «Una nostra versione»: l'esempio va provato contro questi limiti, e dove la forma non ci sta l'esempio la mostra comunque nella sua versione migliore e la voce dice dove si romperebbe.

Il sistema **non sa manipolare le lettere dentro le parole** (misurato, `ideas/10 §6`), **non misura il tempo**, **non sa dove si trova chi legge**, **non registra nulla su nessuno**, **non può impedire niente**, e **ha una persona sola**.

**Tre criteri decidono se una forma sta nel formato, e vanno usati su ogni voce.** Il primo: un contatore che conta **eventi** sta dentro un foglio; uno che conta **minuti** no. Il secondo: una forma che **registra** sta su carta; una forma che **vieta** ha bisogno di qualcuno che vieti. Il terzo, che spiega gli altri due: **una forma sta nel formato quando la verifica è dentro il materiale.** Chiedersi quale sia il limite dominante prima di scrivere ogni voce fa risparmiare mezza voce ogni volta.

**Le regole di disegno del progetto non esistono al momento**: sono state tolte apposta perché la ricerca non nasca già filtrata, e `docs/NON-GOALS.md` è deliberatamente vuoto. Qualche voce vecchia e qualche commento nel codice contengono ancora verdetti di quell'epoca — la voce 22, diario / registro dice che una cosa «è nominata fra le cose vietate», e `panel/drafts.py` e `panel/routes/draft.py` rimandano a `docs/NON-GOALS.md` come se contenesse ancora qualcosa. Non si ripetono e non si estendono; se se ne trovano altri, si annotano in `OSSERVAZIONI.md`.

## 10. Verifica, prima di ogni commit

- `.\.venv\Scripts\python.exe tools\forme_check.py` deve dire 0. Se dice qualcosa, quella cosa è vera.
- `.\.venv\Scripts\python.exe -m pytest tests\test_forme.py -q` deve passare.
- `.\.venv\Scripts\python.exe -m ruff check .` pulito.
- `.\.venv\Scripts\python.exe build\check_refs.py` dopo ogni due voci, e prima del commit.
- `check_colonne.py` **e** `check_stacchi.py` su ogni voce che stampi una griglia.
- `build/check_fonti_citate_<n>.py` su ogni blocco: estrae i nomi di file dalla riga «Fonti» e controlla che ognuno ricompaia nel corpo. Serve a rispettare la regola del §1, ma soprattutto scopre una fonte letta e non sfruttata.
- L'ordine e l'unicità delle cinque righe di intestazione, con il comando del §8, **dopo ogni voce**.
- Uno script di verifica in `build/` per ogni numero stampato, e un secondo metodo quando il conteggio non è banale.
- `.\.venv\Scripts\python.exe tools\forme_scaffold.py --index` rigenerato prima del commit, e `build/conta_capitoli.py` **dopo** di quello.

## 11. Strumenti

In `tools/`: `forme_scaffold.py` (albero e indice, `--index`, `--retemplate`), `forme_check.py` (il controllo), `fetch_exercise_sources.py`, `forme_text.py`. In `tests/`: `test_forme.py`, che è lo stesso controllo dentro la suite.

In `build/`, gitignored e buttabili: `check_refs.py` e `check_refs_oss.py` (i rimandi), `check_colonne.py` e `check_stacchi.py` (le griglie), `conta_capitoli.py` (i conteggi per capitolo), `check_fonti_<n>.py` (prime righe, dimensioni e doppioni sul corpo), `check_titoli_<n>.py` (titoli e rimandi su Wikipedia, con lo `User-Agent`), e la serie `check_<n>.py` e `blocco_<n>.py` con i conti e i blocchi di ogni voce.
