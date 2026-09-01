# Monoverbo

- **Numero** 336 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che lavorano sul senso»
- **Si chiama anche** crittografia a monoverbo, crittografia in una parola, one-word cryptic
- **In una riga** una definizione che si risolve con una parola sola, di solito con un doppio senso.
- **Contratto** voce breve
- **Fonti** `it-crittografia-gioco.txt`, `it-gioco-enigmistico.txt`, `it-enigmistica.txt`, prese il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

**La glossa dell'elenco descrive un'altra cosa.** Il monoverbo non è una definizione: è una **crittografia**, cioè il gioco in cui si guarda un esposto — un gruppo di lettere disposte in un certo modo — lo si dice a parole, e poi si rimettono gli spazi in un altro posto. `it-crittografia-gioco.txt`, presa il 1 settembre 2026, lo dà come un caso e non come un genere: «il solutore deve infatti scoprire una parola (in tal caso si parla più propriamente di monoverbo) o una frase di senso compiuto». **Monoverbo è il nome della crittografia quando la soluzione sta in una parola sola.**

Il gioco ha tre stati, e il salto interessante è fra il secondo e il terzo:

```
 quello che vedi    IN scritto sopra FFICIENTE
 quello che leggi   IN su FFICIENTE
 il diagramma       2 2 9 = 13
 quello che scrivi  .............
```

Parti mobili:

- **L'esposto.** Le lettere e la loro disposizione. Non devono formare parole: *FFICIENTE* non è niente, e va benissimo.
- **La prima lettura.** La frase con cui si descrive quello che si vede. Qui è la sola parte che chiede di interpretare.
- **Il diagramma.** Le lunghezze delle due letture, scritte tutte e due. È la parte che rende il gioco controllabile.
- **La seconda lettura.** Le stesse lettere nello stesso ordine, con gli spazi altrove. Nel monoverbo gli spazi spariscono del tutto.

## Da dove viene

Le prime crittografie italiane compaiono nel 1877, firmate da Pio Alberto Visoni sulla rivista torinese *La gara degli indovini* e sul piacentino *L'aguzzaingegno*, dove furono presentate col nome di **rebus dell'avvenire** (`it-enigmistica.txt`, presa il 1 settembre 2026). Il nome che è rimasto è più tardo.

Il termine *monoverbo* non ha una voce sua da nessuna parte: su Wikipedia in italiano rimanda a *Crittografia (enigmistica)*, controllato il 1 settembre 2026 con `build/check_titoli_335.py`. È coerente con quello che dicono le fonti: non è un gioco, è una taglia.

## Varianti e parenti

- **Crittografia pura** (voce 341, crittografia pura) — la stessa cosa quando l'esposto è fatto solo di segni e la prima lettura ne descrive la forma.
- **Crittografia perifrastica** (voce 342, crittografia perifrastica) — la stessa cosa quando la prima lettura passa per un giro di parole.
- **Crittografia mnemonica, o frase bisenso** — la parente che ha perso il meccanismo: si interpreta soltanto, e le lettere non si conservano.
- **Crittografia a frase** — il caso opposto al monoverbo: la soluzione è una frase, e la doppia lettura è, dice la fonte, «perfetta», perché non c'è nessuna lettera interposta.
- **Bisenso** (voce 335, bisenso) — la materia con cui è fatta la prima lettura.
- **Cambio di spaziatura** (voce 345, cambio di spaziatura) — il meccanismo del monoverbo, isolato e senza la parte da interpretare.
- **Cruciverba crittico** (voce 126, cruciverba crittico) — il parente inglese; la sua definizione singola è la cosa più vicina al monoverbo fuori d'Italia.

## Che cosa se ne sa

**Il monoverbo conserva le lettere, e questo è il suo controllo dell'errore.** Fra la prima e la seconda lettura non si aggiunge e non si toglie niente: cambia solo dove cadono gli spazi. Verificato in `build/check_335.py` su quattro casi, spogliando le due letture di spazi, accenti e apostrofi e confrontando le stringhe nude:

- `RI sotto AL su GO` = *risotto al sugo*, diagramma 2 5 2 2 2 = 7 2 4, tredici lettere per parte (`it-crittografia-gioco.txt`);
- `Dov'ero saprassi` = *doverosa prassi*, 6 8 = 8 6, quattordici lettere (stessa fonte);
- `RI sotto` = *risotto*, 2 5 = 7, sette lettere — è la prima ridotta da noi al caso monoverbo;
- `IN su FFICIENTE` = *insufficiente*, 2 2 9 = 13, ed è nostra.

**Ne segue la cosa che distingue questa voce da tutte le altre della sezione 12.3: qui la verifica sta nel materiale.** Chi risponde può contare le lettere della sua soluzione e confrontarle con il diagramma, e se il conto non torna la risposta è sbagliata senza che nessuno debba dirglielo. È lo stesso meccanismo dell'invariante trovato alla voce 331, anagramma, e in tutta la sezione «Giochi che lavorano sul senso» è l'unico caso.

**La stessa fonte dice dove l'invariante si rompe, e lo dice per un'altra forma.** La crittografia mnemonica tollera le equipollenze «almeno fra articoli, preposizioni, preposizioni articolate nelle due letture»: cioè ammette che le lettere non siano esattamente le stesse. La crittografia a frase non le tollera. È per questo che `it-gioco-enigmistico.txt` mette la frase bisenso fra le crittografie «solo per convenzione; in realtà non si tratta di una crittografia»: **quello che manca alla mnemonica non è la difficoltà, è il conto.** Controprova, in `build/check_335.py`: il canonico `A B C` = *alfabeto muto* non conserva le lettere, e infatti non è una crittografia meccanica.

**Perché il diagramma esiste qui e non nell'indovinello.** `it-indovinello.txt` spiega che l'indovinello non ha diagramma perché, senza uno schema che leghi le parole, un sinonimo della soluzione sarebbe altrettanto esatto. Nella crittografia lo schema c'è, la lunghezza è determinata, e il diagramma si può scrivere. **Il diagramma non è una gentilezza verso chi risolve: è la prova che la risposta è una sola.**

## Esempi trovati

Da `it-crittografia-gioco.txt`, con la sua spiegazione: l'esposto in cui *RI* sta sotto, *AL* sta su *GO*; si legge «RI sotto AL su GO» e si riscrive *risotto al sugo*. Il diagramma dichiarato dalla fonte è (2 5 2 2 2) = (7 2 4), e la fonte lo scrive a sinistra e a destra di un segno di uguale.

Dalla stessa pagina, una mnemonica: *Dov'ero saprassi* = *doverosa prassi*, dove la prima lettura non descrive dei segni ma interpreta un concetto — se mi scoprono si saprà dov'ero.

Le crittografie a monoverbo vere non compaiono con quel nome in nessuna delle pagine prese: le fonti nominano la categoria e non ne danno esempi. Lo si dichiara invece di girarci intorno.

## Una nostra versione

> **Quello che vedi non è quello che c'è scritto**
>
> C'è un gioco italiano vecchio di centocinquant'anni che funziona così. Ti danno delle lettere messe in un certo modo. Tu **dici a voce quello che vedi**, e poi riscrivi la stessa identica sequenza di lettere spostando gli spazi.
>
> Questo è già risolto, per farti vedere il meccanismo:
>
> ```
>       RI
>  ─────────────    si legge  «RI sotto»    si riscrive  risotto
> ```
>
> Adesso tocca a te. Le lettere sono queste, e stanno una sopra l'altra:
>
> ```
>       IN
>  ─────────────
>   FFICIENTE
> ```
>
> ```
>  quello che leggi   ......................    2 2 9
>  quello che scrivi  .............             13
> ```
>
> **Come sai di aver ragione:** conta le lettere. Devono essere tredici prima e tredici dopo. Se non sono tredici, non è la risposta — e non c'entra quanto ti sembra bella.

Il riquadro risolto in cima è la parte che fa funzionare la scheda: il gioco è opaco finché non se ne è visto uno, e trasparente subito dopo. L'ultima riga è il controllo dell'errore, e sta tutto sul foglio.

**Dove si romperebbe.** Sul pannello da quattro righe l'esposto non ci sta: la disposizione delle lettere è metà del gioco, e su una riga sola sparisce. Il sistema non può costruire un monoverbo nuovo, perché servirebbe contare le lettere di una parola e verificare la spartizione — le due cose che sbaglia (`ideas/10 §6`). Può invece stampare quelli già fatti, e può leggere una risposta e dire se ha tredici lettere.

## Da riprendere alla rassegna

**Questa voce differisce dalla voce 335, bisenso perché al bisenso il doppio senso sta dentro una parola sola, e qui sta in una frase breve che descrive un disegno.** È il secondo valore della variabile della sezione: quanta parte del testo deve reggere due letture insieme.

**È l'unica voce del blocco in cui la verifica sta nel materiale, e la ragione è una legge di conservazione.** Il diagramma è la traccia scritta dell'invariante. Alla rassegna vale la pena cercare nelle altre forme dell'elenco quali abbiano una grandezza conservata da stampare accanto alla consegna: è il modo più economico di dare un controllo dell'errore a un compito che non ha una risposta stampata.

**Una glossa sbagliata trovata nel capitolo, e non è la prima.** La riga dell'elenco chiama il monoverbo «una definizione», il che lo confonde con la definizione di un cruciverba crittico. La stessa confusione era già finita dentro la voce 126, cruciverba crittico, ed è stata corretta scrivendo questa.
