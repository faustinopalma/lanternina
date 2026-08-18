/* Sign in, ask for a token, call the panel, show what came back.
 *
 * The order matters and is not obvious: handleRedirectPromise() must run before anything
 * else, because after returning from the identity provider the authorisation code is
 * sitting in the URL and is consumed exactly once.
 */

const cfg = window.LANTERNINA;
const { t, ago, dateTime, onLanguageChange } = window.LanterninaI18n;

// Opening the dashboard is the one event that may warm its read/write API. The response
// is irrelevant: this overlaps scale-from-zero with MSAL and creates no work in the house.
const apiWarmup = fetch(`${cfg.apiBase}/health`, {
  cache: "no-store",
}).catch(() => null);

const msalInstance = new msal.PublicClientApplication({
  auth: {
    clientId: cfg.clientId,
    authority: cfg.authority,
    knownAuthorities: cfg.knownAuthorities,
    redirectUri: window.location.origin,
    navigateToLoginRequestUrl: false,
  },
  cache: {
    // Survives a reload; cleared when the browser is closed. A refresh token in
    // localStorage would outlive the session for no benefit we need.
    cacheLocation: "sessionStorage",
    storeAuthStateInCookie: false,
  },
});

const el = (id) => document.getElementById(id);
const views = ["loading", "signedout", "connecting", "pending", "dashboard", "error"];

// The key, not the sentence: switching language has to be able to say the same thing again.
let ledeKey = "lede.checking";

function show(name, key) {
  views.forEach((v) => el(`view-${v}`).classList.toggle("hidden", v !== name));
  if (key !== undefined) {
    ledeKey = key;
    el("lede").textContent = t(key);
  }
}

function showDiagnostics(claims, apiResult) {
  el("diagnostics").classList.remove("hidden");
  if (claims !== undefined) el("claims").textContent = JSON.stringify(claims, null, 2);
  if (apiResult !== undefined) el("apiresult").textContent = apiResult;
}

function showDashboardShell(account) {
  el("connecting-account").textContent = account.username
    ? t("signin.as", { user: account.username })
    : t("signin.anon");
  show("connecting", "lede.ready");
}

/** Reads the payload for display only. Nothing here is trusted: the panel verifies the
 *  signature, and this cannot, because the browser has no business holding the keys. */
function decodeForDisplay(jwt) {
  try {
    const payload = jwt.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
    return JSON.parse(decodeURIComponent(escape(atob(payload))));
  } catch {
    return { error: t("error.token") };
  }
}

async function getToken(account) {
  const request = { scopes: cfg.scopes, account };
  try {
    return await msalInstance.acquireTokenSilent(request);
  } catch (e) {
    // Silent acquisition fails on first run and whenever consent or interaction is
    // genuinely required; a redirect is the answer, not an error to report.
    if (e instanceof msal.InteractionRequiredAuthError) {
      await msalInstance.acquireTokenRedirect(request);
      return null;
    }
    throw e;
  }
}

async function callPanel(accessToken) {
  const response = await fetch(`${cfg.apiBase}/api/me`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  const body = await response.text();
  return { status: response.status, body };
}

let bearer = null;

function api(path, options = {}) {
  return fetch(`${cfg.apiBase}${path}`, {
    ...options,
    headers: {
      Authorization: `Bearer ${bearer}`,
      "Content-Type": "application/json",
      ...(options.headers ?? {}),
    },
  });
}

// Unknown kinds show their raw name rather than a missing-key placeholder: the panel is
// allowed to meet a kind this build has never heard of.
const KNOWN_KINDS = ["exercise", "routine_prompt", "feedback", "schedule", "print_layout"];
const kindLabel = (kind) => (KNOWN_KINDS.includes(kind) ? t(`kind.${kind}`) : kind);

/* Everything below writes with textContent, never innerHTML: this text was written by a
 * model and must reach the page as words, not as markup. */
function renderBody(host, proposal) {
  if (!String(proposal.contentKind).endsWith("json")) {
    host.appendChild(Object.assign(document.createElement("p"), { textContent: proposal.body }));
    return;
  }
  let content;
  try {
    content = JSON.parse(proposal.body);
  } catch {
    host.appendChild(
      Object.assign(document.createElement("p"), { textContent: proposal.body })
    );
    return;
  }
  host.appendChild(
    Object.assign(document.createElement("h3"), { textContent: content.titolo ?? "" })
  );
  host.appendChild(
    Object.assign(document.createElement("p"), { textContent: content.istruzioni ?? "" })
  );
  const list = document.createElement("ul");
  (content.esercizi ?? []).forEach((entry) => {
    const item = document.createElement("li");
    item.textContent = entry.domanda ?? "";
    const choices = document.createElement("span");
    choices.className = "choices";
    choices.textContent = (entry.scelte ?? []).join(" · ");
    item.appendChild(choices);
    list.appendChild(item);
  });
  host.appendChild(list);
}

function proposalCard(proposal) {
  const card = document.createElement("article");
  card.className = "proposal";

  const kind = document.createElement("p");
  kind.className = "kind";
  kind.textContent = kindLabel(proposal.kind);
  card.appendChild(kind);

  renderBody(card, proposal);

  const why = document.createElement("p");
  why.className = "muted why";
  why.textContent = proposal.rationale;
  card.appendChild(why);

  const actions = document.createElement("div");
  actions.className = "actions";
  const approve = Object.assign(document.createElement("button"), {
    textContent: t("action.approve"),
    className: "primary",
  });
  const refuse = Object.assign(document.createElement("button"), {
    textContent: t("action.refuse"),
  });
  approve.onclick = () => decide(proposal.id, "approved", card, [approve, refuse]);
  refuse.onclick = () => decide(proposal.id, "rejected", card, [approve, refuse]);
  actions.append(approve, refuse);
  card.appendChild(actions);
  return card;
}

async function decide(id, state, card, buttons) {
  buttons.forEach((button) => (button.disabled = true));
  const response = await api(`/api/proposals/${id}/decision`, {
    method: "POST",
    body: JSON.stringify({ state }),
  });
  if (!response.ok) {
    buttons.forEach((button) => (button.disabled = false));
    card.appendChild(
      Object.assign(document.createElement("p"), {
        className: "muted",
        textContent: t("proposals.decideFailed"),
      })
    );
    return;
  }
  card.remove();
  if (!el("proposals").querySelector(".proposal")) showEmptyProposals();
}

function showEmptyProposals() {
  el("proposals").innerHTML = "";
  el("proposals").appendChild(
    Object.assign(document.createElement("p"), {
      className: "muted",
      textContent: t("proposals.empty"),
    })
  );
}

async function loadProposals() {
  const host = el("proposals");
  host.textContent = t("proposals.loading");
  let response;
  try {
    response = await api("/api/proposals");
  } catch {
    host.textContent = t("proposals.unreadable");
    return;
  }
  if (!response.ok) {
    host.textContent = t("proposals.unreadable");
    return;
  }
  const { proposals } = await response.json();
  if (!proposals.length) {
    showEmptyProposals();
    return;
  }
  host.textContent = "";
  proposals.forEach((proposal) => host.appendChild(proposalCard(proposal)));
}

function themeChip(theme) {
  const chip = document.createElement("div");
  chip.className = "theme";
  chip.appendChild(
    Object.assign(document.createElement("span"), { textContent: theme.label })
  );
  const remove = Object.assign(document.createElement("button"), {
    textContent: t("themes.remove"),
    title: t("themes.removeTitle", { label: theme.label }),
  });
  remove.onclick = async () => {
    remove.disabled = true;
    const response = await api(`/api/themes/${theme.id}/remove`, { method: "POST" });
    if (!response.ok) {
      remove.disabled = false;
      showThemeError(t("themes.removeFailed"));
      return;
    }
    chip.remove();
    if (!el("themes").querySelector(".theme")) showEmptyThemes();
  };
  chip.appendChild(remove);
  return chip;
}

function showEmptyThemes() {
  el("themes").textContent = "";
  el("themes").appendChild(
    Object.assign(document.createElement("p"), {
      className: "muted",
      textContent: t("themes.empty"),
    })
  );
}

function showThemeError(message) {
  const box = el("theme-error");
  box.textContent = message;
  box.classList.toggle("hidden", !message);
}

async function loadThemes() {
  const host = el("themes");
  host.textContent = t("themes.loading");
  let response;
  try {
    response = await api("/api/themes");
  } catch {
    host.textContent = t("themes.unreadable");
    return;
  }
  if (!response.ok) {
    host.textContent = t("themes.unreadable");
    return;
  }
  const { themes } = await response.json();
  if (!themes.length) {
    showEmptyThemes();
    return;
  }
  host.textContent = "";
  themes.forEach((theme) => host.appendChild(themeChip(theme)));
}

function fillHourChoices(select, chosen) {
  select.textContent = "";
  for (let hour = 0; hour < 24; hour += 1) {
    const option = document.createElement("option");
    option.value = String(hour);
    option.textContent = `${String(hour).padStart(2, "0")}:00`;
    select.appendChild(option);
  }
  select.value = String(chosen);
}

function fillCadenceChoices(select, choices, chosen) {
  select.textContent = "";
  choices.forEach((hours) => {
    const option = document.createElement("option");
    option.value = String(hours);
    option.textContent = hours === 1 ? t("rhythm.everyHour") : t("rhythm.everyHours", { hours });
    select.appendChild(option);
  });
  select.value = String(chosen);
}

async function loadRhythm() {
  const status = el("rhythm-status");
  status.textContent = t("rhythm.loading");
  let response;
  try {
    response = await api("/api/rhythm");
  } catch {
    status.textContent = t("rhythm.unreadable");
    return;
  }
  if (!response.ok) {
    status.textContent = t("rhythm.unreadable");
    return;
  }
  const rhythm = await response.json();
  fillHourChoices(el("quiet-from"), rhythm.quietFromHour);
  fillHourChoices(el("quiet-until"), rhythm.quietUntilHour);
  fillCadenceChoices(el("cadence"), rhythm.cadenceChoices, rhythm.cadenceHours);
  status.textContent =
    rhythm.quietFromHour === rhythm.quietUntilHour ? t("rhythm.quietOff") : "";
}

/* Saving persists a choice and returns. The house reads it on its next run and decides
 * for itself, so nothing here reaches into the room. */
async function submitRhythm(event) {
  event.preventDefault();
  const status = el("rhythm-status");
  const response = await api("/api/rhythm", {
    method: "POST",
    body: JSON.stringify({
      quietFromHour: Number(el("quiet-from").value),
      quietUntilHour: Number(el("quiet-until").value),
      cadenceHours: Number(el("cadence").value),
    }),
  });
  status.textContent = response.ok ? t("rhythm.saved") : t("rhythm.saveFailed");
}

const KNOWN_LEVELS = ["mains", "ok", "low", "critical"];
const levelLabel = (level) => (KNOWN_LEVELS.includes(level) ? t(`level.${level}`) : level);

/* Deliberately vague: the board has no fuel gauge, so a percentage would be arithmetic
 * performed on a guess. */
function sinceWords(seconds) {
  return seconds < 120 ? t("devices.justNow") : t("devices.heard", { ago: ago(seconds) });
}

function deviceRow(device) {
  const row = document.createElement("div");
  row.className = "device";

  const left = document.createElement("div");
  left.appendChild(
    Object.assign(document.createElement("strong"), { textContent: device.name })
  );
  const detail = document.createElement("span");
  detail.className = "muted";
  const level = levelLabel(device.level);
  detail.textContent = device.silent
    ? `${level} \u00b7 ${t("devices.silent")}`
    : `${level} \u00b7 ${sinceWords(device.silentSeconds)}`;
  left.appendChild(detail);
  row.appendChild(left);

  if (device.silent) {
    row.appendChild(
      Object.assign(document.createElement("span"), {
        className: "warn",
        textContent: t("devices.check"),
      })
    );
  }
  return row;
}

async function loadDevices() {
  const host = el("devices");
  host.textContent = t("devices.loading");
  let response;
  try {
    response = await api("/api/devices");
  } catch {
    host.textContent = t("devices.unreadable");
    return;
  }
  if (!response.ok) {
    host.textContent = t("devices.unreadable");
    return;
  }
  const { devices } = await response.json();
  if (!devices.length) {
    host.textContent = t("devices.empty");
    return;
  }
  host.textContent = "";
  devices.forEach((device) => host.appendChild(deviceRow(device)));
}

/* ---- the gallery -------------------------------------------------------------------
 *
 * The bitmap cannot be fetched by putting the route in `src`: it needs the bearer token,
 * and an <img> sends no headers. So each tile fetches its own bytes and hands the element
 * a blob URL, which is also why the CSP has to allow `blob:` for images.
 *
 * What is shown is the rendered 1-bit image, not the model's original: approving or judging
 * a picture from a smooth PNG would be judging something she never saw.
 */

let pictureLimit = 60;

async function fillTile(img, note, id) {
  let response;
  try {
    response = await api(`/api/pictures/${id}/content`);
  } catch {
    note.textContent = t("pictures.unavailable");
    return;
  }
  if (!response.ok) {
    note.textContent = t("pictures.unavailable");
    return;
  }
  const url = URL.createObjectURL(await response.blob());
  img.onload = () => URL.revokeObjectURL(url);
  img.src = url;
  img.classList.remove("hidden");
}

// Bytes are fetched when a tile comes into view, so opening the gallery costs one small
// listing rather than tens of megabytes of bitmaps.
const tileWatcher =
  "IntersectionObserver" in window
    ? new IntersectionObserver(
        (entries, observer) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            observer.unobserve(entry.target);
            const { img, note, pictureId } = entry.target._tile;
            void fillTile(img, note, pictureId);
          });
        },
        { rootMargin: "200px" }
      )
    : null;

// Written out rather than built from the value, so a missing entry is caught by the tests
// instead of appearing to a parent as a raw key.
function pictureTitle(picture) {
  if (picture.kind === "low") return t("pictures.kind.low");
  if (picture.kind === "critical") return t("pictures.kind.critical");
  return picture.theme || t("pictures.untitled");
}

function pictureTile(picture) {
  const figure = document.createElement("figure");
  figure.className = "tile";

  const img = document.createElement("img");
  img.className = "hidden";
  img.alt = picture.theme || t("pictures.untitled");
  figure.appendChild(img);

  const caption = document.createElement("figcaption");
  const title = document.createElement("strong");
  title.textContent = pictureTitle(picture);
  const when = document.createElement("span");
  when.className = "muted";
  when.textContent = dateTime(picture.createdAt);
  const note = document.createElement("span");
  note.className = "muted";
  caption.append(title, when, note);
  figure.appendChild(caption);

  figure._tile = { img, note, pictureId: picture.id };
  if (tileWatcher) tileWatcher.observe(figure);
  else void fillTile(img, note, picture.id);
  return figure;
}

async function loadPictures() {
  const host = el("pictures");
  host.textContent = t("pictures.loading");
  el("btn-more-pictures").classList.add("hidden");
  let response;
  try {
    response = await api(`/api/pictures?limit=${pictureLimit}`);
  } catch {
    host.textContent = t("pictures.unreadable");
    return;
  }
  if (!response.ok) {
    host.textContent = t("pictures.unreadable");
    return;
  }
  const { pictures } = await response.json();
  host.textContent = "";
  if (!pictures.length) {
    host.appendChild(
      Object.assign(document.createElement("p"), {
        className: "muted",
        textContent: t("pictures.empty"),
      })
    );
    return;
  }
  pictures.forEach((picture) => host.appendChild(pictureTile(picture)));
  // Only offered when the page came back full: otherwise there is nothing more to show.
  el("btn-more-pictures").classList.toggle("hidden", pictures.length < pictureLimit);
}

/* ---- what the models cost ---------------------------------------------------------- */

async function loadUsage() {
  const host = el("usage");
  host.textContent = t("usage.loading");
  let response;
  try {
    response = await api("/api/usage");
  } catch {
    host.textContent = t("usage.unreadable");
    return;
  }
  if (!response.ok) {
    host.textContent = t("usage.unreadable");
    return;
  }
  const { usage, cap } = await response.json();
  const rows = [
    [t("usage.calls"), usage.calls],
    [t("usage.billed"), usage.billedCalls],
    [t("usage.inputTokens"), usage.inputTokens],
    [t("usage.cached"), usage.cachedInputTokens],
    [t("usage.outputTokens"), usage.outputTokens],
    [t("usage.reasoning"), usage.reasoningTokens],
    [t("usage.cap"), cap > 0 ? cap : t("usage.noCap")],
  ];
  const list = document.createElement("dl");
  list.className = "facts";
  rows.forEach(([label, value]) => {
    list.appendChild(Object.assign(document.createElement("dt"), { textContent: label }));
    list.appendChild(
      Object.assign(document.createElement("dd"), { textContent: String(value) })
    );
  });
  host.textContent = "";
  host.appendChild(list);
}

/* ---- the menu ---------------------------------------------------------------------- */

const PANELS = {
  proposals: loadProposals,
  pictures: loadPictures,
  themes: loadThemes,
  rhythm: loadRhythm,
  devices: loadDevices,
  usage: loadUsage,
};

let currentPanel = "proposals";
const menuDrawer = el("menu-drawer");

function closeMenu() {
  if (!menuDrawer.matches(":popover-open")) return;
  menuDrawer.hidePopover();
  el("menu-toggle").focus();
}

function showPanel(name) {
  if (!(name in PANELS)) return;
  currentPanel = name;
  el("menu-toggle-text").textContent = t(`${name}.title`);
  Object.keys(PANELS).forEach((key) => {
    el(`panel-${key}`).classList.toggle("hidden", key !== name);
  });
  el("menu")
    .querySelectorAll("button")
    .forEach((button) => {
      const selected = button.dataset.panel === name;
      button.classList.toggle("current", selected);
      if (selected) button.setAttribute("aria-current", "true");
      else button.removeAttribute("aria-current");
    });
  void PANELS[name]();
}

async function submitTheme(event) {
  event.preventDefault();
  const input = el("theme-input");
  const label = input.value.trim();
  if (!label) return;
  showThemeError("");
  const response = await api("/api/themes", {
    method: "POST",
    body: JSON.stringify({ label }),
  });
  if (!response.ok) {
    const detail = response.status === 400 ? t("themes.badLabel") : t("themes.addFailed");
    showThemeError(detail);
    return;
  }
  input.value = "";
  const theme = await response.json();
  if (!el("themes").querySelector(".theme")) el("themes").textContent = "";
  el("themes").appendChild(themeChip(theme));
}

let account_ = null;
let me_ = null;

/* Built with textContent rather than innerHTML: these values come from the panel, and the
 * one place that renders identifiers should not be the one place that trusts them. */
function renderAccount() {
  if (me_ === null) return;
  el("greeting").textContent = account_?.username
    ? t("signin.as", { user: account_.username })
    : t("signin.anon");
  const facts = el("account-facts");
  facts.textContent = "";
  const rows = [
    [t("facts.status"), me_.status, false],
    [t("facts.account"), me_.accountId, true],
    [t("facts.household"), me_.householdId ?? "\u2014", true],
  ];
  rows.forEach(([label, value, code]) => {
    facts.appendChild(
      Object.assign(document.createElement("dt"), { textContent: label })
    );
    const dd = document.createElement("dd");
    const holder = document.createElement(code ? "code" : "span");
    holder.textContent = String(value);
    dd.appendChild(holder);
    facts.appendChild(dd);
  });
}

async function run() {
  show("loading");
  const redirectResult = await msalInstance.handleRedirectPromise();
  const account = redirectResult?.account ?? msalInstance.getAllAccounts()[0] ?? null;

  if (!account) {
    show("signedout", "lede.signedout");
    return;
  }

  msalInstance.setActiveAccount(account);
  showDashboardShell(account);

  const result = await getToken(account);
  if (!result) return; // a redirect is under way; this page is about to be replaced

  const claims = decodeForDisplay(result.accessToken);
  const { status, body } = await callPanel(result.accessToken);
  showDiagnostics(claims, `HTTP ${status}\n${body}`);

  if (status === 200) {
    const me = JSON.parse(body);
    bearer = result.accessToken;
    account_ = account;
    me_ = me;
    renderAccount();
    show("dashboard", "lede.in");
    showPanel(currentPanel);
    return;
  }

  if (status === 403) {
    show("pending", "lede.pending");
    return;
  }

  // 401 means the token was refused; 503 means the panel has no identity provider
  // configured. Both are our problem, not the parent's, so neither is dressed up.
  el("error-text").textContent =
    status === 503 ? t("error.noAuth") : t("error.refused", { status });
  show("error", "lede.failed");
}

/* A rejected redirect leaves MSAL's interaction flag set, so every later click is refused
 * with interaction_in_progress and the button just stops responding. Say so instead. */
function reportInteractionFailure(e) {
  el("error-text").textContent = e?.errorCode ?? e?.message ?? String(e);
  showDiagnostics(undefined, String(e));
  show("error", "lede.failed");
}

el("btn-signin").onclick = () =>
  msalInstance.loginRedirect({ scopes: cfg.scopes }).catch(reportInteractionFailure);
el("theme-form").onsubmit = submitTheme;
el("rhythm-form").onsubmit = submitRhythm;

const signOut = () =>
  msalInstance
    .logoutRedirect({ postLogoutRedirectUri: window.location.origin })
    .catch(reportInteractionFailure);
el("btn-signout").onclick = signOut;
el("btn-signout-pending").onclick = signOut;
el("btn-signout-error").onclick = signOut;
el("btn-retry").onclick = () => window.location.reload();

el("menu").onclick = (event) => {
  const button = event.target.closest("button[data-panel]");
  if (!button) return;
  showPanel(button.dataset.panel);
  closeMenu();
};

menuDrawer.addEventListener("toggle", (event) => {
  if (event.newState === "open" && window.matchMedia("(max-width: 55.999rem)").matches) {
    el("menu-close").focus();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeMenu();
});

el("btn-more-pictures").onclick = () => {
  pictureLimit = Math.min(pictureLimit + 60, 500);
  void loadPictures();
};

onLanguageChange(() => {
  // applyStaticText has just reset the lede to its markup default; put back what the
  // current view actually says, then redraw everything the catalogs touch.
  el("lede").textContent = t(ledeKey);
  el("menu-toggle-text").textContent = t(`${currentPanel}.title`);
  renderAccount();
  if (!el("view-dashboard").classList.contains("hidden")) {
    void PANELS[currentPanel]();
  }
});

msalInstance
  .initialize()
  .then(() => {
    // Keep the promise observed without making authentication wait for the API.
    void apiWarmup;
    return run();
  })
  .catch((e) => {
    el("error-text").textContent = e?.message ?? String(e);
    showDiagnostics(undefined, String(e));
    show("error", "lede.failed");
  });
