# Nonogramma / picross

- **Numero** 155 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi logici»
- **Si chiama anche** hanjie, griddler, pic-a-pix, picross, paint by numbers, oekaki-logic, illustlogic, crosspix, figurepic, starpic, e in italiano «logimmagini»
- **In una riga** disegnare per numeri.
- **Fonti** `nonogram.txt` e `logic-puzzle.txt`, prese il 30 agosto 2026 da en.wikipedia; il nonogramma della nostra versione è costruito e verificato da noi
- **Stato della ricerca** fatta, 30 agosto 2026

## Che cos'è

Una griglia vuota con dei numeri lungo i bordi. I numeri dicono quanti quadretti pieni ci sono di fila in ogni riga e in ogni colonna, in quell'ordine, con almeno un quadretto vuoto fra un gruppo e il successivo. Riempiendo i quadretti giusti compare un disegno.

Come la voce 154, sudoku e affini (Nikoli), questa è una griglia senza lingua: si consegna identica ovunque. La differenza fra le due è il risultato. **Nel sudoku quello che si ottiene alla fine è la griglia stessa; qui la griglia è il mezzo e quello che si ottiene è un'immagine**, che non serve a risolvere. Rispetto alla voce 142, puzzle a griglia (chi beve cosa, chi vive dove) il confine è lo stesso della voce precedente: là ci sono le parole, qui non ce ne sono affatto.

La fonte dà anche il nome tecnico di quello che sono i numeri, e vale la pena tenerlo: **una forma di tomografia discreta**, cioè la ricostruzione di un oggetto a partire da misure prese lungo delle rette. È la stessa idea che sta dietro a una tomografia medica, in bianco e nero e su venticinque quadretti.

Parti mobili:

- **La dimensione.** La fonte è esplicita: non ci sono limiti teorici, e la griglia non deve essere quadrata.
- **I colori.** In bianco e nero i numeri dicono solo le lunghezze; a colori i numeri sono colorati, e allora **fra due gruppi di colore diverso lo spazio può esserci o non esserci**, il che rende il gioco molto più difficile.
- **Se il disegno si riconosce.** È la parte mobile che l'enciclopedia non si aspetterebbe, e la fonte la tratta come un difetto: vedi sotto.
- **Se si può tirare a indovinare.** Si può, e la fonte spiega perché conviene non farlo.

## Da dove viene

Ha due inventori indipendenti e un anno: **1987**.

**Non Ishida**, redattrice grafica giapponese, vinse un concorso a Tokyo disegnando immagini a griglia **accendendo e spegnendo le luci dei grattacieli**. Da lì le venne l'idea di un gioco basato sul riempire certe caselle di una griglia. Nello stesso periodo, e per coincidenza, un enigmista professionista giapponese, **Tetsuya Nishio**, inventò lo stesso gioco per conto suo e lo pubblicò su un'altra rivista. All'epoca si chiamavano «giochi logici che formano un'immagine».

Nel **1988** Ishida ne pubblica tre in Giappone con il nome *Window Art Puzzles*, e li mostra a **James Dalgety**, collezionista di rompicapi britannico, che si offre di pubblicarli nel mondo. **Il nome «nonogramma» è di Dalgety**, ed è un incrocio: *Non*, dal nome dell'inventrice, e *gram*, da diagramma.

Dal **1990** escono settimanalmente sul *Sunday Telegraph*; nel **1993** esce il primo libro. Nel **1998** il *Sunday Telegraph* indice un concorso fra i lettori per ribattezzarli, e vince *Griddlers*. Nintendo registra il marchio **Picross** — abbreviazione di *picture crossword* — e pubblica due titoli per Game Boy e nove per Super Famicom; fuori dal Giappone ne esce uno solo, *Mario's Picross*.

**Il nome del gioco è il nome di una persona, con la desinenza di un oggetto scientifico attaccata dietro da un terzo che non l'aveva inventato.** È l'unica forma dell'elenco con questa origine.

## Varianti e parenti

- **A colori** — i numeri sono colorati e la regola dello spazio cambia.
- **Non quadrate** — la fonte dice che non c'è nessun vincolo di forma.
- **Con più immagini sovrapposte**, e le altre varianti che le riviste hanno inventato in trent'anni sotto nomi diversi: CrossPix, Descarte's Enigma, FigurePic, Oekaki-Logic, PictureLogic, StarPic.
- **Voce 154, sudoku e affini (Nikoli)** — la griglia gemella, e la differenza è che là non esce nessuna immagine.
- **Voce 142, puzzle a griglia (chi beve cosa, chi vive dove)** — la stessa famiglia secondo `logic-puzzle.txt`, che li elenca insieme; il confine è la lingua.
- **Voce 128, crucipuzzle (word search)** — l'altra griglia in cui si annerisce qualcosa, con le lettere.
- **Voce 131, codice a numeri (A=1)** — l'altra forma dell'elenco in cui dei numeri stampati si traducono in qualcosa da vedere.

Con il capitolo 12, giochi di parole e enigmistica italiana non c'è confine: non ci sono lettere. Con il capitolo 13, giochi matematici e ricreativi nemmeno, e vale la pena dirlo perché sembrerebbe di sì: **il nonogramma non chiede nessuna idea matematica.** La regola di partenza che si vedrà più avanti è un conto di sottrazioni, e la tomografia discreta è il nome che i matematici danno alla cosa, non un'idea che serva a chi risolve.

## Che cosa se ne sa

**Decidere se un nonogramma abbia una soluzione è NP-completo**, e costruirne una — o dimostrare che non esiste — è NP-difficile. Quindi non c'è nessun algoritmo che risolva tutti i nonogrammi in tempo polinomiale, a meno che P non sia uguale a NP. **Certe classi si risolvono in fretta**: per esempio quelle in cui ogni riga e ogni colonna hanno un solo gruppo e tutte le caselle piene sono collegate, che si riducono a un problema di 2-soddisfacibilità.

**C'è una regola di partenza che funziona sempre e che si applica senza pensare.** La fonte la chiama «approccio matematico» ed è questa: si sommano gli indizi di una riga, più uno per ogni spazio obbligatorio fra di loro; si sottrae il risultato dalla larghezza della riga; **ogni indizio più grande di quel resto ha delle caselle certe, e sono tante quante l'indizio meno il resto.** Si trovano spingendo i gruppi tutti da un lato, contando, e tornando indietro del numero ottenuto — e viene lo stesso partendo da destra o da sinistra. **È la seconda volta in questo blocco che una forma ha una regola meccanica che dà un punto di partenza garantito**, dopo la voce 153, problema di ottimizzazione.

**Indovinare è la cosa che rompe tutto, e la fonte spiega esattamente come.** «Se si tira a indovinare, un solo errore può propagarsi su tutto il campo e rovinare completamente la soluzione. A volte un errore viene a galla solo dopo un po', quando è molto difficile correggere il gioco.» **Non è un consiglio di stile: è la descrizione di un guasto irreversibile a metà strada**, ed è la quarta forma dell'elenco che fallisce in silenzio dopo quelle già raccolte alle voci 113, 128 e 144.

**Il disegno non serve a risolvere, e può ingannare.** La riga della fonte è netta: «l'immagine nascosta può aiutare a individuare e a eliminare un errore, ma per il resto gioca un ruolo minimo nel processo di soluzione, perché può fuorviare.» **Questa è l'osservazione più utile della voce e va contro l'intuizione**: il disegno è il premio, non il metodo, e riconoscerlo a metà strada porta a riempire quello che ci si aspetta invece di quello che i numeri dicono. Ne segue una conseguenza per la consegna: **non si deve dire che cosa uscirà.**

**C'è una tecnica per i casi difficili che si chiama contraddizione, e assomiglia a una dimostrazione.** Si prova a mettere una casella piena, si tirano tutte le conseguenze, e se si arriva a un errore allora quella casella era vuota. La fonte dice anche il difetto del metodo: **non c'è un modo rapido di sapere quale casella provare**, e la maggior parte porta a un vicolo cieco. Suggerisce di partire da quelle con molti vicini già decisi, vicine ai bordi, o in righe già molto piene.

**La ricorsione più profonda, dice la fonte, non è praticabile con carta e matita** ed è pratica solo per un calcolatore. È una delle poche volte in cui una pagina di rompicapi traccia esplicitamente il confine fra quello che si fa a mano e quello che no.

**Nessuna misura su chi risolve.** Non c'è, nelle pagine lette, nessun dato su tempi, età, difficoltà percepita. C'è invece una storia editoriale dettagliata, che è il rovescio della situazione di quasi tutte le altre voci del capitolo.

## Esempi trovati

Dal concorso di Tokyo del 1987: un'immagine a griglia composta accendendo e spegnendo le finestre di un grattacielo. **È un nonogramma alto cinquanta piani, e non era un gioco: era una gara di grafica.**

Dal *Sunday Telegraph*, 1990: la pubblicazione settimanale che li porta in Europa.

Dal concorso di rinomina del 1998: *Griddlers*, scelto dai lettori.

Da Nintendo: *Picross*, cioè *picture crossword*, marchio registrato per un gioco che con il cruciverba non ha niente in comune se non la griglia.

Da *Pictopix*, 2017: un gioco per calcolatore la cui caratteristica segnalata dalla fonte è che **permette ai giocatori di condividere le proprie creazioni.** Anche qui, come in mezzo elenco, la forma diventa interessante quando si passa dalla parte di chi costruisce.

Dalla fonte, un indizio letto per esteso: «4 8 3» vuol dire un gruppo di quattro caselle piene, poi almeno una vuota, poi otto, poi almeno una vuota, poi tre.

## Una nostra versione

Un nonogramma va stampato giusto, e i suoi numeri vanno verificati uno per uno. Questo è cinque per cinque, ha una soluzione sola, e i conti sono stati fatti a mano.

> **Venticinque quadretti**
>
> I numeri dicono **quanti quadretti pieni ci sono di fila**, in quell'ordine, con **almeno un quadretto vuoto** fra un gruppo e il successivo. I numeri di sinistra valgono per le righe, quelli in alto per le colonne.
>
> ```
>                  2       2
>              3   1   5   1   3
>            ┌───┬───┬───┬───┬───┐
>         1  │   │   │   │   │   │
>            ├───┼───┼───┼───┼───┤
>         3  │   │   │   │   │   │
>            ├───┼───┼───┼───┼───┤
>         5  │   │   │   │   │   │
>            ├───┼───┼───┼───┼───┤
>     1 1 1  │   │   │   │   │   │
>            ├───┼───┼───┼───┼───┤
>         5  │   │   │   │   │   │
>            └───┴───┴───┴───┴───┘
> ```
>
> **Non ti dico che cosa viene fuori.** Non è per farti un dispetto: è che sapere che cosa aspettarsi fa riempire quello che ci si aspetta invece di quello che i numeri dicono, e da lì non si torna indietro.
>
> **Da dove cominciare, senza tirare a indovinare.** C'è un conto che dà sempre delle caselle certe, e si fa una riga per volta:
>
> ```
>  1. somma i numeri della riga, piu' 1 per ogni
>     spazio obbligatorio fra un numero e l'altro;
>  2. sottrai il totale dalla larghezza della riga
>     (qui, da 5);
>  3. ogni numero PIU' GRANDE del resto ha delle
>     caselle certe: tante quante il numero meno
>     il resto;
>  4. per trovarle: spingi i gruppi tutti a sinistra,
>     poi tutti a destra, e le caselle che sono piene
>     in tutte e due le posizioni sono certe.
> ```
>
> Provalo sulla riga da **1 1 1**: la somma è 1+1+1 più due spazi, cioè **5**; cinque meno cinque fa **zero**; ognuno dei tre numeri è più grande di zero, quindi ognuno ha 1−0 = **una casella certa.** Quella riga è già finita, e non hai indovinato niente.
>
> Provalo sulla riga da **3**: somma 3, cinque meno tre fa **2**; il 3 è più grande di 2, quindi 3−2 = **una casella certa**, quella in mezzo.
>
> **Una regola per non rovinare tutto.** Metti un puntino nelle caselle che sai per certo essere vuote. Se a un certo punto tiri a indovinare e sbagli, l'errore si allarga in silenzio e viene fuori molto dopo, quando non si capisce più da dove veniva. **Non indovinare. Se sei bloccato, ricomincia da una riga o da una colonna che non hai ancora guardato.**
>
> ---
>
> **E poi, se ti va, fanne uno tu.**
>
> ```
>            ┌───┬───┬───┬───┬───┐
>            │   │   │   │   │   │
>            ├───┼───┼───┼───┼───┤
>            │   │   │   │   │   │
>            ├───┼───┼───┼───┼───┤
>            │   │   │   │   │   │
>            ├───┼───┼───┼───┼───┤
>            │   │   │   │   │   │
>            ├───┼───┼───┼───┼───┤
>            │   │   │   │   │   │
>            └───┴───┴───┴───┴───┘
> ```
>
> Annerisci quello che vuoi, poi conta i gruppi di ogni riga e di ogni colonna e scrivi i numeri ai bordi. **Poi ricopia i soli numeri su un foglio pulito e prova a rifare il disegno partendo da quelli.**
>
> Se ci riesci senza mai indovinare, il tuo gioco ha una soluzione sola e lo puoi dare a qualcuno. Se ti blocchi, **non vuol dire che i numeri sono sbagliati: vuol dire che il tuo disegno si può fare in più di un modo**, e allora anneriscine un altro quadretto e riprova.

**I numeri sono stati verificati a mano, riga per riga e colonna per colonna, e poi ricontrollati enumerando tutte le griglie compatibili con gli indizi di riga: ne resta una sola.** La verifica automatica è servita, perché la prima versione di questa voce aveva un indizio di colonna sbagliato e con quello le griglie compatibili erano zero. La deduzione a mano è questa. La colonna centrale ha indizio 5 e quindi è tutta piena; la terza e la quinta riga hanno indizio 5 e quindi sono tutte piene. La prima colonna ha un solo gruppo da tre e deve contenere le caselle già piene della terza e della quinta riga: l'unico gruppo di tre che le contiene entrambe copre le righe tre, quattro e cinque, quindi le prime due caselle di quella colonna sono vuote. L'ultima colonna ha lo stesso indizio e si comporta allo stesso modo. La seconda colonna ha indizio 2 1: il gruppo da due deve venire prima di quello da uno, e l'unica disposizione che lascia piene la terza e la quinta riga mette il gruppo da due sulle righe due e tre e quello da uno sulla riga cinque. La quarta colonna è identica alla seconda. **A quel punto la griglia è piena e non c'è stata nessuna scelta**, il che è la definizione di soluzione unica.

Il disegno che viene fuori non è nominato nel foglio, ed è la decisione più importante della consegna. **La fonte dice che l'immagine può fuorviare, e questo capovolge quello che sembrerebbe una gentilezza**: dire «viene fuori una casetta» sembra un aiuto e invece è la cosa che fa sbagliare, perché chi ha in testa una casetta comincia a disegnarla.

La regola di partenza stampata è la stessa mossa già osservata alla voce 153, problema di ottimizzazione: **una procedura meccanica che dà un appiglio garantito a chi non sa da dove cominciare, e che non toglie niente al problema** perché quello che produce è solo l'inizio. Qui è anche una dimostrazione in piccolo, perché le caselle che dà sono certe e non probabili.

L'ultima parte è la mossa di girare il gioco dalla parte di chi costruisce, con una torsione che questa forma permette e quasi nessun'altra: **la verifica dell'unicità e la costruzione sono la stessa operazione fatta due volte.** Chi disegna e poi risolve i propri numeri senza indovinare ha dimostrato l'unicità della propria soluzione; chi si blocca ha scoperto che il suo disegno non è determinato dai numeri, e la riparazione — annerire un quadretto in più — è alla sua portata. Nessuno deve sapere niente, e il sistema non deve verificare niente.

**Il limite tecnico è lo stesso della voce precedente e va dichiarato:** il sistema che stampa non è affidabile a costruire un nonogramma con soluzione unica di dimensione qualsiasi, perché l'unicità è un'affermazione su tutte le griglie possibili e il problema è NP-completo. Il cinque per cinque qui sopra è stato costruito a mano e verificato a mano; su un venti per venti non si può fare.

Sul pannello da quattro righe da 44 caratteri non ci sta niente di tutto questo: servono cinque righe di griglia più due di intestazione. È una forma da foglio senza rimedio, e l'unica cosa che il pannello potrebbe portare sono gli indizi di una riga sola.

## Da riprendere alla rassegna

**Dire in anticipo che cosa uscirà rovina il compito, e qui c'è la fonte che lo dice.** L'immagine nascosta «gioca un ruolo minimo nella soluzione, perché può fuorviare». Con la misura di Auble, Franks e Soraci raccolta alla voce 110, indovinello classico (enigma) — se la parola chiave arriva prima, l'effetto sparisce — e con quella di Luchins della voce 145, enigma di travaso, fanno tre casi indipendenti in cui **anticipare rovina**, e ognuno con un meccanismo diverso: qui non è la memoria e non è l'abitudine, è che l'aspettativa riempie le caselle al posto del ragionamento.

**Costruire e verificare sono la stessa operazione, ed è la prima volta.** Chi disegna un nonogramma, ne calcola i numeri e poi lo risolve partendo dai soli numeri, ha dimostrato che la soluzione è unica — e se si blocca, ha scoperto che non lo è, con la riparazione già in mano. **In tutte le altre forme il costo di produrre eccede quello di risolvere; qui coincidono**, e questa è l'unica voce raccolta finora di cui si possa dire. Da cercare altrove, perché è la risposta più netta al problema che chiude il capitolo.

**Una regola meccanica che dà un punto di partenza certo, seconda occorrenza.** Alla voce 153, problema di ottimizzazione era il vicino più prossimo, che dà una risposta mediocre ma valida; qui è il conto della sovrapposizione, che dà delle caselle **certe**. La differenza vale la pena guardarla: **l'una dà una risposta da migliorare, l'altra un pezzo di risposta definitivo**, e sono due modi diversi di abbassare la soglia d'ingresso di una forma.

**Il nome di questa forma è fatto di tre pezzi che vengono da tre persone diverse,** e nessuno dei tre l'ha chiamata così per un motivo che riguardi il gioco: il nome di chi l'ha inventata, la desinenza di un oggetto scientifico, e un collezionista inglese che li ha uniti. Con il cavallo da corsa che dà il nome a Nikoli, sono due casi in cui **il nome di una forma non dice niente della forma** — l'esatto contrario dell'economia osservata alla voce 311, zeppa, dove il titolo è metà della consegna.

**Un'immagine si può trasmettere come una fila di numeri, e i numeri sono molti meno dei quadretti.** Venticinque caselle sono descritte da quattordici numeri. È la stessa cosa già osservata alla voce 127, parole crociate senza schema — un disegno che si scrive come un numero — e adesso ci sono due casi. **Per un sistema con un canale testuale largo e un canale grafico stretto vale la pena censirli tutti**, perché sono i punti in cui il vincolo non morde.
