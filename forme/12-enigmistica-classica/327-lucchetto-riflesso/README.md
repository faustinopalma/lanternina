# Lucchetto riflesso

- **Numero** 327 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che uniscono o dividono parole»
- **Si chiama anche** lucchetto a specchio, lucchetto rovesciato, XZz / zZY = XY, chiave riflessa
- **In una riga** lo stesso, con una delle due letta al contrario.
- **Contratto** voce breve
- **Fonti** `it-lucchetto.txt`, `it-biscarto.txt`, `it-bifronte-vero.txt`, prese il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Un lucchetto in cui la chiave, nella seconda parola, è scritta al rovescio. `it-lucchetto.txt` lo scrive **XZz / zZY = XY** e porta *spia / aiola = spola*: in fondo alla prima c'è *ia*, in testa alla seconda c'è *ai*, e sparisce da tutte e due.

La differenza dalla voce 326, lucchetto: là la chiave si trova cercando dove le due parole combaciano; qui bisogna prima girare le lettere. La differenza dalla voce 323, sciarada, che è il termine di paragone del blocco: là le due parole si accostano e basta, qui si sovrappongono su un pezzo comune che sparisce da tutte e due e che nella seconda va letto al contrario.

Parti mobili: quanto è lunga la chiave, e se il gioco dichiara che è riflessa oppure lascia scoprire anche quello.

## Da dove viene

`it-lucchetto.txt`, presa il 1 settembre 2026, lo dà come «un tipo particolare di lucchetto» e non gli assegna né una data né un autore proprio: eredita quelli del lucchetto, teorizzato nel 1950 da Pietro Mercatanti, che firmava Carminetta.

Sta quindi in una famiglia con una genealogia scritta — lucchetto 1950, cerniera 1955, biscarto 1963, doppia estrazione 1973, cernita 1975 (`it-biscarto.txt`) — e ne è l'unico membro che non compare in quell'elenco di date, perché non è un gioco nuovo ma una variante di lettura.

## Varianti e parenti

- **Lucchetto** (326) — la stessa cosa con la chiave dritta, e la voce dove sta la famiglia per intero.
- **Sciarada** (323) — le due parole si accostano e non sparisce niente.
- **Bifronte** (333) — l'altra forma del capitolo che chiede di leggere al contrario, ma là si rovescia la parola intera e non un pezzo (`it-bifronte-vero.txt`).
- **Cerniera** (329) — un altro modo di girare il lucchetto: invece di rovesciare le lettere, si scambia da che parte stanno.
- **Lucchetto riflesso multiplo** — la fonte ammette lucchetti a più di tre parti, e la riflessione si può applicare a ognuno degli agganci.

## Che cosa se ne sa

Questa forma ha una proprietà che il lucchetto semplice non ha, e non è una statistica: si dimostra in una riga.

**La chiave di una lettera sola è sempre valida.** Se le ultime *k* lettere della prima parola, lette al rovescio, sono le prime *k* della seconda, allora in particolare l'ultima lettera della prima è la prima della seconda — perché è il carattere che sta in testa a tutte e due queste sequenze. Quindi ogni volta che esiste una chiave lunga due o più, esiste anche quella di una lettera. **La chiave riflessa non è mai unica.**

Controllato su tutte le coppie di stringhe fino a quattro lettere su un alfabeto di tre: 1 296 coppie hanno una chiave lunga almeno due, e nessuna di queste è senza la chiave corta (`build/check_323.py`). Vale anche per i due esempi della fonte: *spia / aiola* ammette *ia* e *a*, *torre / erba* ammette *re* e *e*, e nei due casi corti viene *spiiola* e *torrrba*.

Per il lucchetto semplice la stessa cosa è falsa, e il controesempio si trova subito: la coppia *aab / aba* ha la chiave *ab* e nessuna chiave di una lettera. Sulle cinque coppie della scheda della voce 326, lucchetto la chiave è unica in tutti e cinque i casi.

Ne segue la sola differenza pratica fra le due forme. **Il lucchetto semplice si risolve leggendo; il riflesso si risolve leggendo e poi scegliendo**, perché la regola meccanica dà sempre almeno due risposte e solo una dà una parola. La verifica del lucchetto sta nel materiale; quella del riflesso torna in un **vocabolario**, come per il resto del capitolo 12.

## Esempi trovati

Da `it-lucchetto.txt`, riscritti: *spia / aiola = spola*; *torre / erba = torba*.

La fonte non ne dà altri, e non dà nessuna misura: `it-lucchetto.txt` è una pagina di poco meno di tre kilobyte che descrive il lucchetto e nomina la variante riflessa in una frase.

## Una nostra versione

> **La chiave, ma allo specchio**
>
> Come il lucchetto della scheda prima, con una differenza: quello che c'è in fondo alla prima parola nella seconda è **scritto al contrario**. Trovalo, buttalo via da tutte e due, attacca quello che resta.
>
> ```
>  PRIMA  SECONDA  LA CHIAVE  IL TOTALE
>  cono   onda     ─────────  ─────────
>  viso   oste     ─────────  ─────────
>  porta  atto     ─────────  ─────────
>  sera   arte     ─────────  ─────────
>  pasta  atto     ─────────  ─────────
> ```
>
> Finito? Adesso guarda una cosa. In tutte e cinque le righe **funziona anche una chiave di una lettera sola** — l'ultima della prima parola è la prima della seconda. Provaci: vengono fuori cinque mostri come *connda*.
>
> Non è un caso ed è dimostrabile in una riga. Scrivi qui perché una chiave di due lettere ne porta sempre con sé una di una:
>
> ```
>  ────────────────────────────────────────────────
> ```

Le cinque righe si risolvono guardando, e la chiave giusta è quella che dà una parola: qui il vocabolario serve, e nella scheda della voce 326, lucchetto no. La differenza è piccola da leggere e grossa da progettare.

La seconda domanda non chiede una parola ma una dimostrazione, e la dimostrazione è alla portata di chi legge: se giro due lettere, la prima delle due girate è quella che stava in fondo. Chi la scrive la può provare su qualunque coppia, il che la rende l'unica parte della scheda che si verifichi da sola.

Dove si romperebbe: il sistema non sa manipolare le lettere dentro le parole (`ideas/10 §6`), quindi non può costruire le cinque coppie. Le abbiamo cercate a mano e verificate con uno script.

## Da riprendere alla rassegna

**Una variante può togliere il controllo dell'errore che la forma di partenza aveva.** Il lucchetto della voce 326, lucchetto si verifica nel materiale; rovesciare la chiave lo riporta nel vocabolario, e per una ragione strutturale — la chiave corta è sempre disponibile. Alla rassegna: quando una forma sta nel formato, le sue varianti non ci stanno per eredità, e vanno guardate una per una.

**Una proprietà negativa dimostrabile in una riga vale come consegna.** «La chiave di una lettera funziona sempre, e non serve a niente» è un fatto vero, breve, e chi lo capisce ha capito la forma. È la terza volta nel capitolo che una domanda su una regola batte una domanda su una parola, dopo la voce 316, cambio di lettera e la voce 321, antipodo.

**La riga di differenza.** Rispetto alla voce 323, sciarada, dove le due parole si accostano e basta: qui si sovrappongono su un pezzo comune che sparisce da tutte e due, e che nella seconda parola è scritto al rovescio.

