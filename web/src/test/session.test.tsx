import { InteractionStatus } from "@azure/msal-browser";
import { act, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { App } from "@/App";
import { LanguageProvider } from "@/i18n";

const auth = vi.hoisted(() => ({
  accounts: [{ homeAccountId: "parent", localAccountId: "parent", username: "parent@example.invalid" }],
  inProgress: "none",
  bearer: vi.fn(),
}));
vi.mock("@azure/msal-react", () => ({ useMsal: () => auth }));
vi.mock("@/auth/msal", () => ({
  bearerFor: auth.bearer, signIn: vi.fn(), signOut: vi.fn(),
}));
vi.mock("@/components/Dashboard", () => ({
  Dashboard: () => <input aria-label="draft" defaultValue="" />,
}));

afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
  auth.inProgress = InteractionStatus.None;
  auth.bearer.mockReset();
});

it("finishes admission even when silent acquisition changes MSAL's interaction state", async () => {
  let finish!: (token: string) => void;
  auth.bearer.mockImplementationOnce(() => new Promise<string>((resolve) => { finish = resolve; }));
  auth.bearer.mockResolvedValue("renewed");
  const fetcher = vi.fn().mockResolvedValue({ ok: true, json: async () => ({}) });
  vi.stubGlobal("fetch", fetcher);
  const tree = () => <LanguageProvider><App /></LanguageProvider>;
  const page = render(tree());
  await act(async () => {});
  auth.inProgress = InteractionStatus.AcquireToken;
  page.rerender(tree());
  await act(async () => finish("first"));
  expect(await screen.findByLabelText("draft")).toBeInTheDocument();
  auth.inProgress = InteractionStatus.None;
  page.rerender(tree());
  expect(screen.getByLabelText("draft")).toBeInTheDocument();
  expect(fetcher).toHaveBeenCalledTimes(1);
});

it("can retry admission after a network failure without logging out or reloading", async () => {
  vi.useFakeTimers();
  window.localStorage.setItem("lanternina.language", "it");
  auth.bearer.mockResolvedValue("current");
  const fetcher = vi.fn().mockRejectedValue(new Error("network"));
  vi.stubGlobal("fetch", fetcher);
  render(<LanguageProvider><App /></LanguageProvider>);
  await act(async () => { await vi.advanceTimersByTimeAsync(1500); });
  expect(fetcher).toHaveBeenCalledTimes(2);
  fetcher.mockResolvedValue({ ok: true, json: async () => ({}) });
  fireEvent.click(screen.getByRole("button", { name: "Riprova" }));
  await act(async () => {});
  expect(screen.getByLabelText("draft")).toBeInTheDocument();
  expect(fetcher).toHaveBeenCalledTimes(3);
});