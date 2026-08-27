# Threat model

This model puts one asset first: protecting the adolescent from the system built for them. Protecting the family's data from the outside comes second. The ordering is deliberate — the likeliest harm here is not a break-in, it is the software drifting into doing something nobody decided it should do.

Scope: the mini-PC, the ESP32 devices, the camera, the printed sheets, the parent panel, and the Azure services the router calls.

Personal material may be processed in the cloud tier and not only in the house. The tier runs in the EU and is held to the confidentiality a bank owes the records it keeps — a standard this model assumes of it, not one it verifies. What follows is therefore about who can reach the data, not about which side of the boundary it sits on.

**"We do not persist it" is not "it never existed anywhere".** The rectified page crop and the prompt around it go to a model provider, and that provider may keep its own copies: request logs, abuse-monitoring buffers, retention windows set by contract or by law. None of that is under this project's control, and no seal, type or test here reaches it. Said in the same register as the line below about physical access: the promise this project can make is about its own stores, and beyond them the promise is somebody else's to make.

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
| The system starts stating verdicts | Adaptation needs a model of what happened, and a model is one rename away from a claim about the person | A reading is read and not kept: `WhatCameBack` closes the implicit routes out of memory, and the record has no field one would fit in. What is durable is what was made and what was configured |
| A verdict surfaces | An adaptation signal is shown to be helpful: "this got easier", a trend line in the panel | Nothing about how somebody is doing is rendered, on paper, on a display or in the panel. The parent sees proposals, not assessments. `tests/test_boundaries.py` fails on that vocabulary in the stored shape, the panel and the prompts |
| A dashboard change starts work in the house | A configuration route also enqueues generation or signals the device | Dashboard mutations persist only; processing begins only on an authenticated request initiated by the home server |
| Content is delivered unreviewed | An agent renders directly; a "fast path" for the demo | `Proposal` has no approval field; delivery verifies two seals; agents never hold the ledger |
| Something unkind or infantilising is said | Model drift, a bad prompt, a tone setting | Content Safety chokepoint, parent approval, age-appropriateness rules in `.github/instructions/agent-boundaries.instructions.md` |
| An error message blames the reader | A stack trace on a display they can see | Errors surface on the parent panel; the adolescent's surfaces stay calm and non-blaming |
| A misread is reported as fact | Low-confidence vision output taken as an answer | `needs_review` instead of guessing; degraded reads are flagged, never silently skipped |

**Residual risk:** none of this stops a *deliberate* change. It is designed so that harm requires a decision, not an oversight.

## T2 — Prompt injection through a worksheet

A worksheet is paper. Anyone who can write on paper — the adolescent, a classmate, a sibling — can put text in front of a vision model.

| Vector | Mitigation |
| --- | --- |
| Handwritten "ignore previous instructions…" | Recognised text is data, never placed in an instruction position |
| Free text the parent types (interests, notes) | Same treatment; the parent is trusted as a person, not as a prompt author |
| A QR code held up to the glass | Nothing is printed on a page that is there for a machine, so there is no QR the reader is looking for; where one is still decoded, the `LNT1\|version\|sheet\|exercise` grammar is parsed strictly and unknown ids are rejected |
| A sheet crafted to trigger a "safety" alert | Escalation covers system faults and blocked content, not conclusions about a person |

**Residual risk:** a sufficiently clever injection could still influence generated content. The parent approval gate is the backstop — nothing generated is delivered unreviewed.

## T3 — The camera photographs a person

It will. It is handheld and carried around, so friends, rooms and faces end up in frame. The threat is not that a person appears in a photograph; it is that something is inferred from them, or that a capture happens without the person holding the device choosing it.

| Vector | Mitigation |
| --- | --- |
| A capture triggered from outside the room | No remote trigger exists; nothing in the cloud and nothing in the parent's panel can take a photograph |
| Firmware that captures without a press | Holding the button is the only path to the sensor having power, and the activity light is wired in series on that rail rather than driven from a pin |
| A preview endpoint added "temporarily" | No streaming endpoint exists; forbidden in NON-GOALS |
| Continuous or motion capture | Single-shot on button press only; no timer or trigger loop exists |
| Face, age, identity or affect analysis | Forbidden including as an intermediate step |
| A photograph nobody meant to keep | What is kept lands in a gallery its owner can see and delete from; Content Safety runs on inbound photographs as well as generated output |

**Residual risk:** none of the above is enforced by a test, because `vision/` is empty and there is nothing yet to enforce it against. Until the intake exists, every row here is a design decision. The README says so in Status.

## T4 — Key and credential compromise

| Vector | Mitigation |
| --- | --- |
| Sealing keys committed | `.gitignore` covers `.env`, `secrets/`, `*.key`; `.env.example` carries no values |
| One key used for both purposes | Two distinct keys; a seal is valid only for its purpose, and the tests assert it |
| Azure credentials in the repo | Entra ID only, no API-key code path; service principal lives in a root-owned systemd `EnvironmentFile` |
| Wi-Fi PSK in firmware | `wifi_secrets.h` is gitignored; a template is committed |
| Stale tokens left in the tree | The previous project left an MSAL cache in the workspace; removed, and `.azure/` is now ignored |

**Rotation:** rotating a sealing key invalidates every existing approval. That is correct — the parent re-approves rather than inheriting state nobody can verify.

## T5 — Local network and devices

The mini-PC and the ESP32s share a home LAN with phones, TVs and guests.

| Vector | Mitigation |
| --- | --- |
| Anyone on the LAN reaching the panel | Authentication required; bound to a specific interface. TODO(hackathon): implement |
| Anyone on the LAN publishing to the device bus | An anonymous broker means anyone on the Wi-Fi can display text in the house. TODO(hackathon): decide auth on the device transport before demo day |
| A device spoofing a button press | Same channel; the mitigation is the same |
| Physical access to the mini-PC | Out of scope. Disk encryption is the answer and it is the household's choice |

This is the weakest area today, and the weakness matters: the device transport delivers text to a screen an adolescent reads.

## T6 — Availability

Not a security threat, but a harm.

| Failure | Behaviour |
| --- | --- |
| Azure unreachable | Serve previously approved cached content; a page that comes back waits until the cloud is reachable |
| Nothing approved in reserve | The system has nothing to show. With no on-device model this is the only offline path, so keeping a reserve stocked is a hard product requirement |
| Mini-PC down | Devices show their last content; no error text on the displays |

---

## Explicitly out of scope

- A determined fork author removing the guarantees. The seals make removal deliberate, not impossible, and that is the intended bar.
- A compromised Azure tenant.
- Malicious use by the parent. The system is theirs; the design assumes they act in the adolescent's interest.
- Attacks requiring physical access to the devices.

## Open questions blocking parts of this model

1. What counts as a "safety signal" that escalates to the guardian? If it includes conclusions about the person drawn from their work, that contradicts T1 and needs a separate decision.
2. Does the device transport get authentication before the demo, or is the LAN treated as trusted?
3. How long are scanned pages retained, and who can delete them? The reading is not kept; the image handed to the provider is a separate question, and it is the provider's answer.
