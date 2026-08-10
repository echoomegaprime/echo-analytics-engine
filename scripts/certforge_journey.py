"""Critical journey for the ECHO Certification Forge.

The Forge runs this argv (declared in ``.echo/certification.json``) inside its
isolated ``python:3.12-alpine`` sandbox, against the exact acquired commit,
with no network and no project dependencies installed -- there is no Node
here, so the Worker itself cannot actually run. The full behavioural suite
(``npm test`` -- typecheck plus real unit tests, imported and executed
against the actual ``src/index.ts`` via Node's native TypeScript support)
runs in CI on this same commit; this journey proves the artifact the Forge
actually acquired is the intact, complete Worker source -- not that it
currently boots.

This repository is TypeScript-only (a single Cloudflare Worker); this
journey therefore checks structural and textual invariants rather than
parsing Python.

Checks:
  1. The critical surfaces exist -- the Worker entrypoint, its test file,
     the pinned Node dependency manifest, and the TypeScript config.
  2. ``src/index.ts``'s bracket counts are balanced -- a cheap, tokenizer-free
     corruption/truncation check. This counts raw characters rather than
     parsing tokens, so it cannot prove syntax validity by itself (that is
     `tsc --noEmit` in `npm test`/CI); it can only prove the file was not
     truncated or grossly corrupted in transit.
  3. No install-lifecycle scripts have crept into ``package.json``.
  4. No hardcoded secret-shaped literals in the acquired source.
  5. ``isAuthorized`` calls the constant-time comparison helper on both the
     API-key and Bearer paths, rather than a raw ``===`` -- a regression
     here reintroduces a timing side-channel on every authenticated request
     (this is the third repository in this consolidation campaign found
     with this exact bug pattern; treat it as a recurring fleet-wide risk,
     not a one-off).
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from typing import NoReturn

CRITICAL_SURFACES = (
    "src/index.ts",
    "tests/pure-functions.test.mjs",
    "package.json",
    "tsconfig.json",
)

INSTALL_LIFECYCLE_HOOKS = ("preinstall", "install", "postinstall", "prepare")

SECRET_LITERAL_PATTERN = re.compile(
    r'(?:api_key|secret|password|token)\s*=\s*["\'][a-zA-Z0-9_\-]{16,}["\']',
    re.IGNORECASE,
)

BALANCE_PAIRS = {"(": ")", "{": "}", "[": "]"}


def _fail(message: str) -> NoReturn:
    print(f"ECHO_ANALYTICS_ENGINE_CRITICAL_JOURNEY_FAILED: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_critical_surfaces() -> None:
    for surface in CRITICAL_SURFACES:
        if not pathlib.Path(surface).exists():
            _fail(f"missing critical surface: {surface}")


def _source_text() -> str:
    return pathlib.Path("src/index.ts").read_text(encoding="utf-8")


def check_index_ts_balanced() -> None:
    text = _source_text()
    for open_ch, close_ch in BALANCE_PAIRS.items():
        opens, closes = text.count(open_ch), text.count(close_ch)
        if opens != closes:
            _fail(
                f"src/index.ts has mismatched '{open_ch}'/'{close_ch}' counts "
                f"({opens} vs {closes}) -- possible truncation or corruption"
            )


def check_no_install_hooks() -> None:
    manifest = pathlib.Path("package.json")
    try:
        scripts = json.loads(manifest.read_text(encoding="utf-8")).get("scripts", {})
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        _fail(f"package.json is not valid JSON: {exc}")
    present = sorted(hook for hook in INSTALL_LIFECYCLE_HOOKS if hook in scripts)
    if present:
        _fail(f"package.json reintroduced install-lifecycle script(s): {', '.join(present)}")


def check_no_hardcoded_secrets() -> None:
    match = SECRET_LITERAL_PATTERN.search(_source_text())
    if match:
        _fail(f"src/index.ts contains a hardcoded secret-shaped literal: {match.group(0)[:40]}...")


def check_constant_time_auth() -> None:
    text = _source_text()
    if "timingSafeEqual(apiKey" not in text or "timingSafeEqual(authHeader" not in text:
        _fail("isAuthorized no longer calls timingSafeEqual on both the API-key and Bearer paths")
    if re.search(r"apiKey\s*===\s*env\.ECHO_API_KEY|authHeader\.slice\(7\)\s*===\s*env\.ECHO_API_KEY", text):
        _fail("isAuthorized regressed to a raw === comparison")


def main() -> None:
    check_critical_surfaces()
    check_index_ts_balanced()
    check_no_install_hooks()
    check_no_hardcoded_secrets()
    check_constant_time_auth()
    print(
        "ECHO_ANALYTICS_ENGINE_CRITICAL_JOURNEY_OK "
        f"critical_surfaces={len(CRITICAL_SURFACES)} "
        "install_hooks=0 hardcoded_secrets=0 constant_time_auth=1"
    )


if __name__ == "__main__":
    main()
