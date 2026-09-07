# Il pannello nel sito pubblico

Il 7 settembre 2026 il genitore ha chiesto di mostrare il pannello, chiarire che il numero degli schermi e configurabile e descrivere in fondo al sito promemoria e quadri. Le introduzioni italiana e inglese ora mostrano due sezioni dell'interfaccia attuale: attivita in attesa e dispositivi. Le catture provengono da `web/src/main.tsx` in modalita locale `?preview`, con `web/src/test/fakeApi.ts`: dati inventati, nessun accesso a una casa reale. Il campione di attivita resta in italiano anche nella cattura dell'interfaccia inglese e la didascalia lo dichiara.

Le immagini sono mostrate una per volta a larghezza piena e si aprono alla risoluzione originale. Questa scelta occupa piu spazio delle miniature affiancate, ma permette di riconoscere i controlli di approvazione e assegnazione. Le copie WebP senza perdita misurano 1200 per 900 pixel. Le prime catture del browser integrato erano tagliate e sono state sostituite dopo l'ispezione.

`panel/devices.py::Thing.jobs` e `InventoryStore.assign` consentono piu compiti per dispositivo. Il registro non impone una coppia di schermi. Il sito distingue quindi la dotazione del prototipo dal numero configurabile di dispositivi; non promette una capacita illimitata misurata.

`devices/trmnl_byos.py` sceglie il contenuto tra i compiti assegnati: promemoria, istruzioni dell'attivita, quadro, in quest'ordine. Le segnalazioni di batteria e identificazione hanno una priorita ulteriore. Promemoria e quadri non sono soltanto un ripiego fuori dall'attivita: schermi dedicati possono mostrarli contemporaneamente, e un promemoria puo comparire sopra un'attivita sullo stesso schermo. `devices/show_reminders.py` applica una finestra di trenta minuti, limitata dalla mezzanotte; la pressione toglie il promemoria senza registrare l'esecuzione del compito.

La build Astro e `site/check-build.py` passano. Il browser ha verificato caricamento delle quattro immagini, collegamenti alle versioni intere, sezioni extra in fondo e assenza di overflow nelle due lingue a 1280 e 390 pixel. Il cambiamento riguarda la descrizione pubblica: non modifica le priorita dei contenuti, il pannello o il codice dell'hub.
