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
if [[ "$LANGUAGE" == "ko" && -d "$ROOT/i18n/ko" ]]; then SRC="$ROOT/i18n/ko"; fi

case "$LANGUAGE" in en|ko) ;; *) echo 'language: en|ko' >&2; exit 1;; esac
case "$DOMAIN" in common|llm|vision|all) ;; *) echo 'domain: common|llm|vision|all' >&2; exit 1;; esac
case "$POLICY" in ask|merge|overwrite|skip) ;; *) echo 'policy: ask|merge|overwrite|skip' >&2; exit 1;; esac
case "$DRY_RUN" in true|false) ;; *) echo 'dry_run: true|false' >&2; exit 1;; esac

if [[ -z "${2:-}" ]]; then
  printf 'Language: 1) English  2) Korean\n'
  read -r -p 'Language [1]: ' choice
  [[ "${choice:-1}" == 2 ]] && LANGUAGE="ko" || LANGUAGE="en"
  SRC="$ROOT"; [[ "$LANGUAGE" == "ko" && -d "$ROOT/i18n/ko" ]] && SRC="$ROOT/i18n/ko"
fi
if [[ -z "${3:-}" ]]; then
  printf 'Domain: 1) Common  2) LLM  3) Vision  4) All\n'
  read -r -p 'Domain [4]: ' choice
  case "${choice:-4}" in 1) DOMAIN="common";; 2) DOMAIN="llm";; 3) DOMAIN="vision";; 4) DOMAIN="all";; *) echo 'Invalid domain' >&2; exit 1;; esac
fi

files=(
  AGENTS.md CLAUDE.md GEMINI.md
  .github/copilot-instructions.md
  .cursor/rules/coding-standard.mdc .windsurf/rules/coding-standard.md
  .clinerules/01-coding-standard.md .continue/rules/01-coding-standard.md
  .junie/AGENTS.md .amazonq/rules/coding-standard.md
  docs/development/CONVENTIONS.md .aider.conf.yml
  core/common/AGENT.md core/common/SKILL.md core/common/ENVIRONMENT.md core/common/environment.py core/common/experiment.py
  domains/manus/PROJECT_INSTRUCTIONS.md domains/manus/SKILL.md domains/manus/README.md
)
if [[ "$DOMAIN" == llm || "$DOMAIN" == all ]]; then
  files+=(.github/instructions/llm.instructions.md domains/llm/AGENT.md domains/llm/SKILL.md domains/llm/ENVIRONMENT.md domains/llm/environment.py domains/llm/experiment.py domains/llm/memory_smoke_test.py domains/llm/README.md domains/llm/config/training.yaml domains/llm/config/ablation.yaml)
  while IFS= read -r f; do files+=("${f#$SRC/}"); done < <(find "$SRC/domains/llm/skills" -type f -name SKILL.md 2>/dev/null | sort)
fi
if [[ "$DOMAIN" == vision || "$DOMAIN" == all ]]; then
  files+=(.github/instructions/vision.instructions.md domains/vision/AGENT.md domains/vision/SKILL.md domains/vision/ENVIRONMENT.md domains/vision/memory_smoke_test.py domains/vision/README.md domains/vision/config/training.yaml domains/vision/config/ablation.yaml)
  while IFS= read -r f; do files+=("${f#$SRC/}"); done < <(find "$SRC/domains/vision/skills" -type f -name SKILL.md 2>/dev/null | sort)
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
  src="$SRC/$rel"; dst="$TARGET/$rel"
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
