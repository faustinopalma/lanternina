/* The record of what the system wrote.
 *
 * Two things are held here. A card carries nothing but a title, a date and the idea — the
 * script arrives when the parent opens one, and until then the page has not paid for it.
 * And what is shown is the system's half only: there is no path from this page to what the
 * adolescent did, because there is no such thing stored.
 */
import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { fakeApi } from "@/test/fakeApi";
import { TheTrail } from "@/sections/Trail";
import { renderPanel } from "@/test/render";

describe("what the system wrote", () => {
  it("shows a card per afternoon, without its script", async () => {
    renderPanel(fakeApi(), <TheTrail />);

    expect(await screen.findByText("Un pomeriggio di nuvole")).toBeInTheDocument();
    expect(screen.getByText(/Si guarda il cielo/)).toBeInTheDocument();
    expect(screen.queryByText(/THE WORLD/)).not.toBeInTheDocument();
  });

  it("opens the script and everything written under it", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi(), <TheTrail />);

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Apri" }));

    expect(await screen.findByText(/THE WORLD/)).toBeInTheDocument();
    expect(screen.getByText("Guarda fuori e dimmi che forma ha.")).toBeInTheDocument();
    // The act it performed, in the house's own vocabulary rather than a second one.
    expect(screen.getByText("Detto su un display")).toBeInTheDocument();
    expect(screen.getByText("Foglio stampato")).toBeInTheDocument();
    // The reasoning reached nobody in the room. It reaches the parent afterwards.
    expect(screen.getByText("Perché: il foglio era tornato vuoto")).toBeInTheDocument();
  });

  it("says so plainly when nothing has run", async () => {
    renderPanel(fakeApi({ trails: async () => [] }), <TheTrail />);

    expect(await screen.findByText("Nessuna attività ancora.")).toBeInTheDocument();
  });

  it("shows the sheet a model wrote, and not the document it arrived as", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi(), <TheTrail />);

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Apri" }));

    expect(await screen.findByText("Sul foglio")).toBeInTheDocument();
    expect(screen.getByText(/Guarda il cielo e disegna quello che vedi/)).toBeInTheDocument();
    expect(screen.queryByText(/^\{/)).not.toBeInTheDocument();
  });

  it("says of a line kept while building that it deletes itself", async () => {
    const user = userEvent.setup();
    const api = fakeApi();
    const whole = await api.trail("aft_1");
    renderPanel(
      fakeApi({
        trail: async () => ({
          ...whole,
          made: [
            {
              id: "made_3",
              at: 0,
              kind: "came",
              heading: "l-ultimo-foglio",
              body: "un cavallo nel terzo riquadro",
              why: "marks",
              pictureId: "",
              asked: "",
              paper: "",
              until: 2_000_000_000,
            },
          ],
        }),
      }),
      <TheTrail />,
    );

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Apri" }));

    expect(await screen.findByText("Quello che è tornato dal vetro")).toBeInTheDocument();
    expect(screen.getByText(/si cancella da sola/)).toBeInTheDocument();
  });

  it("indexes what reached paper, and says when a sheet did not", async () => {
    /* The 5 September 2026 defect, on the side a parent reads. The queue accepted two pages
       and the printer was on another network; the afternoon carried on and the record showed
       one that had gone as written. A page that never arrived now has to be visible here
       without opening every move. */
    const user = userEvent.setup();
    const api = fakeApi();
    const whole = await api.trail("aft_1");
    renderPanel(
      fakeApi({
        trail: async () => ({
          ...whole,
          made: [
            {
              id: "made_9",
              at: 0,
              kind: "fault",
              heading: "il-foglio-del-cielo",
              body: "no page reached the table\nthe printer did not take the page within 120 seconds",
              why: "standard",
              pictureId: "",
              asked: "",
              paper: "",
              until: 0,
            },
          ],
        }),
      }),
      <TheTrail />,
    );

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Apri" }));

    expect(await screen.findByText("Che cosa è finito su carta")).toBeInTheDocument();
    expect(screen.getByText(/Un foglio non è arrivato/)).toBeInTheDocument();
    // And the reason, so the parent knows it is a printer to switch on and not ours to fix.
    expect(screen.getByText(/did not take the page/)).toBeInTheDocument();
  });

  it("reads the afternoons and the readings in one place", async () => {
    /* They were two sections. A parent had to know that an activity they had not decided on
       yet was filed somewhere else from one that had run. */
    renderPanel(fakeApi(), <TheTrail />);

    expect(await screen.findByText("Riletture")).toBeInTheDocument();
  });

  it("does not read an afternoon twice when it has already run", async () => {
    /* An afternoon that ran carries its reading inside its own trail, filed as `judged`.
       Merging the two lists put the same title on the page under two headings. */
    renderPanel(fakeApi(), <TheTrail />);

    await screen.findByText("Riletture");
    expect(screen.getAllByText("Un pomeriggio di nuvole")).toHaveLength(1);
  });

  it("shows what the model was asked for, beside what it produced", async () => {
    /* A page that came out wrong cannot be judged without it: the question is whether it
       was drawn badly or asked for badly, and only one of those is the model's fault. */
    const user = userEvent.setup();
    renderPanel(fakeApi(), <TheTrail />);

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Apri" }));

    expect(await screen.findByText("Foglio disegnato")).toBeInTheDocument();
    expect(screen.getByText(/Che cosa e stato chiesto al modello/)).toBeInTheDocument();
    // A phrase only the request carries: the page's own words appear in both, and matching
    // one of those would pass whether or not the request was ever shown.
    expect(screen.getByText(/Letter this large/)).toBeInTheDocument();
  });

  it("empties the record, and asks twice before it does", async () => {
    /* One press cannot delete a record. The second is not a dialog: the button itself says
       what it is about to do, which is the sentence a parent needs before pressing again. */
    const user = userEvent.setup();
    renderPanel(fakeApi(), <TheTrail />);

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Svuota il registro" }));

    // Still there: the first press only changed what the button says.
    expect(screen.getByText("Un pomeriggio di nuvole")).toBeInTheDocument();
    await user.click(await screen.findByRole("button", { name: /Premi ancora/ }));

    expect(await screen.findByText(/Buttate 1 righe/)).toBeInTheDocument();
    expect(await screen.findByText("Nessuna attività ancora.")).toBeInTheDocument();
  });
});
