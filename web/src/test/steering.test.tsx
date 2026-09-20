import { act, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, expect, it, vi } from "vitest";

import { Steering } from "@/sections/Steering";
import { Experiences } from "@/sections/Experiences";
import { fakeApi } from "@/test/fakeApi";
import { renderPanel } from "@/test/render";

beforeEach(() => window.localStorage.clear());

it("saves and restores topics independently when the interface language changes", async () => {
  const api = fakeApi();
  const user = userEvent.setup();
  renderPanel(api, <Steering />);
  await user.click(await screen.findByRole("tab", { name: "Temi di partenza" }));
  await user.clear(screen.getByLabelText("Temi di partenza", { selector: "textarea" }));
  await user.paste("Mare e navigazione.");
  await user.click(screen.getByRole("button", { name: "Salva indicazioni" }));
  await waitFor(() => expect(api.recorded.steering).toHaveLength(1));
  await user.selectOptions(screen.getByRole("combobox"), "en");
  expect(await screen.findByLabelText("Design", { selector: "textarea" }))
    .toHaveValue("Propose activities with a clear goal.");
  await user.click(screen.getByRole("tab", { name: "Starting topics" }));
  expect(screen.getByLabelText("Starting topics", { selector: "textarea" }))
    .toHaveValue("Light, sound, maps and inventions.");
  await user.clear(screen.getByLabelText("Starting topics", { selector: "textarea" }));
  await user.paste("Tides and navigation.");
  await user.click(screen.getByRole("button", { name: "Save guidance" }));
  await waitFor(() => expect(api.recorded.steering).toHaveLength(2));
  await user.selectOptions(screen.getByRole("combobox"), "it");
  await user.click(await screen.findByRole("tab", { name: "Temi di partenza" }));
  expect(screen.getByLabelText("Temi di partenza", { selector: "textarea" }))
    .toHaveValue("Mare e navigazione.");
  await user.click(screen.getByRole("button", { name: "Ripristina questo prompt" }));
  await user.click(screen.getByRole("button", { name: "Conferma" }));
  await waitFor(() => expect(api.recorded.steering).toHaveLength(3));
  expect((await api.steering("en")).topics).toBe("Tides and navigation.");
  expect((await api.steering("it")).topics).toBe("Luce, suoni, mappe e invenzioni.");
});

it("ignores a late response for the previous language", async () => {
  const api = fakeApi();
  const italian = await api.steering("it");
  const english = await api.steering("en");
  let finish!: (value: typeof italian) => void;
  api.steering = vi.fn((language) => language === "it"
    ? new Promise<typeof italian>((resolve) => { finish = resolve; }) : Promise.resolve(english));
  const user = userEvent.setup();
  renderPanel(api, <Steering />);
  await waitFor(() => expect(api.steering).toHaveBeenCalledWith("it"));
  await user.selectOptions(screen.getByRole("combobox"), "en");
  expect(await screen.findByLabelText("Design", { selector: "textarea" }))
    .toHaveValue(english.instructions);
  await act(async () => { finish(italian); });
  expect(screen.getByLabelText("Design", { selector: "textarea" }))
    .toHaveValue(english.instructions);
});

it("waits for synthesis to finish before reading and showing the new summary", async () => {
  const api = fakeApi();
  const initial = { ...await api.steering(), pendingCount: 2, feedbackCount: 2 };
  const completed = { ...initial, pendingCount: 0, revision: 1, adaptive: "Usa obiettivi precisi." };
  let finish!: () => void;
  api.steering = vi.fn().mockResolvedValueOnce(initial).mockResolvedValue(completed);
  api.synthesizeSteering = vi.fn(() => new Promise<void>((resolve) => { finish = resolve; }));
  const user = userEvent.setup();
  renderPanel(api, <Steering />);
  await user.click(await screen.findByRole("button", { name: "Riprova la sintesi" }));
  expect(screen.getByText("Sintesi in corso.")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Riprova la sintesi" })).toBeDisabled();
  expect(api.steering).toHaveBeenCalledTimes(1);
  expect(screen.getByLabelText("Indicazioni dai feedback")).toHaveValue(initial.adaptive);
  finish();
  expect(await screen.findByText("Sintesi aggiornata.")).toBeInTheDocument();
  expect(screen.getByLabelText("Indicazioni dai feedback")).toHaveValue(completed.adaptive);
  expect(screen.queryByRole("button", { name: "Riprova la sintesi" })).not.toBeInTheDocument();
});

it.each([
  ["synthesis_failed", "La sintesi non è riuscita"],
  ["synthesis_limit", "Il limite mensile delle chiamate è raggiunto"],
])("preserves pending feedback and reports %s", async (error, message) => {
  const api = fakeApi();
  const initial = { ...await api.steering(), pendingCount: 2, feedbackCount: 2 };
  api.steering = vi.fn().mockResolvedValue(initial);
  api.synthesizeSteering = vi.fn().mockRejectedValue(new Error(error));
  const user = userEvent.setup();
  renderPanel(api, <Steering />);
  await user.click(await screen.findByRole("button", { name: "Riprova la sintesi" }));
  expect(await screen.findByText(new RegExp(message))).toBeInTheDocument();
  expect(screen.getByLabelText("Indicazioni dai feedback")).toHaveValue(initial.adaptive);
  expect(screen.getByText("Feedback da sintetizzare: 2")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Riprova la sintesi" })).toBeEnabled();
  expect(api.steering).toHaveBeenCalledTimes(1);
});

it("shows both texts and saves only the field deliberately edited", async () => {
  const api = fakeApi();
  const user = userEvent.setup();
  renderPanel(api, <Steering />);
  const field = await screen.findByLabelText("Progettazione", { selector: "textarea" });
  expect(screen.getByLabelText("Indicazioni dai feedback")).not.toHaveValue("");
  await user.clear(field);
  await user.paste("Usa problemi con un risultato verificabile.");
  await user.click(screen.getByRole("button", { name: "Salva indicazioni" }));
  await waitFor(() => expect(api.recorded.steering).toEqual([{
    revision: 0, action: "save", instructions: "Usa problemi con un risultato verificabile.",
  }]));
  expect(screen.getByRole("button", { name: "Salva indicazioni" })).toBeDisabled();
});

it("confirms resets and keeps the stable instructions", async () => {
  const api = fakeApi();
  const user = userEvent.setup();
  renderPanel(api, <Steering />);
  await screen.findByLabelText("Progettazione", { selector: "textarea" });
  await user.click(screen.getByRole("button", { name: "Azzera sintesi e feedback" }));
  expect(api.recorded.steering).toEqual([]);
  await user.click(screen.getByRole("button", { name: "Conferma" }));
  await waitFor(() => expect(api.recorded.steering[0]?.action).toBe("reset_adaptive"));
  expect(screen.getByLabelText("Progettazione", { selector: "textarea" })).toHaveValue(
    "Proponi attività con un obiettivo chiaro.");
});

it("preserves an edited draft and refreshes the untouched summary after a conflict", async () => {
  const api = fakeApi();
  const original = await api.steering();
  const current = { ...original, revision: 1, adaptive: "Sintesi appena aggiornata." };
  api.steering = vi.fn().mockResolvedValueOnce(original).mockResolvedValue(current);
  api.saveSteering = vi.fn().mockRejectedValueOnce(new Error("guidance_changed"))
    .mockImplementation(async (change) => ({ ...current, ...change, revision: 2 }));
  const user = userEvent.setup();
  renderPanel(api, <Steering />);
  await user.type(await screen.findByLabelText("Progettazione", { selector: "textarea" }), " Usa due indizi.");
  await user.click(screen.getByRole("button", { name: "Salva indicazioni" }));
  expect(await screen.findByText(/Le indicazioni salvate sono cambiate/)).toBeInTheDocument();
  await user.click(screen.getByRole("button", { name: "Aggiorna" }));
  await waitFor(() => expect(screen.getByLabelText("Indicazioni dai feedback"))
    .toHaveValue(current.adaptive));
  expect(screen.getByLabelText("Progettazione", { selector: "textarea" })).toHaveValue(
    original.instructions + " Usa due indizi.");
  await user.click(screen.getByRole("button", { name: "Salva indicazioni" }));
  expect(api.saveSteering).toHaveBeenLastCalledWith({ revision: 1, action: "save",
    instructions: original.instructions + " Usa due indizi." }, "it");
});

it("records selected rejection reasons and the free comment", async () => {
  const api = fakeApi();
  const user = userEvent.setup();
  renderPanel(api, <Experiences />);
  await user.click(await screen.findByRole("button", { name: "Rifiuta" }));
  await user.click(screen.getByLabelText("Troppo difficile"));
  await user.click(screen.getByLabelText("Troppo facile"));
  expect(screen.getByLabelText("Troppo difficile")).not.toBeChecked();
  await user.click(screen.getByLabelText("Troppo aperta: manca un obiettivo preciso"));
  await user.type(screen.getByLabelText("Commento facoltativo"), "Confrontare due indizi va bene.");
  await user.click(screen.getByRole("button", { name: "Conferma lo scarto" }));
  await waitFor(() => expect(api.recorded.feedback).toEqual([{
    id: "aftn-1", feedback: { reasons: ["too_easy", "too_open"],
      note: "Confrontare due indizi va bene." },
  }]));
});

it("keeps edits across tabs and restores only the selected prompt", async () => {
  const api = fakeApi();
  const initial = await api.steering();
  const user = userEvent.setup();
  renderPanel(api, <Steering />);
  await screen.findByLabelText("Progettazione", { selector: "textarea" });
  await user.click(screen.getByRole("tab", { name: "Conduzione e aiuto" }));
  await user.clear(screen.getByLabelText("Conduzione e aiuto", { selector: "textarea" }));
  await user.paste("Aiuto solo su richiesta.");
  await user.click(screen.getByRole("tab", { name: "Verifica e conclusione" }));
  await user.clear(screen.getByLabelText("Verifica e conclusione", { selector: "textarea" }));
  await user.paste("Spiega il primo errore.");
  await user.click(screen.getByRole("tab", { name: "Conduzione e aiuto" }));
  expect(screen.getByLabelText("Conduzione e aiuto", { selector: "textarea" }))
    .toHaveValue("Aiuto solo su richiesta.");
  await user.click(screen.getByRole("button", { name: "Salva indicazioni" }));
  expect(api.recorded.steering[0]).toEqual({ revision: 0, action: "save",
    conduct: "Aiuto solo su richiesta.", review: "Spiega il primo errore." });
  await user.click(screen.getByRole("button", { name: "Ripristina questo prompt" }));
  await user.click(screen.getByRole("button", { name: "Conferma" }));
  await waitFor(() => expect(api.recorded.steering[1]?.action).toBe("restore_conduct"));
  expect(await api.steering()).toMatchObject({ instructions: initial.instructions,
    conduct: initial.conduct, review: "Spiega il primo errore.", adaptive: initial.adaptive });
});