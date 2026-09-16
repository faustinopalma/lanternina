# 01 - The route to the kiosk

## Household brief

The adolescent is interested in outings and maps, can follow a broad line with a finger and can distinguish a bridge from a crossed-out bridge after an adult names them. Supply paper and a broad pencil. The park is fictional. Nothing requires reading street names or interpreting a compass. The adult can read the instruction and help aim the camera. Use at most two printed sheets. Keep the first map throughout.

## Parent output

Title: La strada per il chiosco

Overview: Si segue una strada su una mappa e si sceglie una sosta lungo il percorso. La stampante prepara una mappa e un foglio con due oggetti da aggiungere. Alla fine resta il percorso disegnato. Servono solo carta e matita. Il ragazzo deve distinguere due strade; il genitore può indicare il punto di partenza senza scegliere il percorso.

Themes: parco, percorsi, disegno.

## Script output

Il parco è inventato. Un ingresso e un chiosco sono collegati da due strade. Un ruscello attraversa entrambe: il ponte a sinistra è chiuso, quello a destra è aperto. Il ragazzo cerca un percorso percorribile e lo segna. Se arriva una strada continua attraverso il ponte aperto, il seguito propone di aggiungere una panchina oppure una fontana. Il ragazzo sceglie un oggetto e lo disegna vicino alla strada sul foglio originale. Il seguito non ridisegna la mappa. Si conclude conservando il percorso e l'aggiunta; non serve raccontare una gita avvenuta davvero.

## Cycle 1

### Display - cycle 1

```text
Parti dall'ingresso della mappa.
Segui una strada fino al chiosco.
```

### Page - cycle 1

```json
{"kind":"map","title":"La strada per il chiosco","note":["Parti dall'ingresso.","Disegna la strada fino al chiosco.","Il ponte con la croce è chiuso.","Fotografa la mappa e tienila sul tavolo."],"spaces":[],"illustration":"A simple park map. Entrance at bottom centre, kiosk at top centre. Exactly two broad paths connect them, left and right, with no other junctions. A horizontal stream crosses both paths. Each crossing has one bridge. The left bridge has a large black X; the right bridge is clear. One entrance arch and one small kiosk, visibly distinct. No labels, compass, extra paths or decorative symbols. Leave space beside the right path for a later drawing."}
```

### Image prompt - cycle 1

```text
Draw one complete portrait activity page, 1024 by 1536 pixels, on pure white paper. Use clear black lines, a plain large sans-serif font and generous space. No colour-dependent clues, grey wash, QR code, decorative border or extra words. Print the title exactly: "La strada per il chiosco". Under it print these four sentences on separate lines: "Parti dall'ingresso." "Disegna la strada fino al chiosco." "Il ponte con la croce è chiuso." "Fotografa la mappa e tienila sul tavolo." Below the words, draw an entrance arch at bottom centre and a small kiosk at top centre. Exactly two broad continuous paths connect the arch to the kiosk: one bows left, one bows right. A horizontal stream runs across the middle of the map. Each path crosses it on one bridge. Put a large black X directly across the LEFT bridge; leave the RIGHT bridge unobstructed. The paths meet only at the entrance and kiosk. There are no alternative crossings, gaps or branch roads. Leave white space beside the right path for a later addition. Keep the whole map and both endpoints visible. Do not print labels on the map. Make the X different from any line in the bridge structure. The only printed words are the title and four sentences above.
```

### Help - cycle 1

```text
Appoggia un dito sull'ingresso.
Prova una strada. Guarda quale ponte incontri.
```

### Hypothetical return - cycle 1

A pencil line starts at the entrance, follows the right path across the clear bridge and reaches the kiosk. No other additions are visible. The reader reports the line and its endpoints, not that the adolescent understood the rule or worked unaided.

## Cycle 2

### Display - cycle 2

```text
La linea arriva al chiosco dal ponte aperto.
Scegli una sosta da aggiungere alla mappa.
```

### Page - cycle 2

```json
{"kind":"notebook","title":"Una sosta lungo la strada","note":["Scegli la panchina oppure la fontana.","Disegnala vicino alla tua strada, sulla mappa.","Puoi usare una forma semplice.","Fotografa di nuovo la mappa."],"spaces":[],"illustration":"Two large separate reference drawings of equal visual weight: a plain park bench on the left and a drinking fountain with basin and tap on the right. Both are simple black outlines that can be copied loosely. No scenery, map, sample route, labels or selection marks."}
```

### Image prompt - cycle 2

```text
Draw a complete portrait A4-style page on pure white paper at 1024 by 1536 pixels. Use large plain black type and simple black outlines. Print exactly the title "Una sosta lungo la strada" and these four sentences: "Scegli la panchina oppure la fontana." "Disegnala vicino alla tua strada, sulla mappa." "Puoi usare una forma semplice." "Fotografa di nuovo la mappa." Beneath the text, show two equally large reference drawings separated by ample white space: a park bench on the left and a drinking fountain with a basin and tap on the right. Use only a few clear lines. Do not circle either object, add choice letters, redraw a map or add any other text. These are copying references, not a completed answer. Keep all text and drawings within generous print margins.
```

### Hypothetical return - cycle 2

The original route is still visible. A new rough drawing with a seat and backrest appears beside its lower right section. The form is sufficiently clear to describe as a bench; its scale and location within the real world are not assessed.

## Closing output

```text
Hai aggiunto una panchina vicino alla strada.
La mappa è pronta. Puoi tenerla.
```

## Alternative returns

- A line uses the crossed-out bridge: say "La linea passa sul ponte con la croce. Quel ponte è chiuso. Prova l'altra strada con il dito." Keep the same map. Offer one retry, then close on the attempted route without claiming the chiosco was reached.
- A valid route is drawn outside the two paths and clearly goes around the stream's visible end: accept it if the image really permits it. This is an image-design defect, not a wrong answer to punish.
- A fountain is added instead of a bench: close with "Hai aggiunto una fontana vicino alla strada. La mappa è pronta." Do not print or mention a bench.
- The new shape cannot be identified: say "Vedo un'aggiunta vicino alla strada. La mappa può restare così." Do not force a verbal explanation to earn closure.
- The map is unchanged: offer "Puoi seguire una strada con il dito, senza disegnarla." A parent's report may record that action; a later unchanged photograph cannot prove it occurred.
- The photograph cuts off a bridge: request one full-page photograph; do not call the route wrong or blank.
- Stop or end time: "Lasciamo la mappa così. Per oggi abbiamo finito."

## Comparison checks

The illustration is the evidence. Inspect connectivity and X placement before offering the page. A continuation must inspect the line rather than branch merely on the presence of ink. The second exchange adds something to the same route instead of introducing a new route puzzle. A bench and a fountain are both valid choices.
