# Display

- **Numero** 74 nell'enciclopedia, capitolo 3 — Su che cosa arriva la domanda
- **Si chiama anche** schermo, e-paper, carta elettronica, pannello, cornice, insegna, oggetto da guardare di sfuggita, glanceable display, ambient device
- **In una riga** quattro righe corte, e sparisce quando arriva il prossimo.
- **Fonti** `electronic-paper.txt`, `calm-technology.txt`, `ambient-device.txt`, prese il 30 agosto 2026; `docs/HARDWARE.md` per il dispositivo che usiamo
- **Stato della ricerca** fatta, 30 agosto 2026

## Che cos'è

Una superficie appesa che tiene un'immagine e la cambia quando qualcuno decide di cambiarla. Ha due proprietà che il foglio non ha — può aggiornarsi da sola, e non si può portare via — e ne perde due che il foglio ha: non ci si scrive sopra, e non resta.

Parti mobili:

- **Quanto ci sta.** Un contatore a una cifra, una riga, quattro righe, una pagina intera. La capienza cambia la forma della cosa più della tecnologia.
- **Ogni quanto cambia.** Un aggiornamento all'ora e uno al secondo sono due oggetti diversi: il primo si guarda di sfuggita, il secondo si fissa.
- **Se conserva l'immagine senza corrente.** La carta elettronica sì, uno schermo retroilluminato no. Da questo dipende se il supporto è un oggetto della stanza o un apparecchio acceso.
- **Se emette luce.** Uno schermo che illumina si impone di notte; uno che riflette la luce ambientale scompare al buio, come un foglio.
- **Dove sta.** Al centro dell'attenzione o alla periferia. È la variabile su cui è costruita tutta la letteratura della *calm technology*.
- **Se sa di essere stato letto.** Quasi nessun display lo sa, e questo lo rende meno intelligente di quello che sembra.

Togliendo l'aggiornamento resta un cartello. Togliendo la permanenza dell'immagine resta un apparecchio che va tenuto acceso.

## Da dove viene

La carta elettronica nasce negli anni Settanta a Xerox PARC: **Nick Sheridon** costruisce il *Gyricon*, sferette di polietilene fra i 75 e i 106 micrometri, nere da una parte e bianche dall'altra, sospese nell'olio dentro un foglio di silicone trasparente e girate da un campo elettrico (`electronic-paper.txt`, 30 agosto 2026). Il vantaggio dichiarato già allora è quello che conta ancora adesso: **l'immagine resta anche quando la tensione se ne va**.

Negli anni Novanta un gruppo di studenti del MIT prototipa l'inchiostro elettronico a microcapsule e ne pubblica la descrizione su *Nature*; **E Ink** viene fondata nel 1997 da J. D. Albert, Barrett Comiskey, Joseph Jacobson, Jeremy Rubin e Russ Wilcox per commercializzarla (`electronic-paper.txt`). Le microcapsule — circa 40 micrometri di diametro nelle prime versioni — permettono di fabbricare il pannello per stampa su plastica invece che su vetro, e da lì arrivano i lettori di libri.

La stessa fonte elenca gli usi che non c'entrano con la lettura: etichette di scaffale, insegne, orari alle fermate degli autobus, cartelloni. È un elenco di superfici che stanno appese e che si guardano un secondo.

Il filone teorico è più vecchio del pannello. **Mark Weiser e John Seely Brown** pubblicano *Designing Calm Technology* nel 1995, sempre a Xerox PARC, e definiscono calma «quella tecnologia che informa senza pretendere la nostra attenzione» (`calm-technology.txt`, 30 agosto 2026). L'esempio che Weiser usa è la *Dangling String*: uno spago di due metri e mezzo appeso al soffitto e collegato a un motorino, a sua volta collegato a un cavo Ethernet; ogni pacchetto che passa fa scattare il motore, e la quantità di traffico si legge da quanto lo spago frulla. Nel 2015 Amber Case ne ricava un insieme di principi in *Calm Technology: Principles and Patterns for Non-Intrusive Design*.

Il filone commerciale è l'*ambient device*: oggetti che si leggono con un'occhiata, «glanceable», e che mappano un dato su una scala di una sola dimensione — un colore, un angolo (`ambient-device.txt`, 30 agosto 2026). Il *New York Times Magazine* nomina gli ambient device fra le idee dell'anno nel 2002; il primo prodotto è l'**Ambient Orb**, una sfera di vetro smerigliato che diventa verde o rossa a seconda di come si muove un indice di borsa, e ambra quando l'indice non si muove. Il seguito, il Chumby del 2008, aggiunge il tocco e la connessione, e cessa la produzione nell'aprile 2012.

## Varianti e parenti

- **Il contatore** — una cifra sola, che vuol dire quanto manca o quanti ne restano.
- **La riga singola** — un'insegna, un titolo, una frase.
- **La cornice** — un'immagine che cambia una volta al giorno.
- **Il dispositivo periferico** — non si legge, si nota: colore, posizione, movimento.
- **Lo schermo che si tocca** — cambia natura, perché diventa anche il posto dove si risponde.
- **L'orario alla fermata** — il caso in cui il display esiste solo per dire quanto manca.
- **L'avviso appeso su carta** — voce 73, foglio stampato: la stessa funzione senza aggiornamento.
- **La stanza come supporto** — voce 78, ambiente: quando quello che cambia non è un pannello ma la disposizione delle cose.
- **Il tempo come supporto** — voce 80, tempo: il display è il modo più economico di far esistere il ritorno.

## Che cosa se ne sa

Le tre fonti prese il 30 agosto 2026 non riportano misure di apprendimento né di attenzione: descrivono tecnologie e principi di progetto. Le misure che citano sono fisiche — dimensioni delle particelle, consumo — non psicologiche.

Il fatto tecnico che conta di più: **la carta elettronica ha bistabilità intrinseca**, cioè tiene l'immagine senza alimentazione (`electronic-paper.txt`). Da qui discende tutto il resto. Un pannello che consuma solo quando cambia può stare appeso a batteria per settimane, e sta nella stanza come un quadro invece che come un apparecchio.

Il secondo: **riflette la luce dell'ambiente invece di emetterne**. La fonte lo presenta come un vantaggio di comodità e di angolo di visione, e nota che un display e-paper ideale si legge in pieno sole senza sbiadire. Il rovescio, che la fonte non dice e che è banale, è che **al buio non si legge**: di notte quel pannello è un rettangolo grigio.

Il terzo, dal nostro dispositivo e non dalle fonti generali: il pannello è da 7,5 pollici, quattro livelli di grigio, e riceve dal server un PNG a uno o due bit (`docs/HARDWARE.md`, verificato il 3 agosto 2026). **Il dispositivo chiede al server, mai il contrario**, e nella risposta il server dice quando richiamare. Quindi la latenza è un parametro, non una costante — quindici minuti quando non succede niente, un minuto quando c'è qualcosa in sospeso — e il dispositivo dorme in mezzo.

La conseguenza pratica che nessuna delle fonti tratta ma che l'enciclopedia ha già incontrato: **un display da quattro righe non è un foglio più piccolo.** Per una forma che si legge per contrasto — un modulo con dei buchi, una griglia con una casella vuota — serve vedere la struttura intera, e su quattro righe non si vede mai (voce 63, inferire da un'assenza). La differenza fra i due supporti non è di quantità.

E: **il display può sostituire quello che mostra, il foglio no.** Questo lo rende l'unico supporto che il sistema ha in grado di dire *è finita*, *tocca a te*, *manca poco*. Quale peso abbia una frase che sparisce rispetto a una che resta non è stato misurato, e **va verificato**.

## Esempi trovati

Dalla *Dangling String* di Weiser: il traffico di rete letto da quanto frulla uno spago appeso al soffitto. Nessun numero, nessuna parola, e si capisce dalla porta (`calm-technology.txt`).

Dall'Ambient Orb del 2002: una sfera che diventa verde o rossa secondo un indice di borsa, e ambra quando l'indice sta fermo. Venduta come oggetto d'arredamento con una funzione in più (`ambient-device.txt`).

Dalle etichette di scaffale e dagli orari alle fermate: carta elettronica usata dove un cartello andrebbe cambiato a mano ogni giorno (`electronic-paper.txt`).

Da Soken, alla fiera FPD del 2008: una parete intera di carta da parati elettronica basata sul Gyricon (`electronic-paper.txt`).

## Una nostra versione

> Il display porta questo, e resta finché non arriva qualcosa d'altro:
>
> ```
> ┌────────────────────────────────────────────┐
> │ Sul tavolo ci sono nove cose.              │
> │ Una non c'era stamattina.                  │
> │                                            │
> │ Quando l'hai trovata, gira il foglio.      │
> └────────────────────────────────────────────┘
> ```
>
> E poi, quando il foglio è stato girato:
>
> ```
> ┌────────────────────────────────────────────┐
> │ Era quella?                                │
> │                                            │
> │ Il foglio dice come si fa a esserne sicuri.│
> │                                            │
> └────────────────────────────────────────────┘
> ```

Il display qui non porta il contenuto: porta lo stato. Quattro righe non bastano per dire che cosa fare, e non ci provano — dicono soltanto a che punto siamo, e mandano al foglio. Il fatto che il primo messaggio scompaia quando arriva il secondo è la parte che il foglio non sa fare: non c'è modo di guardare la vecchia consegna e quella nuova insieme, e questo chiude il primo tempo senza doverlo dichiarare.

Il limite dove si romperebbe: se le due righe fossero il compito intero — un elenco da ordinare, una griglia da riempire — non ci starebbero, e non sarebbe una questione di scrivere più corto.

## Da riprendere alla rassegna

**Il display è l'unico posto in cui il sistema può dire che qualcosa è cambiato.** Il foglio non ha stato, la fotografia arriva dopo. Se una forma ha bisogno di un adesso, deve passare da qui.

**Quattro righe che scompaiono sono un'unità narrativa, non un ritaglio del foglio.** Le voci scritte finora hanno quasi sempre trattato il display come la versione ridotta di una consegna. Le due prove che questo non funziona — la voce 63, inferire da un'assenza e l'esempio qui sopra — suggeriscono che valga il contrario: il display porta lo stato e il foglio porta il compito.

**Un pannello e-paper al buio non si legge.** È una proprietà fisica, non una scelta. Ogni forma che si regge sull'idea che il display sia sempre consultabile va guardata due volte.

**Il dispositivo dorme e non sa se qualcuno ha guardato.** L'unica cosa che il sistema sa è quando il pannello ha chiesto l'immagine successiva. Quante forme dell'elenco assumono che il display sia stato letto è da contare.

**La famiglia degli oggetti che si guardano di sfuggita è più larga del pannello.** Lo spago di Weiser, la sfera dell'Ambient Orb: un dato mappato su una dimensione sola, senza parole. Non c'è nessuna voce dell'elenco che descriva questa forma, e sembra mancarci.
