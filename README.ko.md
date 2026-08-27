# codingStandard

> **언어:** [English README](README.md) · 한국어 (현재 문서)

여러 프로젝트에서 AI coding agent가 일관된 규칙으로 개발할 수 있도록 환경 확인, 자원 프로파일링, 실행 설정 결정, 메모리 안전 실행, 학습 재현성을 표준화하는 Coding Standard 저장소입니다.

## 설치

저장소를 clone한 뒤 **적용할 프로젝트의 루트 디렉터리에서** 설치 스크립트를 실행합니다.

### Windows / PowerShell

설치 중 언어를 선택:

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-coding-standard.ps1 -Target .
```

영문:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-coding-standard.ps1 -Target . -Language en
```

한글:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-coding-standard.ps1 -Target . -Language ko
```

Preview:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-coding-standard.ps1 -Target . -Language ko -DryRun
```

충돌 정책:

```powershell
... -ConflictAction Ask
... -ConflictAction Merge
... -ConflictAction Overwrite
... -ConflictAction Skip
```

### Linux / macOS

설치 중 언어를 선택:

```bash
git clone https://github.com/eaglesjo/codingStandard.git
bash ./codingStandard/scripts/install-coding-standard.sh .
```

영문 / 한글:

```bash
bash ./codingStandard/scripts/install-coding-standard.sh . en
bash ./codingStandard/scripts/install-coding-standard.sh . ko
```

Preview 및 충돌 정책:

```bash
bash ./codingStandard/scripts/install-coding-standard.sh . ko ask true
bash ./codingStandard/scripts/install-coding-standard.sh . ko merge false
bash ./codingStandard/scripts/install-coding-standard.sh . ko overwrite false
bash ./codingStandard/scripts/install-coding-standard.sh . ko skip false
```

## 기존 파일 충돌 처리

`Ask` 모드에서는 다음을 선택할 수 있습니다.

```text
M = Merge
O = Overwrite
S = Skip
A = Merge all remaining
W = Overwrite all remaining
K = Skip all remaining
```

`Merge`는 기존 파일을 보존하면서 `codingStandard` 관리 블록만 추가 또는 갱신합니다. Aider의 YAML 설정은 구조를 고려하여 안전하게 처리합니다.

## 지원하는 AI 개발 도구

| 도구 | 설치되는 프로젝트 규칙 |
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

## 사용법

환경 프로파일러:

```bash
python LLM/environment.py
python LLM/environment.py .codingstandard/environment-profile.json
```

프로파일러는 실제 Python/runtime, OS, CPU, RAM, disk, GPU/accelerator, VRAM 및 CUDA/MPS/ROCm/DirectML capability를 측정하고 runtime configuration을 계산합니다.

### Memory Smoke Test

장시간 학습 전에 표준 Smoke Test를 실행합니다.

```bash
python LLM/memory_smoke_test.py --cpu --steps 2
```

가속기를 사용하려면 `--cpu`를 제거합니다. 테스트는 작은 synthetic model로 `load → forward → backward → optimizer step → checkpoint save/reload` 흐름을 검증하고 RAM/VRAM/runtime 정보를 기록합니다.

### Repository Validation

```bash
python scripts/validate.py
python scripts/check_i18n.py
python scripts/test_installers.py
```

## AI 작업 흐름

```text
AI 지침 자동 로딩
        ↓
Repository / project 구조 확인
        ↓
Python / kernel / IDE / runtime 확인
        ↓
CPU / RAM / disk / GPU / VRAM / accelerator 측정
        ↓
Environment Profile 생성
        ↓
Runtime Configuration 결정
        ↓
Memory Smoke Test
        ↓
Environment Lock
        ↓
불필요한 OS / device branch 제거
        ↓
구현 / 학습 / 추론
        ↓
Evaluation / Early Stopping / Checkpoint
        ↓
Ablation / 재현성 / 자원 사용량 기록
        ↓
최종 Clean Run
```

환경을 먼저 측정하고 실행 설정을 결정한 뒤 최소 workload로 검증하고 구현/실행을 진행합니다.

## 자동 AI 지침 로딩

공통 규칙은 다음을 기준으로 합니다.

```text
LLM/AGENT.md
LLM/SKILL.md
LLM/ENVIRONMENT.md
```

설치 스크립트가 `en` 또는 `ko`를 선택하여 각 AI 도구가 기대하는 표준 파일 이름으로 해당 언어 문서를 배치합니다.

## Skills

```text
LLM/skills/
├── environment/SKILL.md
├── training/SKILL.md
├── ablation/SKILL.md
├── notebook/SKILL.md
├── debugging/SKILL.md
└── release/SKILL.md
```

## ML / LLM 학습 원칙

- VRAM/RAM을 100%까지 채우지 않고 여유 자원을 남깁니다.
- 장시간 학습에는 validation metric과 Early Stopping을 적용합니다.
- best checkpoint를 저장하고 Resume 가능하도록 합니다.
- baseline과 Ablation variant를 명시적인 configuration matrix로 관리합니다.
- seed, model/dataset revision, metric, runtime, peak VRAM/RAM, environment profile을 기록합니다.
- OOM 발생 시 단계별 memory recovery를 적용하고 동일 설정을 무한 반복하지 않습니다.

## 저장소 구조

```text
codingStandard/
├── README.md
├── README.ko.md
├── VERSION
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── CONVENTIONS.md
├── .aider.conf.yml
├── .amazonq/
├── .cursor/
├── .windsurf/
├── .clinerules/
├── .continue/
├── .junie/
├── .github/
├── i18n/
├── LLM/
│   ├── AGENT.md
│   ├── SKILL.md
│   ├── ENVIRONMENT.md
│   ├── environment.py
│   ├── memory_smoke_test.py
│   ├── experiment.py
│   ├── config/
│   └── skills/
└── scripts/
    ├── install-coding-standard.ps1
    ├── install-coding-standard.sh
    ├── validate.py
    ├── check_i18n.py
    └── test_installers.py
```

## 문서

- 전체 개발 규칙: `LLM/AGENT.md`
- 실행 절차: `LLM/SKILL.md`
- 환경 최적화: `LLM/ENVIRONMENT.md`
- LLM/Jupyter 사용 가이드: `LLM/README.md`
- 환경 프로파일러: `LLM/environment.py`
- Memory Smoke Test: `LLM/memory_smoke_test.py`
- Experiment Metadata: `LLM/experiment.py`
- [영문 README](README.md)
