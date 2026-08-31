# Asta

- **Numero** 284 nell'enciclopedia, capitolo 9 — Meccaniche di gioco
- **Si chiama anche** incanto, asta al rialzo, asta a busta chiusa, gara d'offerta, licitazione, offerta, rilancio, *auction*, *bidding*, chi offre di più
- **In una riga** chi offre di più si prende la cosa.
- **Fonti** `auction.txt`, `auction-theory.txt`, `vickrey-auction.txt`, `english-auction.txt`, `dutch-auction.txt`, `first-price-sealed-bid-auction.txt`, `winners-curse.txt`, `revenue-equivalence.txt`, `bid-shading.txt`, `bidding-fee-auction.txt`, `game-mechanics.txt` sezione «Auction or bidding», tutte lette il 31 agosto 2026; `it-asta.txt` è una pagina di disambiguazione di 2 540 byte e non serve; `bidding.txt`, `common-value-auction.txt` e `combinatorial-auction.txt` sono state lette e non aggiungono niente alle altre; i conti sono in `build/check_284.py`
- **Stato della ricerca** fatta, 31 agosto 2026

## Che cos'è

C'è una cosa sola e più di uno la vuole. Invece di decidere chi la prende, si decide **come** si decide: ognuno dichiara quanto è disposto a dare, e la cosa va a chi dichiara di più. Il prezzo esce dal procedimento invece di essere fissato prima.

Parti mobili, e sono più di quante sembri:

- **Chi vede che cosa.** Le offerte sono pubbliche mentre si fanno, oppure chiuse e aperte tutte insieme.
- **In che direzione si muove il prezzo.** Sale, come nell'asta inglese; o scende da una cifra alta finché qualcuno la ferma, come nell'asta olandese.
- **Che cosa paga il vincitore.** La propria offerta, oppure la seconda più alta.
- **Che cosa pagano gli altri.** Di norma niente. Se pagano tutti, la forma cambia natura: è l'asta a pagamento, e `bidding-fee-auction.txt` ne descrive la versione commerciale.
- **La moneta.** `game-mechanics.txt`, sezione «Auction or bidding», distingue due casi: si paga con una risorsa del gioco — punti, denaro finto — oppure **l'offerta è la promessa di ottenere un risultato, e chi non lo ottiene paga una penale**. È il meccanismo del contratto nel bridge.
- **Il prezzo di riserva.** Sotto una certa cifra non si vende.
- **Quando finisce.** È la parte che quasi tutte le aste faticano a risolvere, e su cui la storia ha inventato di più.

Togliendo la concorrenza — un solo offerente — non resta niente: il ricavo di un'asta con un offerente solo è zero, ed è il primo dei conti qui sotto.

## Da dove viene

La parola viene da *auctus*, participio passato di *augeō*, «io aumento» (`auction.txt`). Le aste sono documentate almeno dal 500 a.C.: Erodoto racconta che a Babilonia si tenevano ogni anno aste di donne da sposare, e che era illegale dare in sposa una figlia fuori dall'asta. Nell'impero romano i soldati piantavano una lancia per terra e vendevano intorno a essa il bottino, schiavi compresi. **Nel 193 d.C. la guardia pretoriana uccise l'imperatore Pertinace e mise all'asta l'impero**: vinse Didio Giuliano a 6 250 dracme per pretoriano, e fu decapitato due mesi dopo. La storia di questa forma è quasi tutta di questo genere, e la scheda la riporta perché è la storia vera.

Dopo la fine dell'impero le aste sparirono quasi del tutto in Europa fino al Settecento. Il ritorno porta con sé l'invenzione più bella della famiglia: **l'asta a candela**. In Inghilterra fra il Seicento e il Settecento l'asta finiva quando si spegneva la fiamma di una candela, **perché nessuno potesse sapere esattamente quando finiva e fare l'ultima offerta all'ultimo istante**. Compare nei registri della Camera dei Lord nel 1641; nel 1660 Samuel Pepys annota due volte che l'Ammiragliato vendette navi in eccesso «per un pollice di candela», e riferisce il suggerimento di un offerente molto fortunato: **poco prima di spegnersi, lo stoppino ha sempre un piccolo guizzo**, e lui gridava lì la sua offerta finale. A volte, al posto della candela, si usava un altro evento imprevedibile — una corsa a piedi.

La prima casa d'aste conosciuta è la Stockholms Auktionsverk, fondata nel 1674 dal barone Claes Rålamb; Sotheby's nasce a Londra l'11 marzo 1744, Christie's nel 1766.

La teoria è del Novecento e comincia con William Vickrey, che dà il nome all'asta a busta chiusa e secondo prezzo. `revenue-equivalence.txt` enuncia il risultato che governa tutta la famiglia: date certe condizioni, **qualunque meccanismo che assegni la cosa agli stessi offerenti produce lo stesso ricavo atteso**.

## Varianti e parenti

- **Asta inglese** — a voce, il prezzo sale, si vede chi offre.
- **Asta olandese** — il prezzo parte alto e scende; il primo che dice basta prende. Si contratta in un istante invece che in un'ora.
- **Busta chiusa a primo prezzo** — si scrive, si apre insieme, chi ha scritto di più paga quello che ha scritto.
- **Busta chiusa a secondo prezzo** (Vickrey) — chi ha scritto di più paga la seconda cifra.
- **Asta a candela** — finisce quando finisce una cosa fisica, e nessuno sa quando.
- **Asta a pagamento per offerta** — ogni rilancio costa, e chi perde paga lo stesso.
- **Asta combinatoria** — si offre su insiemi di cose e non su una alla volta.
- **Asta al ribasso** (*reverse auction*) — chi chiede meno prende l'incarico.
- **Contratto** — l'offerta è una promessa di risultato, e mancarla costa. È il bridge.
- **Voce 270, risorse da spendere** — l'asta è il modo di distribuire una risorsa quando la contesa è con altri invece che con sé stessi.
- **Voce 72, negoziare** — l'altra strada per assegnare una cosa contesa, senza un prezzo.
- **Voce 259, classifica** — l'altra forma che mette le persone in fila con un numero.
- **Voce 285, deduzione sociale** e **voce 283, bluff** — le altre due forme del capitolo che chiedono più di una persona; l'asta ne chiede almeno due, e i conti qui sotto dicono quanto vale la terza.

## Che cosa se ne sa

L'equivalenza del ricavo è il risultato centrale e si può rifare. Con *n* offerenti i cui valori sono estratti a caso in modo uniforme, **l'asta a secondo prezzo con offerte sincere e l'asta a primo prezzo con l'offerta di equilibrio, che è (n−1)/n del proprio valore, danno esattamente lo stesso ricavo atteso, (n−1)/(n+1)** (`build/check_284.py`, per statistiche d'ordine dell'uniforme e per simulazione su 200 000 aste; le due strade coincidono entro cinque millesimi per n da 2 a 10). Due procedimenti che sembrano diversissimi — uno in cui si dice il vero e uno in cui si mente per costruzione — producono lo stesso numero.

Da lì esce il conto che riguarda direttamente una casa. **Il ricavo cresce con il numero di offerenti così: da uno a due porta 0,3333; da due a tre 0,1667; da tre a quattro 0,1000; da quattro a cinque 0,0667; da cinque a sei 0,0476; da sei a sette 0,0357.** La seconda persona vale dodici volte l'ottava. È lo stesso profilo già misurato alla voce 276, cooperazione con le figurine — dove la seconda persona portava 167,8 pezzi e la sesta 16,4 — e adesso ricompare su una struttura completamente diversa. **Un'asta a due persone è già un'asta; a tre è quasi tutto quello che si può avere.**

L'asta a secondo prezzo ha la proprietà per cui è stata inventata: dire il vero è la cosa migliore da fare, e non serve sapere niente sugli altri. **Con un valore proprio di 7 e un avversario che offre a caso un numero fra 0 e 10, il guadagno atteso cresce fino all'offerta 7, resta identico a 8, e da 9 in poi cala** (`build/check_284.py`, tabella esatta in frazioni e controprova per simulazione su 200 000 aste per ogni riga). Offrire 9 invece di 7 costa 0,0909 a mano. Offrire meno costa di più: offrire 4 invece di 7 costa 0,5455. **Non c'è una punizione per aver detto il vero, e non c'è un premio per aver mentito in nessuna delle due direzioni.**

La maledizione del vincitore è il rovescio, e vale quando la cosa vale lo stesso per tutti ma nessuno sa quanto. `winners-curse.txt`: chi vince è chi ha stimato di più, quindi — se le stime sono in media giuste — chi vince ha sovrastimato. Il fenomeno fu descritto per la prima volta nel 1971 da tre ingegneri della Atlantic Richfield, che notarono come le compagnie petrolifere ottenessero rendimenti bassi «anno dopo anno» nelle prime aste per le concessioni al largo delle coste. **La fonte dice che la gravità cresce col numero di offerenti e non dà nessun numero; il conto si fa.** Con un valore vero di 100 e stime sbagliate al più di dieci in su o in giù, chi offre la propria stima paga di troppo, in media, **3,33 con due offerenti, 5,00 con tre, 6,00 con quattro, 7,14 con sei, 8,18 con dieci** (`build/check_284.py`, per l'attesa del massimo di *n* uniformi e per simulazione). Più gente c'è, più chi vince ha sbagliato.

Il rimedio ha un nome: `bid-shading.txt` chiama *bid shading* l'offrire meno di quanto si creda che la cosa valga. La riga più utile di `winners-curse.txt` è la spiegazione: **«vincere l'asta è una cattiva notizia sul valore della cosa»**, perché vuol dire essere stati i più ottimisti.

Su come si comportano le persone nelle aste vere, `auction.txt` riporta un dato senza grandezza: dall'analisi dei dati di eBay, gli offerenti esperti tendono a fare l'offerta all'ultimo istante, e chi lo fa vince più spesso. Direzione e non grandezza, ancora una volta.

## Esempi trovati

Dall'asta a candela: il guizzo dello stoppino un attimo prima di spegnersi, e l'uomo che gridava lì la sua offerta. **La regola era fatta per rendere imprevedibile la fine, e qualcuno trovò lo stesso il segnale.**

Da `dutch-auction.txt` e da `auction.txt`: l'asta olandese, dove il prezzo scende e il primo che parla prende. Serve dove ci sono migliaia di lotti da vendere in poche ore — i fiori — e trasforma una trattativa in un istante.

Da `game-mechanics.txt`: nel bridge non si offre denaro ma una promessa. Si dichiara quante prese si faranno, e chi le dichiara di più gioca; se poi non le fa, paga. **È l'unica asta in cui si offre una prestazione futura di sé stessi.**

Da `bidding-fee-auction.txt`: l'asta in cui ogni rilancio costa e chi perde ha pagato lo stesso. È la stessa struttura di un'asta normale con una riga cambiata, e la riga cambiata la rovescia.

Da `auction.txt`, sulla parte che nessuna regola risolve: il «giro», cioè offerenti che si accordano per non farsi concorrenza e poi si rivendono la cosa fra loro dopo, dividendosi la differenza. In Gran Bretagna è illegale. **È l'unica forma del capitolo il cui difetto principale è un accordo fra i partecipanti contro il procedimento.**

Da `winners-curse.txt`: un giacimento che vale davvero dieci milioni, stimato da chi fra cinque e venti; vince chi ha detto venti, e scopre dopo.

## Una nostra versione

> **La busta chiusa, e perché conviene scrivere il vero**
>
> Servono almeno due persone. Ognuno riceve **dodici gettoni** — fagioli, monete, quello che c'è — e questo foglio.
>
> Ci sono quattro lotti, e sono cose che succederanno davvero questa settimana.
>
> ```
>  lotto 1  chi sceglie che cosa si mangia sabato
>  lotto 2  chi sceglie il film, e nessuno protesta
>  lotto 3  un'ora in cui non ti si chiede niente
>  lotto 4  chi non sparecchia per tre giorni
> ```
>
> Per ogni lotto, ognuno scrive su un foglietto **quanti gettoni** e lo piega. Si aprono tutti insieme.
>
> **La regola, ed è tutta qui: prende il lotto chi ha scritto di piu', e paga quello che ha scritto il secondo.**
>
> Sembra strana. Ecco perche' e' fatta cosi'. Immagina che il lotto valga sette gettoni per te, e che l'altro scriva un numero qualunque fra zero e dieci. Questa tabella dice quanto ci guadagni in media a seconda di quello che scrivi tu. E' stata calcolata, non stimata.
>
> ```
>  se offro   guadagno in media
>         0                0.00
>         1                0.64
>         2                1.18
>         3                1.64
>         4                2.00
>         5                2.27
>         6                2.45
>         7                2.55
>         8                2.55
>         9                2.45
>        10                2.27
>        11                2.00
> ```
>
> Scrivere sette — cioe' il vero — e' il massimo. Scrivere di meno ti fa perdere lotti che volevi; scrivere di piu' ti fa vincere lotti che paghi troppo. **Non serve indovinare che cosa fara' l'altro**, e questo e' l'unico motivo per cui la regola esiste.
>
> Dopo le quattro buste, una domanda per ciascuno, da scrivere prima di guardare quello che ha scritto l'altro:
>
> ```
>  Con la regola normale, cioe' pagando quello che avevo scritto,
>  che numero avrei messo sul lotto ......?   ......
> ```
>
> Se il secondo numero è più basso del primo, è successa la cosa che si chiama **smussare l'offerta**: con quattro persone il conto dice di scrivere tre quarti di quello che vale davvero, con due la metà. Guarda di quanto l'hai abbassato tu.

La regola del secondo prezzo è la parte che fa il lavoro, e la tabella stampata è la sua dimostrazione ridotta a dodici righe: non è un incoraggiamento a essere onesti, è un conto che mostra che l'onestà non costa niente. Il sistema non deve arbitrare, non deve contare e non deve vietare: **la verifica sta dentro il materiale**, perché i foglietti si aprono insieme e i numeri si leggono. L'ultima domanda produce una misura del proprio smussamento, che è un numero personale senza risposta giusta, e la si chiede a mano fatta per la ragione già raccolta alla voce 274, scoperta: chiesta prima, la si cerca invece di incontrarla.

Dove si romperebbe: **con una persona sola non esiste**, e non c'è nessun ripiego onesto — un'asta con un offerente ha ricavo zero, e il conto lo dice. Il foglio non può nemmeno fare da secondo offerente, perché un'offerta stampata è nota prima e allora basta scrivere uno in più. E i gettoni sono una risorsa che il foglio registra ma non può far rispettare: è la stessa cosa della voce 270, risorse da spendere, e qui non morde soltanto perché i gettoni sono oggetti veri che si posano sul tavolo.

## Da riprendere alla rassegna

**L'asta è il modo di decidere che non chiede a nessuno di essere giusto,** e in una casa asimmetrica questa è la proprietà interessante. Sta accanto a taglia-e-scegli della voce 72, negoziare fra le procedure che non richiedono fiducia — con una differenza che vale la pena guardare: taglia-e-scegli funziona in due, l'asta funziona meglio via via che si è di più, e in una casa non si è mai di più.

**Il secondo prezzo è la sola regola incontrata in duecentottantaquattro voci che renda la sincerità la scelta migliore per interesse.** Non chiede lealtà, non fa appello a niente, e si dimostra con una tabella. Alla rassegna vale la pena chiedersi quali altre forme dell'elenco abbiano una versione con questa proprietà — la voce 244, autovalutazione con rubrica è la prima da guardare, perché è il posto in cui chi dichiara e chi ha lavorato coincidono.

**La seconda persona vale dodici volte l'ottava, ed è la seconda misura indipendente di questa forma.** La prima era sulle figurine, alla voce 276, cooperazione. Due strutture senza niente in comune danno la stessa curva. Per un progetto con una persona sola, la conseguenza è la stessa: quello che manca è quasi tutto nel passaggio da uno a due, e quasi niente dopo.

**La maledizione del vincitore peggiora con il numero di partecipanti,** ed è il primo caso del capitolo in cui aggiungere gente peggiora la qualità della decisione invece di migliorarla. Da accostare alla voce 250, scienza partecipata (citizen science) e al disimpegno della voce 276, cooperazione: tre modi diversi in cui un gruppo produce meno di quanto prometta.

**L'asta a candela è una fine imprevedibile ottenuta con una cosa fisica,** ed è la stessa mossa del cubetto di ghiaccio della voce 88, sfida contro un tempo. Il sistema non misura il tempo; una candela sì, e nessuno può metterla in pausa. Da censire con le altre misure fisiche del tempo.

**L'offerta come promessa di una prestazione futura** — il contratto del bridge — è una struttura che l'elenco non ha in nessuna voce, e non ha bisogno di denaro né di gettoni: si dichiara quanto si farà e mancare costa. Va guardata accanto alla voce 89, sfida contro sé stessi, dove l'obiettivo è dichiarato ma non c'è nessun costo per averlo dichiarato troppo alto.
