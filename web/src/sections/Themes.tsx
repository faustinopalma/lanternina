import { useState, type FormEvent } from "react";

import { useApi } from "@/api/client";
import { ApiError, type Theme } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Input } from "@/components/ui/field";
import { useWords, type MessageKey } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

function Chip({
  theme,
  onRemoved,
  onFailed,
}: {
  theme: Theme;
  onRemoved: () => void;
  onFailed: () => void;
}) {
  const { t } = useWords();
  const api = useApi();
  const [removing, setRemoving] = useState(false);

  return (
    <div className="mt-2 flex max-w-[42rem] items-center justify-between gap-3 rounded-[--radius-control] border border-edge bg-paper py-2 pr-2 pl-3.5">
      <span>{theme.label}</span>
      <Button
        size="small"
        disabled={removing}
        title={t("themes.removeTitle", { label: theme.label })}
        onClick={async () => {
          setRemoving(true);
          try {
            await api.removeTheme(theme.id);
            onRemoved();
          } catch {
            setRemoving(false);
            onFailed();
          }
        }}
      >
        {t("themes.remove")}
      </Button>
    </div>
  );
}

export function Themes() {
  const { t } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.themes());
  const [added, setAdded] = useState<Theme[]>([]);
  const [removed, setRemoved] = useState<string[]>([]);
  const [label, setLabel] = useState("");
  const [problem, setProblem] = useState<MessageKey | null>(null);

  async function add(event: FormEvent) {
    event.preventDefault();
    const wanted = label.trim();
    if (!wanted) return;
    setProblem(null);
    try {
      const theme = await api.addTheme(wanted);
      setAdded((seen) => [...seen, theme]);
      setLabel("");
    } catch (error) {
      setProblem(error instanceof ApiError && error.rejected ? "themes.badLabel" : "themes.addFailed");
    }
  }

  const form = (
    <>
      <form
        onSubmit={add}
        className="my-3.5 flex max-w-[42rem] gap-2.5 rounded-[--radius-control] border border-edge bg-paper p-4"
      >
        <Input
          className="min-w-0 flex-auto"
          maxLength={80}
          autoComplete="off"
          aria-label={t("themes.aria")}
          placeholder={t("themes.placeholder")}
          value={label}
          onChange={(event) => setLabel(event.target.value)}
        />
        <Button type="submit" variant="primary" className="flex-none">
          {t("themes.add")}
        </Button>
      </form>
      {problem !== null ? <Quiet>{t(problem)}</Quiet> : null}
    </>
  );

  if (state.status === "loading") return <Quiet>{t("themes.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("themes.unreadable")}</Quiet>;

  const showing = [...state.data, ...added].filter((theme) => !removed.includes(theme.id));

  return (
    <>
      {form}
      <div aria-live="polite">
        {showing.length === 0 ? (
          <Quiet>{t("themes.empty")}</Quiet>
        ) : (
          showing.map((theme) => (
            <Chip
              key={theme.id}
              theme={theme}
              onRemoved={() => setRemoved((seen) => [...seen, theme.id])}
              onFailed={() => setProblem("themes.removeFailed")}
            />
          ))
        )}
      </div>
    </>
  );
}
