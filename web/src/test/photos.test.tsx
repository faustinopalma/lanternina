import { fireEvent, screen, waitFor } from "@testing-library/react";
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