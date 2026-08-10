# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Security

- Replaced the raw `apiKey === env.ECHO_API_KEY` / `authHeader.slice(7) === env.ECHO_API_KEY`
  comparisons in `isAuthorized` with a constant-time `timingSafeEqual` helper on both paths,
  closing a timing side-channel on the auth check guarding `POST /snapshot`. This is the third
  repository in this consolidation campaign found with this exact bug pattern (`echo-invoice`
  was already fine; `cf-dns-manager` and `echo-affiliate` both had it) -- worth tracking as a
  recurring issue across the fleet's early Cloudflare Worker codebase, not a one-off.
- Fixed a real `tsc` type error surfaced by bumping `@cloudflare/workers-types` to a current
  version: `scheduled()`'s first parameter is `ScheduledController` in current Workers types,
  not the removed `ScheduledEvent` alias.

### Added

- `package.json` `test` script (`tsc --noEmit && node --test`) and `tests/pure-functions.test.mjs`:
  14 real unit tests importing and executing `timingSafeEqual`, `safeNum`, `nestedNum`, and
  `formatDelta` directly from `src/index.ts` via Node's native TypeScript support.
- `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`.
- Hosted CI (`.github/workflows/ci.yml`): runs `npm test` on every push and pull request.
- Issue templates (bug report, feature request) and a pull-request template.
- `.echo/{apps.json,certification.json,sdk.json}` for ECHO Certification Forge and GitHub App
  Suite enrollment; `sdk.json` declares the 6 real `echo.analyticsengine.*` capabilities that
  correspond to this repo's actual routes (explicitly excludes 3 registered
  `echo.analyticsengine.*` capabilities -- `plans`/`upgrade`/`webhook_stripe` -- that belong to
  a different service with no matching route here). `scripts/certforge_journey.py` critical
  journey verified locally to actually fail when the auth regression is deliberately
  reintroduced, then restored.
- This CHANGELOG and a README (the repository previously had no README at all).

### Documentation

- `SECURITY.md` explicitly documents that `/dashboard`, `/growth`, `/metrics/:source`, and
  `/trends` are intentionally public/unauthenticated by design (consistent across all four --
  unlike the missing rate limit found on a sibling repo's dashboard endpoint, this is a
  consistent public-read/protected-write pattern, not left as-is without review).

## [Prior history]

- Add security headers middleware for defense-in-depth hardening.
- Fix fail-open auth, add Bearer token support.
- v1.0.0 -- unified cross-product analytics.
