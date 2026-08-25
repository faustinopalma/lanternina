import { useEffect, useMemo, useState, type FormEvent } from "react";

import { useApi } from "@/api/client";
import type { Rhythm as Spacing } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Input, Label } from "@/components/ui/field";
import { useWords, type MessageKey } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

/** What a zone is called on the screen: the city, not the identifier.
 *
 * `Europe/Rome` reads as a path and not as a place, and the last segment carries an
 * underscore where a space belongs. There is no way to ask the browser for "Roma" — of
 * the things `Intl.DisplayNames` translates, a timezone city is not one — so the city
 * keeps its own spelling and the offset beside it does the work of identifying it. */
export function cityOf(zone: string): string {
  const parts = zone.split("/");
  const city = parts.length > 1 ? parts.slice(1).join(" · ") : zone;
  return city.replace(/_/g, " ");
}

/** How far this zone is from UTC right now, in minutes.
 *
 * Read out of a formatted date rather than computed, so it is whatever the browser's own
 * database says today: summer time is already in it, and it moves on the day the clocks
 * do without anything here knowing the rules. */
export function offsetNow(zone: string, at: Date): number {
  const shown = new Intl.DateTimeFormat("en-US", {
    timeZone: zone,
    timeZoneName: "longOffset",
  })
    .formatToParts(at)
    .find((part) => part.type === "timeZoneName")?.value;
  const found = /GMT([+-])(\d{2}):(\d{2})/.exec(shown ?? "");
  if (!found) return 0;
  const minutes = Number(found[2]) * 60 + Number(found[3]);
  return found[1] === "-" ? -minutes : minutes;
}

function offsetLabel(minutes: number): string {
  const sign = minutes < 0 ? "−" : "+";
  const size = Math.abs(minutes);
  return `UTC${sign}${String(Math.floor(size / 60)).padStart(2, "0")}:${String(size % 60).padStart(2, "0")}`;
}

/** Every zone the browser knows, gathered by what the clock says there right now.
 *
 * Grouped rather than listed because 418 identifiers in database order put Rome pages
 * away from Paris, which is where a parent looking for one of them starts. Cities that
 * agree on the hour sit together, which is also the check the parent is really making.
 *
 * `Intl.supportedValuesOf` is not in every engine, so the fallback is the browser's own
 * zone alone: one right answer beats an empty list, and the panel validates whatever
 * arrives anyway. */
function zonesByOffset(at: Date): { minutes: number; label: string; zones: string[] }[] {
  const here = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const all =
    typeof Intl.supportedValuesOf === "function" ? Intl.supportedValuesOf("timeZone") : [here];
  const grouped = new Map<number, string[]>();
  for (const zone of all) {
    const minutes = offsetNow(zone, at);
    const kept = grouped.get(minutes);
    if (kept) kept.push(zone);
    else grouped.set(minutes, [zone]);
  }
  return [...grouped.entries()]
    .sort(([a], [b]) => a - b)
    .map(([minutes, zones]) => ({
      minutes,
      label: offsetLabel(minutes),
      zones: zones.sort((a, b) => cityOf(a).localeCompare(cityOf(b))),
    }));
}

/** The time where the house is, ticking, so the parent can check it against a clock in
 *  the room. That is the whole reason it is here: a timezone is a setting nobody can
 *  verify by reading it back. */
function ThereNow({ zone, locale }: { zone: string; locale: string }) {
  const [at, setAt] = useState(() => new Date());
  useEffect(() => {
    const beat = window.setInterval(() => setAt(new Date()), 1000);
    return () => window.clearInterval(beat);
  }, []);

  const shown = new Intl.DateTimeFormat(locale, {
    timeZone: zone,
    weekday: "long",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    timeZoneName: "short",
  }).format(at);
  return <>{shown}</>;
}

/* The form takes what was read as a prop, so the fields hold the parent's choice from the
 * first paint. Copying it in afterwards showed an empty form for a moment, which reads as
 * "nothing has been chosen yet". */
function Form({ spacing }: { spacing: Spacing }) {
  const { t, weekday, language } = useWords();
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

  /* The browser has the list already, so it is not shipped from the panel. Built once:
   * it asks the date formatter for an offset 418 times, which is cheap enough to do and
   * far too much to do on every keystroke elsewhere in this form. */
  const groups = useMemo(() => zonesByOffset(new Date()), []);

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
        <span className="flex w-full flex-wrap items-center gap-2">
          <Label htmlFor="time-zone">{t("rhythm.timeZone")}</Label>
          <select
            id="time-zone"
            className="h-9 max-w-full rounded-control border border-edge bg-paper px-2"
            value={timeZone}
            onChange={(event) => setTimeZone(event.target.value)}
          >
            <option value="">{t("rhythm.timeZoneNone")}</option>
            {/* Gathered by what the clock says there now, so the cities that agree on the
                hour sit together — which is the comparison the parent is making. */}
            {groups.map((group) => (
              <optgroup key={group.minutes} label={group.label}>
                {group.zones.map((zone) => (
                  <option key={zone} value={zone}>
                    {cityOf(zone)}
                  </option>
                ))}
              </optgroup>
            ))}
          </select>
          {/* The confirmation. A timezone cannot be checked by reading it back, so the
              house's own clock is put next to it and left running. */}
          <span aria-live="off" className="text-quiet tabular-nums">
            {timeZone ? (
              <ThereNow zone={timeZone} locale={language} />
            ) : (
              t("rhythm.timeZoneUnknown")
            )}
          </span>
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
      <Quiet>{t("rhythm.timeZoneNote")}</Quiet>
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
