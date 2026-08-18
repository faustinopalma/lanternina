import { useApi } from "@/api/client";
import type { Device } from "@/api/types";
import { Quiet } from "@/components/ui/card";
import { useWords, type MessageKey } from "@/i18n";
import { useLoad } from "@/lib/useLoad";

const KNOWN_LEVELS = ["mains", "ok", "low", "critical"];

function Row({ device }: { device: Device }) {
  const { t, ago } = useWords();

  const level = KNOWN_LEVELS.includes(device.level)
    ? t(`level.${device.level}` as MessageKey)
    : device.level;

  /* Deliberately vague: the board has no fuel gauge, so a percentage would be arithmetic
   * performed on a guess. */
  const since = device.silent
    ? t("devices.silent")
    : device.silentSeconds < 120
      ? t("devices.justNow")
      : t("devices.heard", { ago: ago(device.silentSeconds) });

  return (
    <div className="flex items-center justify-between gap-3 border-b border-edge py-3 last:border-b-0">
      <div className="flex flex-col gap-0.5">
        <strong className="font-semibold">{device.name}</strong>
        <span className="text-[0.92rem] text-quiet">
          {level} {"\u00b7"} {since}
        </span>
      </div>
      {device.silent ? (
        <span className="text-[0.92rem] whitespace-nowrap text-focus">{t("devices.check")}</span>
      ) : null}
    </div>
  );
}

export function Devices() {
  const { t } = useWords();
  const api = useApi();
  const [state] = useLoad(() => api.devices());

  if (state.status === "loading") return <Quiet>{t("devices.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("devices.unreadable")}</Quiet>;
  if (state.data.length === 0) return <Quiet>{t("devices.empty")}</Quiet>;

  return (
    <div aria-live="polite">
      {state.data.map((device) => (
        <Row key={device.id} device={device} />
      ))}
    </div>
  );
}
