/* Reading the exercise body the content agent produces.
 *
 * The keys are English so that the household's content language stays a setting rather
 * than a property of the data. Bodies approved before 18 August 2026 carry Italian keys
 * and are not rewritten: the safety seal covers the body byte for byte, so renaming a key
 * inside stored content would invalidate it, and re-sealing would mint an approval the
 * parent never gave. This reader accepts both spellings. The same fallback exists in
 * Python, in `shared/exercise.py`, because the display renders the same bodies.
 */

export interface Exercise {
  question?: string;
  choices?: string[];
  answer?: string;
  /* Read only: the spelling a body produced before the rename still carries. */
  domanda?: string;
  scelte?: string[];
  risposta?: string;
}

export interface Sheet {
  title?: string;
  instructions?: string;
  exercises?: Exercise[];
  titolo?: string;
  istruzioni?: string;
  esercizi?: Exercise[];
}

export function sheetTitle(sheet: Sheet): string {
  return sheet.title ?? sheet.titolo ?? "";
}

export function sheetInstructions(sheet: Sheet): string {
  return sheet.instructions ?? sheet.istruzioni ?? "";
}

export function sheetExercises(sheet: Sheet): Exercise[] {
  return sheet.exercises ?? sheet.esercizi ?? [];
}

export function exerciseQuestion(entry: Exercise): string {
  return entry.question ?? entry.domanda ?? "";
}

export function exerciseChoices(entry: Exercise): string[] {
  return entry.choices ?? entry.scelte ?? [];
}
