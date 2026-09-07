# Prompt, simulazione e documentazione

## La decisione del 7 settembre 2026

Il genitore ha chiesto di migliorare prima i prompt, poi il notebook che simula un pomeriggio e infine la documentazione. Dove le decisioni accumulate si contraddicono, la scelta deve favorire un'esperienza ricca e aperta. La chiarezza riguarda la possibilita di capire e svolgere un'azione; non impone che ogni attivita abbia una risposta unica, un solo gesto o una sola pagina.

Questa prima parte modifica i prompt e corregge un difetto nel materiale inviato alla continuazione. Il notebook e la documentazione generale restano da aggiornare. Nessuna modifica e stata distribuita al container o all'hub.

## Il percorso verificato

`panel/devising.py::devise_experience` costruisce router e Content Safety nel container. Sceglie una forma e una mossa da `methods/`, chiede l'attivita, la legge con il contratto `Experience`, puo riparare una risposta illeggibile, poi puo riparare una volta le contestazioni di `shared/experience_checks.py`. Una risposta che supera i controlli viene sottoposta a Content Safety. Il ramo di riparazione del formato e quello dei controlli sono distinti: il massimo non e necessariamente una sola chiamata di riparazione totale.

`devices/run_experience.py` esegue i momenti e si ferma a un `collect`. Il codice `_play` avanza fino alla raccolta; le durate dichiarate dei momenti non dimostrano da sole una pausa reale per ognuno. La revisione del notebook deve confrontare anche `devices/hands.py`, prima di dichiarare che riproduce l'orologio dell'hub.

L'hub chiede al container la pagina, la lettura e la continuazione. Il codice `_read` passa per `devices/read_page.py`; `_ask` invia un POST a `/api/device/{household}/experience`. `panel/continuing.py` costruisce router e gate nel container. L'hub non costruisce un client Foundry per queste operazioni. Le chiamate dirette del notebook appartengono all'apparato di ricerca e non descrivono la topologia di produzione.

`agents/page_maker.py::asked_for` riceve solo `Page`: titolo, note, etichette e illustrazione. Non riceve lo script, gli aiuti o gli altri momenti. Un indizio contenuto solo nello script non compare automaticamente sul foglio.

## Le modifiche ai prompt

L'apertura e lo script dell'ideatore non impongono piu un mistero sulle intenzioni di una persona a tutte le forme. Costruzioni, osservazioni, disegni, ipotesi e indagini possono mantenere il proprio metodo. Lo script deve indicare materiali, azioni, risultati e dove ciascun elemento arriva nella pagina o nei momenti.

I blocchi condivisi chiedono istruzioni esplicite sulla pagina. La voce narrativa puo accompagnarle, ma non deve farle indovinare. I limiti di testo e di fogli contemporanei restano quelli del contratto e della casa; il limite informale di una o due pagine per tutta l'attivita e stato tolto. Le fasi successive possono sviluppare cio che e stato costruito o scoperto.

Gli aiuti distinguono una risposta verificabile da un esempio per un compito aperto e da una procedura di osservazione. Il risultato osservato non viene inventato in anticipo. Il foglio puo conservare valore dopo la fine, senza creare un obbligo di tornare. La continuazione puo usare cio che il foglio riporta, senza inferire capacita, sforzo o interesse della persona.

Il giudice non considera piu un difetto il fatto che un risultato riguardi un meccanismo. Conosce `ask` come richiesta valida di continuazione e distingue il ramo senza stampa dal foglio effettivamente stampato. Rimane uno strumento fallibile: la seconda valutazione dei sei documenti segnala ancora un tavolo come oggetto non disponibile e tratta alcune operazioni chiuse dentro attivita aperte come contraddizioni. I conteggi delle sue segnalazioni non sono una misura affidabile del miglioramento.

Il cambiamento consente piu forme e conserva le istruzioni necessarie, ma richiede una verifica semantica degli oggetti prodotti: un contratto JSON valido non dimostra che il foglio sia comprensibile o che il disegno generato sia corretto.

## Il confronto misurato

La baseline e il commit `b60df1c3fbef0fa5a87e1c45107d49bcac206409`. Il file [comparison.json](../research/runs/2026-09-07-prompt-clarity/comparison.json) conserva tre coppie di attivita sintetiche, i prompt realmente inviati, le risposte e le riparazioni. La casa, la forma e la mossa sono uguali dentro ogni coppia. La mossa comune e `a-box-ticked-in-the-moment`; le forme sono `facts-printed-three-explanations`, `paper-that-has-to-hold` e `draw-with-one-thing-taken-away`. L'ordine dei due prompt e invertito nella seconda coppia. La scelta del metodo viene sostituita nel processo; generazione, parsing, riparazioni, controlli e sicurezza passano dalla funzione di produzione.

Le sei generazioni e le prime valutazioni hanno impiegato 1099,9 secondi complessivi, misurati dal programma. Tutte le attivita hanno superato formato, controlli e Content Safety. La baseline ha richiesto una riparazione su tre; la versione modificata ne ha richieste due su tre. Il fingerprint dell'ideatore passa da `4358f1f9c9ec` a `8035a0fd81c4`. I tempi comprendono la valutazione automatica e non misurano la durata dell'esperienza umana.

| Forma | Baseline | Prompt modificato |
| --- | --- | --- |
| Ipotesi | Il restauro di un passero diventa un'indagine sul motivo di una crepa lasciata aperta. Nilo e la paura del silenzio compaiono negli aiuti senza essere stabiliti dagli indizi della prima pagina. | Un ventilatore fermo ammette tre cause e segni che potrebbero distinguerle. Il caso resta dichiaratamente aperto. Il foglio fornisce gia cause candidate e conserva una selezione chiusa dei fatti irrilevanti. |
| Costruzione | Il ponte di carta introduce poi una mappa e il mistero di una consegna di semi. | Il ponte viene costruito, provato e modificato; gli esiti e le pieghe sono registrati nel taccuino. |
| Disegno | Il disegno a memoria introduce poi l'intenzione nascosta di Iva, che omette un manico per restituire una tazza. | Un oggetto viene osservato, lasciato altrove, disegnato a memoria e confrontato con il risultato. |

Il confronto mostra che costruzione e disegno non vengono piu ricondotti automaticamente a un mistero. Non dimostra che il pomeriggio sia piu apprezzato o che tutte le istruzioni funzionino. Le attivita nuove contengono ancora dettagli da verificare: per esempio, una chiede di avviare la lettura dallo schermo. Non sono state disegnate pagine, eseguite continuazioni o svolte prove con persone in questo confronto.

La rivalutazione degli stessi sei documenti, conservata in [rejudged.json](../research/runs/2026-09-07-prompt-clarity/rejudged.json), ha impiegato 139,8 secondi. Il file conserva il prompt del giudice e il suo fingerprint. Le segnalazioni errate su `ask` sono scomparse, mentre restano i limiti descritti sopra. Non si deve confrontare numericamente questa valutazione con i punteggi storici di `research/run.py`.

Il programma riproducibile e [research/compare_prompts.py](../research/compare_prompts.py). `python -m research.compare_prompts --output research/runs/NUOVO_NOME` genera un nuovo confronto; `--rejudge PERCORSO/comparison.json` valuta i documenti senza rigenerarli e rifiuta di sovrascrivere una rivalutazione gia presente. Il primo confronto e stato eseguito con il precursore locale `tmp/compare_activity_prompts.py`; il programma conservato esplicita baseline e lista dei blocchi, e la sua modalita `--rejudge` e stata eseguita sui sei documenti. La modalita completa del programma conservato non e stata rieseguita dopo questo riordino.

## La lettura che veniva persa

`agents/page_reader.py` restituisce `WhatCameBack`, con `written`, `same_sheet`, `describes`, `read_at`, `degraded` e `metadata`. `devices/run_experience.py::_ask` invia `reading.to_dict()` al container, che lo passa direttamente all'agente. Prima della correzione, `agents/experience_continuer.py::_ink` leggeva soltanto `cells`, il contratto precedente. Una lettura con descrizioni reali arrivava nel prompt come `What was on it: []`.

[tests/test_continuation_reading.py](../tests/test_continuation_reading.py) ha riprodotto il difetto: due test fallivano e quello legacy passava. La correzione conserva descrizioni e stato, esclude metadati e orario e mantiene il ramo legacy. I tre test ora passano. Il risultato e verificato sul prompt costruito dal codice; una continuazione reale dopo la correzione resta da eseguire nella seconda parte.

## Da dove riprendere il notebook

Il notebook [research/officina.ipynb](../research/officina.ipynb) non e stato modificato ne eseguito in questa sessione. Questi difetti sono stati osservati leggendo le celle e il codice chiamato:

- La raccolta costruisce `reading={"came": CAME, "reading": READ_AS}`. Deve passare il contratto reale del lettore; anche una risposta sintetica testuale deve essere rappresentata esplicitamente come tale, senza fingersi una lettura di immagini.
- Dopo una riparazione che lascia contestazioni, il notebook stampa le contestazioni e prosegue. La produzione solleva `RefusedByTheChecks`. Il notebook deve fermarsi prima del gate e della simulazione.
- Una stampa fallita puo portare comunque a una risposta sintetica testuale e al ramo `marks`. Deve esercitare `instead` e `if_no_page`, oppure dichiarare una modalita di simulazione diversa. Un errore di lettura non equivale a un foglio bianco.
- `IN_HAND` e `SHEET` tengono solo l'ultimo foglio. Il confronto delle ipotesi ha due pagine da leggere insieme. La simulazione deve conservare i materiali necessari e distinguere il foglio raccolto dai fogli disponibili.
- Il ciclo termina dopo 24 passi e stampa comunque `over`. Il limite va riportato come interruzione della simulazione. Anche `DID.stop` viene ignorato nel ramo testuale.
- La continuazione aggiorna `BY_ID` e `ORDER` ma non il documento passato alla continuazione successiva. Va verificata la corrispondenza con il segmento gestito dal runner reale.
- Il recorder registra le risposte riuscite, non le chiamate fallite; non va scambiato per una contabilita completa. La scrittura simulata dell'immagine usa un endpoint distinto e non passa dal recorder.
- Il notebook lascia aperto il gate. Le prove reali hanno emesso numerosi avvisi `Unclosed client session` anche nei percorsi che chiamano `gate.aclose()`: verificare separatamente la chiusura dei client e delle credenziali senza attribuirla al notebook soltanto.
- La ricerca della root puo ciclare se eseguita fuori dal repository. Il caricamento dei prompt e i riferimenti importati vanno verificati con due esecuzioni nel medesimo kernel.

L'apparato testuale `research/play.py` omette `page.illustration`, termina su `ask`, non esercita il clock reale e non inserisce gli aiuti nella trascrizione. `research/calls.appraisal.md` cerca invece l'ultimo aiuto e penalizza l'assenza di una domanda unica. Prima di usare i suoi otto assi come misura del notebook, bisogna correggere il materiale osservato e separare i criteri dei compiti aperti e chiusi. I vecchi punteggi restano storici.

## Da dove riprendere la documentazione

Partire da `README.md`, `docs/ARCHITECTURE.md`, `docs/architecture-overview.html`, `docs/an-afternoon.html`, `research/README.md` e dalle pagine pubbliche in `site/`. Verificare ogni affermazione nel codice che controlla il comportamento, non in un'altra pagina di documentazione. I file HTML e il sito non sono stati modificati in questa sessione.

Il README descrive ancora impostazioni, garanzie e parti non costruite che vanno confrontate con `panel/preferences.py`, `panel/what_happened.py`, `shared/profile.py`, `panel/keeping.py` e l'hardware effettivamente presente. Non sostituire una garanzia vecchia con una nuova non verificata. Distinguere progetto previsto, codice esistente, esecuzione locale e comportamento distribuito. La disponibilita attuale dell'hardware e la versione live del container non sono state controllate.

## Verifiche e stato di consegna

La suite mirata di prompt, agenti, continuazione e confini aveva 83 test superati prima della regressione sulla lettura. Dopo la correzione, la suite completa isolata ha dato 990 test superati e 2 saltati in 126,37 secondi. Lint mirato e diagnostica editor non segnalano errori nei file Python modificati. I prompt assemblati sono rigenerati con `python -m tools.prompts --write`.

Un primo `pytest -q` aveva ereditato le variabili Foundry del terminale e chiamato davvero il giudice nei test del registro: 988 test superati, 2 falliti, 2 saltati, 906,39 secondi. Le righe `judged` aggiunte alle fixture causavano i fallimenti. Rimuovendo dal processo di test le variabili `LANTERNINA_*` relative a Foundry e Content Safety, e ripristinandole dopo, la suite passa. Nessun test del registro e stato modificato. La suite non e completamente isolata dall'ambiente per costruzione: registrare questa trappola, non descriverla come contesa fra processi.

Il worktree era pulito alla partenza. Tutte le modifiche descritte qui appartengono a questa sessione e restano non committate al momento della consegna. La baseline resta il commit indicato sopra. Prima di continuare, controllare `git status` e lavorare con eventuali modifiche nuove dell'utente. Non e stato eseguito alcun deploy.

La seconda parte e fatta quando il notebook esegue un percorso con pagina disegnata, scrittura sintetica, lettura e continuazione basata sul contenuto letto; distingue conclusione reale, interruzione, errore e ripiego; verifica anche foglio bianco, stampa fallita e due fogli. Le prove devono salvare tempi e artefatti sintetici senza pubblicare credenziali o dati di una casa reale. Una prova fisica con l'utente resta necessaria per giudicare pagina stampata e comprensibilita dell'esperienza.

La terza parte e fatta quando le pagine principali descrivono hub, container, modelli e memoria in accordo con i percorsi verificati, separano misure storiche da nuove misure e passano build e controlli pertinenti. La preferenza per aperture e ricchezza resta valida durante entrambe le parti.

## La verifica del notebook del 7 settembre 2026

Il notebook ora usa `research/workbench.py` e chiama `panel.devising.devise_experience` per generazione, parsing, riparazioni, controlli e sicurezza. Questo elimina la copia locale che continuava dopo contestazioni residue. Una prima prova della vecchia cella corretta ha verificato il rifiuto con una riparazione sintetica ancora contestata; la versione finale delega alla funzione di produzione. `research/execute_officina.py` esegue tutte le celle con l'interprete chiamante e conserva gli output anche in caso di errore. L'extra `bench` dichiara anche `nbclient`.

La corsa [2026-09-07-officina-104746-339138](../research/runs/2026-09-07-officina-104746-339138/verification.json) ha completato il notebook in 345,4 secondi misurati dall'esecutore. Il percorso dei modelli con il controllo del foglio bianco ha impiegato 335,6 secondi. La camminata dopo la generazione ha impiegato 195,5 secondi, ha attraversato cinque momenti e ha sommato 63 minuti dichiarati dal documento. Questi 63 minuti non sono tempo umano misurato: i passaggi senza raccolta vengono attraversati subito.

Il brief sintetico richiedeva due fogli complementari su una ferrovia inventata e una ricostruzione aperta. La selezione ha restituito `what-changed-between-two-pictures` e `one-fact-that-changes-what-was-already-read`. Il sistema ha disegnato la mappa e il taccuino, poi il modello della scrittura ha ricevuto il taccuino come prima immagine e la mappa come riferimento. Il lettore ha restituito sette descrizioni: paesaggio blu, tracciato, freccia N e le risposte scritte, inclusa la parola cancellata. Tutte compaiono nel prompt realmente inviato al continuatore. Il seguito usa freccia e direzione per proporre un cambio dell'orientamento e arriva a `close`. Il controllo con due copie della stessa immagine intatta restituisce `written=false`, `same_sheet=true`, `degraded=false`.

Le tre immagini sono state guardate a risoluzione intera. Titoli e istruzioni sono leggibili nell'immagine e il taccuino usa elementi della mappa. La mano sintetica ha anche colorato una matita decorativa gia stampata: non ha conservato ogni pixel originale. Non ha eseguito il cerchio richiesto sulla prima mappa, che resta un foglio di riferimento; non ha materialmente svolto la correzione finale proposta dal seguito. La corsa verifica la generazione di quei momenti, non tutte le azioni umane che descrivono. Non dimostra gradimento o comprensione. Non sono stati usati conteggi dei giudici come misura di qualita.

Il recorder conserva prompt, risposte, tempi ed errori delle chiamate logiche e registra anche la scrittura sintetica, prima esclusa. I retry interni all'SDK e le richieste Content Safety non sono voci indipendenti: non e un registro di fatturazione. Il recorder e dichiaratamente riservato a dati sintetici. Il tipo `WhatCameBack` e riusato, ma i suoi dizionari vengono conservati in questa ricerca, a differenza del percorso ordinario transitorio.

I test esercitano foglio bianco, stampa fallita, due fogli disponibili e un foglio raccolto, lettura fallita o degradata, stop esplicito e limite dei passi. La conclusione richiede `Close`; il limite e lo stop producono `interrupted`, gli errori producono `error`, i ripieghi restano eventi distinti. La raccolta passa `reading.to_dict()` al seguito. Il segmento nuovo sostituisce quello attivo, come nell'hub. Il documento originale resta quello mandato alle richieste successive: continuazioni arbitrarie ripetute non sono state dimostrate.

`bench.reload_prompts()` ora include il lettore. Un test ricarica due marcatori diversi nello stesso processo e verifica che il secondo sostituisca il primo, poi ripristina i prompt originali. La ricerca della root termina anche fuori dal repository. Il gate e il recorder sono chiusi in `finally`; client e credenziale della scrittura sintetica vengono chiusi anche sul percorso d'errore. I test mirati di ricerca, scrittura e workbench hanno dato 30 passati in 6,20 secondi prima delle verifiche finali. La corsa ha emesso avvisi Jupyter su event loop Windows e trasporto TCP locale; gli avvisi non equivalgono a un errore dei modelli.

## Il confronto fra documento e codice

La topologia corrente e hub, container API, router e modelli. Le funzioni del notebook chiamano i modelli dalla macchina di ricerca e non verificano autenticazione HTTP, approvazione, archivi distribuiti o il modello separato che produce osservazioni per il profilo. Il genitore approva `OfferedExperience`; i sigilli del percorso precedente `Proposal` non sono il meccanismo di consegna delle attivita attuali. Il seguito e filtrato ma non riapprovato, e non ha riparazioni. La generazione puo avere una riparazione del formato e una distinta dei controlli.

Il codice conserva esiti, durate, sintesi derivate dalle letture e osservazioni per il profilo. `shared/profile.py` usa gli assi `load`, `ink` e `span`, una finestra di otto elementi e almeno tre collocazioni per asse. `panel/profiles.py` conserva fino a 80 osservazioni. Il profilo e ricalcolato per i prompt. La conservazione amministrativa di sviluppo e distinta: il permesso dura 14 giorni e `kept_for` assegna a ogni nuova riga 14 giorni dalla sua scrittura. Revocare il permesso ferma nuove scritture; non cancella subito quelle esistenti. Le descrizioni precedenti che promettevano solo memoria del materiale generato erano errate.

Il confronto ha trovato due lacune nel runner reale, documentate senza modificarle in questa revisione. `hands._hand_over` mostra `instead` dopo una stampa fallita, ma `run_experience._play` si ferma alla raccolta e non legge `if_no_page`. Il workbench esercita quel ramo del contratto come simulazione dichiaratamente diversa. Inoltre `_play` e `hands.py` non attendono le durate dei momenti consecutivi senza raccolta. La somma dei minuti nel notebook non riproduce quindi un orologio reale. Il timer e lo stato leggibile sono prerequisiti per la via d'uscita e la chiusura; una garanzia assoluta di conclusione sarebbe falsa.

README, architettura, pagine HTML, README di ricerca e pagine pubbliche bilingui vengono allineati a questi comportamenti. Le misure fisiche precedenti restano datate. Nessun deploy e stato eseguito e nessuna casa reale e stata contattata. Per la verifica fisica servono una stampa dei due fogli, la prova delle istruzioni affiancate, una scansione del taccuino compilato e l'osservazione dei tempi sul display. Prima di quella prova occorre verificare separatamente quale codice sia installato su hub e container.

## Verifiche finali della seconda parte

La suite completa isolata ha dato 1003 test passati e 2 saltati in 137,64 secondi, con un avviso di deprecazione Starlette. Il lint mirato e la diagnostica editor sono puliti. La build Astro produce dieci pagine senza errori, avvisi o hint; `site/check-build.py` passa. Il browser ha verificato le otto pagine pubbliche modificate a 1280 e 390 pixel. Ha trovato un overflow desktop nelle due tabelle di stato; una regola limitata alle tabelle descrittive lo ha corretto, e il controllo ripetuto non lo rileva. Il diagramma del ciclo e stato guardato in una cattura del browser. I tre diagrammi Mermaid della pagina di architettura sono renderizzati senza errori dopo aver sostituito un punto e virgola che il parser interpretava come istruzione.

Gli output del notebook conservano otto chiamate logiche riuscite e zero errori o avvisi `Unclosed client`: scelta 17,889 secondi, generazione 118,146 secondi, mappa 43,808 secondi, taccuino 26,250 secondi, mano sintetica 40,015 secondi, lettura 9,599 secondi, continuazione 74,784 secondi e lettura del bianco 2,067 secondi. I tempi provengono dal recorder; non comprendono nello stesso modo i controlli e il filtro esterni alle chiamate registrate. La continuazione di questa corsa non rientra nella vecchia stima di 15-25 secondi.

Il server `astro preview` e uscito prima di rendersi disponibile; la verifica visuale usa la build statica servita solo su localhost. Questo non prova le intestazioni effettive della Static Web App. Le modifiche precedenti sono state conservate. Non sono stati creati commit o eseguiti push.

I quattro diagrammi del walkthrough HTML sono renderizzati senza errori. Il click automatizzato di Playwright ha incontrato problemi di stabilita e puntamento; l'attivazione DOM degli stessi pulsanti ha verificato il gestore: contatore da 0 a 1 e 2, reset a 0. I 35 collegamenti locali dei quattro documenti Markdown aggiornati sono validi. `git diff --check` passa. L'anteprima del sito compilato e disponibile su `http://127.0.0.1:4323/it/`; i documenti HTML sono serviti separatamente su `http://127.0.0.1:4324/`.

## La pulizia del sito pubblico

Il 7 settembre il genitore ha chiesto di eliminare i dettagli di basso valore dalle pagine pubbliche e di pubblicare il risultato. Le introduzioni italiana e inglese perdono la tabella dei tempi storici, il resoconto del deploy e le spiegazioni dei vecchi tipi di consegna. I diagrammi perdono i tempi isolati e la pagina di stato perde tre racconti di debug gia conservati nei resoconti. Restano le informazioni su memoria, approvazione, sicurezza e lacune del runner. Il costo e una minore quantita di dettagli tecnici nel sito; i collegamenti ai documenti del repository li mantengono accessibili.

L'esempio della nuvola viene sostituito dalla mappa di Valle Lunga e dal taccuino compilato della corsa sintetica: le osservazioni e il compito sono scritti sui fogli e la pagina spiega come usarli insieme. I due fogli sono distinti nelle didascalie; il taccuino vuoto e collegato separatamente. Le copie WebP sono senza perdita e mantengono i 1024 per 1536 pixel degli originali. La compilazione resta dichiarata sintetica e non viene presentata come una soluzione verificata. Questo rende esplicita l'azione richiesta, ma non risolve i limiti dell'attivita osservati sopra. Il browser ha verificato immagini caricate e assenza di overflow nelle due lingue a 1280 e 390 pixel. Le immagini si aprono anche a piena risoluzione.
