# Anagramma

- **Numero** 331 nell'enciclopedia, capitolo 12 — Enigmistica classica, sezione «Giochi che uniscono o dividono parole»
- **Si chiama anche** anagramma semplice, trasposizione, *anagram*, *jumble*, *scramble*, parole mescolate, aptagramma, antigramma
- **In una riga** le stesse lettere in altro ordine.
- **Contratto** voce breve
- **Fonti** `it-anagramma.txt` e `anagram.txt`, prese il 30 agosto 2026; `permutation.txt`, `factorial.txt`, `multinomial-theorem.txt`, `anagrams-game.txt`, `anagram-dictionary.txt`, `jumble.txt`, prese il 1 settembre 2026
- **Stato della ricerca** fatta, 1 settembre 2026

## Che cos'è

Si prendono le lettere di una parola e si riscrivono in un altro ordine, tutte, senza aggiungerne e senza toglierne. *Mare* e *rame*. *Attore* e *teatro*.

La riga di differenza dal termine di paragone del blocco, la voce 328, incastro: **là l'ordine interno di ciascuna parola si conserva e cambia soltanto come si intrecciano; qui l'ordine non si conserva affatto.** È il valore estremo della variabile del blocco, e si misura — vedi sotto, 248 contro 40 320.

La definizione più stretta è del 1605 e sta in `anagram.txt`: William Camden chiama anagrammatismo «lo scioglimento di un nome scritto per esteso nelle sue lettere, come suoi elementi, e la sua ricomposizione per trasposizione artificiosa, **senza aggiunta, sottrazione o cambio di alcuna lettera**, in parole diverse che abbiano un senso compiuto applicabile alla persona nominata». Le tre negazioni sono la forma stessa.

Parti mobili: se il risultato debba avere un rapporto con la partenza; se si ammettano scambi di lettere equivalenti; se si riordini una parola o una frase, che è la voce 332, anagramma a frase.

## Da dove viene

`it-anagramma.txt` e `anagram.txt`, prese tutte e due il 30 agosto 2026, raccontano la stessa storia da due parti. Il nome è greco — *anà* più *grámma* — e l'uso antico era divinatorio: Artemidoro, nel secondo secolo, riferisce dell'indovino Aristandro di Telmesso, e Licofrone di Calcide nel terzo secolo avanti Cristo lo usava per adulare Tolomeo II. Nella letteratura talmudica e midrashica serviva a interpretare la Bibbia; i cabalisti lo chiamavano *temurah*.

L'esempio latino più citato è la risposta anagrammatica alla domanda di Pilato: *Quid est veritas?* dà *Est vir qui adest*. `it-anagramma.txt` avverte che l'attribuzione a Sant'Agostino è «attribuita nel medioevo, senza fonti certe», e questa è la riga da tenere: la fonte smonta da sé la sua storia più bella.

Fra Cinquecento e Seicento l'anagramma diventa un mestiere di corte. Luigi XIII teneva un **anagrammista reale**, Thomas Billon, con uno stipendio di 1 200 lire l'anno (`anagram.txt`). John Dryden lo definì «la tortura di una povera parola in diecimila modi», e la cosa non gli fece alcun danno.

Il ramo che conta di più è un altro. Nel Seicento gli astronomi pubblicavano le scoperte in anagramma **per fissare la data senza dire che cosa avevano visto.** Galileo annunciò le fasi di Venere come *Haec immatura a me iam frustra leguntur oy*; Huygens l'anello di Saturno con una stringa di lettere in ordine alfabetico; Hooke la sua legge come *ceiiinosssttuv*, che sciolto è *ut tensio, sic vis*. Keplero provò a sciogliere i due di Galileo e sbagliò tutte e due le volte — e per caso indovinò lo stesso l'esistenza degli oggetti di cui parlava.

Da una parte inattesa arriva il primo conto. `permutation.txt`, presa il 1 settembre 2026, attribuisce il primo uso di permutazioni e combinazioni ad **Al-Khalīl (717-786)**, matematico e crittografo arabo, nel *Libro dei messaggi crittografici*: gli servivano per elencare tutte le parole arabe possibili, con e senza vocali. La prima enumerazione di anagrammi non fu fatta per giocare, ma per fare un elenco esaustivo di parole — cioè la stessa cosa che oggi fa un dizionario di anagrammi. E il primo a scrivere i fattoriali per contarli fu **Fabian Stedman, nel 1677**, spiegando in quanti ordini si possono suonare le campane di un campanile.

## Varianti e parenti

- **Aptagramma** — le due parti hanno significati affini: *Stefano protomartire = santo morto fra pietre*.
- **Antigramma** — le due parti si contraddicono: *astronomers = no more stars*, *funeral = real fun*. In inglese `Antigram` è un rimando ad `Anagram`, controllato il 1 settembre 2026.
- **Anagramma imperfetto** — a cambio o a scarto di una lettera. `it-anagramma.txt` lo dice infrequente.
- **Metatesi** (320) e **spostamento** (319) — anagrammi «molto moderati», in cui una sola lettera migra. La fonte è esplicita: quando ci sono requisiti in più, il gioco prende il nome più specifico e non si chiama anagramma.
- **Anagramma diviso** — fra una parola e più parole: *realtà / sogno = ergastolano*.
- **Anagramma a frase** (332) — si riordina una frase intera.
- **Bifronte** (333) e **palindromo** (334) — riordinamenti vincolati a un verso solo di lettura.
- **Cernita** — lo schema del 1975 che scarta lettere a coppie e legge il resto in anagramma; sta alla voce 329, cerniera.
- **Jumble** — il gioco a stampa quotidiano, `jumble.txt`.
- **Anagrams** — il gioco di tessere, `anagrams-game.txt`, in cui si rubano le parole degli altri rimescolandole.
- **Dizionario di anagrammi** — `anagram-dictionary.txt`: le parole vi compaiono con le lettere messe in ordine alfabetico, così che tutte le anagrammabili fra loro finiscano vicine. È l'indice che rende il gioco meccanico.

## Che cosa se ne sa

**Che cosa si conserva.** `it-anagramma.txt` porta lo strumento che serve, e lo porta con il nome giusto: il **vettore di Parikh** di una stringa è la successione di quante volte compare ogni lettera dell'alfabeto, e due stringhe sono anagrammi quando hanno lo stesso vettore. Essere anagramma è una relazione di equivalenza, e la pagina fa notare che per un matematico ROMA è anagramma di ROMA. Ne segue la cosa che conta per noi: **c'è un invariante, e chi risponde lo può calcolare.** Contare le lettere è alla portata di chiunque, e non richiede né un vocabolario né la soluzione stampata.

**Quanti sono.** Se le *n* lettere sono tutte diverse gli anagrammi sono *n*!; se qualcuna si ripete si divide per il fattoriale di ogni ripetizione. La formula è quella del coefficiente multinomiale, ed è verificata per formula e per enumerazione completa in `build/check_328.py`:

| parola | quanti | come | metodi |
| --- | --- | --- | --- |
| roma | 24 | 4! | formula ed enumerazione |
| mamma | 10 | 120 / (3! × 2!) | formula ed enumerazione |
| calamaro | 6 720 | 40 320 / 3! | formula ed enumerazione |
| satelliti | 45 360 | 362 880 / (2! × 2! × 2!) | formula |
| spontaneo | 90 720 | 362 880 / (2! × 2!) | formula |

**La fonte sbaglia il nome della formula, nell'ultima riga della sua sezione di matematica.** `it-anagramma.txt` chiama *n*! / (*s*₁! … *s*ₖ!) «la formula generale delle già citate disposizioni con ripetizione». Le disposizioni con ripetizione sono *n*ᵏ — su ventuno simboli in cinque posti, 4 084 101 — e non hanno niente a che vedere con questo conto. Le due pagine inglesi lo chiamano con il nome giusto e lo dicono tutte e due: `permutation.txt` intitola la sezione *Permutations of multisets* e scrive che l'anagramma di una parola con lettere ripetute è un esempio di permutazione di multinsieme; `multinomial-theorem.txt` intitola la sua *Number of unique permutations of words*. Tutte e due portano lo stesso esempio, MISSISSIPPI, che ha 1 M, 4 I, 4 S e 2 P: 11! / (4! × 4! × 2!) = **34 650**, rifatto in `build/check_328.py`. Il numero della pagina italiana è giusto e il nome è sbagliato; è il tipo di errore che sopravvive a qualunque rilettura perché sta accanto a un risultato corretto.

**Quanto in fretta cresce.** `factorial.txt`, presa il 1 settembre 2026, riporta l'approssimazione di Stirling e la conclusione che il fattoriale cresce **più in fretta di un esponenziale** e meno in fretta di un doppio esponenziale. È la ragione per cui lo spazio di ricerca di un anagramma non si stampa mai, se non per parole cortissime.

**Quanto è più grande dell'intreccio.** Su otto lettere tutte diverse, gli intrecci di due parole danno 248 stringhe distinte (contate alla voce 324, sciarada alterna), e i riordinamenti liberi 40 320. **Il rapporto è 162,6 volte**, ed è la misura della variabile di questo blocco: quanto costa lasciar cadere il vincolo dell'ordine.

**Una fonte afferma qualcosa che non dimostra.** `it-anagramma.txt` sostiene che più lettere ci sono, più è probabile che l'anagramma dia associazioni sensate, e che «l'incremento nei risultati positivi è dimostrabile col calcolo combinatorio»; poi non lo dimostra. La verifica sta alla voce 332, anagramma a frase, dove il conto si può fare.

## Esempi trovati

Da `it-anagramma.txt`, riscritti: *attore = teatro*; *donna = danno*; *marocchino = monarchico*; *calendario = locandiera*; *doppiatore = pepita d'oro*. Rifatti tutti a macchina, e tornano.

Dalla stessa pagina, l'anagramma che definisce sé stesso, di Enrico Parodi detto Snoopy: *lo determini mercé l'esatto* = *rimescolamento di lettere*. Ventitré lettere per parte, controllate una per una: la frase dice come si fa la cosa che è.

Sempre da lì, gli pseudonimi: **Trilussa** è l'anagramma esatto di **Salustri**, cognome vero del poeta. *Voltaire* invece è imperfetto, e la pagina dichiara le forzature: *Arouet, l[e] j[eune]* con U che vale V e J che vale I.

Da `jumble.txt`: il *Jumble* nasce nel 1954 per mano di Martin Naydel, col nome di *Scramble*; Henri Arnold e Bob Lee lo tengono dal 1962 per almeno trent'anni; nel 2025 lo curano David L. Hoyt e Jeff Knurek, e esce su più di 600 giornali. La forma è fissa: **quattro parole mescolate, due da cinque lettere e due da sei**, alcune lettere cerchiate, e le cerchiate si rimescolano a loro volta per rispondere a una battuta. La versione per bambini ha una parola da tre e tre da quattro.

## Una nostra versione

> **Ventiquattro modi, e sei sono parole**
>
> Prendi le lettere R, O, M, A. I modi di metterle in fila sono **ventiquattro**: quattro scelte per la prima lettera, tre per la seconda, due per la terza, e l'ultima è obbligata. Quattro per tre per due fa ventiquattro, e sono tutti qui.
>
> ```
>  amor  amro  aomr  aorm  armo  arom
>  maor  maro  moar  mora  mrao  mroa
>  oamr  oarm  omar  omra  oram  orma
>  ramo  raom  rmao  rmoa  roam  roma
> ```
>
> Cerchia quelli che vogliono dire qualcosa in italiano. Quanti ne hai cerchiati? ────
>
> Adesso MAMMA, che ha cinque lettere. Il conto di prima darebbe cinque per quattro per tre per due, cioè centoventi. Ma le tre M sono uguali fra loro e le due A anche, quindi ogni parola viene contata più volte: una volta per ogni modo di scambiare le M fra loro — sono sei — e per ogni modo di scambiare le A — sono due. Centoventi diviso sei diviso due fa **dieci**.
>
> Scrivili tutti e dieci. Se te ne vengono undici, due sono uguali.
>
> ```
>  ────────  ────────  ────────  ────────  ────────
>  ────────  ────────  ────────  ────────  ────────
> ```

Le ventiquattro righe sono **lo spazio di ricerca per intero**, ed è l'ultima volta in questo blocco che ci sta: con cinque lettere tutte diverse sarebbero 120, con otto 40 320. Il salto da 24 a 40 320 si vede su un foglio solo perché il foglio si ferma a quattro.

La seconda parte è il conto con le ripetizioni fatto a parole invece che con la formula, e ha una rete: chi sbaglia se ne accorge da solo, perché gli vengono due righe uguali. **La verifica sta nel materiale**, e non in un vocabolario: le lettere si contano.

Il limite tecnico del capitolo non morde per la prima parte — al sistema si chiede di stampare le ventiquattro permutazioni di quattro lettere, che è un elenco fisso — e nemmeno per la seconda, che chiede solo righe vuote. Il giudizio «questa è una parola italiana» resta fuori, e la prima domanda lo dichiara chiedendo *quanti* e non *quali*.

## Da riprendere alla rassegna

**Il secondo termine di paragone del blocco, e il valore estremo della variabile.** Rispetto alla voce 328, incastro qui l'ordine di partenza non si conserva affatto, e la differenza si misura: 248 stringhe contro 40 320, cioè 162,6 volte. È la prima volta nel capitolo che la distanza fra due forme è un numero e non una descrizione.

**Un invariante rende il controllo dell'errore un conto invece che un giudizio.** Il vettore di Parikh si calcola contando, e chi risponde lo può fare. È la seconda scheda del capitolo 12 in cui la verifica sta nel materiale, dopo la voce 326, lucchetto, e ci sta per una ragione diversa: là si leggeva una chiave, qui si conserva una quantità. Alla rassegna: cercare, in tutto l'elenco, le forme che hanno un invariante calcolabile da chi risponde, perché sono le sole in cui il foglio si controlla da solo.

**Un numero giusto con il nome sbagliato accanto.** *Disposizioni con ripetizione* invece di *permutazioni di un multinsieme*, in una pagina che il conto lo fa bene. Da guardare alla rassegna: quante affermazioni di questa enciclopedia poggiano su un nome preso da una fonte invece che sulla cosa.

**Il Jumble è un formato a due tempi, e il secondo tempo dà la verifica.** Si sciolgono quattro anagrammi, si prendono le lettere cerchiate, e si rimescolano per rispondere a una battuta: se la battuta non torna, uno dei quattro è sbagliato. È il modo più economico che si sia visto nel capitolo 12 per rendere un foglio autoverificante, e non richiede la soluzione stampata.
