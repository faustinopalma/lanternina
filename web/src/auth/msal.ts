/* Sign in, then hold one access token for the panel.
 *
 * MSAL comes from npm rather than a CDN: the file is pinned by the lockfile, ships from
 * the same origin as the panel, and lets the page's script-src stay 'self'.
 */
import {
  InteractionRequiredAuthError,
  PublicClientApplication,
  type AccountInfo,
} from "@azure/msal-browser";

import { config } from "@/config";

export const msalInstance = new PublicClientApplication({
  auth: {
    clientId: config.clientId,
    authority: config.authority,
    knownAuthorities: [...config.knownAuthorities],
    redirectUri: window.location.origin,
    // navigateToLoginRequestUrl is gone in msal-browser 5, and so is the behaviour it
    // turned off: returning from the identity provider now lands on redirectUri and stays
    // there. Verified against the installed 5.18.0 typings on 18 August 2026.
  },
  cache: {
    // Survives a reload; cleared when the browser is closed. A refresh token in
    // localStorage would outlive the session for no benefit we need.
    cacheLocation: "sessionStorage",
  },
  // system.serverTelemetryEnabled defaults to false in 5.18.0, so nothing about this
  // browser is sent alongside a token request. Read from the shipped source, not assumed.
});

/** Resolves to a token, or to null when a redirect is under way and this page is about to
 *  be replaced. */
export async function bearerFor(account: AccountInfo): Promise<string | null> {
  const request = { scopes: [...config.scopes], account };
  try {
    const result = await msalInstance.acquireTokenSilent(request);
    return result.accessToken;
  } catch (error) {
    // Silent acquisition fails on first run and whenever consent or interaction is
    // genuinely required; a redirect is the answer, not an error to report.
    if (error instanceof InteractionRequiredAuthError) {
      await msalInstance.acquireTokenRedirect(request);
      return null;
    }
    throw error;
  }
}

export const signIn = () => msalInstance.loginRedirect({ scopes: [...config.scopes] });

export const signOut = () =>
  msalInstance.logoutRedirect({ postLogoutRedirectUri: window.location.origin });
