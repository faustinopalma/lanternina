# Le forme

Un'enciclopedia dei modi in cui si può chiedere a un adolescente di fare qualcosa. Una cartella per voce; le voci sono elencate in `docs/EXERCISE-FORMS.md`, che resta l'unica lista, e `tools/forme_scaffold.py` costruisce l'albero da quel file. L'elenco cresce quando si trova un filone che mancava.

**Si scrive libera.** Mentre si compila non si applica nessuna regola: una forma si descrive per quello che è, con la sua storia, i suoi esempi e quello che si sa di lei. Filtrare mentre si elenca vuol dire elencare solo quello a cui si era già pensato, e sarebbe la fine della ricerca prima di cominciarla. La rassegna — che cosa si tiene, che cosa no — viene quando l'elenco è completo, e da lì verranno le regole di disegno del progetto, che al momento non ci sono.

**È fatta per essere letta.** Non è una base di dati e non è un catalogo di parametri: è un testo, e una voce deve poter essere aperta da sola e capita da sola. Che cosa se ne farà il software è un passo successivo e non deve deformare questo.

Quello che si nota strada facendo va in `OSSERVAZIONI.md`, che è un quaderno di appunti per la rassegna e non un elenco di decisioni.

## Il contratto di una voce

Cinque righe di intestazione e sette sezioni, sempre le stesse e sempre in quest'ordine. `tools/forme_check.py` verifica quello che si può verificare a macchina e fallisce se manca qualcosa.

L'intestazione:

- **Numero** — quale voce è e in che capitolo sta. La scrive lo scaffold.
- **Si chiama anche** — gli altri nomi della stessa cosa, compresi quelli inglesi e quelli che userebbe qualcuno che non sa il termine tecnico. È la riga che permette di trovare una voce partendo da come uno la chiama.
- **In una riga** — la glossa dall'elenco.
- **Fonti** — che cosa è stato letto, con la data. E, se serve, che cosa non è stato letto: *nessuna fra le pagine locali; X è a memoria*. Questa è la riga che distingue un'enciclopedia da un ricordo ben scritto.
- **Stato della ricerca** — `non ancora fatta`, oppure `fatta` con la data.

Le sezioni:

1. **Che cos'è** — la forma descritta in modo che si possa costruire. Non una definizione da dizionario: le parti mobili, e che cosa cambia se se ne toglie una.
2. **Da dove viene** — chi l'ha fatta e quando, dove ha vissuto prima. Quasi ogni forma porta con sé il contesto in cui è nata, e portarlo dentro senza accorgersene è il modo più comune di sbagliare.
3. **Varianti e parenti** — le altre facce della stessa cosa e le forme confinanti. Un elenco puntato; ogni rimando a un'altra voce porta **il numero e il nome**, perché chi legge una voce sola non ha in mente le altre.
4. **Che cosa se ne sa** — quello che è stato misurato, con la fonte e la data. Dove non è stato misurato niente, la voce lo dice: è un'informazione anche quella. Dove una cosa viene dalla memoria e non da una pagina letta, si scrive **va verificato**.
5. **Esempi trovati** — casi reali, con la provenienza. Riscritti, mai copiati.
6. **Una nostra versione** — un esempio costruito da noi, per esteso e giocabile, con sotto due o tre righe che dicono quale parte fa il lavoro. Dove la forma non sta nel nostro formato, l'esempio la mostra nella sua versione migliore e la voce dice dove si romperebbe.
7. **Da riprendere alla rassegna** — osservazioni, non conclusioni. Che cosa costerebbe, dove sta la parte interessante, che cosa resterebbe togliendone un pezzo.

**La voce modello** è `02-che-cosa-mette-in-moto-la-risposta/054-misurare/README.md`. Chi comincia una sessione nuova legge questo file e quella voce, e ha tutto.

## Come si fa la ricerca su una forma

1. Si cerca. Le pagine scaricate stanno in `_reference/esercizi-e-sfide/`, che è gitignored perché sono testi di altri; `tools/fetch_exercise_sources.py` le prende e `tools/forme_text.py` le riduce a testo leggibile a pezzi. Quando una forma non è coperta dalle pagine già prese, si cerca ancora e si aggiunge la fonte a quello script.
2. Si sintetizza. La sintesi è nostra: le fonti si citano con l'indirizzo e la data, non si incollano.
3. Si genera. Un esempio proprio, e non un esempio plausibile.
4. Si annota. Anche quando l'annotazione è «qui non entrerebbe mai», che va scritta con il motivo e senza che questo tolga la forma dall'elenco.
5. Si controlla: `python tools/forme_check.py`.

## Come si lavora su più sessioni

Un capitolo per sessione, e non più di uno. Una sessione lunga perde il filo e comincia a ripetersi: le voci diventano più corte, gli esempi si somigliano, e i rimandi si fanno vaghi. Meglio chiudere e ricominciare.

All'inizio di una sessione: questo file, la voce modello, `OSSERVAZIONI.md`, e l'output di `forme_check.py`. Alla fine: le osservazioni nuove in `OSSERVAZIONI.md`, l'indice rigenerato, il controllo pulito, e un commit.

Ogni tanto, invece di scrivere voci nuove, una sessione va spesa a **verificare**. Le voci accumulano cose ricordate e non lette — ognuna segnata *va verificato* — e sopra una certa quantità l'enciclopedia smette di valere quello che dice di valere.

## Dove si è arrivati

`INDICE.md` ha l'elenco completo con lo stato di ciascuna, ed è generato: `python tools/forme_scaffold.py --index`. Una voce si dichiara fatta cambiando la riga **Stato della ricerca**. `--retemplate` riscrive gli stub ancora vuoti quando il modello cambia, e non tocca le voci già scritte.

## Che cosa questa ricerca non è

Non è un catalogo di cose da costruire, e non è nemmeno un elenco di cose ammesse. È una mappa, e una mappa che contiene solo le strade che si percorrono non dice dove si è.
