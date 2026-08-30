# Cifrario di Cesare

- **Numero** 130 nell'enciclopedia, capitolo 5 — Enigmi, sezione «Enigmi verbali»
- **Si chiama anche** Caesar cipher, cifrario a scorrimento, *shift cipher*, codice di Cesare, ROT13, disco cifrante, anello decodificatore
- **In una riga** ogni lettera si sostituisce con quella che sta n posti più in là nell'alfabeto.
- **Fonti** `caesar-cipher.txt`, `substitution-cipher.txt`, `vigenere-cipher.txt`, `frequency-analysis.txt`, tutte prese il 30 agosto 2026
- **Stato della ricerca** fatta, 30 agosto 2026

## Che cos'è

Un cifrario a sostituzione in cui la tabella non è arbitraria: **è l'alfabeto stesso, fatto scorrere di un numero fisso di posti.** Con uno scorrimento di tre, la A diventa D, la B diventa E, e la fine dell'alfabeto ricomincia dall'inizio.

**Quello che lo separa dal cifrario a sostituzione (voce 129, cifrario a sostituzione) è che la chiave non è una tabella: è un numero.** Non c'è niente da possedere e niente da perdere. Chi sa che lo scorrimento è tre sa tutto, e può ricostruire la corrispondenza intera contando sulle dita. È il primo dei tre gradini di questo blocco: qui la chiave è **una regola aritmetica da applicare**, alla voce 131, codice a numeri (A=1) è una corrispondenza che sanno già tutti, alla voce 132, Morse è un codice storico che si trova ovunque.

Detto in numeri, che è il modo in cui si capisce: si dà alle lettere un numero, A vale 0 e Z vale 25, e allora cifrare è **sommare n e prendere il resto della divisione per ventisei**. Decifrare è sottrarre n e fare lo stesso. Il cifrario di Cesare è l'unica voce di questo capitolo che sia, letteralmente, un'operazione di aritmetica.

Parti mobili:

- **Lo scorrimento.** Un numero da 1 a 25 in inglese, da 1 a 20 in un alfabeto italiano di ventuno lettere. Lo zero non cifra niente.
- **Se l'alfabeto gira.** Svetonio racconta che Augusto usava lo scorrimento di uno **senza far girare l'alfabeto**: al posto della Z scriveva AA. È una scelta diversa e produce un cifrario diverso.
- **Se lo scorrimento cambia lungo il testo.** Se cambia a ogni lettera secondo una parola chiave ripetuta, il cifrario si chiama **Vigenère**, ed è tutt'altro animale: non si rompe contando le lettere. Se la chiave è lunga quanto il messaggio, presa a caso, mai riusata e nota a nessun altro, si chiama **blocco monouso** ed è **impossibile da rompere**. Il problema, dice la fonte, è consegnare quella chiave.
- **Verso quali segni si scorre.** Di solito lettere. Ma si può scorrere verso i numeri, ed è quello che faceva Provenzano.

## Da dove viene

Prende il nome da **Giulio Cesare**, che secondo lo storico romano **Svetonio** lo usava con uno scorrimento di tre per proteggere messaggi di rilievo militare. È il primo uso documentato di questo schema, benché altri cifrari a sostituzione fossero già in circolazione. Sempre Svetonio dice che **Augusto**, suo nipote, usava lo scorrimento di uno. E il grammatico **Aulo Gellio**, nelle *Notti attiche*, cita un trattato — perduto — del grammatico Probo «sul significato segreto delle lettere nella composizione delle epistole di Cesare», il che fa pensare che Cesare usasse anche sistemi più complicati. (`caesar-cipher.txt`, 30 agosto 2026)

**Quanto fosse efficace all'epoca non si sa**, e la fonte lo dice esplicitamente: non esiste nessuna testimonianza di tecniche contemporanee per risolvere i cifrari a sostituzione semplice. Le prime che sopravvivono sono di **Al-Kindi, nel nono secolo**, con la scoperta dell'analisi delle frequenze. Fra Cesare e Al-Kindi ci sono novecento anni in cui, per quel che si sa, il cifrario poteva funzionare davvero.

Una versione ebraica dello scorrimento — da non confondere con l'atbash, che rovescia l'alfabeto — si trova a volte sul retro delle pergamene delle *mezuzot*: sostituendo ogni lettera con quella che la precede si legge *YHWH, nostro Dio, YHWH*, una citazione dalla pergamena stessa.

Nell'Ottocento gli annunci personali dei giornali servivano a scambiarsi messaggi cifrati con sistemi semplici, e David Kahn (1967) descrive innamorati che si scrivevano sul *Times* con il cifrario di Cesare. Nel **1915**, durante la prima guerra mondiale, **l'esercito russo lo adottò come rimpiazzo di cifrari più complicati che le truppe non riuscivano a imparare**, e i crittanalisti tedeschi e austriaci non ebbero nessuna difficoltà a leggere i loro messaggi.

Due usi recenti, e sono tutti e due casi giudiziari. Nell'**aprile 2006** il capo mafioso **Bernardo Provenzano fu catturato in Sicilia anche perché alcuni dei suoi pizzini, scritti in modo maldestro con una variante del cifrario di Cesare, furono decifrati**: il suo cifrario usava numeri, quindi A si scriveva 4, B si scriveva 5, e così via. Nel **2011** un dipendente della British Airways, Rajib Karim, fu condannato per terrorismo dopo aver usato un cifrario di Cesare per discutere attentati; e la fonte riporta il dettaglio che spiega tutto: **avevano a disposizione una crittografia molto migliore, ma scelsero uno schema fatto da loro in un foglio di calcolo, scartando un programma più serio perché «gli infedeli lo conoscono, quindi dev'essere meno sicuro».**

Oggi lo scorrimento di tredici si chiama **ROT13**, e serve su internet a coprire la battuta finale di una barzelletta o il finale di un film: non è crittografia, è una tendina.

## Varianti e parenti

- **Cruciverba crittografato** (voce 354, cruciverba crittografato) — **il confine da dichiarare**: lì il gioco enigmistico italiano in cui la corrispondenza fra numeri e lettere va scoperta risolvendo lo schema; qui il cifrario come sistema di scrittura, in cui la corrispondenza si dà con un numero solo.
- **Cifrario a sostituzione** (voce 129, cifrario a sostituzione) — la famiglia. Il cifrario di Cesare ne è il caso più povero: delle 26 fattoriale tabelle possibili ne usa venticinque.
- **Codice a numeri (A=1)** (voce 131, codice a numeri (A=1)) — il parente stretto: anche lì la corrispondenza è l'ordine dell'alfabeto, ma senza scorrimento.
- **Atbash** — l'alfabeto rovesciato invece che scorso: la A diventa Z. Non è uno scorrimento e non si rompe allo stesso modo.
- **ROT13** — lo scorrimento di tredici, che ha una proprietà comoda: applicato due volte riporta al testo di partenza, perché tredici più tredici fa ventisei.
- **Vigenère** — lo scorrimento cambia a ogni lettera secondo una parola chiave ripetuta. La fonte segnala che una chiave ripetuta introduce uno schema ciclico rilevabile: la Confederazione, nella guerra civile americana, usava *Complete Victory*.
- **Blocco monouso** — il Vigenère con chiave lunga quanto il messaggio, casuale e mai riusata. Indecifrabile, e impraticabile.
- **Disco cifrante e anello decodificatore** — la forma materiale: due alfabeti concentrici che ruotano uno dentro l'altro. `caesar-cipher.txt` nota che il cifrario di Cesare si trova ancora oggi nei giocattoli per bambini sotto forma di anello.
- **Scitala** — l'attrezzo greco per la trasposizione: si nomina qui perché è l'altro polo, quello della voce 121, anagramma.
- **Aritmetica in altra base** (voce 372, aritmetica in altra base) — il parente matematico: anche lì si conta girando attorno a un modulo.

## Che cosa se ne sa

**È il cifrario più debole documentato, e la debolezza è misurata.** `caesar-cipher.txt`, presa il 30 agosto 2026, dà tre numeri.

Il primo: **gli scorrimenti possibili sono venticinque in inglese**, quindi si prova a decifrare con tutti e venticinque e si guarda quale dà una frase sensata. È un attacco di forza bruta che non richiede nessuna competenza. La fonte porta l'esempio `exxegoexsrgi`, in cui lo scorrimento di quattro dà `attackatonce` ed è l'unico che significhi qualcosa.

Il secondo: **la distanza di unicità del cifrario di Cesare è circa 2.** In media bastano due caratteri di testo cifrato per determinare la chiave. In pratica, con sei si è quasi sempre a posto. Per confronto, il cifrario a sostituzione ad alfabeto mescolato della voce 129, cifrario a sostituzione ne chiede 27,6.

Il terzo è un fatto algebrico e ha una conseguenza pratica netta: **cifrare due volte non serve a niente.** Uno scorrimento di A seguito da uno scorrimento di B è identico a un singolo scorrimento di A più B. In termini matematici, le operazioni di cifratura formano un gruppo rispetto alla composizione. Non c'è modo di irrobustire un cifrario di Cesare ripetendolo.

Il metodo di rottura che vale la pena riportare non è quello statistico ma quello manuale, perché è **una procedura che si esegue senza capire niente**, e questo capitolo ne colleziona. Si chiama *completing the plain component*, completare la componente in chiaro: si scrive il testo cifrato in cima al foglio, e sotto ogni lettera si scrive l'alfabeto intero, cominciando da quella lettera e andando in giù. Quando si è finito, **una delle righe orizzontali è il messaggio.** Non c'è niente da indovinare: si guardano le venticinque righe e una si legge.

L'altra strada è l'analisi delle frequenze, che qui è più facile che altrove perché lo scorrimento sposta l'intera distribuzione in blocco: si disegna l'istogramma delle lettere del testo cifrato e si guarda di quanto è slittato rispetto a quello della lingua. In italiano l'ordine di frequenza è **e a i o n l r t s c d u** (`letter-frequency.txt`, da Singh e Galli, *Codici e Segreti*, Rizzoli 1999).

**Non c'è nessuna misura di effetto** su chi lo usa o lo impara, in nessuna delle quattro fonti prese.

Sul nostro sistema: **il sistema non sa manipolare le lettere dentro le parole** (misurato, `ideas/10 §6`), e sommare tre a una lettera è esattamente quel tipo di operazione. Non può cifrare, decifrare, né controllare. Ma qui, a differenza della voce 129, cifrario a sostituzione, **c'è una macchina fisica che fa il lavoro ed è di carta**: due strisce con l'alfabeto scritto sopra, una che scorre sull'altra. La corrispondenza non si ricorda e non si calcola: si guarda. È la stessa idea già raccolta come *il mondo come processore di simboli* alle schede 326 e 333, ed è il caso più semplice che esista.

## Esempi trovati

Da `caesar-cipher.txt`, scorrimento di tre a sinistra: `THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG` diventa `QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD`.

Dalla stessa fonte, l'esempio di rottura: `exxegoexsrgi`, che con scorrimento quattro dà *attack at once*.

Da Svetonio: Cesare scorreva di tre; Augusto di uno, e al posto della Z scriveva AA.

Dalle *mezuzot* ebraiche: sul retro della pergamena, una frase che scorrendo di una lettera indietro dà *YHWH, nostro Dio, YHWH*.

Dagli annunci personali del *Times* nell'Ottocento, secondo David Kahn: innamorati che si scrivevano con il cifrario di Cesare in mezzo alle inserzioni.

Dall'esercito russo, 1915: adottato perché le truppe non riuscivano a imparare niente di più difficile, e letto senza fatica dagli austriaci.

Da Bernardo Provenzano, aprile 2006: pizzini in cui A si scriveva 4 e B si scriveva 5.

Da Usenet: ROT13, che nasconde il finale di una storia a chi non vuole saperlo e non a chi vuole leggerlo.

Dagli anelli decodificatori dei giocattoli, che sono dischi cifranti di Cesare venduti come giochi da almeno un secolo.

## Una nostra versione

La macchina è di carta e si ritaglia in due minuti. Poi si dimostra, con le proprie mani, che non serve a niente — che è la cosa più interessante che questo cifrario abbia da dire.

> **Due strisce, e poi la scala**
>
> Giulio Cesare scriveva ai suoi generali spostando ogni lettera di tre posti in avanti. Suo nipote Augusto la spostava di uno. Nel 1915 l'esercito russo lo usava ancora, perché i soldati non riuscivano a imparare niente di più difficile, e i tedeschi leggevano tutto senza sforzo.
>
> **Primo: la macchina.** Ritaglia le due strisce lungo le righe tratteggiate.
>
> ```
>  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
>   A B C D E F G H I L M N O P Q R S T U V Z
>  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
>   A B C D E F G H I L M N O P Q R S T U V Z A B C D E F G H I L M N O P Q R S T U V Z
>  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
> ```
>
> La striscia lunga porta l'alfabeto **due volte**, ed è per questo che non devi mai contare: quando arrivi in fondo, ricomincia da sé.
>
> Metti la striscia corta sopra quella lunga e falla scivolare a destra di quanti posti vuoi. Quel numero è la chiave. **Se scivoli di tre, sotto la tua A c'è una D.** Cifri leggendo in giù, decifri leggendo in su.
>
> ```
>  Il mio scorrimento è  ────
>
>  Il mio messaggio:
>  ──────────────────────────────────────────────────────────────
>
>  Cifrato:
>  ──────────────────────────────────────────────────────────────
> ```
>
> **Secondo: adesso rompilo.** Senza le strisce.
>
> Prendi le prime otto lettere del tuo messaggio cifrato e scrivile nella riga in alto, una per colonna. Poi sotto ogni lettera scrivi l'alfabeto in giù, partendo da quella lettera. Quando arrivi alla Z ricominci dalla A.
>
> ```
>       ┌───┬───┬───┬───┬───┬───┬───┬───┐
>   0   │   │   │   │   │   │   │   │   │   ← le lettere cifrate
>       ├───┼───┼───┼───┼───┼───┼───┼───┤
>   1   │   │   │   │   │   │   │   │   │
>   2   │   │   │   │   │   │   │   │   │
>   3   │   │   │   │   │   │   │   │   │
>   4   │   │   │   │   │   │   │   │   │
>   5   │   │   │   │   │   │   │   │   │
>   6   │   │   │   │   │   │   │   │   │
>   7   │   │   │   │   │   │   │   │   │
>   8   │   │   │   │   │   │   │   │   │
>   9   │   │   │   │   │   │   │   │   │
>  10   │   │   │   │   │   │   │   │   │
>  11   │   │   │   │   │   │   │   │   │
>  12   │   │   │   │   │   │   │   │   │
>  13   │   │   │   │   │   │   │   │   │
>  14   │   │   │   │   │   │   │   │   │
>  15   │   │   │   │   │   │   │   │   │
>  16   │   │   │   │   │   │   │   │   │
>  17   │   │   │   │   │   │   │   │   │
>  18   │   │   │   │   │   │   │   │   │
>  19   │   │   │   │   │   │   │   │   │
>  20   │   │   │   │   │   │   │   │   │
>       └───┴───┴───┴───┴───┴───┴───┴───┘
> ```
>
> **Una di quelle ventuno righe si legge.** Non serve indovinare, non serve sapere niente: si guarda in orizzontale e una riga è italiano. Questo metodo si chiama, dal Settecento, *completare la componente in chiaro*, e chiunque lo può fare.
>
> ```
>  La riga che si legge è la numero ────
>  Ce n'era più di una che sembrava una parola?   sì ──   no ──
> ```
>
> **Terzo, e questa è una domanda a cui non so rispondere.** In inglese le parole *river* e *arena* sono una lo scorrimento dell'altra: cifrandole con chiavi diverse danno lo stesso risultato, e la scala non basta a scegliere. **In italiano non conosco nessuna coppia così, e la fonte non ne dà.**
>
> ```
>  Se ne trovi una, scrivila qui:  ──────────  e  ──────────
> ```
>
> Serve una parola in cui, spostando tutte le lettere dello stesso numero di posti, ne esca un'altra parola italiana. La scala serve a cercarle: scrivi una parola in cima e guarda tutte e venti le righe.

Le due strisce sono la macchina, e l'alfabeto scritto due volte sulla striscia lunga è tutto il trucco: toglie l'unica operazione difficile, che è tornare all'inizio quando si esce dall'alfabeto. Nessuno conta, nessuno somma, nessuno sbaglia in silenzio.

La scala è la seconda procedura che si esegue senza capire, dopo l'ordinamento alfabetico della voce 121, anagramma e le dieci coppie della voce 123, palindromo. E dimostra una cosa che vale la pena mostrare invece di dire: **un segreto che si rompe scrivendo venti righe non era un segreto.**

L'ultima domanda non ha risposta nel foglio né in chi l'ha scritto, e la scala diventa lo strumento per cercarla. È un caso di *ammettere di non sapere se una cosa esiste, e chiederlo* — la mossa già usata alla voce 104, gioco da tavolo — applicata qui a un fatto sulla lingua italiana.

**Dove si romperebbe.** Il sistema non può stampare un messaggio già cifrato e non può controllare quello scritto a mano: la cifratura la fa la striscia. Sul pannello da quattro righe entra una riga cifrata corta e il numero dello scorrimento, e nient'altro; la scala richiede ventuno righe e non ci sta.

## Da riprendere alla rassegna

**Una macchina di carta fa esattamente l'operazione che il sistema non sa fare,** e costa due tagli di forbice. Due strisce con l'alfabeto, di cui una scritta due volte, eseguono un'aritmetica modulare senza che nessuno la calcoli. È il terzo attrezzo di questo tipo raccolto nel capitolo, dopo il taglio della sciarada e le lettere ritagliate dell'anagramma, e comincia a sembrare una famiglia: **gli strumenti di carta che fanno operazioni esatte.** Da censire tutti insieme.

**Dimostrare che una cosa non funziona è una consegna, e produce più di dimostrare che funziona.** La scala di ventuno righe non serve a decifrare un messaggio: serve a far vedere quanto poco costi. È una struttura che l'enciclopedia non ha ancora nominato — l'esercizio il cui esito è la perdita di una convinzione — e vale la pena cercarla altrove.

**La chiave come numero invece che come tabella** è la ragione per cui questo cifrario è sopravvissuto duemila anni pur essendo inutile: si impara in trenta secondi e non si può perdere. L'esercito russo del 1915 lo ha scelto sapendolo. Vale come principio generale sulla consegna: **una regola che sta in una riga vince su una regola migliore che sta in una pagina**, e vince anche quando è peggiore.

**Ripetere un'operazione debole non la rafforza,** e qui è dimostrato algebricamente. Vale la pena tenerlo come esempio pulito di una cosa che si crede spesso: che fare due volte una cosa sia meglio che farla una volta sola.

**Non si sa se il cifrario di Cesare funzionasse ai tempi di Cesare,** perché non esiste nessuna testimonianza di come si rompessero i cifrari prima di Al-Kindi. È una lacuna di novecento anni dichiarata dalla fonte, ed è un buon promemoria: l'assenza di prove di rottura non è una prova di sicurezza.
