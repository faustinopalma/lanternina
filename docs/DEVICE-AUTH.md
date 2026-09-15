# Household-bound hub authentication

Every device route uses `panel.gate.require_device`. The server validates `X-Device-Key` against the key digest configured for the route's `household_id` before the endpoint can read records, write state or call a model. An unknown household, missing key or wrong key receives the same HTTP 403 response. No configured bindings yields HTTP 503. Development identity headers do not bypass this check.

`LANTERNINA_DEVICE_KEY_HASHES` is a JSON object mapping household IDs to lowercase SHA-256 digests. Each digest must identify exactly one household. Duplicate JSON keys, duplicate digests and malformed bindings are rejected at startup without echoing their values. Digests are computed from cryptographically random API keys, not passwords; use `secrets.token_urlsafe(32)` when provisioning a new hub. Hashing a weak human-selected value does not make it a secure API key.

The raw key stays in the protected hub configuration and the owner's ignored recovery file. It travels only over HTTPS to the API. The new deployment scripts parse the local YAML through `python -m tools.device_bindings secrets.local.yaml`, merge existing bindings and pass only digests to Azure. The command requires a key at least 32 characters long, checks the association and refuses to silently replace an existing digest. The digest cannot be presented as the device credential. Configuration write access can change authorization and must remain restricted to deployment operators.

For compatibility, `LANTERNINA_DEVICE_KEY` works only with an explicit `LANTERNINA_DEVICE_HOUSEHOLD`. An unbound legacy key grants no access. Do not configure the same household through both mechanisms. After migrating to hashes, remove the legacy key environment variable and its unused Container Apps secret. Keep other secrets, identities, environment values and networking unchanged.

## Rotation and revocation

Provision a separate random key for each family. To rotate, securely replace the hub's protected key and the corresponding server digest, then verify an authenticated read. The current format accepts one key per family, so rotation has a brief coordinated interruption; it does not provide overlapping keys. Replacing a digest rejects the old key. Removing the family binding revokes all device requests from that hub. Configuration changes take effect when the new service revision receives traffic; a revision still serving the previous configuration can retain access until it drains.

An API key is a bearer credential. Possession grants the configured device operations for that household, not parent or administrator operations. It does not attest the physical device or prevent replay inside the authorized household. Client certificates or short-lived device tokens would add stronger device identity but require a separate provisioning and renewal workflow. Parent and adolescent authorization and their user-requested deletion paths remain unchanged. The parent-account suspension rules for the adolescent portal are separate from hub-key revocation.

## Verification

The regression test first reproduced HTTP 200 when a valid key changed the family in the URL. After correction, the authorized family's read succeeds while another family's read and deletion return 403 and leave the stored bytes unchanged. A test walks all registered device routes, including scan aliases and portal-photo polling, and checks wrong-family, missing and wrong keys before endpoint logic. Tests also cover configuration parsing, rotation, revocation and the protected export command. Multi-household hardware operation has not been exercised.

The design follows [Microsoft's tenant mapping guidance](https://learn.microsoft.com/azure/architecture/guide/multitenant/considerations/map-requests): map a unique random API key to a tenant on the server, and plan issuance, storage, rotation and revocation. Consulted on 15 September 2026.