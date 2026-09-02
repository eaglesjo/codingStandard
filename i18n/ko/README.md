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
ml     = Common + 일반 ML/DL lifecycle
llm    = Common + LLM
vision = Common + Vision
colab  = Common + Colab runtime 정책
all    = Common + ML + LLM + Vision + Colab
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
│   ├── ml/
│   ├── llm/
│   └── vision/
├── platform/
│   └── colab/
└── docs/
    └── development/
        └── CONVENTIONS.md
```

한국어 리소스는 영문 저장소의 구조를 가능한 한 그대로 미러링합니다. 새 리소스 중 아직 한국어 전용 번역이 없는 기술 task Skill은 설치기에서 영문 원본으로 안전하게 fallback합니다.

## 주요 문서

- `INSTALL.md` — 한국어 설치 가이드
- `AGENT.md` / `AGENTS.md` — AI Agent 규칙
- `core/common/` — 공통 실행환경 및 재현성 규칙
- `domains/ml/` — 일반 ML/DL lifecycle과 공통 Skills
- `domains/llm/` — LLM/ML 규칙과 Skills
- `domains/vision/` — Computer Vision 규칙과 Skills
- `platform/colab/` — Colab ephemeral runtime 정책
- `docs/development/CONVENTIONS.md` — 개발 규칙

## Google Colab

공개 배포 저장소에서는 GitHub README에서 Colab Notebook을 직접 열어 검증할 수 있습니다. Private repository 자격증명 없이 공개 `eaglesjo/codingStandard`에서 테스트하는 것을 기본 시나리오로 합니다.

### 원클릭 검증

- 종합 검증: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb)
- Clean runtime: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/clean_runtime_validation.ipynb)
- LLM QLoRA: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/llm_qlora_validation.ipynb)
- RAG: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/rag_validation.ipynb)

기본 종합 Notebook은 실제 Colab runtime을 기준으로 환경을 감지하며, 로컬 클라이언트의 OS와 혼동하지 않습니다. 장시간 작업은 durable checkpoint와 Resume을 전제로 합니다.
