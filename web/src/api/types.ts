/** The shapes the panel's API answers with. Named as the JSON is, so a field can be
 *  traced from here to `panel/app.py` without a translation step. */

export interface Me {
  accountId: string;
  householdId: string | null;
  status: string;
}

export interface Proposal {
  id: string;
  kind: string;
  agent: string;
  rationale: string;
  createdAt: number;
  state: string;
  contentKind: string;
  body: string;
}

/** The decisions a parent may take. Withdrawal is not one of them yet. */
export type Decision = "approved" | "rejected";

export interface Picture {
  id: string;
  theme: string;
  createdAt: number;
  kind: string;
}

export interface PicturePage {
  pictures: Picture[];
  page: number;
  perPage: number;
  pages: number;
  total: number;
  pageSizes: number[];
}

export interface Theme {
  id: string;
  label: string;
}

/** One sentence the parent wrote, kept as they wrote it. `read` says whether the house
 *  has looked at it yet, which is false until the house asks: the panel cannot interpret
 *  anything at the moment it is typed. */
export interface Reminder {
  id: string;
  text: string;
  createdAt: number;
  read: boolean;
  readAt: number;
}

export interface Reminders {
  reminders: Reminder[];
  textLimit: number;
}

export interface Rhythm {
  quietFrom: string;
  quietUntil: string;
  cadenceMinutes: number;
  minCadenceMinutes: number;
  maxCadenceMinutes: number;
}

export interface NewRhythm {
  quietFrom: string;
  quietUntil: string;
  cadenceMinutes: number;
}

/** Exactly the fields `prompt_hints()` lets out of the house. There is no field for a
 *  name, here or on the route, which is what keeps it out of a model prompt. */
export interface NewPreferences {
  interests: string[];
  avoid: string[];
  difficulty: string;
  variety: string;
  maxWordsPerLine: number;
  language: string;
}

export interface Preferences extends NewPreferences {
  difficultyChoices: string[];
  varietyChoices: string[];
  languageChoices: string[];
  wordsPerLineChoices: number[];
}

/** One thing in the house. `label` is what it calls itself — the id a display puts on its
 *  own screen, or the mDNS service name — and `name` is what the parent called it. The
 *  battery fields are present only for a display that has reported. */
export interface Device {
  id: string;
  kind: string;
  label: string;
  name: string;
  jobs: string[];
  jobChoices: string[];
  model: string;
  address: string;
  nameRefused: boolean;
  level?: string;
  lastSeen: number;
  silentSeconds: number;
  silent: boolean;
}

export interface Inventory {
  devices: Device[];
  nameLimit: number;
}

/** What the parent decided about one thing. Either half may be sent on its own: naming a
 *  printer and telling it to print are two moments. */
export interface NewAssignment {
  jobs?: string[];
  name?: string;
}

export interface Usage {
  calls: number;
  billedCalls: number;
  inputTokens: number;
  outputTokens: number;
  cachedInputTokens: number;
  reasoningTokens: number;
}

export interface UsageAnswer {
  usage: Usage;
  cap: number;
}

/** What `/api/me` said, without the number it said it with: an HTTP code is our problem
 *  and has no business being read by a parent. */
export type Admission =
  | { kind: "in"; me: Me }
  | { kind: "pending" }
  | { kind: "noAuth" }
  | { kind: "refused" };

/** `rejected` marks a body the panel refused as unusable — a theme it will not take, for
 *  instance — as opposed to a call that did not get through. */
export class ApiError extends Error {
  readonly rejected: boolean;

  constructor(message: string, rejected = false) {
    super(message);
    this.name = "ApiError";
    this.rejected = rejected;
  }
}

export interface Api {
  admission(): Promise<Admission>;
  proposals(): Promise<Proposal[]>;
  decide(id: string, state: Decision): Promise<void>;
  pictures(page: number, perPage: number): Promise<PicturePage>;
  pictureContent(id: string): Promise<Blob>;
  themes(): Promise<Theme[]>;
  addTheme(label: string): Promise<Theme>;
  removeTheme(id: string): Promise<void>;
  reminders(): Promise<Reminders>;
  addReminder(text: string): Promise<Reminder>;
  rewriteReminder(id: string, text: string): Promise<Reminder>;
  removeReminder(id: string): Promise<void>;
  rhythm(): Promise<Rhythm>;
  saveRhythm(rhythm: NewRhythm): Promise<Rhythm>;
  preferences(): Promise<Preferences>;
  savePreferences(preferences: NewPreferences): Promise<Preferences>;
  devices(): Promise<Inventory>;
  assignDevice(id: string, assignment: NewAssignment): Promise<Device>;
  removeDevice(id: string): Promise<void>;
  usage(): Promise<UsageAnswer>;
}
