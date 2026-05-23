# Q1 2024 — Engineering Notes

## Sprint 5 (Jan 8–19)
- Completed the user authentication refactor. JWT now stateless; session length configurable via env var.
- Discovered race condition in the payment processor webhook handler — logged as ISSUE-1142.
- Tech debt spike: removed three deprecated API endpoints (`/v1/user/profile`, `/v1/search/legacy`, `/v1/auth/basic`).

## Sprint 6 (Jan 22 – Feb 2)
- ISSUE-1142 fixed. Root cause: two worker processes handling the same webhook ID simultaneously. Added idempotency key check.
- Started the notifications migration from email-only to multi-channel (email + SMS + push).
- Reviewed three libraries for push notifications: FCM, OneSignal, and Courier. Chose Courier — best SDK, has MCP connector.

## Open questions at end of Q1
- Database migrations still run manually before each deploy. Should automate with CI.
- No observability on the webhooks path. Need structured logging + Sentry capture.
- Push notifications: need product sign-off on notification content before SMS goes live.
