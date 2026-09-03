/* The readings, which exist while the prompts are being changed.
 *
 * Two properties are worth a test rather than a look. The counts are what the page is for
 * — a finding on eight afternoons of ten is a prompt problem and on one is an afternoon —
 * and a reading with nothing to report has to look like a result rather than like a page
 * that failed to load.
 */
import { screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { Verdicts } from "@/sections/Verdicts";
import { fakeApi } from "@/test/fakeApi";
import { renderPanel } from "@/test/render";

describe("the readings", () => {
  it("shows what the reader worked out beside the afternoon it read", async () => {
    renderPanel(fakeApi(), <Verdicts />);

    expect(await screen.findByText("Un pomeriggio di nuvole")).toBeInTheDocument();
    expect(screen.getByText("Che forma aveva la nuvola delle sei")).toBeInTheDocument();
    expect(
      screen.getByText("Il terzo aiuto consegna il dettaglio ripetuto."),
    ).toBeInTheDocument();
    // The name from the closed list, and where it was found, unpacked by the panel.
    expect(screen.getByText("given_away · moments[1].help[2]")).toBeInTheDocument();
  });

  it("counts the findings across afternoons, which is what the page is for", async () => {
    renderPanel(fakeApi(), <Verdicts />);

    await screen.findByText("Un pomeriggio di nuvole");
    const counts = screen.getByText("given_away").closest("dl");
    expect(counts).toHaveTextContent("1/2");
    expect(counts).toHaveTextContent("riletti");
  });

  it("says plainly when a reader had nothing to report", async () => {
    renderPanel(fakeApi(), <Verdicts />);

    expect(await screen.findByText("Nessun rilievo.")).toBeInTheDocument();
  });

  it("says so when nothing has been read back yet", async () => {
    renderPanel(fakeApi({ verdicts: async () => [] }), <Verdicts />);

    expect(await screen.findByText("Nessun pomeriggio è ancora stato riletto.")).toBeInTheDocument();
  });
});
