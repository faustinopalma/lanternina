# Assegnata dal genitore

- **Numero** 289 nell'enciclopedia, capitolo 10 — Chi assegna, e chi giudica
- **Si chiama anche** la bozza nel pannello, l'idea del genitore, il compito dato in casa, la commissione, il *brief*, «l'ha chiesta la mamma»
- **In una riga** esiste già: la bozza nel pannello.
- **Fonti** il repository stesso, letto il 31 agosto 2026 — `panel/drafts.py`, `panel/routes/draft.py`, `panel/guidelines.py`, `panel/preferences.py`, `panel/experiences.py`, `panel/requests.py`, `agents/experience_deviser.brief.md`, `agents/experience_deviser.household.md`, `agents/experience_deviser.py`, `shared/experience.py`, `docs/NON-GOALS.md`; e `design-brief.txt`, `commission-art.txt`, `homeschooling.txt`, `delegation.txt`, prese il 31 agosto 2026. I conti in `build/check_289.py`, che legge le costanti dai moduli invece di ricopiarle
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Chi ha scritto: un adulto che vive nella stessa casa, e che quindi non è né anonimo né inventato. Per chi: una persona precisa, che l'adulto conosce. Che cosa si aspetta indietro: la cosa fatta, e — questa è la differenza — **una relazione che continua dopo.**

È l'unica delle otto forme del capitolo che questo progetto costruisca già, e va descritta con i nomi dei file invece che immaginata.

Parti mobili:

- **Chi scrive il testo.** Nel pannello il genitore può scrivere parlando a un modello, che riscrive, oppure digitando direttamente. Le due cose sono separate apposta: `panel/routes/draft.py` chiama la prima *say* e dice che costa una chiamata, e la seconda *type*, che «non costa niente ed è la stessa scrittura inerte di ogni altra rotta del pannello — un genitore che vuole cambiare una parola non deve doverlo chiedere».
- **Che cosa vale come idea.** `panel/drafts.py` dice che una bozza tiene «l'idea, non il piano»: titolo, panoramica, temi e copione, cioè le quattro cose per cui un genitore approva un pomeriggio. I momenti — pesi, appigli, vie d'uscita, controlli — sono macchina, e il testo libero non può diventarli.
- **Che cosa succede all'approvazione.** Il copione viene passato al modello **come commissione**. `agents/experience_deviser.brief.md` è il blocco che sostituisce la metà «non questo di nuovo» del prompt, e dice: «Il genitore ha scritto il pomeriggio che vuole, ed è questo. Costruisci quello.»
- **Che cosa non si allenta.** Niente. La rotta di approvazione fa passare il documento dal formato, dai controlli e dal filtro di sicurezza come ogni altro pomeriggio, e un rifiuto torna indietro con la sua ragione «perché il genitore può cambiare il testo e riprovare».
- **Che cosa il foglio dice del mittente.** Niente. `shared/experience.py` non ha nessun campo per chi abbia chiesto un pomeriggio: i campi sono `experience_id`, `title`, `overview`, `minutes`, `moments`, `requires`, `drawn`, `themes`, `script` e `format_version`. **La forma esiste dal lato di chi scrive e non esiste dal lato di chi legge.**

Se si toglie l'ultima parte — se il foglio dicesse chi l'ha chiesto — la forma diventerebbe la voce 288, assegnata da un personaggio dentro la storia con un mittente vero al posto di uno inventato. Non è quello che il progetto fa oggi.

## Da dove viene

Da tre posti, e vale la pena tenerli distinti perché portano tre patti diversi.

**Dalla commissione.** `design-brief.txt`, letta il 31 agosto 2026, definisce il *design brief* come un documento redatto da un progettista **in consultazione con il committente**, che fissa che cosa va consegnato e in che ambito, comprese funzione, aspetto, tempi e budget; e aggiunge che i brief cambiano nel tempo e si aggiustano man mano. La pagina è un abbozzo di 2 137 byte e non porta misure. `commission-art.txt`, presa lo stesso giorno, descrive la commissione artistica come l'atto di ingaggiare e pagare qualcuno perché faccia un'opera. **In tutti e due i casi chi commissiona non esegue**, ed è questa la struttura che il pannello riproduce: il genitore scrive che cosa vuole, e un altro lo costruisce.

**Dalla delega.** `delegation.txt`, letta il 31 agosto 2026, la definisce come «il processo di distribuire e affidare del lavoro a un'altra persona», e aggiunge che in un'organizzazione **l'autorità e la responsabilità scendono insieme** lungo la catena. Nel pannello succede il contrario, e la differenza è la cosa da tenere: `panel/experiences.py` scrive che «quello che il genitore decide è se questo pomeriggio possa succedere in questa casa», e che tutto quello che c'è dentro raggiunge un adolescente **sulla forza di quell'unica decisione**. L'autorità di scrivere è delegata al modello; la responsabilità resta ferma. La stessa pagina avverte che la delega fatta male porta al microcontrollo.

**Dalla casa che insegna.** `homeschooling.txt`, letta il 31 agosto 2026, tratta l'istruzione dei bambini fuori dalla scuola e descrive uno spettro: da forme molto strutturate, ricalcate sulla lezione scolastica, fino all'*unschooling*, «un processo in cui il genitore cerca di trasformare gli interessi del bambino in momenti educativi». Quella frase è la descrizione più vicina che le fonti diano di quello che il pannello chiede a un genitore di fare. Serve anche per differenza: nella forma che il progetto costruisce **il genitore non insegna e non corregge**, scrive una commissione e la approva.

## Varianti e parenti

- **Il foglio senza mittente** — voce 287, assegnata dal sistema: quello che esce dal pannello, oggi, ha questa faccia.
- **Il mittente inventato** — voce 288, assegnata da un personaggio dentro la storia.
- **Il menu fra cose possibili** — voce 290, scelta da chi la fa: la stessa decisione spostata dall'altra parte.
- **L'idea scritta da chi la esegue** — voce 291, inventata da chi la fa.
- **Decidere prima come sarà fatta una cosa** — voce 66, progettare: il brief è quel verbo applicato al pomeriggio di qualcun altro.
- **La bozza aperta da un pomeriggio esistente.** `panel/routes/draft.py` permette di aprire una bozza copiando un pomeriggio già offerto, e dichiara che è **una copia**: «modificare una bozza non torna mai indietro dentro quello da cui è stata aperta».
- **I limiti che il genitore scrive.** `panel/guidelines.py` tiene le frasi con cui un genitore restringe quello che un pomeriggio può fare improvvisando. Non è una consegna, ma è l'altra metà della stessa penna.

## Che cosa se ne sa

Questa è l'unica voce dell'elenco in cui la fonte principale è il repository, e quindi l'unica in cui i numeri si leggono invece di stimarli. `build/check_289.py` li prende dai moduli invece di ricopiarli, così un numero che cambia nel codice fa cambiare la voce.

**Quanto può scrivere un genitore su una bozza sola.** `panel/drafts.py` fissa 2 000 caratteri per ogni cosa detta, 80 righe di conversazione per bozza — che sono 40 giri, perché ogni giro ne aggiunge due, la sua e quella del modello — e 12 righe passate al modello, cioè 6 giri. Un genitore può quindi scrivere fino a **80 000 caratteri** dentro una bozza, e a bozza piena **il modello ne vede il 15,0%**: dodici righe su ottanta. Ricontato per complemento: 68 righe restano fuori su 80, cioè l'85,0%, e i due conti si sommano a uno. Il commento nel codice dice perché: «un prompt che cresce senza limite diventa più lento e più caro a ogni giro, e la riga più vecchia è la cosa meno utile che ci sia dentro».

**Quanto può scrivere lo stesso genitore in tutto il resto del pannello.** I limiti d'improvvisazione sono 12 righe da 160 caratteri, cioè 1 920; la nota sul momento che la casa attraversa ne vale 600; gli interessi e le cose da evitare sono due elenchi da 12 voci di 200 caratteri, cioè 4 800. In totale **7 320 caratteri**. Una bozza sola ne vale **10,9 volte tanto**. Il rapporto dice dove sta lo spazio di scrittura di un genitore in questo progetto, e non è dove ci si aspetterebbe: **non nelle impostazioni, ma nella singola idea.**

**Il testo di un genitore arriva al modello come materiale, tranne uno.** `agents/experience_deviser.py` lo dichiara: quello che un genitore scrive nel pannello arriva citato come JSON, «che è quello che lo tiene materiale invece che istruzione». Il brief è **l'unica eccezione**, ed è deliberata, perché un genitore che ha lavorato su un'idea e l'ha approvata «sta chiedendo quel pomeriggio e nessun altro». Fuori da lì il prompt dice al modello di non seguire le istruzioni scritte dentro il testo del genitore.

**C'è una misura, ed è un fallimento datato.** `agents/experience_deviser.household.md` riporta che il 27 agosto 2026, data la nota «mese pienissimo di scuola, e il nonno è morto tre settimane fa», il modello ha scritto **due pomeriggi su qualcuno che se ne va e non torna** — «aveva deciso di partire davvero». Aveva preso la nota come argomento. È il caso più netto, in tutto il repository, di una frase scritta da un genitore che produce l'opposto di quello che chiedeva; la correzione è stata dire nel prompt non solo che cosa farne ma che cosa non farne mai. **Due pomeriggi su due**, e la pagina non dice quanti ne siano stati generati in tutto, quindi il denominatore manca: va verificato se fossero due su due o due su più.

**Il permesso è stato tolto e il divieto no, e la data è nota.** `panel/guidelines.py` dice che le righe scritte dal genitore «restringono soltanto, e questo è cambiato il 28 agosto 2026». Prima erano permessi — «uscire in giardino va bene» — e un permesso allarga quello che un pomeriggio può fare, «per cui il prompt doveva portarsi dietro una frase che diceva al modello di non lasciare che uno allentasse i limiti fissi. Una pagina che può solo restringere non può allentare niente, così la garanzia smette di dipendere da una frase che un modello deve rispettare». **È una sostituzione di una promessa con una struttura**, e la stessa mossa è quella che alla voce 285, deduzione sociale era «l'arbitro sostituito da una procedura che tutti possono controllare».

**Il limite dominante del capitolo qui morde, e la risposta è nell'assenza di un campo.** `panel/preferences.py` scrive: «non c'è nessun campo per un nome o per un identificativo, e nessuna rotta che ne porti uno». `panel/drafts.py` ripete la stessa cosa per la bozza: «Niente qui riguarda un adolescente. Una bozza non porta nome, identificativo né storia, e non c'è nessun campo in cui una lettura di una pagina o un resoconto di come sia andata starebbe.» La nota del genitore, che è la sola cosa vicina a un'affermazione su una persona, ha una scadenza di **2 419 200 secondi, cioè 28 giorni, quattro settimane**, ed è **cancellata anziché contrassegnata**. Il commento dà la ragione: «una nota che non può sopravvivere a quattro settimane non può diventare un registro su nessuno».

Quello che nel repository non c'è, e va detto: **nessuna misura di che cosa cambi per chi riceve il foglio.** Non è mai stato provato se un pomeriggio commissionato da un genitore vada diversamente da uno inventato dal sistema, e non potrebbe esserlo con gli strumenti attuali, perché niente registra come sia andata legandolo a chi l'ha chiesta. La forma è costruita e non misurata.

Un'ultima cosa, che riguarda le fonti interne. `panel/drafts.py` e `panel/routes/draft.py` rimandano tutti e due a `docs/NON-GOALS.md` come al documento «emendato invece che piegato in silenzio». Quel file, letto il 31 agosto 2026, **è vuoto per scelta**: le regole sono state tolte perché la ricerca non nasca filtrata. I due rimandi sono dunque a un testo che non c'è più, ed è un residuo dell'epoca precedente. Si registra come fatto, non come difetto.

## Esempi trovati

Dal pannello, oggi: un genitore apre una bozza vuota, scrive tre paragrafi su un pomeriggio che vorrebbe, il modello glieli riscrive, il genitore ne cambia due parole a mano, preme approva. Quello che torna è un pomeriggio approvato all'ingresso — `panel/routes/draft.py` lo dice con una ragione: «il genitore ha scritto questo e ha premuto approva; chiedergli di ritrovarlo nell'elenco in attesa e approvarlo di nuovo sarebbe chiedere due volte una decisione sola».

Dal pannello, l'altro verso: la stessa persona apre una bozza **da un pomeriggio già offerto**, cambia il finale, approva. L'originale resta dov'era.

Dal committente: il brief di progettazione descritto in `design-brief.txt`, che si scrive in consultazione e si aggiusta strada facendo. Non è una consegna a senso unico ed è per questo che è il parente più vicino.

Dal mestiere dell'arte: la commissione, dove chi paga fissa il soggetto e chi esegue fissa tutto il resto. `commission-art.txt` non dice niente su come si divida in pratica quel confine.

Dalla casa che istruisce: l'*unschooling* descritto in `homeschooling.txt`, in cui il genitore trasforma un interesse già esistente in un'occasione. La pagina non porta misure confrontabili con quello che serve qui.

## Una nostra versione

L'esempio è quello che un genitore scrive, perché è l'unico pezzo di questa forma che sia testo. Quello che ne esce, invece, ha la faccia della voce 287, assegnata dal sistema.

> **La bozza, come si scrive nel riquadro del pannello**
>
> ```
>  TITOLO     Il rumore delle otto e mezza
>
>  PANORAMICA Un pomeriggio che comincia dal fatto che a
>             casa nostra, verso le otto e mezza, si sente
>             sempre un rumore che nessuno ha mai
>             identificato. Non voglio la risposta: voglio
>             che si costruisca un modo di descriverlo.
>
>  TEMI       suoni, casa, notazione inventata
>
>  COPIONE    Prima si chiede di segnare per tre sere di
>             seguito che cosa si sente e a che ora, con
>             qualunque scrittura venga in mente: parole,
>             disegni, segni. Non una tabella nostra: la
>             tabella la deve fare chi ascolta.
>             Poi si chiede una legenda, cioe' che cosa
>             vuol dire ogni segno che ha usato.
>             Alla fine si chiede una cosa sola: quale
>             segno ha dovuto inventare due volte perche'
>             il primo non bastava.
> ```

Quattro campi, e sono esattamente i quattro che `panel/drafts.py` tiene. Il copione fa il lavoro: **dice che cosa non fornire** — la tabella —, il che è la mossa che la voce 291, inventata da chi la fa tratta per esteso. Il titolo e la panoramica sono le due cose che il genitore rileggerà per riconoscere il pomeriggio quando gli tornerà davanti approvato.

Sta nel formato senza ripieghi, ed è provato: questa è la sola voce del capitolo in cui la forma non va immaginata perché il codice c'è. **Dove si romperebbe è l'altro capo.** Il pomeriggio che ne esce non porta da nessuna parte che l'abbia chiesto un genitore; nessun campo di `shared/experience.py` lo può dire, e la riga che lo direbbe andrebbe scritta dentro il copione, cioè dentro il testo, come un mittente inventato. **La forma è completa dal lato di chi scrive e muta dal lato di chi legge**, e questa è la cosa che si porta alla rassegna.

## Da riprendere alla rassegna

**Lo spazio di scrittura di un genitore in questo progetto sta nella singola idea e non nelle impostazioni: 80 000 caratteri contro 7 320, un rapporto di 10,9 a uno.** È una scelta di disegno che nessuno ha mai enunciato e che i numeri rendono evidente. Alla rassegna vale la pena chiedersi se sia quella giusta.

**Il modello vede il 15,0% di una bozza piena.** Un genitore che conversa a lungo sta scrivendo per sé, non per il modello, e il pannello non glielo dice. Non è un difetto ovvio — la conversazione intera resta visibile a chi l'ha scritta — ma è un'asimmetria fra quello che uno crede di aver detto e quello che è stato letto.

**La commissione è l'unico testo di un genitore che arrivi al modello come istruzione e non come materiale.** Tutto il resto è citato come JSON con l'avvertenza di non obbedirgli. Questa eccezione è l'intera forma: alla rassegna va guardata come tale e non come un dettaglio di implementazione.

**Sostituire una promessa con una struttura ha una seconda occorrenza, e viene dal codice.** I limiti che possono solo restringere, dal 28 agosto 2026, tolgono la necessità che il modello rispetti una frase. La prima occorrenza era l'arbitro sostituito da una procedura alla voce 285, deduzione sociale. **La regolarità candidata: quando una garanzia dipende da qualcuno che si comporti bene, esiste spesso una forma della stessa garanzia che dipende soltanto da quello che è possibile scrivere.**

**Il foglio non dice mai chi l'ha chiesto, e non c'è nessun campo che potrebbe dirlo.** Questa è la sola cosa che separa la forma costruita dalla forma descritta qui, e la distanza è un campo di una struttura dati. Da guardare insieme alla voce 288, assegnata da un personaggio dentro la storia, dove il mittente costa fra il 36,9% e il 45,0% del foglio.

**Due rimandi nel codice puntano a un documento che è stato svuotato.** `panel/drafts.py` e `panel/routes/draft.py` citano `docs/NON-GOALS.md` come se contenesse ancora le righe di allora. È ancora un residuo dell'epoca dei verdetti, dopo quello già segnalato nella voce 22, diario / registro.

