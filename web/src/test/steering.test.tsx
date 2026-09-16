import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, expect, it, vi } from "vitest";

import { Steering } from "@/sections/Steering";
import { Experiences } from "@/sections/Experiences";
import { fakeApi } from "@/test/fakeApi";
import { renderPanel } from "@/test/render";

beforeEach(() => window.localStorage.clear());

it("shows both texts and saves only the field deliberately edited", async () => {
  const api = fakeApi();
  const user = userEvent.setup();
  renderPanel(api, <Steering />);
  const field = await screen.findByLabelText("Le tue indicazioni");
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
  await screen.findByLabelText("Le tue indicazioni");
  await user.click(screen.getByRole("button", { name: "Azzera sintesi e feedback" }));
  expect(api.recorded.steering).toEqual([]);
  await user.click(screen.getByRole("button", { name: "Conferma" }));
  await waitFor(() => expect(api.recorded.steering[0]?.action).toBe("reset_adaptive"));
  expect(screen.getByLabelText("Le tue indicazioni")).toHaveValue(
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
  await user.type(await screen.findByLabelText("Le tue indicazioni"), " Usa due indizi.");
  await user.click(screen.getByRole("button", { name: "Salva indicazioni" }));
  expect(await screen.findByText(/Le indicazioni salvate sono cambiate/)).toBeInTheDocument();
  await user.click(screen.getByRole("button", { name: "Aggiorna" }));
  await waitFor(() => expect(screen.getByLabelText("Indicazioni dai feedback"))
    .toHaveValue(current.adaptive));
  expect(screen.getByLabelText("Le tue indicazioni")).toHaveValue(
    original.instructions + " Usa due indizi.");
  await user.click(screen.getByRole("button", { name: "Salva indicazioni" }));
  expect(api.saveSteering).toHaveBeenLastCalledWith({ revision: 1, action: "save",
    instructions: original.instructions + " Usa due indizi." });
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