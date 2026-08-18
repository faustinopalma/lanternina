// Values that change between environments. Kept out of app.js so they can be read and
// corrected without touching logic. None of these is a secret: a single-page application
// cannot hold one.
window.LANTERNINA = {
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

  apiBase: "https://ca-lanternina-dev-api.graystone-035aecb2.swedencentral.azurecontainerapps.io",
};
