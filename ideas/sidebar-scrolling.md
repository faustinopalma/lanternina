# Sidebar scrolling

The owner requested an invisible menu scrollbar on 15 September 2026. The menu hides its scrollbar with `scrollbar-width: none` and the WebKit scrollbar selector while retaining native scrolling. This removes the visible track and thumb, including thumb dragging; wheel, touch and keyboard navigation remain available. The content area's scrollbar is unchanged. The browser check verifies the hidden scrollbar styles and repeats the desktop and mobile scrolling checks below.

The desktop menu now scrolls independently of the content. Previously, its sticky positioning kept the top visible, but `overflow-visible` and an unconstrained height left the lower entries below the viewport. Wheel input over the menu scrolled the document until the content reached its end.

The menu keeps `overflow-y-auto` on desktop and contains vertical overscroll. Its maximum height uses the current distance from the viewport top and leaves 24 CSS pixels below it at the default font size. Scroll, resize and document layout changes update that distance. This keeps the last entry reachable both below the page header and after the menu sticks near the viewport top. Measuring the position adds event listeners and a resize observer; it avoids assuming a fixed header height when text wraps or an account notice appears.

## Verification on 15 September 2026

Headless Edge with Playwright exercised the local development preview and synthetic data at 1152 by 645, 1440 by 900 and 960 by 480 CSS pixels, each at document scroll offsets of 0 and 300 CSS pixels. Wheel input over an overflowing menu changed its scroll position while the document stayed still. Further wheel input at the menu bottom stayed contained. The menu bottom remained inside the viewport, and wheel input over the content still scrolled the document. Restoring the previous overflow and height rules reproduced the reported failure.

At 390 by 640 CSS pixels, the mobile drawer scrolled by 173 CSS pixels while the document remained at offset 0. Selecting the last section closed the drawer and navigated to `#usage`. Screenshots were inspected locally. These checks use a development preview, not the deployed panel. The navigation test also checks position updates on scroll and resize and listener cleanup on unmount.