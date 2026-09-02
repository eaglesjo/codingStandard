#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"
LANGUAGE="${2:-en}"
DOMAIN="${3:-all}"
POLICY="${4:-ask}"
DRY_RUN="${5:-false}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
mkdir -p "$TARGET"
TARGET="$(cd "$TARGET" && pwd)"
SRC="$ROOT"
if [[ -d "$ROOT/i18n/$LANGUAGE" ]]; then SRC="$ROOT/i18n/$LANGUAGE"; fi

case "$LANGUAGE" in en|ko|zh-CN|ja|ru) ;; *) echo 'language: en|ko|zh-CN|ja|ru' >&2; exit 1;; esac
case "$DOMAIN" in common|ml|llm|vision|colab|all) ;; *) echo 'domain: common|ml|llm|vision|colab|all' >&2; exit 1;; esac
case "$POLICY" in ask|merge|overwrite|skip) ;; *) echo 'policy: ask|merge|overwrite|skip' >&2; exit 1;; esac
case "$DRY_RUN" in true|false) ;; *) echo 'dry_run: true|false' >&2; exit 1;; esac

if [[ -z "${2:-}" ]]; then
  printf 'Language: 1) English  2) Korean  3) Simplified Chinese  4) Japanese  5) Russian\n'
  read -r -p 'Language [1]: ' choice
  case "${choice:-1}" in
    1|en) LANGUAGE="en";; 2|ko) LANGUAGE="ko";; 3|zh-CN) LANGUAGE="zh-CN";; 4|ja) LANGUAGE="ja";; 5|ru) LANGUAGE="ru";; *) echo 'Invalid language' >&2; exit 1;;
  esac
  SRC="$ROOT"; [[ -d "$ROOT/i18n/$LANGUAGE" ]] && SRC="$ROOT/i18n/$LANGUAGE"
fi
if [[ -z "${3:-}" ]]; then
  printf 'Domain: 1) Common  2) ML  3) LLM  4) Vision  5) Colab  6) All\n'
  read -r -p 'Domain [6]: ' choice
  case "${choice:-6}" in 1) DOMAIN="common";; 2) DOMAIN="ml";; 3) DOMAIN="llm";; 4) DOMAIN="vision";; 5) DOMAIN="colab";; 6) DOMAIN="all";; *) echo 'Invalid domain' >&2; exit 1;; esac
fi

if [[ "$LANGUAGE" != "en" ]]; then
  echo "Language resource mode: $LANGUAGE (translated locale with English fallback for missing domain resources)"
fi

files=(
  AGENTS.md CLAUDE.md GEMINI.md
  .github/copilot-instructions.md
  .cursor/rules/coding-standard.mdc .windsurf/rules/coding-standard.md
  .clinerules/01-coding-standard.md .continue/rules/01-coding-standard.md
  .junie/AGENTS.md .amazonq/rules/coding-standard.md
  docs/development/CONVENTIONS.md .aider.conf.yml
  core/common/AGENT.md core/common/SKILL.md core/common/ENVIRONMENT.md core/common/environment.py core/common/experiment.py core/common/dependencies.py
)
if [[ "$DOMAIN" == ml || "$DOMAIN" == all ]]; then
  files+=(.github/instructions/ml.instructions.md domains/ml/AGENT.md domains/ml/SKILL.md domains/ml/ENVIRONMENT.md domains/ml/README.md)
  while IFS= read -r f; do files+=("${f#$ROOT/}"); done < <(find "$ROOT/domains/ml/skills" -type f -name SKILL.md 2>/dev/null | sort)
fi
if [[ "$DOMAIN" == llm || "$DOMAIN" == all ]]; then
  files+=(.github/instructions/llm.instructions.md domains/llm/AGENT.md domains/llm/SKILL.md domains/llm/ENVIRONMENT.md domains/llm/environment.py domains/llm/experiment.py domains/llm/memory_smoke_test.py domains/llm/README.md domains/llm/config/training.yaml domains/llm/config/ablation.yaml)
  while IFS= read -r f; do files+=("${f#$ROOT/}"); done < <(find "$ROOT/domains/llm/skills" -type f -name SKILL.md 2>/dev/null | sort)
fi
if [[ "$DOMAIN" == vision || "$DOMAIN" == all ]]; then
  files+=(.github/instructions/vision.instructions.md domains/vision/AGENT.md domains/vision/SKILL.md domains/vision/ENVIRONMENT.md domains/vision/memory_smoke_test.py domains/vision/README.md domains/vision/config/training.yaml domains/vision/config/ablation.yaml)
  while IFS= read -r f; do files+=("${f#$ROOT/}"); done < <(find "$ROOT/domains/vision/skills" -type f -name SKILL.md 2>/dev/null | sort)
fi
if [[ "$DOMAIN" == colab || "$DOMAIN" == all ]]; then
  files+=(platform/colab/AGENT.md platform/colab/SKILL.md)
fi

conflict_action() {
  local rel="$1" action="$POLICY" c
  [[ "$POLICY" != "ask" ]] && { printf '%s' "$action"; return; }
  while true; do
    read -r -p "Existing $rel [m]erge [o]verwrite [s]kip: " c
    c="$(printf '%s' "$c" | tr '[:upper:]' '[:lower:]')"
    case "$c" in m) echo merge; return;; o) echo overwrite; return;; s) echo skip; return;; esac
  done
}

merge_text() {
  local old="$1" new="$2" rel="$3" start end tmp
  start='<!-- BEGIN CODINGSTANDARD MANAGED BLOCK -->'; end='<!-- END CODINGSTANDARD MANAGED BLOCK -->'
  [[ "$rel" =~ \.(py|ya?ml|sh|bash)$ ]] && { start='# BEGIN CODINGSTANDARD MANAGED BLOCK'; end='# END CODINGSTANDARD MANAGED BLOCK'; }
  if grep -Fq "$start" <<< "$old"; then
    tmp="$(mktemp)"; printf '%s\n' "$new" > "$tmp"
    awk -v s="$start" -v e="$end" -v nf="$tmp" 'BEGIN { while ((getline line < nf) > 0) new = new line ORS; close(nf) } $0 == s { print; printf "%s", new; inside=1; next } $0 == e { print; inside=0; next } !inside { print }' <<< "$old"
    rm -f "$tmp"
  else
    printf '%s\n\n%s\n%s\n%s\n' "${old%$'\n'}" "$start" "$new" "$end"
  fi
}

for rel in "${files[@]}"; do
  src="$SRC/$rel"
  [[ -f "$src" ]] || src="$ROOT/$rel"
  dst="$TARGET/$rel"
  [[ -f "$src" ]] || { echo "Missing template: $rel" >&2; exit 1; }
  if [[ "$DRY_RUN" == true ]]; then
    [[ -e "$dst" ]] && echo "[DRY-RUN] EXIST $rel" || echo "[DRY-RUN] CREATE $rel"; continue
  fi
  mkdir -p "$(dirname "$dst")"
  if [[ ! -e "$dst" ]]; then cp "$src" "$dst"; continue; fi
  action="$(conflict_action "$rel")"
  case "$action" in skip) ;; overwrite) cp "$src" "$dst" ;; merge) old="$(cat "$dst")"; new="$(cat "$src")"; merge_text "$old" "$new" "$rel" > "$dst" ;; esac
done

echo "Installed: language=$LANGUAGE domain=$DOMAIN dry_run=$DRY_RUN"
