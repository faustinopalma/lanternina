# La macchina fotografica con XIAO ESP32S3 Sense

Fausto ha acquistato una XIAO ESP32S3 con espansione Sense e camera OV3660. Il 7 settembre 2026 le due fotografie del kit hanno permesso di leggere il modello della scheda e la sigla sul cavetto. La [sezione dedicata](../docs/macchina-fotografica/README.md) descrive il cablaggio del pulsante e del LED e conserva i JPEG del kit.

## Che cosa aggiunge al pomeriggio

La macchina permette di restituire una costruzione, un oggetto trovato o un disegno appeso. Lo scanner raccoglie gia' i fogli; la camera rende possibile scegliere qualcosa che resta nel suo posto. Il primo uso da provare e' fotografare una costruzione per conservarne un'immagine prima di modificarla. Il secondo e' portare due fotografie di dettagli a una successiva attivita' di confronto.

Il pulsante assegna lo scatto a chi tiene la macchina. Un LED conferma l'azione senza richiedere un menu. Il costo di una macchina senza schermo e' l'incertezza dell'inquadratura: la forma del contenitore, una distanza di lavoro provata e un eventuale mirino ottico devono essere valutati su fotografie reali. L'assenza di uno schermo non garantisce che la foto riesca.

La scelta riprende la direzione portatile annotata il 25 agosto in [ideas/06-capture.md](06-capture.md). La vecchia postazione fissa resta una ricerca storica. Le regole di progetto sono in revisione; il cablaggio non dipende dal ripristino dei suoi precedenti divieti.

## I collegamenti scelti

Il pulsante chiude `D3/GPIO4` verso massa, con pull-up interno durante il prototipo USB. Il LED esterno usa `D0/GPIO1`, una resistenza da 470 ohm e il ritorno a massa. Questa scelta lascia liberi i collegamenti della camera e della microSD e costa due GPIO.

Il tutorial di Prilchen usa `D2/GPIO3` per il LED. GPIO3 e' anche uno strapping pin che seleziona la sorgente JTAG all'avvio. Il collegamento del tutorial non e' per questo automaticamente guasto, ma GPIO1 evita di caricare quel pin senza richiedere componenti aggiuntivi. La mappa Seeed e la foto del retro permettono di verificare la scelta prima di saldare.

Il LED integrato usa GPIO21, che l'espansione impiega anche per il chip select della microSD. Un LED esterno resta visibile sul contenitore e non interferisce con quel segnale; costa un componente, una resistenza e il cablaggio.

## Che cosa significa eseguito

Una luce collegata al pulsante confermerebbe solo la chiusura del contatto. La luce comandata dal firmware puo' invece confermare che il programma ha ricevuto il comando. La sequenza finale di conferma deve arrivare dopo il salvataggio verificato del JPEG, non dopo la sola pressione o una chiamata fallita alla camera.

La guida propone luce continua durante l'operazione, un impulso finale piu' lungo dopo il salvataggio e tre impulsi brevi se il salvataggio fallisce. Le durate sono iniziali e non misurate. Questa distinzione rende osservabile la perdita di uno scatto, ma chiede di riconoscere due sequenze: va provata prima di fissarla come interfaccia.

## La foto deve poter aspettare

Proponiamo di salvare prima su microSD e consegnare poi all'hub. Questo permette di fotografare anche quando il Wi-Fi manca, ma introduce una copia fisica da proteggere e cancellare. La conferma dello scatto resta locale; la ricevuta dell'hub riguarda un passaggio successivo.

La sola RAM semplificherebbe la gestione dei dati, ma perderebbe la foto al riavvio o all'esaurimento della batteria. Il documento hardware aveva gia' separato acquisizione fuori casa e invio sulla rete domestica. La coda persistente rende questa possibilita' concreta, senza dichiararla gia' implementata.

L'hub e' il destinatario proposto perche' coordina gia' gli strumenti della casa. Questa scelta evita credenziali di un archivio cloud nella macchina, ma richiede un ricevitore autenticato, conferme durevoli e deduplicazione. Nessuno di questi elementi nasce dal semplice collegamento al Wi-Fi.

L'associazione alle attivita' resta da definire. Una fotografia scattata durante un'attivita' e consegnata dopo non appartiene necessariamente all'attivita' aperta al momento dell'arrivo. Prima dell'integrazione dovremo scegliere come conservare il contesto dello scatto e come presentare fotografie senza un contesto certo.

## Da dove partire

La prima prova e' elettrica: pulsante su GPIO4 e LED su GPIO1, alimentazione USB, un evento per pressione. La seconda acquisisce fotografie di due oggetti alternati e misura pressione, disponibilita' del frame, fine scrittura e riscontro LED. La terza interrompe rete e alimentazione su una microSD di prova e verifica recupero e consegna. L'integrazione con l'attivita' segue queste prove. Batteria e sonno vengono dopo, perche' cambiano avvio, latenza e recupero.

Usiamo il driver Espressif `esp32-camera` per acquisire JPEG. Il tutorial segnala un frame precedente restituito allo scatto successivo; la prova con oggetti alternati deve verificare il problema nella configurazione scelta. Non assumiamo che scartare sempre un singolo frame sia una soluzione universale.

## Fatto quando

La documentazione e' pronta quando i collegamenti corrispondono alla scheda fotografata, le fonti sono rintracciabili, le foto sono leggibili senza HEIC e la cartella temporanea e' rimossa. Questi controlli sono stati eseguiti il 7 settembre 2026.

Il prototipo sara' pronto quando una pressione produce una fotografia attuale, una pressione lunga ne produce una sola, il LED conferma soltanto uno stato realmente raggiunto e un invio ripetuto non duplica la fotografia sull'hub. La macchina domestica richiedera' inoltre un contenitore provato, autonomia misurata e una procedura di cancellazione che comprenda dispositivo e hub. Nessuna di queste prove fisiche e' stata eseguita in questa sessione.
