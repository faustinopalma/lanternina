# Le forme

Una cartella per ogni modo di porre a un adolescente una cosa da fare. Trecentodieci, elencate in `docs/EXERCISE-FORMS.md`, che resta l'unica lista: una cartella qui esiste perché una voce esiste là, e `tools/forme_scaffold.py` costruisce l'albero da quel file.

Questa è la ricerca su cui poggia tutto il resto del progetto, e si fa **libera**. Mentre si compila l'elenco non si applica nessuna regola di questo progetto: una forma si descrive per quello che è, con la sua storia, i suoi esempi e quello che si sa di lei, anche se è una forma che qui non si userebbe mai. Filtrare mentre si elenca vuol dire elencare solo quello a cui si era già pensato, e sarebbe la fine della ricerca prima di cominciarla.

**La rassegna viene dopo**, quando l'elenco è completo: si guarderà forma per forma che cosa si tiene, che cosa no e perché, e solo alla fine si vedrà se qualche regola in `.github/copilot-instructions.md §1` va ridefinita. Fino ad allora niente è deciso. Le marcature ereditate dal primo giro — `✗`, `⚠`, `⊘` in `docs/EXERCISE-FORMS.md` — restano nell'intestazione delle schede **come promemoria di quello che si pensava allora**, non come verdetti.

Quello che si nota strada facendo va in `OSSERVAZIONI.md`, che è un quaderno di appunti per la rassegna e non un elenco di decisioni.

## Che cosa contiene una scheda

Ogni cartella ha un `README.md` con le stesse parti, sempre nello stesso ordine.

- **L'intestazione** — numero, capitolo, come la classificava il primo giro, la riga di glossa, e lo stato della ricerca.
- **Che cos'è** — la forma descritta in modo che si possa costruire. Non una definizione da dizionario: le parti mobili, e che cosa cambia se se ne toglie una.
- **Da dove viene** — chi l'ha fatta e quando, dove ha vissuto prima. Quasi ogni forma porta con sé il contesto in cui è nata, e portarlo dentro senza accorgersene è il modo più comune di sbagliare.
- **Varianti e parenti** — le altre facce della stessa cosa, e le forme confinanti da cui si distingue.
- **Che cosa se ne sa** — quello che è stato misurato, con la fonte e la data. Dove non è stato misurato niente, la scheda lo dice: è un'informazione anche quella.
- **Esempi trovati** — casi reali, con la provenienza. Riscritti, mai copiati: quello che sta nel repository è nostro.
- **Una nostra versione** — un esempio costruito da noi. Dove la forma è compatibile con quello che il sistema può stampare, l'esempio è giocabile; dove non lo è, l'esempio mostra la forma nella sua versione migliore e la scheda dice dove si romperebbe. **Non si scarta un esempio perché viola una regola del progetto.**
- **Da riprendere alla rassegna** — osservazioni, non conclusioni. Che cosa costerebbe, che cosa chiederebbe, dove sta la sua parte interessante, che cosa resterebbe se se ne togliesse un pezzo.

Le prime ventidue schede sono state scritte prima di questa decisione e la loro ultima sezione si chiama ancora «Che cosa cambia per noi» e suona conclusiva. Va letta come il resto: appunti per la rassegna, non deliberazioni.

## Come si fa la ricerca su una forma

1. Si cerca online. Le pagine scaricate stanno in `_reference/esercizi-e-sfide/`, che è gitignored perché sono testi di altri; `tools/fetch_exercise_sources.py` le prende e `tools/forme_text.py` le riduce a testo leggibile a pezzi. Quando una forma non è coperta dalle pagine già prese, si cerca ancora e si aggiunge la fonte a quello script.
2. Si sintetizza. La sintesi è nostra: le fonti si citano con l'indirizzo e la data, non si incollano.
3. Si genera. Un esempio proprio, e non un esempio plausibile.
4. Si annota. Anche quando l'annotazione è «qui non entrerebbe mai», che va scritta con il motivo e senza che questo tolga la forma dall'elenco.

## Dove si è arrivati

`INDICE.md` ha l'elenco completo con lo stato di ciascuna, ed è generato: `python tools/forme_scaffold.py --index`. Una scheda si dichiara fatta cambiando la riga **Stato della ricerca** nella sua intestazione. `--retemplate` riscrive gli stub ancora vuoti quando il modello cambia, e non tocca le schede già scritte.

## Che cosa questa ricerca non è

Non è un catalogo di cose da costruire, e non è nemmeno un elenco di cose ammesse. È una mappa, e una mappa che contiene solo le strade che si percorrono non dice dove si è.
