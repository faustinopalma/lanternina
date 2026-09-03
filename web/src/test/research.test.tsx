/* The history of the research runs, as a table read along its rows.
 *
 * What is being read is a difference between two runs on one axis, so the shape of the
 * table is the feature: an axis per row, a run per column, and the denominator in the
 * header rather than in a footnote — a mean over 24 afternoons and a mean over 4 are not
 * the same number, and a table that hides which is which invites the wrong comparison.
 */
import { screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { Research } from "@/sections/Research";
import { fakeApi } from "@/test/fakeApi";
import { renderPanel } from "@/test/render";

describe("the research runs", () => {
  it("puts one run in each column, oldest first, with its denominator", async () => {
    renderPanel(fakeApi(), <Research />);

    const head = within(await screen.findByRole("table")).getAllByRole("columnheader");
    expect(head.map((cell) => cell.textContent)).toEqual([
      "asse",
      expect.stringContaining("prima-corsa"),
      expect.stringContaining("dopo"),
    ]);
    expect(head[1]).toHaveTextContent("24 pomeriggi");
    // The runs that predate fingerprints can be read and not lined up against a later one.
    expect(head[1]).toHaveTextContent("—");
    expect(head[2]).toHaveTextContent("d427131c594e");
  });

  it("reads along a row, so a move on one axis is visible", async () => {
    renderPanel(fakeApi(), <Research />);

    const row = (await screen.findByText("sheetStandsAlone")).closest("tr");
    expect(row).toHaveTextContent("1.95");
    expect(row).toHaveTextContent("3.61");
  });

  it("says so when no run has been recorded", async () => {
    renderPanel(fakeApi({ research: async () => [] }), <Research />);

    expect(await screen.findByText("Nessuna corsa registrata.")).toBeInTheDocument();
  });
});
