/* A display preference, not anything about a person. Private-mode browsers throw on access, and
 * forgetting the choice is a better outcome than a panel that does not load. */

export function readStored(key: string): string | null {
  try {
    return window.localStorage.getItem(key);
  } catch {
    return null;
  }
}

export function writeStored(key: string, value: string): void {
  try {
    window.localStorage.setItem(key, value);
  } catch {
    // Not remembering the choice is better than failing to honour it now.
  }
}
