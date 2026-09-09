import { useCallback, useEffect, useState } from "react";

/** Loading, failed, or here. Three states written down, because a section that quietly
 *  shows nothing is indistinguishable from a section with nothing in it. */
export type Loaded<T> =
  | { status: "loading" }
  | { status: "failed" }
  | { status: "ready"; data: T };

const AGAIN_AFTER_MS = 1500;
const TRIES = 2;
const REFRESH_AFTER_MS = 30_000;

export function useLoad<T>(
  load: () => Promise<T>,
  deps: unknown[] = [],
  { live = false }: { live?: boolean } = {},
): [Loaded<T>, () => void] {
  const [state, setState] = useState<Loaded<T>>({ status: "loading" });
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let current = true;
    let timer = 0;
    let busy = false;
    setState({ status: "loading" });

    const schedule = () => {
      if (current && live) timer = window.setTimeout(refresh, REFRESH_AFTER_MS);
    };
    const ask = (left: number) => {
      if (!current || busy) return;
      window.clearTimeout(timer);
      busy = true;
      Promise.resolve().then(load).then(
        (data) => {
          busy = false;
          if (!current) return;
          setState({ status: "ready", data });
          schedule();
        },
        () => {
          busy = false;
          if (!current) return;
          if (left > 1) {
            timer = window.setTimeout(() => {
              if (live && document.visibilityState === "hidden") schedule();
              else ask(left - 1);
            }, AGAIN_AFTER_MS);
            return;
          }
          setState((previous) => previous.status === "ready" ? previous : { status: "failed" });
          schedule();
        },
      );
    };
    const refresh = () => {
      if (!current || busy) return;
      window.clearTimeout(timer);
      if (document.visibilityState === "hidden" || !navigator.onLine) {
        schedule();
        return;
      }
      ask(TRIES);
    };
    ask(TRIES);
    if (live) {
      window.addEventListener("focus", refresh);
      window.addEventListener("online", refresh);
      document.addEventListener("visibilitychange", refresh);
    }

    return () => {
      current = false;
      window.clearTimeout(timer);
      window.removeEventListener("focus", refresh);
      window.removeEventListener("online", refresh);
      document.removeEventListener("visibilitychange", refresh);
    };
    // `load` is deliberately not a dependency: it is rebuilt on every render, and having it
    // here would ask again on every render. `attempt` and `deps` are what ask again.
  }, [attempt, live, ...deps]);

  return [state, useCallback(() => setAttempt((n) => n + 1), [])];
}
