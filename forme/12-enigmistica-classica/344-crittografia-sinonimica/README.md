# Crittografia sinonimica

- **Numero** 344 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Crittografie»
- **Si chiama anche** sinonimica, crittografia a sinonimo, crittografia di tipo misto
- **In una riga** la soluzione è un sinonimo dell'esposto, letto diversamente.
- **Contratto** voce breve
- **Fonti** `it-crittografia-gioco.txt`, `it-gioco-enigmistico.txt`, `it-sinonimia.txt`, `synonym.txt`, lette il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

La macchina è quella della voce 341, crittografia pura: esposto, prima lettura, seconda lettura fatta delle stesse lettere con gli spazi altrove, diagramma a due lati. Quello che si aggiunge è **un passaggio obbligato attraverso un sinonimo**.

`it-crittografia-gioco.txt`, presa il 1 settembre 2026, lo scrive così: la sinonimica «richiede, a differenza di quella [pura], un preciso riferimento concettuale: per determinare la chiave è infatti necessario introdurre un sinonimo dell'esposto». Chi risolve non può limitarsi a descrivere quello che vede: deve prima chiamare l'esposto con un altro nome, e solo quel nome si lascia rispaziare.

**La riga dell'elenco sposta il sinonimo nel posto sbagliato.** «La soluzione è un sinonimo dell'esposto» non regge sull'esempio della fonte: la soluzione è *Concisa premessa*, che non è sinonimo di niente. Il sinonimo sta **nella prima lettura**, ed è lo strumento per arrivarci; la soluzione, come in ogni crittografia, parla d'altro.

Parti mobili:

- **Quanto è scontato il sinonimo.** Troppo scontato e il gioco è un esercizio; troppo remoto e diventa una perifrasi, e allora è un altro gioco.
- **Se il sinonimo si spezza.** Serve un sinonimo che, oltre a essere giusto, si lasci tagliare in pezzi che vogliano dire qualcosa. Le due condizioni sono indipendenti, ed è questo che rende difficile comporre.
- **Il diagramma, sempre a due lati.**

## Da dove viene

Enigmistica italiana, nel gruppo che `it-gioco-enigmistico.txt` chiama «crittografie di tipo misto», insieme alla voce 342, crittografia perifrastica e alla sillogistica: giochi in cui il ragionamento è insieme meccanico e concettuale. Non ha una voce propria su Wikipedia in italiano — `Crittografia_sinonimica` non esiste, controllato il 1 settembre 2026 con `build/check_titoli_341.py` — e vive di due paragrafi nella pagina generale.

Il sinonimo, invece, ha una letteratura. `it-sinonimia.txt` la definisce come la relazione fra due lessemi che hanno lo stesso significato, e la dà come opposta all'antonimia.

## Varianti e parenti

- **Crittografia pura** (voce 341, crittografia pura) — la stessa macchina senza il passaggio concettuale.
- **Crittografia perifrastica** (voce 342, crittografia perifrastica) — la gemella: al posto del sinonimo, un giro di parole. La fonte dichiara che distinguerle non è sempre agevole.
- **Crittografia sillogistica** — il terzo tipo misto, dove il passaggio è un ragionamento in tre tempi.
- **Crittografia mnemonica** (voce 343, crittografia mnemonica) — le sue mnemoniche «a sinonimi abbinati» sono il confine di sotto: lì i sinonimi ci sono ma non c'è più niente da rispaziare.
- **Cambio di spaziatura** (voce 345, cambio di spaziatura) — il meccanismo che sta sotto, una volta trovato il sinonimo.
- **Bisenso** (voce 335, bisenso) — la parola con due sensi; il sinonimo è la relazione opposta, due parole per un senso.

## Che cosa se ne sa

**L'esempio della fonte, ricontato.** `Con C I saprem essa` = *Concisa premessa*: quindici lettere per parte, diagramma (3 1 1 6 4) = (7 8), verificato in `build/check_341.py`. La nota spiega il passaggio: aggiungendo all'esposto le lettere C e I si ottiene *Colei*, e *colei* definisce il pronome *essa*. Il sinonimo è quella coppia, e senza di lei la prima lettura non si può nemmeno pronunciare.

**Il gioco poggia su una relazione che la lingua non garantisce.** `it-sinonimia.txt` scrive che «la sostituibilità assoluta di due parole raramente è realizzabile»: dal punto di vista connotativo «c'è quasi sempre una variazione di significato», e porta *babbo*, *papà*, *padre*, che appartengono a registri diversi e in certi contesti non si scambiano — *Santo Padre*, *a babbo morto*. `synonym.txt`, presa lo stesso giorno, dice la stessa cosa dall'altra parte: alcuni lessicografi sostengono che **nessun sinonimo sia identico a un altro** in tutti i contesti e a tutti i livelli di lingua. Due pagine, due lingue, nessuna contraddizione. **Un gioco che richiede un sinonimo preciso chiede alla lingua una cosa che la lingua non ha.**

**La fonte afferma una difficoltà e non la misura.** «Talvolta di soluzione più agevole rispetto alla pura»: né *talvolta* né *più agevole* sono quantificati, e nessuna delle pagine prese porta un tempo di soluzione, una percentuale di risolutori o un confronto. **Si registra come opinione della disciplina su sé stessa**, che è il genere di affermazione che circola meglio proprio perché nessuno la controlla.

**Il numero degli stacchi non aiuta a collocarla.** In `build/check_341.py` la sinonimica sposta cinque stacchi su cinque, la perifrastica sei su sette, la pura due su quattro, la sillogistica tre su tre. Zero vale solo per la mnemonica; sopra lo zero **la quota non ordina niente**, e sinonimica e sillogistica pareggiano. La grandezza che separa la mnemonica dal resto non separa il resto.

**Il limite del capitolo morde qui più che altrove.** Comporre una sinonimica vuol dire cercare una parola che sia insieme un sinonimo giusto e una sequenza di lettere che si spezzi bene: il sistema non sa fare la seconda metà (`ideas/10 §6`). Delle tre vie d'uscita provate in questa sezione — girare il gioco dalla parte dell'autore, stampare per intero lo spazio di ricerca, dare il risultato e chiedere l'operazione — qui funziona la prima, e funziona perché **il compito si spezza in due passi che chi risponde può fare con la matita**: trova il sinonimo, poi prova a tagliarlo.

## Esempi trovati

Da `it-crittografia-gioco.txt`: `Con C I saprem essa` = *Concisa premessa*, con la spiegazione in nota — l'esposto, più le lettere C e I, dà *Colei*, che definisce *essa*.

Dalla stessa pagina, il gioco confinante: la perifrastica `A "Ma che dite!" L aiuta` = *Amache di tela iuta*, dove al posto del sinonimo c'è un giro di parole.

Da `it-sinonimia.txt`, fuori dall'enigmistica: i **geosinonimi**, cioè sinonimi che appartengono a varietà regionali diverse — *babbo* e *papà*, *acquaio* e *lavandino*. E i sinonimi che valgono solo in un certo tipo di testo: *la Vecchia Signora* è sinonimo di *Juventus* soltanto nel giornalismo sportivo, ed è una metonimia.

Nostri, e trovati cercando parole che si lascino tagliare in due: *seggiola* → *seggio la*, *dimora* → *di mora*, *sentiero* → *senti ero*, *timore* → *ti more*. La conservazione delle lettere è verificata in `build/blocco_341.py`; che i pezzi siano parole italiane è un giudizio nostro, non un conteggio.

## Una nostra versione

La crittografia intera non si può dare. Si può dare la mossa che la distingue, spezzata nei due passi che la compongono.

> **La parola che, cambiata, si spezza**
>
> Quasi nessuna parola italiana si può tagliare in due parole che vogliano dire qualcosa. *Tavolo* no. *Finestra* no. Ma qualcuna sì, e il trucco degli enigmisti è questo: **se la parola che hai in mano non si spezza, cercane un sinonimo che si spezzi.**
>
> ```
>  la parola   un suo sinonimo   il sinonimo, rispaziato
>  la sedia    seggiola          seggio la
>  la casa     dimora            .................
>  la paura    timore            .................
>  la strada   sentiero          .................
> ```
>
> **Come sai di aver ragione:** le lettere devono essere le stesse, nello stesso ordine, e nessuna in più o in meno. *Seggiola* e *seggio la* hanno otto lettere tutt'e due. Se ti tocca aggiungere o togliere una lettera per far tornare le parole, non vale.
>
> Poi tocca a te. Trova una parola qualsiasi che si spezzi in due, e chiedi a qualcuno di trovare di che cosa è il sinonimo.

Il taglio in due si controlla contando, e il conto sta sul foglio: è lo stesso invariante della voce 341, crittografia pura, ridotto al minimo. Quello che resta fuori è se i due pezzi siano davvero parole, e quello lo decide chi legge.

**Dove si romperebbe.** Il sistema non può proporre i sinonimi giusti né verificare i tagli, perché entrambe le cose richiedono di guardare dentro le parole. Può però stampare la scheda e, letta una risposta, contare che le lettere siano le stesse — la verifica è un confronto fra due stringhe, non una manipolazione. Sul pannello da quattro righe la tabella non entra: sono cinque righe e tre colonne.

## Da riprendere alla rassegna

**Questa voce differisce dalla voce 341, crittografia pura perché lì la prima lettura si ricava guardando l'esposto, mentre qui bisogna prima chiamarlo con un altro nome.** È lo stesso scalino della voce 342, crittografia perifrastica, e le due si distinguono solo per il tipo di passaggio — un sinonimo invece di un giro di parole. La variabile della sezione è quanta parte della prima lettura è meccanica, e qui ne resta la maggior parte.

**Un compito che si spezza in due passi indipendenti si può dare anche quando il compito intero è fuori portata.** Trova il sinonimo, poi taglialo: due mosse piccole, ognuna con la sua verifica. Da provare su tutte le forme che il sistema non sa costruire.

**Il gioco chiede alla lingua una precisione che la lingua non ha**, e funziona lo stesso da centocinquant'anni. Alla rassegna vale la pena guardare quante forme dell'elenco poggino su relazioni approssimate — sinonimo, somiglianza, «più o meno la stessa cosa» — e se questo sia un difetto o il motivo per cui reggono.

