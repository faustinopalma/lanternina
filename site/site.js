/* The language switch. Italian is what the document ships as, so with this file blocked
   the page is still a whole page rather than an empty one. */
(function () {
  "use strict";

  var LANGS = ["it", "en"];
  var KEY = "lanternina.lang";

  function remembered() {
    try {
      var saved = window.localStorage.getItem(KEY);
      return LANGS.indexOf(saved) === -1 ? null : saved;
    } catch (e) {
      return null; // private browsing refuses localStorage; a default is fine here
    }
  }

  function preferred() {
    var list = navigator.languages || [navigator.language || ""];
    for (var i = 0; i < list.length; i++) {
      var tag = String(list[i]).toLowerCase().slice(0, 2);
      if (LANGS.indexOf(tag) !== -1) return tag;
    }
    return "en"; // a reader whose browser asks for neither is likelier to read English
  }

  function apply(lang) {
    document.documentElement.lang = lang;

    document.querySelectorAll("[data-set-lang]").forEach(function (button) {
      button.setAttribute("aria-pressed", String(button.dataset.setLang === lang));
    });

    // alt text is an attribute, so it cannot be duplicated the way the prose is.
    document.querySelectorAll("img[data-alt-" + lang + "]").forEach(function (img) {
      img.alt = img.dataset["alt" + lang.charAt(0).toUpperCase() + lang.slice(1)];
    });
  }

  apply(remembered() || preferred());

  document.querySelectorAll("[data-set-lang]").forEach(function (button) {
    button.addEventListener("click", function () {
      var lang = button.dataset.setLang;
      apply(lang);
      try {
        window.localStorage.setItem(KEY, lang);
      } catch (e) {
        /* the choice still holds for this page view */
      }
    });
  });
})();
