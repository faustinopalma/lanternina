/* The afternoon path, from the offered document to the recorded decision.
 *
 * Three things are held here, and none of them is that a button works. The parent can read
 * every step before deciding, so the overview is not the only thing that exists. Deciding
 * records a decision and nothing else. And there is nothing on this page that asks for an
 * afternoon to be devised — the house asks, and a control here that did would be the one
 * thing an inert panel forbids.
 */
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it } from "vitest";

import { fakeApi, SAMPLE_AFTERNOON } from "@/test/fakeApi";
import { Experiences } from "@/sections/Experiences";
import { renderPanel } from "@/test/render";

describe("an afternoon offered to the parent", () => {
  beforeEach(() => window.localStorage.clear());

  it("says enough to decide on without opening anything", async () => {
    renderPanel(fakeApi(), <Experiences />);

    expect(await screen.findByText("Sei passaggi di una trasformazione")).toBeInTheDocument();
    expect(screen.getByText(/Un oggetto della stanza/)).toBeInTheDocument();
    // The parent judges an idea. How long, how much paper and whether the scanner is
    // wanted are what they decide on; the steps are behind a button they need not press.
    const summary = screen.getByText(/Circa 90 minuti/);
    expect(summary.textContent).toMatch(/fogli stampati/);
    expect(summary.textContent).toMatch(/chiede lo scanner/);
  });

  it("opens every step, including the branch that is not written yet", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi(), <Experiences />);

    await screen.findByText("Sei passaggi di una trasformazione");
    // Nothing of the plan is on the page until it is asked for.
    expect(screen.queryByText("Sei riquadri")).not.toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Se vuoi vedere com'è fatta" }));

    expect(screen.getByText("Scegli un oggetto")).toBeInTheDocument();
    expect(screen.getByText("Sei riquadri")).toBeInTheDocument();
    // Every word that will be lettered on the paper, because the parent approves once.
    expect(screen.getByText("Disegna lo stesso oggetto sei volte.")).toBeInTheDocument();
    expect(screen.getByText("«primo riquadro» «una parola»")).toBeInTheDocument();
    // The branch the format leaves open reads as a sentence, not as the word `ask`.
    expect(
      screen.getByText("Con dei segni → il resto viene scritto in quel momento"),
    ).toBeInTheDocument();
    expect(screen.getByText("Vuoto → basta-cosi")).toBeInTheDocument();
  });

  it("records an approval and takes it off the list of things to decide", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api, <Experiences />);

    await screen.findByText("Sei passaggi di una trasformazione");
    await user.click(screen.getByRole("button", { name: "Approva" }));

    await waitFor(() => expect(screen.getByText("Nessuna attività in attesa.")).toBeInTheDocument());
    expect(api.recorded.experienceDecisions).toEqual([{ id: "aftn-1", state: "approved" }]);
    // Approving is the whole effect: no proposal was decided, nothing else was called.
    expect(api.recorded.decisions).toEqual([]);
  });

  it("records a refusal the same way", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api, <Experiences />);

    await screen.findByText("Sei passaggi di una trasformazione");
    await user.click(screen.getByRole("button", { name: "Rifiuta" }));

    await waitFor(() => expect(api.recorded.experienceDecisions).toHaveLength(1));
    expect(api.recorded.experienceDecisions[0]).toEqual({ id: "aftn-1", state: "rejected" });
  });

  it("lets an approved afternoon be withdrawn afterwards", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api, <Experiences />);

    await screen.findByText("Sei passaggi di una trasformazione");
    await user.click(screen.getByRole("button", { name: "Approva" }));

    await user.click(await screen.findByRole("button", { name: "Non più" }));
    await waitFor(() => expect(api.recorded.experienceDecisions).toHaveLength(2));
    expect(api.recorded.experienceDecisions[1]).toEqual({ id: "aftn-1", state: "withdrawn" });
  });

  it("says so and leaves the afternoon there when the decision does not get through", async () => {
    const api = fakeApi({ decideExperience: () => Promise.reject(new Error("no")) });
    const user = userEvent.setup();
    renderPanel(api, <Experiences />);

    await screen.findByText("Sei passaggi di una trasformazione");
    await user.click(screen.getByRole("button", { name: "Approva" }));

    expect(
      await screen.findByText("Non sono riuscito a registrare la decisione. Riprova più tardi."),
    ).toBeInTheDocument();
    expect(screen.getByText("Sei passaggi di una trasformazione")).toBeInTheDocument();
  });

  it("offers no way to ask for one, which is the rule rather than an omission", async () => {
    renderPanel(fakeApi(), <Experiences />);

    await screen.findByText("Sei passaggi di una trasformazione");
    const buttons = screen.getAllByRole("button").map((one) => one.textContent);
    expect(buttons).toEqual(
      expect.arrayContaining(["Approva", "Rifiuta", "Se vuoi vedere com'è fatta"]),
    );
    expect(buttons.filter((name) => /nuovo|chiedi|inventa|genera/i.test(name ?? ""))).toEqual([]);
  });
});

/* The one thing that reaches an afternoon already running. What is held here is what the
 * control is not: there is no box to type a sentence in, and neither button stops
 * anything. Both write a row and leave the house to come for it. */
describe("an afternoon the house has begun", () => {
  const begun = { ...SAMPLE_AFTERNOON, state: "approved", begunAt: 1_755_500_000 };
  const running = () =>
    fakeApi({ experiences: async (state) => (state === "approved" ? [begun] : []) });

  beforeEach(() => window.localStorage.clear());

  it("offers an hour and nothing to write in", async () => {
    renderPanel(running(), <Experiences />);

    expect(await screen.findByLabelText("Finisce entro")).toHaveAttribute("type", "time");
    expect(screen.getByRole("button", { name: "Sposta l'ora" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Falla finire adesso" })).toBeInTheDocument();
    // `shared/message.py`: the defence against free text is having nowhere to put it.
    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
    // Nor is there a way to take it back once the house has it.
    expect(screen.queryByRole("button", { name: "Non più" })).not.toBeInTheDocument();
  });

  it("records the hour the parent chose and nothing else", async () => {
    const api = running();
    const user = userEvent.setup();
    renderPanel(api, <Experiences />);

    await user.type(await screen.findByLabelText("Finisce entro"), "17:30");
    await user.click(screen.getByRole("button", { name: "Sposta l'ora" }));

    await waitFor(() => expect(api.recorded.said).toEqual([{ says: "end_by", at: "17:30" }]));
    expect(api.recorded.experienceDecisions).toEqual([]);
    expect(
      await screen.findByText(
        "Scritto. La casa lo trova alla prossima richiesta, entro un minuto.",
      ),
    ).toBeInTheDocument();
  });

  it("brings the ending forward with one press and no hour", async () => {
    const api = running();
    const user = userEvent.setup();
    renderPanel(api, <Experiences />);

    await user.click(await screen.findByRole("button", { name: "Falla finire adesso" }));

    await waitFor(() => expect(api.recorded.said).toEqual([{ says: "close_now" }]));
  });

  it("says so and keeps the hour when it does not get through", async () => {
    const api = fakeApi({
      experiences: async (state) => (state === "approved" ? [begun] : []),
      say: () => Promise.reject(new Error("no")),
    });
    const user = userEvent.setup();
    renderPanel(api, <Experiences />);

    await user.click(await screen.findByRole("button", { name: "Falla finire adesso" }));

    expect(
      await screen.findByText("Non sono riuscito a registrarlo. Riprova più tardi."),
    ).toBeInTheDocument();
  });
});
