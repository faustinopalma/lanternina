# Immagine da comporre in controluce

- **Numero** 390 nell'enciclopedia, capitolo 14 — Percezione e inganno dell'occhio
- **Si chiama anche** crittografia visuale, condivisione visiva di un segreto, due lucidi, *visual cryptography*, *visual secret sharing*, immagine in due parti
- **In una riga** due fogli che insieme dicono una cosa che nessuno dei due dice.
- **Contratto** voce breve
- **Fonti** `visual-cryptography.txt`, `it-crittografia-visuale.txt`, `secret-sharing.txt`, `halftone.txt`, `superimposition.txt`, `anaglyph-3d.txt`, lette il 2 settembre 2026. I conti sono nostri, in `build/check_385.py`
- **Stato della ricerca** fatta, 2 settembre 2026

## Che cos'è

Due fogli. Ognuno, guardato da solo, è una distribuzione di macchie senza significato. Sovrapposti e tenuti contro la luce, mostrano un'immagine che non sta su nessuno dei due.

**Questa voce guarda il lato dell'occhio.** Il lato del foglio — che cosa bisogna stampare perché la cosa funzioni — è la voce 140, sovrapposizione di due fogli, e quella scheda dichiara il confine con queste parole: là si guarda che cosa bisogna stampare perché si possano sommare, qui che cosa succede all'occhio quando due immagini si sommano.

E quello che succede all'occhio ha un nome preciso, che è la parola del mestiere della stampa: **retino**. `halftone.txt`: quando i punti del retino sono piccoli, l'occhio interpreta le zone così stampate come se fossero tinte continue. La crittografia visuale non produce nero e bianco: produce **nero e mezzo nero**, e conta sull'occhio per trasformare il mezzo nero in un grigio.

Parti mobili:

- **Quanto è grande la cella.** Decide tutto, ed è tirata da due parti opposte.
- **Quanto sono allineati i due fogli.** Il contrasto cala linearmente con lo scarto e si annulla.
- **Quanto contrasto resta.** Metà, nel caso base.
- **Quante parti sono.** Due, o *n* di cui ne bastano due.
- **Chi ha il secondo foglio.** La stessa persona, o un'altra.

## Da dove viene

**La forma matematica ha una data e due nomi.** `visual-cryptography.txt` e `it-crittografia-visuale.txt`: nel **1994** Moni Naor e Adi Shamir presentano uno schema di condivisione visiva di un segreto. Un'immagine in bianco e nero è divisa in *n* parti stampate su altrettanti lucidi; solo chi le ha tutte può ricostruirla, e *n* − 1 parti non dicono niente. **La decifrazione non richiede nessun calcolo: si sovrappongono i lucidi e si guarda.**

**Il ramo a cui appartiene è più vecchio di quindici anni.** `secret-sharing.txt`: la condivisione di un segreto è stata inventata indipendentemente da Adi Shamir e George Blakley nel **1979**. Uno schema a soglia (*t*, *n*) consegna a ognuno degli *n* una parte, e ne bastano *t* per ricostruire il segreto; con meno di *t* non si sa niente più di chi non ne ha nessuna.

**La pagina inglese dichiara anche degli antecedenti che non elenca**: brevetti degli anni Sessanta, e lavori sulla percezione e sulla comunicazione sicura. La pagina italiana è un abbozzo di 3 343 byte e non aggiunge storia; aggiunge però la descrizione dell'esempio con il logo di Wikipedia, che è il modo in cui la cosa viene insegnata quasi ovunque.

## Varianti e parenti

- **Schema due su due** — il caso base: due fogli, tutti e due necessari.
- **Schema due su *n*** — le parti sono molte e ne bastano due qualsiasi.
- **Steganografia visiva** — `visual-cryptography.txt`: con sottocelle 2×2, un bianco diventa tre sottocelle nere e un nero quattro, così che **ogni foglio porti a sua volta un'immagine leggibile**. Il contrasto del segreto cala alla metà.
- **Blocco monouso** — con due lucidi si realizza un cifrario a chiave usa e getta: uno è la chiave casuale, l'altro il testo cifrato.
- **Anaglifo** — `anaglyph-3d.txt`: l'altro modo di sovrapporre due immagini perché l'occhio le separi, con due colori e due filtri. Richiede il colore da tutte e due le parti, e noi non ne abbiamo.
- **Moiré** — `superimposition.txt`: due strati periodici sovrapposti producono da soli una figura. Vedi la voce 389, moiré.
- **Voce 140, sovrapposizione di due fogli** — il lato del foglio, con la stessa fonte principale.
- **Voce 141, griglia di Cardano** — anche là due fogli, ma uno dei due si legge già da solo.
- **Voce 175, puzzle ottico** — quella scheda nomina questa e dice che il suo capitolo è il 5. È il capitolo 14, e la riga va corretta là.

## Che cosa se ne sa

**Il contrasto che resta è la metà, e la fonte lo dichiara senza chiamarlo così.** `visual-cryptography.txt`: sovrapponendo le parti, tutte le sottocelle del pixel nero diventano nere, mentre **il 50% delle sottocelle del pixel bianco resta bianco**. Cioè: nero contro grigio a metà, e non nero contro bianco. **Il contrasto è del 50%, non del 100%.** Nella variante a 2×2 sottocelle è 4/4 contro 3/4, cioè **il 25%**: la metà della metà.

**Il registro decide tutto, e adesso c'è un numero.** Con celle da 8 mm, `build/check_385.py` calcola quanto contrasto resta spostando un foglio rispetto all'altro. La formula è `50% − 150% × scarto/lato`, e il tre mezzi non è quello che verrebbe a occhio: una volta su due lo scorrimento porta il nero del secondo foglio **fuori** dalla cella e non guadagna niente. La simulazione — una striscia di tremila celle sorteggiate, con le celle vicine, campionata punto per punto — dà gli stessi numeri entro due punti percentuali. Mezzo millimetro di scarto costa un quinto del contrasto, un millimetro ne costa quasi due quinti, e **il contrasto si annulla a 2,7 mm**, cioè a un terzo del lato della cella.

**Le due esigenze tirano in versi opposti, e il rapporto è quarantasette.** Perché due fogli allineati a mano funzionino, la cella deve essere grande: a 8 mm si tollera mezzo millimetro di scarto perdendo un quinto del contrasto. Perché l'occhio veda un grigio invece di due mezze celle, la cella deve stare sotto il retino tipografico: `halftone.txt` dà 150 righe al pollice come valore usuale, cioè **0,169 mm**. La cella che regge il registro a mano è **47 volte** più larga di quella che l'occhio fonderebbe. **Su carta allineata a mano il grigio non si vede: si vedono le mezze celle, e l'immagine si legge dalla tessitura invece che dal tono.** È un fatto e non un difetto, ma va detto sul foglio.

**La stampante non è il collo di bottiglia, e questo è il contrario della voce 389, moiré.** A 600 punti per pollice una cella da 0,169 mm sarebbe di quattro punti, che basterebbero. Quello che manca non è la risoluzione: è la mano che allinea.

**Un foglio solo non è la prova di niente.** `visual-cryptography.txt` lo scrive per esteso: avendo una delle due parti si può costruire una seconda parte falsa che, sovrapposta, produce **qualunque** immagine si voglia. Un foglio non rivela il segreto e non testimonia nemmeno che ci fosse un segreto.

**La stessa fonte dichiara come si bara.** Horng e colleghi: *n* − 1 partecipanti che colludono possono confrontare le proprie parti per dedurre dove l'*n*-esimo avrà i pixel neri, e costruire una parte nuova che con la sua produce un messaggio diverso. La sicurezza è sull'immagine, non sull'onestà.

**Quello che le fonti non dicono, e che serviva.** Nessuna misura di quanta luce passi attraverso due fogli di carta da stampante sovrapposti. Tutte le pagine descrivono la cosa su lucidi. La voce 140, sovrapposizione di due fogli lo segnava come da verificare: la parte geometrica è verificata qui, la parte fotometrica **va ancora verificata**, e si verifica con due fogli e una finestra.

## Esempi trovati

Da Naor e Shamir, 1994: due lucidi che sembrano rumore e che sovrapposti mostrano una parola.

Dal logo di Wikipedia, diviso in due parti: l'esempio con cui la cosa si insegna in italiano e in inglese.

Da *The Prisoner*, episodio del 1967 «Do Not Forsake Me Oh My Darling»: il protagonista sovrappone più lucidi per scoprire dove si nasconde uno scienziato.

Dalla protezione dei dati biometrici: la parte in cui la decifrazione non richiede nessun calcolo è esattamente il motivo per cui la si propone.

## Una nostra versione

> **Metà immagine per uno**
>
> Ti do due fogli. Su ognuno ci sono quattrocento quadretti da otto millimetri, e ogni quadretto ha una metà nera. Guardali uno alla volta: **non c'è niente**, e non è un modo di dire — un foglio solo può stare insieme a un secondo foglio qualunque e far comparire qualunque cosa.
>
> Sovrapponili facendo combaciare i quattro crocini agli angoli, e tienili contro una finestra. Compare un disegno.
>
> Poi fai questa prova, e scrivi i risultati. **Sposta il foglio davanti di mezzo millimetro alla volta**, e ogni volta guarda quanto si vede ancora:
>
> ```
>  se i fogli sono spostati di  quanto si vede
>  0,0 mm                                  50%
>  0,5 mm                                  41%
>  1,0 mm                                  31%
>  1,5 mm                                  22%
>  2,0 mm                                  12%
>  2,7 mm                                   0%
> ```
>
> I numeri sono calcolati, non misurati: dicono quanto **contrasto** resta, non quanto ci vedi tu. Confronta la tabella con i tuoi occhi e dimmi a che millimetro **tu** smetti di leggere il disegno. Sarà prima o dopo di quello che dice la tabella?
>
> E poi la domanda vera: a un millimetro e mezzo di scarto il contrasto è sceso da 50 a 22, cioè a meno della metà di quello che era, e il disegno si legge ancora. **Perché lo leggi lo stesso?**

Il conto si fa in due modi: una formula, e una simulazione su tremila celle sorteggiate che campiona l'inchiostro punto per punto tenendo conto delle celle vicine. I due metodi concordano entro due punti percentuali, e concordano anche sul fattore tre mezzi, che una derivazione a occhio sbaglia.

L'ultima domanda ha una risposta e non è nella scheda: si legge lo stesso perché il disegno è fatto di forme note e l'occhio ne ha bisogno di poco. È la porta d'ingresso alla stessa idea che regge la voce 383, pareidolia, presa dal lato opposto.

**Tre limiti, dichiarati sul foglio prima e non dopo.** Le celle da 8 mm sono quarantasette volte più larghe del retino tipografico, quindi il grigio non si fonde: si vedono le mezze celle, e il disegno si legge dalla tessitura. Due fogli di carta comune contro una finestra lasciano passare poca luce, e quanto poca non è misurato. E l'allineamento a mano vale un millimetro scarso, che è già un terzo del contrasto perso: **se non funziona non è colpa di chi ha allineato.**

## Da riprendere alla rassegna

**Due vincoli opposti sulla stessa grandezza, misurati, con un rapporto di quarantasette.** La cella deve essere grande perché due fogli si allineino a mano e piccola perché l'occhio fonda le mezze celle in un grigio. Non si può soddisfare tutti e due, e la scelta è già fatta: si tiene il registro e si perde il grigio. **Alla rassegna questo è il primo caso raccolto in cui il vincolo di stampa e il vincolo dell'occhio si contraddicono, e il numero dice di quanto.**

**La stampante non c'entra, ed è il contrario della voce accanto.** Alla voce 389, moiré la precisione di stampa fissa il tetto dell'effetto; qui la stampante avanza risoluzione e a mancare è la mano. Alla rassegna: «dipende dalla precisione di stampa» va sempre scomposto in stampante, carta e mano, perché nel blocco 385-390 le tre cose danno tre risposte diverse.

**Una forma che consegna la propria degradazione insieme all'effetto.** La tabella dello scarto sta sul foglio, davanti, e serve a togliere la colpa a chi allinea. È il rovescio della scheda che promette e basta, e sta accanto alla scheda della voce 375, topologia ricreativa che stampa la contraddizione della propria fonte.

**La riga di differenza.** Alla voce 385, cecità al cambiamento il foglio contiene sei letture e l'occhio non ne prende nessuna. Qui, come alla voce 389, moiré, nessuno dei due fogli contiene niente e l'occhio ne prende una — ma con una differenza dalla voce accanto: là la figura che compare non l'ha decisa nessuno, qui l'ha decisa chi ha riempito il secondo foglio, e non è chi ha stampato il primo.

