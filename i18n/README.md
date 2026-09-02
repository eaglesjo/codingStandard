# Language Resources

`codingStandard` separates **documentation localization** from **runtime policy localization** so a language is never advertised as fully translated before its Agent / Skill / Environment resources are actually translated and validated.

## Documentation languages

| Locale | Language | Entry point |
|---|---|---|
| `en` | English | [`README.md`](../README.md) |
| `ko` | 한국어 | [`ko/README.md`](ko/README.md) |
| `zh-CN` | 简体中文 | [`zh-CN/README.md`](zh-CN/README.md) |
| `ja` | 日本語 | [`ja/README.md`](ja/README.md) |
| `ru` | Русский | [`ru/README.md`](ru/README.md) |

## Runtime resource languages

The installer currently accepts five locale codes:

- `en` — English canonical resources
- `ko` — Korean localized resources
- `zh-CN` — Simplified Chinese localized common policy resources
- `ja` — Japanese localized common policy resources
- `ru` — Russian localized common policy resources

All five locales can be installed through the common domain. Domain resources that have not yet been translated are resolved from the English source tree, and the installer reports this fallback mode explicitly.

## Localization rules

1. English remains the canonical source of truth.
2. A locale may be listed as a documentation language once its README entrypoint exists.
3. A locale may be listed as a runtime resource language when it contains validated localized resources for at least the common policy layer.
4. Missing domain-specific translations must fall back to English rather than copying or inventing untranslated text.
5. Documentation and runtime support must never be conflated.
6. New locales must be added to `i18n/languages.json` and validated in CI.
