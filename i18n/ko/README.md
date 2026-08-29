# codingStandard 한국어 안내

`codingStandard`의 한국어 문서와 설치 리소스를 제공합니다.

## 설치

영문/한국어 설치기는 저장소의 `scripts/installers/`에 있습니다.

### Windows / PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\installers\install-domains.ps1 -Target . -Language ko -Domain all
```

### Linux / macOS

```bash
bash ./codingStandard/scripts/installers/install-domains.sh . ko all overwrite false
```

인자 순서는 `TARGET LANGUAGE DOMAIN CONFLICT_POLICY DRY_RUN`입니다.

## 설치 도메인

```text
common = Common만
all    = Common + LLM + Vision
llm    = Common + LLM
vision = Common + Vision
```

기존 파일은 `Ask`, `Merge`, `Overwrite`, `Skip` 정책으로 처리할 수 있습니다.

## 한국어 리소스 구조

```text
i18n/ko/
├── README.md
├── INSTALL.md
├── AGENT.md
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── .github/
├── .cursor/
├── .clinerules/
├── .continue/
├── .junie/
├── .amazonq/
├── .windsurf/
├── .aider.conf.yml
├── core/
│   └── common/
├── domains/
│   ├── llm/
│   ├── vision/
│   └── manus/
└── docs/
    └── development/
        └── CONVENTIONS.md
```

한국어 리소스는 영문 저장소의 구조를 가능한 한 그대로 미러링하여 설치기와 i18n 검사가 동일한 상대 경로를 사용할 수 있도록 합니다.

## 주요 문서

- `INSTALL.md` — 한국어 설치 가이드
- `AGENT.md` / `AGENTS.md` — AI Agent 규칙
- `core/common/` — 공통 실행환경 및 재현성 규칙
- `domains/llm/` — LLM/ML 규칙과 Skills
- `domains/vision/` — Computer Vision 규칙과 Skills
- `domains/manus/` — Manus Project Instructions와 Skill
- `docs/development/CONVENTIONS.md` — 개발 규칙

## Google Colab

Colab 검증 Notebook은 `tests/colab/codingstandard_colab_test.ipynb`에 있습니다. Notebook은 실제 Colab runtime을 기준으로 환경을 감지하며, 로컬 클라이언트의 OS와 혼동하지 않습니다.
