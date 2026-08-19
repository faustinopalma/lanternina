/* The words the parent reads. The catalogs are data — `it.json` and `en.json` — and this
 * file is the only logic around them.
 *
 * Adding a language means adding one JSON file and one entry in CATALOGS. The selector
 * builds itself from these keys, and nothing else in the panel changes.
 *
 * Deliberately absent: anything that reaches the adolescent. The display and the paper
 * follow the household's
 * content language, which the parent sets once in the settings. It must never follow a
 * browser preference — a parent switching their phone to English would otherwise silently
 * change what arrives on paper, and content approved in one language is not approved in
 * another.
 *
 * Relative times are not in the catalogs either. Intl.RelativeTimeFormat already knows how
 * to say them in any language, plurals included, so a new language gets them for free.
 */
import {
  createContext,
  use,
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import en from "./en.json";
import it from "./it.json";

export type MessageKey = keyof typeof it;

// Typed rather than checked at runtime: a key present in one catalog and missing from the
// other stops the build. tests/test_web_i18n.py says the same thing from outside.
const CATALOGS: Record<string, Record<MessageKey, string>> = { it, en };

export const LANGUAGES = Object.keys(CATALOGS);

// Endonyms: a language names itself the same way in every catalog, so these are not
// translated strings and have no catalog entry.
export const LANGUAGE_NAMES: Record<string, string> = { it: "Italiano", en: "English" };

const DEFAULT_LANGUAGE = "it";
const STORAGE_KEY = "lanternina.language";

/* A display preference, not anything about a person. Private-mode browsers throw on access, and
 * forgetting the choice is a better outcome than a panel that does not load. */
function stored(): string | null {
  try {
    return window.localStorage.getItem(STORAGE_KEY);
  } catch {
    return null;
  }
}

/** The parent's choice, then the browser's, then the default. */
function detect(): string {
  const saved = stored();
  if (saved !== null && LANGUAGES.includes(saved)) return saved;
  for (const tag of navigator.languages ?? [navigator.language ?? ""]) {
    const base = String(tag).toLowerCase().split("-")[0] ?? "";
    if (LANGUAGES.includes(base)) return base;
  }
  return DEFAULT_LANGUAGE;
}

export type Vars = Record<string, string | number>;

function translate(language: string, key: MessageKey, vars?: Vars): string {
  const table = CATALOGS[language] ?? CATALOGS[DEFAULT_LANGUAGE]!;
  let text = table[key] ?? CATALOGS[DEFAULT_LANGUAGE]![key];
  // Show the key rather than nothing: a gap in a catalog has to be visible.
  if (text === undefined) return key;
  if (vars !== undefined) {
    for (const [name, value] of Object.entries(vars)) {
      text = text.replaceAll(`{${name}}`, String(value));
    }
  }
  return text;
}

export interface Words {
  language: string;
  setLanguage: (language: string) => void;
  t: (key: MessageKey, vars?: Vars) => string;
  /** "5 minuti fa" or "5 minutes ago", without either phrase being written down. */
  ago: (seconds: number) => string;
  /** A date the parent can read, in whatever language is current. */
  dateTime: (seconds: number) => string;
}

const WordsContext = createContext<Words | null>(null);

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState(detect);

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  const setLanguage = useCallback((next: string) => {
    if (!LANGUAGES.includes(next)) return;
    setLanguageState(next);
    try {
      window.localStorage.setItem(STORAGE_KEY, next);
    } catch {
      // Not remembering the choice is better than failing to honour it now.
    }
  }, []);

  const words = useMemo<Words>(
    () => ({
      language,
      setLanguage,
      t: (key, vars) => translate(language, key, vars),
      ago: (seconds) => {
        const format = new Intl.RelativeTimeFormat(language, { numeric: "auto" });
        const minutes = Math.round(seconds / 60);
        if (minutes < 90) return format.format(-minutes, "minute");
        const hours = Math.round(minutes / 60);
        if (hours < 36) return format.format(-hours, "hour");
        return format.format(-Math.round(hours / 24), "day");
      },
      dateTime: (seconds) =>
        seconds
          ? new Intl.DateTimeFormat(language, {
              dateStyle: "medium",
              timeStyle: "short",
            }).format(new Date(seconds * 1000))
          : "",
    }),
    [language, setLanguage],
  );

  return <WordsContext value={words}>{children}</WordsContext>;
}

export function useWords(): Words {
  const words = use(WordsContext);
  if (words === null) throw new Error("useWords outside LanguageProvider");
  return words;
}
