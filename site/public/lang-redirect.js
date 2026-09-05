/* Sends a reader from / to /en/ or /it/, once.
 *
 * External rather than inline because the Content-Security-Policy on this site allows
 * scripts only from 'self'. An inline block would need 'unsafe-inline' or a hash, and the
 * first of those weakens the policy for every page to save one file.
 */
(function () {
  var saved = null;
  try {
    saved = localStorage.getItem("lanternina.lang");
  } catch (e) {
    /* private browsing refuses localStorage; the sniff below still works */
  }

  if (saved !== "it" && saved !== "en") {
    var asked =
      navigator.languages && navigator.languages.length
        ? navigator.languages
        : navigator.language
          ? [navigator.language]
          : [];
    saved = "en";
    for (var i = 0; i < asked.length; i++) {
      var tag = String(asked[i]).toLowerCase().split("-")[0];
      if (tag === "it" || tag === "en") {
        saved = tag;
        break;
      }
    }
  }

  location.replace("/" + saved + "/");
})();
