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
  NewAssignment,
  NewPreferences,
  NewRhythm,
  PicturePage,
  Preferences,
  Proposal,
  Rhythm,
  Theme,
  UsageAnswer,
} from "@/api/types";

export interface Recorded {
  decisions: { id: string; state: Decision }[];
  rhythm: NewRhythm[];
  preferences: NewPreferences[];
  themesAdded: string[];
  themesRemoved: string[];
  assignments: { id: string; assignment: NewAssignment }[];
  devicesRemoved: string[];
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

const SAMPLE_PICTURES: PicturePage = {
  pictures: Array.from({ length: 6 }, (_, index) => ({
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
    job: "picture",
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
    job: "",
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
    job: "print",
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
    themesAdded: [],
    themesRemoved: [],
    assignments: [],
    devicesRemoved: [],
  };
  let themes: Theme[] = [
    { id: "theme-1", label: "gatti che dormono" },
    { id: "theme-2", label: "vele in porto" },
  ];
  let devices: Device[] = SAMPLE_DEVICES;
  let rhythm: Rhythm = {
    quietFrom: "21:30",
    quietUntil: "07:00",
    cadenceMinutes: 60,
    minCadenceMinutes: 1,
    maxCadenceMinutes: 1440,
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

  const base: Api = {
    admission: async (): Promise<Admission> => ({
      kind: "in",
      me: { accountId: "acct-demo", householdId: "house-demo", status: "active" },
    }),
    proposals: async () => SAMPLE_PROPOSALS,
    decide: async (id, state) => {
      recorded.decisions.push({ id, state });
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
    devices: async () => ({ devices, nameLimit: 40 }),
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
      devices = devices.filter((device) => device.id !== id);
    },
    usage: async (): Promise<UsageAnswer> => ({
      usage: {
        calls: 214,
        billedCalls: 209,
        inputTokens: 118_402,
        outputTokens: 44_910,
        cachedInputTokens: 61_200,
        reasoningTokens: 0,
      },
      cap: 900,
    }),
  };

  return { ...base, ...overrides, recorded };
}
