# Enigma di teoria dei giochi

- **Numero** 157 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi logici»
- **Si chiama anche** gioco risolto, strategia vincente, posizioni vincenti e perdenti, gioco di sottrazione, Nim, *combinatorial game*, *solved game*, *winning strategy*
- **In una riga** chi ha una strategia vincente.
- **Fonti** [Combinatorial game theory](https://en.wikipedia.org/wiki/Combinatorial_game_theory), [Nim](https://en.wikipedia.org/wiki/Nim), [Game theory](https://en.wikipedia.org/wiki/Game_theory), [Prisoner's dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma) e [Zero-sum game](https://en.wikipedia.org/wiki/Zero-sum_game), prese il 30 agosto 2026 da en.wikipedia; la tabella del gioco di sottrazione dell'esempio giocabile è calcolata a mano

## Che cos'è

Un gioco a due con regole brevissime, e una domanda che non è «come si gioca» ma **«chi vince, se tutti e due giocano bene».** Il compito non è vincere una partita: è dimostrare chi vincerebbe sempre.

Con la voce 158, enigma auto-referenziale chiude il capitolo dal lato astratto, e le due si somigliano in un punto: **si ragiona su un ragionamento.** Qui su quello di un avversario che ragiona come noi; là su una frase che parla di sé. La differenza con la voce 156, problema di scacchi è che lì l'avversario è scritto e le sue mosse sono un elenco chiuso; qui l'avversario è vivo e sceglie, e la strategia deve reggere a qualunque cosa scelga.

Parti mobili:

- **Se l'informazione è completa.** Se tutti e due vedono tutto e non c'è caso, il gioco è combinatorio e in linea di principio si risolve. Se c'è un dado o una carta coperta, si entra in un altro ramo della materia.
- **Se le mosse sono le stesse per tutti e due.** Se sì, il gioco è **imparziale** — il Nim; se no, è **partigiano** — gli scacchi, dove il Bianco non può muovere i pezzi neri.
- **Chi vince quando non si può più muovere.** È la convenzione: nel gioco normale perde chi non può muovere, nel gioco *misère* vince.
- **Quanti stati ha.** È la parte mobile che decide se la forma sta su un foglio. Un gioco con venti stati si analizza tutto; il Go no.
- **Che cosa si chiede.** Chi vince; oppure qual è la mossa vincente; oppure quali posizioni sono perdenti per chi deve muovere, che è la domanda che produce la risposta alle altre due.

## Da dove viene

Il capostipite è il **Nim**: due giocatori, dei mucchi di oggetti, e a ogni turno si tolgono quanti oggetti si vuole ma **da un mucchio solo.** Chi prende l'ultimo vince, oppure perde, a seconda della convenzione.

Le sue varianti si giocano dall'antichità, e la fonte è prudente sull'origine: si dice che venga dalla Cina — assomiglia molto al gioco *jiǎn-shízǐ*, «raccogliere sassi» — ma l'origine è incerta; i primi riferimenti europei sono dell'inizio del Cinquecento. **Il nome è di Charles L. Bouton, dell'università di Harvard, che nel 1901 ne pubblicò anche la teoria completa**; perché lo abbia chiamato così non è mai stato del tutto spiegato, e l'Oxford English Dictionary lo fa venire dal verbo tedesco *nimm*, «prendi».

La teoria dei giochi combinatori nasce da lì. Negli anni Trenta il **teorema di Sprague-Grundy** mostra che **ogni gioco imparziale equivale a un mucchio di Nim**, che è una unificazione notevole: giochi che sembrano diversissimi sono lo stesso gioco travestito. Negli anni Sessanta **Elwyn Berlekamp, John Conway e Richard Guy** estendono la teoria ai giochi partigiani; il primo libro pubblicato è *On Numbers and Games* di Conway, 1976, che introduce i numeri surreali, e poi *Winning Ways for your Mathematical Plays*, 1982. Conway dichiarò che l'ispirazione gli venne guardando i finali di Go, che spesso si scompongono in somme di finali più semplici isolati in punti diversi della scacchiera.

L'altro ramo — quello che la fonte chiama teoria dei giochi «economica» — si occupa di probabilità e informazione incompleta, e usa l'utilità e gli equilibri. Il suo esempio più noto è il **dilemma del prigioniero**, ideato da **Merrill Flood e Melvin Dresher** alla RAND Corporation nel **1950**: due agenti razionali, ognuno dei quali può collaborare per il bene comune o tradire per il proprio. Flood è la stessa persona che negli anni Trenta si era messo a studiare il problema del commesso viaggiatore cercando di organizzare dei percorsi di scuolabus, alla voce 153, problema di ottimizzazione.

## Varianti e parenti

- **Il Nim normale e il Nim *misère*** — chi prende l'ultimo oggetto vince, oppure perde. Cambia solo l'ultima mossa, e cambia tutta la strategia.
- **I giochi di sottrazione** — un mucchio solo, e un insieme dichiarato di quantità che si possono togliere.
- **Il tris** — risolto: giocando bene si finisce sempre in parità.
- **La dama** — dichiarata risolta *debolmente* nel **2007**, con la conclusione che il gioco perfetto finisce in parità; la dimostrazione ha richiesto il calcolatore.
- **Hackenbush**, **Toads and Frogs**, **Domineering** — i giochi che *Winning Ways* usa come esempi introduttivi. Di Toads and Frogs la fonte annota una cosa che ci riguarda: **a differenza degli altri, una posizione si rappresenta con una breve stringa di caratteri**, quindi si stampa e si scrive senza disegnare niente.
- **Il dilemma del prigioniero** e i **giochi a somma zero** — l'altro ramo, dove non si cerca una strategia vincente ma un equilibrio.
- **Voce 367, gioco combinatorio imparziale** — nel capitolo 13, giochi matematici e ricreativi, ed è dove il Nim sta come contenuto: la somma di Nim, Sprague-Grundy, i numeri surreali. **Qui sta come forma di pagina: un gioco stampato la cui analisi è l'esercizio.** Il confine è quello già fissato, e in questo caso è particolarmente sottile, perché la strategia del Nim si scrive in binario e quello è matematica.
- **Voce 156, problema di scacchi** — l'avversario scritto invece che vivo.
- **Voce 104, gioco da tavolo** — il supporto.
- **Voce 146, enigma di cappelli** — dove si concordava una strategia prima e la si verificava su tutti i casi. È la stessa struttura.
- **Voce 152, problema impossibile** — l'altra voce del capitolo che chiede una dimostrazione invece di una risposta.

Con il capitolo 12, giochi di parole e enigmistica italiana non c'è nessun contatto.

## Che cosa se ne sa

**Un gioco può essere «risolto», ed è un termine tecnico.** Il tris è risolto: il gioco ottimo da tutte e due le parti dà sempre parità. La dama è risolta *debolmente* dal 2007 e dà parità anch'essa, **ma la dimostrazione ha richiesto il calcolatore.** Molti giochi reali restano troppo complessi: analizzare una posizione, dice la fonte, vuol dire trovare la migliore sequenza di mosse per tutti e due i giocatori fino alla fine, «e questo diventa estremamente difficile per qualunque cosa più complicata dei giochi semplici».

**Il Nim è completamente risolto, per qualunque numero di mucchi e di oggetti**, e c'è un modo facilmente calcolabile di sapere chi vincerà e quali mosse vincenti ha a disposizione. È una delle poche cose dell'elenco di cui si possa dire.

**La distinzione fra giochi imparziali e partigiani è la più utile della voce.** In un gioco imparziale le mosse a disposizione sono le stesse per tutti e due, quindi la posizione è tutto e chi deve muovere non conta; in un gioco partigiano ognuno ha i propri pezzi. **Solo i giochi imparziali si riducono al Nim.** Ne segue che gli scacchi, la dama e il Go non sono riconducibili a un mucchio, e per questo sono difficili.

**Il gioco *misère* non è il gioco normale al contrario.** La fonte è netta: tutti i giochi imparziali a gioco normale hanno un valore di Nim, ma «questo non è il caso sotto la convenzione *misère*», e solo i giochi *docili* si possono giocare con la stessa strategia del Nim *misère*. **Cambiare chi vince all'ultima mossa non è un dettaglio: è un altro gioco**, e a volte molto più difficile.

**C'è un modo di dimostrare che qualcuno ha una strategia vincente senza trovarla.** La fonte lo nomina fra i risultati teorici tipici della materia: **l'argomento del furto di strategia**. È il parente più stretto delle dimostrazioni di impossibilità della voce 152, problema impossibile, e ha una proprietà che l'enciclopedia non aveva ancora incontrato: **dice che una cosa esiste senza mostrarla.**

**La distinzione fra «giochi da matematici» e «giochi da giocare» è dichiarata**, e la fonte la usa come categoria: i *mathgames* interessano per l'esplorazione teorica, i *playgames* si giocano per divertimento e per competizione. **Il Nim sta in tutte e due**, ed è probabilmente per questo che è il più adatto a un foglio.

**Nel dilemma del prigioniero il numero delle partite cambia quello che è razionale fare.** Flood e Dresher, nel 1950, invitarono l'economista Armen Alchian e il matematico John Williams a giocare cento mani, e osservarono che i due sceglievano spesso di collaborare. Interrogato sul risultato, **John Nash osservò che il comportamento razionale nella versione ripetuta può essere diverso da quello della versione a mano singola.** È il punto in cui la teoria comincia a spiegare come possa emergere la collaborazione. Per un foglio di casa vale la pena tenerlo: **la stessa situazione giocata una volta o dieci non è la stessa situazione.**

**Le macchine che giocano a Nim sono più vecchie dei calcolatori.** Alla Fiera mondiale di New York del **1939** la Westinghouse espose il **Nimatron**; dall'11 maggio al 27 ottobre 1940 pochissime persone riuscirono a batterlo, e a chi ci riusciva veniva data una moneta con scritto *Nim Champ*. La Ferranti ne costruì uno per il Festival of Britain del 1951. Nel 1952 tre ingegneri della W. L. Maxson Corporation ne fecero uno da 23 chili che vinceva regolarmente. **Ne è stato descritto anche uno costruito con il Meccano di legno.**

**Nessuna misura su chi impara.** Nessuna delle pagine lette dice quanto ci metta una persona a scoprire la strategia del Nim, né a che età. Si legge però una cosa di didattica: il tris è ancora usato per insegnare i concetti fondamentali dell'intelligenza artificiale nei giochi agli studenti di informatica.

## Esempi trovati

Dal Nim classico: tre mucchi da tre, quattro e cinque oggetti, e due giocatori che alternano.

Dal Nimatron, 1940: sei mesi di fiera, e una moneta per chi lo batteva.

Da *L'anno scorso a Marienbad*, 1961: una versione del Nim giocata nel film, dove — annota la fonte — ha anche un'importanza simbolica.

Da Martin Gardner: la rubrica *Mathematical Games* del febbraio 1958 su *Scientific American* è dedicata al Nim.

Da Conway: i finali di Go che si scompongono in somme di finali più semplici, e da lì la teoria dei giochi partigiani.

Da Toads and Frogs: una posizione che si scrive come una stringa di caratteri.

## Un esempio giocabile

Il foglio non può far giocare due persone e poi dire chi ha vinto: quello lo fa il gioco. Quello che può fare è **stampare un gioco abbastanza piccolo perché lo si possa risolvere tutto**, e dare la tabella su cui si risolve. Sedici righe bastano.

> **Il gioco dei quindici**
>
> Quindici fiammiferi in fila. Due giocatori a turno ne prendono **uno, due o tre**. Chi prende l'ultimo **vince**.
>
> ```
>  ▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮
> ```
>
> Giocaci due o tre volte con qualcuno, senza pensarci troppo. Poi lascia stare i fiammiferi, perché la domanda non è chi vince una partita.
>
> ```
>  Se tutti e due giocano nel modo migliore possibile,
>  vince chi comincia o chi risponde?
> ```
>
> ---
>
> **Si può sapere, e si sa riempiendo questa tabella dall'alto.** Ogni riga dice: se davanti a te ci sono *n* fiammiferi e tocca a te, sei messo bene o male?
>
> ```
>   fiammiferi │ chi deve muovere...  │ perche'
>   davanti a  │                      │
>   chi muove  │                      │
>  ────────────────────────────────────────────────────
>       0      │  PERDE               │ non c'e' piu'
>              │                      │ niente: l'ha
>              │                      │ preso l'altro
>       1      │  ────────            │ ─────────────
>       2      │  ────────            │ ─────────────
>       3      │  ────────            │ ─────────────
>       4      │  ────────            │ ─────────────
>       5      │  ────────            │ ─────────────
>       6      │  ────────            │ ─────────────
>       7      │  ────────            │ ─────────────
>       8      │  ────────            │ ─────────────
>       9      │  ────────            │ ─────────────
>      10      │  ────────            │ ─────────────
>      11      │  ────────            │ ─────────────
>      12      │  ────────            │ ─────────────
>      13      │  ────────            │ ─────────────
>      14      │  ────────            │ ─────────────
>      15      │  ────────            │ ─────────────
> ```
>
> **La regola per riempirla, e non ce n'è altra:**
>
> ```
>  Da n fiammiferi puoi lasciarne n-1, n-2 o n-3.
>
>  - se ALMENO UNA di quelle tre righe, piu' in alto,
>    dice PERDE, allora questa riga dice VINCE:
>    ti basta lasciare l'altro in quella posizione;
>
>  - se TUTTE E TRE dicono VINCE, allora questa riga
>    dice PERDE: comunque tu muova, metti l'altro
>    in una posizione buona.
> ```
>
> Ogni riga si decide guardando solo le righe che hai già riempito. Non c'è niente da indovinare e non c'è niente da provare: **quando arrivi in fondo, sai chi vince, e lo sai per tutte le partite che si potrebbero mai giocare.**
>
> Guarda la colonna quando è finita. **Le righe che dicono PERDE hanno una cosa in comune.** Scrivila:
>
> ```
>  ────────────────────────────────────────────────────
> ```
>
> Adesso torna dalla persona con cui hai giocato e non perdere più.
>
> ---
>
> **E poi cambia una regola sola.** Adesso se ne possono prendere **uno, due, tre o quattro**. Rifai la tabella su un foglio a parte. **Le righe che dicono PERDE hanno ancora qualcosa in comune, ma non è più la stessa cosa.**
>
> ```
>  con 1-2-3 le posizioni perdenti sono ─────────────
>  con 1-2-3-4 le posizioni perdenti sono ───────────
>  e allora, se se ne potessero prendere da 1 a 9,
>  sarebbero ────────────────────────────────────────
> ```

**La tabella è stata calcolata a mano ed è questa.** Zero perde. Uno, due e tre vincono, perché si prende tutto. Quattro perde, perché qualunque cosa si faccia si lascia l'altro con uno, due o tre. Cinque, sei e sette vincono, perché si può lasciare quattro. Otto perde. Nove, dieci e undici vincono. Dodici perde. Tredici, quattordici e quindici vincono. **Le posizioni perdenti sono i multipli di quattro**, e con quindici fiammiferi **vince chi comincia**, prendendone tre e lasciandone dodici. Con la regola da uno a quattro le posizioni perdenti diventano i multipli di cinque, e in generale, potendone prendere da uno a *k*, sono i multipli di *k*+1 — l'ultima riga del foglio chiede proprio quello, e la risposta per uno-nove è i multipli di dieci.

La tabella è la verifica esaustiva già raccolta alla voce 146, enigma di cappelli, in una forma nuova: **non è un elenco di casi, è una catena.** Ogni riga si giustifica con quelle sopra, e la prima si giustifica da sola. Sedici righe coprono tutte le partite possibili — che sono molte di più di sedici — e questo è il punto: **si dimostra una cosa su un numero enorme di partite guardando sedici posizioni.**

Nessuno deve sapere la risposta. **La regola di riempimento è una procedura che non richiede fiducia**, e chi la applica ottiene la risposta senza che il foglio gliela dica; chi sbaglia una riga se ne accorge perché la regolarità in fondo alla colonna non compare. È lo stesso controllo dell'errore nel materiale già visto alla voce 148, enigma induttivo, dove la colonna delle somme doveva contenere esattamente una ripetizione.

L'ultima parte — cambiare la regola e rifare la tabella — è la mossa che trasforma una risposta in una legge. **Due tabelle danno due risposte; la terza domanda chiede la regola, e a quel punto la si può scrivere senza calcolarla.** È lo stesso passo dell'induzione osservato alla voce 149, enigma di successione, con la differenza che qui la regola non è arbitraria: si può dimostrare.

Su un pannello di poche righe corte ci stanno il gioco e la domanda — «quindici fiammiferi, se ne prendono 1, 2 o 3, vince chi prende l'ultimo: chi vince?» —, e per una volta la consegna sul pannello è completa. La tabella no.

## Che cosa la rende interessante

**Una tabella di sedici righe dimostra una cosa su un numero enorme di partite.** Non è un campione e non è un elenco di casi: è una catena, in cui ogni riga si appoggia alle precedenti. È **la terza forma di verifica esaustiva raccolta** — dopo l'elenco delle disposizioni della voce 146, enigma di cappelli e la colonna dei conti della voce 148, enigma induttivo — ed è la più potente delle tre, perché il numero delle cose dimostrate non ha niente a che vedere con il numero delle righe. Da provare ovunque ci sia una struttura che cresce un passo per volta.

**Cambiare un parametro e rifare il conto trasforma una risposta in una legge.** Uno-due-tre dà i multipli di quattro; uno-due-tre-quattro dà i multipli di cinque. Due tabelle e la terza si scrive senza calcolarla. **Costa una riga di consegna e produce l'unica cosa che vale la pena portarsi via**, ed è applicabile a ogni forma dell'elenco che abbia un numero dentro.

**C'è un modo di dimostrare che una strategia esiste senza trovarla.** L'argomento del furto di strategia. L'enciclopedia non aveva niente del genere: tutte le sue verifiche mostrano una cosa, questa dice che c'è. Se una dimostrazione di esistenza pura possa stare su un foglio resta da capire, e sarebbe un'idea che non si incontra da nessun'altra parte.

**Cambiare chi vince all'ultima mossa cambia tutto il gioco.** Nel Nim *misère* la teoria che funziona per il gioco normale smette di funzionare. È il caso più netto raccolto di **una regola marginale che non è marginale**, e riguarda ogni consegna in cui si decida come si finisce.

**Una macchina che gioca a Nim è del 1939, e i giochi risolti si insegnano ancora.** Il Nimatron alla fiera di New York, la moneta *Nim Champ*, i tre ingegneri e i loro ventitré chili. Vale la pena notare che **la prima cosa a cui si è fatta giocare una macchina è il gioco che si può risolvere del tutto**, e che il tris è ancora oggi il primo esercizio di chi impara a far giocare un programma.

**Una posizione che si scrive come una stringa di caratteri.** Toads and Frogs. Dove il canale testuale è largo e quello grafico è stretto è la stessa osservazione già fatta alla voce 127, parole crociate senza schema e alla voce 155, nonogramma / picross, e adesso i casi sono tre: **i giochi il cui stato si scrive in una riga si possono portare avanti fra una consegna e l'altra.**
