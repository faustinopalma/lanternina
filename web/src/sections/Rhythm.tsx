import { useEffect, useMemo, useState, type FormEvent } from "react";

import { useApi } from "@/api/client";
import type { Rhythm as Spacing } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Input, Label } from "@/components/ui/field";
import { useWords, type MessageKey } from "@/i18n";
import CITIES from "@/i18n/cities.json";
import { useLoad } from "@/lib/useLoad";
import { useUnsaved } from "@/lib/useUnsaved";

/** What a zone is called on the screen: the city, in the panel's language.
 *
 * `Europe/Rome` reads as a path and not as a place, and its last segment is English.
 * `Intl` will not translate it — of the things `Intl.DisplayNames` does, a timezone city
 * is not one, checked in a browser — so the names come from CLDR, which is the same data
 * the browsers are built on. `web/src/i18n/cities.json` holds only the ones that differ
 * from English, which is 92 of them in Italian and 3 KB; everything else falls back to
 * the database's own spelling, which is already English.
 */
export function cityOf(zone: string, language = "en"): string {
  const named = (CITIES as Record<string, Record<string, string>>)[language]?.[zone];
  if (named) return named;
  const parts = zone.split("/");
  const city = parts.length > 1 ? parts.slice(1).join(" · ") : zone;
  return city.replace(/_/g, " ");
}

/** Which country each zone belongs to, as an ISO code that has a name.
 *
 * There is no zone-to-country call, but there is a country-to-zones one, so this walks
 * the 676 two-letter codes and turns it round. Measured in a browser on 25 August 2026:
 * 273 codes answer and all 418 zones come back with a country.
 *
 * A code is only taken if it can be named. Several withdrawn ISO codes still claim zones
 * and sort earlier than the country everyone would look under — Riyadh came back as "NT",
 * the Neutral Zone, instead of Saudi Arabia, and Kiritimati as "CT". Six zones were
 * affected; requiring a name fixes all six and leaves none without a country.
 */
function regionOfZone(named: (code: string) => boolean): Map<string, string> {
  const found = new Map<string, string>();
  if (typeof new Intl.Locale("en").getTimeZones !== "function") return found;
  const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  for (const first of letters) {
    for (const second of letters) {
      const code = `${first}${second}`;
      if (!named(code)) continue;
      let zones: string[] | undefined;
      try {
        zones = new Intl.Locale(`und-${code}`).getTimeZones?.();
      } catch {
        continue;
      }
      for (const zone of zones ?? []) {
        if (!found.has(zone)) found.set(zone, code);
      }
    }
  }
  return found;
}

export interface Place {
  zone: string;
  label: string;
  /** The English spelling, when the language has its own. A parent who knows the zone as
   *  "Rome" must not fail to find it because the box now says "Roma". */
  alsoKnownAs: string;
}

/** Every zone the browser knows, as "City — Country", in alphabetical order.
 *
 * Sorted rather than gathered by offset, which is what this was until somebody pointed
 * out the obvious: finding Rome under UTC+02:00 means already knowing Rome is on UTC+2
 * today, and the offset is the thing being looked up. Italy is on +1 for five months of
 * the year, so the grouping asked the parent for the answer to their own question.
 *
 * `Intl.supportedValuesOf` is not in every engine, so the fallback is the browser's own
 * zone alone: one right answer beats an empty list, and the panel validates whatever
 * arrives anyway.
 */
export function placesIn(language: string): Place[] {
  const here = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const all =
    typeof Intl.supportedValuesOf === "function" ? Intl.supportedValuesOf("timeZone") : [here];
  let countryName: Intl.DisplayNames | null = null;
  try {
    countryName = new Intl.DisplayNames([language], { type: "region" });
  } catch {
    countryName = null;
  }
  // A code with no name of its own comes back as the code, which is how the unnamed ones
  // are told apart without a list of them here.
  const nameOf = (code: string) => countryName?.of(code) ?? code;
  const regions = regionOfZone((code) => nameOf(code) !== code);
  return all
    .map((zone) => {
      const region = regions.get(zone);
      const country = region ? nameOf(region) : "";
      const here = cityOf(zone, language);
      const english = cityOf(zone);
      return {
        zone,
        label: country ? `${here} — ${country}` : here,
        alsoKnownAs: english === here ? "" : english,
      };
    })
    .sort((a, b) => a.label.localeCompare(b.label, language));
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
  const [picturesFrom, setPicturesFrom] = useState(spacing.picturesFrom);
  const [picturesUntil, setPicturesUntil] = useState(spacing.picturesUntil);
  const [cadence, setCadence] = useState(String(spacing.cadenceMinutes));
  const [days, setDays] = useState<string[]>(spacing.afternoonDays);
  const [afternoonFrom, setAfternoonFrom] = useState(spacing.afternoonFrom);
  const [afternoonUntil, setAfternoonUntil] = useState(spacing.afternoonUntil);
  const [timeZone, setTimeZone] = useState(spacing.timeZone);
  const [wanted, setWanted] = useState(String(spacing.scriptsWanted));
  const [aDay, setADay] = useState(String(spacing.afternoonsADay));
  const [status, setStatus] = useState<MessageKey | null>(
    spacing.picturesFrom === spacing.picturesUntil ? "rhythm.picturesAllDay" : null,
  );
  const [asked, setAsked] = useState<MessageKey | null>(null);

  /* The browser has the list already, so it is not shipped from the panel. Built once per
   * language: it walks 676 country codes and sorts 418 places, which is cheap enough to
   * do on opening the section and far too much to do on every keystroke in this form. */
  const places = useMemo(() => placesIn(language), [language]);
  const byZone = useMemo(
    () => new Map(places.map((place) => [place.zone, place.label])),
    [places],
  );
  const byLabel = useMemo(
    () => new Map(places.map((place) => [place.label, place.zone])),
    [places],
  );
  /* What is in the box, which is a label and not a zone. Kept apart from `timeZone` so a
   * half-typed word is not a half-chosen setting: the zone only moves on a full match. */
  const [typed, setTyped] = useState(() => byZone.get(spacing.timeZone) ?? "");

  const { changed, saved } = useUnsaved({
    picturesFrom,
    picturesUntil,
    cadence,
    days,
    afternoonFrom,
    afternoonUntil,
    timeZone,
    wanted,
    aDay,
  });

  /* Saving persists a choice and returns. The house reads it on its next run and decides
   * for itself, so nothing here reaches into the room. */
  async function save(event: FormEvent) {
    event.preventDefault();
    try {
      await api.saveRhythm({
        picturesFrom,
        picturesUntil,
        cadenceMinutes: Number(cadence),
        afternoonDays: days,
        afternoonFrom,
        afternoonUntil,
        timeZone,
        scriptsWanted: Number(wanted),
        afternoonsADay: Number(aDay),
      });
      saved();
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
        className="my-3.5 flex max-w-[42rem] flex-col gap-5 rounded-control border border-edge bg-paper p-4"
      >
        {/* The clock first: everything below is an hour, and an hour means nothing until
            the house knows which clock it is on. */}
        <fieldset className="flex flex-col gap-2 border-0 p-0">
          <legend className="mb-1 font-medium">{t("rhythm.clockSection")}</legend>
          <span className="flex flex-wrap items-center gap-2">
            <Label htmlFor="time-zone">{t("rhythm.timeZone")}</Label>
            {/* A text box with a list rather than a dropdown of 418: alphabetical, and the
                parent types the first letters of their city instead of scrolling to it. */}
            <Input
              id="time-zone"
              list="the-places"
              className="w-64"
              placeholder={t("rhythm.timeZonePlaceholder")}
              value={typed}
              onChange={(event) => {
                const wrote = event.target.value;
                setTyped(wrote);
                if (wrote === "") setTimeZone("");
                else {
                  const found = byLabel.get(wrote);
                  if (found) setTimeZone(found);
                }
              }}
            />
            <datalist id="the-places">
              {/* The English spelling goes in the label, which browsers search as well as
                  the value: somebody who knows the zone as "Rome" still finds Roma. */}
              {places.map((place) => (
                <option key={place.zone} value={place.label} label={place.alsoKnownAs} />
              ))}
            </datalist>
            {/* The confirmation. A timezone cannot be checked by reading it back, so the
                house's own clock is put next to it and left running. */}
            <span aria-live="off" className="text-quiet tabular-nums">
              {timeZone && byZone.get(timeZone) === typed ? (
                <ThereNow zone={timeZone} locale={language} />
              ) : (
                t("rhythm.timeZoneUnknown")
              )}
            </span>
          </span>
          <Quiet>{t("rhythm.timeZoneNote")}</Quiet>
        </fieldset>

        {/* The hours a picture may change, said as hours it may — not as a pause. Until
            25 August 2026 this was a "pause" sitting above the afternoon controls, and a
            parent could not tell which of the two it bounded. */}
        <fieldset className="flex flex-col gap-2 border-0 p-0">
          <legend className="mb-1 font-medium">{t("rhythm.picturesSection")}</legend>
          <span className="flex flex-wrap items-center gap-x-4 gap-y-3">
            <span className="flex items-center gap-2">
              <Label htmlFor="pictures-from">{t("rhythm.picturesFrom")}</Label>
              <Input
                id="pictures-from"
                type="time"
                required
                className="w-34"
                value={picturesFrom}
                onChange={(event) => setPicturesFrom(event.target.value)}
              />
            </span>
            <span className="flex items-center gap-2">
              <Label htmlFor="pictures-until">{t("rhythm.picturesUntil")}</Label>
              <Input
                id="pictures-until"
                type="time"
                required
                className="w-34"
                value={picturesUntil}
                onChange={(event) => setPicturesUntil(event.target.value)}
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
          </span>
          <Quiet>{t("rhythm.wakeNote")}</Quiet>
        </fieldset>

        {/* No day chosen means no afternoon, which is where every house starts. The count
            beside it is a ceiling on the day and not a record: the house keeps the number,
            resets it at midnight and sends it to nobody, and this field only says how high
            it may go. */}
        <fieldset className="flex flex-col gap-2 border-0 p-0">
          <legend className="mb-1 font-medium">{t("rhythm.afternoonSection")}</legend>
          <span className="flex flex-wrap items-center gap-x-3 gap-y-2">
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
          </span>
          <span className="flex flex-wrap items-center gap-x-4 gap-y-3">
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
              <Label htmlFor="afternoon-until">{t("rhythm.afternoonUntil")}</Label>
              <Input
                id="afternoon-until"
                type="time"
                required
                className="w-34"
                value={afternoonUntil}
                onChange={(event) => setAfternoonUntil(event.target.value)}
              />
            </span>
          </span>
          <Quiet>{t("rhythm.afternoonNote")}</Quiet>
          <span className="flex items-center gap-2">
            <Label htmlFor="afternoons-a-day">{t("rhythm.aDay")}</Label>
            <Input
              id="afternoons-a-day"
              type="number"
              required
              className="w-24"
              min={spacing.minAfternoonsADay}
              max={spacing.maxAfternoonsADay}
              value={aDay}
              onChange={(event) => setADay(event.target.value)}
            />
          </span>
          <Quiet>{t("rhythm.aDayNote")}</Quiet>
          <span className="flex items-center gap-2">
            <Label htmlFor="scripts-wanted">{t("rhythm.wanted")}</Label>
            <Input
              id="scripts-wanted"
              type="number"
              required
              className="w-24"
              min={spacing.minScriptsWanted}
              max={spacing.maxScriptsWanted}
              value={wanted}
              onChange={(event) => setWanted(event.target.value)}
            />
          </span>
          <Quiet>{t("rhythm.wantedNote")}</Quiet>
        </fieldset>

        {/* The button is the confirmation. Grey means the house has what is on the screen;
            the sentence beside it says what the house will do with it. A confirmation is
            about the values that were saved, so editing again takes it away — a refusal
            stays, because nothing was saved and the parent still has to know. */}
        <span className="flex flex-wrap items-center justify-end gap-3">
          <Quiet aria-live="polite" className="text-right">
            {status === null || (changed && status !== "rhythm.saveFailed") ? "" : t(status)}
          </Quiet>
          <Button type="submit" variant="primary" disabled={!changed} className="flex-none">
            {t("rhythm.save")}
          </Button>
        </span>
      </form>
      <div className="my-3.5 flex max-w-[42rem] flex-wrap items-center gap-3">
        <Button type="button" onClick={beginNow} className="flex-none">
          {t("rhythm.beginNow")}
        </Button>
        <Quiet aria-live="polite">{asked === null ? t("rhythm.beginNote") : t(asked)}</Quiet>
      </div>
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
