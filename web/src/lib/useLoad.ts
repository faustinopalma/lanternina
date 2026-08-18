import { useCallback, useEffect, useState } from "react";

/** Loading, failed, or here. Three states written down, because a section that quietly
 *  shows nothing is indistinguishable from a section with nothing in it. */
export type Loaded<T> =
  | { status: "loading" }
  | { status: "failed" }
  | { status: "ready"; data: T };

export function useLoad<T>(
  load: () => Promise<T>,
  deps: unknown[] = [],
): [Loaded<T>, () => void] {
  const [state, setState] = useState<Loaded<T>>({ status: "loading" });
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let current = true;
    setState({ status: "loading" });
    load().then(
      (data) => current && setState({ status: "ready", data }),
      () => current && setState({ status: "failed" }),
    );
    return () => {
      current = false;
    };
    // `load` is deliberately not a dependency: it is rebuilt on every render, and having it
    // here would ask again on every render. `attempt` and `deps` are what ask again.
  }, [attempt, ...deps]);

  return [state, useCallback(() => setAttempt((n) => n + 1), [])];
}
