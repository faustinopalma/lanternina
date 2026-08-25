/// <reference types="vite/client" />

/* The two values the administration page needs. Typed as possibly absent because they are
 * absent until the app registration exists, and the page has a state for that. */
interface ImportMetaEnv {
  readonly VITE_ADMIN_CLIENT_ID?: string;
  readonly VITE_ADMIN_TENANT_ID?: string;
}

declare namespace Intl {
  /* Shipped by browsers and not yet in TypeScript's lib. Declared optional and called
   * behind a typeof check, because "the engine has it" is what the check is for. */
  interface Locale {
    getTimeZones?(): string[] | undefined;
  }
}
