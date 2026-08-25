/* Choosing where the house is, and being able to check the answer.
 *
 * A timezone is the one setting a parent cannot verify by reading it back: `Europe/Rome`
 * and `Europe/London` look equally plausible on a screen, and the difference only shows
 * up an hour later when nothing happens. So the page puts the clock next to the choice.
 *
 * The list had two faults and only one was the one guessed at. `Europe/Rome` is in the
 * browser's list — checked, 418 zones and 58 in Europe — so nothing was missing. What was
 * wrong is that 418 identifiers in database order put Rome pages away from Paris, and
 * that they read as paths rather than as places.
 *
 * Nothing here asserts a particular offset. Rome is UTC+2 today and UTC+1 in January, so
 * a test that pinned the number would pass until the clocks changed.
 */
import { screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { cityOf, offsetNow } from "@/sections/Rhythm";
import { fakeApi } from "@/test/fakeApi";
import { renderPanel } from "@/test/render";

const JULY = new Date("2026-07-15T12:00:00Z");
const JANUARY = new Date("2026-01-15T12:00:00Z");

async function openRhythm(user: ReturnType<typeof userEvent.setup>) {
  await user.click(
    within(screen.getByRole("navigation")).getByRole("button", { name: "Ritmo" }),
  );
}

describe("what a zone is called", () => {
  it("shows the city, not the identifier", () => {
    expect(cityOf("Europe/Rome")).toBe("Rome");
    expect(cityOf("America/New_York")).toBe("New York");
    expect(cityOf("America/Argentina/Ushuaia")).toBe("Argentina · Ushuaia");
    expect(cityOf("UTC")).toBe("UTC");
  });
});

describe("where a zone sits", () => {
  it("follows summer time rather than a fixed offset", () => {
    /* The whole reason the offset is read out of a formatted date instead of stored. */
    expect(offsetNow("Europe/Rome", JULY)).toBe(120);
    expect(offsetNow("Europe/Rome", JANUARY)).toBe(60);
  });

  it("puts Rome with Paris in both halves of the year", () => {
    /* What the parent asked for: the cities that agree on the hour, together. */
    for (const at of [JULY, JANUARY]) {
      expect(offsetNow("Europe/Rome", at)).toBe(offsetNow("Europe/Paris", at));
      expect(offsetNow("Europe/Madrid", at)).toBe(offsetNow("Europe/Paris", at));
    }
  });

  it("does not put London with Paris, in either half", () => {
    /* The failure this setting exists for: the hub was on London and the house is not. */
    for (const at of [JULY, JANUARY]) {
      expect(offsetNow("Europe/London", at)).not.toBe(offsetNow("Europe/Paris", at));
    }
  });

  it("reads a zone behind UTC as a negative offset", () => {
    expect(offsetNow("America/New_York", JULY)).toBe(-240);
    expect(offsetNow("Pacific/Kiritimati", JULY)).toBe(840);
  });
});

describe("choosing it on the page", () => {
  it("gathers Rome with Paris under one heading", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());
    await openRhythm(user);

    const chooser = await screen.findByLabelText("Fuso orario di casa");
    const rome = within(chooser).getByRole("option", { name: /^Rome/ });
    const paris = within(chooser).getByRole("option", { name: /^Paris/ });

    expect(rome.parentElement?.tagName).toBe("OPTGROUP");
    expect(rome.parentElement).toBe(paris.parentElement);
  });

  it("does not put London under that heading", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());
    await openRhythm(user);

    const chooser = await screen.findByLabelText("Fuso orario di casa");
    const rome = within(chooser).getByRole("option", { name: /^Rome/ });
    const london = within(chooser).getByRole("option", { name: /^London/ });

    expect(london.parentElement).not.toBe(rome.parentElement);
  });

  it("shows the time the house will keep, so the choice can be checked", async () => {
    /* The confirmation. `fakeApi` has the household in Europe/Rome, and what is asserted
     * is that a clock is there and reads as one — not what it says, which changes every
     * second and twice a year. */
    const user = userEvent.setup();
    renderPanel(fakeApi());
    await openRhythm(user);

    await screen.findByLabelText("Fuso orario di casa");
    const now = new Intl.DateTimeFormat("it", {
      timeZone: "Europe/Rome",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date());

    expect(screen.getByText(new RegExp(now.replace(":", ":")))).toBeInTheDocument();
  });

  it("says it cannot tell the time when no zone has been chosen", async () => {
    const kept = fakeApi();
    const api = fakeApi({
      rhythm: async () => ({ ...(await kept.rhythm()), timeZone: "" }),
    });
    const user = userEvent.setup();
    renderPanel(api);
    await openRhythm(user);

    expect(
      await screen.findByText("Da qui non si vede che ora è in casa."),
    ).toBeInTheDocument();
  });
});
