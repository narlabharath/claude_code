# Q2 2024 — Engineering Notes

## Sprint 7 (Feb 5–16)
- Notifications multi-channel shipped. Email + SMS live; push notifications still pending product sign-off.
- Sentry integration added to webhook path. First week of data: 3 uncaught exceptions per day, all timeout-related.
- Started CI pipeline for DB migrations. Using Flyway. Staging environment validated.

## Sprint 8 (Feb 19 – Mar 1)
- DB migration CI live. Deployment incidents from manual migration errors: 0 this sprint (was averaging 1/sprint).
- Timeout errors in webhooks traced to third-party payment processor — they're slow when processing refunds.
- Investigated: adding a 30s retry with exponential backoff reduced timeout errors by 70%.

## Sprint 9 (Mar 4–15)
- Push notifications signed off by product. FCM channel added. Rollout to 5% of users.
- Performance profiling run on the search API. P99 at 1.2s — target is 400ms. Main bottleneck: N+1 query in the results endpoint.
- Started N+1 fix. Expected to ship in Sprint 10.

## End of Q2 status
- Notifications: fully live (email + SMS + push). No major incidents.
- Reliability: webhook reliability up from 94% → 99.1% since Sprint 7.
- Search performance: still above target, fix in progress.
