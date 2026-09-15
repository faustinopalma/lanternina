import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, expect, it, vi } from "vitest";

import { LanguageProvider } from "@/i18n";
import { PhotoPortal, PortalSession } from "@/portal/Portal";
import { PortalError, type PortalApi } from "@/portal/api";
import { portalEntry, invitationToken } from "@/portal/session";
import { Adolescents } from "@/sections/Adolescents";
import { fakeApi } from "@/test/fakeApi";
import { renderPanel } from "@/test/render";

vi.mock("@/auth/msal", () => ({ bearerFor: vi.fn(), signIn: vi.fn(), signOut: vi.fn() }));
vi.mock("@/portal/api", async (original) => ({
  ...await original<typeof import("@/portal/api")>(),
  preparePhoto: vi.fn(async () => new Blob(["image"], { type: "image/jpeg" })),
}));

function api(): PortalApi {
  return {
    me: vi.fn(async () => ({ id: "teen", email: "teen@example.test" })),
    accept: vi.fn(async () => undefined),
    photos: vi.fn(async () => ({ photos: [], total: 0, page: 1, pages: 1 })),
    content: vi.fn(async () => new Blob(["image"], { type: "image/jpeg" })),
    send: vi.fn(async (id) => ({ id, camera: "portal:teen", receivedAt: 100, capturedAt: 100,
      date: 100, width: 40, height: 30, state: "pending" as const })),
    delete: vi.fn(async () => undefined),
  };
}

beforeEach(() => {
  localStorage.setItem("lanternina.language", "it");
  sessionStorage.clear();
});
afterEach(() => { vi.useRealTimers(); vi.restoreAllMocks(); history.replaceState(null, "", "/"); });

it("keeps invitation across the identity-provider return without leaving it in the URL", () => {
  const token = "a".repeat(43);
  history.replaceState(null, "", `/portal#invite=${token}`);
  expect(portalEntry()).toBe(true);
  expect(location.hash).toBe("");
  expect(invitationToken()).toBe(token);
  history.replaceState(null, "", "/");
  expect(portalEntry()).toBe(true);
});

it("accepts the invitation explicitly and then opens the adolescent photos", async () => {
  const service = api();
  sessionStorage.setItem("lanternina.portal.invite", "a".repeat(43));
  render(<LanguageProvider><PortalSession api={service} /></LanguageProvider>);
  expect(service.accept).not.toHaveBeenCalled();
  await userEvent.click(screen.getByRole("button", { name: "Accetta l'invito" }));
  expect(await screen.findByRole("heading", { name: "Mostra a Lanternina" })).toBeVisible();
  expect(service.accept).toHaveBeenCalledWith("a".repeat(43));
  expect(invitationToken()).toBeNull();
});

it("explains an email mismatch and retains the invitation", async () => {
  const service = api();
  vi.mocked(service.accept).mockRejectedValue(new PortalError(403, "invitation_email_mismatch"));
  sessionStorage.setItem("lanternina.portal.invite", "a".repeat(43));
  render(<LanguageProvider><PortalSession api={service} /></LanguageProvider>);
  await userEvent.click(screen.getByRole("button", { name: "Accetta l'invito" }));
  expect(await screen.findByRole("alert")).toHaveTextContent("non corrisponde all'invito");
  expect(invitationToken()).not.toBeNull();
  expect(service.photos).not.toHaveBeenCalled();
});

it("distinguishes a network error from revoked access and permits retry", async () => {
  const service = api();
  vi.mocked(service.me).mockRejectedValue(new Error("offline"));
  render(<LanguageProvider><PortalSession api={service} /></LanguageProvider>);
  expect(await screen.findByRole("alert", {}, { timeout: 3000 })).toHaveTextContent("Non riesco a collegarmi");
  vi.mocked(service.me).mockResolvedValue({ id: "teen", email: "teen@example.test" });
  await userEvent.click(screen.getByRole("button", { name: "Riprova" }));
  expect(await screen.findByRole("heading", { name: "Mostra a Lanternina" })).toBeVisible();
});

it("previews a photo and retries the same upload identifier after a lost response", async () => {
  const service = api();
  vi.mocked(service.send).mockRejectedValueOnce(new Error("network"));
  const { container } = render(<LanguageProvider><PhotoPortal api={service} /></LanguageProvider>);
  fireEvent.change(container.querySelector('input[type="file"]')!, {
    target: { files: [new File(["image"], "photo.jpg", { type: "image/jpeg" })] },
  });
  expect(await screen.findByAltText("Foto da inviare")).toBeVisible();
  expect(service.send).not.toHaveBeenCalled();
  await userEvent.click(screen.getByRole("button", { name: "Invia foto" }));
  await screen.findByText(/La foto non è stata confermata/);
  expect(screen.getByAltText("Foto da inviare")).toBeVisible();
  await userEvent.click(screen.getByRole("button", { name: "Invia foto" }));
  await screen.findByText(/Foto ricevuta/);
  const calls = vi.mocked(service.send).mock.calls;
  expect(calls).toHaveLength(2);
  expect(calls[0]![0]).toBe(calls[1]![0]);
  expect(screen.queryByAltText("Foto da inviare")).toBeNull();
});

it("requires confirmation before deleting an authenticated photograph", async () => {
  const service = api();
  const photo = await service.send("a".repeat(32), new Blob());
  vi.mocked(service.photos).mockResolvedValue({ photos: [photo], total: 1, page: 1, pages: 1 });
  render(<LanguageProvider><PhotoPortal api={service} /></LanguageProvider>);
  await userEvent.click(await screen.findByRole("button", { name: "Elimina foto" }));
  expect(service.delete).not.toHaveBeenCalled();
  await userEvent.click(screen.getByRole("button", { name: "Annulla" }));
  expect(service.delete).not.toHaveBeenCalled();
  await userEvent.click(screen.getByRole("button", { name: "Elimina foto" }));
  await userEvent.click(screen.getByRole("button", { name: "Elimina foto" }));
  await waitFor(() => expect(service.delete).toHaveBeenCalledWith(photo.id));
});

it("sends a parent invitation and requires confirmation to revoke a membership", async () => {
  const user = userEvent.setup();
  const writeText = vi.spyOn(navigator.clipboard, "writeText");
  const inviteAdolescent = vi.fn(async () => ({ id: "invite", code: "a".repeat(43),
    expiresAt: 1000, status: "ready" as const }));
  const revokeAdolescent = vi.fn(async () => undefined);
  renderPanel(fakeApi({ inviteAdolescent, revokeAdolescent,
    familyAccess: async () => ({ invitations: [],
      members: [{ id: "teen", email: "teen@example.test", active: true, joinedAt: 100 }] }),
  }), <Adolescents />);
  await userEvent.type(await screen.findByLabelText("Email dell'adolescente"), "new@example.test");
  await userEvent.click(screen.getByRole("button", { name: "Genera codice" }));
  await waitFor(() => expect(inviteAdolescent).toHaveBeenCalledWith("new@example.test"));
  expect(await screen.findByLabelText("Codice di invito")).toHaveValue("a".repeat(43));
  await user.click(screen.getByRole("button", { name: "Copia codice" }));
  expect(writeText).toHaveBeenCalledWith("a".repeat(43));
  await user.click(screen.getByRole("button", { name: "Copia link" }));
  expect(writeText).toHaveBeenCalledWith(`${location.origin}/portal#invite=${"a".repeat(43)}`);
  await userEvent.click(await screen.findByRole("button", { name: "Revoca accesso" }));
  expect(revokeAdolescent).not.toHaveBeenCalled();
  await userEvent.click(screen.getByRole("button", { name: "Revoca accesso" }));
  await waitFor(() => expect(revokeAdolescent).toHaveBeenCalledWith("teen"));
});

it("keeps an unsent preview through a network outage but closes it on confirmed revocation", async () => {
  const service = api();
  const { container } = render(<LanguageProvider><PortalSession api={service} /></LanguageProvider>);
  await screen.findByRole("heading", { name: "Mostra a Lanternina" });
  fireEvent.change(container.querySelector('input[type="file"]')!, {
    target: { files: [new File(["image"], "photo.jpg", { type: "image/jpeg" })] },
  });
  await screen.findByAltText("Foto da inviare");
  vi.useFakeTimers();
  vi.mocked(service.me).mockRejectedValue(new Error("network"));
  await act(async () => {
    window.dispatchEvent(new Event("focus"));
    await vi.advanceTimersByTimeAsync(1600);
  });
  expect(screen.getByAltText("Foto da inviare")).toBeVisible();
  vi.mocked(service.me).mockRejectedValue(new PortalError(403, "portal_access_required"));
  await act(async () => { window.dispatchEvent(new Event("focus")); });
  expect(screen.queryByAltText("Foto da inviare")).toBeNull();
  expect(screen.getByRole("alert")).toHaveTextContent("L'accesso non è attivo");
});

it("redeems a pasted code after registration and allows correcting an invalid code", async () => {
  const service = api();
  vi.mocked(service.me).mockRejectedValue(new PortalError(403, "portal_access_required"));
  vi.mocked(service.accept).mockRejectedValueOnce(new PortalError(410, "invitation_unavailable"));
  render(<LanguageProvider><PortalSession api={service} /></LanguageProvider>);
  const field = await screen.findByLabelText("Codice di invito");
  await userEvent.type(field, "b".repeat(43));
  await userEvent.click(screen.getByRole("button", { name: "Accetta l'invito" }));
  await screen.findByText(/Il codice non è valido/);
  await userEvent.clear(field);
  await userEvent.type(field, "a".repeat(43));
  vi.mocked(service.me).mockResolvedValue({ id: "teen", email: "teen@example.test" });
  await userEvent.click(screen.getByRole("button", { name: "Accetta l'invito" }));
  expect(await screen.findByRole("heading", { name: "Mostra a Lanternina" })).toBeVisible();
  expect(service.accept).toHaveBeenLastCalledWith("a".repeat(43));
});