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

## 3. Withdrawing an approval

**What it is.** A "not any more" on something already approved.

**Why.** Today approval is one-way. If the parent changes their mind, or if a piece of
content turns out to be wrong once they see it on the printed sheet, there is no way back.
The `ApprovalLedger` contract already has `withdraw`: only the road to it is missing.

**How.** `POST /api/proposals/{id}/decision` already takes a state; it is enough to admit
`withdrawn` among the decidable ones and show it in the list of approved items. The home
server sees it on the next request and stops delivering it.

**What it costs.** A product question with no obvious answer: what happens to a sheet that
is already printed? Withdrawal applies to the future. We can do nothing about paper already
in the house, and the panel has to say so rather than pretend.

---

## 4. Refusing with a reason, and having it mean something

**What it is.** On refusal, three buttons instead of a free-text field: *she does not like
it*, *too hard*, *subject to avoid*. The third adds an entry to the list of things to
avoid.

**Why.** Today a refusal throws a proposal away and teaches nothing: next time the system
offers the same thing. But mind what it must **not** become: it is not a signal about her,
it is a preference stated by the parent. The difference is that it stays written down,
visible and editable, instead of being inferred.

**How.** The decision's `note` field already exists. The three buttons write a fixed value;
only the third touches the settings, and it says so explicitly before doing it.

**What it costs.** The temptation to let the list grow on its own. If a refusal changed the
settings without the parent seeing it, we would have built the automatic adaptation we
ruled out, under a kinder name.

---

## 5. The real settings

**What it is.** Interests, things to avoid, difficulty, variety, words per line, language.

**Why.** Today they are a `LearnerProfile` written into the home server's code, with
invented names. Every piece of content generated so far is tuned to a person who does not
exist.

**How.** The same shape as the themes: a Cosmos container, a route for the parent, a route
for the device. The home server asks for them along with the themes.

**What it costs.** Her name must **not** enter the cloud. The profile that goes up is
already redacted (`prompt_hints()` excludes name and id): that function has to be respected
here too, or the separation between household and person is lost in a text field.

One of these settings is now load-bearing rather than cosmetic. The **content language** —
what she reads on paper and on the display — belongs to the household and must not follow
the parent's browser. A parent switching their phone to another language would otherwise
silently change what she reads, and content approved in one language is not approved in
another.

---

## 6. How much approved content is left

**What it is.** One line: "there are 12 approved activities and 4 themes".

**Why.** When the cloud does not answer, the system serves only content that was already
approved. If the reserve is empty the system goes dark — the thing we declared
unacceptable. Today nobody knows how full it is.

**How.** A count in routes that already exist. No new work.

**What it costs.** A risk of tone: it must not become a chore assigned to the parent. "There
are few left" is a fact; a notification that insists is something else.

---

## 7. Putting a picture back

**What it is.** In the gallery, next to a picture already shown: put this one back on the
display.

**Why.** The archive keeps every picture byte for byte, and the hub can already install one
again — `tools/home_server.py restore` does it. Today that is reachable only by somebody
with a terminal, which means it is not reachable by the parent.

**How.** The panel records a request; it does not deliver a picture. Something like
`POST /api/pictures/{id}/again`, which persists one pending request per household, and
`GET /api/device/{household}/request`, which the hub reads on its next hourly run and
clears once it has acted. The rhythm setting is the shape to copy: the panel writes, the
hub reads and decides.

**What it costs.** A new contract, and it sits close to the rule that dashboard writes are
inert. It stays inside the rule only while the panel persists a request and nothing else:
no wake-up, no notification, and the hub free to look when it chooses and to decline. Two
decisions have to be written down rather than discovered: what happens when two requests
arrive before the hub looks — the last one wins is the simplest answer — and how long a
request nobody collected stays alive.

**Where it starts.** `panel/pictures.py` and `panel/app.py` for the two routes, `web/app.js`
for the gallery tile, `devices/pull_picture.py` for the side that acts.

**Done when.** With the hub's timer stopped, the request is still there. On the next run the
chosen picture is on the display, and the request is gone.

---

## 8. Retiring the diagnostics block

**What it is.** Removing the `Technical details` block at the foot of the panel.

**Why.** It prints the token's claims and the raw body of `/api/me`. It is marked
`TODO(poc)` in the markup because it is a development aid, and it is the kind of thing that
stays for a year. Nothing there is meant for a parent.

**How.** Delete the `<details>` element, the `showDiagnostics` calls, and the three catalog
keys in both languages.

**What it costs.** The fastest way to see why a token was refused. It is worth replacing
with one line that names the cause — audience, issuer, expiry — without printing the claims
themselves.

**Where it starts.** `web/index.html`, `web/app.js`, `web/i18n.js`.

**Done when.** The served page no longer contains `id="diagnostics"`, and
`tests/test_web_i18n.py` still passes with the keys removed from both catalogs.
