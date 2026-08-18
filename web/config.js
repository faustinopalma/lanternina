// Values that change between environments. Kept out of app.js so they can be read and
// corrected without touching logic. None of these is a secret: a single-page application
// cannot hold one.
window.LANTERNINA = {
  clientId: "e80af2eb-6eb5-4524-b8d1-aef90717e10a",

  // No /v2.0 here on purpose: MSAL appends it when fetching authority metadata, and a
  // doubled segment produces a metadata fetch that fails without saying why.
  authority: "https://lantessveb.ciamlogin.com/lantessveb.onmicrosoft.com",

  // Required for any authority outside login.microsoftonline.com. Without it MSAL refuses
  // the authority as untrusted before a single request leaves the browser.
  knownAuthorities: ["lantessveb.ciamlogin.com"],

  // The scope that decides who the token is addressed to. Asking for the wrong one yields
  // a valid token the panel will refuse.
  scopes: ["api://e80af2eb-6eb5-4524-b8d1-aef90717e10a/access_as_parent"],

  apiBase: "https://ca-lanternina-dev-api.graystone-035aecb2.swedencentral.azurecontainerapps.io",
};
