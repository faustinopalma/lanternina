# Rebus

- **Numero** 346 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Rebus e forme miste»
- **Si chiama anche** rebus, scrittura per immagini, principio del rebus, emoji
- **In una riga** immagini con lettere sopra, e la lettura produce una frase.
- **Fonti** `puzzle.txt`, presa il 30 agosto 2026; le convenzioni italiane sono a memoria
- **Stato della ricerca** fatta, 30 agosto 2026

## Che cos'è

Un disegno con delle lettere sopra alcuni elementi. Si legge il nome di quello che si vede, si inseriscono le lettere al posto giusto, e la sequenza continua di lettere che ne esce si spezza in un altro modo per dare una frase.

La forma italiana ha una convenzione precisa: le lettere sono stampate accanto o sopra la parte di disegno a cui si riferiscono, e il **diagramma** in fondo — *(3 5 2 6)* — dice come si spezza la soluzione.

Parti mobili:

- **Quante lettere sono date** rispetto a quante vengono dai disegni.
- **Se le figure sono ambigue di proposito.** Un disegno che può essere *cane* o *bracco* è la difficoltà vera.
- **Il tipo di lettura**: il nome dell'oggetto, il verbo dell'azione, il nome proprio.
- **La distanza fra la scena disegnata e la frase risolta**, che nei rebus riusciti è enorme.

## Da dove viene

Il nome viene dal latino *rebus*, «con le cose». La forma è antichissima come scrittura — il principio del rebus è il passo con cui quasi ogni sistema di scrittura ha smesso di disegnare le cose e ha cominciato a scriverne i suoni, dai geroglifici in poi.

Come gioco moderno è codificato nella tradizione italiana con le sue convenzioni grafiche, e ha una comunità di autori e disegnatori.

## Varianti e parenti

- **Rebus stereoscopico** (347) — due vignette che condividono elementi.
- **Rebus a domanda** (348) — la soluzione risponde a qualcosa che il disegno chiede.
- **Crittografia** (341–344) — lo stesso principio senza immagini.
- **Cambio di spaziatura** (345) — il meccanismo finale del rebus, isolato.
- **Scrittura rebus storica** — geroglifici, cuneiforme, e il *principio del rebus* come tappa nella storia della scrittura.
- **Emoji** — la scrittura rebus spontanea di oggi.
- **Droodle** (122) — disegno minimo con una lettura, ma comica invece che linguistica.

## Che cosa se ne sa

Fonte: `_reference/esercizi-e-sfide/puzzle.txt`, presa il 30 agosto 2026, che colloca il rebus fra i giochi di parole. La tradizione italiana con le sue convenzioni **non viene da lì** ed è mia: va verificata.

Due cose che si possono dire.

**È la forma dell'elenco più lontana da quello che il sistema sa fare.** Chiede di comporre lettere, contarle, e poi spezzarle in un punto diverso da dove sono state composte. Tre operazioni sulle lettere in fila, e ognuna è quella che un modello sbaglia. Non c'è versione parziale che si salvi.

**E chiede un disegno preciso.** Le figure di un rebus devono essere riconoscibili con un nome solo, che è il contrario di quello che un generatore di immagini garantisce. Un disegno che può essere letto in tre modi rende il rebus irrisolvibile invece che difficile.

Quindi è doppiamente fuori portata: nella lingua e nel disegno. Vale la pena averlo scritto per esteso, perché è il caso limite che definisce il confine.

## Esempi trovati

La forma canonica, descritta: un disegno con un uomo che dorme, la lettera R sopra la testa, un pesce con sopra AL. Si legge *R + [dorme] + AL + [pesce]*, e la sequenza si spezza altrove.

Dalla storia della scrittura: il nome di un re scritto con il disegno di un'ape e di una foglia, che si leggono per il loro suono e non per la cosa.

Da Leonardo: i rebus del Codice Atlantico, che sono la stessa cosa cinque secoli fa.

Dai messaggi di oggi: la sequenza di emoji che si legge ad alta voce e dice una frase, che nessuno chiama rebus e che lo è.

## Una nostra versione

Il sistema non può costruire un rebus. Può chiedere di costruirne uno, e la costruzione è più istruttiva della soluzione perché costringe a guardare come funziona la scrittura.

> **Come si scriveva prima di avere le lettere**
>
> Per scrivere il nome di una persona, quando le lettere non c'erano ancora, si disegnavano cose che *suonavano* come quel nome. Il disegno di un'ape non voleva dire ape: voleva dire il suono «a-pe».
>
> Prova a scrivere così **il tuo nome**, o quello di qualcuno di casa. Solo disegni, nessuna lettera.
>
> ```
>  ┌────────────────────────────────────────┐
>  │                                           │
>  │                                           │
>  │                                           │
>  └────────────────────────────────────────┘
> ```
>
> Sotto ogni disegno scrivi che cosa hai disegnato, così chi guarda sa che cosa deve leggere.
>
> Se una sillaba non ha nessun oggetto che le somigli, disegna una cosa che ci va vicino e segnala con un punto interrogativo. Succedeva anche a loro.

Non c'è niente da verificare e niente che il sistema debba generare: la consegna è una spiegazione storica e un rettangolo. La riga finale toglie il vicolo cieco più probabile — una sillaba senza oggetto — e lo fa dicendo che è un problema vecchio di cinquemila anni, il che è vero e cambia come si legge.

## Da riprendere alla rassegna

**È il caso limite del limite tecnico**, e per questo utile: fuori portata sia nella lingua sia nel disegno. Ogni volta che si vorrà stabilire se una forma è generabile, il rebus è il confronto contro cui misurarla.

**Il disegno che deve avere un nome solo** è un requisito che nessun'altra voce dell'elenco pone, ed è il contrario di quello che si chiede di solito a un'illustrazione. Da segnare, perché se un giorno servisse un disegno univoco il modo di ottenerlo non è chiedere meglio: è stampare il nome sotto.

**La spiegazione storica come consegna.** Raccontare da dove viene una forma è costato tre righe e ha sostituito la spiegazione della regola. Sembra funzionare meglio, e vale la pena vedere su quante altre voci si possa fare.

Da verificare: i rebus di Leonardo. **Le convenzioni grafiche e la notazione del diagramma sono state verificate il 30 agosto 2026** su `it-rebus.txt`, scrivendo la voce 119, rebus: i grafemi apposti alla vignetta vanno leggibili da sinistra a destra nel loro ordine e non sono mai più di tre consecutivi, e meno ce ne sono più il gioco è considerato elegante; l'insieme di un oggetto e dei suoi grafemi si chiama **chiave**; il diagramma numerico dà la lunghezza delle parole della soluzione e può riportare anche la prima lettura, ma di solito solo nei rebus difficili; esiste il **rebus muto**, senza lettere, in cui gli asterischi segnalano quali oggetti contano. La fonte distingue inoltre i rebus **statici**, che si risolvono nominando gli oggetti, dai **dinamici**, che chiedono di dire che cosa un oggetto fa rispetto a un altro.
