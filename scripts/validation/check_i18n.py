#!/usr/bin/env python3
"""Validate runtime locale resources against the English canonical tree."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "i18n" / "languages.json"
REQUIRED_COMMON = ("core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md")
LOCALE_ROOT_FILES = frozenset({"README.md", "AGENT.md", "SKILL.md", "ENVIRONMENT.md", "COLAB.md", "ML_RUNTIME_VALIDATION.md"})
SEMANTIC_DOCUMENTS = ("core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md", "domains/ml/AGENT.md", "domains/ml/SKILL.md", "domains/ml/ENVIRONMENT.md", "domains/llm/AGENT.md", "domains/llm/SKILL.md", "domains/llm/ENVIRONMENT.md", "domains/vision/AGENT.md", "domains/vision/SKILL.md", "domains/vision/ENVIRONMENT.md", "platform/colab/AGENT.md", "platform/colab/SKILL.md")
CONCEPT_ALTERNATIVES = {
    "environment": {"en": ("environment", "runtime"), "ko": ("환경", "실행환경", "런타임", "environment", "runtime"), "zh-CN": ("环境", "运行环境", "运行时", "environment", "runtime"), "ja": ("環境", "実行環境", "ランタイム", "environment", "runtime"), "ru": ("сред", "окруж", "environment", "runtime"), "de": ("umgebung", "laufzeit", "environment", "runtime"), "it": ("ambiente", "esecuzione", "runtime", "environment"), "fr": ("environnement", "exécution", "runtime", "environment"), "es": ("entorno", "ejecución", "runtime", "environment"), "pt": ("ambiente", "execução", "runtime", "environment"), "tr": ("ortam", "çalışma ortamı", "çalışma", "runtime", "environment"), "ar": ("بيئة", "التشغيل", "environment", "runtime"), "hi": ("पर्यावरण", "execution environment", "runtime", "environment"), "id": ("lingkungan", "environment", "runtime"), "vi": ("môi trường", "execution environment", "runtime", "environment"), "th": ("สภาพแวดล้อม", "environment", "runtime"), "nl": ("omgeving", "execution environment", "runtime", "environment"), "pl": ("środowisko", "execution environment", "runtime", "environment"), "sv": ("miljö", "execution environment", "runtime", "environment"), "uk": ("середовище", "execution environment", "runtime", "environment")},
    "memory": {"en": ("memory", "ram", "vram"), "ko": ("메모리", "램", "브이램", "ram", "vram", "memory"), "zh-CN": ("内存", "显存", "ram", "vram", "memory"), "ja": ("メモリ", "メモリー", "ram", "vram", "memory"), "ru": ("памят", "оперативная", "видеопамят", "ram", "vram", "memory"), "de": ("speicher", "ram", "vram", "memory"), "it": ("memoria", "ram", "vram", "memory"), "fr": ("mémoire", "ram", "vram", "memory"), "es": ("memoria", "ram", "vram", "memory"), "pt": ("memória", "ram", "vram", "memory"), "tr": ("bellek", "ram", "vram", "memory"), "ar": ("ذاكرة", "ram", "vram", "memory"), "hi": ("मेमोरी", "राम", "वीआरएएम", "ram", "vram", "memory"), "id": ("memori", "ram", "vram", "memory"), "vi": ("bộ nhớ", "ram", "vram", "memory"), "th": ("หน่วยความจำ", "ram", "vram", "memory"), "nl": ("geheugen", "ram", "vram", "memory"), "pl": ("pamięć", "ram", "vram", "memory"), "sv": ("minne", "ram", "vram", "memory"), "uk": ("пам’ять", "пам'ять", "ram", "vram", "memory")},
    "early stopping": {"en": ("early stopping",), "ko": ("early stopping", "얼리 스토핑", "조기 종료"), "zh-CN": ("early stopping", "提前停止", "早停"), "ja": ("early stopping", "早期終了", "アーリーストッピング"), "ru": ("early stopping", "ранн", "досрочн"), "de": ("early stopping", "frühzeitiger abbruch"), "it": ("early stopping", "arresto anticipato"), "fr": ("early stopping", "arrêt précoce"), "es": ("early stopping", "parada temprana"), "pt": ("early stopping", "parada antecipada"), "tr": ("early stopping", "erken durdurma"), "ar": ("early stopping", "الإيقاف المبكر"), "hi": ("early stopping", "शीघ्र रोक", "जल्दी रोकना"), "id": ("early stopping", "penghentian dini"), "vi": ("early stopping", "dừng sớm"), "th": ("early stopping", "หยุดก่อนกำหนด"), "nl": ("early stopping", "vroegtijdig stoppen"), "pl": ("early stopping", "wczesne zatrzymanie"), "sv": ("early stopping", "tidigt stopp"), "uk": ("early stopping", "рання зупинка")},
    "checkpoint": {"en": ("checkpoint",), "ko": ("checkpoint", "체크포인트"), "zh-CN": ("checkpoint", "检查点"), "ja": ("checkpoint", "チェックポイント"), "ru": ("checkpoint", "контрольн", "восстановления"), "de": ("checkpoint", "prüfpunkt"), "it": ("checkpoint", "punto di controllo"), "fr": ("checkpoint", "point de contrôle"), "es": ("checkpoint", "punto de control"), "pt": ("checkpoint", "ponto de controlo", "ponto de controle"), "tr": ("checkpoint", "kontrol noktası"), "ar": ("checkpoint", "نقطة حفظ", "نقطة تحقق"), "hi": ("checkpoint", "चेकपॉइंट", "पुनर्प्राप्ति बिंदु"), "id": ("checkpoint", "titik pemeriksaan"), "vi": ("checkpoint", "điểm kiểm tra"), "th": ("checkpoint", "จุดตรวจสอบ"), "nl": ("checkpoint", "controlepunt"), "pl": ("checkpoint", "punkt kontrolny"), "sv": ("checkpoint", "kontrollpunkt"), "uk": ("checkpoint", "контрольна точка")},
}


def load_catalog(path: Path) -> tuple[dict, list[str]]:
    if not path.is_file(): return {}, ["i18n/languages.json is missing"]
    try: data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: return {}, [f"invalid i18n/languages.json: {exc}"]
    return (data, []) if isinstance(data, dict) else ({}, ["i18n/languages.json must contain an object"])


def fail(message: str, errors: list[str]) -> None: errors.append(message)


def validate_catalog_contract(root: Path, data: dict, errors: list[str]) -> dict[str, dict]:
    documentation, runtime_resources = data.get("documentation"), data.get("runtime_resources")
    if data.get("default") != "en": fail("default locale must be en", errors)
    if not isinstance(documentation, list) or not documentation: fail("documentation must be a non-empty list", errors); documentation = []
    if not isinstance(runtime_resources, list) or not runtime_resources: fail("runtime_resources must be a non-empty list", errors); runtime_resources = []
    docs_by_locale: dict[str, dict] = {}
    for entry in documentation:
        if not isinstance(entry, dict) or not all(isinstance(entry.get(k), str) and entry[k] for k in ("locale", "name", "path")): fail(f"invalid documentation entry: {entry!r}", errors); continue
        locale = entry["locale"]
        if locale in docs_by_locale: fail(f"duplicate documentation locale: {locale}", errors); continue
        docs_by_locale[locale] = entry
        if not (root / entry["path"]).is_file(): fail(f"documentation entrypoint missing for {locale}: {entry['path']}", errors)
    runtime_by_locale: dict[str, dict] = {}
    for entry in runtime_resources:
        if not isinstance(entry, dict) or not all(isinstance(entry.get(k), str) and entry[k] for k in ("locale", "name", "path")): fail(f"invalid runtime resource entry: {entry!r}", errors); continue
        locale = entry["locale"]
        if locale in runtime_by_locale: fail(f"duplicate runtime locale: {locale}", errors); continue
        runtime_by_locale[locale] = entry
        if not (root / entry["path"]).is_dir(): fail(f"runtime resource root missing for {locale}: {entry['path']}", errors)
        fallback = entry.get("fallback")
        if locale == "en" and fallback is not None: fail("English runtime locale must not have a fallback", errors)
        if locale != "en" and fallback != "en": fail(f"non-English runtime locale must explicitly fallback to en: {locale}", errors)
    for locale in sorted(set(runtime_by_locale) - set(docs_by_locale)): fail(f"runtime locale missing documentation entry: {locale}", errors)
    if "en" not in runtime_by_locale: fail("English must be declared as a runtime locale", errors)
    if "en" not in docs_by_locale: fail("English documentation entry is required", errors)
    return runtime_by_locale


def contains_any(text: str, alternatives: tuple[str, ...]) -> bool: return any(term.lower() in text for term in alternatives)


def validate_locale(root: Path, locale: str, entry: dict, errors: list[str]) -> None:
    if locale == "en": return
    localized_root = root / entry["path"]
    if not localized_root.is_dir(): return
    for rel in REQUIRED_COMMON:
        if not (localized_root / rel).is_file(): fail(f"runtime locale {locale} is missing required common resource: {rel}", errors)
    for path in sorted(p for p in localized_root.rglob("*") if p.is_file()):
        rel = path.relative_to(localized_root).as_posix()
        if rel in LOCALE_ROOT_FILES: continue
        if not (root / rel).is_file(): fail(f"runtime locale {locale} contains orphan resource without English source: {rel}", errors)
    semantic_docs_found = False
    for rel in SEMANTIC_DOCUMENTS:
        localized, canonical = localized_root / rel, root / rel
        if not localized.is_file() or not canonical.is_file(): continue
        semantic_docs_found = True
        if locale not in CONCEPT_ALTERNATIVES["environment"]:
            fail(f"missing semantic concept catalog for runtime locale: {locale}", errors); break
        localized_text, canonical_text = localized.read_text(encoding="utf-8").lower(), canonical.read_text(encoding="utf-8").lower()
        for concept, alternatives in CONCEPT_ALTERNATIVES.items():
            if contains_any(canonical_text, alternatives["en"]) and not contains_any(localized_text, alternatives[locale]): fail(f"runtime locale {locale} missing localized concept '{concept}' in {rel}", errors)
    if not semantic_docs_found: fail(f"runtime locale {locale} has no localized semantic policy documents", errors)


def validate(root: Path = ROOT, catalog_path: Path = CATALOG) -> list[str]:
    data, errors = load_catalog(catalog_path)
    if errors: return errors
    runtime_by_locale = validate_catalog_contract(root, data, errors)
    for locale, entry in runtime_by_locale.items(): validate_locale(root, locale, entry, errors)
    if errors: return errors
    docs_only = sorted({entry["locale"] for entry in data["documentation"]} - set(runtime_by_locale))
    print("i18n parity OK: runtime=" + ",".join(sorted(runtime_by_locale)) + " docs-only=" + ",".join(docs_only))
    return []


def main() -> int:
    errors = validate()
    if errors:
        print("i18n parity failed:")
        for error in errors: print(f"- {error}")
        return 1
    return 0


if __name__ == "__main__": raise SystemExit(main())
