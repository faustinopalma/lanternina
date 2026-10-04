import { config } from "@/config";

const INVITE = "lanternina.portal.invite";
const PORTAL = "lanternina.portal.return";

export function portalEntry(): boolean {
  try {
    if (window.location.pathname.replace(/\/$/, "") === "/portal") {
      sessionStorage.setItem(PORTAL, "1");
      const token = new URLSearchParams(window.location.hash.slice(1)).get("invite");
      if (token && /^[A-Za-z0-9_-]{40,100}$/.test(token)) {
        sessionStorage.setItem(INVITE, token);
        history.replaceState(null, "", "/portal");
      }
      return true;
    }
    return sessionStorage.getItem(PORTAL) === "1";
  } catch { return window.location.pathname.startsWith("/portal"); }
}

export function invitationToken(): string | null {
  try { return sessionStorage.getItem(INVITE); } catch { return null; }
}

export function clearInvitation() {
  try { sessionStorage.removeItem(INVITE); } catch {}
}

export function clearPortalReturn() {
  try { sessionStorage.removeItem(PORTAL); } catch {}
}

export async function sessionDestination(bearer: () => Promise<string | null>):
Promise<"parent" | "adolescent" | "new"> {
  const token = await bearer();
  if (!token) throw new Error("signin_required");
  const response = await fetch(`${config.apiBase}/api/session`, {
    cache: "no-store", signal: AbortSignal.timeout(60_000),
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) throw new Error("session_unavailable");
  const { destination } = await response.json();
  if (!["parent", "adolescent", "new"].includes(destination)) throw new Error("invalid_session");
  return destination;
}