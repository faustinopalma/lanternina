# La macchina fotografica

La macchina fotografica di Lanternina parte dalla Seeed Studio XIAO ESP32S3 con espansione Sense acquistata da Fausto. Chi la tiene in mano inquadra un oggetto e preme un pulsante. Il dispositivo acquisisce una fotografia e segnala l'esito con un LED. Il progetto prevede l'invio a lanternina hub attraverso il Wi-Fi di casa.

Al 7 settembre 2026 abbiamo identificato i componenti dalle fotografie e verificato i collegamenti nella documentazione del produttore. Il cablaggio, il firmware fotografico e la ricezione sull'hub devono ancora essere realizzati e provati. Questa sezione descrive il montaggio e il comportamento previsto; non documenta una macchina gia' funzionante.

## Il dispositivo acquistato

![Il kit acquistato: scheda XIAO ESP32S3, espansione Sense con camera OV3660, antenna e connettori non saldati](images/kit-ov3660.jpg)

La foto mostra la scheda base marcata `XIAO-ESP32-S3`, l'espansione Sense, l'antenna a 2,4 GHz e due file di pin ancora separate. La scritta `OV3660` sul cavetto identifica il modulo fotografico. Seeed dichiara per questo sensore una risoluzione massima di 2048 x 1536 pixel; il modello e la risoluzione effettivamente utilizzati andranno confermati dal firmware. Non e' il sensore OV2640 del tutorial di partenza.

L'espansione comprende anche uno slot microSD e un microfono. Il progetto usa la camera e prevede la microSD per le fotografie in attesa di consegna. Il firmware fotografico non inizializzera' il microfono. L'acquisto di una microSD, di un pulsante, di un LED e di una batteria non e' attestato dalle foto.

## Il materiale per pulsante e LED

| Quantita' | Componente | Caratteristica richiesta |
| --- | --- | --- |
| 1 | Pulsante momentaneo | Contatto normalmente aperto, senza ritenuta; due terminali oppure contatti `COM` e `NO` |
| 1 | LED diffuso rosso o ambra | LED ordinario a due terminali, adatto a pochi mA; non un modulo indicatore da 12 V |
| 1 | Resistenza da 470 ohm | Potenza nominale di 0,25 W; in serie al LED |
| Alcuni | Fili flessibili isolati | Corti, come indicazione di montaggio entro circa 15 cm nel contenitore |
| Quanto serve | Guaina termorestringente e supporto | Isolamento dei terminali e fissaggio che impedisca ai fili di tirare le saldature |
| 1 | Cavo USB-C dati | Alimentazione e programmazione durante il collaudo |

Il pulsante deve chiudere un contatto quando viene premuto e riaprirlo al rilascio. Nei pulsanti illuminati i contatti della luce sono separati da quelli dell'interruttore: questa guida usa un LED esterno indipendente.

## Dove saldare sulla tua scheda

![Retro della scheda acquistata, con USB-C in alto e serigrafia dei pin leggibile](images/scheda-retro.jpg)

La vista seguente corrisponde alla seconda fotografia: guardiamo il retro, quello con la scritta `XIAO ESP32S3` e le piazzole `BAT`; teniamo la presa USB-C in alto. Guardando invece il lato dei componenti, destra e sinistra si scambiano.

```text
                   USB-C
             +---------------+
      VUSB   o               o   D0  GPIO1  --> resistenza e LED
      GND    o               o   D1  GPIO2
      3V3    o               o   D2  GPIO3
      D10    o               o   D3  GPIO4  --> pulsante
      D9     o               o   D4  GPIO5
      D8     o               o   D5  GPIO6
      D7     o               o   D6  GPIO43
             +---------------+
                 VISTA RETRO
```

Usiamo tre piazzole laterali della scheda base: `D0`, `D3` e `GND`. Nella foto `D0` e' la prima a destra dall'alto, `D3` la quarta a destra e `GND` la seconda a sinistra. Le sigle sono il riferimento principale: controllale prima di saldare. Le piazzole centrali `BAT`, `D+`, `D-`, `EN` e JTAG non servono a questi collegamenti.

| Funzione | Sigla sulla scheda | GPIO del chip | Configurazione firmware |
| --- | --- | --- | --- |
| Ingresso pulsante | D3 | GPIO4 | `INPUT_PULLUP`; premuto = `LOW` |
| Uscita LED esterno | D0 | GPIO1 | `OUTPUT`; acceso = `HIGH` |
| Ritorno comune | GND | Massa | Collegato sia al pulsante sia al catodo del LED |

`D3` non significa `GPIO3`: nel codice Arduino si usera' `D3` oppure il numero GPIO `4`. Per il LED si usera' `D0` oppure `1`. La selezione della scheda dovra' essere `XIAO_ESP32S3`.

Seeed assegna alla camera GPIO10-18, GPIO38-40, GPIO47 e GPIO48. La microSD usa GPIO7, GPIO8, GPIO9 e GPIO21; il microfono usa GPIO41 e GPIO42. GPIO1 e GPIO4 restano disponibili per questi due collegamenti. Il LED utente integrato e' su GPIO21, condiviso con il chip select della microSD: non lo usiamo come conferma fotografica. Il LED di carica indica lo stato del circuito di alimentazione e non lo scatto.

## Il collegamento del pulsante

Esegui le saldature con USB e batteria scollegati. Collega un terminale del pulsante a `D3` e l'altro a `GND`. Il pulsante non ha polarita'. Se ha tre terminali marcati, usa `COM` e `NO`, lasciando libero `NC`.

```text
  3V3 interno
       |
  pull-up interno al chip, abilitato dal firmware
       |
  D3 / GPIO4 -------- pulsante normalmente aperto -------- GND
```

La resistenza interna mantiene l'ingresso alto quando il pulsante e' rilasciato. Premendo, il contatto porta l'ingresso a massa. Per il prototipo alimentato da USB non serve una resistenza esterna sul pulsante. Non collegare il pulsante a `VUSB`, a 5 V o al positivo della batteria: i GPIO lavorano a 3,3 V e non sono tolleranti a 5 V.

Un pulsante tattile a quattro piedini contiene due coppie gia' unite internamente. A scheda scollegata, usa il multimetro in continuita' per individuare una coppia di terminali che risulti aperta a riposo e chiusa alla pressione. Collega quei due terminali; due piedini della stessa coppia darebbero un ingresso sempre premuto. La disposizione fisica dei piedini da sola non basta a identificarli.

## Il collegamento del LED

Collega `D0` a un capo della resistenza da 470 ohm. Collega l'altro capo all'anodo del LED. Collega il catodo a `GND`, lo stesso ritorno del pulsante.

```text
  D0 / GPIO1 ---- [ 470 ohm ] ---- anodo LED catodo ---- GND
```

Nel LED nuovo l'anodo ha di solito il terminale piu' lungo. Il catodo ha di solito il terminale corto ed e' vicino al lato piatto della base. Se i terminali sono stati tagliati o il contenitore e' diverso, verifica la polarita' con il datasheet o con la funzione diodo del multimetro. La resistenza non ha verso e puo' stare su qualunque lato del LED, purche' sia in serie.

Con uscita a 3,3 V e caduta del LED assunta tra 1,8 e 2,2 V, la corrente calcolata e' tra 2,3 e 3,2 mA: `(3,3 V - Vf) / 470 ohm`. La potenza calcolata nella resistenza resta sotto 5 mW. Sono stime elettriche, non misure sul LED acquistato; luminosita' e caduta reale dipendono dal componente. La resistenza da 0,25 W ha margine rispetto a questo carico.

Il LED e' comandato dal firmware, non dal contatto del pulsante. Collegarlo direttamente al pulsante indicherebbe soltanto che il contatto si e' chiuso, anche con il programma fermo. Collegarlo direttamente al GPIO senza resistenza puo' danneggiare il LED o l'uscita. Un indicatore da pannello a 5 V o 12 V richiede un circuito diverso: non sostituirlo al LED qui descritto.

## L'ordine di montaggio

1. Scollega ogni alimentazione. Identifica `D0`, `D3` e `GND` sulla serigrafia del retro.
2. Prova il pulsante con il multimetro e identifica anodo e catodo del LED.
3. Salda i collegamenti sulle piazzole laterali, oppure salda i connettori del kit e prova su breadboard. Evita ponti di stagno verso le piazzole vicine e la schermatura metallica.
4. Unisci i due ritorni di massa su un piccolo punto di giunzione isolato e porta un solo filo a `GND`. Questo evita di ammassare due fili sulla piazzola piccola.
5. Isola la resistenza e le giunzioni con guaina. Fissa i fili al supporto, lasciando un poco di gioco vicino alla scheda.
6. Controlla in continuita' che `D3` e `GND` si uniscano solo premendo. Verifica che non ci siano ponti metallici tra piazzole adiacenti. Le misure attraverso i semiconduttori della scheda non sono equivalenti a un corto metallico.
7. Monta il modulo camera e l'antenna secondo le istruzioni Seeed, operazione gia' nota. Togli la pellicola protettiva dall'obiettivo, visibile nella prima foto, prima delle prove fotografiche.
8. Alimenta inizialmente soltanto da USB-C. Interrompi la prova se compaiono odore, riscaldamento anomalo o riavvii ripetuti.

Il contenitore deve sostenere il pulsante senza trasferire la pressione alla scheda. Il LED deve essere visibile a chi inquadra, non rivolto verso il soggetto come un flash. La lente, l'antenna e la presa USB-C devono restare libere; distanziali isolanti impediscono contatti tra scheda, viti e batteria.

## Che cosa deve confermare la luce

Il firmware deve distinguere il comando ricevuto dalla fotografia salvata. Proponiamo questa sequenza, da verificare con il dispositivo in mano:

| Evento | LED esterno | Significato |
| --- | --- | --- |
| Attesa, dispositivo alimentato | Spento | Nessuna acquisizione in corso; da solo non distingue attesa da mancanza di alimentazione |
| Pressione stabile riconosciuta | Si accende | Il firmware ha ricevuto il comando |
| Acquisizione e salvataggio | Resta acceso | L'operazione e' in corso |
| JPEG salvato e verificato su microSD | Si spegne per 150 ms, si accende per 500 ms, poi si spegne | La fotografia e' conservata sul dispositivo |
| Acquisizione o salvataggio falliti | Tre impulsi da 150 ms, separati da 150 ms spenti, poi spento | La fotografia non e' stata conservata |

Queste durate sono valori iniziali di progetto, non tempi misurati. L'invio all'hub procede separatamente: la conferma locale non significa che la foto sia stata ricevuta dall'hub o usata nell'attivita'. Nel collaudo elettrico iniziale, un impulso puo' confermare la sola lettura del pulsante, ma quel programma non va presentato come firmware fotografico.

Il firmware dovra' applicare un antirimbalzo iniziale di 30 ms, produrre un solo evento per pressione e richiedere un rilascio stabile prima di riarmarsi. Una pressione lunga non deve generare una raffica. Le pressioni durante acquisizione e segnalazione finale non si accodano. Con alimentazione USB, l'avvio a pulsante gia' premuto attende il rilascio; una futura modalita' di risveglio dal pulsante richiedera' invece una gestione esplicita della causa di risveglio.

Un errore deve interrompere l'operazione entro un tempo massimo configurato; i valori andranno scelti dopo le prime misure. Il programma deve liberare il frame anche in errore e tornare disponibile. Il breve segnale d'errore permette di sapere che la foto manca, ma la sua comprensibilita' resta una prova da fare, non una proprieta' dimostrata.

## Come entra in Lanternina

La macchina serve a fotografare costruzioni, oggetti e lavori che non entrano nello scanner. Chi la usa sceglie il soggetto e il momento dello scatto. Lo scanner resta il percorso gia' esistente per i fogli.

La proposta completa prevede questa successione:

1. Il pulsante avvia una singola acquisizione con il driver `esp32-camera`, configurato per la XIAO Sense e il sensore rilevato. La PSRAM deve essere abilitata; il solo nome della scheda non basta a dimostrare che sia disponibile.
2. Il firmware scrive il JPEG in un file temporaneo su microSD, controlla byte scritti e rilettura, chiude il file e lo promuove nella coda delle foto pronte. Il recupero al riavvio deve distinguere file incompleti e completi; il filesystem FAT da solo non garantisce resistenza a un'interruzione di alimentazione.
3. Il LED conferma il salvataggio. La coda ha un limite esplicito e non sovrascrive silenziosamente fotografie ancora da consegnare. Capacita' e limite saranno fissati dopo aver misurato la dimensione dei JPEG reali.
4. Sulla rete di casa il dispositivo consegna il JPEG a un ricevitore autenticato di lanternina hub. Identita' del dispositivo e identificativo persistente dello scatto consentono di riprovare senza creare copie. Un nome basato solo su `millis()` non sopravvive ai riavvii.
5. L'hub conferma solo dopo aver acquisito durevolmente la responsabilita' del file. La macchina elimina la propria copia dopo quella conferma. Una risposta persa provoca una nuova consegna con lo stesso identificativo, non una nuova foto.
6. L'hub presenta la foto nel percorso deciso per l'attivita'. Una foto ricevuta in ritardo non viene attribuita automaticamente al momento attivo: l'associazione deve essere definita prima dell'integrazione.

Il ricevitore, la coda e l'associazione alle attivita' sono da implementare. Durante le prime prove si useranno oggetti di test. Le fotografie reali resteranno fuori dal repository. Prima dell'uso domestico vanno definite conservazione, cancellazione anche delle copie ancora in coda, accesso del genitore e trattamento delle persone eventualmente inquadrate. La microSD contiene immagini estraibili fisicamente: il contenitore chiuso ne limita l'accesso, ma non equivale a cifrarla.

Le credenziali saranno individuali e revocabili, fuori dai sorgenti. Il trasporto dovra' autenticare anche il ricevitore, per esempio con HTTPS e verifica del certificato; il Wi-Fi di casa non sostituisce questa verifica. La ricezione di un codice HTTP qualsiasi non basta a dichiarare successo: servono lo stato atteso e una conferma riferita allo stesso scatto. Google Drive, WebDAV e FTP non sono dipendenze di questo miniprogetto.

## Alimentazione e autonomia

Il primo prototipo usa USB-C per separare le prove fotografiche dai problemi di alimentazione. La versione portatile richiedera' una batteria ricaricabile LiPo a singola cella, nominalmente 3,7 V, protetta e compatibile con il caricatore della revisione posseduta. Le piazzole `BAT` sono sulla scheda base; questa guida non prescrive ancora il cablaggio della batteria. Non usare `VUSB` o `3V3` al posto di `BAT` e non saldare direttamente sulla cella.

Seeed riporta per la Sense con espansione circa 3 mA in deep sleep, contro 14 microampere per la scheda base: sono valori del produttore, non misure di questa unita'. Non possiamo dedurre l'autonomia dal solo ESP32-S3. Servono misure con camera, microSD, LED e regolazione di alimentazione realmente montati, anche durante i picchi di acquisizione e Wi-Fi.

GPIO4 puo' essere destinato al risveglio in una fase successiva. Prima vanno verificati pull-up mantenuto in sonno o resistenza esterna verso 3V3, causa del risveglio, rilascio del pulsante e prevenzione dei risvegli ripetuti. Il normale `INPUT_PULLUP` del prototipo non costituisce da solo una configurazione di deep sleep.

## Il collaudo

| Prova | Risultato richiesto | Stato al 7 settembre 2026 |
| --- | --- | --- |
| Identificazione dalle foto | XIAO ESP32S3, espansione Sense, scritta OV3660 | Verificato sulle due foto |
| Piedinatura | GPIO1 e GPIO4 disponibili; mappa del retro coerente con Seeed | Verificato su foto e documentazione |
| Conversione delle foto del kit | Due JPEG leggibili, 3024 x 4032 pixel, senza EXIF | Verificato con Pillow |
| Pulsante rilasciato e premuto | GPIO4 rispettivamente alto e basso | Da misurare |
| Dieci pressioni distinte | Dieci eventi, ciascuno con riscontro LED | Da provare |
| Pressione mantenuta per 5 s | Un solo evento, riarmo dopo rilascio | Da provare |
| Accensione USB con pulsante premuto | Nessuno scatto fino al rilascio e alla nuova pressione | Da provare |
| Alternanza tra due soggetti riconoscibili | Ogni file contiene il soggetto attuale, non il frame precedente | Da provare |
| microSD assente o piena | Nessuna conferma di salvataggio e nessuna sovrascrittura | Da provare |
| Wi-Fi assente | Foto salvata localmente e inviata al ritorno della rete | Da provare |
| Risposta dell'hub persa | Nuovo invio dello stesso scatto; una sola acquisizione logica sull'hub | Da provare |
| Alimentazione interrotta durante la scrittura | File incompleto riconosciuto; foto precedenti ancora utilizzabili | Da provare |
| Contenitore chiuso | Pulsante comodo, LED visibile, immagine orientata e leggibile | Da provare |

La prova con soggetti alternati controlla il problema dei frame vecchi descritto nel tutorial. Scartare un frame puo' essere utile in una configurazione, ma non dimostra freschezza per ogni numero di buffer o modalita' di acquisizione. Il risultato richiesto e' una foto del soggetto presente al nuovo scatto.

## Fotografie e fonti

Le due foto sono state fornite da Fausto il 7 settembre 2026. `20260907_135427752_iOS.HEIC` e' diventata `images/kit-ov3660.jpg`; `20260907_135509834_iOS.HEIC` e' diventata `images/scheda-retro.jpg`. La conversione usa Pillow con pillow-heif, qualita' JPEG 95, sottocampionamento cromatico disattivato, orientamento EXIF applicato e metadati EXIF rimossi. Non sono state ridimensionate. Gli originali sono conservati localmente in `private/macchina-fotografica/originali/`, esclusa da Git; la cartella temporanea di provenienza e' stata rimossa prima del commit.

Fonti consultate il 7 settembre 2026:

- [Seeed, XIAO ESP32-S3 Series](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/): modelli, piedinatura, strapping, alimentazione e specifiche dichiarate.
- [Seeed, Pin Multiplexing](https://wiki.seeedstudio.com/xiao_esp32s3_pin_multiplexing/): GPIO occupati da camera, microfono e microSD.
- [Espressif, piedinature CameraWebServer](https://github.com/espressif/arduino-esp32/blob/master/libraries/ESP32/examples/Camera/CameraWebServer/camera_pins.h): riscontro della mappa `CAMERA_MODEL_XIAO_ESP32S3`.
- [Prilchen, macchina fotografica ESP32-S3](https://prilchen.de/diy-fotoapparat-mit-esp32-s3-das-die-bilder-direkt-in-dein-google-drive-schickt/): spunto per l'oggetto con pulsante e LED, e segnalazione del problema del frame precedente. Testo, immagini, codice e contenitore non sono riprodotti qui.

Le motivazioni delle scelte sono in [ideas/macchina-fotografica-xiao.md](../../ideas/macchina-fotografica-xiao.md). La lettura delle fonti e' registrata in [docs/EVIDENCE.md](../EVIDENCE.md#camera-hardware-references-7-september-2026).
