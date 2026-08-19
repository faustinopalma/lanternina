import { useState } from "react";

import { useApi } from "@/api/client";
import type { Device, NewAssignment } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Input, Select } from "@/components/ui/field";
import { useWords, type MessageKey } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

const KNOWN_LEVELS = ["mains", "ok", "low", "critical"];
const KNOWN_KINDS = ["display", "printer", "scanner"];
const KNOWN_JOBS = ["picture", "sheet", "print", "scan"];

/* A key the panel does not have yet would otherwise be drawn as the key itself. Falling
 * back to a word we do have keeps a hub that reports something new from looking broken. */
function known(list: string[], value: string, prefix: string, fallback: MessageKey): MessageKey {
  return list.includes(value) ? (`${prefix}.${value}` as MessageKey) : fallback;
}

function Row({ device, nameLimit }: { device: Device; nameLimit: number }) {
  const { t, ago } = useWords();
  const api = useApi();
  const [name, setName] = useState(device.name);
  const [job, setJob] = useState(device.job);
  const [problem, setProblem] = useState<MessageKey | null>(null);

  /* Saving persists a choice and returns. Nothing is printed and nothing is scanned: the
   * hub reads the list on its next report and decides for itself. */
  async function save(assignment: NewAssignment) {
    setProblem(null);
    try {
      await api.assignDevice(device.id, assignment);
    } catch {
      setProblem("devices.saveFailed");
    }
  }

  const kind = t(known(KNOWN_KINDS, device.kind, "kind", "kind.display"));
  /* Deliberately vague: the board has no fuel gauge, so a percentage would be arithmetic
   * performed on a guess. A printer has no charge to report at all. */
  const level =
    device.level === undefined ? null : t(known(KNOWN_LEVELS, device.level, "level", "level.ok"));
  const since = device.silent
    ? t("devices.silent")
    : device.silentSeconds < 120
      ? t("devices.justNow")
      : t("devices.heard", { ago: ago(device.silentSeconds) });

  return (
    <div className="flex flex-col gap-2.5 py-3.5">
      <div className="flex flex-wrap items-baseline justify-between gap-x-3">
        <strong className="font-semibold">{device.label || device.id}</strong>
        <span className="text-[0.92rem] text-quiet">
          {kind}
          {level === null ? "" : ` \u00b7 ${level}`} {"\u00b7"} {since}
        </span>
      </div>
      <div className="flex flex-wrap items-center gap-2.5">
        <Input
          className="min-w-0 flex-auto"
          maxLength={nameLimit}
          autoComplete="off"
          aria-label={t("devices.nameAria")}
          placeholder={t("devices.namePlaceholder")}
          value={name}
          onChange={(event) => setName(event.target.value)}
          onBlur={() => {
            if (name !== device.name) void save({ name });
          }}
        />
        <Select
          className="flex-none"
          aria-label={t("devices.jobAria")}
          value={job}
          onChange={(event) => {
            setJob(event.target.value);
            void save({ job: event.target.value });
          }}
        >
          <option value="">{t("devices.noJob")}</option>
          {device.jobChoices.map((choice) => (
            <option key={choice} value={choice}>
              {t(known(KNOWN_JOBS, choice, "job", "devices.noJob"))}
            </option>
          ))}
        </Select>
      </div>
      {problem === null ? <></> : <Quiet>{t(problem)}</Quiet>}
      {device.silent ? <span className="text-[0.92rem] text-focus">{t("devices.check")}</span> : <></>}
    </div>
  );
}

export function Devices() {
  const { t } = useWords();
  const api = useApi();
  const [state, reload] = useLoad(() => api.devices());
  const [removing, setRemoving] = useState<string | null>(null);

  if (state.status === "loading") return <Quiet>{t("devices.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("devices.unreadable")}</Quiet>;
  if (state.data.devices.length === 0) return <Quiet>{t("devices.empty")}</Quiet>;

  const { devices, nameLimit } = state.data;

  return (
    <div aria-live="polite">
      <Quiet>{t("devices.nameNote", { limit: nameLimit })}</Quiet>
      {devices.map((device) => (
        <div
          key={device.id}
          className="flex items-start gap-3 border-b border-edge last:border-b-0"
        >
          <div className="min-w-0 flex-auto">
            <Row device={device} nameLimit={nameLimit} />
          </div>
          <Button
            size="small"
            className="mt-4 flex-none"
            disabled={removing === device.id}
            title={t("devices.removeTitle", { name: device.name || device.label || device.id })}
            onClick={async () => {
              // Nothing leaves the list for going quiet, so this is the only way out —
              // and it is a decision somebody took, not something that happened.
              setRemoving(device.id);
              await api.removeDevice(device.id).catch(() => null);
              setRemoving(null);
              reload();
            }}
          >
            {t("devices.remove")}
          </Button>
        </div>
      ))}
    </div>
  );
}
