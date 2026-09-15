/* Two things a parent runs into that nothing was watching.
 *
 * The API scales to zero, so the first request of a sitting can lose a race with the
 * container starting. Until this was covered, a section that lost that race said it could
 * not read anything and stayed that way — the only way out was reloading the page. And
 * reloading threw them back to the first section, which is a worse fault than the one that
 * made them reload.
 */
import { fireEvent, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { fakeApi } from "@/test/fakeApi";
import { renderPanel } from "@/test/render";

function open(user: ReturnType<typeof userEvent.setup>, name: string) {
  return user.click(within(screen.getByRole("navigation")).getByRole("button", { name }));
}

describe("coming back to the panel", () => {
  beforeEach(() => {
    window.localStorage.clear();
    window.location.hash = "";
  });
  afterEach(() => {
    window.location.hash = "";
  });

  it("fits the menu below its actual viewport position after scrolling and resizing", () => {
    const bounds = vi.spyOn(HTMLElement.prototype, "getBoundingClientRect")
      .mockReturnValue(new DOMRect(0, 140, 208, 500));
    try {
      const { unmount } = renderPanel(fakeApi());
      const menu = screen.getByRole("complementary");
      expect(menu.style.getPropertyValue("--menu-top")).toBe("140px");

      bounds.mockReturnValue(new DOMRect(0, 24, 208, 500));
      fireEvent.scroll(window);
      expect(menu.style.getPropertyValue("--menu-top")).toBe("24px");

      bounds.mockReturnValue(new DOMRect(0, 180, 208, 500));
      fireEvent.resize(window);
      expect(menu.style.getPropertyValue("--menu-top")).toBe("180px");

      unmount();
      bounds.mockClear();
      fireEvent.scroll(window);
      fireEvent.resize(window);
      expect(bounds).not.toHaveBeenCalled();
    } finally {
      bounds.mockRestore();
    }
  });

  it("puts the open section in the address bar", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());

    await open(user, "Ritmo");

    await waitFor(() => expect(window.location.hash).toBe("#rhythm"));
  });

  it("opens where the address bar says, which is what a reload lands on", async () => {
    /* A reload is something a parent does when a section will not load. Losing their place
       as well is the fault that made the first one worse. */
    window.location.hash = "#usage";
    renderPanel(fakeApi());

    const nav = within(screen.getByRole("navigation"));
    expect(await nav.findByRole("button", { name: "Consumo" })).toHaveAttribute(
      "aria-current",
      "true",
    );
  });

  it("falls back to the first section when the address names one that is gone", async () => {
    window.location.hash = "#qualcosa-che-non-esiste";
    renderPanel(fakeApi());

    const nav = within(screen.getByRole("navigation"));
    expect(
      await nav.findByRole("button", { name: "In attesa di una decisione" }),
    ).toHaveAttribute("aria-current", "true");
  });

  it("asks a second time before saying it cannot read anything", async () => {
    /* One retry and no more. A section that kept asking would hold the container up and
       cost money for nobody's benefit. */
    let asked = 0;
    const api = fakeApi({
      rhythm: async () => {
        asked += 1;
        if (asked === 1) throw new Error("il contenitore si stava accendendo");
        return fakeApi().rhythm();
      },
    });
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Ritmo");

    expect(
      await screen.findByLabelText("Quadro nuovo ogni", {}, { timeout: 4000 }),
    ).toBeInTheDocument();
    expect(asked).toBe(2);
  });

  it("says so plainly once it has tried twice", async () => {
    let asked = 0;
    const api = fakeApi({
      rhythm: async () => {
        asked += 1;
        throw new Error("via");
      },
    });
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Ritmo");

    expect(
      await screen.findByText(/Non riesco a leggere/, {}, { timeout: 4000 }),
    ).toBeInTheDocument();
    expect(asked).toBe(2);
  });
});
