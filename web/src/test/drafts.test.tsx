/* A parent working on an idea of their own.
 *
 * What is held here is the shape of the trade. The conversation and the text are the same
 * draft seen twice, so a rewrite has to move both. Typing is the parent's own and must not
 * cost a call. And approving is not a decision about somebody else's idea — it is the end
 * of their own work, so a refusal has to come back with its reason.
 */
import { screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { fakeApi } from "@/test/fakeApi";
import { Drafts } from "@/sections/Drafts";
import { renderPanel } from "@/test/render";

async function openBlank(user: ReturnType<typeof userEvent.setup>) {
  await user.click(await screen.findByRole("button", { name: "Comincia da una pagina bianca" }));
}

describe("an idea the parent is writing", () => {
  it("opens a blank page without asking a model anything", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api, <Drafts />);

    await openBlank(user);

    expect(await screen.findByLabelText("Il copione")).toHaveValue("");
    // Opening one is inert. The first message is what spends anything.
    expect(api.recorded.saidToDraft).toEqual([]);
  });

  it("says why the first answer is slow rather than showing a spinner", async () => {
    /* The container that answers has scaled to zero and is starting. A spinner would not
       explain that, and a parent who is not told assumes it is broken. The fake here never
       answers, which is the only way to look at the pane while it is waiting. */
    const api = fakeApi({ sayToDraft: () => new Promise(() => {}) });
    const user = userEvent.setup();
    renderPanel(api, <Drafts />);
    await openBlank(user);

    await user.type(await screen.findByLabelText("Dì che cosa cambiare"), "qualcosa sul pane");
    await user.click(screen.getByRole("button", { name: "Manda" }));

    expect(await screen.findByText(/La prima risposta è lenta/)).toBeInTheDocument();
    // And nothing can be sent twice while it is waiting.
    expect(screen.getByRole("button", { name: "Manda" })).toBeDisabled();
  });

  it("moves both panes when a turn comes back", async () => {
    /* The conversation and the text are the same draft seen twice. A rewrite that showed
       up in only one of them would leave the parent editing something stale. */
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api, <Drafts />);
    await openBlank(user);

    await user.type(await screen.findByLabelText("Dì che cosa cambiare"), "spostala in cucina");
    await user.click(screen.getByRole("button", { name: "Manda" }));

    expect(await screen.findByText("spostala in cucina")).toBeInTheDocument();
    expect(await screen.findByText("Ho spostato il finale.")).toBeInTheDocument();
    await waitFor(() =>
      expect(screen.getByLabelText("Titolo")).toHaveValue("Le ventitré tacche del pensile"),
    );
  });

  it("lets the parent type in the text, and does not pay a model for it", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api, <Drafts />);
    await openBlank(user);

    const script = await screen.findByLabelText("Il copione");
    await user.type(script, "THE WORLD");
    await user.click(screen.getByRole("button", { name: "Tieni quello che hai scritto" }));

    await waitFor(() => expect(api.recorded.typedIntoDraft).toHaveLength(1));
    expect(api.recorded.typedIntoDraft[0]!.text.script).toBe("THE WORLD");
    expect(api.recorded.saidToDraft).toEqual([]);
  });

  it("keeps the keep button grey until the text and the draft differ", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api, <Drafts />);
    await openBlank(user);

    await screen.findByLabelText("Il copione");
    expect(screen.getByRole("button", { name: "Tieni quello che hai scritto" })).toBeDisabled();
  });

  it("will not approve a draft with nothing in it", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi(), <Drafts />);
    await openBlank(user);

    await screen.findByLabelText("Il copione");
    expect(
      screen.getByRole("button", { name: "Approva e prepara l'attività" }),
    ).toBeDisabled();
  });

  it("approves a finished one and leaves the page", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api, <Drafts />);
    await openBlank(user);

    await user.type(await screen.findByLabelText("Il copione"), "THE WORLD");
    await user.click(screen.getByRole("button", { name: "Tieni quello che hai scritto" }));
    await waitFor(() => expect(api.recorded.typedIntoDraft).toHaveLength(1));
    await user.click(screen.getByRole("button", { name: "Approva e prepara l'attività" }));

    await waitFor(() => expect(api.recorded.approvedDrafts).toHaveLength(1));
    expect(
      await screen.findByRole("button", { name: "Comincia da una pagina bianca" }),
    ).toBeInTheDocument();
  });

  it("says what the checks refused, because the parent can change the text", async () => {
    const api = fakeApi({
      approveDraft: () => Promise.reject(new Error("un traguardo che conta punti")),
    });
    const user = userEvent.setup();
    renderPanel(api, <Drafts />);
    await openBlank(user);

    await user.type(await screen.findByLabelText("Il copione"), "punteggio");
    await user.click(screen.getByRole("button", { name: "Tieni quello che hai scritto" }));
    await user.click(screen.getByRole("button", { name: "Approva e prepara l'attività" }));

    expect(await screen.findByText(/un traguardo che conta punti/)).toBeInTheDocument();
    // Still here, with the text still open.
    expect(screen.getByLabelText("Il copione")).toBeInTheDocument();
  });

  it("closes one without approving it", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi(), <Drafts />);
    await openBlank(user);

    await screen.findByLabelText("Il copione");
    await user.click(screen.getByRole("button", { name: "Chiudi senza approvare" }));

    expect(
      await screen.findByRole("button", { name: "Comincia da una pagina bianca" }),
    ).toBeInTheDocument();
  });

  it("says plainly that approving runs the same checks as everything else", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi(), <Drafts />);
    await openBlank(user);

    const note = await screen.findByText(/Passa dagli stessi controlli/);
    expect(within(note).getByText(/puoi correggere il testo e riprovare/)).toBeDefined();
  });
});
