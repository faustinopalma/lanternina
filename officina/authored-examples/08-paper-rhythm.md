# 08 - A rhythm on paper

## Household brief

The adolescent enjoys making gentle sounds and agrees to try a short pattern with another person. Confirm tolerance for the two proposed sounds rather than assuming it. Use a stable table and bare hands only. An adult demonstrates one gentle tap and one quiet clap, without asking for imitation until the adolescent wants to try. The adult can track each symbol with a finger at an unhurried pace; precise tempo, counting, hearing an audio prompt and left-to-right reading are not prerequisites. Two printed sheets. No microphone or sound recording is used.

## Parent output

Title: Un ritmo da cambiare

Overview: Si sceglie un suono e si prova una breve sequenza con una pausa. La stampante prepara i due gesti e poi la sequenza scelta. Resta un foglio per riprovarla insieme. Bastano mani, tavolo e matita. Il genitore indica i gesti uno alla volta. Se il suono dà fastidio, si può fare il movimento senza produrlo o smettere.

Themes: suoni, pause, sequenze.

## Script output

Il genitore mostra un colpo leggero sul tavolo e un battito piano di mani. Il ragazzo sceglie quale usare, segnando il disegno corrispondente. Nel percorso principale sceglie il tavolo. Il seguito stampa tre gesti: un colpo, mani ferme, un colpo. Il genitore li indica in ordine mentre la persona prova. Il ragazzo può trasformare uno dei colpi in pausa cerchiandolo. Nel secondo ritorno il colpo finale è cerchiato. La sequenza modificata resta sul foglio originale. Il sistema descrive la modifica e non afferma di avere ascoltato o valutato il ritmo.

## Cycle 1

### Display - cycle 1

```text
Prova i due suoni con chi è con te.
Scegli quello che vuoi usare.
```

### Page - cycle 1

```json
{"kind":"notebook","title":"Scegli un suono","note":["Puoi dare un colpo leggero sul tavolo.","Oppure puoi battere piano le mani.","Cerchia il gesto che vuoi usare.","Fotografa il foglio con la scelta."],"spaces":[],"illustration":"Two large equally prominent action drawings side by side. Left: one hand gently tapping a tabletop once, with a short contact mark. Right: two hands making one gentle clap. No music notation, repeated-motion trails, numbers, choice labels, ratings or selected option. Leave ample room to circle either drawing."}
```

### Image prompt - cycle 1

```text
Create a complete portrait page at 1024 by 1536 pixels, pure white with large plain black text. Print exactly the title "Scegli un suono" and four lines: "Puoi dare un colpo leggero sul tavolo." "Oppure puoi battere piano le mani." "Cerchia il gesto che vuoi usare." "Fotografa il foglio con la scelta." Below, place two equally large separated outline action drawings. On the left, one hand touches a horizontal tabletop with one short contact mark. On the right, two hands meet in one gentle clap. Use clear anatomy and no exaggerated force. Leave space around each drawing for a broad circle. Do not add letters, music notes, numbers, labels, rewards or any other text. No option is preselected.
```

### Help - cycle 1

```text
Puoi scegliere anche senza provare il suono.
Indica il gesto a chi è con te.
```

### Hypothetical return - cycle 1

The tabletop-tap drawing is circled. The clap drawing is unchanged. The choice is known; whether either sound was tried is unknown.

## Cycle 2

### Display - cycle 2

```text
Hai scelto il colpo sul tavolo.
Prova la sequenza con chi è con te.
```

### Page - cycle 2

```json
{"kind":"notebook","title":"Un colpo e una pausa","note":["Segui i tre gesti con chi è con te.","Dai un colpo, tieni ferme le mani, dai un colpo.","Puoi cerchiare un colpo per trasformarlo in pausa.","Fotografa il foglio che vuoi tenere."],"spaces":[],"illustration":"One wide horizontal sequence of three large distinct action drawings: hand tapping a tabletop, two hands resting still on that tabletop, hand tapping again. Connect drawings left to right with two simple arrows. The tapping drawings have a small contact mark; resting hands have none. Leave room to circle either tapping drawing. No numbers, musical notation or extra words."}
```

### Image prompt - cycle 2

```text
Draw a complete portrait page on pure white at 1024 by 1536 pixels. Use large simple black text. Print the title "Un colpo e una pausa" and exactly these four lines: "Segui i tre gesti con chi è con te." "Dai un colpo, tieni ferme le mani, dai un colpo." "Puoi cerchiare un colpo per trasformarlo in pausa." "Fotografa il foglio che vuoi tenere." Under the text, make a spacious horizontal row of exactly three outlined gestures. First: one hand gently tapping a tabletop, with a small contact mark. Middle: two hands resting still on the tabletop, with no motion or contact marks. Last: the same one-hand tap as the first. Two simple arrows show the order. Leave white space to circle a tapping gesture without touching the next. No coloured coding, numerals, music notation, additional text or pre-drawn selection circles.
```

### Hypothetical return - cycle 2

The final tapping drawing is circled; the first tap and middle resting-hands drawing are unchanged. The circle means a requested pause under the stated rule. It is not evidence that a sound was heard or omitted in an actual performance.

## Closing output

```text
Hai trasformato l'ultimo colpo in una pausa.
Il foglio resta pronto per riprovare insieme.
```

## Alternative returns

- The clap is chosen first: print clap, resting hands, clap, and change the visible instruction accordingly. A tabletop sequence would ignore the return.
- The sequence is unchanged and the person wants it: keep it. Changing a beat is optional.
- Both tapping drawings are circled: the result can be an all-pause sequence. Ask whether that is what the person wants; do not declare an error or secretly restore a sound.
- The resting-hands drawing is circled: its meaning is uncertain under this rule. Ask once whether to keep the pause or change something. Do not infer a hidden new sound.
- The photograph is blurred: keep the marked gesture unknown and offer one clearer picture, or end without interpreting the mark.
- A parent reports that the person only watched: record that report if needed; do not praise a performance that did not occur.
- Stop, discomfort reported by the person or end time: "Fermiamo i suoni. Il foglio può restare qui."

## Comparison checks

The image must distinguish contact from rest without a written label for each beat. The system observes a graphic arrangement, not audio, rhythm accuracy, attention or motor coordination. Participation can be observation or silent movement. No metronome, test of memory or requirement to repeat until correct is added.
