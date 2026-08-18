/* One place that talks to the panel's API, so a bearer token is attached in one place and
 * nothing else in the interface knows a token exists. Components take an `Api`, which is
 * why the tests can hand them a fake one. */
import { createContext, use, type ReactNode } from "react";

import { config } from "@/config";

import {
  ApiError,
  type Admission,
  type Api,
  type Decision,
  type Device,
  type NewPreferences,
  type NewRhythm,
  type PicturePage,
  type Preferences,
  type Proposal,
  type Rhythm,
  type Theme,
  type UsageAnswer,
} from "./types";

/** Opening the dashboard is the one event that may warm its read/write API. The response
 *  is irrelevant: this overlaps scale-from-zero with MSAL and creates no work in the
 *  house. */
export function warmUp(): void {
  void fetch(`${config.apiBase}/health`, { cache: "no-store" }).catch(() => null);
}

const RHYTHM_FIELDS = [
  "quietFrom",
  "quietUntil",
  "cadenceMinutes",
  "minCadenceMinutes",
  "maxCadenceMinutes",
] as const;

const PREFERENCES_FIELDS = [
  "interests",
  "avoid",
  "difficulty",
  "variety",
  "maxWordsPerLine",
  "language",
  "difficultyChoices",
  "varietyChoices",
  "languageChoices",
  "wordsPerLineChoices",
] as const;

export function httpApi(token: string): Api {
  async function call(path: string, options: RequestInit = {}): Promise<Response> {
    return fetch(`${config.apiBase}${path}`, {
      ...options,
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
        ...(options.headers ?? {}),
      },
    });
  }

  /* An answer that does not carry what a section needs is a failure to read it, not data.
   * Showing an empty form instead would be guessing, and the parent would take the blank
   * for the truth — which is how an API left behind by a deploy looks like a setting that
   * was never chosen. */
  function shaped<T>(body: unknown, needs: readonly string[], where: string): T {
    const answer = body as Record<string, unknown> | null;
    const missing =
      answer === null || typeof answer !== "object"
        ? [...needs]
        : needs.filter((field) => answer[field] === undefined);
    if (missing.length > 0) throw new ApiError(`${where} answered without ${missing.join(", ")}`);
    return body as T;
  }

  async function json<T>(
    path: string,
    options: RequestInit = {},
    needs: readonly string[] = [],
  ): Promise<T> {
    const response = await call(path, options);
    if (!response.ok) throw new ApiError(path, response.status === 400);
    return shaped<T>(await response.json(), needs, path);
  }

  const write = (body: unknown) => ({ method: "POST", body: JSON.stringify(body) });

  return {
    async admission(): Promise<Admission> {
      const response = await call("/api/me");
      if (response.ok) return { kind: "in", me: await response.json() };
      if (response.status === 403) return { kind: "pending" };
      // 503 means the panel has no identity provider configured. Ours to fix, not the
      // parent's, so it is named rather than dressed up as a refusal.
      if (response.status === 503) return { kind: "noAuth" };
      return { kind: "refused" };
    },

    async proposals(): Promise<Proposal[]> {
      const answer = await json<{ proposals: Proposal[] }>("/api/proposals", {}, ["proposals"]);
      return answer.proposals;
    },

    async decide(id: string, state: Decision): Promise<void> {
      // The whole effect of an approval: a row changes state. Nothing is enqueued, nobody
      // is notified, and the house finds out when it next asks.
      await json(`/api/proposals/${id}/decision`, write({ state, note: "" }));
    },

    pictures: (page: number, perPage: number) =>
      json<PicturePage>(`/api/pictures?page=${page}&perPage=${perPage}`, {}, [
        "pictures",
        "page",
        "perPage",
        "pages",
        "total",
        "pageSizes",
      ]),

    async pictureContent(id: string): Promise<Blob> {
      const response = await call(`/api/pictures/${id}/content`);
      if (!response.ok) throw new ApiError("picture");
      return response.blob();
    },

    async themes(): Promise<Theme[]> {
      const answer = await json<{ themes: Theme[] }>("/api/themes", {}, ["themes"]);
      return answer.themes;
    },

    addTheme: (label: string) => json<Theme>("/api/themes", write({ label }), ["id", "label"]),

    async removeTheme(id: string): Promise<void> {
      await json(`/api/themes/${id}/remove`, { method: "POST" });
    },

    rhythm: () => json<Rhythm>("/api/rhythm", {}, RHYTHM_FIELDS),
    saveRhythm: (rhythm: NewRhythm) => json<Rhythm>("/api/rhythm", write(rhythm), RHYTHM_FIELDS),

    preferences: () => json<Preferences>("/api/preferences", {}, PREFERENCES_FIELDS),
    savePreferences: (preferences: NewPreferences) =>
      json<Preferences>("/api/preferences", write(preferences), PREFERENCES_FIELDS),

    async devices(): Promise<Device[]> {
      const answer = await json<{ devices: Device[] }>("/api/devices", {}, ["devices"]);
      return answer.devices;
    },

    usage: () => json<UsageAnswer>("/api/usage", {}, ["usage", "cap"]),
  };
}

const ApiContext = createContext<Api | null>(null);

export function ApiProvider({ api, children }: { api: Api; children: ReactNode }) {
  return <ApiContext value={api}>{children}</ApiContext>;
}

export function useApi(): Api {
  const api = use(ApiContext);
  if (api === null) throw new Error("useApi outside ApiProvider");
  return api;
}
