# Camera completion results

## Scope and decisions

Work continued from 97ca39d on 9 September 2026, preserving the pending source and panel changes. Device-specific display intervals are cached by authenticated display identity, with the previous household value and old cache format retained as fallback. This permits independent settings without changing e-paper firmware, at the cost of applying each update only when that display next connects.

Photographic collection uses an optional `source: camera` on the existing collect moment. Existing documents keep the scanner default. The reader receives one photograph and explicit uncertainty rather than comparing an object with a blank page. This supports constructions without printing first; it adds a capability-dependent source to the moment contract. The scanner remains available. Diagnostic USB captures retain their purpose through offline storage and cannot advance activities.

Interrupted processing is closed only after explicit review, through the authenticated hub endpoint and `tools.camera_review`. Archiving does not retry physical effects. This avoids duplicate printing after an ambiguous crash, at the cost of manual inspection before continuing that activity.

## Device evidence

The hub hostname, active camera/display services, USB identity 94:A9:90:D0:9D:D0 and original source hash were rechecked. The camera build now uses a MAC-specific protected directory, regenerates credentials and checks chip, flash size and backup before upload. One physical camera was compiled and updated with hash verification and a mounted filesystem; fresh authenticated telemetry passed the post-flash check. Two distinct identities and stale-header replacement were tested locally, not on two physical cameras.

An explicit USB capture produced 75,932 bytes at 1600 x 1200. Firmware measurements were 366 ms sensor initialization, 543 ms framebuffer readiness, 1,217 ms verified storage, 1,776 ms acquisition plus storage and 707 ms upload. HTTP 201 and queue zero were observed. These are internal USB-triggered timings, not physical press-to-exposure measurements.

The first offline check exposed a real defect: a LOW shutter input prevented the one-minute USB retry. The retry now runs independently of the released-button check required for sleep. The repeated check saved a 77,846-byte JPEG with the receiver stopped, then delivered the same identifier once after restart with an empty queue. The acceptance command took 77.1 seconds. USB_TEST_OFF was acknowledged after each diagnostic test. GPIO4 still sampled LOW; no electrical repair is claimed.

## Physical checks still required

The owner must repair and test the intermittent shutter and LED. Deliberate battery-powered presses, LED interpretation, alternating subjects and varied lighting, current consumption, a power cut during file writing and a second camera installation remain physical checks. Missing/full filesystem handling exists in firmware but has not been destructively exercised on the family queue. An activity with a real construction and a person remains an acceptance test beyond the automated runner and reader tests. No battery percentage is inferred.

## Verification and publication

Focused checks covered device persistence and cache migration, two authenticated display responses, photographic uncertainty and stale capture binding, camera-only activity execution, durable duplicate receipts, deletion precedence and review without replay. Full-suite and publication outcomes are recorded below after execution. Existing GitHub workflows deploy the API, panel and bilingual site; hub installation is separate and preserves e-paper provisioning with registered-only discovery.

Local gates on 9 September passed 1,063 Python tests with two skips, all 140 browser unit tests, full Ruff, the web production build, the Astro build and the site's ten-page bilingual/canonical check. The final scoped USB check passed seven tests after a line-length correction. The editor reported no errors in the touched reader, format, provisioning, paper route and Devices component. The local Azure CLI did not recognize the deployment subscription in its active context; no login or infrastructure was changed. Publication uses the existing GitHub federated credentials and requires live verification afterward.