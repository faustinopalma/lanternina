# L'enciclopedia delle forme

Trecentonovantacinque voci sui modi in cui si può chiedere a un adolescente di fare qualcosa. Ogni voce è una tecnica: come è fatta, da dove viene, che cosa se ne sa, e un esempio scritto per esteso che si può usare così com'è.

[L'elenco completo è in `INDICE.md`](INDICE.md), in quattordici capitoli. Chi non sa da dove cominciare può aprire la voce [73, foglio stampato](03-su-che-cosa-arriva-la-domanda/073-foglio-stampato/README.md): è di una famiglia che tutti conoscono, e mostra com'è fatta una voce.

## A che cosa serve

A trovare una forma che non si era considerata. Chi deve proporre qualcosa da fare — un genitore, un insegnante, chi scrive un gioco, chi progetta un esercizio — ne conosce una decina e usa sempre quelle. Qui ce ne sono 395, ognuna con la sua storia e con la sua parte fragile dichiarata.

Non è un elenco di cose consigliate e non è nemmeno un elenco di cose ammesse. Una mappa che contiene solo le strade che si percorrono non dice dove si è. Ci sono forme costose, forme che richiedono più persone, forme che su carta non stanno: ognuna dice dove si romperebbe.

## Com'è fatta una voce

Quattro righe di intestazione e sette sezioni, sempre le stesse e sempre in quest'ordine.

L'intestazione:

- **Numero** — quale voce è e in che capitolo sta.
- **Si chiama anche** — gli altri nomi della stessa cosa, compresi quelli inglesi e quelli che userebbe chi non sa il termine tecnico. È la riga che permette di trovare una voce partendo da come uno la chiama.
- **In una riga** — la forma in una frase.
- **Fonti** — che cosa è stato letto, con l'indirizzo e la data. E, quando è il caso, che cosa non è stato letto: *nessuna fonte letta; X è a memoria*. Questa è la riga che distingue un'enciclopedia da un ricordo ben scritto.

Le sezioni:

1. **Che cos'è** — la forma descritta in modo che si possa costruire. Non una definizione da dizionario: le parti mobili, e che cosa cambia se se ne toglie una.
2. **Da dove viene** — chi l'ha fatta e quando, dove ha vissuto prima. Quasi ogni forma porta con sé il contesto in cui è nata, e portarlo dentro senza accorgersene è il modo più comune di sbagliare.
3. **Varianti e parenti** — le altre facce della stessa cosa e le forme confinanti. Ogni rimando a un'altra voce porta **il numero e il nome**, perché chi legge una voce sola non ha in mente le altre.
4. **Che cosa se ne sa** — quello che è stato misurato, con la fonte e la data. Dove non è stato misurato niente, la voce lo dice: è un'informazione anche quella. Dove una cosa viene dalla memoria e non da una pagina letta, si legge **va verificato**.
5. **Esempi trovati** — casi reali, con la provenienza. Riscritti, mai copiati.
6. **Un esempio giocabile** — un esempio costruito apposta, per esteso, con sotto due o tre righe che dicono quale parte fa il lavoro. Dove la forma non sta su un foglio, l'esempio la mostra nella sua versione migliore e la voce dice dove si romperebbe. Ce l'hanno 394 voci su 395.
7. **Che cosa la rende interessante** — che cosa costa, dove sta la parte che fa il lavoro, che cosa resterebbe togliendone un pezzo.

Una voce sta in 124 righe, quella di mezzo; la più corta ne ha 65 e la più lunga 193.

## Le fonti

Le voci citano 1 304 pagine distinte, tutte di Wikipedia — 1 129 in inglese e 175 in italiano — lette fra il 30 agosto e il 2 settembre 2026. Nel corpo di una voce una fonte è nominata col suo titolo fra virgolette basse, «Crossword»; l'indirizzo sta una volta sola, nella riga **Fonti** dell'intestazione, perché quasi cinquemila collegamenti dentro la prosa la renderebbero illeggibile.

Le date sono quelle di lettura. Una pagina di Wikipedia cambia, e senza la data la citazione non dice niente.

Le sintesi sono nostre. Le fonti si citano, non si incollano.

## Come si legge

Una voce alla volta, e da sola. Non c'è un ordine obbligato e non c'è niente da leggere prima: i rimandi «voce N, nome» portano il nome accanto al numero proprio perché si possa saltare da una parte all'altra senza avere l'indice in mente.

I capitoli raggruppano per domanda, non per difficoltà. I primi quattro guardano la richiesta — com'è fatta, che cosa mette in moto, su che cosa arriva, com'è impacchettata. Dal quinto in poi guardano dei generi: enigmi, cacce, vincoli formali, didattica, meccaniche di gioco, chi assegna e chi giudica, come finisce, enigmistica classica, giochi matematici, percezione.

## Che cosa manca

Le forme collettive sono sottorappresentate. Molte voci descrivono qualcosa che ha bisogno di più di una persona, e sono state scritte pensando a chi ne ha una sola a disposizione: la variante per due c'è, ma quasi sempre come nota.

Le forme sonore e gestuali sono descritte e non messe in pratica, perché un foglio stampato non porta un suono né un gesto. Le voci lo dicono, e mostrano che cosa resta della forma quando la si obbliga a passare per la pagina.

Sessantadue voci contengono almeno una riga segnata **va verificato**: viene dalla memoria e non da una pagina letta. Sono dichiarate una per una invece di essere nascoste.

## Che cos'era prima

Questa è la parte pubblicabile di una ricerca interna al progetto Lanternina, compilata fra il 30 agosto e il 2 settembre 2026. La ricerca era scritta libera, senza applicare nessuna regola di disegno mentre compilava: filtrare mentre si elenca vuol dire elencare solo quello a cui si era già pensato.

Dalla versione pubblica sono usciti i quaderni di lavoro, i riferimenti agli strumenti interni e i vincoli di un prodotto che chi legge non conosce. Il resto — la storia, gli esempi, le misure con la loro provenienza, e le righe che dicono dove una forma si romperebbe — è quello che era.

## Verifica

```
python tools/enciclopedia_check.py
```

Controlla che ogni voce abbia le sette sezioni nell'ordine, l'intestazione completa, i rimandi col nome accanto al numero, e nessuna citazione che chi legge non possa aprire. Fallisce se non trova nessuna voce: un controllo che può passare su zero file non è un controllo.

L'indice si rigenera con `python tools/enciclopedia_indice.py`, che lo ricava da [docs/EXERCISE-FORMS.md](../docs/EXERCISE-FORMS.md) — l'elenco resta l'unica lista.
