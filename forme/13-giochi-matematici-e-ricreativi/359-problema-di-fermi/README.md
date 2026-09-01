# Problema di Fermi

- **Numero** 359 nell'enciclopedia, capitolo 13 — Giochi matematici e ricreativi
- **Si chiama anche** stima di Fermi, domanda di Fermi, Fermi question, Fermi quiz, problema d'ordine di grandezza, calcolo sul retro della busta, back-of-the-envelope calculation, guesstimate, stima a spanne
- **In una riga** stimare a spanne una quantità che nessuno sa, scomponendola. *Quanti accordatori di pianoforte ci sono a Chicago.*
- **Contratto** voce breve
- **Fonti** `fermi-problem.txt`, `it-problema-di-fermi.txt`, `back-of-the-envelope.txt`, `order-of-magnitude.txt`, `enrico-fermi.txt`, lette il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Una domanda a cui non si può rispondere guardando da nessuna parte, e a cui si risponde lo stesso spezzandola in fattori che si sanno indovinare. Il risultato non è un numero: è un ordine di grandezza, e la forma dichiara di volere solo quello.

Le parti mobili:

- **La catena.** Quanti fattori si moltiplicano. Ognuno è una quantità su cui chi risponde ha un'opinione, anche senza saperla.
- **La tolleranza dichiarata.** `order-of-magnitude.txt` la definisce in modo controllabile: due numeri stanno entro un ordine di grandezza se il rapporto fra il più grande e il più piccolo non supera dieci.
- **Che cosa si consegna.** Il numero, oppure la catena. Sono due compiti diversi, e il secondo è l'unico che qualcuno possa correggere.
- **Se si chiede anche un intervallo.** `fermi-problem.txt` dice che le stime di Fermi «comportano tipicamente ipotesi motivate sulle quantità e sulla loro varianza o sui loro estremi». Chiedere il minimo e il massimo insieme al numero cambia il compito.

La glossa dell'elenco dice «una quantità che nessuno sa», e le fonti dicono un'altra cosa: `it-problema-di-fermi.txt` scrive «quantità che sembrano impossibili da calcolare, date le limitate informazioni disponibili». Gli accordatori di Chicago si possono contare sull'elenco telefonico; quello che manca è a chi risponde, in quel momento. **È una differenza che conta, perché sposta la forma da «non si sa» a «non lo so io adesso», e la seconda si può porre su qualunque cosa.**

## Da dove viene

Dal fisico Enrico Fermi, per la sua abitudine di arrivare a numeri quasi giusti senza dati. Il caso documentato è il test Trinity del 16 luglio 1945: lasciò cadere pezzi di carta mentre passava l'onda d'urto, misurò a passi quanto erano stati spostati e ne ricavò la potenza della bomba (`enrico-fermi.txt`, `fermi-problem.txt`, `back-of-the-envelope.txt`, tutte e tre lette il 1 settembre 2026).

Il nome inglese della pratica generale è più vecchio e più largo: *back-of-the-envelope calculation*, il conto fatto sul retro di una busta. `back-of-the-envelope.txt` lo definisce «più di un'ipotesi ma meno di un calcolo accurato», e ne elenca casi che non hanno niente a che fare con la fisica: il calcolo di una pagina con cui Arnold Wilkins mostrò a Robert Watson Watt che il raggio della morte tedesco era impossibile — e da lì venne il radar —, la curva di Laffer disegnata su un tovagliolo da bar nel 1974, il protocollo BGP schizzato nel 1989 su «tre tovaglioli macchiati di ketchup», UTF-8 progettato su una tovaglietta da Ken Thompson e Rob Pike.

Come esercizio scolastico esiste una gara con questo nome, la Fermi Competition, e `fermi-problem.txt` ne riporta tre domande: quanta acqua si porterebbe a ebollizione convertendo in calore la massa di un cucchiaino d'acqua; di quanto si scalda il fiume Thames passando la diga di Fanshawe; qual è la massa di tutte le automobili rottamate in Nord America questo mese.

## Varianti e parenti

- **Stima con estremi** — si chiede il numero, e anche il più piccolo e il più grande che si accetterebbero.
- **Stima al contrario** — dato il risultato, si chiede quale fattore lo ha fatto sbagliare.
- **Equazione di Drake** — la stessa catena moltiplicativa applicata al numero di civiltà nella galassia; la nominano sia `fermi-problem.txt` sia `it-problema-di-fermi.txt`.
- **Analisi dimensionale** — arrivare all'ordine di grandezza dalle sole unità di misura, senza indovinare niente. `fermi-problem.txt` la dà come strada alternativa.
- **Voce 54, misurare** — lì si confronta una grandezza con un'unità e si ottiene un numero; qui non si misura niente e il numero viene lo stesso.
- **Voce 340, quesito narrativo** — l'altro quesito in prosa dell'elenco che si verifica ragionando invece che sapendo.
- **Voce 114, indovinello dell'anno** — la stessa aritmetica annidata, usata per nascondere invece che per stimare.
- **Voce 8, scala di accordo (Likert)** — la misura senza unità, quando basta l'ordine e il numero non serve.

## Che cosa se ne sa

**La catena di Chicago, rifatta.** `it-problema-di-fermi.txt` stampa le sei ipotesi per esteso: cinque milioni di abitanti, due persone per casa, un pianoforte ogni venti case, un'accordatura all'anno per pianoforte, due ore per accordatura, cinquanta settimane da cinque giorni da otto ore. Rifacendo i conti in `build/check_359.py`: 125 000 accordature all'anno, 1 000 accordature per accordatore, **125 accordatori.** I numeri della fonte tornano tutti e tre.

**Perché funziona, con il numero.** `fermi-problem.txt` dà l'argomento e non lo lascia a parole: moltiplicare stime equivale a sommare logaritmi, gli errori si comportano come una passeggiata casuale, e lo scarto cresce come la radice del numero dei passi invece che come il numero dei passi. La fonte fa il conto su nove passi ciascuno sbagliato di un fattore due: nel caso peggiore si sbaglia di 2⁹ = 512, in pratica di 2³ = 8. Sulla catena di Chicago, che ha sei fattori, lo stesso conto dà **un fattore 64 nel peggio contro un fattore 5,5 in media**: la scomposizione non aggiunge errore, lo divide. Rifatto in `build/check_359.py`.

**Due fonti in casa danno due numeri diversi per la stessa cosa, e non cambia niente.** La potenza reale di Trinity è 21 kilotoni secondo `fermi-problem.txt` e 18,6 kilotoni secondo `back-of-the-envelope.txt` e `enrico-fermi.txt`: le tre pagine **discordano del 12.9%**, e due su tre stanno sul valore più basso. La stima di Fermi era 10 kilotoni, cioè un fattore 2,1 dal primo numero e 1,86 dal secondo: **entro un ordine di grandezza in tutti e due i casi**, che è esattamente quello che la forma dichiara di volere. È il primo caso, nelle 359 voci scritte, in cui una discordanza fra fonti non tocca l'affermazione, perché l'affermazione porta con sé la propria tolleranza. Nella riga «Fonti» resta segnata la discordanza, non risolta.

**Dove sta la verifica: da nessuna parte.** È l'unica delle sei voci di questo blocco in cui chi propone non può scrivere la risposta prima di porre la domanda, e la sola in cui non esiste un insieme di casi da provare. Le due cose sono la stessa cosa: **quando non c'è niente da enumerare non c'è niente da controllare.** Il vincolo del progetto — chiedere solo qualcosa di cui si è già scritta la risposta, `ideas/10 §8` — morde qui e in nessun'altra voce del blocco.

## Esempi trovati

Da `it-problema-di-fermi.txt`: gli accordatori di pianoforte di Chicago, con le sei ipotesi e i tre passaggi.

Da `enrico-fermi.txt` e `back-of-the-envelope.txt`: i pezzi di carta lasciati cadere a Trinity, e la distanza misurata a passi.

Da `fermi-problem.txt`: le tre domande della Fermi Competition, che chiedono un volume, una temperatura e una massa, tutte con l'unità dichiarata fra parentesi.

Da `back-of-the-envelope.txt`: il calcolo di una pagina di Arnold Wilkins sul raggio della morte, che rispose «impossibile» e aprì la strada al radar; e i tovaglioli di BGP, di UTF-8 e della curva di Laffer.

Da `fermi-problem.txt`: il negozio di attrezzature per accordatori che avrebbe bisogno di diecimila clienti, e la stima che dice di cambiare mestiere prima di aprirlo. È l'unico esempio in cui la stima serve a decidere.

## Una nostra versione

> **Quante volte si apre la porta**
>
> Non lo sa nessuno in questa casa, e non c'è niente da guardare. Si fa lo stesso, e si fa due volte per strade diverse.
>
> ```
>  Quante volte si apre la porta, in un anno?
>
>  PRIMA STRADA
>    persone che vivono qui              ......
>    uscite di ognuna, al giorno         ......
>    giorni in un anno                   ......
>    i tre moltiplicati, poi per due     ......
>
>  SECONDA STRADA
>    volte che l'ho sentita, oggi        ......
>    ore in cui l'ho ascoltata           ......
>    ore da sveglio, in un anno          ......
>    primo diviso secondo, per il terzo  ......
>
>  I DUE TOTALI
>    il grande diviso il piccolo         ......
>
>  Meno di dieci: le due strade concordano.
> ```
>
> Le due strade non useranno nessun numero in comune. Se arrivano vicine, vuol dire qualcosa.

La forma non ha una risposta da correggere, e il foglio ne costruisce una: **due catene indipendenti sulla stessa quantità si controllano a vicenda**, e il criterio di accordo è quello dichiarato dalla fonte — un rapporto sotto dieci. Il «poi per due» della prima strada è l'unico passaggio dato: chi esce, rientra.

## Da riprendere alla rassegna

**È la voce del blocco in cui la variabile vale meno, ed è il termine di paragone delle altre cinque.** La variabile è *dove sta la prova che si è finito*: qui da nessuna parte; alla voce 360, rompicapo classico in una risposta che l'autore pubblica; alla voce 361, crittarismo (alfametica) e alla voce 362, quadrato magico dentro il materiale, rifacendo il conto; alla voce 363, problema di parità e alla voce 364, invariante dentro l'argomento stesso, che si controlla da sé.

**Chiedere due stime invece di una sposta la verifica da nessuna parte a dentro il materiale, e costa una riga.** È la mossa più economica trovata finora per una forma senza risposta, e va provata su tutte le altre forme che ne sono prive — il censimento del controllo dell'errore ne conta circa la metà.

**Una tolleranza dichiarata rende innocua una discordanza fra fonti.** Vale oltre questa voce: quando un'affermazione porta scritto entro quanto vale, due fonti che non concordano possono essere tenute tutte e due. Da guardare come modo di scrivere, non solo come proprietà di questa forma.

**Il conto sul retro della busta non è una forma scolastica.** Radar, BGP, UTF-8, la curva di Laffer: quattro casi in cui il conto approssimativo è stato la decisione. Se questa forma entra in casa, entra come modo di decidere e non come esercizio.

