# Mission and camera on the public site

## Decision, 10 September 2026

The public site opens with a short mission page in each of its existing languages. It explains who Lanternina is for, what an afternoon can involve and what still requires trials with a person. The technical overview, flows, identity and implementation pages follow it. This gives a new reader the purpose before the implementation at the cost of one additional page. Existing technical URLs remain unchanged; the root language chooser and brand link lead to the mission.

The owner clarified that the camera serves to return completed work. The public use case is a photograph of the completed sheet, compared with the exact original page kept for printing. The site does not propose photographing objects, constructions or surroundings. This update changes the public explanation, not the firmware or backend contracts. The owner's current pin repair is outside this site update.

## Evidence and images

The camera firmware README records owner-observed shutter and LED operation on 9 September, three inspected battery cycles with matching receipts and empty queues, and preceding RTC sleep durations of 118, 135 and 74 seconds at one-second resolution. It also records receiver-offline retry and a 10 September autoexposure USB capture: selected framebuffer ready at 831 ms and acquisition plus verified storage at 2,307 ms. These are bounded observations, not battery-life or broad image-quality claims. Later wiring revisions require separate physical acceptance.

The owner supplied three iPhone photographs dated 9 September 2026 and authorized publication and removal of their temporary source folder. The site uses WebP derivatives with a maximum dimension of 1,600 pixels, encoded at quality 86. EXIF and XMP metadata are removed. The photographs show assembly internals, the closed camera and the camera beside a display; none is presented as output from the prototype camera. The assembly image documents its date and is not a wiring guide.

Source mapping: `20260909_175805466_iOS.HEIC` becomes `camera-prototype-1.webp`; `20260909_180150703_iOS.HEIC` becomes `camera-prototype-2.webp`; `20260909_181621079_iOS.HEIC` becomes `camera-prototype-3.webp`. The WebP files contain 213,506, 183,430 and 123,476 bytes respectively, measured after conversion. All three were decoded and visually inspected before removal of the temporary originals.

## Verification

Later on 10 September, the owner requested swapping the opening photographs. The mission uses `hero.jpg`, showing a poodle on the display. The overview uses the photograph of the camera beside the display and dragon, with its original aspect ratio.

The owner then requested replacing that display's reminder with a game clue through the existing image API. The first `camera-prototype-game.webp` illustrated a clue leading to the books. The original `camera-prototype-3.webp` remains available. The photograph illustrates an activity rather than documenting one running on the device.

The existing Azure OpenAI deployment `gpt-image-2-2026-04-21` produced three initial candidates. Two masked photograph edits placed text too close to the foreground camera. The third call generated only the flat e-paper content, which was mapped to the screen's perspective and adjusted to its measured background lighting. The calls took 49.9, 46.8 and 22.8 seconds respectively, measured around the SDK call including authentication and client setup. A screen polygon limits the composite. Comparing the decoded first WebP against the original found no changed pixels outside that polygon and changes inside it. That lossless derivative measured 1,099,424 bytes at 1,600 by 1,200 pixels; this encoding preserves the untouched pixels at the cost of a larger download.

The owner requested a further revision on 10 September: remove the illustrative image's provenance caption, reduce repetition in the overview and replace the book riddle. Both overviews now start with the hub's technical role and leave the activity sequence to the numbered steps. The photograph has descriptive alternative text and no caption. Production details remain in this note.

The replacement activity, "Il passaggio segreto", asks the player to choose three objects in the room, turn them into a bridge, a tower and a refuge on a map, and decide where to hide a passage. It offers a spatial and narrative choice instead of an answer supplied by the prompt itself, at the cost of needing a map to draw on. The same image deployment generated the new screen in 23.4 seconds, measured as above. The perspective composite measures 1,101,130 bytes at 1,600 by 1,200 pixels. The outside-screen pixel comparison passed again; visual inspection confirmed the complete text and clear margins.

Run `npm --prefix site run build` and `python site/check-build.py` from the repository root. Check the root language redirect, language switching, mission-to-overview navigation, image enlargement and mobile layout in a browser. Publish through the existing site workflow after committing only this update and verify the public mission and camera section.

## Editorial revision, 10 September 2026

The owner requested clearer language for technical readers after the mission page, without making the account pedantic. Both language trees now name the hub and cloud API consistently in the activity sequence, define a moment at first use and describe diagram actions directly. The mission retains its broader audience. The identity page leaves app-role troubleshooting to the linked deployment documentation. Page order, images, measurements and implementation limits remain in place. Local definitions reduce the reader's dependence on repository terminology without adding a glossary or repeating the architecture on every page.