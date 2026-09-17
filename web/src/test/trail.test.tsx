/* The record of what the system wrote.
 *
 * Two things are held here. A card carries nothing but a title, a date and the idea — the
 * script arrives when the parent opens one, and until then the page has not paid for it.
 */
import { fireEvent, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { fakeApi } from "@/test/fakeApi";
import { TheTrail } from "@/sections/Trail";
import { renderPanel } from "@/test/render";

describe("what the system wrote", () => {
  const currentRun = {
    runId: "aft_1", title: "Un pomeriggio di nuvole", beganAt: 100, endsAt: 2000,
    momentId: "clouds", heading: "Il passo attuale", phase: "waiting" as const, waitingSince: 120,
  };

  it("terminates only the selected activity after confirmation", async () => {
    const user = userEvent.setup();
    const api = fakeApi({ currentTrail: async () => ({ updatedAt: Date.now() / 1000, runs: [currentRun] }) });
    const say = vi.spyOn(api, "say");
    renderPanel(api, <TheTrail />);
    await user.click(await screen.findByRole("button", { name: "Termina attività" }));
    expect(say).not.toHaveBeenCalled();
    await user.click(screen.getByRole("button", { name: "Annulla" }));
    expect(say).not.toHaveBeenCalled();
    await user.click(screen.getByRole("button", { name: "Termina attività" }));
    await user.click(screen.getByRole("button", { name: "Conferma terminazione" }));
    expect(say).toHaveBeenCalledWith({ says: "terminate", runId: "aft_1" });
    expect(await screen.findByText("Terminazione richiesta. In attesa dell'hub.")).toBeVisible();
    expect(screen.getByText(currentRun.heading)).toBeVisible();
  });

  it("does not report a received photo as an unanswered wait", async () => {
    renderPanel(fakeApi({ currentTrail: async () => ({ updatedAt: Date.now() / 1000,
      runs: [{ ...currentRun, phase: "received", receivedAt: 140 }],
    }) }), <TheTrail />);
    expect(await screen.findByText("Foto ricevuta; questo passo è ancora aperto")).toBeVisible();
    expect(screen.queryByText("In attesa di una risposta, non ancora ricevuta")).not.toBeInTheDocument();
  });

  it("keeps a queued termination visible after reload while the hub is offline", async () => {
    renderPanel(fakeApi({ currentTrail: async () => ({ updatedAt: 100, runs: [currentRun] }),
      messages: async () => [{ id: "say_one", says: "terminate", runId: "aft_1", writtenAt: 101, minutes: 0 }],
    }), <TheTrail />);
    expect(await screen.findByText("Terminazione richiesta. In attesa dell'hub.")).toBeVisible();
    expect(screen.queryByRole("button", { name: "Termina attività" })).not.toBeInTheDocument();
  });

  it.each([false, true])("keeps technical documents apart and closed (current: %s)", async (current) => {
    const user = userEvent.setup();
    const whole = await fakeApi().trail("aft_1");
    const prototype = whole.made![0]!;
    renderPanel(fakeApi({
      currentTrail: async () => ({ updatedAt: Date.now() / 1000, runs: current ? [currentRun] : [] }),
      trail: async () => ({ ...whole, made: [
        ...whole.made!,
        { ...prototype, id: "plan", kind: "plan", body: '[{"act":"collect"}]', why: "" },
        { ...prototype, id: "judged", kind: "judged", body: '{"findings":[]}', why: "" },
      ] }),
    }), <TheTrail />);
    if (!current) await user.click(await screen.findByRole("button", { name: "Apri" }));
    const summary = await screen.findByText("Dettagli tecnici: piano, prompt e valutazioni");
    expect(summary.closest("details")).not.toHaveAttribute("open");
    expect(screen.getByText('[{"act":"collect"}]')).not.toBeVisible();
    expect(screen.getByText('{"findings":[]}')).not.toBeVisible();
    expect(screen.getByText(/Ultima pagina stampata:/)).toBeVisible();
    expect(screen.getByText("Guarda fuori e dimmi che forma ha.")).toBeVisible();
    await user.click(summary);
    expect(screen.getByText('[{"act":"collect"}]')).toBeVisible();
    expect(screen.getByText('{"findings":[]}')).toBeVisible();
    expect(screen.getByText(/Non attestano azioni svolte/)).toBeVisible();
    expect(screen.getAllByText(/Archiviato nel registro:/)).toHaveLength(5);
    expect(summary.closest("details")!.querySelector("details")).toBeNull();
    expect(summary.closest("details")!.querySelector("img")).toBeNull();
  });

  it("does not call a drawn page printed or a historical run still waiting", async () => {
    const user = userEvent.setup();
    const whole = await fakeApi().trail("aft_1");
    renderPanel(fakeApi({ trail: async () => ({
      ...whole, made: whole.made!.filter((one) => one.kind === "drawn"),
    }) }), <TheTrail />);
    await user.click(await screen.findByRole("button", { name: "Apri" }));
    expect(await screen.findByText("Non ci sono ancora interazioni registrate.")).toBeVisible();
    const sheets = screen.getByRole("region", { name: "Fogli preparati" });
    expect(await within(sheets).findByRole("img")).toBeVisible();
    expect(sheets.closest("details")).toBeNull();
    expect(screen.queryByText(/Ultima pagina stampata:/)).not.toBeInTheDocument();
    expect(screen.queryByText("In attesa di una risposta, non ancora ricevuta")).not.toBeInTheDocument();
  });

  it("opens the current activity and its steps without a click, then follows its ending", async () => {
    let runs = [currentRun];
    const api = fakeApi({ currentTrail: async () => ({ updatedAt: Date.now() / 1000, runs }) });
    renderPanel(api, <TheTrail />);
    expect(await screen.findByText("Il passo attuale")).toBeInTheDocument();
    expect(await screen.findByText("Guarda fuori e dimmi che forma ha.")).toBeInTheDocument();
    expect(screen.getByText("In attesa di una risposta, non ancora ricevuta")).toBeVisible();
    expect(screen.getByText(/Ultima pagina stampata:/)).toBeVisible();
    expect(screen.getAllByText("Un pomeriggio di nuvole")).toHaveLength(1);
    expect(screen.queryByRole("button", { name: /Cancella dal registro:/ })).not.toBeInTheDocument();
    runs = [];
    fireEvent.focus(window);
    expect(await screen.findByText("Nessuna attività in corso.")).toBeInTheDocument();
    expect(await screen.findByRole("button", { name: /Cancella dal registro:/ })).toBeInTheDocument();
  });

  it("refreshes steps of the running activity on focus", async () => {
    const base = fakeApi();
    const whole = await base.trail("aft_1");
    let title = "Primo passo";
    renderPanel(fakeApi({
      currentTrail: async () => ({ updatedAt: Date.now() / 1000, runs: [currentRun] }),
      trail: async () => ({ ...whole, made: [{ ...whole.made![0]!, heading: title }] }),
    }), <TheTrail />);
    const timeline = within(await screen.findByRole("list", { name: "Durante l'attività" }));
    expect(timeline.getByText("Primo passo")).toBeVisible();
    title = "Passo successivo";
    fireEvent.focus(window);
    await waitFor(() => expect(timeline.getByText("Passo successivo")).toBeVisible());
  });

  it("clears displayed steps after bulk deletion without stopping the current status", async () => {
    const user = userEvent.setup();
    const base = fakeApi();
    renderPanel(fakeApi({
      currentTrail: async () => ({ updatedAt: Date.now() / 1000, runs: [currentRun] }),
      trail: base.trail, trails: base.trails, forgetTrail: base.forgetTrail,
    }), <TheTrail />);
    await screen.findByText("Guarda fuori e dimmi che forma ha.");
    await user.click(screen.getByRole("button", { name: "Svuota il registro" }));
    await user.click(screen.getByRole("button", { name: "Premi ancora per cancellare il registro" }));
    await waitFor(() => expect(screen.queryByText("Guarda fuori e dimmi che forma ha.")).not.toBeInTheDocument());
    expect(screen.getByText("Il passo attuale")).toBeInTheDocument();
  });

  it("labels an old snapshot and keeps its record deletable", async () => {
    renderPanel(fakeApi({ currentTrail: async () => ({ updatedAt: 100, runs: [currentRun] }) }), <TheTrail />);
    expect(await screen.findByText(/non aggiorna lo stato/)).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Ultimo stato noto" })).toBeInTheDocument();
    expect(screen.queryByText("Nessuna attività in corso.")).not.toBeInTheDocument();
    expect(await screen.findByRole("button", { name: /Cancella dal registro:/ })).toBeInTheDocument();
  });

  it("does not call a missing snapshot idle", async () => {
    renderPanel(fakeApi({ currentTrail: async () => ({ updatedAt: 0, runs: [] }) }), <TheTrail />);
    expect(await screen.findByRole("button", { name: /Cancella dal registro:/ })).toBeInTheDocument();
    expect(screen.queryByText("Nessuna attività in corso.")).not.toBeInTheDocument();
  });

  it("keeps the other history cards unchanged after a single deletion", async () => {
    const user = userEvent.setup();
    const [first] = await fakeApi().trails();
    const second = { ...first!, runId: "aft_2", title: "Seconda attività" };
    let records = [first!, second];
    const remove = vi.fn(async (runId: string) => {
      records = records.filter((run) => run.runId !== runId);
      return { forgotten: 1 };
    });
    renderPanel(fakeApi({ trails: async () => records, forgetRun: remove }), <TheTrail />);
    await user.click(await screen.findByRole("button", { name: /Cancella dal registro: Un pomeriggio/ }));
    await user.click(screen.getByRole("button", { name: "Cancella questa attività" }));
    await waitFor(() => expect(screen.queryByText("Un pomeriggio di nuvole")).not.toBeInTheDocument());
    expect(screen.getByText("Seconda attività")).toBeInTheDocument();
    expect(records).toEqual([second]);
    expect(remove).toHaveBeenCalledExactlyOnceWith("aft_1");
  });

  it("deletes just the selected run after confirmation, and can cancel", async () => {
    const user = userEvent.setup();
    const base = fakeApi();
    const remove = vi.fn(base.forgetRun);
    const clear = vi.fn(base.forgetTrail);
    renderPanel(fakeApi({ trails: base.trails, forgetRun: remove, forgetTrail: clear }), <TheTrail />);
    const button = await screen.findByRole("button", { name: /Cancella dal registro:/ });
    await user.click(button);
    expect(remove).not.toHaveBeenCalled();
    await user.click(screen.getByRole("button", { name: "Annulla" }));
    expect(remove).not.toHaveBeenCalled();
    await user.click(button);
    await user.click(screen.getByRole("button", { name: "Cancella questa attività" }));
    expect(await screen.findByText("Nessuna attività ancora.")).toBeInTheDocument();
    expect(remove).toHaveBeenCalledExactlyOnceWith("aft_1");
    expect(clear).not.toHaveBeenCalled();
  });

  it("keeps the run visible if deletion fails", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi({ forgetRun: async () => { throw new Error("offline"); } }), <TheTrail />);
    await user.click(await screen.findByRole("button", { name: /Cancella dal registro:/ }));
    await user.click(screen.getByRole("button", { name: "Cancella questa attività" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("non è stata cancellata");
    expect(screen.getByText("Un pomeriggio di nuvole")).toBeInTheDocument();
  });

  it("shows a card per afternoon, without its script", async () => {
    renderPanel(fakeApi(), <TheTrail />);

    expect(await screen.findByText("Un pomeriggio di nuvole")).toBeInTheDocument();
    expect(screen.getByText(/Si guarda il cielo/)).toBeInTheDocument();
    expect(screen.queryByText(/THE WORLD/)).not.toBeInTheDocument();
  });

  it("shows what Lanternina delivered and keeps internal reasoning closed", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi(), <TheTrail />);

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Apri" }));

    expect(await screen.findByText(/THE WORLD/)).not.toBeVisible();
    expect(screen.getByText("Guarda fuori e dimmi che forma ha.")).toBeVisible();
    expect(screen.getByText("Lanternina ha mostrato sul display")).toBeVisible();
    expect(screen.getByText("Lanternina ha stampato un foglio")).toBeVisible();
    expect(screen.getByText("Prendi il foglio dal tavolo.")).toBeVisible();
    expect(screen.getByText(/Guarda il cielo e disegna quello che vedi/)).toBeVisible();
    expect(screen.queryByText("Che cosa ne e uscito")).not.toBeInTheDocument();
    expect(screen.getByText("Nota tecnica di Lanternina: il foglio era tornato vuoto")).not.toBeVisible();
    expect(screen.queryByText("Dettagli tecnici del passaggio")).not.toBeInTheDocument();
    await user.click(screen.getByText("Dettagli tecnici: piano, prompt e valutazioni"));
    expect(screen.getByText("Nota tecnica di Lanternina: il foglio era tornato vuoto")).toBeVisible();
  });

  it("keeps the steps in the order they happened", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi(), <TheTrail />);

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Apri" }));
    await screen.findByText("Lanternina ha mostrato sul display");

    const steps = within(screen.getByRole("list", { name: "Durante l'attività" }))
      .getAllByRole("listitem").map((one) => one.textContent ?? "");
    const said = steps.findIndex((one) => one.includes("Lanternina ha mostrato sul display"));
    const printed = steps.findIndex((one) => one.includes("Lanternina ha stampato un foglio"));

    expect(said).toBeGreaterThanOrEqual(0);
    expect(printed).toBeGreaterThan(said);
    expect(steps).toHaveLength(2);
    expect(steps.some(one => one.includes("Foglio disegnato"))).toBe(false);
  });

  it("says so plainly when nothing has run", async () => {
    renderPanel(fakeApi({ trails: async () => [] }), <TheTrail />);

    expect(await screen.findByText("Nessuna attività ancora.")).toBeInTheDocument();
  });

  it("shows the sheet a model wrote, and not the document it arrived as", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi(), <TheTrail />);

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Apri" }));

    expect(
      await screen.findByText(/Guarda il cielo e disegna quello che vedi/),
    ).toBeInTheDocument();
    expect(screen.queryByText(/^\{/)).not.toBeInTheDocument();
  });

  it("distinguishes Lanternina's reading from the adolescent's response", async () => {
    const user = userEvent.setup();
    const api = fakeApi();
    const whole = await api.trail("aft_1");
    renderPanel(
      fakeApi({
        trail: async () => ({
          ...whole,
          made: [
            {
              id: "made_3",
              at: 0,
              kind: "came",
              heading: "l-ultimo-foglio",
              body: "un cavallo nel terzo riquadro",
              why: "marks",
              pictureId: "",
              asked: "",
              paper: "",
              until: 2_000_000_000,
            },
          ],
        }),
      }),
      <TheTrail />,
    );

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Apri" }));

    expect(await screen.findByText("Lanternina ha letto il materiale restituito")).toBeVisible();
    expect(screen.getByText("un cavallo nel terzo riquadro")).not.toBeVisible();
    expect(screen.getByText(/si cancella da sola/)).not.toBeVisible();
    await user.click(screen.getByText("Dettagli tecnici: piano, prompt e valutazioni"));
    expect(screen.getByText("Lettura automatica di Lanternina")).toBeVisible();
    expect(screen.getByText("un cavallo nel terzo riquadro")).toBeVisible();
    expect(screen.queryByText("Lanternina ha ricevuto una risposta")).not.toBeInTheDocument();
  });

  it("puts a sheet that never arrived in the trace, with its reason", async () => {
    /* The 5 September 2026 defect, on the side a parent reads. The queue accepted two pages
       and the printer was on another network; the afternoon carried on and the record showed
       one that had gone as written. */
    const user = userEvent.setup();
    const api = fakeApi();
    const whole = await api.trail("aft_1");
    renderPanel(
      fakeApi({
        trail: async () => ({
          ...whole,
          made: [
            {
              id: "made_9",
              at: 0,
              kind: "fault",
              heading: "il-foglio-del-cielo",
              body: "no page reached the table\nthe printer did not take the page within 120 seconds",
              why: "standard",
              pictureId: "",
              asked: "",
              paper: "",
              until: 0,
            },
          ],
        }),
      }),
      <TheTrail />,
    );

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Apri" }));

    expect(await screen.findByText("Lanternina ha incontrato un problema")).toBeVisible();
    expect(screen.queryByText(/Ultima pagina stampata:/)).not.toBeInTheDocument();
    expect(screen.getByText(/did not take the page/)).toBeVisible();
  });

  it("has no readings section of its own any more", async () => {
    /* It was a second list under the trace, and a reading is one of the things the model
       did: it belongs in the trace, at the moment it happened, like everything else. */
    renderPanel(fakeApi(), <TheTrail />);

    await screen.findByText("Un pomeriggio di nuvole");
    expect(screen.queryByText("Riletture")).not.toBeInTheDocument();
  });

  it("names the model as the prompt recipient inside the technical drill-down", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi(), <TheTrail />);

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Apri" }));

    expect(await screen.findByText(/Letter this large/)).not.toBeVisible();
    expect(screen.queryByText("Che cosa e stato chiesto")).not.toBeInTheDocument();
    await user.click(screen.getByText("Dettagli tecnici: piano, prompt e valutazioni"));
    const prompt = screen.getByText("Prompt inviato al modello");
    expect(prompt).toBeVisible();
    expect(screen.getByText(/Letter this large/)).toBeVisible();
  });

  it("does not offer empty technical details or hide a picture-only sheet", async () => {
    const user = userEvent.setup();
    const whole = await fakeApi().trail("aft_1");
    const prototype = whole.made![0]!;
    renderPanel(fakeApi({ trail: async () => ({ ...whole, script: " \n ", made: [
      { ...prototype, why: " \n ", asked: " \t " },
      { ...prototype, id: "empty-plan", kind: "plan", body: " \n ", why: "", heading: "Empty plan" },
      { ...prototype, id: "empty-unknown", kind: "unknown", body: "", why: "", heading: "Empty diagnostic" },
      { ...prototype, id: "picture-only", kind: "drawn", body: "", why: "", pictureId: "pic_7" },
    ] }) }), <TheTrail />);
    await user.click(await screen.findByRole("button", { name: "Apri" }));
    expect(await screen.findByText("Guarda fuori e dimmi che forma ha.")).toBeVisible();
    expect(await screen.findByRole("img")).toBeVisible();
    expect(screen.queryByText("Dettagli tecnici: piano, prompt e valutazioni")).not.toBeInTheDocument();
    expect(screen.queryByText("Empty plan")).not.toBeInTheDocument();
    expect(screen.queryByText("Empty diagnostic")).not.toBeInTheDocument();
    expect(screen.queryByText(/Ultima pagina stampata:/)).not.toBeInTheDocument();
  });

  it("empties the record, and asks twice before it does", async () => {
    /* One press cannot delete a record. The second is not a dialog: the button itself says
       what it is about to do, which is the sentence a parent needs before pressing again. */
    const user = userEvent.setup();
    renderPanel(fakeApi(), <TheTrail />);

    await screen.findByText("Un pomeriggio di nuvole");
    await user.click(screen.getByRole("button", { name: "Svuota il registro" }));

    // Still there: the first press only changed what the button says.
    expect(screen.getByText("Un pomeriggio di nuvole")).toBeInTheDocument();
    await user.click(await screen.findByRole("button", { name: /Premi ancora/ }));

    expect(await screen.findByText(/Buttate 1 righe/)).toBeInTheDocument();
    expect(await screen.findByText("Nessuna attività ancora.")).toBeInTheDocument();
  });
});
