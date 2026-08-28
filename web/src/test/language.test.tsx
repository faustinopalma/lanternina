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
import italian from "@/i18n/it.json";

async function openSettings(user: ReturnType<typeof userEvent.setup>) {
  const menu = screen.getByRole("navigation");
  await user.click(within(menu).getByRole("button", { name: "Da dove partire" }));
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
    // Something has to change before there is anything to save. The button is the
    // confirmation, so it is grey until the screen and the house differ.
    await user.selectOptions(await screen.findByLabelText("Lingua dei contenuti"), "en");
    await user.click(screen.getByRole("button", { name: "Salva" }));

    await waitFor(() => expect(api.recorded.preferences).toHaveLength(1));
    expect(Object.keys(api.recorded.preferences[0]!).sort()).toEqual([
      "avoid",
      "difficulty",
      "interests",
      "language",
      "note",
      "sheets",
      "variety",
    ]);
  });

  it("says the writing is inert, in the words the parent reads", async () => {
    // Said by the save confirmation and not by a note above the controls: a parent needs
    // to know when it takes effect, not that our writes queue nothing.
    expect(italian["preferences.saved"]).toMatch(/al prossimo giro/i);
    expect(italian["rhythm.saved"]).toMatch(/al prossimo giro/i);
  });

  it("says when the note stops standing, because that is what makes it safe to write", async () => {
    // The note is the one free paragraph on the page, so it is the one place a sentence
    // about a person can get in. It is bounded by being deleted, and a parent who cannot
    // see that has been given a permanent field that merely looks temporary.
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await openSettings(user);

    const note = await screen.findByLabelText("In questo periodo");
    expect(note).toHaveValue("");
    expect(screen.getByText(/28 giorni, poi si cancella/i)).toBeInTheDocument();

    await user.type(note, "mese pieno di scuola");
    await user.click(screen.getByRole("button", { name: "Salva" }));

    await waitFor(() => expect(api.recorded.preferences).toHaveLength(1));
    expect(api.recorded.preferences[0]?.note).toBe("mese pieno di scuola");
  });

  it("says the sheets number is a ceiling on the table, not a budget for the whole run", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await openSettings(user);

    const sheets = await screen.findByLabelText("Quanti fogli al massimo sul tavolo");
    expect(sheets).toHaveValue("2");
    expect(screen.getByText(/tetto, non un obiettivo/i)).toBeInTheDocument();
    expect(screen.getByText(/non quanti ne stampa in tutto/i)).toBeInTheDocument();

    await user.selectOptions(sheets, "1");
    await user.click(screen.getByRole("button", { name: "Salva" }));

    await waitFor(() => expect(api.recorded.preferences).toHaveLength(1));
    expect(api.recorded.preferences[0]?.sheets).toBe(1);
  });
});
