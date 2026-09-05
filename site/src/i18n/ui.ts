/** Everything that appears in both trees, in both languages.
 *
 * Keeping the two side by side in one file rather than in two is deliberate: a string that
 * exists in one language and not the other is a type error here, and would otherwise be a
 * page that quietly renders in the wrong language.
 */

export const LANGS = ["en", "it"] as const;
export type Lang = (typeof LANGS)[number];

export const OTHER: Record<Lang, Lang> = { en: "it", it: "en" };

export const LOCALE: Record<Lang, string> = { en: "en_GB", it: "it_IT" };

export const LANG_NAME: Record<Lang, string> = { en: "English", it: "Italiano" };

/** The pages, in sidebar order. `slug` is the directory under /<lang>/. */
export const PAGES = [
  { slug: "", key: "overview" },
  { slug: "flows", key: "flows" },
  { slug: "identity", key: "identity" },
  { slug: "status", key: "status" },
] as const;

export type PageKey = (typeof PAGES)[number]["key"];

type Dict = Record<Lang, string>;

export const NAV: Record<PageKey, Dict> = {
  overview: { en: "Overview", it: "Che cos'è" },
  flows: { en: "How it flows", it: "Come funziona" },
  identity: { en: "Identity and access", it: "Identità e accessi" },
  status: { en: "What is built", it: "Cosa c'è davvero" },
};

export const NAV_NOTE: Record<PageKey, Dict> = {
  overview: { en: "The system in one page", it: "Il sistema in una pagina" },
  flows: { en: "Three diagrams", it: "Tre diagrammi" },
  identity: { en: "Two tenants, two audiences", it: "Due tenant, due audience" },
  status: { en: "Running, and not", it: "Ciò che gira e ciò che no" },
};

export const UI = {
  tagline: {
    en: "An afternoon on paper, invented for one person and approved by a parent",
    it: "Un pomeriggio su carta, inventato per una persona e approvato da un genitore",
  },
  skip: { en: "Skip to content", it: "Salta al contenuto" },
  menu: { en: "Menu", it: "Menu" },
  sections: { en: "Sections", it: "Sezioni" },
  langGroup: { en: "Language", it: "Lingua" },
  sourceNote: {
    en: "A project built in one house. The code, the measurements and the open problems are public.",
    it: "Un progetto costruito in una casa. Il codice, le misure e i problemi aperti sono pubblici.",
  },
  repo: { en: "Source on GitHub", it: "Il codice su GitHub" },
  privacy: {
    en: "This site sets no cookies, collects no statistics, and loads nothing from anybody else's server.",
    it: "Questo sito non usa cookie, non raccoglie statistiche e non carica niente da altri server.",
  },
  next: { en: "Next", it: "Avanti" },
  prev: { en: "Back", it: "Indietro" },
} satisfies Record<string, Dict>;

export const REPO = "https://github.com/faustinopalma/lanternina";

export function pathFor(lang: Lang, slug: string): string {
  return slug ? `/${lang}/${slug}/` : `/${lang}/`;
}
