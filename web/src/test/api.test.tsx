/* The boundary with the API.
 *
 * Written after a real failure: the deployed API was six commits behind the panel and
 * answered /api/pictures without any paging fields. The panel read `pageSizes.map` on
 * nothing and the whole page went white, taking the menu with it.
 *
 * Two things had to become true. An answer that does not carry what a section needs is a
 * failure to read it, not data — because showing an empty form instead would let a parent
 * take the blank for a choice nobody made. And whatever still gets through must not be
 * able to erase the panel.
 */
import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { httpApi } from "@/api/client";
import { Boundary } from "@/components/Boundary";

function answering(body: unknown, status = 200) {
  return vi.fn().mockResolvedValue({
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  } as unknown as Response);
}

afterEach(() => vi.unstubAllGlobals());

describe("an answer that is not the shape the panel needs", () => {
  const CURRENT_PICTURES = {
    pictures: [],
    page: 1,
    perPage: 20,
    pages: 1,
    total: 0,
    pageSizes: [10, 20, 30, 50],
  };

  it("is refused when the paging fields are missing", async () => {
    // Exactly what the API at bb4fee8 answered.
    vi.stubGlobal("fetch", answering({ pictures: [] }));
    await expect(httpApi("t").pictures(1, 20)).rejects.toThrow(/pageSizes/);
  });

  it("is accepted when they are all there", async () => {
    vi.stubGlobal("fetch", answering(CURRENT_PICTURES));
    await expect(httpApi("t").pictures(1, 20)).resolves.toMatchObject({ total: 0 });
  });

  it("is refused when the rhythm comes back in the old shape", async () => {
    vi.stubGlobal("fetch", answering({ quietFromHour: 21, quietUntilHour: 7, cadenceHours: 1 }));
    await expect(httpApi("t").rhythm()).rejects.toThrow(/quietFrom/);
  });

  it("is refused when the settings route is not there at all", async () => {
    vi.stubGlobal("fetch", answering({ detail: "Not Found" }, 404));
    await expect(httpApi("t").preferences()).rejects.toThrow();
  });
});

describe("what /api/me says", () => {
  it("tells the three cases apart without showing a number to anyone", async () => {
    vi.stubGlobal("fetch", answering({ accountId: "a", householdId: "h", status: "active" }));
    expect((await httpApi("t").admission()).kind).toBe("in");

    vi.stubGlobal("fetch", answering({ detail: "not_authorised" }, 403));
    expect((await httpApi("t").admission()).kind).toBe("pending");

    vi.stubGlobal("fetch", answering({ detail: "auth_not_configured" }, 503));
    expect((await httpApi("t").admission()).kind).toBe("noAuth");
  });
});

describe("a section that throws", () => {
  function Broken(): never {
    throw new Error("boom");
  }

  it("is contained, and the rest of the panel stays where it is", () => {
    // React reports a caught error to the console; the parent must not see it either way.
    const logged = vi.spyOn(console, "error").mockImplementation(() => undefined);

    render(
      <div>
        <p>il menu</p>
        <Boundary resetOn="pictures" fallback={<p>questa sezione non si apre</p>}>
          <Broken />
        </Boundary>
      </div>,
    );

    expect(screen.getByText("questa sezione non si apre")).toBeInTheDocument();
    expect(screen.getByText("il menu")).toBeInTheDocument();
    expect(document.body.textContent).not.toContain("boom");
    logged.mockRestore();
  });
});
