# The XIAO ESP32S3 Sense camera

The camera uses a XIAO ESP32S3 with a Sense expansion board and OV3660 sensor. On 7 September 2026, the two photographs of the kit allowed us to read the board model and the marking on the ribbon cable. The [dedicated section](../docs/macchina-fotografica/README.md) describes the button and LED wiring and holds the kit photographs as JPEGs.

## What it adds to an afternoon

The camera allows someone to return an image of a construction, a found object or a drawing on a wall. The scanner already collects sheets; the camera makes it possible to choose something that stays where it is. The first use to test is photographing a construction to keep an image before changing it. The second is bringing two photographs of details to a later comparison activity.

The button puts the decision to capture in the hands of the person holding the camera. An LED confirms the action without requiring a menu. A screenless camera costs certainty about framing: the enclosure shape, a tested working distance and a possible optical viewfinder must be assessed through actual photographs. The absence of a screen does not guarantee a successful photograph.

This choice follows the handheld direction recorded on 25 August in [ideas/06-capture.md](06-capture.md). The old fixed station remains historical research. The project's design rules are under review; the wiring does not depend on reinstating its earlier prohibitions.

## The chosen connections

The shutter connects D1/GPIO2 to ground; the external LED uses D4/GPIO5 through its series resistor. The owner reported both wiring changes on 9 September and the matching firmware is installed. GPIO2 handles capture and deep-sleep wakeup; the retired GPIO4 and GPIO3 inputs have both pulls disabled. D1 measured 3.2 V in the preceding unloaded test. Physical press, LED and battery-wake acceptance remain open.

The former LED pin GPIO3 also selects the JTAG source at startup. It is now unused. USB Serial/JTAG identification and firmware updates succeeded after the D1/D4 rewiring; this does not replace a battery cold-start test.

The built-in LED uses GPIO21, which the expansion also uses for the microSD chip select. An external LED remains visible on the enclosure and does not interfere with that signal; it costs a component, a resistor and wiring.

## What completion means

A light wired to the button would confirm only that the contact has closed. A firmware-controlled light can instead distinguish acceptance of the command from delivery of the photograph. On 7 September 2026, Fausto chose one flash when the firmware accepts the press and two flashes when the image has been uploaded into the system. We define that second event as a valid acknowledgement from lanternina hub after durable storage of the identified capture, not a local microSD write or completion of model processing.

On 9 September the owner replaced the initial fixed pulse with continuous light throughout acquisition, ending when the selected framebuffer is complete. This gives a usable indication of when framing may change, at the cost of a variable initial light duration. The two delivery flashes remain 150 ms each, with 150 ms between them and at least 500 ms darkness after acquisition. Three flashes report capture or storage failure. The firmware keeps acquisition state separate from the network work and uses an atomic flag between the worker and LED loop.

This replaces the earlier proposal of steady light during capture and confirmation after local storage. It tells the person that the image has reached the system, but makes confirmation depend on the network. A queued image receives its two flashes only when delivery is acknowledged, possibly much later. Duplicate receipts must not replay the signal, and overlapping feedback sequences must be serialised. One LED cannot identify which queued photograph arrived; the hub's receipt record must retain that association.

The [wiring diagram](../docs/macchina-fotografica/images/button-led-wiring.svg) shows the D1 shutter and D4 LED. The button and LED share ground, with no connection between their signal pins.

## The photograph must be able to wait

The implementation uses a LittleFS partition in the board's flash, rather than requiring a microSD card. It holds at most three pending JPEGs, each at most 750,000 bytes. This gives offline capture without another component, but costs flash writes and limits the queue. A full queue refuses a new capture with the error signal and does not overwrite an earlier image.

RAM alone would simplify data management, but would lose the photograph on restart or battery depletion. The hardware document had already separated capture away from home from delivery over the home network. A persistent queue provides a way to support this, without claiming it is already implemented.

The hub is the proposed recipient because it already coordinates the household equipment. This choice keeps cloud archive credentials out of the camera, but requires an authenticated receiver, acknowledgements backed by durable storage and deduplication. Simply connecting to Wi-Fi supplies none of these.

The receiver binds a timestamped photograph to the run, collect and arrival time at that collect. The worker checks that binding again under the activity lock. An undated photograph or one whose collect has changed remains in the archive. The camera synchronises its clock while connected; a cold-start capture made before that succeeds cannot advance the activity. This costs one automatic association rather than attributing an old photograph to a new task.

## Where to start

The wiring and firmware installation are complete. Check D1 voltage released, pressed and released again, then verify one photograph per accepted press, LED feedback and battery sleep/wake. Keep unused wire ends insulated. No further investigation of D3 is required by the owner.

We use Espressif's `esp32-camera` driver for JPEG capture. Alternating subjects checks that each capture contains the current subject. Discarding a frame is not assumed to establish freshness in every configuration.

## Completion criteria

The documentation is ready when the wiring matches the photographed board, sources can be traced, photographs can be viewed without HEIC support and the temporary directory has been removed. These checks were performed on 7 September 2026.

The prototype will be ready when an accepted press produces one flash and a current photograph, a long press produces only one capture, and the two-flash confirmation occurs only after a valid hub receipt. Missing, rejected or duplicate receipts must not produce a false or repeated success signal. Repeated delivery must not duplicate the photograph on the hub. A camera for domestic use will also require a tested enclosure, measured battery life and a deletion procedure covering both device and hub. None of these physical tests was performed in this session.
