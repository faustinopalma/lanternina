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

  it("traces what the model did, in order, with what went in and what came out", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi(), <TheTrail />);

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Apri" }));

    expect(await screen.findByText(/THE WORLD/)).toBeInTheDocument();
    expect(screen.getByText("Guarda fuori e dimmi che forma ha.")).toBeInTheDocument();
    // The kind sits on the same line as the time, because a step of a trace is a moment
    // first and a category second.
    expect(screen.getByText(/Detto su un display/)).toBeInTheDocument();
    expect(screen.getByText(/Foglio stampato/)).toBeInTheDocument();
    // Both halves are labelled on every step, which is the whole shape of the page.
    expect(screen.getAllByText("Che cosa ne e uscito").length).toBeGreaterThan(0);
    // The reasoning reached nobody in the room. It reaches the parent afterwards.
    expect(screen.getByText("Perché: il foglio era tornato vuoto")).toBeInTheDocument();
  });

  it("keeps the steps in the order they happened", async () => {
    /* It is a trace, so the order is the content. Reading it by timestamp rather than by
       kind is what makes it possible to see what the model did after what. */
    const user = userEvent.setup();
    renderPanel(fakeApi(), <TheTrail />);

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Apri" }));
    await screen.findByText(/Detto su un display/);

    const steps = screen.getAllByRole("listitem").map((one) => one.textContent ?? "");
    const said = steps.findIndex((one) => one.includes("Detto su un display"));
    const drawn = steps.findIndex((one) => one.includes("Foglio disegnato"));
    const printed = steps.findIndex((one) => one.includes("Foglio stampato"));

    expect(said).toBeGreaterThanOrEqual(0);
    expect(drawn).toBeGreaterThan(said);
    expect(printed).toBeGreaterThan(drawn);
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

    expect(
      await screen.findByText(/Guarda il cielo e disegna quello che vedi/),
    ).toBeInTheDocument();
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

    expect(await screen.findByText(/Quello che è tornato dal vetro/)).toBeInTheDocument();
    expect(screen.getByText(/si cancella da sola/)).toBeInTheDocument();
  });

  it("puts a sheet that never arrived in the trace, with its reason", async () => {
    /* The 5 September 2026 defect, on the side a parent reads. The queue accepted two pages
       and the printer was on another network; the afternoon carried on and the record showed
       one that had gone as written. */
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

    expect(await screen.findByText(/Qui non ha funzionato/)).toBeInTheDocument();
    // And the reason, so the parent knows it is a printer to switch on and not ours to fix.
    expect(screen.getByText(/did not take the page/)).toBeInTheDocument();
  });

  it("has no readings section of its own any more", async () => {
    /* It was a second list under the trace, and a reading is one of the things the model
       did: it belongs in the trace, at the moment it happened, like everything else. */
    renderPanel(fakeApi(), <TheTrail />);

    await screen.findByText("Un pomeriggio di nuvole");
    expect(screen.queryByText("Riletture")).not.toBeInTheDocument();
  });

  it("shows what the model was asked for, beside what it produced", async () => {
    /* A page that came out wrong cannot be judged without it: the question is whether it
       was drawn badly or asked for badly, and only one of those is the model's fault. */
    const user = userEvent.setup();
    renderPanel(fakeApi(), <TheTrail />);

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Apri" }));

    expect(await screen.findByText(/Foglio disegnato/)).toBeInTheDocument();
    expect(screen.getByText("Che cosa e stato chiesto")).toBeInTheDocument();
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
