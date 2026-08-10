# Echo Analytics Engine

Unified cross-product fleet analytics -- a Cloudflare Worker (D1 + KV + service bindings) that
aggregates engine/doctrine/query counts, knowledge-doc counts, brain-message/instance counts,
and a fleet health score across the Echo stack, tracks daily growth trends, and exposes them for
dashboards. Runs a scheduled 6-hourly snapshot via a Worker Cron Trigger.

## Endpoints

| Access | Method | Path | Description |
|---|---|---|---|
| Public | GET | `/`, `/health` | Service info / health check |
| Public | GET | `/dashboard` | Current metrics + 24h/7d deltas + last 30 days of trend rows |
| Public | GET | `/growth?days=N` | Growth-tracking rows for the last N days (max 90) |
| Public | GET | `/metrics/:source` | Raw metric snapshots for one source, optionally filtered |
| Public | GET | `/trends` | Trend series |
| Authenticated | POST | `/snapshot` | Trigger an immediate metrics snapshot/ingestion |

## Authentication

Only `POST /snapshot` requires `X-Echo-API-Key` or an `Authorization: Bearer` token, compared to
`env.ECHO_API_KEY` in constant time. The read endpoints are intentionally public by design --
this is internal fleet-scale telemetry (counts and growth rates), not customer data or secrets --
but see [SECURITY.md](SECURITY.md) if this Worker is ever exposed on a public route rather than
reached only via internal service binding.

## Verify

```powershell
npm install
npm test
```

## License

See [LICENSE](LICENSE). Contributions: see [CONTRIBUTING.md](CONTRIBUTING.md).
