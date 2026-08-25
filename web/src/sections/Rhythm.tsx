import { useState, type FormEvent } from "react";

import { useApi } from "@/api/client";
import type { Rhythm as Spacing } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Input, Label } from "@/components/ui/field";
import { useWords, type MessageKey } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

/** Every zone this browser knows, with its own first.
 *
 * `Intl.supportedValuesOf` is not in every engine, so the fallback is the browser's own
 * zone alone: one right answer beats an empty list, and the panel validates whatever
 * arrives anyway. */
function zoneChoices(): string[] {
  const here = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const all =
    typeof Intl.supportedValuesOf === "function" ? Intl.supportedValuesOf("timeZone") : [];
  return [here, ...all.filter((zone) => zone !== here)];
}

/* The form takes what was read as a prop, so the fields hold the parent's choice from the
 * first paint. Copying it in afterwards showed an empty form for a moment, which reads as
 * "nothing has been chosen yet". */
function Form({ spacing }: { spacing: Spacing }) {
  const { t, weekday } = useWords();
  const api = useApi();
  const [quietFrom, setQuietFrom] = useState(spacing.quietFrom);
  const [quietUntil, setQuietUntil] = useState(spacing.quietUntil);
  const [cadence, setCadence] = useState(String(spacing.cadenceMinutes));
  const [days, setDays] = useState<string[]>(spacing.afternoonDays);
  const [afternoonFrom, setAfternoonFrom] = useState(spacing.afternoonFrom);
  const [timeZone, setTimeZone] = useState(spacing.timeZone);
  const [status, setStatus] = useState<MessageKey | null>(
    spacing.quietFrom === spacing.quietUntil ? "rhythm.quietOff" : null,
  );
  const [asked, setAsked] = useState<MessageKey | null>(null);

  /* The browser has the zone list already, so it is not shipped from the panel. The one
   * the browser is in goes first, because on the machine the parent is holding it is
   * almost always the right answer. */
  const zones = zoneChoices();

  /* Saving persists a choice and returns. The house reads it on its next run and decides
   * for itself, so nothing here reaches into the room. */
  async function save(event: FormEvent) {
    event.preventDefault();
    try {
      await api.saveRhythm({
        quietFrom,
        quietUntil,
        cadenceMinutes: Number(cadence),
        afternoonDays: days,
        afternoonFrom,
        timeZone,
      });
      setStatus("rhythm.saved");
    } catch {
      setStatus("rhythm.saveFailed");
    }
  }

  /* One row is written and that is the whole effect. The house finds it when it next
   * looks, so the wording says it was asked for and never that it has started. */
  async function beginNow() {
    setAsked(null);
    try {
      await api.beginNow();
      setAsked("rhythm.beginAsked");
    } catch {
      setAsked("rhythm.beginFailed");
    }
  }

  return (
    <>
      <form
        onSubmit={save}
        className="my-3.5 flex max-w-[42rem] flex-wrap items-center gap-x-4 gap-y-3 rounded-control border border-edge bg-paper p-4"
      >
        <span className="flex items-center gap-2">
          <Label htmlFor="quiet-from">{t("rhythm.quietFrom")}</Label>
          <Input
            id="quiet-from"
            type="time"
            required
            className="w-34"
            value={quietFrom}
            onChange={(event) => setQuietFrom(event.target.value)}
          />
        </span>
        <span className="flex items-center gap-2">
          <Label htmlFor="quiet-until">{t("rhythm.quietUntil")}</Label>
          <Input
            id="quiet-until"
            type="time"
            required
            className="w-34"
            value={quietUntil}
            onChange={(event) => setQuietUntil(event.target.value)}
          />
        </span>
        <span className="flex items-center gap-2">
          <Label htmlFor="cadence">{t("rhythm.cadence")}</Label>
          <Input
            id="cadence"
            type="number"
            required
            step={1}
            min={spacing.minCadenceMinutes}
            max={spacing.maxCadenceMinutes}
            className="w-26"
            value={cadence}
            onChange={(event) => setCadence(event.target.value)}
          />
          <span className="text-quiet">{t("rhythm.minutes")}</span>
        </span>
        {/* No day chosen means no afternoon, which is where every house starts. There is
            no count beside this and there will not be one: the days say when one may
            happen, and nothing keeps track of the ones that did. */}
        <fieldset className="flex w-full flex-wrap items-center gap-x-3 gap-y-2 border-0 p-0">
          <legend className="sr-only">{t("rhythm.afternoonDays")}</legend>
          <span className="text-quiet">{t("rhythm.afternoonDays")}</span>
          {spacing.dayChoices.map((day) => (
            <label key={day} className="flex items-center gap-1.5">
              <input
                type="checkbox"
                checked={days.includes(day)}
                onChange={(event) =>
                  setDays((chosen) =>
                    event.target.checked
                      ? [...chosen, day]
                      : chosen.filter((one) => one !== day),
                  )
                }
              />
              {weekday(day)}
            </label>
          ))}
        </fieldset>
        <span className="flex items-center gap-2">
          <Label htmlFor="afternoon-from">{t("rhythm.afternoonFrom")}</Label>
          <Input
            id="afternoon-from"
            type="time"
            required
            className="w-34"
            value={afternoonFrom}
            onChange={(event) => setAfternoonFrom(event.target.value)}
          />
        </span>
        <span className="flex items-center gap-2">
          <Label htmlFor="time-zone">{t("rhythm.timeZone")}</Label>
          <select
            id="time-zone"
            className="h-9 rounded-control border border-edge bg-paper px-2"
            value={timeZone}
            onChange={(event) => setTimeZone(event.target.value)}
          >
            <option value="">{t("rhythm.timeZoneNone")}</option>
            {zones.map((zone) => (
              <option key={zone} value={zone}>
                {zone}
              </option>
            ))}
          </select>
        </span>
        <Button type="submit" variant="primary" className="ml-auto flex-none">
          {t("rhythm.save")}
        </Button>
      </form>
      <div className="my-3.5 flex max-w-[42rem] flex-wrap items-center gap-3">
        <Button type="button" onClick={beginNow} className="flex-none">
          {t("rhythm.beginNow")}
        </Button>
        <Quiet aria-live="polite">{asked === null ? t("rhythm.beginNote") : t(asked)}</Quiet>
      </div>
      <Quiet>{t("rhythm.wakeNote")}</Quiet>
      <Quiet>{t("rhythm.afternoonNote")}</Quiet>
      <Quiet aria-live="polite">{status === null ? "" : t(status)}</Quiet>
    </>
  );
}

export function Rhythm() {
  const { t } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.rhythm());

  if (state.status === "loading") return <Quiet>{t("rhythm.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("rhythm.unreadable")}</Quiet>;
  return <Form spacing={state.data} />;
}
