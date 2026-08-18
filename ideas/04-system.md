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

**Why.** A few things exist only on the hub, and until 18 August it was not known which.
The weekly backup exists and has been tested, but the **restore** never has. An unverified
backup is a hope.

**What the keys turned out to be, measured on 18 August 2026.** The three keys were
compared by fingerprint rather than by value: `tools/key_fingerprint.py` prints a salted
SHA-256 truncated to twelve hex characters, and the same code was run on both machines, so
the comparison does not depend on reading a secret out loud.

- `device_key` is the same on the development machine and in `/etc/lanternina/panel.env`:
  48 characters, same digest. The live API accepts it.
- `approval_key` and `safety_key` are **not on the hub at all**. Searched twice: by variable
  name, and by literal value across `/etc /opt /srv /home /root /var/lib /usr/local /boot`.
  The second search found the device key in the file that is known to hold it, and that
  positive control is what makes its silence about the other two worth anything — the first
  attempt returned an empty result for the wrong reason, because PowerShell had put a
  carriage return on the end of each pattern. Neither key is in the API's environment
  either, which has nineteen variables and none of them these.

So the warning this entry used to carry was wrong in two ways, and both matter.

First, losing the card cannot lose the seal keys, because they were never on it. The single
copy is `secrets.local.yaml` on the development machine.

Second, it is not the approval key that has the property described. The approval seal is
minted and verified inside one run of `tools/home_server.py show`, seconds apart: a fresh
random value behaves identically and nothing stored anywhere refers to the old one. The
seal that crosses a process boundary is the safety seal — `offer` mints it at screening
time, the panel stores it as `payloadSeal`, and `show` verifies it later, possibly days
later. **Losing `safety_key` is what makes already-screened content undeliverable.**

Measured rather than read off the code: the four approved proposals in the panel today all
verify under the development machine's `safety_key`, and none of them verifies under a key
differing from it by one bit. The negative half is the part that makes the positive half
mean something.

**What the backup holds, measured the same day.** `/usr/local/sbin/lanternina-backup` runs
on Sunday at 04:00: a `dd` of the boot partition and a `tar --one-file-system` of the
rootfs, both onto the NVMe at `/srv/lanternina/backup`, keeping three copies. Reading the
archive of 16 August (1.9 GB compressed) from end to end took 47 s on the hub and exited 0
with 100,170 entries. The archive was intact. That was more than was known before, and less
than a restore.

Four gaps came out of that reading. Three are now closed, and the closing was measured too.

- `/etc/lanternina/panel.env` was not in it. The file had been created on 17 August at
  06:21, after the backup of the 16th at 22:10, so this was timing rather than a rule — but
  it meant that restoring from the newest archive would have produced a hub with no device
  key, no panel URL and no household id. **Closed**: a backup was run by hand on 18 August
  at 14:05 and finished at 14:10:47, five minutes and six seconds wall, and the file is in
  it. Running it dropped the copy of 4 August, which is what keeping three copies means.
- The household id lived in that one file. It is not regenerable — it names the family's
  rows in Cosmos. **Closed** by writing it into `secrets.local.yaml` beside the keys, with
  the panel URL. It can also still be read back by signing in to the panel.
- The script ended its `tar` with `|| true`, so a tar that died halfway left a truncated
  archive and the unit still exited 0. **Closed**, and not by deleting the `|| true`: on a
  live filesystem `tar` exits 1 for "file changed as we read it", which is normal and leaves
  the archive usable, so a plain `set -e` would have failed every run. The script now treats
  1 as success and 2 or more as fatal, re-reads the finished archive with `tar -tzf`, and
  **prunes the older copies only after that read succeeds**. The script and its two units
  are now in `deploy/`, byte-identical to what is installed.
- The archive still sits on the NVMe of the machine it protects. That covers a dead eMMC
  and nothing else. **Open**, and it needs a decision about where a second copy would go
  rather than a change to the script.

**The nearest thing to a restore that costs nothing.** On 18 August the nine files a hub
cannot start without were extracted from the newest archive into a scratch directory and
compared with the live ones: identical byte for byte, and identical in owner and mode —
including `root:lanternina 640` on `panel.env` and on the display registry, which is the
pair that broke the display once before when a rewrite dropped the group. Forty-five seconds,
and it touches nothing outside `/tmp`. It does not prove that a card boots. It does prove
that the archive contains usable files rather than merely readable ones, which is the half
that was being assumed.

**What has to be recovered.**

- The household id. Now in `secrets.local.yaml` as well as in `panel.env`, and readable
  from the panel by signing in.
- `safety_key`. Regenerating it costs every proposal now waiting in the panel: generated
  again, screened again, and approved again by the parent — which is the expensive part.
- The display's token in `trmnl-devices.json`. The server registers a display only through
  the USB provisioner; `/api/setup` answers 404 to a MAC it does not know. A lost registry
  therefore means opening the case and provisioning over USB, not a step done over the
  network. It is in the backup, and it comes back out with its group intact.
- The display's Wi-Fi credentials, in `trmnl-provisioning.json`. Also in
  `secrets.local.yaml`, also in the backup. They belong to the display: the hub is on
  Ethernet.

**What can be regenerated, at a stated price.**

- `approval_key`: a fresh random value, nothing to coordinate.
- `device_key`: a fresh value in `secrets.local.yaml`, one run of `scripts/deploy.ps1`, one
  line in `panel.env`.
- `/opt/lanternina`: from the repository.
- The backup script and its two units: from `deploy/`, where they now live. Before
  18 August they existed only on the hub, which meant the thing that makes recovery possible
  was itself only recoverable from a backup.
- `/srv/lanternina/build`: the firmware tree, from `firmware/patches/`. About half an hour
  on a hub that already has PlatformIO and the ESP32 toolchain — which a blank card does
  not. Installing those is roughly 2.4 GB of download and has not been timed.
- The printer: one `lpadmin` line, driverless.
- ssh host keys, `screen.bmp`, the status file and the device log.

**How.** The installer `deploy/install-trmnl-byos.sh` already covers the display service.
What is missing is the order the rest goes back in, written down.

**What this entry deliberately does not cover.** Standing up a *new* hub — a machine that
has never run Lanternina — is a different problem from putting this one back, and it has no
written procedure either. Parked on 18 August 2026, to be taken up on its own rather than
folded in here.

**What it costs.** An afternoon, and a second card so the working one is not touched. The
two things worth doing first were done on 18 August and took about ten minutes between
them: the household id now has a second copy, and the newest archive now contains
`panel.env`. What is left is the part that needs hardware and an afternoon.

**Where it starts.** `deploy/lanternina-backup` and `deploy/install-trmnl-byos.sh`.

**Done when.** A second card, restored from the newest archive, serves `/api/display` to
the display in the house and installs an hourly picture, with nothing typed in by hand that
is not already either in `secrets.local.yaml` or in the repository.

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

**What it is.** One automated check that loads the deployed panel in a real browser and
fails on a page error or on an authority that cannot resolve its endpoints.

**Why.** Two failures reached the deployed site with every local check passing. Both causes
are now gone: the panel is one bundle rather than classic scripts sharing a global scope, so
a name collision is a build error, and the identity library comes from npm pinned by the
lockfile rather than from a CDN at `@latest`. What remains uncovered is the deployed
artefact itself. The component tests run against a fake API in jsdom; they say nothing about
whether the published site loads, whether its content security policy lets the real bundle
run, or whether the authority still resolves.

**How.** A headless browser, the deployed URL, and three assertions: no `pageerror` during
load, the signed-out view visible, and `acquireTokenRedirect` with a navigation client that
returns false reaching an authorize endpoint rather than throwing. That last one is the part
that would have caught both old failures, and it needs no credentials.

**What it costs.** A browser in the loop, which is slower than the rest of the suite and
fails for reasons that are not ours. It belongs after a deploy and on demand, not on every
commit. What it cannot check is a real sign-in: that needs credentials, and saying so is
part of the check being honest.

**Where it starts.** A script beside `tests/`, run separately from `pytest`. Playwright is
already a dependency of nothing in this repository, which is part of the cost.

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
