# Contributing

Thank you for improving Echo Analytics Engine. This is a public, proprietary infrastructure
project: contributions are welcome for review, but repository visibility does not grant a
general use or redistribution license.

## Development path

1. Open an issue describing the metrics/analytics behavior being changed.
2. Create a focused branch from current `main`.
3. Add a failing test before changing authentication or the public/private scope of any route.
4. Validate before opening a pull request:

   ```powershell
   npm install
   npm test
   ```

5. Open a pull request using the repository template and include exact test output.

## Pull-request requirements

- No secrets (`ECHO_API_KEY`) are included.
- No stubs, placeholders, skipped security checks, or self-asserted readiness.
- Changes to the authentication boundary on `POST /snapshot`, or to which routes are public vs.
  authenticated, are called out explicitly in the pull request description.
