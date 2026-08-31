# Risorse da spendere

- **Numero** 270 nell'enciclopedia, capitolo 9 — Meccaniche di gioco
- **Si chiama anche** risorse, gettoni, monete, punti azione, valuta di gioco, bilancio, budget, «hai dieci punti da distribuire», *resource management*, *action points*, *worker placement*, *engine building*
- **In una riga** quantità limitate da distribuire fra usi alternativi.
- **Fonti** `game-mechanics.txt`, `opportunity-cost.txt`, `it-costo-opportunita.txt`, `resource-management.txt`, `deck-building-game.txt`, lette il 31 agosto 2026. I conti sulle distribuzioni di un bilancio sono nostri, verificati in `build/check_270.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

C'è una quantità limitata di qualcosa, e più modi di usarla. Usarla in un modo vuol dire non usarla negli altri.

**È la seconda forma del capitolo che toglie, dopo la voce 266, vite / tentativi, e toglie in un modo diverso.** Le vite si consumano quando si sbaglia, cioè per un fatto che non si è scelto; le risorse si consumano quando si decide, ed è la decisione a costare. **Un contatore di vite dice quanto margine di errore resta; un contatore di risorse dice quanto potere di scelta resta.**

**E ha una parte che nessun'altra forma del capitolo ha: il costo di quello che non si è fatto.** `opportunity-cost.txt`: il costo opportunità di una scelta è **il valore della migliore alternativa a cui si rinuncia**, quando, date risorse limitate, bisogna scegliere fra alternative che si escludono a vicenda. La pagina italiana lo dice con un esempio che non riguarda il denaro: chi comincia a lavorare rinuncia a una parte del proprio tempo libero, e **il tempo libero è il costo opportunità di quella scelta** (`it-costo-opportunita.txt`).

Parti mobili:

- **Quanta ce n'è.** Il bilancio, che è la parte che decide se ci sia una scelta.
- **Quanti impieghi.** Due impieghi fanno un confronto, cinque fanno un problema.
- **Se gli impieghi rendono uguale.** Se rendono uguale non c'è nessuna decisione, e si può contare.
- **Se c'è un tetto per impiego.** Un tetto trasforma «metti tutto sul migliore» in un problema vero.
- **Se la risorsa si rigenera.** Una volta sola, oppure tanta per turno.
- **Se si può accumulare.** Tenerla da parte è un impiego come gli altri.
- **Se si compete per gli impieghi.** Nel piazzamento di lavoratori l'impiego migliore lo prende chi arriva prima, e la scarsità non è nella risorsa ma nel posto.

## Da dove viene

**Nel vocabolario dei giochi la voce esiste, è generica, e la fonte lo dichiara.** `game-mechanics.txt`: molti giochi comportano la gestione di risorse, e sono risorse i gettoni, il denaro, la terra, le risorse naturali, quelle umane e i punti; chi gioca **stabilisce dei valori relativi** fra i tipi di risorsa disponibili, nel contesto dello stato attuale del gioco e dell'esito desiderato, e le regole dicono come si aumentano, si spendono e si scambiano. La stessa pagina la elenca fra gli esempi comuni di meccanica insieme al passaggio del turno, al movimento delle pedine, alla raccolta di serie e all'offerta.

**Una variante ha una data e un primo esemplare con il nome.** `game-mechanics.txt`: il **piazzamento di lavoratori** è la meccanica in cui si assegna un numero limitato di gettoni a più postazioni che offrono azioni diverse. Stewart Woods identifica **_Keydom_, 1998** — poi rifatto come *Aladdin's Dragons* — come il primo gioco a metterla in pratica; **_Caylus_, 2005**, la rende popolare, e da lì diventa un elemento fisso del genere dei giochi tedeschi, con *Stone Age* e *Agricola*. La pagina segnala che il concetto è stato usato anche per analizzare altri tipi di gioco: Adams e Dormans descrivono l'assegnazione di compiti alle unità operaie di *StarCraft* come un caso di piazzamento di lavoratori.

**E ce n'è una che costruisce invece di consumare.** La **costruzione di un motore** è il meccanismo in cui si costruisce e si ottimizza un sistema che produce un flusso di risorse; *SimCity* ne è l'esempio in forma di videogioco — il denaro attiva meccanismi di costruzione, che aprono anelli di retroazione fra popolazione, posti di lavoro, energia, capacità di trasporto e tipi di zona. È la voce 272, costruzione di un motore, che viene subito dopo questa.

**Il concetto economico è più vecchio e più severo, e distingue due costi che si confondono sempre.** `opportunity-cost.txt`: i costi **espliciti** sono quelli diretti, con un esborso e un valore in denaro; i costi **impliciti** sono quelli di usare risorse che già si possiedono per una cosa invece che per un'altra, e la pagina dice che «spesso restano nascosti all'occhio nudo e non vengono resi noti», non si possono identificare con chiarezza né riportare, e non entrano in contabilità. **La stessa pagina esclude dal costo opportunità i costi già sostenuti e non recuperabili** — i costi sommersi —, che «non dovrebbero influenzare le azioni o le decisioni presenti e future».

**La fonte con il nome giusto non serve, e va detto.** `resource-management.txt` è di 6,7 kB e riguarda **la gestione delle risorse di un'organizzazione** — pianificazione, allocazione, personale —; non ha niente sui giochi né sulle decisioni sotto vincolo, ed è stata scaricata e non usata. La pagina italiana sul costo opportunità porta in cima l'avviso «non cita le fonti necessarie o quelle presenti sono insufficienti»: dà una definizione chiara e nessun dato, e va usata solo per quella.

## Varianti e parenti

- **Bilancio da distribuire** — tanto in tutto, e si sceglie dove metterlo.
- **Punti azione** — la risorsa è il numero di cose che si possono fare in un turno.
- **Piazzamento di lavoratori** — gli impieghi sono posti, e chi arriva prima li occupa.
- **Costruzione di un motore** — spendere adesso per avere più risorse dopo. Voce 272, costruzione di un motore.
- **Mazzo che si costruisce** — la risorsa è la composizione del proprio mazzo, e si spende per cambiarla. `deck-building-game.txt`: si comincia con un mazzetto di carte di poco valore, ogni turno se ne pescano alcune e si gioca, e con l'effetto delle carte giocate **si comprano altre carte da un mercato al centro del tavolo**. La pagina indica *StarCraft: The Board Game*, 2007, come il primo gioco del genere, e *Dominion*, Rio Grande Games, **2008**, come il primo di successo e quello che ne ha fissato lo standard.
- **Valuta di gioco** — la risorsa universale, scambiabile con tutte le altre.
- **Risorsa che si rigenera** — tanta per turno, e non si accumula.
- **Voce 266, vite / tentativi** — l'altro contatore che scende, ma per un errore invece che per una scelta.
- **Voce 256, punti** — dove il numero si accumula e non si spende. La differenza è dichiarata in quella voce: «un punto che resta è una misura; un punto che si spende è una moneta».
- **Voce 284, asta** — dove il prezzo lo fa la concorrenza invece del listino.
- **Voce 268, scelta con conseguenza** — la scelta senza quantità.

## Che cosa se ne sa

**Le fonti locali non contengono nessuna misura su che cosa faccia a chi gioca il dover distribuire una quantità limitata.** `game-mechanics.txt` è una tassonomia; `opportunity-cost.txt` è teoria microeconomica con esempi costruiti; `it-costo-opportunita.txt` non cita fonti. **Su questa forma non c'è nessun numero misurato, e va detto prima di tutto il resto.** Va verificato.

**Quello che si può fare è contare, e il conto dice quando una risorsa è davvero una decisione.** Dodici gettoni, tre impieghi con un rendimento e un tetto ciascuno — cinque punti a gettone fino a quattro gettoni, tre punti fino a sei, due punti fino a dieci. Le distribuzioni possibili sono **trentadue**, contate per enumerazione **e** per la formula di stelle e barre con inclusione ed esclusione sui tetti, concordi. Il massimo vale **42** ed è raggiunto da **una sola distribuzione**, quattro gettoni sul primo impiego, sei sul secondo e due sul terzo; il minimo vale **26** (`build/check_270.py`, massimo trovato per enumerazione **e** con la regola avida, che con valori lineari e tetti è dimostrabilmente ottima, concordi).

**E poi la parte che interessa: quante distribuzioni si avvicinano al massimo.**

```
     entro il   distribuzioni   su   quota
         100%               1   32    3,1%
          95%               3   32    9,4%
          90%               7   32   21,9%
          80%              16   32   50,0%
          70%              26   32   81,2%
```

**Una distribuzione su trentadue è perfetta, ma metà arrivano all'80% e quattro su cinque al 70%.** Questo è il modo di dire quanto una scelta di spesa conti: se quasi tutte le strade danno quasi lo stesso risultato, la risorsa è una decorazione. La stessa domanda posta alla voce 268, scelta con conseguenza per le scelte binarie, qui posta per le quantità.

**Il caso limite si costruisce e si conta.** Con lo stesso bilancio, gli stessi tetti e **tre impieghi che rendono tutti uguale**, le distribuzioni restano trentadue e **gli esiti distinti diventano uno solo**: tutte valgono 36. **Una risorsa da spendere fra impieghi che rendono uguale non è una risorsa: è un rito.** È l'analogo esatto dell'imbuto narrativo descritto alla voce 269, ramificazione, dove trentadue percorsi portano a un finale solo.

**Il costo opportunità del singolo gettone si può stampare, ed è la cosa più didattica di tutta la voce.** Aumentando il bilancio di uno alla volta e prendendo ogni volta la distribuzione migliore, il guadagno dell'ultimo gettone è **5, 5, 5, 5, poi 3, 3, 3, 3, 3, 3, poi 2, 2, 2…**: cala a gradini, e ogni gradino è il momento in cui l'impiego migliore si è esaurito e si passa al successivo. **La curva è il costo opportunità reso visibile: il quinto gettone rende tre e non cinque, e la differenza è esattamente quello che si è perso a non poter mettere altro sul primo impiego.**

**Sui costi sommersi la fonte è netta e vale la pena riportarla, perché è il rovescio della forma.** `opportunity-cost.txt`: i costi già sostenuti e non recuperabili «restano immutati e non dovrebbero influenzare le azioni o le decisioni presenti e future». **Una risorsa spesa non entra nel conto di che cosa fare adesso, e questa è la cosa che chi gioca sbaglia più spesso.** La pagina non riporta nessuno studio su quanto spesso venga sbagliata: cercato con grep, non c'è nessuna sezione sperimentale e nessun esperimento con dei partecipanti.

## Esempi trovati

*Keydom*, 1998, indicato da Stewart Woods come il primo gioco con il piazzamento di lavoratori; e *Caylus*, 2005, che lo ha reso popolare.

*Stone Age* e *Agricola*, dove il numero di lavoratori è la risorsa e le postazioni sono contese.

*StarCraft*, dove Adams e Dormans leggono l'assegnazione dei compiti alle unità operaie come lo stesso meccanismo.

*SimCity*, dove il denaro attiva costruzioni che aprono anelli di retroazione fra popolazione, posti di lavoro, energia, trasporti e zone.

*Ra*, riportato da `game-mechanics.txt` come esempio di offerta: chi vince deve pagare il privilegio con una forma di risorsa di gioco.

*I coloni di Catan*, dove una pedina neutrale — il brigante — riduce la produzione di risorse di chi le sta vicino, e chi gioca la sposta di solito dove danneggia di più chi sta vincendo. È una risorsa che si toglie a qualcun altro.

L'esempio non monetario della pagina italiana: chi comincia a lavorare rinuncia a una parte del proprio tempo libero, e quel tempo è il costo della scelta.

## Una nostra versione

**Il limite dominante è mite, ed è la seconda voce del blocco che il formato regge.** Una risorsa si conta in gettoni, non in minuti: per il criterio del capitolo sta dentro un foglio. Restano i due limiti già trovati alla voce 266, vite / tentativi: **la carta non può obbligare** — nessuno impedisce di spendere tredici gettoni quando ne hai dodici — e **il foglio non ricorda** che cosa hai speso ieri. Entrambi si aggirano con la stessa mossa: la spesa si scrive, e quello che si scrive resta visibile.

> **Dodici gettoni**
>
> Hai dodici gettoni. Ci sono tre cose in cui puoi metterli, e ognuna ha un tetto.
>
> ```
>   ┌──────────┬───────────────────┬──────────────┬─────────────┐
>   │  dove    │  rende a gettone  │  al massimo  │  ne metto   │
>   ├──────────┼───────────────────┼──────────────┼─────────────┤
>   │    A     │         5         │      4       │             │
>   ├──────────┼───────────────────┼──────────────┼─────────────┤
>   │    B     │         3         │      6       │             │
>   ├──────────┼───────────────────┼──────────────┼─────────────┤
>   │    C     │         2         │     10       │             │
>   └──────────┴───────────────────┴──────────────┴─────────────┘
>
>              totale gettoni  ────────      totale punti  ────────
> ```
>
> Prima riempi la colonna a destra come ti pare, e fai il totale.
>
> **Adesso i fatti.** Le distribuzioni possibili sono **32**. La migliore vale **42**, la peggiore **26**, e la migliore e' **una sola**. Meta' delle trentadue arrivano almeno a 34, cioe' all'80% del massimo.
>
> **Dov'e' finita la tua?** Scrivi qui il tuo totale e di' quante ne restano sopra di te:
>
> ```
>   il mio totale ────────
> ```
>
> E l'ultima, che e' la domanda vera: **il quinto gettone quanto ti ha reso?** Il primo, il secondo, il terzo e il quarto rendono cinque l'uno. Il quinto non puo' rendere cinque, perche' A e' pieno. Scrivi quanto rende ognuno dei dodici, in fila:
>
> ```
>   5  5  5  5  ──  ──  ──  ──  ──  ──  ──  ──
> ```
>
> Quella fila che scende a gradini ha un nome in economia: **si chiama costo opportunita', ed e' il valore di quello che non hai potuto fare.**

Il foglio non impedisce di barare, e non prova a farlo: dichiara i numeri veri dopo che la distribuzione è stata scritta, così che l'unica cosa che si possa confrontare sia la propria con quelle possibili. La fila dei dodici guadagni è la parte che insegna qualcosa: **il costo opportunità non è una definizione da imparare, è la differenza fra il quarto gettone e il quinto**, ed è visibile appena la si scrive.

**Dove si rompe.** Si rompe in due punti già noti e in uno nuovo. I due noti: nessuno impedisce di scrivere tredici, e il foglio non sa che cosa si sia speso ieri. Quello nuovo: **qui i gettoni non comprano niente**, e una risorsa che non compra è un esercizio di aritmetica. Perché sia una risorsa vera il gettone deve procurare qualcosa che si desidera, e questo il foglio può soltanto raccontarlo. **La versione piena richiederebbe che i gettoni comprassero pezzi di un pomeriggio vero**, ed è la cosa che il sistema potrebbe fare e non fa: chi stampa il foglio decide che cosa c'è dentro.

## Da riprendere alla rassegna

**Il conto delle distribuzioni vicine al massimo dice se una risorsa sia una decisione o un rito.** Una su trentadue è perfetta, ma metà arrivano all'80%: la scelta conta, e conta poco. **Con tre impieghi che rendono uguale, trentadue distribuzioni danno un unico esito**, e la risorsa scompare pur restando stampata. Da usare come prova su qualunque cosa il progetto proponga di distribuire: **se le strade valgono tutte lo stesso, la distribuzione è un rito.**

**La fila dei guadagni marginali è il modo più economico di far vedere un concetto vero.** Dodici numeri in fila — 5, 5, 5, 5, 3, 3, 3, 3, 3, 3, 2, 2 — contengono il costo opportunità per intero, senza definizioni e senza matematica oltre la sottrazione. **È una delle cose più dense trovate in tutta l'enciclopedia per rapporto fra inchiostro e contenuto**, e si accosta alla voce 54, misurare, dove due misure che non coincidono contengono l'idea di errore.

**Il secondo criterio trovato alla voce 266, vite / tentativi vale anche qui, e con lo stesso esito.** Un contatore di risorse conta eventi e si scrive su carta; ma **spendere è una restrizione, e una restrizione ha bisogno di qualcuno che la faccia valere.** La via d'uscita usata qui — dichiarare che non si può obbligare e usare la scrittura come tracciato invece che come freno — è la stessa e funziona due volte. **Alla rassegna vale la pena guardarla come una mossa generale e non come un ripiego: rinunciare a obbligare e chiedere di registrare.**

**Il costo sommerso è nominato dalle fonti come l'errore più comune e non è misurato da nessuna delle 850 pagine locali.** «I costi già sostenuti non dovrebbero influenzare le decisioni presenti»: è una prescrizione, non una descrizione. **Da guardare accanto alla voce 260, serie di giorni (streak), che funziona esattamente perché chi ha trenta giorni alle spalle li tratta come una cosa da proteggere e non come una cosa già spesa.** Sono la stessa asimmetria vista da due parti, ed è la prima volta che due voci di questo capitolo si incontrano su un punto di psicologia invece che di struttura.
