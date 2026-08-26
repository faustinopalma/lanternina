import { useCallback, useEffect, useState } from "react";

/** Loading, failed, or here. Three states written down, because a section that quietly
 *  shows nothing is indistinguishable from a section with nothing in it. */
export type Loaded<T> =
  | { status: "loading" }
  | { status: "failed" }
  | { status: "ready"; data: T };

/* How long to wait before asking a second time, and how many times. One retry and no more:
 * the API scales to zero, so the first request of a sitting can lose a race with the
 * container starting — and that is a transient failure that used to leave a section saying
 * it could not read anything until the parent reloaded the whole page. What it must not
 * become is polling: a section that kept asking would hold the container up and cost money
 * for nobody's benefit. */
const AGAIN_AFTER_MS = 1500;
const TRIES = 2;

export function useLoad<T>(
  load: () => Promise<T>,
  deps: unknown[] = [],
): [Loaded<T>, () => void] {
  const [state, setState] = useState<Loaded<T>>({ status: "loading" });
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let current = true;
    let timer = 0;
    setState({ status: "loading" });

    const ask = (left: number) => {
      load().then(
        (data) => current && setState({ status: "ready", data }),
        () => {
          if (!current) return;
          if (left > 1) {
            timer = window.setTimeout(() => current && ask(left - 1), AGAIN_AFTER_MS);
            return;
          }
          setState({ status: "failed" });
        },
      );
    };
    ask(TRIES);

    return () => {
      current = false;
      window.clearTimeout(timer);
    };
    // `load` is deliberately not a dependency: it is rebuilt on every render, and having it
    // here would ask again on every render. `attempt` and `deps` are what ask again.
  }, [attempt, ...deps]);

  return [state, useCallback(() => setAttempt((n) => n + 1), [])];
}
