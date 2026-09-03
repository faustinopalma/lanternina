import { Menu, X } from "lucide-react";
import { useEffect, useState, type ComponentType } from "react";

import { ApiProvider } from "@/api/client";
import type { Api } from "@/api/types";
import { Boundary } from "@/components/Boundary";
import { LimitReached } from "@/components/LimitReached";
import { Button } from "@/components/ui/button";
import { Quiet } from "@/components/ui/card";
import { useWords } from "@/i18n";
import { cn } from "@/lib/utils";
import { Devices } from "@/sections/Devices";
import { Drafts } from "@/sections/Drafts";
import { Experiences } from "@/sections/Experiences";
import { Guidelines } from "@/sections/Guidelines";
import { Pictures } from "@/sections/Pictures";
import { Preferences } from "@/sections/Preferences";
import { Proposals } from "@/sections/Proposals";
import { Reminders } from "@/sections/Reminders";
import { Rhythm } from "@/sections/Rhythm";
import { Themes } from "@/sections/Themes";
import { TheTrail } from "@/sections/Trail";
import { Usage } from "@/sections/Usage";
import { Verdicts } from "@/sections/Verdicts";

interface Section {
  name: string;
  title: string;
  note: string;
  Body: ComponentType;
}

interface Group {
  name: string;
  title: string;
  sections: Section[];
}

/* One page for everything waiting on a decision. They were two, and a parent could not
 * tell them apart because the difference is not in what they ask of the reader: an
 * activity is a whole afternoon devised in the cloud, a proposal is one piece of content
 * sealed on the device, and nothing on the hub has submitted one of the second kind since
 * the afternoons arrived. So the live one is the page, and the older one appears inside it
 * if it ever has anything. */
function WaitingForYou() {
  return (
    <>
      <Experiences />
      <Proposals />
    </>
  );
}

/* Which section is open lives in the address bar, not only in state.
 *
 * Reloading is something a parent does — the API scales to zero and a cold start can leave a
 * section saying it cannot read anything — and until this was here, reloading also threw them
 * back to the first page. Losing your place is a worse fault than the one that made you
 * reload. It also makes the back button do what it looks like it does. */
function opened(): string {
  return window.location.hash.replace(/^#/, "");
}

export function Dashboard({ api }: { api: Api }) {
  const { t } = useWords();
  const [current, setCurrent] = useState(() => opened() || "experiences");
  const [drawerOpen, setDrawerOpen] = useState(false);

  // Written out one by one rather than built from the name: a key that only exists at
  // runtime is a key no test can find missing. The four groups answer four different
  // questions — what wants an answer now, what the house has to say, how it should
  // behave, what it is made of — and a flat list of ten made all four look alike.
  const groups: Group[] = [
    {
      name: "decide",
      title: t("menu.group.decide"),
      sections: [
        {
          name: "experiences",
          title: t("experiences.title"),
          note: t("experiences.note"),
          Body: WaitingForYou,
        },
        {
          name: "drafts",
          title: t("drafts.title"),
          note: t("drafts.note"),
          Body: Drafts,
        },
      ],
    },
    {
      name: "content",
      title: t("menu.group.content"),
      sections: [
        { name: "themes", title: t("themes.title"), note: t("themes.note"), Body: Themes },
        {
          name: "pictures",
          title: t("pictures.title"),
          note: t("pictures.note"),
          Body: Pictures,
        },
        {
          name: "reminders",
          title: t("reminders.title"),
          note: t("reminders.note"),
          Body: Reminders,
        },
      ],
    },
    {
      name: "settings",
      title: t("menu.group.settings"),
      sections: [
        { name: "rhythm", title: t("rhythm.title"), note: t("rhythm.note"), Body: Rhythm },
        {
          name: "preferences",
          title: t("preferences.title"),
          note: t("preferences.note"),
          Body: Preferences,
        },
        {
          name: "guidelines",
          title: t("guidelines.title"),
          note: t("guidelines.note"),
          Body: Guidelines,
        },
      ],
    },
    {
      name: "house",
      title: t("menu.group.house"),
      sections: [
        { name: "devices", title: t("devices.title"), note: t("devices.note"), Body: Devices },
        { name: "trail", title: t("trail.title"), note: t("trail.note"), Body: TheTrail },
        // Temporary, for the weeks the prompts are being changed. See
        // panel/routes/verdicts.py for what has to be true before it goes.
        {
          name: "verdicts",
          title: t("verdicts.title"),
          note: t("verdicts.note"),
          Body: Verdicts,
        },
        { name: "usage", title: t("usage.title"), note: t("usage.note"), Body: Usage },
      ],
    },
  ];

  const sections = groups.flatMap((group) => group.sections);
  const section = sections.find((entry) => entry.name === current) ?? sections[0]!;

  useEffect(() => {
    const moved = () => setCurrent(opened() || "experiences");
    window.addEventListener("hashchange", moved);
    return () => window.removeEventListener("hashchange", moved);
  }, []);

  useEffect(() => {
    if (!drawerOpen) return;
    const close = (event: KeyboardEvent) => event.key === "Escape" && setDrawerOpen(false);
    document.addEventListener("keydown", close);
    return () => document.removeEventListener("keydown", close);
  }, [drawerOpen]);

  return (
    <ApiProvider api={api}>
      {/* Above the sections rather than inside one: the limit stops every one of them, and
          the parent who needs to read this did not come looking for it. */}
      <LimitReached />
      <section className="rounded-panel border border-edge bg-card p-[26px] pb-7 shadow-card wide:p-7">
        <div className="wide:grid wide:grid-cols-[13rem_minmax(0,1fr)] wide:items-start wide:gap-8">
          {/* Icon only: the heading right below already names the section, and saying it
              twice on a phone reads as a mistake. */}
          <Button
            className="mb-4 w-12 px-0 wide:hidden"
            aria-label={t("menu.open")}
            aria-expanded={drawerOpen}
            onClick={() => setDrawerOpen(true)}
          >
            <Menu aria-hidden className="size-5" />
          </Button>

          {drawerOpen ? (
            <div
              aria-hidden
              className="fixed inset-0 z-10 bg-black/30 wide:hidden"
              onClick={() => setDrawerOpen(false)}
            />
          ) : null}

          <aside
            className={cn(
              "fixed inset-y-0 left-0 z-20 h-dvh w-[min(19rem,calc(100vw-48px))] overflow-y-auto",
              "border-r border-edge bg-card p-5 shadow-[12px_0_32px_rgb(0_0_0/0.18)]",
              drawerOpen ? "block" : "hidden",
              "wide:sticky wide:top-6 wide:z-auto wide:block wide:h-auto wide:w-auto wide:overflow-visible",
              "wide:border-0 wide:bg-transparent wide:p-0 wide:shadow-none",
            )}
          >
            <Button
              variant="ghost"
              className="mb-3.5 ml-auto flex w-11 px-0 wide:hidden"
              aria-label={t("menu.close")}
              autoFocus={drawerOpen}
              onClick={() => setDrawerOpen(false)}
            >
              <X aria-hidden className="size-5" />
            </Button>
            <nav aria-label={t("menu.aria")} className="flex flex-col gap-0.5">
              {groups.map((group) => (
                <div key={group.name} className="mt-3.5 first:mt-0">
                  <h4 className="mb-1 px-3.5 text-[0.75rem] font-semibold tracking-[0.06em] text-quiet uppercase">
                    {group.title}
                  </h4>
                  {group.sections.map((entry) => (
                    <button
                      key={entry.name}
                      type="button"
                      aria-current={entry.name === section.name ? "true" : undefined}
                      onClick={() => {
                        setCurrent(entry.name);
                        window.location.hash = entry.name;
                        setDrawerOpen(false);
                      }}
                      className={cn(
                        "w-full cursor-pointer rounded-r-control border-0 border-l-[3px]",
                        "border-transparent px-3 py-2.5 pl-3.5 text-left font-sans text-base",
                        entry.name === section.name
                          ? "border-l-accent bg-accent-soft font-semibold text-ink"
                          : "bg-transparent text-quiet hover:bg-paper hover:text-ink",
                      )}
                    >
                      {entry.title}
                    </button>
                  ))}
                </div>
              ))}
            </nav>
          </aside>

          <div className="min-w-0">
            {/* The menu says which section is open; the heading says it again where the
                reading actually starts, and is the only title on a phone. */}
            <h3 className="mb-1.5 text-[1.15rem] font-semibold tracking-tight">
              {section.title}
            </h3>
            <Quiet>{section.note}</Quiet>
            <Boundary resetOn={current} fallback={<Quiet>{t("section.broken")}</Quiet>}>
              <section.Body />
            </Boundary>
          </div>
        </div>
      </section>
    </ApiProvider>
  );
}
