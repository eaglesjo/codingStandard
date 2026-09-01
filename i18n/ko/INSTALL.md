# 설치 가이드

`install-domains.ps1`과 `install-domains.sh`가 첫 공개 배포 전 공식 설치기입니다.

## 1. Clone

```bash
git clone https://github.com/eaglesjo/codingStandard.git
```

적용하려는 프로젝트의 루트에서 설치기를 실행합니다. 대상 폴더가 없으면 설치기가 생성합니다.

## 2. 언어와 도메인 선택

설치기는 영문/한글과 다음 여섯 가지 도메인을 지원합니다.

```text
언어
  en = English
  ko = Korean

도메인
  common = 공통 규칙만
  ml     = Common + 일반 ML/DL lifecycle
  llm    = Common + LLM
  vision = Common + Vision
  colab  = Common + Colab runtime 정책
  all    = Common + ML + LLM + Vision + Colab
```

### Windows / PowerShell

대화형 설치:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\installers\install-domains.ps1 -Target .
```

명시적 설치:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\installers\install-domains.ps1 -Target . -Language ko -Domain ml
```

### Linux / macOS

대화형 설치:

```bash
bash ./codingStandard/scripts/installers/install-domains.sh .
```

명시적 설치:

```bash
bash ./codingStandard/scripts/installers/install-domains.sh . ko ml overwrite false
```

인자 순서는 다음과 같습니다.

```text
TARGET LANGUAGE DOMAIN CONFLICT_POLICY DRY_RUN
```

## 3. 설치 전 미리보기

PowerShell:

```powershell
... -Language ko -Domain all -DryRun
```

Bash:

```bash
bash ./codingStandard/scripts/installers/install-domains.sh . ko all ask true
```

Dry-run은 대상 프로젝트를 변경하지 않습니다.

## 4. 기존 파일 처리

대상 파일이 이미 존재하면 다음 중 하나를 선택합니다.

```text
Ask       파일별로 선택
Merge     기존 내용을 유지하고 codingStandard 관리 블록만 갱신
Overwrite 대상 파일 전체를 교체
Skip      기존 파일을 그대로 유지
```

프로젝트 자체 규칙을 유지해야 하는 Agent 지침 파일에는 `Merge`를 권장합니다. 표준이 전체를 소유하는 파일에는 `Overwrite`를 사용할 수 있습니다.

## 5. Common 설치 내용

Common은 모든 프로젝트에 공통으로 적용되는 AI Agent 진입점과 규칙을 설치합니다.

```text
AGENTS.md
CLAUDE.md
GEMINI.md
.github/*
.cursor/*
.windsurf/*
.clinerules/*
.continue/*
.junie/*
.amazonq/*
CONVENTIONS.md
.aider.conf.yml
core/common/*
```

## 6. ML 추가 내용

ML 도메인을 선택하면 다음 lifecycle과 Skill이 추가됩니다.

```text
.github/instructions/ml.instructions.md
domains/ml/AGENT.md
domains/ml/SKILL.md
domains/ml/ENVIRONMENT.md
domains/ml/skills/*
```

Skill은 Data Validation, Experiment Design, Evaluation, Training, Distributed Training, HPO, Inference, MLOps를 다룹니다.

## 7. LLM 추가 내용

LLM 도메인을 선택하면 다음이 추가됩니다.

```text
domains/llm/AGENT.md
domains/llm/SKILL.md
domains/llm/ENVIRONMENT.md
domains/llm/environment.py
domains/llm/memory_smoke_test.py
domains/llm/skills/*
```

LLM에는 기존 규칙과 함께 Fine-Tuning, PEFT, Quantization Skill이 포함됩니다.

## 8. Vision 추가 내용

Vision 도메인을 선택하면 다음이 추가됩니다.

```text
domains/vision/AGENT.md
domains/vision/SKILL.md
domains/vision/ENVIRONMENT.md
domains/vision/memory_smoke_test.py
domains/vision/skills/*
```

Vision Skill은 Classification, Detection, Segmentation, OCR, Pose Estimation, Image Generation, VLM을 다룹니다.

## 9. Colab 추가 내용

Colab 도메인을 선택하면 다음 실행 정책이 추가됩니다.

```text
platform/colab/AGENT.md
platform/colab/SKILL.md
```

Google Colab을 ephemeral runtime으로 취급하고 dependency bootstrap, 실제 자원 측정, smoke test, durable checkpoint/artifact, Resume 검증을 적용합니다.

## 10. 설치 후 검증

공통 검증:

```bash
python scripts/validation/validate.py
python scripts/installers/test_installers.py
```

LLM이 설치된 경우:

```bash
python domains/llm/memory_smoke_test.py --cpu --steps 2
```

Vision이 설치된 경우:

```bash
python domains/vision/memory_smoke_test.py --device auto --image-size 224 --batch-size 1 --steps 2
```

Colab에서는 `tests/colab/`의 검증 Notebook을 fresh runtime에서 실행하고 checkpoint persistence/resume을 확인합니다.

## 11. Windows / Colab 검증

Windows 설치 동작은 GitHub Actions에서 자동 검증합니다. PowerShell 5.1과 PowerShell 7, 언어/도메인 조합, Dry-run, Merge, Unicode 및 공백 경로를 확인합니다.

Google Colab에서는 저장소의 검증 Notebook을 실행할 수 있습니다.

[Colab 검증 Notebook](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb)

## 12. 권장 작업 흐름

```text
설치
→ Agent adapter
→ 공통 정책
→ 관련 ML/LLM/Vision domain
→ Colab이면 ephemeral runtime 정책
→ Data 검증
→ 실제 환경 측정
→ Runtime 설정 계산
→ Baseline / Experiment
→ Memory Smoke Test
→ 환경 확정
→ 개발 / 학습 / 추론
→ Evaluation
→ Early Stopping / Checkpoint / Resume
→ Ablation / Experiment 기록
→ 최종 검증
```