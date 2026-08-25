# System: infrastructure, costs, things to close

## 1. Closed: the cloud could not paint (401 PermissionDenied)

**Where it was.** `POST /api/device/{household}/paint` answered 503 carrying a `401 PermissionDenied` from the image deployment on the AI account.

**What it turned out to be.** Two things stacked, which is why each single fix appeared to do nothing. The managed identity had been correct all along — a diagnostic route decoding `oid` and `appid` from the token obtained inside the container proved it in one step, after four role assignments had been made on a deduction. Underneath the role propagation sat an `ImportError: aiohttp package is not installed`: the async Content Safety transport needs it and the SDK does not declare it.

**What the episode is worth keeping for.** Every hypothesis about *which* identity was calling had been a deduction. The measurement took ten minutes and should have come first. That diagnostic route is still there, and it returns claims only — never the token.

---

## 2. Closed: the hourly cycle

**What it is.** A timer on the hub that asks for a new picture every hour and installs it.

**How it was done.** A `systemd` timer with `OnCalendar=hourly` and `RandomizedDelaySec`, calling the `paint` route with the device key and writing the BMP atomically over the screen file. The hub needs no Azure credential; it holds the device key and nothing else.

**What it costs.** A refusal from the content gate, a reached cap and an unreachable cloud are all treated the same way: keep the picture already on the wall. Going blank is never the answer to a failure upstream.

---

## 3. Closed: the drift between the templates and what runs

**What it was.** Some live configuration was not described in the templates, so a plain `./scripts/deploy.ps1` would have reset it.

**What it turned out to be, measured on 18 August 2026.** Three of the nineteen environment variables on the API were absent from the template: `LANTERNINA_DEVICE_KEY`, `LANTERNINA_CONTENT_SAFETY_ENDPOINT` and `LANTERNINA_FOUNDRY_ACCOUNT_ENDPOINT`. Worse, and not noticed before: the script passed five parameters and none of them were `apiImage`, `apiTargetPort` or the sign-in settings. A run would therefore have replaced the API with the placeholder image on port 80 and blanked the identity configuration — the panel would have answered 404, then 503.

**How it was closed.** The two endpoints are the same AIServices host, so they are now derived from `ai.outputs.accountEndpoint` rather than passed by hand — a value nobody can forget. The device key is a `@secure()` parameter carried into a container-app secret, read by the script from `secrets.local.yaml`. The script also reads the running app and hands its image, port and sign-in settings back in, so a plain run re-applies what is there instead of resetting it. Without a key it refuses to run at all.

**What it cost.** The key travels on the command line while the deployment runs: `az` refuses a JSON parameter file alongside a `.bicepparam` file, which was measured rather than assumed. On a shared machine that would matter.

**How it was checked.** `what-if` plans no change to the image or the port, keeps all four restored variables, and removes only three ARM defaults. Hiding `secrets.local.yaml` makes the script refuse, which was watched rather than trusted.

---

## 4. What an hourly picture costs

**What it is.** A measurement, not an estimate.

**Why.** Twenty-four images a day for thirty days is 720 generations a month. The unit price of one image with this model is still unknown, and inventing it is not acceptable: the difference between two cents and twenty cents an image is the difference between fifteen euros a month and a hundred and forty.

**What is now measured.** Every call is counted per household, with the tokens the backend reported. One 1024×1024 image came back as 12 input and 196 output tokens, so a picture is billed in tokens rather than per picture — the assumption of "one image, one unit" was wrong. The response also echoes `"quality": "low"`, a default nobody chose, and both size and quality change the price.

**What is still missing.** The unit price. The budget is already configured on the subscription; the remaining step is reading cost per deployment in Cost Management after a day of generation, and reconciling it against our own count using the request id we store.

**What it costs.** A day of waiting. It should be done before raising the cadence, not after.

---

## 5. Rebuilding the hub from scratch

**What it is.** A drill: take a blank card and stand everything back up.

**Why.** A few things exist only on the hub, and until 18 August it was not known which. The weekly backup exists and has been tested, but the **restore** never has. An unverified backup is a hope.

**What the keys turned out to be, measured on 18 August 2026.** The three keys were compared by fingerprint rather than by value: `tools/key_fingerprint.py` prints a salted SHA-256 truncated to twelve hex characters, and the same code was run on both machines, so the comparison does not depend on reading a secret out loud.

- `device_key` is the same on the development machine and in `/etc/lanternina/panel.env`: 48 characters, same digest. The live API accepts it.
- `approval_key` and `safety_key` are **not on the hub at all**. Searched twice: by variable name, and by literal value across `/etc /opt /srv /home /root /var/lib /usr/local /boot`. The second search found the device key in the file that is known to hold it, and that positive control is what makes its silence about the other two worth anything — the first attempt returned an empty result for the wrong reason, because PowerShell had put a carriage return on the end of each pattern. Neither key is in the API's environment either, which has nineteen variables and none of them these.

So the warning this entry used to carry was wrong in two ways, and both matter.

First, losing the card cannot lose the seal keys, because they were never on it. The single copy is `secrets.local.yaml` on the development machine.

Second, it is not the approval key that has the property described. The approval seal is minted and verified inside one run of `tools/home_server.py show`, seconds apart: a fresh random value behaves identically and nothing stored anywhere refers to the old one. The seal that crosses a process boundary is the safety seal — `offer` mints it at screening time, the panel stores it as `payloadSeal`, and `show` verifies it later, possibly days later. **Losing `safety_key` is what makes already-screened content undeliverable.**

Measured rather than read off the code: the four approved proposals in the panel today all verify under the development machine's `safety_key`, and none of them verifies under a key differing from it by one bit. The negative half is the part that makes the positive half mean something.

**What the backup holds, measured the same day.** `/usr/local/sbin/lanternina-backup` runs on Sunday at 04:00: a `dd` of the boot partition and a `tar --one-file-system` of the rootfs, both onto the NVMe at `/srv/lanternina/backup`, keeping three copies. Reading the archive of 16 August (1.9 GB compressed) from end to end took 47 s on the hub and exited 0 with 100,170 entries. The archive was intact. That was more than was known before, and less than a restore.

Four gaps came out of that reading. Three are now closed, and the closing was measured too.

- `/etc/lanternina/panel.env` was not in it. The file had been created on 17 August at 06:21, after the backup of the 16th at 22:10, so this was timing rather than a rule — but it meant that restoring from the newest archive would have produced a hub with no device key, no panel URL and no household id. **Closed**: a backup was run by hand on 18 August at 14:05 and finished at 14:10:47, five minutes and six seconds wall, and the file is in it. Running it dropped the copy of 4 August, which is what keeping three copies means.
- The household id lived in that one file. It is not regenerable — it names the family's rows in Cosmos. **Closed** by writing it into `secrets.local.yaml` beside the keys, with the panel URL. It can also still be read back by signing in to the panel.
- The script ended its `tar` with `|| true`, so a tar that died halfway left a truncated archive and the unit still exited 0. **Closed**, and not by deleting the `|| true`: on a live filesystem `tar` exits 1 for "file changed as we read it", which is normal and leaves the archive usable, so a plain `set -e` would have failed every run. The script now treats 1 as success and 2 or more as fatal, re-reads the finished archive with `tar -tzf`, and **prunes the older copies only after that read succeeds**. The script and its two units are now in `deploy/`, byte-identical to what is installed.
- The archive still sits on the NVMe of the machine it protects. That covers a dead eMMC and nothing else. **Open**, and it needs a decision about where a second copy would go rather than a change to the script.

**The nearest thing to a restore that costs nothing.** On 18 August the nine files a hub cannot start without were extracted from the newest archive into a scratch directory and compared with the live ones: identical byte for byte, and identical in owner and mode — including `root:lanternina 640` on `panel.env` and on the display registry, which is the pair that broke the display once before when a rewrite dropped the group. Forty-five seconds, and it touches nothing outside `/tmp`. It does not prove that a card boots. It does prove that the archive contains usable files rather than merely readable ones, which is the half that was being assumed.

**What has to be recovered.**

- The household id. Now in `secrets.local.yaml` as well as in `panel.env`, and readable from the panel by signing in.
- `safety_key`. Regenerating it costs every proposal now waiting in the panel: generated again, screened again, and approved again by the parent — which is the expensive part.
- The display's token in `trmnl-devices.json`. The server registers a display only through the USB provisioner; `/api/setup` answers 404 to a MAC it does not know. A lost registry therefore means opening the case and provisioning over USB, not a step done over the network. It is in the backup, and it comes back out with its group intact.
- The display's Wi-Fi credentials, in `trmnl-provisioning.json`. Also in `secrets.local.yaml`, also in the backup. They belong to the display: the hub is on Ethernet.

**What can be regenerated, at a stated price.**

- `approval_key`: a fresh random value, nothing to coordinate.
- `device_key`: a fresh value in `secrets.local.yaml`, one run of `scripts/deploy.ps1`, one line in `panel.env`.
- `/opt/lanternina`: from the repository.
- The backup script and its two units: from `deploy/`, where they now live. Before 18 August they existed only on the hub, which meant the thing that makes recovery possible was itself only recoverable from a backup.
- `/srv/lanternina/build`: the firmware tree, from `firmware/patches/`. About half an hour on a hub that already has PlatformIO and the ESP32 toolchain — which a blank card does not. Installing those is roughly 2.4 GB of download and has not been timed.
- The printer: one `lpadmin` line, driverless.
- ssh host keys, `screen.bmp`, the status file and the device log.

**How.** The installer `deploy/install-trmnl-byos.sh` already covers the display service. What is missing is the order the rest goes back in, written down.

**What this entry deliberately does not cover.** Standing up a *new* hub — a machine that has never run Lanternina — is a different problem from putting this one back, and it has no written procedure either. Parked on 18 August 2026, to be taken up on its own rather than folded in here.

**What it costs.** An afternoon, and a second card so the working one is not touched. The two things worth doing first were done on 18 August and took about ten minutes between them: the household id now has a second copy, and the newest archive now contains `panel.env`. What is left is the part that needs hardware and an afternoon.

**What the hardware has to be, and why it is not the one in the house.** A Raspberry Pi 4 or 5 with its own SD card, bought for this. The hub in the house is not a candidate: it is the only one that works, and a restore drill that goes wrong on it takes the house down. Before buying, three things have to be ready, or the card arrives and waits — the order the pieces go back in, written down; a copy of the newest archive somewhere off the hub's NVMe, which is the gap still open above; and the answer to whether the CM5's rootfs restores onto a Pi 4 or 5 at all, since the boot partition being `dd`-ed is that machine's.

**Where it starts.** `deploy/lanternina-backup` and `deploy/install-trmnl-byos.sh`.

**Done when.** A second card, restored from the newest archive, serves `/api/display` to the display in the house and installs an hourly picture, with nothing typed in by hand that is not already either in `secrets.local.yaml` or in the repository.

---

## 6. Closed: app.lanternina.com returning 404

**What it was.** The custom domain answered 404 every so often. The headers said the 404 did not come from our site: the good responses carried HSTS and our CSP, the 404 carried only `Date` and `Transfer-Encoding`. Pinning each ingress IP with `curl --resolve` found `9.163.40.246` answering 404 deterministically while `132.220.38.112` was mixed — a name binding missing on some nodes and present on others, inside Azure, after the domain had been moved from a Static Web App that was then deleted.

**How it closed.** On its own, and the rate fell the whole way: 38% one day, then 13%, then 5% half an hour later, then nothing. Measured again on 19 August 2026, 40 requests alternating `/` and `/admin`: 40 answers of 200, none missing HSTS. Then the discriminating test, six requests against each of the two ingress IPs collected from four public resolvers, `9.163.40.246` included: 200 every time.

**What is left.** Nothing to do. The binding was never deleted and recreated, so whatever propagated is not something we did; if the symptom returns, the technique above is what tells a stale binding apart from a DNS problem, in one command.

---

## 7. Closed: field names that are not Italian

**What it was.** The keys the content agent produced were Italian: `titolo`, `istruzioni`, `esercizi`, `domanda`, `scelte`, `risposta`. A seventh, `perche`, carried the sentence the parent reads with the proposal; it was in the same JSON and had the same problem.

**Why.** The household's content language is a setting. It could not be one while the language was baked into the shape of the data: a sheet in English would still have been a document with a field called `domanda`, and the prompt that produced it asked for that field by name.

**The decision, taken before starting.** Content approved before the change is not rewritten; the readers accept both spellings. The choice was not a matter of taste. The safety seal covers `body` byte for byte and the approval seal covers the payload that holds it, so renaming a key inside stored content invalidates both, and re-sealing would mint an approval the parent never gave. Migrating the data would therefore have meant an agent setting approval, which is the one thing the seals exist to prevent.

**How it was closed, 18 August 2026.** The keys are now `title`, `instructions`, `exercises`, `question`, `choices`, `answer` and `rationale`. Generation asks for those and validates those; a body in the old shape is refused as unusable, because it can no longer come from us. Reading goes through one function per language — `field()` in `shared/exercise.py`, six named readers in `web/src/lib/sheet.ts` — which try the current key and fall back to the Italian one. Those two files are the only places in the running system where an Italian key is named, and a test in `tests/test_boundaries.py` says so: `agents/`, `devices/`, `tools/`, `printing/`, the rest of `shared/`, `orchestrator/`, `panel/`, `vision/` and `web/src/` may not name one. The check looks for a key, not a word, so the Italian prose in the prompts — "da 2 a 4 scelte" — is left alone.

**What it cost.** Two small files that would not exist if the data could be migrated, and one dictionary lookup per field when a body carries the current keys. The cost is permanent: as long as one approved body from before the change survives, the fallback cannot go. Nothing removes it later, because nothing can tell from the outside whether the last old body has been withdrawn.

**How it was checked.** Three claims, each broken on purpose and watched to fail before it was restored. Removing the Python fallback makes the display render of an old sheet differ from the new one at byte 35 of the PNG. Removing the TypeScript fallback makes the panel show an empty title. Reintroducing `entry.get("domanda")` in `devices/epaper.py` and `sheet.titolo` in `Proposals.tsx` makes the boundary test name both files. The suite went from 198 to 201 pytest tests and from 25 to 26 in the panel; `ruff check` and `tsc --noEmit` stay clean.

---

## 8. A browser check for the panel

**What it is.** One automated check that loads the deployed panel in a real browser and fails on a page error or on an authority that cannot resolve its endpoints.

**Why.** Two failures reached the deployed site with every local check passing. Both causes are now gone: the panel is one bundle rather than classic scripts sharing a global scope, so a name collision is a build error, and the identity library comes from npm pinned by the lockfile rather than from a CDN at `@latest`. What remains uncovered is the deployed artefact itself. The component tests run against a fake API in jsdom; they say nothing about whether the published site loads, whether its content security policy lets the real bundle run, or whether the authority still resolves.

**How.** A headless browser, the deployed URL, and three assertions: no `pageerror` during load, the signed-out view visible, and `acquireTokenRedirect` with a navigation client that returns false reaching an authorize endpoint rather than throwing. That last one is the part that would have caught both old failures, and it needs no credentials.

**What it costs.** A browser in the loop, which is slower than the rest of the suite and fails for reasons that are not ours. It belongs after a deploy and on demand, not on every commit. What it cannot check is a real sign-in: that needs credentials, and saying so is part of the check being honest.

**Where it starts.** A script beside `tests/`, run separately from `pytest`. Playwright is already a dependency of nothing in this repository, which is part of the cost.

**Done when.** Pointing it at a panel with the old domain-form authority fails, and at the current one passes.

---

## 9. Closed: the text path says what it consumed, and says which kind it is

**What it was.** The counter had two names, `KIND_IMAGE` and `KIND_TEXT`, and only ever recorded the first. On 20 August 2026 the reminder wording started recording the second, and `/api/usage` went on returning one undivided block: the same six figures a parent had been reading as "pictures" now held pictures and wordings summed together, under a cap called `monthly_picture_cap` that had never counted only pictures.

**What was done.** `UsageSummary` now carries a `UsageTotals` for the month and one per kind, and `/api/usage` answers `{"usage": {"period", "total", "byKind": {"image", "text"}}, "cap"}`. A kind nobody used is reported as zeros rather than left out, so a missing key never has to be read as "no such thing". The panel shows two blocks — pictures, written words — each with its six figures, then a third saying calls, of which paid for, and the cap. The cap moved name with its meaning: `monthly_call_cap`, `LANTERNINA_MONTHLY_CALL_CAP`. The variable was set nowhere in `infra/`, so the rename lost no configuration.

**What it cost.** Three tests, and a page that is three short lists instead of one. The cap bites sooner than it did, which is what a cap counting everything it pays for is supposed to do.

**Distributed, 20 August 2026.** Image `lanternina/panel:6853d29` on revision `--0000039`, shown to be the one answering rather than assumed: the served `/openapi.json` describes `/api/usage` as "split by kind", a phrase only this build has. The image went first and the push after, because the workflow ships the page on any push touching `web/`. The page then served `/assets/src-CqLf1yAL.js`, carrying both new labels, Italian and English.

**What it does not do.** Only the picture path refused when the cap was reached; the wording path counted against the cap without checking it. That was deliberate for the day it was written — a wording starts once per sentence a parent wrote, so it cannot loop on its own — and it was written down as the first thing to change if anything else ever started calling a model. That happened the next day: §11 below.

---

## 10. Closed: what a panel build costs, phase by phase

**What it was.** After the `.dockerignore` fix took the context from 116.8 MiB to 321 KiB, the remaining time had never been split up, and the Dockerfile carried an obvious suspect: it copies the source and only then runs `pip install`, so every changed line of Python reinstalls every dependency.

**Measured on 19 August 2026**, five runs against `acrlanterninadevssveb`, phase boundaries read from the run log rather than from the client. Times in seconds.

| Dockerfile | build step | push | server total | client wall |
| --- | --- | --- | --- | --- |
| base image and `CMD` only | 6.0 | 5.2 | 14 | 41.4 |
| ours, `pip install` removed | 17.1 | 10.4 | 32.5 | 70.6 |
| ours, one `COPY` instead of six | 16.7 | 5.2 | — | 38.5 |
| ours, unchanged | 34.2 | 11.3 | 49.8 | 69.8 |
| ours, unchanged, second run | 33.5 | 10.8 | 49.8 | 69.8 |

So `pip install` is **17.1 s** — the largest single phase, obtained by removing it and subtracting, not by reading the log.

**The suspect is real and worthless.** Reordering the Dockerfile to install dependencies before copying the source only pays if a cached layer survives to the next build, and none does. The control: the same tag was built twice from a byte-identical context, and the second run reported **zero** `Using cache` lines. `az acr build` hands each run a fresh agent whose Docker daemon has never seen the previous image, so the 17.1 s would be paid whatever the order of the instructions. The comment in the Dockerfile now says this, so the next person does not re-derive it.

Two smaller findings, both from the same runs. Collapsing the six `COPY` instructions into one moved the build step by 0.4 s, which is inside the noise — layer count is not the cost. The client waits about twenty seconds longer than the server works, and that gap is not constant: 41.4 s of client wall for a 14 s run, 70.6 s for a 32.5 s one. It is time spent waiting for an agent, and it varies by more than the whole of `pip`.

**What is left, and its price.** The only way to remove the 17.1 s is a second image holding the dependencies, rebuilt when `pyproject.toml` changes and pulled by this one. That buys about a quarter of a two-minute cycle and costs a second artifact that can go stale silently — change a pin, forget the rebuild, and the container runs against dependencies nobody chose. Not done, and recorded here so the trade is visible rather than rediscovered.

**Also closed.** `scripts/build-and-deploy-images.ps1` now passes `--no-logs` and reads the outcome from `az acr repository show-tags`, naming the failing run when the tag is absent. Streaming the log either kills the local CLI on a `UnicodeEncodeError` or sits there looking stuck, in both cases while the build carries on and succeeds.

---

## 11. Closed: reading is counted, and every path that pays now reads the cap

**What it was.** Two of the four ways this system spends money left no trace. Reading a page — `devices/read_page.py` posting to `/api/device/{h}/read-sheet` — and reading the parent's sentences — inside `/api/device/{h}/reminders` — both called the model and wrote nothing into `panel/usage.py`. So the cap could not see them and the parent could not either: a household scanning ten sheets a day paid for three hundred calls a month that appeared nowhere. It is the same hole the wording had until 20 August, and half of it was already fixed, because `_FoundryBackend.complete` had started reporting its tokens.

**A third kind, not the second one.** `KIND_READ`, alongside `KIND_IMAGE` and `KIND_TEXT`. A reading is a measurement — which boxes carry a mark, what hour a sentence names — and nothing it produces is shown to anybody; the wordings under `KIND_TEXT` are read off a display by the person the system is for. Summing the two would give back a figure whose name says less than it holds, which is exactly what §9 had just taken apart. The panel now shows three blocks and then the total.

**Where it starts.** `panel/reading.py` now hands back what the call consumed, the way `panel/wording.py` already did: `read_sheet` and `read_sentences` return the result and the `ModelUsage` beside it. The two routes record the event, and neither lets a bookkeeping failure eat a reading that was already paid for.

**The cap, on all four paths.** A path that counts against a cap without checking it can only be stopped by whichever path does check, which is not a thing to rely on. So:

- `/read-sheet` answers 429. The house reads the page with its own arithmetic and marks the reading degraded, which is what it already does when the panel cannot be reached at all — `devices/read_page.py` turns any HTTP error into `PanelUnreachable`.
- `/reminders` does not answer 429, and this is the one place the two paths differ. The answer carries the reminders already placed, and a refusal would take those with it for the sake of the sentences it cannot read. So the sentences stay unread, `degraded` comes back true, and the house is told its answer is short in the words it already understands.
- the wording checks the cap itself, and not only where the reading does. The reading of a batch is one call and the wording is one per sentence in it, so a parent who writes forty sentences at once passes the cap in the middle of the batch.
- the reading event is written **before** the wordings are asked for, so that a batch large enough to pass the cap is stopped by the call it has itself just made.

**What it costs.** The cap bites sooner again: a household that scans is now spending from the same thousand as one that paints. Whether a thousand is still the right number is a question these figures will answer and could not before — that is the point of counting them. Six tests, all of which fail against the routes as they were.

**Done when.** `/api/usage` reports `byKind.read` with a non-zero `calls` after a page has been read, and a household at its cap gets 429 from `/read-sheet` and `degraded: true` from `/reminders` while still receiving the reminders it already had.

---

## 12. Closed: the cap became the thing that decides, so it moved to 2000

**What it was.** `DEFAULT_MONTHLY_CALL_CAP` was 1000, and the sentence above it explained the number entirely in pictures: "an hourly picture is at most 744 a month". That was true when a picture was the only thing that cost anything. §11 added two more kinds, and the month stopped fitting.

**The month, added up per path rather than guessed.** Every figure below comes from a constant in the code or from a rate somebody chooses, and the arithmetic is repeated in `tests/test_usage.py::test_the_cap_leaves_room_for_a_month_of_ordinary_use` so that it fails if any of them moves.

| Path | Rate | Calls in a 31-day month |
| --- | --- | --- |
| Pictures, `/paint` | one per picture, at the default 60-minute spacing with the night pause switched off | 744 |
| Readings, `/read-sheet` | one per page put on the glass, ten a day | 310 |
| Reminders, `/reminders` | one reading and one wording per sentence, once in its life, one new sentence a day | 62 |
| | | **1116** |

Nothing in that month is unusual, and it is over 1000. A parent who moves the spacing to half an hour reaches 1260 on the pictures alone. So the cap had stopped being the thing that stops a fault and had become the thing that decides how much a house may do.

**What it is now.** 2000 — twice the ordinary month. What that buys is that a house behaving as designed never meets the cap. What it costs is that a runaway loop runs about a day longer before it is stopped: the finest spacing a parent may set is one minute, which is 900 pictures a day inside the default waking hours, so 1000 ends it on the second day and 2000 on the third.

`LANTERNINA_MONTHLY_CALL_CAP` is set nowhere in `infra/`, so the default is what every household gets and changing it changes everything.

**What could not be measured, and why.** The intention was to read `/api/usage` for the real household and let its figures decide rather than this arithmetic. Neither road is open from a laptop, and both were tried on 20 August:

- Cosmos directly: `cos-lanternina-dev-ssveb` has `publicNetworkAccess: Disabled` and an empty `ipRules`, so it is private-endpoint only. No firewall rule would help; the container app reaches it and nothing outside the VNet does.
- `/api/usage` through the panel: it answers 403 without a parent token. The parent identity provider is the CIAM tenant `lantessveb.ciamlogin.com`, which the Azure CLI cannot mint a token for, and `LANTERNINA_DEV_AUTH` is `0` on the running app. The admin tenant is the same one the CLI is signed in to, but the admin routes only admit accounts.

So the figures above are computed, not measured, and they are marked as such. The measurement is one browser sign-in away and needs nothing built: open the panel, read the usage block, compare `byKind` against the table. Until somebody does that, the row worth doubting most is the ten pages a day — it is a habit, not a constant.

**Done when.** A month of real `byKind` figures from `/api/usage` is compared against the table above, and the cap is moved again if the real month disagrees by more than the headroom.

**The cap became a fuse a parent can move, 25 August 2026.** It first left the usage page altogether, because it read there as a budget somebody had been given. That was the wrong half of the problem: what a cap this shape can do is stop a house in silence, and until this change the only sign was that nothing happened.

Three things now hold. It is reported: `/api/usage` returns `reached`, `spent`, `raisedAt` and `raisedBy`, so a house running on a moved fuse says so rather than looking like one that was always there. It is loud: `web/src/components/BlownFuse.tsx` sits above every section, so a parent who opens the panel to find out why nothing is happening reads it on the page they land on rather than in a section they would have to go looking for. And it can be moved: `POST /api/usage/fuse` writes a per-household figure that overrides the configured default, with `MAX_MONTHLY_CALL_CAP` at 20000 as the highest the panel may reach. Zero — no fuse at all — stays a deployment decision, reachable only through `LANTERNINA_MONTHLY_CALL_CAP`.

The per-household figure is absent until somebody moves it, so raising the deployment's default still reaches every house that never touched its own. `tests/test_fuse.py` pins that, and pins the two ways this goes quietly wrong: a fuse set at or below what the month has already spent (the parent presses the button and nothing changes) and a raise reported as though it were the configured figure.

A ceiling the parent chooses, with a figure they set in advance and a warning before it is met, is still a different feature and still not designed. It will need its own name.


**Distributed, 20 August 2026.** Image `lanternina/panel:9052cf9` on revision `--0000040`, shown to be the one answering rather than assumed: the served `/openapi.json` describes `/read-sheet` as refusing "as many calls as it is allowed", a phrase only this build has. The first read after the update still came from `--0000039`, and the second, twenty seconds later, from the new one. The image went first and the push after, because the workflow ships the page on any push touching `web/`. The page then served `/assets/src-BPUFPyvk.js`, carrying both new labels, Italian and English.

## 21. No moderation of our own — decided 25 August 2026, not carried out

**The decision.** The models we call moderate their own output, and Foundry moderates it again on the way out. We do not build a second system beside them, and we do not tune one. `orchestrator/safety.py` and its Azure Content Safety gate are ours, and they are the thing this removes.

**What is not removed, because a provider cannot know it.**

- The parent approves. Nothing reaches the room without a person in the house having said yes.
- `shared/blocklist.py` — the words *this house* asked never to see. A provider has no way to hold that; it is a household's own list, checked before saving and again at runtime.
- The format refuses a document it cannot read: `shared/experience_checks.py`, the line lengths, the ids, the way out that reaches for an object nobody was given. That is correctness, not moderation, and it does work no filter does.
- The age-appropriateness and tone rules in the prompts themselves. Those shape what is asked for, which is cheaper and better than judging what came back.

**What this costs, said plainly.** Provider moderation is not tuned to a particular adolescent in a particular house, and it does not know what this family finds unkind. The blocklist and the parent's approval are what stand in for that, and they are narrower. This is a judgement that the second filter was not earning its place, not a claim that nothing is lost.

**Where to start.** `orchestrator/router.py` holds the chokepoint; `generate_for_user` screens and seals, `analyze()` does not. The seal is the hard part and it is not cosmetic: `ScreenedPayload` is a *type* the rest of the system requires, `panel/` stores `payloadSeal`, and `tools/home_server.py show` verifies it days later on the device with a key the cloud does not have. Taking the gate out without deciding what the seal means would leave a signature over nothing.

Two ways, and the first is probably right:

1. Keep `ScreenedPayload` and the seal, and let the gate become a pass-through that seals what the provider already moderated plus what `shared/blocklist.py` refuses. Small change, no type churn, and the device-side verification keeps meaning "this text is the text the panel approved".
2. Remove the type. Larger, touches everything, and gives up the tamper-evidence between panel and house, which was never about moderation.

**Done when.** No Azure Content Safety call is made, the blocklist still refuses, an afternoon still cannot be delivered without a parent's approval and a verifiable seal, and `docs/THREAT-MODEL.md` T1 says what now answers it.
