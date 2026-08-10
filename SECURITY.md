# Security policy

Echo Analytics Engine is a Cloudflare Worker (D1 + KV + service bindings to
`echo-engine-runtime`, `echo-shared-brain`, `echo-doctrine-forge`, `echo-knowledge-forge`,
`echo-autonomous-daemon`) that aggregates internal fleet-scale metrics (engine/doctrine/query
counts, fleet health score, daemon cycles). `POST /snapshot` (the ingestion/write path) requires
`X-Echo-API-Key` or a Bearer token, checked in constant time. The read endpoints (`/dashboard`,
`/growth`, `/metrics/:source`, `/trends`) are intentionally public/unauthenticated by design
(consistent across all four); they expose internal fleet-scale telemetry, not customer data or
secrets, but should still be treated as reconnaissance-relevant if this Worker is ever exposed
on a public route rather than reached only via service binding.

## Supported version

Security fixes target the current `main` branch and the currently deployed Worker release.
Historical commits are retained for evidence and are not patched in place.

## Report a vulnerability

Do not open a public issue for a suspected vulnerability. Send a private report to
`security@echo-op.com` with:

- affected endpoint and exact revision;
- reproduction steps and expected impact;
- whether the `X-Echo-API-Key`/Bearer authentication boundary on `POST /snapshot`, or the public
  exposure scope of the read endpoints, may be involved;
- safe contact details for follow-up.

Never include a live `ECHO_API_KEY` in a report.
