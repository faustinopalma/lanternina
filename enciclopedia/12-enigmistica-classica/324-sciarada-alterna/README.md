# Sciarada alterna

- **Numero** 324 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che uniscono o dividono parole»
- **Si chiama anche** lettura alterna, sciarada intrecciata, intreccio, XX / YY = XYXY, *riffle*, mescolata a una mano
- **In una riga** le lettere delle due parole si alternano.
- **Fonti** [Sciarada](https://it.wikipedia.org/wiki/Sciarada), [Intarsio (enigmistica)](https://it.wikipedia.org/wiki/Intarsio_(enigmistica)), [Riffle shuffle permutation](https://en.wikipedia.org/wiki/Riffle_shuffle_permutation), prese il 1 settembre 2026

## Che cos'è

Le due parole non si accostano: si intrecciano. «Sciarada» la scrive **XX / YY = XYXY** e porta *cane / pira = capinera* — i pezzi sono *ca, pi, ne, ra*, e si prendono a due lettere per volta, prima dalla prima parola e poi dalla seconda.

La differenza dalla voce 323, sciarada: **là il punto di contatto è uno, qui sono tanti.** Tutte le lettere sopravvivono e restano nel loro ordine dentro la parola di provenienza; quello che cambia è che si alternano invece di stare in fila.

La fonte precisa che il nome è improprio: la sciarada alterna «è un tipico esempio di lettura alterna, assimilabile all'incastro e all'intarsio», e non è una sciarada. La glossa dell'elenco dice «le lettere si alternano», ed è imprecisa nello stesso punto: **si alternano i blocchi, non le lettere singole**, e nell'esempio della fonte i blocchi sono di due.

Parti mobili: la grandezza dei blocchi, se è dichiarata o no, e chi comincia.

## Da dove viene

«Sciarada», presa il 1 settembre 2026, la classifica fra le forme che «a dispetto del nome, non sono vere e proprie sciarade», e non le dà né una data né un inventore — a differenza di quasi tutte le altre voci di questo capitolo, dove l'enigmistica italiana registra l'anno e lo pseudonimo. Il nome è dunque ereditato dalla sciarada per somiglianza di superficie, e la fonte lo dichiara.

La stessa fonte aggiunge che nell'enigmistica moderna la sciarada alterna si può svolgere a diagramma o a enigmi collegati, cioè che il gioco resta lo stesso e cambia il modo di presentarlo: nel primo caso si scrive quanto sono lunghe le parti, nel secondo ogni parte ha il suo indovinello.

## Varianti e parenti

- **Sciarada** (323) — il caso in cui non si intreccia niente, e il termine di paragone di questo blocco.
- **Intarsio (tarsia)** (330) — la stessa famiglia delle letture alterne, con un vincolo in più: «Intarsio (enigmistica)» chiede che il capo e la coda della prima parola restino agli estremi del totale. Nella sciarada alterna il totale comincia con la prima parola e finisce con la seconda; nell'intarsio comincia e finisce con la prima.
- **Incastro** (328) — la seconda parola entra intera, senza essere spezzata.
- **Sciarada incatenata** (325) — le due parole si sovrappongono invece di intrecciarsi.
- **Mescolata a una mano** — fuori dall'enigmistica, la stessa operazione fatta con un mazzo di carte.

## Che cosa se ne sa

Il conto è la cosa che questa forma ha e le altre no, ed è grande. Partendo dal totale, ogni lettera può venire dalla prima o dalla seconda parola: le assegnazioni sono 2ⁿ, e togliendo le due che lasciano una parola vuota restano **2ⁿ − 2**. Su una parola di otto lettere sono 254, contro i 7 tagli di una sciarada: **trentasei volte tanto.** Calcolato per formula e per enumerazione completa.

L'operazione ha un nome fuori dall'enigmistica. «Riffle shuffle permutation», presa il 1 settembre 2026, chiama *riffle shuffle permutation* l'ordine che si ottiene intrecciando due mazzi in un colpo solo, e dà il numero di quelle distinte su *n* carte: **2ⁿ − n**, cioè 1, 2, 5, 12, 27, 58, 121, 248 (successione A000325). Su otto lettere sono 248, e su un mazzo da 52 la pagina dà 4 503 599 627 370 444.

I due numeri non coincidono, e la differenza dice una cosa sulle due voci. Le 254 assegnazioni danno 248 intrecci diversi perché **le nove che non intrecciano niente danno tutte lo stesso risultato**, cioè la parola intatta: sette di quelle nove sono esattamente i tagli della sciarada. Il conto torna, 254 − 7 + 1 = 248, ed è verificato enumerando tutte le 256 assegnazioni. Ne segue che **la sciarada è il caso degenere della sciarada alterna**, e non due forme accostate per comodità di elenco.

La verifica sta in un **vocabolario**, come per tutto il capitolo. Ma quando i blocchi sono dichiarati la lettura diventa meccanica, e allora il vocabolario serve solo a confermare, non a cercare.

## Esempi trovati

Da «Sciarada», riscritto: *cane / pira = capinera*, con i blocchi di due.

Da «Intarsio (enigmistica)», per confronto e non come esempio di questa voce: *asine / censo = ascensione* è un intarsio, perché comincia con *as* e finisce con *ne*, cioè con capo e coda della prima parola.

## Un esempio giocabile

> **Due parole intrecciate, due lettere per volta**
>
> CAMERATA è fatta di due parole, ma non una dopo l'altra: a turno, due lettere ciascuna. I numeri dicono da dove viene ogni pezzo.
>
> ```
>  c a   m e   r a   t a
>   1     2     1     2
>
>  la parola  1 :  ─ ─ ─ ─
>  la parola  2 :  ─ ─ ─ ─
> ```
>
> Fatto? Adesso il numero che rende la cosa meno facile di come sembra. **Senza la regola dei due, i modi di dividere in due le otto lettere di CAMERATA sono 254.** Con la regola ce n'è uno solo, ed è quello che hai appena letto.
>
> Prova a costruirne una tu: scegli due parole di quattro lettere e intrecciale. Su dieci tentativi te ne verrà bene forse uno, e questo è il motivo per cui i giochi di questo tipo li scrive chi ha pazienza.

I numeri sotto i blocchi sono il controllo dell'errore messo nel materiale: chi legge male se ne accorge perché una delle due righe non si riempie. Il 254 non è ornamento — dice quanto costa la regola che è appena stata data, ed è la sola cosa del foglio che chi legge non può ricavarsi.

Dove si romperebbe: la seconda parte chiede di giudicare se una stringa sia una parola, e quel giudizio sta in un vocabolario, che in casa non è garantito. La bassa resa è dichiarata prima, così che il fallimento sia previsto.

## Che cosa la rende interessante

**La sciarada è il caso degenere della sciarada alterna, e il conto lo dimostra.** 254 assegnazioni, 248 intrecci distinti, e la differenza sono i 7 tagli della sciarada che collassano su un risultato solo. È la prima volta nell'enciclopedia che due forme vicine si scoprono legate da un'identità aritmetica invece che da una somiglianza descrittiva. Vale la pena chiedersi quante altre coppie stiano così.

**Un numero grande stampato accanto a una regola misura la regola, non il gioco.** Qui il 254 dice quanto vincolo porta la frase «due lettere per volta», e chi legge lo capisce senza sapere niente di combinatoria. Da riusare ovunque una consegna restringa lo spazio: è il modo più economico di far vedere che una regola aiuta.

**La riga di differenza.** Rispetto alla voce 323, sciarada, dove le due parole si accostano e basta: qui le due parole si intrecciano a blocchi, e il punto di contatto non è uno ma tanti.

