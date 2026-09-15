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