# codingStandard

> **언어:** [English README](README.md) · 한국어 (현재 문서) · [한국어 설치 가이드](i18n/ko/INSTALL.md)

AI coding agent, LLM/ML, Computer Vision 프로젝트에서 일관된 개발 규칙과 실행 환경 최적화를 적용하기 위한 Coding Standard입니다.

## 설치

저장소를 clone한 뒤 적용할 프로젝트의 루트에서 새 도메인 설치기를 실행합니다.

### Windows / PowerShell

대상 폴더가 없어도 자동으로 생성합니다. 언어와 도메인을 생략하면 선택 화면이 표시됩니다.

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target .
```

명시적으로 설치:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target . -Language ko -Domain vision
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target . -Language ko -Domain all
```

`-DryRun`으로 설치 전에 변경 대상을 확인하고, `-ConflictAction Ask|Merge|Overwrite|Skip`으로 기존 파일 처리를 지정할 수 있습니다.

### Linux / macOS

```bash
bash ./codingStandard/scripts/install-domains.sh .
```

명시적 설치:

```bash
bash ./codingStandard/scripts/install-domains.sh . ko vision ask false
bash ./codingStandard/scripts/install-domains.sh . ko all overwrite false
```

인자 순서는 `TARGET LANGUAGE DOMAIN CONFLICT_POLICY DRY_RUN`입니다.

## 설치 도메인

```text
common = Common만
llm    = Common + LLM
vision = Common + Vision
all    = Common + LLM + Vision
```

Common은 모든 프로젝트에 적용되는 기본 규칙입니다. LLM과 Vision은 작업 도메인에 맞는 Agent, Skill, Environment, 설정 및 Smoke Test를 추가합니다.

## 기존 파일 처리

기존 파일이 있으면 다음 중 하나를 선택합니다.

```text
Merge      기존 내용을 유지하고 codingStandard 관리 블록만 갱신
Overwrite  파일 전체 교체
Skip       기존 파일 유지
Ask        파일별로 결정
```

설치 전 `DryRun`을 사용해 변경 계획을 확인하는 것을 권장합니다.

## 지원하는 AI 개발 도구

| 도구 | 프로젝트 규칙 |
| --- | --- |
| OpenAI Codex / 호환 Agent | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Gemini CLI | `GEMINI.md` |
| GitHub Copilot | `.github/copilot-instructions.md` + `.github/instructions/` |
| Cursor | `.cursor/rules/coding-standard.mdc` |
| Windsurf | `.windsurf/rules/coding-standard.md` |
| Cline | `.clinerules/01-coding-standard.md` |
| Continue | `.continue/rules/coding-standard.md` |
| JetBrains Junie | `.junie/AGENTS.md` |
| Amazon Q Developer | `.amazonq/rules/coding-standard.md` |
| Aider | `CONVENTIONS.md` + `.aider.conf.yml` |
| Manus | `MANUS/PROJECT_INSTRUCTIONS.md` + `MANUS/SKILL.md` |

### Manus

Manus는 다른 coding agent처럼 저장소 루트의 특정 instruction 파일을 자동으로 읽는 방식이 공식 문서로 확인되지 않습니다. 현재 공식적인 연동 방식은 Manus Project Instructions와 파일 기반 Skill입니다.

설치기는 다음 리소스를 함께 제공합니다.

```text
MANUS/PROJECT_INSTRUCTIONS.md
MANUS/SKILL.md
MANUS/README.md
```

`MANUS/PROJECT_INSTRUCTIONS.md`의 내용을 Manus 프로젝트의 Project Instructions에 넣고, `MANUS/SKILL.md`는 Manus Skills에서 가져와 사용합니다. GitHub에서 Skill을 가져오는 경우와 커뮤니티 Skill 사용 시에는 포함된 스크립트와 리소스를 먼저 검토해야 합니다.

## Common / LLM / Vision 구조

```text
COMMON/
  공통 Agent / Skill / Environment / Experiment

LLM/
  LLM / NLP / RAG / Fine-tuning / Jupyter / Colab

VISION/
  Classification / Detection / Segmentation / OCR
  Pose Estimation / Image Generation / VLM

MANUS/
  Manus Project Instructions / Skill integration
```

## 실행 환경 최적화

환경은 특정 장비를 전제로 하지 않습니다. 실제 실행 환경을 측정하고 workload에 맞는 설정을 계산합니다.

```text
Detect
→ Measure
→ Resolve
→ Memory Smoke Test
→ Lock
→ Optimize
→ Execute
```

CPU, RAM, GPU/accelerator, VRAM, disk, CUDA/ROCm/MPS/DirectML, FP16/BF16 capability 등을 확인하고 보수적인 시작 설정을 선택합니다.

## LLM 사용법

```bash
python LLM/environment.py
python LLM/memory_smoke_test.py --cpu --steps 2
```

## Vision 사용법

Vision에서는 이미지 해상도, batch, channels, activation/feature-map memory, augmentation worker, cache, prefetch를 주요 자원 변수로 관리합니다.

```bash
python VISION/memory_smoke_test.py --device auto --image-size 224 --batch-size 1 --steps 2
```

## 학습 / 실험

장시간 학습에는 validation, Early Stopping, best Checkpoint, Resume, Ablation Study, 재현성 metadata를 기본 적용합니다.

설정은 도메인별 YAML로 관리합니다.

```text
LLM/config/training.yaml
LLM/config/ablation.yaml
VISION/config/training.yaml
VISION/config/ablation.yaml
```

실험 기록은 환경 프로파일, Git 상태, configuration hash, seed, model/dataset revision, metric, runtime, peak RAM/VRAM, checkpoint를 포함해야 합니다.

공통 experiment metadata helper는 `COMMON/experiment.py`에서 제공합니다.

## 플랫폼 검증

GitHub Actions는 실제 `windows-latest` runner에서 Windows PowerShell과 PowerShell 7을 사용해 영문/한글 및 Common/LLM/Vision/All 설치를 검증합니다. Dry-run, Merge, Unicode/공백 경로도 테스트합니다.

Google Colab용 검증 Notebook도 제공합니다.

[Colab 검증 Notebook 열기](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb)

Notebook은 깨끗한 Colab runtime에서 저장소를 clone하고 환경 측정, LLM/Vision Memory Smoke Test, repository validation을 수행한 뒤 JSON 결과를 저장합니다.

## 검증

```bash
python scripts/validate.py
python scripts/check_i18n.py
python scripts/test_installers.py
```

## 버전

현재 버전은 `VERSION` 파일에서 관리합니다.

## 구조

```text
codingStandard/
├── README.md
├── README.ko.md
├── INSTALL.md
├── LICENSE
├── VERSION
├── AGENTS.md
├── COMMON/
├── LLM/
├── VISION/
├── MANUS/
├── i18n/ko/
├── tests/colab/
├── .github/workflows/
└── scripts/
    ├── install-domains.ps1
    ├── install-domains.sh
    ├── validate.py
    ├── check_i18n.py
    ├── test_installers.py
    └── test_installers_windows.ps1
```

## 문서

- [영문 설치 가이드](INSTALL.md)
- [한글 설치 가이드](i18n/ko/INSTALL.md)
- [Common Agent](COMMON/AGENT.md)
- [LLM Agent](LLM/AGENT.md)
- [LLM Skill](LLM/SKILL.md)
- [Vision Agent](VISION/AGENT.md)
- [Vision Skill](VISION/SKILL.md)
- [Manus 연동](MANUS/README.md)
