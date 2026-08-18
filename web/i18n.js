/* The words the parent reads, one catalog per language.
 *
 * Adding a language means adding one object to CATALOGS. The selector builds itself from
 * these keys, and nothing else in the panel changes.
 *
 * Deliberately absent: anything she sees. The display and the paper follow the household's
 * content language, which the parent sets once. It must never follow a browser preference —
 * a parent switching their phone to English would otherwise silently change what she reads,
 * and content approved in one language is not approved in another.
 *
 * Relative times are not in the catalogs either. Intl.RelativeTimeFormat already knows how
 * to say them in any language, plurals included, so a new language gets them for free.
 */

// Wrapped because this file and app.js are classic scripts sharing one global scope: a
// bare `function t()` here collides with `const { t } = ...` there, and the collision is a
// SyntaxError that stops the other file from running at all.
(function () {

const CATALOGS = {
  it: {
    name: "Italiano",
    strings: {
      "lede.checking": "Sto controllando se hai già effettuato l'accesso.",
      "lede.ready": "Il pannello è pronto. Sto caricando i dati.",
      "lede.signedout": "Non hai ancora effettuato l'accesso.",
      "lede.in": "Sei dentro.",
      "lede.pending": "Accesso riuscito, account non ancora abilitato.",
      "lede.failed": "Qualcosa non ha funzionato.",

      "loading.moment": "Un momento.",

      "signin.title": "Accesso",
      "signin.body": "Per usare il pannello serve un account. Puoi crearlo al primo accesso.",
      "signin.button": "Entra",
      "signin.as": "Accesso effettuato come {user}.",
      "signin.anon": "Accesso effettuato.",
      "signout": "Esci",

      "panel.title": "Pannello",
      "connecting.loading": "Caricamento dei dati",
      "connecting.note":
        "Puoi lasciare aperta questa pagina. Il servizio può avviarsi da zero mentre il pannello è già visibile.",

      "pending.title": "Account in attesa",
      "pending.body":
        "L'accesso è riuscito. L'account però non è ancora abilitato: serve che una persona lo approvi.",
      "pending.note":
        "Non c'è niente da fare da qui. Questa pagina non cambierà da sola: ricaricala quando l'approvazione è avvenuta.",

      "facts.status": "Stato",
      "facts.account": "Account",
      "facts.household": "Nucleo",

      "proposals.title": "Da approvare",
      "proposals.note":
        "Niente di tutto questo è già arrivato a lei. Quello che approvi resta pronto e viene mostrato più avanti, quando serve.",
      "proposals.loading": "Sto caricando le proposte.",
      "proposals.unreadable": "Non riesco a leggere le proposte adesso.",
      "proposals.empty": "Nessuna proposta in attesa.",
      "proposals.decideFailed": "Non sono riuscito a registrare la decisione. Riprova più tardi.",
      "action.approve": "Approva",
      "action.refuse": "Rifiuta",

      "kind.exercise": "Foglio da stampare",
      "kind.routine_prompt": "Promemoria sul display",
      "kind.feedback": "Risposta dopo un foglio",
      "kind.schedule": "Piano della giornata",
      "kind.print_layout": "Impaginazione",

      "themes.title": "Temi dei quadri",
      "themes.note":
        "Il display disegna un quadro nuovo su uno di questi temi. Approvi il tema, non la singola immagine: quello che togli non viene più usato.",
      "themes.placeholder": "per esempio: gatti che dormono",
      "themes.aria": "Nuovo tema",
      "themes.add": "Aggiungi",
      "themes.remove": "Togli",
      "themes.removeTitle": "Togli “{label}”",
      "themes.removeFailed": "Non sono riuscito a togliere il tema. Riprova più tardi.",
      "themes.loading": "Sto caricando i temi.",
      "themes.unreadable": "Non riesco a leggere i temi adesso.",
      "themes.empty": "Nessun tema. Finché la lista è vuota il display usa i temi di partenza.",
      "themes.badLabel": "Questo tema non va bene.",
      "themes.addFailed": "Non riuscito.",

      "devices.title": "Dispositivi",
      "devices.note":
        "Lo stato dei display. Qui compaiono i guasti: sullo schermo che guarda lei non compare mai niente del genere.",
      "devices.loading": "Sto caricando i dispositivi.",
      "devices.unreadable": "Non riesco a leggere i dispositivi adesso.",
      "devices.empty": "Nessun dispositivo si è ancora fatto sentire.",
      "devices.justNow": "si è fatto sentire ora",
      "devices.heard": "si è fatto sentire {ago}",
      "devices.silent": "non si fa sentire",
      "devices.check": "da controllare",

      "level.mains": "collegato alla corrente",
      "level.ok": "batteria carica",
      "level.low": "da ricaricare presto",
      "level.critical": "da ricaricare",

      "menu.aria": "Sezioni del pannello",
      "menu.open": "Apri le sezioni del pannello",
      "menu.close": "Chiudi le sezioni del pannello",

      "pictures.title": "Quadri",
      "pictures.note":
        "Tutti i quadri gi\u00e0 comparsi sul display, dal pi\u00f9 recente. Sono mostrati come li vede lei: due soli livelli, senza grigi.",
      "pictures.loading": "Sto caricando i quadri.",
      "pictures.unreadable": "Non riesco a leggere i quadri adesso.",
      "pictures.empty": "Nessun quadro ancora. Il primo arriva quando il display ne chiede uno.",
      "pictures.more": "Mostrane altri",
      "pictures.untitled": "senza tema",
      "pictures.unavailable": "immagine non disponibile",
      "pictures.kind.low": "avviso batteria",
      "pictures.kind.critical": "avviso batteria",

      "usage.title": "Consumo",
      "usage.note":
        "Quanto hanno consumato i modelli questo mese. Sono numeri sulle macchine, non su di lei, e non sono un obiettivo da raggiungere.",
      "usage.loading": "Sto leggendo il consumo.",
      "usage.unreadable": "Non riesco a leggere il consumo adesso.",
      "usage.calls": "chiamate",
      "usage.billed": "di cui pagate",
      "usage.inputTokens": "token in ingresso",
      "usage.outputTokens": "token in uscita",
      "usage.cached": "letti dalla cache",
      "usage.reasoning": "di ragionamento",
      "usage.cap": "tetto mensile",
      "usage.noCap": "nessun tetto",

      "error.title": "Non è riuscito",
      "error.retry": "Riprova",
      "error.noAuth": "Il pannello non ha ancora una configurazione di accesso.",
      "error.refused": "Il pannello ha rifiutato la richiesta (HTTP {status}).",
      "error.token": "il token non è decodificabile",

      "diag.summary": "Dettagli tecnici",
      "diag.claims": "Claim del token",
      "diag.apiresult": "Risposta di",

      "language.label": "Lingua",
    },
  },

  en: {
    name: "English",
    strings: {
      "lede.checking": "Checking whether you are already signed in.",
      "lede.ready": "The panel is ready. Loading your data.",
      "lede.signedout": "You are not signed in yet.",
      "lede.in": "You are in.",
      "lede.pending": "Signed in, but the account is not enabled yet.",
      "lede.failed": "Something did not work.",

      "loading.moment": "One moment.",

      "signin.title": "Sign in",
      "signin.body": "The panel needs an account. You can create one the first time you sign in.",
      "signin.button": "Sign in",
      "signin.as": "Signed in as {user}.",
      "signin.anon": "Signed in.",
      "signout": "Sign out",

      "panel.title": "Panel",
      "connecting.loading": "Loading your data",
      "connecting.note":
        "You can leave this page open. The service may be starting from zero while the panel is already visible.",

      "pending.title": "Account waiting",
      "pending.body":
        "Signing in worked. The account is not enabled yet: a person has to approve it.",
      "pending.note":
        "There is nothing to do from here. This page will not change on its own: reload it once the approval has happened.",

      "facts.status": "Status",
      "facts.account": "Account",
      "facts.household": "Household",

      "proposals.title": "To approve",
      "proposals.note":
        "None of this has reached her. What you approve is kept ready and shown later, when it is needed.",
      "proposals.loading": "Loading the proposals.",
      "proposals.unreadable": "I cannot read the proposals right now.",
      "proposals.empty": "Nothing waiting.",
      "proposals.decideFailed": "I could not record the decision. Try again later.",
      "action.approve": "Approve",
      "action.refuse": "Refuse",

      "kind.exercise": "Sheet to print",
      "kind.routine_prompt": "Reminder on the display",
      "kind.feedback": "Reply after a sheet",
      "kind.schedule": "Plan for the day",
      "kind.print_layout": "Page layout",

      "themes.title": "Picture themes",
      "themes.note":
        "The display draws a new picture on one of these themes. You approve the theme, not each image: what you remove is no longer used.",
      "themes.placeholder": "for example: sleeping cats",
      "themes.aria": "New theme",
      "themes.add": "Add",
      "themes.remove": "Remove",
      "themes.removeTitle": "Remove “{label}”",
      "themes.removeFailed": "I could not remove the theme. Try again later.",
      "themes.loading": "Loading the themes.",
      "themes.unreadable": "I cannot read the themes right now.",
      "themes.empty": "No themes. While the list is empty the display uses the starting ones.",
      "themes.badLabel": "This theme will not do.",
      "themes.addFailed": "It did not work.",

      "devices.title": "Devices",
      "devices.note":
        "How the displays are doing. Faults appear here: nothing of the kind ever appears on the screen she looks at.",
      "devices.loading": "Loading the devices.",
      "devices.unreadable": "I cannot read the devices right now.",
      "devices.empty": "No device has been heard from yet.",
      "devices.justNow": "heard from just now",
      "devices.heard": "heard from {ago}",
      "devices.silent": "not being heard from",
      "devices.check": "worth a look",

      "level.mains": "on mains power",
      "level.ok": "battery full",
      "level.low": "recharge it soon",
      "level.critical": "recharge it",

      "menu.aria": "Panel sections",
      "menu.open": "Open the panel sections",
      "menu.close": "Close the panel sections",

      "pictures.title": "Pictures",
      "pictures.note":
        "Every picture that has appeared on the display, newest first. They are shown as she sees them: two levels only, no greys.",
      "pictures.loading": "Loading the pictures.",
      "pictures.unreadable": "I cannot read the pictures right now.",
      "pictures.empty": "No pictures yet. The first arrives when the display asks for one.",
      "pictures.more": "Show more",
      "pictures.untitled": "no theme",
      "pictures.unavailable": "image unavailable",
      "pictures.kind.low": "battery notice",
      "pictures.kind.critical": "battery notice",

      "usage.title": "Usage",
      "usage.note":
        "What the models consumed this month. These are numbers about machines, not about her, and not a target to reach.",
      "usage.loading": "Reading the usage.",
      "usage.unreadable": "I cannot read the usage right now.",
      "usage.calls": "calls",
      "usage.billed": "of which paid for",
      "usage.inputTokens": "input tokens",
      "usage.outputTokens": "output tokens",
      "usage.cached": "read from cache",
      "usage.reasoning": "spent reasoning",
      "usage.cap": "monthly cap",
      "usage.noCap": "no cap",

      "error.title": "It did not work",
      "error.retry": "Try again",
      "error.noAuth": "The panel has no sign-in configuration yet.",
      "error.refused": "The panel refused the request (HTTP {status}).",
      "error.token": "the token cannot be decoded",

      "diag.summary": "Technical details",
      "diag.claims": "Token claims",
      "diag.apiresult": "Response from",

      "language.label": "Language",
    },
  },
};

const DEFAULT_LANGUAGE = "it";
const STORAGE_KEY = "lanternina.language";
const LANGUAGES = Object.keys(CATALOGS);

const reported = new Set();

function stored() {
  try {
    return window.localStorage.getItem(STORAGE_KEY);
  } catch {
    // A browser refusing storage is allowed to; it just does not remember the choice.
    return null;
  }
}

/** The parent's choice, then the browser's, then the default. */
function detect() {
  const saved = stored();
  if (saved && LANGUAGES.includes(saved)) return saved;
  for (const tag of navigator.languages ?? [navigator.language ?? ""]) {
    const base = String(tag).toLowerCase().split("-")[0];
    if (LANGUAGES.includes(base)) return base;
  }
  return DEFAULT_LANGUAGE;
}

let current = detect();

function t(key, vars = {}) {
  const table = CATALOGS[current]?.strings ?? {};
  let text = table[key] ?? CATALOGS[DEFAULT_LANGUAGE].strings[key];
  if (text === undefined) {
    // Show the key rather than nothing: a gap in a catalog has to be visible.
    if (!reported.has(key)) {
      reported.add(key);
      console.warn(`missing translation: ${key}`);
    }
    return key;
  }
  for (const [name, value] of Object.entries(vars)) {
    text = text.replaceAll(`{${name}}`, String(value));
  }
  return text;
}

/** "5 minuti fa" or "5 minutes ago", without either phrase being written down. */
function ago(seconds) {
  const format = new Intl.RelativeTimeFormat(current, { numeric: "auto" });
  const minutes = Math.round(seconds / 60);
  if (minutes < 90) return format.format(-minutes, "minute");
  const hours = Math.round(minutes / 60);
  if (hours < 36) return format.format(-hours, "hour");
  return format.format(-Math.round(hours / 24), "day");
}

/** A date the parent can read, in whatever language is current. */
function dateTime(seconds) {
  if (!seconds) return "";
  return new Intl.DateTimeFormat(current, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(seconds * 1000));
}

function applyStaticText(root = document) {
  root.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  root.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
    node.placeholder = t(node.dataset.i18nPlaceholder);
  });
  root.querySelectorAll("[data-i18n-label]").forEach((node) => {
    node.setAttribute("aria-label", t(node.dataset.i18nLabel));
  });
  document.documentElement.lang = current;
}

const listeners = [];

function onLanguageChange(handler) {
  listeners.push(handler);
}

function setLanguage(language) {
  if (!LANGUAGES.includes(language) || language === current) return;
  current = language;
  try {
    window.localStorage.setItem(STORAGE_KEY, language);
  } catch {
    // Not remembering the choice is better than failing to honour it now.
  }
  applyStaticText();
  listeners.forEach((handler) => handler(language));
}

/** Builds itself from the catalogs, so a new language needs no markup. */
function fillLanguageChooser(select) {
  select.textContent = "";
  LANGUAGES.forEach((code) => {
    const option = document.createElement("option");
    option.value = code;
    option.textContent = CATALOGS[code].name;
    select.appendChild(option);
  });
  select.value = current;
  select.onchange = () => setLanguage(select.value);
}

window.LanterninaI18n = {
  t,
  ago,
  dateTime,
  applyStaticText,
  setLanguage,
  onLanguageChange,
  fillLanguageChooser,
  get language() {
    return current;
  },
};

// Applied here rather than from app.js: if the identity library fails to load, app.js
// throws on its first line and the parent would be left looking at a page with no words.
applyStaticText();
const chooser = document.getElementById("lang");
if (chooser !== null) fillLanguageChooser(chooser);
})();
