# Scambio

- **Numero** 318 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che tolgono, aggiungono o cambiano lettere»
- **Si chiama anche** scambio di consonanti, scambio di vocali, scambio di lettere, scambio di estremi, scambio di iniziali, trasposizione, *transposition*, contrepèterie, papera, *spoonerism*
- **In una riga** due lettere si scambiano di posto: *carta → tarca*.
- **Contratto** voce breve
- **Fonti** `it-scambio.txt`, `damerau-levenshtein-distance.txt`, `spoonerism.txt`, `transposition-cipher.txt`, prese il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Due lettere si scambiano di posto, e tutto il resto resta dov'era. La glossa dell'elenco — *carta → tarca* — è un caso che fallisce, perché *tarca* non è una parola: la condizione è la stessa di tutto il capitolo, deve venir fuori un'altra parola italiana.

Lo scambio dichiara sempre **che cosa** si scambia e **dove**, e i nomi sono cinque: di consonanti, di vocali, di lettere quando le due sono una consonante e una vocale, di estremi quando sono la prima e l'ultima, di iniziali quando sono le prime lettere di due parole diverse dentro una frase.

Differenza dalla voce 321, antipodo, che è il termine di paragone di questo blocco: là non si sceglie niente, perché la mossa è decisa dalla parola. **Qui si scelgono due posizioni fra n.** Su una parola di otto lettere sono ventisette stringhe diverse contro due (`build/check_318.py`), e la tabella che esaurisce l'antipodo qui non si può stampare.

## Da dove viene

Dalla tradizione enigmistica italiana, dove è uno degli schemi elementari, e `it-scambio.txt` non ne dà né una data né un inventore.

Il parente estero ha invece una storia documentata. Lo scambio di iniziali fra due parole di una frase è la **contrepèterie** francese, pubblicata per la prima volta da François Rabelais nel Cinquecento nel *Pantagruel*, e in inglese è lo **spoonerism**, dal reverendo William Archibald Spooner (1844-1930) di New College a Oxford. `spoonerism.txt` registra la parola nell'*Oxford English Dictionary* già nel 1900 — e poi riporta che nel 1928 il *Daily Herald* diede la cosa per leggenda, citando un ex allievo secondo cui Spooner ne fece **uno solo in tutta la vita**, nel 1879. La forma porta il nome di qualcuno che quasi certamente non la praticava.

`it-scambio.txt` osserva che in italiano il gioco rende meno che in francese, perché grafia e pronuncia coincidono quasi sempre e allora lo scambio si vede prima di essere sentito; e che manca il registro osceno che regge la contrepèterie, di cui la fonte porta un esempio solo e non lo sviluppa.

## Varianti e parenti

- **Scambio di sillabe** — la stessa mossa con un'unità più grande, che `it-scambio.txt` nomina in una riga.
- **Spostamento** (319) — una lettera cambia posto ma nessuna prende il suo: è la mossa vicina, e le due si confondono quando le lettere sono contigue.
- **Metatesi** (320) — lo stesso fenomeno guardato dalla linguistica invece che dall'enigmistica.
- **Antipodo** (321) — la trasposizione senza scelte.
- **Anagramma** (331) — lo scambio ripetuto quante volte si vuole; uno scambio solo ne è il caso minimo.
- **Crittografia pura** (341) — le cifrature a trasposizione fanno esattamente questo su un messaggio intero: `transposition-cipher.txt` le definisce come le cifre che permutano le posizioni senza toccare le lettere, in opposizione a quelle a sostituzione.
- **Papere e lapsus** — lo scambio non voluto, che è la ragione per cui il fenomeno è stato studiato prima di essere giocato.

## Che cosa se ne sa

**Lo scambio è la quarta operazione della distanza di edit, e la quarta operazione vale solo per le lettere contigue.** La distanza di Levenshtein ammette inserzione, cancellazione e sostituzione; `damerau-levenshtein-distance.txt` definisce la distanza di Damerau–Levenshtein aggiungendo «la trasposizione di due caratteri **adiacenti**». Questa restrizione ha una conseguenza esatta, e va contro l'aspettativa: **nessuno dei cinque esempi canonici dello scambio enigmistico sta a distanza uno, nemmeno con la quarta operazione**, perché in tutti e cinque le due lettere sono lontane.

```
 tipo        prima           dopo            Lev  D-L
 consonanti  maschera        marchesa        2    2
 vocali      balletto        bolletta        2    2
 lettere     ercole          creole          2    2
 estremi     astio           ostia           2    2
 iniziali    costo del pane  posto del cane  2    2
 contigue    prati           parti           2    1
 contigue    treno           terno           2    1
```

Le due ultime righe sono nostre e servono da controprova: lì le lettere sono contigue, e la quarta operazione morde. Le distanze sono state calcolate in due modi diversi — programmazione dinamica, e enumerazione completa di tutte le stringhe a una operazione — in `build/check_318.py`.

Lo stesso conto dice quanto pesi la quarta operazione: su *carta* le stringhe a una operazione passano da 226 a 230, su *maschera* da 349 a 356. **Aggiungere la trasposizione allarga il vicinato dell'1,8% e del 2,0%.** È poco, e spiega perché nella pratica le due distanze si comportino quasi allo stesso modo.

Il numero che gira su questa operazione va preso con la sua ambiguità. `damerau-levenshtein-distance.txt` riferisce che Damerau, studiando gli errori di scrittura per un sistema di ricerca documentale, trovò **più dell'80%** riconducibili a un solo errore di uno dei quattro tipi; la stessa pagina dice però, due righe dopo, che il suo lavoro considerava soltanto gli errori correggibili con al più una modifica. Le due affermazioni accostate non dicono su quale popolazione sia calcolato l'80%, e la percentuale va usata come indicazione dell'ordine di grandezza e non come misura.

Sul confine con lo spostamento la fonte italiana è esplicita e onesta: quando le due lettere sono contigue lo scambio e lo spostamento coincidono, «esistono opinioni contrastanti» su quale dei due nomi valga, e la questione «non è poi di fondamentale importanza». Il confine è lo stesso della distanza di edit e della linguistica, ed è **la contiguità**.

## Esempi trovati

Da `it-scambio.txt`, riscritti: di consonanti *maschera / marchesa*; di vocali *balletto / bolletta*; di lettere *Ercole / creole*; di estremi *astio / ostia*; di iniziali *costo del pane / posto del cane*.

Da `spoonerism.txt`: *crushing blow* che diventa *blushing crow*, e la frase attribuita a Spooner nel 1879, *Kinkering Kongs their Titles Take* per *Conquering Kings*.

Nostri, per il caso contiguo che le fonti non danno: *prati / parti* e *treno / terno*.

## Una nostra versione

> **Cinque coppie, cinque nomi, e non ne avanza nessuno**
>
> In ognuna di queste coppie due lettere si sono scambiate di posto. Il gioco non è indovinare la seconda parola — te la do io. È dire **quali due lettere** hanno cambiato posto, e come si chiama quel tipo di scambio.
>
> ```
>  1  maschera / marchesa
>  2  balletto / bolletta
>  3  astio / ostia
>  4  Ercole / creole
>  5  costo del pane / posto del cane
> ```
>
> Scrivi il numero giusto in ogni casella. Ogni numero va usato una volta sola, e questa è la tua rete: se ti avanza una casella, hai sbagliato prima.
>
> ```
>  di vocali ───       di consonanti ───   di lettere ───
>  di estremi ───      di iniziali ───
> ```
>
> Poi la parte difficile, e senza rete: **fanne una tu.** Prendi due parole che stanno bene insieme, scambia le loro iniziali, e vedi se esce ancora qualcosa di sensato.

**La verifica è dentro il materiale, e per la prima volta in questo capitolo non serve un vocabolario.** Le parole sono già date tutte e dieci; quello che si chiede è di dire che operazione le lega, e cinque numeri in cinque caselle si controllano da soli. Chiedere l'operazione invece del risultato è la **terza via d'uscita** dal limite del capitolo, dopo girare il gioco dalla parte dell'autore e stampare per intero lo spazio di ricerca.

La coda gira il gioco dalla parte dell'autore, e lì il vocabolario torna a servire. È messa dopo apposta: la prima metà si chiude comunque.

Dove si romperebbe: il sistema non può né costruire né correggere nulla di tutto questo (`ideas/10 §6`), e la scheda funziona perché le cinque coppie le ha scelte una persona.

## Da riprendere alla rassegna

**Dare il risultato e chiedere l'operazione.** È una mossa di formato, non di enigmistica, e sposta la verifica dentro il foglio senza spostare il lavoro su chi legge, come invece fa girare il gioco dalla parte dell'autore. Da provare su tutte le forme del capitolo 12: quasi tutte hanno una versione «di che gioco si tratta» che è chiusa e autocorreggibile.

**Una consegna che è una biiezione porta con sé il proprio controllo.** Cinque numeri in cinque caselle: chi ne ha una in avanzo sa di aver sbagliato senza che nessuno glielo dica. Da cercare altrove nell'elenco, perché è una proprietà del formato e non del contenuto.

**Il confine della contiguità torna in tre discipline diverse.** L'enigmistica non sa se chiamare scambio o spostamento due lettere vicine; la distanza di Damerau–Levenshtein ammette la trasposizione solo se sono adiacenti; la linguistica distingue metatesi a contatto e a distanza. Tre campi che non si parlano tracciano la stessa linea. Da guardare alla rassegna: quando tre discipline concordano su un confine, quel confine probabilmente è nella cosa e non nella nomenclatura.

**La forma porta il nome di chi non la faceva.** Spooner ne avrebbe fatta una sola in vita sua. È un caso della trappola già scritta — le affermazioni più forti di una pagina sono le meno sostenute — e qui l'affermazione forte è l'eponimo stesso.

**Differenza dal termine di paragone.** Rispetto alla voce 321, antipodo, dove non si sceglie niente, qui si scelgono due posizioni fra *n*: lo spazio passa da 2 a 27 su una parola di otto lettere, e smette di stare su un foglio.
