import { InteractionRequiredAuthError, type AccountInfo, type AuthenticationResult } from "@azure/msal-browser";
import { afterEach, expect, it, vi } from "vitest";

import { bearerFor, msalInstance } from "@/auth/msal";

const account = { homeAccountId: "parent", localAccountId: "local" } as AccountInfo;
const answer = (accessToken: string) => ({ accessToken }) as AuthenticationResult;
afterEach(() => vi.restoreAllMocks());

it("shares concurrent acquisition but asks MSAL again for the next request", async () => {
  const silent = vi.spyOn(msalInstance, "acquireTokenSilent").mockResolvedValue(answer("first"));
  expect(await Promise.all([bearerFor(account), bearerFor(account)])).toEqual(["first", "first"]);
  expect(silent).toHaveBeenCalledTimes(1);
  silent.mockResolvedValue(answer("renewed"));
  expect(await bearerFor(account)).toBe("renewed");
  expect(silent).toHaveBeenCalledTimes(2);
});

it("starts only one redirect when concurrent callers need interaction", async () => {
  vi.spyOn(msalInstance, "acquireTokenSilent").mockRejectedValue(
    new InteractionRequiredAuthError("interaction_required", "test-correlation"),
  );
  const redirect = vi.spyOn(msalInstance, "acquireTokenRedirect").mockResolvedValue();
  expect(await Promise.all([bearerFor(account), bearerFor(account)])).toEqual([null, null]);
  expect(redirect).toHaveBeenCalledTimes(1);
});

it("does not retain a failed token request", async () => {
  const silent = vi.spyOn(msalInstance, "acquireTokenSilent").mockRejectedValueOnce(new Error("network"));
  await expect(bearerFor(account)).rejects.toThrow("network");
  silent.mockResolvedValue(answer("recovered"));
  expect(await bearerFor(account)).toBe("recovered");
});