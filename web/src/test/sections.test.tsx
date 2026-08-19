/* The gallery, the rhythm and the devices — the three sections whose behaviour is not
 * obvious from their markup. */
import { screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

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
});

describe("the rhythm", () => {
  beforeEach(() => window.localStorage.clear());

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
      quietFrom: "21:30",
      quietUntil: "07:00",
      cadenceMinutes: 90,
    });
    expect(await screen.findByText(/La casa lo applica al prossimo giro/)).toBeInTheDocument();
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
});
