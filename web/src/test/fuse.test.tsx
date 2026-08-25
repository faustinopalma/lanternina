/* The fuse, on the page a parent lands on.
 *
 * The property worth pinning is the one a quiet failure would hide: a house stopped by
 * the fuse must say so where somebody who came to find out why nothing happened will read
 * it, which is the first page and not a settings section they have to go looking for.
 */
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import type { UsageAnswer } from "@/api/types";
import { fakeApi } from "@/test/fakeApi";
import { renderPanel } from "@/test/render";

function blown(overrides: Partial<UsageAnswer> = {}) {
  const api = fakeApi();
  const base = api.usage;
  return fakeApi({
    usage: async () => ({
      ...(await base()),
      cap: 900,
      spent: 900,
      reached: true,
      ...overrides,
    }),
  });
}

describe("the fuse", () => {
  it("says nothing at all while it is whole", async () => {
    renderPanel(fakeApi());

    await screen.findByRole("navigation");
    expect(screen.queryByRole("alert")).toBeNull();
  });

  it("says the house is stopped on the page the parent lands on", async () => {
    renderPanel(blown());

    const said = await screen.findByRole("alert");
    // The section the panel opens on, so this was not reached by going looking for it.
    expect(screen.getByRole("heading", { name: "Da approvare" })).toBeVisible();
    expect(said).toHaveTextContent("Il fusibile è saltato");
    // The two figures a parent needs to judge it: what was spent and where the fuse is.
    expect(said).toHaveTextContent("900 chiamate");
    expect(said).toHaveTextContent("fusibile è a 900");
  });

  it("offers twice where it is, and never past what the panel may set", async () => {
    renderPanel(blown({ cap: 19_000, spent: 19_000, maxCap: 20_000 }));

    await screen.findByRole("alert");
    expect(await screen.findByLabelText("Alza il fusibile a")).toHaveValue(20_000);
  });

  it("raises it and says the house carries on by itself", async () => {
    const api = blown();
    const user = userEvent.setup();
    renderPanel(api);

    await screen.findByRole("alert");
    await user.click(screen.getByRole("button", { name: "Alza" }));

    await screen.findByText(/Fusibile alzato/);
    await waitFor(() => expect(api.recorded.fuseRaisedTo).toEqual([1800]));
    // No form left behind: pressing it twice would only move it again.
    expect(screen.queryByLabelText("Alza il fusibile a")).toBeNull();
  });
});
