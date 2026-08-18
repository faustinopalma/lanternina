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

  async function json<T>(path: string, options: RequestInit = {}): Promise<T> {
    const response = await call(path, options);
    if (!response.ok) throw new ApiError(path, response.status === 400);
    return (await response.json()) as T;
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
      const answer = await json<{ proposals: Proposal[] }>("/api/proposals");
      return answer.proposals;
    },

    async decide(id: string, state: Decision): Promise<void> {
      // The whole effect of an approval: a row changes state. Nothing is enqueued, nobody
      // is notified, and the house finds out when it next asks.
      await json(`/api/proposals/${id}/decision`, write({ state, note: "" }));
    },

    pictures: (page: number, perPage: number) =>
      json<PicturePage>(`/api/pictures?page=${page}&perPage=${perPage}`),

    async pictureContent(id: string): Promise<Blob> {
      const response = await call(`/api/pictures/${id}/content`);
      if (!response.ok) throw new ApiError("picture");
      return response.blob();
    },

    async themes(): Promise<Theme[]> {
      const answer = await json<{ themes: Theme[] }>("/api/themes");
      return answer.themes;
    },

    addTheme: (label: string) => json<Theme>("/api/themes", write({ label })),

    async removeTheme(id: string): Promise<void> {
      await json(`/api/themes/${id}/remove`, { method: "POST" });
    },

    rhythm: () => json<Rhythm>("/api/rhythm"),
    saveRhythm: (rhythm: NewRhythm) => json<Rhythm>("/api/rhythm", write(rhythm)),

    preferences: () => json<Preferences>("/api/preferences"),
    savePreferences: (preferences: NewPreferences) =>
      json<Preferences>("/api/preferences", write(preferences)),

    async devices(): Promise<Device[]> {
      const answer = await json<{ devices: Device[] }>("/api/devices");
      return answer.devices;
    },

    usage: () => json<UsageAnswer>("/api/usage"),
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
