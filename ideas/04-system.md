# System: infrastructure, costs, things to close

## 1. Closed: the cloud could not paint (401 PermissionDenied)

**Where it was.** `POST /api/device/{household}/paint` answered 503 carrying a
`401 PermissionDenied` from the image deployment on the AI account.

**What it turned out to be.** Two things stacked, which is why each single fix appeared to
do nothing. The managed identity had been correct all along — a diagnostic route decoding
`oid` and `appid` from the token obtained inside the container proved it in one step, after
four role assignments had been made on a deduction. Underneath the role propagation sat an
`ImportError: aiohttp package is not installed`: the async Content Safety transport needs
it and the SDK does not declare it.

**What the episode is worth keeping for.** Every hypothesis about *which* identity was
calling had been a deduction. The measurement took ten minutes and should have come first.
That diagnostic route is still there, and it returns claims only — never the token.

---

## 2. Closed: the hourly cycle

**What it is.** A timer on the hub that asks for a new picture every hour and installs it.

**How it was done.** A `systemd` timer with `OnCalendar=hourly` and `RandomizedDelaySec`,
calling the `paint` route with the device key and writing the BMP atomically over the screen
file. The hub needs no Azure credential; it holds the device key and nothing else.

**What it costs.** A refusal from the content gate, a reached cap and an unreachable cloud
are all treated the same way: keep the picture already on the wall. Going blank is never the
answer to a failure upstream.

---

## 3. Closed: the drift between the templates and what runs

**What it was.** Some live configuration was not described in the templates, so a plain
`./scripts/deploy.ps1` would have reset it.

**What it turned out to be, measured on 18 August 2026.** Three of the nineteen environment
variables on the API were absent from the template: `LANTERNINA_DEVICE_KEY`,
`LANTERNINA_CONTENT_SAFETY_ENDPOINT` and `LANTERNINA_FOUNDRY_ACCOUNT_ENDPOINT`. Worse, and
not noticed before: the script passed five parameters and none of them were `apiImage`,
`apiTargetPort` or the sign-in settings. A run would therefore have replaced the API with
the placeholder image on port 80 and blanked the identity configuration — the panel would
have answered 404, then 503.

**How it was closed.** The two endpoints are the same AIServices host, so they are now
derived from `ai.outputs.accountEndpoint` rather than passed by hand — a value nobody can
forget. The device key is a `@secure()` parameter carried into a container-app secret, read
by the script from `secrets.local.yaml`. The script also reads the running app and hands
its image, port and sign-in settings back in, so a plain run re-applies what is there
instead of resetting it. Without a key it refuses to run at all.

**What it cost.** The key travels on the command line while the deployment runs: `az`
refuses a JSON parameter file alongside a `.bicepparam` file, which was measured rather
than assumed. On a shared machine that would matter.

**How it was checked.** `what-if` plans no change to the image or the port, keeps all four
restored variables, and removes only three ARM defaults. Hiding `secrets.local.yaml` makes
the script refuse, which was watched rather than trusted.

---

## 4. What an hourly picture costs

**What it is.** A measurement, not an estimate.

**Why.** Twenty-four images a day for thirty days is 720 generations a month. The unit price
of one image with this model is still unknown, and inventing it is not acceptable: the
difference between two cents and twenty cents an image is the difference between fifteen
euros a month and a hundred and forty.

**What is now measured.** Every call is counted per household, with the tokens the backend
reported. One 1024×1024 image came back as 12 input and 196 output tokens, so a picture is
billed in tokens rather than per picture — the assumption of "one image, one unit" was
wrong. The response also echoes `"quality": "low"`, a default nobody chose, and both size
and quality change the price.

**What is still missing.** The unit price. The budget is already configured on the
subscription; the remaining step is reading cost per deployment in Cost Management after a
day of generation, and reconciling it against our own count using the request id we store.

**What it costs.** A day of waiting. It should be done before raising the cadence, not
after.

---

## 5. Rebuilding the hub from scratch

**What it is.** A drill: take a blank card and stand everything back up.

**Why.** Some things exist only on the hub — the seal keys, the device key, the display
registry with its tokens, the Wi-Fi configuration. The weekly backup exists and has been
tested, but the **restore** never has. An unverified backup is a hope.

⚠️ "Only on the hub" is too strong, and was corrected on 18 August 2026: `secrets.local.yaml`
on the development machine holds `device_key`, `approval_key` and `safety_key`. The device
key there was verified to be the one the live API accepts. Whether the other two match what
the hub uses is **not** verified, and that is the thing to check first — it is minutes of
work and it changes how bad a lost card would be.

**How.** The installer `deploy/install-trmnl-byos.sh` already covers the display service.
The rest is missing, and what is missing most is knowing which secrets have to be
regenerated and which recovered: if the approval key is lost, all content already approved
stops being deliverable — which is the correct behaviour, but it should be known in advance.

**What it costs.** An afternoon, and a second card so the working one is not touched.

---

## 6. app.lanternina.com

**What it is.** The custom domain that answers 404 every so often.

**Why it is nearly closed.** The headers say that 404 does not come from our site: the good
responses carry HSTS and our CSP, the 404 carries only `Date` and `Transfer-Encoding`. The
measured rate fell on its own: 38% one day, then 13%, then 5% half an hour later.

**What to do.** Measure again with 60 requests. If it is at zero, touch nothing. If it has
settled above zero, delete and recreate the domain binding — the CNAME is already correct,
so no new validation is needed and the operation takes a few minutes.

**What it costs.** A few minutes of the name being unavailable. The generated host is not
involved.

---

## 7. Field names that are not Italian

**What it is.** Renaming the keys the content agent produces: `titolo`, `istruzioni`,
`esercizi`, `domanda`, `scelte`, `risposta`.

**Why.** The household's content language is meant to be a setting. It cannot be, while the
language is baked into the shape of the data: a sheet in English would still be a document
with a field called `domanda`, and the prompt that produces it asks for that field by name.
This is the obstacle in front of multilingual content, and it is in front of it rather than
beside it.

**How.** Neutral keys — `title`, `instructions`, `exercises`, `question`, `choices`,
`answer` — changed in four places at once: the prompt and the validation in
`agents/content.py`, the renderer in `devices/epaper.py`, the batch tool in
`tools/generate_batch.py`, and the fixtures in `tests/test_content_agent.py`.

**What it costs.** Content already approved and stored carries the old keys. Either the
reader accepts both for a while, which is a small amount of code and an honest migration,
or previously approved items stop rendering — which is not acceptable, because approval is
the expensive part. Decide before starting, not halfway.

**Where it starts.** `agents/content.py`, then follow the field names outward.

**Done when.** No Italian field name appears in `agents/`, `devices/` or `tools/`, and a
document produced before the change still renders on the display.

---

## 8. A browser check for the panel

**What it is.** One automated check that loads the panel in a real browser and fails on a
page error or on an authority that cannot resolve its endpoints.

**Why.** Two failures reached the deployed site with every local check passing. `node
--check` cannot see a name collision between two classic scripts sharing one global scope,
because each file is valid alone. And the identity library is now deliberately unpinned, so
a release can change the panel with nobody acting — which is exactly what happened between
its major 3 and its major 5: the sign-in button stopped working and said nothing.

**How.** A headless browser, the deployed URL, and three assertions: no `pageerror` during
load, the signed-out view visible, and `acquireTokenRedirect` with a navigation client that
returns false reaching an authorize endpoint rather than throwing. That last one is the
part that would have caught both failures, and it needs no credentials.

**What it costs.** A browser in the loop, which is slower than the rest of the suite and
fails for reasons that are not ours — a CDN with a bad minute. It belongs on demand and
before a deploy, not on every commit. What it cannot check is a real sign-in: that needs
credentials, and saying so is part of the check being honest.

**Where it starts.** A script beside `tests/`, run separately from `pytest`.

**Done when.** Pointing it at a panel with the old domain-form authority fails, and at the
current one passes.

---

## 9. The text path does not say what it consumed

**What it is.** Counting tokens for generated text as they are already counted for images.

**Why.** The monthly cap and the usage panel describe the picture path only. Half the system
is therefore invisible in a number the parent is shown as if it were the whole. A cap that
measures half of what it caps is a number with a wrong name.

**How.** The counter exists and so does the name: `panel/usage.py` declares `KIND_TEXT`
beside `KIND_IMAGE`, and nothing has ever recorded one. An event carries tokens, cached
reads and the provider's request id; the text path has to record one too, so the two kinds
can be read apart as well as together.

**What it costs.** Small, and it makes the cap bite sooner — which is the point. The usage
panel needs a line saying which kind each figure belongs to, or the change silently makes
the old numbers mean something new.

**Where it starts.** `agents/content.py` and `orchestrator/router.py`, then `panel/usage.py`.

**Done when.** A text generation appears in `/api/usage` with its own kind, and the cap
counts it.
