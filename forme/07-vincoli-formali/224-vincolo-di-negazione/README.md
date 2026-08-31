# Vincolo di negazione

- **Numero** 224 nell'enciclopedia, capitolo 7 — Vincoli formali
- **Si chiama anche** parola proibita, senza mai dirlo, giro di parole, perifrasi, circonlocuzione, preterizione, eufemismo, *Taboo*, *forbidden word*, *circumlocution*, *periphrasis*, *apophasis*, *paralipsis*, *praeteritio*, *euphemism*
- **In una riga** raccontare una cosa senza mai nominarla.
- **Fonti** `_reference/esercizi-e-sfide/taboo-game.txt`, `circumlocution.txt`, `apophasis.txt`, `euphemism.txt`, `it-perifrasi.txt`, `it-eufemismo.txt`, lette il 31 agosto 2026; `constrained-writing.txt` e `oulipo.txt` erano già fra le pagine locali. `it-eufemismo.txt` porta in cima l'avviso di essere un abbozzo, e da lì non è stato preso niente che non fosse terminologia.
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Far arrivare qualcuno a una cosa senza mai dire la parola che la nomina, e senza dire nemmeno le parole che la nominerebbero al posto suo.

Parti mobili:

- **Quante parole sono vietate.** Una sola è quasi niente, perché i sinonimi bastano. Il gioco commerciale ne vieta cinque oltre a quella, e cinque bastano a togliere la strada facile.
- **Quali cinque.** È tutta la difficoltà, e non sta in chi risponde: **una carta di questo tipo è progettata, non scelta a caso.** Le cinque parole giuste sono le cinque che verrebbero in mente per prime.
- **Se conta anche un pezzo di parola.** Nel gioco sì, ed è la clausola che rende il vincolo serio: se è vietato *baseball*, è vietato anche *base*.
- **Se si può indicare, disegnare, fare un verso.** Nel gioco no, e questa clausola esiste perché senza di lei il vincolo verbale si aggira senza parlare.
- **Se chi ascolta deve arrivarci.** Qui sì. C'è un altro modo di non nominare una cosa in cui invece si vuole che l'altro *non* ci arrivi, o in cui si nomina proprio dicendo che non si nomina: sono l'eufemismo e la preterizione, e stanno più sotto.

Il verbo generale è la voce 69, vincolare, e il confine con il capitolo è già dichiarato dalla voce 209, lipogramma.

## Da dove viene

La figura retorica ha duemila anni e due nomi. `circumlocution.txt` (letta il 31 agosto 2026) chiama **circonlocuzione** l'uso di un numero inutilmente grande di parole per esprimere un'idea, e ne dà come sinonimi *circumduzione*, *circumvoluzione*, *perifrasi*, *kenning* e *ambage*. L'esempio che porta è netto: dire «uno strumento che serve a tagliare cose come la carta e i capelli» invece di «forbici». La stessa pagina fa un'osservazione che ribalta la faccenda: **la maggior parte dei dizionari definisce le parole per circonlocuzione**, e cioè fa di mestiere quello che questo vincolo chiede di fare per gioco.

`it-perifrasi.txt` dà l'etimologia — dal greco *perì* e *phrazein*, «dire intorno» — e una fila di esempi italiani: «andò, prima della raccolta, a ricevere il premio della sua carità» per dire che un benefattore morì e andò in paradiso (Manzoni); «nella calotta del mio pensiero» per la propria mente (Montale); «re de l'universo» e «colui che tutto move» per Dio (Dante); e due perifrasi triviali sempre di Dante, «ed elli avea del cul fatto trombetta» e «'l tristo sacco / che merda fa di quel che si trangugia». **La stessa figura serve per la reverenza e per l'oscenità**, e sono le due ragioni per cui non si nomina una cosa.

L'altra faccia è la **preterizione**, che `apophasis.txt` chiama *apophasis* e anche *paralipsis*, *occupatio*, *occultatio*, *praeteritio*, *parasiopesis*: si porta un argomento negandolo, o negando che vada portato. L'esempio classico è «non ho intenzione di dirti che te l'avevo detto». La pagina la dà come parente retorica dell'ironia, e ne elenca gli usi: attaccare qualcuno scaricando la responsabilità dell'attacco («mi rifiuto di discutere la voce che il mio avversario sia un ubriacone»), toccare un argomento tabù, criticare per via diplomatica. Cita Cicerone nella *Pro Caelio*: «dimentico ormai le tue offese, Clodia, depongo la memoria del mio dolore». **La preterizione non è questo vincolo: è il suo rovescio**, perché la parola vietata la dice.

Il gioco è recente e ha un autore. `taboo-game.txt` dà ***Taboo***, disegnato da **Brian Hersch**, pubblicato da **Parker Brothers nel 1989** e poi passato a Hasbro. Da quattro a dieci giocatori, dai dodici anni, venti-sessanta minuti, e una clessidra da un minuto. Su ogni carta c'è la parola da far indovinare in alto e **cinque parole vietate** sotto. Chi dà gli indizi non può dirle; un «censore» della squadra avversaria tiene il ronzatore e lo schiaccia se scappano.

## Varianti e parenti

- **Perifrasi** — la figura, quando serve a dire meglio invece che a nascondere.
- **Circonlocuzione** — la stessa cosa quando serve ad aggirare un buco: `circumlocution.txt` osserva che la usano molto **chi ha un'afasia** e chi sta imparando una lingua, e che le strategie più comuni sono la frase relativa («i pompieri sono le persone che chiami quando la tua casa va a fuoco»), il sinonimo e la similitudine.
- **Eufemismo** — non nominare per non offendere o per superstizione: la fonte porta «il Vecchio Nick» per il diavolo, «la commedia scozzese» per *Macbeth*, «la dozzina del fornaio» per tredici.
- **Preterizione** — nominare dicendo di non nominare. Il rovescio esatto.
- **Insinuazione** e **equivoco** — le due forme in cui non si nomina per non impegnarsi.
- **Indovinello classico (enigma)** (110) — dove non nominare la cosa è la forma stessa dell'oggetto, e c'è una soluzione da trovare.
- **Definizione** (15) — perché una definizione di dizionario è una circonlocuzione riuscita, e la differenza è solo che nessuno deve indovinare.
- **Lipogramma** (209) — l'altro vincolo del capitolo che vieta dei segni; là si vietano lettere, qui parole.
- **Monovocalismo** (210) — perché anche là il magazzino è ridotto, ma per desinenza e non per argomento.

## Che cosa se ne sa

**«Non dirla» non vuol dire niente finché non lo si specifica, e servono otto clausole.** È il dato più utile raccolto, e viene dal regolamento di `taboo-game.txt`. Le ho contate in `build/check_224.py` e sono otto: non la parola da indovinare; non le cinque parole vietate; **non un pezzo di una parola vietata** — *base* dentro *baseball*; **non una forma diversa** — *marry* se è vietato *marriage*, *bridal* se è vietato *bride*; solo parlato, quindi niente gesti, versi, disegni; si può cantare solo se si cantano parole e non se si fischietta; niente rime con una parola vietata; niente abbreviazioni di una parola vietata. **Un divieto di una parola sola richiede sette regole in più per reggere**, e questa è la cosa che il vincolo insegna prima ancora di essere giocato.

**Quattro di quelle otto clausole riguardano le lettere dentro le parole**, e cioè l'operazione che questo sistema non sa fare (misurato, `ideas/10 §6`): la terza, la quarta, la settima e l'ottava. Un arbitro automatico di questo gioco è quindi fuori portata. **La via d'uscita qui non è stampare la procedura: è che l'arbitro c'è già.** È il primo caso in questo capitolo in cui il limite si aggira perché la casa contiene una persona che sa fare in un istante quello che il sistema non sa fare affatto, e questo va detto perché è una risorsa e non un ripiego.

**La difficoltà non sta in chi gioca, sta nella carta.** Le cinque parole vietate sono la parte progettata, e il criterio si legge nell'esempio della fonte: per far indovinare *baseball* sono vietate *sport*, *game*, *pastime*, *hitter*, *pitcher*. Sono le cinque parole che verrebbero in mente per prime. Vietare cinque parole a caso non produrrebbe nessuna difficoltà. **Il costo di questa forma è tutto a monte**, come alla voce 223, vincolo combinatorio, dove il lavoro stava nelle rime uguali di Queneau.

**La circonlocuzione è quello che fanno i dizionari e quello che fa chi ha perso una parola.** `circumlocution.txt` mette accanto tre cose che di solito non si mettono accanto: la definizione da dizionario, la strategia di chi impara una lingua, e la strategia di chi ha un'afasia. Sono la stessa operazione con tre valori diversi — mestiere, esercizio, necessità —, e questo dice che il vincolo non è artificiale: **è quello che si fa quando la parola non c'è.**

**Non ci sono misure.** Nessuna delle sei pagine lette contiene un dato su che cosa faccia questo esercizio a chi lo fa. `circumlocution.txt` riporta che chi ha un'afasia la usa, e non porta studi; `taboo-game.txt` è una descrizione di prodotto con l'elenco delle edizioni e dei colori del ronzatore. È lo stesso vuoto già registrato per tutte le altre voci di questo blocco.

**Una fonte italiana è un abbozzo.** `it-eufemismo.txt` porta l'avviso in cima e sono 3,3 kB; da lì non si è preso niente se non il termine. Con `it-registro.txt`, `it-diafasia.txt` e le quattro già registrate nel primo blocco fa dieci pagine italiane con un avviso in dieci sessioni.

## Esempi trovati

Dal gioco, 1989: far indovinare *baseball* senza dire *sport*, *game*, *pastime*, *hitter*, *pitcher* né *baseball*, e senza dire *base*.

Dal dizionario: «uno strumento che serve a tagliare cose come la carta e i capelli». È la definizione di forbici, ed è anche un indovinello riuscito.

Da chi impara una lingua: «un pomodoro granato è una specie di frutto, è rosso, e ha dentro tantissimi semini piccoli». La fonte lo dà come strategia normale di chi non ha ancora la parola, e le tecniche che elenca sono tre: frase relativa, sinonimo, similitudine.

Da Manzoni: «andò, prima della raccolta, a ricevere il premio della sua carità» — cioè morì.

Da Dante: «colui che tutto move», al primo verso del *Paradiso*.

Dalla superstizione: «il Vecchio Nick» per il diavolo, «la commedia scozzese» per *Macbeth*, «la dozzina del fornaio» per tredici. Sono tre parole non dette per tre motivi diversi, e nessuno dei tre è il gioco.

Da Cicerone: «dimentico ormai le tue offese, Clodia, depongo la memoria del mio dolore», detto a un processo, che è il modo di elencarle tutte.

## Una nostra versione

> ```
>  SENZA MAI DIRLO
>
>  Scegli una riga. Devi far indovinare quella parola a
>  qualcun altro, scrivendo. Non puoi usare la parola e non
>  puoi usare le cinque vietate. Nemmeno un pezzo di quelle
>  parole: se e vietata «palazzo», non puoi dire «palazzina».
>  Nemmeno una forma diversa: se e vietata «salire», non
>  puoi dire «salita».
>
>  DA FAR INDOVINARE  VIETATE
>  -------------------------------------------------
>  ascensore          salire    scendere  piano
>                     palazzo   bottone
>  -------------------------------------------------
>  temporale          pioggia   tuono     lampo
>                     nuvola    bagnato
>  -------------------------------------------------
>  gomito             braccio   piegare   osso
>                     punta     corpo
>  -------------------------------------------------
>  ombra              sole      luce      buio
>                     terra     seguire
>  -------------------------------------------------
>
>  Scrivi qui sotto, poi strappa lungo la riga tratteggiata
>  e da' solo la striscia a chi deve indovinare.
>
>  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
>
>
>
>
>
>  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
>
>  Quando ha indovinato, chiedigli quale parola gli e venuta
>  in mente per prima. Se e una delle cinque vietate, la
>  carta era fatta bene.
> ```

Una descrizione di prova per la prima riga: *Una stanza piccolissima che si sposta da sola dentro un edificio alto. Ci entri fermo e ne esci fermo, ma nel frattempo hai cambiato posto senza camminare.* Ventisette parole, **nessuna delle sei vietate**, e nessuna che contenga o sia contenuta in una di quelle: verificato in `build/check_224.py`, con due controlli distinti — uno sulle parole intere e uno sulle sottostringhe, quest'ultimo con un minimo di quattro lettere, perché sotto quella soglia dà solo falsi allarmi.

La griglia è stata generata dallo script e incollata, non composta a mano. Le quattro righe portano ventiquattro parole vietate in tutto.

Lo strappo è la parte che fa il lavoro. Il gioco commerciale ha bisogno di due squadre, di un cronometro e di un censore; questa versione non ha niente di tutto ciò, e ottiene la stessa asimmetria con una striscia di carta: **chi indovina non deve vedere la carta, e non vederla è una cosa che si ottiene strappando.** È il decimo caso, in questo capitolo, di stampare la procedura invece della cosa, e la faccia nuova è la stessa già usata alla voce 221, cadavere squisito e alla voce 222, Mad Libs vista da un terzo lato: prima la piega, poi il retro, adesso lo strappo. **La carta ha tre modi di nascondere sé stessa, e non gliene serve un quarto.**

L'ultima domanda — quale parola ti è venuta in mente per prima — è la verifica, e non verifica chi ha scritto: **verifica la carta.** Se la prima parola che viene in mente a chi indovina è fra le cinque vietate, quelle cinque erano quelle giuste.

Sta nel formato del progetto senza attriti: un A4 in bianco e nero, e un cronometro non serve perché il progetto non ne ha uno. **La cosa che il sistema non sa fare è arbitrare**, perché quattro delle otto clausole di questo gioco chiedono di guardare dentro le parole; ma l'arbitro è chi legge, e in casa c'è. Sul display da quattro righe per quarantaquattro caratteri ci sta una carta intera — la parola in alto e cinque sotto sono sei parole —, e quella è la parte più facile: la difficoltà è che qualcuno debba non vederla.

## Da riprendere alla rassegna

**Un divieto ha bisogno di sette regole in più per essere un divieto**, e questa è forse la cosa più generale che il capitolo 7 abbia prodotto. Vale per ogni vincolo dell'elenco: quello che una regola dice non è quello che una regola fa, e la differenza sta nelle clausole che nessuno scrive.

**L'arbitro può essere una persona invece che il sistema.** È la prima volta in tutto l'elenco che un limite tecnico si aggira così, e non è un ripiego: un adulto in casa riconosce in un istante che *salita* è una forma di *salire*. Alla rassegna vale la pena scorrere le voci già scritte cercando quelle che diventerebbero possibili con un arbitro umano dichiarato.

**Il lavoro sta nella carta e non nella partita.** Come la voce 223, vincolo combinatorio, questa forma è tutta a monte. Chi prepara le cinque parole vietate sta facendo la cosa difficile, e potrebbe essere l'esercizio migliore dei due — da provare: far preparare la carta invece che giocarla.

**La stessa figura serve a onorare e a offendere.** Le perifrasi di Dante per Dio e quelle per una flatulenza sono lo stesso meccanismo. Non nominare è un gesto senza segno proprio, e questo lo rende adatto a un pomeriggio in cui non si vuole decidere in anticipo che cosa significhi.

