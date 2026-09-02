#!/usr/bin/env python3
"""Validate the documentation/runtime language support contract."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "i18n" / "languages.json"
REQUIRED_COMMON = ("core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md")


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def main() -> int:
    if not CATALOG.is_file():
        return fail("i18n/languages.json is missing")

    try:
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"invalid i18n/languages.json: {exc}")

    if data.get("default") != "en":
        return fail("default locale must be en")

    documentation = data.get("documentation")
    runtime_resources = data.get("runtime_resources")
    if not isinstance(documentation, list) or not documentation:
        return fail("documentation must be a non-empty list")
    if not isinstance(runtime_resources, list) or not runtime_resources:
        return fail("runtime_resources must be a non-empty list")

    docs_by_locale: dict[str, dict] = {}
    for entry in documentation:
        if not all(isinstance(entry.get(key), str) and entry[key] for key in ("locale", "name", "path")):
            return fail(f"invalid documentation entry: {entry!r}")
        locale = entry["locale"]
        if locale in docs_by_locale:
            return fail(f"duplicate documentation locale: {locale}")
        docs_by_locale[locale] = entry
        if not (ROOT / entry["path"]).is_file():
            return fail(f"documentation entrypoint missing for {locale}: {entry['path']}")

    runtime_by_locale: dict[str, dict] = {}
    for entry in runtime_resources:
        if not all(isinstance(entry.get(key), str) and entry[key] for key in ("locale", "name", "path")):
            return fail(f"invalid runtime resource entry: {entry!r}")
        locale = entry["locale"]
        if locale in runtime_by_locale:
            return fail(f"duplicate runtime locale: {locale}")
        runtime_by_locale[locale] = entry
        if not (ROOT / entry["path"]).is_dir():
            return fail(f"runtime resource root missing for {locale}: {entry['path']}")
        fallback = entry.get("fallback")
        if locale == "en" and fallback is not None:
            return fail("English runtime locale must not have a fallback")
        if locale != "en" and fallback not in {"en"}:
            return fail(f"non-English runtime locale must explicitly fallback to en: {locale}")
        if locale != "en":
            localized_root = ROOT / entry["path"]
            missing_common = [rel for rel in REQUIRED_COMMON if not (localized_root / rel).is_file()]
            if missing_common:
                return fail(f"runtime locale {locale} is missing translated common resources: {', '.join(missing_common)}")

    if not set(runtime_by_locale).issubset(docs_by_locale):
        missing = sorted(set(runtime_by_locale) - set(docs_by_locale))
        return fail(f"runtime locales missing documentation entries: {', '.join(missing)}")

    if "en" not in docs_by_locale or "ko" not in docs_by_locale:
        return fail("English and Korean documentation entries are required")

    print(
        "language catalog OK: documentation="
        + ",".join(docs_by_locale)
        + " runtime="
        + ",".join(runtime_by_locale)
        + " common-policy-locales="
        + ",".join(sorted(runtime_by_locale))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
