import { act, fireEvent, renderHook, screen } from "@testing-library/react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";

import { useLoad } from "@/lib/useLoad";
import { Experiences } from "@/sections/Experiences";
import { fakeApi, SAMPLE_AFTERNOON } from "@/test/fakeApi";
import { renderPanel } from "@/test/render";

beforeEach(() => vi.useFakeTimers());
afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
});
const tick = (milliseconds = 0) => act(async () => { await vi.advanceTimersByTimeAsync(milliseconds); });

it("refreshes without discarding the last data while a request is pending", async () => {
  let finish!: (value: string) => void;
  const load = vi.fn().mockResolvedValueOnce("first")
    .mockImplementation(() => new Promise<string>((resolve) => { finish = resolve; }));
  const { result, unmount } = renderHook(() => useLoad(load, [], { live: true }));
  await tick();
  await tick(30_000);
  expect(load).toHaveBeenCalledTimes(2);
  expect(result.current[0]).toEqual({ status: "ready", data: "first" });
  fireEvent.focus(window);
  await tick(60_000);
  expect(load).toHaveBeenCalledTimes(2);
  await act(async () => finish("second"));
  expect(result.current[0]).toEqual({ status: "ready", data: "second" });
  unmount();
  await tick(60_000);
  expect(load).toHaveBeenCalledTimes(2);
});

it("pauses while hidden and reads again on return and reconnection", async () => {
  const load = vi.fn().mockResolvedValue("data");
  renderHook(() => useLoad(load, [], { live: true }));
  await tick();
  const visibility = vi.spyOn(document, "visibilityState", "get").mockReturnValue("hidden");
  await tick(60_000);
  expect(load).toHaveBeenCalledTimes(1);
  visibility.mockReturnValue("visible");
  fireEvent(document, new Event("visibilitychange"));
  await tick();
  expect(load).toHaveBeenCalledTimes(2);
  fireEvent.online(window);
  await tick();
  expect(load).toHaveBeenCalledTimes(3);
});

it("keeps the data through a failed background refresh and recovers later", async () => {
  const load = vi.fn().mockResolvedValueOnce("first").mockRejectedValue(new Error("offline"));
  const { result } = renderHook(() => useLoad(load, [], { live: true }));
  await tick();
  await tick(31_500);
  expect(result.current[0]).toEqual({ status: "ready", data: "first" });
  load.mockResolvedValue("recovered");
  await tick(30_000);
  expect(result.current[0]).toEqual({ status: "ready", data: "recovered" });
});

it("does not poll a form that has not opted into live data", async () => {
  const load = vi.fn().mockResolvedValue("saved");
  renderHook(() => useLoad(load));
  await tick();
  fireEvent.focus(window);
  await tick(60_000);
  expect(load).toHaveBeenCalledTimes(1);
});

it("ignores a late response for a section that has been replaced", async () => {
  let finish!: (value: string) => void;
  const load = vi.fn().mockImplementationOnce(() => new Promise<string>((resolve) => { finish = resolve; }))
    .mockResolvedValue("new section");
  const { result, rerender } = renderHook(({ section }) => useLoad(load, [section], { live: true }),
    { initialProps: { section: "old" } });
  await tick();
  rerender({ section: "new" });
  await tick();
  await act(async () => finish("old section"));
  expect(result.current[0]).toEqual({ status: "ready", data: "new section" });
});

it("shows a newly offered experience and preserves the open plan and selection", async () => {
  const original = fakeApi();
  let added = false;
  const api = fakeApi({ experiences: async (state) => {
    const list = await original.experiences(state);
    return state === "pending" && added
      ? { ...list, experiences: [...list.experiences, { ...SAMPLE_AFTERNOON, id: "new", title: "Nuova esperienza" }] }
      : list;
  } });
  renderPanel(api, <Experiences />);
  await tick();
  fireEvent.click(screen.getByRole("button", { name: "Se vuoi vedere com'è fatta" }));
  fireEvent.click(screen.getByRole("checkbox"));
  added = true;
  await tick(30_000);
  expect(screen.getByText("Nuova esperienza")).toBeInTheDocument();
  expect(screen.getByText("Scegli un oggetto")).toBeInTheDocument();
  expect(screen.getAllByRole("checkbox")[0]).toBeChecked();
});