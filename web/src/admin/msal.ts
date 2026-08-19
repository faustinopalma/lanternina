/* Sign in as an administrator, then hold one access token for the administration routes.
 *
 * A separate instance from the parent's, against a separate directory. They never meet:
 * this file is only in the administration bundle, and its cache key is a different client
 * id, so signing out of one leaves the other alone.
 */
import {
  InteractionRequiredAuthError,
  PublicClientApplication,
  type AccountInfo,
} from "@azure/msal-browser";

import { adminConfig } from "@/config";

// The page the identity provider sends the administrator back to, which is this one.
export const redirectUri = `${window.location.origin}/admin`;

export const adminMsal = new PublicClientApplication({
  auth: {
    clientId: adminConfig.clientId,
    authority: adminConfig.authority,
    redirectUri,
  },
  cache: { cacheLocation: "sessionStorage" },
});

/** Resolves to a token, or to null when a redirect is under way and this page is about to
 *  be replaced. */
export async function adminBearerFor(account: AccountInfo): Promise<string | null> {
  const request = { scopes: [...adminConfig.scopes], account };
  try {
    const result = await adminMsal.acquireTokenSilent(request);
    return result.accessToken;
  } catch (error) {
    if (error instanceof InteractionRequiredAuthError) {
      await adminMsal.acquireTokenRedirect(request);
      return null;
    }
    throw error;
  }
}

export const adminSignIn = () => adminMsal.loginRedirect({ scopes: [...adminConfig.scopes] });

export const adminSignOut = () => adminMsal.logoutRedirect({ postLogoutRedirectUri: redirectUri });
