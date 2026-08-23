# Threat model

This model puts one asset first: protecting the adolescent from the system built for
them. Protecting the family's data from the outside comes second. The ordering is
deliberate — the likeliest harm here is not a break-in, it is the software drifting into
doing something nobody decided it should do.

Scope: the mini-PC, the ESP32 devices, the camera, the printed sheets, the parent panel,
and the Azure services the router calls.

---

## Assets, in priority order

| # | Asset | Why it matters |
| --- | --- | --- |
| 1 | The adolescent's dignity and autonomy | The system can humiliate, pressure, or label a person. No firewall prevents this. |
| 2 | Scans of their work | Images of a minor's handwriting, produced daily. The most sensitive artefact the system creates. |
| 3 | Their profile and routines | Reveals private preferences and the household's daily pattern. |
| 4 | The two sealing keys | Whoever holds them can forge screened, approved content and deliver it. |
| 5 | Azure credentials | Cost and blast radius beyond this house. |
| 6 | Wi-Fi / device credentials | Foothold on the home network. |

---

## T1 — The system itself becomes the harm

**The primary threat.** No external actor required.

| Failure | How it happens | Mitigation |
| --- | --- | --- |
| Engagement optimisation creeps in | A streak "to help motivation"; a nudge after two quiet days | Forbidden by [NON-GOALS.md](NON-GOALS.md); `tests/test_boundaries.py` fails on the vocabulary; no metric is stored to optimise against |
| The system starts stating verdicts | Adaptation needs a model of what happened, and a model is one rename away from a claim about the person | Adaptation is allowed and expected; what may be stored is what was observed, not a score, ability or progress field. `tests/test_boundaries.py` fails on that vocabulary |
| A verdict surfaces | An adaptation signal is shown to be helpful: "this got easier", a trend line in the panel | Nothing about how somebody is doing is rendered, on paper, on a display or in the panel. The parent sees proposals, not assessments |
| A dashboard change starts work in the house | A configuration route also enqueues generation or signals the device | Dashboard mutations persist only; processing begins only on an authenticated request initiated by the home server |
| Content is delivered unreviewed | An agent renders directly; a "fast path" for the demo | `Proposal` has no approval field; delivery verifies two seals; agents never hold the ledger |
| Something unkind or infantilising is said | Model drift, a bad prompt, a tone setting | Content Safety chokepoint, parent approval, age-appropriateness rules in `.github/instructions/agent-boundaries.instructions.md` |
| An error message blames the reader | A stack trace on a display they can see | Errors surface on the parent panel; the adolescent's surfaces stay calm and non-blaming |
| A misread is reported as fact | Low-confidence vision output taken as an answer | `needs_review` instead of guessing; degraded reads are flagged, never silently skipped |

**Residual risk:** none of this stops a *deliberate* change. It is designed so that harm
requires a decision, not an oversight.

## T2 — Prompt injection through a worksheet

A worksheet is paper. Anyone who can write on paper — the adolescent, a classmate, a
sibling — can put text in front of a vision model. The QR code is likewise attacker-writable:
anyone can print one.

| Vector | Mitigation |
| --- | --- |
| Handwritten "ignore previous instructions…" | Recognised text is data, never placed in an instruction position |
| Free text the parent types (interests, notes) | Same treatment; the parent is trusted as a person, not as a prompt author |
| A QR code from another sheet, or a hand-made one | Fixed `LNT1\|version\|sheet\|exercise` grammar, parsed strictly; unknown ids rejected; unknown spec versions refused rather than guessed |
| A sheet crafted to trigger a "safety" alert | Escalation covers system faults and blocked content, not conclusions about a person |

**Residual risk:** a sufficiently clever injection could still influence generated content.
The parent approval gate is the backstop — nothing generated is delivered unreviewed.

## T3 — Camera captures more than a page

| Vector | Mitigation |
| --- | --- |
| Camera remounted or knocked, framing the room | Pipeline requires four ArUco markers; without them it raises `MarkersNotFound` and stops. TODO(hackathon): add the frame-fill check |
| Full frames written for debugging | `RawFrame` cannot be pickled, copied or serialised; `cv2.imwrite` in `vision/` fails the boundary test |
| A preview endpoint added "temporarily" | No streaming endpoint exists; forbidden in NON-GOALS and enforced by test |
| Continuous or motion capture | Single-shot on button press only; no timer or trigger loop exists |
| Face or affect analysis | Forbidden including as an intermediate step; identifier-level test |

**Residual risk:** the framing guarantee is physical until the frame-fill check lands.

## T4 — Key and credential compromise

| Vector | Mitigation |
| --- | --- |
| Sealing keys committed | `.gitignore` covers `.env`, `secrets/`, `*.key`; `.env.example` carries no values |
| One key used for both purposes | Two distinct keys; a seal is valid only for its purpose, and the tests assert it |
| Azure credentials in the repo | Entra ID only, no API-key code path; service principal lives in a root-owned systemd `EnvironmentFile` |
| Wi-Fi PSK in firmware | `wifi_secrets.h` is gitignored; a template is committed |
| Stale tokens left in the tree | The previous project left an MSAL cache in the workspace; removed, and `.azure/` is now ignored |

**Rotation:** rotating a sealing key invalidates every existing approval. That is correct —
the parent re-approves rather than inheriting state nobody can verify.

## T5 — Local network and devices

The mini-PC and the ESP32s share a home LAN with phones, TVs and guests.

| Vector | Mitigation |
| --- | --- |
| Anyone on the LAN reaching the panel | Authentication required; bound to a specific interface. TODO(hackathon): implement |
| Anyone on the LAN publishing to the device bus | An anonymous broker means anyone on the Wi-Fi can display text in the house. TODO(hackathon): decide auth on the device transport before demo day |
| A device spoofing a button press | Same channel; the mitigation is the same |
| Physical access to the mini-PC | Out of scope. Disk encryption is the answer and it is the household's choice |

This is the weakest area today, and the weakness matters: the device transport delivers
text to a screen an adolescent reads.

## T6 — Availability

Not a security threat, but a harm.

| Failure | Behaviour |
| --- | --- |
| Azure unreachable | Serve previously approved cached content; read only locally-readable cells |
| Nothing approved in reserve | The system has nothing to show. With no on-device model this is the only offline path, so keeping a reserve stocked is a hard product requirement |
| Mini-PC down | Devices show their last content; no error text on the displays |

---

## Explicitly out of scope

- A determined fork author removing the guarantees. The seals make removal deliberate, not
  impossible, and that is the intended bar.
- A compromised Azure tenant.
- Malicious use by the parent. The system is theirs; the design assumes they act in the
  adolescent's interest.
- Attacks requiring physical access to the devices.

## Open questions blocking parts of this model

1. What counts as a "safety signal" that escalates to the guardian? If it includes
   conclusions about the person drawn from their work, that contradicts T1 and needs a
   separate decision.
2. Does the device transport get authentication before the demo, or is the LAN treated as
   trusted?
3. How long are scanned pages retained, and who can delete them?
