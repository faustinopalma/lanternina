# Confronto dei prompt del 7 settembre 2026

Questa directory contiene tre coppie di attivita sintetiche. `comparison.json` conserva ingressi nei prompt, risposte, riparazioni, documenti finali e primi verdetti. `rejudged.json` conserva una seconda valutazione degli stessi documenti con il protocollo del giudice corretto e il testo completo della sua istruzione.

La baseline e `b60df1c3fbef0fa5a87e1c45107d49bcac206409`; i fingerprint dell'ideatore sono `4358f1f9c9ec` e `8035a0fd81c4`. I metodi sono fissi dentro ogni coppia. La selezione del metodo non viene misurata. Generazione, riparazioni, controlli e sicurezza usano `panel.devising.devise_experience`.

Tutte le sei attivita sono state accettate. La baseline richiede una riparazione su tre; la revisione ne richiede due su tre. Il confronto con i primi giudizi dura 1099,9 secondi, la rivalutazione 139,8 secondi. Queste sono misure del programma e non della durata dell'attivita umana.

Le nuove costruzioni e i nuovi disegni mantengono il proprio metodo invece di diventare misteri sulle intenzioni di un personaggio. Il campione non misura gradimento, correttezza delle immagini o continuita dell'esperienza dopo `ask`. Il giudice conserva falsi positivi; non sommare le sue segnalazioni come punteggio di qualita.

Il resoconto, i limiti e i prossimi passi sono in [ideas/13-prompts-and-simulation.md](../../../ideas/13-prompts-and-simulation.md). Il programma conservato e [research/compare_prompts.py](../../compare_prompts.py).