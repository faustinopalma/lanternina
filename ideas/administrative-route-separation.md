# Administrative Route Separation

On 15 September 2026 the owner requested minimal separation of family and administrative access, with public documentation that describes the separation rather than presenting a shared API as a benefit.

The administrative router now owns its prefix and common authorization dependency and is registered separately from family routes. This protects a newly added administrative endpoint even if it omits an individual authentication parameter, while retaining existing paths, stores, exception handling and deployment. The tradeoff is that process, identity and data permissions remain shared: this change reduces accidental authorization omissions but does not contain a process compromise.

Two applications or processes were not introduced because the requested minimum can be enforced at the router boundary without changing request state, middleware or lifecycle handling. A future service split requires separate runtime permissions as well as separate routing. The bilingual site and architecture document describe this limit next to the separation claim.

The tests cover every current administrative operation and a temporary route without individual authentication. The notebook index separately includes the historical workbench, and public research links lead to the Officina directory. No notebook was moved or rerun for these changes.
