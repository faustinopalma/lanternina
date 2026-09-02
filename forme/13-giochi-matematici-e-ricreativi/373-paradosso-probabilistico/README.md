# Paradosso probabilistico

- **Numero** 373 nell'enciclopedia, capitolo 13 — Giochi matematici e ricreativi
- **Si chiama anche** paradosso veridico, illusione cognitiva, problema delle tre porte, problema dei compleanni, *Monty Hall problem*, *birthday problem*, *Simpson's paradox*, *veridical paradox*
- **In una riga** Monty Hall, il paradosso dei compleanni, il paradosso di Simpson.
- **Contratto** voce breve
- **Fonti** `monty-hall-problem.txt`, `it-monty-hall.txt`, `birthday-problem.txt`, `simpsons-paradox.txt`, `it-paradosso-di-simpson.txt`, `boy-or-girl-paradox.txt`, `bertrands-box-paradox.txt`, lette il 2 settembre 2026
- **Stato della ricerca** fatta, 2 settembre 2026

## Che cos'è

Una situazione in cui la risposta giusta è dimostrabile in tre righe e continua a sembrare sbagliata dopo che si è letta la dimostrazione. `birthday-problem.txt` la chiama **paradosso veridico**: sembra falsa a prima vista ed è vera. Non c'è nessun trucco nell'enunciato e nessuna informazione nascosta; quello che sbaglia è l'intuizione, e sbaglia in modo stabile e ripetibile.

Le parti mobili:

- **La quantità di casi da enumerare.** Quasi sempre pochissimi. Tre porte, novantadue casi, due bambini.
- **Che cosa fa scattare l'errore.** Trattare un'informazione ottenuta con una regola come se fosse casuale; guardare il totale invece delle parti; contare le persone invece delle coppie.
- **Se si può giocare.** Alcuni si possono ripetere venti volte con tre bicchieri; altri no.
- **Quanto è chiaro l'enunciato.** Questa parte non è un dettaglio ed è il difetto ricorrente della famiglia: molti di questi problemi hanno più di una risposta perché hanno più di una lettura.

**La differenza dalla voce 371, costruzione con riga e compasso:** là la prova sta nello strumento e il pericolo è l'errore invisibile. Qui la prova sta **nell'argomento**, come per i ponti della voce 366, problema di grafi — e succede una cosa che nel resto dell'enciclopedia non succede: **l'argomento è corretto, chiunque può controllarlo, e non convince.** La prova che convince è un'altra, ed è la ripetizione.

## Da dove viene

**Monty Hall nasce come lettera a una rivista di statistica e diventa famoso quindici anni dopo su un settimanale.** `monty-hall-problem.txt`: Steve Selvin lo pone in una lettera all'*American Statistician* nel **febbraio 1975**, e in una seconda lettera dell'agosto dello stesso anno gli dà il nome. È una variazione sul gioco vero: il vero Monty Hall apriva una porta con una capra per aumentare la tensione, ma non offriva il cambio — offriva denaro. La fama arriva con la rubrica *Ask Marilyn* di Marilyn vos Savant su *Parade*, che risponde a una lettera del lettore Craig Whitaker.

**La stessa cosa esisteva già da sedici anni con un altro nome.** `monty-hall-problem.txt` dichiara che il problema è matematicamente equivalente al **problema dei tre prigionieri**, che Martin Gardner presentò nella sua rubrica su *Scientific American* nel **1959**, e alle tre conchiglie di *Aha! Gotcha*. Più indietro ancora sta il **paradosso della scatola di Bertrand**, che Joseph Bertrand pose nel suo *Calcul des probabilités* del **1889** (`bertrands-box-paradox.txt`). La stessa struttura ha cambiato nome tre volte in un secolo.

**Il paradosso dei compleanni non ha un padre certo.** `birthday-problem.txt` lo attribuisce a Harold Davenport, intorno al **1927**, con l'avvertenza che Davenport non ne rivendicava la paternità «perché non poteva credere che non fosse stato enunciato prima». La prima pubblicazione di una sua versione è di **Richard von Mises**, **1939**.

**Il paradosso di Simpson ha due esempi canonici e sono tutti e due dati reali.** `simpsons-paradox.txt`: le ammissioni alla scuola di specializzazione di Berkeley nell'autunno del **1973**, dove gli uomini risultavano ammessi più spesso delle donne con uno scarto troppo grande per essere caso, e dove il conto per dipartimento mostrava che le donne si candidavano ai dipartimenti più selettivi; sui dati aggregati e corretti restava «un piccolo ma statisticamente significativo vantaggio a favore delle donne». Il secondo è uno studio clinico su due trattamenti dei calcoli renali, dove il trattamento A è migliore sui calcoli piccoli **e** sui calcoli grandi, e peggiore sul totale.

## Varianti e parenti

- **Monty Hall** — tre porte, il conduttore ne apre una che sa essere perdente, conviene cambiare.
- **I tre prigionieri, le tre conchiglie, la scatola di Bertrand** — la stessa struttura sotto altri nomi.
- **Compleanni** — bastano ventitré persone perché due condividano il giorno con probabilità superiore a un mezzo.
- **Simpson** — un andamento che si inverte quando si aggregano i gruppi.
- **Due bambini** — il caso in cui la domanda stessa è ambigua. Vedi sotto.
- **Due buste** — si apre una busta e ci si chiede se convenga scambiare; il conto ingenuo dice sempre sì, il che è assurdo.
- **Voce 152, problema impossibile** — l'altra forma in cui il compito è accorgersi che il proprio primo pensiero era sbagliato. Là l'errore è sulla possibilità, qui sul numero.
- **Voce 151, paradosso** — la forma generale, che l'elenco descrive come «una cosa che non torna e sulla quale non c'è niente da fare». Qui invece c'è: si conta.
- **Voce 359, problema di Fermi** — l'altra voce del capitolo in cui si maneggiano numeri che nessuno sa a mente.

## Che cosa se ne sa

**Il conto è di nove casi e la reazione fu di diecimila lettere.** `monty-hall-problem.txt`: dopo l'uscita della rubrica **circa 10 000 lettori scrissero alla rivista, quasi 1 000 dei quali con un dottorato**, e la maggioranza diceva che vos Savant aveva torto. La pagina aggiunge che molti non accettarono la risposta nemmeno dopo spiegazioni, simulazioni e dimostrazioni formali, e che **Paul Erdős** — che è uno dei matematici più prolifici della storia — restò non convinto finché non gli fu mostrata una simulazione al calcolatore. In uno studio su **228 soggetti**, solo il **13%** scelse di cambiare.

**Nove casi, e li conta anche un bambino.** `build/check_371.py` enumera le tre posizioni dell'auto per le tre scelte iniziali: nove casi equiprobabili, cambiando si vince in **sei**, restando in **tre**. Una simulazione su 60 000 partite dà 0,663 e 0,337. Le due strade concordano, e la seconda è quella che convinse Erdős.

**Lo spazio da provare è il più piccolo di tutta l'enciclopedia, e la difficoltà non c'entra niente con lui.** Due strategie: cambiare o restare. Nel blocco precedente la grandezza interessante era quanto spazio chiude una riga di ragionamento — dodici milioni di coperture alla voce 363, problema di parità, un numero con sei milioni di cifre alla voce 365, principio dei cassetti. **Qui lo spazio è due e la riga di ragionamento non basta lo stesso.** La grandezza che misurava la difficoltà smette di misurarla.

**Venti partite bastano quasi sempre, e si può dire quanto spesso.** `build/check_371.py`: giocando *n* partite e segnando ogni volta chi avrebbe vinto, la strategia giusta risulta la più frequente nel **78,7%** dei casi con dieci partite, nel **90,8%** con venti, nel **95,7%** con trenta e nel **98,9%** con cinquanta. Venti partite sono cinque minuti con tre bicchieri e una moneta. **È la misura che dice quanto costa mettere la prova nel materiale invece che nell'argomento**, e costa venti partite.

**I compleanni, per due strade.** La formula del complemento dà **0,5073** per ventitré persone; una simulazione su 40 000 stanze dà 0,5068. Ventitré è il primo numero che supera la metà, verificato scorrendo tutti i valori. La spiegazione che la pagina dà è aritmetica e sta in una riga: **le coppie non sono ventitré, sono 253.**

**Un paradosso di questa famiglia può non avere una risposta, e l'autore l'ha ammesso.** `boy-or-girl-paradox.txt`: Martin Gardner pose le due domande sui due figli nella rubrica del **maggio 1959** e diede le risposte 1/2 e 1/3; **più tardi riconobbe che la seconda domanda era ambigua** e che senza sapere come si è ottenuta l'informazione non è possibile rispondere. La risposta 1/3 richiede un'assunzione — che di un maschio si parli sempre, e di una femmina mai — che, dicono Marks e Smith citati nella pagina, non viene mai enunciata. **Qui l'enunciato è il problema**, e questo distingue la sotto-famiglia sana da quella malata.

**Le due pagine italiane prese portano tutte e due un avviso, e una sbaglia una data.** `it-paradosso-di-simpson.txt` è di 7 671 byte e ha in cima l'avviso di essere «priva o carente di note e riferimenti bibliografici puntuali»; la definizione che dà — una relazione fra due fenomeni che appare modificata quando si aggregano i gruppi — combacia con quella inglese, e gli esempi numerici stanno solo nella pagina inglese. L'altra è più interessante da guardare.

**Le due pagine su Monty Hall discordano su una data, ed è l'italiana a sbagliare.** `monty-hall-problem.txt` data la prima rubrica al **9 settembre 1990**, *Parade* p. 16, e la terza al **17 febbraio 1991**, p. 12. `it-monty-hall.txt` cita «Parade Magazine 12 (17 febbraio 1990)», riprendendola da una fonte secondaria: **giorno, mese e numero di pagina sono quelli della terza rubrica, l'anno è quello della prima.** Non è una contraddizione fra due ricostruzioni: è una citazione di seconda mano che ha unito due righe. Si tiene la data inglese, che rimanda all'archivio della rivista.

## Esempi trovati

Da *Parade*, settembre 1990: «Sei a un gioco a premi e ti danno da scegliere fra tre porte. Dietro una c'è un'automobile, dietro le altre due una capra». È il testo che ha generato le diecimila lettere.

Da Gardner, 1959: i tre prigionieri, uno dei quali sarà graziato, e il guardiano che rivela il nome di uno dei due che saranno giustiziati.

Da Bertrand, 1889: tre scatole, una con due monete d'oro, una con due d'argento, una mista; si estrae una moneta d'oro, che probabilità c'è che l'altra nella stessa scatola sia d'oro.

Da Berkeley, 1973: i sei dipartimenti più grandi, i cui numeri sono in `simpsons-paradox.txt`, dove il totale dice una cosa e ogni riga dice il contrario.

Dal baseball, nella stessa pagina: Derek Jeter ha una media più bassa di David Justice nel 1995 e nel 1996, e più alta sui due anni messi insieme. La pagina riporta che, secondo Ken Ross, il caso si verifica **circa una volta l'anno** fra le coppie di giocatori possibili.

## Una nostra versione

> **Tre bicchieri, venti partite**
>
> Serve un compagno e tre bicchieri capovolti. Sotto uno c'è una monetina: **la mette lui e tu non guardi.**
>
> Tu indichi un bicchiere, senza alzarlo. Lui — che sa dov'è la monetina — alza **uno degli altri due, e alza sempre uno vuoto.** Poi ti chiede se vuoi cambiare.
>
> Non decidere adesso. Gioca venti partite e ogni volta, alla fine, segna cosa sarebbe successo:
>
> ```
>  C se cambiando vincevi, T se tenendo.
>
>  __ __ __ __ __ __ __ __ __ __
>  __ __ __ __ __ __ __ __ __ __
>
>  quante C? ____      quante T? ____
> ```
>
> Adesso guarda le due caselle in fondo e dimmi tu che cosa conviene fare.
>
> Se ti dice che è uguale, ha ragione a pensarlo e ha torto sui numeri, e sono in buona compagnia: quando questo problema uscì su un settimanale americano nel 1990, diecimila lettori scrissero che la risposta era sbagliata, e mille di loro avevano un dottorato.

Le venti partite sono la parte importante e non un contorno: l'argomento dei nove casi sta in tre righe e non convince, e le venti caselle sì. La probabilità che venti partite mostrino la risposta giusta è il 90,8%, calcolata in `build/check_371.py`; è alta e non è uno, e questo va detto invece che nascosto — se le due colonne vengono pari, la cosa da fare è giocarne altre venti. **Chi propone deve alzare sempre un bicchiere vuoto**, e questa è la sola regola che, se salta, cambia la risposta.

## Da riprendere alla rassegna

**Sulla scala del blocco prende un valore che il censimento non aveva: la prova sta nell'argomento, e l'argomento non basta.** Alla voce 363, problema di parità e alla voce 364, invariante l'argomento chiudeva la questione. Qui l'argomento è dello stesso genere — nove casi, si contano — e diecimila persone lo rifiutano. **Il posto della prova e il posto della persuasione non coincidono**, e questa è la prima voce in cui si separano.

**La ripetizione è il posto della persuasione, e ha un prezzo misurato.** Venti partite: 90,8%. Cinquanta: 98,9%. Alla rassegna questo dà una regola pratica per tutte le forme in cui la risposta è controintuitiva — **non si stampa la dimostrazione, si stampa la griglia da riempire** — e dice quanto lunga deve essere la griglia. Con la voce 359, problema di Fermi, dove si chiedono due stime indipendenti invece di una, fa due mosse che spostano la verifica dentro il materiale senza cambiare il contenuto.

**Il vincolo di `ideas/10 §8` non morde, e per una ragione che vale la pena isolare.** Non si chiede a nessuno di calcolare una probabilità: si chiede di segnare venti caselle e di contarle. La risposta che il foglio non conosce — quante volte è uscita C — non deve tornare indietro come testo da leggere, perché a leggerla è chi ha giocato. **È il caso più netto raccolto di forma che aggira il vincolo spostando il lettore invece del contenuto.**

**La famiglia si divide in due, e la divisione va tenuta.** Da una parte i paradossi con un enunciato che regge — Monty Hall con la regola del conduttore dichiarata, i compleanni, Simpson —; dall'altra quelli in cui la risposta dipende da come si è saputa la cosa, e il caso dei due bambini è il capofila, con l'autore che lo ammette dopo. **Alla rassegna, i secondi non sono una versione più difficile dei primi: sono un genere diverso**, e chiedono a chi legge di indovinare l'intenzione di chi scrive invece di ragionare su un fatto.

**Il paradosso di Simpson è quello che serve fuori dal pomeriggio, e non è giocabile.** Non ci sono venti partite da fare: ci sono due tabelle da leggere. Alla rassegna è il candidato più forte del capitolo per una forma che porta via qualcosa di utile — leggere una percentuale aggregata è una cosa che si fa tutta la vita — ed è anche quello che sta peggio nel formato, perché richiede di guardare dati veri che non stanno su una scheda.

