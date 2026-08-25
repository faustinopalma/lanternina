/* The monthly limit, on the page a parent lands on.
 *
 * The property worth pinning is the one a quiet failure would hide: a house stopped by
 * the limit must say so where somebody who came to find out why nothing happened will
 * read it, which is the first page and not a settings section they have to go looking for.
 */
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import type { UsageAnswer } from "@/api/types";
import { fakeApi } from "@/test/fakeApi";
import { renderPanel } from "@/test/render";

function reached(overrides: Partial<UsageAnswer> = {}) {
  const api = fakeApi();
  const base = api.usage;
  return fakeApi({
    usage: async () => ({
      ...(await base()),
      limit: 900,
      spent: 900,
      reached: true,
      ...overrides,
    }),
  });
}

describe("the monthly limit", () => {
  it("says nothing at all while the house is under it", async () => {
    renderPanel(fakeApi());

    await screen.findByRole("navigation");
    expect(screen.queryByRole("alert")).toBeNull();
  });

  it("says the house is stopped on the page the parent lands on", async () => {
    renderPanel(reached());

    const said = await screen.findByRole("alert");
    // The section the panel opens on, so this was not reached by going looking for it.
    expect(screen.getByRole("heading", { name: "Da approvare" })).toBeVisible();
    expect(said).toHaveTextContent("La casa ha raggiunto il limite");
    // The two figures a parent needs to judge it: what was spent and where the limit is.
    expect(said).toHaveTextContent("900 chiamate");
    expect(said).toHaveTextContent("limite è 900");
  });

  it("offers twice where it is, and never past what the panel may set", async () => {
    renderPanel(reached({ limit: 19_000, spent: 19_000, maxLimit: 20_000 }));

    await screen.findByRole("alert");
    expect(await screen.findByLabelText("Alza il limite a")).toHaveValue(20_000);
  });

  it("raises it and says the house carries on by itself", async () => {
    const api = reached();
    const user = userEvent.setup();
    renderPanel(api);

    await screen.findByRole("alert");
    await user.click(screen.getByRole("button", { name: "Alza" }));

    await screen.findByText(/Limite alzato/);
    await waitFor(() => expect(api.recorded.limitSetTo).toEqual([1800]));
    // No form left behind: pressing it twice would only move it again.
    expect(screen.queryByLabelText("Alza il limite a")).toBeNull();
  });

  it("can be set from the usage page without waiting for the house to stop", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await user.click(screen.getByRole("button", { name: "Consumo" }));
    const field = await screen.findByLabelText("Chiamate al mese");
    // What it is now, so the parent edits a figure rather than typing into a blank.
    expect(field).toHaveValue(900);

    await user.clear(field);
    await user.type(field, "3000");
    await user.click(screen.getByRole("button", { name: "Salva" }));

    await waitFor(() => expect(api.recorded.limitSetTo).toEqual([3000]));
    await screen.findByText("Limite salvato: 3000 chiamate al mese.");
  });
});
