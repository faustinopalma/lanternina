# Le forme

Una cartella per ogni modo di porre a un adolescente una cosa da fare. Trecentodieci, elencate in `docs/EXERCISE-FORMS.md`, che resta l'unica lista: una cartella qui esiste perché una voce esiste là, e `tools/forme_scaffold.py` costruisce l'albero da quel file.

Questa è la ricerca su cui poggia tutto il resto del progetto. I vincoli scritti in `.github/copilot-instructions.md §1` sono stati posti prima che qualcuno avesse fatto girare un pomeriggio, e diversi di essi vietano cose che nessuno intendeva vietare. **La ricerca serve anche a correggerli**, e quando una scheda trova un motivo per farlo lo scrive nella sezione «Che cosa cambia per noi», da dove poi si va a toccare la regola. Le sole voci che non si toccano per questa via sono quelle che parlano dell'adolescente e non del disegno del software.

## Che cosa contiene una scheda

Ogni cartella ha un `README.md` con sette parti, sempre le stesse.

- **L'intestazione** — numero, capitolo, come l'enciclopedia la classifica (`aperto`, `⚠ costoso`, `✗ chiuso`, `⊘ irraggiungibile`), la riga di glossa, e lo stato della ricerca.
- **Che cos'è** — la forma descritta in modo che si possa costruire. Non una definizione da dizionario: le parti mobili, e che cosa cambia se se ne toglie una.
- **Da dove viene** — chi l'ha fatta e quando, dove ha vissuto prima di arrivare qui. Serve perché quasi ogni forma porta con sé il contesto in cui è nata, e portarlo dentro senza accorgersene è il modo più comune di sbagliare.
- **Che cosa se ne sa** — quello che è stato misurato, con la fonte e la data. Dove non è stato misurato niente, la scheda lo dice: è un'informazione anche quella.
- **Esempi trovati** — casi reali, con la provenienza. Riscritti, mai copiati: quello che sta nel repository è nostro.
- **Una nostra versione** — un esempio costruito per questo sistema, con i suoi limiti veri: un display da quattro righe di quarantaquattro caratteri, fogli A4 stampati in bianco e nero, una persona sola, niente suono, niente rete in mano, e nessun esito da sbagliare. Se la forma non ci sta, l'esempio mostra dove si rompe.
- **Che cosa cambia per noi** — la conclusione operativa in poche righe: si usa, si usa così, non si usa e perché, oppure una regola del progetto è più stretta di quanto serva e va rivista.

## Come si fa la ricerca su una forma

1. Si cerca online. Le pagine scaricate stanno in `_reference/esercizi-e-sfide/`, che è gitignored perché sono testi di altri; `tools/fetch_exercise_sources.py` le prende e `tools/forme_text.py` le riduce a testo leggibile a pezzi. Quando una forma non è coperta dalle 74 pagine già prese, si cerca ancora e si aggiunge la fonte a quello script.
2. Si sintetizza. La sintesi è nostra: le fonti si citano con l'indirizzo e la data, non si incollano.
3. Si genera. Un esempio proprio, provato contro i limiti fisici, e non un esempio plausibile.
4. Si conclude. Anche quando la conclusione è «questa forma non serve a niente qui», che è una risposta e va scritta.

## Dove si è arrivati

`INDICE.md` ha l'elenco completo con lo stato di ciascuna, ed è generato: `python tools/forme_scaffold.py --index`. Una scheda si dichiara fatta cambiando la riga **Stato della ricerca** nella sua intestazione.

L'ordine con cui si procede non è il numero. Si comincia dalle forme che il progetto ha chiuso o marcato costose, perché sono quelle dove il vincolo iniziale rischia di essere sbagliato, e una forma tenuta fuori per un motivo che non regge è la perdita che non si vede.

## Che cosa questa ricerca non è

Non è un catalogo di cose da costruire. Molte forme qui dentro sono descritte con cura e non verranno usate mai, e alcune sono descritte proprio perché non vanno usate. Una mappa che contiene solo le strade che si percorrono non dice dove si è.
