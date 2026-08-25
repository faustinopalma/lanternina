/* Choosing where the house is, and being able to check the answer.
 *
 * A timezone is the one setting a parent cannot verify by reading it back: `Europe/Rome`
 * and `Europe/London` look equally plausible on a screen, and the difference only shows
 * up an hour later when nothing happens. So the page puts a running clock next to it.
 *
 * The list took three goes and the middle one is the lesson. First it was 418 raw
 * identifiers in database order. Then they were gathered by their offset — which reads
 * well and is useless, because finding Rome under UTC+02:00 means already knowing Rome is
 * on UTC+2 today, and Italy is on +1 for five months of the year. The question the parent
 * is asking IS the offset. Now it is one alphabetical list of "City — Country", typed
 * into rather than scrolled through.
 *
 * Nothing here asserts a particular offset inside the page. Rome is UTC+2 today and UTC+1
 * in January, so a test that pinned the number would pass until the clocks changed.
 */
import { screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { cityOf, offsetNow, placesIn } from "@/sections/Rhythm";
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
  it("shows the city in the panel's language, and falls back to the database", () => {
    /* `Intl` has no city name, so the ones that differ come from CLDR. The rest fall back
     * to the identifier's own segment, which is already English. */
    expect(cityOf("Europe/Rome", "it")).toBe("Roma");
    expect(cityOf("Europe/London", "it")).toBe("Londra");
    expect(cityOf("Africa/Cairo", "it")).toBe("Il Cairo");
    expect(cityOf("Europe/Rome", "en")).toBe("Rome");
    // No Italian of its own, so the database's spelling stands — which is right.
    expect(cityOf("America/New_York", "it")).toBe("New York");
    expect(cityOf("America/Argentina/Ushuaia", "it")).toBe("Argentina · Ushuaia");
    expect(cityOf("UTC", "it")).toBe("UTC");
  });

  it("names the country in the language the panel is in", () => {
    const italian = placesIn("it");
    const english = placesIn("en");

    expect(italian.find((p) => p.zone === "Europe/Rome")?.label).toBe("Roma — Italia");
    expect(english.find((p) => p.zone === "Europe/Rome")?.label).toBe("Rome — Italy");
    expect(italian.find((p) => p.zone === "Europe/London")?.label).toBe(
      "Londra — Regno Unito",
    );
  });

  it("keeps the English spelling beside a translated one, so both can be typed", () => {
    /* A parent who has seen "Rome" before must not fail to find it now that it says
     * Roma. Where the two agree there is nothing to keep. */
    const italian = placesIn("it");

    expect(italian.find((p) => p.zone === "Europe/Rome")?.alsoKnownAs).toBe("Rome");
    expect(italian.find((p) => p.zone === "America/New_York")?.alsoKnownAs).toBe("");
    expect(placesIn("en").every((p) => p.alsoKnownAs === "")).toBe(true);
  });

  it("gives every zone a country, leaving none unfindable", () => {
    /* There is no zone-to-country call, so this is built by walking 676 country codes and
     * turning the answer round. A zone the walk misses would sit under a bare city name
     * with nothing to search it by. */
    const places = placesIn("it");

    expect(places.length).toBeGreaterThan(300);
    expect(places.filter((p) => !p.label.includes(" — "))).toEqual([]);
  });

  it("does not label a place with a withdrawn code nobody would look under", () => {
    /* Riyadh came back as "NT" — the Neutral Zone, retired decades ago but still claiming
     * the zone and sorting before SA. Six zones were affected. */
    const places = placesIn("it");
    const country = (zone: string) => places.find((p) => p.zone === zone)?.label.split(" — ")[1];

    expect(country("Asia/Riyadh")).toBe("Arabia Saudita");
    expect(country("Pacific/Kiritimati")).toBe("Kiribati");
    expect(places.filter((p) => /— [A-Z]{2}$/.test(p.label))).toEqual([]);
  });

  it("is in alphabetical order for the language it is in", () => {
    const labels = placesIn("it").map((p) => p.label);

    expect(labels).toEqual([...labels].sort((a, b) => a.localeCompare(b, "it")));
  });
});

describe("where a zone sits", () => {
  it("follows summer time rather than a fixed offset", () => {
    /* The whole reason the offset is read out of a formatted date instead of stored, and
     * the reason the list is no longer grouped by it. */
    expect(offsetNow("Europe/Rome", JULY)).toBe(120);
    expect(offsetNow("Europe/Rome", JANUARY)).toBe(60);
  });

  it("does not put London on the same offset as Paris, in either half", () => {
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
  it("offers the places to type into, in one alphabetical list", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());
    await openRhythm(user);

    const box = await screen.findByLabelText("Fuso orario di casa");
    const list = document.getElementById(box.getAttribute("list") ?? "");
    const labels = [...(list?.children ?? [])].map((option) => option.getAttribute("value"));

    expect(labels).toContain("Roma — Italia");
    expect(labels).toContain("Parigi — Francia");
    expect(labels.length).toBeGreaterThan(300);
  });

  it("shows the chosen place written out, not the identifier", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());
    await openRhythm(user);

    expect(await screen.findByLabelText("Fuso orario di casa")).toHaveValue("Roma — Italia");
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

    expect(screen.getByText(new RegExp(now))).toBeInTheDocument();
  });

  it("does not claim to know the hour while the name is half typed", async () => {
    /* A half-typed word is not a half-chosen setting. The clock would otherwise go on
     * showing the previous place while the box says something else. */
    const user = userEvent.setup();
    renderPanel(fakeApi());
    await openRhythm(user);

    const box = await screen.findByLabelText("Fuso orario di casa");
    await user.clear(box);
    await user.type(box, "Rom");

    expect(screen.getByText("Da qui non si vede che ora è in casa.")).toBeInTheDocument();
  });

  it("takes the place once the whole name is there", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());
    await openRhythm(user);

    const box = await screen.findByLabelText("Fuso orario di casa");
    await user.clear(box);
    await user.type(box, "Parigi — Francia");

    expect(
      screen.queryByText("Da qui non si vede che ora è in casa."),
    ).not.toBeInTheDocument();
  });
});
