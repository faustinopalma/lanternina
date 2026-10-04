import { InteractionStatus, type AccountInfo } from "@azure/msal-browser";
import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";

import { Entry } from "@/Entry";
import { LanguageProvider } from "@/i18n";
import { portalEntry, sessionDestination } from "@/portal/session";

const session = vi.hoisted(() => ({
  accounts: [{ homeAccountId: "first", localAccountId: "first" }] as AccountInfo[],
  inProgress: "none",
}));
vi.mock("@azure/msal-react", () => ({ useMsal: () => session }));
vi.mock("@/App", () => ({ App: () => <h1>Parent panel</h1> }));
vi.mock("@/portal/Portal", () => ({ Portal: () => <h1>Adolescent portal</h1> }));
vi.mock("@/auth/msal", () => ({ bearerFor: vi.fn(async () => "test-token") }));
vi.mock("@/portal/session", async (original) => ({
  ...await original<typeof import("@/portal/session")>(), sessionDestination: vi.fn(),
}));

beforeEach(() => {
  sessionStorage.clear();
  localStorage.setItem("lanternina.language", "it");
  session.inProgress = InteractionStatus.None;
  session.accounts = [{ homeAccountId: "first", localAccountId: "first" }] as AccountInfo[];
});
afterEach(() => { history.replaceState(null, "", "/"); vi.resetAllMocks(); });

it.each(["/", "/portal"])("routes an adolescent at %s from the server role", async (path) => {
  history.replaceState(null, "", path);
  vi.mocked(sessionDestination).mockResolvedValue("adolescent");
  render(<LanguageProvider><Entry portalRequested={portalEntry()} /></LanguageProvider>);
  expect(await screen.findByText("Adolescent portal")).toBeVisible();
  expect(screen.queryByText("Parent panel")).toBeNull();
  expect(location.pathname).toBe("/portal");
});

it.each(["/", "/portal"])("routes a parent at %s despite stale portal state", async (path) => {
  history.replaceState(null, "", path);
  sessionStorage.setItem("lanternina.portal.return", "1");
  sessionStorage.setItem("lanternina.portal.invite", "a".repeat(43));
  vi.mocked(sessionDestination).mockResolvedValue("parent");
  render(<LanguageProvider><Entry portalRequested={portalEntry()} /></LanguageProvider>);
  expect(await screen.findByText("Parent panel")).toBeVisible();
  expect(screen.queryByText("Adolescent portal")).toBeNull();
  expect(location.pathname).toBe("/");
  expect(sessionStorage.getItem("lanternina.portal.invite")).toBeNull();
  expect(sessionStorage.getItem("lanternina.portal.return")).toBeNull();
});

it("keeps explicit redemption for an unknown invited identity", async () => {
  vi.mocked(sessionDestination).mockResolvedValue("new");
  render(<LanguageProvider><Entry portalRequested /></LanguageProvider>);
  expect(await screen.findByText("Adolescent portal")).toBeVisible();
});

it("does not infer a role when the server cannot be reached", async () => {
  vi.mocked(sessionDestination).mockRejectedValue(new Error("offline"));
  render(<LanguageProvider><Entry portalRequested={false} /></LanguageProvider>);
  expect(await screen.findByRole("alert", {}, { timeout: 3000 })).toBeVisible();
  expect(screen.queryByText("Parent panel")).toBeNull();
  expect(screen.queryByText("Adolescent portal")).toBeNull();
});

it("resolves again when the authenticated account changes", async () => {
  vi.mocked(sessionDestination).mockResolvedValueOnce("adolescent").mockResolvedValueOnce("parent");
  const view = render(<LanguageProvider><Entry portalRequested /></LanguageProvider>);
  await screen.findByText("Adolescent portal");
  session.accounts = [{ homeAccountId: "second", localAccountId: "second" }] as AccountInfo[];
  view.rerender(<LanguageProvider><Entry portalRequested /></LanguageProvider>);
  await waitFor(() => expect(screen.getByText("Parent panel")).toBeVisible());
  expect(screen.queryByText("Adolescent portal")).toBeNull();
});