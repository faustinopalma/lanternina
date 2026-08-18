/* The gallery.
 *
 * The bitmap cannot be fetched by putting the route in `src`: it needs the bearer token,
 * and an <img> sends no headers. So each tile fetches its own bytes and hands the element
 * a blob URL, which is also why the CSP has to allow `blob:` for images.
 *
 * What is shown is the rendered two-level image, not the model's original: judging a
 * picture from a smooth PNG would be judging something she never saw.
 */
import { useEffect, useRef, useState } from "react";

import { useApi } from "@/api/client";
import type { Picture } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { Label, Select } from "@/components/ui/field";
import { useWords } from "@/i18n";
import { readStored, writeStored } from "@/lib/stored";
import { useLoad } from "@/lib/useLoad";

const PAGE_SIZE_KEY = "lanternina.picturesPerPage";

function Tile({ picture }: { picture: Picture }) {
  const { t, dateTime } = useWords();
  const api = useApi();
  const frame = useRef<HTMLElement>(null);
  const [url, setUrl] = useState<string | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let live = true;
    let watcher: IntersectionObserver | null = null;

    const fetchBytes = async () => {
      try {
        const blob = await api.pictureContent(picture.id);
        if (live) setUrl(URL.createObjectURL(blob));
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
      className="m-0 overflow-hidden rounded-[--radius-control] border border-edge bg-paper"
    >
      {url !== null ? (
        <img
          src={url}
          alt={picture.theme || t("pictures.untitled")}
          /* Two levels and no greys: smoothing would show the parent something softer
             than the display does. */
          className="block h-auto w-full border-b border-edge bg-white [image-rendering:pixelated]"
        />
      ) : null}
      <figcaption className="flex flex-col gap-0.5 px-3 pt-2.5 pb-3 text-[0.85rem]">
        <strong className="font-semibold">{title}</strong>
        <span className="text-quiet">{dateTime(picture.createdAt)}</span>
        {failed ? <span className="text-quiet">{t("pictures.unavailable")}</span> : null}
      </figcaption>
    </figure>
  );
}

export function Pictures() {
  const { t } = useWords();
  const api = useApi();
  const [page, setPage] = useState(1);
  const [perPage, setPerPage] = useState(() => Number(readStored(PAGE_SIZE_KEY)) || 20);
  const [state] = useLoad(() => api.pictures(page, perPage), [page, perPage]);

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
        <span className="ml-auto flex gap-2">
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
      </div>

      {answer.pictures.length === 0 ? (
        <Quiet>{t("pictures.empty")}</Quiet>
      ) : (
        <div
          className="grid gap-4.5 [grid-template-columns:repeat(auto-fill,minmax(210px,1fr))]"
          aria-live="polite"
        >
          {answer.pictures.map((picture) => (
            <Tile key={picture.id} picture={picture} />
          ))}
        </div>
      )}
    </>
  );
}
