/* A stand-in for the panel's API, used by the tests and by the dev-only preview.
 *
 * Everything here is invented. Nothing in this file describes a real household, and it
 * never will: personal data does not live in the repository.
 */
import type {
  Admission,
  Api,
  Decision,
  Device,
  Guidelines,
  NewAssignment,
  NewPreferences,
  NewRhythm,
  OfferedExperience,
  PicturePage,
  Preferences,
  Proposal,
  Reminder,
  Rhythm,
  Said,
  NewSaid,
  Theme,
  UsageAnswer,
  HouseRequest,
} from "@/api/types";

export interface Recorded {
  decisions: { id: string; state: Decision }[];
  rhythm: NewRhythm[];
  preferences: NewPreferences[];
  guidelines: string[][];
  themesAdded: string[];
  themesRemoved: string[];
  remindersAdded: string[];
  remindersRewritten: { id: string; text: string }[];
  remindersRemoved: string[];
  assignments: { id: string; assignment: NewAssignment }[];
  devicesRemoved: string[];
  identified: string[];
  looked: string[];
  askedAgain: string[];
  limitSetTo: number[];
  begunNow: number;
  experienceDecisions: { id: string; state: Decision }[];
  said: NewSaid[];
}

export interface FakeApi extends Api {
  recorded: Recorded;
}

const NOW = 1_755_500_000;

export const SAMPLE_PROPOSALS: Proposal[] = [
  {
    id: "prop-1",
    kind: "exercise",
    agent: "content",
    rationale: "Un foglio breve, con quattro domande.",
    createdAt: NOW - 600,
    state: "pending",
    contentKind: "application/json",
    body: JSON.stringify({
      title: "Le stagioni",
      instructions: "Scegli la parola giusta.",
      exercises: [
        { question: "In che stagione cadono le foglie?", choices: ["estate", "autunno"] },
        { question: "Quando fiorisce il ciliegio?", choices: ["primavera", "inverno"] },
      ],
    }),
  },
  {
    id: "prop-2",
    kind: "routine_prompt",
    agent: "content",
    rationale: "Un promemoria per la sera.",
    createdAt: NOW - 900,
    state: "pending",
    contentKind: "text/plain",
    body: "Prepara lo zaino per domani.",
  },
];

/** What the parent has already approved and the house has not yet been offered. Two, so a
 *  count of them is not the same number as anything else on the page. */
export const SAMPLE_APPROVED: Proposal[] = [
  {
    id: "prop-9",
    kind: "exercise",
    agent: "content",
    rationale: "Approvato ieri.",
    createdAt: NOW - 90_000,
    state: "approved",
    contentKind: "application/json",
    body: JSON.stringify({ title: "I pianeti", instructions: "", exercises: [] }),
  },
  {
    id: "prop-10",
    kind: "routine_prompt",
    agent: "content",
    rationale: "Approvato ieri.",
    createdAt: NOW - 91_000,
    state: "approved",
    contentKind: "text/plain",
    body: "Annaffia le piante.",
  },
];

/** The three weights, the four rungs and the way out, filled in once. What these tests are
 *  about is what the page renders, not what a plausible afternoon says. */
const weighed = (lines: string[]) => ({
  short: { minutes: 5, lines },
  standard: { minutes: 10, lines },
  extended: { minutes: 15, lines },
});
const ladder = [
  { after_minutes: 3, lines: ["Il foglio è lì."] },
  { after_minutes: 6, lines: ["Comincia da un angolo."] },
  { after_minutes: 10, lines: ["Basta un segno."] },
  { after_minutes: 15, lines: ["Va bene anche una riga."] },
];
const wayOut = {
  in_hand: "il foglio",
  heading: "Basta così",
  lines: ["Posa il foglio sul tavolo."],
  minutes: 10,
};

/** One devised afternoon, in the shape the panel hands it over: a display, a sheet, a
 *  page coming back, and a branch left to be written when it does. */
export const SAMPLE_AFTERNOON: OfferedExperience = {
  id: "aftn-1",
  title: "Sei passaggi di una trasformazione",
  overview:
    "Un oggetto della stanza, disegnato sei volte mentre cambia. Il foglio torna dallo scanner e il pomeriggio va avanti da lì.",
  minutes: 90,
  createdAt: NOW - 1800,
  state: "pending",
  begunAt: 0,
  experience: {
    experience_id: "aftn-1",
    title: "Sei passaggi di una trasformazione",
    overview: "Un oggetto della stanza, disegnato sei volte mentre cambia.",
    minutes: 90,
    drawn: {
      frame: "una stanza di pomeriggio",
      role: "chi guarda un oggetto",
      mechanic: "disegnare la stessa cosa",
      progress: "un riquadro alla volta",
      paper: "i sei riquadri",
      glass: "consegnare il foglio",
      displays: "la voce che dice cosa fare",
      camera: "nessuna",
      tone: "asciutto",
      ending: "il foglio resta lì",
    },
    moments: [
      {
        act: "say",
        id: "guarda",
        heading: "Scegli un oggetto",
        weights: weighed(["Uno che sta in mano."]),
        help: ladder,
        way_out: wayOut,
      },
      {
        act: "hand_over",
        id: "il-foglio",
        heading: "Esce un foglio",
        weights: weighed(["Sul tavolo c'è il foglio."]),
        help: ladder,
        way_out: wayOut,
        instead: ["Oggi il foglio non esce."],
        page: {
          kind: "notebook",
          title: "Sei riquadri",
          illustration: "six empty frames in a row, drawn by hand",
          note: ["Disegna lo stesso oggetto sei volte."],
          spaces: [
            { label: "primo riquadro", room: "a_box" },
            { label: "una parola", room: "a_line" },
          ],
        },
      },
      {
        act: "collect",
        id: "come-e-tornato",
        heading: "Mettilo sul vetro",
        weights: weighed(["Metti il foglio sul vetro."]),
        help: ladder,
        way_out: wayOut,
        outcomes: [
          { when: "marks", then: "ask" },
          { when: "blank", then: "basta-cosi" },
        ],
        if_no_page: "basta-cosi",
      },
      {
        act: "close",
        id: "basta-cosi",
        heading: "Va bene così",
        weights: weighed(["Il foglio resta lì."]),
        help: ladder,
        way_out: wayOut,
      },
    ],
  },
};

const SAMPLE_PICTURES: PicturePage = {  pictures: Array.from({ length: 6 }, (_, index) => ({
    id: `pic-${index + 1}`,
    theme: index === 0 ? "" : "gatti che dormono",
    createdAt: NOW - index * 3600,
    kind: index === 5 ? "low" : "ok",
  })),
  page: 1,
  perPage: 20,
  pages: 2,
  total: 26,
  pageSizes: [10, 20, 30, 50],
};

const SAMPLE_DEVICES: Device[] = [
  {
    id: "94:A9:90:CF:7D:04",
    kind: "display",
    label: "CF7D04",
    name: "il quadro in corridoio",
    jobs: ["picture"],
    jobChoices: ["picture", "sheet"],
    model: "xiao_epaper_display",
    address: "",
    nameRefused: false,
    level: "ok",
    lastSeen: NOW - 120,
    silentSeconds: 120,
    silent: false,
  },
  {
    id: "E8:3D:C1:FB:9F:18",
    kind: "display",
    label: "FB9F18",
    name: "",
    jobs: [],
    jobChoices: ["picture", "sheet"],
    model: "xiao_epaper_display",
    address: "",
    nameRefused: false,
    level: "low",
    lastSeen: NOW - 40000,
    silentSeconds: 40000,
    silent: true,
  },
  {
    id: "stampante.local",
    kind: "printer",
    label: "stampante.local",
    name: "la stampante di sotto",
    jobs: ["print"],
    jobChoices: ["print"],
    model: "un modello qualunque",
    address: "192.168.0.5",
    nameRefused: false,
    lastSeen: NOW - 300,
    silentSeconds: 300,
    silent: false,
  },
];

/** A one-pixel bitmap, so a tile has something to show without a network. */
const TINY_BITMAP = new Uint8Array([
  0x42, 0x4d, 0x3e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3e, 0x00, 0x00, 0x00, 0x28,
  0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0x00,
  0x00, 0x00, 0x00, 0x00,
]);

export function fakeApi(overrides: Partial<Api> = {}): FakeApi {
  const recorded: Recorded = {
    decisions: [],
    rhythm: [],
    preferences: [],
    guidelines: [],
    themesAdded: [],
    themesRemoved: [],
    remindersAdded: [],
    remindersRewritten: [],
    remindersRemoved: [],
    assignments: [],
    devicesRemoved: [],
    identified: [],
    looked: [],
    askedAgain: [],
    limitSetTo: [],
    begunNow: 0,
    experienceDecisions: [],
    said: [],
  };
  let themes: Theme[] = [
    { id: "theme-1", label: "gatti che dormono" },
    { id: "theme-2", label: "vele in porto" },
  ];
  let devices: Device[] = SAMPLE_DEVICES;
  let forgotten: Device[] = [];
  let standing: HouseRequest | null = null;
  let approved: Proposal[] = SAMPLE_APPROVED;
  let afternoons: OfferedExperience[] = [SAMPLE_AFTERNOON];
  // What the parent has said to a running afternoon and the house has not yet come for.
  let waiting: Said[] = [];
  // One the house has placed, and one it has not been asked about yet.
  let reminders: Reminder[] = [
    {
      id: "rm_1",
      text: "lavarsi i denti dopo cena",
      createdAt: NOW - 7200,
      read: true,
      readAt: NOW - 3000,
      at: "21:00",
      days: [],
      question: "",
      words: ["È ora dei denti.", "Un minuto per i denti."],
    },
    {
      id: "rm_2",
      text: "mercoled\u00ec porta fuori il bidone",
      createdAt: NOW - 3600,
      read: false,
      readAt: 0,
      at: "",
      days: [],
      question: "",
      words: [],
    },
  ];
  let rhythm: Rhythm = {
    picturesFrom: "07:00",
    picturesUntil: "21:30",
    cadenceMinutes: 60,
    minCadenceMinutes: 1,
    maxCadenceMinutes: 1440,
    afternoonDays: ["wed", "sat"],
    afternoonFrom: "15:00",
    afternoonUntil: "19:00",
    timeZone: "Europe/Rome",
    dayChoices: ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
  };
  let preferences: Preferences = {
    interests: ["gatti", "vele"],
    avoid: ["tempeste"],
    difficulty: "gentle",
    variety: "balanced",
    maxWordsPerLine: 6,
    language: "it",
    difficultyChoices: ["gentle", "steady", "stretch"],
    varietyChoices: ["familiar", "balanced", "frequent"],
    languageChoices: ["it", "en"],
    wordsPerLineChoices: [3, 4, 5, 6, 7, 8],
  };
  /* One line written, so the page shows both halves: what this house allowed and what
   * holds everywhere. The fixed ones are the API's own words, in the model's language. */
  let guidelines: Guidelines = {
    lines: ["va bene uscire in giardino"],
    fixed: [
      "Never say anything about the person: not how well anything was done, not how much effort it took, not what any of it suggests about them.",
      "Never announce, explain or apologise for a change of course. It arrives as part of what is happening.",
      "An ending stays reachable from wherever the activity has got to, and an ending reached early is the same ending.",
      "Use only what this house has. Never invent equipment, materials or a place.",
      "Nothing can be failed and nothing has to be finished.",
    ],
    updatedAt: NOW - 4000,
    lineLimit: 160,
    maxLines: 12,
  };

  const base: Api = {
    admission: async (): Promise<Admission> => ({
      kind: "in",
      me: { accountId: "acct-demo", householdId: "house-demo", status: "active" },
    }),
    proposals: async () => SAMPLE_PROPOSALS,
    approved: async () => approved,
    decide: async (id, state) => {
      recorded.decisions.push({ id, state });
      if (state === "withdrawn") approved = approved.filter((row) => row.id !== id);
    },
    pictures: async (page, perPage) => ({ ...SAMPLE_PICTURES, page, perPage }),
    pictureContent: async () => new Blob([TINY_BITMAP], { type: "image/bmp" }),
    themes: async () => themes,
    addTheme: async (label) => {
      recorded.themesAdded.push(label);
      const theme = { id: `theme-${themes.length + 1}`, label };
      themes = [...themes, theme];
      return theme;
    },
    removeTheme: async (id) => {
      recorded.themesRemoved.push(id);
      themes = themes.filter((theme) => theme.id !== id);
    },
    reminders: async () => ({ reminders, textLimit: 200 }),
    addReminder: async (text) => {
      recorded.remindersAdded.push(text);
      const reminder: Reminder = {
        id: `rm_${reminders.length + 1}`,
        text,
        createdAt: NOW,
        read: false,
        readAt: 0,
        at: "",
        days: [],
        question: "",
        words: [],
      };
      reminders = [...reminders, reminder];
      return reminder;
    },
    rewriteReminder: async (id, text) => {
      recorded.remindersRewritten.push({ id, text });
      reminders = reminders.map((reminder) =>
        reminder.id === id
          ? { ...reminder, text, read: false, readAt: 0, words: [] }
          : reminder,
      );
      return reminders.find((reminder) => reminder.id === id)!;
    },
    removeReminder: async (id) => {
      recorded.remindersRemoved.push(id);
      reminders = reminders.filter((reminder) => reminder.id !== id);
    },
    rhythm: async () => rhythm,
    saveRhythm: async (next) => {
      recorded.rhythm.push(next);
      rhythm = { ...rhythm, ...next };
      return rhythm;
    },
    preferences: async () => preferences,
    savePreferences: async (next) => {
      recorded.preferences.push(next);
      preferences = { ...preferences, ...next };
      return preferences;
    },
    guidelines: async () => guidelines,
    saveGuidelines: async (lines) => {
      recorded.guidelines.push(lines);
      guidelines = { ...guidelines, lines };
      return guidelines;
    },
    devices: async () => ({ devices, forgotten, nameLimit: 40 }),
    assignDevice: async (id, assignment) => {
      recorded.assignments.push({ id, assignment });
      const updated = devices.map((device) =>
        device.id === id ? { ...device, ...assignment } : device,
      );
      devices = updated;
      return updated.find((device) => device.id === id)!;
    },
    removeDevice: async (id) => {
      recorded.devicesRemoved.push(id);
      // Set aside rather than destroyed, as the panel does: what was removed keeps its
      // job and its name so putting it back can give them.
      const gone = devices.find((device) => device.id === id);
      if (gone !== undefined) forgotten = [...forgotten, gone];
      devices = devices.filter((device) => device.id !== id);
    },
    recallDevice: async (id) => {
      const back = forgotten.find((device) => device.id === id);
      if (back !== undefined) devices = [...devices, back];
      forgotten = forgotten.filter((device) => device.id !== id);
    },
    identifyDevice: async (id) => {
      recorded.identified.push(id);
    },
    lookForDevices: async () => {
      recorded.looked.push("asked");
    },
    usage: async (): Promise<UsageAnswer> => ({
      usage: {
        period: "2026-08",
        total: {
          calls: 220,
          billedCalls: 215,
          inputTokens: 123_202,
          outputTokens: 46_230,
          cachedInputTokens: 61_200,
          reasoningTokens: 640,
        },
        byKind: {
          image: {
            calls: 211,
            billedCalls: 206,
            inputTokens: 118_360,
            outputTokens: 44_820,
            cachedInputTokens: 61_200,
            reasoningTokens: 0,
          },
          text: {
            calls: 3,
            billedCalls: 3,
            inputTokens: 42,
            outputTokens: 90,
            cachedInputTokens: 0,
            reasoningTokens: 0,
          },
          read: {
            calls: 6,
            billedCalls: 6,
            inputTokens: 4_800,
            outputTokens: 1_320,
            cachedInputTokens: 0,
            reasoningTokens: 640,
          },
        },
      },
      limit: 900,
      maxLimit: 20_000,
      spent: 215,
      reached: false,
      changedAt: 0,
      changedBy: "",
    }),
    setLimit: async (calls) => {
      recorded.limitSetTo.push(calls);
      const before = await base.usage();
      return { ...before, limit: calls, reached: false, changedAt: NOW, changedBy: "acct-demo" };
    },
    askAgain: async (pictureId) => {
      recorded.askedAgain.push(pictureId);
      standing = {
        id: `ask-${recorded.askedAgain.length}`,
        kind: "showAgain",
        subject: pictureId,
        askedAt: NOW,
      };
      return standing;
    },
    beginNow: async () => {
      recorded.begunNow += 1;
      standing = {
        id: `ask-begin-${recorded.begunNow}`,
        kind: "beginNow",
        subject: "any",
        askedAt: NOW,
      };
      return standing;
    },
    standingRequest: async () => standing,

    experiences: async (state) => afternoons.filter((row) => row.state === state),
    decideExperience: async (id, state) => {
      recorded.experienceDecisions.push({ id, state });
      afternoons = afternoons.map((row) => (row.id === id ? { ...row, state } : row));
    },

    say: async (what) => {
      recorded.said.push(what);
      const [hours = "0", minutes = "0"] = (what.at ?? "").split(":");
      const one: Said = {
        id: `say_${recorded.said.length}`,
        says: what.says,
        writtenAt: NOW,
        minutes: what.says === "end_by" ? Number(hours) * 60 + Number(minutes) : 0,
      };
      waiting = [...waiting, one];
      return one;
    },
    messages: async () => waiting,
  };

  return { ...base, ...overrides, recorded };
}
