# Mission and camera on the public site

## Decision, 10 September 2026

The public site opens with a short mission page in each of its existing languages. It explains who Lanternina is for, what an afternoon can involve and what still requires trials with a person. The technical overview, flows, identity and implementation pages follow it. This gives a new reader the purpose before the implementation at the cost of one additional page. Existing technical URLs remain unchanged; the root language chooser and brand link lead to the mission.

The owner clarified that the camera serves to return completed work. The public use case is a photograph of the completed sheet, compared with the exact original page kept for printing. The site does not propose photographing objects, constructions or surroundings. This update changes the public explanation, not the firmware or backend contracts. The owner's current pin repair is outside this site update.

## Evidence and images

The camera firmware README records owner-observed shutter and LED operation on 9 September, three inspected battery cycles with matching receipts and empty queues, and preceding RTC sleep durations of 118, 135 and 74 seconds at one-second resolution. It also records receiver-offline retry and a 10 September autoexposure USB capture: selected framebuffer ready at 831 ms and acquisition plus verified storage at 2,307 ms. These are bounded observations, not battery-life or broad image-quality claims. Later wiring revisions require separate physical acceptance.

The owner supplied three iPhone photographs dated 9 September 2026 and authorized publication and removal of their temporary source folder. The site uses WebP derivatives with a maximum dimension of 1,600 pixels, encoded at quality 86. EXIF and XMP metadata are removed. The photographs show assembly internals, the closed camera and the camera beside a display; none is presented as output from the prototype camera. The assembly image documents its date and is not a wiring guide.

Source mapping: `20260909_175805466_iOS.HEIC` becomes `camera-prototype-1.webp`; `20260909_180150703_iOS.HEIC` becomes `camera-prototype-2.webp`; `20260909_181621079_iOS.HEIC` becomes `camera-prototype-3.webp`. The WebP files contain 213,506, 183,430 and 123,476 bytes respectively, measured after conversion. All three were decoded and visually inspected before removal of the temporary originals.

## Verification

Run `npm --prefix site run build` and `python site/check-build.py` from the repository root. Check the root language redirect, language switching, mission-to-overview navigation, image enlargement and mobile layout in a browser. Publish through the existing site workflow after committing only this update and verify the public mission and camera section.