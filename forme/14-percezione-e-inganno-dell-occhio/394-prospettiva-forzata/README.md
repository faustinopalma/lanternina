# Prospettiva forzata

- **Numero** 394 nell'enciclopedia, capitolo 14 — Percezione e inganno dell'occhio
- **Si chiama anche** prospettiva forzata, falsa prospettiva, la foto in cui reggi la torre, *forced perspective*, *false perspective*, effetto Hagrid
- **In una riga** un oggetto vicino che sembra grande, e la fotografia che lo prova.
- **Contratto** voce breve
- **Fonti** `forced-perspective.txt`, `it-prospettiva-forzata.txt`, `depth-perception.txt`, `perspective-distortion.txt`, `perspective-graphical.txt`, `vanishing-point.txt`, `dolly-zoom.txt`, `miniature-faking.txt`, `subjective-constancy.txt`, `emmerts-law.txt`, `moon-illusion.txt`, `ames-window.txt`, `ames-room.txt`, lette il 2 settembre 2026. I conti sono nostri, in `build/check_391.py`
- **Stato della ricerca** fatta, 2 settembre 2026

## Che cos'è

Si mettono due oggetti a distanze diverse da un solo punto di vista, e li si sceglie in modo che occupino sulla retina lo stesso angolo. Da quel punto e solo da quello, il piccolo vicino e il grande lontano sembrano della stessa taglia.

`forced-perspective.txt` dà la formula, ed è tutta la forma:

```
theta = 2 · arctan( h / 2D )
```

dove `h` è l'altezza vera dell'oggetto e `D` la distanza dall'occhio. **Due oggetti di altezza diversa occupano lo stesso angolo quando il rapporto fra altezza e distanza è lo stesso.**

Parti mobili:

- **Il rapporto fra le due distanze.** È il solo parametro che conta.
- **Da dove si guarda.** Il punto di vista non è un dettaglio dell'esecuzione: è metà della cosa.
- **Che cos'altro tradisce la distanza.** L'illuminazione, il fuoco, l'ombra: `forced-perspective.txt` elenca i modi in cui si correggono.
- **Se il punto di vista si può muovere.** Se sì, l'inganno cade subito. Se è un occhio solo e fermo — cioè una macchina fotografica — non cade mai.
- **Se l'oggetto è riconoscibile.** Una cosa di cui si conosce la taglia vera è più difficile da falsificare.

## Da dove viene

`forced-perspective.txt`: era già un tratto del cinema muto tedesco, e *Quarto potere* ne rilanciò l'uso; i film a basso costo degli anni Cinquanta e Sessanta ne sono pieni. Nella scena finale di *Casablanca*, girata tutta in studio, l'aereo è un fondale dipinto «servito» da persone di bassa statura messe accanto, e un acquazzone artificiale distrae lo sguardo abbastanza da reggere l'insieme.

**In architettura è più vecchia e più tranquilla.** La stessa pagina: nell'Aula Palatina di Costantino a Treviri le finestre dell'abside sono più piccole e il pavimento è rialzato, così l'abside sembra più profonda — e da fuori si vede che le finestre sono davvero di due misure. La Statua della Libertà è costruita con una lieve prospettiva forzata perché appaia proporzionata guardandola dalla base.

`it-prospettiva-forzata.txt` sono **1 926 byte** dichiarati abbozzo, che traducono l'apertura della pagina inglese e citano un manuale italiano di scenotecnica del 1982. Non aggiungono niente e lo si dice.

**La prospettiva lineare da cui tutto questo dipende ha una data.** `perspective-graphical.txt`: Brunelleschi condusse fra il **1415 e il 1420** la serie di esperimenti da cui viene, e la sua tavola del Battistero è perduta, il che lascia aperta ogni questione sulla correttezza della costruzione. `vanishing-point.txt`: il punto di fuga fu introdotto da Leon Battista Alberti nel *De pictura* del **1435**.

## Varianti e parenti

- **Far sembrare grande il piccolo** — la mano che schiaccia una testa, la persona che regge la torre.
- **Far sembrare piccolo il grande** — `miniature-faking.txt`: si sfoca il sopra e il sotto della fotografia per imitare la poca profondità di campo del primo piano, e una città sembra un plastico. Si scatta dall'alto, che è il punto di vista di chi guarda un modellino.
- **Prospettiva forzata in architettura** — costruita nel muro, e permanente.
- **Stanza di Ames** — `ames-room.txt`: la stanza deformata in cui due persone sembrano di taglia diversa. È la stessa idea con il punto di vista imposto da un buco.
- **Finestra di Ames** — `ames-window.txt`: un trapezio dipinto come una finestra rettangolare che, girando, sembra oscillare invece che ruotare. Adelbert Ames, 1947.
- **Dolly zoom** — `dolly-zoom.txt`: si arretra con la macchina mentre si zooma avanti, così il soggetto resta della stessa taglia e lo sfondo si allunga. Inventato da Irmin Roberts, operatore di seconda unità della Paramount, per *La donna che visse due volte* di Hitchcock, e non accreditato nei titoli.
- **Illusione della Luna** — `moon-illusion.txt`: la Luna all'orizzonte sembra più grande, e la pagina dichiara che **la spiegazione resta inconclusa**; l'illusione di Ponzo è quella più citata. Ci si può aggiungere `emmerts-law.txt`: Emil Emmert, 1881, notò che un'immagine residua sembra crescere se la si proietta più lontano — ma «l'aumento percepito è molto minore di quanto la geometria predirebbe».
- **Costanza di grandezza** — `subjective-constancy.txt`: entro un certo intervallo si percepisce la taglia vera invece di quella sulla retina. La prospettiva forzata è quel meccanismo preso in castagna.
- **Voce 382, anamorfosi** — l'altra voce del capitolo in cui la risposta sta nella posizione del corpo di chi guarda. Là la deformazione è sul foglio; qui è nella stanza.
- **Voce 379, ambiguità figura-sfondo** e **voce 380, figura reversibile** — là le letture sono due e stanno tutte e due sul foglio; qui la lettura è una sola per ogni posizione della macchina.

## Che cosa se ne sa

**Il conto che serve per farla, fatto.** Una mano alta 18 cm tenuta a 40 cm dall'occhio occupa **25,4 gradi**. Una persona alta 170 cm occupa lo stesso angolo a **3,78 m**. Non ci sono altri parametri: se le due si allineano nell'inquadratura, la persona sta in mano.

```
 che cosa       alto  lontano  quanto occupa
 la mia mano   18 cm    40 cm     25,4 gradi
 una persona  170 cm   3,78 m     25,4 gradi
```

**Quanto arretramento serve, sul caso più famoso.** `forced-perspective.txt` dà le altezze di Elijah Wood, 5 piedi e 6 pollici, e di Ian McKellen, 5 piedi e 11: la differenza vera è **12,70 cm**. Per far sembrare il primo alto la metà del secondo, va messo **1,859 volte** più lontano dalla macchina: con Gandalf a 3 m, Frodo sta a 5,58 m, cioè **2,58 m più indietro**, che sono 8,5 piedi. La pagina scrive «displaced by several feet in depth» e il conto lo conferma.

**E la stessa pagina si contraddice su due numeri, tutti e due controllabili con la pagina in mano.** Il primo: dice «solo 5 pollici (13 cm)» e poco prima ha dato le altezze in metri come 1,68 e 1,80, la cui differenza è 12. La differenza vera è 12,70, quindi i 13 cm sono l'arrotondamento giusto e i metri arrotondati danno un centimetro in meno. Il secondo è più grosso: la pagina spiega bene che la luce di una sorgente puntiforme cala **come l'inverso del quadrato della distanza**, e che quindi a distanza doppia serve **quattro volte** la luce; venti righe dopo scrive che l'illuminamento cala «come `1/2d`», che a distanza doppia darebbe due volte la luce. Le due affermazioni si escludono, e a decidere è la prima, che porta con sé il proprio conto.

**Su diciannove indizi di profondità, dieci sopravvivono a un foglio, e nessuno muore per il bianco e nero.** `depth-perception.txt` elenca **sedici indizi monoculari e tre binoculari**. Un foglio fermo e piatto ne perde sei: quattro perché non si muove — parallasse di movimento, profondità dal movimento, effetto cinetico di profondità, parallasse oculare — e due perché è piatto — accomodazione e sfocatura. I tre binoculari appartengono alla voce 395, stereogramma. Restano **dieci indizi monoculari su sedici**, e sono quelli che la prospettiva forzata usa: prospettiva lineare, grandezza relativa, grandezza familiare, grandezza assoluta, occlusione, gradiente di trama, luce e ombra, elevazione, prospettiva aerea e prospettiva curvilinea. Il conto è in `build/check_391.py`, ricavato leggendo le intestazioni della fonte invece che ricopiandole.

**Il bianco e nero morde una volta sola e non su un indizio.** La prospettiva aerea ha due componenti: il calo di contrasto, che sopravvive, e lo spostamento verso il blu delle cose lontane, che no. `forced-perspective.txt` la chiama *chromostereopsis* e cita Cézanne, che scaldava con il rosso quello che voleva vicino e raffreddava con il blu quello che voleva lontano. In bianco e nero resta il contrasto e sparisce la tinta, cioè **metà di un indizio su dieci**.

**La previsione della voce 382, anamorfosi su questa voce è sbagliata, e il motivo è istruttivo.** Quella scheda scrive che il limite della fotografia varrà «probabilmente» anche qui. Non vale. All'anamorfosi l'effetto sta nella posizione dell'occhio **rispetto al foglio**, e una fotografia presa da sopra lo distrugge. Qui l'effetto sta nella posizione della macchina **rispetto alla scena**, e appena lo scatto è fatto l'inganno è dentro l'immagine piana per sempre: si stampa, si fotocopia, si rifotografa, e resta. `perspective-distortion.txt` lo dice in una riga che vale tutta la voce: **«i cambiamenti di prospettiva lineare sono causati dalla distanza, non dall'obiettivo»**. La fotografia non è il limite di questa forma: **è il suo strumento.**

**Quello che la fotografia toglie è la prova, non l'effetto.** `forced-perspective.txt`: se il punto di vista si sposta, la parallasse rivela subito le vere posizioni in profondità; e anche solo ruotando la macchina, se non la si ruota attorno al punto giusto — il *punto a parallasse zero*, che in pratica è il centro della pupilla d'ingresso — il punto di vista si sposta per sbaglio. **Un'immagine ferma è l'unico supporto su cui questa forma non si smonta**, e questo la mette esattamente all'opposto della voce 395, stereogramma, dove è l'immagine ferma a non bastare.

**C'è però un secondo limite della stampa, ed è una distanza.** `perspective-distortion.txt`: la deformazione dipende dalle distanze **di ripresa e di visione** messe insieme, e `vanishing-point.txt` dice dove va l'occhio, cioè nell'*oculus*, il punto da cui l'immagine restituisce la geometria giusta. Per una stampa larga 150 mm quella distanza è:

```
 inquadratura  da quanto lontano guardarla
     30 gradi                       280 mm
     45 gradi                       181 mm
     65 gradi                       118 mm
     90 gradi                        75 mm
```

Con un'inquadratura larga bisognerebbe tenere il foglio a sette centimetri dall'occhio, e nessuno lo fa. **Chi guarda una fotografia grandangolare da distanza normale la vede meno deformata di com'è.** Non impedisce l'effetto, lo attenua, e di quanto dipende da come è stata scattata.

**Il muro di `ideas/10 §8` non morde**, perché la risposta è una formula e la formula è scritta sul foglio.

## Esempi trovati

Da *Casablanca*: l'aereo dipinto, servito da persone di bassa statura, sotto la pioggia.

Da *Il Signore degli Anelli*: gli attori spostati di un paio di metri in profondità, e i mobili di due misure. La stessa cosa in *Harry Potter*, per Hagrid.

Dall'Aula Palatina di Treviri: le finestre dell'abside più piccole delle altre, e il pavimento rialzato.

Dai parchi a tema: il castello della Bella Addormentata a Disneyland è alto **23 metri** e sembra molto più alto perché gli elementi architettonici rimpiccioliscono salendo; a Cinderella Castle, alto **58 metri**, fanno lo stesso; al padiglione The American Adventure a Epcot lo usano al contrario, per far sembrare di tre piani un edificio di due.

Dai diorami dei musei di storia naturale: piano inclinato, fondale dipinto, oggetti rimpiccioliti verso il fondo. Il primo lo costruì Carl Akeley nel **1889**, con dei castori.

Dalle fotografie che tutti hanno fatto: reggere la torre di Pisa, tenere il sole in mano.

## Una nostra versione

> **Metti una persona in mano**
>
> Serve una macchina fotografica — quella del telefono va bene — e una persona che stia ferma.
>
> Un oggetto occupa nell'occhio un angolo che dipende **solo** dal rapporto fra quanto è alto e quanto è lontano. Se due oggetti hanno lo stesso rapporto, occupano lo stesso angolo, e nella fotografia sono grandi uguali.
>
> ```
>  che cosa       alto  lontano  quanto occupa
>  la mia mano   18 cm    40 cm     25,4 gradi
>  una persona  170 cm   3,78 m     25,4 gradi
> ```
>
> Quindi: tieni la mano a **40 cm** dall'obiettivo e manda la persona a **3,8 metri**. Scatta. La persona ti sta in mano.
>
> Adesso misura tu, invece di copiare:
>
> ```
>  quanto e' alto chi fotografo   ........ cm
>  a che distanza l'ho messo      ........ cm
>  quanto e' alta la mia mano     ........ cm
>  a che distanza tengo la mano   ........ cm
> ```
>
> I due rapporti **altezza diviso distanza** devono venire uguali. Vengono? Di quanto sbagliano?
>
> Poi la domanda vera: **come si potrebbe smascherare la fotografia?** Non guardandola meglio. Prova a spostarti di un passo e a guardare la stessa scena con i tuoi occhi.

Il ragionamento sta in una divisione, e si controlla con un metro. La risposta all'ultima domanda è la parallasse: appena il punto di vista si sposta, le due distanze si separano e l'illusione cade. Vale la pena farlo notare, perché è la ragione per cui questa forma vive nelle fotografie e non nelle stanze.

Dove si romperebbe: non nel sistema, ma nella catena. Il foglio che si stampa contiene il conto e le righe da riempire, e quello che torna indietro sono i numeri, non l'immagine — il sistema legge la fotografia di **un foglio**, non della scena. Chi fa l'attività si tiene la fotografia. È un caso in cui la forma sta nel formato per intero, e il risultato più bello resta fuori.

## Da riprendere alla rassegna

**Una previsione di una voce precedente è stata verificata e smentita.** La voce 382, anamorfosi diceva che il limite della fotografia sarebbe valso «probabilmente» anche qui. Non vale, e il perché è generale: **conta di che cosa la fotografia sia una fotografia.** Se l'effetto sta nella posizione dell'occhio rispetto al foglio, fotografare il foglio lo distrugge; se sta nella posizione della macchina rispetto alla scena, fotografarla lo fissa. Alla rassegna: una previsione scritta dentro una voce va verificata quando si arriva alla voce prevista, e non ripetuta.

**È l'unica forma del capitolo il cui supporto naturale è una fotografia e non un foglio.** L'immagine ferma non è un ripiego: è la condizione. Alla rassegna sta all'opposto della voce 395, stereogramma, dove il foglio serve ma non basta, e della voce 382, anamorfosi, dove il foglio è indispensabile e la fotografia lo rovina.

**Il bianco e nero morde mezzo indizio su dieci, e per la prima volta la frazione è misurabile.** Su diciannove indizi di profondità elencati dalla fonte, sei muoiono perché il foglio è fermo e piatto, tre sono binoculari, dieci restano, e il bianco e nero toglie la metà colorata di uno solo di quei dieci. È il conto più fine che sia stato possibile fare sul vincolo di stampa in tutto il capitolo, e la ragione è che qui la fonte elenca gli indizi uno per uno.

**Una fonte si contraddice su una legge fisica dentro la stessa pagina, e la parte giusta porta il proprio conto.** L'inverso del quadrato e il `1/2d` non possono valere insieme. Alla rassegna vale come promemoria: quando una pagina enuncia una legge e poi la richiama in forma abbreviata, la forma abbreviata è quella da controllare.

**La riga di differenza.** Alle voci 391, 392 e 393 il foglio contiene l'oggetto, in tutto o in parte, e il lavoro è ricostruirlo. Qui il foglio contiene **una scena che non esiste**: tutto quello che si vede è vero, ogni oggetto è dove è stampato, e ciò che è falso è una sola cosa, la distanza. **È la prima forma del capitolo in cui non manca niente e non c'è niente di ambiguo, e la lettura è comunque sbagliata.**
