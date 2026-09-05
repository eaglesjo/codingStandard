# Language Resources

`codingStandard` separates **documentation localization** from **runtime policy localization** so a language is never advertised as fully translated before its Agent / Skill / Environment resources are actually translated and validated.

## Documentation languages

The documentation catalog currently covers 20 locales:

| Locale | Language |
|---|---|
| `en` | English |
| `ko` | 한국어 |
| `fr` | Français |
| `es` | Español |
| `zh-CN` | 简体中文 |
| `ja` | 日本語 |
| `ru` | Русский |
| `tr` | Türkçe |
| `de` | Deutsch |
| `it` | Italiano |
| `pt` | Português |
| `ar` | العربية |
| `hi` | हिन्दी |
| `id` | Bahasa Indonesia |
| `vi` | Tiếng Việt |
| `th` | ไทย |
| `nl` | Nederlands |
| `pl` | Polski |
| `sv` | Svenska |
| `uk` | Українська |

Each documentation locale has its own README entrypoint and is tracked in [`languages.json`](languages.json).

## Runtime resource languages

The installer currently provides validated runtime resources for five locale codes:

- `en` — English canonical resources
- `ko` — Korean localized resources
- `zh-CN` — Simplified Chinese localized common policy resources
- `ja` — Japanese localized common policy resources
- `ru` — Russian localized common policy resources

The remaining documentation locales are intentionally not advertised as runtime-resource languages yet. Domain resources that have not been translated are resolved from the English source tree, and the installer reports fallback mode explicitly.

## Runtime i18n parity validation

CI validates every locale declared under `runtime_resources` in [`languages.json`](languages.json). Non-English runtime locales must declare an explicit `fallback` to `en`, contain the required `core/common` policy resources, and keep every localized file paired with an English canonical source. The semantic-policy checks cover `AGENT.md`, `SKILL.md`, and `ENVIRONMENT.md` resources when those localized domain files exist, using locale-aware concept alternatives.

Documentation-only locales are intentionally outside runtime parity checks. Promoting a documentation locale to runtime support therefore requires translated core resources, a semantic-concept vocabulary, and CI validation.

## Localization rules

1. English remains the canonical source of truth.
2. A locale may be listed as a documentation language once its README entrypoint exists.
3. A locale may be listed as a runtime resource language when it contains validated localized resources for at least the common policy layer.
4. Missing domain-specific translations must fall back to English rather than copying or inventing untranslated text.
5. Documentation and runtime support must never be conflated.
6. New locales must be added to `i18n/languages.json` and validated in CI.
7. RTL locales such as Arabic must be treated as layout-sensitive when promoted to runtime support.
