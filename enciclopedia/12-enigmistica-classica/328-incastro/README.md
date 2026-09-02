# Incastro

- **Numero** 328 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che uniscono o dividono parole»
- **Si chiama anche** parola incastrata, sciarada mista, innesto, parola avvinta, incastro doppio, incastro con due cuori, XX / Y = XYX
- **In una riga** una parola si infila dentro un'altra: *pane* dentro *ora* dà *panora*.
- **Fonti** [Incastro (enigmistica)](https://it.wikipedia.org/wiki/Incastro_(enigmistica)) e [Sciarada](https://it.wikipedia.org/wiki/Sciarada), prese il 30 agosto 2026; [Intarsio (enigmistica)](https://it.wikipedia.org/wiki/Intarsio_(enigmistica)) e [Riffle shuffle permutation](https://en.wikipedia.org/wiki/Riffle_shuffle_permutation), prese il 1 settembre 2026

## Che cos'è

Si taglia in due la prima parola e ci si mette dentro la seconda, intera. «Incastro (enigmistica)» la scrive **XX / Y = XYX**: *cane* tagliata in *ca* e *ne*, *micio* in mezzo, e viene *camicione*.

È il **valore più povero** della variabile di questo blocco, che è *quanta libertà ha l'ordine delle lettere nel totale.* Qui la seconda parola resta tutta insieme e i punti in cui le due si toccano sono due, il minimo possibile sopra la sciarada. Le voci 330, 331 e 332 aumentano quella libertà, e ognuna si descrive in una riga di differenza da qui.

Parti mobili: dove cade il taglio nella prima parola; quante parole si infilano (una, due); se il risultato è una parola sola o una frase.

La glossa dell'elenco non funziona. Con *pane* e *ora* gli incastri possibili sono cinque — *opanera*, *orpanea*, *panorae*, *paorane*, *poraane* — e *panora* non è fra questi: ha sei lettere invece delle sette della coppia, cioè per strada ne perde una, e un incastro non perde niente. Verificato.

## Da dove viene

«Incastro (enigmistica)», presa il 30 agosto 2026, dà una data e un nome: le prime combinazioni si devono al **Tarlo, nel 1879**, e si chiamavano *parole incastrate*. Prima del nome attuale il gioco ne ebbe altri tre — *sciarada mista*, *innesto*, *parola avvinta* — e la sequenza dei nomi dice che per un pezzo l'incastro fu visto come una variante della sciarada e non come una forma sua.

La stessa pagina distingue due modi di infilarne due invece di una, e li distingue con una formula per ciascuno. **XX / Y / Z = XYZX** mette le due parole nello stesso buco, e si chiama *incastro con due cuori*: *mosca / trafila / teli = mostra filatelica*. **XX / YY / Z = XYZYX** le annida una dentro l'altra: *cantica / risa / talleri = cristalleria antica*, dove *risa* è a sua volta spezzata attorno a *talleri*.

La pagina chiude con una riga sui nomi che vale come avvertimento: «generalmente non si parla di incastro a frase, ma il nome esiste accanto a quello, diverso, di frase a incastro». La voce `Frase_a_incastro` su Wikipedia in italiano **non esiste**, controllato il 1 settembre 2026: il secondo dei due nomi non ha una pagina, e qui non se ne dice altro.

## Varianti e parenti

- **Incastro doppio** — due parole dentro la prima, annidate: XX / YY / Z = XYZYX.
- **Incastro con due cuori** — due parole dentro la prima, di seguito: XX / Y / Z = XYZX.
- **Incastro a frase** — il totale è una frase e non una parola: *casco / adagio = casa da gioco*.
- **Sciarada** (323) — le due parole si accostano e basta: un solo punto di contatto invece di due.
- **Intarsio (tarsia)** (330) — la seconda parola entra spezzata invece che intera. È la differenza che «Intarsio (enigmistica)» usa per definire l'intarsio.
- **Sciarada alterna** (324) — le due parole si intrecciano a blocchi regolari, senza il vincolo su capo e coda.
- **Anagramma** (331) — le lettere si riordinano liberamente, e l'ordine di partenza sparisce.
- **Composizione** — la lingua fa la sciarada da sé, ma non fa l'incastro: nessuna parola italiana nasce infilando un lessema dentro un altro tagliato a metà. È un'osservazione nostra, e va verificata.

## Che cosa se ne sa

«Incastro (enigmistica)» è breve — 2 181 byte — e non contiene nessuna misura: dà la formula, la data e gli esempi.

Il conto si fa da qui, e mostra una cosa che le fonti non dicono. Prendiamo un totale di otto lettere e chiamiamo *prima parola* quella che possiede la prima lettera. Ogni modo di dividere le otto lettere fra le due parole è una stringa di otto scelte, e sono 2⁷ − 1 = **127**. Il numero di **giunzioni** — i punti in cui una lettera di una parola è seguita da una lettera dell'altra — classifica queste 127 spartizioni, e ogni classe ha già un nome nell'enigmistica italiana:

| giunzioni | quante | formula | come si chiama |
| --- | --- | --- | --- |
| 1 | 7 | C(7,1) | sciarada |
| 2 | 21 | C(7,2) | incastro |
| 3 | 35 | C(7,3) | sciarada alterna |
| 4 | 35 | C(7,4) | intarsio |
| 5 | 21 | C(7,5) | sciarada alterna |
| 6 | 7 | C(7,6) | intarsio |
| 7 | 1 | C(7,7) | sciarada alterna |

Sommando: sciarada 7, incastro 21, intarsio 42, sciarada alterna 57, e 7 + 21 + 42 + 57 = 127. Verificato per formula binomiale e enumerando tutte le 128 stringhe. **I quattro giochi sono le quattro classi di una sola partizione**, e le pagine che li descrivono non lo dicono mai: ognuna definisce il suo per differenza dalla precedente.

L'incastro sta nella casella con due giunzioni, e ne segue lo spazio di ricerca. Partendo dal totale di otto lettere, le letture possibili sono le **21** della tabella: si scelgono due tagli fra i sette disponibili. Partendo invece dalle due parole, le letture sono i tagli della prima soltanto — su una parola di quattro lettere, **tre**. Il gioco è quasi immediato in un verso e quasi immediato anche nell'altro, ed è il solo di questa sezione di cui si possa dire.

La verifica sta in un **vocabolario**, come per quasi tutto il capitolo 12: la parte meccanica si controlla contando le lettere, ma il giudizio «queste due sono parole» resta fuori.

## Esempi trovati

Da «Incastro (enigmistica)», riscritti: *cane / micio = camicione*; e in versione a frase *casco / adagio = casa da gioco*, dove le undici lettere della coppia sono le stesse undici del totale.

Dalla stessa pagina, i due modi di infilarne due: *mosca / trafila / teli = mostra filatelica* e *cantica / risa / talleri = cristalleria antica*.

## Un esempio giocabile

> **Ventun modi di tagliare, e uno solo dà due parole**
>
> POMODORO ha otto lettere. Se la tagli in tre pezzi — un pezzo, poi un altro, poi un altro ancora — e butti via quello di mezzo, ti resta la parola di fuori. Il pezzo di mezzo è la parola di dentro.
>
> I modi di tagliarla in tre sono **ventuno**, e sono tutti qui. Non ce n'è un ventiduesimo.
>
> ```
>   1  p|o|modoro   2  p|om|odoro   3  p|omo|doro
>   4  p|omod|oro   5  p|omodo|ro   6  p|omodor|o
>   7  po|m|odoro   8  po|mo|doro   9  po|mod|oro
>  10  po|modo|ro  11  po|modor|o  12  pom|o|doro
>  13  pom|od|oro  14  pom|odo|ro  15  pom|odor|o
>  16  pomo|d|oro  17  pomo|do|ro  18  pomo|dor|o
>  19  pomod|o|ro  20  pomod|or|o  21  pomodo|r|o
> ```
>
> Uno solo dei ventuno lascia **due parole italiane**. Scrivi il numero: ────
>
> Adesso senza l'elenco. Sono quattro, e funzionano tutti nello stesso modo: la parola di fuori è di quattro lettere, tagliata nel mezzo.
>
> ```
>  IL TOTALE  LA PRIMA  LA SECONDA
>  calamaro   ────────  ──────────
>  vaporoso   ────────  ──────────
>  lacerato   ────────  ──────────
>  arrivato   ────────  ──────────
> ```

Le ventun righe sono **lo spazio di ricerca per intero**, e ci stanno su sette. È la stessa mossa della voce 323, sciarada, dove le righe erano otto: lì si sceglieva un punto, qui se ne scelgono due, e il numero passa da *n* − 1 a C(*n* − 1, 2). La seconda parte è la stessa domanda senza l'elenco, e serve a far vedere che l'elenco non era un aiuto qualsiasi.

Il limite tecnico del capitolo — un modello linguistico non sa manipolare le lettere dentro le parole — non morde: si chiede di stampare ventun stringhe che si ricavano tagliando una parola in tutti i modi, non di giudicarle. Il giudizio «questa è una parola italiana» resta a una persona o a un vocabolario, e in casa un vocabolario non è garantito.

## Che cosa la rende interessante

**Il termine di paragone di questo blocco.** Le quattro forme che stanno sulla stessa variabile — questa scheda, la voce 330, intarsio (tarsia), la voce 331, anagramma e la voce 332, anagramma a frase — differiscono in una cosa sola: **quanta libertà ha l'ordine delle lettere nel totale.** Qui è al minimo: due giunzioni, e la seconda parola tutta intera. Le altre tre ne aggiungono, e ognuna porta la sua riga di differenza. La voce 329, cerniera sta nello stesso blocco ma non su questa variabile.

**Quattro giochi, una sola partizione, e nessuno la disegna.** Sciarada, incastro, intarsio e sciarada alterna sono le classi delle 127 spartizioni di un totale di otto lettere, indicizzate dal numero di giunzioni. È la seconda struttura nascosta trovata in questa sezione, dopo la griglia dei quattro biscarti della voce 326, lucchetto, e tutte e due sono venute fuori mettendo in fila le formule che le pagine danno una per una.

**Un gioco può essere facile nei due versi, ed è raro.** Dal totale 21 letture, dalle due parole 3: l'incastro non ha un verso difficile. Vale la pena chiedersi se una forma senza verso difficile sia ancora un enigma, o soltanto un esercizio di lettura.

**La glossa dell'elenco è sbagliata di nuovo**, e questa volta per una ragione che si vede contando: l'esempio perde una lettera, e l'incastro non ne perde nessuna.
