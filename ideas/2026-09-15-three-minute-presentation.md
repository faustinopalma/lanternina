# A three-minute presentation

The presentation lives at https://lanternina.com/it/present/ and https://lanternina.com/en/present/. It shares the public site's deployment, but the site's navigation does not link to it. Both pages declare `noindex, nofollow` and are excluded from the sitemap. This reduces discovery; it does not make either URL private.

The five slides cover the afternoon, the parent's choice, a paper exchange, the technical components and the activity's ending. The presentation reuses existing public prototype photographs, invented panel data and the Valle Lunga example. The slide with blue handwriting states that a model simulated it. Reusing those images shows the implementation; the tradeoff is that the activity sheets remain in Italian in the English presentation.

The speech contains 384 Italian words and 379 English words, counted from the built note templates on 15 September 2026. Three minutes requires approximately 128 words per minute. This is a calculated pace, not a measured delivery. Each slide's notebook button opens its corresponding paragraph. Arrow keys, Page Up, Page Down, Home, End, navigation buttons and horizontal touch gestures change slides. A language change preserves the current slide.

The initial sketch described a fixed three-sheet ceiling, vision checks before any human review and a parent-to-child note. The delivered account follows the current public implementation instead: the parent approves the initial activity, automatic checks apply to continuations, and vision reads returned material. The 28-day preference note gives temporary context to the system. The presentation describes sheet limits without conflating simultaneous sheets with the whole game's paper budget. The system overview and implementation status pages supplied these distinctions.

## Annotations

The owner supplied the portable reference now stored in `site/docs/WHITEBOARD.md`. Its original content is preserved. `site/src/scripts/whiteboard.ts` adapts it for the presentation only. Each slide has an SVG overlay inside its scrolling area. Pen proximity arms the overlay and disables pen panning; mouse and touch restore ordinary navigation unless the mouse-drawing checkbox is enabled. The eraser removes whole nearby strokes. Width uses the pressure at the start of a stroke, matching the reference rather than claiming continuously variable brush pressure.

Colours, width, undo and clear belong to a collapsible toolbar. Clear affects only the current slide and asks for confirmation. Undo also restores erased or cleared strokes, with a maximum of 50 action snapshots per slide in memory. Restored strokes can be undone after reloading.

Ink is saved under `lanternina-presentation-ink-v1:it` or `lanternina-presentation-ink-v1:en` in the browser's local storage. It is never uploaded. Storage failure leaves drawing available in memory, so persistence depends on browser permissions and available space. Each record contains only recognised colours, a bounded width and finite normalised coordinates. The languages have separate records because translated layouts differ. Coordinates scale with the slide's content area; annotations are not attached to individual words, so a responsive reflow can change their alignment. Use the intended presentation viewport when annotating.

## Verification

Run `npm --prefix site run build` and `python site/check-build.py`. Restart Astro preview after rebuilding: the preview process used here retained an earlier build until restarted. Browser checks cover image loading, slide navigation, language continuity, notes, pen and eraser events, pressure-derived width, optional mouse drawing, touch pass-through, local persistence, slide isolation, undo and clear. Check 1440 by 900 and 1280 by 720 pixels for projection, and 390 by 844 and 320 by 640 pixels for mobile layout.

Synthetic pointer events verify the browser engine; they do not establish Wacom driver behaviour or physical pen performance. A physical front-tip/back-tip trial remains for the owner. This document records implementation choices, not evidence of educational benefit.