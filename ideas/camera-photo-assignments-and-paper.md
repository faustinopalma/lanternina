# Camera display assignments and photographed paper

## Findings on 9 September 2026

The owner reported successful photographs after the D1 shutter and D4 LED rewiring, including battery operation. The hub's inspected diagnostic history contained three completed battery capture events with previousSleepConfirmed=true, matching upload identifiers, HTTP 201 and queue zero. Their preceding sleep durations were 118, 135 and 74 seconds. These are device RTC readings with one-second resolution, not measurements of current or battery life.

The owner also reported a photograph appearing on an unassigned display. The live jobs cache gave both CF7D04 and FB9F18 only picture, sheet and remind. A receipt recorded a photograph displayed on CF7D04. CameraHub.process_one fell back to a picture display when no photo display existed, and the BYOS server also allowed a stored photo layer with the picture job. Both paths now require an explicit photo assignment. This respects the parent's choice and costs the previous automatic display fallback. Existing photo files cannot override that choice on the next display request; the originals remain archived.

Camera inventory rows have no job choices. The browser now omits the job group when no choices exist, instead of saying that the camera has no job. A UI test uses two camera identities and checks that both remain independently named and listed. Credentials and archive identities remain per camera.

## Paper reading

The owner requested a physical trial using the camera to return a written sheet. Paper collect moments keep the existing scanner source/default, but may also receive a time-bound camera photo. That route loads the exact A4 PNG retained for printing and sends it first, followed by the photograph. A dedicated prompt compares page content, discounts perspective, rotation, lighting and table background, and transcribes visible additions. It reports unreadable portions and requires an explicit uncertainty flag; uncertainty prevents activity advancement. Object/construction collection with source=camera still sends a single image and does not assume a printed reference.

The API preserves the supplied original in photograph mode. Both photographic modes skip the separate page-placement task intended for scans. Tests check exact original pixels at the runner, image order at the model request, both images through the HTTP route, uncertainty and the existing single-image construction path. The physical handwriting trial has not yet occurred. It should use the original already printed for the waiting paper moment, one deliberate photo and inspection of the actual transcription before treating camera acquisition as readable.

Unfinished scan-archive changes remain separate and are not part of this publication.