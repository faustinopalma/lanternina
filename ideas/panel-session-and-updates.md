# Panel session and live lists

## Report and reproduction

The parent reported a panel that sometimes stayed on the connecting screen or required signing out and back in. New experiences appeared only after a page reload. The investigation and local checks took place on 7 September 2026.

The API client captured one access token when the panel opened. Every later request reused it. The new API regression test failed because a second request never consulted the credential provider. The client now asks MSAL for a current token on each request. MSAL returns a valid cached token or renews it. Concurrent requests for the same account share the acquisition already in progress, including its interactive fallback.

The admission effect depended on MSAL's interaction state. A change during acquisition cancelled the effect's response handler. The new session test reproduced the connecting screen by changing that state before resolving the token request. Admission now belongs to a component keyed by account identity. Token acquisition events leave that component and its dashboard mounted. Admission retries a failed read once after 1.5 seconds; the retry button repeats admission without reloading the document or signing out.

The shared loader previously read each section only on mount or an explicit local reload. The new live-list tests failed on periodic refresh, returning to the tab, recovery after a background failure, and arrival of a new experience. Those cases now pass.

## Reading updates

Live reads ask again 30 seconds after the previous result. This interval is a chosen polling interval, not a measured delivery guarantee. Network and token acquisition time add to it. Polling reads existing data; it does not request model generation or start an activity in the house.

The loader skips background reads while the tab is hidden or the browser reports that it is offline. Returning to the tab, focusing the window, or reconnecting triggers a read. Each loader has at most one automatic read in flight. Unmounting removes its listeners and timer, and responses from a previous section cannot replace the current section's data.

Experiences, their pending messages, proposals, the draft list, pictures, the standing picture request, devices, and the activity trail opt into live reads. Settings forms and the draft editor keep their existing explicit-load behaviour so automatic reads do not replace unfinished edits. Components retain their keys and loaded state while refreshing, which preserves open plans and selections. A failed background refresh leaves the previous data visible and tries again later; the interface currently does not label those retained data as stale.

Polling gives the parent updates without a reload and costs repeated reads while the tab is visible. Hidden tabs do not keep requesting data. A push channel could avoid repeated reads, but would require a server-side notification path that this change does not introduce.

GET requests bypass the browser cache and have a 30-second HTTP timeout. Writes retain their existing timeout behaviour because some writes wait for model generation. MSAL governs its own token acquisition timeouts. A genuinely expired identity-provider session may still require authentication; the change preserves that check.

## Verification and remaining work

The regression tests cover current credentials per request, concurrent acquisition, one interactive redirect for concurrent callers, recovery after a failed acquisition, admission through an interaction-state change, retry without logout, new experience arrival, retained selections and plans, hidden tabs, reconnection, slow reads, failed background reads, and obsolete responses. The production build checks TypeScript in the tests as well as the application.

The local browser preview uses synthetic household data. Playwright advanced its clock across refresh intervals at 1440 by 1000 pixels and 390 by 844 pixels. The selection and open plan survived in both viewports, and the browser reported no JavaScript errors. The mobile check also found an existing layout issue in the multiple-decision button group: a 390-pixel viewport had a 406-pixel document. The group's non-wrapping button container is unchanged here.

The real identity-provider session and a real newly offered experience have not been exercised with the changed client in production. These changes have not been published. The local preview is available at `http://127.0.0.1:5182/?preview`; it uses synthetic data and does not change the house.

Microsoft documents the per-request acquisition pattern in [Acquiring and using an access token](https://learn.microsoft.com/entra/msal/javascript/browser/acquire-token#acquiring-an-access-token) and the renewal behaviour in [Token lifetimes, expiration, and renewal](https://learn.microsoft.com/entra/msal/javascript/browser/token-lifetimes#token-renewal).