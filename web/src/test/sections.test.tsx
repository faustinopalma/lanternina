/* The gallery, the rhythm and the devices — the three sections whose behaviour is not
 * obvious from their markup. */
import { fireEvent, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { fileName } from "@/sections/Pictures";
import { fakeApi } from "@/test/fakeApi";
import { renderPanel } from "@/test/render";

async function open(user: ReturnType<typeof userEvent.setup>, name: string) {
  await user.click(within(screen.getByRole("navigation")).getByRole("button", { name }));
}

describe("the page around the sections", () => {
  beforeEach(() => window.localStorage.clear());

  it("keeps one way out, in the header rather than under the content", () => {
    renderPanel(fakeApi());

    const out = screen.getAllByRole("button", { name: "Esci" });
    expect(out).toHaveLength(1);
    // Before the menu, so it is where a reader looks for it rather than past everything.
    expect(out[0]!.compareDocumentPosition(screen.getByRole("navigation"))).toBe(
      Node.DOCUMENT_POSITION_FOLLOWING,
    );
  });

  it("shows the account as an address, not as a sentence about one", () => {
    renderPanel(fakeApi());
    expect(screen.getByLabelText("Account con cui sei entrato")).toHaveTextContent(
      /^genitore@example\.invalid$/,
    );
  });
});

describe("the gallery", () => {
  beforeEach(() => window.localStorage.clear());

  it("fetches each bitmap itself, because an <img> sends no token", async () => {
    const api = fakeApi();
    const asked = vi.spyOn(api, "pictureContent");
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Quadri");
    await waitFor(() => expect(asked).toHaveBeenCalled());
    const images = await screen.findAllByRole("img");
    expect(images[0]).toHaveAttribute("src", expect.stringContaining("blob:"));
  });

  it("goes back to the first page when the page size changes, and remembers the size", async () => {
    const api = fakeApi();
    const asked = vi.spyOn(api, "pictures");
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Quadri");
    await screen.findByLabelText("Per pagina");

    await user.click(screen.getByRole("button", { name: "Successivi" }));
    await waitFor(() => expect(asked).toHaveBeenLastCalledWith(2, 20));

    await user.selectOptions(screen.getByLabelText("Per pagina"), "50");
    await waitFor(() => expect(asked).toHaveBeenLastCalledWith(1, 50));
    expect(window.localStorage.getItem("lanternina.picturesPerPage")).toBe("50");
  });

  it("asks for a picture back by writing it down, and says the house decides when", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Quadri");
    // Only on the enlarged picture: the grid is for finding one, not for acting on it.
    const tiles = await screen.findAllByRole("button", { name: "Ingrandisci" });
    expect(screen.queryByRole("button", { name: "Rimetti su questo" })).toBeNull();

    await user.click(tiles[0]!);
    const enlarged = await screen.findByRole("dialog");
    const again = within(enlarged).getByRole("button", { name: "Rimetti su questo" });
    await user.click(again);

    await within(enlarged).findByText(
      "Richiesta registrata. La casa lo rimette la prossima volta che cambia il quadro.",
    );
    expect(api.recorded.askedAgain).toEqual(["pic-1"]);
    // Pressing again would only replace the row, so the button stops offering it.
    expect(again).toBeDisabled();
  });

  it("names a saved picture by its moment, and keeps two of the same minute apart", () => {
    const name = fileName({
      id: "pic-1",
      theme: "gatti / cani",
      createdAt: 1_755_500_000,
      kind: "ok",
    });
    expect(name).toMatch(/^\d{4}-\d{2}-\d{2}-\d{4} gatti cani pic-1\.bmp$/);
  });

  it("opens one picture on its own, with a way to keep that one", async () => {
    const api = fakeApi();
    const saved = vi
      .spyOn(HTMLAnchorElement.prototype, "click")
      .mockImplementation(() => undefined);
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Quadri");
    const tiles = await screen.findAllByRole("button", { name: "Ingrandisci" });
    await user.click(tiles[0]!);

    const enlarged = await screen.findByRole("dialog");
    await user.click(within(enlarged).getByRole("button", { name: "Scarica questo" }));
    expect(saved).toHaveBeenCalled();
    saved.mockRestore();
  });

  it("packs into one file every picture from the chosen day on, walking every page", async () => {
    const api = fakeApi();
    const listed = vi.spyOn(api, "pictures");
    const bytes = vi.spyOn(api, "pictureContent");
    const saved = vi
      .spyOn(HTMLAnchorElement.prototype, "click")
      .mockImplementation(() => undefined);
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Quadri");
    // Written rather than left at the default, so the test does not depend on today.
    fireEvent.change(await screen.findByLabelText("Scarica i quadri dal"), {
      target: { value: "2000-01-01" },
    });
    await user.click(screen.getByRole("button", { name: "Scarica" }));

    await waitFor(() => expect(saved).toHaveBeenCalled());
    // Every page, not only the one the parent is standing on, and at the largest step the
    // archive offers rather than a number it would quietly refuse.
    expect(listed.mock.calls).toContainEqual([1, 50]);
    expect(listed.mock.calls).toContainEqual([2, 50]);
    expect(bytes.mock.calls.length).toBeGreaterThanOrEqual(12);
    saved.mockRestore();
  });

  it("stops at the chosen day instead of reading the rest of the archive", async () => {
    const api = fakeApi();
    const listed = vi.spyOn(api, "pictures");
    const saved = vi
      .spyOn(HTMLAnchorElement.prototype, "click")
      .mockImplementation(() => undefined);
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Quadri");
    // Later than every picture in the archive, so the walk ends on the first one it reads.
    fireEvent.change(await screen.findByLabelText("Scarica i quadri dal"), {
      target: { value: "2099-01-01" },
    });
    await user.click(screen.getByRole("button", { name: "Scarica" }));

    await screen.findByText("Nessun quadro da quel giorno in poi.");
    // The first page was read and no other: the listing comes newest first.
    expect(listed.mock.calls.filter(([page]) => page === 2)).toHaveLength(0);
    expect(saved).not.toHaveBeenCalled();
    saved.mockRestore();
  });

  it("shows the request the house has not collected after a reload", async () => {
    const api = fakeApi({
      standingRequest: async () => ({
        id: "ask-1",
        kind: "showAgain",
        subject: "pic-3",
        askedAt: 1_755_500_000,
      }),
    });
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Quadri");
    const tiles = await screen.findAllByRole("button", { name: "Ingrandisci" });

    // Carried by the picture it was asked for, and by no other. Before this moved into
    // the enlarged view it was shown on the grid, where it had to be counted to be sure
    // it appeared once; opening the right picture says the same thing without counting.
    await user.click(tiles[2]!);
    const enlarged = await screen.findByRole("dialog");
    await within(enlarged).findByText(
      "Richiesta registrata. La casa lo rimette la prossima volta che cambia il quadro.",
    );
    expect(within(enlarged).getByRole("button", { name: "Rimetti su questo" })).toBeDisabled();
  });
});

describe("the rhythm", () => {
  beforeEach(() => window.localStorage.clear());

  it("keeps the save button grey until something differs, and greys it again after", async () => {
    /* The confirmation is the button, not a sentence. A parent needs to know two things —
       did it go through, and have I already saved this — and one control answers both
       without anything appearing or asking to be dismissed. */
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Ritmo");
    const cadence = await screen.findByLabelText("Quadro nuovo ogni");
    const save = screen.getByRole("button", { name: "Salva" });
    expect(save).toBeDisabled();

    await user.clear(cadence);
    await user.type(cadence, "90");
    expect(save).toBeEnabled();

    await user.click(save);
    await waitFor(() => expect(api.recorded.rhythm).toHaveLength(1));
    await waitFor(() => expect(save).toBeDisabled());
  });

  it("puts the same value back and asks the house for nothing", async () => {
    /* Typing a value back to what it was leaves the button grey, which is right: there is
       nothing to tell the house. A flag set by each field would have said otherwise. */
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Ritmo");
    const cadence = await screen.findByLabelText("Quadro nuovo ogni");
    await user.clear(cadence);
    await user.type(cadence, "90");
    await user.clear(cadence);
    await user.type(cadence, "60");

    expect(screen.getByRole("button", { name: "Salva" })).toBeDisabled();
    expect(api.recorded.rhythm).toHaveLength(0);
  });

  it("takes the confirmation away as soon as the parent edits again", async () => {
    /* It is about the values that were saved. Left standing over newer ones it says the
       house has something it does not have. */
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Ritmo");
    const cadence = await screen.findByLabelText("Quadro nuovo ogni");
    await user.clear(cadence);
    await user.type(cadence, "90");
    await user.click(screen.getByRole("button", { name: "Salva" }));
    await screen.findByText(/La casa lo applica al prossimo giro/);

    await user.clear(cadence);
    await user.type(cadence, "45");

    expect(screen.queryByText(/La casa lo applica al prossimo giro/)).not.toBeInTheDocument();
  });

  it("saves the hours and the spacing, and says the house applies them later", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Ritmo");
    const cadence = await screen.findByLabelText("Quadro nuovo ogni");
    expect(cadence).toHaveValue(60);

    await user.clear(cadence);
    await user.type(cadence, "90");
    await user.click(screen.getByRole("button", { name: "Salva" }));

    await waitFor(() => expect(api.recorded.rhythm).toHaveLength(1));
    expect(api.recorded.rhythm[0]).toEqual({
      picturesFrom: "07:00",
      picturesUntil: "21:30",
      cadenceMinutes: 90,
      // Sent back untouched: one form saves three sections, and changing the spacing must
      // not quietly clear the days an afternoon may begin on, nor move the house back
      // onto whatever clock the hub's own machine happens to be set to.
      afternoonDays: ["wed", "sat"],
      afternoonFrom: "15:00",
      afternoonUntil: "19:00",
      timeZone: "Europe/Rome",
      scriptsWanted: 10,
    });
    expect(await screen.findByText(/La casa lo applica al prossimo giro/)).toBeInTheDocument();
  });

  it("turns afternoons off by unticking the last day, and saves that", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Ritmo");
    await user.click(await screen.findByLabelText("mer"));
    await user.click(screen.getByLabelText("sab"));
    await user.click(screen.getByRole("button", { name: "Salva" }));

    await waitFor(() => expect(api.recorded.rhythm).toHaveLength(1));
    expect(api.recorded.rhythm[0]!.afternoonDays).toEqual([]);
  });

  it("asks for an afternoon now, and says it was asked rather than started", async () => {
    /* The wording is the test. The panel cannot reach the house, so a button that said
     * "started" would be claiming something it has no way to know. */
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Ritmo");
    await user.click(
      await screen.findByRole("button", { name: "Fai cominciare un'attività adesso" }),
    );

    await waitFor(() => expect(api.recorded.begunNow).toBe(1));
    expect(await screen.findByText(/La casa lo trova al prossimo giro/)).toBeInTheDocument();
    // Pressing must not save the form: the hours are a separate decision.
    expect(api.recorded.rhythm).toHaveLength(0);
  });

  it("says what beginning now does not override", async () => {
    /* The end hour is the part it never steps over, and saying so is the difference
       between a button that looks broken and one whose limit was stated. */
    const user = userEvent.setup();
    renderPanel(fakeApi());
    await open(user, "Ritmo");
    expect(await screen.findByText(/non l'ora di fine/)).toBeInTheDocument();
  });

  it("sets how many ideas the house keeps waiting for a decision", async () => {
    /* It is here and not with the content settings because it never reaches a model: those
       are exactly the fields that may, and this one bounds the parent's own queue. */
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);
    await open(user, "Ritmo");

    const wanted = await screen.findByLabelText("Idee da tenere pronte");
    expect(wanted).toHaveValue(10);
    await user.clear(wanted);
    await user.type(wanted, "4");
    await user.click(screen.getByRole("button", { name: "Salva" }));

    await waitFor(() => expect(api.recorded.rhythm).toHaveLength(1));
    expect(api.recorded.rhythm[0]!.scriptsWanted).toBe(4);
  });

  it("says that zero stops them, so the number is not only a size", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());
    await open(user, "Ritmo");
    expect(await screen.findByText(/Zero le ferma/)).toBeInTheDocument();
  });

  it("keeps the note about the display waking about every ten minutes", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());
    await open(user, "Ritmo");
    expect(await screen.findByText(/circa ogni dieci minuti/)).toBeInTheDocument();
  });
});

describe("the devices", () => {
  beforeEach(() => window.localStorage.clear());

  it("says the charge in words, never as a percentage", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());

    await open(user, "Dispositivi");
    expect(await screen.findByText(/batteria carica/)).toBeInTheDocument();
    expect(screen.getByText(/da ricaricare presto/)).toBeInTheDocument();
    expect(document.body.textContent).not.toMatch(/\d+\s?%/);
  });

  it("shows what each thing calls itself, so a row can be matched to a shelf", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());

    await open(user, "Dispositivi");
    // The display with no name yet is found by the id it puts on its own screen.
    expect(await screen.findByText("FB9F18")).toBeInTheDocument();
    expect(screen.getByText("CF7D04")).toBeInTheDocument();
  });

  it("hands out a job and writes a name, and neither reaches into the house", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Dispositivi");
    const groups = await screen.findAllByRole("group", {
      name: "A cosa serve questo dispositivo",
    });
    await user.click(
      within(groups[1]!).getByRole("checkbox", { name: "mostra le azioni da compiere" }),
    );
    await waitFor(() =>
      expect(api.recorded.assignments).toEqual([
        { id: "E8:3D:C1:FB:9F:18", assignment: { jobs: ["sheet"] } },
      ]),
    );

    const names = screen.getAllByLabelText("Nome di questo dispositivo");
    await user.type(names[1]!, "lo schermo in cucina");
    await user.tab();
    await waitFor(() =>
      expect(api.recorded.assignments[1]).toEqual({
        id: "E8:3D:C1:FB:9F:18",
        assignment: { name: "lo schermo in cucina" },
      }),
    );
  });

  it("lets one display hold two jobs, and does not take either from anybody", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Dispositivi");
    const groups = await screen.findAllByRole("group", {
      name: "A cosa serve questo dispositivo",
    });
    // The first display already shows the pictures; adding the second job keeps both.
    await user.click(
      within(groups[0]!).getByRole("checkbox", { name: "mostra le azioni da compiere" }),
    );

    await waitFor(() =>
      expect(api.recorded.assignments).toEqual([
        { id: "94:A9:90:CF:7D:04", assignment: { jobs: ["picture", "sheet"] } },
      ]),
    );
  });

  it("offers a printer only the job a printer can do", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());

    await open(user, "Dispositivi");
    const groups = await screen.findAllByRole("group", {
      name: "A cosa serve questo dispositivo",
    });
    const choices = within(groups[2]!)
      .getAllByRole("checkbox")
      .map((box) => box.closest("label")?.textContent);
    expect(choices).toEqual(["stampa i fogli"]);
  });

  it("takes a thing off the list and offers it back with what it had", async () => {
    // Before 25 August 2026 the hub's next report put it straight back, stripped of its
    // job and its name, so a press made by mistake read as the panel losing a setting.
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Dispositivi");
    const removals = await screen.findAllByRole("button", { name: "Togli" });
    await user.click(removals[0]!);

    await screen.findByRole("heading", { name: "Tolti dall'elenco" });
    await user.click(screen.getByRole("button", { name: "Rimetti" }));

    await waitFor(() =>
      expect(screen.queryByRole("heading", { name: "Tolti dall'elenco" })).toBeNull(),
    );
  });

  it("asks the house to look at the network, and says when the answer arrives", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Dispositivi");
    await user.click(await screen.findByRole("button", { name: "Cerca stampanti e scanner" }));

    await waitFor(() => expect(api.recorded.looked).toEqual(["asked"]));
    // What was written down, how long it takes, and what to do next.
    await screen.findByText(/compare in questo elenco entro un minuto/);
  });

  it("asks a display which one it is, and says what ends it", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Dispositivi");
    const asking = await screen.findAllByRole("button", { name: "Qual è?" });
    // Only the displays: a printer has no screen to say it on.
    expect(asking).toHaveLength(2);

    await user.click(asking[0]!);

    await waitFor(() => expect(api.recorded.identified).toEqual(["94:A9:90:CF:7D:04"]));
    // The press on the box is the only thing that ends it, and the panel says so.
    await screen.findByText(/finché non premi il pulsante sul display stesso/);
  });
});

describe("the themes", () => {
  beforeEach(() => window.localStorage.clear());

  it("adds one and takes one away", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Temi dei quadri");
    await user.type(await screen.findByLabelText("Nuovo tema"), "barche a remi");
    await user.click(screen.getByRole("button", { name: "Aggiungi" }));
    await waitFor(() => expect(api.recorded.themesAdded).toEqual(["barche a remi"]));

    await user.click(screen.getAllByRole("button", { name: "Togli" })[0]!);
    await waitFor(() => expect(api.recorded.themesRemoved).toEqual(["theme-1"]));
    expect(screen.queryByText("gatti che dormono")).not.toBeInTheDocument();
  });
});

describe("the reminders", () => {
  beforeEach(() => window.localStorage.clear());

  it("writes a sentence down and says nobody in the house has read it", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Promemoria");
    await user.type(await screen.findByLabelText("Nuovo promemoria"), "annaffiare le piante");
    await user.click(screen.getByRole("button", { name: "Aggiungi" }));

    await waitFor(() => expect(api.recorded.remindersAdded).toEqual(["annaffiare le piante"]));
    // The page says plainly that writing it changed nothing else.
    expect(screen.getAllByText(/non l'ha ancora letto/).length).toBeGreaterThan(0);
    expect(screen.getByText(/non fa partire niente/)).toBeInTheDocument();
  });

  it("corrects a sentence in place, leaving one copy and not two", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Promemoria");
    const boxes = await screen.findAllByLabelText("Promemoria");
    await user.clear(boxes[0]!);
    await user.type(boxes[0]!, "lavarsi i denti alle 21:00");
    await user.tab();

    await waitFor(() =>
      expect(api.recorded.remindersRewritten).toEqual([
        { id: "rm_1", text: "lavarsi i denti alle 21:00" },
      ]),
    );
    expect(screen.getAllByLabelText("Promemoria")).toHaveLength(2);
  });

  it("takes one away, and keeps no count of anything", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Promemoria");
    await user.click((await screen.findAllByRole("button", { name: "Togli" }))[0]!);

    await waitFor(() => expect(api.recorded.remindersRemoved).toEqual(["rm_1"]));
    expect(screen.queryByDisplayValue("lavarsi i denti dopo cena")).not.toBeInTheDocument();
  });

  it("shows the parent the sentences the display will use", async () => {
    // Approval here is of the reminder and not of each sentence, so the sentences have to
    // be readable somewhere the parent goes, and not only on a screen in another room.
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Promemoria");
    expect(await screen.findByText(/È ora dei denti/)).toBeInTheDocument();
    expect(screen.getByText(/Un minuto per i denti/)).toBeInTheDocument();
  });
});

describe("the latitude", () => {
  beforeEach(() => window.localStorage.clear());

  it("writes a line and takes one away, sending the whole list each time", async () => {
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Limiti dell'attività");
    await user.type(
      await screen.findByLabelText("Un vincolo per l'attività"),
      "niente forbici o lame",
    );
    await user.click(screen.getByRole("button", { name: "Aggiungi" }));

    await waitFor(() =>
      expect(api.recorded.guidelines).toEqual([
        ["non deve uscire di casa", "niente forbici o lame"],
      ]),
    );

    await user.click(screen.getAllByRole("button", { name: "Togli" })[0]!);
    await waitFor(() => expect(api.recorded.guidelines).toHaveLength(2));
    expect(api.recorded.guidelines[1]).toEqual(["niente forbici o lame"]);
  });

  it("shows every bound we wrote, in the parent's language and with nothing to press", async () => {
    /* The panel's copy and the prompt's copy are two renderings of one rule, so what is
     * held down is the count: a bound added to the prompt and not here would otherwise
     * simply not be shown to the parent. */
    const api = fakeApi();
    const user = userEvent.setup();
    renderPanel(api);

    await open(user, "Limiti dell'attività");
    const ours = await screen.findByText(/valgono in ogni casa/);
    const listed = ours.parentElement!.querySelectorAll("li");

    expect(listed).toHaveLength((await api.guidelines()).fixed.length);
    expect(listed[0]!.textContent).toMatch(/niente sulla persona/);
    expect(within(ours.parentElement as HTMLElement).queryAllByRole("button")).toEqual([]);
  });

  it("says plainly that writing here starts nothing", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());

    await open(user, "Limiti dell'attività");
    expect(await screen.findByText(/non fa partire niente/)).toBeInTheDocument();
  });

  it("says the three examples are examples, and that pressing one settles nothing", async () => {
    /* Unlabelled, they read as three lines already in force: they sit in boxes that look
     * exactly like the controls beside them. */
    const user = userEvent.setup();
    renderPanel(fakeApi());

    await open(user, "Limiti dell'attività");
    expect(await screen.findByText(/Tre esempi/)).toBeInTheDocument();

    const field = screen.getByLabelText("Un vincolo per l'attività");
    await user.click(screen.getByRole("button", { name: "Niente forbici o lame" }));

    expect(field).toHaveValue("Niente forbici o lame");
  });

  it("every example is a limit, because a fact about a drawer bounds nothing", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi());

    await open(user, "Limiti dell'attività");
    for (const shown of [
      "Non deve uscire di casa",
      "Niente forbici o lame",
      "Niente che faccia rumore dopo le nove",
    ]) {
      expect(await screen.findByRole("button", { name: shown })).toBeInTheDocument();
    }
  });
});
