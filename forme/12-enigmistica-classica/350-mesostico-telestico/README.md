# Mesostico, telestico

- **Numero** 350 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Rebus e forme miste»
- **Si chiama anche** mesostico, telestico, mesostic, telestich, acrostico finale, doppio acrostico, diastico
- **In una riga** la stessa cosa con le lettere centrali o finali.
- **Contratto** voce breve
- **Fonti** `it-mesostico.txt`, `it-telestico.txt`, `mesostic.txt`, `it-gioco-enigmistico.txt`, prese il 1 settembre 2026. `it-mesostico.txt` dichiara di essere un abbozzo, ed è di 1 455 byte: la definizione e i rimandi, e nient'altro
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Due varianti dell'acrostico della voce 349, acrostico, che cambiano una cosa sola: quale lettera di ogni riga si legge in verticale.

Il **telestico** prende l'ultima. `it-telestico.txt`, presa il 1 settembre 2026: «con procedura inversa rispetto all'acrostico, le lettere o le sillabe o le parole finali di ciascun verso formano un nome o una frase». Il **mesostico** prende una lettera in mezzo. `it-mesostico.txt`, presa lo stesso giorno: «sono le lettere o le sillabe o le parole **centrali** di ciascun verso, e non quelle iniziali, che formano un nome o una frase».

**Fra i due c'è una differenza che le due definizioni non nominano, ed è la sola cosa importante di questa voce.** L'inizio di una riga e la fine di una riga sono posizioni che esistono senza che nessuno le dichiari: sono i due bordi. Il mezzo no. «Centrale» non è una posizione: è un'intera fascia, e per ogni riga bisogna sapere quale carattere sia quello buono. Il telestico è l'acrostico rovesciato; il mesostico è un'altra cosa che gli somiglia.

Parti mobili:

- **Quale bordo, o nessuno dei due.**
- **Come si dichiara la colonna del mesostico.** Con le maiuscole, con un rientro, con una colonna tipografica vera, o con una regola formale.
- **Se si fanno insieme.** `it-telestico.txt` scrive che il telestico «viene spesso associato» all'acrostico, e nei casi più complessi anche al mesostico.

## Da dove viene

Il telestico è antico quanto l'acrostico e meno praticato: la fonte lo dice in una riga — «tecnica compositiva meno diffusa dell'acrostico» — e non dà una data. L'esempio più vecchio che riporta è un'iscrizione latina in esametri del quarto secolo, dal Nordafrica, nota come *Praedium Sammacis*, che è acrostica e telestica insieme. Il caso più spinto è di Teofilo Folengo, cinque esametri che sono contemporaneamente acrostici, mesostici e telestici, riportati da Giampaolo Dossena nel *Dizionario dei giochi con le parole*, 1994.

Il mesostico ha invece un secondo padre e un secolo di distanza. `mesostic.txt`, presa il 1 settembre 2026, attribuisce a **Jackson Mac Low** la pratica di usare parole-indice per selezionare pezzi di un testo preesistente — la chiamava *diastics* — e dice che il compositore **John Cage** la usò estesamente. E riporta due tarature della regola, dovute ad Andrew Culver, assistente di Cage: in un mesostico **al cinquanta per cento**, fra due lettere maiuscole non ci può essere la seconda delle due; in uno **al cento per cento**, non ci può essere né l'una né l'altra.

**Le due tradizioni fanno con la stessa struttura due cose opposte.** L'enigmistica italiana la usa per nascondere un nome dentro un componimento che qualcuno dovrà trovare; Mac Low e Cage la usano per **estrarre** un testo nuovo da uno vecchio, e il risultato non è un enigma ma una composizione. Nessuna delle due fonti sa dell'altra.

## Varianti e parenti

- **Acrostico** (voce 349, acrostico) — il termine di paragone di questa metà del blocco: la lettera sta all'inizio, e a dichiararlo è la forma stessa.
- **Acrostico** (voce 122, acrostico) — la forma letteraria e la sua storia, dove il telestico è già nominato come variante.
- **Doppio acrostico** — acrostico e telestico nello stesso testo, come nel *Praedium Sammacis*.
- **Quadrato del Sator** — il caso in cui i procedimenti si sommano fino a leggersi in tutte le direzioni; `it-telestico.txt` lo cita esattamente per questo.
- **Rebus** (voce 346, rebus) — l'altro punto del blocco in cui la disposizione grafica porta informazione che non è scritta: là due vocali, qui la colonna.
- **Steganografia** (voce 135, steganografia) — la famiglia dei messaggi nascosti dentro altri.
- **Vincolare** (voce 69, vincolare) — la famiglia a cui il mesostico appartiene quando serve a scrivere invece che a nascondere, cioè nell'uso di Cage.

## Che cosa se ne sa

**Il mesostico è lo spazio di ricerca più grande di tutta la sezione, e non lo si sarebbe detto.** Contato in `build/check_346.py` sul mesostico che `mesostic.txt` riporta per esteso: se le maiuscole non ci fossero, le sue sette righe — contate in lettere, che sono le sole a poter portare il verticale — offrirebbero **4 665 600** letture, contro le 2 097 152 spartizioni del rebus della voce 346, rebus. Il conto è stato fatto per due strade, il prodotto delle lunghezze e l'enumerazione vera delle scelte sulle prime quattro righe, dove i casi sono ancora contabili. Le maiuscole lo riducono a **una**.

**Quindi il mesostico fa con la tipografia quello che il rebus fa con il diagramma.** È la stessa mossa: dichiarare accanto alla domanda una grandezza che la risposta deve avere, e che non rivela la risposta. La differenza è che il diagramma è un numero e la colonna è un modo di stampare — e il progetto stampa, quindi la leva c'è.

**La regola di Culver è l'unica regola di questa sezione che una macchina possa controllare da sola.** Verificata in `build/check_346.py` sul mesostico *KITCHEN*: fra ogni coppia di maiuscole consecutive non compare nessuna delle due lettere, quindi è al cento per cento; e la regola al cento per cento implica quella al cinquanta, mentre il contrario non vale. Sono due tarature della stessa condizione, non due giochi. È un controllo sulla **presenza di una stringa**, cioè della stessa specie della *macrologia* che la voce 337, indovinello in versi aveva isolato come l'unico dei sette difetti dell'indovinello verificabile a macchina.

**E qui il controllo automatico non serve a giudicare chi risponde: serve a giudicare chi chiede.** Un mesostico che non rispetta la regola non è irrisolvibile, è ambiguo — chi legge trova la lettera sbagliata prima di quella giusta. La regola esiste per fare in modo che, scorrendo la riga, la prima occorrenza utile sia quella dell'autore. Detto in un altro modo: **Culver ha scritto la condizione che rende la colonna trovabile senza le maiuscole**, ed è il motivo per cui i mesostici di Cage si possono stampare senza segni e restano leggibili.

**Le due lingue classificano diversamente, e la freccia lo dice.** Controllato il 1 settembre 2026 con `build/check_titoli_346.py`: in inglese `Telestich` **rimanda** ad `Acrostic`, cioè il telestico non ha una pagina propria e vive dentro l'acrostico; in italiano `Telestico` e `Mesostico` sono due voci separate. La stessa cosa è una variante da una parte e una forma dall'altra, e il rimando è l'affermazione che lo dichiara.

**Sul sistema, qui cade il confine.** La voce 349, acrostico ha lasciato un'ipotesi da verificare: che il sistema sappia costruire un acrostico, perché l'unica lettera da maneggiare è la prima di una riga, cioè un confine. Il telestico sta dalla stessa parte — l'ultima lettera è l'altro confine. **Il mesostico no**: chiede la *k*-esima lettera dentro una parola, che è esattamente l'operazione misurata come sbagliata in `ideas/10 §6`. Se l'ipotesi regge, questa voce è mezza dentro e mezza fuori, e il taglio passa in mezzo a lei. Non è stato provato, e **va verificato**.

## Esempi trovati

Dal Nordafrica, quarto secolo: l'iscrizione del *Praedium Sammacis*, otto esametri le cui iniziali danno PRAEDIVM e le cui finali danno SAMMACIS. Ricontato in `build/check_346.py` per due strade — riga per riga, e impaginando le otto righe in una griglia di caratteri e leggendone due colonne.

Da Teofilo Folengo, riportato da Dossena 1994: cinque esametri che danno NECAT in acrostico e NECAT in telestico. Il mesostico che la fonte gli attribuisce **non è verificabile sul testo che abbiamo**, perché la colonna centrale dipende dall'impaginazione e l'estrazione della pagina la perde: si dichiara invece di ricostruirla a naso.

Da John Cage, riportato da `mesostic.txt`: un mesostico al cento per cento su KITCHEN, sette righe in inglese.

Dal *Quadrato del Sator*: la stessa idea portata al limite, con le parole che si leggono in tutti i sensi.

## Una nostra versione

Due parti. La prima si legge, e la verifica è dentro il materiale. La seconda si costruisce, e usa il metodo di Mac Low per togliere di mezzo la parte impossibile: le righe non si inventano, si trovano.

> **Le due colonne**
>
> Questa è un'iscrizione latina del quarto secolo, dal Nordafrica. Non serve sapere il latino.
>
> ```
>  PRAESIDIVM  AETERNAE  FIRMAT  PRVDENTIA PACIS
>  REM QVOQVE ROMANAM FIDAT VT AT VNDIQVE DEXTRA
>  AMNI   PRAEPOSITVM  FIRMANS  MVNIMINE  MONTEM
>  E   CVIVS   NOMEN   VOCITAVIT  NOMINE  PETRAM
>  DENIQVE   FINITIMAE   GENTES  DEPONERE  BELLA
>  IN  TVA  CONCVRRVNT  CVPIENTES FOEDERA SAMMAC
>  VT  VIRTVS  COMITATA  FIDEM CONCORDET IN OMNI
>  MUNERE   ROMVLEIS   SEMPER  SOCIATA  TRIVMFIS
> ```
>
> Leggi la prima colonna, dall'alto in basso. Poi leggi l'ultima. Sono due parole latine, e insieme fanno il nome con cui questa pietra è conosciuta: **il podere di Sammac**.
>
> Gli spazi in mezzo alle parole sono stati allargati apposta, perché le righe finissero tutte nello stesso punto. Senza quell'accorgimento la seconda colonna non ci sarebbe.
>
> **Adesso la parte difficile.** C'è una terza versione dello stesso gioco in cui la lettera non sta all'inizio né alla fine, ma **in mezzo**. Il compositore John Cage ne ha scritti a centinaia. Uno dei suoi:
>
> ```
>  let us maKe
>  of thIs
>  modesT
>  plaCe
>  a room Holding
>  tons of lovE
>  (&, Naturally, much good food, too)
>
>  La tua, su una parola di sei lettere, presa da
>  un libro che hai gia' in casa:
>
>  ----------------------------------------
>  ----------------------------------------
>  ----------------------------------------
>  ----------------------------------------
>  ----------------------------------------
>  ----------------------------------------
> ```
>
> Il modo di Cage era questo, e toglie la parte impossibile: **le righe non le inventi, le trovi.** Apri un libro qualunque, scorri finché non trovi una riga che contiene la lettera che ti serve, e copiala mettendo quella lettera in maiuscolo. Poi la riga successiva, per la lettera successiva.
>
> Una regola in più, se vuoi che il tuo mesostico si legga anche senza le maiuscole: fra una maiuscola e la successiva non deve ricomparire nessuna delle due lettere. La inventò l'assistente di Cage, e serve a far sì che chi legge trovi la lettera giusta e non un'altra prima.

La prima parte ha una risposta sola e si controlla senza foglio delle soluzioni: le due colonne danno due parole latine, e il testo dice che cosa significano.

La seconda parte è l'unica consegna di tutto il capitolo 12 in cui chi risponde attinge a un libro che ha già in casa. Non è un ripiego: è il metodo dell'autore, e toglie il vincolo che rende un mesostico difficile da comporre, cioè trovare righe che stiano in piedi e abbiano la lettera nel punto giusto.

La regola in fondo è facoltativa apposta. È un controllo che si fa con un dito e che una macchina farebbe meglio; darla come opzione invece che come obbligo è quello che la distingue da un compito.

Dove si romperebbe: sul display da quattro righe per quarantaquattro caratteri l'iscrizione non ci sta, e un mesostico di quattro lettere sì. Sul foglio in bianco e nero ci sta tutto, e la colonna la fa il maiuscolo, che non ha bisogno di colore.

## Da riprendere alla rassegna

**La riga di differenza.** Questa voce e la voce 349, acrostico stanno sulla variabile **dove sta la lettera che si legge, e chi lo dichiara**: all'inizio nell'acrostico, alla fine nel telestico — in tutti e due i casi lo dichiara la forma —, in mezzo nel mesostico, e lì non lo dichiara nessuno. Le prime tre voci della sezione — voce 346, rebus, voce 347, rebus stereoscopico e voce 348, rebus a domanda — stanno su un'altra variabile, di che cosa sia fatto l'esposto, e il loro termine di paragone è la voce 346, rebus. La voce 351, frase bipartita non sta su nessuna delle due.

**Una posizione che non è un bordo va dichiarata, e dichiararla costa una scelta tipografica.** Vale ben oltre l'enigmistica: ogni volta che un foglio chiede di guardare in un punto che non è l'inizio o la fine di qualcosa, quel punto va segnato. Da tenere accanto alla voce 349, acrostico, dove tre manoscritti biblici facevano già la stessa cosa con le maiuscole e con l'inchiostro rosso.

**La stessa struttura può servire a nascondere o a generare.** L'enigmistica ci nasconde un nome; Cage e Mac Low ci estraggono testi nuovi da libri vecchi. È il caso più netto che l'enciclopedia abbia raccolto di una forma con due usi opposti, e il secondo uso è quello che una casa può fare senza nessuno che nasconda niente.

**Trovare le righe invece di inventarle** è una mossa nuova nell'elenco, e viene da un compositore e non da un pedagogista. Toglie il costo della composizione lasciando intatto il vincolo, e si può provare su tutte le forme che chiedono di scrivere sotto costrizione — la voce 124, lipogramma, la voce 69, vincolare, e metà del capitolo 7.

**Una fonte può attribuire a un testo una proprietà che il testo estratto non porta più.** Il mesostico dei cinque esametri di Folengo dipende dall'incolonnamento, e l'estrazione della pagina lo perde. È lo stesso guasto delle figure che non arrivano nel testo, applicato agli spazi: **quando una proprietà è tipografica, il testo semplice non la conserva.**
