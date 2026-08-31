# Indizio a scaglioni

- **Numero** 187 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Meccanismi da escape room»
- **Si chiama anche** aiuto a livelli, suggerimento graduato, scala di indizi, salvagente, aiuto a pagamento, *hint system*, *fading*
- **In una riga** l'aiuto arriva a livelli, come la scala a quattro pioli di questo formato.
- **Fonti** `escape-room.txt`, `it-escape-room.txt`, `worked-example-effect.txt`, `scaffolding.txt`, `strategy-guide.txt`, lette il 31 agosto 2026. Il problema dell'orto e i conti sulle aree sono nostri, verificati in `build/check_187.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

L'aiuto non è una cosa sola. È una scala: il primo gradino sposta l'attenzione, l'ultimo dà la soluzione, e in mezzo ci sono i gradini che fanno il lavoro vero.

Parti mobili:

- **Quanti gradini.** Sotto i tre la scala non è una scala; sopra i cinque i gradini si somigliano.
- **Che cosa fa ognuno.** I quattro che si ritrovano ovunque sono: dire dove guardare, dire che genere di cosa è, dare la struttura, dare la procedura.
- **Che cosa costa salire.** Tempo, un numero limitato di usi, oppure niente.
- **Chi decide che serve.** È la domanda che divide questa forma in due, e sotto c'è tutta la voce.
- **Se salire lascia traccia.** Un aiuto usato e non registrato è un aiuto che non è mai esistito, per chi guarda il risultato.

**La proprietà che la definisce è che l'ultimo gradino è la risposta.** Una scala di indizi finisce sempre nello stesso posto; quello che cambia è quanto in alto si è saliti. È l'unica forma raccolta il cui esito migliore è **non usarla**, e l'unica il cui uso è insieme il rimedio e la misura del problema.

## Da dove viene

**Dalle escape room, ed è una conseguenza obbligata della struttura, non un servizio.** `escape-room.txt` scrive che se i giocatori si bloccano «può esserci un meccanismo con cui chiedere un indizio»; che gli indizi arrivano scritti, in video, in audio, o da un conduttore o da un attore presente nella stanza; e che **ci possono essere limiti al numero di indizi, oppure una penalità come la perdita di tempo.** La stessa pagina registra che chi non finisce nel tempo «fallisce», ma che la maggior parte dei gestori cerca comunque di far divertire i clienti, e che alcune sedi concedono tempo in più o una visita accelerata a quello che restava.

**Quel paragrafo è la fattura di un difetto strutturale, ed è stato già identificato.** Alla voce 181, percorso lineare la catena ha un punto di rottura solo, e senza salvagente si ferma al primo passo che non viene; alla voce 182, percorso a imbuto il punto di rottura unico non c'è, e infatti l'imbuto non ha bisogno di aiuti. **Un sistema di indizi è quello che una struttura fragile deve comprarsi**, e il prezzo che le escape room hanno scelto — tempo, o un numero fisso di usi — dice che lo sanno.

**Nella didattica la stessa cosa esiste, ha un nome diverso e va nel verso opposto.** `worked-example-effect.txt` descrive il **fading**: si parte da un esempio completamente risolto e si tolgono via via i passi della soluzione, «per facilitare il passaggio dall'imparare su esempi risolti al risolvere problemi». La ragione per cui è necessario è misurata e si chiama **effetto di inversione dell'esperienza** — Kalyuga, Ayres, Chandler e Sweller (2000, 2001, 2003): studiare esempi risolti perde efficacia man mano che l'esperienza cresce, e per chi già sa diventa ridondante e dannoso. Il lavoro di riferimento sul come è Renkl, Atkinson e Große, *How fading worked solution steps works*, 2004.

**Una scala di indizi e un esempio sfumato sono lo stesso oggetto percorso nelle due direzioni.** L'esempio risolto parte dalla soluzione e la toglie; l'indizio a scaglioni parte da niente e la aggiunge. Coincidono al centro, e nessuna delle due letterature nomina l'altra.

**E la letteratura didattica dice la condizione che il nostro sistema non può soddisfare.** `scaffolding.txt`: perché una strategia si qualifichi come buon sostegno, quello che conta è se sia applicata **in modo contingente**, e se faccia parte di un processo di sfumatura e di trasferimento della responsabilità. *Contingente* vuol dire che risponde a quello che sta succedendo a chi impara. **Il sistema stampa un foglio e non sa che cosa succede a chi lo legge.**

Le guide strategiche dei videogiochi sono la versione commerciale della stessa cosa, e `strategy-guide.txt` registra che contengono di tutto — mappe complete con la posizione degli oggetti nascosti, spiegazioni degli enigmi, soluzioni passo per passo. **Non hanno gradini: sono l'ultimo gradino e basta.**

## Varianti e parenti

- **Scala a quattro gradini** — dove guardare, che genere di cosa è, la struttura, la procedura.
- **Indizio a pagamento** — costa tempo. È la forma standard nelle escape room.
- **Indizio contingente** — arriva quando qualcuno si accorge che serve. Richiede quel qualcuno.
- **Indizio a richiesta** — chi lavora decide, e la scala è stampata coperta.
- **Esempio sfumato** — la stessa scala percorsa al contrario, dalla soluzione al niente.
- **Soluzione e basta** — la guida strategica: un gradino solo, l'ultimo.
- **Voce 181, percorso lineare** — la struttura che ha bisogno di questa forma per non incepparsi.
- **Voce 182, percorso a imbuto** — la struttura che non ne ha bisogno, e la ragione per cui.
- **Voce 183, percorso aperto** — l'altra struttura che se ne può fare a meno.
- **Voce 86, interrogazione** — l'altra forma dell'elenco in cui esiste un foglio di chi conduce.

## Che cosa se ne sa

**Il sistema non sa se qualcuno si è fermato, e questa è la voce in cui il limite morde di più.** Non ha un orologio, non riceve niente finché non arriva una fotografia, e la fotografia arriva quando il foglio è finito — cioè esattamente nel caso in cui l'aiuto non serviva. **Un indizio contingente è fuori portata, e non per poco.**

**Quello che resta è una scala che chi legge apre da sé, e non è un ripiego: è un'altra forma.** Chi decide di salire un gradino sta dichiarando di essere fermo, e la dichiarazione è la parte utile. Un sistema che non può accorgersi di niente può però **stampare la domanda** e ricevere la risposta insieme al resto.

**Ne segue la sola mossa nuova che questa voce propone: il prezzo dell'aiuto non è il tempo, è scriverlo.** Nelle escape room salire costa minuti, e i minuti li conta un orologio che qui non c'è. Su un foglio l'unico costo disponibile è **lasciare traccia**, e ha il vantaggio di trasformare il costo in un dato: chi ha finito senza aiuti e chi ha finito con tre gradini hanno prodotto lo stesso risultato e due fogli diversi.

**I quattro gradini non sono arbitrari, e la loro struttura si legge nelle due letterature messe insieme.** Il primo sposta l'attenzione senza dire niente — è la stessa cosa della riga «il bastoncino non deve per forza restare dentro un numero» già usata alle voci 162, 163 e 168, e cioè togliere un divieto che nessuno ha imposto. Il secondo nomina il genere del problema. Il terzo dà la struttura, cioè le lettere e la relazione, che è il passo che il *fading* toglie per ultimo. Il quarto dà la procedura, e chi lo legge non sta più risolvendo.

**Una scala di indizi è insieme il rimedio e la misura del guasto.** Se molti arrivano al quarto gradino, il problema è troppo difficile; se nessuno apre il primo, gli indizi non servivano. **È il solo strumento raccolto in sette sessioni che produca, come effetto collaterale, la valutazione di sé stesso**, ed è quello che un sistema senza ritorno può usare al posto del ritorno che non ha.

**Non c'è, in nessuna delle fonti lette, un numero.** Quanti indizi convenga concedere, quanto tempo debba costarne uno, quanti gradini debba avere una scala: le pagine sulle escape room dicono che i limiti esistono e non dicono quali. **Va verificato**, e sarebbe uno dei pochi numeri utili di tutto il capitolo.

## Esempi trovati

Il limite dichiarato al numero di indizi, in molte escape room.

La penalità in tempo: chiedere un aiuto toglie minuti a quelli che restano.

L'indizio consegnato da un attore presente nella stanza, che è la variante contingente e richiede una persona.

Il tempo in più o la visita accelerata concessi a chi non ha finito, che è un quinto gradino dato dopo la fine.

L'esempio risolto a cui si tolgono i passi uno per volta, nella didattica, che è la stessa scala percorsa al contrario.

La guida strategica, che è la scala ridotta al solo ultimo gradino e venduta in libreria.

## Una nostra versione

> **L'orto e il muro**
>
> Hai dodici metri di rete e vuoi recintare un orto **il più grande possibile**. L'orto sta addossato a un muro dritto e lungo.
>
> ```
>   ████████████████████████████████████  ← il muro
>
>            l'orto sta qui sotto
> ```
>
> **Quanti metri quadrati riesci a recintare?**
>
> ```
>   ────────  metri quadrati
> ```
>
> ---
>
> **Se ti sei bloccato, qui sotto ci sono quattro aiuti.** Sono in ordine: il primo dice pochissimo, l'ultimo dice quasi tutto. **Non costano tempo e non costano niente. Costano una crocetta.**
>
> ```
>   □  AIUTO 1   Il muro fa una parte del lavoro. Quale?
>
>   □  AIUTO 2   Con il muro, la rete deve coprire tre lati
>                e non quattro.
>
>   □  AIUTO 3   Chiama y i due lati corti e x il lato lungo
>                il muro. Allora x + 2y = 12.
>
>   □  AIUTO 4   Prova y = 1, poi 2, poi 3, poi 4, poi 5.
>                Ogni volta calcola x e poi x per y.
> ```
>
> ---
>
> **Quando hai finito, tre righe. Sono la parte che serve a me.**
>
> ```
>   Fino a che aiuto sei arrivato?   □ nessuno  □ 1  □ 2  □ 3  □ 4
>
>   Quale ti ha fatto ripartire?     ────
>
>   Che cosa stavi provando a fare, prima di aprirlo?
>   ────────────────────────────────────────────────────────────
> ```
>
> ---
>
> **E adesso la cosa che vale la pena sapere.** Senza il muro, con gli stessi dodici metri di rete, l'orto più grande è un quadrato di tre per tre: **nove metri quadrati.** Con il muro sono **diciotto**. Il muro non ha aggiunto rete: ha tolto un lato, e ha raddoppiato l'orto.

Il problema è verificato in `build/check_187.py`. Con il muro, chiamando y i due lati corti, l'area è y per (12 − 2y): vale **10, 16, 18, 16, 10** per y da 1 a 5, e cercando ogni ventesimo di metro il massimo resta **18**, a y = 3. Senza muro, con perimetro 12, il massimo è **9**. Il rapporto è esattamente **2**.

I quattro aiuti sono i quattro gradini nominati sopra, e sono scritti in modo che ognuno lasci qualcosa da fare. Il quarto dà la procedura e non il risultato: chi lo legge deve ancora fare cinque moltiplicazioni. **Nessun gradino di questa scala dice diciotto**, ed è la sola regola di scrittura che una scala di indizi abbia.

Le crocette sono il prezzo. Non tolgono tempo, non tolgono punti, e non c'è nessun modo di verificare che siano state segnate onestamente — **e la voce non finge di potere.** Quello che ottengono è che un foglio finito porti scritto quanto è costato finirlo, e che due fogli identici nel risultato non lo siano più.

La domanda «che cosa stavi provando a fare, prima di aprirlo» è la sola cosa del foglio che vada oltre il problema. Non ha risposta sbagliata, e restituisce l'unica informazione che il sistema non potrebbe avere in nessun altro modo: **dove qualcuno era fermo, e con quale idea in testa.**

Dove si romperebbe: gli aiuti sono stampati in chiaro, quindi si leggono anche senza volerlo, e questo non si può evitare su un foglio. La versione con la piega — gli aiuti sul retro, o coperti da una linguetta da strappare — è meglio e costa una piega. **Sul pannello da quattro righe la forma migliora**, perché un aiuto per volta è la cosa che quattro righe fanno bene, e chiedere il gradino successivo è un gesto invece che uno sguardo. Ma il pannello non registra niente, e la traccia sparirebbe.

## Da riprendere alla rassegna

**Un indizio contingente è fuori portata, e la letteratura dice che la contingenza è la condizione.** Il sostegno vale se risponde a quello che sta succedendo a chi impara; il sistema stampa un foglio e non sa che cosa stia succedendo. **È il limite più netto che una fonte pedagogica abbia posto a questo progetto in sette sessioni**, e non si aggira con una scrittura migliore.

**Il prezzo dell'aiuto può essere lasciare traccia invece che perdere tempo.** Nelle escape room salire costa minuti; qui i minuti non ci sono, e l'unico costo disponibile è la crocetta. **Ha il vantaggio di trasformare il costo in un dato**, e trasforma un foglio finito in un foglio che dice quanto è costato finirlo. Da provare su tutte le forme che abbiano un aiuto.

**Una scala di indizi valuta sé stessa.** Se tutti arrivano al quarto gradino il problema è troppo difficile; se nessuno apre il primo gli indizi erano superflui. **È il solo strumento raccolto che produca la propria valutazione come effetto collaterale**, e per un sistema senza ritorno vale più dell'aiuto che dà.

**L'esempio sfumato e la scala di indizi sono lo stesso oggetto nelle due direzioni, e le due letterature non si nominano.** Il *fading* parte dalla soluzione e la toglie; l'indizio parte da niente e la aggiunge; si incontrano al terzo gradino, quello della struttura. **Alla rassegna vale la pena guardarle insieme**, perché la didattica ha misure — l'inversione dell'esperienza — che il mondo degli enigmi non ha.

**Nessun numero, e sarebbe utile.** Quanti aiuti, quanto costano, quanti gradini. Le fonti dicono che i limiti esistono e non dicono quali. **Va verificato.**
