# Problema di ottimizzazione con vincoli fisici

- **Numero** 377 nell'enciclopedia, capitolo 13 — Giochi matematici e ricreativi
- **Si chiama anche** calcolatore analogico, il problema risolto dall'oggetto, albero di Steiner, lamina di sapone, catenaria, *soap film computer*, *Steiner tree*, *analogue computing*
- **In una riga** il percorso più breve fatto con uno spago.
- **Fonti** [Steiner tree problem](https://en.wikipedia.org/wiki/Steiner_tree_problem), [Soap bubble](https://en.wikipedia.org/wiki/Soap_bubble), [Minimal surface](https://en.wikipedia.org/wiki/Minimal_surface), [Plateau's problem](https://en.wikipedia.org/wiki/Plateau%27s_problem), [Catenary](https://en.wikipedia.org/wiki/Catenary), [Isoperimetric inequality](https://en.wikipedia.org/wiki/Isoperimetric_inequality), [Bolla di sapone](https://it.wikipedia.org/wiki/Bolla_di_sapone), [Travelling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem), lette il 2 settembre 2026

## Che cos'è

Si pone un problema di minimo e non lo si calcola: si costruisce un oggetto fisico i cui vincoli sono quelli del problema, si lascia che l'oggetto si sistemi, e si legge la risposta sull'oggetto. Uno spago teso fra due chiodi si mette dritto; una catena appesa prende la forma di minima energia; una lamina di sapone fra due fili prende l'area minima. **Il conto lo fa la materia.**

Le parti mobili:

- **Qual è l'oggetto.** Spago, catena, lamina di sapone, elastico, sabbia.
- **Che cosa si minimizza.** Lunghezza, area, energia potenziale. L'oggetto decide, e chi propone deve saperlo.
- **Come si legge la risposta.** Si misura con un metro, oppure si guarda la forma e si nomina.
- **Se l'oggetto trova il minimo o *un* minimo.** Questa è la parte che rovina tutto, e sta sotto.

**La differenza dalla voce 371, costruzione con riga e compasso:** là la prova stava nello strumento e lo strumento poteva sbagliare di un millimetro. Qui la prova sta ancora nello strumento, e lo strumento può sbagliare **in modo diverso e peggiore**: non di poco, ma di risposta, perché si ferma in un minimo locale e non ha modo di accorgersene. **È il valore della scala del blocco in cui la verifica dentro il materiale è più economica e meno affidabile insieme**, e le due cose vengono dalla stessa proprietà dell'oggetto.

## Da dove viene

**Il problema della rete più corta è del 1811 e non porta il nome di chi l'ha posto.** «Steiner tree problem»: la formulazione euclidea — dati *N* punti nel piano, collegarli con tratti di lunghezza totale minima — fu posta da **Joseph Diez Gergonne** nel 1811 in questi termini: «un certo numero di città si trova in posizioni note su un piano; il problema è collegarle con un sistema di canali di lunghezza complessiva minima». Il nome è di Jakob Steiner. Il primo trattamento serio è un articolo **in ceco** di Vojtěch Jarník e Miloš Kössler del **1934**, «a lungo trascurato», che secondo la pagina contiene già «praticamente tutte le proprietà generali degli alberi di Steiner» poi attribuite ad altri.

**Le lamine di sapone diventano matematica con Lagrange, e sperimentali con Plateau.** «Minimal surface» e «Plateau's problem»: Lagrange pone il problema variazionale della superficie di area minima su un contorno chiuso dato, e non trova nessuna soluzione oltre il piano. **Sulla data le due pagine non concordano**: il corpo di «Minimal surface» dice 1762, la sua nota bibliografica e «Plateau's problem» dicono 1760, e la nota rimanda a *Miscellanea Taurinensia* 2 del 1760. Nel **1776** Meusnier trova che l'elicoide e la catenoide soddisfano l'equazione. Il problema porta il nome di **Joseph Plateau**, che invece delle equazioni faceva esperimenti con le lamine di sapone; la soluzione completa è di Jesse Douglas e Tibor Radó, fra il 1925 e il 1950.

**La catena appesa ha una storia con dentro un aneddoto falso e un anagramma.** «Catenary»: si dice spesso che Galileo credesse che la catena appesa fosse una parabola, e **non è vero** — nei *Discorsi* del 1638 scrive che è una parabola solo approssimata, e che l'approssimazione migliora al diminuire della curvatura. Robert Hooke annuncia alla Royal Society nel **1671** di aver risolto il problema della forma ottima di un arco, e nel **1675** ne pubblica la soluzione **cifrata, come anagramma latino**, in appendice a un altro libro. L'equazione la ricavano **Leibniz, Huygens e Johann Bernoulli** nel **1691**, rispondendo a una sfida di Jakob Bernoulli, e la pubblicano insieme sugli *Acta Eruditorum* di giugno.

**Il problema isoperimetrico è il più antico e ha un nome di leggenda.** «Isoperimetric inequality»: trovare la figura piana di area massima a perimetro dato. Il problema affine, quello di Didone, chiede l'area massima delimitata da una retta e da un arco, e prende il nome dalla fondatrice leggendaria di Cartagine. Che la risposta sia il cerchio sembra ovvio ed è difficile da dimostrare: il primo progresso è di **Jakob Steiner, 1838**, che mostrò che *se* una soluzione esiste allora è il cerchio — e la parte mancante, cioè che esista, fu colmata dopo.

## Varianti e parenti

- **Spago teso** — il percorso più corto fra due punti, e con dei chiodi in mezzo il più corto che li tocchi.
- **Albero di Steiner** — la rete più corta che collega *N* punti, con la libertà di aggiungere punti nuovi.
- **Lamina di sapone fra due lastre di plexiglas** — con dei pioli fra le due lastre, la lamina disegna una rete di Steiner.
- **Catena appesa** — la catenaria, e capovolta è la forma dell'arco.
- **Bolla di sapone** — l'area minima a volume dato, cioè la sfera.
- **Modello di sabbia o di gesso** — l'ottimo trovato per gravità invece che per tensione.
- **Voce 153, problema di ottimizzazione** — la forma di pagina; rimanda qui, e dichiara che il confine è meno netto di come lo pone l'elenco perché Dantzig, Fulkerson e Johnson usarono davvero uno spago. **Ricontrollato: regge**, e la differenza vera non è lo spago, è dove sta la prova.
- **Voce 366, problema di grafi** — il commesso viaggiatore, dove la prova che si è finito non sta da nessuna parte.
- **Voce 272, costruzione di un motore** — l'altra voce in cui la verifica sta in un oggetto che si comporta da sé.
- **Voce 46, modello in scala** — la stessa idea senza il minimo: l'oggetto fa il conto delle proporzioni.
- **Voce 371, costruzione con riga e compasso** — l'altra voce del blocco in cui lo strumento è la prova.

## Che cosa se ne sa

**La lamina di sapone è un calcolatore analogico, e lo dice la fonte con queste parole.** «Soap bubble»: «a volte è più facile costruirle fisicamente che calcolarle con un modello matematico. È per questo che le lamine di sapone possono essere considerate calcolatori analogici che, a seconda della complessità del sistema, possono battere i calcolatori convenzionali». La pagina cita Cyril Isenberg, *The Soap Film: An Analogue Computer*, *American Scientist*, **1976**. **L'ingegnere Frei Otto usò lamine di sapone per determinare la geometria delle sue coperture tese**, e ne uscì il padiglione tedesco all'Expo 67 di Montreal.

**E la lamina trova un minimo, non il minimo. La stessa parola compare in due pagine.** «Minimal surface», prima riga: «una superficie che minimizza **localmente** la sua area»; e più sotto, per esteso: «questa proprietà è locale: possono esistere regioni della superficie minima per cui esistono altre superfici di area minore con lo stesso bordo». **La macchina che risolve il problema non sa dire se ha risolto il problema.** È lo stesso difetto dell'ettagono approssimato della voce 371, costruzione con riga e compasso, in una forma peggiore: là l'errore era di un millimetro, qui è di risposta.

**Gli angoli sono gli stessi in due discipline, e questo è il fatto che tiene insieme la voce.** «Soap bubble» enuncia le leggi di Plateau: dove tre pareti di bolla si incontrano lungo una linea, i tre angoli valgono **120 gradi**, perché la tensione superficiale è uguale nelle tre superfici; in un punto se ne incontrano al massimo quattro, e le linee triple che vi convergono formano angoli di **arccos(−1/3) ≈ 109,47 gradi**. «Steiner tree problem» enuncia la stessa cosa per la geometria: i punti aggiunti in un albero di Steiner hanno grado **tre** e i tre tratti che ne escono formano **tre angoli di 120 gradi**. **La lamina di sapone obbedisce alla legge dell'albero di Steiner perché è la stessa legge**, e questo si vede in un bicchiere.

**Sui quattro angoli di un quadrato la risposta migliore non è fra quelle che si potevano provare.** Enumerando tutti i modi di collegare quattro punti usando solo tratti fra i punti: sono **16** alberi ricoprenti, che è quello che dice la formula di Cayley, 4² = 16. Il più corto misura **3** lati. L'albero di Steiner, che aggiunge due punti che nessuno aveva dato, misura **1 + √3 = 2,732**, cioè l'**8,93%** in meno. Verificato per due strade: la formula chiusa e un minimo numerico cercato per raffinamenti successivi, che concordano fino alla quarta cifra. L'angolo ai due punti aggiunti è 120,00 gradi, calcolato. **Lo spago non sceglie fra le sedici possibilità: le scarta tutte e sedici.**

**Quanto si guadagna al massimo, e la domanda è aperta dal 1968.** «Steiner tree problem»: il **rapporto di Steiner** è il massimo rapporto fra l'albero ricoprente minimo e l'albero di Steiner minimo. La congettura di Gilbert–Pollak dice che vale **2/√3 ≈ 1,1547**, cioè il caso del triangolo equilatero, e **nonostante dimostrazioni annunciate in passato la congettura è tuttora aperta**; il limite superiore accettato è **1,2134**, di Chung e Graham, 1985. Sul nostro quadrato il rapporto vale 1,0981, dentro il limite. **Il guadagno che la materia offre gratis è al massimo del quindici per cento, e non si sa dimostrarlo.**

**Il problema che la materia risolve è NP-difficile, e questo va detto insieme al resto.** La versione decisionale dell'albero di Steiner sui grafi è fra i ventuno problemi NP-completi originali di Karp; quella euclidea è NP-difficile. **Non si sa nemmeno se stia in NP**, perché non si sa se la lunghezza ottima si possa scrivere in modo verificabile in tempo polinomiale. La stessa pagina però avverte che in pratica molte varianti si risolvono efficientemente su istanze reali grandi. **Il caso peggiore e il caso normale dicono cose opposte, e la fonte le dice tutte e due.**

**La pagina italiana sulle bolle è corretta e non aggiunge niente di misurato.** «Bolla di sapone» dà la ragione della forma sferica — la sfera ha la superficie minima a volume dato — e la regola della fusione di due bolle, ma non riporta né le leggi di Plateau con i loro angoli né l'uso come calcolatore. È stata letta e serve solo a confermare la parte già coperta.

## Esempi trovati

Da Frei Otto, in «Soap bubble»: la geometria di un tetto teso determinata immergendo un telaio in acqua saponata. È un edificio progettato da una lamina.

Da Gaudí, in «Catenary»: gli archi a catenaria sotto il tetto di Casa Milà a Barcellona. Gaudí li trovava appendendo catenelle e guardando il modello capovolto.

Da «Catenary», come curiosità che si può costruire: una ruota **quadrata** rotola perfettamente liscia su una strada fatta di gobbe a catenaria capovolta. Funziona per ogni poligono regolare tranne il triangolo.

Da Hooke, 1675: la soluzione del problema dell'arco pubblicata come anagramma latino, cioè un risultato scientifico consegnato in forma di enigma per rivendicare la priorità senza rivelare il contenuto.

Da «Travelling salesman problem»: Dantzig, Fulkerson e Johnson nel 1954 usarono uno spago per esaminare i giri sulla loro istanza di 49 città. È la voce 153, problema di ottimizzazione che lo segnala, ed è il caso in cui lo strumento fisico serve a chi il conto lo sa fare.

## Un esempio giocabile

> **Quattro capanni e uno spago**
>
> Quattro capanni ai quattro angoli di un quadrato di venti centimetri, disegnati su un cartoncino. Vanno collegati tutti — non serve che ogni capanno tocchi tutti gli altri, basta che da uno si arrivi a ogni altro seguendo i sentieri.
>
> ```
>  A-----------------B
>  |                 |
>  |                 |
>  |                 |
>  |                 |
>  D-----------------C
>
>  filo teso:  ______ cm
>  il piu' corto che ho trovato: ______ cm
> ```
>
> Prima con lo spago sui quattro angoli, misurando ogni volta. Poi prova a fare di meglio **aggiungendo dei punti che non c'erano**: un incrocio in mezzo al campo, dove i sentieri si uniscono.
>
> Se collegando solo capanno con capanno ci sono sedici modi, e il migliore misura sessanta centimetri. **Con due incroci aggiunti si scende sotto i cinquantacinque**, e la differenza è del nove per cento. Quando ci arrivi, guarda con che angolo si aprono i tre sentieri a ogni incrocio, e misuralo.
>
> Poi, se hai una bacinella di acqua e sapone e due lastrine di plastica trasparente con quattro chiodini in mezzo: immergile e tira fuori. La lamina di sapone ti dà la stessa figura in un secondo, e non sa niente di geometria.

Lo spago misura ma non dimostra: la lunghezza si legge sul metro e resta una misura. Il numero che serve — l'8,93% e i 120 gradi — è calcolato, e va stampato perché sul cartoncino non si distingue un ottimo da un quasi ottimo. **La parte che vale è la seconda domanda**, quella in cui si scopre che la risposta migliore usa punti che non stavano nel problema. Il pezzo con il sapone è facoltativo e non regge da solo: richiede materiale che non è carta.

## Che cosa la rende interessante

**Sulla scala del blocco è il valore in cui la verifica è più economica e meno affidabile insieme, e le due cose hanno la stessa causa.** L'oggetto fisico si sistema da solo — non c'è niente da calcolare, niente da controllare — e proprio perché si sistema da solo si ferma dove capita di essere fermo, cioè in un minimo locale. **La verifica dentro il materiale non è una categoria sola.** Le forbici della voce 375, topologia ricreativa contano pezzi interi e non sbagliano; il compasso della voce 371, costruzione con riga e compasso misura e sbaglia di poco; la lamina risolve e può sbagliare del tutto.

**La risposta migliore non stava fra le possibili, ed è la cosa più forte del blocco.** Sedici modi di collegare quattro punti, e il migliore non è nessuno dei sedici perché aggiunge due punti che non erano dati. Nelle altre sei voci del blocco lo spazio dei candidati si restringe; qui si scopre che era il posto sbagliato dove cercare. **Vale come domanda generale su ogni forma che consegna un elenco di possibilità: chi ha deciso l'elenco?**

**Due discipline lontane danno lo stesso numero, e questo è materiale d'oro per un pomeriggio.** Centoventi gradi negli angoli di una lamina di sapone, per via della tensione superficiale; centoventi gradi ai punti aggiunti di un albero di Steiner, per via di un calcolo di minimo. Sono la stessa cosa, e si vede in un bicchiere. **È il collegamento più corto raccolto in tutta l'enciclopedia fra una cosa che si guarda e un teorema.**

**Il costo materiale è il secondo del blocco dopo i pentamini.** Uno spago e un cartoncino bastano; la bacinella di sapone e le lastrine no, e la scheda le mette come facoltative apposta. **La regola generale che ne viene: quando una forma ha una versione povera e una ricca, la scheda deve funzionare per intero con la povera**, e la ricca va scritta come aggiunta invece che come metà della consegna.

