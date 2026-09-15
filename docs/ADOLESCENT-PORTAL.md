# Adolescent portal

The parent enters the adolescent's email in the Adolescent access section and generates a code. The panel offers the code and an invitation link for copying and sharing outside Lanternina. The adolescent registers or signs in through the existing identity provider, then pastes the code in `/portal` and accepts the invitation. Opening the shared link fills the code automatically. The application stores that identity-provider subject in a separate membership register; it never creates an approved parent account for that subject.

The adolescent can take or choose a photograph, inspect the preview, send it, see its processing state and delete it. The parent sees the photograph in the family archive. Each adolescent sees only photographs submitted by their own membership. Revocation prevents subsequent portal requests, including requests with a token issued before revocation. A suspended parent also closes the access they granted.

## Activation

The API needs the existing OIDC and private Blob Storage configuration. The identity provider's user flow must allow registration and emit the recipient's email as `email` or `preferred_username`, as the current token verifier expects. Registration, email verification, password recovery and authentication remain the provider's responsibility. The invitation secret and a matching authenticated account are both required for membership.

The frontend uses the current MSAL application and root redirect URI. It saves the invitation in session storage before authentication and removes the secret from the visible URL. Acceptance clears the stored secret. Browser session storage must be available for this redirect flow. No new redirect URI is needed when `/portal` is on the panel's existing origin. The existing SPA fallback serves `/portal`.

Invitations require no email submission service or additional environment variables. The owner excluded Azure Communication Services on 15 September 2026. The SMTP adapter and its configuration were removed. The code replaces invitation delivery, not registration: the identity provider can still send its own email verification messages.

Deploy the API and frontend, then update the hub's Python code and restart its existing camera hub service. The new hub pulls `/api/device/{household}/portal-photos/pull`, so update the API before the hub. The frontend and hub must target the same API and household data. Existing infrastructure, identities and network settings remain unchanged.

## Invitations and storage

An invitation carries 32 random bytes in URL-safe encoding. Only its SHA-256 digest is stored. The creation response returns the code once with `Cache-Control: no-store`; the code remains in the parent's open page, not in browser storage or subsequent invitation lists. A lost code must be regenerated. It expires after 72 hours. Acceptance is atomic; competing accounts cannot consume the same invitation. Repeated acceptance by the same active member returns the existing result. Generating another code for the same address atomically revokes earlier outstanding invitations in that household. Revoking a membership also invalidates outstanding invitations to its address. Codes created by the earlier email implementation remain redeemable until expiry or revocation.

Each household may generate ten invitations in a rolling 24-hour period. Each authenticated subject may attempt redemption twenty times in a 15-minute window. Invites, bounded attempt counters and memberships live in the private `portal/access.json` blob in the pictures container. Conditional ETag writes handle concurrent API replicas. Every access lookup retrieves this shared document, so it suits the current small installation rather than an unbounded population. The memory implementation is for local development and tests. A Cosmos-configured deployment without Blob Storage refuses to start rather than silently forgetting memberships.

The browser accepts JPEG, PNG and WebP inputs up to 25 MB and converts them to a JPEG bounded by 1600 by 1200 pixels. The API independently limits uploads to 12 MB and decoded images to 12 megapixels. It re-encodes without EXIF metadata, with a stored JPEG limit of 750,000 bytes. HEIC requires conversion to a supported format. Photograph time means server receipt time, not the capture time of an older library image.

An adolescent may retain 200 photographs and reserve up to 1,000 uploads per rolling 24 hours. Concurrent uploads reserve capacity in the membership record. Recent reservations cover the interval between the archive listing and storage; reservations expire after 120 seconds when no stored photograph exists. Completed photographs remain subject to the retained-photo count. Deletions free retained capacity. A retry uses the same identifier and cannot reset a completed photograph to pending. The selected photograph remains in the open page after a network failure; closing the page loses an unsent selection.

Photo content endpoints require authentication and return `Cache-Control: no-store`. Deletion replaces archived bytes with the existing tombstone and propagates to the hub on its next synchronization. It does not undo an already printed page or completed activity. Revocation preserves photographs for the parent; it is not a request to delete family photographs.

## Home processing

The camera hub retrieves at most ten pending portal photographs per synchronization and stores them through its existing SQLite receipt path. Synchronization follows the existing worker interval of 60 seconds, plus network and processing time. A disconnected home leaves the photograph pending in the cloud.

The hub associates receipt time with a single waiting camera-return moment when one exists. That photograph follows the existing activity reading and continuation path. Otherwise the hub displays it on an assigned photo display, or archives it when no display is assigned. The portal does not promise a model response for every photograph. Its done state means that the hub completed this existing processing path.

## Verification

The code-based flow was deployed to https://app.lanternina.com/portal on 15 September 2026. The parent creates invitations at https://app.lanternina.com/#adolescents. API revision 0000123 runs image portal-code-20260915071502; the existing hub synchronizer was updated with a recoverable backup. Live checks verified the new assets, authentication refusals, CORS, the registration redirect and an authenticated hub pull. The identity provider presents its registration option. No real adolescent account was created during deployment, so its first interactive registration and redemption remain to be exercised by the family.

The implementation was checked locally on 15 September 2026. Backend tests cover code generation without email, no-store responses, expiry, regeneration, revocation, matching email, redemption attempt limits, parent suspension, concurrent acceptance, household and sibling isolation, Blob ETag conflicts and restart, concurrent upload capacity, image validation, EXIF removal, idempotency, hub synchronization, processing state and deletion. Frontend tests cover code and link copying, manual redemption and correction, authentication return, explicit acceptance, mismatched email, network retry, parent controls, photo preview, retry with the same identifier and confirmed deletion.

Run `python -m pytest tests/test_adolescent_portal.py tests/test_panel.py tests/test_photo_blob.py tests/test_photo_sync.py tests/test_photos.py tests/test_photo_store.py tests/test_scan_archive.py tests/test_web_i18n.py -q`, then `npm --prefix web test` and `npm --prefix web run build`. Use the repository interpreter and keep live model credentials out of the test environment.

Run `npm --prefix web run dev` and open `/portal?preview` for a local UI preview. This development-only mode stores synthetic photographs in browser memory. It does not authenticate, send mail, persist photographs remotely or contact equipment. The normal `/portal` path uses authentication and API requests. Browser checks exercised preview, upload and confirmed deletion at viewport widths of 390 and 1440 pixels; images loaded and no horizontal text overflow was measured.

A production acceptance test needs registration through the configured identity provider and an updated connected hub. Verify code generation and copying, acceptance with the invited address, rejection of another address, denial of parent APIs from the adolescent account, photograph processing and access revocation while the adolescent is signed in. Local tests do not establish identity-provider registration or physical-device behaviour.