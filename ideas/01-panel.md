# The parent's panel

## 1. A preview of what it will actually look like

**What it is.** Next to every picture, the 800×480 two-level image — the one that ends up
on the display — instead of the original PNG.

**Why.** Dithering changes an image a great deal, sometimes to the point of ruining it: we
saw that with the texture that appeared across a white background. If the parent approves
while looking at the original, they are signing off on one thing and another arrives. An
approval given on the wrong preview is not an approval, it is a formality.

**How.** The route already exists: `GET /api/pictures/{id}/content` returns the BMP with
`Content-Type: image/bmp`, which browsers render natively. All that is needed is an `<img>`
in the gallery and in picture proposals. No server work.

**What it costs.** Almost nothing: an image tag and some CSS. The risk is visual — a 1-bit
BMP scaled by the browser looks bad; it has to be shown at full size or at integer
multiples, with `image-rendering: pixelated`.

---

## 2. The state of the devices — built

**What it is.** A box with one row per display: when it was last heard from, how the charge
is, how good the signal is.

**Why.** The data was already being collected: the BYOS server writes `batteryVoltage`,
`rssi`, `firmware` and `lastSeen` on every request. It used to end up in a file on the hub
where nobody saw it. It had the best value-to-work ratio on the whole list, and it is now
built: the hub posts to `POST /api/device/{household}/devices` and the panel shows it on
`GET /api/devices`.

**What it cost.** One detail that had to be right: the charge is shown **coarsely** — full,
half, recharge it — and never as a percentage. A percentage derived from a volt reading
taken under load is a precision we do not have. Writing "37%" would be inventing.

The gap next to it is still open: **silent liveness**. If the hub dies, the e-paper keeps
its last image forever and everything looks normal. The panel says "this display has not
been heard from in six hours", which covers the case only when the parent looks.

---

## 3. Withdrawing an approval — built, 20 August 2026

**What it is.** A "not any more" on something already approved.

**Why.** Approval was one-way. If the parent changed their mind, or if a piece of content
turned out to be wrong once they saw it on the printed sheet, there was no way back. The
`ApprovalLedger` contract already had `withdraw`: only the road to it was missing.

**How.** `POST /api/proposals/{id}/decision` now admits `withdrawn`, and the panel shows
what is already approved with a *not any more* next to each item. The home server sees it
on its next request — `/api/device/{h}/proposals` asks for `approved` and a withdrawn row
is no longer in that list.

**What it cost.** One rule that had to be decided rather than inherited: withdrawal is a
*second* decision and applies only to something approved. A refusal is already a no, and
nothing goes back to pending, so `withdrawn` on anything else answers 409. That keeps the
state a record of what was decided rather than a field somebody can cycle.

The product question has an answer and it is not a good one: a sheet already printed is
beyond reach. Withdrawal applies to the future. The panel says so in the same breath as
confirming it — "un foglio già stampato resta in casa: da qui non si può richiamare" —
rather than letting the parent assume otherwise.

**Where it starts.** `panel/proposals.py` for `DECIDABLE` and `WITHDRAWABLE_FROM`,
`panel/routes/proposals.py` for the rule, `web/src/sections/Proposals.tsx` for the list.

**Done when.** Four tests in `tests/test_proposals.py` and three in the web suite. Checked
by breaking it: with `WITHDRAWN` out of `DECIDABLE` four fail, and with the approved-only
check removed the one that guards it fails on its own. Distributed on revision `--0000041`
and page chunk `/assets/src-D6SP-mAK.js`; the labels *Non più* and *Ritirata* are in the
served bundle. Not pressed by a parent yet.

---

## 4. Refusing with a reason, and having it mean something

**What it is.** On refusal, three buttons instead of a free-text field: *not to their
taste*, *too hard*, *subject to avoid*. The third adds an entry to the list of things to
avoid.

**Why.** Today a refusal throws a proposal away and teaches nothing: next time the system
offers the same thing. A refusal is the cheapest evidence in the system — the parent has
already looked at the content and decided — and it is thrown away.

**How.** The decision's `note` field already exists. The three buttons write a fixed value;
only the third touches the settings, and it says so explicitly before doing it.

**What it costs.** Where the reason goes. Feeding it back into generation is fine and is
the point. Writing it into the settings without the parent seeing it is not: the settings
are the parent's, and a list that grows on its own stops being something they can read.

---

## 5. The real settings — built

**What it is.** Interests, things to avoid, difficulty, variety, words per line, language.

**Why.** They were a `LearnerProfile` written into the home server's code, with invented
names. Every piece of content generated until now was tuned to a person who does not exist.

**How.** The same shape as the themes, and it is now built: a document per household in
Cosmos, `GET`/`POST /api/preferences` for the parent, `GET /api/device/{household}/preferences`
for the home server, which asks for them alongside the themes and adds the name locally.

**What it cost.** The name must **not** enter the cloud, and the way that is held is
mechanical rather than remembered: what the panel stores is exactly the field list
`prompt_hints()` allows out, a test compares the two, and a body carrying an unknown field
is refused rather than accepted and ignored. The hub reads the name and the id from its own
environment; neither has anywhere to be written down up here.

One of these settings is load-bearing rather than cosmetic. The **content language** — what
is read on paper and on the display — belongs to the household and does not follow the
parent's browser. A parent switching their phone to another language would otherwise
silently change what arrives on paper, and content approved in one language is not approved
in another.

---

## 6. How much approved content is left — built, 20 August 2026

**What it is.** One line at the foot of the approvals page: "Da parte — attività
approvate: 12; temi: 4."

**Why.** When the cloud does not answer, the system serves only content that was already
approved. If the reserve is empty the system goes dark — the thing we declared
unacceptable. Nobody could see how full it was.

**How.** A count on routes that already existed: `/api/proposals?state=approved` and
`/api/themes`. Nothing new is stored for it, and withdrawing an item shortens it.

**What it cost.** A risk of tone, and it shaped the words. It is written as a label and a
number rather than a sentence urging anything, there is no threshold at which it changes
colour, and a test asserts the page carries no exclamation mark and no imperative. The
label form also avoids a plural the catalogs cannot inflect — "1 attività approvate" would
have been wrong Italian, and adding plural rules for one line was not worth it.

**Where it starts.** `web/src/sections/Proposals.tsx`, the `Approved` component.

**Done when.** Three tests in the web suite, which fail against the section as it was.
Distributed on page chunk `/assets/src-D6SP-mAK.js`, which carries `approvate:
{activities}`. Not seen by a parent yet.

---

## 7. Putting a picture back — built, 20 August 2026

**What it is.** In the gallery, next to a picture already shown: put this one back on the
display.

**Why.** The archive keeps every picture byte for byte, and the hub can already install one
again — `tools/home_server.py restore` does it. Until now that was reachable only by
somebody with a terminal, which means it was not reachable by the parent.

**How.** The panel records a request; it does not deliver a picture. `POST
/api/pictures/{id}/again` persists one pending request per household, `GET
/api/device/{household}/request` is what the hub reads, and `POST
/api/device/{household}/request/{id}/done` is how it says it has acted. The rhythm setting
is the shape that was copied: the panel writes, the hub reads and decides.

**What it cost.** A new contract, sitting close to the rule that dashboard writes are
inert. It stays inside the rule because the panel persists a row and nothing else: no
wake-up, no notification, and the hub free to look when it chooses and to decline. Three
decisions were written down rather than left to be discovered, and they sit in the
docstring of `panel/requests.py` next to the code they govern:

* Two presses before the hub looks: the last one wins. A queue would put a picture the
  parent has changed their mind about on the display first, and would need a rule for how
  long it may grow.
* A request nobody collected expires after a day, which is `MAX_CADENCE_MINUTES` — the
  widest spacing a parent may set, so the longest a request can legitimately be waiting.
* The hub clears by id, so a press that lands while the hub is fetching the previous
  picture survives.

The wait is the real cost. The hub asks for a request at the moment a picture is due and
not before, so a press is honoured up to one spacing later — an hour on the default. The
panel has no way to shorten that and is not given one; asking every minute would hold an
API replica awake all day to hear "nothing" almost every time. When a request is standing,
serving it takes the place of the painting, so it costs no model call.

**Where it starts.** `panel/requests.py` for the contract, `panel/routes/requests.py` for
the four routes, `panel/cosmos_store.py` for the stored version,
`web/src/sections/Pictures.tsx` for the gallery tile, `devices/pull_picture.py` for the
side that acts.

**Done when — the code half is done, the physical half is not.** 13 tests in
`tests/test_requests.py`, of which 5 fail with the routes unregistered and the id-aware
clear removed, and 2 in the web suite that fail against the gallery as it was.

Distributed on 20 August 2026: image `lanternina/panel:fa62ffe` on revision `--0000041`,
shown to be the one answering by the four request routes appearing in the served
`/openapi.json`; the page on `/assets/src-D6SP-mAK.js`, carrying the label *Rimetti su
questo*; `devices/pull_picture.py` installed on the hub, md5 `d54e7e2f…` matching the
repository copy, and `lanternina-picture.service` last exited 0.

No picture has been put back on a display: nobody has pressed the button. That check needs
somebody at the panel — with the hub's picture timer stopped, press *rimetti su questo* in
the gallery and confirm the row is still there on `GET /api/device/{household}/request`;
start the timer and see the picture land at the next spacing with the request gone.

---

## 8. Retiring the diagnostics block — done, 18 August 2026

**What it was.** The `Technical details` block at the foot of the panel.

**Why.** It printed the token's claims and the raw body of `/api/me`. It was marked
`TODO(poc)` in the markup because it is a development aid, and it is the kind of thing that
stays for a year. Nothing there was meant for a parent.

**How it went.** It was removed while the panel was rewritten as a React application: the
block, the calls that filled it, and the three catalog keys in both languages are gone.
Two other numbers went with it. A refused request used to say `HTTP {status}`, and a failed
sign-in printed MSAL's error code; both now say what happened in a sentence, because a
status code is our problem and not something a parent can act on.

**What it cost.** The fastest way to see why a token was refused. `/api/me` still answers
the three cases apart — 200, 403, 503 — so the cause is one `curl` away for whoever is
debugging; it is simply no longer on the parent's screen.

---

## 9. Everything in the house, with a job and a name

**What it is.** One list of the things the house can use — the two displays, the printers
and the scanners on the network — and next to each one a job the parent chooses and a name
the parent writes. The name is the one the adolescent reads.

**Why.** Three constants are doing this job today and none of them is the parent's. Which
scanner reads is an environment variable on the hub. Which queue prints is another. Which
display shows pictures is decided by which file happens to exist, and on 19 August one
press converted the picture display into the sheet display for good (02 §6). Every one of
those is a choice about the room, made in a place the parent cannot reach.

**Why one list and not two.** A display, a printer and a scanner differ in how they arrive
— a display announces itself, because its firmware is already asking the hub for something
to show, while a printer and a scanner have to be looked for over mDNS — and in nothing
else that matters here. They are all things with an identity, a job and a name. Building
the displays now and retrofitting the printers later means building it twice and leaving
two shapes behind.

**How.** The hub is the only thing that can see the network. A display puts itself on the
list by talking: the firmware reaches `/api/setup` and the registry gains a row, which is
how both units in the house got there. Printers and scanners do not talk to us, so the hub
looks for them — `_ipp._tcp` and `_uscan._tcp` — and it does that on the status push it
already makes every five minutes rather than on a timer of its own. The panel stores one
row per thing. The parent picks the job and writes the name; the hub reads them on its next
run and acts. Nothing here reaches into the house — a printer chosen in the panel prints
nothing until something in the house asks it to.

**Remembering what is switched off.** Nothing is removed from the list because it went
quiet. That matters differently for the two kinds. A printer that is off answers no mDNS
query, and that is exactly the moment the parent goes looking for it to ask why nothing came
out. A display that is asleep is not talking either. The cost is that the list accumulates,
so a thing that has genuinely left the house has to be removed by hand — which is the right
way round, because forgetting is then something somebody decided rather than something that
happened while nobody was looking.

**What identifies a thing.** Not its address. Between 4 and 19 August the printer moved
from `192.168.0.138` to `192.168.0.5` and the hub from `.157` to `.158`; a list keyed on
addresses would have grown a duplicate for each. The mDNS service name — `EPSOND59029.local`
— is the key for a printer or a scanner, and the MAC for a display.

**The name is read by somebody, and that has three consequences.** It reaches the model:
the point of a descriptive name is that a sentence can be built around it — "the sheet is
waiting on the printer downstairs" — rather than the string being repeated verbatim. So it
crosses as material, and like every other setting the parent writes it is data in a prompt
and never an instruction in one. It lands on a screen the adolescent reads, so it is a name
and never a status: no "offline", no "error", nothing that says something is wrong. And the
renderer has a fixed width, so the length has a limit that the panel states while the parent
is typing rather than enforcing afterwards by truncation.

The third consequence is the one that needs a mechanical guard rather than a warning. A
person's name never goes into a model prompt, and a free-text field is the easiest place in
the whole system to break that by accident: "Sofia's printer" is exactly what somebody
would naturally type. The check belongs on the hub, because the hub is the only side that
knows the name — it reads it from its own environment and the cloud has nowhere to store it
(§5). A device name that contains it is refused there, before it can leave, and the parent
is told why.

**What it costs.** A new store, a new pair of routes and a section in the panel, and a
discovery step on the hub that has to be tolerant: mDNS answers late and sometimes empty —
the first scan after a quiet spell has returned `SANE offers []` and then found the device a
minute later. An empty answer must mean "found nothing this time", never "the list is now
empty". And the choice has to be cached on the hub like the rhythm, so a panel that cannot
be reached leaves the house working to the last known assignment.

**Where it starts.** `panel/devices.py` for the row and the store, `panel/app.py` for the
parent routes and for the answer to the status push, `web/src/sections/Devices.tsx` for the
list, `devices/push_status.py` for the report and the cache, `devices/trmnl_byos.py` and
`devices/pull_picture.py` for the display side, `devices/scan_sheet.py` and the print path
for the other two.

**Done when.** A parent who has never used a terminal can say which display holds the
pictures, which one stands by the printer, which printer prints and which scanner reads,
and can call each of them something an adolescent would recognise. A display with no job
yet shows its own id, so the row in the panel and the thing on the shelf can be matched
without a cable.

### Built on 19 August 2026 — the panel, and the hub waiting to be installed

The panel is live: image `lanternina/panel:9edc724` on revision
`ca-lanternina-dev-api--0000028`, and the front end published by the `panel` workflow.
Both displays already have a row — `94:A9:90:CF:7D:04` and `E8:3D:C1:FB:9F:18` — with no
job and no name, because the hub's existing status push creates them without knowing about
any of this: a report with no `kind` reads as a display.

What was measured rather than chosen. The name limit is 40 characters: the notice renderer
has 728 px, forty characters of ordinary Italian come to 692 px and stay on one line, forty
capital Ws come to 1280 px and do not. So the limit is a comfortable case and not a
guarantee, and the panel states it while the parent types instead of truncating afterwards.

Two decisions worth keeping. A job belongs to one thing, so handing it over takes it from
whoever held it — without that the hub would have to choose between two displays claiming
the pictures, and it would choose by luck. And there are three answers to "what is this
display for", not two: a job, no job, and never mentioned. The third is what keeps a hub
that cannot reach the panel from turning every screen in the house into an id card.

**Still to do, and in this order.** The hub code is written and tested but **not
installed**, deliberately: the moment it runs, a display with no job shows its id instead
of what it is showing now, so the parent assigns the two jobs first. Then
`deploy/lanternina-status.service` needs its new `ReadWritePaths`, the display server needs
`LANTERNINA_JOBS_FILE=/var/lib/lanternina/state/jobs.json` in
`/etc/lanternina/trmnl-byos.env`, and one thing has to be checked on the machine rather
than reasoned about: whether `avahi-browse` can reach the avahi daemon over D-Bus from a
unit running under `ProtectSystem=strict`. If it cannot, discovery returns nothing and says
nothing — an empty answer is indistinguishable from a quiet network, which is exactly the
failure this feature is built to tolerate and therefore the one it cannot report.

### Installed on 19 August 2026 — and what it found

**The sandbox does not block discovery.** Measured with `systemd-run` carrying the unit's
own directives — `ProtectSystem=strict`, `ProtectHome`, `NoNewPrivileges`, `PrivateTmp`,
`User=fausto`, `Group=lanternina` — rather than from a shell, where it would have proved
nothing: `_ipp._tcp` answered in 3.4 s and `_uscan._tcp` in 1.0 s, both inside the 12 s
timeout. So the one failure that could have been silent is not there.

Two defects were, and both were found by running it rather than by reading it.

**A name arrived with `\032` where its spaces were.** The printer announces itself as
`EPSON\032ET-2870\032Series`, and the decoder knew `\;` and `\\` only. That string is what
the parent would have read in the panel. The fixture that let it through used
`EPSOND59029`, a name with no spaces in it.

**One box offering two services became one row.** Four things were reported and three came
back. The Epson answers both `_ipp._tcp` and `_uscan._tcp` from the same hostname, and the
row was keyed on the hostname alone, so the scanner overwrote the printer and took its kind
with it — leaving a house in which the `print` job could not be handed to anything. The
identity now carries the kind: `printer:EPSOND59029.local` and `scanner:EPSOND59029.local`.
The paragraph above, which says the mDNS service name is the key, was the mistake: a
hostname is not a service name, and one machine has as many services as it advertises.

**Three things are left, and none of them is code.**

- `LANTERNINA_LEARNER_NAME` is set in neither `panel.env` nor `trmnl-byos.env`, so
  `learner_name()` returns `""` and the refusal never fires on this hub. The mechanism
  itself is not in doubt: on 19 August 2026 one push was run with
  `LANTERNINA_LEARNER_NAME=Quadro` and `LANTERNINA_JOBS_FILE` pointed at a scratch file, and
  it printed `refused the name on E8:3D:C1:FB:9F:18: it carries a person's name` — the
  display called "un bel quadro che cambia" came back with an empty name and
  `nameRefused` true, CF7D04 untouched, and the real cache unchanged either side. What is
  missing is the name, and it holds a person's name, so it is for somebody in the house to
  write into a local env file, not for anything here. `panel.env` is where it belongs: it
  is read by `lanternina-status.service`, which is the only consumer, and at
  `root:lanternina` 640 it already holds the device key.
- A stale row `EPSOND59029.local`, of kind `scanner`, is still on the panel's list from
  before the identity changed. Removing it is the parent's decision, and the panel is the
  only place it can be taken. On screen it is one of three rows all labelled "EPSON
  ET-2870 Series"; what tells it apart is when it was last heard, because the hub no
  longer reports that id. At 20:44 on 19 August 2026 the two live rows had been heard 3 s
  ago and the stale one 4705 s ago.
- The two jobs the parent chose are the opposite way round from what the notes assumed:
  **CF7D04 holds `sheet`** ("dispositivo che da le istruzioni") and **FB9F18 holds
  `picture`** ("un bel quadro che cambia"). The panel is the authority — it is where the
  choice was made — and anything that hardcodes a screen file has to be read against it.

**The picture now follows the job.** In the log either side of the moment the cache
appeared: at 19:15, with no `jobs.json`, the picture went to the shared `screen.bmp`; at
19:18, with it, to `screen-FB9F18.bmp`. What each display is served was then compared with
what is on disk, byte for byte, because a screen that does not change proves nothing —
FB9F18 is served `screen-FB9F18.bmp` and CF7D04 the shared file, both matching exactly.

**One inconsistency, closed on 19 August 2026.** `devices/pull_picture.py` asked the cache
which display holds `picture`; `devices/run_blueprint.py` took `--screen` as an argument
and asked nothing. So the sheet landed wherever the caller said, and a caller working from
the wrong assumption put a notice on the picture display. `run_blueprint` now resolves the
`sheet` holder the same way, from `TRMNL_SCREEN_FILE` and the cached assignment;
`--screen` remains as an override for a house with no cache yet. Measured on the hub: with
both env files sourced, `screen_in(os.environ)` returns
`/var/lib/lanternina/state/screen-CF7D04.bmp`, and the whole second half then ran with no
`--screen` at all in 39.2 s, updating CF7D04 at 20:37:52 and leaving FB9F18 at 20:26:17.

**The command needs both env files.** `TRMNL_SCREEN_FILE` and `LANTERNINA_JOBS_FILE` live
in `trmnl-byos.env`, not `panel.env`. A run that sources only `panel.env` and omits
`--screen` says there is no display in this house, which is correct and unhelpful.

**A thing holds several jobs, and a job several things — 19 August 2026.** Until then a job
belonged to one thing, and handing it over took it from whoever held it. That cannot
survive three things to show on two displays, which is what this house has: the picture,
what to do next, and the reminders of `05 §1`. So a thing now carries a set of jobs, no job
is taken from anybody, and when more than one thing can do something the house picks
between them — the oldest picture first for the pictures, because that is the only rule
under which every frame actually changes, and at random for a notice, which is what makes
where the next thing appears worth looking for. The cost of the second is worth stating: on
a house with two, a notice lands on one of them, and somebody standing at the other does
not see it.

The name the parent reads changed with it. "sta accanto alla stampante" described where a
display stood, and the display does not have to stand anywhere near the printer: the sheet
can be put on the glass and the button pressed somewhere else entirely. It is now "mostra
le azioni da compiere", which is what the display does rather than where it is.

The hub reads a cache written either way — a single `job` or a list of `jobs` — so it can be
updated before the panel. The other order would put an id card on every display in the
house for as long as the two disagreed.

**Removing something is not permanent, and the panel now says so.** The hub reports what it
finds on every status push, and the panel creates a row it does not have, so a printer or a
scanner still switched on returns to the list on its own. What does not return is the jobs
it had been given: `forget` drops the row, and the parent's choice is the one thing in it
nothing else can reconstruct. That is why the answer is a sentence in the panel and not a
"look now" button — a button would have to ask the hub to do something, which is exactly
what a panel write may not do, and it would gain nothing, because the hub already looks
every five minutes.

**A run under `sudo` created a screen the button path could not write.** The first
`screen-CF7D04.bmp` came out `root:root` 644. The display server reads it — it is
world-readable — so nothing looked wrong, but `lanternina-scan.service` runs as
`fausto:lanternina`, and pressing the button on that display would have failed to change
it. Measured with `systemd-run` carrying the unit's own directives: before, `test -w`
answered REFUSED for `screen-CF7D04.bmp` and WRITABLE for its two siblings; after
`chown root:lanternina` and `chmod 664`, WRITABLE for all three, with the file's contents
unchanged (sha256 `3862123e…` either side). `_replace` now gives a file it creates the
directory's owner and mode 664, and still keeps what it finds on a file that exists.

