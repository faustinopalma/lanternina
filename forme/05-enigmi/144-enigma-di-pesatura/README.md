# Enigma di pesatura

- **Numero** 144 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi logici»
- **Si chiama anche** problema della moneta falsa, problema delle dodici monete, enigma della bilancia, *balance puzzle*, *weighing puzzle*, *counterfeit coin problem*, *oddball*
- **In una riga** trovare la moneta falsa in tre pesate.
- **Fonti** `balance-puzzle.txt`, presa il 30 agosto 2026 da en.wikipedia
- **Stato della ricerca** fatta, 30 agosto 2026

## Che cos'è

Ci sono delle monete tutte uguali tranne una, che pesa diverso. C'è una bilancia a due piatti, e la si può usare un numero fissato di volte. Bisogna trovare quale.

È un enigma di stato come la voce 143, enigma di attraversamento, ma quello che si conserva è un'altra cosa. Lì contava chi stava su quale sponda; **qui conta quanta informazione si è raccolta**, e il conto si fa in anticipo, prima di toccare qualsiasi moneta.

Il fatto su cui gira tutto è che **una bilancia a due piatti ha tre esiti**, non due: pende a sinistra, pende a destra, sta in pari. Da qui segue tutto il resto, e da qui segue anche perché il problema si generalizza in modo così netto.

Parti mobili:

- **Quante pesate.** Il numero che decide quante monete si possono trattare.
- **Se si sa in che verso è falsa.** Sapere che la moneta cattiva è più leggera dimezza il problema: con *n* pesate se ne trattano 3ⁿ. Non saperlo lo rende un problema diverso, e i numeri crollano.
- **Se bisogna anche dire se è più pesante o più leggera**, o se basta indicarla. Sono due problemi con due risposte diverse, e la differenza è di una moneta.
- **Se c'è una moneta buona di riferimento.** Averne una certa aggiunge una moneta sospetta al massimo trattabile.
- **Se le pesate sono decise in anticipo o dipendono dall'esito.** Questa è la parte mobile più interessante e la meno ovvia: esistono soluzioni **non adattive**, in cui tutte e tre le pesate sono scritte prima di cominciare.

## Da dove viene

Il problema delle dodici monete, nella forma completa — non si sa se la falsa è più pesante o più leggera, tre pesate, e bisogna anche dire in che verso —, **compare per la prima volta in un articolo del 1945**, e la fonte non dice altro sull'autore.

Il caso più semplice, nove monete e due pesate con la falsa più leggera, è più vecchio e non ha una data: è uno di quei problemi che circolano senza padre.

Il resto è generalizzazione matematica novecentesca: la variante a tredici monete, quella a trentanove monete in quattro pesate, la formulazione con più bilance, quella con più monete false. La pagina le raccoglie tutte con le loro formule e non racconta nessuna storia. **È l'unica voce di questo blocco che non ha un aneddoto**, ed è coerente con quello che è: un problema di conteggio travestito da monete.

## Varianti e parenti

- **Nove monete, due pesate, falsa più leggera** — la versione da cui si comincia.
- **Dodici monete, tre pesate, verso ignoto** — la versione classica, e quella del 1945.
- **Tredici monete, tre pesate** — si trova quale, ma **non sempre si riesce a dire se è più pesante o più leggera.** È il caso limite, e la differenza fra tredici e dodici è esattamente quella riga.
- **Con una moneta di riferimento** — se si ha una moneta certamente buona, le sospette possono essere tredici e si riesce a dire tutto.
- **Più monete false** — la procedura standard si rompe, e in un modo che vale la pena raccontare: se due monete sono false, **la procedura in genere non ne indica nessuna delle due, ma indica una moneta autentica.** Non dà un errore, dà una risposta sbagliata.
- **Voce 143, enigma di attraversamento** — l'altro enigma di stato di questo blocco. Lì la risorsa scarsa è la barca, qui è il numero di pesate.
- **Voce 145, enigma di travaso** — la terza: lì la risorsa scarsa sono le due capacità dei recipienti.
- **Voce 59, escludere** — il verbo. Ogni pesata divide l'insieme in tre parti e ne butta via due.
- **Voce 54, misurare** — il parente materiale, e la differenza è netta: qui non si misura niente, si confronta. Non serve nessun numero e nessuna unità.
- **Voce 372, aritmetica in altra base** — nel capitolo 13. La soluzione non adattiva delle dodici monete è scritta in base tre, e il legame è letterale, non analogico.
- **Voce 365, principio dei cassetti** — sempre nel capitolo 13. Lo stesso tipo di ragionamento: si conta prima e si conclude senza guardare.

## Che cosa se ne sa

**Il conto è tutto, e sta in una riga: con *n* pesate ci sono 3ⁿ esiti possibili, e ogni caso da distinguere deve avere il suo.** Da qui la fonte ricava i numeri esatti. Con *n* pesate si può individuare la moneta diversa fra al massimo **(3ⁿ − 1) / 2** monete, cioè tredici con tre pesate. Ma per riuscire sempre anche a dire **se è più pesante o più leggera** il massimo scende a **(3ⁿ − 3) / 2**, cioè dodici. La differenza fra le due formule è una moneta, e quella moneta è quella che non si mette mai sulla bilancia: se tutte le pesate stanno in pari, è lei — ma nessuno l'ha mai vista muovere un piatto, quindi non si sa da che parte.

**La costruzione della soluzione a nove monete è la cosa che si può insegnare in tre righe.** Si parte da una domanda più piccola: **qual è il massimo numero di monete fra cui una sola pesata trova la più leggera?** La risposta è tre — si confrontano due monete e si lascia fuori la terza; se le due pesano uguale è la terza. Da lì: nove monete in tre pile da tre, una pesata dice quale pila, una seconda dice quale moneta. E per estensione, tre pesate bastano per ventisette monete e quattro per ottantuno. **Questa è la struttura da dare, e non la soluzione.**

**Esiste una soluzione in cui le tre pesate sono decise prima di cominciare, e questa è la cosa più elegante della pagina.** Si numerano le monete con tre cifre in base tre; il piatto di sinistra è etichettato 0, il piatto di destra 2, e «fuori dalla bilancia» è 1. Alla pesata *n*-esima si mette ogni moneta nel posto indicato dalla sua *n*-esima cifra. **Le tre pesate non dipendono da niente**, e alla fine i tre esiti letti insieme formano il numero della moneta. È il contrario esatto della procedura passo passo, in cui la seconda pesata dipende da come è andata la prima.

**Il fallimento con due monete false è documentato, e va guardato.** «Se due monete sono false, questa procedura in generale non ne sceglie nessuna delle due, ma piuttosto una moneta autentica.» La fonte fa anche l'esempio: se sono false la 1 e la 2, viene indicata a torto la 4 o la 5. **Una procedura che dà una risposta sbagliata anziché segnalare che le ipotesi non valgono** è la stessa cosa già osservata alla voce 128, crucipuzzle (word search) con le griglie che non contengono nessuna parola, e vale per qualunque cosa questo sistema stampi che presupponga qualcosa sul mondo.

**La versione rilassata ha una nota che chiarisce dove sta il costo.** Se basta trovare la moneta falsa senza dire quanto pesa, qualunque soluzione che a un certo punto pesava tutte le monete si può adattare per gestirne una in più — quella moneta non finisce mai sulla bilancia, e se tutte le pesate sono in pari è lei. **E non si può fare di meglio**, perché a una moneta che è stata sulla bilancia si può sempre assegnare un verso.

**Nessuna delle fonti dice niente su chi risolve.** Non c'è nessun dato su quanto sia difficile, per chi, a che età. La pagina è tutta matematica.

## Esempi trovati

Dalla versione a nove monete: tre pile da tre, e due pesate. È il caso che si racconta per primo perché la struttura si vede.

Dalla versione a dodici, 1945: quattro monete per piatto alla prima pesata, e poi una seconda pesata che sposta tre monete dal piatto leggero a quello pesante, toglie tre dal pesante e mette tre monete mai pesate su quello leggero. È una mossa che nessuno inventa a caso, e chi la vede la prima volta non capisce perché funzioni.

Dalla variante con moneta di riferimento: tre pesate scritte per esteso, con la moneta buona numerata 0 e le sospette da 1 a 13, e la nota che **si possono fare in qualunque ordine** — perché non dipendono l'una dall'altra.

Dalla lettura degli esiti: se la bilancia si sbilancia una volta sola, è una delle monete che compaiono in una pesata sola. Se non sta mai in pari, è una di quelle che compaiono in tutte e tre.

## Una nostra versione

Il sistema stampa il problema, la griglia e il conto; la bilancia e le monete stanno in casa, e la verifica è fisica. Non c'è nessun limite tecnico da aggirare, e non serve che nessuno sappia la risposta.

> **Tre risposte per volta**
>
> Prima ti serve una bilancia, e te la fai. Un righello di legno appoggiato di traverso su una matita, e due tappi di bottiglia uguali fissati alle due estremità con un pezzo di nastro. Quando è vuota deve stare in pari: se pende sempre dalla stessa parte, sposta la matita finché non smette.
>
> Poi ti servono nove monete uguali. Chiedi a qualcuno in casa di **appiccicare un pezzetto di pongo sotto una sola di esse e di non dirti quale.** Quella pesa di più.
>
> **Prima di cominciare, scrivi qui la tua previsione:**
>
> ```
>  con DUE pesate, quante monete al massimo
>  penso di poter smascherare?             ──────
>
>  perché                                  ─────────────────────
> ```
>
> Adesso trovala. Hai **due pesate**, non tre.
>
> ```
>  pesata 1:  a sinistra ───────  a destra ───────  esito ───────
>  pesata 2:  a sinistra ───────  a destra ───────  esito ───────
>
>  la moneta pesante è la  ───────
> ```
>
> Per controllare, mettila su un piatto e una qualunque delle altre sull'altro.
>
> ---
>
> Se ci sei riuscito, il motivo è questo: **una bilancia non risponde sì o no. Risponde in tre modi** — pende di qua, pende di là, sta in pari. Con due pesate le combinazioni di esiti sono tre per tre, cioè nove, e le monete erano nove.
>
> ```
>  allora con TRE pesate quante monete?    ──────
>
>  e con QUATTRO?                          ──────
> ```
>
> Ultima domanda, e non ha una risposta breve. **E se non ti dicessero che la moneta falsa è più pesante — se potesse essere anche più leggera?** Il numero che hai scritto qui sopra scende. Di quanto, e perché?
>
> ```
>  ────────────────────────────────────────────────────────────
> ```

La previsione scritta prima è la struttura raccolta cinque volte nel capitolo dei verbi, e qui è indispensabile: senza, il conto delle tre risposte per pesata arriva come una spiegazione invece che come una scoperta. Il numero previsto e il numero trovato si confrontano sulla stessa pagina.

Il pezzetto di pongo messo da qualcun altro è la seconda persona ridotta al minimo: non deve sapere niente, non deve giudicare niente, e non deve nemmeno restare in giro. **La verifica non passa da lei** — si controlla rimettendo la moneta sulla bilancia contro una qualunque.

Due limiti da dichiarare sul foglio e non dopo. Il primo: **una bilancia fatta con un righello non è sensibile come quella dell'enunciato**, e se il pongo è troppo poco non si vede niente. Il problema matematico assume una bilancia perfetta; l'oggetto no, e la differenza fra i due è essa stessa una cosa da guardare. Il secondo: la costruzione della bilancia è metà del pomeriggio, ed è la voce 44, costruzione più che questa.

Sul display da quattro righe l'enunciato ci sta per intero — «nove monete, una pesa di più, due pesate» sono meno di quaranta caratteri. Ma non ci sta il posto dove scrivere, e questa forma senza il posto dove tenere il conto degli esiti si affronta a memoria e si perde.

## Da riprendere alla rassegna

**Un esito a tre valori invece che a due, e cambia tutto.** Quasi ogni cosa che questa enciclopedia consegna produce una risposta binaria: giusto o sbagliato, sì o no, riuscito o no. La bilancia ne dà tre, e i tre non sono «sì, no, forse»: sono tre risultati alla pari. **È il primo strumento incontrato con questa proprietà**, e vale la pena chiedersi quali altri esistano — un confronto fra due cose che possa dire «uguali» è già un terzo esito, e la voce 9, confronto a coppie non lo prevede.

**Il conteggio prima della prova.** La struttura di questa forma non è «prova finché non trovi», è «conta quanti casi devi distinguere e quanti te ne dà lo strumento, poi progetta». Il conto si fa senza toccare niente, e dice in anticipo se la cosa è possibile. **È il gemello del problema impossibile della voce 152, problema impossibile**, visto dal lato in cui la risposta è sì.

**Una procedura che risponde male invece di dire che non sa.** Con due monete false l'algoritmo indica una moneta autentica, e nessuno se ne accorge. È la terza occorrenza di questo tipo di guasto silenzioso — le altre sono il crucipuzzle senza parole della voce 128, crucipuzzle (word search) e il conto sbagliato dell'enumerazione della voce 113, indovinello per enumerazione. **Alla rassegna vanno elencate insieme tutte le forme che possono fallire in silenzio**, perché in un sistema che stampa senza sapere se il foglio è stato usato sono quelle che fanno il danno maggiore.

**Le pesate decise prima e le pesate decise dopo sono due compiti diversi.** La soluzione non adattiva in base tre è più difficile da inventare e più facile da eseguire: si scrive tutto prima, poi si eseguono tre pesate senza pensare, poi si legge il risultato. Quella adattiva è il contrario. **Questa distinzione — decidere tutto prima o decidere strada facendo — attraversa molte forme dell'elenco** e non è ancora stata nominata da nessuna parte.

Da verificare: l'articolo del 1945 in cui il problema delle dodici monete compare per la prima volta. La fonte lo cita in nota e non lo nomina nel testo, e non l'ho cercato.
