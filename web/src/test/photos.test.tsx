import { act, fireEvent, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import type { PhotoPage } from "@/api/types";
import { Photos, dateSelection } from "@/sections/Photos";
import { fakeApi } from "@/test/fakeApi";
import { renderPanel } from "@/test/render";

const photoId = "a".repeat(32);
const data: PhotoPage = {
  photos: [{ id: photoId, camera: "camera", capturedAt: 100, receivedAt: 102, date: 100,
    width: 1600, height: 1200, state: "done" }],
  total: 1, pages: 1, page: 1, lastReceivedAt: 102,
  hub: { contactAt: 103, pending: 0, localPhotos: 1, lastReceivedAt: 102 },
};

describe("family photographs", () => {
  it("requires an explicit choice among frozen photo candidates", async () => {
    const user = userEvent.setup();
    const assignPhoto = vi.fn(async () => ({ queued: true }));
    const run = { runId: "aft_1", title: "Prima attività", beganAt: 1, endsAt: 0,
      momentId: "page", heading: "Primo foglio", phase: "waiting" as const, waitingSince: 100 };
    renderPanel(fakeApi({ assignPhoto,
      currentTrail: async () => ({ updatedAt: Date.now() / 1000, runs: [run, { ...run, runId: "aft_other" }] }),
      photos: async () => ({ ...data, photos: [{ ...data.photos[0]!, state: "awaiting_assignment",
        target: { candidates: [{ run: "aft_1", moment: "page", since: 100 },
          { run: "aft_old", moment: "page", since: 50 }] } }] }),
    }), <Photos />);
    const select = await screen.findByLabelText("Attività");
    expect(screen.getByRole("button", { name: "Associa foto" })).toBeDisabled();
    expect(within(select).getAllByRole("option")).toHaveLength(2);
    await user.selectOptions(select, "aft_1");
    await user.click(screen.getByRole("button", { name: "Associa foto" }));
    expect(assignPhoto).toHaveBeenCalledWith(photoId, "aft_1");
    expect(await screen.findByText("Associazione richiesta. In attesa dell'hub.")).toBeVisible();
  });
  beforeEach(() => {
    HTMLDialogElement.prototype.showModal = function () { this.open = true; };
    HTMLDialogElement.prototype.close = function () { this.open = false; };
  });

  it("fetches authenticated originals and shows hub diagnostics", async () => {
    const photoContent = vi.fn(async () => new Blob(["photo"], { type: "image/jpeg" }));
    renderPanel(fakeApi({ photos: async () => data, photoContent }), <Photos />);
    await screen.findByText(/Ultimo contatto/);
    expect(await screen.findByRole("img")).toHaveAttribute("src", expect.stringMatching(/^blob:/));
    expect(photoContent).toHaveBeenCalledWith(photoId);
    expect(screen.getByText(/da sincronizzare: 0/)).toBeInTheDocument();
  });

  it("requires confirmation and allows cancelling all-photo deletion", async () => {
    const user = userEvent.setup();
    const deletePhotos = vi.fn(async () => ({ deleted: [photoId], failed: [] }));
    renderPanel(fakeApi({ photos: async () => data, deletePhotos,
      previewPhotoDeletion: async () => ({ ids: [photoId] }) }), <Photos />);
    await user.click(await screen.findByRole("button", { name: "Elimina tutte" }));
    await screen.findByRole("dialog");
    expect(deletePhotos).not.toHaveBeenCalled();
    await user.click(screen.getByRole("button", { name: "Annulla" }));
    expect(deletePhotos).not.toHaveBeenCalled();
    await user.click(screen.getByRole("button", { name: "Elimina tutte" }));
    await screen.findByRole("dialog");
    await user.click(screen.getByRole("button", { name: "Conferma eliminazione" }));
    await waitFor(() => expect(deletePhotos).toHaveBeenCalledWith({ mode: "all" }, [photoId]));
  });

  it("keeps date deletion disabled until both dates form a valid interval", async () => {
    const preview = vi.fn(async () => ({ ids: [photoId] }));
    renderPanel(fakeApi({ photos: async () => data, previewPhotoDeletion: preview }), <Photos />);
    const button = screen.getByRole("button", { name: "Elimina per date" });
    expect(button).toBeDisabled();
    fireEvent.change(screen.getByLabelText("Dal"), { target: { value: "2026-09-09" } });
    fireEvent.change(screen.getByLabelText("Al"), { target: { value: "2026-09-08" } });
    expect(button).toBeDisabled();
    fireEvent.change(screen.getByLabelText("Al"), { target: { value: "2026-09-09" } });
    expect(button).toBeEnabled();
    fireEvent.click(button);
    await waitFor(() => expect(preview).toHaveBeenCalledWith(dateSelection("2026-09-09", "2026-09-09")));
  });

  it.each([false, true])("expires only successful deletion messages (failed=%s)", async failed => {
    const user = userEvent.setup();
    renderPanel(fakeApi({ photos: async () => data,
      previewPhotoDeletion: async () => ({ ids: [photoId] }),
      deletePhotos: async () => ({ deleted: failed ? [] : [photoId], failed: failed ? [photoId] : [] }),
    }), <Photos />);
    await user.click(await screen.findByRole("button", { name: "Elimina tutte" }));
    await screen.findByRole("dialog");
    vi.useFakeTimers();
    try {
      await act(async () => { fireEvent.click(screen.getByRole("button", { name: "Conferma eliminazione" })); });
      expect(screen.getByRole("status")).toBeVisible();
      await act(async () => { vi.advanceTimersByTime(4999); });
      expect(screen.getByRole("status")).toBeVisible();
      await act(async () => { vi.advanceTimersByTime(1); });
      if (failed) expect(screen.getByRole("status")).toBeVisible();
      else expect(screen.queryByRole("status")).toBeNull();
    } finally { vi.useRealTimers(); }
  });

  it("includes the entire final local day", () => {
    const range = dateSelection("2026-09-09", "2026-09-09");
    expect(range).toEqual({ mode: "range", start: new Date("2026-09-09T00:00:00").getTime()/1000,
      end: new Date("2026-09-10T00:00:00").getTime()/1000 });
    expect(dateSelection("", "2026-09-09")).toBeNull();
  });

  it("does not call announced sleep confirmed sleep", async () => {
    const user = userEvent.setup();
    renderPanel(fakeApi({ photos: async () => ({ ...data, hub: {
      contactAt: 103, pending: 0, localPhotos: 1, lastReceivedAt: 102,
      cameras: [{ id: "camera", history: [{ receivedAt: 103, phase: "sleep_planned",
        previousSleepConfirmed: false, captureMs: 2866, queued: 0 }] }],
    } }) }), <Photos />);
    await user.click(await screen.findByText("Diagnostica fotocamera"));
    expect(screen.getByText(/sonno annunciato, non ancora confermato/)).toBeVisible();
    expect(screen.queryByText(/risveglio da deep sleep confermato/)).toBeNull();
  });
});