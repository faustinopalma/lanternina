/* The afternoon path, from the offered document to the recorded decision.
 *
 * Three things are held here, and none of them is that a button works. The parent can read
 * every step before deciding, so the overview is not the only thing that exists. Deciding
 * records a decision and nothing else. And there is nothing on this page that asks for an
 * afternoon to be devised — the house asks, and a control here that did would be the one
 * thing an inert panel forbids.
 */
import { screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it } from "vitest";

import { fakeApi } from "@/test/fakeApi";
import { renderPanel } from "@/test/render";

async function openAfternoons(user: ReturnType<typeof userEvent.setup>) {
  await user.click(
    within(screen.getByRole("navigation")).getByRole("button", { name: "Pomeriggi" }),
  );
}

describe("an afternoon offered to the parent", () => {
  beforeEach(() => window.localStorage.clear());

  it("shows the overview and its length before anything is decided", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());
    await openAfternoons(user);

    expect(await screen.findByText("Sei passaggi di una trasformazione")).toBeInTheDocument();
    expect(screen.getByText(/Un oggetto della stanza/)).toBeInTheDocument();
    expect(screen.getByText("Circa 90 minuti.")).toBeInTheDocument();
  });

  it("opens every step, including the branch that is not written yet", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());
    await openAfternoons(user);

    await screen.findByText("Sei passaggi di una trasformazione");
    // Nothing of the plan is on the page until it is asked for.
    expect(screen.queryByText("Sei riquadri")).not.toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Leggi ogni passaggio" }));

    expect(screen.getByText("Scegli un oggetto")).toBeInTheDocument();
    expect(screen.getByText("Sei riquadri")).toBeInTheDocument();
    expect(screen.getByText("«Comincia da come è adesso.» «primo riquadro» «una parola»"))
      .toBeInTheDocument();
    // The branch the format leaves open reads as a sentence, not as the word `ask`.
    expect(
      screen.getByText("Con dei segni → il resto viene scritto in quel momento"),
    ).toBeInTheDocument();
    expect(screen.getByText("Vuoto → basta-cosi")).toBeInTheDocument();
  });

  it("records an approval and takes it off the list of things to decide", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);
    await openAfternoons(user);

    await screen.findByText("Sei passaggi di una trasformazione");
    await user.click(screen.getByRole("button", { name: "Approva" }));

    await waitFor(() => expect(screen.getByText("Nessun pomeriggio in attesa.")).toBeInTheDocument());
    expect(api.recorded.experienceDecisions).toEqual([{ id: "aftn-1", state: "approved" }]);
    // Approving is the whole effect: no proposal was decided, nothing else was called.
    expect(api.recorded.decisions).toEqual([]);
  });

  it("records a refusal the same way", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);
    await openAfternoons(user);

    await screen.findByText("Sei passaggi di una trasformazione");
    await user.click(screen.getByRole("button", { name: "Rifiuta" }));

    await waitFor(() => expect(api.recorded.experienceDecisions).toHaveLength(1));
    expect(api.recorded.experienceDecisions[0]).toEqual({ id: "aftn-1", state: "rejected" });
  });

  it("lets an approved afternoon be withdrawn afterwards", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);
    await openAfternoons(user);

    await screen.findByText("Sei passaggi di una trasformazione");
    await user.click(screen.getByRole("button", { name: "Approva" }));

    await user.click(await screen.findByRole("button", { name: "Non più" }));
    await waitFor(() => expect(api.recorded.experienceDecisions).toHaveLength(2));
    expect(api.recorded.experienceDecisions[1]).toEqual({ id: "aftn-1", state: "withdrawn" });
  });

  it("says so and leaves the afternoon there when the decision does not get through", async () => {
    const api = fakeApi({ decideExperience: () => Promise.reject(new Error("no")) });
    const user = userEvent.setup();
    renderPanel(api);
    await openAfternoons(user);

    await screen.findByText("Sei passaggi di una trasformazione");
    await user.click(screen.getByRole("button", { name: "Approva" }));

    expect(
      await screen.findByText("Non sono riuscito a registrare la decisione. Riprova più tardi."),
    ).toBeInTheDocument();
    expect(screen.getByText("Sei passaggi di una trasformazione")).toBeInTheDocument();
  });

  it("offers no way to ask for one, which is the rule rather than an omission", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());
    await openAfternoons(user);

    await screen.findByText("Sei passaggi di una trasformazione");
    const buttons = screen.getAllByRole("button").map((one) => one.textContent);
    expect(buttons).toEqual(
      expect.arrayContaining(["Approva", "Rifiuta", "Leggi ogni passaggio"]),
    );
    expect(buttons.filter((name) => /nuovo|chiedi|inventa|genera/i.test(name ?? ""))).toEqual([]);
  });
});
