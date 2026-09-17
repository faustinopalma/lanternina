# Activity record and clock

The parent asked for 24-hour times throughout the panel, deletion of individual historical activities, a step-by-step view of the current activity, and two checks of the record-clearing operation before using it again. The earlier deletion incident selected a household's documents from the shared container and removed settings as well as history.

## Time display

The shared time input now accepts `HH:MM`, from `00:00` through `23:59`. A text input with an HTML validation pattern makes the format independent of the browser's native time picker; it costs the native picker and its hour/minute controls. The Rhythm and running-activity deadline forms use this input. Localized timestamps, the household clock and the hub camera gallery explicitly use `hourCycle: "h23"`. Their existing timezone selection remains unchanged.

## Current activity

The hub reports its current run files after processing endings and before the schedule checks, and again after starting an activity. The device-key route stores one snapshot per household. The authenticated panel reads the snapshot and opens each current activity's chronological record. The status gives the current heading, the wait start and the expected ending. The trace shows recorded events; it does not prove that every physical action has completed.

The existing hub timer runs every 60 seconds. The visible panel refreshes every 30 seconds and on focus. These intervals are configuration values, not a measured delivery guarantee: long-running work and network failures can delay reporting. The panel labels a snapshot older than 180 seconds as the last known state. This chosen threshold tolerates missed updates but leaves up to three minutes in which an old state can look current. A missing snapshot is unavailable, not idle. An unreadable run file is reported explicitly. Historical deletion remains available when a stale snapshot still names a run.

## Deletion scope

Both deletion routes derive the household from the authenticated account. Single deletion also selects the requested run ID. The Cosmos store checks the dedicated `trail` container identity, supplies the household partition key and parameterized predicates, materializes the complete candidate list, and validates each candidate before the first delete. Only `trail` and `made` documents qualify. Each write deletes one document by ID and household partition. No container or partition deletion API is used.

The snapshot has type `progress` and survives both operations. Settings, approved activities and other households survive. Single deletion leaves other runs untouched. The UI requires a confirmation and allows cancellation; bulk deletion also invalidates any displayed current trace so deleted steps do not remain visible.

These operations remove activity-log documents. They do not stop a running activity or delete the separate returned-material, observation and blob stores. An operation interrupted during point deletes can leave some selected rows in place; repeating it is supported. A running hub can write new rows after deletion. There is no tombstone, cross-store purge or migration of legacy records still in `sources`.

## Local verification on 17 September 2026

The storage checks exercise bulk and single deletion, repeat calls, other runs, other households, unexpected document types, unsafe query results and a misrouted container. The HTTP check uses the real `CosmosTrailStore` with two mapped simulated containers. It deletes four synthetic record documents, including an orphan step, and compares all protected documents and the settings container before and after. The repeat request reports zero deletions. The frontend transport test verifies distinct authenticated DELETE routes and an encoded single-run ID.

Two negative controls ran in disposable Python processes without changing repository files. Routing the store to the simulated shared container made the HTTP regression fail. Removing candidate validation made all four unsafe-result cases fail. The installed Cosmos SDK constructor was inspected locally and assigns `ContainerProxy.id`; this check made no network request.

The backend command `python -m pytest tests/test_trail.py tests/test_run_experience.py tests/test_afternoon_clock.py tests/test_panel.py -q` passed 121 tests in 13.05 seconds, measured by pytest. It includes the browser-method CORS regression. The frontend command `npm --prefix web test` passed 190 tests in 17.34 seconds, measured by Vitest. Ruff passed on the eight changed Python files. TypeScript and the production build passed; Vite reported the existing chunk-size warning. Starlette reported its existing test-client deprecation warning.

Browser checks used only synthetic data under `?preview`. At 390 by 844 pixels and 1440 by 1000 pixels, the current trace had no horizontal overflow. Screenshots were inspected, the synthetic image loaded, and displayed times contained no AM/PM suffix. The stale-state check retained the historical delete button. The bulk-delete check observed zero calls after cancellation and exactly one after confirmation, while preserving current status. A separate single-delete check removed only the synthetic record. The camera gallery's scripts were executed with synthetic midnight and afternoon photographs and displayed `00:07:00` and `15:07:00`.

## Release boundary

These changes are local. No production deletion, service-level Cosmos deletion test, deployment, commit or push was performed. The published button has not been revalidated by these tests. Release requires the updated API, hub code and frontend; deploy the API before the two clients. Before treating the production operation as verified, repeat deletion against disposable Cosmos test data with protected documents compared before and after. Keep that test separate from the family's records.
