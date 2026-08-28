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
});
