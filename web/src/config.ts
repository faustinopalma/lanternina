/* Values that change between environments. Kept apart from the components so they can be
 * read and corrected without touching logic. None of these is a secret: a single-page
 * application cannot hold one.
 */
export const config = {
  clientId: "e80af2eb-6eb5-4524-b8d1-aef90717e10a",

  // The tenant GUID, not the domain form: msal-browser 5 fetches the domain form's
  // metadata (HTTP 200) and then rejects it with endpoints_resolution_error. Measured
  // 18 August 2026; both forms publish the same issuer, endpoints and keys.
  // No /v2.0 here: MSAL appends it, and a doubled segment fails without saying why.
  authority: "https://lantessveb.ciamlogin.com/79825125-8a69-4adc-8eba-831c7decedad",

  // Required for any authority outside login.microsoftonline.com. Without it MSAL refuses
  // the authority as untrusted before a single request leaves the browser.
  knownAuthorities: ["lantessveb.ciamlogin.com"],

  // The scope that decides who the token is addressed to. Asking for the wrong one yields
  // a valid token the panel will refuse.
  scopes: ["api://e80af2eb-6eb5-4524-b8d1-aef90717e10a/access_as_parent"],

  apiBase:
    "https://ca-lanternina-dev-api.graystone-035aecb2.swedencentral.azurecontainerapps.io",
} as const;

/* The administration page signs in against the workforce tenant, which is a different
 * directory from the one parents use. Two applications, two audiences: a parent's token
 * is refused by the API's audience check before any question of roles is asked.
 *
 * Read from the build environment rather than written here, because these values do not
 * exist until the app registration is made — and a plausible-looking placeholder would
 * fail at sign-in with a message about the tenant instead of about the configuration.
 */
const adminClientId = import.meta.env.VITE_ADMIN_CLIENT_ID ?? "";
const adminTenantId = import.meta.env.VITE_ADMIN_TENANT_ID ?? "";

export const adminConfig = {
  clientId: adminClientId,
  authority: adminTenantId ? `https://login.microsoftonline.com/${adminTenantId}` : "",
  // One scope, named after the API rather than after a function. What an administrator may
  // do is carried by app roles, which is what the API checks; a scope per function would
  // look like it separated permissions without separating anything.
  scopes: adminClientId ? [`api://${adminClientId}/access_as_admin`] : [],
  apiBase: config.apiBase,
  configured: Boolean(adminClientId && adminTenantId),
} as const;
