# Stereogramma

- **Numero** 395 nell'enciclopedia, capitolo 14 — Percezione e inganno dell'occhio
- **Si chiama anche** stereogramma, autostereogramma, immagine stereoscopica, coppia stereoscopica, *Magic Eye*, occhio magico, stereogramma a punti casuali, SIRDS, anaglifo
- **In una riga** due immagini che diventano profondità quando gli occhi si arrendono.
- **Contratto** voce breve
- **Fonti** `autostereogram.txt`, `stereoscopy.txt`, `stereoscope.txt`, `charles-wheatstone.txt`, `random-dot-stereogram.txt`, `magic-eye.txt`, `bela-julesz.txt`, `binocular-disparity.txt`, `stereopsis.txt`, `cyclopean-image.txt`, `vergence-accommodation-conflict.txt`, `wiggle-stereoscopy.txt`, `pupillary-distance.txt`, `amblyopia.txt`, `ascii-stereogram.txt`, `anaglyph-3d.txt`, `depth-perception.txt`, `it-stereoscopia.txt`, `it-stereogramma.txt`, lette il 2 settembre 2026. I conti sono nostri, in `build/check_391.py`
- **Stato della ricerca** fatta, 2 settembre 2026

## Che cos'è

Si danno ai due occhi due immagini leggermente diverse, e il cervello ne ricava una profondità che sul foglio non c'è. `binocular-disparity.txt`: la disparità è la differenza fra l'immagine dell'occhio sinistro e quella del destro, e quella orizzontale è la parte che produce la profondità.

Ci sono due modi di darle, e sono forme diverse.

- **Due immagini affiancate.** Ognuno dei due occhi ne guarda una. Serve o uno strumento — `stereoscope.txt` — oppure la *visione libera*, cioè decidere a mano dove convergere.
- **Una immagine sola con un motivo che si ripete.** `autostereogram.txt`: se la stessa trama si ripete in orizzontale, l'occhio sinistro può agganciarsi a una copia e il destro a quella accanto. Il cervello accetta lo scambio, e **la profondità del piano dipende solo da quanto sono distanti due copie**. Ripetizioni più corte danno un piano più vicino.

**In tutti e due i casi il foglio contiene una cosa e i due occhi insieme ne producono un'altra.** Non è una lettura che si aggiunge: è una lettura che sostituisce, e per averla bisogna smettere di guardare il foglio.

`depth-perception.txt` elenca **tre soli indizi binoculari** contro sedici monoculari: la stereopsi, la convergenza — che funziona sotto i dieci metri — e la stereopsi da ombre. Questa voce sta su tutti e tre, e le altre quattro del blocco su nessuno.

Parti mobili:

- **Quanto distano le due immagini, o le due copie.** È il solo parametro, e vale in millimetri.
- **Se si guarda a occhi paralleli o incrociati.** `autostereogram.txt`: la stessa immagine letta nei due modi dà la profondità rovesciata.
- **Che cosa c'è nella trama.** Punti a caso, un disegnino ripetuto, o lettere.
- **Se serve uno strumento.** Lo stereoscopio, gli occhiali rossi e ciano, o niente.
- **Quanti piani di profondità.** Da due a molti.

## Da dove viene

`autostereogram.txt` mette in fila le date, e sono di cose diverse.

- **1593**, Giambattista della Porta guarda una pagina di un libro con un occhio e l'altra con l'altro, e riesce a leggerne una alla volta. È il primo caso noto di disaccoppiamento fra convergenza e messa a fuoco — ma quello che vide era rivalità fra i due occhi, non cooperazione.
- **1838**, Charles Wheatstone pubblica «Contributions to the physiology of vision. Part 1», e mostra che due figure piane che differiscono solo per la posizione orizzontale danno una sensazione di profondità. `charles-wheatstone.txt`: nel **1840** ricevette per questo la Royal Medal. `random-dot-stereogram.txt` data invece al 1840 la costruzione dello stereoscopio: sono due fatti, non una discordanza. **Ma `stereopsis.txt` colloca Wheatstone «alla fine del diciannovesimo secolo» e tre righe sotto scrive 1838**, e la seconda affermazione è quella che porta con sé il titolo dell'articolo.
- **1844**, David Brewster nota l'*effetto carta da parati*: fissando un motivo ripetuto e cambiando la convergenza, lo si vede davanti o dietro il muro.
- **1939**, Boris Kompaneysky pubblica il primo stereogramma a punti casuali, un volto di Venere disegnato a mano.
- **1959**, Béla Julesz inventa gli stereogrammi a punti casuali ai Bell Labs — `cyclopean-image.txt` precisa che era un ingegnere radaristi ungherese e che **cercava un modo per scoprire oggetti mimetizzati nelle fotografie aeree delle ricognizioni**. `random-dot-stereogram.txt` racconta l'inizio: nel 1956 stava cercando strutture nell'uscita dei generatori di numeri casuali, provò a guardare due copie identiche con lo stereoscopio, e spostò un quadrato al centro di una delle due. `bela-julesz.txt` dà le date — 1928-2003 — e aggiunge che fu anche il primo a studiare la discriminazione delle trame vincolandone le statistiche del secondo ordine, che è il meccanismo della voce 384, mimetismo e camuffamento visto dall'altro lato.
- **1979**, Christopher Tyler, allievo di Julesz, unisce le due idee e produce **il primo autostereogramma a punti casuali in bianco e nero**, con un Apple II e un programma in BASIC scritto da Maureen Clarke.
- **1991**, Tom Baccei e Cheri Smith fanno i primi a colori. `magic-eye.txt`: il primo libro esce in Giappone alla fine del 1991, con i rappresentanti mandati agli angoli delle strade a insegnare come si guarda, e diventa un successo in poche settimane; il primo libro nordamericano è del **1993**.

`it-stereogramma.txt` e `it-stereoscopia.txt` portano tutte e due un avviso in cima — una è dichiarata da controllare per «linguaggio colloquiale», l'altra non formattata secondo gli standard — e la prima ha comunque la cosa più utile delle due: **un elenco degli otto tipi di stereogramma**, dall'immagine parallela all'anaglifo alla barriera di parallasse all'integramma di Lippmann fino al wiggle-gram.

## Varianti e parenti

- **Coppia affiancata, parallela** — la più antica. `stereoscopy.txt`: l'immagine fusa sembra più grande e più lontana.
- **Coppia affiancata, incrociata** — le due immagini si scambiano di posto e si converge davanti al foglio. L'immagine fusa sembra più piccola e più vicina, e `stereoscopy.txt` dice che di solito è più facile per chi comincia.
- **Autostereogramma a carta da parati** — un disegno riconoscibile ripetuto a intervalli variabili.
- **Autostereogramma a punti casuali (SIRDS)** — la trama non vuol dire niente e la figura sta soltanto negli scarti.
- **SIRTS, a lettere** — `ascii-stereogram.txt`: lo stesso, fatto di caratteri invece che di punti. Si stampa su qualunque cosa scriva testo.
- **Anaglifo** — `anaglyph-3d.txt`: le due immagini sovrapposte in due colori opposti, di solito rosso e ciano, e occhiali con due filtri. La prima descrizione è di W. Rollmann, agosto **1853**; nel 1858 Joseph D'Almeida proietta con filtri rossi e verdi.
- **Barriera di parallasse e integramma** — `it-stereogramma.txt`: la prima registrata da Frederic Eugene Ives nel 1903, il secondo proposto da Gabriel Lippmann nel 1908. Sono i nonni della voce 389, moiré nella sua variante a lenti.
- **Wiggle-gram** — `wiggle-stereoscopy.txt`: le due immagini si alternano al posto di essere date una per occhio. **Dà profondità anche a chi vede da un occhio solo**, e richiede il movimento, quindi non è stampabile.
- **Voce 390, immagine da comporre in controluce** — l'altra voce del capitolo fatta di due fogli. Là i due fogli si sovrappongono e a decidere è il registro; qui non si sovrappongono e a decidere sono gli occhi.
- **Voce 394, prospettiva forzata** — l'opposto esatto: là un'immagine ferma basta e avanza, qui un'immagine ferma non basta finché non intervengono due occhi.
- **Voce 384, mimetismo e camuffamento** — la parentela è storica e non metaforica: Julesz cercava di scoprire cose mimetizzate.

## Che cosa se ne sa

**La cosa più importante è quante persone non lo vedono, e il numero dipende da come si pone la domanda.** Quattro cifre, da quattro fonti, con quattro statuti diversi:

- `amblyopia.txt`: l'ambliopia riguarda **l'1-5%** degli adulti, il **2-5%** della popolazione nei paesi occidentali, e **l'1-4%** dei bambini «a seconda del criterio scelto per la diagnosi».
- `random-dot-stereogram.txt`: circa il **5%** non percepisce la profondità negli stereogrammi a punti casuali, per disturbi vari della visione binoculare, e si identifica con prove apposite.
- `stereoscopy.txt`: si ritiene che circa il **12%** non riesca a vedere correttamente le immagini tridimensionali; e secondo un altro esperimento **fino al 30%** ha una visione stereoscopica molto debole.

**Non sono in contraddizione: contano cose diverse**, dalla diagnosi clinica alla capacità di fondere, alla comodità di farlo. Quello che conta per una casa è il capo alto: **fra una persona su venti e una su tre potrebbe non vedere niente**, e non è questione di applicazione né di ingegno. `autostereogram.txt` aggiunge la parte che decide: se il difetto non è corretto entro un periodo critico dell'infanzia, il danno è permanente.

**Quanto largo può essere uno stereogramma stampato su A4, contato.** `stereoscopy.txt`: nella visione libera i punti corrispondenti degli oggetti lontani devono stare a una distanza pari a quella fra gli occhi **e non di più**, perché gli occhi non divergono; la media dichiarata è **63 mm**. Quindi una coppia affiancata su A4 usa al massimo `2 × 63 = 126 mm` dei 210 disponibili, cioè il **60%** del foglio, e ogni immagine è larga al massimo 63 mm. Per stare comodi anche a chi ha gli occhi più vicini — `pupillary-distance.txt` dà gli intervalli su cui si progettano gli strumenti binoculari, **da 52 a 72 mm** e da 55 a 75 — si scende a 104 mm, il 50% del foglio. **Un A4 può contenere uno stereogramma grande metà A4.**

**Un autostereogramma si può fare di lettere, e sta in un blocco di testo.** Con quattordici caratteri di ripetizione e una spaziatura di dieci caratteri per pollice — cioè 2,54 mm l'uno, che è la spaziatura classica dei caratteri a passo fisso — la ripetizione misura **35,6 mm**, che sta sotto i 52 mm anche per gli occhi più stretti. Tenendo il foglio a 40 cm, i piani si fondono così:

```
 gradino  ripetizione      il piano si fonde a
       1      35,6 mm  518 mm dietro il foglio
       2      33,0 mm  441 mm dietro il foglio
       3      30,5 mm  375 mm dietro il foglio
       4      27,9 mm  319 mm dietro il foglio
```

I quattro piani vengono da quattro ripetizioni che differiscono di un carattere ciascuna, e **un carattere di differenza vale fra i 56 e i 78 millimetri di profondità**. La distanza a cui si tiene il foglio è un'ipotesi nostra, dichiarata: cambiandola, cambiano proporzionalmente tutte le profondità.

**Che il disegno sia davvero dentro il testo è stato verificato al contrario.** `build/check_391.py` tesse la trama con la ricetta della fonte — ogni carattere ricopia quello che sta a *ripetizione meno profondità* posti a sinistra — e poi la rilegge con un metodo che **non sa che cosa contenga**: per ogni colonna cerca lo scorrimento che fa combaciare il carattere in tutte e tredici le righe insieme. Con undici lettere e tredici righe una coincidenza per caso vale `11⁻¹³`, quindi non serve nessuna soglia. Tutte e **30** le colonne leggibili — quelle dopo la prima ripetizione — restituiscono il gradino giusto.

**Il bianco e nero morde su uno degli otto tipi, ed è quello che tutti conoscono.** `anaglyph-3d.txt`: l'anaglifo è definito su due colori cromaticamente opposti, e senza colori non esiste. Gli altri sette dell'elenco di `it-stereogramma.txt` sopravvivono; in particolare **il primo autostereogramma della storia era in bianco e nero**, quello di Tyler del 1979. Il bianco e nero non toglie la forma: toglie la versione con gli occhialini.

**La fotografia non morde sull'andata e morde sul ritorno.** Il foglio si stampa e funziona; quello che il sistema non può fare è verificare che sia stato visto, perché il rilievo non sta nel foglio fotografato ma nei due occhi di chi guarda. Quello che si può chiedere indietro è una cosa che il rilievo permette di leggere e la trama piana no.

**Il costo dichiarato dalla forma.** `vergence-accommodation-conflict.txt`: guardare una cosa così mette in disaccordo la convergenza degli occhi e la messa a fuoco, che normalmente vanno insieme. Il risultato è affaticamento visivo e, dopo poco, mal di testa. `stereoscope.txt` dice la stessa cosa dal suo lato: la visione libera è possibile con pratica ma non riproduce gli indizi naturali, e stanca. **Non è una forma da tenere a lungo.**

**Il muro di `ideas/10 §8` non morde**, perché la trama si costruisce dalla mappa di profondità: chi la stampa sa già che cosa contiene.

## Esempi trovati

Da Wheatstone, 1838: due piastre piane con due righe verticali, che differiscono solo per la posizione orizzontale.

Da Brewster, 1844: la carta da parati di casa, guardata storto.

Da Julesz, 1959: due copie di una nuvola di punti casuali, con un quadrato spostato al centro. `cyclopean-image.txt` riassume la differenza con Wheatstone in due parole: Wheatstone aveva mostrato che la disparità binoculare è **necessaria**, Julesz che è **sufficiente**.

Dai libri *Magic Eye*, dal 1991, e dalle riviste per ragazzi degli anni Novanta, che ne avevano una pagina fissa.

Dagli stereogrammi in fondo alle firme dei messaggi di posta elettronica, fatti di caratteri, che `ascii-stereogram.txt` cita come uso reale.

Dagli ortottisti: `magic-eye.txt` dice che gli stessi stereogrammi si usano nel trattamento di alcuni disturbi della visione binoculare.

Dalle cartoline stereoscopiche dell'Ottocento: `it-stereogramma.txt` racconta il passaggio dalla stampa su cartoncino a quella su carta sottile e poi su vetro, per guadagnare contrasto illuminando in trasparenza.

## Una nostra versione

> **Una scala fatta di lettere**
>
> Qui sotto ci sono tredici righe di lettere. Sembrano niente, e in parte lo sono: la trama si ripete ogni quattordici caratteri, e a occhi normali si vede solo che si ripete.
>
> ```
>  ruuoreusraresruuoreusrresruuoreusresruuoreus
>  tnunsilnlnmustnunsilnlmustnunsilnmustnunsiln
>  lruotilruutetlruotilrutetlruotilrtetlruotilr
>  muieretleiulnmuieretleulnmuieretlulnmuieretl
>  tumsmntmslamltumsmntmsamltumsmntmamltumsmntm
>  munlormtmeummmunlormtmummmunlormtummmunlormt
>  ossnlenlmsaeeossnlenlmaeeossnlenlaeeossnlenl
>  entnaoenotionentnaoenoionentnaoenionentnaoen
>  minmnneluntliminmnnelutliminmnneltliminmnnel
>  rttoatsrotriirttoatsroriirttoatsrriirttoatsr
>  loonioemonnttloonioemonttloonioemnttloonioem
>  nntmmiotmtumnnntmmiotmumnnntmmiotumnnntmmiot
>  nsuaemiutlrlensuaemiutrlensuaemiurlensuaemiu
> ```
>
> **Come si guarda.** Tieni il foglio vicinissimo al naso: così vicino non riesci a metterlo a fuoco, e gli occhi smettono di provarci. Poi allontanalo piano piano senza cercare di mettere a fuoco. A un certo punto le lettere si agganciano, e il foglio si spezza in **quattro gradini**, ognuno più avanti del precedente andando verso destra.
>
> Se non succede subito, non insistere più di un minuto: stanca sul serio, perché stai chiedendo agli occhi di puntare lontano e di mettere a fuoco vicino, e normalmente le due cose vanno insieme.
>
> **E se non succede per niente**, non vuol dire niente su di te. Fra una persona su venti e una su tre non vede questo genere di immagini, per come sono fatti i suoi occhi, e non è una cosa che si impari.
>
> Quando l'hai visto, misura: **quanti caratteri contiene la ripetizione, in ognuno dei quattro gradini?** Si conta sul foglio, con la matita, senza guardare in rilievo. Sono quattro numeri, e sono diversi.

I quattro numeri sono 14, 13, 12 e 11 e si contano cercando dove la trama ricomincia uguale. La domanda finale è girata al contrario apposta: chiede una cosa che si fa **sul foglio piatto**, con la matita, e che quindi torna indietro al sistema. Chi non riesce a vedere il rilievo fa lo stesso l'esercizio per intero, e scopre da sé che la cosa che ha visto chi lo ha visto è scritta lì, in quattro numeri.

Il foglio è un blocco di testo largo 44 caratteri — la stessa larghezza delle righe del display di casa — e si stampa su qualunque cosa. La ripetizione misura 35,6 mm con un carattere a passo fisso da dieci per pollice, e sta sotto la distanza fra gli occhi anche per chi li ha più vicini della media.

Dove si romperebbe: se la stampa usa un carattere proporzionale invece che a passo fisso, la ripetizione non è più costante e non funziona più niente. Non è una questione di precisione: è una questione di scelta del carattere, ed è l'unico requisito.

## Da riprendere alla rassegna

**È l'unica forma dell'enciclopedia che una parte delle persone non può eseguire, e non per una ragione che si possa aggirare.** Fra il 5% e il 30% secondo come si pone la domanda. Non è difficoltà: è visione binoculare. Alla rassegna va guardata due volte, perché è la prima volta che una forma esclude per costruzione, e perché la scheda ha dovuto trovare un modo di funzionare comunque — la domanda finale si risolve sul foglio piatto.

**Il vincolo che decide è la distanza fra gli occhi, e non ha niente a che vedere con la stampa.** Nel resto del capitolo i limiti erano la stampante, la carta e la mano. Qui il numero è 63 mm ed è un dato anatomico: fissa la larghezza massima di una coppia stereoscopica, che è metà A4, e la ripetizione massima di un autostereogramma. **È il primo vincolo del progetto che sta nel corpo di chi legge.**

**Un autostereogramma fatto di caratteri sta in 44 colonne**, cioè esattamente nella larghezza di riga del display di casa. Alla rassegna vale come promemoria: prima di dichiarare che una forma visiva richiede il disegno, si guarda se esista una versione fatta di testo. Questa esisteva, ed è documentata come uso reale dagli anni delle firme di posta elettronica.

**La forma dichiara da sé il proprio costo**, e non è il tempo di preparazione: è il mal di testa. Il conflitto fra convergenza e accomodazione è documentato e non si aggira. Alla rassegna sta accanto alle poche forme che hanno un limite di durata scritto nella loro fisiologia.

**La riga di differenza.** Alle voci 391, 392 e 393 il foglio contiene l'oggetto e il lavoro è ricostruirlo; alla voce 394, prospettiva forzata contiene una scena falsa che un occhio solo legge benissimo. Qui il foglio contiene **una cosa per un occhio e un'altra per due**, e non è un'aggiunta: la prima lettura sparisce quando compare la seconda. È il valore opposto della grandezza del capitolo rispetto alla voce 391, unisci i puntini, dove il foglio e l'occhio dicono la stessa identica cosa.
