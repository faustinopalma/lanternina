# Crittografia pura

- **Numero** 341 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Crittografie»
- **Si chiama anche** crittografia semplice, crittografia senza aggettivi, esposto, plexer, cryptic
- **In una riga** una sequenza di lettere e numeri da leggere come frase: `A B C = alfabeto muto`.
- **Contratto** voce breve
- **Fonti** scritta il 30 agosto 2026 senza fonti e dichiarandolo; ampliata e corretta il 1 settembre 2026 su `it-crittografia-gioco.txt`, `it-gioco-enigmistico.txt`, `it-enigmistica.txt`, `it-cesura-enigmistica.txt`
- **Stato della ricerca** fatta, 30 agosto 2026, ampliata il 1 settembre 2026

## Che cos'è

Una crittografia è un gioco in tre tempi. C'è un **esposto**: lettere, numeri e segni disposti in un certo modo. C'è una **prima lettura**: la frase con cui si dice quello che si vede. E c'è una **seconda lettura**: le stesse identiche lettere, nello stesso ordine, con gli spazi in un altro posto. Un **diagramma** numerico dichiara le lunghezze delle parole di tutt'e due le letture, e le separa con un segno di uguale.

La crittografia è **pura** quando la prima lettura è la sola descrizione della forma dell'esposto, senza nessun riferimento al significato. `it-crittografia-gioco.txt`, presa il 1 settembre 2026, la chiama «semplice, o pura, o più spesso crittografia senza aggettivi», e aggiunge la cosa che la definisce: «l'esposto può talvolta essere privo di significato». Il ragionamento è «di tipo meccanico».

Parti mobili:

- **La disposizione dell'esposto.** Sopra, sotto, dentro, ripetuto, capovolto: la prima lettura nomina la posizione, e i nomi delle posizioni sono le parole che poi si spezzano.
- **Il diagramma a due lati.** A sinistra la prima lettura, a destra la seconda. È la parte che rende il gioco controllabile.
- **La lunghezza della soluzione.** Quando sta in una parola sola il gioco si chiama monoverbo — voce 336, monoverbo.
- **Quanto è lontano quello che si vede da quello che si legge.**

## Da dove viene

Enigmistica italiana. `it-enigmistica.txt`, presa il 1 settembre 2026, data le prime crittografie al **1877**, a firma di Pio Alberto Visoni, sulla torinese *La gara degli indovini* e sul piacentino *L'aguzzaingegno*, dove uscirono col nome di **rebus dell'avvenire**. Il nome che è rimasto è più tardo.

Fuori d'Italia il gioco non ha una casella sua. `it-crittografia-gioco.txt` scrive che «gran parte delle crittografie italiane verrebbero comprese nel mondo anglosassone come rebus, in particolare nella categoria definita come plexer (rebus in cui non vi sono immagini ma lettere o simboli)», o come definizioni di *cryptic crossword*. Il controllo dei titoli fatto il 1 settembre 2026 con `build/check_titoli_341.py` conferma la parte debole dell'affermazione: `Plexer` su Wikipedia in inglese non ha una pagina propria e rimanda a `Rebus`.

## Varianti e parenti

- **Crittografia sinonimica** (voce 344, crittografia sinonimica) — la stessa meccanica, con un sinonimo da trovare prima.
- **Crittografia perifrastica** (voce 342, crittografia perifrastica) — la stessa meccanica, con un giro di parole.
- **Crittografia sillogistica** — la stessa meccanica, con un sillogismo da esplicitare; non ha una voce sua nell'elenco.
- **Crittografia mnemonica** (voce 343, crittografia mnemonica) — quella che ha perso la meccanica: si interpreta e basta.
- **Crittografia a frase** — la soluzione è una frase doppia e non ci sono lettere interposte a legarne le parole; la fonte dice che lì «la doppia lettura è perfetta».
- **Cambio di spaziatura** (voce 345, cambio di spaziatura) — il meccanismo nudo, senza la parte da leggere.
- **Monoverbo** (voce 336, monoverbo) — la crittografia con la soluzione in una parola sola.
- **Anagramma crittografico** — un'altra conservazione: le lettere restano le stesse ma cambiano ordine invece di cambiare spaziatura. Confina con la voce 331, anagramma.
- **Rebus** (voce 346, rebus) — la stessa idea con le immagini al posto dei segni.
- **Cruciverba crittico** (voce 126, cruciverba crittico) — il parente più vicino fuori dall'Italia.

## Che cosa se ne sa

**La riga dell'elenco porta l'esempio di un altro gioco.** `A B C = alfabeto muto` non è una crittografia pura: le lettere non si conservano — `abc` contro `alfabetomuto` — e quindi non c'è nessuna rispaziatura. È una crittografia mnemonica, cioè una frase che descrive l'esposto in un senso e vuol dire tutt'altro nell'altro. Verificato in `build/check_335.py` il 1 settembre 2026 e ripreso in `build/check_341.py`. **La versione di questa scheda scritta il 30 agosto 2026 aveva preso l'esempio dell'elenco per buono, e da lì aveva ricavato tutto il resto.**

L'esempio canonico che la fonte dà è un altro: l'esposto in cui *RI* sta sotto e *AL* sta su *GO*, prima lettura «RI sotto AL su GO» (2 5 2 2 2), seconda lettura *risotto al sugo* (7 2 4). Tredici lettere di qua e tredici di là.

**Il diagramma a due lati è la firma delle crittografie meccaniche, e la mnemonica non ce l'ha.** In `build/check_341.py` le cinque tipologie sono messe in fila e si conta, per ognuna, quanti stacchi fra parole si spostano fra la prima e la seconda lettura:

```
 tipologia     diagramma              stacchi che si spostano
 pura          2 5 2 2 2 = 7 2 4      2 su 4
 sinonimica    3 1 1 6 4 = 7 8        5 su 5
 perifrastica  1 2 3 4 1 5 = 6 2 4 4  6 su 7
 sillogistica  1 1 10 = 6 6           3 su 3
 mnemonica     8 3 8                  nessuno
```

Zero stacchi mossi vale per la mnemonica e per nessun'altra tipologia. Sopra quello zero, però, **la quota non ordina niente**: la pura ne muove di meno, ma sinonimica e sillogistica pareggiano a cento per cento e la perifrastica sta in mezzo. La grandezza separa la mnemonica dal resto, e su cinque esempi non fa altro.

**Una tipologia su sei si risolve senza mettere in mezzo un concetto.** `it-gioco-enigmistico.txt`, presa il 1 settembre 2026, elenca sei tipi di crittografia e li raggruppa in tre: meccanico — la pura; mnemonico — la frase bisenso e la crittografia a frase; misto — sinonimica, perifrastica, sillogistica. Uno, tre, due. La pura è il caso limite in cui non c'è niente da capire e c'è solo da guardare.

**Il sistema non può costruire una crittografia né verificarla.** Richiede di ragionare insieme sui nomi delle lettere, sulla loro posizione e sul loro numero, e poi di controllare che la soluzione abbia esattamente le lettere dichiarate: le due cose che sbaglia (`ideas/10 §6`). Può però stampare quelle già fatte, e può far contare le lettere a chi risponde.

**È la forma con la curva d'ingresso più ripida dell'elenco.** Non è difficile: è opaca. Chi non ha mai visto una soluzione non può cominciare, e chi ne ha viste tre risolve. Poche forme hanno un salto così netto fra il non capire e il capire, e nessuna via di mezzo. Questa osservazione è del 30 agosto 2026 e nessuna delle fonti prese poi la conferma o la smentisce: **va verificata**.

## Esempi trovati

Da `it-crittografia-gioco.txt`, con la spiegazione in nota: `RI sotto AL su GO` = *risotto al sugo*, diagramma (2 5 2 2 2) = (7 2 4). È l'esempio che la pagina presenta prima di dire «una crittografia del tipo presentato sopra si dice semplice, o pura».

Dalla stessa pagina, la sillogistica `U L trasferiti` = *Ultras feriti*: le lettere U e L cambiano *casa* in *causa* e *paese* in *palese*, chi cambia casa e paese si trasferisce, quindi U e L si sono trasferiti. Dodici lettere per parte.

Dalla stessa pagina, l'anagramma crittografico `Recondita` = *donatrice*, che definisce l'esposto *Befana* perché le due parole si leggono di seguito. Nove lettere, stesso multinsieme, ordine diverso: **è un'altra conservazione**, e non è quella della crittografia.

Dal cruciverba crittico inglese, che ha lo stesso spirito con altre regole: ogni definizione contiene due parti, una che definisce e una che costruisce la parola pezzo per pezzo, e il difficile è capire dove passa il confine.

Dal mondo di tutti i giorni: `6 3 1 mito` e le abbreviazioni dei messaggi, che sono crittografie spontanee e che nessuno ha dovuto insegnare. Osservazione del 30 agosto 2026, senza fonte.

## Una nostra versione

Il sistema non può costruire una crittografia. Può però dare l'unica cosa che manca a chi non ha mai visto il gioco — un esempio risolto — e poi girarlo dalla parte dell'autore.

> **Il quaderno di chi scriveva male apposta**
>
> C'è un gioco italiano del 1877 che funziona così. Ti danno delle lettere messe in un certo modo. Tu **dici a voce quello che vedi**, e poi riscrivi le stesse identiche lettere spostando gli spazi. Niente si aggiunge e niente si toglie.
>
> ```
>       ─────      AL
>         RI       ──
>                  GO
>
>  si dice    RI sotto AL su GO      2 5 2 2 2
>  si scrive  risotto al sugo        7 2 4
> ```
>
> I numeri a destra sono le lunghezze delle parole, prima e dopo. Contali: tredici di sopra e tredici di sotto. Devono essere sempre uguali, ed è questo che ti dice se hai ragione.
>
> Adesso scrivine tre tu. Non devono essere difficili: devono funzionare quando qualcuno te le legge ad alta voce.
>
> ```
>  ─────────────────  si dice    ─────────────────  ─────────
>                     si scrive  ─────────────────  ─────────
> ```
>
> Poi copia la tua preferita su un foglietto, **senza la seconda riga**, e lasciala in giro per casa.

L'esempio risolto è l'intera consegna: nessuna spiegazione della regola funzionerebbe altrettanto bene, e questo è il caso più puro dell'esempio svolto che si trovi nell'elenco. La riga sul contare le lettere mette il controllo dell'errore dentro il foglio. Il foglietto lasciato in giro lo sposta fuori dal foglio e fuori dal sistema.

**Dove si romperebbe.** Sul pannello da quattro righe la disposizione dell'esposto non ci sta, e la disposizione è metà del gioco. Le tre righe da riempire il sistema non le può leggere: può contare le lettere delle due letture, non giudicare se la prima descrive davvero il disegno.

## Da riprendere alla rassegna

**Questa è la voce di paragone della sezione «Crittografie», e la variabile è quanta parte della prima lettura è meccanica.** Qui è tutta meccanica: si guarda l'esposto e lo si descrive. Alla voce 344, crittografia sinonimica e alla voce 342, crittografia perifrastica bisogna passare per un concetto. Alla voce 343, crittografia mnemonica non resta altro che il concetto, e con lui sparisce il conto.

**La consegna fatta di soli esempi risolti** è il modo giusto di aprire qualunque forma opaca, e questa è la forma più opaca dell'elenco. Da tenere in mente per tutte le voci che hanno un salto netto fra non capire e capire.

**La distinzione fra difficile e opaco** merita un posto suo. Una cosa difficile si affronta e non viene; una cosa opaca non si affronta nemmeno. Sembrano chiedere rimedi diversi e nell'elenco sono confuse.

**Una glossa dell'elenco può essere giusta e portare l'esempio di un altro gioco**, ed è la seconda volta nel capitolo 12 dopo la voce 323, sciarada. Qui l'esempio sbagliato era finito dentro la scheda e ne aveva deciso il contenuto per due giorni: **un esempio non controllato costa più di una definizione non controllata**, perché da lui si ricava il resto.
