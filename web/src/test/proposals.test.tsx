/* The approval path, from the list to the recorded decision.
 *
 * The point being held here is not that a button works. It is that approving does exactly
 * one thing — it records a decision — and that the parent can see what they are deciding
 * about before they decide.
 */
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it } from "vitest";

import type { Proposal } from "@/api/types";
import { fakeApi, SAMPLE_PROPOSALS } from "@/test/fakeApi";
import { Proposals } from "@/sections/Proposals";
import { renderPanel } from "@/test/render";

describe("to approve", () => {
  beforeEach(() => window.localStorage.clear());

  it("shows the content of a proposal before asking for a decision", async () => {
    renderPanel(fakeApi(), <Proposals />);

    expect(await screen.findByText("Le stagioni")).toBeInTheDocument();
    expect(screen.getByText("In che stagione cadono le foglie?")).toBeInTheDocument();
    expect(screen.getByText("estate · autunno")).toBeInTheDocument();
    // The reason it was proposed sits with the proposal, not behind a click.
    expect(screen.getByText("Un foglio breve, con quattro domande.")).toBeInTheDocument();
  });

  it("records the decision and takes the proposal off the list", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api, <Proposals />);

    await screen.findByText("Le stagioni");
    await user.click(screen.getAllByRole("button", { name: "Approva" })[0]!);

    await waitFor(() => expect(screen.queryByText("Le stagioni")).not.toBeInTheDocument());
    expect(api.recorded.decisions).toEqual([{ id: "prop-1", state: "approved" }]);
    // The other one is untouched: a decision is about one proposal.
    expect(screen.getByText("Prepara lo zaino per domani.")).toBeInTheDocument();
  });

  it("records a refusal the same way", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api, <Proposals />);

    await screen.findByText("Le stagioni");
    await user.click(screen.getAllByRole("button", { name: "Rifiuta" })[0]!);

    await waitFor(() => expect(api.recorded.decisions).toHaveLength(1));
    expect(api.recorded.decisions[0]).toEqual({ id: "prop-1", state: "rejected" });
  });

  it("disables both buttons while the decision is in flight", async () => {
    let release: (() => void) | null = null;
    const api = fakeApi({
      decide: () =>
        new Promise<void>((resolve) => {
          release = resolve;
        }),
    });
    const user = userEvent.setup();
    renderPanel(api, <Proposals />);

    await screen.findByText("Le stagioni");
    const approve = screen.getAllByRole("button", { name: "Approva" })[0]!;
    const refuse = screen.getAllByRole("button", { name: "Rifiuta" })[0]!;
    await user.click(approve);

    expect(approve).toBeDisabled();
    expect(refuse).toBeDisabled();
    release!();
  });

  it("says so and lets the parent try again when the decision does not get through", async () => {
    const api = fakeApi({
      decide: () => Promise.reject(new Error("no")),
    });
    const user = userEvent.setup();
    renderPanel(api, <Proposals />);

    await screen.findByText("Le stagioni");
    const approve = screen.getAllByRole("button", { name: "Approva" })[0]!;
    await user.click(approve);

    expect(
      await screen.findByText("Non sono riuscito a registrare la decisione. Riprova più tardi."),
    ).toBeInTheDocument();
    expect(approve).toBeEnabled();
    // Still there: nothing was decided, so nothing leaves the list.
    expect(screen.getByText("Le stagioni")).toBeInTheDocument();
  });

  it("says nothing at all rather than taking up the page it no longer owns", async () => {
    // Nothing on the hub submits a proposal, so this is the ordinary state. It shares a
    // page with the activities now, and an empty notice under a full list would read as
    // the panel contradicting itself.
    const { container } = renderPanel(fakeApi({ proposals: async () => [] }), <Proposals />);

    await waitFor(() => expect(container.textContent).not.toContain("Da approvare"));
    expect(screen.queryByText(/proposta/i)).toBeNull();
  });

  it("shows a sheet written before the field names changed", async () => {
    /* Content approved before 18 August 2026 carries Italian keys and cannot be rewritten:
     * the safety seal covers the body byte for byte. It has to read the same here. */
    const stored: Proposal = {
      ...SAMPLE_PROPOSALS[0]!,
      body: JSON.stringify({
        titolo: "Le stagioni",
        istruzioni: "Scegli la parola giusta.",
        esercizi: [
          { domanda: "In che stagione cadono le foglie?", scelte: ["estate", "autunno"] },
        ],
      }),
    };
    renderPanel(fakeApi({ proposals: async () => [stored] }), <Proposals />);

    expect(await screen.findByText("Le stagioni")).toBeInTheDocument();
    expect(screen.getByText("In che stagione cadono le foglie?")).toBeInTheDocument();
    expect(screen.getByText("estate · autunno")).toBeInTheDocument();
  });

  it("stays quiet when the list cannot be read, with no code and no stack", async () => {
    renderPanel(
      fakeApi({ proposals: () => Promise.reject(new Error("boom")) }),
      <Proposals />,
    );

    await waitFor(() => expect(document.body.textContent).not.toContain("boom"));
    expect(screen.queryByRole("button", { name: "Approva" })).toBeNull();
    expect(document.body.textContent).not.toMatch(/HTTP|\b[45]\d\d\b/);
  });
});

describe("what is already approved", () => {
  beforeEach(() => window.localStorage.clear());

  it("says how much is in reserve, as a fact rather than a task", async () => {
    renderPanel(fakeApi(), <Proposals />);

    expect(
      await screen.findByText("Da parte — attività approvate: 2; temi: 2."),
    ).toBeInTheDocument();
    // No exclamation, no instruction, nothing that reads as a chore assigned to anyone.
    expect(document.body.textContent).not.toMatch(/!|Devi |Ricorda di /);
  });

  it("withdraws one, shortens the count, and says what withdrawal cannot reach", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api, <Proposals />);

    await screen.findByText("Da parte — attività approvate: 2; temi: 2.");
    await user.click(screen.getAllByRole("button", { name: "Non più" })[0]!);

    await screen.findByText("Da parte — attività approvate: 1; temi: 2.");
    expect(api.recorded.decisions).toEqual([{ id: "prop-9", state: "withdrawn" }]);
    expect(
      screen.getByText(
        "Ritirata. Non verrà più consegnata. Un foglio già stampato resta in casa: da qui non si può richiamare.",
      ),
    ).toBeInTheDocument();
  });

  it("says so when the withdrawal does not get through, and keeps the item", async () => {
    const api = fakeApi({ decide: () => Promise.reject(new Error("no")) });
    const user = userEvent.setup();
    renderPanel(api, <Proposals />);

    await screen.findByText("Da parte — attività approvate: 2; temi: 2.");
    await user.click(screen.getAllByRole("button", { name: "Non più" })[0]!);

    expect(
      await screen.findByText("Non sono riuscito a registrare il ritiro. Riprova più tardi."),
    ).toBeInTheDocument();
    expect(screen.getByText("Da parte — attività approvate: 2; temi: 2.")).toBeInTheDocument();
  });
});
