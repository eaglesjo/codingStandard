# codingStandard

> **언어:** [English README](README.md) · 한국어 (현재 문서)

AI coding agent, LLM/ML, Computer Vision 프로젝트에서 일관된 개발 규칙과 실행 환경 최적화를 적용하기 위한 Coding Standard입니다.

## 설치

저장소를 clone한 뒤 적용할 프로젝트의 루트에서 새 도메인 설치기를 실행합니다.

### Windows / PowerShell

인자를 생략하면 언어와 도메인을 선택합니다.

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

공통 진입점과 도구별 프로젝트 규칙을 설치합니다.

| 도구 | 프로젝트 규칙 |
| --- | --- |
| OpenAI Codex / 호환 Agent | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Gemini CLI | `GEMINI.md` |
| GitHub Copilot | `.github/copilot-instructions.md` + `.github/instructions/` |
| Cursor | `.cursor/rules/coding-standard.mdc` |
| Windsurf | `.windsurf/rules/coding-standard.md` |
| Cline | `.clinerules/01-coding-standard.md` |
| Continue | `.continue/rules/01-coding-standard.md` |
| JetBrains Junie | `.junie/AGENTS.md` |
| Amazon Q Developer | `.amazonq/rules/coding-standard.md` |
| Aider | `CONVENTIONS.md` + `.aider.conf.yml` |

## 공통 / LLM / Vision 구조

```text
COMMON/
  공통 Agent / Skill / Environment

LLM/
  LLM / NLP / RAG / Fine-tuning / Jupyter / Colab

VISION/
  Classification / Detection / Segmentation / OCR
  Pose Estimation / Image Generation / VLM
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

장시간 학습에는 validation, Early Stopping, best Checkpoint, Resume, Ablation Study, 재현성 metadata를 기본 적용합니다.

## Vision 사용법

Vision에서는 이미지 해상도, batch, channels, activation/feature-map memory, augmentation worker, cache, prefetch를 주요 자원 변수로 관리합니다.

```bash
python VISION/memory_smoke_test.py --device auto --image-size 224 --batch-size 1 --steps 2
```

## Skills

LLM:

```text
LLM/skills/
├── environment/
├── training/
├── ablation/
├── notebook/
├── debugging/
└── release/
```

Vision:

```text
VISION/skills/
├── classification/
├── detection/
├── segmentation/
├── ocr/
├── pose-estimation/
├── image-generation/
└── vlm/
```

## 실험 / 학습

설정은 도메인별 YAML로 관리합니다.

```text
LLM/config/training.yaml
LLM/config/ablation.yaml
VISION/config/training.yaml
VISION/config/ablation.yaml
```

실험 기록은 환경 프로파일, Git 상태, configuration hash, seed, model/dataset revision, metric, runtime, peak RAM/VRAM, checkpoint를 포함해야 합니다.

## 검증

```bash
python scripts/validate.py
python scripts/check_i18n.py
python scripts/test_installers.py
```

GitHub Actions는 저장소 구조, Python syntax, 하드웨어 하드코딩, 영/한 필수 문서, 설치기 동작 및 CPU Memory Smoke Test를 검증합니다.

## 버전

현재 버전은 `VERSION` 파일에서 관리합니다.
