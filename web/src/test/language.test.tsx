/* The content language belongs to the household, and the language of this page does not.
 *
 * This is the guarantee that is easiest to lose by accident: one convenient line wiring the
 * page's language selector to the settings, and a parent switching their phone to English
 * silently changes what arrives on paper. The test fails on that line.
 */
import { screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it } from "vitest";

import { fakeApi } from "@/test/fakeApi";
import { renderPanel } from "@/test/render";

async function openSettings(user: ReturnType<typeof userEvent.setup>) {
  const menu = screen.getByRole("navigation");
  await user.click(within(menu).getByRole("button", { name: "Interessi e difficoltà" }));
}

describe("the language of the page", () => {
  beforeEach(() => window.localStorage.clear());

  it("does not touch the settings when the parent switches it", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await openSettings(user);
    await screen.findByLabelText("Lingua dei contenuti");

    await user.selectOptions(screen.getByLabelText("Lingua"), "en");

    // The page is in English now; the household's content language is still Italian.
    expect(await screen.findByLabelText("Content language")).toHaveValue("it");
    expect(api.recorded.preferences).toEqual([]);
  });

  it("saves the content language only when the parent asks for it", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await openSettings(user);
    const chosen = await screen.findByLabelText("Lingua dei contenuti");

    await user.selectOptions(chosen, "en");
    // Still nothing saved: choosing is not saving.
    expect(api.recorded.preferences).toEqual([]);
    // And the page has not changed language either: this is the household's setting.
    expect(screen.getByLabelText("Lingua")).toHaveValue("it");

    await user.click(screen.getByRole("button", { name: "Salva" }));
    await waitFor(() => expect(api.recorded.preferences).toHaveLength(1));
    expect(api.recorded.preferences[0]?.language).toBe("en");
  });
});

describe("what a saved setting carries", () => {
  beforeEach(() => window.localStorage.clear());

  it("sends exactly the fields the settings are made of, and no name", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await openSettings(user);
    await screen.findByLabelText("Lingua dei contenuti");
    await user.click(screen.getByRole("button", { name: "Salva" }));

    await waitFor(() => expect(api.recorded.preferences).toHaveLength(1));
    expect(Object.keys(api.recorded.preferences[0]!).sort()).toEqual([
      "avoid",
      "difficulty",
      "interests",
      "language",
      "maxWordsPerLine",
      "variety",
    ]);
  });

  it("says the writing is inert, in the words the parent reads", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());

    await openSettings(user);
    expect(
      await screen.findByText(/salvare qui non avvia nessuna generazione/i),
    ).toBeInTheDocument();
  });
});
