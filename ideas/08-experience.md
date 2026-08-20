# An experience, devised and run

The paper loop as it stands is: here is a task, do it, I will look at it. That is a
worksheet with extra steps, and it is not what this is for. What it should be is an
experience — thought up fresh, run across an afternoon, landing partly on a display and
partly on paper, and coming back through the glass. It has a beginning and it ends.

This file is the design. Nothing in it is built, and the entry below is deliberately not
the agent: three things have to be decided first, because each one closes off work if it
is decided late.

---

## 1. What dies, what survives, and what must not be thrown away

**What dies.** Four ArUco markers at the corners, the QR code, the 50 mm ruler, and the
cell geometry underneath all three.

They are not wrong. They are the machinery for one question — *is there a mark inside this
rectangle* — and that question is going away. The markers exist so a scanned page can be
rectified onto a fixed canvas, after which a declared rectangle becomes a pixel rectangle
by multiplication. The ruler exists to prove the print was not scaled, which matters only
because scaling breaks that multiplication. When the page is read as a page — *what did
somebody do here* — none of it is load-bearing, and it costs a corner of every sheet, a
detector, a spec version, and a class of failure where a marker decodes but reports corners
a few pixels out.

**What survives, and it is one thing.** A page comes back hours later, and the house has to
know which experience it belongs to and which step. That is identity, and it does not need
a QR: a short code printed in a corner, read by the same model that reads the rest, is
enough. One subsystem instead of two.

**What must not be thrown away.** The ecology is not a matter of care, it is a mechanism,
and it is independent of everything above. `shared/pagedesign.py` has no mark that fills an
area — so a heavy page is unreachable rather than discouraged — and `printing/compose.py`
measures the ink in square millimetres and refuses above a budget. Both were measured
against real sheets on 20 August 2026, `03 §6`. Restarting the sheet code and keeping those
two properties is a different thing from restarting and losing them.

**The cost of reading a page as a page, stated once.** Today `CHECKBOX` and `CHOICE_BOX`
are readable on the hub by arithmetic, which is what makes "the cloud is unreachable" mean
reduced capability rather than a stopped system on the paper path. A page read as a whole
has no local tier at all: no cloud, no reading. That is a real loss and belongs in a
decision rather than in a discovery six weeks from now.

---

## 2. The three decisions that come before code

### Who decides what happens next, and when

An experience unfolds over hours, so something has to hold it and move it along. The rule
that shapes the answer already exists: a write from the panel is inert, and the panel has
no way to reach into the house. So the house asks, and the cloud thinks inside the answer
to that request — the shape `POST /api/device/{household}/reminders` already has, where a
sentence is read by a model inside the call the hub made on its own timer.

An experience is then a row the hub asks about: *this is what came back, what now*. Nothing
is pushed, nothing is scheduled from outside, and an experience that nobody continues
simply stops — which is what "stopping is a legitimate outcome" has to mean here.

### What the parent approves

Today an agent proposes and a parent approves each thing. An experience invented fresh
every time and unfolding over an afternoon cannot work that way without the parent becoming
a relay.

The candidate answer is that the parent approves **the experience**, once, before it
starts: its plan in full, in a form they can read to the end. The agent may then move
within it. This is the same trade a picture theme already makes — the parent approves the
subject, not each image — and it has the same cost, said plainly: what the adolescent sees
inside an approved experience has not been seen by an adult first. The content gate is
still the only thing between a model and a person.

What that requires of the plan is that it be readable. A plan that is prose is a signature
on something nobody read; a plan over a closed vocabulary of verbs is not. `shared/
blueprint.py` already made that argument and it still holds — what changes is that a
blueprint was written by hand and this is devised, which raises the stakes on the same
property rather than lowering them.

### Whether the thing that ends is allowed to be satisfying

`docs/NON-GOALS.md` and the working rules refuse streaks, daily goals, don't-break-the-
chain, variable reward schedules, and any notification triggered by inactivity.

Every one of those exists to pull somebody back on a day they were not going to come. An
experience that starts in the afternoon, has a shape, and finishes — with something at the
end that was worth getting to — is not that, and needs no rule relaxed. It is already
allowed and always was.

The line is worth stating exactly, because it is thin and it is the whole of what the
project is: **an ending is allowed to be satisfying; nothing may be built whose purpose is
to make the next one more likely.** A reveal at the end of an afternoon is the first. A
counter of how many afternoons in a row is the second wearing its coat.

If a specific thing is wanted that falls on the wrong side, it should be named, and the
rule edited deliberately, in the file, with the date and the reason — the way the two rules
dropped on 19 August 2026 were.

---

## 3. What an experience is made of

Sketch, not a contract. The contract is written after the three decisions above.

- **It is devised.** Not chosen from a list. Fresh each time, from what this house has —
  which displays, which paper, what was liked before — and from nothing about a person that
  is a verdict.
- **It has steps on different surfaces.** A display says something now; a sheet is left on
  the table as a physical object; a page comes back through the glass and changes what
  happens next. The surfaces are the senses this house has, and the list will grow. The
  agent should not change when it does: another surface is another tool, not another agent.
- **It is followed.** What comes back is read, and the next step is decided knowing it.
  That is the difference between an experience and a worksheet, and it is the expensive
  part.
- **It ends.** A few hours, and then it is over and says so. Nothing waits for a page that
  never comes back.

**Where it starts.** `shared/pagedesign.py` for the marks and the ink budget, which stay.
`shared/blueprint.py` for the argument about readable plans, which stays even though the
format will not. `panel/routes/reminders.py` for the shape of "the house asks and the cloud
thinks inside the answer". `agents/sheet_designer.py` for the prompt work already measured.

**Done when.** One experience is devised by a model, approved by a parent in full, run
across an afternoon on the two displays and the printer, followed through at least one
page coming back off the glass, and finished — with the parent able to read afterwards what
happened, and nothing kept that is a claim about anybody.

**What it costs.** The largest thing attempted here. It replaces the paper loop, changes
what approval means, and puts a model in charge of a plan rather than of a paragraph. The
mitigation is the order: the three decisions above, then a contract, then one experience by
hand in that contract before any model fills it — the same sequence `07 §1` used, and the
reason it found the reading defect before the format was built on.
