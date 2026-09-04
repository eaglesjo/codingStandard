# Language Resources

`codingStandard` separates **documentation localization** from **runtime policy localization** so a language is never advertised as fully translated before its Agent / Skill / Environment resources are actually translated and validated.

## Documentation languages

| Locale | Language | Entry point |
|---|---|---|
| `en` | English | [`README.md`](../README.md) |
| `ko` | 한국어 | [`ko/README.md`](ko/README.md) |
| `fr` | Français | [`fr/README.md`](fr/README.md) |
| `es` | Español | [`es/README.md`](es/README.md) |
| `zh-CN` | 简体中文 | [`zh-CN/README.md`](zh-CN/README.md) |
| `ja` | 日本語 | [`ja/README.md`](ja/README.md) |
| `ru` | Русский | [`ru/README.md`](ru/README.md) |
| `tr` | Türkçe | [`tr/README.md`](tr/README.md) |

## Runtime resource languages

The installer currently provides validated runtime resources for five locale codes:

- `en` — English canonical resources
- `ko` — Korean localized resources
- `zh-CN` — Simplified Chinese localized common policy resources
- `ja` — Japanese localized common policy resources
- `ru` — Russian localized common policy resources

The documentation-only locales `fr`, `es`, and `tr` are intentionally not advertised as runtime-resource languages yet. Domain resources that have not been translated are resolved from the English source tree, and the installer reports fallback mode explicitly.

## Runtime i18n parity validation

CI validates every locale declared under `runtime_resources` in [`languages.json`](languages.json). Non-English runtime locales must declare an explicit `fallback` to `en`, contain the required `core/common` policy resources, and keep every localized file paired with an English canonical source. The semantic-policy checks cover `AGENT.md`, `SKILL.md`, and `ENVIRONMENT.md` resources when those localized domain files exist, using locale-aware concept alternatives.

Documentation-only locales are intentionally outside runtime parity checks. Adding a new runtime locale therefore requires a valid semantic-concept vocabulary in `scripts/validation/check_i18n.py`; adding only a README remains a documentation-only change.

## Colab documentation

The public Colab validation flow is documented in locale-specific guides:

| Locale | Colab guide |
|---|---|
| `ko` | [`ko/COLAB.md`](ko/COLAB.md) |
| `fr` | [`fr/COLAB.md`](fr/COLAB.md) |
| `es` | [`es/COLAB.md`](es/COLAB.md) |
| `zh-CN` | [`zh-CN/COLAB.md`](zh-CN/COLAB.md) |
| `ja` | [`ja/COLAB.md`](ja/COLAB.md) |
| `ru` | [`ru/COLAB.md`](ru/COLAB.md) |
| `tr` | [`tr/COLAB.md`](tr/COLAB.md) |

The English canonical Colab guide remains [`tests/colab/README.md`](../tests/colab/README.md).

## ML/DL runtime validation

Locale-specific ML/DL runtime validation guides are available for the seven non-English documentation locales:

| Locale | Runtime validation guide |
|---|---|
| `ko` | [`ko/ML_RUNTIME_VALIDATION.md`](ko/ML_RUNTIME_VALIDATION.md) |
| `fr` | [`fr/ML_RUNTIME_VALIDATION.md`](fr/ML_RUNTIME_VALIDATION.md) |
| `es` | [`es/ML_RUNTIME_VALIDATION.md`](es/ML_RUNTIME_VALIDATION.md) |
| `zh-CN` | [`zh-CN/ML_RUNTIME_VALIDATION.md`](zh-CN/ML_RUNTIME_VALIDATION.md) |
| `ja` | [`ja/ML_RUNTIME_VALIDATION.md`](ja/ML_RUNTIME_VALIDATION.md) |
| `ru` | [`ru/ML_RUNTIME_VALIDATION.md`](ru/ML_RUNTIME_VALIDATION.md) |
| `tr` | [`tr/ML_RUNTIME_VALIDATION.md`](tr/ML_RUNTIME_VALIDATION.md) |

The English canonical guide remains [`docs/development/ML_RUNTIME_VALIDATION.md`](../docs/development/ML_RUNTIME_VALIDATION.md) in the private source tree; the public distribution receives the public-safe documentation set selected by the release workflow.

## Localization rules

1. English remains the canonical source of truth.
2. A locale may be listed as a documentation language once its README entrypoint exists.
3. A locale may be listed as a runtime resource language when it contains validated localized resources for at least the common policy layer.
4. Missing domain-specific translations must fall back to English rather than copying or inventing untranslated text.
5. Documentation and runtime support must never be conflated.
6. New locales must be added to `i18n/languages.json` and validated in CI.
