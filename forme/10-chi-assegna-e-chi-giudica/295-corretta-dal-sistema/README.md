# Corretta dal sistema

- **Numero** 295 nell'enciclopedia, capitolo 10 — Chi assegna, e chi giudica
- **Si chiama anche** correzione automatica, la macchina che corregge, foglio a lettura ottica, *Scantron*, griglia delle risposte, *automated scoring*, macchina per insegnare, istruzione programmata
- **In una riga** la risposta viene confrontata con quella attesa da una macchina.
- **Fonti** `automated-essay-scoring.txt`, `optical-mark-recognition.txt`, `teaching-machine.txt`, `programmed-learning.txt`, `knowledge-of-results.txt`, `criterion-referenced-test.txt`, `norm-referenced-test.txt`, `multiple-choice.txt`, `intelligent-tutoring-system.txt`, `corrective-feedback.txt`, lette il 1 settembre 2026; `shared/blocklist.py`, `shared/vision_contracts.py`, `shared/experience.py`, `agents/page_reader.py` e `agents/page_reader.instruction.md` nel repository, letti lo stesso giorno; `docs/EVIDENCE.md`, letto lo stesso giorno; i conti in `build/check_295.py`. `scantron.txt`, presa lo stesso giorno, è la scheda dell'azienda e non della cosa, e non è stata usata
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Chi guarda: una macchina. Che cosa confronta: quello che è stato scritto con una tabella di risposte scritta prima. Che cosa succede dopo che ha guardato: dice giusto o sbagliato, e lo dice subito.

La forma richiede tre cose e non due: una risposta **decidibile**, una risposta attesa **depositata prima**, e una **regola di confronto**. La terza è quella che si dimentica, ed è quella che decide tutto: fra «uguale carattere per carattere», «uguale a meno degli spazi» e «la casella annerita è la terza» ci sono tre macchine diverse.

Parti mobili:

- **Che cosa si confronta.** Una casella annerita, una parola, un numero, un testo intero. La difficoltà cresce di un ordine di grandezza a ogni passo, e all'ultimo passo la macchina smette di confrontare e comincia a stimare.
- **Quando arriva il verdetto.** Subito, a fine pagina, o mai. La macchina di Pressey del 1926 non passava alla domanda dopo finché la risposta non era giusta: il verdetto era immediato **e** bloccante.
- **Che cosa dice il verdetto.** Solo giusto o sbagliato; oppure quale sia la risposta giusta; oppure che tipo di sbaglio è stato fatto. Sono tre macchine di costo crescente e la prima è quasi gratis.
- **Se il verdetto è registrato.** Correggere e conservare sono due cose separabili, e quasi tutti i sistemi reali le fanno insieme.
- **Che cosa succede se la macchina si sbaglia.** Il caso non è raro e non è previsto quasi mai.

**Il confine con le altre quattro schede.** Qui il confronto lo fa una macchina, e la caratteristica che la distingue da tutte non è la velocità: è che **la risposta attesa esiste prima della domanda**. Alla voce 296, corretta da sé, alla voce 297, corretta da un pari e alla voce 299, verificata dal mondo il termine di paragone si forma dopo o non si formula affatto; alla voce 298, non corretta non c'è.

## Da dove viene

**Dalla lettura meccanica di un segno, e la data è il 1926.** `teaching-machine.txt` e `knowledge-of-results.txt`, lette il 1 settembre 2026, danno **Sidney L. Pressey** come inventore della prima macchina che insegnava: un dispositivo che poneva domande a scelta multipla e poteva essere regolato in modo da avanzare **solo quando la risposta era giusta**. L'articolo è *A simple apparatus which gives tests and scores — and teaches*, *School & Society*, 20 marzo 1926. La stessa pagina riporta la frase con cui Pressey descriveva il proprio programma nel 1932: la macchina avrebbe portato «una rivoluzione industriale nell'educazione».

**E prima ancora dall'idea di un libro che si apra solo a chi ha risposto.** La stessa fonte cita Edward L. Thorndike, 1912: «Se, per un miracolo di ingegnosità meccanica, un libro potesse essere fatto in modo che la pagina due diventi visibile solo a chi ha fatto quello che era scritto a pagina uno, e così via, molto di quello che oggi richiede un insegnante potrebbe essere sbrigato dalla stampa.» È la descrizione, quattordici anni prima, di quello che oggi si chiama sblocco di contenuti — la voce 263, sblocco di contenuti — con la correzione automatica come chiave.

**Dalla lettura ottica dei segni, che è una tecnologia industriale e non didattica.** `optical-mark-recognition.txt`, letta lo stesso giorno: il primo lettore fu l'**IBM 805 Test Scoring Machine**, che leggeva la grafite di una matita misurando la conducibilità elettrica con coppie di spazzole metalliche. Il primo lettore **ottico** funzionante fu di **Everett Franklin Lindquist**, brevetto US 3.050.248 depositato nel 1955 e concesso nel 1962; Lindquist aveva costruito parecchi test standardizzati e gli serviva una macchina migliore della 805. La **Scantron**, fondata nel 1972, cambiò il modello commerciale: distribuiva lettori a basso costo alle scuole e guadagnava vendendo i moduli — al punto che molti chiamano *scantron* qualunque modulo a lettura di segni.

**Dalla correzione dei temi, che è il tentativo più ambizioso e il più contestato.** `automated-essay-scoring.txt`, letta lo stesso giorno, fa risalire il campo a **Ellis Batten Page**, che nel 1966 sostenne che i temi si potessero correggere a macchina e nel 1968 pubblicò il *Project Essay Grade*. Il calcolo dell'epoca lo rendeva antieconomico e Page smise per una ventina d'anni; il campo riprese verso il 1990.

## Varianti e parenti

- **Nessuno confronta niente** — voce 298, non corretta.
- **Confronta chi ha lavorato** — voce 296, corretta da sé.
- **Confronta un altro che sta facendo la stessa cosa** — voce 297, corretta da un pari.
- **Confronta la fisica** — voce 299, verificata dal mondo: là non c'è nessuna tabella depositata prima, e il verdetto non si può contestare.
- **La forma di domanda che questa macchina sa leggere** — voce 1, scelta multipla, e in second'ordine la voce 5, corrispondenza (matching) e la voce 11, risposta breve.
- **Chi manda la consegna è la stessa macchina** — voce 287, assegnata dal sistema: la coppia naturale di questa scheda, ed è il caso normale della scuola.
- **Il verdetto blocca l'avanzamento** — voce 263, sblocco di contenuti.
- **Il verdetto diventa un numero conservato** — voce 259, classifica.
- **Un segnale d'errore locale invece che finale** — voce 181, percorso lineare, dove un risultato sbagliato manda a una casella che non esiste: è correzione automatica ottenuta senza nessuna macchina.
- **Il ripasso governato dall'esito di ogni risposta** — voce 242, ripasso distanziato (spaced repetition).

## Che cosa se ne sa

**L'accordo fra due correttori umani esperti è il metro con cui si giudica una macchina, e la fonte lo dà come una fascia larga.** `automated-essay-scoring.txt`: l'accordo esatto fra due esperti sta **fra il 53% e l'81%** dei temi, e l'accordo entro un punto **fra il 97% e il 100%**. Da qui si ricava, in `build/check_295.py`, la banda che la fonte non scrive: la quota di temi su cui due esperti differiscono di **esattamente un punto** sta fra **16 e 47 punti percentuali** — quattro combinazioni possibili degli estremi, cioè 16, 19, 44 e 47 —, e la quota su cui differiscono di più di due punti sta fra 0 e 3. **Il metro contro cui si misura una macchina è largo quasi mezzo intervallo.**

**Il metodo per giudicare una macchina è dichiarato e ha un difetto dichiarato.** La regola d'uso è: se il punteggio della macchina concorda con uno dei due umani quanto i due umani concordano fra loro, la macchina è affidabile. Il difetto che la stessa fonte solleva riguarda la gara Hewlett del 2012, in cui 201 partecipanti provarono a prevedere i voti umani su migliaia di temi: gli organizzatori dichiararono che la correzione automatica era affidabile quanto quella umana, **ma nessuna verifica statistica fu eseguita, perché alcuni fornitori avevano posto come condizione per partecipare che non se ne facessero.** Randy E. Bennett, dell'Educational Testing Service, contestò la conclusione; fra le critiche riportate, che cinque degli otto insiemi di dati erano paragrafi e non temi, e che il termine di paragone usato non era la media dei due correttori umani ma un «punteggio risolto» che in quattro casi su otto **era il più alto dei due**, il che permetteva alle macchine di arrotondare per eccesso.

**Il verdetto di una macchina su una scheda corta è in buona parte rumore, e il numero è nostro.** Con quattro opzioni per domanda e una soglia di passaggio al 60%, la probabilità che chi tira a indovinare passi è del **10,35%** su cinque domande, del **2,73%** su otto, dell'**1,97%** su dieci e dello **0,09%** su venti. Calcolata in `build/check_295.py` per formula binomiale **e** per enumerazione completa dei 4ⁿ profili di risposta fino a n = 10, con le due strade che coincidono a meno di 10⁻¹². **Alla lunghezza di scheda che questo progetto stampa — cinque, sei domande — un verdetto automatico è una volta su dieci puro caso.** E la precisione di una misura fatta su una scheda è quella che ci si aspetta: quattro giuste su cinque danno un intervallo di Wilson al 95% da **37,6% a 96,4%**, cioè ampio 58,8 punti. Un foglio non misura niente su nessuno, e questo è un fatto aritmetico prima che una scelta.

**La macchina più affidabile è quella che legge di meno, e il costo è quasi tutto nella carta.** `optical-mark-recognition.txt` dice che la lettura di segni si distingue dal riconoscimento di caratteri perché **non serve un motore di riconoscimento complicato**: il segno è costruito perché sia quasi impossibile leggerlo male. Il prezzo di quella affidabilità è la precisione di stampa — i moduli si progettano con una tolleranza dichiarata di **0,05 mm** — e il modulo prestampato costava da 0,10 a 0,19 dollari a pagina, un fattore 1,90 fra i due capi.

**E la macchina che legge di meno può sbagliare comunque, in modo silenzioso e su larga scala.** Alle presidenziali americane del 2008, nella contea di Gwinnett in Georgia, oltre **19 000 schede per il voto per corrispondenza** furono stampate con il contorno degli ovali troppo spesso, e la macchina le leggeva **tutte come annerite**. La differenza non era visibile a occhio nudo e fu scoperta solo con una prova di lettura a fine ottobre, quando circa 10 000 schede erano già rientrate: **il 52,6%**, calcolato in `build/check_295.py`. Il numero va preso per quello che è — la fonte scrive «oltre 19 000» e «circa 10 000», quindi il rapporto è un ordine di grandezza e non una misura.

**La critica principale alla correzione automatica di un testo è che misura la superficie.** Yang e colleghi, riportati dalla stessa pagina: eccessiva dipendenza da tratti superficiali della risposta, insensibilità al contenuto e alla creatività, e vulnerabilità a modi di barare nuovi. La procedura di base lo conferma: si parte da temi corretti a mano, si misurano grandezze **calcolabili senza nessuna comprensione** — quante parole, quante subordinate, il rapporto fra maiuscole e minuscole —, e si costruisce un modello che le lega ai voti. La petizione *Professionals Against Machine Scoring of Student Essays in High-Stakes Assessment*, lanciata il 12 marzo 2013 e firmata fra gli altri da Noam Chomsky, descrive la pratica come «banale, riduttiva, imprecisa, non diagnostica, iniqua e segreta», e limita esplicitamente la propria obiezione agli esami a posta alta.

**In questo progetto la correzione dal sistema non è difficile: è scritta come esclusa, in due posti, e i due si leggono nel codice.** `shared/blocklist.py` contiene **42 regole** divise in cinque gruppi, di cui **8 nel gruppo del biasimo** — conteggio fatto leggendo il file in `build/check_295.py` invece di ricopiarlo. Le otto rifiutano *hai sbagliato*, *hai fatto un errore*, *non hai capito*, *la tua risposta è sbagliata*, *riprova*, *non è quella giusta*, e gli inglesi *that is wrong* e *try again*. La ragione dichiarata nello stesso file non è il vocabolario ma la persona: quello che si rifiuta è **la seconda persona che porta un giudizio**, e infatti un registro contabile può contenere un errore e una battaglia si può vincere.

E `agents/page_reader.instruction.md`, che è il prompt con cui un modello guarda la fotografia di un foglio scritto a mano, dice **due volte** di non dire se qualcosa sia giusto — il conteggio è fatto dallo script, non a occhio — e ne dà la ragione: «non c'è niente qui che si possa sbagliare, quindi non c'è niente su cui avere ragione». Quello che quel lettore restituisce sono al massimo **8 descrizioni da 120 caratteri** (`shared/vision_contracts.py`, `MAX_DESCRIPTIONS` e `MAX_DESCRIPTION_CHARS`, lette dal modulo), e sono descrizioni di inchiostro: *una casa disegnata nel riquadro a sinistra*, *tre parole sulla prima riga*.

**Il confine con quello che il progetto ammette è più stretto di quanto sembri, e sta in una riga di `docs/EVIDENCE.md`.** Il paragrafo 3 di quel documento dice che **una domanda con una risposta giusta è ammessa** e che quello che non lo è è **la conseguenza** di sbagliarla: la richiesta è che sbagliare non costi niente, che il finale resti raggiungibile da dove si è arrivati, e che la via d'uscita sia scritta e data invece che lasciata da scoprire. Sono tre condizioni sulla conseguenza, non sull'esistenza della risposta. **Ne segue che il pezzo di questa scheda che il progetto non può fare non è il confronto: è la frase che comunica l'esito.**

**Un limite tecnico misurato restringe ulteriormente che cosa si possa confrontare.** Il sistema non sa manipolare le lettere dentro le parole — misurato e registrato in `ideas/10 §6` —, quindi non può verificare un anagramma, una sciarada, un acrostico, né contare le lettere di una parola scritta a mano. Insieme al fatto che non misura il tempo, non sa dove si trovi chi legge e non registra nulla su nessuno, quello che resterebbe da confrontare è: un numero, una casella, una parola intera.

## Esempi trovati

Dalla macchina di Pressey, 1926: quattro tasti, una domanda per volta, e il meccanismo che non avanza finché il tasto premuto non è quello giusto. È il primo esempio noto di una consegna in cui l'errore ha una conseguenza meccanica.

Dai fogli a bolle: matita numero 2 obbligatoria perché i primi lettori misuravano la luce che **passava attraverso** il foglio, e l'inchiostro blu era invisibile alle fototube sensibili al blu. I lettori moderni misurano la luce riflessa, e infatti accettano il nero. **Un dettaglio di consegna che sembrava una pignoleria era una proprietà fisica del sensore.**

Dal Regno Unito, riportato dalla stessa pagina: il modulo a lettura di segni più familiare non è scolastico, è la schedina della lotteria nazionale.

Dall'ETS, il servizio *Criterion*, che usa il motore e-rater per dare insieme un punteggio e un riscontro mirato: il caso in cui la macchina non dice solo se, ma anche che cosa.

Da `criterion-referenced-test.txt` e `norm-referenced-test.txt`, lette il 1 settembre 2026, la distinzione che decide che cosa una macchina possa dire: una prova **riferita a un criterio** confronta la risposta con una descrizione di che cosa vuol dire saper fare una cosa; una prova **riferita a una norma** la confronta con quello che hanno fatto gli altri. La seconda richiede gli altri, e questo progetto ne ha uno solo.

## Una nostra versione

> **La tabella la scrivi tu, e poi la macchina non serve più**
>
> Qui sotto c'è una frase cifrata. Ogni lettera è stata spostata in avanti nell'alfabeto **sempre dello stesso numero di posti** — e quel numero non te lo diciamo. I posti possibili sono ventisei, e uno solo dà una frase italiana.
>
> ```
>  SH JOPHCL L KLUAYV PS SPIYV CLYKL ZBS ZLJVUKV YPWPHUV
> ```
>
> Non ti diamo la chiave. Ti diamo **una cosa sola**, ed è quella che fa da macchina:
>
> ```
>  ┌─────────────────────────────────────────────────────┐
>  │ quando pensi di avere trovato la frase, conta le E. │
>  │ nella frase giusta le E sono 6.                     │
>  └─────────────────────────────────────────────────────┘
> ```
>
> Se le E sono sei, la frase è quella. Se sono cinque o sette, no — e adesso sai anche quanto sei lontano, perché sai quante ne mancano o quante ce ne sono di troppo.
>
> Il controllo lo fai tu, e non è un'opinione: sei è sei.

Il cifrario, la frase e la proprietà sono generati e verificati da `build/blocco_295.py`. La frase in chiaro ha 44 lettere in 10 parole — contate per somma delle classi di frequenza **e** per scansione —, e la E vi compare sei volte. Lo script prova poi **tutti e ventisei gli scarti possibili** e conta le E in ognuno: gli altri venticinque danno 0, 1, 2, 3, 4 o 5 E, e **nessuno ne dà sei.** La proprietà stampata non accompagna la risposta: la individua.

Il pezzo che fa il lavoro è lo spostamento del confronto. Una macchina che corregge tiene la risposta attesa nascosta e restituisce un verdetto; qui **la risposta attesa è sostituita da una proprietà della risposta**, la proprietà è stampata sul foglio, e chi ha risposto la verifica contando. Nessuno tiene niente nascosto e nessuno pronuncia un giudizio: **il numero sei non è d'accordo o in disaccordo con nessuno.**

La proprietà scelta è un conteggio e non un confronto, ed è una scelta obbligata. Il sistema non sa manipolare le lettere dentro le parole, quindi non potrebbe verificare da sé quello che sta chiedendo di verificare — ma **chi ha il foglio in mano sì**, perché contare sei lettere in una frase di dieci parole è un gesto che riesce a chiunque e non richiede nessuna competenza. È lo stesso rovesciamento della tabella scritta prima del tiro di dado, registrato per la voce 281, casualità dichiarata: il limite del sistema non morde perché la verifica non passa dal sistema.

Il verdetto è **parziale e non binario**, ed è la parte che si perderebbe scrivendo una consegna più semplice. «Cinque invece di sei» dice che manca una occorrenza; «sette invece di sei» dice che ce n'è una di troppo. Un verdetto che dice solo *no* fa ricominciare, un verdetto che dice *quante ne mancano* fa correggere — la differenza già misurata alla voce 181, percorso lineare e alla voce 182, percorso a imbuto.

Dove si romperebbe. **La frase e la proprietà sono state scelte contandone le lettere, e il sistema non sa contare le lettere dentro le parole**: un modello a cui si chiedesse di produrre questa consegna da solo scriverebbe un numero sbagliato, e chi legge conterebbe sei E davanti a un foglio che ne dichiara cinque. Il rimedio è che la proprietà non sia sulle lettere ma su qualcosa che il modello sa maneggiare — quante **parole** ha la frase, quale sia l'ultima, quante righe occupa —, e allora la stessa struttura regge e vale un po' meno, perché quelle proprietà distinguono meno. **La forma sta nel formato; questo esempio in particolare è stato costruito con uno strumento che il sistema non ha**, e la distanza fra le due cose è esattamente il conteggio delle lettere.

## Da riprendere alla rassegna

**La correzione automatica si può sostituire con una proprietà verificabile della risposta, stampata insieme alla domanda.** È il risultato principale di questa scheda e non richiede né una macchina né una tabella nascosta: chi risponde conta, e il conteggio non è un'opinione. Da provare all'indietro su tutto il capitolo 5 e sul capitolo 12, dove quasi ogni forma ha una risposta sola.

**La proprietà verificabile va scelta fra quelle che il sistema sa costruire, e l'elenco di quelle che non sa è corto e noto.** Niente sulle lettere dentro le parole, niente sui minuti, niente su dove sia chi legge. Alla rassegna vale la pena scrivere quell'elenco una volta sola e poi usarlo come filtro, invece di riscoprirlo voce per voto.

**Un verdetto che dice quanto manca vale più di uno che dice sì o no, e costa lo stesso.** Vale per le macchine e vale per i fogli. È la scala già registrata fra segnale locale e segnale aggregato, e questa scheda ne aggiunge un caso in cui la scelta fra i due è letteralmente una parola nella consegna.

**Il metro contro cui si misurano le macchine è largo, e nessuno lo dice mai.** Due correttori umani esperti danno lo stesso voto fra il 53% e l'81% delle volte. Alla rassegna serve per tenere le proporzioni: quando si dice che una cosa «non si può valutare a macchina», il termine implicito è una valutazione umana che concorda con sé stessa poco più della metà delle volte.

**Un numero riportato da chi vende è stato accettato come misura per undici anni.** La gara Hewlett del 2012 dichiarò che le macchine erano affidabili quanto gli umani senza eseguire nessuna verifica statistica, **su richiesta di alcuni dei fornitori partecipanti.** È l'esempio più netto raccolto finora del promemoria già registrato: più una fonte dice quello che si sperava, più conviene guardare la nota.

