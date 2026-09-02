# Sezione e proiezione

- **Numero** 393 nell'enciclopedia, capitolo 14 — Percezione e inganno dell'occhio
- **Si chiama anche** proiezioni ortogonali, pianta e prospetto, viste multiple, sezione, sviluppo di un solido, geometria descrittiva, metodo di Monge, *orthographic projection*, *cross section*, *net*
- **In una riga** dato un solido, che ombra fa.
- **Contratto** voce breve
- **Fonti** `orthographic-projection.txt`, `multiview-orthographic-projection.txt`, `descriptive-geometry.txt`, `gaspard-monge.txt`, `technical-drawing.txt`, `isometric-projection.txt`, `net-polyhedron.txt`, `cross-section-geometry.txt`, `conic-section.txt`, `shadowgraph.txt`, `it-geometria-descrittiva.txt`, `it-proiezioni-ortogonali.txt`, lette il 2 settembre 2026. I conti sono nostri, in `build/check_391.py`
- **Stato della ricerca** fatta, 2 settembre 2026

## Che cos'è

Si dà di un solido qualcosa che non è il solido — le sue viste da tre parti, la figura che viene tagliandolo con un piano, la sua superficie aperta e stesa — e si chiede di ricostruire l'oggetto, o viceversa.

Sono tre operazioni diverse, e conviene tenerle distinte perché perdono cose diverse.

- **La proiezione** schiaccia il solido su un piano. `orthographic-projection.txt`: i raggi che proiettano sono tutti perpendicolari al piano, cioè partono da infinitamente lontano. Perde la profondità, tutta.
- **La sezione** taglia il solido con un piano e tiene la figura del taglio. `cross-section-geometry.txt`: perde tutto quello che non sta sul piano, e la figura che resta dipende da come il piano è messo.
- **Lo sviluppo** apre la superficie e la stende. `net-polyhedron.txt`: non perde niente della superficie, e perde il modo in cui era piegata.

**La glossa dell'elenco descrive solo la prima delle tre.** «Dato un solido, che ombra fa» è la proiezione — e nemmeno tutta: l'ombra del sole è una proiezione parallela, l'ombra di una lampada no, perché i raggi partono da un punto vicino. La sezione non è un'ombra e lo sviluppo nemmeno.

Parti mobili:

- **Quante viste si danno.** `multiview-orthographic-projection.txt` ne elenca sei — davanti, dietro, destra, sinistra, alto, basso — e scrive che «di solito tre bastano».
- **Da che parte si taglia.** È l'unico parametro della sezione, e cambia tutto.
- **Quale verso si chiede.** Dal solido alla vista, o dalla vista al solido.
- **Se la risposta è unica.** Non lo è, e questo è il fatto della voce.

## Da dove viene

`descriptive-geometry.txt` e `net-polyhedron.txt` datano tutte e due al **1525** il libro di Albrecht Dürer che contiene gli sviluppi dei solidi platonici e di alcuni archimedei — ma ne danno il titolo con due grafie diverse e due traduzioni diverse, una delle quali rende *Richtscheyt* con «livella a bolla» invece che con «riga». La data combacia, la traduzione no; per noi conta la data. `net-polyhedron.txt` aggiunge che a chiamarli *reti* per primo fu **Augustin Hirschvogel nel 1543**.

**La geometria descrittiva nasce dentro una fortificazione ed è stata un segreto militare.** `gaspard-monge.txt`: Monge era disegnatore alla Scuola Reale del Genio di Mézières e gli fu chiesto di calcolare il *défilement* di una fortificazione, cioè l'allineamento delle sommità in modo da sfuggire al tiro da un'altura fuori dalle mura. Vauban aveva proposto un procedimento lento e manuale, con soldati mandati sul posto; Monge lo risolse per via geometrica, e la pagina scrive che il metodo **fu tenuto come segreto militare francese per anni**. `descriptive-geometry.txt` data al **1765** le prime scoperte. Le lezioni del 1795 furono stampate nel **1799** come *Géométrie descriptive*.

`it-geometria-descrittiva.txt` porta la storia più indietro: Vitruvio, fra il I secolo avanti Cristo e il I dopo, usa piante e prospetti e li chiama *icnografie* e *ortografie*. La stessa pagina attribuisce a Poncelet, allievo di Monge, gli studi conclusivi di geometria proiettiva.

**Le sezioni del cono sono più vecchie di tutto il resto.** `conic-section.txt`: i greci le studiarono fino all'opera sistematica di Apollonio di Perga, attorno al 200 avanti Cristo; il cerchio è un caso particolare dell'ellisse, anche se Apollonio lo contava come quarto tipo.

## Varianti e parenti

- **Proiezioni ortogonali** — tre o sei viste, ognuna perpendicolare a un asse. `multiview-orthographic-projection.txt` distingue **primo diedro**, usato in Europa, e **terzo diedro**: cambia dove si mette ogni vista rispetto alle altre, e le due convenzioni si contraddicono.
- **Assonometria e isometria** — `isometric-projection.txt`: nell'isometria i tre assi sono accorciati allo stesso modo e fra due qualsiasi ci sono **120 gradi**. Un solo disegno invece di tre, al prezzo che nessuna faccia è in misura vera.
- **Sezione** — `cross-section-geometry.txt`: la figura che resta dipende da come il piano è messo. Tutte le sezioni di una palla sono cerchi; quelle di un cubo no.
- **Sezione conica** — il caso studiato: piano contro cono, e vengono ellisse, parabola, iperbole.
- **Sviluppo** — `net-polyhedron.txt`: gli spigoli che si tagliano devono formare un **albero ricoprente** del solido, ed è la stessa struttura della voce 366, problema di grafi.
- **Sviluppo per la strada più corta** — la strada più breve fra due punti sulla superficie di un solido è una retta su uno sviluppo scelto bene, e per trovarla bisogna provarne più di uno. È il problema del ragno e della mosca.
- **Ombra** — `shadowgraph.txt` è stata presa credendo che parlasse di questo e **parla d'altro**: è la visualizzazione dei flussi, cioè le ombre che i gradienti di indice di rifrazione dell'aria proiettano su uno schermo. Non riguarda la proiezione di un solido, e viene citata qui e in fondo per una cosa sola che contiene.
- **Voce 392, rotazione mentale** — `visuospatial-ability.txt` mette la prova del taglio mentale e la prova dello sviluppo delle superfici accanto a quella di rotazione, come sorelle.
- **Voce 371, costruzione con riga e compasso** — l'altra forma dell'enciclopedia in cui il foglio contiene una costruzione geometrica esatta e lo strumento decide se torna.
- **Voce 375, topologia ricreativa** — anche là si taglia e si apre della carta, ma là quello che conta è che cosa resta collegato, e qui che forma viene.

## Che cosa se ne sa

**Undici, e il conto è stato rifatto due volte da due parti opposte.** Le reti del cubo sono **11**. `build/check_391.py` le ottiene facendo rotolare un cubo su una scacchiera e segnando quale faccia tocca ogni casella — 11 forme diverse a meno delle otto simmetrie del quadrato — e poi ricomincia dall'altro capo: costruisce tutti i **35** poliomini liberi di sei celle e prova su ognuno se un cubo ci possa rotolare sopra toccando tutte e sei le facce. Ne restano 11, **e sono gli stessi undici**. Il grafo delle facce del cubo ha **384** alberi ricoprenti, che è quanti sono gli svolgimenti prima di identificare quelli uguali per simmetria.

**La sezione del cubo di traverso alla diagonale cambia numero di lati due volte.** Tagliando con piani perpendicolari alla diagonale maggiore si passa da un punto a un triangolo, poi a un esagono, poi di nuovo a un triangolo e a un punto.

```
 dove taglia              che figura viene
 vicino a un angolo       un triangolo
 a un terzo               un triangolo
 a meta' esatta           un esagono regolare
 a due terzi              un esagono
 vicino all'altro angolo  un triangolo
```

`cross-section-geometry.txt` dice esattamente questo — «un punto, un triangolo o un esagono» — e il conto lo conferma per costruzione: si intersecano i dodici spigoli col piano e si contano i punti distinti. **A metà esatta della diagonale l'esagono è regolare**, e i sei lati misurano `√2/2 = 0,707107` con uno scarto fra il più lungo e il più corto sotto il miliardesimo.

**Tre viste non bastano, e la fonte del disegno tecnico dice il contrario di quella del disegno tecnico.** `multiview-orthographic-projection.txt` scrive che «di solito tre viste danno abbastanza informazione per costruire l'oggetto», con un *di solito* che nessuno legge; `technical-drawing.txt` è più netto e scrive che i disegni artistici si interpretano soggettivamente mentre **«i disegni tecnici si intendono avere un solo significato inteso»**. Preso un solido di sette cubetti dentro una scatola 3 × 3 × 3 e calcolate le sue tre viste, `build/check_391.py` enumera tutti i solidi di quella scatola che danno quelle tre viste: sono **2**, uno di sei cubetti e uno di sette. La differenza è un cubetto in un angolo che nessuna delle tre viste può vedere. **Il significato inteso è uno, il significato possibile no**, e la distanza fra le due cose si misura in cubetti.

**Una domanda aperta si tocca con le forbici.** `net-polyhedron.txt`: nel **1975** G. C. Shephard chiese se ogni poliedro convesso abbia almeno uno sviluppo che non si sovrapponga — la congettura di Dürer — e la domanda è tuttora senza risposta. Esistono poliedri non convessi senza sviluppo; nel **2014** Mohammad Ghomi ha mostrato che ogni poliedro convesso ne ha uno dopo una trasformazione affine. È la terza volta in due capitoli che una forma di questa enciclopedia confina con un problema aperto su cui si entra con carta e forbici, dopo la voce 370, dissezione geometrica e la voce 376, impacchettamento e tassellazione.

**Una pagina attribuisce l'invenzione del metodo a un nome che nessun'altra fonte nomina.** `it-proiezioni-ortogonali.txt` scrive che «la formulazione originale di questo metodo, ideata da Paolo Sglavo, non prevedeva il piano laterale», con un richiamo di nota che rimanda a una pagina dello Smithsonian sui modelli di Jullien per la geometria descrittiva, cioè a un documento che non dice quello. La stessa pagina non nomina mai Monge. `descriptive-geometry.txt`, `gaspard-monge.txt`, `technical-drawing.txt` e `it-geometria-descrittiva.txt` attribuiscono tutte e quattro il metodo a Monge. Si tiene Monge e si dichiara l'altra.

**Il bianco e nero non morde: il disegno tecnico è nato in bianco e nero.** `cross-section-geometry.txt` ricorda che le sezioni si campiscono a tratteggio, e che **è il tratteggio a dire di che materiale sono** — cioè la convenzione usa la trama e non la tinta. `technical-drawing.txt` codifica il resto in una norma, la ISO 128. **La fotografia non morde**, perché quello che si fotografa è un disegno al tratto. **Il muro di `ideas/10 §8` non morde**, perché il foglio si costruisce dal solido: si sceglie l'oggetto e se ne calcolano le viste.

**Una fonte presa per questa voce serve a un'altra, già scritta.** `shadowgraph.txt` riguarda un'altra disciplina, ma contiene questo: negli anni Cinquanta l'editore inglese E. T. W. Dennis & Sons di Londra e Scarborough chiamava *Shadowgraph* una serie di cartoline «da tenere contro la luce», in cui **attraverso un'immagine innocente se ne vede un'altra**. È esattamente la voce 390, immagine da comporre in controluce, in versione commerciale e con settant'anni di anticipo.

## Esempi trovati

Da Dürer, 1525: gli sviluppi dei solidi platonici, disegnati per essere ritagliati.

Da Monge a Mézières, 1765: il calcolo del *défilement* di una fortificazione, tenuto segreto.

Da Vitruvio: le piante e i prospetti degli edifici, chiamati icnografie e ortografie.

Dalla scuola: le proiezioni ortogonali si insegnano ancora così, tre viste su un foglio, e l'Europa usa una convenzione diversa da altri paesi.

Da Apollonio di Perga, verso il 200 avanti Cristo: il cono tagliato in tutti i modi possibili.

Dai libri di prove attitudinali: `visuospatial-ability.txt` elenca la prova del taglio mentale e quella dello sviluppo delle superfici, in cui una figura piana ha i lati numerati e un solido le facce con le lettere.

## Una nostra versione

> **Tre viste, e non basta**
>
> Un oggetto è fatto di cubetti dentro una scatola di 3 × 3 × 3. Ecco come si vede da tre parti. Un `#` è pieno, un `.` è vuoto.
>
> ```
>  da davanti  da destra   dall'alto
>     ###         ###         ###
>     #..         #..         #..
>     #..         #..         #..
> ```
>
> La domanda che fa il libro di disegno è: **quanti cubetti ha l'oggetto?**
>
> La domanda vera è un'altra: **quanti oggetti diversi danno esattamente queste tre viste?**
>
> Disegnali tutti, a piani, come faresti per un palazzo: prima il piano che tocca il tavolo, poi quello sopra, poi quello sopra ancora.

Gli oggetti sono **due**, uno di sei cubetti e uno di sette, e differiscono per un cubetto in un angolo che nessuna delle tre viste può vedere: sta dietro rispetto a davanti, dietro rispetto a destra, e sotto rispetto all'alto. La verifica è per enumerazione completa dentro la scatola, in `build/check_391.py`.

La consegna è girata al contrario, e qui non toglie niente: la domanda di scuola — ricostruisci il solido — è contenuta dentro la nostra, perché per contare gli oggetti bisogna prima saperne costruire uno.

E c'è un secondo foglio che costa un ritaglio:

> **Undici**
>
> Prendi un foglio a quadretti e ritaglia una fila di sei quadretti attaccati fra loro, come vuoi tu, purché ogni quadretto tocchi un altro per un lato intero. Prova a piegarla in un cubo.
>
> Le figure di sei quadretti che si possono fare sono **35**. Di quelle, **11** si chiudono in un cubo e 24 no. Trovane più che puoi, e per ognuna scrivi se si chiude.
>
> Quando ne hai trovate parecchie, guarda le undici che si chiudono e dimmi che cosa hanno in comune.

Dove si romperebbe: da nessuna parte, ma il secondo foglio chiede forbici e pazienza, e cercare tutte e trentacinque le figure a mano è più lungo che risolvere il primo. La scheda funziona per intero con il primo foglio solo; il secondo è un'aggiunta.

## Da riprendere alla rassegna

**È la forma in cui il foglio dice meno dell'oggetto, e si può misurare quanto meno.** Tre viste ortogonali di un solido in una scatola 3 × 3 × 3 ne lasciano due possibili; la stessa domanda su una scatola più grande ne lascerebbe molti di più. Alla rassegna è il modello di tutte le forme che consegnano una descrizione incompleta: **la differenza fra descrizione e oggetto è un numero, e si conta.**

**Il disegno tecnico è l'unica forma di questo capitolo che dichiara di non essere ambigua**, e la dichiarazione è quasi vera. `technical-drawing.txt` scrive che un disegno tecnico ha un solo significato inteso; il conto dice che ne ha due possibili. La distanza fra «inteso» e «possibile» è tutta la materia del capitolo, e qui compare in una disciplina che si era costruita apposta per eliminarla.

**Undici, e rifare batte confrontare per la quinta volta.** La fonte dà il numero delle reti del cubo dentro una successione di numeri di svolgimenti di ipercubi; rifarlo per rotolamento e poi per filtro sui trentacinque poliomini costa venti righe e regge da solo. Sta accanto alla tabella del kakuro, ai pentamini, all'alfabeto di Bacone e alle regole degli automi.

**Una forma che confina con un problema aperto, ancora una volta.** La congettura di Dürer del 1975 si enuncia con un foglio e un paio di forbici. È il terzo caso, dopo la dissezione geometrica e le tassellazioni, e a questo punto è una proprietà del materiale e non un caso: **la geometria fatta con la carta ha un bordo su cui si arriva senza attrezzatura.**

**La riga di differenza.** Alla voce 391, unisci i puntini il foglio contiene la figura per intero e la mano la ricalca; alla voce 392, rotazione mentale il foglio contiene l'oggetto per intero e non dice da che parte lo si guardi. Qui il foglio **contiene meno dell'oggetto**, e la parte mancante non si recupera guardando meglio: si recupera immaginando, e più di una risposta è corretta.
