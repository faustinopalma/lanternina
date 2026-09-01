# Sciarada

- **Numero** 323 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che uniscono o dividono parole»
- **Si chiama anche** sciarada semplice, sciarada pura, charade, *charade*, «primo, secondo, intero», primiero e intiero, giustapposizione, X + Y = XY
- **In una riga** due parole si accostano e ne fanno una terza: *pane + rone → panerone*.
- **Contratto** voce breve
- **Fonti** `it-sciarada.txt`, `charades.txt`, `concatenation.txt`, `it-univerbazione.txt`, `it-composizione-linguistica.txt`, prese il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Si accostano due parole, nell'ordine, e viene fuori una terza. `it-sciarada.txt` la scrive **X + Y = XY**: *tram + busto = trambusto*. Non si toglie niente, non si sovrappone niente, non si intreccia niente.

È il **valore più povero** della variabile di questo blocco, che è *che cosa succede alle lettere nel punto in cui le due parole si toccano.* Qui non succede niente, e le altre quattro voci si descrivono per differenza da qui.

Ne segue una proprietà che le altre non hanno. Partendo dal totale, i candidati sono i punti in cui lo si può tagliare in due: su una parola di *n* lettere sono *n* − 1, e su *trambusto* sono otto. Otto righe stanno su un foglio, e allora **lo spazio di ricerca si stampa per intero** — la mossa della voce 314, scarto e della voce 321, antipodo, ed è la terza volta che il capitolo 12 la permette.

Parti mobili: quante parti sono (due, tre, di più), se l'ordine è dichiarato, e se il taglio cade dentro una sillaba o fra due.

La glossa dell'elenco non funziona: *rone* non è una parola italiana, e il formaggio lombardo si scrive *pannerone* con due n. È un giudizio nostro sul lessico, e vale come tale; la fonte porta invece un esempio che regge, *tram + busto*.

## Da dove viene

`it-sciarada.txt`, presa il 1 settembre 2026, fa risalire il meccanismo all'oniromanzia antica. Plutarco racconta che Alessandro, all'assedio di Tiro, sognò di catturare un satiro, e l'indovino Aristandro lesse σάτυρος come σα Τύρος, «Tiro è tua». Svetonio riferisce di un fulmine che abbatté la C di *Caesar* da una statua di Augusto: cento giorni di vita — C è cento — e poi la divinità, perché *aesar* in etrusco è il dio.

Come gioco si impone nella Francia del Settecento; il nome viene dal provenzale *charado*, chiacchierata. Le parti si chiamavano *premier, second, entier*, tradotti in italiano con *primiero, secondo, intiero*. La prima descrizione italiana è del 1835, in un codicetto de *Il Gondoliere* di Venezia, scritta da Bennassù Montanari.

Qui la fonte registra una biforcazione che vale per tutto il capitolo. In Francia e in Inghilterra si affermò un criterio **fonetico**: contava il suono, e *chat + rade = charade* era valida. In italiano si affermò un criterio **grafico**, «poi esteso a tutti i giochi enigmistici». Una decisione presa sulla sciarada regola oggi ogni gioco delle quarantotto voci di questo capitolo.

`charades.txt`, presa lo stesso giorno, segue l'altro ramo: il gioco di società inglese chiamato *charades* consisteva nel recitare una sillaba per volta, nell'ordine, e poi il tutto. Il gioco che oggi porta quel nome è mimato e ha perso le sillabe: **è rimasto il nome e se n'è andata la sciarada.**

## Varianti e parenti

- **Frase doppia** — una sola sequenza di lettere tagliata in due punti diversi: *tre | mendicanti* e *tremendi | canti*. `it-sciarada.txt` la dà come prima variante, e non è una sciarada perché non ci sono due parole da unire.
- **Sciarada alterna** (324) — le due parole si intrecciano invece di accostarsi.
- **Sciarada incatenata** (325) — le due parole si sovrappongono, e la parte comune si scrive una volta sola.
- **Lucchetto** (326) — le due parole si sovrappongono e la parte comune sparisce.
- **Incastro** (328) — la seconda entra intera dentro la prima.
- **Sciarada a bisensi** — la fonte la nomina e la tiene distinta dalle altre tre.
- **Univerbazione** — la stessa mossa fatta dalla lingua, senza gioco: *pomo d'oro → pomodoro*, *in vece → invece* (`it-univerbazione.txt`).
- **Composizione** — *crocevia*, *saliscendi*, *lavastoviglie*: due parole che ne fanno una terza (`it-composizione-linguistica.txt`).

## Che cosa se ne sa

`it-sciarada.txt` è una pagina di storia e di repertorio: dà le date, i nomi e la classificazione, e nessuna misura.

La misura viene da fuori. L'operazione della sciarada ha un nome in informatica — **concatenazione** — e `concatenation.txt`, presa il 1 settembre 2026, dice che le stringhe su un alfabeto con la concatenazione formano un **monoide libero**: l'operazione è associativa e l'elemento neutro è la stringa vuota. Due conseguenze si vedono sul foglio. Che sia associativa è il motivo per cui una sciarada a tre parti non ha bisogno di dire dove stanno le parentesi: *S + cara + faggio* si legge in un modo solo. Che non sia commutativa è il gioco: *busto + tram* non è *trambusto*, e l'ordine è metà della difficoltà.

Il conto che serve al foglio è elementare e lo si fa a mano: **i tagli di una parola di *n* lettere sono *n* − 1.** Su *trambusto*, otto. Verificato per formula e per enumerazione in `build/check_323.py`, dove sono anche stampati tutti e otto.

Su *trambusto* la risposta è **una sola**, e la ragione si può scrivere senza contare le parole italiane: delle otto parti sinistre — *t, tr, tra, tram, tramb, trambu, trambus, trambust* — solo *tra* e *tram* sono parole, e *mbusto* non lo è. Il giudizio sulle otto sinistre è nostro, dichiarato in `build/check_323.py`.

La verifica di questa forma sta in un **vocabolario**, come per tutto il capitolo 12: nessuna delle cinque classi del censimento del controllo dell'errore la copre.

## Esempi trovati

Da `it-sciarada.txt`, riscritti: *tram + busto = trambusto*; *ciocco + latino = cioccolatino*. E la frase doppia *tre mendicanti = tremendi canti*, tredici lettere nei due sensi.

Dalla letteratura, per via della stessa fonte: in *Harry Potter e il Calice di Fuoco* c'è una sciarada in tre parti, **S + cara + faggio**, dove la prima parte non è una parola ma una lettera indicata per posizione.

Dalla lingua, non dal gioco: *pomo d'oro* diventa *pomodoro* e *in vece* diventa *invece*. Sono sciarade avvenute per conto loro, e nessuno le ha proposte a nessuno.

## Una nostra versione

> **Otto tagli, e uno solo è quello giusto**
>
> TRAMBUSTO ha nove lettere, quindi otto punti in cui la si può spezzare in due. Sono tutti qui: non ce n'è un nono.
>
> ```
>  1  t|rambusto    2  tr|ambusto
>  3  tra|mbusto    4  tram|busto
>  5  tramb|usto    6  trambu|sto
>  7  trambus|to    8  trambust|o
> ```
>
> Uno solo di questi otto dà **due parole italiane.** Trovalo e scrivi il numero: ────
>
> Adesso il contrario, che è più difficile e non ha aiuti. Prendi TREMENDICANTI, tredici lettere di fila. Tagliala in due in **due modi diversi**, e tutte e due le volte deve venire qualcosa che si può dire.
>
> ```
>  ──────── | ────────────        ──────── | ────────────
> ```

Le otto righe sono **lo spazio di ricerca per intero**, e ci stanno su quattro. Il limite dominante del capitolo — il sistema non sa manipolare le lettere dentro le parole — non morde, perché al sistema non si chiede né di costruire né di verificare: gli si chiede di stampare otto stringhe che si ricavano tagliando una parola in tutti i modi.

La seconda metà non si può stampare per esteso, ed è dichiarata come la parte senza rete. Il giudizio «questa è una parola italiana» resta fuori dal sistema, e in casa un vocabolario non è garantito.

## Da riprendere alla rassegna

**Il termine di paragone di questo blocco.** Le cinque forme — questa scheda, la voce 324, sciarada alterna, la voce 325, sciarada incatenata, la voce 326, lucchetto e la voce 327, lucchetto riflesso — differiscono in una cosa sola: **che cosa succede alle lettere nel punto in cui le due parole si toccano.** Qui non succede niente. Le altre quattro aggiungono qualcosa, e ognuna si descrive in una riga di differenza da qui.

**Stampare per intero lo spazio di ricerca, per la terza volta nel capitolo.** Alla voce 314, scarto lo spazio era lineare nella lunghezza della parola e alla voce 321, antipodo era costante; qui è lineare di nuovo, e per una ragione diversa — si sceglie un punto, non una lettera. Da guardare alla rassegna: quante forme dell'elenco hanno uno spazio di ricerca che sta su un foglio, perché sono quelle in cui il limite tecnico del capitolo smette di contare.

**Una decisione presa su una forma può regolare un capitolo intero.** Il criterio grafico contro quello fonetico è stato scelto sulla sciarada nell'Ottocento e vale oggi per tutti i giochi enigmistici italiani. È il tipo di eredità che la rassegna dovrà cercare anche altrove: una regola che sembra della disciplina e viene invece da una forma sola.

