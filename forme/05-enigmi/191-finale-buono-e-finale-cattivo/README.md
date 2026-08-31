# Finale buono e finale cattivo

- **Numero** 191 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Meccanismi da escape room»
- **Si chiama anche** finali multipli, doppio finale, esito buono ed esito cattivo, storia che si biforca, *good ending / bad ending*, *multiple endings*
- **In una riga** la stessa storia arriva a due esiti, uno migliore dell'altro.
- **Fonti** `escape-room.txt`, `it-escape-room.txt`, `gamebook.txt`, `choose-your-own-adventure.txt`, `nonlinear-gameplay.txt`, `nonlinear-narrative.txt`, lette il 31 agosto 2026. Il meccanismo dell'esempio e i conti sulle strade sono nostri, verificati in `build/check_191.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

Lo stesso materiale produce due esiti diversi, e quale dei due si ottiene dipende da quello che chi lavora ha fatto. Non è una valutazione data alla fine: **è una fine diversa**, scritta prima e scelta dai fatti.

**Il confine con il capitolo 11 va dichiarato adesso, perché è vicino.** Là ci sarà come un'attività si chiude come esperienza — che cosa resta, come si saluta, che cosa si porta via. **Qui c'è un meccanismo: due testi stampati, una regola che dice quale dei due si legge.** Sono due cose diverse, e il capitolo 11 è ancora tutto da scrivere.

Parti mobili:

- **Quanti finali.** Due è il caso minimo e il più comune; oltre i quattro nessuno li conta più.
- **Che cosa decide.** Una scelta sola, la somma di molte scelte, oppure se si è finito nel tempo.
- **Se uno dei due è un fallimento.** È la differenza principale, e le due tradizioni hanno risposto in modo opposto.
- **Se si può rileggere l'altro.** Su carta sì, sempre, e questo cambia tutto.
- **Quando si sa quale si è preso.** Alla fine, quasi sempre; e quasi mai si sa perché.

## Da dove viene

**Dalle escape room, dove i due finali sono l'esito del tempo.** `escape-room.txt`: i giocatori possono ricevere esperienze diverse a seconda che riescano o falliscano, «nella forma di *good endings* e *bad endings*». Il finale buono di solito è uscire vivi entro il tempo, completare l'obiettivo, o fermare la minaccia o l'antagonista della storia; **quello cattivo rappresenta di solito i giocatori uccisi dalla forza che muove la storia, o l'antagonista che viene a prenderli allo scadere del tempo.** La stessa pagina registra che alcune stanze hanno cominciato a incorporare percorsi ramificati che cambiano l'esperienza in base alle decisioni.

**La fonte italiana ha una tassonomia che l'inglese non ha, e mette questa forma in cima.** `it-escape-room.txt` distingue quattro tipi: la **puzzle room**, che è una serie di enigmi senza filo conduttore; la **thematic room**, dove un tema guida il tipo di indizi; la **narrative room**, dove i giocatori assumono un ruolo; e la **hypernarrative room**, in cui **le scelte dei giocatori e le soluzioni trovate influiscono direttamente sulla trama.** È il quarto tipo, ed è quello che questa voce descrive.

**Dai libri-gioco viene la distinzione che conta, e le due tradizioni hanno deciso il contrario.** `gamebook.txt`: nelle avventure in solitario molti libri hanno **un solo finale «riuscito» e tutti gli altri sono «fallimenti»**, e la fonte tira la conseguenza — «così il libro-gioco diventa un enigma, perché solo pochi percorsi, o uno solo, portano alla vittoria». I romanzi a trama ramificata invece «tendono a occuparsi della risoluzione narrativa più che del vincere o perdere, e quindi hanno spesso **diversi finali che si possono considerare ugualmente riusciti**».

**Due finali di cui uno è un fallimento e due finali che valgono uguale sono due macchine diverse con lo stesso nome.**

**I numeri della serie più venduta ci sono.** `choose-your-own-adventure.txt`: la collana *Choose Your Own Adventure*, dall'idea di Edward Packard, pubblicata da Bantam Books, ha venduto **più di 250 milioni di copie fra il 1979 e il 1998**, in **184 titoli** e **40 lingue**. Il numero di finali va **da 44 nei primi titoli a 7 negli ultimi**. E la fonte dichiara che **non c'è nessuno schema riconoscibile fra i titoli quanto al numero di pagine per finale, al rapporto fra finali buoni e finali cattivi, o al procedere avanti e indietro nel libro** — cosa che, scrive, dà un senso realistico di imprevedibilità e rende possibile rileggere.

**E c'è il finale che si può raggiungere solo sbagliando.** In *Inside UFO 54-40* esiste un finale — il pianeta paradiso — che **si raggiunge soltanto barando o girando pagina per errore**, e l'unica via d'uscita da lì è chiudere il libro e ricominciare dalla prima pagina.

**Sui costi la fonte è netta, e riguarda chi costruisce.** `nonlinear-gameplay.txt`: le storie lineari costano meno tempo e meno denaro, perché c'è una sola sequenza di eventi e nessuna decisione importante da tenere sotto controllo. Diversi giochi della serie *Wing Commander* offrivano una trama ramificata, e **la cosa fu poi abbandonata perché troppo cara.** Le storie non lineari aumentano la probabilità di errori e assurdità se non sono provate bene. E alcuni giocatori hanno reagito male alle storie ramificate **perché è difficile e faticoso vedere tutto il contenuto che si è pagato.**

**Il compromesso ha un nome e una forma:** storie che si biforcano e poi si richiudono in una sola linea, convergendo su un evento inevitabile, «dando l'impressione di una non linearità senza usare una narrazione interattiva».

## Varianti e parenti

- **Due finali di cui uno è un fallimento** — la forma da libro-gioco d'avventura e da escape room.
- **Due finali che valgono uguale** — la forma da romanzo a trama ramificata.
- **Finale deciso da una scelta sola** — un bivio, e tutto il resto non conta.
- **Finale deciso da una somma** — molte scelte piccole, e nessuna decisiva.
- **Biforcazione che si richiude** — si sceglie, e si arriva comunque allo stesso posto.
- **Finale raggiungibile solo per errore** — esiste, e ha un esempio famoso.
- **Voce 189, conto alla rovescia** — perché nelle escape room a decidere il finale è il tempo.
- **Voce 188, oggetto che cambia significato** — l'altra forma in cui lo stesso materiale dice due cose.
- **Voce 183, percorso aperto** — l'altra forma in cui a decidere è chi lavora.
- **Voce 25, dialogo scritto** — dove erano già comparse la prima e l'ultima battuta date e il mezzo libero.

## Che cosa se ne sa

**Che cosa decide il finale cambia il peso di ogni singola decisione, e si conta.** Questa è la cosa che questa voce può aggiungere, e `build/check_191.py` la calcola su cinque scelte binarie, cioè trentadue strade.

- **A soglia**, se il finale dipende da quante scelte di un certo tipo si sono fatte: le strade si dividono in **16 e 16**, e **ogni singola scelta cambia il finale in 12 strade su 32** — la stessa cifra per tutte e cinque.
- **Ad albero**, se il finale dipende dalla prima scelta e basta: le strade si dividono ancora in **16 e 16**, ma **la prima scelta cambia il finale in 32 strade su 32 e le altre quattro in nessuna.**

**Due meccanismi che dall'esterno sembrano identici — cinque domande, due finali, metà e metà — distribuiscono il peso in due modi opposti**, e chi risponde non ha modo di sapere in quale dei due si trova.

**Nel caso a soglia, 20 strade su 32 sono a un passo dal confine**, cioè hanno esattamente due o esattamente tre risposte del tipo che conta. Vuol dire che in venti casi su trentadue **una sola risposta diversa avrebbe dato l'altro finale**, e questo è il genere di cosa che si può stampare in fondo a un foglio.

**Il rapporto fra finali buoni e finali cattivi non è stato progettato da nessuno**, e la fonte lo dichiara per la collana che ha venduto duecentocinquanta milioni di copie: nessuno schema riconoscibile, e la cosa è considerata un pregio perché produce imprevedibilità.

**Un finale cattivo non è la stessa cosa di un fallimento, e le escape room lo sanno.** La fonte scrive che chi non finisce «fallisce», e subito dopo che la maggior parte dei gestori cerca di far divertire i clienti anche quando non vincono, concedendo tempo in più o una visita accelerata a quello che restava. **Il finale cattivo è un testo; il fallimento è non avere nessun testo**, e la differenza è tutto quello che un secondo finale compra.

**Costa in modo più che proporzionale, ed è documentato con un caso.** Una serie di videogiochi abbandonò la trama ramificata perché troppo cara. Con il costo delle strutture ad accumulo registrato alla voce 186, sblocco progressivo dello spazio fanno due casi in cui una fonte dichiara che la struttura più ricca è la più cara.

**Su carta il difetto principale sparisce.** «È faticoso vedere tutto il contenuto» è un problema di chi deve rigiocare; **un foglio ha i due finali stampati tutti e due, e leggere quello che non è toccato costa dieci secondi.** È il caso più netto del blocco in cui un limite del supporto d'origine non esiste sul nostro.

**Non c'è nessun dato sull'effetto.** Nessuna delle fonti misura se avere due finali cambi quanto una cosa piaccia, quanto la si ricordi, o quanto la si rifaccia. **Va verificato.**

## Esempi trovati

I *good endings* e i *bad endings* delle escape room, con l'antagonista che entra allo scadere del tempo.

La *hypernarrative room*, il quarto e ultimo tipo della classificazione italiana, in cui le soluzioni trovate cambiano la trama.

*Choose Your Own Adventure*, 184 titoli, 250 milioni di copie, e un numero di finali che scende da 44 a 7 senza che nessuno abbia deciso il rapporto fra buoni e cattivi.

Il pianeta paradiso di *Inside UFO 54-40*, un finale che si raggiunge solo barando o sbagliando pagina, e da cui si esce solo chiudendo il libro.

*Consider the Consequences!* di Doris Webster e Mary Alden Hopkins, 1930, che dichiarava «una dozzina o più» di finali diversi secondo il gusto del lettore.

*Night of January 16th* di Ayn Rand, 1936: alcuni spettatori vengono scelti come giuria, e il loro verdetto decide il finale, colpevole o innocente.

## Una nostra versione

> **Cinque porte e due finali**
>
> Una piccola storia. **A ogni porta scegli, e non sai che cosa cambia.**
>
> ```
>   1  Il portone del palazzo è socchiuso.
>      □  entro subito          □  prima giro intorno
>
>   2  Nell'atrio c'è un citofono con un nome cancellato.
>      □  suono                 □  salgo a piedi
>
>   3  Al primo piano una porta è aperta di un dito.
>      □  la spingo             □  tiro dritto
>
>   4  Sul pianerottolo c'è una scatola con sopra il tuo nome.
>      □  la apro adesso        □  la porto via chiusa
>
>   5  L'ultima rampa è al buio.
>      □  salgo lo stesso       □  accendo la luce
> ```
>
> **Conta le crocette che hai messo nella colonna di sinistra.**
>
> ```
>   ────
> ```
>
> **Se sono zero, una o due, leggi il finale A. Se sono tre, quattro o cinque, leggi il finale B.**
>
> ```
>   ┌─ FINALE A ───────────────────────────────────────────────┐
>   │  Arrivi in cima e il palazzo è vuoto da anni. Hai fatto  │
>   │  tutto con calma e non hai visto niente. Sotto la porta  │
>   │  dell'ultimo appartamento c'è un biglietto, e lo prendi. │
>   └──────────────────────────────────────────────────────────┘
>
>   ┌─ FINALE B ───────────────────────────────────────────────┐
>   │  Arrivi in cima e qualcuno ci è arrivato prima di te.    │
>   │  Hai fatto in fretta e hai visto molte cose, e adesso    │
>   │  una di quelle cose ti sta aspettando sul pianerottolo.  │
>   └──────────────────────────────────────────────────────────┘
> ```
>
> **Adesso leggi anche l'altro.** Sono stampati tutti e due e non c'è nessun motivo per non farlo.
>
> ---
>
> **Tre domande, e non sono sulla storia.**
>
> ```
>   Secondo te quale dei due è il finale buono?
>   □ A    □ B    □ non si capisce
>
>   Quale singola crocetta, cambiata da sola, ti avrebbe
>   portato all'altro finale?          ────
>
>   Ce n'era una che contava più delle altre?   □ sì   □ no
> ```
>
> **L'ultima risposta è no, e si può dimostrare.** Le strade possibili sono **32**: sedici portano ad A e sedici a B. E ognuna delle cinque scelte, cambiata da sola, sposta il finale in **12 strade su 32** — lo stesso numero per tutte e cinque. Nessuna porta conta più di un'altra.
>
> Se invece avessi scritto che il finale dipende dalla **prima** scelta e basta, i finali sarebbero ancora sedici e sedici, ma la prima scelta avrebbe cambiato tutto in **32 strade su 32** e le altre quattro **in nessuna.** Dal foglio le due storie sembrano identiche.

I conti sono in `build/check_191.py`, che enumera tutte e trentadue le combinazioni di cinque risposte binarie. Nella regola a soglia: **16** strade al finale A, **16** al B, **12 su 32** per ognuna delle cinque scelte, e **20 strade su 32** che stanno a una crocetta dal confine. Nella regola ad albero: ancora 16 e 16, ma **32 su 32** per la prima scelta e **0** per le altre.

I due finali sono scritti in modo che nessuno dei due sia un fallimento, ed è una scelta e non una gentilezza: **la tradizione dei libri-gioco d'avventura mette un finale riuscito e tutti gli altri falliti, quella dei romanzi a trama ramificata li fa valere uguale.** La prima domanda in fondo — quale dei due è il finale buono — non ha risposta, e la casella «non si capisce» è quella giusta.

La riga che dice di leggere anche l'altro finale è l'unica parte del foglio che non esisterebbe altrove. In un libro rileggere costa sfogliare, in un gioco costa rigiocare, e la fonte registra che i giocatori se ne lamentano; **su un foglio i due finali sono a tre centimetri di distanza.** Il supporto toglie gratis il difetto principale della forma.

Il conto finale è la parte progettata. Non aggiunge niente alla storia e dice una cosa sul foglio: **che due meccanismi indistinguibili da fuori distribuiscono il peso delle decisioni in modo opposto.** È un'informazione su come sono fatte le cose che si ricevono, e non richiede di credere a nessuno perché si può rifare contando.

Dove si romperebbe: **non si rompe**, ed è la voce del blocco che costa meno di tutte — nessun materiale, nessun tempo, nessun'altra persona, e una sola facciata. La fotografia mostra le cinque crocette, e da quelle il sistema ricava quale finale è stato letto senza doverlo chiedere. Sul pannello da quattro righe funzionerebbe anche meglio per la parte delle scelte, **ma i due finali stampati insieme sono il punto**, e un supporto che ne mostra uno solo per volta riporta la forma al difetto che la carta le toglie.

## Da riprendere alla rassegna

**Che cosa decide il finale cambia il peso di ogni decisione, e si conta.** A soglia: 12 strade su 32 per ognuna delle cinque scelte. Ad albero: 32 su 32 per la prima e 0 per le altre. **Dall'esterno i due meccanismi sono indistinguibili**, e alla rassegna vale la pena chiedersi quale dei due si voglia, perché è una scelta che nessuno fa consapevolmente.

**Un finale cattivo non è un fallimento, e la differenza è che c'è un testo.** Chi non finisce una escape room «fallisce» e non riceve niente; chi arriva a un finale cattivo riceve una fine. **Per un sistema che consegna un foglio al giorno, un secondo finale è il modo più economico di fare in modo che non finire non voglia dire non aver ottenuto niente.**

**Le due tradizioni hanno deciso il contrario, e con lo stesso nome.** Un finale riuscito e tutti gli altri falliti, contro molti finali ugualmente riusciti. **È il secondo disaccordo esplicito fra comunità raccolto in questo blocco**, dopo quello fra il problema di scacchi e il racconto giallo della voce 185, rossa aringa (red herring), e conviene tenerne il conto.

**Il rapporto fra finali buoni e cattivi non è stato progettato da nessuno**, nemmeno nella collana che ha venduto duecentocinquanta milioni di copie, e la fonte lo considera un pregio. **È il primo caso in cui l'assenza di un disegno è dichiarata come una qualità**, e vale la pena guardarlo insieme a tutte le voci in cui si è cercato un parametro che non esisteva.

**Il supporto toglie gratis il difetto principale della forma.** «È faticoso vedere tutto il contenuto» è la lamentela documentata dei giocatori; su un foglio i due finali sono stampati entrambi. **Da censire tutte le forme che su carta perdono il loro difetto d'origine**, perché sono quelle su cui questo progetto ha un vantaggio e non un handicap.

**Il capitolo 11 confina qui e non è ancora cominciato.** Là ci sarà come un'attività si chiude come esperienza, qui c'è un meccanismo che produce due testi. **Quando si scriverà quel capitolo, questa voce va riletta**, perché è la sola del capitolo 5 che parli di come una cosa finisce.
