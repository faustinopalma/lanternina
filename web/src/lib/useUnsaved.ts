import { useState } from "react";

/** Whether the form holds anything the house has not been told yet.
 *
 * The confirmation a parent needs after saving is not a sentence — it is the Save button
 * going quiet. Grey means the house has what is on the screen; live means it does not yet.
 * That answers "did it go through" and "have I already saved this" with one control, and it
 * answers them without anything appearing, moving or asking to be dismissed.
 *
 * The comparison is on the serialised values rather than on a flag set by every field,
 * because a flag is set in as many places as there are inputs and is forgotten in one of
 * them. Typing a value back to what it was leaves the button grey, which is right: there is
 * nothing to tell the house.
 *
 * Call ``saved()`` after the write returns, never before. The snapshot it takes is this
 * render's values, which are the ones that were sent.
 */
export function useUnsaved<T>(current: T): { changed: boolean; saved: () => void } {
  const now = JSON.stringify(current);
  const [kept, setKept] = useState(now);
  return { changed: now !== kept, saved: () => setKept(now) };
}
