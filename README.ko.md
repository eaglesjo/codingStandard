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

충돌 처리 정책도 미리 지정할 수 있습니다.

```powershell
# 기존 파일이 있으면 질문
... -ConflictAction Ask

# 기존 내용 + codingStandard 관리 블록으로 병합
... -ConflictAction Merge

# 기존 파일 덮어쓰기
... -ConflictAction Overwrite

# 기존 파일 유지
... -ConflictAction Skip
```

### Linux / macOS

설치 중 언어를 선택:

```bash
git clone https://github.com/eaglesjo/codingStandard.git
bash ./codingStandard/scripts/install-coding-standard.sh .
```

영문:

```bash
bash ./codingStandard/scripts/install-coding-standard.sh . en
```

한글:

```bash
bash ./codingStandard/scripts/install-coding-standard.sh . ko
```

충돌 처리 정책은 세 번째 인자로 지정할 수 있습니다.

```bash
bash ./codingStandard/scripts/install-coding-standard.sh . en merge
bash ./codingStandard/scripts/install-coding-standard.sh . ko overwrite
bash ./codingStandard/scripts/install-coding-standard.sh . ko skip
```

### 기존 파일 충돌 처리

`Ask` 모드에서 대상 파일이 이미 존재하면 다음을 선택할 수 있습니다.

```text
M = Merge
O = Overwrite
S = Skip
A = Merge all remaining
W = Overwrite all remaining
K = Skip all remaining
```

Markdown/코드 파일의 Merge는 기존 내용을 유지하면서 `codingStandard`가 관리하는 명확한 블록을 추가합니다. 다시 설치하면 같은 관리 블록을 갱신하므로 중복으로 계속 붙지 않습니다.

`.aider.conf.yml`은 YAML 구조를 고려하여 기존 `read` 설정이 있으면 `CONVENTIONS.md`를 가능한 범위에서 안전하게 추가하고, 그렇지 않으면 관리 블록으로 추가합니다.

## 지원하는 AI 개발 도구

설치기는 공통 `AGENTS.md`와 함께 각 도구가 지원하는 프로젝트별 규칙 파일을 설치합니다.

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
| Aider | `CONVENTIONS.md` + `.aider.conf.yml` |

## 사용법

설치 후 대상 프로젝트 루트에서 환경 프로파일러를 실행합니다.

```bash
python LLM/environment.py
```

프로파일 저장:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

프로파일러는 현재 Python/runtime, OS, CPU, RAM, GPU, VRAM, CUDA/MPS, IDE/Jupyter/Colab 상태를 측정하고 workload에 맞는 보수적인 runtime configuration을 계산합니다.

특정 GPU, RAM, OS, IDE를 필수 전제조건으로 고정하지 않습니다. 실제 측정값과 workload를 기준으로 최종 설정을 결정합니다.

## AI 작업 흐름

```text
AI 지침 자동 로딩
        ↓
Repository / project 구조 확인
        ↓
Python / kernel / IDE / runtime 확인
        ↓
CPU / RAM / GPU / VRAM / accelerator 측정
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

## 자동 AI 지침 로딩

공통 규칙은 다음을 기준으로 합니다.

```text
LLM/AGENT.md
LLM/SKILL.md
LLM/ENVIRONMENT.md
```

설치 스크립트가 `en` 또는 `ko`를 선택하여 각 AI 도구가 기대하는 표준 파일 이름으로 해당 언어 문서를 배치합니다.

## 환경 최적화

`LLM/environment.py`가 실제 CPU/RAM/GPU/VRAM/가속기 및 runtime을 측정하고 실행 설정을 계산합니다. 권장값은 시작점이며 Memory Smoke Test 결과가 최종 결정 기준입니다.

## ML / LLM 학습 원칙

- VRAM/RAM을 100%까지 채우지 않고 여유 자원을 남깁니다.
- 장시간 학습에는 validation metric과 Early Stopping을 적용합니다.
- best checkpoint를 저장하고 Resume 가능하도록 합니다.
- baseline과 Ablation variant를 명시적인 configuration matrix로 관리합니다.
- variant 간 평가 조건을 통제합니다.
- seed, model/dataset revision, metric, runtime, peak VRAM/RAM, environment profile을 기록합니다.
- OOM 발생 시 단계별 memory recovery를 적용하고 동일 설정을 무한 반복하지 않습니다.

## 저장소 구조

```text
codingStandard/
├── README.md                    # English default
├── README.ko.md                 # 한국어 안내
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── CONVENTIONS.md
├── .aider.conf.yml
├── .cursor/rules/
├── .windsurf/rules/
├── .clinerules/
├── .continue/rules/
├── .junie/
├── .github/
├── i18n/
│   ├── README.md
│   └── ko/
├── LLM/
└── scripts/
    ├── install-coding-standard.ps1
    └── install-coding-standard.sh
```

## 문서

- 전체 개발 규칙: `LLM/AGENT.md`
- 실행 절차: `LLM/SKILL.md`
- 환경 최적화: `LLM/ENVIRONMENT.md`
- LLM/Jupyter 사용 가이드: `LLM/README.md`
- 환경 프로파일러: `LLM/environment.py`
- [영문 README](README.md)
