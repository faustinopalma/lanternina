# Enigma in versi

- **Numero** 338 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che lavorano sul senso»
- **Si chiama anche** enigma, enimma, gioco poetico, indovinello lungo, verse riddle
- **In una riga** l'indovinello lungo, spesso in due parti, in cui la lettura di superficie racconta una scena intera.
- **Contratto** voce breve
- **Fonti** `it-gioco-enigmistico.txt`, `it-indovinello.txt`, `it-enigmistica.txt`, `exeter-book-riddles.txt`, prese il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Un componimento in versi che descrive una cosa senza nominarla, tenendo insieme due letture: quella apparente, che racconta una scena che sta in piedi da sola, e quella reale, che è la soluzione. Fin qui è la voce 337, indovinello in versi. Quello che cambia è **il tono e la misura**: l'enigma è serio e poetico dove l'indovinello è spiritoso e leggero, ed è lungo dove quello è breve.

**Le due fonti che abbiamo in casa non concordano, e la divergenza va dichiarata:**

```
                     it-gioco-enigmistico  it-indovinello
 indovinello         gioco breve           la stessa cosa
 enigma              gioco poetico         la stessa cosa
 che cosa li separa  il tono e la misura   niente
```

`it-indovinello.txt` apre con «l'indovinello o enigma e, meno comunemente, enimma», cioè li dà per sinonimi; e su Wikipedia in italiano *Enigma (enigmistica)* rimanda proprio a *Indovinello* — verificato il 1 settembre 2026 con `build/check_titoli_335.py`. `it-gioco-enigmistico.txt` invece li separa: «in un'accezione ancora più stretta, è enigma soltanto quel gioco affine all'indovinello, ma che se ne differenzia per il carattere serio e poetico anziché spiritoso e leggero», e nella sua classificazione mette l'indovinello fra i **giochi brevi o epigrammatici** e l'enigma fra i **giochi poetici**.

**Si tiene la seconda,** perché è quella che produce una classificazione e la si può controllare contando i versi; la prima è un'osservazione sull'uso corrente della parola, e le due cose non sono in contraddizione — la seconda dice «in un'accezione più stretta».

**La glossa dell'elenco è vera a metà.** «L'indovinello lungo» regge; «spesso in due parti» non compare in nessuna delle tre fonti prese, e nessuna descrive l'enigma come bipartito. Quello che le fonti chiamano gioco a due parti è un'altra cosa: il gioco a **enigmi collegati**, dove più indovinelli giustapposti definiscono le parti di una combinazione — cioè una sciarada esposta in versi, non un enigma.

## Da dove viene

È la forma con cui l'enigmistica italiana esce dalla tradizione orale ed entra nella letteratura, fra il Cinquecento e il Settecento. Da `it-enigmistica.txt`, presa il 1 settembre 2026: la prima raccolta italiana è del **1538**, i *Sonetti giocosi da interpretare* del maniscalco senese Angiolo Cenni, detto il Resoluto; Straparola chiude con un enigma quasi ogni novella delle *Piacevoli notti* (1550, ampliate nel 1553); Giulio Cesare Croce, quello di *Bertoldo*, pubblica a Bologna cento enigmi nel 1594 e altri cento nel 1601.

La data che conta per tutta la sezione 12.3 è però un'altra. Nel **1689** escono a Venezia gli *Enimmi* di Caton l'Uticense — pseudonimo di Leone Santucci, canonico a Lucca — centoquarantadue enigmi in cui, dice la fonte, «per la prima volta si comincia a vedere utilizzata la dilogia, vale a dire l'uso della stessa parola con due significati distinti, uno poetico e l'altro relativo alla soluzione». **La dilogia è il bisenso, e questa è la sua prima comparsa datata.** Prima di allora l'enigma descriveva l'oggetto direttamente, con parole scelte per sviare: «non c'era insomma la differenza tra il senso apparente e quello reale».

## Varianti e parenti

- **Indovinello in versi** (voce 337, indovinello in versi) — lo stesso meccanismo in tono leggero e in pochi versi.
- **Bisenso** (voce 335, bisenso) — la materia; nell'enigma si chiama dilogia.
- **Poesia enigmatica** (voce 339, poesia enigmatica) — l'enigma a cui si toglie la consegna.
- **Giochi a enigmi collegati** — più enigmi giustapposti che definiscono le parti di una sciarada; è il gioco che la glossa descrive credendo di descrivere questo.
- **Colibrì, ibis, marabù** — le tre varianti in verso libero inventate da Guido Iazzetta, nominate per grandezza crescente e descritte in `it-indovinello.txt`.
- **Indovinello classico (enigma)** (voce 110, indovinello classico (enigma)) — **il confine da dichiarare**: lì la forma come genere internazionale, con i corpora latini, anglosassoni e norreni; qui il gioco codificato dell'enigmistica italiana, con le sue regole di gara.

## Che cosa se ne sa

**La differenza fra le due forme si misura contando i versi, ed è un fattore quattro.** I componimenti che `it-enigmistica.txt` riporta per esteso: l'indovinello di Turandot sul pane sta in **un verso**, quello del Mancino sulla bussola in **due**, la sciaradina di Gastone di Foix in **uno**; l'ottava di Tommaso Stigliani sulle forbici sta in **otto**. Contati in `build/check_335.py`. Quattro componimenti non sono una misura, e questo è un ordine di grandezza dichiarato per tale: dice che la differenza è di scala e non di grado.

**Il doppio senso ha impiegato duecentotrent'anni a diventare la regola.** Dalla prima dilogia documentata, il 1689 di Caton l'Uticense, al momento in cui il metodo a doppio soggetto si afferma come sistema principale di esposizione, che `it-enigmistica.txt` colloca «solo negli anni venti». Le due date estreme sono della fonte; il conto è nostro. **Per la maggior parte della sua storia, il gioco che oggi si definisce con il doppio senso non lo aveva.**

**Un enigma non ha bisogno di essere difficile per essere lungo.** L'ottava di Stigliani sulle forbici si apre dichiarando che il soggetto è «un solo e due» e che «fa due ciò ch'era uno primamente»: la soluzione è quasi data alla prima riga, e i sei versi seguenti servono a costruire il quadro. **La lunghezza dell'enigma non serve a nascondere, serve a reggere la lettura apparente**, che con un verso solo non si può fare. È lo stesso motivo per cui, dice `exeter-book-riddles.txt`, gli indovinelli inglesi antichi sono discorsivi mentre quelli latini sono brevi e oscuri: la lunghezza compra la scena, non la difficoltà.

**Sul nostro caso.** Come per la voce 337, indovinello in versi, il limite del capitolo 12 — il sistema non sa manipolare le lettere dentro le parole — qui non morde: non c'è niente da contare. L'enigma è anzi la forma del capitolo che il sistema può generare con meno attrezzi, e la difficoltà è tutta di qualità. Il rischio specifico, che l'indovinello breve non ha: **otto versi di lettura apparente sono otto occasioni di sbavatura**, e una sola riga che non sta in piedi da sola rovina la forma senza rendere l'enigma irrisolvibile — cioè in un modo che nessun controllo automatico può prendere.

## Esempi trovati

Da `it-enigmistica.txt`, l'ottava di Tommaso Stigliani sulle forbici, in cui il soggetto parla di sé: dice di essere a un tempo uno e due, di essere adoperato da una mano con le sue cinque dita contro gli infiniti capelli che la gente ha in testa, di essere tutto bocca dalla cintura in su e di mordere più da sdentato che con i denti. Gli occhi li ha nei piedi, e nei suoi occhi ci finiscono le dita. È un enigma del Seicento e la parte che ancora funziona è l'ultima: le due immagini — gli anelli chiamati occhi, e le dita che ci entrano dentro — reggono senza sapere niente di poesia barocca.

Dalla stessa pagina, i due indovinelli brevi che fanno da contrasto: *Il corriere della sera*, di Turandot, un verso solo, dove il quotidiano di gran formato è il pane, che compare ogni giorno sulla tavola ed è fatto di grano; e *La vecchia nonna*, del Mancino, due versi, dove la nonna che lavora d'ago fino a mezzanotte per aggiustare le mutande rotte è la bussola.

Da `it-enigmistica.txt` ancora, un fatto di costume che riguarda il corpus: gli enigmi di Stigliani sono in gran parte perduti perché messi all'Indice per licenziosità, e Straparola è stato malvisto nella storia letteraria per la stessa ragione. **Una parte dell'enigmistica italiana del Cinquecento non ci è arrivata per censura, non per incuria.**

## Una nostra versione

> **La stessa cosa, detta in due modi**
>
> Scegli un oggetto. Uno solo, e non dirlo a nessuno.
>
> Adesso descrivilo due volte, senza mai nominarlo, e senza cambiare oggetto.
>
> **Prima volta — un verso solo.** Deve far ridere, o almeno sorridere. Se non ci sta in una riga, taglia.
>
> ```
>  ──────────────────────────────────────────────────────
> ```
>
> **Seconda volta — otto righe.** Qui non deve far ridere. Deve raccontare una scena vera, con un altro protagonista: qualcuno che fa qualcosa, e che non è il tuo oggetto. Chi legge deve poter capire quella scena senza sospettare niente.
>
> ```
>  ──────────────────────────────────────────────────────
>  ──────────────────────────────────────────────────────
>  ──────────────────────────────────────────────────────
>  ──────────────────────────────────────────────────────
>  ──────────────────────────────────────────────────────
>  ──────────────────────────────────────────────────────
>  ──────────────────────────────────────────────────────
>  ──────────────────────────────────────────────────────
> ```
>
> Poi rileggi le otto righe fingendo di non sapere la risposta. **Quante stanno in piedi da sole?** Segna il numero qui: ....
>
> Le due versioni sono lo stesso gioco, e in enigmistica hanno due nomi diversi: la prima è un indovinello, la seconda un enigma.

La consegna dà il nome delle due forme alla fine e non all'inizio, perché il nome non serve a fare la cosa. La domanda «quante righe stanno in piedi da sole» è il controllo dell'errore, e vale otto invece di uno: è la sola parte in cui l'enigma lungo offra un appiglio che l'indovinello breve non ha.

**Dove si romperebbe.** Otto righe da cinquantaquattro caratteri stanno su un A4 e non stanno sul pannello, che ne mostra quattro da quarantaquattro. E il conteggio finale è un giudizio di chi scrive su sé stesso, quindi non è verificabile da nessuno: qui il foglio dà un metodo, non una prova.

## Da riprendere alla rassegna

**Questa voce differisce dalla voce 335, bisenso perché al bisenso il doppio senso sta dentro una parola sola, e qui deve reggere per otto versi.** È il valore più alto della variabile del blocco fra le forme che hanno ancora una consegna.

**È l'unica voce del capitolo 12 la cui differenza specifica è un tono e non un meccanismo.** Tutte le altre quarantasette si distinguono per che cosa si fa alle lettere o alle parole; questa si distingue per come suona. Alla rassegna vale la pena chiedersi che cosa se ne faccia una raccolta che vuole essere ordinata per meccanismo.

**La lunghezza compra la scena e non la difficoltà.** È un'osservazione che vale fuori dall'enigmistica: ogni volta che una consegna si allunga, conviene chiedersi se la lunghezza stia comprando informazione o contesto. Da riusare sulle voci del capitolo 8 e del capitolo 9.

**Un corpus può mancare per censura.** Le fonti dicono che parte degli enigmi italiani del Cinquecento e Seicento è andata perduta perché indecente. Ogni volta che questa enciclopedia conta quanti esemplari di una forma ci sono arrivati, sta contando anche un filtro.
