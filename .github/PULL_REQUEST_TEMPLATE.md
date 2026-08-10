## Objective

Describe the metrics/analytics behavior this change adds or fixes.

## Evidence

- Exact source revision:
- Test output (`npm test`):
- Negative paths exercised (missing/invalid key on `/snapshot`):
- Hosted CI run:

## Security and release impact

- [ ] No secrets (`ECHO_API_KEY`) are included.
- [ ] The `POST /snapshot` authentication boundary is unchanged, or the change is called out
      explicitly.
- [ ] Any change to which routes are public vs. authenticated is called out explicitly.
- [ ] Staging-first deployment and rollback implications are documented.
