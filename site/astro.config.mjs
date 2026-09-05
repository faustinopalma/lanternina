import sitemap from "@astrojs/sitemap";
import { defineConfig } from "astro/config";

// The two language trees are real directories of real HTML, not one page with a switch.
// That is the whole reason for the framework: a crawler has to find /en/ and /it/ as
// separate documents, each declaring the other with hreflang.
export default defineConfig({
  site: "https://lanternina.com",
  trailingSlash: "always",
  // Never inline a stylesheet: the Content-Security-Policy allows styles from 'self' only,
  // and Astro inlines small ones by default, which would silently render one page unstyled.
  build: { format: "directory", inlineStylesheets: "never" },
  integrations: [
    sitemap({
      i18n: { defaultLocale: "en", locales: { en: "en", it: "it" } },
      // The root is a redirect to a language, so it is not itself a destination.
      filter: (page) => page !== "https://lanternina.com/",
    }),
  ],
});
