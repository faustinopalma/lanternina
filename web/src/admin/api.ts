/* The only place that talks to the administration routes.
 *
 * Separate from `@/api/client` on purpose: the parent's API object carries a parent's
 * token, and a page that held both would be one mistake away from sending the wrong one.
 */
import { adminConfig } from "@/config";

/** A sign-up waiting for a decision. The fields are the ones `panel/admin.py` sends, and
 *  there are no others: no household, no subject, nothing about a person. */
export interface Waiting {
  id: string;
  contact: string;
  status: string;
  createdAt: number;
  decidedAt: number | null;
}

/** What an administrator may set. The API refuses anything else with 400. */
export type Admission = "active" | "rejected";

/** Told apart because the remedies differ: sign in again, ask for the role, or fix the
 *  deployment. */
export type Standing = "in" | "notAdmin" | "notConfigured" | "failed";

export interface AdminApi {
  standing: () => Promise<Standing>;
  waiting: () => Promise<Waiting[]>;
  decide: (id: string, state: Admission) => Promise<void>;
}

export function httpAdminApi(token: string): AdminApi {
  const call = (path: string, options: RequestInit = {}) =>
    fetch(`${adminConfig.apiBase}${path}`, {
      ...options,
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
        ...(options.headers ?? {}),
      },
    });

  return {
    async standing(): Promise<Standing> {
      const response = await call("/api/admin/me");
      if (response.ok) return "in";
      // 503 means no administrator provider is configured at all. Ours to fix, and saying
      // so beats a refusal the administrator would try to solve by signing in again.
      if (response.status === 503) return "notConfigured";
      if (response.status === 403) return "notAdmin";
      return "failed";
    },

    async waiting(): Promise<Waiting[]> {
      const response = await call("/api/admin/accounts");
      if (!response.ok) throw new Error("accounts");
      const body: unknown = await response.json();
      const accounts = (body as { accounts?: Waiting[] }).accounts;
      if (accounts === undefined) throw new Error("accounts");
      return accounts;
    },

    async decide(id: string, state: Admission): Promise<void> {
      const response = await call(`/api/admin/accounts/${id}/decision`, {
        method: "POST",
        body: JSON.stringify({ state, note: "" }),
      });
      if (!response.ok) throw new Error("decision");
    },
  };
}
