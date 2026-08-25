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

/** The decisions a parent may take. `withdrawn` is a second decision on something already
 *  approved, and the panel refuses it on anything else. */
export type Decision = "approved" | "rejected" | "withdrawn";

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
  /* What the house made of the sentence: "HH:MM", or empty when it could not place it. */
  at: string;
  /* Empty means every day. */
  days: string[];
  /* What the house needs to know before this can be a reminder. Empty when it does not. */
  question: string;
  /* Ways of saying the same thing, for the display to pick from. Empty means the sentence
   * is shown as it was written, which is what happens when the house could not word it. */
  words: string[];
}

export interface Reminders {
  reminders: Reminder[];
  textLimit: number;
}

/** A place to write on a page, and how much of it there is. `room` is one of `a_line`,
 *  `some_lines` and `a_box`: how much room, never where. */
export interface Space {
  label: string;
  room: string;
}

/** What kind of object the paper is, and every word that will be lettered on it. There are
 *  no coordinates: the whole page is drawn from these words, and `illustration` describes a
 *  drawing rather than anything printed as text. */
export interface Page {
  kind: string;
  title: string;
  illustration: string;
  note: string[];
  spaces: Space[];
}

/** One step of an afternoon at one of its three costs: how long it takes, and what the
 *  display says. `shared/experience.py` refuses a moment that does not carry all three. */
export interface Weighing {
  minutes: number;
  lines: string[];
}

/** One rung of the help ladder, and after how many minutes the next one arrives. */
export interface Help {
  after_minutes: number;
  lines: string[];
}

/** How to reach the ending from exactly this moment, starting from something in hand. */
export interface WayOut {
  in_hand: string;
  heading: string;
  lines: string[];
  minutes: number;
}

/** One step of an afternoon. The four acts are `shared/experience.py`'s, and a `collect`
 *  is the only one that branches: `then` names a later moment, or is `ask`, which means
 *  the rest is written when the page comes back. */
export interface Moment {
  act: string;
  id: string;
  heading: string;
  weights: Record<string, Weighing>;
  help: Help[];
  way_out: WayOut;
  page?: Page;
  instead?: string[];
  outcomes?: { when: string; then: string }[];
  if_no_page?: string;
}

/** The ten dimensions an afternoon was drawn along. Every one of them is about the
 *  afternoon; there is no dimension here that is about a person. */
export type Drawn = Record<string, string>;

export interface ExperiencePlan {
  experience_id: string;
  title: string;
  overview: string;
  minutes: number;
  drawn?: Drawn;
  moments: Moment[];
}

/** An afternoon a model devised for this house, waiting for the parent to decide.
 *  `overview` is what approval is given to; `experience` is the whole plan, present so
 *  that an overview is not the only thing that exists. */
export interface OfferedExperience {
  id: string;
  title: string;
  overview: string;
  minutes: number;
  createdAt: number;
  state: string;
  experience: ExperiencePlan;
  /* When the house began it, or 0. Written by the house, not by anybody deciding: it is
   * what stops an approved afternoon being handed over again the next day. */
  begunAt: number;
}

export interface Rhythm {
  quietFrom: string;
  quietUntil: string;
  cadenceMinutes: number;
  minCadenceMinutes: number;
  maxCadenceMinutes: number;
  /* Which days an afternoon may begin on, and from what hour. Empty means none, which is
   * where every household starts: nothing happens until the parent picks a day. */
  afternoonDays: string[];
  afternoonFrom: string;
  /* Where the house is, as an IANA name. Empty means the hub falls back to whatever zone
   * its own machine is set to, which is how one house honoured every chosen hour an hour
   * late for a week without anything being able to say so. */
  timeZone: string;
  dayChoices: string[];
}

export interface NewRhythm {
  quietFrom: string;
  quietUntil: string;
  cadenceMinutes: number;
  afternoonDays: string[];
  afternoonFrom: string;
  timeZone: string;
}

/** Exactly the fields `prompt_hints()` returns. There is no field for a name, here or on
 *  the route, because nothing has needed one yet. */
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

/** How far the house may improvise when an afternoon did not go the way it was planned.
 *  `lines` are the parent's and can be changed here; `fixed` are ours, sent so that what
 *  they are adding to is legible, and refused if they come back. */
export interface Guidelines {
  lines: string[];
  fixed: string[];
  updatedAt: number;
  lineLimit: number;
  maxLines: number;
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
  /** Taken off the list by the parent. Kept apart: the only thing to do with one is put
   *  it back, with the job and the name it had. */
  forgotten: Device[];
  nameLimit: number;
}

/** What the parent decided about one thing. Either half may be sent on its own: naming a
 *  printer and telling it to print are two moments. */
export interface NewAssignment {
  jobs?: string[];
  name?: string;
}

export interface UsageTotals {
  calls: number;
  billedCalls: number;
  inputTokens: number;
  outputTokens: number;
  cachedInputTokens: number;
  reasoningTokens: number;
}

/** Told apart by kind as well as together: a picture and a wording cost different amounts
 *  of different things, and one figure covering both says less than it looks like. */
export interface Usage {
  period: string;
  total: UsageTotals;
  byKind: Record<string, UsageTotals>;
}

export interface UsageAnswer {
  usage: Usage;
  limit: number;
  maxLimit: number;
  spent: number;
  /** The house is being refused right now. */
  reached: boolean;
  /** Zero when nobody has set the limit, so a default never looks like a decision. */
  changedAt: number;
  changedBy: string;
}

/** Something the parent asked the house to do, still waiting to be collected. The panel
 *  records it and cannot deliver it: the house finds it when it next looks. */
export interface HouseRequest {
  id: string;
  kind: string;
  subject: string;
  askedAt: number;
}

/** One of the two things a parent may say to an afternoon that is already running.
 *  `shared/message.py` says why there is no third and why none of them is a sentence:
 *  `end_by` moves the hour it is over by, `close_now` brings that hour to now. `at` is
 *  "HH:MM" and is read only for `end_by`. */
export interface NewSaid {
  says: string;
  at?: string;
}

/** One said thing the house has not yet come for. `minutes` is past midnight, which is
 *  what the house reads; the panel sends and shows the hour the parent chose. */
export interface Said {
  id: string;
  says: string;
  writtenAt: number;
  minutes: number;
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
  approved(): Promise<Proposal[]>;
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
  guidelines(): Promise<Guidelines>;
  saveGuidelines(lines: string[]): Promise<Guidelines>;
  devices(): Promise<Inventory>;
  assignDevice(id: string, assignment: NewAssignment): Promise<Device>;
  removeDevice(id: string): Promise<void>;
  recallDevice(id: string): Promise<void>;
  identifyDevice(id: string): Promise<void>;
  usage(): Promise<UsageAnswer>;
  setLimit(calls: number): Promise<UsageAnswer>;
  askAgain(pictureId: string): Promise<HouseRequest>;
  /** Ask that an afternoon begin at the house's next look, whatever the hour says. */
  beginNow(): Promise<HouseRequest>;
  standingRequest(): Promise<HouseRequest | null>;
  experiences(state: string): Promise<OfferedExperience[]>;
  decideExperience(id: string, state: Decision): Promise<void>;
  say(said: NewSaid): Promise<Said>;
  messages(): Promise<Said[]>;
}
