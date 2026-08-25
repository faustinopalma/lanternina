/* The gallery.
 *
 * The bitmap cannot be fetched by putting the route in `src`: it needs the bearer token,
 * and an <img> sends no headers. So each tile fetches its own bytes and hands the element
 * a blob URL, which is also why the CSP has to allow `blob:` for images.
 *
 * What is shown is the rendered two-level image, not the model's original: judging a
 * picture from a smooth PNG would be judging something that was never on the display.
 */
import { zip } from "fflate";
import { useEffect, useRef, useState } from "react";

import { useApi } from "@/api/client";
import type { Picture } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Input, Label, Select } from "@/components/ui/field";
import { useWords } from "@/i18n";
import { readStored, writeStored } from "@/lib/stored";
import { useLoad } from "@/lib/useLoad";

const PAGE_SIZE_KEY = "lanternina.picturesPerPage";

/* A name that sorts by when the picture was shown. The id is kept on the end because two
 * pictures can share a minute and a theme, and a zip cannot hold the same name twice. */
export function fileName(picture: Picture): string {
  const when = new Date(picture.createdAt * 1000);
  const two = (value: number) => String(value).padStart(2, "0");
  const stamp =
    `${when.getFullYear()}-${two(when.getMonth() + 1)}-${two(when.getDate())}` +
    `-${two(when.getHours())}${two(when.getMinutes())}`;
  // Letters, digits, spaces and dashes survive; a run of anything a file system argues
  // about becomes one space.
  const theme = picture.theme
    .replace(/[^\p{L}\p{N} _-]+/gu, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 60);
  return `${stamp}${theme === "" ? "" : ` ${theme}`} ${picture.id}.bmp`;
}

/* Hand the bytes to the browser's own download. The object URL is released later rather
 * than at once: revoking it in the same tick cuts the save short in some browsers. */
function save(blob: Blob, name: string) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = name;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 10_000);
}

/* A day as the date field writes it, in the parent's own zone rather than in UTC. */
function asDay(when: Date): string {
  const two = (value: number) => String(value).padStart(2, "0");
  return `${when.getFullYear()}-${two(when.getMonth() + 1)}-${two(when.getDate())}`;
}

function aWeekAgo(): string {
  const when = new Date();
  when.setDate(when.getDate() - 7);
  return asDay(when);
}

/* Midnight of that day where the parent is, in seconds. An unreadable field reaches back
 * to the beginning rather than forward, so a slip gathers too much and never too little. */
function dayStart(day: string): number {
  const at = new Date(`${day}T00:00:00`);
  return Number.isNaN(at.getTime()) ? 0 : at.getTime() / 1000;
}

type Gathering =
  | { at: "idle" }
  | { at: "walking"; done: number }
  | { at: "empty" }
  | { at: "failed" };

function Tile({
  picture,
  standing,
  onOpen,
}: {
  picture: Picture;
  standing: string | null;
  onOpen: (picture: Picture, bytes: Blob) => void;
}) {
  const { t, dateTime } = useWords();
  const api = useApi();
  const frame = useRef<HTMLElement>(null);
  const [url, setUrl] = useState<string | null>(null);
  const [bytes, setBytes] = useState<Blob | null>(null);
  const [failed, setFailed] = useState(false);
  const [asked, setAsked] = useState<boolean | null>(null);

  useEffect(() => {
    let live = true;
    let watcher: IntersectionObserver | null = null;

    const fetchBytes = async () => {
      try {
        const blob = await api.pictureContent(picture.id);
        if (live) {
          setBytes(blob);
          setUrl(URL.createObjectURL(blob));
        }
      } catch {
        if (live) setFailed(true);
      }
    };

    // Bytes are fetched when a tile comes into view, so opening the gallery costs one
    // small listing rather than tens of megabytes of bitmaps.
    const node = frame.current;
    if (node !== null && typeof IntersectionObserver !== "undefined") {
      watcher = new IntersectionObserver(
        (entries) => {
          if (!entries.some((entry) => entry.isIntersecting)) return;
          watcher?.disconnect();
          void fetchBytes();
        },
        { rootMargin: "200px" },
      );
      watcher.observe(node);
    } else {
      void fetchBytes();
    }

    return () => {
      live = false;
      watcher?.disconnect();
    };
  }, [api, picture.id]);

  useEffect(() => () => void (url !== null && URL.revokeObjectURL(url)), [url]);

  // Written out rather than built from the value, so a missing entry is caught by the
  // tests instead of appearing to a parent as a raw key.
  let title = picture.theme || t("pictures.untitled");
  if (picture.kind === "low") title = t("pictures.kind.low");
  if (picture.kind === "critical") title = t("pictures.kind.critical");

  return (
    <figure
      ref={frame}
      className="m-0 overflow-hidden rounded-control border border-edge bg-paper"
    >
      {/* The tile holds the display's own proportions before the bytes arrive, so the
          grid does not jump as the pictures come in one by one. */}
      <div className="aspect-[5/3] border-b border-edge bg-white">
        {url !== null && bytes !== null ? (
          <button
            type="button"
            className="block h-full w-full cursor-zoom-in border-0 bg-transparent p-0"
            aria-label={t("pictures.enlarge")}
            title={t("pictures.enlarge")}
            onClick={() => onOpen(picture, bytes)}
          >
            <img
              src={url}
              alt={picture.theme || t("pictures.untitled")}
              /* Two levels and no greys: smoothing would show the parent something softer
                 than the display does. */
              className="h-full w-full object-contain [image-rendering:pixelated]"
            />
          </button>
        ) : null}
      </div>
      <figcaption className="flex flex-col gap-0.5 px-3 pt-2.5 pb-3 text-[0.85rem]">
        <strong className="font-semibold">{title}</strong>
        <span className="text-quiet">{dateTime(picture.createdAt)}</span>
        {failed ? <span className="text-quiet">{t("pictures.unavailable")}</span> : null}
        {/* The button writes a row and stops. What it says afterwards is what actually
            happens: the house puts the picture up when it next changes it, which the
            panel cannot hurry. */}
        <span className="mt-1.5 flex flex-col gap-1">
          <Button
            size="small"
            disabled={asked === true || standing === picture.id}
            onClick={async () => {
              try {
                await api.askAgain(picture.id);
                setAsked(true);
              } catch {
                setAsked(false);
              }
            }}
          >
            {t("pictures.again")}
          </Button>
          {asked === true || standing === picture.id ? (
            <span className="text-quiet">{t("pictures.again.asked")}</span>
          ) : null}
          {asked === false ? (
            <span className="text-quiet">{t("pictures.again.failed")}</span>
          ) : null}
        </span>
      </figcaption>
    </figure>
  );
}

/* The picture on its own, as large as the window allows. A native dialog is used so that
 * Escape closes it and the rest of the page stops taking clicks, without writing either. */
function Enlarged({
  picture,
  bytes,
  onClose,
}: {
  picture: Picture;
  bytes: Blob;
  onClose: () => void;
}) {
  const { t, dateTime } = useWords();
  const frame = useRef<HTMLDialogElement>(null);
  const [url, setUrl] = useState<string | null>(null);

  useEffect(() => {
    const made = URL.createObjectURL(bytes);
    setUrl(made);
    return () => URL.revokeObjectURL(made);
  }, [bytes]);

  useEffect(() => {
    const node = frame.current;
    if (node === null) return;
    // Where the modal behaviour is missing (jsdom, older browsers) the picture still opens;
    // what is lost is the backdrop and Escape, not the picture.
    if (typeof node.showModal === "function") node.showModal();
    else node.open = true;
  }, []);

  return (
    <dialog
      ref={frame}
      onClose={onClose}
      onClick={(event) => {
        // Clicking the backdrop lands on the dialog itself, never on its children.
        if (event.target === frame.current) frame.current?.close();
      }}
      className="max-h-[92vh] max-w-[96vw] rounded-control border border-edge bg-paper p-0 backdrop:bg-black/60"
    >
      <div className="flex max-h-[92vh] flex-col">
        <div className="min-h-0 flex-1 bg-white p-2">
          {url !== null ? (
            <img
              src={url}
              alt={picture.theme || t("pictures.untitled")}
              className="max-h-[74vh] w-auto max-w-full object-contain [image-rendering:pixelated]"
            />
          ) : null}
        </div>
        <div className="flex flex-wrap items-center gap-x-4 gap-y-2 border-t border-edge px-3 py-2.5 text-[0.85rem]">
          <span className="flex flex-col gap-0.5">
            <strong className="font-semibold">
              {picture.theme || t("pictures.untitled")}
            </strong>
            <span className="text-quiet">{dateTime(picture.createdAt)}</span>
          </span>
          <span className="ml-auto flex gap-2">
            <Button size="small" onClick={() => save(bytes, fileName(picture))}>
              {t("pictures.download")}
            </Button>
            <Button size="small" onClick={() => frame.current?.close()}>
              {t("pictures.close")}
            </Button>
          </span>
        </div>
      </div>
    </dialog>
  );
}

export function Pictures() {
  const { t } = useWords();
  const api = useApi();
  const [page, setPage] = useState(1);
  const [perPage, setPerPage] = useState(() => Number(readStored(PAGE_SIZE_KEY)) || 20);
  const [state] = useLoad(() => api.pictures(page, perPage), [page, perPage]);
  // Which picture the house has not yet come to collect, so a parent who reloads sees the
  // request they already made instead of a button that looks unpressed.
  const [request] = useLoad(() => api.standingRequest(), []);
  const standing =
    request.status === "ready" && request.data !== null ? request.data.subject : null;
  const [open, setOpen] = useState<{ picture: Picture; bytes: Blob } | null>(null);
  const [since, setSince] = useState(() => aWeekAgo());
  const [gathering, setGathering] = useState<Gathering>({ at: "idle" });

  const downloadSince = async (step: number) => {
    const from = dayStart(since);
    setGathering({ at: "walking", done: 0 });
    const files: Record<string, Uint8Array> = {};
    try {
      // The listing is paged and comes newest first, so the walk stops at the first
      // picture older than the chosen day rather than reading the rest of the archive.
      // Bytes are fetched one at a time: this runs in the background of a parent's
      // evening, and a burst of parallel requests would buy nothing.
      let reached = false;
      for (let wanted = 1; !reached; wanted += 1) {
        const shown = await api.pictures(wanted, step);
        for (const picture of shown.pictures) {
          if (picture.createdAt < from) {
            reached = true;
            break;
          }
          const blob = await api.pictureContent(picture.id);
          files[fileName(picture)] = new Uint8Array(await blob.arrayBuffer());
          setGathering({ at: "walking", done: Object.keys(files).length });
        }
        if (shown.page >= shown.pages) reached = true;
      }
      if (Object.keys(files).length === 0) {
        setGathering({ at: "empty" });
        return;
      }
      const packed = await new Promise<Uint8Array>((resolve, reject) => {
        // Level 0: a bitmap of two levels is already small, and packing costs more than
        // it saves on a phone.
        zip(files, { level: 0 }, (error, data) => (error ? reject(error) : resolve(data)));
      });
      save(
        new Blob([packed as BlobPart], { type: "application/zip" }),
        t("pictures.zipName", { since }),
      );
      setGathering({ at: "idle" });
    } catch {
      setGathering({ at: "failed" });
    }
  };

  if (state.status === "loading") return <Quiet>{t("pictures.loading")}</Quiet>;
  if (state.status === "failed") return <Quiet>{t("pictures.unreadable")}</Quiet>;

  const answer = state.data;

  return (
    <>
      {/* The pager sits above the pictures, so the parent knows how much there is before
          scrolling rather than after. */}
      <div className="mt-4 mb-4.5 flex flex-wrap items-center gap-x-4 gap-y-2.5 border-b border-edge pb-3.5">
        <span className="flex items-center gap-2">
          <Label htmlFor="pictures-per-page">{t("pictures.perPage")}</Label>
          <Select
            id="pictures-per-page"
            value={String(answer.perPage)}
            onChange={(event) => {
              // Changing how many fit on a page moves the parent to the first one: keeping
              // the number would land them somewhere they were not looking.
              setPerPage(Number(event.target.value));
              setPage(1);
              writeStored(PAGE_SIZE_KEY, event.target.value);
            }}
          >
            {answer.pageSizes.map((size) => (
              <option key={size} value={size}>
                {size}
              </option>
            ))}
          </Select>
        </span>
        <span className="text-quiet" aria-live="polite">
          {t("pictures.pageOf", {
            page: answer.page,
            pages: answer.pages,
            total: answer.total,
          })}
        </span>
        {/* The three read as one control. Kept apart, the button looked like a second,
            unrelated thing and nobody could tell it was the date it would act on. */}
        <span className="ml-auto flex items-center gap-2 rounded-control border border-edge bg-paper px-2.5 py-1.5">
          <Label htmlFor="pictures-since" className="mb-0">
            {t("pictures.since")}
          </Label>
          <Input
            id="pictures-since"
            type="date"
            value={since}
            max={asDay(new Date())}
            onChange={(event) => setSince(event.target.value)}
          />
          <Button
            size="small"
            disabled={answer.total === 0 || gathering.at === "walking" || since === ""}
            /* The largest page the archive offers: a size it does not know falls back to
               the default, which would walk the gallery in more steps than needed. */
            onClick={() => void downloadSince(Math.max(...answer.pageSizes))}
          >
            {t("pictures.downloadSince")}
          </Button>
        </span>
        <span className="flex gap-2">
          <Button
            size="small"
            disabled={answer.page <= 1}
            onClick={() => setPage(Math.max(1, answer.page - 1))}
          >
            {t("pictures.previous")}
          </Button>
          <Button
            size="small"
            disabled={answer.page >= answer.pages}
            onClick={() => setPage(answer.page + 1)}
          >
            {t("pictures.next")}
          </Button>
        </span>
        {gathering.at === "idle" ? null : (
          <span className="w-full text-quiet" aria-live="polite">
            {gathering.at === "failed" ? t("pictures.downloadSince.failed") : null}
            {gathering.at === "empty" ? t("pictures.downloadSince.none") : null}
            {gathering.at === "walking"
              ? t("pictures.downloadSince.gathering", { done: gathering.done })
              : null}
          </span>
        )}
      </div>

      {answer.pictures.length === 0 ? (
        <Quiet>{t("pictures.empty")}</Quiet>
      ) : (
        <div
          className="grid gap-4.5 [grid-template-columns:repeat(auto-fill,minmax(210px,1fr))]"
          aria-live="polite"
        >
          {answer.pictures.map((picture) => (
            <Tile
              key={picture.id}
              picture={picture}
              standing={standing}
              onOpen={(shown, bytes) => setOpen({ picture: shown, bytes })}
            />
          ))}
        </div>
      )}

      {open !== null ? (
        <Enlarged
          picture={open.picture}
          bytes={open.bytes}
          onClose={() => setOpen(null)}
        />
      ) : null}
    </>
  );
}
